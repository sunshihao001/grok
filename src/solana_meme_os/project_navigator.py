"""Read-only navigation for existing Solana Meme knowledge and project capabilities.

This is a deterministic candidate locator, not semantic comprehension, a Grok
Bot invocation, network research, or a live market/data integration. Preserve
the original knowledge sources and inspect their evidence before conclusions.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
NAV = ROOT / "knowledge/system/knowledge-navigation.v1.json"


def load_navigation(path: Path = NAV) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0" or data.get("status") != "DESIGN_AND_INDEX_ONLY":
        raise ValueError("unsupported navigation index")
    return data


def _safe_relative(path: str) -> bool:
    if not isinstance(path, str) or not path or "\\" in path or path.startswith("/"):
        return False
    return all(p not in ("", ".", "..") for p in path.split("/"))


def audit(data: dict[str, Any] | None = None, root: Path = ROOT) -> dict[str, Any]:
    """Verify local knowledge links, cross-refs and declarations; no remote API."""
    d = data if data is not None else load_navigation()
    errors: list[str] = []
    paths_checked = 0
    try:
        ontology = json.loads((root / "knowledge/system/ontology.v1.json").read_text(encoding="utf-8"))
        specialists = json.loads((root / "knowledge/experts/registry.v1.json").read_text(encoding="utf-8"))
        index = json.loads((root / "knowledge/system/gpt-meme-project-index.v1.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"ok": False, "errors": [str(exc)], "local_paths_checked": 0,
                "remote_engineering_paths_unchecked": 0}
    valid_domains = {x["id"] for x in ontology["domains"]}
    valid_experts = {x["id"] for x in specialists["specialists"]}
    valid_references = {x["id"] for x in index["reference_assets"]["items"]}
    route_ids = [x.get("id") for x in d.get("routes", [])]
    ui_ids = [x.get("id") for x in d.get("ui_views", [])]
    engineering = {x.get("id"): x for x in d.get("engineering_assets", [])}
    canonical = d.get("canonical_assets", [])
    if len(route_ids) != len(set(route_ids)) or not route_ids:
        errors.append("duplicate or empty intent routes")
    if len(ui_ids) != len(set(ui_ids)) or not ui_ids:
        errors.append("duplicate or empty UI views")
    if len(engineering) != len(d.get("engineering_assets", [])):
        errors.append("duplicate engineering IDs")
    local_paths = {x.get("path") for x in canonical}
    for route in d.get("routes", []):
        rid = route.get("id")
        if not route.get("goal") or not route.get("expected_output") or not route.get("cues"):
            errors.append(f"{rid}: missing goal, cues or expected output")
        local_paths.update(route.get("knowledge_files", []))
        for key, permitted in (("domains", valid_domains), ("experts", valid_experts),
                               ("reference_ids", valid_references), ("ui_views", set(ui_ids)),
                               ("engineering_ids", set(engineering))):
            for value in route.get(key, []):
                if value not in permitted:
                    errors.append(f"{rid}: unknown {key} {value}")
    for path in local_paths:
        if not _safe_relative(path):
            errors.append(f"unsafe knowledge path {path!r}")
            continue
        if not (root / path).is_file():
            errors.append(f"missing knowledge path {path}")
        else:
            paths_checked += 1
    for asset in d.get("engineering_assets", []):
        if not _safe_relative(asset.get("path")):
            errors.append(f"unsafe engineering path {asset.get('path')!r}")
    for view in d.get("ui_views", []):
        for rid in view.get("default_intents", []):
            if rid not in route_ids:
                errors.append(f"view {view.get('id')} points to unknown route {rid}")
    if d.get("branches", {}).get("knowledge") == d.get("branches", {}).get("engineering"):
        errors.append("knowledge and engineering branches conflated")
    return {
        "ok": not errors,
        "errors": sorted(errors),
        "local_paths_checked": paths_checked,
        "remote_engineering_paths_unchecked": len(d.get("engineering_assets", [])),
        "scope": "static navigation only; no remote code, runtime, source accuracy or Grok deployment verified",
    }


def _present(route: dict[str, Any], engineering: dict[str, Any], branch: str,
             score: float | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "intent": route["id"],
        "goal": route["goal"],
        "domain_ids": route["domains"],
        "expert_lens_ids": route["experts"],
        "knowledge_paths_on_current_branch": route["knowledge_files"],
        "engineering_candidates_on_separate_branch": [
            {"path": engineering[id]["path"], "branch": branch,
             "declared_role": engineering[id]["role"], "invoked": False,
             "available_in_current_checkout": (ROOT / engineering[id]["path"]).is_file(),
             "checkout_is_not_runtime_validation": True}
            for id in route["engineering_ids"]
        ],
        "reference_asset_ids": route["reference_ids"],
        "ui_views": route["ui_views"],
        "expected_output": route["expected_output"],
    }
    if score is not None:
        result["literal_cue_score_not_confidence"] = round(score, 2)
    return result


def shortlist(question: str, data: dict[str, Any] | None = None,
              limit: int = 3, intent: str | None = None) -> dict[str, Any]:
    """Return file/role candidates. Do NOT use this as authority for reasoning."""
    d = data if data is not None else load_navigation()
    engineering = {x["id"]: x for x in d["engineering_assets"]}
    branch = d["branches"]["engineering"]
    if not isinstance(question, str):
        raise ValueError("question must be string")
    limit = max(1, min(int(limit), 5))
    routes = d["routes"]
    if intent is not None:
        selected = [r for r in routes if r["id"] == intent]
        if not selected:
            raise ValueError(f"unknown navigation intent: {intent}")
        picks = [_present(selected[0], engineering, branch)]
        match_kind = "explicit_intent"
    else:
        normalized = question.casefold().strip()
        scores = []
        for route in routes:
            hits = {c.casefold() for c in route["cues"] if c and c.casefold() in normalized}
            score = sum(min(3.0, 0.7 + len(c) / 4.0) for c in hits)
            if score:
                scores.append((score, route))
        scores.sort(key=lambda entry: (-entry[0], entry[1]["id"]))
        picks = [_present(r, engineering, branch, score) for score, r in scores[:limit]]
        match_kind = "literal_cue_candidates_not_semantic_routing"
    return {
        "query": question,
        "match_kind": match_kind,
        "routes": picks,
        "no_match": not picks,
        "guidance": (
            "AI must infer task intent, inspect relevant ORIGINAL research and actual source/code; "
            "this shortlist does not read files, run tools, confirm a claim or invoke Grok. "
            "If omitted or wrong, search ontology/cross-domain relationships and revise the shortlist."
        ),
    }


def open_knowledge(path: str, data: dict[str, Any] | None = None,
                   root: Path = ROOT, max_chars: int = 2400) -> dict[str, Any]:
    """Read a specifically indexed, local ORIGINAL source, never any arbitrary path."""
    d = data if data is not None else load_navigation()
    permitted = {x["path"] for x in d["canonical_assets"]}
    permitted.update(path for route in d["routes"] for path in route["knowledge_files"])
    if path not in permitted or not _safe_relative(path):
        raise ValueError("path is not an allowlisted knowledge source")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError("knowledge source missing or outside repository")
    raw = resolved.read_bytes()
    if len(raw) > 2_000_000:
        raise ValueError("knowledge source exceeds safe read limit")
    content = raw.decode("utf-8")
    cap = max(200, min(int(max_chars), 12000))
    return {
        "source_path": path,
        "source_branch": d["branches"]["knowledge"],
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "characters_total": len(content),
        "excerpt": content[:cap],
        "truncated": len(content) > cap,
        "note": "Original source excerpt read locally; interpretation and evidence validation are separate.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only project knowledge navigator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--audit", action="store_true")
    group.add_argument("--list", action="store_true")
    group.add_argument("--question")
    group.add_argument("--intent")
    group.add_argument("--open-path", help="Read a permitted original knowledge file excerpt")
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args(argv)
    try:
        data = load_navigation()
        if args.audit:
            output = audit(data)
        elif args.open_path:
            output = open_knowledge(args.open_path, data)
        elif args.list:
            output = {"intents": [{"id": x["id"], "goal": x["goal"]} for x in data["routes"]],
                      "status": data["status"]}
        else:
            output = shortlist(args.question or "", data, limit=args.limit, intent=args.intent)
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0 if not args.audit or output["ok"] else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
