"""Fail-closed admission for K1 source routing, separate from source provenance.

A pinned document is not validated market evidence. Review-only documents can
be read during an explicitly initiated source audit but are not suggested by
default research and Bot source routing.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ADMISSION_FILE = ROOT / "knowledge/source-admission.v1.json"
INDEX_FILE = ROOT / "knowledge/source_index.v1.json"
VALID_STATES = {"context_candidate", "review_only"}
PIN_FIELDS = ("repository", "commit", "path")


def load_admission(index: dict[str, Any] | None = None,
                   path: Path = ADMISSION_FILE) -> dict[str, dict[str, Any]]:
    """Validate complete, exact coverage of K1 pins; unknown means inaccessible."""
    index = index if index is not None else json.loads(INDEX_FILE.read_text(encoding="utf-8"))
    policy = json.loads(path.read_text(encoding="utf-8"))
    if policy.get("schema_version") != "1.0" or not isinstance(policy.get("items"), list):
        raise ValueError("invalid source admission policy")
    source_items = index.get("items")
    if not isinstance(source_items, list) or not source_items:
        raise ValueError("invalid source index")
    indexed = {x["id"]: x for x in source_items}
    if len(indexed) != len(source_items):
        raise ValueError("duplicate source index ID")
    rows: dict[str, dict[str, Any]] = {}
    for item in policy["items"]:
        if not isinstance(item, dict) or not item.get("id") or item["id"] in rows:
            raise ValueError("duplicate or malformed source admission")
        if item.get("admission_state") not in VALID_STATES or not item.get("reason"):
            raise ValueError("invalid admission state or missing reason")
        original = indexed.get(item["id"])
        if not original or any(item.get(k) != original.get(k) for k in PIN_FIELDS):
            raise ValueError("source admission pin conflicts with index")
        rows[item["id"]] = item
    if set(rows) != set(indexed):
        raise ValueError("source admission coverage mismatch")
    return rows


def is_routable(source_id: str, rows: dict[str, dict[str, Any]],
                include_review_only: bool = False) -> bool:
    """Explicit review opt-in does not confer factual, causal or alpha validity."""
    item = rows.get(source_id)
    if item is None:
        return False
    return item["admission_state"] == "context_candidate" or (
        include_review_only and item["admission_state"] == "review_only"
    )
