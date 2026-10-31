"""Offline end-to-end vertical slice: normalized source fixture -> M2 -> bounded research.

Does not simulate market-wide live coverage or execute any specialist/RPC call.
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from solana_meme_os.market_observatory import analyze
from solana_meme_os.research_dispatch import make_plan

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "market-observatory-synthetic.json"


class DualLoopVerticalSliceTests(unittest.TestCase):
    def test_existing_m2_fixture_yields_reproducible_research_handoffs(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))
        report = analyze(source, allow_fixture=True)
        plan = make_plan(report, max_cases=8, max_source_checks=15,
                         max_per_case=4)
        self.assertEqual(plan, make_plan(report, max_cases=8,
                                         max_source_checks=15, max_per_case=4))
        self.assertEqual(plan["mode"], "fixture")
        self.assertFalse(plan["marketwide_coverage_confirmed"])
        self.assertFalse(plan["time_safe_prediction_qualified"])
        self.assertEqual(plan["agent_execution_status"], "NOT_RUN")
        self.assertEqual(plan["source_rpc_execution_status"], "NOT_RUN")
        self.assertTrue(plan["no_trading"])
        self.assertGreater(plan["case_count_available"], 0)
        self.assertGreater(plan["signature_checks_planned"], 0)
        self.assertLessEqual(plan["signature_checks_planned"], 15)
        self.assertTrue(all(c["research_role_ids"] for c in plan["cases"]))
        self.assertTrue(all(c["verification_status"] == "OFFLINE_SYNTHETIC_ONLY"
                            for c in plan["cases"] if c["source_checks_proposed"]))

    def test_episode_scopes_never_merge_source_only_and_mint_evidence(self):
        source = json.loads(FIXTURE.read_text(encoding="utf-8"))
        report = analyze(source, allow_fixture=True)
        plan = make_plan(report, max_cases=50, max_source_checks=100,
                         max_per_case=10)
        observed_kinds = {row["kind"] for row in report["group_candidates"]}
        if "FUNDING_FANOUT" in observed_kinds:
            self.assertTrue(any(
                c["scope"].startswith("SOURCE:") and "FUNDING_FANOUT" in c["event_types"]
                for c in plan["cases"]))
        for c in plan["cases"]:
            self.assertFalse(c["scope"].startswith("MINT:") and
                             "FUNDING_FANOUT" in c["event_types"])
        self.assertTrue(all(c["no_economic_owner_or_anomaly_conclusion"]
                            for c in plan["cases"]))


if __name__ == "__main__":
    unittest.main()
