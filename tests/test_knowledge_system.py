import copy
import unittest
from solana_meme_os.knowledge_system import read, validate_system, route_domains, filter_plan

class KnowledgeSystemTests(unittest.TestCase):
    def test_full_structural_map(self):
        report = validate_system()
        self.assertEqual((report["layers"], report["domains"], report["legacy_cards_mapped"]), (8, 12, 15))
        self.assertEqual(report["external_units"], 3)
        self.assertIn("D01", report["gaps"])
        self.assertIn("D07", report["gaps"])
        self.assertFalse(report["production_trading_authorized"])

    def test_cross_domain_route(self):
        result = route_domains("跟单资金网络滑点退出成本")
        self.assertEqual(result["status"], "DOMAIN_MATCH")
        self.assertIn("D05", result["matched_domains"])
        self.assertIn("D08", result["matched_domains"])
        self.assertIn("D09", result["matched_domains"])
        self.assertIn("D01", result["required_domains"])

    def test_unknown_is_a_gap_not_answer(self):
        r = route_domains("火星羊奶酪")
        self.assertEqual(r["status"], "RESEARCH_GAP")
        self.assertEqual(r["legacy_card_ids"], [])

    def test_source_must_be_pinned(self):
        sources = copy.deepcopy(read("source-registry.v1.json"))
        sources["source_entries"][0]["commit"] = "main"
        with self.assertRaisesRegex(ValueError, "pinned"):
            validate_system(sources=sources)

    def test_external_findings_never_auto_promote(self):
        units = copy.deepcopy(read("research-units.v1.json"))
        units["units"][0]["runtime_policy"] = "approved_monitor_only"
        with self.assertRaisesRegex(ValueError, "self-promote"):
            validate_system(units=units)

    def test_catalog_drift_fails(self):
        ontology = copy.deepcopy(read("ontology.v1.json"))
        ontology["domains"][0]["primary_card_ids"] = ["phantom"]
        ontology["domains"][0]["coverage"] = "legacy_seeded_unverified"
        with self.assertRaisesRegex(ValueError, "mapping"):
            validate_system(ontology=ontology)

    def test_packets_reuse_ontology_without_promoting_reports(self):
        from solana_meme_os.research import build_packet
        packet = build_packet("钱包协调以后，跟单能赚钱吗？利润和成本如何判断")
        self.assertIn("D08", packet["ontology_route"]["matched_domains"])
        self.assertIn("D09", packet["ontology_route"]["matched_domains"])
        self.assertTrue(packet["research_unit_candidates"])
        self.assertTrue(all(x["runtime_policy"] == "research_reference_only"
                            for x in packet["research_unit_candidates"]))

    def test_on_demand_source_pins_match(self):
        self.assertEqual(validate_system()["on_demand_source_pointers"], 17)

    def test_strategy_route_does_not_force_wallet_conspiracy(self):
        r = route_domains("跟单")
        self.assertIn("D08", r["required_domains"])
        self.assertNotIn("D05", r["required_domains"])
        self.assertNotIn("D06", r["required_domains"])
        self.assertIn("D05", r["contextual_domain_candidates"])

    def test_time_context_and_social_attention_are_searchable(self):
        r = route_domains("社交叙事注意力变化")
        self.assertIn("D07", r["matched_domains"])
        self.assertNotIn("D05", r["required_domains"])

    def test_statistical_method_can_be_studied_without_execution(self):
        r = route_domains("反证回测")
        self.assertEqual(r["required_domains"], ["D11"])
        self.assertEqual(r["crosscut_evidence_controls"], ["D10", "D11"])

    def test_gate_plan_never_self_approves(self):
        v = filter_plan("ECONOMIC")
        self.assertEqual(len(v["gates"]), 7)
        self.assertEqual([g["id"] for g in v["gates"] if g["required_for_objective"]],
                         ["F0", "F1", "F2", "F3", "F4", "F5"])
        self.assertTrue(all(g["status"] != "PASS_WITH_EVIDENCE" for g in v["gates"]))
        self.assertFalse(v["automatic_rule_promotion"])
        self.assertEqual(filter_plan("EXPLAIN")["gates"][5]["status"], "NOT_APPLICABLE")

    def test_wrong_filter_objective_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown"):
            filter_plan("BYPASS")

    def test_research_packet_receives_unassessed_evidence_gates(self):
        from solana_meme_os.research import build_packet
        p = build_packet("同源资金能跟单吗？")
        self.assertEqual(len(p["filter_plan"]["gates"]), 7)
        self.assertTrue(all(g["status"] == "NOT_EVALUATED" for g in p["filter_plan"]["gates"]))

    def test_cycles_fail(self):
        ontology = copy.deepcopy(read("ontology.v1.json"))
        ontology["domains"][0]["depends_on"] = ["D02"]
        with self.assertRaisesRegex(ValueError, "cyclic"):
            validate_system(ontology=ontology)
if __name__ == "__main__":
    unittest.main()
