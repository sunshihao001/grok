"""Grok handoff smoke test: existing Mint collector -> verified evidence outbox.

All provider responses below are synthetic. This does not test Grok cloud
execution, real Solana transactions or continuously running monitoring.
"""
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from solana_meme_os import mint_v01, vendor_event_handoff

MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
POOL = "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB"
TOKEN_ACCOUNT = "BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i"


def payloads():
    dex = json.dumps([{
        "chainId": "solana", "pairAddress": POOL, "dexId": "pumpswap",
        "baseToken": {"address": MINT, "symbol": "TEST"},
        "quoteToken": {"address": "So11111111111111111111111111111111111111112",
                       "symbol": "SOL"},
    }]).encode()
    rug = json.dumps({
        "mint": MINT, "creator": "11111111111111111111111111111111",
        "topHolders": [{"address": TOKEN_ACCOUNT, "owner": POOL, "pct": 5.88}],
        "knownAccounts": {POOL: {"type": "AMM", "name": "Pool"}},
        "markets": [{"pubkey": POOL, "liquidityA": TOKEN_ACCOUNT,
                     "liquidityAAccount": {"mint": MINT, "owner": POOL}}],
        "risks": [{"name": "Vendor warning", "level": "warn", "score": 120}],
    }).encode()
    return dex, rug


def collect_mocked(mint_dir, *, dex_ok=True):
    dex, rug = payloads()
    with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
               return_value=(dex, "https://api.dexscreener.com/token-pairs/v1/solana/" + MINT)
               if dex_ok else None) as pairs:
        if not dex_ok:
            pairs.side_effect = OSError("DEX provider unavailable")
        with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                   return_value=rug):
            with contextlib.redirect_stdout(io.StringIO()):
                status = mint_v01.main([MINT, "--rugcheck",
                                        "--out-dir", str(mint_dir)])
    return status


def run_handoff(mint_dir, handoff_dir):
    with contextlib.redirect_stdout(io.StringIO()):
        return vendor_event_handoff.main([
            "--report", str(mint_dir / "report.json"),
            "--rugcheck-raw", str(mint_dir / "rugcheck-provider-raw.json"),
            "--dex-raw", str(mint_dir / "dex-provider-raw.json"),
            "--out-dir", str(handoff_dir),
        ])


class GrokMintEvidencePipeline(unittest.TestCase):
    def test_two_existing_commands_produce_verifiable_grok_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            mint_dir = Path(tmp) / "mint"
            outbox = Path(tmp) / "grok-outbox"
            self.assertEqual(collect_mocked(mint_dir), 0)
            self.assertEqual(run_handoff(mint_dir, outbox), 0)

            report = json.loads((mint_dir / "report.json").read_text())
            evidence = json.loads((outbox / "evidence.json").read_text())
            dex, rug = payloads()
            self.assertEqual(report["mint"], MINT)
            self.assertTrue(report["no_trading"])
            self.assertEqual((mint_dir / "dex-provider-raw.json").read_bytes(), dex)
            self.assertEqual((mint_dir / "rugcheck-provider-raw.json").read_bytes(), rug)
            self.assertEqual(evidence["source_proofs"]["dex_sha256"],
                             hashlib.sha256(dex).hexdigest())
            self.assertEqual(evidence["source_proofs"]["rugcheck_sha256"],
                             hashlib.sha256(rug).hexdigest())
            self.assertEqual(evidence["source_proofs"]["report_sha256"],
                             hashlib.sha256((mint_dir / "report.json").read_bytes()).hexdigest())
            self.assertEqual(evidence["disposition"],
                             "PREPARE_GROK_TASKS_ONLY_NO_BOT_INVOKED")
            self.assertEqual(evidence["model_calls"], 0)
            self.assertEqual(evidence["auto_payments"], 0)
            self.assertEqual(evidence["coverage"]["wallet_transactions"], "NOT_OBSERVED")
            self.assertEqual(len(evidence["suppressed_candidates"]), 1)
            self.assertIn("POOL_INFRASTRUCTURE",
                          evidence["suppressed_candidates"][0]["outcome"])
            self.assertEqual(len(evidence["investigations"]), 1)
            self.assertIsNone(evidence["investigations"][0]["chain_transaction_signature"])
            self.assertEqual(len(list(outbox.glob("grok_task_*.md"))), 1)
            self.assertIn("NOT_EXECUTED",
                          (outbox / "provisional_monitor_opinion.md").read_text())

    def test_missing_required_market_source_fails_handoff_instead_of_faking_bot(self):
        with tempfile.TemporaryDirectory() as tmp:
            mint_dir = Path(tmp) / "mint"
            outbox = Path(tmp) / "grok-outbox"
            # Mint report may still succeed using a single vendor, but the
            # two-source Grok evidence workflow must NOT pass.
            self.assertEqual(collect_mocked(mint_dir, dex_ok=False), 0)
            report = json.loads((mint_dir / "report.json").read_text())
            self.assertEqual(report["source_status"]["dex_public_pairs"], "UNAVAILABLE")
            self.assertFalse((mint_dir / "dex-provider-raw.json").exists())
            with self.assertRaises(FileNotFoundError):
                run_handoff(mint_dir, outbox)
            self.assertFalse((outbox / "evidence.json").exists())


if __name__ == "__main__":
    unittest.main()
