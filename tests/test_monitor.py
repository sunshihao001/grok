import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from solana_meme_os.monitor import process
from solana_meme_os.gmgn_collect import collect

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "rules/monitor.v0.json").read_text(encoding="utf-8"))
FIRST = json.loads((ROOT / "fixtures/observation-1.json").read_text(encoding="utf-8"))
SECOND = json.loads((ROOT / "fixtures/observation-2.json").read_text(encoding="utf-8"))
NOW = datetime(2026, 10, 29, 7, 10, tzinfo=timezone.utc)


class TestMonitor(unittest.TestCase):
    def test_baseline_and_new_events_and_deltas(self):
        with TemporaryDirectory() as temp:
            path = Path(temp)
            first = process(FIRST, RULES, path, NOW, allow_fixture=True)
            self.assertEqual(first["status"], "FIXTURE")
            self.assertFalse(first["alerts"])
            second = process(SECOND, RULES, path, NOW, allow_fixture=True)
            self.assertEqual({a["type"] for a in second["alerts"]},
                             {"LIQUIDITY_DROP", "TOP10_SHARE_RISE", "NEW_SOURCE_EVENT"})
            repeated = process(SECOND, RULES, path, NOW, allow_fixture=True)
            self.assertEqual(repeated["status"], "IGNORED_NON_NEWER")
            self.assertEqual(repeated["alerts"], [])
            self.assertEqual(len((path / "runs.jsonl").read_text().splitlines()), 2)

    def test_fixture_cannot_pollute_live_state(self):
        with TemporaryDirectory() as temp:
            process(FIRST, RULES, Path(temp), NOW, allow_fixture=True)
            real = copy.deepcopy(SECOND)
            real["mode"] = "live"
            with self.assertRaisesRegex(ValueError, "cannot share"):
                process(real, RULES, Path(temp), NOW)

    def test_fixture_requires_explicit_mode(self):
        with TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "fixture"):
                process(FIRST, RULES, Path(temp), NOW)

    def test_live_stale_rejected_without_state_written(self):
        with TemporaryDirectory() as temp:
            item = copy.deepcopy(FIRST)
            item["mode"] = "live"
            with self.assertRaisesRegex(ValueError, "stale"):
                process(item, RULES, Path(temp), NOW + timedelta(hours=2))
            self.assertFalse(list(Path(temp).glob("*.json")))

    def test_missing_metric_is_unknown_not_zero(self):
        with TemporaryDirectory() as temp:
            item = copy.deepcopy(FIRST)
            item["metrics"].pop("liquidity_usd")
            result = process(item, RULES, Path(temp), NOW, allow_fixture=True)
            self.assertIn("liquidity_usd", result["missing_fields"])

    def test_reject_invalid_metric(self):
        with TemporaryDirectory() as temp:
            item = copy.deepcopy(FIRST)
            item["metrics"]["top10_holder_pct"] = 111
            with self.assertRaisesRegex(ValueError, "top10_holder_pct"):
                process(item, RULES, Path(temp), NOW, allow_fixture=True)


class TestGmgnAdapter(unittest.TestCase):
    def test_readonly_commands_and_explicit_unknown_mapping(self):
        with TemporaryDirectory() as temp:
            with patch("solana_meme_os.gmgn_collect.subprocess.run", return_value=SimpleNamespace(stdout='{"data": {}}')) as mock_run:
                path = collect(FIRST["token_address"], Path(temp))
            self.assertEqual(mock_run.call_count, 3)
            self.assertTrue(all("swap" not in str(c.args[0]) for c in mock_run.call_args_list))
            self.assertEqual(json.loads(path.read_text())["metrics"], {})


if __name__ == "__main__":
    unittest.main()
