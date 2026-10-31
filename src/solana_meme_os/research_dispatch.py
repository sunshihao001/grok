"""Research-only, bounded triage of existing M2 observatory output.

Two loops are separate:
  Fast loop: deterministic event aggregation (existing M2, external input).
  Slow loop: a *plan* for source checks and specialist knowledge (this module).
This neither runs agents nor fetches RPC, publishes alerts or trades.

Input: JSON emitted by solana_meme_os.market_observatory.analyze.
Usage:
  PYTHONPATH=src python -m solana_meme_os.research_dispatch \
      --input .runtime/m2-observatory.json --max-cases 4 \
      --max-source-checks 12 --max-per-case 4
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

from .expert_router import route


SUPPORTED = {
    "SAME_SLOT_MULTIWALLET_BUY",
    "FUNDING_FANOUT",
    "TOKEN_CONSOLIDATION",
    "FUNDING_TO_BUY_CANDIDATE",
    "CROSS_MINT_FUNDING_REUSE",
    "CROSS_MINT_WALLET_ACTIVITY",
}
# These are *research-workload* priorities, NOT anomaly/risk/profit scores.
PRIORITY = {
    "FUNDING_TO_BUY_CANDIDATE": 1,
    "TOKEN_CONSOLIDATION": 1,
    "CROSS_MINT_FUNDING_REUSE": 1,
    "FUNDING_FANOUT": 2,
    "SAME_SLOT_MULTIWALLET_BUY": 2,
    "CROSS_MINT_WALLET_ACTIVITY": 3,
}
FAMILY = {
    "SAME_SLOT_MULTIWALLET_BUY": "MINT",
    "TOKEN_CONSOLIDATION": "MINT",
    "FUNDING_TO_BUY_CANDIDATE": "MINT",
    "FUNDING_FANOUT": "SOURCE",
    "CROSS_MINT_FUNDING_REUSE": "SOURCE",
    "CROSS_MINT_WALLET_ACTIVITY": "WALLET",
}


def _positive_int(value: object, name: str, *, allow_zero: bool = False) -> int:
    if type(value) is not int or value < (0 if allow_zero else 1):
        raise ValueError(f"{name} must be a nonnegative integer" if allow_zero
                         else f"{name} must be a positive integer")
    return value


def _scope(kind: str, row: dict) -> str:
    """Preserve each observed episode; do NOT coalesce a Mint's entire history.

    M2's cross-mint and funding-to-buy candidates are already cohort-wide
    aggregates, with no event window; label that explicitly rather than
    inventing an episode time.
    """
    if kind in {"SAME_SLOT_MULTIWALLET_BUY", "TOKEN_CONSOLIDATION",
                "FUNDING_TO_BUY_CANDIDATE"}:
        mint = row.get("mint")
        if not isinstance(mint, str) or not mint:
            raise ValueError(f"{kind} requires explicit mint")
        if kind == "SAME_SLOT_MULTIWALLET_BUY":
            slot = row.get("slot")
            if type(slot) is not int or slot < 0:
                raise ValueError("same-slot buy candidate requires slot")
            return f"MINT:{mint}:BUY_SLOT:{slot}"
        if kind == "TOKEN_CONSOLIDATION":
            window, recipient = row.get("start"), row.get("recipient")
            if not all(isinstance(v, str) and v for v in (window, recipient)):
                raise ValueError("token consolidation requires window and recipient")
            return f"MINT:{mint}:TOKEN_TO:{recipient}:WINDOW:{window}"
        funder = row.get("candidate_funder")
        if not isinstance(funder, str) or not funder:
            raise ValueError("funding-to-buy requires candidate_funder")
        return f"MINT:{mint}:SOURCE:{funder}:COHORT_AGGREGATE"
    if kind in {"FUNDING_FANOUT", "CROSS_MINT_FUNDING_REUSE"}:
        src = row.get("funder", row.get("candidate_funder"))
        if not isinstance(src, str) or not src:
            raise ValueError(f"{kind} requires source address")
        if kind == "FUNDING_FANOUT":
            window = row.get("start")
            if not isinstance(window, str) or not window:
                raise ValueError("funding fanout requires window start")
            return f"SOURCE:{src}:FANOUT_WINDOW:{window}"
        return f"SOURCE:{src}:CROSS_MINT_AGGREGATE"
    if kind == "CROSS_MINT_WALLET_ACTIVITY":
        wallet = row.get("wallet")
        if not isinstance(wallet, str) or not wallet:
            raise ValueError("cross-mint wallet activity requires wallet")
        return "WALLET:" + wallet + ":CROSS_MINT_AGGREGATE"
    # Unrecognized events are NOT silently mapped to an existing schema.
    anchor = row.get("mint") or row.get("funder") or row.get("wallet")
    if anchor is not None and (not isinstance(anchor, str) or not anchor):
        raise ValueError("unknown candidate anchor must be nonempty string")
    return "UNMAPPED:" + (anchor or "GENERAL") + ":TYPE:" + kind


def _candidate_id(scope: str, kinds: list[str], signatures: list[str]) -> str:
    canonical = json.dumps([scope, kinds, signatures], ensure_ascii=False,
                           separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()[:20]


def make_plan(report: dict, *, max_cases: int = 4,
              max_source_checks: int = 12, max_per_case: int = 4,
              expert_map: dict | None = None) -> dict:
    """Bounded and idempotent planning. No calls to network, LLM, or transactions."""
    for key, val in (("max_cases", max_cases),
                     ("max_source_checks", max_source_checks),
                     ("max_per_case", max_per_case)):
        _positive_int(val, key)
    if not isinstance(report, dict) or report.get("schema_version") != "0.1":
        raise ValueError("expected M2 schema 0.1")
    if report.get("result_type") != "MULTI_WALLET_EVENT_OBSERVATORY":
        raise ValueError("only M2 observatory output accepted")
    if report.get("no_trading") is not True:
        raise ValueError("M2 input must expressly forbid trading")
    if report.get("coverage_status") != "INPUT_COHORT_ONLY_NO_CHAIN_WIDE_COMPLETENESS_CLAIM":
        raise ValueError("unsupported/overstated market coverage")
    info = report.get("input_status")
    if not isinstance(info, dict):
        raise ValueError("M2 input_status missing")
    mode = info.get("input_mode")
    if mode not in {"fixture", "source_derived", "rpc_supplied"}:
        raise ValueError("unknown M2 input mode")
    asof = info.get("decision_time_filter")
    # No decision-time proof? Never infer that any downstream predictive
    # experiment has a valid signal arrival time.
    if asof is not None and not isinstance(asof, str):
        raise ValueError("invalid decision-time field")
    rows = report.get("group_candidates")
    if not isinstance(rows, list):
        raise ValueError("M2 group_candidates must be a list")
    bucket: dict[str, dict] = defaultdict(
        lambda: {"kinds": set(), "signatures": set(), "rows": 0, "unknown": False})
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("candidate is not a mapping")
        kind = row.get("kind")
        if not isinstance(kind, str) or not kind:
            raise ValueError("candidate missing kind")
        signatures = row.get("signatures", [])
        if not isinstance(signatures, list) or any(
                not isinstance(s, str) or not s.strip() for s in signatures):
            raise ValueError("candidate signatures must be strings")
        scope = _scope(kind, row)
        b = bucket[scope]
        b["kinds"].add(kind)
        b["signatures"].update(signatures)
        b["rows"] += 1
        b["unknown"] |= kind not in SUPPORTED
    grouped = []
    for scope, b in bucket.items():
        kinds = sorted(b["kinds"])
        sigs = sorted(b["signatures"])
        # Unrecognized mechanisms merit separate discovery review. But that
        # flag is not a claim that they are statistically anomalous.
        level = 0 if b["unknown"] else min(PRIORITY[k] for k in kinds)
        grouped.append((level, scope, kinds, sigs, b))
    grouped.sort(key=lambda t: (t[0], t[1]))
    accepted = grouped[:max_cases]
    remaining_checks = max_source_checks
    already_proposed: set[str] = set()
    tasks = []
    for level, scope, kinds, signatures, evidence in accepted:
        route_out = route(kinds, question="Explain structure and rule out ordinary mechanisms",
                          mapping=expert_map)
        # Signature verification is re-used across cases. Do not charge the
        # same raw transaction against two independent research tasks.
        reused = [sig for sig in signatures if sig in already_proposed]
        fresh = [sig for sig in signatures if sig not in already_proposed]
        n = min(max_per_case, remaining_checks, len(fresh))
        checked = fresh[:n]
        already_proposed.update(checked)
        remaining_checks -= n
        status = ("OFFLINE_SYNTHETIC_ONLY" if mode == "fixture" else
                  "SOURCE_CONFIRMATION_REQUIRED")
        if not signatures:
            status = "MISSING_SIGNATURES_REQUIRE_SOURCE_REPAIR"
        tasks.append({
            "case_id": _candidate_id(scope, kinds, signatures),
            "scope": scope,
            "research_priority": level,
            "priority_not_a_market_risk_score": True,
            "event_types": kinds,
            "candidate_records_in_input": evidence["rows"],
            "unique_signatures_in_input": len(signatures),
            "verification_status": status,
            "source_checks_proposed": checked,
            "reusable_prior_case_signature_checks": reused,
            "unselected_signatures": len(signatures) - n - len(reused),
            "research_role_ids": route_out["primary_experts"],
            "independent_review_roles": route_out["independent_challengers"],
            "optional_role_ids": route_out["conditional_experts"],
            "source_index_ids_to_consult": route_out["source_index_ids_to_read"],
            "source_card_ids_to_consult": route_out["source_card_ids_to_read"],
            "typed_handoff_ids": [
                v["id"] for v in route_out["typed_expert_handoffs"]["active_handoffs"]],
            "open_discovery": evidence["unknown"] or
                              route_out["status"] == "OPEN_DISCOVERY_REQUIRED",
            "research_questions": route_out["scenario_research_questions"],
            "claim_retractions_supported": "PLAN_ONLY_NO_PERSISTENT_CLAIM_STORE",
            "no_economic_owner_or_anomaly_conclusion": True,
        })
    return {
        "schema_version": "0.1", "result_type": "BOUNDED_RESEARCH_DISPATCH_PLAN",
        "operating_model": "DETERMINISTIC_FAST_LOOP_PLUS_SELECTIVE_SLOW_RESEARCH",
        "mode": mode, "decision_time_filter": asof,
        "time_safe_prediction_qualified": False,
        "marketwide_coverage_confirmed": False,
        "case_count_available": len(grouped),
        "case_count_scheduled_for_readonly_research": len(tasks),
        "case_count_deferred": len(grouped) - len(tasks),
        "total_signature_checks_budget": max_source_checks,
        "signature_checks_planned": max_source_checks - remaining_checks,
        "budget_unspent": remaining_checks,
        "cases": tasks,
        "publication_status": "NOT_PUBLISHED",
        "agent_execution_status": "NOT_RUN",
        "source_rpc_execution_status": "NOT_RUN",
        "baseline_calibrated": False, "no_trading": True,
        "limitations": [
            "One M2 source cohort is not whole-chain coverage",
            "Source/funder scopes are never auto-merged with a Mint",
            "Source-derived or rpc-supplied records require instruction verification",
            "Research priority reflects workload, not manipulation or forecast confidence",
            "No real agent handoff, persistent queue, watcher, market alert, or order is executed",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True, help="M2 output JSON path")
    p.add_argument("--output", type=Path)
    p.add_argument("--max-cases", type=int, default=4)
    p.add_argument("--max-source-checks", type=int, default=12)
    p.add_argument("--max-per-case", type=int, default=4)
    args = p.parse_args()
    with args.input.open(encoding="utf-8") as fh:
        report = json.load(fh)
    payload = json.dumps(make_plan(
        report, max_cases=args.max_cases,
        max_source_checks=args.max_source_checks,
        max_per_case=args.max_per_case), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
