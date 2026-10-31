import copy
import unittest
from cashflow_semantics import audit_funding_table


def sample():
    return {"n_wallets": 2, "n_genesis_reached": 1,
            "n_prebuy_window_reached": 2,
            "wallets": [
                {"wallet": "A", "genesis_reached": True,
                 "prebuy_window_reached": True, "inflows": [
                    {"signature": "tx1", "nature": "financement", "tx_source": "SYSTEM_PROGRAM", "tx_type": "TRANSFER", "source": "F", "amount_sol": 2, "n_debited_accounts": 1},
                    {"signature": "tx2", "nature": "produit_de_vente", "tx_source": "SOLANA_PROGRAM_LIBRARY", "tx_type": "CLOSE_ACCOUNT", "source": "WSOL", "amount_sol": 3, "n_debited_accounts": 1}]},
                {"wallet": "B", "genesis_reached": False, "prebuy_window_reached": True,
                 "inflows": [
                    {"signature": "tx3", "nature": "financement", "tx_source": "METEORA", "tx_type": "REMOVE_LIQUIDITY_BY_RANGE", "source": "POOL", "amount_sol": 4, "n_debited_accounts": 1}]}]}


class TestCashflowSemantics(unittest.TestCase):
    def test_counterexamples_remain_source_derived(self):
        o = audit_funding_table(sample())
        self.assertEqual(o["source_inflow_rows"], 3)
        self.assertEqual(o["genesis_uncovered"], 1)
        self.assertEqual(o["recorded_nature"], {"financement": 2, "produit_de_vente": 1})
        self.assertEqual(o["funding_label_non_system_transfer_candidates"][0]["source"], "METEORA")
        self.assertEqual(o["sale_label_non_swap_type_candidates"][0]["type"], "CLOSE_ACCOUNT")
        self.assertFalse(o["non_system_is_error"])
        self.assertFalse(o["confirmed_original_funder"])
        self.assertTrue(o["no_trading"])
    def test_missing_wallet_history_flags_are_rejected(self):
        d = sample()
        d["wallets"][0].pop("genesis_reached")
        with self.assertRaisesRegex(ValueError, "coverage flags"):
            audit_funding_table(d)
    def test_unsupported_empty_inflows_is_not_invented(self):
        d = sample()
        del d["wallets"][0]["inflows"]
        with self.assertRaisesRegex(ValueError, "inflows must be a list"):
            audit_funding_table(d)
    def test_duplicate_wallet_is_rejected(self):
        d = sample()
        d["wallets"][1]["wallet"] = "A"
        with self.assertRaisesRegex(ValueError, "duplicate wallet"):
            audit_funding_table(d)
    def test_stale_summary_is_rejected(self):
        d = sample()
        d["n_genesis_reached"] = 2
        with self.assertRaisesRegex(ValueError, "genesis count"):
            audit_funding_table(d)
    def test_same_signature_and_amount_without_instruction_id_is_flagged_not_deleted(self):
        d = sample()
        d["wallets"][0]["inflows"].append(copy.deepcopy(d["wallets"][0]["inflows"][0]))
        out = audit_funding_table(d)
        self.assertEqual(out["source_inflow_rows"], 4)
        self.assertEqual(len(out["duplicate_like_rows_needing_instruction_ids"]), 1)

if __name__ == "__main__":
    unittest.main()
