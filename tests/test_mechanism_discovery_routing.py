"""V5 discovery-to-expert orchestration remains a deterministic offline contract."""
from __future__ import annotations
import unittest

from solana_meme_os.expert_router import route
from solana_meme_os.mechanism_discovery import discover_cashflow_mechanisms


def synthetic_wallet(index: int, *, genesis: bool, finance: bool):
    return {
        "wallet": "wallet-" + str(index),
        "genesis_reached": genesis,
        "prebuy_window_reached": genesis,
        "inflows": ([{
            "signature": "synthetic-signature-" + str(index),
            "nature": "financement",
            "tx_source": "SYSTEM_PROGRAM",
            "tx_type": "TRANSFER",
            "amount_sol": "1.000000000",
        }] if finance else []),
    }


class DiscoveryToExpertTests(unittest.TestCase):
    def test_source_value_inversion_assigns_capital_not_fake_trade_experts(self):
        doc = {
            "n_wallets": 1, "n_genesis_reached": 1,
            "n_prebuy_window_reached": 1,
            "wallets": [{
                "wallet": "wallet-a", "genesis_reached": True,
                "prebuy_window_reached": True,
                "inflows": [
                    {"signature": f"small-{i}", "nature": "financement",
                     "tx_source": "SYSTEM_PROGRAM", "tx_type": "TRANSFER",
                     "amount_sol": "1"} for i in range(3)
                ] + [{"signature": "lp-large", "nature": "financement",
                       "tx_source": "METEORA",
                       "tx_type": "REMOVE_LIQUIDITY_BY_RANGE",
                       "amount_sol": "150"}]}],
        }
        found = discover_cashflow_mechanisms(doc)
        kinds = [c["id"] for c in found["candidate_mechanisms"]]
        self.assertEqual(kinds, ["COUNT_VALUE_ECONOMIC_TYPE_INVERSION"])
        experts = route(kinds, question="What is the actual origin of this SOL?")
        self.assertEqual(experts["lead_expert"], "graph")
        self.assertIn("liquidity", experts["primary_experts"])
        self.assertIn("review", experts["independent_challengers"])
        self.assertFalse(found["capital_injection_confirmed"])
        self.assertTrue(found["no_trading"])
        self.assertTrue(experts["no_trading"])

    def test_coverage_silence_assigns_data_quality_not_operator_attribution(self):
        wallets = [synthetic_wallet(i, genesis=True, finance=True)
                   for i in range(20)]
        wallets.extend(synthetic_wallet(i+20, genesis=False, finance=i < 4)
                       for i in range(20))
        doc = {"n_wallets": 40, "n_genesis_reached": 20,
               "n_prebuy_window_reached": 20, "wallets": wallets}
        found = discover_cashflow_mechanisms(doc)
        kinds = [c["id"] for c in found["candidate_mechanisms"]]
        self.assertEqual(kinds, ["HISTORY_COVERAGE_RECEIPT_SILENCE_TENSION"])
        experts = route(kinds, question="Does missing genesis history create false wallet independence?")
        self.assertEqual(experts["lead_expert"], "data")
        self.assertIn("statistics", experts["primary_experts"])
        self.assertIn("review", experts["independent_challengers"])
        self.assertFalse(found["economic_controller_confirmed"])
        self.assertFalse(found["abnormality_confirmed"])


if __name__ == "__main__":
    unittest.main()
