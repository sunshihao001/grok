"""Role-aware K0/K1 syllabus routing and offline handoff contract validation.

This module CANNOT read live Solana data, configure Grok Bots, or prove an edge.
Use it to prevent accidental knowledge drift, false promotion, and broken handoffs.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import quote

from .knowledge_system import ROOT, filter_plan, route_domains

PROFILES = ROOT / "knowledge/bot-knowledge-profiles.v1.json"
SOURCE_INDEX = ROOT / "knowledge/source_index.v1.json"
HANDOFF_SCHEMA = ROOT / "knowledge/bot-handoff.schema.json"
DOMAIN_MAP = ROOT / "knowledge/system/ontology.v1.json"
CATALOG = ROOT / "knowledge/catalog.v1.json"
ROSTER = ROOT / "design/bot-roster.v1.json"
POLICY = ROOT / "knowledge/system/filter-policy.v1.json"

PACKET_OWNER = {
    "research_brief": "B01",
    "evidence_observation": "B02",
    "structural_hypothesis": "B03",
    "strategy_candidate": "B04",
    "adversarial_review": "B05",
    "qa_report": "B06",
    "monitor_observation": "B07",
}

def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def _utc(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp missing")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("timestamp requires explicit timezone")
    return dt.astimezone(timezone.utc)

def validate_profiles(program: dict[str, Any] | None = None,
                      index: dict[str, Any] | None = None) -> dict[str, Any]:
    program = program if program is not None else _json(PROFILES)
    index = index if index is not None else _json(SOURCE_INDEX)
    o, catalog, roster, gate = (_json(x) for x in (DOMAIN_MAP, CATALOG, ROSTER, POLICY))
    if program.get("schema_version") != "1.0" or index.get("schema_version") != "1.0":
        raise ValueError("invalid role or source index version")
    roles = {r["id"]: r for r in roster["bots"]}
    domains = {d["id"] for d in o["domains"]}
    cards = {c["id"] for c in catalog["cards"]}
    gates = {g["id"] for g in gate["gates"]}
    sources = {s["id"]: s for s in index["items"]}
    if len(sources) != len(index["items"]) or not sources:
        raise ValueError("duplicate or missing K1 source")
    profiles = program.get("profiles", [])
    if {p["id"] for p in profiles} != set(roles) or len(profiles) != len(roles):
        raise ValueError("role profiles must exactly match B01-B07 roster")
    all_ids = set(roles)
    needed_keys = {"id", "title", "status", "phase", "primary_domains", "gate_responsibility",
                   "resident_knowledge", "legacy_card_ids", "read_on_demand_source_ids",
                   "minimum_knowledge_files", "k2_required_fields", "consumes_from", "produces_for",
                   "skills_to_configure", "start_condition", "stop_condition", "permitted_actions",
                   "prohibited_actions", "success_criterion"}
    knowledge_count = 0
    for p in profiles:
        if needed_keys - set(p):
            raise ValueError(f"missing required role fields: {p.get('id')}")
        r = roles[p["id"]]
        if p["status"] != "planned_not_provisioned" or p["phase"] != r["phase"]:
            raise ValueError("role falsely asserts provisioning or changes phase")
        if p["primary_domains"] != r["domain_ids"] or p["gate_responsibility"] != r["gate_ids"]:
            raise ValueError("role/domain/gate ownership drift")
        for key, allowed in (("primary_domains", domains), ("gate_responsibility", gates),
                             ("legacy_card_ids", cards), ("read_on_demand_source_ids", set(sources))):
            values = p[key]
            if not isinstance(values, list) or len(values) != len(set(values)) or set(values) - allowed:
                raise ValueError(f"invalid {key}: {p['id']}")
        if not p["read_on_demand_source_ids"] or not p["resident_knowledge"]:
            raise ValueError("Bot without concrete K0/K1 knowledge reserve")
        for path in p["minimum_knowledge_files"]:
            if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts or not (ROOT / path).is_file():
                raise ValueError("missing/unsafe K0 source file")
        ids = set()
        for unit in p["resident_knowledge"]:
            if unit.get("id") in ids or not unit.get("id", "").startswith(p["id"] + "-K"):
                raise ValueError("duplicate or wrong role knowledge unit ID")
            if unit.get("domain_id") not in domains or any(not unit.get(k) for k in ("title", "method", "do_not_infer")):
                raise ValueError("incomplete K0 unit or invalid domain")
            if unit.get("epistemic_state") != "curriculum_target_not_empirically_validated":
                raise ValueError("unverified syllabus incorrectly promoted as market truth")
            ids.add(unit["id"])
            knowledge_count += 1
        for k in ("consumes_from", "produces_for"):
            if not isinstance(p[k], list):
                raise ValueError("Bot connections must be listed")
            for other in p[k]:
                if other not in all_ids and other != "human_approved_frozen_rules":
                    raise ValueError("unknown Bot handoff endpoint")
                if other == p["id"]:
                    raise ValueError("Bot cannot self-review via handoff")
        if p["id"] != "B07" and "B07" in p["produces_for"]:
            raise ValueError("development Bot may not publish directly into Monitor")
        if "real_trade" not in p["prohibited_actions"] or "self_approve_rule" not in p["prohibited_actions"]:
            raise ValueError("Bot is missing core safety boundaries")
        if not p["k2_required_fields"] or not p["stop_condition"] or not p["success_criterion"]:
            raise ValueError("missing K2/gap/success contract")
    return {
        "structure": "VALID",
        "verification": "STATIC_REFERENCES_ONLY_NOT_CLOUD_BOT_OR_MARKET_VALIDATION",
        "profiles": len(profiles),
        "resident_curriculum_topics": knowledge_count,
        "selective_k1_source_pointers": len(sources),
        "real_market_data_verified": False,
        "cloud_bots_provisioned": False,
    }


def build_role_brief(bot_id: str, question: str, limit: int = 4) -> dict[str, Any]:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question required")
    if not 1 <= limit <= 5:
        raise ValueError("max sources per first look must be 1..5")
    prog, idx = _json(PROFILES), _json(SOURCE_INDEX)
    profile = next((p for p in prog["profiles"] if p["id"] == bot_id), None)
    if not profile:
        raise ValueError("unknown Bot")
    entries = {s["id"]: s for s in idx["items"]}
    query = question.casefold()
    relevant = []
    for source_id in profile["read_on_demand_source_ids"]:
        s = entries[source_id]
        hits = [k for k in s["topics"] if k.casefold() in query]
        if hits:
            relevant.append((len(hits), source_id, s, hits))
    relevant.sort(key=lambda t: (-t[0], t[1]))
    chosen = relevant[:limit]
    return {
        "bot_id": bot_id,
        "role": profile["title"],
        "role_status": profile["status"],
        "question": question,
        "method": "literal_source_cues_not_semantic_retrieval_or_proof",
        "domain_route": route_domains(question),
        "knowledge_requirements": [
            {"id": t["id"], "domain_id": t["domain_id"], "title": t["title"],
             "boundary": t["do_not_infer"]} for t in profile["resident_knowledge"]
        ],
        "historical_card_ids": profile["legacy_card_ids"],
        "source_match_state": "MATCHED_CANDIDATES" if chosen else "SOURCE_DISCOVERY_REQUIRED",
        "on_demand_source_candidates": [
            {"source_id": source_id, "repository": s["repository"], "commit": s["commit"],
             "path": s["path"], "matched_topics": hits,
             "url": f"https://github.com/{s['repository']}/blob/{s['commit']}/" +
                    "/".join(quote(segment, safe="") for segment in s["path"].split("/")),
             "source_is_not_market_evidence": True} for _, source_id, s, hits in chosen
        ],
        "k2_required_fields": profile["k2_required_fields"],
        "can_claim_source_observed": False,
        "filter_plan": filter_plan(),
        "next_action": "Read only matched primary sources, obtain as-of raw data, and hand off an auditable packet."
    }


def validate_handoff(packet: dict[str, Any]) -> dict[str, Any]:
    """Reject structurally dangerous handoffs; independent fact verification is still required."""
    schema, program, index = _json(HANDOFF_SCHEMA), _json(PROFILES), _json(SOURCE_INDEX)
    required = set(schema["required"])
    if not isinstance(packet, dict) or required - set(packet) or set(packet) - set(schema["properties"]):
        raise ValueError("handoff missing required or contains unsupported fields")
    if packet["schema_version"] != "1.0" or packet["mode"] not in ("fixture", "research_only", "real_observation"):
        raise ValueError("unsupported handoff version/mode")
    bots = {p["id"]: p for p in program["profiles"]}
    producer, typ = packet["producer_bot_id"], packet["packet_type"]
    if producer not in bots or (typ in PACKET_OWNER and producer != PACKET_OWNER[typ]):
        raise ValueError("wrong Bot is producing this packet")
    if typ not in set(PACKET_OWNER) | {"research_gap"}:
        raise ValueError("unknown packet type")
    if producer == "B07" and typ not in {"monitor_observation", "research_gap"}:
        raise ValueError("Monitor cannot author research rules")
    recipients = packet["recipient_bot_ids"]
    if not isinstance(recipients, list) or len(recipients) != len(set(recipients)) or (
        set(recipients) - set(bots)
    ) or producer in recipients:
        raise ValueError("bad handoff recipients")
    _utc(packet["created_at_utc"])
    cutoff = _utc(packet["decision_cutoff_utc"])
    for key in ("task_id", "packet_id", "objective", "population", "next_action"):
        if not isinstance(packet[key], str) or not packet[key].strip():
            raise ValueError(f"missing packet field {key}")
    if packet["objective"] not in {"EXPLAIN", "PREDICT", "ECONOMIC", "MONITOR_RELEASE"}:
        raise ValueError("unknown research objective")
    known_domains = {d["id"] for d in _json(DOMAIN_MAP)["domains"]}
    known_cards = {c["id"] for c in _json(CATALOG)["cards"]}
    if not packet["domain_ids"] or set(packet["domain_ids"]) - known_domains or len(packet["domain_ids"]) != len(set(packet["domain_ids"])):
        raise ValueError("invalid packet domains")
    if len(packet["knowledge_ids"]) != len(set(packet["knowledge_ids"])):
        raise ValueError("duplicate knowledge refs")
    if set(packet["knowledge_ids"]) - (known_cards | {v["id"] for p in program["profiles"] for v in p["resident_knowledge"]}):
        raise ValueError("unknown knowledge reference")
    source_index = {s["id"]: s for s in index["items"]}
    source_ids = set()
    for ref in packet["source_refs"]:
        if not isinstance(ref, dict) or not ref.get("ref_id") or ref["ref_id"] in source_ids:
            raise ValueError("bad or duplicate source ref")
        if ref.get("kind") == "pinned_document":
            entry = source_index.get(ref["ref_id"])
            if not entry or any(ref.get(k) != entry[k] for k in ("repository", "commit", "path")):
                raise ValueError("pinned source reference must match registry")
        elif ref.get("kind") == "primary_chain":
            if not ref.get("source_uri") or not ref.get("signature_or_slot"):
                raise ValueError("primary chain source requires immutable location and signature/slot")
        elif ref.get("kind") == "fixture":
            if packet["mode"] != "fixture" or not ref.get("source_uri"):
                raise ValueError("fixture refs are not live observations")
        else:
            raise ValueError("unknown source reference type")
        source_ids.add(ref["ref_id"])
    for claim in packet["claims"]:
        if not isinstance(claim, dict) or any(not claim.get(key) for key in ("claim_id", "statement", "epistemic_status")):
            raise ValueError("incomplete claim")
        if claim["epistemic_status"] not in ("hypothesis", "external_reported", "raw_observation", "derived_inference"):
            raise ValueError("no handoff-level self-declared independent validation")
        refs = claim.get("source_ref_ids", [])
        if not isinstance(refs, list) or set(refs) - source_ids:
            raise ValueError("claim cites unknown source")
        if claim["epistemic_status"] == "raw_observation":
            if not refs or not any(ref["ref_id"] in refs and ref["kind"] in ("primary_chain", "fixture") for ref in packet["source_refs"]):
                raise ValueError("raw observation cannot be supported by a K1 document alone")
            if packet["mode"] == "research_only":
                raise ValueError("raw observations require real or fixture source mode")
        observed = claim.get("event_at_utc")
        available = claim.get("available_at_utc")
        if observed is not None or available is not None or claim.get("predictive_feature"):
            if not observed or not available:
                raise ValueError("as-of claim requires both event and available timestamps")
            t_event, t_available = _utc(observed), _utc(available)
            if t_available < t_event:
                raise ValueError("available_at cannot precede original event")
            if claim.get("predictive_feature") and (t_event > cutoff or t_available > cutoff):
                raise ValueError("lookahead feature unavailable at decision time")
    if not isinstance(packet["missing"], list) or not isinstance(packet["alternatives"], list) or not isinstance(packet["counterevidence"], list):
        raise ValueError("handoff needs explicit missing/alternative/counterevidence arrays")
    gate_ids = {g["id"] for g in _json(POLICY)["gates"]}
    statuses = set(_json(POLICY)["result_values"])
    seen = set()
    for g in packet["gate_results"]:
        gate_id = g.get("gate_id")
        if gate_id in seen or gate_id not in gate_ids or g.get("status") not in statuses:
            raise ValueError("bad gate result")
        seen.add(gate_id)
        if g["status"] == "PASS_WITH_EVIDENCE":
            refs = g.get("source_ref_ids")
            if packet["mode"] == "fixture" or not refs or set(refs) - source_ids:
                raise ValueError("gate pass needs non-fixture cited evidence")
            if gate_id in {"F4", "F5", "F6"} and (
                g.get("reviewer_bot_id") not in {"B05", "B06"} or g.get("reviewer_bot_id") == producer
            ):
                raise ValueError("independent reviewer required for economic/validation pass")
            if gate_id == "F6" and (
                not packet.get("human_approval_ref") or not packet.get("frozen_rule_commit")
            ):
                raise ValueError("F6 requires recorded human approval and immutable rule")
    if producer == "B07" and packet["packet_type"] == "monitor_observation":
        if not packet.get("frozen_rule_commit") or not packet.get("human_approval_ref"):
            raise ValueError("monitor must cite frozen approved rule")
    return {"status":"STRUCTURALLY_VALID_ONLY", "verified_market_evidence":False,
            "authorized_real_trading":False, "packet_id":packet["packet_id"],
            "producer_bot_id":producer, "claims":len(packet["claims"]), "gates":len(packet["gate_results"])}


def main() -> int:
    p = argparse.ArgumentParser(description="Role knowledge map and handoff validator (offline only)")
    selection = p.add_mutually_exclusive_group(required=True)
    selection.add_argument("--audit", action="store_true")
    selection.add_argument("--bot")
    selection.add_argument("--validate-handoff", type=Path)
    p.add_argument("--question", help="Needed with --bot; question is not market evidence")
    p.add_argument("--max-sources", type=int, default=4)
    ns = p.parse_args()
    try:
        if ns.audit:
            out = validate_profiles()
        elif ns.bot:
            out = build_role_brief(ns.bot, ns.question, ns.max_sources)
        else:
            out = validate_handoff(json.loads(ns.validate_handoff.read_text(encoding="utf-8")))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status":"ERROR", "error":str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
