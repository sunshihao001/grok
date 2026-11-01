"""Verify saved OKX JSON never becomes market proof or triggers CLI payments."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

from solana_meme_os.okx_snapshot import parse_snapshot
from solana_meme_os.knowledge_system import ROOT

MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
FIXTURE=ROOT/"fixtures/okx-price.synthetic.json"


class OKXSnapshotTests(unittest.TestCase):
    def _parse(self, payload,op="token_price_info",**kwargs):
        return parse_snapshot(json.dumps(payload).encode("utf-8"),op,MINT,**kwargs)

    def test_positive_shape_is_only_unverified_capture(self):
        result=parse_snapshot(FIXTURE.read_bytes(),"token_price_info",MINT)
        self.assertEqual(result["status"],"UNVERIFIED_PROVIDER_CAPTURE")
        self.assertEqual(result["candidate_numeric_fields"]["price_usd"],"0.0000123")
        self.assertEqual(result["candidate_numeric_fields"]["liquidity_usd"],"9000")
        self.assertTrue(result["address_confirmed"])
        self.assertFalse(result["source_authenticated"])
        self.assertFalse(result["eligible_as_decision_feature"])
        self.assertFalse(result["eligible_as_live_monitor_input"])
        self.assertFalse(result["payment_authorized"])

    def test_absent_field_not_fabricated_as_zero(self):
        payload={"ok":True,"notifications":[],"data":{"tokenContractAddress":MINT,"price":"0"}}
        r=self._parse(payload)
        self.assertEqual(r["candidate_numeric_fields"]["price_usd"],"0")
        self.assertIn("liquidity_usd",r["missing_fields"])
        self.assertNotIn("liquidity_usd",r["candidate_numeric_fields"])

    def test_payment_notification_blocks_data_promotion(self):
        payload={"ok":True,"confirming":True,"notifications":[{"code":"MARKET_API_PREMIUM_OVER_QUOTA"}],
                 "data":{"tokenContractAddress":MINT,"price":"1"}}
        r=self._parse(payload)
        self.assertEqual(r["status"],"PROVIDER_NOTIFICATIONS_REQUIRE_HUMAN_REVIEW")
        self.assertEqual(r["candidate_numeric_fields"],{})
        self.assertFalse(r["payment_authorized"])

    def test_nonblocking_notice_also_requires_review(self):
        payload={"ok":True,"notifications":[{"code":"MARKET_API_NEW_USER_INTRO"}],
                 "data":{"tokenContractAddress":MINT,"price":"1"}}
        self.assertEqual(self._parse(payload)["status"],"PROVIDER_NOTIFICATIONS_REQUIRE_HUMAN_REVIEW")

    def test_provider_error_is_not_empty_market(self):
        payload={"ok":False,"data":None}
        self.assertEqual(self._parse(payload)["status"],"PROVIDER_RESULT_UNAVAILABLE")

    def test_wrong_token_address_rejected(self):
        payload={"ok":True,"data":{"tokenContractAddress":"11111111111111111111111111111111","price":"1"}}
        self.assertEqual(self._parse(payload)["status"],"PROVIDER_ADDRESS_MISMATCH")

    def test_bad_numeric_and_float_rejected(self):
        with self.assertRaisesRegex(ValueError,"not float"):
            self._parse({"ok":True,"data":{"price":1.1}})
        with self.assertRaisesRegex(ValueError,"non-negative"):
            self._parse({"ok":True,"data":{"price":"-1"}})

    def test_percent_bounds_in_meme_shape(self):
        r=self._parse({"ok":True,"data":{"tokenAddress":MINT,"tags":{"top10HoldingsPercent":"35.5"},
                                             "market":{"marketCapUsd":"1200"},"bondingPercent":"83.21"}},"memepump_token_details")
        self.assertEqual(r["candidate_numeric_fields"]["top10_holder_pct"],"35.5")
        with self.assertRaisesRegex(ValueError,"exceeds 100"):
            self._parse({"ok":True,"data":{"tags":{"top10HoldingsPercent":"101"}}},"memepump_token_details")

    def test_historical_ingest_does_not_prove_earlier_visibility(self):
        r=self._parse({"ok":True,"requestTime":"1780300000000","data":{"price":"1"}},
                      provider_received_at_utc="2026-10-01T00:00:20Z")
        self.assertIsNotNone(r["provider_request_time_ms"])
        self.assertFalse(r["eligible_as_decision_feature"])

    def test_no_receipt_time_is_explicitly_missing(self):
        self.assertIsNone(self._parse({"ok":True,"data":{"price":"1"}})["provider_received_at_utc"])

    def test_operation_not_authorized(self):
        with self.assertRaisesRegex(ValueError,"allowlist"):
            self._parse({"ok":True,"data":{}},"wallet_swap")

    def test_invalid_raw_type_or_token(self):
        with self.assertRaisesRegex(ValueError,"invalid Solana"):
            parse_snapshot(b'{}',"token_price_info","not-a-mint")
        with self.assertRaisesRegex(ValueError,"JSON"):
            parse_snapshot(b'{ broken',"token_price_info",MINT)

    def test_cli_works_without_okx_installation(self):
        import os
        env=os.environ.copy()
        env["PYTHONPATH"]=str(ROOT/"src")
        resp=subprocess.run([sys.executable,"-m","solana_meme_os.okx_snapshot",
                             "--input",str(FIXTURE),"--operation","token_price_info","--address",MINT],
                            cwd=ROOT,env=env,text=True,capture_output=True)
        self.assertEqual(resp.returncode,0,resp.stderr)
        self.assertEqual(json.loads(resp.stdout)["status"],"UNVERIFIED_PROVIDER_CAPTURE")


if __name__=="__main__":
    unittest.main()
