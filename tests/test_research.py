"""Tests are offline: network source reads are mocked."""
from __future__ import annotations

from datetime import datetime, timezone
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from solana_meme_os.research import (build_packet, ephemeral_excerpt,
    evaluate_observations, load_index, select_sources)


class SourceBridgeTests(TestCase):
    def test_reference_index_pins_external_docs_without_copying_them(self):
        idx = load_index()
        self.assertGreaterEqual(len(idx["items"]), 15)
        third_party = [i for i in idx["items"] if "Why-Solana" in i["repository"]]
        self.assertGreaterEqual(len(third_party), 9)
        self.assertTrue(all(i.get("license_note") for i in third_party))
        self.assertTrue(all(i["availability"] == "remote_on_demand" for i in idx["items"]))

    def test_real_problem_fetches_precise_source_topics(self):
        packet = build_packet("同源资金是不是交易所hub，如何排除共同基础设施？")
        ids = {r["id"] for r in packet["sources"]}
        self.assertIn("hermes-source-relations", ids)
        self.assertNotIn("funding-graph-control", ids)
        self.assertGreater(packet["review_only_source_matches_withheld"], 0)
        self.assertEqual(packet["research_status"], "EVIDENCE_REQUIRED")
        self.assertEqual(packet["observations"]["state"], "DECISION_TIME_MISSING")
        self.assertFalse(packet["observations"]["accepted"])

    def test_profit_question_does_not_claim_an_edge(self):
        packet = build_packet("发现钱包协调以后，跟单能赚钱吗？利润和成本如何判断")
        self.assertNotIn("tradability-vs-structure", [r["id"] for r in packet["sources"]])
        reviewed = build_packet("发现钱包协调以后，跟单能赚钱吗？利润和成本如何判断", include_review_only=True)
        self.assertIn("tradability-vs-structure", [r["id"] for r in reviewed["sources"]])
        self.assertTrue(all(r["admission_state"] == "review_only" for r in reviewed["sources"] if r["repository"].endswith("Why-Solana-Memecoins-Are-Over")))
        self.assertIn("No evidence", packet["note"])

    def test_unknown_problem_calls_for_new_research(self):
        packet = build_packet("神秘xyz协议完全未知的事物")
        self.assertEqual(packet["reference_status"], "SOURCE_DISCOVERY_REQUIRED")
        self.assertFalse(packet["sources"])

    def test_time_boundary_accepts_past_facts_and_rejects_future(self):
        cutoff = "2026-10-29T07:00:05Z"
        facts = [
            {"claim": "wallet transfer", "source_ref": "solana:signature:A", "observed_at": "2026-10-29T07:00:00Z", "available_at": "2026-10-29T07:00:04Z"},
            {"claim": "future high", "source_ref": "source:B", "observed_at": "2026-10-29T07:05:00Z", "available_at": "2026-10-29T07:05:10Z"},
            {"claim": "late indexed", "source_ref": "source:C", "observed_at": "2026-10-29T06:00:00Z", "available_at": "2026-10-29T07:01:00Z"},
            {"claim": "missing availability", "source_ref": "source:D", "observed_at": "2026-10-29T06:00:00Z"}
        ]
        review = evaluate_observations(facts, cutoff)
        self.assertEqual(len(review["accepted"]), 1)
        self.assertEqual(len(review["rejected"]), 3)
        self.assertEqual(review["rejected"][0]["reason"], "NOT_KNOWN_AT_DECISION_TIME")

    def test_decision_timezone_required(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            evaluate_observations([], "2026-10-29T07:00:00")

    def test_remote_preview_only_approved_pinned_source(self):
        q = "同源资金是不是交易所hub"
        ref = next(x for x in select_sources(q) if x["id"] == "hermes-source-relations")
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, n): return "共同基础设施和资金路径不是控制权证据。".encode("utf-8")
        with patch("solana_meme_os.research.urlopen", return_value=Response()) as get:
            got = ephemeral_excerpt(ref, q, max_chars=400)
        self.assertTrue(got["excerpt_only"])
        self.assertIn("共同基础设施", got["excerpt"])
        self.assertIn(ref["commit"], get.call_args.args[0].full_url)
        forged = dict(ref)
        forged["commit"] = "0"*40
        with self.assertRaisesRegex(ValueError, "not selected"):
            ephemeral_excerpt(forged, q)


    def test_review_only_source_cannot_be_previewed_by_default(self):
        q = "同源资金交易所hub"
        review = next(x for x in select_sources(q, include_review_only=True)
                      if x["id"] == "funding-graph-control")
        with self.assertRaisesRegex(ValueError, "not selected"):
            ephemeral_excerpt(review, q)

    def test_review_only_research_units_are_withheld(self):
        q = "钱包协调以后，跟单能赚钱吗？"
        packet = build_packet(q)
        self.assertEqual(packet["research_unit_candidates"], [])
        explicit = build_packet(q, include_review_only=True)
        self.assertTrue(explicit["research_unit_candidates"])
        self.assertTrue(all(r["status"] == "external_reported"
                            for r in explicit["research_unit_candidates"]))

    def test_source_registry_rejects_non_allowlisted_repository(self):
        original = load_index()
        bad = copy.deepcopy(original)
        bad["items"][0]["repository"] = "evilcorp/unknown"
        with TemporaryDirectory() as d:
            path = Path(d)/"bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not allowed"):
                load_index(path)

    def test_observation_without_source_is_rejected(self):
        p = build_packet("钱包资金同源", decision_time="2026-10-29T07:00:05Z",
          observations=[{"claim": "unknown", "observed_at": "2026-10-29T07:00:00Z", "available_at": "2026-10-29T07:00:00Z"}])
        self.assertEqual(p["research_status"], "EVIDENCE_REQUIRED")
        self.assertEqual(p["observations"]["rejected"][0]["reason"], "MISSING_CLAIM_OR_SOURCE")
