"""Read-only M2 event/window observatory. Input is normalized, source-linked events.

This module DOES NOT fetch live chain data, prove Jito bundles, infer beneficial
ownership, calibrate abnormality, or evaluate trades. It is a deterministic
aggregation and candidate-graph layer over supplied records.

Usage:
  PYTHONPATH=src python -m solana_meme_os.market_observatory \\
      --input fixtures/market-observatory-synthetic.json --allow-fixture
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import json
from pathlib import Path
import re
import sys

KINDS = frozenset({"SOL_TRANSFER", "TOKEN_TRANSFER", "SWAP_BUY", "SWAP_SELL"})
TOKEN_KINDS = frozenset({"TOKEN_TRANSFER", "SWAP_BUY", "SWAP_SELL"})
TRANSFER_KINDS = frozenset({"SOL_TRANSFER", "TOKEN_TRANSFER"})
BASE = datetime(1970, 1, 1, tzinfo=timezone.utc)
RAW_INT = re.compile(r"^(0|[1-9][0-9]*)$")


def parse_time(value: object, field: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field} requires timezone-aware ISO-8601")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field} invalid ISO-8601") from exc
    if dt.tzinfo is None:
        raise ValueError(f"{field} requires timezone")
    return dt.astimezone(timezone.utc)


def required_string(row: dict, key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"missing {key}")
    return value


def raw_units(row: dict, key: str) -> int:
    value = row.get(key)
    if not isinstance(value, str) or not RAW_INT.fullmatch(value):
        raise ValueError(f"{key}: expected nonnegative integer string (raw units)")
    return int(value)


def iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def sol(lamports: int) -> str:
    return format(Decimal(lamports) / Decimal(10**9), "f")


def token(raw: int, decimals: int) -> str:
    return format(Decimal(raw) / Decimal(10**decimals), "f")


def _identity(row: dict) -> tuple:
    return row["signature"], row["instruction_index"], row.get("inner_instruction_index")


def _window_start(dt: datetime, seconds: int) -> datetime:
    timestamp = int((dt - BASE).total_seconds())
    return BASE + timedelta(seconds=(timestamp // seconds) * seconds)


def validate_and_deduplicate(doc: dict, *, allow_fixture: bool = False,
                             decision_at: str | None = None) -> tuple[list[dict], dict]:
    if not isinstance(doc, dict) or doc.get("schema_version") != "0.1" or doc.get("chain") != "sol":
        raise ValueError("expected schema_version 0.1 and chain sol")
    mode = doc.get("mode")
    if mode not in {"fixture", "source_derived", "rpc_supplied"}:
        raise ValueError("mode must be fixture/source_derived/rpc_supplied")
    if mode == "fixture" and not allow_fixture:
        raise ValueError("fixture requires --allow-fixture")
    rows = doc.get("events")
    if not isinstance(rows, list) or len(rows) > 100000:
        raise ValueError("events must be a list of at most 100000 normalized records")
    decision = parse_time(decision_at, "decision_at") if decision_at else None
    saved: dict[tuple, dict] = {}
    sources: dict[tuple, set[str]] = defaultdict(set)
    excluded = {"unknown_availability": 0, "post_decision": 0}
    mint_decimals: dict[str, int] = {}

    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("every event must be a mapping")
        kind = row.get("event_kind")
        if kind not in KINDS:
            raise ValueError("unknown event_kind; no unverified sell/transfer coercion")
        sig = required_string(row, "signature")
        source = required_string(row, "source_ref")
        slot = row.get("slot")
        if type(slot) is not int or slot < 0:
            raise ValueError("slot must be nonnegative integer")
        txidx = row.get("transaction_index")
        if txidx is not None and (type(txidx) is not int or txidx < 0):
            raise ValueError("transaction_index must be nonnegative integer")
        idx = row.get("instruction_index")
        inner = row.get("inner_instruction_index")
        if type(idx) is not int or idx < 0 or (inner is not None and (type(inner) is not int or inner < 0)):
            raise ValueError("instruction_index/inner_instruction_index invalid")
        dt = parse_time(row.get("block_time"), "block_time")
        available = parse_time(row["available_at"], "available_at") if row.get("available_at") else None
        received = parse_time(row["received_at"], "received_at") if row.get("received_at") else None
        if kind in TRANSFER_KINDS:
            required_string(row, "from_owner")
            required_string(row, "to_owner")
            raw_units(row, "amount_raw")
        if kind in TOKEN_KINDS:
            mint = required_string(row, "mint")
            decimals = row.get("decimals")
            if type(decimals) is not int or not 0 <= decimals <= 18:
                raise ValueError("token decimals must be 0..18")
            if mint in mint_decimals and mint_decimals[mint] != decimals:
                raise ValueError(f"inconsistent token decimals for {mint}")
            mint_decimals[mint] = decimals
            if kind == "TOKEN_TRANSFER":
                raw_units(row, "amount_raw")
            else:
                required_string(row, "wallet")
                raw_units(row, "sol_amount_lamports")
                raw_units(row, "token_amount_raw")
        else:
            if row.get("mint") is not None:
                raise ValueError("SOL_TRANSFER must not assert a mint association")
        if available is not None and received is not None and received < available:
            raise ValueError("received_at cannot precede available_at")
        if decision:
            if available is None or received is None:
                excluded["unknown_availability"] += 1
                continue
            if available > decision or received > decision or dt > decision:
                excluded["post_decision"] += 1
                continue
        key = (sig, idx, inner)
        comparable = {k: v for k, v in row.items()
                      if k not in {"source_ref", "available_at", "received_at"}}
        if key in saved:
            if {k: v for k, v in saved[key].items()
                if k not in {"source_ref", "available_at", "received_at"}} != comparable:
                raise ValueError(f"conflicting event identity across sources: {key}")
        else:
            saved[key] = dict(row)
        sources[key].add(source)
    clean = sorted(saved.values(), key=lambda r: (
        parse_time(r["block_time"], "block_time"), r["slot"], r["signature"],
        r["instruction_index"], r.get("inner_instruction_index", -1)
        if r.get("inner_instruction_index") is not None else -1))
    for r in clean:
        r["source_refs"] = sorted(sources[_identity(r)])
    return clean, {"input_events": len(rows), "unique_events": len(clean),
                   "duplicate_records": len(rows)-sum(excluded.values())-len(clean),
                   "decision_time_filter": iso(decision) if decision else None,
                   "excluded": excluded, "input_mode": mode}


def summarize(rows: list[dict], window_seconds: int) -> list[dict]:
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for e in rows:
        dt = parse_time(e["block_time"], "block_time")
        bucket = _window_start(dt, window_seconds)
        buckets[("INPUT_COHORT_ALL_MINTS", bucket)].append(e)
        if e["event_kind"] in TOKEN_KINDS:
            buckets[(e["mint"], bucket)].append(e)
    out = []
    for (scope, start), ev in sorted(buckets.items(), key=lambda item: (item[0][1], item[0][0])):
        kinds: dict[str, int] = defaultdict(int)
        actors = set()
        traders = set()
        senders, receivers = set(), set()
        sol_sent = sol_bought = sol_sold = 0
        token_transfers: dict[str, int] = defaultdict(int)
        decimals: dict[str, int] = {}
        sigs = set()
        for e in ev:
            kind = e["event_kind"]
            kinds[kind] += 1
            sigs.add(e["signature"])
            if kind in TRANSFER_KINDS:
                senders.add(e["from_owner"])
                receivers.add(e["to_owner"])
                actors.update((e["from_owner"], e["to_owner"]))
                if kind == "SOL_TRANSFER":
                    sol_sent += raw_units(e, "amount_raw")
                else:
                    token_transfers[e["mint"]] += raw_units(e, "amount_raw")
                    decimals[e["mint"]] = e["decimals"]
            else:
                actors.add(e["wallet"])
                traders.add(e["wallet"])
                if kind == "SWAP_BUY":
                    sol_bought += raw_units(e, "sol_amount_lamports")
                else:
                    sol_sold += raw_units(e, "sol_amount_lamports")
        out.append({"scope": scope, "window_seconds": window_seconds,
                    "start": iso(start), "end_exclusive": iso(start + timedelta(seconds=window_seconds)),
                    "event_count": len(ev), "transaction_count": len(sigs),
                    "unique_actor_addresses": len(actors), "unique_trade_wallets": len(traders),
                    "unique_senders": len(senders),
                    "unique_receivers": len(receivers), "event_kinds": dict(sorted(kinds.items())),
                    "sol_transferred": sol(sol_sent), "sol_spent_on_buys": sol(sol_bought),
                    "sol_received_from_sells": sol(sol_sold),
                    "token_transferred": {m: token(raw, decimals[m]) for m, raw in sorted(token_transfers.items())},
                    "signature_refs": sorted(sigs),
                    "anomaly_status": "UNASSESSED_NO_BASELINE", "economic_edge_verified": False})
    return out


def _sliding_windows(records: list[dict], seconds: int, participant: str) -> list[list[dict]]:
    """Emit candidate windows on distinct-participant expansions, including bucket boundaries.

    This is a descriptive rolling detector, not an anomaly threshold. In a
    sustained burst each newly observed distinct participant can emit an
    updated candidate; no market baseline has been fitted.
    """
    ordered = sorted(records, key=lambda e: (parse_time(e["block_time"], "block_time"),
                                            e["signature"], e["instruction_index"]))
    active: deque[dict] = deque()
    counts: Counter[str] = Counter()
    windows = []
    for e in ordered:
        now = parse_time(e["block_time"], "block_time")
        while active and now - parse_time(active[0]["block_time"], "block_time") >= timedelta(seconds=seconds):
            expired = active.popleft()
            counts[expired[participant]] -= 1
            if counts[expired[participant]] == 0:
                del counts[expired[participant]]
        previous = len(counts)
        active.append(e)
        counts[e[participant]] += 1
        if len(counts) >= 2 and len(counts) > previous:
            windows.append(list(active))
    return windows


def candidates(rows: list[dict], *, seconds: int = 60, funding_lookback: int = 300) -> list[dict]:
    """Candidates describe structures, NOT abnormality, same-owner, bundles or profit."""
    output = []
    # Same-slot buys; shared slots do not establish atomic Jito submission.
    by_slot: dict[tuple, list[dict]] = defaultdict(list)
    for e in rows:
        if e["event_kind"] == "SWAP_BUY":
            by_slot[(e["mint"], e["slot"])].append(e)
    for (mint, slot), ev in sorted(by_slot.items()):
        buyers = sorted({x["wallet"] for x in ev})
        if len(buyers) < 2:
            continue
        output.append({"kind": "SAME_SLOT_MULTIWALLET_BUY", "mint": mint, "slot": slot,
                       "wallets": buyers, "unique_wallets": len(buyers),
                       "transactions": len({x["signature"] for x in ev}),
                       "sol_spent": sol(sum(raw_units(x, "sol_amount_lamports") for x in ev)),
                       "signatures": sorted({x["signature"] for x in ev}),
                       "jito_bundle_status": "UNVERIFIED", "entity_link_status": "UNVERIFIED",
                       "anomaly_status": "UNASSESSED_NO_BASELINE"})
    # Source fanout: rolling-window receiver expansion, not clock-aligned bins.
    funding: dict[str, list[dict]] = defaultdict(list)
    for e in rows:
        if e["event_kind"] == "SOL_TRANSFER":
            funding[e["from_owner"]].append(e)
    for source, ev in sorted(funding.items()):
        for window in _sliding_windows(ev, seconds, "to_owner"):
            recipients = sorted({x["to_owner"] for x in window})
            start = parse_time(window[0]["block_time"], "block_time")
            output.append({"kind": "FUNDING_FANOUT", "funder": source, "start": iso(start),
                           "end_exclusive": iso(start + timedelta(seconds=seconds)),
                           "window_seconds": seconds, "recipient_wallets": recipients,
                           "unique_recipients": len(recipients),
                           "transfer_events": len(window),
                           "sol_transferred": sol(sum(raw_units(x, "amount_raw") for x in window)),
                           "signatures": sorted({x["signature"] for x in window}),
                           "shared_control_status": "UNVERIFIED",
                           "anomaly_status": "UNASSESSED_NO_BASELINE"})
    # Token routing: independently assess recipients per Mint, in rolling windows.
    consolidation: dict[tuple, list[dict]] = defaultdict(list)
    for e in rows:
        if e["event_kind"] == "TOKEN_TRANSFER":
            consolidation[(e["mint"], e["to_owner"])].append(e)
    for (mint, receiver), ev in sorted(consolidation.items()):
        for window in _sliding_windows(ev, seconds, "from_owner"):
            origins = sorted({x["from_owner"] for x in window})
            start = parse_time(window[0]["block_time"], "block_time")
            output.append({"kind": "TOKEN_CONSOLIDATION", "mint": mint,
                           "recipient": receiver, "start": iso(start),
                           "end_exclusive": iso(start + timedelta(seconds=seconds)),
                           "window_seconds": seconds, "origin_wallets": origins,
                           "unique_origins": len(origins), "transfer_events": len(window),
                           "token_transferred": token(sum(raw_units(x, "amount_raw") for x in window),
                                                      window[0]["decimals"]),
                           "signatures": sorted({x["signature"] for x in window}),
                           "subsequent_sale_status": "NOT_CHECKED",
                           "entity_link_status": "UNVERIFIED",
                           "anomaly_status": "UNASSESSED_NO_BASELINE"})
    # Look back from buy to funding of the buyer. More than one possible funder
    # is not silently collapsed into one presumed beneficial owner.
    credits: dict[str, list[dict]] = defaultdict(list)
    for e in rows:
        if e["event_kind"] == "SOL_TRANSFER":
            credits[e["to_owner"]].append(e)
    groups: dict[tuple, dict] = defaultdict(lambda: {"buyers": set(), "signatures": set(), "ambiguous_buyers": set()})
    for e in rows:
        if e["event_kind"] != "SWAP_BUY":
            continue
        when = parse_time(e["block_time"], "block_time")
        eligible = [x for x in credits[e["wallet"]] if
                    timedelta(0) <= when-parse_time(x["block_time"], "block_time") <= timedelta(seconds=funding_lookback)
                    and (x["slot"] < e["slot"] or
                         (x["slot"] == e["slot"] and
                          type(x.get("transaction_index")) is int and
                          type(e.get("transaction_index")) is int and
                          x["transaction_index"] < e["transaction_index"]))]
        funders = {x["from_owner"] for x in eligible}
        for funder in funders:
            k = (funder, e["mint"])
            groups[k]["buyers"].add(e["wallet"])
            groups[k]["signatures"].add(e["signature"])
            groups[k]["signatures"].update(x["signature"] for x in eligible if x["from_owner"] == funder)
            if len(funders) > 1:
                groups[k]["ambiguous_buyers"].add(e["wallet"])
    for (funder, mint), g in sorted(groups.items()):
        if len(g["buyers"]) < 2:
            continue
        output.append({"kind": "FUNDING_TO_BUY_CANDIDATE", "mint": mint,
                       "candidate_funder": funder, "buyer_wallets": sorted(g["buyers"]),
                       "unique_buyers": len(g["buyers"]), "funding_lookback_seconds": funding_lookback,
                       "buyers_with_multiple_funders": sorted(g["ambiguous_buyers"]),
                       "signatures": sorted(g["signatures"]),
                       "relationship": "TIME_BOUNDED_FLOW_HYPOTHESIS_NOT_OWNERSHIP",
                       "anomaly_status": "UNASSESSED_NO_BASELINE"})
    # Cross-Mint recurrence is descriptive. Repeated service-provider use is a
    # competing explanation, not automatic evidence of common beneficial owner.
    reuse: dict[str, dict] = defaultdict(lambda: {"mints": set(), "buyers": set(), "signatures": set()})
    for (funder, mint), group in groups.items():
        reuse[funder]["mints"].add(mint)
        reuse[funder]["buyers"].update(group["buyers"])
        reuse[funder]["signatures"].update(group["signatures"])
    for funder, group in sorted(reuse.items()):
        if len(group["mints"]) < 2:
            continue
        output.append({"kind": "CROSS_MINT_FUNDING_REUSE", "candidate_funder": funder,
                       "mints": sorted(group["mints"]), "unique_mints": len(group["mints"]),
                       "buyer_wallets": sorted(group["buyers"]),
                       "signatures": sorted(group["signatures"]),
                       "economic_owner_status": "UNVERIFIED",
                       "anomaly_status": "UNASSESSED_NO_BASELINE"})
    by_buyer: dict[str, set[str]] = defaultdict(set)
    for e in rows:
        if e["event_kind"] in {"SWAP_BUY", "SWAP_SELL"}:
            by_buyer[e["wallet"]].add(e["mint"])
    for buyer, mints in sorted(by_buyer.items()):
        if len(mints) > 1:
            output.append({"kind": "CROSS_MINT_WALLET_ACTIVITY", "wallet": buyer,
                           "mints": sorted(mints), "unique_mints": len(mints),
                           "role_status": "UNCLASSIFIED",
                           "anomaly_status": "UNASSESSED_NO_BASELINE"})
    return sorted(output, key=lambda c: (c["kind"], c.get("mint", ""), c.get("slot", -1),
                                         c.get("start", ""), c.get("funder", c.get("candidate_funder", ""))))


def analyze(doc: dict, *, allow_fixture: bool = False, decision_at: str | None = None,
            windows: tuple[int, ...] = (5, 30, 300)) -> dict:
    if not windows or len(windows) > 8 or any(type(x) is not int or not 1 <= x <= 86400 for x in windows):
        raise ValueError("windows must be 1..86400 seconds (at most eight)")
    events, meta = validate_and_deduplicate(doc, allow_fixture=allow_fixture,
                                             decision_at=decision_at)
    return {"schema_version": "0.1", "result_type": "MULTI_WALLET_EVENT_OBSERVATORY",
            "input_status": meta, "events": events,
            "window_aggregates": [agg for size in sorted(set(windows)) for agg in summarize(events, size)],
            "group_candidates": candidates(events),
            "normalized_event_count": len(events), "no_trading": True,
            "coverage_status": "INPUT_COHORT_ONLY_NO_CHAIN_WIDE_COMPLETENESS_CLAIM",
            "abnormality_confirmed": False, "ownership_confirmed": False,
            "jito_bundle_confirmed": False, "paper_trade_qualified": False,
            "limitations": ["Input records require external RPC/instruction verification",
                            "No representative normal-behavior baseline or null model",
                            "No real-time source ingestion, execution simulator or cloud deployment"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-fixture", action="store_true")
    parser.add_argument("--decision-at", help="ISO timestamp: drop data unavailable at decision time")
    parser.add_argument("--windows", type=int, nargs="+", default=[5, 30, 300])
    args = parser.parse_args()
    try:
        with args.input.open(encoding="utf-8") as fh:
            source = json.load(fh)
        result = analyze(source, allow_fixture=args.allow_fixture,
                         decision_at=args.decision_at, windows=tuple(args.windows))
        serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(serialized, encoding="utf-8")
        else:
            print(serialized, end="")
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc), "no_trading": True},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
