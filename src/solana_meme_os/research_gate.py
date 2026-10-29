"""KNOW-003: fail-closed, synthetic-only research protocol/return audit.

The purpose is to disprove false promotion claims. It is NOT a backtester,
signalling system, live RPC source, or trading execution implementation.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys
from typing import Any


def timestamp(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be ISO-8601 string")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid timestamp") from exc
    if dt.tzinfo is None:
        raise ValueError("timestamp requires timezone")
    return dt.astimezone(timezone.utc)


def nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing {name}")
    return value


def money(value: Any, name: str, *, positive: bool = False) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError(f"invalid {name}")
    try:
        val = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"invalid {name}") from exc
    if not val.is_finite() or val < 0 or (positive and val <= 0):
        raise ValueError(f"invalid {name}")
    return val


def audit(document: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(document, dict) or document.get("schema_version") != "1.0":
        raise ValueError("invalid research schema")
    if document.get("data_mode") != "synthetic_fixture":
        raise ValueError("only synthetic_fixture is supported")
    nonempty(document.get("study_id"), "study_id")
    h = document.get("hypothesis")
    if not isinstance(h, dict):
        raise ValueError("hypothesis required")
    for name in ("mechanism", "prediction", "falsification"):
        nonempty(h.get(name), f"hypothesis.{name}")
    if not isinstance(h.get("alternatives"), list) or len(h["alternatives"]) < 2:
        raise ValueError("at least two competing explanations required")
    for a in h["alternatives"]:
        nonempty(a, "alternative")
    protocol = document.get("protocol")
    if not isinstance(protocol, dict):
        raise ValueError("protocol required")
    for field in ("sample_frame", "independence_unit", "baseline", "matched_controls",
                  "null_model", "missing_policy", "multiple_testing_policy",
                  "exit_convention", "fee_convention", "raw_source_ref"):
        nonempty(protocol.get(field), f"protocol.{field}")
    if protocol.get("metric") != "realized_net_roi":
        raise ValueError("metric must be realized_net_roi")
    locked = timestamp(protocol.get("locked_at"))
    start = timestamp(protocol.get("test_start"))
    if locked > start:
        raise ValueError("pre-registration must precede TEST start")
    rows = document.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ValueError("rows required")
    seen = set()
    by_split: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    missing: dict[str, int] = defaultdict(int)
    for r in rows:
        if not isinstance(r, dict):
            raise ValueError("invalid row")
        key = nonempty(r.get("id"), "id")
        if key in seen:
            raise ValueError("duplicate row")
        seen.add(key)
        split = r.get("split")
        if split not in ("TRAIN", "TEST"):
            raise ValueError("split must be TRAIN or TEST")
        decision = timestamp(r.get("decision_at"))
        if (split == "TRAIN" and decision >= start) or (split == "TEST" and decision < start):
            raise ValueError("split violates pre-registered time boundary")
        if split == "TEST" and decision < locked:
            raise ValueError("test decision before locked rule")
        feats = r.get("features")
        if not isinstance(feats, list) or not feats:
            raise ValueError("every row needs time-stamped feature evidence")
        for feature in feats:
            if not isinstance(feature, dict):
                raise ValueError("invalid feature")
            name = nonempty(feature.get("name"), "feature.name")
            nonempty(feature.get("source_ref"), "feature.source_ref")
            event = timestamp(feature.get("event_at"))
            available = timestamp(feature.get("available_at"))
            if not event <= available <= decision:
                raise ValueError(f"feature availability leaks future for {name}")
            if any(word in name.lower() for word in ("future", "peak", "trough", "target_hit", "outcome")):
                raise ValueError("future label cannot be an input feature")
        measure = r.get("measurement_status")
        if measure == "MISSING":
            nonempty(r.get("missing_reason"), "missing_reason")
            if any(field in r for field in ("hit_target", "buy_filled_usd", "sell_filled_usd")):
                raise ValueError("missing rows cannot silently inherit outcomes")
            missing[split] += 1
            continue
        if measure != "MEASURED":
            raise ValueError("measurement_status must be MEASURED/MISSING")
        if not isinstance(r.get("signal"), bool) or not isinstance(r.get("hit_target"), bool):
            raise ValueError("measured row needs signal and hit_target booleans")
        entry = timestamp(r.get("entry_at"))
        exit_time = timestamp(r.get("exit_at"))
        outcome = timestamp(r.get("outcome_observed_at"))
        if entry < decision or exit_time < entry or outcome < decision:
            raise ValueError("entry/exit/outcome chronology invalid")
        buy = money(r.get("buy_filled_usd"), "buy_filled_usd", positive=True)
        sell = money(r.get("sell_filled_usd"), "sell_filled_usd")
        buy_fee = money(r.get("buy_fees_usd"), "buy_fees_usd")
        sell_fee = money(r.get("sell_fees_usd"), "sell_fees_usd")
        priority = money(r.get("priority_fees_usd"), "priority_fees_usd")
        if r.get("exit_status") not in ("FILLED", "FAILED"):
            raise ValueError("exit_status must be FILLED or FAILED")
        if r["exit_status"] == "FAILED" and sell != 0:
            raise ValueError("failed exit must use zero proceeds under conservative convention")
        cost = buy + buy_fee + priority
        roi = (sell - sell_fee - cost) / cost
        by_split[split]["selected" if r["signal"] else "baseline"].append(
            {"id": key, "roi": roi, "hit": r["hit_target"], "exit_failed": r["exit_status"] == "FAILED"})
    summary = {}
    for split in ("TRAIN", "TEST"):
        detail = {}
        for cohort in ("selected", "baseline"):
            samples = by_split[split][cohort]
            if samples:
                mean_net_roi = sum((v["roi"] for v in samples), Decimal(0)) / len(samples)
                detail[cohort] = {"n": len(samples),
                                  "hit_rate": sum(v["hit"] for v in samples) / len(samples),
                                  "mean_net_roi": float(mean_net_roi),
                                  "failed_exits": sum(v["exit_failed"] for v in samples)}
            else:
                detail[cohort] = {"n": 0, "hit_rate": None, "mean_net_roi": None, "failed_exits": 0}
        detail["missing_n"] = missing[split]
        summary[split] = detail
    test = summary["TEST"]["selected"]
    if test["n"] == 0:
        observed = "NO_EVALUABLE_SELECTED_TEST"
    elif test["mean_net_roi"] <= 0:
        observed = "NON_POSITIVE_NET_IN_SYNTHETIC_TEST"
    else:
        observed = "POSITIVE_SYNTHETIC_TEST_NOT_VALIDATED"
    return {
        "schema_version": "1.0", "study_id": document["study_id"],
        "status": "REFERENCE_ONLY_NOT_VALIDATED",
        "data_mode": "synthetic_fixture",
        "gate": {"mechanism": "HYPOTHESIS_NOT_INDEPENDENTLY_VERIFIED",
                 "prediction": "NOT_ESTABLISHED_BY_DESCRIPTIVE_RATES",
                 "capture": "NOT_ESTABLISHED_BY_SYNTHETIC_FILLS",
                 "promotion": "DO_NOT_PROMOTE"},
        "summary": summary,
        "descriptive_verdict": observed,
        "comparison_limit": "Matched controls, null permutations and true fill economics are declared but NOT executed.",
        "no_trading": True
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synthetic research preregistration and cashflow audit")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--allow-fixture", action="store_true")
    args = parser.parse_args()
    try:
        if not args.allow_fixture:
            raise ValueError("must explicitly pass --allow-fixture")
        print(json.dumps(audit(json.loads(args.input.read_text(encoding="utf-8"))),
                         ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc), "no_trading": True}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
