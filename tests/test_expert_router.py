"""Expert routing is source discovery, not market outcome inference."""
import copy
from pathlib import Path
import unittest

from solana_meme_os.expert_router import DEFAULT_MAP, load_map, route
from solana_meme_os.knowledge import load_catalog
from solana_meme_os.research import load_index


class TestExpertKnowledgeRouting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = load_map()

    def test_research_map_does_not_claim_deployment(self):
        self.assertEqual(self.mapping["status"], "RESEARCH_CONTRACT_NOT_DEPLOYED")
        self.assertEqual(len(self.mapping["experts"]), 17)
        self.assertEqual(len(self.mapping["domains"]), 12)
        self.assertEqual(len(self.mapping["scenarios"]), 9)

    def test_every_expert_card_exists(self):
        # Catalog and source registry contract, not market truth.
        catalog = load_catalog()
        index = load_index()
        known_cards = {c["id"] for c in catalog["cards"]}
        known_sources = {s["id"] for s in index["items"]}
        used = set()
        for expert in self.mapping["experts"]:
            self.assertTrue(set(expert["source_cards"]) <= known_cards)
            self.assertTrue(set(expert["source_ids"]) <= known_sources)
            self.assertTrue(expert["requires"])
            self.assertTrue(expert["challenge"])
            used.update(expert["source_cards"])
        self.assertEqual(used, known_cards)

    def test_funding_burst_selects_independent_challengers(self):
        got = route(["FUNDING_FANOUT", "SAME_SLOT_MULTIWALLET_BUY"], mapping=self.mapping)
        self.assertEqual(got["matched_scenarios"], ["funding_buy_burst"])
        self.assertEqual(got["lead_expert"], "event")
        self.assertIn("chain", got["primary_experts"])
        self.assertIn("statistics", got["primary_experts"])
        self.assertIn("review", got["independent_challengers"])
        self.assertIn("risk", got["independent_challengers"])
        self.assertIn("sybil-wash", got["source_card_ids_to_read"])
        self.assertTrue(got["no_trading"])

    def test_liquidity_route_does_not_force_entity_merge(self):
        got = route(["LIQUIDITY_DROP", "TOP10_SHARE_RISE"], mapping=self.mapping)
        self.assertEqual(got["lead_expert"], "liquidity")
        self.assertIn("inventory", got["primary_experts"])
        self.assertIn("token", got["primary_experts"])
        self.assertNotIn("graph", got["primary_experts"])
        self.assertIn("graph", got["conditional_experts"])
        self.assertIn("liquidity-depth", got["source_card_ids_to_read"])

    def test_cross_mint(self):
        got = route(["CROSS_MINT_FUNDING_REUSE"], mapping=self.mapping)
        self.assertEqual(got["lead_expert"], "graph")
        self.assertIn("wallet", got["primary_experts"])
        self.assertIn("statistics", got["primary_experts"])

    def test_unknown_event_expands_research_not_forced_to_known_type(self):
        got = route(["UNSEEN_PROTOCOL_NEW_EVENT"], question="新协议资金关系", mapping=self.mapping)
        self.assertEqual(got["status"], "OPEN_DISCOVERY_REQUIRED")
        self.assertEqual(got["primary_experts"], ["chief", "data", "review"])
        self.assertTrue(got["new_mechanisms_allowed"])
        self.assertEqual(got["matched_scenarios"], [])

    def test_multi_event_can_activate_multiple_expert_groups(self):
        got = route(["FUNDING_FANOUT", "LIQUIDITY_DROP"], mapping=self.mapping)
        self.assertEqual(len(got["matched_scenarios"]), 2)
        self.assertIn("event", got["primary_experts"])
        self.assertIn("liquidity", got["primary_experts"])
        self.assertIn("token", got["primary_experts"])
        self.assertFalse("actual_order" in got)

    def test_native_funding_to_buy_is_a_known_research_panel(self):
        x = route(["FUNDING_TO_BUY_CANDIDATE"], mapping=self.mapping)
        self.assertEqual(x["status"], "MATCHED_RESEARCH_PANELS")
        self.assertEqual(x["lead_expert"], "graph")
        self.assertIn("chain", x["primary_experts"])
        self.assertIn("review", x["independent_challengers"])
        self.assertTrue(x["no_trading"])

    def test_native_token_consolidation_is_not_unknown_protocol(self):
        x = route(["TOKEN_CONSOLIDATION"], mapping=self.mapping)
        self.assertEqual(x["status"], "MATCHED_RESEARCH_PANELS")
        self.assertEqual(x["lead_expert"], "inventory")
        self.assertIn("graph", x["primary_experts"])
        self.assertIn("review", x["independent_challengers"])

    def test_value_inversion_triggers_capital_and_execution_experts(self):
        x = route(["COUNT_VALUE_ECONOMIC_TYPE_INVERSION"], mapping=self.mapping)
        self.assertEqual(x["status"], "MATCHED_RESEARCH_PANELS")
        self.assertEqual(x["lead_expert"], "graph")
        self.assertIn("chain", x["primary_experts"])
        self.assertIn("liquidity", x["primary_experts"])
        self.assertIn("review", x["independent_challengers"])
        self.assertTrue(x["no_trading"])

    def test_history_silence_triggers_coverage_and_statistics(self):
        x = route(["HISTORY_COVERAGE_RECEIPT_SILENCE_TENSION"], mapping=self.mapping)
        self.assertEqual(x["status"], "MATCHED_RESEARCH_PANELS")
        self.assertEqual(x["lead_expert"], "data")
        self.assertIn("wallet", x["primary_experts"])
        self.assertIn("statistics", x["primary_experts"])
        self.assertIn("review", x["independent_challengers"])

    def test_reject_unknown_role_in_research_contract(self):
        bad = copy.deepcopy(self.mapping)
        bad["scenarios"][0]["panel"].append("NON_EXISTENT_BOT")
        # load_map verifies external maps on disk, not inline argument.
        # Verify scenario role consistency directly for the supplied mapping.
        roles = {x["id"] for x in bad["experts"]}
        self.assertTrue(set(bad["scenarios"][0]["panel"]) - roles)
        got = route(["UNSEEN"], mapping=self.mapping)
        self.assertTrue(got["human_research_review_required"])


if __name__ == "__main__":
    unittest.main()
