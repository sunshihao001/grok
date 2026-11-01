from pathlib import Path
import unittest
from unittest.mock import patch
from solana_meme_os import mint_v01

MINT="DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263"

class TestMintV01(unittest.TestCase):
    def test_one_mint_routes_public_without_wallet_or_keys(self):
        with patch('solana_meme_os.mint_v01.public_pair_report.main',return_value=2) as fn:
            self.assertEqual(mint_v01.main([MINT]),2)
            self.assertEqual(fn.call_args.args[0][0:2],["--mint", MINT])
    def test_saved_okx_routes_to_mature_adapter(self):
        with patch('solana_meme_os.mint_v01.mint_report.main',return_value=0) as fn:
            self.assertEqual(mint_v01.main([MINT,'--okx-json','okx.json','--out-dir','out']),0)
            self.assertIn('--okx-json',fn.call_args.args[0])
            self.assertEqual(fn.call_args.args[0][-1],'out')
    def test_fixture_flag_requires_saved_json(self):
        with self.assertRaises(SystemExit): mint_v01.main([MINT, '--fixture'])
    def test_fixture_flag_passed_through(self):
        with patch('solana_meme_os.mint_v01.mint_report.main',return_value=0) as fn:
            mint_v01.main([MINT,'--okx-json','okx.json','--fixture'])
            self.assertIn('--fixture',fn.call_args.args[0])

if __name__ == '__main__': unittest.main()