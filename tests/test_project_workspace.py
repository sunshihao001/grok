"""Cross-branch integration tests: mocked original Mint CLI → persisted report → original expertise."""
from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from solana_meme_os import mint_v01, project_navigator, project_workspace, public_token_accounts

MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"


class WorkspaceIntegrationTests(unittest.TestCase):
    def test_original_section_contains_valid_source_span(self):
        section = project_navigator.relevant_knowledge_section(
            "knowledge/domain/L3-E-L3-02-capital-organization-incentives.md",
            "资金来源钱包的经济主体如何判断")
        self.assertEqual(section["match_status"], "ORIGINAL_SECTION_LEXICAL_CANDIDATE")
        self.assertGreaterEqual(section["line_start"], 1)
        self.assertGreaterEqual(section["line_end"], section["line_start"])
        self.assertTrue(section["excerpt"])
        self.assertFalse(section["interpretation_validated"])

    def test_existing_mint_pipeline_to_original_knowledge_without_live_api(self):
        sample = {"jsonrpc": "2.0", "id": 1, "result": {"context": {"slot": 123}, "value": []}}
        raw_rpc = json.dumps(sample).encode()
        original_collect = public_token_accounts.collect

        def fake_rpc(mint):
            return original_collect(mint, request_fn=lambda method, params: raw_rpc,
                                    retrieved_at="2026-11-01T00:00:00Z")

        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "out"
            with patch("solana_meme_os.mint_v01.public_pair_report.fetch_pairs",
                       return_value=(b"[]", "https://api.dexscreener.com/test")):
                with patch("solana_meme_os.mint_v01.public_token_accounts.collect",
                           side_effect=fake_rpc):
                    with contextlib.redirect_stdout(io.StringIO()):
                        self.assertEqual(
                            mint_v01.main([MINT, "--rpc-holders", "--out-dir", str(path)]), 0)
            saved = path / "report.json"
            self.assertTrue(saved.is_file())
            result = project_workspace.build_brief(
                saved, "这些钱包是否存在共同资金来源",
                intent="FUNDING_ENTITY")
            self.assertEqual(result["mint"], MINT)
            self.assertTrue(result["read_only"])
            self.assertFalse(result["live_api_called"])
            self.assertFalse(result["grok_bot_called"])
            self.assertEqual(
                result["source_status_from_saved_report"]["dex_public_pairs"],
                "NO_PAIRS_RETURNED_COVERAGE_UNKNOWN")
            self.assertTrue(any("UNKNOWN" in x for x in result["unknown_source_coverage"]))
            self.assertTrue(result["original_knowledge_sections"])
            self.assertTrue(any(x["source_sha256"] for x in result["original_knowledge_sections"]))
            self.assertIn("原知识文件", project_workspace.render_markdown(result))

    def test_cross_branch_engineering_modules_are_present_but_not_invoked(self):
        navigation = project_navigator.shortlist(
            "分析这个Mint的Holder候选和流动性池", intent="MINT_OVERVIEW")
        candidates = navigation["routes"][0]["engineering_candidates_on_separate_branch"]
        self.assertTrue(candidates)
        self.assertTrue(all(c["available_in_current_checkout"] for c in candidates))
        self.assertTrue(all(c["invoked"] is False for c in candidates))
        self.assertTrue(all(c["source_of_record_branch"].startswith("research/") for c in candidates))

    def test_existing_knowledge_and_engineering_are_auditable_together(self):
        a = project_navigator.audit()
        self.assertTrue(a["ok"])
        self.assertEqual(a["engineering_paths_available_in_current_checkout"], 8)

    def test_reject_non_readonly_or_broken_report(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "report.json"
            for payload in ({"mint": MINT, "no_trading": False, "source_status": {}},
                            {"mint": MINT, "no_trading": True},
                            {"mint": 123, "no_trading": True, "source_status": {}}):
                with self.subTest(payload=payload):
                    p.write_text(json.dumps(payload), encoding="utf-8")
                    with self.assertRaises(ValueError):
                        project_workspace.build_brief(p, "钱包资金", intent="FUNDING_ENTITY")

    def test_no_matching_context_does_not_fabricate_claims(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "report.json"
            p.write_text(json.dumps({
                "mint": MINT, "no_trading": True,
                "source_status": {"dex_public_pairs": "UNAVAILABLE"},
                "source_errors": {"dex_public_pairs": "rate-limited"}}, ensure_ascii=False),
                encoding="utf-8")
            data = project_workspace.build_brief(
                p, "说不清楚一个没有关键词的问题")
            self.assertEqual(data["knowledge_route_candidates"], [])
            self.assertEqual(data["original_knowledge_sections"], [])
            self.assertIn("dex_public_pairs:UNAVAILABLE", data["unknown_source_coverage"])
            self.assertFalse(data["live_api_called"])


if __name__ == "__main__":
    unittest.main()
