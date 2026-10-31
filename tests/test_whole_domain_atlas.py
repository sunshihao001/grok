"""Offline structural checks for complete scope inventory, not empirical validity."""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "knowledge/system/whole-domain-atlas.v1.json"
ONTOLOGY_PATH = ROOT / "knowledge/system/ontology.v1.json"
EXPERTS_PATH = ROOT / "knowledge/experts/registry.v1.json"
HANDBOOK_PATH = ROOT / "knowledge/system/whole-domain-expert-handbook.md"


class WholeDomainKnowledgeAtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.atlas = json.loads(ATLAS_PATH.read_text(encoding="utf-8"))
        cls.ontology = json.loads(ONTOLOGY_PATH.read_text(encoding="utf-8"))
        cls.experts = json.loads(EXPERTS_PATH.read_text(encoding="utf-8"))["specialists"]
        cls.handbook = HANDBOOK_PATH.read_text(encoding="utf-8")

    def test_existing_ontology_and_21_specialists_unchanged(self):
        self.assertEqual({x["id"] for x in self.atlas["domains"]},
                         {x["id"] for x in self.ontology["domains"]})
        self.assertEqual({x["id"] for x in self.ontology["layers"]},
                         {f"L{i}" for i in range(8)})
        self.assertEqual(len(self.experts), 21)
        self.assertTrue(all(e["kind"] == "internal_specialist_lens_not_installed_bot"
                            for e in self.experts))

    def test_all_domains_have_twelve_distinct_molecular_questions(self):
        self.assertEqual(len(self.atlas["domains"]), 12)
        self.assertEqual(len(self.atlas["core_governance"]), 8)
        all_units = list(self.atlas["core_governance"])
        for domain in self.atlas["domains"]:
            self.assertEqual(len(domain["units"]), 12, domain["id"])
            self.assertEqual(domain["coverage"], "catalogued_partial_mechanism_depth")
            for unit in domain["units"]:
                self.assertEqual(unit["domain"], domain["id"])
                self.assertTrue(unit["id"].startswith(domain["id"] + "-K"))
                self.assertTrue(unit["title"])
                self.assertGreaterEqual(len(unit["expert_question"]), 9)
                self.assertGreaterEqual(len(unit["mechanism_to_study"]), 9)
                self.assertGreaterEqual(len(unit["forbidden_shortcut"]), 6)
                self.assertEqual(unit["research_state"], "mapped_unverified")
                self.assertTrue((ROOT / unit["source_anchor"]).is_file(), unit["id"])
            all_units += domain["units"]
        self.assertEqual(len(all_units), 152)
        self.assertEqual(len({u["id"] for u in all_units}), 152)
        self.assertEqual(len({u["title"] for u in all_units}), 152)
        self.assertEqual(self.atlas["status"],
                         "exhaustive_scope_inventory_not_complete_research")

    def test_all_21_experts_are_covered_by_an_existing_domain(self):
        names = {e["id"] for e in self.experts}
        referred = set()
        for domain in self.atlas["domains"]:
            self.assertIn(domain["lead_expert_id"], names)
            self.assertTrue((ROOT / domain["existing_anchor"]).is_file())
            self.assertFalse(set(domain["support_expert_ids"]) - names)
            referred.update([domain["lead_expert_id"],
                             *domain["support_expert_ids"]])
            self.assertTrue(all(unit["primary_expert_id"] ==
                                domain["lead_expert_id"]
                                for unit in domain["units"]))
        referred.update(u["primary_expert_id"]
                        for u in self.atlas["core_governance"])
        self.assertEqual(referred, names)

    def test_handbook_has_all_twelve_domain_sections_and_capability_boundary(self):
        for domain in self.atlas["domains"]:
            self.assertIn("### " + domain["id"], self.handbook)
        self.assertIn("结构目录完整", self.atlas["definition_of_done"])
        self.assertIn("尚未完成", self.handbook)
        self.assertIn("不是 21 个已安装 Bot", self.handbook)
        self.assertIn("全域定位与缺口暴露", self.handbook)
        self.assertIn("K0", self.handbook)
        self.assertIn("K1", self.handbook)
        self.assertIn("K2", self.handbook)

    def test_cross_domain_mechanisms_not_silently_upgraded_to_rules(self):
        self.assertGreaterEqual(len(self.atlas["cross_domain_requirements"]), 7)
        self.assertIn("empirical_hypothesis", self.atlas["separation"])
        self.assertIn("approved_readonly_rule", self.atlas["separation"])
        self.assertTrue(all(u["research_state"] == "mapped_unverified"
                            for domain in self.atlas["domains"]
                            for u in domain["units"]))


if __name__ == "__main__":
    unittest.main()
