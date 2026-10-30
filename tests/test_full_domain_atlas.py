"""Audit that the expert-first knowledge atlas remains complete, honest and non-deploying."""
import unittest
from pathlib import Path

from solana_meme_os.knowledge_atlas import atlas_audit, load_atlas, select

ROOT = Path(__file__).resolve().parents[1]


class FullDomainKnowledgeAtlasTests(unittest.TestCase):
    def test_all_original_ids_remain_covered_without_truth_promotion(self):
        state = atlas_audit()
        self.assertEqual(state["status"], "STRUCTURALLY_COVERED_MECHANISMS_UNVERIFIED")
        self.assertEqual(state["layers"], 8)
        self.assertEqual(state["domains"], 12)
        self.assertEqual(state["domain_units"], 96)
        self.assertEqual(state["L0_governance_units"], 8)
        self.assertEqual(state["specialists_referenced"], 21)
        self.assertEqual(state["bot_owners"], 7)
        self.assertEqual(state["legacy_competences_referenced"], 52)
        self.assertEqual(state["legacy_cards_referenced"], 15)
        self.assertFalse(state["market_alpha_verified"])
        self.assertFalse(state["grok_bots_provisioned"])

    def test_each_domain_has_eight_distinct_expert_mechanisms(self):
        data = load_atlas()
        self.assertEqual(data["status"], "research_content_drafted_not_market_validated")
        for d in data["domains"]:
            doc = (ROOT / d["atlas_document"]).read_text(encoding="utf-8")
            for uid in d["units"]:
                matching = [u for u in data["units"] if u["id"] == uid]
                self.assertEqual(len(matching), 1)
                self.assertIn(uid + "｜", doc)
                self.assertIn(matching[0]["title"], doc)
                self.assertIn(matching[0]["mechanism"], doc)
                self.assertIn(matching[0]["invalid_inference"], doc)
                self.assertTrue(matching[0]["state"].endswith("unverified_market"))

    def test_cross_domain_knowledge_and_l0_are_not_disconnected(self):
        cross = (ROOT / "knowledge/atlas/cross-domain-chains.md").read_text(encoding="utf-8")
        l0 = (ROOT / "knowledge/atlas/L0-governance.md").read_text(encoding="utf-8")
        readme = (ROOT / "knowledge/atlas/README.md").read_text(encoding="utf-8")
        for i in range(1, 13):
            self.assertIn(f"X{i:02d}｜", cross)
            self.assertIn(f"[D{i:02d} ", readme)
            self.assertTrue((ROOT / f"knowledge/atlas/D{i:02d}.md").is_file())
        for i in range(1, 9):
            self.assertIn(f"L0-{i:02d}｜", l0)
        self.assertIn("不等于", readme)
        self.assertIn("review_only", (ROOT / "knowledge/atlas/source-coverage-and-gaps.md").read_text(encoding="utf-8"))

    def test_offline_select_domain_atom_and_expert_never_claims_trade(self):
        d = select(domain="D03", limit=8)
        self.assertEqual(d["total_matches"], 8)
        self.assertTrue(d["not_authorized_to_trade"])
        self.assertEqual({x["domain_id"] for x in d["units"]}, {"D03"})
        x = select(unit="D05-01")
        self.assertEqual(x["total_matches"], 1)
        self.assertEqual(x["units"][0]["id"], "D05-01")
        by_expert = select(expert="E-L3-02", domain="D05")
        self.assertEqual(by_expert["total_matches"], 8)
        self.assertEqual({x["domain_id"] for x in by_expert["units"]}, {"D05"})
        self.assertEqual(select(expert="E-L3-02", domain="D03")["total_matches"], 0)

    def test_bad_requests_fail_without_guessing_a_domain_or_expert(self):
        for keyword in ({"domain": "D13"}, {"unit": "D07-99"},
                        {"expert": "E-L99-99"}, {"limit": 0}, {"limit": 97}):
            with self.assertRaises(ValueError):
                select(**keyword)


if __name__ == "__main__":
    unittest.main()
