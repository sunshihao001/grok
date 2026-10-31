"""Offline M2 observatory contract and counterexample tests. No RPC or trades."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from solana_meme_os.market_observatory import analyze

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = json.loads((ROOT / "fixtures/market-observatory-synthetic.json").read_text(encoding="utf-8"))


class TestMarketObservatory(unittest.TestCase):
    def test_source_provenance_and_no_trade_claim(self):
        result = analyze(FIXTURE, allow_fixture=True)
        self.assertEqual(result["normalized_event_count"], 11)
        self.assertEqual(result["input_status"]["input_mode"], "fixture")
        self.assertFalse(result["abnormality_confirmed"])
        self.assertFalse(result["ownership_confirmed"])
        self.assertFalse(result["jito_bundle_confirmed"])
        self.assertFalse(result["paper_trade_qualified"])
        self.assertTrue(result["no_trading"])

    def test_window_exact_counts_and_distinct_meanings(self):
        result = analyze(FIXTURE, allow_fixture=True)
        market = next(x for x in result["window_aggregates"]
                      if x["scope"] == "MARKET_WIDE" and x["window_seconds"] == 30
                      and x["start"] == "2026-10-29T07:00:00Z")
        self.assertEqual(market["event_count"], 8)
        self.assertEqual(market["transaction_count"], 8)
        self.assertEqual(market["unique_wallet_count"], 6)
        self.assertEqual(market["unique_senders"], 4)
        self.assertEqual(market["unique_receivers"], 4)
        self.assertEqual(market["sol_transferred"], "10")
        self.assertEqual(market["sol_spent_on_buys"], "7.8")
        self.assertEqual(market["sol_received_from_sells"], "0")
        self.assertEqual(market["token_transferred"], {"Mint-ONE": "42"})
        self.assertEqual(market["anomaly_status"], "UNASSESSED_NO_BASELINE")
        mint = next(x for x in result["window_aggregates"]
                    if x["scope"] == "Mint-ONE" and x["window_seconds"] == 30)
        self.assertEqual(mint["event_count"], 4)
        self.assertEqual(mint["sol_transferred"], "0")
        self.assertEqual(mint["sol_spent_on_buys"], "3.8")

    def test_four_candidate_types_never_assert_operator_or_bundle(self):
        result = analyze(FIXTURE, allow_fixture=True)
        cand = result["group_candidates"]
        kinds = {x["kind"] for x in cand}
        self.assertIn("FUNDING_FANOUT", kinds)
        self.assertIn("TOKEN_CONSOLIDATION", kinds)
        self.assertIn("SAME_SLOT_MULTIWALLET_BUY", kinds)
        self.assertIn("FUNDING_TO_BUY_CANDIDATE", kinds)
        buy = next(x for x in cand if x["kind"] == "SAME_SLOT_MULTIWALLET_BUY")
        self.assertEqual(buy["unique_wallets"], 2)
        self.assertEqual(buy["sol_spent"], "3.8")
        self.assertEqual(buy["jito_bundle_status"], "UNVERIFIED")
        route = next(x for x in cand if x["kind"] == "TOKEN_CONSOLIDATION")
        self.assertEqual(route["unique_origins"], 2)
        self.assertEqual(route["token_transferred"], "42")
        self.assertEqual(route["subsequent_sale_status"], "NOT_CHECKED")
        relation = [x for x in cand if x["kind"] == "FUNDING_TO_BUY_CANDIDATE"
                    and x["mint"] == "Mint-ONE"][0]
        self.assertEqual(relation["candidate_funder"], "Funder-F")
        self.assertEqual(relation["unique_buyers"], 2)
        self.assertEqual(relation["relationship"], "TIME_BOUNDED_FLOW_HYPOTHESIS_NOT_OWNERSHIP")

    def test_idempotent_cross_provider_dedupe_with_source_refs(self):
        data = copy.deepcopy(FIXTURE)
        duplicate = copy.deepcopy(data["events"][0])
        duplicate["source_ref"] = "provider-secondary:tx0"
        data["events"].append(duplicate)
        out = analyze(data, allow_fixture=True)
        self.assertEqual(out["input_status"]["duplicate_records"], 1)
        self.assertEqual(out["normalized_event_count"], 11)
        first = next(x for x in out["events"] if x["signature"] == "sol-fund-a")
        self.assertEqual(first["source_refs"], sorted([
            "fixtures/market-observatory-synthetic.json", "provider-secondary:tx0"]))

    def test_conflicting_duplicate_identity_rejected(self):
        data = copy.deepcopy(FIXTURE)
        duplicate = copy.deepcopy(data["events"][0])
        duplicate["amount_raw"] = "5000000000"
        duplicate["source_ref"] = "another-provider"
        data["events"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "conflicting event identity"):
            analyze(data, allow_fixture=True)

    def test_decision_time_filters_late_and_unknown(self):
        data = copy.deepcopy(FIXTURE)
        data["events"][0].pop("available_at")
        output = analyze(data, allow_fixture=True, decision_at="2026-10-29T07:00:19Z")
        self.assertEqual(output["input_status"]["excluded"]["unknown_availability"], 1)
        self.assertEqual(output["input_status"]["excluded"]["post_decision"], 5)
        self.assertEqual(output["normalized_event_count"], 5)
        self.assertEqual(output["input_status"]["decision_time_filter"], "2026-10-29T07:00:19Z")

    def test_fixture_requires_explicit_opt_in(self):
        with self.assertRaisesRegex(ValueError, "fixture requires"):
            analyze(FIXTURE)

    def test_no_synthetic_profit_from_flow(self):
        res = analyze(FIXTURE, allow_fixture=True)
        self.assertTrue(all(x["anomaly_status"] == "UNASSESSED_NO_BASELINE"
                            for x in res["group_candidates"]))
        self.assertNotIn("profit", json.dumps(res["group_candidates"]).lower())

    def test_reject_non_timezone_timestamp(self):
        data = copy.deepcopy(FIXTURE)
        data["events"][0]["block_time"] = "2026-10-29T07:00:00"
        with self.assertRaisesRegex(ValueError, "timezone"):
            analyze(data, allow_fixture=True)

    def test_reject_float_amount_and_mint_mismatch(self):
        data = copy.deepcopy(FIXTURE)
        data["events"][0]["amount_raw"] = 2000000000.0
        with self.assertRaisesRegex(ValueError, "integer string"):
            analyze(data, allow_fixture=True)
        data = copy.deepcopy(FIXTURE)
        data["events"][4]["decimals"] = 9
        with self.assertRaisesRegex(ValueError, "inconsistent token decimals"):
            analyze(data, allow_fixture=True)

    def test_reject_different_instruction_kind_same_identity(self):
        data = copy.deepcopy(FIXTURE)
        duplicate = copy.deepcopy(data["events"][0])
        duplicate["event_kind"] = "TOKEN_TRANSFER"
        duplicate["mint"] = "Mint-ONE"
        duplicate["decimals"] = 2
        data["events"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "conflicting event identity"):
            analyze(data, allow_fixture=True)

    def test_reject_unsupported_window(self):
        with self.assertRaisesRegex(ValueError, "windows"):
            analyze(FIXTURE, allow_fixture=True, windows=(0,))
