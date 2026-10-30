"""On-demand research intake. No Hermes runtime, no bulk knowledge migration.

This deterministic preprocessor returns source candidates and falsification requirements.
It is not the Grok model and cannot reason about unobserved Solana events.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

from .knowledge import for_question
from .knowledge_system import route_domains, read as read_knowledge_system, filter_plan
from .source_admission import load_admission, is_routable

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "knowledge/source_index.v1.json"
ALLOWED_REPOS = {"sunshihao001/Why-Solana-Memecoins-Are-Over", "sunshihao001/-", "sunshihao001/meme-", "sunshihao001/qb-"}
REQ = {"id", "repository", "commit", "path", "topics", "why", "kind", "availability"}
CONSTANT_CHECKS = [
    "定义研究对象、决策时间、样本总体及分母；不存在的数据不能假装为零。",
    "把链上事实、平台标签、主体归因、获利预测分开；给出至少一个竞争机制。",
    "任何预测特征必须在决策时间已被观测且可取得，禁止事后数据泄漏。",
    "用未命中样本、随机/null对照或历史同类失败案例挑战假说。",
    "只有在价格、延迟、滑点、手续费、退出可行性被测量后，才讨论经济优势。",
]


def _time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be ISO-8601 with timezone")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid ISO-8601 timestamp") from exc
    if dt.tzinfo is None:
        raise ValueError("timestamp must contain timezone")
    return dt.astimezone(timezone.utc)


def load_index(path: Path = INDEX) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0" or not isinstance(data.get("items"), list) or not data["items"]:
        raise ValueError("invalid source registry")
    seen = set()
    for item in data["items"]:
        if not isinstance(item, dict) or not REQ.issubset(item):
            raise ValueError("incomplete source item")
        if item["id"] in seen or not item["topics"] or not isinstance(item["topics"], list):
            raise ValueError("duplicate source ID or missing topics")
        if item["repository"] not in ALLOWED_REPOS:
            raise ValueError("source repository not allowed")
        if len(item["commit"]) != 40 or any(c not in "0123456789abcdef" for c in item["commit"]):
            raise ValueError("source must be pinned to a Git commit")
        if item["path"].startswith("/") or any(p in ("", ".", "..") for p in item["path"].split("/")):
            raise ValueError("unsafe source path")
        seen.add(item["id"])
    return data


def _ref(item: dict[str, Any], hits: list[str]) -> dict[str, Any]:
    path = "/".join(quote(p, safe="") for p in item["path"].split("/"))
    return {"id": item["id"], "why": item["why"], "kind": item["kind"], "matched_topics": hits,
            "repository": item["repository"], "commit": item["commit"], "path": item["path"],
            "source_url": f"https://github.com/{item['repository']}/blob/{item['commit']}/{path}",
            "availability": item["availability"], "license_note": item.get("license_note")}


def select_sources(question: str, index: dict[str, Any] | None = None, limit: int = 5,
                   include_review_only: bool = False) -> list[dict[str, Any]]:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("question is required")
    if not 1 <= limit <= 12:
        raise ValueError("limit out of range")
    index = index or load_index()
    admission = load_admission(index)
    query = question.casefold()
    found = []
    for item in index["items"]:
        if not is_routable(item["id"], admission, include_review_only):
            continue
        hits = [tag for tag in item["topics"] if tag.casefold() in query]
        if hits:
            # Prefer specific matches but don't claim this is semantic understanding.
            ref = _ref(item, hits)
            ref["admission_state"] = admission[item["id"]]["admission_state"]
            found.append((len(hits), item["id"], ref))
    found.sort(key=lambda e: (-e[0], e[1]))
    return [r for _, _, r in found[:limit]]


def evaluate_observations(observations: list[dict[str, Any]], decision_time: str | None) -> dict[str, Any]:
    """Validate provenance and time-of-knowledge, without inferring the market."""
    if not isinstance(observations, list):
        raise ValueError("observations must be a JSON list")
    if not decision_time:
        return {"state": "DECISION_TIME_MISSING", "accepted": [], "rejected": len(observations)}
    cutoff = _time(decision_time)
    accepted, rejected = [], []
    for i, fact in enumerate(observations):
        if not isinstance(fact, dict) or not fact.get("source_ref") or not fact.get("claim"):
            rejected.append({"index": i, "reason": "MISSING_CLAIM_OR_SOURCE"})
            continue
        try:
            observed = _time(fact["observed_at"])
            available = _time(fact["available_at"])
        except (KeyError, ValueError):
            rejected.append({"index": i, "reason": "MISSING_OR_INVALID_TIMESTAMPS"})
            continue
        if observed > cutoff or available > cutoff or available < observed:
            rejected.append({"index": i, "reason": "NOT_KNOWN_AT_DECISION_TIME"})
            continue
        accepted.append({"claim": fact["claim"], "source_ref": fact["source_ref"],
                         "observed_at": fact["observed_at"], "available_at": fact["available_at"]})
    return {"state": "INPUT_REVIEWED", "cutoff": cutoff.isoformat(), "accepted": accepted, "rejected": rejected}


def build_packet(question: str, decision_time: str | None = None,
                 observations: list[dict[str, Any]] | None = None,
                 include_review_only: bool = False) -> dict[str, Any]:
    refs = select_sources(question, include_review_only=include_review_only)
    index = load_index()
    admission = load_admission(index)
    query = question.casefold()
    withheld = sum(1 for item in index["items"]
                   if admission[item["id"]]["admission_state"] == "review_only"
                   and not include_review_only
                   and any(tag.casefold() in query for tag in item["topics"]))
    source_repos = {s["id"]: s["repository"] for s in
                    read_knowledge_system("source-registry.v1.json")["source_entries"]}

    def unit_admitted(unit: dict[str, Any]) -> bool:
        repo = source_repos.get(unit["primary_source"]["source_id"])
        path = unit["primary_source"]["path"]
        return any(is_routable(item["id"], admission, include_review_only)
                   for item in index["items"]
                   if item["repository"] == repo and item["path"] == path)
    domain = for_question(question)
    assessed = evaluate_observations(observations or [], decision_time)
    ontology_route = route_domains(question)
    research_unit_candidates = [
        {"id": unit["id"], "title": unit["title"], "status": unit["status"],
         "runtime_policy": unit["runtime_policy"],
         "source_id": unit["primary_source"]["source_id"]}
        for unit in read_knowledge_system("research-units.v1.json")["units"]
        if set(unit["domains"]).intersection(ontology_route["matched_domains"]) and unit_admitted(unit)
    ]
    return {
        "schema_version": "1.0",
        "purpose": "research_intake_not_conclusion",
        "question": question,
        "reference_status": "SOURCES_INDEXED" if refs else ("REVIEW_ONLY_SOURCES_WITHHELD" if withheld else "SOURCE_DISCOVERY_REQUIRED"),
        "review_only_source_matches_withheld": withheld,
        "admission_policy": "Pinned source references are study candidates, not independently verified market observations.",
        "research_status": "EVIDENCE_REQUIRED" if not assessed["accepted"] else "OBSERVATIONS_TO_CHALLENGE",
        "sources": refs,
        "domain_knowledge": domain["references"][:3],
        "ontology_route": ontology_route,
        "filter_plan": filter_plan(),
        "filter_note": "The filters are NOT_EVALUATED. Existing observation cutoff review is not primary-data verification.",
        "research_unit_candidates": research_unit_candidates,
        "observations": assessed,
        "validation_contract": CONSTANT_CHECKS,
        "next_action": "Read primary sources selectively, verify data definitions and test competing hypotheses; do not auto-promote a rule.",
        "note": "No evidence of profitable alpha is asserted. A cited methodology is not a validated Solana strategy."
    }


def ephemeral_excerpt(ref: dict[str, Any], question: str, max_chars: int = 1200,
                      include_review_only: bool = False) -> dict[str, Any]:
    """Fetch only a pinned approved source; never store or publish a derived source copy."""
    if not 200 <= max_chars <= 2000:
        raise ValueError("excerpt size out of range")
    # Re-validate caller reference against the approved index, not arbitrary URLs.
    originals = {r["id"]: r for r in select_sources(question, limit=12,
                         include_review_only=include_review_only)}
    approved = originals.get(ref.get("id"))
    if not approved or any(approved[k] != ref.get(k) for k in ("repository", "commit", "path")):
        raise ValueError("source not selected from approved registry")
    path = "/".join(quote(p, safe="") for p in approved["path"].split("/"))
    url = f"https://raw.githubusercontent.com/{approved['repository']}/{approved['commit']}/{path}"
    req = Request(url, headers={"User-Agent": "Solana-Meme-Research-ReadOnly/0.1"})
    with urlopen(req, timeout=12) as response:
        raw = response.read(350001)
    if len(raw) > 350000:
        raise ValueError("source too large; inspect source directly")
    content = raw.decode("utf-8", errors="strict")
    query = question.casefold()
    terms = [x.casefold() for x in approved["matched_topics"]]
    matches = [content.casefold().find(t) for t in terms if len(t) >= 3 and content.casefold().find(t) >= 0]
    start = max(0, min(matches) - 220) if matches else 0
    return {"source_url": approved["source_url"], "excerpt": content[start:start + max_chars],
            "excerpt_only": True, "text_not_a_verified_market_claim": True,
            "license_note": approved.get("license_note")}


def main() -> int:
    p = argparse.ArgumentParser(description="Build a research intake packet from indexed sources")
    p.add_argument("--question", required=True)
    p.add_argument("--decision-at", help="timezone-aware ISO 8601")
    p.add_argument("--observations", type=Path, help="JSON list of evidence facts")
    p.add_argument("--fetch-excerpts", action="store_true", help="Optional read-only source previews")
    p.add_argument("--include-review-only", action="store_true", help="Explicit source audit, not normal routing or claim validation")
    args = p.parse_args()
    try:
        facts = json.loads(args.observations.read_text(encoding="utf-8")) if args.observations else None
        packet = build_packet(args.question, args.decision_at, facts,
                              include_review_only=args.include_review_only)
        if args.fetch_excerpts:
            packet["ephemeral_source_previews"] = []
            for ref in packet["sources"][:3]:
                try:
                    packet["ephemeral_source_previews"].append(ephemeral_excerpt(
                        ref, args.question, include_review_only=args.include_review_only))
                except (OSError, UnicodeError, ValueError) as exc:
                    packet["ephemeral_source_previews"].append({"source_url": ref["source_url"],
                        "status": "UNAVAILABLE", "error": str(exc)})
        print(json.dumps(packet, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
