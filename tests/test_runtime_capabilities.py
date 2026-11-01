"""Provider capability policies must remain disabled in the read-only research phase."""
import json
import unittest
from solana_meme_os.knowledge_system import ROOT


class ProviderRuntimePolicyTests(unittest.TestCase):
    def setUp(self):
        self.registry=json.loads((ROOT/"design/local-provider-capabilities.v1.json").read_text(encoding="utf-8"))
        self.providers={p["id"]:p for p in self.registry["source_adapters"]}

    def test_all_adapters_are_unverified_not_live(self):
        self.assertEqual(self.registry["schema_version"],"1.0")
        self.assertEqual(len(self.providers),len(self.registry["source_adapters"]))
        self.assertTrue(all(p["enabled_in_runtime"] is False for p in self.providers.values()))
        self.assertTrue(all(p["credentials_in_repo"] is False for p in self.providers.values()))

    def test_okx_read_skill_source_is_commit_pinned(self):
        okx=self.providers["okx_dex_market"]
        self.assertEqual(len(okx["source_commit"]),40)
        self.assertIn("explicit_install_approval",okx["requirements"])
        self.assertIn("payments",okx["prohibited_methods"])

    def test_okx_wallet_permissions_held_back(self):
        wallet=self.providers["okx_agentic_wallet"]
        self.assertEqual(wallet["phase"],"prohibited_in_phase_1")
        self.assertEqual(wallet["capabilities"],[])
        self.assertIn("swap",wallet["prohibited_methods"])


if __name__=="__main__":
    unittest.main()
