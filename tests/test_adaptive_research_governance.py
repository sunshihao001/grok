"""Task-shaped regressions for Solana Meme V1.1 governance.

These checks exercise the existing deterministic routing/approval boundaries and
whether the instructions still force obsolete steps. They do NOT evaluate the
quality of GPT reasoning, the truth of market hypotheses, or a running Grok Bot.
"""
import json
from pathlib import Path
import unittest

from solana_meme_os.expert_brief import recommend_experts
from solana_meme_os.knowledge_system import filter_plan, route_domains

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class AdaptiveResearchGovernanceTests(unittest.TestCase):
    def test_actual_expert_inventory_remains_intact_but_nonmandatory(self):
        registry = json.loads(read("knowledge/experts/registry.v1.json"))
        self.assertEqual(len(registry["specialists"]), 22)
        self.assertTrue(registry["expert_is_not_bot"])
        self.assertTrue(all(x["evidence_status"] for x in registry["specialists"]))
        activation = registry["activation"]
        self.assertIn("zero specialists is valid", activation)
        self.assertIn("never a mandatory", activation.lower())
        self.assertNotIn("scan every currently registered", activation)
        self.assertNotIn("For isolated mechanisms select 1–3", activation)

    def test_project_prompt_preserves_research_while_removing_compulsory_roles(self):
        text = read("knowledge/system/gpt-meme-project-instructions.v1.md")
        active = text.split("## 指令正文（可直接用于 Project Instructions）")[1].split("## 知识和实际工作入口")[0]
        self.assertLess(len(active), 2300, "short prompt must not become the whole knowledge system")
        for word in ("Solana Meme", "22专家视角", "152问题", "65参考项目",
                     "按信息价值", "自主", "来源", "UNKNOWN", "GitHub", "Grok"):
            self.assertIn(word, active)
        for forced in ("由最适合的一个专家主导", "全员会诊", "每轮必须",
                       "必须完整承担", "固定进度块"):
            if forced == "固定进度块":
                # The string may appear only as a negative statement.
                self.assertIn("不强制22专家会诊、P1–P6阶段、每轮进度块", active)
            else:
                self.assertNotIn(forced, active)
        self.assertIn("review_only", text)
        self.assertIn("Project", text)
        self.assertIn("附加", text)

    def test_v2_no_longer_orders_fixed_round_template(self):
        text = read("knowledge/system/gpt-meme-continuity-v2.md")
        self.assertNotIn("全文最后一项必须是", text)
        self.assertNotIn("持续研究回答必须在最后写", text)
        self.assertIn("自适应收尾与实际验收", text)
        self.assertIn("一句短而开放", text)
        self.assertIn("NO_CHANGE", text)

    def test_actual_funding_question_keeps_specialist_evidence_only(self):
        r = recommend_experts("资金同源是不是共享交易所节点", objective="EXPLAIN")
        self.assertEqual(r["status"], "SPECIALISTS_SELECTED_FOR_RESEARCH_ONLY")
        self.assertIn("E-L3-02", [x["id"] for x in r["specialists"]])
        self.assertLessEqual(len(r["specialists"]), 3)
        self.assertIn("not_semantic_evaluation", r["selection_method"])
        self.assertTrue(r["frozen_monitor_cannot_generate_new_rules"])

    def test_actual_copytrade_cost_question_reaches_execution_economics(self):
        r = recommend_experts("钱包跟单后滑点和退出成本", objective="ECONOMIC")
        self.assertIn("E-L5-01", [x["id"] for x in r["specialists"]])
        self.assertNotIn("E-L7-02", [x["id"] for x in r["specialists"]])
        plan = filter_plan("ECONOMIC")
        required = [x["id"] for x in plan["gates"] if x["required_for_objective"]]
        self.assertIn("F5", required)
        self.assertNotIn("F6", required)
        self.assertFalse(plan["automatic_rule_promotion"])

    def test_unknown_question_researches_outside_registry_not_fake_expert(self):
        r = recommend_experts("火星奶酪未知非相关概念", objective="EXPLAIN")
        self.assertEqual(r["status"], "SOURCE_DISCOVERY_REQUIRED")
        self.assertEqual(r["specialists"], [])
        self.assertEqual(route_domains("火星奶酪未知非相关概念")["status"], "RESEARCH_GAP")

    def test_actual_monitor_release_keeps_distinct_high_bar(self):
        r = recommend_experts("规则发布和监控", objective="MONITOR_RELEASE", max_experts=5)
        self.assertIn("E-L7-02", [x["id"] for x in r["specialists"]])
        plan = filter_plan("MONITOR_RELEASE")
        self.assertTrue(all(x["required_for_objective"] for x in plan["gates"]))
        self.assertFalse(plan["automatic_rule_promotion"])
        self.assertTrue(r["frozen_monitor_cannot_generate_new_rules"])

    def test_real_mint_report_is_an_information_task_not_a_deployed_bot(self):
        r = recommend_experts("Solana Meme Mint关键钱包报告和资金数据源", objective="EXPLAIN")
        self.assertIn(r["status"], {"SPECIALISTS_SELECTED_FOR_RESEARCH_ONLY", "SOURCE_DISCOVERY_REQUIRED"})
        self.assertLessEqual(len(r["specialists"]), 3)
        self.assertNotIn("E-L7-02", [x["id"] for x in r["specialists"]])
        self.assertIn("V1.1", read("knowledge/system/current-operating-guidance.md"))


if __name__ == "__main__":
    unittest.main()
