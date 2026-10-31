import copy
import hashlib
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.knowledge import load_catalog, for_question, for_observation
from solana_meme_os.monitor import process

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "rules" / "monitor.v0.json").read_text())
FIRST = json.loads((ROOT / "fixtures" / "observation-1.json").read_text())
SECOND = json.loads((ROOT / "fixtures" / "observation-2.json").read_text())
NOW = datetime(2026, 10, 29, 7, 10, tzinfo=timezone.utc)


class KnowledgeTests(unittest.TestCase):
    def test_archived_knowledge_matches_pinned_original_git_blobs(self):
        manifest = json.loads((ROOT / "knowledge/legacy-snapshots/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["documents"]), 21)
        for entry in manifest["documents"]:
            raw = (ROOT / entry["snapshot_path"]).read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + bytes([0]) + raw).hexdigest()
            self.assertEqual(digest, entry["source_git_blob_sha"], entry["snapshot_path"])

    def test_catalog_has_pinned_provenance_and_nonempty_knowledge(self):
        catalog = load_catalog()
        self.assertGreaterEqual(len(catalog["cards"]), 15)
        for c in catalog["cards"]:
            self.assertTrue(c["required_evidence"])
            self.assertTrue(c["alternative_explanations"])
            self.assertIn(c["status"], {"source_contract", "documented_legacy_method", "unverified_hypothesis"})
            self.assertTrue(all(len(s["commit"]) == 40 for s in c["sources"]))

    def test_expanded_catalog_trigger_vocabulary_is_supported(self):
        catalog = load_catalog()
        self.assertEqual(len(catalog["cards"]), 24)
        ids = {c["id"] for c in catalog["cards"]}
        self.assertTrue({
            "first-funder-history-coverage",
            "sol-receipt-economic-semantics",
            "cashflow-count-value-inversion",
            "creator-fee-economic-path",
            "normal-bot-ecology-baseline",
            "trade-direction-source-gate",
            "market-utility-vs-tradability",
        }.issubset(ids))
        for card in catalog["cards"]:
            self.assertTrue(card["triggers"])
            self.assertTrue(all(isinstance(t, str) and t for t in card["triggers"]))

    def test_question_routes_real_concepts_not_generic_summary(self):
        routed = for_question("这批钱包同源资金会不会只是交易所转账？")
        self.assertEqual(routed["route_status"], "MATCHED_REFERENCE")
        self.assertIn("funding-graph", [c["id"] for c in routed["references"]])
        src = routed["references"][0]["sources"][0]
        self.assertTrue(src["url"].startswith("https://github.com/"))

    def test_unknown_question_is_not_hallucinated(self):
        routed = for_question("火星人的红色奶酪")
        self.assertEqual(routed["route_status"], "NO_KNOWN_REFERENCE")
        self.assertEqual(routed["references"], [])

    def test_liquidity_alert_uses_domain_knowledge_without_rug_conclusion(self):
        with TemporaryDirectory() as tmp:
            process(FIRST, RULES, Path(tmp), NOW, allow_fixture=True)
            result = process(SECOND, RULES, Path(tmp), NOW, allow_fixture=True)
        cards = result["knowledge"]["interpretation_candidates"]
        ids = [c["id"] for c in cards]
        self.assertIn("liquidity-depth", ids)
        self.assertIn("concentration", ids)
        lp = next(c for c in cards if c["id"] == "liquidity-depth")
        self.assertIn("价格变动", " ".join(lp["alternative_explanations"]))
        self.assertIn("不能断言", lp["inference_limit"])
        self.assertEqual(result["status"], "FIXTURE")
        self.assertTrue(result["no_trading"])

    def test_missing_fields_trigger_source_quality_questions(self):
        item = copy.deepcopy(FIRST)
        item["metrics"] = {}
        with TemporaryDirectory() as tmp:
            result = process(item, RULES, Path(tmp), NOW, allow_fixture=True)
        cards = [c["id"] for c in result["knowledge"]["interpretation_candidates"]]
        self.assertIn("gmgn-raw-prototype", cards)

    def test_card_malformed_source_fails_validation(self):
        bad = load_catalog()
        bad["cards"][0]["sources"][0]["commit"] = "main"
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps(bad), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unpinned"):
                load_catalog(path)

    def test_invalid_keyword_query_does_not_guess(self):
        with self.assertRaisesRegex(ValueError, "question required"):
            for_question("  ")

    def test_observation_without_alerts_has_baseline_domain_context(self):
        routed = for_observation({"alerts": [], "missing_fields": []})
        self.assertIn("BASELINE", routed["triggered_by"])
        self.assertGreater(len(routed["interpretation_candidates"]), 0)


if __name__ == "__main__":
    unittest.main()
