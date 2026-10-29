"""Curated historical knowledge as source-bound *questions*, never trading signals."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "knowledge" / "catalog.v1.json"

REQUIRED = ("id", "title", "status", "triggers", "keywords", "mechanism",
            "required_evidence", "alternative_explanations", "inference_limit", "next_check", "sources")
VALID_STATUSES = {"source_contract", "documented_legacy_method", "unverified_hypothesis"}
VALID_TRIGGERS = {"BASELINE", "MISSING_FIELDS", "LIQUIDITY_DROP", "TOP10_SHARE_RISE", "NEW_SOURCE_EVENT", "ON_DEMAND"}
PRIORITIES = {"source_contract": 2, "documented_legacy_method": 1, "unverified_hypothesis": 0}


def load_catalog(path: Path = CATALOG) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0" or not isinstance(data.get("cards"), list):
        raise ValueError("invalid knowledge catalog version or cards")
    seen: set[str] = set()
    for card in data["cards"]:
        if any(not card.get(key) for key in REQUIRED):
            raise ValueError(f"incomplete knowledge card: {card.get('id')}")
        if card["id"] in seen or card["status"] not in VALID_STATUSES:
            raise ValueError("duplicate card or invalid status")
        if not isinstance(card["triggers"], list) or set(card["triggers"]) - VALID_TRIGGERS:
            raise ValueError("invalid triggers")
        if not isinstance(card["keywords"], list):
            raise ValueError("invalid keywords")
        for item in card["sources"]:
            if not all(item.get(k) for k in ("repository", "commit", "path", "url")):
                raise ValueError("card must have exact source provenance")
            snapshot = item.get("snapshot_path")
            if snapshot and (not snapshot.startswith("knowledge/legacy-snapshots/") or not (ROOT / snapshot).is_file()):
                raise ValueError("referenced local knowledge snapshot missing")
            if len(item["commit"]) != 40 or not all(x in "0123456789abcdef" for x in item["commit"]):
                raise ValueError("unpinned source commit")
        seen.add(card["id"])
    if not data["cards"]:
        raise ValueError("empty catalog")
    return data


def public_card(card: dict[str, Any]) -> dict[str, Any]:
    return {key: card[key] for key in ("id", "title", "status", "mechanism",
          "required_evidence", "alternative_explanations", "inference_limit",
          "next_check", "sources")}


def for_question(question: str, catalog: dict[str, Any] | None = None, limit: int = 5) -> dict[str, Any]:
    """Keyword triage for a plain-language command; not a semantic reasoner."""
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question required")
    catalog = catalog or load_catalog()
    query = question.casefold()
    scored = []
    for card in catalog["cards"]:
        hits = [w for w in card["keywords"] if w.casefold() in query]
        if hits:
            scored.append((len(hits), PRIORITIES[card["status"]], card["id"], card))
    scored.sort(key=lambda row: (-row[0], -row[1], row[2]))
    return {"route_status": "MATCHED_REFERENCE" if scored else "NO_KNOWN_REFERENCE",
            "question": question, "catalog_version": catalog["schema_version"],
            "method": "literal_keyword_triage_not_semantic_reasoning",
            "references": [public_card(card) for _, _, _, card in scored[:limit]],
            "gap": None if scored else "No match in catalog; request evidence research, do not invent a method."}


def for_observation(result: dict[str, Any], catalog: dict[str, Any] | None = None, limit: int = 6) -> dict[str, Any]:
    """Attach source-backed interpretation questions to *observations*, never assert causality."""
    catalog = catalog or load_catalog()
    triggers = {a["type"] for a in result.get("alerts", [])}
    if result.get("missing_fields"):
        triggers.add("MISSING_FIELDS")
    if not triggers:
        triggers.add("BASELINE")
    selected = []
    for card in catalog["cards"]:
        matching = triggers.intersection(card["triggers"])
        if matching:
            # Prefer narrowly applicable concepts over broad generic catch-all cards.
            # Each additional trigger broadens applicability, reducing priority.
            score = (6 - len(card["triggers"])) * 5 + 2 * len(matching)
            selected.append((score, PRIORITIES[card["status"]], card["id"], card))
    selected.sort(key=lambda row: (-row[0], -row[1], row[2]))
    return {"catalog_version": catalog["schema_version"], "triggered_by": sorted(triggers),
            "limitations": "Historically documented knowledge; hypotheses not verified for this token.",
            "interpretation_candidates": [public_card(card) for _, _, _, card in selected[:limit]]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Route a plain-language research question to documented knowledge")
    parser.add_argument("--question", required=True)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    args = parser.parse_args()
    try:
        result = for_question(args.question, catalog=load_catalog(args.catalog))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"route_status": "ERROR", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
