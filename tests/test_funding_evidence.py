"""KB-002 synthetic-only regressions. No real addresses, no network."""
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.funding_evidence import examine

ROOT = Path(__file__).resolve().parents[1]
BASE = json.loads((ROOT / "fixtures/kb002-funding.json").read_text(encoding="utf-8"))


def item(sender: str, recipient: str, amount: int, signature: str = "synthetic-x", *,
         occurred: str = "2026-10-29T08:12:00Z", available: str = "2026-10-29T08:12:05Z",
         instruction: int = 0) -> dict:
    return {"asset": "SOL_NATIVE", "signature": signature, "instruction_index": instruction,
            "from_wallet": sender, "to_wallet": recipient, "lamports": amount,
            "block_time": occurred, "available_at": available, "source_ref": f"fixture:{signature}:{instruction}"}


class FundingEvidenceTests(unittest.TestCase):
    def test_direct_inbound_candidate_is_never_owner_claim(self):
        result = examine(BASE)
        self.assertEqual(result["status"], "REFERENCE_ONLY_NOT_VALIDATED")
        self.assertEqual(len(result["groups"]), 2)
        group = next(g for g in result["groups"] if g["relation"] == "observed_shared_inbound")
        self.assertEqual(group["recipient_count"], 2)
        self.assertEqual({x["source_ref"] for x in group["evidence"]}, {"fixture:tx-a", "fixture:tx-b"})
        self.assertIn("!=", group["caveat"])
        self.assertNotIn("gate_decision", result)

    def test_hub_is_excluded_without_hiding_edges(self):
        result = examine(BASE)
        hub = next(g for g in result["groups"] if g["relation"] == "hub_excluded")
        self.assertEqual(hub["recipient_count"], 2)
        self.assertEqual(result["counts"]["dust_like_count"], 1)

    def test_unknown_source_requires_hub_review(self):
        doc = copy.deepcopy(BASE)
        doc["transfers"] += [item("9"*32,"2"*32,10000000,"u1"),
                              item("9"*32,"3"*32,10000000,"u2")]
        result = examine(doc)
        self.assertIn("needs_hub_review", {g["relation"] for g in result["groups"]})

    def test_future_available_and_future_occurrence_are_excluded(self):
        result = examine(BASE)
        self.assertEqual(result["counts"]["excluded_future_available"], 1)
        doc = copy.deepcopy(BASE)
        doc["transfers"].append(item("8"*32,"2"*32,10000000,"fut",
                                     occurred="2026-10-29T08:40:00Z",available="2026-10-29T08:40:01Z"))
        self.assertEqual(examine(doc)["counts"]["excluded_future_available"], 2)

    def test_funding_threshold_is_illustrative_not_protocol_fact(self):
        doc = copy.deepcopy(BASE)
        doc["policy"]["status"] = "validated_alpha"
        with self.assertRaisesRegex(ValueError, "illustrative"):
            examine(doc)

    def test_incomplete_or_failed_rpc_never_claims_no_link(self):
        doc = copy.deepcopy(BASE)
        doc["transfers"] = []
        doc["coverage"]["rpc_errors"] = 1
        result = examine(doc)
        self.assertEqual(result["groups"], [])
        self.assertEqual(result["coverage_state"], "UNKNOWN_INCOMPLETE")
        self.assertTrue(result["absence_interpretation"].startswith("No observed"))

    def test_duplicate_signature_instruction_and_invalid_lamports_rejected(self):
        doc = copy.deepcopy(BASE)
        doc["transfers"].append(copy.deepcopy(doc["transfers"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate signature"):
            examine(doc)
        doc = copy.deepcopy(BASE)
        doc["transfers"][0]["lamports"] = True
        with self.assertRaisesRegex(ValueError, "lamports"):
            examine(doc)

    def test_two_instructions_in_one_signature_are_separately_auditable(self):
        doc = copy.deepcopy(BASE)
        doc["transfers"] = [
            item("6"*32, "2"*32, 11000000, "same-sig", instruction=0),
            item("6"*32, "3"*32, 12000000, "same-sig", instruction=1)]
        self.assertEqual(len(examine(doc)["groups"][0]["evidence"]), 2)

    def test_future_hub_label_is_rejected(self):
        doc = copy.deepcopy(BASE)
        doc["sources"][0]["checked_at"] = "2026-10-29T09:00:00Z"
        with self.assertRaisesRegex(ValueError, "cutoff"):
            examine(doc)

    def test_live_modes_cannot_sneak_into_fixture_runner(self):
        doc = copy.deepcopy(BASE)
        doc["mode"] = "live"
        with self.assertRaisesRegex(ValueError, "fixtures"):
            examine(doc)


if __name__ == "__main__":
    unittest.main()
