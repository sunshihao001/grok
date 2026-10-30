"""Structural + adversarial regressions for optional specialist reasoning briefs."""
import copy
import unittest

from solana_meme_os.expert_brief import (
    audit_registry, expert_brief, load_registry, recommend_experts,
)


class LayerExpertTests(unittest.TestCase):
    def test_every_existing_layer_has_at_least_two_specialists(self):
        r = audit_registry()
        self.assertEqual(r["status"], "STRUCTURALLY_VALID_NOT_DEPLOYED")
        self.assertFalse(r["no_live_market_facts_verified"] is False)
        self.assertTrue(r["no_grok_bots_provisioned"])
        self.assertGreaterEqual(r["specialists"], 20)
        j = load_registry()
        for layer in r["layers"]:
            specialists = [e for e in j["specialists"] if e["layer"] == layer]
            self.assertGreaterEqual(len(specialists), 2)
            self.assertTrue(all(len(e["specialist_knowledge_primitives"]) >= 3 for e in specialists))
            self.assertTrue(all(e["reasoning_sequence"] and e["decisive_next_check"] for e in specialists))

    def test_explicit_expert_has_own_knowledge_and_distinguishing_logic(self):
        brief = expert_brief("E-L3-02")
        x = brief["specialist"]
        self.assertEqual(x["name"], "资金溯源与经济主体取证专家")
        self.assertEqual(x["workflow_owner"], "B03")
        self.assertIn("D05", x["domain_ids"])
        self.assertIn("HUB", " ".join(x["specialist_knowledge_primitives"]))
        self.assertTrue(brief["source_admission_required"])
        self.assertFalse(brief["is_deployed_bot"])

    def test_copytrading_economic_question_routes_cost_specialist(self):
        x = recommend_experts("钱包跟单后滑点和退出成本", objective="ECONOMIC")
        self.assertEqual(x["status"], "SPECIALISTS_SELECTED_FOR_RESEARCH_ONLY")
        self.assertIn("E-L5-01", [v["id"] for v in x["specialists"]])
        self.assertNotIn("E-L7-02", [v["id"] for v in x["specialists"]])
        self.assertTrue(x["frozen_monitor_cannot_generate_new_rules"])

    def test_funding_question_routes_graph_expert(self):
        x = recommend_experts("资金同源是不是共享交易所节点", max_experts=4)
        self.assertIn("E-L3-02", [v["id"] for v in x["specialists"]])

    def test_unknown_question_does_not_invent_an_expert(self):
        x = recommend_experts("火星奶酪未知非相关概念")
        self.assertEqual(x["status"], "SOURCE_DISCOVERY_REQUIRED")
        self.assertEqual(x["specialists"], [])

    def test_explicit_review_not_auto_trade_execution(self):
        m = expert_brief("E-L7-02")
        self.assertTrue(m["no_alpha_or_monitor_approval"])
        self.assertFalse(m["is_deployed_bot"])
        x = recommend_experts("规则发布和监控", objective="MONITOR_RELEASE", max_experts=5)
        self.assertIn("E-L7-02", [s["id"] for s in x["specialists"]])

    def test_fake_owner_and_missing_knowledge_are_rejected(self):
        r = copy.deepcopy(load_registry())
        r["specialists"][0]["workflow_owner"] = "B99"
        with self.assertRaisesRegex(ValueError, "mapping"):
            audit_registry(r)
        r = copy.deepcopy(load_registry())
        r["specialists"][0]["knowledge_files"] = ["../../private_key"]
        with self.assertRaisesRegex(ValueError, "knowledge source"):
            audit_registry(r)

    def test_prior_52_topic_ids_are_not_invented_or_cross_role(self):
        registry = load_registry()
        self.assertTrue(all(len(x["prior_research_competency_ids"]) >= 2
                            for x in registry["specialists"]))
        corrupt = copy.deepcopy(registry)
        corrupt["specialists"][0]["prior_research_competency_ids"] = ["B07-K01"]
        with self.assertRaisesRegex(ValueError, "prior knowledge"):
            audit_registry(corrupt)

    def test_expert_cannot_silently_upgrade_authority(self):
        r = copy.deepcopy(load_registry())
        r["specialists"][0]["authority"] = "approve_live_trades"
        with self.assertRaisesRegex(ValueError, "self-authorize"):
            audit_registry(r)

    def test_external_report_not_used_as_direct_specialist_fact(self):
        r = load_registry()
        self.assertTrue(all(e["evidence_status"] == "proposed_not_live_validated" for e in r["specialists"]))
        self.assertTrue(all(not e["knowledge_files"] or
                            all(path.startswith("knowledge/domain/") for path in e["knowledge_files"])
                            for e in r["specialists"]))


if __name__ == "__main__":
    unittest.main()
