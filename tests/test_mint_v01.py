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

if __name__ == '__main__': unittest.main()