"""KNOW-003 offline adversarial fixtures (no trading, no live data)."""
import copy
import json
from pathlib import Path
import unittest
from solana_meme_os.research_gate import audit

BASE = json.loads((Path(__file__).resolve().parents[1] / "fixtures/know003-study.json").read_text(encoding="utf-8"))


class ResearchGateTests(unittest.TestCase):
    def test_high_hit_rate_still_negative_net_and_no_promotion(self):
        out = audit(BASE)
        cohort = out["summary"]["TEST"]["selected"]
        self.assertEqual(cohort["n"], 4)
        self.assertEqual(cohort["hit_rate"], .75)
        self.assertLess(cohort["mean_net_roi"], 0)
        self.assertEqual(out["gate"]["promotion"], "DO_NOT_PROMOTE")
        self.assertEqual(out["descriptive_verdict"], "NON_POSITIVE_NET_IN_SYNTHETIC_TEST")

    def test_future_available_feature_is_rejected(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["features"][0]["available_at"] = "2026-10-17T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "leaks future"):
            audit(doc)

    def test_event_time_is_not_enough_if_data_late(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["features"][0]["event_at"] = "2026-10-14T00:00:00Z"
        doc["rows"][2]["features"][0]["available_at"] = "2026-10-17T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "leaks future"):
            audit(doc)

    def test_future_outcome_cannot_enter_features(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["features"][0]["name"] = "future_peak"
        with self.assertRaisesRegex(ValueError, "future label"):
            audit(doc)

    def test_outcome_cannot_precede_entry_fill(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["outcome_observed_at"] = doc["rows"][2]["decision_at"]
        with self.assertRaisesRegex(ValueError, "chronology"):
            audit(doc)

    def test_protocol_must_be_frozen_before_test(self):
        doc = copy.deepcopy(BASE)
        doc["protocol"]["locked_at"] = "2026-10-17T00:00:00Z"
        with self.assertRaisesRegex(ValueError, "pre-registration"):
            audit(doc)

    def test_missing_capture_never_becomes_zero_return(self):
        doc = copy.deepcopy(BASE)
        row = doc["rows"][5]
        row["measurement_status"] = "MISSING"
        row["missing_reason"] = "HTTP 429, paging unknown"
        for field in ("hit_target", "buy_filled_usd", "sell_filled_usd"):
            row.pop(field)
        out = audit(doc)
        self.assertEqual(out["summary"]["TEST"]["missing_n"], 1)
        self.assertEqual(out["summary"]["TEST"]["selected"]["n"], 3)
        self.assertEqual(out["gate"]["promotion"], "DO_NOT_PROMOTE")

    def test_missing_cannot_hide_existing_outcome(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][3]["measurement_status"] = "MISSING"
        doc["rows"][3]["missing_reason"] = "RPC timeout"
        with self.assertRaisesRegex(ValueError, "missing rows"):
            audit(doc)

    def test_failed_exit_cannot_claim_proceeds(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][5]["sell_filled_usd"] = 50
        with self.assertRaisesRegex(ValueError, "failed exit"):
            audit(doc)

    def test_positive_fiction_still_not_validated(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][5]["sell_filled_usd"] = 120
        doc["rows"][5]["exit_status"] = "FILLED"
        out = audit(doc)
        self.assertGreater(out["summary"]["TEST"]["selected"]["mean_net_roi"], 0)
        self.assertEqual(out["descriptive_verdict"], "POSITIVE_SYNTHETIC_TEST_NOT_VALIDATED")
        self.assertEqual(out["gate"]["promotion"], "DO_NOT_PROMOTE")

    def test_split_and_duplicated_rows_are_rejected(self):
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["split"] = "TRAIN"
        with self.assertRaisesRegex(ValueError, "time boundary"):
            audit(doc)
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["id"] = doc["rows"][1]["id"]
        with self.assertRaisesRegex(ValueError, "duplicate"):
            audit(doc)

    def test_missing_controls_and_unbounded_values_fail_closed(self):
        doc = copy.deepcopy(BASE)
        doc["protocol"]["null_model"] = ""
        with self.assertRaisesRegex(ValueError, "null_model"):
            audit(doc)
        doc = copy.deepcopy(BASE)
        doc["rows"][2]["buy_fees_usd"] = "-0.3"
        with self.assertRaisesRegex(ValueError, "buy_fees"):
            audit(doc)

    def test_synthetic_only(self):
        doc = copy.deepcopy(BASE)
        doc["data_mode"] = "live"
        with self.assertRaisesRegex(ValueError, "synthetic"):
            audit(doc)


if __name__ == "__main__":
    unittest.main()
