"""Deterministic availability audit for *supplied* read-only Solana event metadata.

A valid record is not independently authenticated and does not prove prediction or fill.
No network, wallet or transaction capabilities exist here.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

NEEDED = ("event_id", "source_ref", "capture_mode", "event_at_utc",
          "provider_received_at_utc", "parsed_at_utc", "feature_available_at_utc",
          "decision_cutoff_utc")
CAPTURES = {"live_recorded", "historical_backfill"}


def _dt(value: str, key: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} requires timezone-aware timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{key} invalid ISO8601 timestamp") from exc
    if result.tzinfo is None:
        raise ValueError(f"{key} requires timezone-aware timestamp")
    return result.astimezone(timezone.utc)


def audit_event(record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(record, dict):
        raise ValueError("event must be object")
    if set(NEEDED) - set(record):
        raise ValueError("required as-of provenance field absent")
    if not isinstance(record["event_id"], str) or not record["event_id"].strip():
        raise ValueError("event_id required")
    if not isinstance(record["source_ref"], str) or not record["source_ref"].strip():
        raise ValueError("source_ref required")
    if record["capture_mode"] not in CAPTURES:
        raise ValueError("capture_mode must be live_recorded or historical_backfill")
    decision = _dt(record["decision_cutoff_utc"], "decision_cutoff_utc")
    if record["event_at_utc"] is None:
        return {"event_id":record["event_id"],"status":"EVENT_TIME_UNKNOWN",
                "eligible_as_decision_feature":False,
                "reason":"null blockTime must remain unknown; require alternate slot/receipt audit"}
    event = _dt(record["event_at_utc"], "event_at_utc")
    received = _dt(record["provider_received_at_utc"], "provider_received_at_utc")
    parsed = _dt(record["parsed_at_utc"], "parsed_at_utc")
    available = _dt(record["feature_available_at_utc"], "feature_available_at_utc")
    # Early provider receipt is not a proof of a later finalized event.
    if event > received or received > parsed or parsed > available:
        return {"event_id":record["event_id"],"status":"INCONSISTENT_TIME_ORDER",
                "eligible_as_decision_feature":False,
                "reason":"event <= provider_received <= parsed <= available must hold"}
    if record["capture_mode"] != "live_recorded":
        return {"event_id":record["event_id"],"status":"NO_CONTEMPORANEOUS_AVAILABILITY_PROOF",
                "eligible_as_decision_feature":False,
                "reason":"historical chain timestamps do not prove real-time observability"}
    if available > decision:
        return {"event_id":record["event_id"],"status":"POST_DECISION_UNAVAILABLE",
                "eligible_as_decision_feature":False,
                "reason":"feature was available only after the decision cutoff"}
    return {"event_id":record["event_id"],"status":"TIME_CUTOFF_ELIGIBLE_UNVERIFIED",
            "eligible_as_decision_feature":True,
            "reason":"supplied live timestamps pass order/cutoff; source authenticity and data content remain unverified"}


def audit_batch(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(events, list):
        raise ValueError("events must be a list")
    seen=set()
    decisions=[]
    for event in events:
        if not isinstance(event, dict):
            raise ValueError("events must contain objects")
        id=event.get("event_id")
        if id in seen:
            raise ValueError("duplicate event_id")
        seen.add(id)
        decisions.append(audit_event(event))
    counts={}
    for d in decisions:
        counts[d["status"]]=counts.get(d["status"],0)+1
    return {"status":"OFFLINE_TIME_AUDIT_ONLY","items":decisions,
            "counts":counts,"external_source_authenticated":False,
            "market_edge_proven":False,"live_trade_authorized":False}


def main() -> int:
    parser=argparse.ArgumentParser(description="Audit supplied as-of metadata; never fetch or trade")
    parser.add_argument("--input",type=Path,required=True)
    ns=parser.parse_args()
    try:
        data=json.loads(ns.input.read_text(encoding="utf-8"))
        print(json.dumps(audit_batch(data),ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"ERROR","reason":str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
