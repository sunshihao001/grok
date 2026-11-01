"""Read-only handoff contract: offline tests, not live wallet/Grok tests."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from solana_meme_os.vendor_event_handoff import triage, write_outputs

MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
OWNER = "11111111111111111111111111111111"
ACCOUNT = "So11111111111111111111111111111111111111112"

def raw(value):
    return json.dumps(value, sort_keys=True).encode()

def fixture():
    rug = {
        "mint": MINT,
        "topHolders": [{"address": ACCOUNT, "owner": OWNER, "pct": 12.2}],
        "knownAccounts": {OWNER: {"type": "AMM"}},
        "markets": [{"pubkey": OWNER, "liquidityA": ACCOUNT,
                     "liquidityAAccount": {"mint": MINT, "owner": OWNER}}],
        "risks": [{"name": "Copycat token", "score": 2000, "level": "warn"}],
    }
    dex = [{"chainId": "solana", "pairAddress": OWNER,
            "baseToken": {"address": MINT}}]
    report = {
        "schema_version": "grok.mint_v01_combined.v0",
        "mint": MINT,
        "status": "OK",
        "no_trading": True,
        "processed_at": "2026-11-01T03:26:30+00:00",
        "source_status": {
            "rugcheck_public_report": "RUGCHECK_CACHED_VENDOR_REPORT_NOT_INDEPENDLY_VERIFIED",
            "dex_public_pairs": "PUBLIC_PROVIDER_PAIR_SNAPSHOT_UNVERIFIED_ONCHAIN",
        },
        "rugcheck_public": {
            "mint": MINT,
            "source": {"input_sha256": hashlib.sha256(raw(rug)).hexdigest()},
        },
        "dex_public": {
            "mint": MINT,
            "raw_input_sha256": hashlib.sha256(raw(dex)).hexdigest(),
            "returned_pair_count": 1,
        },
    }
    # Match the actual report's exact status enum.
    report["source_status"]["rugcheck_public_report"] = (
        "RUGCHECK_CACHED_VENDOR_REPORT_NOT_INDEPENDENTLY_VERIFIED")
    return report, rug, dex

def evaluate(report=None, rug=None, dex=None):
    a, b, c = fixture()
    return triage(raw(a if report is None else report),
                  raw(b if rug is None else rug),
                  raw(c if dex is None else dex))

class VendorTriageContract(unittest.TestCase):
    def test_vendor_label_is_not_a_verified_chain_signal(self):
        item = evaluate()
        self.assertEqual(len(item["investigations"]), 1)
        claim = item["investigations"][0]
        self.assertEqual(claim["vendor_label"], "Copycat token")
        self.assertIsNone(claim["chain_transaction_signature"])
        self.assertEqual(item["coverage"]["wallet_transactions"], "NOT_OBSERVED")
        self.assertEqual(item["model_calls"], 0)
        self.assertIn("NO_BOT_INVOKED", item["disposition"])

    def test_pool_vault_does_not_trigger_whale_claim(self):
        item = evaluate()
        self.assertEqual(item["suppressed_candidates"][0]["outcome"],
                         "POOL_INFRASTRUCTURE_EXPLANATION_SUPPRESSES_WHALE_ALERT")
        a, b, c = fixture()
        b["markets"][0]["liquidityAAccount"]["owner"] = ACCOUNT
        a["rugcheck_public"]["source"]["input_sha256"] = hashlib.sha256(raw(b)).hexdigest()
        changed = evaluate(report=a, rug=b)
        self.assertIn("INSUFFICIENT_IDENTITY_EVIDENCE",
                      changed["suppressed_candidates"][0]["outcome"])

    def test_source_hash_tampering_rejected(self):
        a, b, c = fixture()
        b["risks"][0]["name"] = "made up"
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            evaluate(rug=b)
        c[0]["pairAddress"] = ACCOUNT
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            evaluate(dex=c)

    def test_wrong_mint_or_chain_rejected(self):
        a, b, c = fixture()
        a["mint"] = OWNER
        with self.assertRaisesRegex(ValueError, "mint mismatch"):
            evaluate(report=a)
        c[0]["chainId"] = "ethereum"
        a["dex_public"]["raw_input_sha256"] = hashlib.sha256(raw(c)).hexdigest()
        with self.assertRaisesRegex(ValueError, "wrong chain"):
            evaluate(report=a, dex=c)

    def test_no_signal_creates_no_bot_task(self):
        a, b, c = fixture()
        b["risks"] = []
        b["topHolders"][0]["pct"] = 0.1
        a["rugcheck_public"]["source"]["input_sha256"] = hashlib.sha256(raw(b)).hexdigest()
        p = evaluate(report=a, rug=b)
        self.assertFalse(p["investigations"])
        with tempfile.TemporaryDirectory() as root:
            write_outputs(Path(root), p)
            self.assertFalse(list(Path(root).glob("grok_task_*.md")))

    def test_task_file_reports_not_executed(self):
        item = evaluate()
        with tempfile.TemporaryDirectory() as root:
            write_outputs(Path(root), item)
            tasks = list(Path(root).glob("grok_task_*.md"))
            self.assertEqual(len(tasks), 1)
            self.assertIn("Grok 主 Bot", tasks[0].read_text())
            self.assertIn("NOT_EXECUTED",
                          (Path(root)/"provisional_monitor_opinion.md").read_text())
            self.assertEqual(json.loads((Path(root)/"evidence.json").read_text())["model_calls"], 0)

if __name__ == "__main__":
    unittest.main()
