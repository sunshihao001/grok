"""Small, fail-closed knowledge registry for read-only interpretive context.

This module attaches *limitations* and source pointers; it is not a trade signal.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = ROOT / "knowledge" / "registry.v0.json"
_SHA = re.compile(r"^[a-f0-9]{40}$")
_REQUIRED = {"SNAPSHOT", "LIQUIDITY_DROP", "TOP10_SHARE_RISE", "NEW_SOURCE_EVENT", "MISSING_DATA"}


def load_registry(path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    path = Path(path)
    obj = json.loads(path.read_text(encoding="utf-8"))
    if obj.get("schema_version") != "1.0" or not isinstance(obj.get("version"), str):
        raise ValueError("unsupported knowledge registry schema/version")
    sources = obj.get("sources")
    packs = obj.get("packs")
    if not isinstance(sources, list) or not sources or not isinstance(packs, list) or not packs:
        raise ValueError("knowledge registry must contain sources and packs")
    ids: set[str] = set()
    for src in sources:
        if (not isinstance(src, dict) or not isinstance(src.get("id"), str)
                or src["id"] in ids or not isinstance(src.get("repository"), str)
                or not isinstance(src.get("path"), str) or not src["path"]
                or not _SHA.fullmatch(str(src.get("commit", "")))
                or not _SHA.fullmatch(str(src.get("blob_sha", "")))):
            raise ValueError("invalid or duplicate knowledge source reference")
        ids.add(src["id"])
    used: set[str] = set()
    root = path.resolve().parent.parent
    for pack in packs:
        if (not isinstance(pack, dict) or pack.get("stage") != "reference_only"
                or not isinstance(pack.get("id"), str) or pack["id"] in used
                or not isinstance(pack.get("source_ids"), list)
                or not pack["source_ids"] or set(pack["source_ids"]) - ids):
            raise ValueError("invalid knowledge pack or source IDs")
        used.add(pack["id"])
        rel = pack.get("path")
        if not isinstance(rel, str) or not rel.startswith("knowledge/packs/") or not rel.endswith(".md"):
            raise ValueError("invalid knowledge pack path")
        resolved = (root / rel).resolve()
        if not resolved.is_relative_to(root / "knowledge" / "packs") or not resolved.is_file():
            raise ValueError("knowledge pack file missing or outside pack directory")
        if not resolved.read_text(encoding="utf-8").strip():
            raise ValueError("knowledge pack is empty")
        guidance = pack.get("trigger_guidance")
        triggers = pack.get("triggers")
        if (not isinstance(guidance, dict) or not isinstance(triggers, list)
                or set(guidance) != set(triggers) or not _REQUIRED.issubset(guidance)):
            raise ValueError("knowledge trigger coverage incomplete")
        if any(not isinstance(v, dict) or not v.get("interpretation") or not v.get("verify") for v in guidance.values()):
            raise ValueError("knowledge guidance requires interpretation and verify")
    return obj


def contextualize(result: dict[str, Any], registry_path: Path = DEFAULT_REGISTRY) -> dict[str, Any]:
    """Attach provenance and cautious interpretation, never change any alert or gate."""
    registry = load_registry(registry_path)
    tags = {"SNAPSHOT"}
    tags.update(a.get("type") for a in result.get("alerts", []) if isinstance(a, dict))
    if result.get("missing_fields"):
        tags.add("MISSING_DATA")
    guidance: list[dict[str, str]] = []
    relevant: list[dict[str, Any]] = []
    for pack in registry["packs"]:
        intersection = sorted(tags.intersection(pack["triggers"]))
        if not intersection:
            continue
        relevant.append({"id": pack["id"], "version": pack["version"],
                         "stage": pack["stage"], "path": pack["path"], "source_ids": pack["source_ids"]})
        for tag in intersection:
            v = pack["trigger_guidance"][tag]
            guidance.append({"trigger": tag, "pack": pack["id"],
                             "interpretation": v["interpretation"], "verify": v["verify"]})
    return {"registry_version": registry["version"], "packs": relevant,
            "guidance": guidance, "status": "REFERENCE_ONLY_NOT_VALIDATED",
            "note": "Knowledge guides explanation and source checks only; it is not a tested signal, gate, or performance claim."}
