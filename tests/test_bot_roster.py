"""Validate proposed roles without pretending cloud Bots are provisioned."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
class BotRosterTests(unittest.TestCase):
    def test_roles_are_six_development_and_one_monitor(self):
        d=json.loads((ROOT/"design/bot-roster.v1.json").read_text(encoding="utf-8"))
        self.assertEqual((d["bot_count"],d["development_count"],d["production_count"]),(7,6,1))
        self.assertEqual([x["id"] for x in d["bots"]],[f"B{i:02d}" for i in range(1,8)])
        self.assertEqual([x["phase"] for x in d["bots"]],["development"]*6+["production"])
        self.assertEqual(d["status"],"PLANNED_NOT_PROVISIONED")
        self.assertFalse(d["role_separation_is_security_boundary"])
        self.assertFalse(d["live_trading_allowed"])
        self.assertTrue(d["human_rule_approval_required"])
        self.assertTrue(all(not b["may_trade"] and not b["can_approve_own_research"] for b in d["bots"]))
    def test_domain_gate_ids_and_independence(self):
        d=json.loads((ROOT/"design/bot-roster.v1.json").read_text(encoding="utf-8"))
        o=json.loads((ROOT/"knowledge/system/ontology.v1.json").read_text(encoding="utf-8"))
        p=json.loads((ROOT/"knowledge/system/filter-policy.v1.json").read_text(encoding="utf-8"))
        ids={v["id"] for v in o["domains"]}; gates={v["id"] for v in p["gates"]}
        for b in d["bots"]:
            self.assertTrue(b["domain_ids"] and b["gate_ids"])
            self.assertFalse(set(b["domain_ids"])-ids)
            self.assertFalse(set(b["gate_ids"])-gates)
        self.assertEqual(d["bots"][-1]["gate_ids"],["F6"])
        self.assertIn("F5",d["bots"][3]["gate_ids"])
        self.assertIn("F5",d["bots"][4]["gate_ids"])
        self.assertIn("F5",d["bots"][5]["gate_ids"])
if __name__=="__main__": unittest.main()
