"""Deterministic cross-domain mechanism discovery on synthetic derived receipts."""
from __future__ import annotations

import copy
import unittest
from decimal import Decimal

from solana_meme_os.mechanism_discovery import discover_cashflow_mechanisms


def cohort():
    return {
        "n_wallets": 2, "n_genesis_reached": 1, "n_prebuy_window_reached": 1,
        "wallets": [
            {"wallet": "A", "genesis_reached": True, "prebuy_window_reached": True,
             "inflows": [
                {"signature": "a1", "nature": "financement", "tx_source": "SYSTEM_PROGRAM",
                 "tx_type": "TRANSFER", "amount_sol": 1},
                {"signature": "a2", "nature": "financement", "tx_source": "SYSTEM_PROGRAM",
                 "tx_type": "TRANSFER", "amount_sol": "1.000000001"},
                {"signature": "a3", "nature": "financement", "tx_source": "SYSTEM_PROGRAM",
                 "tx_type": "TRANSFER", "amount_sol": 1},
                {"signature": "a4", "nature": "financement", "tx_source": "METEORA",
                 "tx_type": "REMOVE_LIQUIDITY_BY_RANGE", "amount_sol": "120.000000001"},
                {"signature": "a5", "nature": "produit_de_vente", "tx_source": "PUMP_FUN",
                 "tx_type": "SWAP", "amount_sol": 20},
            ]},
            {"wallet": "B", "genesis_reached": False, "prebuy_window_reached": False,
             "inflows": []},
        ],
    }


class TestMechanismDiscovery(unittest.TestCase):
    def test_count_value_inversion_generates_competing_mechanisms(self):
        r = discover_cashflow_mechanisms(cohort())
        self.assertTrue(r["source_value_dominance_inversion"])
        self.assertEqual(r["labelled_rows"], 4)
        self.assertEqual(r["other_program_labelled_rows"], 1)
        self.assertEqual(r["other_program_count_share"], "0.250000")
        self.assertEqual(r["other_program_value_share"], "0.975610")
        self.assertEqual(r["labelled_positive_sol_receipt"], "123.000000002")
        self.assertEqual(r["other_program_labelled_sol"], "120.000000001")
        self.assertEqual(r["replay_priority_signatures"][0]["signature"], "a4")
        self.assertEqual(r["candidate_mechanisms"][0]["id"],
                         "COUNT_VALUE_ECONOMIC_TYPE_INVERSION")

    def test_source_labels_not_equated_to_external_capital_or_controller(self):
        r = discover_cashflow_mechanisms(cohort())
        self.assertFalse(r["capital_injection_confirmed"])
        self.assertFalse(r["abnormality_confirmed"])
        self.assertFalse(r["economic_controller_confirmed"])
        self.assertFalse(r["hypotheses_tested_on_real_rpc"])
        self.assertTrue(r["no_trading"])

    def test_old_financing_label_can_have_no_inversion(self):
        d = cohort()
        d["wallets"][0]["inflows"][3]["amount_sol"] = "0.1"
        r = discover_cashflow_mechanisms(d)
        self.assertFalse(r["source_value_dominance_inversion"])
        self.assertEqual(r["candidate_mechanisms"], [])

    def test_source_coverage_is_not_confused_with_zero_funding(self):
        r = discover_cashflow_mechanisms(cohort())
        self.assertEqual(r["genesis_covered"], 1)
        self.assertEqual(r["genesis_uncovered"], 1)
        self.assertEqual(r["prebuy_uncovered"], 1)

    def test_missing_source_amount_or_program_is_not_zero(self):
        for bad_field in ("amount_sol", "tx_source", "tx_type"):
            d = cohort()
            d["wallets"][0]["inflows"][3].pop(bad_field)
            with self.assertRaises(ValueError):
                discover_cashflow_mechanisms(d)

    def test_losing_precision_or_negative_amount_is_rejected(self):
        for bad in ("0.0000000001", "NaN", "-1", True, None):
            d = cohort()
            d["wallets"][0]["inflows"][3]["amount_sol"] = bad
            with self.assertRaises(ValueError):
                discover_cashflow_mechanisms(d)

    def test_history_coverage_asymmetry_generates_distinct_data_hypothesis(self):
        x = cohort()
        x["wallets"] = []
        for i in range(21):
            row = copy.deepcopy(cohort()["wallets"][0])
            row["wallet"] = "complete-" + str(i)
            # Only one financing event is necessary to distinguish observed
            # presence; signature names remain synthetic.
            row["inflows"] = [dict(row["inflows"][0],
                                   signature="synthetic-" + str(i))]
            x["wallets"].append(row)
        for i in range(19):
            row = copy.deepcopy(cohort()["wallets"][1])
            row["wallet"] = "incomplete-" + str(i)
            if i < 4:
                row["inflows"] = [{
                    "signature": "incomplete-sig-" + str(i),
                    "nature": "financement", "tx_source": "SYSTEM_PROGRAM",
                    "tx_type": "TRANSFER", "amount_sol": "1"}]
            x["wallets"].append(row)
        x["n_wallets"] = 40
        x["n_genesis_reached"] = 21
        x["n_prebuy_window_reached"] = 21
        r = discover_cashflow_mechanisms(x)
        self.assertTrue(r["history_coverage_receipt_silence_tension"])
        self.assertEqual(r["genesis_coverage_receipt_presence"]["GENESIS_COVERED"]["without_label_receipt"], 0)
        self.assertEqual(r["genesis_coverage_receipt_presence"]["GENESIS_UNCOVERED"]["without_label_receipt"], 15)
        self.assertIn("HISTORY_COVERAGE_RECEIPT_SILENCE_TENSION",
                      [c["id"] for c in r["candidate_mechanisms"]])
        self.assertFalse(r["capital_injection_confirmed"])

    def test_nonfocal_trades_are_not_assumed_to_be_financing(self):
        r = discover_cashflow_mechanisms(cohort(), label="produit_de_vente")
        self.assertEqual(r["labelled_rows"], 1)
        self.assertEqual(r["labelled_positive_sol_receipt"], "20.000000000")

    def test_missing_cohort_summary_is_rejected(self):
        d = cohort()
        d["n_wallets"] = 3
        with self.assertRaisesRegex(ValueError, "wallet count"):
            discover_cashflow_mechanisms(d)

    def test_identical_input_has_identical_result_and_no_signature_execution(self):
        r = discover_cashflow_mechanisms(cohort(), majority_share=Decimal(".50"))
        self.assertEqual(r, discover_cashflow_mechanisms(copy.deepcopy(cohort())))
        self.assertEqual(r["replay_priority_signatures"][0]["source_replay_status"],
                         "NOT_CHECKED")

    def test_zero_focal_rows_do_not_become_anomalies(self):
        r = discover_cashflow_mechanisms(cohort(), label="unknown_event_class")
        self.assertEqual(r["labelled_rows"], 0)
        self.assertFalse(r["source_value_dominance_inversion"])
        self.assertEqual(r["candidate_mechanisms"], [])


if __name__ == "__main__":
    unittest.main()
