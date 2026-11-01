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

    def test_holder_and_funding_candidate_from_documented_fields(self):
        a = sample()
        a["data"]["structure"]["holders"] = [{
            "holderWalletAddress": "So11111111111111111111111111111111111111112",
            "holdAmount": "100000000.000000001", "holdPercent": "10.000000000000001",
            "fundingSource": "11111111111111111111111111111111",
            "realizedPnlUsd": "3.20"}]
        x = compile_report(a, MINT, fixture=True, source_sha256="z", processed_at="2026-11-01T00:00:00Z")
        b = x["business_summary"]
        self.assertEqual(b["holder_sample_rows"], 1)
        self.assertEqual(b["key_wallet_candidates"][0]["hold_amount"], "100000000.000000001")
        self.assertEqual(b["funding_source_hints"][0]["interpretation"], "VENDOR_FUNDING_HINT_NOT_COMMON_CONTROLLER")
        self.assertIn("不等于全体持有人", markdown(x))

    def test_vendor_cluster_is_not_confirmed_anomaly(self):
        a = sample()
        a["data"]["structure"]["cluster"] = {
            "clusterConcentration": "High", "holderSameFundSourcePercent": "0.47800",
            "rugPullPercent": "1.00000", "holderNewAddressPercent": "--"}
        result = compile_report(a, MINT, fixture=True, source_sha256="z", processed_at="x")
        b = result["business_summary"]["vendor_cluster_statistics"]
        self.assertEqual({x["field"] for x in b},
                         {"clusterConcentration", "holderSameFundSourcePercent", "rugPullPercent"})
        self.assertTrue(all(x["verified_abnormal"] is False for x in b))
        self.assertIn("尚未确证异常", markdown(result))

    def test_unrecognized_holder_shape_does_not_fabricate_zero_wallets(self):
        a = sample()
        a["data"]["structure"]["holders"] = {"someNewVendorSchema": 5}
        result = compile_report(a, MINT, fixture=True, source_sha256="z", processed_at="x")
        self.assertEqual(result["business_summary"]["holder_sample_status"], "UNSUPPORTED_RESPONSE_SHAPE")
        self.assertEqual(result["business_summary"]["holder_sample_rows"], 0)
        self.assertEqual(result["business_summary"]["holder_coverage"].startswith("UNKNOWN"), True)

    def test_empty_holder_response_not_equivalent_whole_market_empty(self):
        a = sample()
        a["data"]["structure"]["holders"] = {"list": []}
        result = compile_report(a, MINT, fixture=True, source_sha256="z", processed_at="x")
        self.assertEqual(result["business_summary"]["holder_sample_status"], "RETURNED_SAMPLE_ONLY")
        self.assertIn("UNKNOWN_NOT_WHOLE_CHAIN", result["business_summary"]["holder_coverage"])

    def test_vendor_request_time_kept_distinct_from_processing_time(self):
        a = sample()
        a["data"]["core"]["info"] = [{"requestTime": 1790000000000, "tokenSymbol": "X"}]
        a["data"]["core"]["price"] = [{"time": "1790000000123", "price": "0.1"}]
        result = compile_report(a, MINT, fixture=False, source_sha256="z", processed_at="2026-11-01T12:01:00Z")
        self.assertIsNone(result["vendor_data_time"])
        hints = result["business_summary"]["per_field_source_time_hints"]
        self.assertEqual(len(hints), 2)
        self.assertEqual(hints[0]["source_path"], "data.core.info[0].requestTime")
        self.assertEqual(hints[1]["source_path"], "data.core.price[0].time")

    def test_dev_available_is_label_not_history_verified(self):
        a = sample()
        a["data"]["launchpad"] = {"devInfo": {"historicalLaunches": 4}, "bundleInfo": {"bundleRate": "5%"}}
        result = compile_report(a, MINT, fixture=True, source_sha256="z", processed_at="x")
        self.assertEqual(result["business_summary"]["developer_history_vendor_status"], "PRESENT_UNVERIFIED")
        self.assertEqual(result["business_summary"]["bundle_vendor_status"], "PRESENT_UNVERIFIED")
        self.assertEqual(result["chain_event_time"], None)


if __name__ == "__main__":
    unittest.main()