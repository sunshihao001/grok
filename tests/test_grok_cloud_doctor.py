"""Checks the offline diagnostic without inventing Grok app entitlements."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from solana_meme_os.knowledge_system import ROOT

SCRIPT=ROOT/"scripts/grok_cloud_doctor.py"


class GrokCloudDoctorTests(unittest.TestCase):
    @staticmethod
    def _load():
        spec=importlib.util.spec_from_file_location("grok_cloud_doctor",SCRIPT)
        assert spec and spec.loader
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_static_preflight_is_honest(self):
        doc=self._load().inspect(ROOT)
        self.assertTrue(all(doc["required_files"].values()))
        self.assertFalse(doc["trading_authorized"])
        self.assertFalse(doc["rpc_live_data_verified"])
        self.assertIsNone(doc["grok_bot_created"])
        self.assertIsNone(doc["grok_skill_installed"])

    def test_probe_does_not_assume_any_checkout_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            report=self._load().inspect(Path(tmp))
            self.assertEqual(report["status"],"MISSING_LOCAL_PREREQUISITES")
            self.assertIsNone(report["git_commit"])

    def test_cli_returns_json_without_credentials(self):
        response=subprocess.run([sys.executable,str(SCRIPT),"--repo",str(ROOT)],
                                capture_output=True,text=True,cwd=ROOT)
        self.assertEqual(response.returncode,0,response.stderr)
        result=json.loads(response.stdout)
        self.assertNotIn("env",result)
        self.assertFalse(result["trading_authorized"])


if __name__=="__main__":
    unittest.main()
