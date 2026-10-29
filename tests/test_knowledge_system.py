import copy
import unittest
from solana_meme_os.knowledge_system import read, validate_system, route_domains

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

    def test_cycles_fail(self):
        ontology = copy.deepcopy(read("ontology.v1.json"))
        ontology["domains"][0]["depends_on"] = ["D12"]
        with self.assertRaisesRegex(ValueError, "cyclic"):
            validate_system(ontology=ontology)
if __name__ == "__main__":
    unittest.main()
