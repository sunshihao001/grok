"""Check evolving goal records against regression and scope failures."""
from __future__ import annotations

import copy
import unittest

from solana_meme_os import goal_state


class GoalStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = goal_state.load()

    def test_record_has_verifiable_next_action(self):
        result = goal_state.audit(self.record)
        self.assertTrue(result["ok"], result["errors"])
        self.assertGreaterEqual(result["goals_checked"], 6)
        self.assertGreaterEqual(result["options_checked"], 2)

    def test_original_copy_wallet_goal_is_retained(self):
        goals = {x["id"]: x for x in self.record["goals"]}
        self.assertEqual(goals["C1"]["status"], "retained")
        self.assertTrue(any(x["from"] == "C1" and x["to"] == "C2"
                            for x in self.record["changes"]))

    def test_blix_only_provisional_and_not_run(self):
        self.assertEqual(self.record["decision"]["preferred"], "A")
        self.assertEqual(self.record["decision"]["state"], "provisional")
        self.assertEqual(self.record["next_action"]["state"], "NOT_RUN")
        self.assertTrue(self.record["evidence_status"]["unknown"])

    def test_invalid_relation_fails(self):
        bad = copy.deepcopy(self.record)
        bad["links"].append({"from": "C1", "to": "nonexistent", "relation": "enables"})
        self.assertFalse(goal_state.audit(bad)["ok"])

    def test_unfalsifiable_option_fails(self):
        bad = copy.deepcopy(self.record)
        bad["decision"]["options"][0].pop("falsifier")
        self.assertFalse(goal_state.audit(bad)["ok"])

    def test_removing_human_boundary_fails(self):
        bad = copy.deepcopy(self.record)
        bad["boundaries"]["operation"] = "auto_trade"
        self.assertFalse(goal_state.audit(bad)["ok"])

    def test_missing_acceptance_fails(self):
        bad = copy.deepcopy(self.record)
        bad["next_action"]["acceptance"] = []
        self.assertFalse(goal_state.audit(bad)["ok"])

    def test_brief_does_not_claim_agent_execution(self):
        out = goal_state.brief(self.record)
        self.assertIn("does not confirm", out["warning"])
        self.assertEqual(out["next_action"]["state"], "NOT_RUN")


if __name__ == "__main__":
    unittest.main()
