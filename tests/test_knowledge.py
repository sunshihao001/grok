"""Deterministic, no-network knowledge intake checks."""
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.knowledge import DEFAULT_REGISTRY, contextualize, load_registry
from solana_meme_os.monitor import process

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "rules/monitor.v0.json").read_text(encoding="utf-8"))
FIRST = json.loads((ROOT / "fixtures/observation-1.json").read_text(encoding="utf-8"))
SECOND = json.loads((ROOT / "fixtures/observation-2.json").read_text(encoding="utf-8"))


class TestKnowledgeIntake(unittest.TestCase):
    def test_pinned_sources_and_pack_are_present(self):
        reg = load_registry()
        self.assertEqual(reg["version"], "KB-001.0")
        self.assertEqual(len(reg["sources"]), 7)
        self.assertEqual(reg["packs"][0]["stage"], "reference_only")
        self.assertTrue((ROOT / reg["packs"][0]["path"]).exists())

    def test_snapshot_and_missing_data_have_readable_guidance(self):
        result = contextualize({"alerts": [], "missing_fields": ["liquidity_usd"]})
        self.assertEqual(result["status"], "REFERENCE_ONLY_NOT_VALIDATED")
        self.assertEqual({x["trigger"] for x in result["guidance"]}, {"SNAPSHOT", "MISSING_DATA"})
        self.assertTrue(all(x["verify"] for x in result["guidance"]))

    def test_bad_source_and_escaped_pack_fail_closed(self):
        original = load_registry()
        for mutate in ("sha", "path"):
            with self.subTest(mutate=mutate), TemporaryDirectory(dir=ROOT) as tmp:
                directory = Path(tmp)
                (directory / "knowledge" / "packs").mkdir(parents=True)
                doc = directory / "knowledge" / "packs" / "KB-001-evidence-bounds.md"
                doc.write_text("known pack", encoding="utf-8")
                reg = copy.deepcopy(original)
                if mutate == "sha":
                    reg["sources"][0]["blob_sha"] = "unverified"
                else:
                    reg["packs"][0]["path"] = "knowledge/../README.md"
                catalog = directory / "knowledge" / "registry.v0.json"
                catalog.write_text(json.dumps(reg), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_registry(catalog)

    def test_monitor_attaches_knowledge_without_changing_existing_alerts(self):
        with TemporaryDirectory() as tmp:
            process(FIRST, RULES, Path(tmp), allow_fixture=True)
            report = process(SECOND, RULES, Path(tmp), allow_fixture=True)
            self.assertEqual({a["type"] for a in report["alerts"]},
                             {"LIQUIDITY_DROP", "TOP10_SHARE_RISE", "NEW_SOURCE_EVENT"})
            self.assertEqual(report["knowledge_context"]["status"], "REFERENCE_ONLY_NOT_VALIDATED")
            self.assertTrue({"SNAPSHOT", "LIQUIDITY_DROP", "TOP10_SHARE_RISE", "NEW_SOURCE_EVENT"}.issubset(
                {x["trigger"] for x in report["knowledge_context"]["guidance"]}))
            self.assertNotIn("gate_decision", report)


if __name__ == "__main__":
    unittest.main()
