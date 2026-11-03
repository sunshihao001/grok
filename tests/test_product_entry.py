"""Characterize the product CLI using synthetic provider bytes; no Grok or live RPC."""
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from solana_meme_os import product

# Reuse the one canonical synthetic two-source fixture, not a second test data model.
from test_grok_mint_evidence_pipeline import MINT, payloads


class OneCommandMintProduct(unittest.TestCase):
    def _run(self, dest, *, dex_ok=True, rug_ok=True, reject=False):
        dex, rug = payloads()
        dex_result = (dex, "https://api.dexscreener.com/token-pairs/v1/solana/" + MINT)
        with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                   return_value=dex_result) as pairs:
            if not dex_ok:
                pairs.side_effect = OSError("synthetic DEX unavailable")
            with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                       return_value=rug) as rugged:
                if not rug_ok:
                    rugged.side_effect = OSError("synthetic RugCheck unavailable")
                with patch("solana_meme_os.product.vendor_event_handoff.triage",
                           wraps=product.vendor_event_handoff.triage) as triage:
                    if reject:
                        triage.side_effect = ValueError("synthetic source mismatch")
                    with contextlib.redirect_stdout(io.StringIO()) as output:
                        code = product.main([MINT, "--out-dir", str(dest)])
        return code, json.loads(output.getvalue()), triage

    def test_one_command_creates_verified_evidence_without_running_grok(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "one"
            code, result, triage = self._run(run)
            self.assertEqual(code, 0)
            self.assertTrue(triage.called)
            self.assertEqual(result["status"], "READY_FOR_GROK_REVIEW_NOT_EXECUTED")
            self.assertFalse(result["grok_executed"])
            self.assertTrue(result["no_trading"])
            self.assertFalse(result["payment_executed"])
            self.assertEqual(result["wallet_transactions"], "NOT_OBSERVED")
            self.assertEqual(result["funding_graph"], "NOT_OBSERVED")
            dex, rug = payloads()
            self.assertEqual((run / "mint/dex-provider-raw.json").read_bytes(), dex)
            self.assertEqual((run / "mint/rugcheck-provider-raw.json").read_bytes(), rug)
            self.assertTrue((run / "mint/report.md").exists())
            self.assertTrue((run / "grok-outbox/provisional_monitor_opinion.md").exists())
            evidence = json.loads((run / "grok-outbox/evidence.json").read_text())
            self.assertEqual(evidence["source_proofs"]["rugcheck_sha256"], hashlib.sha256(rug).hexdigest())
            self.assertEqual(evidence["source_proofs"]["dex_sha256"], hashlib.sha256(dex).hexdigest())
            self.assertEqual(evidence["disposition"], "PREPARE_GROK_TASKS_ONLY_NO_BOT_INVOKED")
            self.assertEqual(json.loads((run / "run_status.json").read_text()), result)

    def test_rugcheck_missing_keeps_useful_dex_report_but_no_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "partial"
            code, result, triage = self._run(run, rug_ok=False)
            self.assertEqual(code, 4)
            self.assertEqual(result["status"], "PARTIAL_MINT_REPORT_NO_GROK_HANDOFF")
            self.assertEqual(result["missing_sources"], ["RUGCHECK"])
            self.assertTrue((run / "mint/report.json").exists())
            self.assertFalse((run / "grok-outbox/evidence.json").exists())
            self.assertFalse(triage.called)

    def test_dex_missing_keeps_rugcheck_report_but_no_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "partial"
            code, result, triage = self._run(run, dex_ok=False)
            self.assertEqual(code, 4)
            self.assertEqual(result["missing_sources"], ["DEX"])
            self.assertTrue((run / "mint/report.json").exists())
            self.assertFalse(triage.called)

    def test_no_provider_returns_a_failure_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "failed"
            code, result, triage = self._run(run, dex_ok=False, rug_ok=False)
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "COLLECT_FAILED")
            self.assertTrue((run / "run_status.json").exists())
            self.assertFalse(triage.called)

    def test_bad_source_cannot_produce_review_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "rejected"
            code, result, triage = self._run(run, reject=True)
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "EVIDENCE_REJECTED")
            self.assertIn("mismatch", result["reason"])
            self.assertTrue((run / "mint/report.json").exists())
            self.assertFalse((run / "grok-outbox/evidence.json").exists())
            self.assertTrue(triage.called)

    def test_invalid_mint_and_overwrite_refuse(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = Path(tmp) / "absent"
            with contextlib.redirect_stderr(io.StringIO()):
                bad = product.main(["not-a-valid-solana-address", "--out-dir", str(run)])
            self.assertEqual(bad, 2)
            self.assertFalse(run.exists())
            run.mkdir()
            with contextlib.redirect_stderr(io.StringIO()):
                code = product.main([MINT, "--out-dir", str(run)])
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
