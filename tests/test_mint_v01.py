from pathlib import Path
import contextlib
import io
import json
import tempfile
import unittest
from unittest.mock import patch
from solana_meme_os import mint_v01, public_token_accounts

MINT="DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"

class TestMintV01(unittest.TestCase):
    def test_one_mint_routes_public_without_wallet_or_keys(self):
        with patch('solana_meme_os.mint_v01.public_pair_report.main',return_value=2) as fn:
            self.assertEqual(mint_v01.main([MINT]),2)
            self.assertEqual(fn.call_args.args[0][0:2],["--mint", MINT])
    def test_saved_okx_routes_to_mature_adapter(self):
        with patch('solana_meme_os.mint_v01.mint_report.main',return_value=0) as fn:
            self.assertEqual(mint_v01.main([MINT,'--okx-json','okx.json','--out-dir','out']),0)
            self.assertIn('--okx-json',fn.call_args.args[0])
            self.assertEqual(fn.call_args.args[0][-1],'out')
    def test_fixture_flag_requires_saved_json(self):
        with self.assertRaises(SystemExit): mint_v01.main([MINT, '--fixture'])
    def test_fixture_flag_passed_through(self):
        with patch('solana_meme_os.mint_v01.mint_report.main',return_value=0) as fn:
            mint_v01.main([MINT,'--okx-json','okx.json','--fixture'])
            self.assertIn('--fixture',fn.call_args.args[0])

    def test_rpc_optin_combines_public_pool_with_onchain_token_accounts(self):
        sample = {"jsonrpc": "2.0", "id": 1,
                  "result": {"context": {"slot": 123}, "value": []}}
        raw = json.dumps(sample).encode()
        original_collect = public_token_accounts.collect
        def local_rpc(mint):
            return original_collect(mint, request_fn=lambda method, params: raw,
                                                retrieved_at="2026-11-01T00:00:00Z")
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(b"[]", "https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           side_effect=local_rpc):
                    with contextlib.redirect_stdout(io.StringIO()):
                        code = mint_v01.main([MINT, "--rpc-holders", "--out-dir", str(out)])
            self.assertEqual(code, 0)
            obj = json.loads((out/"report.json").read_text())
            self.assertEqual(obj["source_status"]["dex_public_pairs"],
                             "NO_PAIRS_RETURNED_COVERAGE_UNKNOWN")
            self.assertEqual(obj["source_status"]["solana_public_rpc_token_accounts"],
                             "EMPTY_TOP_TOKEN_ACCOUNT_SAMPLE_COVERAGE_UNKNOWN")
            self.assertTrue(obj["no_trading"])
            self.assertEqual((out/"rpc-largest-accounts-raw.json").read_bytes(), raw)
            self.assertTrue((out/"dex-provider-raw.json").is_file())
            self.assertIn("不是前20个真实持有人", (out/"report.md").read_text())

    def test_rpc_failure_keeps_actual_pool_result_with_unknown_status(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(b"[]", "https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           side_effect=OSError("RPC limited")):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(mint_v01.main([MINT,"--rpc-holders","--out-dir",str(out)]),0)
            result=json.loads((out/"report.json").read_text())
            self.assertEqual(result["source_status"]["solana_public_rpc_token_accounts"],"UNAVAILABLE")
            self.assertIn("RPC limited",result["source_errors"]["public_rpc_token_accounts"])
            self.assertIsNone(result["rpc_token_accounts"])

    def test_all_public_sources_unavailable_does_not_make_success_report(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       side_effect=OSError("no DEX")):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           side_effect=OSError("no RPC")):
                    with contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(mint_v01.main([MINT,"--rpc-holders","--out-dir",str(out)]),3)
            self.assertFalse(out.exists())

    def test_saved_okx_fixture_and_rpc_are_separate_evidence_not_live_verified(self):
        envelope={"ok":True,"data":{"workflow":"token-research","address":MINT,"chain":"501",
                 "core":{"info":{"name":"Test"}},"structure":{"holders":{"list":[]}}}}
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"out"
            infile=Path(temp)/"okx.json";infile.write_text(json.dumps(envelope))
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       side_effect=OSError("public endpoint offline")):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           side_effect=OSError("RPC offline")):
                    with contextlib.redirect_stdout(io.StringIO()):
                        code=mint_v01.main([MINT,"--okx-json",str(infile),"--fixture",
                                            "--rpc-holders","--out-dir",str(out)])
            self.assertEqual(code,0)
            result=json.loads((out/"report.json").read_text())
            self.assertEqual(result["status"],"FIXTURE_WITH_PUBLIC_SOURCES")
            self.assertEqual(result["source_status"]["okx_saved_json"],"FIXTURE_DEMO_ONLY")
            self.assertEqual(result["source_status"]["dex_public_pairs"],"UNAVAILABLE")
            self.assertEqual((out/"okx-saved-input.json").read_bytes(),infile.read_bytes())

    def test_invalid_saved_okx_does_not_silently_fall_back_to_public_sources(self):
        with tempfile.TemporaryDirectory() as temp:
            infile=Path(temp)/"wrong.json"
            infile.write_text(json.dumps({"ok":False}))
            out=Path(temp)/"out"
            with contextlib.redirect_stderr(io.StringIO()):
                status=mint_v01.main([MINT,"--okx-json",str(infile),"--rpc-holders",
                                      "--out-dir",str(out)])
            self.assertEqual(status,3)
            self.assertFalse(out.exists())

    def test_rugcheck_cached_report_enriches_one_mint_without_rpc(self):
        token_account="So11111111111111111111111111111111111111112"
        raw=json.dumps({"mint":MINT,"creator":"11111111111111111111111111111111",
                        "topHolders":[{"address":token_account,"owner":"11111111111111111111111111111111",
                                        "pct":12.5}],
                        "risks":[{"name":"Vendor Risk","level":"warn","score":5}]}).encode()
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(b"[]", "https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                           return_value=raw):
                    with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                               side_effect=AssertionError("must not contact limited RPC")):
                        with contextlib.redirect_stdout(io.StringIO()):
                            code=mint_v01.main([MINT,"--rugcheck","--out-dir",str(out)])
            self.assertEqual(code,0)
            result=json.loads((out/"report.json").read_text())
            self.assertEqual(result["source_status"]["solana_public_rpc_token_accounts"],"NOT_REQUESTED")
            self.assertEqual(len(result["rugcheck_public"]["top_holders"]),1)
            self.assertEqual(result["rugcheck_public"]["creator_vendor_candidate"],"11111111111111111111111111111111")
            self.assertEqual((out/"rugcheck-provider-raw.json").read_bytes(),raw)
            self.assertIn("免费报告可能缓存",(out/"report.md").read_text())

    def test_rugcheck_unavailable_is_unknown_not_fake_holder_count(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(b"[]", "https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                           side_effect=OSError("no vendor")):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(mint_v01.main([MINT,"--rugcheck","--out-dir",str(out)]),0)
            result=json.loads((out/"report.json").read_text())
            self.assertEqual(result["source_status"]["rugcheck_public_report"],"UNAVAILABLE")
            self.assertIsNone(result["rugcheck_public"])
            self.assertIn("no vendor",result["source_errors"]["rugcheck_public_report"])


    def test_cross_source_pool_owner_address_match_is_not_whale(self):
        pool_addr = "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB"
        token_account = "BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i"
        pool = {"pairs": [{"pool": pool_addr, "dex": "pumpswap", "source_path": "root[0]"}]}
        holders = {"top_holders": [{
            "token_account_candidate": token_account,
            "owner_candidate": pool_addr,
            "pct_vendor": 5.877731005322626,
            "source_path": "root.topHolders[0]",
        }]}
        records = mint_v01.pool_related_holder_observations(pool, holders)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["matched_as"], "owner_candidate")
        self.assertEqual(records[0]["matching_pool_address"], pool_addr)
        self.assertEqual(records[0]["holder_token_account"], token_account)
        self.assertIn("NOT_FREE_WHALE", records[0]["economic_interpretation"])
        self.assertIn("NOT_CHAIN_VERIFIED", records[0]["status"])

    def test_cross_source_requires_exact_match_and_both_sources(self):
        pool_addr = "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB"
        pool = {"pairs": [{"pool": pool_addr, "dex": "pumpswap"}]}
        holders = {"top_holders": [{"token_account_candidate": "BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i",
                                    "owner_candidate": "11111111111111111111111111111111",
                                    "pct_vendor": 99}]}
        self.assertEqual(mint_v01.pool_related_holder_observations(pool, holders), [])
        self.assertEqual(mint_v01.pool_related_holder_observations(None, holders), [])
        self.assertEqual(mint_v01.pool_related_holder_observations(pool, None), [])

    def test_cross_source_evidence_written_in_combined_report(self):
        pool_addr = "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB"
        account = "BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i"
        pool_raw = json.dumps([{"chainId": "solana", "pairAddress": pool_addr,
                                "dexId": "pumpswap",
                                "baseToken": {"address": MINT, "symbol": "TEST"},
                                "quoteToken": {"address": "So11111111111111111111111111111111111111112", "symbol":"SOL"}}]).encode()
        rug_raw = json.dumps({"mint": MINT, "topHolders": [{"address": account,
                    "owner": pool_addr, "pct": 5.88}]}).encode()
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(pool_raw, "https://api.dexscreener.com/token-pairs/v1/solana/" + MINT)):
                with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                           return_value=rug_raw):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(mint_v01.main([MINT,"--rugcheck","--out-dir",str(out)]),0)
            report=json.loads((out/"report.json").read_text())
            matches=report["pool_related_holder_candidates"]
            self.assertEqual(len(matches),1)
            self.assertEqual(matches[0]["holder_pct_vendor"],5.88)
            md=(out/"report.md").read_text()
            self.assertIn("禁止直接算作独立鲸鱼", md)
            self.assertTrue(report["no_trading"])



    def test_cross_vendor_pool_owner_overlap_is_flagged_not_called_a_whale(self):
        pool="So11111111111111111111111111111111111111112"
        token_account="11111111111111111111111111111111"
        vendor=json.dumps({"mint":MINT,"topHolders":[{"address":token_account,"owner":pool,
                             "pct":5.8}],
                          "knownAccounts":{pool:{"name":"Pool AMM","type":"AMM"}}}).encode()
        pair=json.dumps([{"chainId":"solana","dexId":"pumpswap","pairAddress":pool,
                           "baseToken":{"address":MINT,"symbol":"TEST"},
                           "quoteToken":{"address":"11111111111111111111111111111111","symbol":"SOL"}}]).encode()
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/"out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(pair,"https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                           return_value=vendor):
                    with contextlib.redirect_stdout(io.StringIO()):
                        status=mint_v01.main([MINT,"--rugcheck","--out-dir",str(dest)])
            self.assertEqual(status,0)
            report=json.loads((dest/"report.json").read_text())
            overlap=report["cross_source_pool_owner_matches"]
            self.assertEqual(len(overlap),1)
            self.assertEqual(overlap[0]["address"],pool)
            self.assertEqual(report["rugcheck_public"]["vendor_infrastructure_candidate_count"],1)
            self.assertIn("不列为已确认独立交易钱包",(dest/"report.md").read_text())


    def test_reconcile_exact_token_account_owner_agrees_not_beneficial_owner(self):
        acct = "So11111111111111111111111111111111111111112"
        owner = "11111111111111111111111111111111"
        vendor = {"mint": MINT, "retrieved_at": "2026-11-01T00:00:00Z",
                  "vendor_detected_at": "2026-10-30T00:00:00Z",
                  "top_holders": [{"token_account_candidate": acct, "owner_candidate": owner,
                                   "source_path": "root.topHolders[2]", "amount_raw_vendor": "100"}]}
        rpc = {"mint": MINT, "retrieved_at": "2026-11-02T00:00:00Z",
               "rpc_slot_largest": 100, "rpc_slot_owner_lookup": 105,
               "rows": [{"token_account": acct, "owner_candidate": owner,
                         "owner_status": "RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER",
                         "source_path": "getTokenLargestAccounts.result.value[0]",
                         "owner_source_path": "getMultipleAccounts.result.value[0].data.parsed.info.owner",
                         "amount_raw_at_first_slot": "90"}]}
        x = mint_v01.reconcile_vendor_holders_with_rpc(vendor, rpc)
        self.assertEqual(x["matched_token_accounts"], 1)
        self.assertEqual(x["owner_address_agreements"], 1)
        self.assertEqual(x["owner_address_conflicts"], 0)
        self.assertIn("NOT_BENEFICIAL_OWNER_PROOF", x["observations"][0]["status"])
        self.assertEqual(x["observations"][0]["rpc_owner_lookup_slot"], 105)
        self.assertEqual(x["observations"][0]["vendor_path"], "root.topHolders[2]")
        self.assertTrue(x["observations"][0]["amounts_not_same_slot"])
        self.assertTrue(x["no_trading"])

    def test_reconcile_owner_disagreement_is_temporal_conflict_not_common_control(self):
        acct = "So11111111111111111111111111111111111111112"
        vendor = {"mint": MINT, "top_holders": [
            {"token_account_candidate": acct, "owner_candidate": "11111111111111111111111111111111"}]}
        rpc = {"mint": MINT, "rows": [
            {"token_account": acct, "owner_candidate": "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB",
             "owner_status": "RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER"}]}
        x = mint_v01.reconcile_vendor_holders_with_rpc(vendor, rpc)
        self.assertEqual(x["owner_address_conflicts"], 1)
        self.assertEqual(x["owner_address_agreements"], 0)
        self.assertIn("SNAPSHOTS_NOT_ATOMIC", x["observations"][0]["status"])

    def test_reconcile_shared_owner_without_exact_token_account_is_not_match(self):
        vendor = {"mint": MINT, "top_holders": [
            {"token_account_candidate": "So11111111111111111111111111111111111111112",
             "owner_candidate": "11111111111111111111111111111111"}]}
        rpc = {"mint": MINT, "rows": [
            {"token_account": "81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB",
             "owner_candidate": "11111111111111111111111111111111",
             "owner_status": "RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER"}]}
        x = mint_v01.reconcile_vendor_holders_with_rpc(vendor, rpc)
        self.assertEqual(x["status"], "NO_TOKEN_ACCOUNT_OVERLAP_COVERAGE_UNKNOWN")
        self.assertEqual(x["matched_token_accounts"], 0)
        self.assertEqual(x["vendor_accounts_not_in_rpc_top20"], 1)

    def test_reconcile_rpc_unresolved_not_mismatch_and_missing_source(self):
        acct = "So11111111111111111111111111111111111111112"
        vendor = {"mint": MINT, "top_holders": [
            {"token_account_candidate": acct, "owner_candidate": "11111111111111111111111111111111"}]}
        rpc = {"mint": MINT, "rows": [
            {"token_account": acct, "owner_candidate": None,
             "owner_status": "UNKNOWN_ACCOUNT_NOT_FOUND"}]}
        x = mint_v01.reconcile_vendor_holders_with_rpc(vendor, rpc)
        self.assertEqual(x["owner_comparison_unresolved"], 1)
        self.assertEqual(x["owner_address_conflicts"], 0)
        self.assertEqual(x["observations"][0]["status"], "TOKEN_ACCOUNT_MATCH_OWNER_UNRESOLVED")
        self.assertIsNone(mint_v01.reconcile_vendor_holders_with_rpc(vendor, None))
        self.assertIsNone(mint_v01.reconcile_vendor_holders_with_rpc(None, rpc))
        with self.assertRaises(ValueError):
            mint_v01.reconcile_vendor_holders_with_rpc(vendor, {**rpc, "mint": acct})

    def test_reconcile_top_20_missing_is_coverage_unknown_not_no_holder(self):
        vendor = {"mint": MINT, "top_holders": [
            {"token_account_candidate": "So11111111111111111111111111111111111111112",
             "owner_candidate": "11111111111111111111111111111111"}]}
        rpc = {"mint": MINT, "rows": []}
        x = mint_v01.reconcile_vendor_holders_with_rpc(vendor, rpc)
        self.assertEqual(x["vendor_accounts_not_in_rpc_top20"], 1)
        self.assertIn("COVERAGE_UNKNOWN", x["status"])
        self.assertIn("RPC_TOP20_ABSENCE_NOT_PROOF", x["limitations"][0])

    def test_reconcile_in_combined_report_without_any_extra_rpc_calls(self):
        acct = "So11111111111111111111111111111111111111112"
        owner = "11111111111111111111111111111111"
        raw = json.dumps({"mint": MINT,
                          "topHolders": [{"address": acct, "owner": owner, "amount": "1"}]}).encode()
        rpc = {"mint": MINT, "status": "RPC_TOKEN_ACCOUNTS_AND_OWNER_HINTS",
               "rpc_slot_largest": 120, "rpc_slot_owner_lookup": 123,
               "rows": [{"token_account": acct, "owner_candidate": owner,
                         "owner_status": "RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER",
                         "source_path": "getTokenLargestAccounts.result.value[0]",
                         "owner_source_path": "getMultipleAccounts.result.value[0].data.parsed.info.owner"}],
               "no_trading": True}
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "report"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(b"[]", "https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           return_value=(rpc, {})) as collect_mock:
                    with patch("solana_meme_os.mint_v01.public_rugcheck_report.fetch_report",
                               return_value=raw) as rug_mock:
                        with contextlib.redirect_stdout(io.StringIO()):
                            exit_code = mint_v01.main([MINT, "--rpc-holders", "--rugcheck",
                                                       "--out-dir", str(out)])
            self.assertEqual(exit_code, 0)
            collect_mock.assert_called_once_with(MINT)
            rug_mock.assert_called_once_with(MINT)
            report = json.loads((out / "report.json").read_text())
            x = report["holder_rpc_reconciliation"]
            self.assertEqual(x["matched_token_accounts"], 1)
            self.assertEqual(x["owner_address_agreements"], 1)
            md = (out / "report.md").read_text()
            self.assertIn("同 Token Account 跨源核对", md)
            self.assertIn("不证明经济同控", md)
            self.assertEqual((out / "rugcheck-provider-raw.json").read_bytes(), raw)
            self.assertTrue(report["no_trading"])


if __name__ == '__main__': unittest.main()