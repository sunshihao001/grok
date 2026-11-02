"""Offline, source-equivalent counterexample for Why-Solana's native SOL flow heuristic.

Source: sunshihao001/Why-Solana-Memecoins-Are-Over
  exit_destination/code/ed_trace.py::txflow
  funder_network/code/fn_40_posthoc.py::main, section 7

This deliberately tests *only the extracted decision predicate*; it does NOT
run the source repository, decode real Solana instructions, access RPC or
estimate the incidence of false edges in the historical FN sample.
"""
import unittest

LAMPORTS_PER_SOL = 1_000_000_000


def source_equivalent_pick(keys, pre, post, fee_lamports, subject):
    """Mirror the inspected largest-positive-lamport-gain rule with no token/tip accounts."""
    balance_delta = dict(zip(keys, (b - a for a, b in zip(pre, post))))
    fee_payer = keys[0]
    subject_native_change = (
        balance_delta[subject] + (fee_lamports if fee_payer == subject else 0)
    ) / LAMPORTS_PER_SOL
    amount = -subject_native_change
    gains = {
        k: (v + (fee_lamports if k == fee_payer else 0)) / LAMPORTS_PER_SOL
        for k, v in balance_delta.items() if k != subject
    }
    selected = max(
        (k for k in gains if gains[k] > 0),
        key=lambda k: (gains[k], k),
        default=None,
    )
    return selected, amount


class FundingEdgeSourceEquivalentCases(unittest.TestCase):
    def test_single_transfer_selects_actual_destination(self):
        fee = 5_000
        # A is fee payer, and moves 9 SOL to R.
        keys = ["A", "R"]
        pre = [100 * LAMPORTS_PER_SOL, 0]
        post = [91 * LAMPORTS_PER_SOL - fee, 9 * LAMPORTS_PER_SOL]
        self.assertEqual(sum(pre) - sum(post), fee)
        self.assertEqual(source_equivalent_pick(keys, pre, post, fee, "A"),
                         ("R", 9.0))

    def test_two_unrelated_transfers_create_false_edge_to_fee_payer(self):
        fee = 5_000
        # D pays fees and signs. The two ACTUAL System instructions are:
        #     A -> R: 9 SOL
        #     U -> D: 10 SOL
        # There is NO A -> D instruction, no D authority over A, and
        # no shared beneficial owner is implied by this synthetic message.
        instructions = [("A", "R", 9), ("U", "D", 10)]
        keys = ["D", "A", "U", "R"]
        signed_by = {"D", "A", "U"}
        pre = [1 * LAMPORTS_PER_SOL, 100 * LAMPORTS_PER_SOL,
               100 * LAMPORTS_PER_SOL, 0]
        post = [11 * LAMPORTS_PER_SOL - fee, 91 * LAMPORTS_PER_SOL,
                90 * LAMPORTS_PER_SOL, 9 * LAMPORTS_PER_SOL]
        self.assertEqual(sum(pre) - sum(post), fee)
        self.assertFalse(any(src == "A" and dst == "D"
                             for src, dst, _ in instructions))

        # The code's inferred transfer endpoint is D, not the actual R.
        inferred_dst, inferred_sol = source_equivalent_pick(
            keys, pre, post, fee, "A"
        )
        self.assertEqual((inferred_dst, inferred_sol), ("D", 9.0))
        # A downstream summary checking only message signer flags would
        # count this *wrongly inferred* endpoint as a fee-paying signer.
        self.assertIn(inferred_dst, signed_by)
        self.assertEqual(inferred_dst, keys[0])
        self.assertIn(("A", "R", 9), instructions)

if __name__ == "__main__":
    unittest.main()
