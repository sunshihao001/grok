"""Regression tests for bounded knowledge navigation; no remote or trading calls."""
from __future__ import annotations

import copy
import unittest

from solana_meme_os import project_navigator as nav


class NavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = nav.load_navigation()

    def test_all_local_links_and_registered_ids(self):
        result = nav.audit(self.data)
        self.assertTrue(result["ok"], result["errors"])
        self.assertGreaterEqual(result["local_paths_checked"], 15)
        self.assertEqual(result["remote_engineering_paths_unchecked"], 10)

    def test_integrated_checkout_connects_existing_knowledge_to_real_code(self):
        # Source file existence is NOT live API, financial validity or Grok execution.
        for intent, fragment in [("WALLET_ACTORS", "public_wallet_rpc_sample.py"),
                                 ("MINT_OVERVIEW", "vendor_event_handoff.py")]:
            found = nav.shortlist("", self.data, intent=intent)["routes"][0]
            matches = [x for x in found["engineering_candidates_on_separate_branch"]
                       if fragment in x["path"]]
            self.assertEqual(len(matches), 1)
            self.assertTrue(matches[0]["available_in_current_checkout"])
            self.assertFalse(matches[0]["invoked"])
            self.assertTrue(matches[0]["checkout_is_not_runtime_validation"])

    def test_wallet_funding_and_batch_question(self):
        found = nav.shortlist("一批钱包同时转账，可能有同源资金吗", self.data, limit=5)
        selected = {x["intent"] for x in found["routes"]}
        self.assertIn("FUNDING_ENTITY", selected)
        self.assertIn("ANOMALY_TIME", selected)

    def test_design_routes_to_product_not_fake_implementation(self):
        found = nav.shortlist("UI设计与项目整体页面布局怎么做", self.data)
        self.assertEqual(found["routes"][0]["intent"], "PRODUCT_UI")
        self.assertTrue(all(
            item["invoked"] is False
            for r in found["routes"] for item in r["engineering_candidates_on_separate_branch"]
        ))

    def test_research_question_not_forced_into_development(self):
        found = nav.shortlist("经济机制推演以及反证", self.data)
        self.assertEqual(found["routes"][0]["intent"], "MECHANISM_RESEARCH")
        self.assertEqual(found["routes"][0]["engineering_candidates_on_separate_branch"], [])

    def test_explicit_intent_overrides_literal_ranking(self):
        found = nav.shortlist("", self.data, intent="GROK_OPERATION")
        self.assertEqual(found["match_kind"], "explicit_intent")
        self.assertEqual(found["routes"][0]["intent"], "GROK_OPERATION")

    def test_unknown_question_requires_real_reasoning(self):
        found = nav.shortlist("这事我说不清楚", self.data)
        self.assertTrue(found["no_match"])
        self.assertEqual(found["routes"], [])

    def test_unknown_reference_is_not_silently_accepted(self):
        bad = copy.deepcopy(self.data)
        bad["routes"][0]["reference_ids"].append("REF-NONEXISTENT")
        result = nav.audit(bad)
        self.assertFalse(result["ok"])
        self.assertTrue(any("REF-NONEXISTENT" in x for x in result["errors"]))

    def test_missing_file_is_reported(self):
        bad = copy.deepcopy(self.data)
        bad["routes"][0]["knowledge_files"].append("knowledge/no-such-file.md")
        self.assertFalse(nav.audit(bad)["ok"])

    def test_branch_authority_not_merged(self):
        bad = copy.deepcopy(self.data)
        bad["branches"]["engineering"] = bad["branches"]["knowledge"]
        self.assertTrue(any("conflated" in x for x in nav.audit(bad)["errors"]))

    def test_original_research_can_be_read_with_hash(self):
        result = nav.open_knowledge("knowledge/system/current-operating-guidance.md", self.data)
        self.assertIn("AI思维", result["excerpt"])
        self.assertEqual(len(result["source_sha256"]), 64)

    def test_unregistered_file_cannot_be_opened(self):
        with self.assertRaises(ValueError):
            nav.open_knowledge("AGENTS.md", self.data)

    def test_natural_language_route_regressions(self):
        # Shortlist regression only; these examples do not validate expert reasoning.
        cases = [
            ("Top10持仓很多但里面可能是池子地址", "SUPPLY_CONTROL"),
            ("多个地址反复在不同新币中一起出现，有什么隐藏关系", "FUNDING_ENTITY"),
            ("我想知道链上交易原始指令能不能还原真实买卖", "DATA_SEMANTICS"),
            ("这套系统的首页应该显示什么数据和入口", "PRODUCT_UI"),
        ]
        for question, expected in cases:
            with self.subTest(question=question):
                got = nav.shortlist(question, self.data, limit=3)["routes"]
                self.assertTrue(got, question)
                self.assertEqual(got[0]["intent"], expected)

    def test_out_of_scope_id_fails(self):
        with self.assertRaises(ValueError):
            nav.shortlist("", self.data, intent="AUTOTRADE")


if __name__ == "__main__":
    unittest.main()
