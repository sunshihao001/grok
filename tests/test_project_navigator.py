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
        self.assertEqual(result["remote_engineering_paths_unchecked"], 8)

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

    def test_real_multihop_shared_service_query_starts_with_funding_identity(self):
        # Known baseline failure: "一批" made ANOMALY_TIME rank above the
        # economic identity investigation; routing is only a shortlist.
        q = "一批多跳资金钱包到底同控，还是共用交易服务？"
        found = nav.shortlist(q, self.data, limit=3)
        self.assertEqual(found["routes"][0]["intent"], "FUNDING_ENTITY")
        self.assertIn("knowledge/domain/L3-actor-economic-mechanisms-deepstudy.md",
                      found["routes"][0]["knowledge_paths_on_current_branch"])
        self.assertIn("knowledge/system/legacy-meme-multihop-deep-audit-2026-11-02.md",
                      found["routes"][0]["knowledge_paths_on_current_branch"])
        self.assertEqual(found["match_kind"], "literal_cue_candidates_not_semantic_routing")

    def test_real_provider_reuse_query_starts_with_implementation_evidence(self):
        # Prior ties allowed funding theory to outrank vendor capability review.
        q = "OKX GMGN Bubblemaps如何复用到V0.2钱包资金报告"
        found = nav.shortlist(q, self.data, limit=3)
        self.assertEqual(found["routes"][0]["intent"], "SOURCE_REUSE")
        self.assertIn("E-L7-03", found["routes"][0]["expert_lens_ids"])
        self.assertIn("knowledge/system/reference-capability-reuse-ledger.v1.md",
                      found["routes"][0]["knowledge_paths_on_current_branch"])
        self.assertTrue(all(
            not item["invoked"]
            for route in found["routes"]
            for item in route["engineering_candidates_on_separate_branch"]
        ))

    def test_governance_maintenance_question_uses_current_rules_not_old_stage(self):
        q = ("继续 Solana Meme 项目，原位优化现有专家、知识调用与持续推进制度，"
             "清除重复和冲突约束，保留专业知识与可靠证据，并通过实际任务检验改进效果")
        found = nav.shortlist(q, self.data, limit=3)
        self.assertEqual(found["routes"][0]["intent"], "KNOWLEDGE_MANAGEMENT")
        files = found["routes"][0]["knowledge_paths_on_current_branch"]
        self.assertIn("knowledge/system/current-operating-guidance.md", files)
        self.assertIn("knowledge/system/gpt-meme-progress-current.md", files)
        self.assertIn("knowledge/experts/registry.v1.json", files)

    def test_extended_real_mechanism_routing_cases(self):
        # Fixed cases sourced from recurring Solana Meme project questions.
        # This tests candidate selection, NOT economic inference or an LLM A/B.
        cases = [
            ("原Holder把Token转给另外20个新钱包，但没有Swap，算出货了吗？",
             "SUPPLY_CONTROL", "knowledge/domain/L3-actor-economic-mechanisms-deepstudy.md"),
            ("收款钱包与资金中转Hub共同签名能证明由一个人掌握全部私钥吗？",
             "FUNDING_ENTITY", "knowledge/domain/L3-actor-economic-mechanisms-deepstudy.md"),
            ("Solana v1交易中Token Account owner、fee payer和signer不同，如何计算真实Swap成本？",
             "DATA_SEMANTICS", "knowledge/domain/L1-L2-chain-market.md"),
            ("OKX holderSameFundSourcePercent 是否可以证明这些钱包属于同一经济主体？",
             "DATA_SEMANTICS", "knowledge/system/legacy-meme-multihop-deep-audit-2026-11-02.md"),
            ("Why-Solana五跳资金追踪只递归最大转出分支，会遗漏小额钱包吗？",
             "FUNDING_ENTITY", "knowledge/system/legacy-meme-multihop-deep-audit-2026-11-02.md"),
            ("Why-Solana FN冻结表记载409条下游路径但报告408条，是哪里去重？",
             "DATA_SEMANTICS", "knowledge/system/legacy-meme-multihop-deep-audit-2026-11-02.md"),
            ("GMGN smart money盈利率高的钱包可以直接跟单赚钱吗？",
             "TRADING_ECONOMICS", "knowledge/domain/L6-L7-investigation-cases.md"),
            ("继续项目，去掉强制专家会诊和固定进度模板，但保留所有旧专业知识",
             "KNOWLEDGE_MANAGEMENT", "knowledge/system/current-operating-guidance.md"),
            ("GMGN bundler钱包和Jito Bundle是不是一回事？",
             "DATA_SEMANTICS", "knowledge/domain/meme-anomaly-discovery-state.v1.md"),
            ("群体停止交易后，同批资金转仓到新Mint，如何区分迁移与普通退出？",
             "FUNDING_ENTITY", "knowledge/domain/meme-anomaly-discovery-state.v1.md"),
        ]
        for question, intent, original_source in cases:
            with self.subTest(question=question):
                out = nav.shortlist(question, self.data, limit=3)
                self.assertTrue(out["routes"], question)
                self.assertEqual(out["routes"][0]["intent"], intent)
                self.assertIn(original_source, out["routes"][0]["knowledge_paths_on_current_branch"])
                # A shortlist is not an API call, expert Bot, or runtime proof.
                self.assertTrue(all(not e["invoked"] for route in out["routes"]
                                    for e in route["engineering_candidates_on_separate_branch"]))

    def test_mechanism_routing_changes_do_not_swallow_unrelated_goals(self):
        unchanged_cases = [
            ("这套系统的首页应该显示什么数据和入口", "PRODUCT_UI"),
            ("Top10持仓很多但里面可能是池子地址", "SUPPLY_CONTROL"),
            ("我想知道链上交易原始指令能不能还原真实买卖", "DATA_SEMANTICS"),
            ("检查创建者Dev以前发过哪些代币", "CREATOR_LIFECYCLE"),
        ]
        for question, intent in unchanged_cases:
            with self.subTest(question=question):
                self.assertEqual(nav.shortlist(question, self.data)["routes"][0]["intent"], intent)

    def test_unseen_paraphrases_are_marked_weak_not_mistaken_for_understanding(self):
        # Held-out wording: only two of nine happen to rank the intended
        # specialist first; do NOT extend the cue list to manufacture 9/9.
        paraphrases = [
            "一种代币从A的ATA移动到B的ATA，DEX并没有成交，算已经抛售了吗？",
            "交易所作为中间节点，出入账金额差不多，可以认定背后同一个人吗？",
            "同slot的五笔机器人买入是否一定属于Jito打包？",
            "OKX统计前一千名持币者彼此转主流币的比例，能推断资金出自一个人吗？",
            "一组地址在某币上停止活动，过两天换一组新地址出现在新币上，算资金接力吗？",
            "这几个账户互相转币，集团库存实际有减少吗？",
            "为什么榜单显示某个聪明钱很赚，普通人复制他的交易却亏？",
            "对照代码，原报告记录路径条数不同，如何排查重复计数？",
            "Meme研究体系还要全员会诊吗，还是按情况深入？",
        ]
        for q in paraphrases:
            with self.subTest(question=q):
                out = nav.shortlist(q, self.data, limit=3)
                self.assertTrue(out["weak_literal_match"])
                self.assertIn("AI must determine intent", out["weak_literal_match_note"])
                self.assertEqual(out["match_kind"], "literal_cue_candidates_not_semantic_routing")

    def test_explicit_intent_is_not_a_lexical_guess(self):
        out = nav.shortlist("unexpected phrasing", self.data, intent="DATA_SEMANTICS")
        self.assertFalse(out["weak_literal_match"])
        self.assertEqual(out["match_kind"], "explicit_intent")

    def test_out_of_scope_id_fails(self):
        with self.assertRaises(ValueError):
            nav.shortlist("", self.data, intent="AUTOTRADE")


if __name__ == "__main__":
    unittest.main()
