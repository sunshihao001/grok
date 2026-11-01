import json
import unittest

from solana_meme_os.public_rugcheck_report import compile_report, fetch_report, markdown, source_url

MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
OWNER = "11111111111111111111111111111111"
TOKEN_ACCOUNT = "So11111111111111111111111111111111111111112"


def sample():
    return {"mint": MINT, "creator": OWNER, "topHolders": [{
        "address": TOKEN_ACCOUNT, "owner": OWNER, "amount": "900000000000",
        "pct": 34.5, "insider": True}],
        "token": {"mintAuthority": None, "freezeAuthority": None},
        "creatorTokens": [{"mint": "another"}],
        "risks": [{"name": "High Holder Concentration", "score": 300, "level": "warn"}],
        "score_normalised": 29, "detectedAt": "2026-10-28T00:00:00Z", "markets": [{}]}


class FakeResponse:
    status = 200
    def __init__(self, body):
        self.body = body
    def __enter__(self): return self
    def __exit__(self, *_): return None
    def read(self, _limit): return self.body


class RugCheckTests(unittest.TestCase):
    def test_one_bounded_public_get_no_keys_or_refresh(self):
        seen = []
        def fetch(req, timeout):
            seen.append((req.full_url, req.get_method(), req.headers, timeout))
            return FakeResponse(json.dumps(sample()).encode())
        raw = fetch_report(MINT, opener=fetch)
        self.assertEqual(json.loads(raw)["mint"], MINT)
        self.assertEqual(seen[0][0], source_url(MINT))
        self.assertEqual(seen[0][1], "GET")
        self.assertEqual(seen[0][3], 12)
        self.assertNotIn("Authorization", seen[0][2])
        self.assertNotIn("refresh", seen[0][0])

    def test_vendor_caching_holders_creator_risk_not_proven(self):
        raw = json.dumps(sample()).encode()
        result = compile_report(raw, MINT, retrieved_at="2026-11-01T00:00:00Z")
        self.assertEqual(result["creator_vendor_candidate"], OWNER)
        self.assertEqual(result["top_holders"][0]["owner_candidate"], OWNER)
        self.assertEqual(result["top_holders"][0]["pct_vendor"], 34.5)
        self.assertEqual(result["creator_tokens_vendor_count"], 1)
        self.assertEqual(result["source"]["cache_policy"], "FREE_REPORT_MAY_BE_STALE")
        self.assertEqual(result["source"]["input_sha256"], __import__("hashlib").sha256(raw).hexdigest())
        self.assertIn("未独立复核", markdown(result))
        self.assertTrue(result["no_trading"])

    def test_bad_mint_and_response_rejected(self):
        for mint in ("", "../etc/passwd", "0"*40):
            with self.assertRaises(ValueError):
                source_url(mint)
        for obj in ({}, {"mint": OWNER}, {"mint": MINT,"topHolders":"not array"},
                    {"mint":MINT,"topHolders":[1]}):
            with self.assertRaises(ValueError):
                compile_report(json.dumps(obj).encode(), MINT)
        with self.assertRaises(ValueError):
            compile_report(b"<html>error</html>", MINT)

    def test_missing_holders_kept_unknown_not_zero_supply(self):
        r = compile_report(json.dumps({"mint": MINT}).encode(), MINT)
        self.assertEqual(r["top_holders_status"], "UNKNOWN_NOT_PROVIDED")
        self.assertEqual(r["top_holders_rows_returned"], 0)
        self.assertIsNone(r["creator_vendor_candidate"])
        self.assertIsNone(r["creator_tokens_vendor_count"])
        self.assertIn("缓存", markdown(r))


if __name__ == "__main__":
    unittest.main()
