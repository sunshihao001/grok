"""Cross-registry integrity tests for the canonical knowledge architecture.

These tests validate file references and internal knowledge contracts only.
They do not validate Solana chain truth, anomaly calibration or trading utility.
"""
from __future__ import annotations
import json
from pathlib import Path
import unittest

from solana_meme_os.knowledge import load_catalog, for_question
from solana_meme_os.research import load_index
from solana_meme_os.expert_router import load_map
from solana_meme_os.expert_interaction import load_graph

ROOT = Path(__file__).resolve().parents[1]


def read_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class KnowledgeArchitectureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.arch = read_json("knowledge/architecture.v2.json")
        cls.catalog = load_catalog()
        cls.sources = load_index()
        cls.mapping = load_map()
        cls.graph = load_graph(expert_map=cls.mapping)
        cls.external = read_json("knowledge/external-method-sources.v1.json")
        cls.hypotheses = read_json("knowledge/mechanism-synthesis-hypotheses.v1.json")
        cls.projects = read_json("knowledge/reference-project-discovery.v1.json")

    def test_architecture_is_canonical_but_not_claimed_deployed(self):
        self.assertEqual(self.arch["status"], "CANONICAL_REFERENCE_NOT_DEPLOYED")
        self.assertEqual([x["id"] for x in self.arch["knowledge_layers"]],
                         [f"L{i}" for i in range(8)])
        self.assertEqual([x["id"] for x in self.arch["research_stages"]],
                         [f"S{i}" for i in range(8)])
        self.assertEqual([x["id"] for x in self.arch["product_capabilities"]],
                         [f"M{i}" for i in range(8)])
        self.assertEqual(len(self.arch["knowledge_graphs"]), 5)

    def test_registry_counts_match_real_assets(self):
        r = self.arch["registries"]
        manifest = read_json("knowledge/legacy-snapshots/manifest.json")
        self.assertEqual(r["knowledge_cards"]["count"], len(self.catalog["cards"]))
        self.assertEqual(r["source_pointers"]["count"], len(self.sources["items"]))
        self.assertEqual(r["expert_disciplines"]["count"], len(self.mapping["experts"]))
        self.assertEqual(r["knowledge_domains"]["count"], len(self.mapping["domains"]))
        self.assertEqual(r["research_stages"]["count"], len(self.mapping["stages"]))
        self.assertEqual(r["scenario_routes"]["count"], len(self.mapping["scenarios"]))
        self.assertEqual(r["expert_handoffs"]["count"], len(self.graph["links"]))
        self.assertEqual(r["external_method_sources"]["count"], len(self.external["references"]))
        self.assertEqual(r["mechanism_hypotheses"]["count"], len(self.hypotheses["hypotheses"]))
        self.assertEqual(r["reference_projects"]["count"], len(self.projects["projects"]))
        self.assertEqual(r["legacy_snapshots"]["count"], len(manifest["documents"]))
        self.assertEqual(r["research_units"]["count"], len(list((ROOT / "knowledge/research").glob("R*.md"))))

    def test_every_card_is_assigned_to_at_least_one_expert(self):
        card_ids = {c["id"] for c in self.catalog["cards"]}
        assigned = {card for expert in self.mapping["experts"]
                    for card in expert["source_cards"]}
        self.assertEqual(assigned, card_ids)

    def test_cards_have_valid_domain_maturity_and_accountable_experts(self):
        domains = {x["id"] for x in self.mapping["domains"]}
        expert_ids = {x["id"] for x in self.mapping["experts"]}
        for card in self.catalog["cards"]:
            self.assertIn(card["domain"], domains)
            self.assertIn(card["maturity"], {"K0", "K1", "K2", "K3", "K4"})
            self.assertTrue(card["maturity_basis"])
            self.assertTrue(set(card["owner_experts"]) <= expert_ids)
            self.assertTrue(card["owner_experts"])

    def test_expert_source_and_scenario_references_resolve(self):
        source_ids = {x["id"] for x in self.sources["items"]}
        card_ids = {x["id"] for x in self.catalog["cards"]}
        expert_ids = {x["id"] for x in self.mapping["experts"]}
        for expert in self.mapping["experts"]:
            self.assertTrue(set(expert["source_cards"]) <= card_ids)
            self.assertTrue(set(expert["source_ids"]) <= source_ids)
        for scenario in self.mapping["scenarios"]:
            roles = [scenario["lead"], *scenario["panel"],
                     *scenario["conditional"], *scenario["vetoReview"]]
            self.assertTrue(set(roles) <= expert_ids)

    def test_handoff_graph_and_external_method_edges_resolve(self):
        expert_ids = {x["id"] for x in self.mapping["experts"]}
        edge_ids = {x["id"] for x in self.graph["links"]}
        self.assertEqual(len(edge_ids), len(self.graph["links"]))
        for link in self.graph["links"]:
            self.assertIn(link["from"], expert_ids)
            self.assertIn(link["to"], expert_ids)
            self.assertTrue(link["contract"])
            self.assertTrue(link["counter_signal"])
        for ref in self.external["references"]:
            self.assertTrue(set(ref["linked_expert_edges"]) <= edge_ids)

    def test_mechanism_hypothesis_expert_references_resolve(self):
        expert_ids = {x["id"] for x in self.mapping["experts"]}
        for hypothesis in self.hypotheses["hypotheses"]:
            self.assertTrue(set(hypothesis["specialists"]) <= expert_ids)
            self.assertTrue(hypothesis["predicts"])
            self.assertTrue(hypothesis["alternatives"])
            self.assertTrue(hypothesis["discriminator"])
            self.assertTrue(hypothesis["reject_when"])

    def test_new_research_cards_are_retrievable(self):
        cases = [
            ("first funder 历史覆盖不足，不能证明独立钱包", "first-funder-history-coverage"),
            ("SOL流入可能是 CloseAccount 或 LP撤出，不一定是外部注资", "sol-receipt-economic-semantics"),
            ("次数与金额反转，资本规模由少数LP释放主导", "cashflow-count-value-inversion"),
            ("多通道钱包群与共享funding hub如何区分", "multichannel-wallet-evidence"),
            ("跨Mint 地址轮换后的经济角色不变量", "capital-role-invariance"),
            ("正常机器人生态 null model 公共基础设施", "normal-bot-ecology-baseline"),
            ("BUY SELL 方向必须由指令解码确认", "trade-direction-source-gate"),
            ("市场监控价值和可交易净收益是否相同", "market-utility-vs-tradability"),
        ]
        for question, expected in cases:
            result = for_question(question, catalog=self.catalog)
            self.assertEqual(result["route_status"], "MATCHED_REFERENCE", question)
            self.assertIn(expected, {x["id"] for x in result["references"]}, question)

    def test_source_registry_pointers_are_pinned_and_unique(self):
        items = self.sources["items"]
        ids = [x["id"] for x in items]
        self.assertEqual(len(ids), len(set(ids)))
        for item in items:
            self.assertRegex(item["commit"], r"^[0-9a-f]{40}$")
            self.assertTrue(item["repository"])
            self.assertTrue(item["path"])
            self.assertTrue(item["topics"])
            self.assertIn(item["availability"], {"remote_on_demand"})

    def test_product_component_paths_exist_and_statuses_are_explicit(self):
        for module in self.arch["software_components"]:
            self.assertTrue((ROOT / module["path"]).is_file(), module["path"])
            self.assertTrue(module["status"])
        for product in self.arch["product_capabilities"]:
            self.assertTrue(product["status"])
            for path in product["code"]:
                self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
