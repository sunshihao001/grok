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
                      if x["scope"] == "INPUT_COHORT_ALL_MINTS" and x["window_seconds"] == 30
                      and x["start"] == "2026-10-29T07:00:00Z")
        self.assertEqual(market["event_count"], 8)
        self.assertEqual(market["transaction_count"], 8)
        self.assertEqual(market["unique_actor_addresses"], 6)
        self.assertEqual(market["unique_trade_wallets"], 3)
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

    def test_rolling_candidates_cross_fixed_bucket_boundaries(self):
        data = copy.deepcopy(FIXTURE)
        data["events"] = data["events"][:2]
        data["events"][0]["block_time"] = "2026-10-29T07:00:29Z"
        data["events"][0]["available_at"] = "2026-10-29T07:00:29Z"
        data["events"][0]["received_at"] = "2026-10-29T07:00:29Z"
        data["events"][1]["block_time"] = "2026-10-29T07:00:31Z"
        data["events"][1]["available_at"] = "2026-10-29T07:00:31Z"
        data["events"][1]["received_at"] = "2026-10-29T07:00:31Z"
        out = analyze(data, allow_fixture=True, windows=(30,))
        self.assertEqual(len([c for c in out["group_candidates"]
                              if c["kind"] == "FUNDING_FANOUT"]), 1)
        self.assertEqual(len([w for w in out["window_aggregates"]
                              if w["scope"] == "INPUT_COHORT_ALL_MINTS"]), 2)

    def test_cross_mint_is_descriptive_not_entity_identity(self):
        out = analyze(FIXTURE, allow_fixture=True)
        recurring = [x for x in out["group_candidates"]
                     if x["kind"] == "CROSS_MINT_FUNDING_REUSE"
                     and x["candidate_funder"] == "Funder-F"]
        self.assertEqual(len(recurring), 1)
        self.assertEqual(recurring[0]["mints"], ["Mint-ONE", "Mint-TWO"])
        self.assertEqual(recurring[0]["economic_owner_status"], "UNVERIFIED")
        activity = [x for x in out["group_candidates"]
                    if x["kind"] == "CROSS_MINT_WALLET_ACTIVITY"]
        self.assertEqual(activity[0]["wallet"], "Wallet-A")
        self.assertEqual(activity[0]["role_status"], "UNCLASSIFIED")

    def test_distinct_instruction_events_same_tx_not_double_transaction(self):
        data = copy.deepcopy(FIXTURE)
        event = copy.deepcopy(data["events"][0])
        event["instruction_index"] = 1
        event["amount_raw"] = "1000000000"
        data["events"].append(event)
        out = analyze(data, allow_fixture=True, windows=(30,))
        market = next(x for x in out["window_aggregates"]
                      if x["scope"] == "INPUT_COHORT_ALL_MINTS"
                      and x["start"] == "2026-10-29T07:00:00Z")
        self.assertEqual(market["event_count"], 9)
        self.assertEqual(market["transaction_count"], 8)
        self.assertEqual(market["sol_transferred"], "11")

    def test_same_slot_funding_order_not_assumed(self):
        data = copy.deepcopy(FIXTURE)
        for e in data["events"]:
            if e["signature"] in {"sol-fund-a", "sol-fund-b"}:
                e["slot"] = 200
                e["block_time"] = "2026-10-29T07:00:10Z"
                e["available_at"] = "2026-10-29T07:00:10Z"
                e["received_at"] = "2026-10-29T07:00:11Z"
        result = analyze(data, allow_fixture=True)
        found = [x for x in result["group_candidates"]
                 if x["kind"] == "FUNDING_TO_BUY_CANDIDATE"
                 and x["mint"] == "Mint-ONE"]
        self.assertFalse(found, "same Slot without transaction indices is not proven funding-before-buy")

    def test_same_slot_proven_execution_order_allows_candidate(self):
        data = copy.deepcopy(FIXTURE)
        for e in data["events"]:
            if e["signature"] in {"sol-fund-a", "sol-fund-b"}:
                e["slot"] = 200
                e["block_time"] = "2026-10-29T07:00:10Z"
                e["available_at"] = "2026-10-29T07:00:10Z"
                e["received_at"] = "2026-10-29T07:00:11Z"
                e["transaction_index"] = 2
            if e["signature"].startswith("buy-m1"):
                e["transaction_index"] = 3
        result = analyze(data, allow_fixture=True)
        found = [x for x in result["group_candidates"]
                 if x["kind"] == "FUNDING_TO_BUY_CANDIDATE"
                 and x["mint"] == "Mint-ONE"]
        self.assertEqual(len(found), 1)

    def test_receive_time_must_not_precede_source_availability(self):
        data = copy.deepcopy(FIXTURE)
        data["events"][0]["received_at"] = "2026-10-28T07:00:00Z"
        with self.assertRaisesRegex(ValueError, "received_at"):
            analyze(data, allow_fixture=True)

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
