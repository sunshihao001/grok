"""Research-only knowledge/expert panel router for Solana Meme events.

A routing suggestion is not a market analysis, anomalous activity detection,
confirmed entity identity or trade permission. The listed specialists are
knowledge disciplines; no Grok cloud Bots are instantiated by this module.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP = ROOT / "knowledge" / "expert-capability-map.v1.json"


def load_map(path: Path = DEFAULT_MAP) -> dict:
    with path.open(encoding="utf-8") as stream:
        mapping = json.load(stream)
    if mapping.get("schema_version") != "1.0":
        raise ValueError("unsupported expert map schema")
    ids = [r["id"] for r in mapping.get("experts", [])]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError("invalid expert role IDs")
    available = set(ids)
    for entry in mapping.get("scenarios", []):
        required = [entry["lead"], *entry["panel"], *entry["conditional"], *entry["vetoReview"]]
        if not set(required) <= available:
            raise ValueError("scenario refers to unknown expert role")
    return mapping


def route(event_types: list[str], *, question: str = "",
          mapping: dict | None = None) -> dict:
    """Match known event types and preserve an open discovery path.

    This method intentionally does not choose a causal mechanism. It returns
    knowledge to consult, hypotheses to challenge, and explicit data needs.
    """
    mapping = mapping if mapping is not None else load_map()
    if any(not isinstance(s, str) or not s.strip() for s in event_types):
        raise ValueError("event_types must be non-empty strings")
    names = set(event_types)
    matched = []
    for entry in mapping["scenarios"]:
        actual = names & set(entry["triggers"])
        if actual:
            matched.append((len(actual), entry))
    matched.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    lookup = {r["id"]: r for r in mapping["experts"]}
    if matched:
        # A true simultaneous event can use multiple panels, not only the
        # highest-scoring keyword match.
        scenarios = [entry for _, entry in matched]
        lead = scenarios[0]["lead"]
        full = []
        for item in scenarios:
            # The lead of every matched scenario must participate, not only
            # the first; otherwise a second independent evidence domain is lost.
            full.append(item["lead"])
            full.extend(item["panel"])
        primary = list(dict.fromkeys(full))
        challenger = list(dict.fromkeys(
            role for s in scenarios for role in s["vetoReview"] if role not in primary))
        conditional = list(dict.fromkeys(
            role for s in scenarios for role in s["conditional"]
            if role not in primary and role not in challenger))
        mode = "MATCHED_RESEARCH_PANELS"
    else:
        scenarios = []
        primary = ["chief", "data", "review"]
        challenger = []
        conditional = list(dict.fromkeys(
            role for role in lookup if role not in primary))
        mode = "OPEN_DISCOVERY_REQUIRED"
    selected = list(dict.fromkeys([*primary, *challenger]))
    source_cards = sorted({card for role in selected for card in lookup[role]["source_cards"]})
    source_ids = sorted({s for role in selected for s in lookup[role]["source_ids"]})
    data_requirements = sorted({field for role in selected for field in lookup[role]["requires"]})
    challenges = [dict(role_id=role, challenge=lookup[role]["challenge"]) for role in selected]
    # Contract suggestions come from a separate typed knowledge dependency graph.
    # No expert is actually executed, and no LLM conclusion is inferred.
    from .expert_interaction import handoffs_for_roles, load_graph
    handoffs = handoffs_for_roles(
        load_graph(expert_map=mapping), active=selected, conditional=conditional)
    return {
        "status": mode,
        "question": question,
        "input_event_types": sorted(names),
        "matched_scenarios": [s["id"] for s in scenarios],
        "lead_expert": primary[0],
        "primary_experts": primary,
        "independent_challengers": challenger,
        "conditional_experts": conditional,
        "source_card_ids_to_read": source_cards,
        "source_index_ids_to_read": source_ids,
        "data_fields_to_check": data_requirements,
        "hypothesis_challenges": challenges,
        "typed_expert_handoffs": handoffs,
        "scenario_research_questions": list(dict.fromkeys(
            q for item in scenarios for q in item["questions"])),
        "expected_research_outputs": list(dict.fromkeys(
            r for item in scenarios for r in item["outputs"])),
        "cannot_conclude": ["not market-wide coverage",
                           "not calibrated abnormality",
                           "not confirmed beneficial ownership",
                           "not verified Jito bundle",
                           "not an executable trade or net alpha",
                           "not proof that any Grok Bot is deployed"],
        "no_trading": True,
        "new_mechanisms_allowed": True,
        "human_research_review_required": True,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Select research knowledge specialists, not market conclusions")
    p.add_argument("--event", action="append", required=True, help="Event type; repeatable")
    p.add_argument("--question", default="", help="Original user/market research question")
    p.add_argument("--map", type=Path, default=DEFAULT_MAP)
    args = p.parse_args()
    print(json.dumps(route(args.event, question=args.question, mapping=load_map(args.map)),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
