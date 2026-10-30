"""Offline guardrails for staged GPT -> GitHub -> Grok teaching."""
import copy
import json
import unittest
from solana_meme_os.knowledge_delivery import ROOT, audit, plan

class KnowledgeDeliveryTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/"knowledge/transfer/curriculum.v1.json").read_text(encoding="utf-8"))

    def test_curated_lessons_start_as_draft_not_auto_published(self):
        stats=audit()
        self.assertGreaterEqual(stats["learning_units"],1)
        self.assertEqual(stats["approved_for_study"],0)
        self.assertEqual(stats["market_claims_verified"],False)

    def test_role_preview_exposes_only_targeted_draft(self):
        self.assertEqual(plan("B01","C1")["learning_units"],[])
        preview=plan("B01","C1",include_drafts=True)
        self.assertEqual(len(preview["learning_units"]),1)
        self.assertTrue(preview["learning_units"][0]["for_preview_only"])
        self.assertEqual(plan("B07","C4",True)["learning_units"],[])

    def test_lesson_does_not_promote_production_trading(self):
        altered=copy.deepcopy(self.data)
        altered["units"][0]["monitor_rule_authorized"]=True
        with self.assertRaisesRegex(ValueError,"may not validate"):
            audit(altered)

    def test_draft_cannot_claim_owner_approval(self):
        altered=copy.deepcopy(self.data)
        altered["units"][0]["approval_ref"]="claim-but-no-review"
        with self.assertRaisesRegex(ValueError,"draft cannot claim"):
            audit(altered)

    def test_approved_lesson_requires_review_reference(self):
        altered=copy.deepcopy(self.data)
        altered["units"][0]["status"]="approved_for_study"
        with self.assertRaisesRegex(ValueError,"approval reference required"):
            audit(altered)

    def test_path_escape_fails(self):
        altered=copy.deepcopy(self.data)
        altered["units"][0]["knowledge_path"]="../README.md"
        with self.assertRaisesRegex(ValueError,"traversal|unsafe"):
            audit(altered)

    def test_unknown_roles_or_levels_fail(self):
        with self.assertRaisesRegex(ValueError,"unknown Bot"):
            plan("B99","C2")
        with self.assertRaisesRegex(ValueError,"unknown learning level"):
            plan("B01","C7")

    def test_self_dependency_rejected(self):
        altered=copy.deepcopy(self.data)
        altered["units"][0]["prerequisite_unit_ids"]=["C1-001"]
        with self.assertRaisesRegex(ValueError,"self prerequisite"):
            audit(altered)

    def test_unknown_domains_fails(self):
        altered=copy.deepcopy(self.data)
        altered["units"][0]["domain_ids"]=["D99"]
        with self.assertRaisesRegex(ValueError,"domains"):
            audit(altered)

if __name__=="__main__":
    unittest.main()
