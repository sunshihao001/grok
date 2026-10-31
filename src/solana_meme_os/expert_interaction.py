"""Typed, reversible expert-to-expert evidence contracts (research only).

This is a deterministic checker/planner. It does not run LLM agents, ingest RPC,
update persistent claim stores, prove a market claim or authorize trading.
"""
from __future__ import annotations

from collections import defaultdict, deque
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "knowledge" / "expert-interaction-graph.v1.json"


def load_graph(path: Path = GRAPH, expert_map: dict | None = None) -> dict:
    with path.open(encoding="utf-8") as stream:
        graph = json.load(stream)
    if graph.get("schema_version") != "1.0":
        raise ValueError("unsupported expert interaction graph schema")
    if expert_map is None:
        from .expert_router import load_map
        expert_map = load_map()
    experts = {x["id"] for x in expert_map["experts"]}
    links = graph.get("links")
    if not isinstance(links, list) or not links:
        raise ValueError("empty expert interaction graph")
    ids = set()
    connected = set()
    for link in links:
        if not isinstance(link, dict):
            raise ValueError("invalid expert interaction link")
        if link.get("id") in ids:
            raise ValueError("duplicate expert interaction link")
        ids.add(link["id"])
        if link.get("from") not in experts or link.get("to") not in experts:
            raise ValueError("unknown expert in interaction graph")
        if not all(isinstance(link.get(k), str) and link[k].strip()
                   for k in ("link_type", "artifact", "contract", "counter_signal", "on_counter_signal")):
            raise ValueError("expert interaction missing typed evidence contract")
        connected.update((link["from"], link["to"]))
    if connected != experts:
        raise ValueError("at least one knowledge expert is disconnected")
    return graph


def handoffs_for_roles(graph: dict, *, active: list[str],
                       conditional: list[str] | None = None) -> dict:
    """A dependency blueprint, not causal truth or automated task execution."""
    act = set(active)
    candidates = set(conditional or [])
    out = []
    proposals = []
    for link in graph["links"]:
        edge = {k: link[k] for k in
                ("id", "from", "to", "link_type", "artifact", "contract",
                 "counter_signal", "on_counter_signal")}
        if link["from"] in act and link["to"] in act:
            out.append(edge)
        elif link["from"] in act and link["to"] in candidates:
            proposals.append(edge)
    return {"active_handoffs": out, "conditional_handoff_proposals": proposals,
            "execution_status": "CONTRACTS_ONLY_NOT_DISPATCHED"}


def impacted_by_retraction(claims: list[dict], retracted_claim_id: str) -> dict:
    """Plan transitive challenge propagation without altering original claims.

    A dependent may have corroborating independent evidence. Flag it as
    CONTESTED_RECOMPUTE, not automatically false or financially actionable.
    """
    by_id = {}
    reverse: dict[str, set[str]] = defaultdict(set)
    for c in claims:
        cid = c.get("claim_id")
        if not isinstance(cid, str) or not cid or cid in by_id:
            raise ValueError("each claim requires a unique claim_id")
        by_id[cid] = c
    if retracted_claim_id not in by_id:
        raise ValueError("retraction references unknown claim")
    for cid, claim in by_id.items():
        deps = claim.get("depends_on_claim_ids")
        if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps):
            raise ValueError("depends_on_claim_ids must be string list")
        if cid in deps:
            raise ValueError("claim cannot depend on itself")
        if not set(deps) <= set(by_id):
            raise ValueError("unknown claim dependency; preserve unresolved input")
        for dep in deps:
            reverse[dep].add(cid)
    # A published claim version must be acyclic even when the real economic
    # graph includes repeated transfers and cyclic money flows.
    visited, in_stack = set(), set()
    def inspect(cid: str) -> None:
        if cid in in_stack:
            raise ValueError("cyclic epistemic dependency")
        if cid in visited:
            return
        in_stack.add(cid)
        for dependency in by_id[cid]["depends_on_claim_ids"]:
            inspect(dependency)
        in_stack.remove(cid)
        visited.add(cid)
    for cid in by_id:
        inspect(cid)
    affected, seen = [], {retracted_claim_id}
    queue = deque([retracted_claim_id])
    while queue:
        parent = queue.popleft()
        for child in sorted(reverse[parent]):
            if child not in seen:
                seen.add(child)
                affected.append({"claim_id": child, "status": "CONTESTED_RECOMPUTE",
                                 "reason": f"depends (directly or transitively) on {retracted_claim_id}"})
                queue.append(child)
    return {"target": retracted_claim_id, "target_new_status": "RETRACTED",
            "affected": affected, "original_claims_mutated": False,
            "trading_or_probability_conclusion": False}
