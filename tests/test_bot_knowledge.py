"""Offline consistency, role retrieval and source-linked handoff regression tests."""
import copy
import json
from pathlib import Path
import unittest

from solana_meme_os.bot_knowledge import (
    ROOT, build_role_brief, validate_handoff, validate_profiles,
)

EXAMPLE=json.loads((ROOT/"fixtures/bot-handoff-brief.fixture.json").read_text(encoding="utf-8"))

class BotKnowledgeTests(unittest.TestCase):
    def test_seven_roles_reuse_pinned_sources(self):
        a=validate_profiles()
        self.assertEqual(a["profiles"],7)
        self.assertEqual(a["selective_k1_source_pointers"],21)
        self.assertGreaterEqual(a["resident_curriculum_topics"],50)
        self.assertFalse(a["cloud_bots_provisioned"])

    def test_role_has_concrete_skill_templates_and_no_live_credentials(self):
        p=json.loads((ROOT/"knowledge/bot-knowledge-profiles.v1.json").read_text(encoding="utf-8"))
        for role in p["profiles"]:
            for skill in role["skills_to_configure"]:
                path=ROOT/"skills"/skill/"SKILL.md"
                self.assertTrue(path.is_file(), str(path))
                body = path.read_text(encoding="utf-8")
                self.assertIn("name:", body)
                if "solana-meme" not in skill:
                    self.assertIn("Paper-Only", body)
                    self.assertIn("not proof of installation", body)

    def test_monitor_is_not_an_autonomous_researcher_or_rule_author(self):
        program=json.loads((ROOT/"knowledge/bot-knowledge-profiles.v1.json").read_text(encoding="utf-8"))
        monitor=next(p for p in program["profiles"] if p["id"]=="B07")
        self.assertEqual(monitor["source_access_mode"],"frozen_context_only_during_routine")
        self.assertNotIn("create_feature_branch_pr",monitor["permitted_actions"])
        monitor["permitted_actions"].append("create_feature_branch_pr")
        with self.assertRaisesRegex(ValueError,"cannot author research"):
            validate_profiles(program=program)

    def test_role_routes_only_role_relevant_materials(self):
        x=build_role_brief("B03","同源钱包和资金回流可能是交易所节点吗")
        ids=[s["source_id"] for s in x["on_demand_source_candidates"]]
        self.assertIn("hermes-source-relations",ids)
        self.assertLessEqual(len(ids),4)
        self.assertTrue(all(x["source_is_not_market_evidence"] for x in x["on_demand_source_candidates"]))
        self.assertFalse(x["can_claim_source_observed"])

    def test_default_role_brief_withholds_review_only_sources(self):
        q = "同源钱包资金回流交易所hub"
        brief = build_role_brief("B03", q)
        self.assertGreater(brief["review_only_source_matches_withheld"], 0)
        self.assertTrue(all(src["admission_state"] == "context_candidate"
                            for src in brief["on_demand_source_candidates"]))
        manual = build_role_brief("B03", q, include_review_only=True)
        self.assertTrue(any(src["admission_state"] == "review_only"
                            for src in manual["on_demand_source_candidates"]))
        with self.assertRaisesRegex(ValueError, "frozen monitor"):
            build_role_brief("B07", q, include_review_only=True)

    def test_unknown_role_or_question_does_not_invent_knowledge(self):
        with self.assertRaisesRegex(ValueError,"unknown Bot"):
            build_role_brief("B99","资金")
        x=build_role_brief("B05","火星奶酪")
        self.assertEqual(x["source_match_state"],"SOURCE_DISCOVERY_REQUIRED")
        self.assertEqual(x["on_demand_source_candidates"],[])

    def test_handoff_example_is_only_structurally_valid(self):
        x=validate_handoff(EXAMPLE)
        self.assertEqual(x["status"],"STRUCTURALLY_VALID_ONLY")
        self.assertFalse(x["verified_market_evidence"])
        self.assertFalse(x["authorized_real_trading"])

    def test_historical_text_cannot_pose_as_raw_chain_observation(self):
        v=copy.deepcopy(EXAMPLE)
        v["claims"][0]["epistemic_status"]="raw_observation"
        with self.assertRaisesRegex(ValueError,"K1 document"):
            validate_handoff(v)

    def test_lookahead_feature_is_rejected_even_with_time_string(self):
        v=copy.deepcopy(EXAMPLE)
        v["claims"][0]["event_at_utc"]="2026-10-29T09:00:03Z"
        v["claims"][0]["available_at_utc"]="2026-10-29T09:00:05Z"
        v["claims"][0]["predictive_feature"]=True
        with self.assertRaisesRegex(ValueError,"lookahead"):
            validate_handoff(v)

    def test_false_gate_pass_is_not_allowed(self):
        v=copy.deepcopy(EXAMPLE)
        v["gate_results"][0]["status"]="PASS_WITH_EVIDENCE"
        with self.assertRaisesRegex(ValueError,"non-fixture"):
            validate_handoff(v)

    def test_real_observation_must_have_explicit_available_at(self):
        v=copy.deepcopy(EXAMPLE)
        v["mode"]="real_observation"
        v["claims"][0]["epistemic_status"]="raw_observation"
        v["source_refs"]=[{"ref_id":"primary-tx","kind":"primary_chain",
                            "source_uri":"solana:signature:fixture-example",
                            "signature_or_slot":"sample-slot"}]
        v["claims"][0]["source_ref_ids"]=["primary-tx"]
        with self.assertRaisesRegex(ValueError,"requires event and available timestamps"):
            validate_handoff(v)

    def test_external_document_alone_cannot_pass_alpha_gate(self):
        v=copy.deepcopy(EXAMPLE)
        v["mode"]="real_observation"
        v["gate_results"]=[{"gate_id":"F4","status":"PASS_WITH_EVIDENCE",
                            "source_ref_ids":["hermes-source-relations"],
                            "reviewer_bot_id":"B05"}]
        with self.assertRaisesRegex(ValueError,"cannot pass from K1 papers alone"):
            validate_handoff(v)

    def test_wrong_bot_cannot_publish_monitor_message(self):
        v=copy.deepcopy(EXAMPLE)
        v["packet_type"]="monitor_observation"
        with self.assertRaisesRegex(ValueError,"wrong Bot"):
            validate_handoff(v)

    def test_proposal_cannot_promote_from_b04_to_monitor(self):
        prog=json.loads((ROOT/"knowledge/bot-knowledge-profiles.v1.json").read_text(encoding="utf-8"))
        p=next(x for x in prog["profiles"] if x["id"]=="B04")
        p["produces_for"].append("B07")
        with self.assertRaisesRegex(ValueError,"directly"):
            validate_profiles(program=prog)

    def test_claim_source_id_must_be_valid(self):
        v=copy.deepcopy(EXAMPLE)
        v["claims"][0]["source_ref_ids"]=["missing-ref"]
        with self.assertRaisesRegex(ValueError,"unknown source"):
            validate_handoff(v)

if __name__=="__main__":
    unittest.main()
