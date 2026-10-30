"""Deterministic specialist briefing, NOT an LLM or a Grok Bot orchestrator.

The registry describes how to investigate Solana Meme problems. Selecting a
specialist never verifies evidence or invokes a deployed agent.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .knowledge_system import ROOT, read as read_system, route_domains

REGISTRY = ROOT / "knowledge/experts/registry.v1.json"
ROSTER = ROOT / "design/bot-roster.v1.json"
CATALOG = ROOT / "knowledge/catalog.v1.json"
REVIEW_IDS = {"E-L6-01", "E-L6-02"}
NO_AUTO_ID = "E-L7-02"
VALID_OBJECTIVES = {"EXPLAIN", "PREDICT", "ECONOMIC", "MONITOR_RELEASE"}


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_registry(registry: dict[str, Any] | None = None) -> dict[str, Any]:
    data = registry if registry is not None else load_registry()
    ontology = read_system("ontology.v1.json")
    roster = json.loads(ROSTER.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    layers = {x["id"] for x in ontology["layers"]}
    domains = {x["id"] for x in ontology["domains"]}
    bots = {x["id"] for x in roster["bots"]}
    cards = {x["id"] for x in catalog["cards"]}
    specialists = data.get("specialists")
    if data.get("schema_version") != "1.0" or data.get("expert_is_not_bot") is not True:
        raise ValueError("invalid or unsafe expert contract")
    if not isinstance(specialists, list) or not specialists:
        raise ValueError("no specialists")
    by_id = {}
    for x in specialists:
        sid = x.get("id")
        if not isinstance(sid, str) or sid in by_id or x.get("layer") not in layers:
            raise ValueError("invalid or duplicate specialist id")
        if (not x.get("domain_ids") or set(x["domain_ids"]) - domains or
                x.get("workflow_owner") not in bots or
                x.get("kind") != "internal_specialist_lens_not_installed_bot"):
            raise ValueError("invalid specialist mapping")
        if set(x.get("legacy_card_ids", [])) - cards or len(x.get("specialist_knowledge_primitives", [])) < 3:
            raise ValueError("expert knowledge is incomplete")
        if (len(x.get("reasoning_sequence", [])) < 3 or
                not x.get("competing_mechanisms") or
                not x.get("decisive_next_check") or
                not x.get("abstain_or_downgrade_when")):
            raise ValueError("expert reasoning evidence contract incomplete")
        for p in x.get("knowledge_files", []):
            loc = Path(p)
            if loc.is_absolute() or ".." in loc.parts or not (ROOT / loc).is_file():
                raise ValueError("invalid expert knowledge source")
        if x.get("authority") != "hypotheses_and_readonly_evidence_only":
            raise ValueError("specialist cannot self-authorize trading")
        by_id[sid] = x
    if {x["layer"] for x in specialists} != layers:
        raise ValueError("expert coverage does not span L0-L7")
    for x in specialists:
        if set(x.get("handoff_to_expert_ids", [])) - set(by_id):
            raise ValueError("unknown downstream specialist")
    if by_id[NO_AUTO_ID]["workflow_owner"] != "B07":
        raise ValueError("frozen monitor role mapping broken")
    return {"status": "STRUCTURALLY_VALID_NOT_DEPLOYED",
            "specialists": len(by_id), "layers": sorted(layers),
            "owners": sorted({x["workflow_owner"] for x in specialists}),
            "no_live_market_facts_verified": True,
            "no_grok_bots_provisioned": True}


def _brief(expert: dict[str, Any]) -> dict[str, Any]:
    fields = ("id", "name", "layer", "workflow_owner", "domain_ids",
              "specialist_knowledge_primitives", "cognitive_model",
              "reasoning_sequence", "competing_mechanisms",
              "decisive_next_check", "abstain_or_downgrade_when",
              "knowledge_files", "legacy_card_ids", "handoff_to_expert_ids")
    return {key: expert[key] for key in fields}


def expert_brief(expert_id: str) -> dict[str, Any]:
    audit_registry()
    expert = next((x for x in load_registry()["specialists"] if x["id"] == expert_id), None)
    if not expert:
        raise ValueError("unknown specialist")
    return {"status": "EXPERT_METHOD_NOT_MARKET_CONCLUSION",
            "is_deployed_bot": False, "specialist": _brief(expert),
            "source_admission_required": True,
            "no_alpha_or_monitor_approval": True}


def recommend_experts(question: str, objective: str = "EXPLAIN",
                      max_experts: int = 3) -> dict[str, Any]:
    if objective not in VALID_OBJECTIVES:
        raise ValueError("invalid research objective")
    if not 1 <= max_experts <= 5:
        raise ValueError("max experts must be 1..5")
    audit_registry()
    route = route_domains(question)
    specialists = load_registry()["specialists"]
    matches = set(route["matched_domains"])
    required = set(route["required_domains"])
    if not matches:
        return {"status": "SOURCE_DISCOVERY_REQUIRED",
                "question": question, "objective": objective,
                "specialists": [], "domain_route": route,
                "note": "No literal domain match; request source discovery, not an invented specialist verdict."}
    scored = []
    for expert in specialists:
        if expert["id"] == NO_AUTO_ID and objective != "MONITOR_RELEASE":
            continue
        x = set(expert["domain_ids"])
        score = 5 * len(x & matches) + len(x & required)
        if not score:
            continue
        if objective == "ECONOMIC" and "D09" in x:
            score += 8
        if objective == "PREDICT" and expert["id"] == "E-L1-02":
            score += 8
        if objective == "MONITOR_RELEASE" and expert["id"] == NO_AUTO_ID:
            score += 20
        if objective == "EXPLAIN" and "D11" in x and "D05" in matches:
            score += 6
        if expert["id"] == "E-L7-01":
            score -= 4
        scored.append((score, expert["id"], expert))
    scored.sort(key=lambda z: (-z[0], z[1]))
    picked = [x[2] for x in scored[:max_experts]]
    return {"status": "SPECIALISTS_SELECTED_FOR_RESEARCH_ONLY",
            "question": question, "objective": objective,
            "selection_method": "literal_domain_matches_and_objective_not_semantic_evaluation",
            "domain_route": route,
            "specialists": [_brief(x) for x in picked],
            "note": "Experts are procedural lenses, not running Grok agents. Consult source admission and obtain K2 raw evidence before any factual verdict.",
            "frozen_monitor_cannot_generate_new_rules": True}


def main() -> int:
    p = argparse.ArgumentParser(description="Offline expert knowledge briefing")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--audit", action="store_true")
    g.add_argument("--expert-id")
    g.add_argument("--question")
    p.add_argument("--objective", choices=sorted(VALID_OBJECTIVES), default="EXPLAIN")
    p.add_argument("--max-experts", type=int, default=3)
    a = p.parse_args()
    try:
        result = (audit_registry() if a.audit else expert_brief(a.expert_id)
                  if a.expert_id else recommend_experts(a.question, a.objective, a.max_experts))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
