"""Research method integrity: actual domain ontology stays the source of truth.

These checks test planning/document routing only. They do not validate market hypotheses,
protocol behavior in production, profitability or Grok cloud deployment.
"""
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class MechanismFirstMethodTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = read_json("knowledge/system/mechanism-research-plan.v1.json")
        cls.atlas = read_json("knowledge/system/whole-domain-atlas.v1.json")
        cls.ontology = read_json("knowledge/system/ontology.v1.json")
        cls.registry = read_json("knowledge/experts/registry.v1.json")
        cls.units = {
            unit["id"]
            for unit in cls.atlas["core_governance"] +
            [u for domain in cls.atlas["domains"] for u in domain["units"]]
        }
        cls.experts = {s["id"] for s in cls.registry["specialists"]}

    def test_method_uses_existing_taxonomy_and_evidence_gates(self):
        sources = self.plan["source_of_truth"]
        self.assertEqual(sources["ontology"], "knowledge/system/ontology.v1.json")
        self.assertEqual(sources["units"], "knowledge/system/whole-domain-atlas.v1.json")
        self.assertEqual(sources["specialists"], "knowledge/experts/registry.v1.json")
        for p in sources.values():
            self.assertTrue((ROOT / p).is_file(), p)
        self.assertEqual(len(self.atlas["domains"]), len(self.ontology["domains"]))
        self.assertEqual(len(self.experts), 21)
        self.assertEqual(len(self.units), 152)
        self.assertEqual(self.plan["status"], "draft_knowledge_workplan_not_executed")
        self.assertEqual(self.plan["default_mode"],
                         "GPT_theory_first_with_protocol_primary_sources")

    def test_roadmap_selects_one_lead_and_real_cross_domain_challenges(self):
        tracks = self.plan["tracks"]
        self.assertEqual([x["id"] for x in tracks],
                         ["M01", "M02", "M03", "M04", "F01"])
        for track in tracks:
            self.assertIn(track["lead"], self.experts)
            self.assertTrue(set(track["challengers"]) <= self.experts)
            self.assertNotIn(track["lead"], track["challengers"])
            self.assertTrue(set(track["focus_units"]) <= self.units)
            self.assertTrue(set(track["on_demand_primitives"]) <= self.units)
            self.assertGreater(len(set(track["focus_units"])), 1)
            self.assertGreater(len(track["competitive_worlds"]), 1)
            self.assertGreater(len(track["condition_changes"]), 1)
            self.assertTrue(track["root_question"])
            self.assertTrue(track["depth_breakthrough"])
            self.assertTrue(track["ready_when"])
        self.assertEqual(tracks[0]["lead"], "E-L4-02")
        self.assertEqual(tracks[0]["status"], "next_planned_not_started")
        self.assertIn("D04-K02", tracks[0]["focus_units"])
        self.assertIn("D05-K02", tracks[0]["focus_units"])
        self.assertIn("D06-K05", tracks[0]["focus_units"])
        self.assertIn("D07-K11", tracks[0]["focus_units"])
        self.assertIn("D09-K01", tracks[0]["focus_units"])

    def test_maturity_boundaries_and_no_production_promotion(self):
        self.assertTrue(all(unit["research_state"] == "mapped_unverified"
                            for domain in self.atlas["domains"]
                            for unit in domain["units"]))
        self.assertTrue(all(x["status"].startswith(("next_planned", "planned", "parallel"))
                            for x in self.plan["tracks"]))
        review = self.plan["review_separation"]
        self.assertIn("not_empirical_proof", review["theory_completion"])
        self.assertIn("F4_F5", review["empirical_claim"])
        self.assertIn("F6", review["monitor_publish"])
        self.assertTrue(self.plan["separate_operations_track"]["status"].startswith(
            "Grok_cloud_S1_not_verified"))

    def test_research_method_and_d03_brief_are_reachable(self):
        method = ROOT / self.plan["method"]
        self.assertTrue(method.is_file())
        method_text = method.read_text(encoding="utf-8")
        for keyword in ["152", "主专家", "向下挖", "向上推", "条件反转",
                        "知识单元", "回填", "F0–F6"]:
            self.assertIn(keyword, method_text)
        brief = ROOT / self.plan["first_project_mechanism_brief"]
        self.assertTrue(brief.is_file())
        text = brief.read_text(encoding="utf-8")
        for keyword in ["E-L4-02", "M01", "关键钱包", "Bundler",
                        "D05", "D06", "D09", "next_planned_not_started"]:
            self.assertIn(keyword, text)
        self.assertIn("真正完成研究时", text)
        self.assertIn("尚未撰写", text)
        old_d03 = (ROOT / self.plan["previous_d03_brief"]).read_text(
            encoding="utf-8")
        self.assertIn("技术辅稿", old_d03)
        self.assertIn("不再决定研究执行顺序", old_d03)
        origin_audit = (ROOT / self.plan["project_origin_audit"]).read_text(
            encoding="utf-8")
        for term in ["Hermes", "meme-", "qb-", "Why-Solana",
                     "review_only", "关键钱包", "项目原点"]:
            self.assertIn(term, origin_audit)
        for p in ["knowledge/README.md", "knowledge/domain/README.md",
                  "knowledge/system/README.md", "knowledge/experts/README.md",
                  "skills/solana-meme-knowledge/SKILL.md",
                  "docs/next-steps.md"]:
            t = (ROOT / p).read_text(encoding="utf-8")
            self.assertIn("expert-mechanism-research-method.md", t, p)


    def test_reference_knowledge_is_integrated_in_bounded_batches(self):
        integration = self.plan["integration_mode"]
        self.assertEqual(integration["approach"], "rolling_vertical_slices")
        self.assertEqual(
            integration["within_batch"],
            ["source_understanding", "cross_project_expert_synthesis",
             "reviewed_Grok_knowledge_compilation"],
        )
        self.assertEqual(integration["parallel_wip_limits"]["main_expert_research"], 1)
        self.assertEqual(integration["parallel_wip_limits"]["next_batch_source_audit"], 1)
        self.assertEqual(integration["parallel_wip_limits"]["previous_batch_reviewed_compilation"], 1)
        self.assertTrue(integration["no_global_repository_bulk_migration"])
        self.assertTrue(integration["not_a_new_ontology"])
        self.assertEqual([b["id"] for b in integration["batches"]],
                         ["B01", "B02", "B03", "B04", "B05"])
        self.assertEqual(integration["batches"][0]["lead"], "E-L4-02")
        self.assertEqual(integration["batches"][0]["related_track"], "M01")
        self.assertNotEqual(integration["batches"][0]["status"], "completed")
        for batch in integration["batches"]:
            self.assertIn(batch["lead"], self.experts)
            self.assertGreaterEqual(len(batch["connects"]), 2)
            self.assertTrue(batch["topic"])
            self.assertNotEqual(batch["status"], "completed")
        playbook = ROOT / self.plan["integration_method"]
        self.assertTrue(playbook.is_file())
        text = playbook.read_text(encoding="utf-8")
        for phrase in ["原资料理解", "专家融合", "Grok知识编译",
                       "Why-Solana", "review_only", "B01", "B05"]:
            self.assertIn(phrase, text)
        self.assertIn("rolling-reference-knowledge-integration.md",
                      (ROOT / "docs/next-steps.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
