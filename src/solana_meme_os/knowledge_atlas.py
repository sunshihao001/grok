"""Local, deterministic retrieval of the 12-domain knowledge atlas.

It does NOT load an AI expert, run a network call, or verify market facts.
The existing ontology and expert registry remain authoritative.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ATLAS = ROOT / "knowledge" / "atlas" / "registry.v1.json"


def load_atlas() -> dict[str, Any]:
    return json.loads(ATLAS.read_text(encoding="utf-8"))


def atlas_audit() -> dict[str, Any]:
    data = load_atlas()
    ontology = json.loads((ROOT / data["ontology"]).read_text(encoding="utf-8"))
    experts = json.loads((ROOT / data["expert_registry"]).read_text(encoding="utf-8"))
    profiles = json.loads((ROOT / data["bot_competencies"]).read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "knowledge/catalog.v1.json").read_text(encoding="utf-8"))
    by_domain = {d["id"]: d for d in ontology["domains"]}
    by_expert = {e["id"]: e for e in experts["specialists"]}
    by_bot = {p["id"]: p for p in profiles["profiles"]}
    prior = {u["id"] for p in profiles["profiles"] for u in p["resident_knowledge"]}
    cards = {c["id"] for c in catalog["cards"]}
    domains = data["domains"]
    units = data["units"]
    if data["preserves_existing_ontology"] is not True:
        raise ValueError("atlas must not replace existing ontology")
    if len(by_domain) != 12 or len(domains) != 12 or set(d["id"] for d in domains) != set(by_domain):
        raise ValueError("12 domain mapping broken")
    if len(by_expert) != 21 or len(by_bot) != 7 or len(prior) != 52 or len(cards) != 15:
        raise ValueError("baseline expert, Bot, competence or card count changed")
    if len(units) != 96 or len({u["id"] for u in units}) != 96:
        raise ValueError("expected 96 distinct knowledge units")
    if not (ROOT / data["knowledge_layer_L0_document"]).is_file():
        raise ValueError("missing L0 horizontal governance")
    by_unit = {u["id"]: u for u in units}
    all_linked_competencies = set()
    all_legacy_cards = set()
    for d in domains:
        if d["layer"] != by_domain[d["id"]]["layer"]:
            raise ValueError("domain layer shifted")
        if d["existing_ontology_coverage"] != by_domain[d["id"]]["coverage"]:
            raise ValueError("cannot silently upgrade ontology coverage")
        if len(d["units"]) != 8 or d["unit_count"] != 8:
            raise ValueError("expected eight atomized topics per domain")
        if not (ROOT / d["atlas_document"]).is_file():
            raise ValueError("missing domain dossier")
        if set(d["lead_expert_ids"]) - set(by_expert):
            raise ValueError("unknown expert")
        if set(d["workflow_owners"]) - set(by_bot):
            raise ValueError("unknown workflow owner")
        if set(d["prior_competency_ids"]) - prior:
            raise ValueError("unknown prior competence")
        if set(d["existing_legacy_card_ids"]) != set(by_domain[d["id"]]["primary_card_ids"]):
            raise ValueError("old knowledge cards lost")
        all_linked_competencies.update(d["prior_competency_ids"])
        all_legacy_cards.update(d["existing_legacy_card_ids"])
        for uid in d["units"]:
            u = by_unit.get(uid)
            if (not u or u["domain_id"] != d["id"] or u["layer"] != d["layer"]
                    or u["state"] != "mechanism_drafted_unverified_market"):
                raise ValueError("inconsistent unit mapping or invalid evidence state")
            if (len(u["mechanism"]) < 32 or len(u["invalid_inference"]) < 15
                    or u["document"] != d["atlas_document"]):
                raise ValueError("unit is shallow or points to a different document")
    if all_linked_competencies != prior or all_legacy_cards != cards:
        raise ValueError("52 prior competences or 15 old cards not covered")
    if set(x["id"] for x in units) != set(uid for d in domains for uid in d["units"]):
        raise ValueError("unit missing from domain index")
    return {
        "status": "STRUCTURALLY_COVERED_MECHANISMS_UNVERIFIED",
        "layers": len(ontology["layers"]), "domains": len(domains),
        "domain_units": len(units), "L0_governance_units": 8,
        "specialists_referenced": len(by_expert), "bot_owners": len(by_bot),
        "legacy_competences_referenced": len(prior),
        "legacy_cards_referenced": len(cards),
        "market_alpha_verified": False, "grok_bots_provisioned": False,
    }


def select(*, domain: str | None = None, expert: str | None = None,
           unit: str | None = None, limit: int = 8) -> dict[str, Any]:
    data = load_atlas()
    if limit < 1 or limit > 96:
        raise ValueError("limit out of range")
    if domain and domain not in {x["id"] for x in data["domains"]}:
        raise ValueError("unknown domain")
    specialists = json.loads((ROOT / data["expert_registry"]).read_text(encoding="utf-8"))
    if expert and expert not in {x["id"] for x in specialists["specialists"]}:
        raise ValueError("unknown expert")
    if unit and unit not in {x["id"] for x in data["units"]}:
        raise ValueError("unknown unit")
    domain_scope = {domain} if domain else None
    if expert:
        matching = next(e for e in specialists["specialists"] if e["id"] == expert)
        domain_scope = set(matching["domain_ids"])
        if domain:
            domain_scope &= {domain}
    hits = [x for x in data["units"]
            if (domain_scope is None or x["domain_id"] in domain_scope)
            and (unit is None or x["id"] == unit)]
    return {"status": "RESEARCH_KNOWLEDGE_NOT_MARKET_EVIDENCE",
            "total_matches": len(hits), "units": hits[:limit],
            "not_authorized_to_trade": True}


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline knowledge atlas, no market claims")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--domain")
    parser.add_argument("--expert")
    parser.add_argument("--unit")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    result = atlas_audit() if args.audit else select(
        domain=args.domain, expert=args.expert, unit=args.unit, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
