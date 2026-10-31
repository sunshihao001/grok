"""Synthetic contract tests for fast-loop to slow-loop research planning.

These are source-derived *fixtures*, not market truth or agent execution.
"""
import copy
import unittest

from solana_meme_os.research_dispatch import make_plan


def sample():
    return {
        "schema_version": "0.1", "result_type": "MULTI_WALLET_EVENT_OBSERVATORY",
        "no_trading": True,
        "coverage_status": "INPUT_COHORT_ONLY_NO_CHAIN_WIDE_COMPLETENESS_CLAIM",
        "input_status": {"input_mode": "fixture", "decision_time_filter": None},
        "group_candidates": [
            {"kind": "SAME_SLOT_MULTIWALLET_BUY", "mint": "M1", "slot": 7,
             "wallets": ["W1", "W2"], "signatures": ["buy-a", "buy-b"]},
            {"kind": "TOKEN_CONSOLIDATION", "mint": "M1",
             "signatures": ["move-a"]},
            {"kind": "FUNDING_FANOUT", "funder": "F", "signatures": ["fund-a", "fund-b"]},
            {"kind": "CROSS_MINT_FUNDING_REUSE", "candidate_funder": "F",
             "mints": ["M1", "M2"], "signatures": ["fund-b", "m2-buy"]},
            {"kind": "CROSS_MINT_WALLET_ACTIVITY", "wallet": "W1",
             "mints": ["M1", "M2"], "signatures": []},
        ],
    }


class ResearchDispatchTests(unittest.TestCase):
    def test_bounded_and_deterministic(self):
        x = make_plan(sample(), max_cases=2, max_source_checks=3, max_per_case=2)
        y = make_plan(copy.deepcopy(sample()), max_cases=2,
                      max_source_checks=3, max_per_case=2)
        self.assertEqual(x, y)
        self.assertEqual(x["signature_checks_planned"], 3)
        self.assertEqual(x["case_count_available"], 3)
        self.assertEqual(x["case_count_deferred"], 1)
        self.assertTrue(x["no_trading"])
        self.assertEqual(x["agent_execution_status"], "NOT_RUN")

    def test_no_unproven_mint_funder_merge(self):
        x = make_plan(sample())
        self.assertEqual({a["scope"] for a in x["cases"]},
                         {"MINT:M1", "SOURCE:F", "WALLET:W1"})
        self.assertTrue(all(a["no_economic_owner_or_anomaly_conclusion"]
                            for a in x["cases"]))

    def test_priority_means_workload_not_market_risk(self):
        x = make_plan(sample(), max_cases=2)
        self.assertEqual(x["cases"][0]["scope"], "MINT:M1")
        self.assertEqual(x["cases"][1]["scope"], "SOURCE:F")
        self.assertTrue(all(a["priority_not_a_market_risk_score"]
                            for a in x["cases"]))
        self.assertFalse(x["baseline_calibrated"])

    def test_duplicate_candidate_signatures_are_not_double_counted(self):
        x = make_plan(sample())
        funder = next(a for a in x["cases"] if a["scope"] == "SOURCE:F")
        self.assertEqual(funder["unique_signatures_in_input"], 3)
        self.assertEqual(funder["candidate_records_in_input"], 2)

    def test_missing_signature_never_silently_becomes_verified(self):
        x = make_plan(sample())
        row = next(a for a in x["cases"] if a["scope"] == "WALLET:W1")
        self.assertEqual(row["verification_status"],
                         "MISSING_SIGNATURES_REQUIRE_SOURCE_REPAIR")
        self.assertEqual(row["source_checks_proposed"], [])

    def test_unfamiliar_event_preserves_open_world_discovery(self):
        x = sample()
        x["group_candidates"] = [{"kind": "NEW_PROGRAM_RECEIPT",
                                  "mint": "M9", "signatures": ["sig-new"]}]
        y = make_plan(x)
        self.assertTrue(y["cases"][0]["open_discovery"])
        self.assertEqual(y["cases"][0]["research_priority"], 0)
        self.assertEqual(y["cases"][0]["scope"], "UNMAPPED:M9")

    def test_source_derived_is_not_rpc_confirmed(self):
        x = sample()
        x["input_status"]["input_mode"] = "source_derived"
        y = make_plan(x)
        self.assertTrue(all(row["verification_status"] ==
                            "SOURCE_CONFIRMATION_REQUIRED"
                            for row in y["cases"] if row["unique_signatures_in_input"]))
        self.assertFalse(y["time_safe_prediction_qualified"])

    def test_asof_is_preserved_not_pretended(self):
        x = sample()
        x["input_status"]["decision_time_filter"] = "2026-10-31T01:00:00Z"
        y = make_plan(x)
        self.assertEqual(y["decision_time_filter"], "2026-10-31T01:00:00Z")
        self.assertFalse(y["time_safe_prediction_qualified"])

    def test_invalid_or_overstated_source_is_rejected(self):
        for key, bad in (("no_trading", False), ("coverage_status", "FULL_CHAIN"),
                         ("result_type", "UNRELATED")):
            x = sample()
            x[key] = bad
            with self.assertRaises(ValueError):
                make_plan(x)

    def test_budget_and_schema_fail_closed(self):
        with self.assertRaises(ValueError):
            make_plan(sample(), max_cases=0)
        with self.assertRaises(ValueError):
            make_plan(sample(), max_source_checks=True)
        x = sample()
        x["group_candidates"][0]["signatures"] = [42]
        with self.assertRaises(ValueError):
            make_plan(x)

    def test_empty_cohort_is_not_normal_market(self):
        x = sample()
        x["group_candidates"] = []
        y = make_plan(x)
        self.assertEqual(y["case_count_available"], 0)
        self.assertFalse(y["marketwide_coverage_confirmed"])

    def test_specialist_handoffs_remain_unexecuted(self):
        x = make_plan(sample())
        mint_case = next(v for v in x["cases"] if v["scope"] == "MINT:M1")
        self.assertIn("chain", mint_case["research_role_ids"])
        self.assertIn("review", mint_case["independent_review_roles"])
        self.assertTrue(mint_case["typed_handoff_ids"])


if __name__ == "__main__":
    unittest.main()
