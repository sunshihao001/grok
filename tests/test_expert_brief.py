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

    def test_l3_specialists_open_with_expert_view_not_academic_chapter(self):
        from pathlib import Path

        registry = load_registry()
        lead = "knowledge/domain/L3-actor-expert-perspectives.md"
        leads = [x for x in registry["specialists"] if x["layer"] == "L3"]
        self.assertEqual({x["id"] for x in leads},
                         {"E-L3-01", "E-L3-02", "E-L3-03", "E-L3-04", "E-L3-05"})
        self.assertTrue(all(x["knowledge_files"][0] == lead for x in leads))
        self.assertFalse(any(lead in x["knowledge_files"]
                             for x in registry["specialists"] if x["layer"] != "L3"))
        root = Path(__file__).resolve().parents[1]
        text = (root / lead).read_text(encoding="utf-8")
        for e in leads:
            self.assertIn(e["id"], text)
        self.assertIn("真正专家不会", text)
        self.assertIn("市场提问", text)
        self.assertIn("L0–L7", text)
        self.assertIn("概念情境", text)
        self.assertIn("不是", text)

    def test_funding_expert_has_non_generic_mechanism_study(self):
        from pathlib import Path

        registry = load_registry()
        path = "knowledge/domain/L3-E-L3-02-capital-organization-incentives.md"
        funder = next(e for e in registry["specialists"] if e["id"] == "E-L3-02")
        self.assertEqual(funder["knowledge_files"][1], path)
        self.assertFalse(any(path in e["knowledge_files"] for e in registry["specialists"]
                             if e["id"] != "E-L3-02"))
        text = (Path(__file__).resolve().parents[1] / path).read_text(encoding="utf-8")
        for required in ("风险本金", "执行预算", "托管与归集", "LP 资本",
                         "创建者收入", "不同的“真实世界”", "CPMM", "Raydium"):
            self.assertIn(required, text)
        self.assertIn("不是某个真实 Mint", text)
        self.assertIn("不直接证明", text)

    def test_illustrative_cpmm_follower_cost_math_is_self_consistent(self):
        # Strictly fee-free theoretical constant-product model, NOT a market signal.
        x, y = 1_000_000.0, 100.0
        trade_sol = 10.0
        leader_tokens = x * trade_sol / (y + trade_sol)
        x1, y1 = x - leader_tokens, y + trade_sol
        follower_tokens = x1 * trade_sol / (y1 + trade_sol)
        x2, y2 = x1 - follower_tokens, y1 + trade_sol
        self.assertAlmostEqual(leader_tokens, 90909.09090909, places=5)
        self.assertAlmostEqual(follower_tokens, 75757.57575758, places=5)
        self.assertAlmostEqual(follower_tokens / leader_tokens, 5 / 6)
        self.assertAlmostEqual((trade_sol / follower_tokens) /
                               (trade_sol / leader_tokens), 1.2)
        self.assertAlmostEqual((y1 / x1) / (y / x), 1.21)
        self.assertAlmostEqual((y2 / x2) / (y / x), 1.44)
        # A fee-free immediate exact reversal restores the original quote input;
        # price impact alone does not make this round trip lose money.
        recovered_sol = y2 * follower_tokens / (x2 + follower_tokens)
        self.assertAlmostEqual(recovered_sol, trade_sol)

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
