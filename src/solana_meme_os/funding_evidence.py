"""KB-002: time-bounded fixture-only examination of shared inbound SOL.

Observed transfers are not evidence of a shared real-world owner or a profitable
trade. This module reads no keys, calls no network and never sends a transaction.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

from .monitor import ADDRESS


def utc(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be ISO-8601 string")
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid timestamp") from exc
    if date.tzinfo is None:
        raise ValueError("timestamp needs timezone")
    return date.astimezone(timezone.utc)


def address(value: Any) -> str:
    if not isinstance(value, str) or not ADDRESS.fullmatch(value):
        raise ValueError("invalid wallet address")
    return value


def ref(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing original evidence reference")
    return value


def examine(document: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(document, dict) or document.get("schema_version") != "1.0" or document.get("chain") != "sol":
        raise ValueError("unsupported schema / chain")
    if document.get("mode") != "fixture":
        raise ValueError("KB-002 only supports explicit fixtures until live data validation")
    cutoff = utc(document.get("analysis_cutoff"))
    targets_raw = document.get("target_wallets")
    if not isinstance(targets_raw, list) or len(targets_raw) < 2:
        raise ValueError("requires two or more target_wallets")
    targets = [address(a) for a in targets_raw]
    if len(set(targets)) != len(targets):
        raise ValueError("duplicate target wallet")
    coverage = document.get("coverage")
    if not isinstance(coverage, dict) or not isinstance(coverage.get("complete"), bool) or not isinstance(coverage.get("truncated"), bool):
        raise ValueError("coverage needs explicit complete/truncated")
    errors = coverage.get("rpc_errors")
    if isinstance(errors, bool) or not isinstance(errors, int) or errors < 0:
        raise ValueError("invalid rpc_errors")
    if not isinstance(document.get("policy"), dict):
        raise ValueError("missing funding policy")
    floor = document["policy"].get("min_material_lamports")
    if isinstance(floor, bool) or not isinstance(floor, int) or floor < 1:
        raise ValueError("invalid min_material_lamports")
    if document["policy"].get("status") != "illustrative":
        raise ValueError("funding threshold must remain illustrative")
    source_list = document.get("sources")
    if not isinstance(source_list, list):
        raise ValueError("sources must be a list")
    sources: dict[str, dict] = {}
    for s in source_list:
        if not isinstance(s, dict):
            raise ValueError("invalid source metadata")
        key = address(s.get("address"))
        if key in sources or s.get("classification") not in ("known_hub", "non_hub_reviewed", "unclassified"):
            raise ValueError("invalid/duplicate source classification")
        ref(s.get("classification_ref"))
        checked = utc(s.get("checked_at"))
        if checked > cutoff:
            raise ValueError("source label was not available at cutoff")
        sources[key] = s
    transfers = document.get("transfers")
    if not isinstance(transfers, list):
        raise ValueError("transfers must be a list")
    seen: set[tuple[str, int]] = set()
    funding: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    counters = {"excluded_future_available": 0, "dust_like_count": 0, "out_of_scope_count": 0, "accepted_transfer_count": 0}
    for event in transfers:
        if not isinstance(event, dict) or event.get("asset") != "SOL_NATIVE":
            raise ValueError("only native SOL transfer events allowed")
        src = address(event.get("from_wallet"))
        dst = address(event.get("to_wallet"))
        if src == dst:
            raise ValueError("transfer endpoints must differ")
        signature = ref(event.get("signature"))
        idx = event.get("instruction_index")
        if isinstance(idx, bool) or not isinstance(idx, int) or idx < 0:
            raise ValueError("invalid instruction_index")
        key = signature, idx
        if key in seen:
            raise ValueError("duplicate signature/instruction_index")
        seen.add(key)
        amount = event.get("lamports")
        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
            raise ValueError("invalid lamports amount")
        ref(event.get("source_ref"))
        occurred, available = utc(event.get("block_time")), utc(event.get("available_at"))
        if available < occurred:
            raise ValueError("available_at cannot precede block_time")
        if occurred > cutoff or available > cutoff:
            counters["excluded_future_available"] += 1
            continue
        if dst not in targets:
            counters["out_of_scope_count"] += 1
            continue
        if amount < floor:
            counters["dust_like_count"] += 1
            continue
        funding[src][dst].append({"signature": signature, "instruction_index": idx,
                                   "lamports": amount, "block_time": event["block_time"],
                                   "available_at": event["available_at"], "source_ref": event["source_ref"]})
        counters["accepted_transfer_count"] += 1
    groups = []
    for src, recipients in sorted(funding.items()):
        if len(recipients) < 2:
            continue
        classification = sources.get(src, {}).get("classification", "unclassified")
        kind = {"known_hub": "hub_excluded", "non_hub_reviewed": "observed_shared_inbound",
                "unclassified": "needs_hub_review"}[classification]
        group_events = []
        for wallet in sorted(recipients):
            for row in recipients[wallet]:
                group_events.append({"to_wallet": wallet, **row})
        groups.append({"source_wallet": src, "recipient_count": len(recipients),
                       "target_wallets": sorted(recipients), "relation": kind,
                       "claim_class": "observational_candidate",
                       "infrastructure_evidence": sources.get(src, {}).get("classification_ref"),
                       "evidence": sorted(group_events, key=lambda v: (v["available_at"], v["signature"], v["instruction_index"])),
                       "caveat": "shared inbound transfer != shared owner or trade intent"})
    incomplete = not coverage["complete"] or coverage["truncated"] or errors > 0
    return {"schema_version": "1.0", "knowledge_pack": "KB-002", "mode": "fixture",
            "status": "REFERENCE_ONLY_NOT_VALIDATED", "analysis_cutoff": document["analysis_cutoff"],
            "policy": {"min_material_lamports": floor, "status": "illustrative"},
            "coverage_state": "UNKNOWN_INCOMPLETE" if incomplete else "COMPLETE_AS_DECLARED_IN_FIXTURE",
            "groups": groups, "counts": counters, "no_trading": True,
            "absence_interpretation": "No observed shared material direct inbound in declared scope; not a proof of independence." if not groups else None,
            "follow_up": ["verify raw transactions and pagination", "independently verify hub classifications",
                          "compare ordinary wallet nulls and cross-period stability", "do not infer ownership or profitability"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline reference-only inbound SOL evidence checks")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--allow-fixture", action="store_true")
    args = parser.parse_args()
    try:
        if not args.allow_fixture:
            raise ValueError("explicit --allow-fixture is required")
        result = examine(json.loads(args.input.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "message": str(exc), "no_trading": True}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
