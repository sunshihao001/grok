"""Competitor-inspired cross-Mint overlap using local RugCheck samples only."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from solana_meme_os import cross_mint_holders

M1 = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"
M2 = "So11111111111111111111111111111111111111112"
M3 = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
OWNER = "11111111111111111111111111111111"
POOL = "SysvarRent111111111111111111111111111111111"
ACC1 = "Vote111111111111111111111111111111111111111"
ACC2 = "Stake11111111111111111111111111111111111111"
ACC3 = "BPFLoaderUpgradeab1e11111111111111111111111"


def holder(owner, account, role="UNCLASSIFIED_TOKEN_ACCOUNT_OWNER", path="root.topHolders[0]"):
    return {
        "owner_candidate": owner, "token_account_candidate": account,
        "role_interpretation": role,
        "source_path": path,
    }


def saved(mint, holders, status="VENDOR_CACHED_SAMPLE_UNVERIFIED",
          pool_match=False):
    return {
        "mint": mint, "no_trading": True,
        "status": "READONLY_MULTISOURCE_CANDIDATES_NOT_FULL_MINT_INTELLIGENCE",
        "source_status": {"rugcheck_public_report": "RUGCHECK_CACHED_VENDOR_REPORT_NOT_INDEPENDENTLY_VERIFIED"},
        "rugcheck_public": {
            "mint": mint, "top_holders_status": status,
            "retrieved_at": "2026-11-01T00:00:00Z",
            "source": {"input_sha256": "original-provider-hash"},
            "top_holders": holders,
        },
        "pool_related_holder_candidates": (
            [{"holder_token_account": ACC3, "holder_owner_vendor": POOL}]
            if pool_match else []),
        "cross_source_pool_owner_matches": [],
    }


class CrossMintOverlapTests(unittest.TestCase):
    def _run(self, *reports):
        with tempfile.TemporaryDirectory() as td:
            paths = []
            for i, value in enumerate(reports):
                p = Path(td) / f"{i}.json"
                p.write_text(json.dumps(value), encoding="utf-8")
                paths.append(p)
            return cross_mint_holders.compare_saved_reports(paths)

    def test_shared_unclassified_owner_is_evidence_not_controller(self):
        a = saved(M1, [holder(OWNER, ACC1), holder(OWNER, ACC2, path="root.topHolders[1]")])
        b = saved(M2, [holder(OWNER, ACC3)])
        r = self._run(a, b)
        pair = r["pairs"][0]
        self.assertEqual(pair["shared_owner_candidates_count"], 1)
        self.assertEqual(r["reports"][0]["unclassified_unique_owner_candidates"], 1)
        self.assertEqual(len(pair["shared_owner_candidates"][0]["mint_a"]["token_account_candidates"]), 2)
        self.assertFalse(pair["same_economic_controller_proven"])
        self.assertFalse(pair["overlap_absence_proven"])
        self.assertEqual(r["network_calls"], 0)
        self.assertIn("不是资金同源图", cross_mint_holders.markdown(r))

    def test_known_amm_locker_and_pool_related_owners_are_excluded(self):
        a = saved(M1, [holder(OWNER, ACC1), holder(POOL, ACC3,
                role="VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE")])
        b = saved(M2, [holder(OWNER, ACC2), holder(POOL, ACC3)], pool_match=True)
        r = self._run(a, b)
        self.assertEqual(r["pairs"][0]["shared_owner_candidates_count"], 1)
        self.assertEqual(r["reports"][1]["sample_counts"]["infrastructure"], 1)
        self.assertEqual(r["pairs"][0]["shared_owner_candidates"][0]["owner_candidate"], OWNER)

    def test_missing_coverage_is_unknown_not_zero_overlap(self):
        a = saved(M1, [holder(OWNER, ACC1)])
        b = saved(M2, None, status="UNKNOWN_NOT_PROVIDED")
        r = self._run(a, b)
        self.assertIsNone(r["pairs"][0]["shared_owner_candidates_count"])
        self.assertEqual(r["pairs"][0]["comparison_status"], "UNKNOWN_SOURCE_COVERAGE")
        self.assertIn("不是零重叠", cross_mint_holders.markdown(r))

    def test_no_sample_match_is_not_absence_proof(self):
        a = saved(M1, [holder(OWNER, ACC1)])
        b = saved(M2, [holder(POOL, ACC2)])
        r = self._run(a, b)
        self.assertEqual(r["pairs"][0]["shared_owner_candidates_count"], 0)
        self.assertFalse(r["pairs"][0]["overlap_absence_proven"])

    def test_distinct_mints_required_and_max_five(self):
        a = saved(M1, [holder(OWNER, ACC1)])
        with self.assertRaises(ValueError):
            self._run(a, a)
        with self.assertRaises(ValueError):
            self._run(a)
        with self.assertRaises(ValueError):
            self._run(*[saved(m, []) for m in [M1, M2, M3, M1, M2, M3]])

    def test_offline_cli_writes_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            files = [base / "a" / "report.json", base / "b" / "report.json"]
            for p, obj in zip(files, [saved(M1, [holder(OWNER, ACC1)]),
                                      saved(M2, [holder(OWNER, ACC2)])]):
                p.parent.mkdir()
                p.write_text(json.dumps(obj), encoding="utf-8")
            out_json, out_md = base / "result.json", base / "result.md"
            with contextlib.redirect_stdout(io.StringIO()):
                code = cross_mint_holders.main([
                    str(files[0]), str(files[1]), "--out-json", str(out_json),
                    "--out-md", str(out_md)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out_json.read_text())["pairs"][0]["shared_owner_candidates_count"], 1)
            self.assertIn("只代表这些有限样本", out_md.read_text())


if __name__ == "__main__":
    unittest.main()
