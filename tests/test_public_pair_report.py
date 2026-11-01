import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from solana_meme_os.public_pair_report import compile_pairs, fetch_pairs, main, render_markdown, source_url

MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
POOL = "So11111111111111111111111111111111111111112"


def fake(*, role="BASE"):
    tokens = {"baseToken":{"address":MINT,"symbol":"BONK"},"quoteToken":{"address":POOL,"symbol":"SOL"}}
    if role == "QUOTE": tokens = {"baseToken": tokens["quoteToken"],"quoteToken": tokens["baseToken"]}
    return [{"chainId":"solana","dexId":"raydium","pairAddress":POOL,
             **tokens,"priceUsd":"0.01","liquidity":{"usd":1000},
             "volume":{"h24":500},"txns":{"h24":{"buys":5,"sells":3}},
             "pairCreatedAt":1770000000000}]

class FakeResponse:
    def __init__(self, raw): self.raw=raw; self.status=200
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def read(self, n): return self.raw

class PublicPairTests(unittest.TestCase):
    def test_public_url_fixed_valid_mint(self):
        self.assertEqual(source_url(MINT), "https://api.dexscreener.com/token-pairs/v1/solana/"+MINT)
        for mint in ("../etc/passwd","", "https://example.com/x", "_"*33):
            with self.assertRaises(ValueError): source_url(mint)

    def test_one_public_get_with_no_keys(self):
        seen=[]
        def getter(req, timeout):
            seen.append((req.full_url,req.get_method(),req.headers,timeout))
            return FakeResponse(b"[]")
        raw,url=fetch_pairs(MINT,opener=getter)
        self.assertEqual(raw,b"[]")
        self.assertEqual(seen[0][1],"GET")
        self.assertNotIn("Authorization",seen[0][2])
        self.assertEqual(seen[0][3],12)

    def test_base_pool_summary_provenance_and_unknowns(self):
        raw=json.dumps(fake()).encode()
        r=compile_pairs(raw,MINT,retrieved_at="2026-11-01T00:00:00Z",source=source_url(MINT))
        self.assertEqual(r["returned_pair_count"],1)
        self.assertEqual(r["pairs"][0]["price_usd_for_target"],"0.01")
        self.assertEqual(r["pairs"][0]["pair_transactions_24h"]["buys"],5)
        self.assertEqual(r["not_available"]["key_wallets"],"UNKNOWN_NOT_PROVIDED")
        self.assertIn("不等于Mint创建时间",render_markdown(r))
        self.assertTrue(r["no_trading"])

    def test_quote_mint_must_not_use_base_price(self):
        r=compile_pairs(json.dumps(fake(role="QUOTE")).encode(),MINT,retrieved_at="x",source="x")
        self.assertIsNone(r["pairs"][0]["price_usd_for_target"])
        self.assertEqual(r["pairs"][0]["price_status"],"UNKNOWN_QUOTE_TOKEN_PRICE")

    def test_reject_different_mint_or_chain(self):
        for patchdata in ( {"baseToken":{"address":POOL,"symbol":"SOL"},"quoteToken":{"address":POOL,"symbol":"SOL"}}, {"chainId":"ethereum"} ):
            case=fake()[0]
            case.update(patchdata)
            with self.assertRaises(ValueError): compile_pairs(json.dumps([case]).encode(), MINT,retrieved_at="x",source="x")

    def test_empty_response_no_false_no_pool_conclusion(self):
        r=compile_pairs(b"[]",MINT,retrieved_at="x",source="x")
        self.assertEqual(r["status"],"NO_PAIRS_RETURNED_COVERAGE_UNKNOWN")
        self.assertIn("不能断言",render_markdown(r))

    def test_invalid_shapes_fail_closed(self):
        for raw in (b"{}",b"not json",json.dumps([{"chainId":"solana"}]).encode()):
            with self.assertRaises(ValueError):compile_pairs(raw,MINT,retrieved_at="x",source="x")

    def test_cli_outputs_real_provider_response_format_only_when_fetched(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"out"
            with patch("solana_meme_os.public_pair_report.fetch_pairs",return_value=(json.dumps(fake()).encode(),source_url(MINT))):
                with contextlib.redirect_stdout(io.StringIO()) as buf:
                    code=main(["--mint",MINT,"--out-dir",str(out)])
            self.assertEqual(code,0)
            self.assertTrue((out/"provider-raw.json").is_file())
            self.assertEqual(json.loads((out/"report.json").read_text())["returned_pair_count"],1)
            self.assertEqual(json.loads(buf.getvalue())["no_trading"],True)

    def test_cli_public_unavailable_does_not_generate_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/"out"
            with patch("solana_meme_os.public_pair_report.fetch_pairs",side_effect=OSError("network disabled")):
                with contextlib.redirect_stderr(io.StringIO()):
                    code=main(["--mint",MINT,"--out-dir",str(out)])
            self.assertEqual(code,3)
            self.assertFalse(out.exists())

if __name__=="__main__":unittest.main()