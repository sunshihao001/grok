import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from solana_meme_os.mint_report import compile_report, main, markdown

MINT = "87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump"

def sample():
    return {"ok": True, "data": {"workflow": "token-research", "address": MINT, "chain": "501",
            "core": {"info": {"tokenSymbol": "SYNTHETIC_DEMO"}, "price": None,
                     "contract": {}, "security": None},
            "structure": {"holders": [{"address": "SYNTHETIC_ONLY"}], "cluster": None,
                          "topTraders": None, "signals": []}, "launchpad": None}}

class TestMintReport(unittest.TestCase):
    def test_valid_report_preserves_unknown(self):
        r = compile_report(sample(), MINT, fixture=True, source_sha256="1" * 64, processed_at="2026-11-01T00:00:00+00:00")
        self.assertEqual(r["status"], "FIXTURE_DEMO_ONLY")
        self.assertEqual(r["sections"][1]["status"], "UNKNOWN")
        self.assertEqual(r["sections"][5]["value"], None)
        self.assertIsNone(r["vendor_data_time"])
        self.assertTrue(r["no_trading"])
        self.assertIn("不等于0", markdown(r))
    def test_wrong_mint_rejected(self):
        with self.assertRaisesRegex(ValueError, "Mint differs"):
            compile_report(sample(), "So11111111111111111111111111111111111111112", fixture=False, source_sha256="x", processed_at="x")
    def test_failed_cli_rejected(self):
        with self.assertRaisesRegex(ValueError, "not a successful"):
            compile_report({"ok": False, "error": "bad"}, MINT, fixture=False, source_sha256="x", processed_at="x")
    def test_all_core_null_rejected(self):
        a = sample(); a["data"]["core"] = {"info": None, "price": None, "contract": None, "security": None}
        with self.assertRaisesRegex(ValueError, "all OKX core fields are null"):
            compile_report(a, MINT, fixture=False, source_sha256="x", processed_at="x")
    def test_output_files_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "in.json"; out = Path(d) / "output"; p.write_text(json.dumps(sample()))
            with contextlib.redirect_stdout(io.StringIO()) as buf:
                status = main(["--mint", MINT, "--okx-json", str(p), "--out-dir", str(out), "--fixture"])
            self.assertEqual(status, 0)
            self.assertEqual(json.loads(buf.getvalue())["status"], "FIXTURE_DEMO_ONLY")
            self.assertTrue((out / "report.md").exists())
            self.assertTrue((out / "report.json").exists())
            self.assertEqual(json.loads((out / "report.json").read_text())["source"]["provider"], "OKX OnchainOS")
    def test_rejects_non_okx_structure(self):
        a = sample(); del a["data"]["structure"]
        with self.assertRaisesRegex(ValueError, "missing OKX core/structure"):
            compile_report(a, MINT, fixture=False, source_sha256="x", processed_at="x")

if __name__ == "__main__":
    unittest.main()