"""Adversarial offline fixtures: all identifiers and transactions are synthetic."""
from __future__ import annotations

import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.raw_tx_adapter import normalize, TOKEN, TOKEN_2022, SYSTEM, WSOL
from solana_meme_os.wallet_batch_monitor import analyze

ROOT = Path(__file__).resolve().parents[1]
T0 = datetime(2026, 10, 31, 0, 0, tzinfo=timezone.utc)
MINT = "M" * 44
OWNER = "A" * 44
OTHER = "B" * 44
FEEPAYER = "P" * 44
AUTHORITY = "D" * 44
SOURCE_TOKEN = "T" * 44
DEST_TOKEN = "U" * 44
ROUTER = "R" * 44


def ts(seconds: int) -> str:
    return (T0 + timedelta(seconds=seconds)).isoformat().replace("+00:00", "Z")


def b58(data: bytes) -> str:
    alpha = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(data, "big")
    chars = ""
    while n:
        n, i = divmod(n, 58)
        chars = alpha[i] + chars
    return "1" * (len(data) - len(data.lstrip(b"\x00"))) + (chars or "")


def initial():
    return {"schema_version": "m01.raw.v1", "chain": "sol", "mode": "fixture", "mint": MINT,
            "quote_mint": WSOL, "quote_decimals": 9,
            "coverage": {"start": ts(0), "end": ts(900), "complete": True, "gaps": []},
            "as_of": ts(1000), "source": {"tool": "synthetic_rpc_fixture", "ref": "fixture://raw-adapter"},
            "transactions": []}


def token_balances(src=SOURCE_TOKEN, dest=DEST_TOKEN, mint=MINT, owner=OWNER, recipient=OTHER, src_idx=2, dst_idx=3):
    def bal(idx, account_owner):
        return {"accountIndex": idx, "mint": mint, "owner": account_owner,
                "programId": TOKEN, "uiTokenAmount": {"amount": "1000", "decimals": 6}}
    return {"preTokenBalances": [bal(src_idx, owner), bal(dst_idx, recipient)],
            "postTokenBalances": [bal(src_idx, owner), bal(dst_idx, recipient)]}


def record(ix=None, sig="fixture-sig-1", second=1, program=TOKEN, meta_overrides=None):
    keys = [{"pubkey": FEEPAYER, "signer": True, "writable": True, "source": "transaction"},
            {"pubkey": AUTHORITY, "signer": True, "writable": True, "source": "transaction"},
            {"pubkey": SOURCE_TOKEN, "signer": False, "writable": True, "source": "transaction"},
            {"pubkey": DEST_TOKEN, "signer": False, "writable": True, "source": "transaction"},
            {"pubkey": program, "signer": False, "writable": False, "source": "transaction"}]
    if ix is None:
        ix = {"programId": program, "program": "spl-token", "parsed": {"type": "transferChecked",
              "info": {"source": SOURCE_TOKEN, "destination": DEST_TOKEN, "mint": MINT,
                       "authority": AUTHORITY, "tokenAmount": {"amount": "250", "decimals": 6}}}}
    meta = {**token_balances(), "err": None, "innerInstructions": [], "fee": 5000}
    if meta_overrides:
        meta.update(meta_overrides)
    return {"signature": sig, "source_ref": f"fixture://{sig}", "available_at": ts(second + 2),
            "rpc": {"slot": 90000 + second, "blockTime": int(T0.timestamp()) + second,
                    "version": 0,
                    "transaction": {"signatures": [sig], "message": {"accountKeys": keys,
                                                                    "instructions": [ix]}},
                    "meta": meta}}


class RawAdapterTests(unittest.TestCase):
    def test_parsed_direct_token_transfer_only(self):
        p = initial(); p["transactions"] = [record()]
        r = normalize(p)
        self.assertEqual(r["schema_version"], "m01.v1")
        self.assertEqual(len(r["events"]), 1)
        e = r["events"][0]
        self.assertEqual(e["kind"], "TRANSFER")
        self.assertEqual(e["wallet_owner"], OWNER)
        self.assertEqual(e["authority"], AUTHORITY)
        self.assertEqual(e["fee_payer"], FEEPAYER)
        self.assertEqual(e["destination_owner"], OTHER)
        self.assertEqual(e["transfer_amount_raw"], 250)
        self.assertEqual(analyze(r)["timeframes"]["1m"]["windows"][0]["active_wallet_count"], 1)
        self.assertEqual(analyze(r)["timeframes"]["1m"]["windows"][0]["buy_quote_raw"], 0)

    def test_transfer_does_not_become_buy_when_token_balance_changes(self):
        p = initial(); p["transactions"] = [record()]
        self.assertFalse(any(e["kind"] in ("BUY", "SELL") for e in normalize(p)["events"]))

    def test_failed_transaction_never_produces_successful_transfer(self):
        p = initial(); p["transactions"] = [record(meta_overrides={"err": {"InstructionError": [0, "Custom"]}})]
        r = normalize(p)
        self.assertEqual(r["events"], [])
        self.assertIn("FAILED_TRANSACTION", r["adapter_audit"]["unsupported"][0]["reason"])

    def test_token_owner_missing_unknown_not_fee_payer_or_authority(self):
        p = initial(); t = record()
        for b in t["rpc"]["meta"]["preTokenBalances"] + t["rpc"]["meta"]["postTokenBalances"]:
            if b["accountIndex"] == 2: b.pop("owner")
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(r["events"], [])
        self.assertFalse(r["coverage"]["complete"])
        self.assertIn("TOKEN_SOURCE_OWNER_UNKNOWN", [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_inner_cpi_transfer_is_unknown_not_swap(self):
        p = initial(); t = record(ix={"programId": ROUTER, "accounts": [], "data": "1"})
        t["rpc"]["meta"]["innerInstructions"] = [{"index": 0, "instructions": [
            {"programId": TOKEN, "parsed": {"type": "transferChecked", "info":
              {"source": SOURCE_TOKEN, "destination": DEST_TOKEN, "mint": MINT,
               "authority": AUTHORITY, "tokenAmount": {"amount": "500", "decimals": 6}}}}
        ]}]
        p["transactions"] = [t]
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertFalse(r["events"])
        self.assertIn("CPI_TOKEN_MOVEMENT_NOT_SWAP", [x["reason"] for x in r["adapter_audit"]["unresolved"]])
        self.assertEqual(analyze(r)["timeframes"]["1m"]["windows"][0]["data_status"], "INCOMPLETE")

    def test_system_cpi_not_a_user_funding_event(self):
        p = initial()
        t = record(ix={"programId": ROUTER, "data": "1", "accounts": []},
                   meta_overrides={"preTokenBalances": [], "postTokenBalances": []})
        t["rpc"]["meta"]["innerInstructions"] = [{"index": 0, "instructions": [
            {"programId": SYSTEM, "parsed": {"type": "transfer", "info":
                {"source": FEEPAYER, "destination": OTHER, "lamports": 888}}}]}]
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(r["adapter_audit"]["funding_events"], [])
        self.assertFalse(r["coverage"]["complete"])
        self.assertIn("CPI_SOL_MOVEMENT_NOT_USER_FUNDING", [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_admin_token_instruction_is_not_transfer_or_swap(self):
        p = initial(); t = record()
        t["rpc"]["transaction"]["message"]["instructions"][0]["parsed"] = {
            "type": "initializeAccount3", "info": {"mint": MINT, "account": SOURCE_TOKEN, "owner": OWNER}}
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(r["events"], [])
        self.assertEqual(r["adapter_audit"]["funding_events"], [])
        # Balance metadata alone is not an economic Swap event.
        self.assertFalse(r["coverage"]["complete"])

    def test_unsupported_tx_version_fails_closed(self):
        p = initial(); t = record(); t["rpc"]["version"] = 4
        p["transactions"] = [t]
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertEqual(r["events"], [])
        self.assertIn("UNSUPPORTED_TX_VERSION", [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_current_v1_format_fails_closed_until_decoder_supports_it(self):
        # Solana transaction v1 is supported by the chain, not by this adapter.
        # An unsupported version must NEVER be interpreted as an empty activity window.
        p = initial()
        t = record()
        t["rpc"]["version"] = 1
        p["transactions"] = [t]
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertEqual(r["events"], [])
        self.assertIn("UNSUPPORTED_TX_VERSION",
                      [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_token_2022_transferchecked_supported_but_fee_extension_not(self):
        self.assertEqual(TOKEN_2022, "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb")
        p = initial(); t = record(program=TOKEN_2022)
        t["rpc"]["meta"]["preTokenBalances"][0]["programId"] = TOKEN_2022
        p["transactions"] = [t]
        self.assertEqual(len(normalize(p)["events"]), 1)
        t["rpc"]["transaction"]["message"]["instructions"][0]["parsed"]["type"] = "transferCheckedWithFee"
        r = normalize(p)
        self.assertEqual(r["events"], [])
        self.assertFalse(r["coverage"]["complete"])

    def test_sol_funding_separate_from_mint_activity(self):
        p = initial(); t = record(ix={"programId": SYSTEM, "parsed": {"type": "transfer", "info":
            {"source": FEEPAYER, "destination": OTHER, "lamports": 1000000}}},program=SYSTEM,
            meta_overrides={"preTokenBalances": [], "postTokenBalances": []})
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(r["events"], [])
        self.assertEqual(r["adapter_audit"]["funding_events"][0]["lamports"], 1000000)
        self.assertEqual(r["adapter_audit"]["funding_events"][0]["kind"], "SOL_TRANSFER")

    def test_compiled_versioned_lookup_addresses_correctly_resolved(self):
        p = initial()
        data = bytes([3]) + (777).to_bytes(8, "little")
        t = record(ix={"programIdIndex": 2, "accounts": [3, 4, 1], "data": b58(data)})
        t["rpc"]["transaction"]["message"] = {
          "header": {"numRequiredSignatures": 2},
          "accountKeys": [FEEPAYER, AUTHORITY, TOKEN],
          "addressTableLookups": [{"accountKey": ROUTER, "writableIndexes": [0, 1], "readonlyIndexes": []}],
          "instructions": [{"programIdIndex": 2, "accounts": [3, 4, 1], "data": b58(data)}]}
        t["rpc"]["meta"]["loadedAddresses"] = {"writable": [SOURCE_TOKEN, DEST_TOKEN], "readonly": []}
        t["rpc"]["meta"].update(token_balances(src_idx=3,dst_idx=4))
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(r["events"][0]["transfer_amount_raw"], 777)
        self.assertEqual(r["events"][0]["wallet_owner"], OWNER)
        t["rpc"]["meta"].pop("loadedAddresses")
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertEqual(r["events"], [])
        self.assertIn("ACCOUNT_KEYS_UNRESOLVED", [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_compiled_direct_system_sol_transfer(self):
        p = initial()
        t = record(program=SYSTEM,meta_overrides={"preTokenBalances": [], "postTokenBalances": []})
        t["rpc"]["transaction"]["message"] = {"header": {"numRequiredSignatures": 1},
              "accountKeys": [FEEPAYER, OTHER, SYSTEM],
              "instructions": [{"programIdIndex": 2, "accounts": [0, 1],
                                 "data": b58(b"\x02\x00\x00\x00" + (12345).to_bytes(8, "little"))}]}
        p["transactions"] = [t]
        self.assertEqual(normalize(p)["adapter_audit"]["funding_events"][0]["lamports"], 12345)

    def test_repeated_independent_instructions_not_deduped(self):
        p = initial(); t = record()
        ix = t["rpc"]["transaction"]["message"]["instructions"][0]
        t["rpc"]["transaction"]["message"]["instructions"].append(copy.deepcopy(ix))
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(len(r["events"]), 2)
        self.assertNotEqual(r["events"][0]["event_id"], r["events"][1]["event_id"])

    def test_rpc_signature_mismatch_rejected(self):
        p = initial(); t = record()
        t["rpc"]["transaction"]["signatures"] = ["another-signature"]
        p["transactions"] = [t]
        with self.assertRaisesRegex(ValueError, "signature mismatch"):
            normalize(p)

    def test_missing_block_time_downgrades_cover_without_fake_timestamp(self):
        p = initial(); t = record(); t["rpc"]["blockTime"] = None; p["transactions"] = [t]
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertFalse(r["events"])
        self.assertEqual(r["adapter_audit"]["unresolved"][0]["reason"], "BLOCK_TIME_UNKNOWN")

    def test_missing_cpi_trace_downgrades_complete_even_with_token_balance(self):
        p = initial(); t = record(); t["rpc"]["meta"]["innerInstructions"] = None; p["transactions"] = [t]
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertIn("INNER_TRACE_UNAVAILABLE", [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_post_balance_owner_conflict_downgrades(self):
        p = initial(); t = record()
        t["rpc"]["meta"]["postTokenBalances"][0]["owner"] = OTHER
        p["transactions"] = [t]
        self.assertIn("TOKEN_OWNER_CONFLICT", [x["reason"] for x in normalize(p)["adapter_audit"]["unresolved"]])

    def test_late_available_evidence_downgrades_complete(self):
        p = initial(); t = record(); t["available_at"] = ts(1100); p["transactions"] = [t]
        r = normalize(p)
        self.assertFalse(r["coverage"]["complete"])
        self.assertIn("EVIDENCE_ARRIVED_AFTER_AS_OF", [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_duplicate_signature_envelopes_are_rejected(self):
        p = initial(); t = record(); p["transactions"] = [t, copy.deepcopy(t)]
        with self.assertRaisesRegex(ValueError, "duplicate signature"):
            normalize(p)

    def test_invalid_b58_instruction_fails_closed(self):
        p = initial(); t = record()
        t["rpc"]["transaction"]["message"] = {"header": {"numRequiredSignatures": 1},
                "accountKeys": [FEEPAYER,TOKEN,SOURCE_TOKEN,DEST_TOKEN,AUTHORITY],
                "instructions": [{"programIdIndex": 1, "accounts": [2,3,4],"data": "0INVALID"}]}
        t["rpc"]["meta"].update(token_balances(src_idx=2,dst_idx=3))
        p["transactions"] = [t]
        r = normalize(p)
        self.assertEqual(r["events"], [])
        self.assertFalse(r["coverage"]["complete"])

    def test_unknown_dex_balance_activity_does_not_become_swap(self):
        p = initial(); t = record(ix={"programId": ROUTER, "accounts": [], "data":"1"}); p["transactions"]=[t]
        r=normalize(p)
        self.assertEqual(r["events"],[])
        self.assertIn("TARGET_MINT_ECONOMIC_ACTION_UNCLASSIFIED",[x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_fixture_only_and_no_network(self):
        p=initial();p["mode"]="live"
        with self.assertRaisesRegex(ValueError,"fixture-only"):
            normalize(p)

    def test_token_program_plain_transfer_and_same_account_owner_correct(self):
        p=initial();t=record()
        t["rpc"]["transaction"]["message"]["instructions"][0]["parsed"]={
            "type":"transfer","info":{"source":SOURCE_TOKEN,"destination":DEST_TOKEN,
                                     "authority":AUTHORITY,"amount":"1999"}}
        p["transactions"]=[t]
        r=normalize(p)
        self.assertEqual(r["events"][0]["transfer_amount_raw"],1999)

    def test_cli_round_trip_with_repository_fixture(self):
        fixture_path=ROOT/"fixtures"/"raw-solana-transfers-demo.json"
        with TemporaryDirectory() as t:
            out=Path(t)/"normalized.json"
            cli=subprocess.run([sys.executable,"-m","solana_meme_os.raw_tx_adapter","--input",str(fixture_path),
                                "--output",str(out)],capture_output=True,text=True,env={"PYTHONPATH":str(ROOT/"src")})
            self.assertEqual(cli.returncode,0,cli.stderr)
            r=json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(r["schema_version"],"m01.v1")
            self.assertGreater(len(r["events"]),0)
            self.assertTrue(r["adapter_audit"]["no_trading"])


if __name__ == "__main__":
    unittest.main()