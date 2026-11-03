"""Full two-CLI handoff contract, with network response bytes stubbed.

Tests Mint V0.1 -> stored raw provider JSON -> vendor triage -> Grok outbox.
This is *not* a Grok Bot run, a new live vendor request or a transaction feed.
"""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from solana_meme_os import mint_v01, vendor_event_handoff


MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
POOL = "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB"
TOKEN_ACCOUNT = "BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i"


def sources():
    dex = [{
        "chainId": "solana",
        "dexId": "pumpswap",
        "pairAddress": POOL,
        "baseToken": {"address": MINT, "symbol": "TEST"},
        "quoteToken": {"address": "So11111111111111111111111111111111111111112", "symbol": "SOL"}
    }]
    rug = {
        "mint": MINT,
        "creator": POOL,
        "topHolders": [{"address": TOKEN_ACCOUNT, "owner": POOL, "pct": 5.88}],
        "knownAccounts": {POOL: {"name": "AMM", "type": "AMM"}},
        "markets": [{
            "pubkey": POOL, "liquidityA": TOKEN_ACCOUNT,
            "liquidityAAccount": {"mint": MINT, "owner": POOL},
        }],
        "risks": [{"name": "Vendor risk requires review", "level": "warn", "score": 100}],
    }
    return json.dumps(dex).encode("utf-8"), json.dumps(rug).encode("utf-8")


class GrokHandoffIntegration(unittest.TestCase):
    def run_mint_offline(self, directory):
        dex, rug = sources()
        with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                   return_value=(dex, "https://api.dexscreener.com/token-pairs/v1/solana/" + MINT)):
            with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                       return_value=rug):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           side_effect=AssertionError("unexpected RPC")):
                    with contextlib.redirect_stdout(io.StringIO()):
                        code = mint_v01.main([MINT, "--rugcheck", "--out-dir", str(directory)])
        self.assertEqual(code, 0)
        return dex, rug

    def test_existing_two_cli_steps_produce_checked_bot_outbox(self):
        with tempfile.TemporaryDirectory() as tmp:
            mint_dir = Path(tmp) / "run" / "mint"
            outbox = Path(tmp) / "run" / "outbox"
            dex, rug = self.run_mint_offline(mint_dir)
            with contextlib.redirect_stdout(io.StringIO()):
                code = vendor_event_handoff.main([
                    "--report", str(mint_dir / "report.json"),
                    "--rugcheck-raw", str(mint_dir / "rugcheck-provider-raw.json"),
                    "--dex-raw", str(mint_dir / "dex-provider-raw.json"),
                    "--out-dir", str(outbox),
                ])
            self.assertEqual(code, 0)
            packet = json.loads((outbox / "evidence.json").read_text())
            report = json.loads((mint_dir / "report.json").read_text())
            self.assertEqual(packet["mint"], MINT)
            self.assertEqual(packet["source_proofs"]["dex_sha256"], hashlib.sha256(dex).hexdigest())
            self.assertEqual(packet["source_proofs"]["rugcheck_sha256"], hashlib.sha256(rug).hexdigest())
            self.assertEqual(packet["source_proofs"]["report_sha256"],
                             hashlib.sha256((mint_dir / "report.json").read_bytes()).hexdigest())
            self.assertTrue(report["no_trading"])
            self.assertEqual(packet["model_calls"], 0)
            self.assertEqual(packet["auto_payments"], 0)
            self.assertEqual(packet["coverage"]["wallet_transactions"], "NOT_OBSERVED")
            self.assertEqual(packet["coverage"]["funding_graph"], "NOT_OBSERVED")
            self.assertEqual(packet["disposition"], "PREPARE_GROK_TASKS_ONLY_NO_BOT_INVOKED")
            self.assertEqual(len(packet["investigations"]), 1)
            self.assertIsNone(packet["investigations"][0]["chain_transaction_signature"])
            self.assertEqual(
                packet["suppressed_candidates"][0]["outcome"],
                "POOL_INFRASTRUCTURE_EXPLANATION_SUPPRESSES_WHALE_ALERT",
            )
            self.assertEqual(len(list(outbox.glob("grok_task_*.md"))), 1)
            self.assertFalse((outbox / "grok_analysis.md").exists(),
                             "A local Python test cannot claim that Grok reasoned or ran.")

    def test_tampered_raw_source_cannot_be_reused_for_new_bot_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            mint_dir = Path(tmp) / "run" / "mint"
            outbox = Path(tmp) / "run" / "outbox"
            self.run_mint_offline(mint_dir)
            raw_path = mint_dir / "rugcheck-provider-raw.json"
            raw = json.loads(raw_path.read_text())
            raw["risks"][0]["name"] = "tampered claim"
            raw_path.write_text(json.dumps(raw))
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as error:
                    vendor_event_handoff.main([
                        "--report", str(mint_dir / "report.json"),
                        "--rugcheck-raw", str(raw_path),
                        "--dex-raw", str(mint_dir / "dex-provider-raw.json"),
                        "--out-dir", str(outbox),
                    ])
            self.assertEqual(error.exception.code, 2)
            self.assertFalse(outbox.exists())

if __name__ == "__main__":
    unittest.main()
