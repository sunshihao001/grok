import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from solana_meme_os.public_token_accounts import (
    RPC_URL, collect, decode_rpc, main, markdown, rpc_request, TOKEN_PROGRAMS,
)

MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
TOKEN_ACCOUNT = "So11111111111111111111111111111111111111112"
OWNER = "11111111111111111111111111111111"


def response(value, slot=200):
    return json.dumps({"jsonrpc": "2.0", "id": 1, "result": {
        "context": {"slot": slot}, "value": value
    }}).encode("utf-8")


def largest():
    return [{"address": TOKEN_ACCOUNT, "amount": "9999999999999999999",
             "decimals": 9, "uiAmountString": "9999999999.999999999"}]


def token_info(*, mint=MINT, owner=OWNER):
    return [{"owner": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
             "data": {"program": "spl-token", "parsed": {"info": {
                 "mint": mint, "owner": owner, "tokenAmount": {"amount": "9", "decimals": 9},
             }}}}]


class FakeResponse:
    status = 200
    def __init__(self, body):
        self.body = body
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return None
    def read(self, _limit):
        return self.body


class PublicTokenAccountTests(unittest.TestCase):
    def test_fixed_endpoint_jsonrpc_post_without_key(self):
        seen = []
        def fetch(req, timeout):
            seen.append((req.full_url, req.get_method(), req.data, req.headers, timeout))
            return FakeResponse(response([]))
        data = rpc_request("getTokenLargestAccounts", [MINT], opener=fetch)
        self.assertEqual(decode_rpc(data), (200, []))
        url, method, body, headers, timeout = seen[0]
        self.assertEqual(url, RPC_URL)
        self.assertEqual(method, "POST")  # JSON-RPC read-only method
        self.assertEqual(timeout, 12)
        self.assertEqual(json.loads(body)["method"], "getTokenLargestAccounts")
        self.assertNotIn("Authorization", headers)
        for forbidden in ("sendTransaction", "requestAirdrop", "getProgramAccounts"):
            with self.assertRaisesRegex(ValueError, "unsupported"):
                rpc_request(forbidden, [MINT], opener=fetch)

    def test_token_account_owner_candidate_not_wallet_identity(self):
        calls = []
        def fetch(method, params):
            calls.append((method, params))
            return response(largest(), 200) if method == "getTokenLargestAccounts" else response(token_info(), 201)
        report, raw = collect(MINT, request_fn=fetch, retrieved_at="2026-11-01T00:00:00Z")
        self.assertEqual(report["status"], "RPC_TOKEN_ACCOUNTS_AND_OWNER_HINTS")
        self.assertEqual(report["returned_token_accounts"], 1)
        self.assertEqual(report["rpc_slot_largest"], 200)
        self.assertEqual(report["rpc_slot_owner_lookup"], 201)
        self.assertFalse(report["same_slot_atomic_snapshot"])
        self.assertEqual(report["rows"][0]["amount_raw_at_first_slot"], "9999999999999999999")
        self.assertEqual(report["rows"][0]["owner_candidate"], OWNER)
        self.assertIn("NOT_BENEFICIAL_OWNER", report["rows"][0]["owner_status"])
        self.assertEqual(calls[1][1][1]["minContextSlot"], 200)
        self.assertEqual(calls[1][1][1]["encoding"], "jsonParsed")
        self.assertIn("largest-accounts-raw.json", raw)
        self.assertIn("account-owners-raw.json", raw)
        self.assertIn("不是前20个真实持有人", markdown(report))

    def test_owner_lookup_failure_keeps_largest_with_unknown(self):
        def fetch(method, params):
            if method == "getTokenLargestAccounts":
                return response(largest(), 100)
            raise OSError("connection refused")
        report, raw = collect(MINT, request_fn=fetch)
        self.assertEqual(report["status"], "PARTIAL_OWNER_LOOKUP_UNKNOWN")
        self.assertEqual(len(raw), 1)
        self.assertIsNone(report["rows"][0]["owner_candidate"])
        self.assertEqual(report["rows"][0]["owner_status"], "UNKNOWN_NOT_RESOLVED")
        self.assertIn("connection refused", report["owner_lookup_error"])

    def test_wrong_mint_or_non_token_program_does_not_infer_owner(self):
        for altered in (token_info(mint=TOKEN_ACCOUNT), [{"owner": OWNER, "data": {"program": "system"}}], [None]):
            def fetch(method, params):
                return response(largest()) if method == "getTokenLargestAccounts" else response(altered, 201)
            report, _ = collect(MINT, request_fn=fetch)
            self.assertIsNone(report["rows"][0]["owner_candidate"])
            self.assertTrue(report["rows"][0]["owner_status"].startswith("UNKNOWN"))

    def test_empty_sample_is_not_zero_supply(self):
        report, raw = collect(MINT, request_fn=lambda method, params: response([]))
        self.assertEqual(report["status"], "EMPTY_TOP_TOKEN_ACCOUNT_SAMPLE_COVERAGE_UNKNOWN")
        self.assertEqual(report["returned_token_accounts"], 0)
        self.assertIsNone(report["rpc_slot_owner_lookup"])
        self.assertEqual(list(raw), ["largest-accounts-raw.json"])

    def test_rpc_error_or_malformed_data_rejected(self):
        fail = json.dumps({"jsonrpc": "2.0", "error": {"code": -32005}, "id": 1}).encode()
        for data in (fail, b"not json", b"[]", response([{"address": TOKEN_ACCOUNT,"amount": 123, "decimals":9}]),
                     response(largest()*21)):
            with self.assertRaises(ValueError):
                collect(MINT, request_fn=lambda *_: data)
        with self.assertRaises(ValueError):
            collect("bad", request_fn=lambda *_: b"{}")

    def test_no_network_is_clear_error_and_no_fake_output(self):
        with tempfile.TemporaryDirectory() as t:
            with patch("solana_meme_os.public_token_accounts.rpc_request", side_effect=OSError("offline")):
                # collect default callable bound at import time; patch collect instead
                with patch("solana_meme_os.public_token_accounts.collect", side_effect=OSError("offline")):
                    with contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(main(["--mint", MINT, "--out-dir", str(Path(t)/"out")]), 3)
                self.assertFalse((Path(t)/"out").exists())

    def test_no_private_key_or_trading_methods(self):
        from solana_meme_os import public_token_accounts as m
        import inspect
        source = inspect.getsource(m)
        self.assertNotIn("sendTransaction", source.split("def rpc_request")[1].split("def decode_rpc")[0])
        self.assertEqual(len(TOKEN_PROGRAMS), 2)


if __name__ == "__main__":
    unittest.main()
