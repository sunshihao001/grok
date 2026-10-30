"""Checks project-internal specialist knowledge packaging, not market truth."""
import re
import unittest
from pathlib import Path

from solana_meme_os.knowledge_system import read

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = ROOT / "knowledge" / "domain"
FILES = [
    "L1-L2-chain-market.md",
    "L3-wallet-actors.md",
    "L4-L5-copytrade-edge.md",
    "L6-L7-investigation-cases.md",
]


class DomainKnowledgeTests(unittest.TestCase):
    def test_existing_twelve_domains_all_have_nonempty_real_content(self):
        domain_ids = {d["id"] for d in read("ontology.v1.json")["domains"]}
        observed = []
        for name in FILES:
            document = (DOMAIN / name).read_text(encoding="utf-8")
            self.assertGreater(len(document), 1500)
            headings = re.findall(r"^## (D\d\d)\s*[｜|]", document, flags=re.MULTILINE)
            observed.extend(headings)
            self.assertGreaterEqual(document.count("### D"), 2)
            self.assertIn("不是", document)
        self.assertEqual(set(observed), domain_ids)
        self.assertEqual(len(observed), 12)

    def test_index_and_skill_refer_to_real_files_without_bulk_loading(self):
        index = (DOMAIN / "README.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills/solana-meme-knowledge/SKILL.md").read_text(encoding="utf-8")
        for name in FILES:
            self.assertIn(name, index)
            self.assertIn(name, skill)
            self.assertTrue((DOMAIN / name).is_file())
        self.assertIn("按问题取用", index)
        self.assertIn("not indiscriminately load", skill)

    def test_copytrade_note_does_not_claim_proven_profit_or_live_source(self):
        content = (DOMAIN / "L4-L5-copytrade-edge.md").read_text(encoding="utf-8")
        self.assertIn("T_provider_receive", content)
        self.assertIn("follower_asof_net_result", content)
        self.assertIn("EXIT_ROUTE_UNAVAILABLE", content)
        self.assertIn("不是已成立的策略", content)
        self.assertIn("只读与纸面回放", content)


if __name__ == "__main__":
    unittest.main()
