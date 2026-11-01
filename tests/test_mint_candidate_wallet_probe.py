"""Real-adapter integration contract. All fixtures and network calls are offline."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from solana_meme_os.mint_candidate_wallet_probe import run, shortlist, validate_sources, target_mint_observation

MINT="DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
CREATOR="9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y"
OWNER="7Ej1sc9rwXZdxe9ZGcvCf8QrryFyjR6wj3emKnJXEdY9"
POOL="11111111111111111111111111111111"
VAULT="So11111111111111111111111111111111111111112"
SIG="3"*88


def rpc(result):
    return json.dumps({"jsonrpc":"2.0","result":result,"id":1}).encode()


def sources(root:Path):
    dexbytes=b'{"pairs":[]}'
    rugbytes=b'{"mint":"sample"}'
    report={
        "schema_version":"grok.mint_v01_combined.v0",
        "mint":MINT,"chain":"solana",
        "status":"READONLY_MULTISOURCE_CANDIDATES_NOT_FULL_MINT_INTELLIGENCE",
        "dex_public":{"chain":"solana","mint":MINT,"raw_input_sha256":hashlib.sha256(dexbytes).hexdigest(),
                      "pairs":[{"pool":POOL}]},
        "rugcheck_public":{
            "chain":"solana","mint":MINT,"source":{"input_sha256":hashlib.sha256(rugbytes).hexdigest()},
            "creator_vendor_candidate":CREATOR,
            "pool_vault_matches_vendor":[{"token_account":VAULT,"market":POOL}],
            "top_holders":[
                {"token_account_candidate":VAULT,"owner_candidate":POOL,
                 "role_interpretation":"VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE",
                 "source_path":"root.topHolders[0]"},
                {"token_account_candidate":OWNER,"owner_candidate":OWNER,
                 "role_interpretation":"UNCLASSIFIED_TOKEN_ACCOUNT_OWNER",
                 "source_path":"root.topHolders[1]"},
            ]},
        "rpc_token_accounts":None,
        "pool_related_holder_candidates":[],
    }
    (root/"dex-provider-raw.json").write_bytes(dexbytes)
    (root/"rugcheck-provider-raw.json").write_bytes(rugbytes)
    (root/"report.json").write_text(json.dumps(report))
    return report


def request(method,params):
    if method=="getSignaturesForAddress":
        return rpc([{"signature":SIG,"slot":501,"blockTime":1780000000,
                     "err":None,"confirmationStatus":"finalized"}])
    if method=="getTransaction":
        return rpc({"slot":501,"transaction":{"message":{"accountKeys":[
                    {"pubkey":CREATOR,"signer":True},{"pubkey":OWNER,"signer":False}]}},
                    "meta":{"err":None,"fee":5000,"preBalances":[100000,1000],
                            "postBalances":[95000,1000],
                            "preTokenBalances":[],"postTokenBalances":[]}})
    raise AssertionError(method)


class MintCandidateIntegrationTests(unittest.TestCase):
    def test_real_source_schema_to_limited_two_wallets_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            rdir=root/"input"
            rdir.mkdir()
            report=sources(rdir)
            calls=[]
            def fake(method,params):
                calls.append(method)
                return request(method,params)
            result=run(rdir,root/"evidence",request_fn=fake)
            self.assertEqual([x["wallet"] for x in result["wallet_probe_results"]],[CREATOR, OWNER])
            self.assertEqual(calls,["getSignaturesForAddress","getTransaction"]*2)
            self.assertEqual(result["selection"]["excluded_infrastructure_address_count"],2)
            self.assertEqual(result["discovery_coverage"],"NOT_MILLION_DISCOVERY_NO_HELIUS_KEY")
            self.assertFalse(result["wallet_probe_results"][0]["target_mint_observation"]
                             ["mint_in_reported_token_balances"])
            self.assertIsNone(result["actual_wallet_activity_count"])
            for row in result["wallet_probe_results"]:
                self.assertEqual(row["rpc_status"],"RAW_TRANSACTION_AVAILABLE_NOT_ECONOMICALLY_DECODED")
                self.assertEqual(row["signatures_returned"],1)
                self.assertEqual(row["observation"]["successful_swap"],"NOT_ASSESSED")
                rawpath=root/"evidence"/"wallets"/row["wallet"]/"wallet-first-transaction-raw.json"
                self.assertEqual(hashlib.sha256(rawpath.read_bytes()).hexdigest(),
                                 row["raw_sha256"]["wallet-first-transaction-raw.json"])
            self.assertTrue((root/"evidence"/"candidate-observations.json").is_file())

    def test_mint_creator_and_pool_filtered_even_when_vendor_calls_pool_biggest(self):
        row={"mint":MINT,"rugcheck_public":{"creator_vendor_candidate":POOL,
                "top_holders":[{"owner_candidate":POOL,"token_account_candidate":VAULT,
                                "role_interpretation":"VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE",
                                "source_path":"root.topHolders[0]"}]},
             "dex_public":{"pairs":[{"pool":POOL}]},"rpc_token_accounts":None}
        picked=shortlist(row)
        self.assertEqual(picked["candidates"],[])
        self.assertGreaterEqual(len(picked["skipped"]),1)

    def test_fresh_rpc_owner_from_token_account_not_beneficial_owner(self):
        row={"mint":MINT,"dex_public":{"pairs":[{"pool":POOL}]},"rugcheck_public":{},
             "rpc_token_accounts":{"rows":[
                 {"owner_candidate":OWNER,"owner_status":"RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER",
                  "owner_source_path":"getMultipleAccounts.result.value[0].data.parsed.info.owner",
                  "token_account":VAULT}]}}
        o=shortlist(row)
        self.assertEqual(o["candidates"][0]["source_kind"],
                         "FINALIZED_RPC_TOKEN_ACCOUNT_OWNER_HINT")
        self.assertEqual(o["candidates"][0]["economic_identity"],"UNKNOWN")

    def test_vendor_source_hash_tamper_rejected_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            sources(p)
            (p/"rugcheck-provider-raw.json").write_bytes(b'{"modified":1}')
            with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
                validate_sources(json.loads((p/"report.json").read_text()),p)
            with self.assertRaisesRegex(ValueError,"SHA256 mismatch"):
                run(p,p/"out",request_fn=lambda *_: self.fail("RPC called on bad evidence"))
            self.assertFalse((p/"out").exists())

    def test_public_rpc_failure_is_unknown_not_no_wallet_activities(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            p=root/"input"
            p.mkdir()
            sources(p)
            out=run(p,root/"out",max_wallets=1,
                    request_fn=lambda *_: (_ for _ in ()).throw(OSError("HTTP 429")))
            self.assertEqual(len(out["wallet_probe_results"]),1)
            self.assertEqual(out["wallet_probe_results"][0]["rpc_status"],
                             "RPC_UNAVAILABLE_NOT_ZERO_ACTIVITY")
            self.assertIsNone(out["wallet_probe_results"][0]["signatures_returned"])
            self.assertIsNone(out["actual_wallet_activity_count"])
            self.assertFalse((root/"out"/"wallets").exists())

    def test_stale_output_refused_and_probe_limit_strict(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            p=root/"input"
            p.mkdir()
            sources(p)
            out=root/"out"
            out.mkdir()
            (out/"old-task.md").write_text("stale")
            with self.assertRaisesRegex(ValueError,"must be empty"):
                run(p,out,request_fn=request)
            self.assertEqual((out/"old-task.md").read_text(),"stale")
            for n in (0,3,True):
                with self.assertRaises(ValueError):
                    shortlist(json.loads((p/"report.json").read_text()),max_wallets=n)

    def test_fixture_report_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            report=sources(p)
            report["status"]="FIXTURE_WITH_PUBLIC_SOURCES"
            with self.assertRaisesRegex(ValueError,"fixture"):
                validate_sources(report,p)


    def test_real_unrelated_usdc_transaction_is_not_a_meme_event(self):
        tx = {"jsonrpc":"2.0", "result":{"meta":{
                "preTokenBalances":[{"accountIndex":1,
                  "mint":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                  "owner":OWNER, "uiTokenAmount":{"amount":"49795913"}}],
                "postTokenBalances":[{"accountIndex":1,
                  "mint":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                  "owner":OWNER, "uiTokenAmount":{"amount":"0"}}],
                "err":None
            }}}
        observed=target_mint_observation(json.dumps(tx).encode(), MINT, OWNER)
        self.assertFalse(observed["mint_in_reported_token_balances"])
        self.assertEqual(observed["status"],
            "TARGET_MINT_NOT_IN_REPORTED_TOKEN_BALANCES_OF_THIS_BOUNDED_TX")
        self.assertFalse(observed["mint_trade_or_transfer_proven"])

    def test_target_mint_appearing_in_failed_tx_does_not_prove_wallet_buy(self):
        token={"mint":MINT, "accountIndex":6, "owner":POOL,
               "uiTokenAmount":{"amount":"100"}}
        tx={"jsonrpc":"2.0","result":{"meta":{
            "err":{"InstructionError":[2,{"Custom":1}]},
            "preTokenBalances":[token],"postTokenBalances":[token]}}}
        got=target_mint_observation(json.dumps(tx).encode(),MINT,CREATOR)
        self.assertTrue(got["mint_in_reported_token_balances"])
        self.assertFalse(got["queried_wallet_is_reported_mint_token_owner"])
        self.assertEqual(got["target_token_accounts_reported"],1)
        self.assertFalse(got["mint_trade_or_transfer_proven"])

    def test_missing_token_metadata_is_unknown_not_no_activity(self):
        got=target_mint_observation(json.dumps({"result":{"meta":{}}}).encode(),MINT,OWNER)
        self.assertIsNone(got["mint_in_reported_token_balances"])
        self.assertFalse(got["mint_trade_or_transfer_proven"])
        self.assertEqual(target_mint_observation(None,MINT,OWNER),
                         target_mint_observation(b"{",MINT,OWNER))

if __name__=="__main__":
    unittest.main()
