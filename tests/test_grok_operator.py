"""Grok must execute GPT-built code at a fixed SHA, not develop it."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

from solana_meme_os.knowledge_system import ROOT
FILE=ROOT/"scripts/grok_operator.py"


def load():
    if str(ROOT/"scripts") not in sys.path:
        sys.path.insert(0,str(ROOT/"scripts"))
    spec=importlib.util.spec_from_file_location("grok_operator",FILE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class OperatorContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.operator=load()
        git=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,
                           capture_output=True,text=True,check=False)
        if git.returncode:
            raise unittest.SkipTest("Git checkout not available")
        cls.sha=git.stdout.strip()

    def test_no_external_installer_or_wallet_commands(self):
        text=FILE.read_text(encoding="utf-8")
        for prohibited in ("npx -y","onchainos ws start","sendTransaction"):
            self.assertNotIn(prohibited,text)

    def test_sha_mismatch_fails_without_running_demo(self):
        out=self.operator.demo(ROOT,"f"*40,test_suite=False,persist=False)
        self.assertEqual(out["status"],"OFFLINE_DEMO_FAILED")
        self.assertEqual(out["error"],"RELEASE_SHA_MISMATCH")

    def test_release_pin_required(self):
        out=self.operator.demo(ROOT,None,test_suite=False,persist=False)
        self.assertEqual(out["error"],"RELEASE_SHA_REQUIRED")

    def test_full_offline_demo_wires_existing_modules(self):
        out=self.operator.demo(ROOT,self.sha,test_suite=False,persist=False)
        self.assertEqual(out["status"],"OFFLINE_DEMO_PASSED",out.get("error"))
        self.assertEqual(out["checks"]["handoff"]["recipient_states"]["B02"],"CLAIMED")
        self.assertEqual(out["checks"]["monitor"]["status"],"FIXTURE_PASS")
        self.assertEqual(out["checks"]["okx_parser"]["status"],"FIXTURE_PASS")
        self.assertFalse(out["real_provider_connected"])
        self.assertFalse(out["production_monitor_enabled"])
        self.assertFalse(out["trading_authorized"])

    def test_cli_status_reports_honest_grok_state(self):
        r=subprocess.run([sys.executable,str(FILE),"status"],cwd=ROOT,
                         capture_output=True,text=True,check=False)
        self.assertEqual(r.returncode,0,r.stderr)
        out=json.loads(r.stdout)
        self.assertIsNone(out["grok_bot_created"])
        self.assertFalse(out["rpc_live_data_verified"])


if __name__=="__main__":
    unittest.main()
