"""Typed handoff graph and retraction planning; all claims in tests are SYNTHETIC."""
from __future__ import annotations
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from solana_meme_os.expert_router import load_map, route
from solana_meme_os.expert_interaction import (
    load_graph, handoffs_for_roles, impacted_by_retraction
)


def chain():
    return [
        {"claim_id": "raw:tx", "depends_on_claim_ids": []},
        {"claim_id": "event:buy", "depends_on_claim_ids": ["raw:tx"]},
        {"claim_id": "window:burst", "depends_on_claim_ids": ["event:buy"]},
        {"claim_id": "hypothesis:coord", "depends_on_claim_ids": ["window:burst"]},
        {"claim_id": "risk:warning", "depends_on_claim_ids": ["hypothesis:coord"]},
        {"claim_id": "paper:outcome", "depends_on_claim_ids": ["hypothesis:coord"]},
        {"claim_id": "independent:fact", "depends_on_claim_ids": []}
    ]


class ExpertInteractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping = load_map()
        cls.graph = load_graph(expert_map=cls.mapping)

    def test_every_domain_expert_connected_and_links_typed(self):
        self.assertEqual(len(self.graph["links"]), 40)
        ids = {r["id"] for r in self.mapping["experts"]}
        linked = {x["from"] for x in self.graph["links"]} | {
            x["to"] for x in self.graph["links"]}
        self.assertEqual(ids, linked)
        self.assertEqual(len({x["id"] for x in self.graph["links"]}), 40)

    def test_route_includes_active_and_optional_typed_handoffs(self):
        r = route(["FUNDING_FANOUT", "SAME_SLOT_MULTIWALLET_BUY"],
                  mapping=self.mapping)
        self.assertEqual(r["typed_expert_handoffs"]["execution_status"],
                         "CONTRACTS_ONLY_NOT_DISPATCHED")
        links = r["typed_expert_handoffs"]["active_handoffs"]
        self.assertTrue(any(l["from"] == "chain" and l["to"] == "event" for l in links))
        self.assertTrue(any(l["from"] == "event" and l["to"] == "graph" for l in links))
        self.assertTrue(all(l["contract"] and l["counter_signal"] for l in links))
        self.assertTrue(r["no_trading"])

    def test_independent_role_not_forcibly_copied(self):
        x = handoffs_for_roles(self.graph, active=["data", "chain"],
                               conditional=["event", "statistics"])
        self.assertTrue(any(e["from"] == "data" and e["to"] == "chain"
                            for e in x["active_handoffs"]))
        self.assertTrue(any(e["from"] == "chain" and e["to"] == "event"
                            for e in x["conditional_handoff_proposals"]))
        self.assertFalse(any(e["to"] == "statistics" for e in x["active_handoffs"]))

    def test_transitive_retraction_marks_dependents_not_independent(self):
        out = impacted_by_retraction(chain(), "raw:tx")
        self.assertEqual(out["target_new_status"], "RETRACTED")
        self.assertEqual({r["claim_id"] for r in out["affected"]},
                         {"event:buy", "window:burst", "hypothesis:coord",
                          "risk:warning", "paper:outcome"})
        self.assertNotIn("independent:fact", {r["claim_id"] for r in out["affected"]})
        self.assertTrue(all(x["status"] == "CONTESTED_RECOMPUTE"
                            for x in out["affected"]))
        self.assertFalse(out["original_claims_mutated"])

    def test_retract_leaf_no_cascade(self):
        self.assertEqual(impacted_by_retraction(chain(), "paper:outcome")["affected"], [])

    def test_unknown_dependency_is_not_silent(self):
        claims = chain()
        claims[0]["depends_on_claim_ids"] = ["unseen:external"]
        with self.assertRaisesRegex(ValueError, "unknown claim dependency"):
            impacted_by_retraction(claims, "raw:tx")

    def test_cyclic_epistemic_proof_is_forbidden(self):
        claims = chain()
        claims[0]["depends_on_claim_ids"] = ["paper:outcome"]
        with self.assertRaisesRegex(ValueError, "cyclic epistemic dependency"):
            impacted_by_retraction(claims, "raw:tx")

    def test_invalid_graph_role_or_edge_fails_fast(self):
        malformed = copy.deepcopy(self.graph)
        malformed["links"][0]["to"] = "imaginary-bot"
        with TemporaryDirectory() as d:
            path = Path(d) / "graph.json"
            path.write_text(json.dumps(malformed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown expert"):
                load_graph(path, expert_map=self.mapping)
            malformed = copy.deepcopy(self.graph)
            malformed["links"][0]["contract"] = ""
            path.write_text(json.dumps(malformed), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "typed evidence contract"):
                load_graph(path, expert_map=self.mapping)


if __name__ == "__main__":
    unittest.main()
