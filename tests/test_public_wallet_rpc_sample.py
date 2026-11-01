"""No network is used by these tests."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from solana_meme_os import public_wallet_rpc_sample as probe
from solana_meme_os.public_token_accounts import RPC_URL, rpc_request

WALLET = "9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y"
SIGNATURE = "3" * 88

def enc(result):
    return json.dumps({"jsonrpc": "2.0", "result": result, "id": 1}).encode()

def req(method, params):
    if method == "getSignaturesForAddress":
        return enc([{"signature": SIGNATURE, "slot": 777, "blockTime": 1780000000,
                     "err": None, "confirmationStatus": "finalized"}])
    if method == "getTransaction":
        return enc({"slot": 777, "blockTime": 1780000000, "transaction": {},
                    "meta": {"err": None}})
    raise AssertionError(method)

class WalletProbeTests(unittest.TestCase):
    def test_bounded_signature_and_single_raw_transaction(self):
        calls = []
        def mock(method, params):
            calls.append((method, params))
            return req(method, params)
        report, raw = probe.sample(WALLET, request_fn=mock,
                                   retrieved_at="2026-11-01T00:00:00Z")
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][1][1]["limit"], 2)
        self.assertEqual(calls[1][1][0], SIGNATURE)
        self.assertEqual(len(report["rows"]), 1)
        self.assertEqual(report["rows"][0]["event_type"], "UNKNOWN_NOT_DECODED")
        self.assertEqual(report["transaction"]["status"],
                         "RAW_TRANSACTION_AVAILABLE_NOT_ECONOMICALLY_DECODED")
        self.assertEqual(report["source"]["url"], RPC_URL)
        self.assertFalse(report["coverage"]["continuous_monitoring"])
        self.assertFalse(report["grok_bot_called"])
        for name, data in raw.items():
            self.assertEqual(report["raw_input_sha256"][name],
                             hashlib.sha256(data).hexdigest())

    def test_empty_page_is_unknown_coverage_not_no_wallet(self):
        report, raws = probe.sample(WALLET, request_fn=lambda *_: enc([]))
        self.assertEqual(report["rows"], [])
        self.assertFalse(report["coverage"]["full_wallet_history"])
        self.assertEqual(len(raws), 1)
        self.assertEqual(report["transaction"]["status"],
                         "NOT_AVAILABLE_NO_SIGNATURES")

    def test_tx_error_does_not_claim_success_or_trade(self):
        def fail(method, params):
            if method == "getTransaction":
                raise OSError("HTTP 429")
            return req(method, params)
        report, raw = probe.sample(WALLET, request_fn=fail)
        self.assertEqual(report["transaction"]["status"],
                         "RAW_TRANSACTION_UNAVAILABLE")
        self.assertIn("429", report["transaction"]["error"])
        self.assertEqual(len(raw), 1)
        self.assertEqual(report["coverage"]["swap_buy_sell_classification"],
                         "NOT_PERFORMED")

    def test_inconsistent_slot_rejected_as_partial(self):
        def mismatch(method, params):
            if method == "getTransaction":
                return enc({"slot": 778})
            return req(method, params)
        report, _ = probe.sample(WALLET, request_fn=mismatch)
        self.assertEqual(report["transaction"]["status"],
                         "RAW_TRANSACTION_UNAVAILABLE")

    def test_bad_wallet_or_limit_rejected_without_requests(self):
        for wallet,limit in [("bad",1), (WALLET,4), (WALLET,0),
                             (WALLET,True)]:
            with self.assertRaises(ValueError):
                probe.sample(wallet, limit=limit, request_fn=lambda *_: 1)

    def test_malformed_or_duplicate_signature_page_rejected(self):
        for raw in [
            enc([{"signature":SIGNATURE,"slot":4}]*2),
            enc([{"signature":"bad","slot":4}]),
            enc([{"signature":SIGNATURE,"slot":-1}]),
            b"{",
            enc("bad response"),
        ]:
            with self.assertRaises(ValueError):
                probe.sample(WALLET, request_fn=lambda *_: raw)

    def test_no_signing_or_paid_method_via_transport(self):
        for forbidden in ("sendTransaction","requestAirdrop","getProgramAccounts"):
            with self.assertRaises(ValueError):
                rpc_request(forbidden,[WALLET],opener=lambda *_: None)

    def test_cli_failure_returns_no_false_wallet_report(self):
        with tempfile.TemporaryDirectory() as t:
            with patch("solana_meme_os.public_wallet_rpc_sample.sample", side_effect=OSError("429")):
                self.assertEqual(probe.main(["--wallet",WALLET,"--out-dir",t]), 3)
            self.assertFalse((Path(t)/"report.json").exists())


    def test_real_mainnet_failed_cpi_reconstructed_evidence_regression(self):
        # Reconstructed minimal fields from GitHub Action 41314447575;
        # full untouched RPC data stays in artifact #13086538862.
        target = "9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y"
        payer = "7Ej1sc9rwXZdxe9ZGcvCf8QrryFyjR6wj3emKnJXEdY9"
        tx = {"slot": 464112229, "version": 0,
              "transaction": {"message": {"accountKeys": [
                  {"pubkey": payer, "signer": True},
                  {"pubkey": target, "signer": False}
              ]}},
              "meta": {"err": {"InstructionError": [2, {"Custom": 1}]},
                       "fee": 7000,
                       "preBalances": [1242995, 22957220],
                       "postBalances": [1235995, 22957220],
                       "preTokenBalances": [],
                       "postTokenBalances": []}}
        observed = probe.execution_facts(tx, target)
        self.assertEqual(observed["status"], "FAILED_ROLLED_BACK")
        self.assertEqual(observed["fee_lamports"], 7000)
        self.assertTrue(observed["wallet_in_transaction_accounts"])
        self.assertFalse(observed["wallet_is_signer"])
        self.assertFalse(observed["wallet_is_fee_payer"])
        self.assertEqual(observed["sol_account_deltas_from_meta"],
                         [{"account": payer, "delta_lamports": -7000}])
        self.assertEqual(observed["token_balance_comparison"], "UNCHANGED_REPORTED_TOKEN_BALANCES")
        self.assertIs(observed["successful_swap"], False)
        self.assertIs(observed["transaction_committed_program_movements"], False)

    def test_success_does_not_imply_buy_or_wallet_controller(self):
        target = WALLET
        tx = {"transaction": {"message": {"accountKeys": [
                  {"pubkey": WALLET, "signer": True},
                  {"pubkey": "11111111111111111111111111111111", "signer": False}]}},
              "meta": {"err": None, "fee": 5000,
                       "preBalances": [100000, 10000], "postBalances": [85000, 20000],
                       "preTokenBalances": [], "postTokenBalances": []}}
        observed = probe.execution_facts(tx, target)
        self.assertEqual(observed["status"], "SUCCESSFUL_EXECUTION_UNCLASSIFIED")
        self.assertEqual(observed["successful_swap"], "NOT_ASSESSED")
        self.assertTrue(observed["wallet_is_fee_payer"])
        self.assertEqual(len(observed["sol_account_deltas_from_meta"]), 2)

    def test_incomplete_meta_never_invents_zero_movement(self):
        self.assertEqual(probe.execution_facts({"meta": {"err": None}}, WALLET)
                         ["status"], "UNKNOWN_INCOMPLETE_EXECUTION_META")
        self.assertEqual(probe.execution_facts({
            "transaction": {"message": {"accountKeys": [{"pubkey": WALLET, "signer": True}]}},
            "meta": {"err": None, "fee": 5000,
                     "preBalances": [1000], "postBalances": []}}, WALLET)
                         ["status"], "UNKNOWN_INCONSISTENT_EXECUTION_BALANCES")

if __name__ == "__main__":
    unittest.main()
