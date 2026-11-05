"""Read-only validation and recovery of the project's evolving goal/decision state.

This is a deterministic ledger reader, NOT an autonomous goal-reasoning agent.
The AI must still interpret user intent, inspect original sources and take scoped actions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GOAL_RECORD = ROOT / "docs/goal-evolution-current.json"


def load(path: Path = GOAL_RECORD) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("goal record must be a JSON object")
    return data


def audit(data: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("unknown schema version")
    if data.get("boundaries", {}).get("operation") != "read_only":
        errors.append("current project boundary must be read_only")
    goals = data.get("goals", [])
    if not isinstance(goals, list):
        goals = []
    ids = [g.get("id") for g in goals if isinstance(g, dict)]
    if not ids or len(ids) != len(goals) or len(ids) != len(set(ids)):
        errors.append("duplicate or invalid goal IDs")
    valid = set(ids)
    for goal in goals:
        if not all(goal.get(k) for k in ("id", "level", "status", "authority", "text")):
            errors.append("goal lacks required fields")
        if goal.get("level") in ("purpose", "strategy") and goal.get("authority") not in ("user", "ai_recommendation"):
            errors.append("invalid strategic authority")
    for link in data.get("links", []):
        if link.get("from") not in valid or link.get("to") not in valid or not link.get("relation"):
            errors.append("broken goal relationship")
    for change in data.get("changes", []):
        if change.get("from") not in valid or change.get("to") not in valid or not change.get("meaning") or not change.get("basis"):
            errors.append("unsubstantiated goal change")
    dec = data.get("decision", {})
    options = dec.get("options", [])
    option_ids = [o.get("id") for o in options]
    if len(option_ids) < 2 or len(option_ids) != len(set(option_ids)):
        errors.append("missing or duplicated strategic options")
    if dec.get("preferred") not in option_ids or not dec.get("why") or not dec.get("reopen_if"):
        errors.append("decision lacks preferred option, reasoning or reopening triggers")
    for option in options:
        if not all(option.get(k) for k in ("id", "route", "benefit", "risk", "falsifier")):
            errors.append("option lacks evidence-facing comparison or falsification")
    action = data.get("next_action", {})
    if (not action.get("id") or not action.get("action") or not action.get("state")
            or not action.get("acceptance") or any(g not in valid for g in action.get("goal_ids", []))):
        errors.append("next action lacks testable acceptance or linked goals")
    ev = data.get("evidence_status", {})
    if not ev.get("unknown") or not ev.get("source_review") or not data.get("knowledge_preservation"):
        errors.append("evidence boundaries or old-knowledge preservation missing")
    return {
        "ok": not errors, "errors": errors,
        "goals_checked": len(goals), "options_checked": len(options),
        "scope": "record consistency only; does not confirm semantic goal understanding, market data or runtime",
    }


def brief(data: dict[str, Any]) -> dict[str, Any]:
    checked = audit(data)
    if not checked["ok"]:
        raise ValueError("; ".join(checked["errors"]))
    return {
        "kind": data["record_kind"],
        "current_goals": [g for g in data["goals"] if g["status"] in ("active", "retained")],
        "historical_changes": data["changes"],
        "current_decision": data["decision"],
        "next_action": data["next_action"],
        "human_boundaries": data["boundaries"],
        "evidence_status": data["evidence_status"],
        "warning": checked["scope"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect current user goals without claiming to infer them")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true")
    group.add_argument("--brief", action="store_true")
    parser.add_argument("--file", type=Path, default=GOAL_RECORD)
    args = parser.parse_args(argv)
    try:
        data = load(args.file)
        result = audit(data) if args.audit else brief(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if not args.audit or result["ok"] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
