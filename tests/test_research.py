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

    def test_new_wallet_forensics_sources_pinned_and_discoverable(self):
        idx = load_index()
        self.assertGreaterEqual(len(idx["items"]), 27)
        named = {x["id"]: x for x in idx["items"]}
        required = ("forensic-raw-sol-replay",
                    "developer-funding-convergence",
                    "wallet-first-funder-unknown",
                    "wallet-clustering-cross-layer-unknown",
                    "holder-supply-coverage-method")
        for key in required:
            self.assertIn(key, named)
            self.assertEqual(len(named[key]["commit"]), 40)
            self.assertEqual(named[key]["availability"], "remote_on_demand")
        funding = select_sources("最早资金 首次资金来源 未知 RPC分页", limit=12)
        self.assertIn("wallet-first-funder-unknown", [x["id"] for x in funding])
        dev = select_sources("开发者 发币钱包 上游资金 多跳 dev", limit=12)
        self.assertIn("developer-funding-convergence", [x["id"] for x in dev])
        recon = select_sources("原始交易 交易复算 SOL资金 原始签名 forensic", limit=12)
        self.assertIn("forensic-raw-sol-replay", [x["id"] for x in recon])

    def test_unknown_first_funder_is_not_proof_of_independence(self):
        idx = load_index()
        a = next(x for x in idx["items"] if x["id"] == "wallet-first-funder-unknown")
        b = next(x for x in idx["items"] if x["id"] == "wallet-clustering-cross-layer-unknown")
        self.assertIn("null", a["why"])
        self.assertIn("independent[]", b["why"])
        self.assertIn("must not be treated", a["why"])

    def test_real_problem_fetches_precise_source_topics(self):
        packet = build_packet("同源资金是不是交易所hub，如何排除共同基础设施？")
        ids = {r["id"] for r in packet["sources"]}
        self.assertIn("funding-graph-control", ids)
        self.assertEqual(packet["research_status"], "EVIDENCE_REQUIRED")
        self.assertEqual(packet["observations"]["state"], "DECISION_TIME_MISSING")
        self.assertFalse(packet["observations"]["accepted"])

    def test_profit_question_does_not_claim_an_edge(self):
        packet = build_packet("发现钱包协调以后，跟单能赚钱吗？利润和成本如何判断")
        self.assertIn("tradability-vs-structure", [r["id"] for r in packet["sources"]])
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
        ref = next(x for x in select_sources(q) if x["id"] == "funding-graph-control")
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

    def test_source_registry_rejects_non_allowlisted_repository(self):
        original = load_index()
        bad = copy.deepcopy(original)
        bad["items"][0]["repository"] = "evilcorp/unknown"
        with TemporaryDirectory() as d:
            path = Path(d)/"bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not allowed"):
                load_index(path)

    def test_marketwide_source_bridge_includes_coordination_and_tool_docs(self):
        idx = load_index()
        ids = {item["id"] for item in idx["items"]}
        self.assertTrue({
            "hermes-sybil-coordination",
            "downstream-exit-structure",
            "slot-sequence-case",
            "okx-market-readonly",
        }.issubset(ids))
        okx = select_sources("OKX 行情 数据源 钱包交易", limit=12)
        self.assertIn("okx-market-readonly", {r["id"] for r in okx})
        self.assertTrue(all(r["availability"] == "remote_on_demand" for r in okx))
        coordination = select_sources("同 Slot 捆绑 交易顺序", limit=12)
        self.assertIn("slot-sequence-case", {r["id"] for r in coordination})

    def test_observation_without_source_is_rejected(self):
        p = build_packet("钱包资金同源", decision_time="2026-10-29T07:00:05Z",
          observations=[{"claim": "unknown", "observed_at": "2026-10-29T07:00:00Z", "available_at": "2026-10-29T07:00:00Z"}])
        self.assertEqual(p["research_status"], "EVIDENCE_REQUIRED")
        self.assertEqual(p["observations"]["rejected"][0]["reason"], "MISSING_CLAIM_OR_SOURCE")
