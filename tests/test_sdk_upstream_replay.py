"""Optional SDK not imported for core regression tests; Action tests SDK corpus."""
import unittest
from solana_meme_os.sdk_upstream_replay import account_views

A="11111111111111111111111111111111"
B="So11111111111111111111111111111111111111112"
C="SysvarRent111111111111111111111111111111111"
M="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"

def fixture():
    tx={"message":{"accountKeys":[A,B]},"signatures":["signed-fixture"]}
    row=lambda amount, owner=A: {"accountIndex":1, "mint":M, "programId":M,
                                 "owner":owner,"uiTokenAmount":{"amount":amount}}
    meta={"loadedAddresses":{"writable":[],"readonly":[]},"preBalances":[10,20],
          "postBalances":[5,25],"preTokenBalances":[row("100")],
          "postTokenBalances":[row("75")]}
    return meta, tx

class RouteBalanceTests(unittest.TestCase):
    def test_account_observation_and_no_controller_inference(self):
        m,t=fixture()
        x=account_views(m,t)
        self.assertEqual(x["resolved_accounts"],2)
        self.assertEqual(len(x["sol_delta_accounts"]),2)
        self.assertEqual(x["token_accounts"][0]["delta_raw"],-25)
        self.assertFalse(x["token_accounts"][0]["economic_owner_proven"])
        self.assertFalse(x["all_wallet_economic_roles_proven"])

    def test_missing_side_never_implies_zero(self):
        m,t=fixture()
        m["postTokenBalances"]=[]
        x=account_views(m,t)["token_accounts"][0]
        self.assertEqual(x["status"],"MISSING_SIDE")
        self.assertIsNone(x["delta_raw"])

    def test_owner_hint_conflict_does_not_fake_transfer(self):
        m,t=fixture()
        m["postTokenBalances"][0]["owner"]=B
        x=account_views(m,t)["token_accounts"][0]
        self.assertEqual(x["status"],"OWNER_HINT_CONFLICT")
        self.assertIsNone(x["delta_raw"])

    def test_alt_accounts_preserved_not_merged(self):
        m,t=fixture()
        m["loadedAddresses"]["writable"]=[C]
        m["preBalances"].append(0)
        m["postBalances"].append(0)
        self.assertEqual(account_views(m,t)["resolved_accounts"],3)

    def test_unsupported_float_and_mismatched_accounts_rejected(self):
        m,t=fixture()
        m["postTokenBalances"][0]["uiTokenAmount"]["amount"]=1.0
        with self.assertRaisesRegex(ValueError,"raw integer string"):
            account_views(m,t)
        m,t=fixture()
        m["postBalances"].pop()
        with self.assertRaisesRegex(ValueError,"account or SOL balance mismatch"):
            account_views(m,t)

if __name__=="__main__":
    unittest.main()
