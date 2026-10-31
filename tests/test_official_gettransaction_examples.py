"""Official Solana Foundation published RPC examples; no network access during tests.

These are source-pinned examples, not independent RPC re-fetches.
A synthetic available_at is injected ONLY because docs omit actual observation time.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import copy
import json
from pathlib import Path
import unittest

from solana_meme_os.raw_tx_adapter import normalize, WSOL
from solana_meme_os.wallet_batch_monitor import analyze

ROOT = Path(__file__).resolve().parents[1]
DOC = json.loads((ROOT / "fixtures" / "official-solana-gettransaction-samples.json").read_text(encoding="utf-8"))
SOURCE_URL = (
    "https://github.com/solana-foundation/solana-com/blob/"
    "4cb392f61c2ab0f8953cc314378aaf8256b7699a/"
    "apps/docs/content/docs/en/rpc/http/gettransaction.mdx"
)
TARGET_MINT = "5kR7n7QJv85NrwwXdYWZ52qkRcyvXqKWDPNooYcfDV6e"
# This is deliberately synthetic; do not use this as an actual knowledge time.
FIXTURE_AVAILABLE = "2026-10-31T00:00:00Z"


def fixture_for(example):
    tx = copy.deepcopy(example["rpc"])
    moment = datetime.fromtimestamp(tx["blockTime"], timezone.utc)
    start = moment.replace(minute=moment.minute // 15 * 15, second=0, microsecond=0)
    end = start + timedelta(minutes=15)
    assert moment < end
    return {
        "schema_version": "m01.raw.v1",
        "mode": "fixture",
        "chain": "sol",
        "mint": TARGET_MINT,
        "quote_mint": WSOL,
        "quote_decimals": 9,
        "source": {"tool": "official_documentation_snapshot", "ref": SOURCE_URL},
        "coverage": {
            # Only an input declaration for this one transaction; not real Mint-wide completeness.
            "start": start.isoformat().replace("+00:00", "Z"),
            "end": end.isoformat().replace("+00:00", "Z"),
            "complete": True,
            "gaps": [],
        },
        "as_of": FIXTURE_AVAILABLE,
        "transactions": [{
            "signature": tx["transaction"]["signatures"][0],
            "source_ref": SOURCE_URL + "#" + example["id"],
            "available_at": FIXTURE_AVAILABLE,
            "rpc": tx,
        }],
    }


class OfficialPublishedTransactionExamples(unittest.TestCase):
    def test_source_signatures_and_slot_are_real_documentation_values(self):
        self.assertEqual(DOC["provenance"]["source_commit"],
                         "4cb392f61c2ab0f8953cc314378aaf8256b7699a")
        self.assertEqual(DOC["examples"][0]["rpc"]["slot"], 423108383)
        self.assertEqual(DOC["examples"][1]["rpc"]["slot"], 423118809)
        self.assertEqual(DOC["examples"][1]["rpc"]["transaction"]["signatures"][0],
                         DOC["examples"][2]["rpc"]["transaction"]["signatures"][0])
        self.assertIn("not independently refetched", DOC["provenance"]["source"])

    def test_official_legacy_one_sol_transfer_is_not_a_meme_swap(self):
        example = DOC["examples"][0]
        result = normalize(fixture_for(example))
        self.assertEqual(result["events"], [])
        self.assertEqual(len(result["adapter_audit"]["funding_events"]), 1)
        funding = result["adapter_audit"]["funding_events"][0]
        self.assertEqual(funding["lamports"], 1_000_000_000)
        self.assertEqual(funding["source_wallet"],
                         example["rpc"]["transaction"]["message"]["accountKeys"][0])
        self.assertEqual(funding["destination_wallet"],
                         example["rpc"]["transaction"]["message"]["accountKeys"][1])
        self.assertEqual(funding["fee_payer"], funding["source_wallet"])
        self.assertTrue(result["coverage"]["complete"])
        self.assertEqual(result["adapter_audit"]["decoded_target_transfers"], 0)
        self.assertEqual(analyze(result)["status"], "FIXTURE_RESEARCH_ONLY")

    def test_official_v0_ata_creation_json_not_transfer_or_swap(self):
        example = DOC["examples"][1]
        self.assertEqual(example["rpc"]["meta"]["postTokenBalances"][0]["uiTokenAmount"]["amount"], "0")
        result = normalize(fixture_for(example))
        self.assertEqual(result["events"], [])
        self.assertEqual(result["adapter_audit"]["funding_events"], [])
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["adapter_audit"]["decoded_target_transfers"], 0)
        self.assertTrue(result["adapter_audit"]["unresolved"])
        self.assertTrue(all(e["kind"] != "BUY" for e in result["events"]))

    def test_official_v0_ata_creation_jsonparsed_not_transfer_or_swap(self):
        example = DOC["examples"][2]
        result = normalize(fixture_for(example))
        self.assertEqual(result["events"], [])
        self.assertEqual(result["adapter_audit"]["funding_events"], [])
        self.assertFalse(result["coverage"]["complete"])
        self.assertEqual(result["adapter_audit"]["decoded_target_transfers"], 0)
        self.assertEqual(analyze(result)["timeframes"]["1m"]["windows"][0]["data_status"],
                         "INCOMPLETE")

    def test_documented_token_ata_creation_is_not_mint_purchase_from_rent(self):
        example = DOC["examples"][1]
        rpc = example["rpc"]
        self.assertEqual(rpc["transaction"]["message"]["accountKeys"][4],
                         "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")
        self.assertEqual(len(rpc["meta"]["innerInstructions"][0]["instructions"]), 4)
        self.assertEqual(rpc["meta"]["preTokenBalances"], [])
        self.assertEqual(rpc["meta"]["postTokenBalances"][0]["owner"],
                         "47eFuHR9ste9kopiJ9eRxcwahmE62JovbKe5r7AjANut")
        self.assertEqual(rpc["meta"]["postTokenBalances"][0]["uiTokenAmount"]["amount"], "0")
        result = normalize(fixture_for(example))
        self.assertEqual(result["adapter_audit"]["decoded_target_transfers"], 0)
        self.assertFalse(result["coverage"]["complete"])


    def test_missing_rpc_meta_err_is_unknown_not_successful_funding(self):
        item = fixture_for(DOC["examples"][0])
        del item["transactions"][0]["rpc"]["meta"]["err"]
        r = normalize(item)
        self.assertFalse(r["coverage"]["complete"])
        self.assertEqual(r["events"], [])
        self.assertEqual(r["adapter_audit"]["funding_events"], [])
        self.assertIn("TRANSACTION_STATUS_UNKNOWN",
                      [x["reason"] for x in r["adapter_audit"]["unresolved"]])

    def test_evidence_after_as_of_is_not_emitted_even_as_funding(self):
        item = fixture_for(DOC["examples"][0])
        item["as_of"] = "2026-10-31T00:00:00Z"
        item["transactions"][0]["available_at"] = "2026-10-31T00:00:10Z"
        r = normalize(item)
        self.assertFalse(r["coverage"]["complete"])
        self.assertEqual(r["events"], [])
        self.assertEqual(r["adapter_audit"]["funding_events"], [])
        self.assertIn("EVIDENCE_ARRIVED_AFTER_AS_OF",
                      [x["reason"] for x in r["adapter_audit"]["unresolved"]])


if __name__ == "__main__":
    unittest.main()
