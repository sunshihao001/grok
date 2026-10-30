"""Audit versioned GPT-to-GitHub-to-Grok learning-unit delivery.

Learning progress is NOT market evidence, model fine-tuning or monitor authorization.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from .knowledge_system import ROOT

REGISTRY = ROOT / "knowledge/transfer/curriculum.v1.json"
ROSTER = ROOT / "design/bot-roster.v1.json"
ONTOLOGY = ROOT / "knowledge/system/ontology.v1.json"
SOURCES = ROOT / "knowledge/source_index.v1.json"
LEVELS = ("C0", "C1", "C2", "C3", "C4")
STATUSES = {"draft", "approved_for_study", "retired"}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_file(path: str) -> Path:
    if not isinstance(path, str) or not path or path.startswith("/") or "\\" in path:
        raise ValueError("invalid knowledge file path")
    parts = Path(path).parts
    if any(part in ("", ".", "..") for part in parts):
        raise ValueError("path traversal not allowed")
    resolved = (ROOT / path).resolve()
    if not resolved.is_relative_to(ROOT.resolve()) or not resolved.is_file():
        raise ValueError(f"knowledge file missing or unsafe: {path}")
    return resolved


def audit(data: dict[str, Any] | None = None) -> dict[str, Any]:
    data = data if data is not None else _load(REGISTRY)
    if data.get("schema_version") != "1.0" or data.get("level_order") != list(LEVELS):
        raise ValueError("unknown curriculum schema or learning level order")
    levels = data.get("levels", [])
    if [x["id"] for x in levels] != list(LEVELS):
        raise ValueError("missing learning level")
    roles = {b["id"] for b in _load(ROSTER)["bots"]}
    domains = {d["id"] for d in _load(ONTOLOGY)["domains"]}
    source_ids = {x["id"] for x in _load(SOURCES)["items"]}
    units = data.get("units", [])
    ids = [x["id"] for x in units]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate lesson ID")
    lookup = {u["id"]: u for u in units}
    for u in units:
        required = {"id", "title", "level", "status", "approval_ref",
                    "target_bot_ids", "domain_ids", "knowledge_path",
                    "authority_paths", "source_index_ids", "prerequisite_unit_ids",
                    "review_questions", "success_conditions",
                    "market_evidence_status", "monitor_rule_authorized"}
        if required - set(u):
            raise ValueError("incomplete learning unit")
        if u["level"] not in LEVELS or not u["id"].startswith(u["level"] + "-"):
            raise ValueError("lesson ID/level mismatch")
        if u["status"] not in STATUSES:
            raise ValueError("invalid lesson status")
        if u["status"] == "approved_for_study" and not u["approval_ref"]:
            raise ValueError("learning approval reference required")
        if u["status"] == "draft" and u["approval_ref"]:
            raise ValueError("draft cannot claim learning approval")
        if u["market_evidence_status"] != "not_evaluated" or u["monitor_rule_authorized"] is not False:
            raise ValueError("learning curriculum may not validate market evidence or release rules")
        if not u["target_bot_ids"] or set(u["target_bot_ids"]) - roles or len(u["target_bot_ids"]) != len(set(u["target_bot_ids"])):
            raise ValueError("invalid learner roles")
        if not u["domain_ids"] or set(u["domain_ids"]) - domains:
            raise ValueError("invalid knowledge domains")
        if set(u["source_index_ids"]) - source_ids:
            raise ValueError("unknown source index reference")
        if not u["review_questions"] or not u["success_conditions"]:
            raise ValueError("lesson must have explicit acceptance questions")
        _safe_file(u["knowledge_path"])
        for path in u["authority_paths"]:
            _safe_file(path)
        for prereq in u["prerequisite_unit_ids"]:
            if prereq not in lookup or prereq == u["id"]:
                raise ValueError("unknown or self prerequisite")
            if LEVELS.index(lookup[prereq]["level"]) > LEVELS.index(u["level"]):
                raise ValueError("lesson depends on future level")
    visiting, visited = set(), set()
    def walk(unit_id: str) -> None:
        if unit_id in visiting:
            raise ValueError("cyclic learning unit dependency")
        if unit_id in visited:
            return
        visiting.add(unit_id)
        for prereq in lookup[unit_id]["prerequisite_unit_ids"]:
            walk(prereq)
        visiting.remove(unit_id)
        visited.add(unit_id)
    for unit_id in ids:
        walk(unit_id)
    return {
        "status":"VALID_STATIC_CURRICULUM",
        "learning_units":len(units),
        "approved_for_study":sum(u["status"]=="approved_for_study" for u in units),
        "draft_units":sum(u["status"]=="draft" for u in units),
        "grok_skill_installed":False,
        "market_claims_verified":False,
        "monitor_rule_authorized":False,
    }


def plan(bot_id: str, through_level: str, include_drafts: bool = False) -> dict[str, Any]:
    result = audit()
    data = _load(REGISTRY)
    roles = {b["id"] for b in _load(ROSTER)["bots"]}
    if bot_id not in roles:
        raise ValueError("unknown Bot ID")
    if through_level not in LEVELS:
        raise ValueError("unknown learning level")
    max_level = LEVELS.index(through_level)
    allowed = {"approved_for_study"} | ({"draft"} if include_drafts else set())
    units = [u for u in data["units"] if bot_id in u["target_bot_ids"]
             and LEVELS.index(u["level"]) <= max_level and u["status"] in allowed]
    included_ids = {u["id"] for u in units}
    returned = []
    for u in units:
        missing = [p for p in u["prerequisite_unit_ids"] if p not in included_ids]
        if missing:
            continue
        returned.append({
            "unit_id":u["id"],
            "title":u["title"],
            "level":u["level"],
            "release_status":u["status"],
            "for_preview_only":u["status"] != "approved_for_study",
            "knowledge_path":u["knowledge_path"],
            "authority_paths":u["authority_paths"],
            "study_checks":u["review_questions"],
            "market_evidence_status":u["market_evidence_status"],
        })
    return {
        "bot_id":bot_id,
        "through_level":through_level,
        "draft_preview_mode":include_drafts,
        "selection":"VERSIONED_LEARNING_POINTERS_NOT_LOADED_GROK_MEMORY",
        "learning_units":returned,
        "total_lessons_in_registry":result["learning_units"],
        "missing_approved_lessons_is_not_a_market_negative":True,
        "next_action":"Grok must read selected files at a pinned checkout and return an independently reviewable response."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline GPT/GitHub/Grok knowledge delivery")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true")
    group.add_argument("--bot")
    parser.add_argument("--through", choices=LEVELS, default="C1")
    parser.add_argument("--preview-drafts", action="store_true")
    args = parser.parse_args()
    try:
        result = audit() if args.audit else plan(args.bot, args.through, args.preview_drafts)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status":"ERROR","error":str(exc)}, ensure_ascii=False),file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
