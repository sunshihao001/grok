"""Check portable ChatGPT Project knowledge compiles the existing Meme ontology.

These tests check complete scope, links and epistemic boundaries, not market
truth, actual ChatGPT Project attachment, Grok deployment or trading alpha.
"""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYS = ROOT / "knowledge" / "system"


def j(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class GPTProjectKnowledgeCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = j("knowledge/system/ontology.v1.json")
        cls.atlas = j("knowledge/system/whole-domain-atlas.v1.json")
        cls.experts = j("knowledge/experts/registry.v1.json")
        cls.index = j("knowledge/system/gpt-meme-project-index.v1.json")
        cls.core = (SYS / "gpt-meme-project-core.v1.md").read_text(encoding="utf-8")
        cls.protocol = (SYS / "gpt-meme-knowledge-accumulation.v1.md").read_text(encoding="utf-8")
        cls.instructions = (SYS / "gpt-meme-project-instructions.v1.md").read_text(encoding="utf-8")

    def test_no_new_ontology_and_complete_152_unit_coverage(self):
        self.assertEqual(len(self.ontology["layers"]), 8)
        self.assertEqual(len(self.ontology["domains"]), 12)
        self.assertEqual(len(self.experts["specialists"]), 21)
        self.assertEqual(self.index["counts"]["atomic_units"], 152)
        self.assertEqual(len(self.atlas["core_governance"]), 8)
        self.assertEqual(len(self.atlas["domains"]), 12)
        for item in self.atlas["core_governance"]:
            self.assertIn(item["id"], self.core)
            self.assertIn(item["title"], self.core)
        for d in self.atlas["domains"]:
            self.assertEqual(len(d["units"]), 12)
            self.assertIn(d["id"], self.core)
            for item in d["units"]:
                self.assertIn(item["id"], self.core)
                self.assertIn(item["title"], self.core)
                self.assertIn(item["expert_question"], self.core)
                self.assertIn(item["mechanism_to_study"], self.core)
                self.assertIn(item["forbidden_shortcut"], self.core)
        for e in self.experts["specialists"]:
            self.assertIn(e["id"], self.core)
            self.assertIn(e["name"], self.core)
        self.assertEqual(self.index["counts"]["specialists"], 21)

    def test_index_is_exact_existing_domain_expert_map(self):
        domains={x["id"]:x for x in self.ontology["domains"]}
        atlas={x["id"]:x for x in self.atlas["domains"]}
        self.assertEqual({d["id"] for d in self.index["domain_index"]},set(domains))
        for d in self.index["domain_index"]:
            self.assertEqual(d["name"], domains[d["id"]]["name"])
            self.assertEqual(d["lead"], atlas[d["id"]]["lead_expert_id"])
            self.assertEqual(d["unit_ids"], [x["id"] for x in atlas[d["id"]]["units"]])
        self.assertEqual(self.index["expert_ids"],
                         [e["id"] for e in self.experts["specialists"]])

    def test_project_mirror_never_claims_automatic_project_attachment(self):
        self.assertIn("requires_user_action",self.index["mirror_state"])
        for text in [self.core,self.protocol,self.instructions]:
            self.assertIn("Project",text)
            self.assertIn("GitHub",text)
            self.assertIn("review_only",text)
            self.assertTrue("不是" in text or "不等于" in text)
        self.assertIn("项目",self.core)
        self.assertIn("必须",self.protocol)
        self.assertIn("附加",self.instructions)

    def test_full_domain_mechanisms_and_feedback_cover_project_business(self):
        for keyword in ["批量转账", "同源钱包", "FCZ", "Smart Money",
                        "跟单", "跨Mint", "库存", "152", "向上", "向下",
                        "问题生问题", "B01", "K0/K1/K2", "F0–F6"]:
            self.assertIn(keyword, self.core)
        for keyword in ["D07-K08","D05-K03","D06-K09",
                        "D10-K05","D11-K03","supports","challenges",
                        "supersedes"]:
            self.assertIn(keyword, self.protocol)

    def test_all_sources_and_gpt_entries_are_real_files(self):
        for key in ["classification_source", "atomic_source", "expert_source",
                    "core_mirror", "accumulation_protocol", "instructions",
                    "current_research", "source_admission"]:
            self.assertTrue((ROOT / self.index[key]).is_file(),
                            (key,self.index[key]))
        for p in ["knowledge/README.md","knowledge/system/README.md",
                  "skills/solana-meme-knowledge/SKILL.md","docs/next-steps.md"]:
            text=(ROOT/p).read_text(encoding="utf-8")
            self.assertIn("gpt-meme-project-core.v1.md",text,p)
        self.assertEqual(self.index["current_research_batch"],"B01")
        self.assertIn("pending",self.index["current_research_status"])
        self.assertIn("not_verified",self.index["operational_status"])


if __name__=="__main__":
    unittest.main()
