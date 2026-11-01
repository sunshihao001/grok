"""Admission integrity and contamination-boundary regressions (no live data)."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.source_admission import load_admission, is_routable, ADMISSION_FILE
from solana_meme_os.research import load_index, select_sources


class SourceAdmissionTests(unittest.TestCase):
    def test_21_source_pointers_have_exact_pins_and_explicit_status(self):
        index = load_index()
        admission = load_admission(index)
        self.assertEqual(len(admission), 21)
        self.assertEqual(sum(v["admission_state"] == "review_only" for v in admission.values()), 13)
        self.assertEqual(sum(v["admission_state"] == "context_candidate" for v in admission.values()), 8)

    def test_review_only_sources_never_enter_default_research(self):
        hits = select_sources("同源资金交易所hub预测跟单")
        self.assertTrue(all(v["admission_state"] == "context_candidate" for v in hits))
        self.assertFalse(any("Why-Solana" in v["repository"] for v in hits))
        explicit = select_sources("同源资金交易所hub预测跟单", include_review_only=True)
        self.assertTrue(any(v["admission_state"] == "review_only" for v in explicit))

    def test_missing_entry_fails_closed(self):
        index = load_index()
        data = json.loads(ADMISSION_FILE.read_text(encoding="utf-8"))
        data["items"].pop()
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "coverage mismatch"):
                load_admission(index, path)

    def test_modified_commit_cannot_retain_admission(self):
        index = load_index()
        data = json.loads(ADMISSION_FILE.read_text(encoding="utf-8"))
        data["items"][0]["commit"] = "0" * 40
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "pin conflicts"):
                load_admission(index, path)

    def test_unlisted_id_is_never_routable(self):
        admission = load_admission()
        self.assertFalse(is_routable("not-registered", admission, True))


if __name__ == "__main__":
    unittest.main()
