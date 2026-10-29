"""Research ledger is a scoped, source-bound question queue, not alpha claims."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "knowledge/research_ledger.v0.json"
REGISTRY = ROOT / "knowledge/registry.v0.json"


class ResearchLedgerTests(unittest.TestCase):
    def test_all_sources_exist_and_nothing_claims_validation(self):
        records = json.loads(LEDGER.read_text(encoding="utf-8"))["records"]
        sources = {s["id"] for s in json.loads(REGISTRY.read_text(encoding="utf-8"))["sources"]}
        self.assertEqual(len(records), 10)
        self.assertEqual(len({r["id"] for r in records}), len(records))
        self.assertTrue(all(r["source_ids"] and set(r["source_ids"]) <= sources for r in records))
        self.assertTrue(all(r["state"].startswith(("UNVALIDATED_", "EXTERNAL_NEGATIVE_")) for r in records))

    def test_new_hypotheses_have_competing_hypotheses_and_falsifiers(self):
        rows = json.loads(LEDGER.read_text(encoding="utf-8"))["records"]
        active = [r for r in rows if r["kind"] == "hypothesis"]
        self.assertEqual(len(active), 6)
        for item in active:
            self.assertGreaterEqual(len(item["alternatives"]), 2)
            for key in ("population", "decision_clock", "baseline", "null_model",
                        "primary_metric", "falsifier", "next_experiment", "required_data"):
                self.assertTrue(item[key], f"{item['id']} missing {key}")

    def test_negative_knowledge_is_scope_bounded_and_reopenable(self):
        rows = json.loads(LEDGER.read_text(encoding="utf-8"))["records"]
        negatives = [r for r in rows if r["kind"] == "negative_reference"]
        self.assertEqual(len(negatives), 4)
        for r in negatives:
            self.assertTrue(r["scope"])
            self.assertTrue(r["reopen_only_if"])
            self.assertTrue(r["not_claimed"])


if __name__ == "__main__":
    unittest.main()
