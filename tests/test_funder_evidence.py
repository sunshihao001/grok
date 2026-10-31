"""Synthetic counterexamples for cross-project first-funder semantics.

This protects the distinction between missing funding history, public
infrastructure, confirmed transfer sources and inferred economic ownership.
"""
from __future__ import annotations

import copy
import unittest

from solana_meme_os.funder_evidence import classify_first_funders


def resolved(wallet: str, funder: str, *, kind: str = "PRIVATE_CANDIDATE",
             method: str = "TRANSFER_INSTRUCTION_CONFIRMED", amount: str = "2000000000") -> dict:
    return {"wallet": wallet, "state": "RESOLVED", "funder": funder,
            "source_type": kind, "trace_method": method,
            "amount_lamports": amount, "signature": f"signature-{wallet}",
            "source_ref": "SYNTHETIC_FUNDING_EVENT"}


def fixture() -> list[dict]:
    return [
        resolved("Wallet-A", "Funding-F"),
        resolved("Wallet-B", "Funding-F"),
        resolved("Wallet-C", "Public-CEX", kind="PUBLIC_CEX"),
        {"wallet": "Wallet-D", "state": "UNRESOLVED", "reason": "HISTORY_PAGE_FULL"},
        {"wallet": "Wallet-E", "state": "PENDING"},
        resolved("Wallet-F", "Maybe-F", method="NET_BALANCE_DELTA_HEURISTIC"),
        resolved("Wallet-G", "Unique-F"),
        resolved("Wallet-H", "Tiny-F", amount="10"),
        resolved("Wallet-I", "Unknown-Hub", kind="UNKNOWN"),
    ]


class TestFunderEvidence(unittest.TestCase):
    def test_unknown_does_not_become_independent(self):
        got = classify_first_funders(fixture())
        states = {row["wallet"]: row for row in got["wallet_states"]}
        self.assertEqual(states["Wallet-D"]["status"], "FIRST_FUNDER_UNKNOWN")
        self.assertEqual(states["Wallet-E"]["status"], "NOT_YET_SCANNED")
        self.assertFalse(states["Wallet-D"]["confirmed_economic_independence"])
        self.assertIsNone(got["confirmed_independent_wallet_count"])

    def test_confirmed_shared_source_is_not_shared_owner(self):
        got = classify_first_funders(fixture())
        self.assertEqual(got["status_counts"]["SHARED_PRIVATE_FUNDER_CANDIDATE"], 2)
        self.assertEqual(got["shared_private_source_candidates"][0]["wallets"],
                         ["Wallet-A", "Wallet-B"])
        self.assertFalse(got["beneficial_owner_verified"])

    def test_known_public_never_becomes_private_group(self):
        got = classify_first_funders(fixture())
        state = next(s for s in got["wallet_states"] if s["wallet"] == "Wallet-C")
        self.assertEqual(state["status"], "KNOWN_PUBLIC_INFRASTRUCTURE")

    def test_largest_loser_heuristic_cannot_count_as_verified_funder(self):
        got = classify_first_funders(fixture())
        states = {x["wallet"]: x for x in got["wallet_states"]}
        self.assertEqual(states["Wallet-F"]["status"], "FUNDER_HEURISTIC_UNCONFIRMED")
        self.assertFalse(any(r["source"] == "Maybe-F"
                             for r in got["shared_private_source_candidates"]))

    def test_unique_funder_still_does_not_confirm_independence(self):
        got = classify_first_funders(fixture())
        states = {x["wallet"]: x for x in got["wallet_states"]}
        self.assertEqual(states["Wallet-G"]["status"],
                         "UNIQUE_OBSERVED_FUNDER_NOT_OWNER_INDEPENDENCE")

    def test_dust_and_unknown_infra_are_separate(self):
        got = classify_first_funders(fixture())
        states = {x["wallet"]: x for x in got["wallet_states"]}
        self.assertEqual(states["Wallet-H"]["status"], "DUST_EDGE_NOT_DISCRIMINATING")
        self.assertEqual(states["Wallet-I"]["status"], "SOURCE_INFRASTRUCTURE_UNKNOWN")

    def test_high_degree_is_ambiguous_not_automatically_cex_or_independent(self):
        records = [resolved(f"Wallet-{i}", "Large-Source")
                   for i in range(6)]
        got = classify_first_funders(records)
        self.assertEqual(got["status_counts"], {"HIGH_DEGREE_SOURCE_AMBIGUOUS": 6})
        self.assertEqual(got["shared_private_source_candidates"], [])

    def test_reject_missing_transaction_provenance(self):
        records = fixture()
        records[0].pop("signature")
        with self.assertRaisesRegex(ValueError, "exact transaction signature"):
            classify_first_funders(records)

    def test_reject_nan_float_and_duplicate_wallet(self):
        records = fixture()
        records[0]["amount_lamports"] = 2e9
        with self.assertRaisesRegex(ValueError, "exact raw lamport string"):
            classify_first_funders(records)
        records = fixture() + [copy.deepcopy(fixture()[0])]
        with self.assertRaisesRegex(ValueError, "duplicate wallet"):
            classify_first_funders(records)

    def test_unresolved_cannot_claim_source(self):
        records = fixture()
        records[3]["funder"] = "Unknown-Guess"
        with self.assertRaisesRegex(ValueError, "cannot assert a funder"):
            classify_first_funders(records)

    def test_does_not_trigger_live_action_or_certain_normal_class(self):
        got = classify_first_funders(fixture())
        self.assertTrue(got["no_trading"])
        self.assertFalse(got["normal_wallet_baseline_qualified"])
        self.assertTrue(all(not w["confirmed_economic_independence"]
                            for w in got["wallet_states"]))


if __name__ == "__main__":
    unittest.main()
