"""Offline tests using synthetic fixtures; no external corpus data copied."""
from decimal import Decimal
import unittest
from solana_meme_os.position_audit import audit, amount


def fixture(sold="10", flow="100", bought="100"):
    b = {"lancements": [{"mint": "mint-1", "buys": [{"wallet": "wallet-A", "tokens": bought}]}]}
    f = {"lancements": [{"mint": "mint-1", "wallets": [
        {"wallet": "wallet-A", "tokens_transferes": flow, "tokens_vendus": sold}]}]}
    s = {"lancements": [{"mint": "mint-1", "slot": 123, "contigu": True,
                         "ratio_premier_externe_sur_operateur": 3.4}]}
    return b, f, s


class ReconciliationTests(unittest.TestCase):
    def test_excess_is_not_called_chain_violation(self):
        out = audit(*fixture())
        self.assertEqual(out["counts"]["outflow_exceeds_creation_buys"], 1)
        self.assertEqual(out["cases"][0]["conditional_minimum_unseen_inflow"], "10")
        self.assertFalse(out["raw_rpc_checked"])
        self.assertFalse(out["profit_or_alpha_verified"])
        self.assertFalse(out["cases"][0]["source_sell_is_confirmed_swap"])

    def test_balanced(self):
        out = audit(*fixture("0"))
        self.assertEqual(out["counts"]["within_tolerance"], 1)
        self.assertFalse(out["cases"][0]["asset_path_closed"])

    def test_less_than_creation_buys(self):
        out = audit(*fixture("0", "90"))
        self.assertEqual(out["counts"]["outflow_below_creation_buys"], 1)

    def test_reject_unknown_instead_of_zero(self):
        with self.assertRaisesRegex(ValueError, "missing/invalid"):
            amount(None)

    def test_reject_duplicate_mint(self):
        b, f, s = fixture()
        b["lancements"].append(b["lancements"][0])
        with self.assertRaisesRegex(ValueError, "duplicate mint"):
            audit(b, f, s)

    def test_reject_nonmatching_wallets(self):
        b, f, s = fixture()
        f["lancements"][0]["wallets"][0]["wallet"] = "other-wallet"
        with self.assertRaisesRegex(ValueError, "wallet sets differ"):
            audit(b, f, s)

    def test_reject_missing_mint(self):
        b, f, s = fixture()
        f["lancements"] = []
        with self.assertRaisesRegex(ValueError, "unmatched mint"):
            audit(b, f, s)

    def test_precision(self):
        out = audit(*fixture("0.01", "100", "100"))
        self.assertEqual(out["counts"]["within_tolerance"], 1)
        self.assertIsInstance(Decimal(out["cases"][0]["excess_outflow_vs_creation_buys"]), Decimal)

    def test_refuse_invalid_amount(self):
        for val in (True, "NaN", "Infinity", "-1"):
            with self.assertRaises(ValueError):
                amount(val)


if __name__ == "__main__":
    unittest.main()
