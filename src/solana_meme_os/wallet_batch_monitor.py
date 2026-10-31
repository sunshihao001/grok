"""M01 offline wallet-batch research prototype; normalized fixtures only, no RPC or trading.

Inputs are economic-action records, NOT raw Solana CPI/token balance deltas. The
upstream decoder is responsible for wallet authority resolution and swap deduping.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

ADDRESS = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
KINDS = {"BUY", "SELL", "TRANSFER"}
STATUSES = {"SUCCESS", "FAILED", "UNRESOLVED"}
WINDOW_MINUTES = (1, 5, 15)
MAX_EVENTS = 100_000


def parse_time(value: Any) -> datetime:
    if not isinstance(value, str):
        raise ValueError("timestamp must be ISO-8601 with timezone")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid ISO-8601 timestamp") from exc
    if dt.tzinfo is None:
        raise ValueError("timestamp must include timezone")
    return dt.astimezone(timezone.utc)


def iso(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def address(value: Any, field: str) -> str:
    if not isinstance(value, str) or not ADDRESS.fullmatch(value):
        raise ValueError(f"{field} must be a Solana base58 address (32-44 chars)")
    return value


def raw_int(value: Any, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")
    return value


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("schema_version") != "m01.v1":
        raise ValueError("schema_version must be m01.v1")
    if payload.get("chain") != "sol" or payload.get("mode") != "fixture":
        raise ValueError("M01 accepts only sol / fixture; no live collector")
    mint = address(payload.get("mint"), "mint")
    quote_mint = address(payload.get("quote_mint"), "quote_mint")
    decimals = payload.get("quote_decimals")
    if type(decimals) is not int or not 0 <= decimals <= 18:
        raise ValueError("quote_decimals must be 0..18")
    src = payload.get("source")
    if not isinstance(src, dict) or not all(isinstance(src.get(k), str) and src[k] for k in ("tool", "ref")):
        raise ValueError("source.tool and source.ref required")
    coverage = payload.get("coverage")
    if not isinstance(coverage, dict) or type(coverage.get("complete")) is not bool:
        raise ValueError("coverage.complete must be boolean")
    start, end = parse_time(coverage.get("start")), parse_time(coverage.get("end"))
    as_of = parse_time(payload.get("as_of"))
    if end <= start or (end - start) > timedelta(days=3):
        raise ValueError("invalid coverage range (max 3 days)")
    if as_of < end:
        raise ValueError("as_of must be at/after coverage end (complete windows only)")
    if any((t.minute % 15, t.second, t.microsecond) != (0, 0, 0) for t in (start, end)):
        raise ValueError("coverage boundaries must align to 15-minute windows")
    raw_gaps = coverage.get("gaps", [])
    if not isinstance(raw_gaps, list):
        raise ValueError("coverage.gaps must be a list")
    gaps = []
    for gap in raw_gaps:
        if not isinstance(gap, dict):
            raise ValueError("invalid coverage gap")
        a, b = parse_time(gap.get("start")), parse_time(gap.get("end"))
        if not start <= a < b <= end:
            raise ValueError("coverage gap outside window")
        gaps.append((a, b))
    gaps.sort()
    if any(gaps[i][1] > gaps[i + 1][0] for i in range(len(gaps) - 1)):
        raise ValueError("overlapping coverage gaps")
    events = payload.get("events")
    if not isinstance(events, list) or len(events) > MAX_EVENTS:
        raise ValueError("events must be a list of at most 100000 records")
    unique: dict[str, dict[str, Any]] = {}
    ignored_duplicates = 0
    for e in events:
        if not isinstance(e, dict):
            raise ValueError("event must be an object")
        for field in ("event_id", "signature", "source_ref"):
            if not isinstance(e.get(field), str) or not e[field].strip():
                raise ValueError(f"missing {field}")
        if type(e.get("slot")) is not int or e["slot"] < 0:
            raise ValueError("slot must be nonnegative integer")
        when, available = parse_time(e.get("event_time")), parse_time(e.get("available_at"))
        if not start <= when < end or available < when:
            raise ValueError("event outside coverage or available before occurrence")
        kind, status = e.get("kind"), e.get("tx_status")
        if kind not in KINDS or status not in STATUSES:
            raise ValueError("unrecognized kind or tx_status")
        if status == "SUCCESS":
            address(e.get("wallet_owner"), "wallet_owner")
            if kind in {"BUY", "SELL"}:
                if raw_int(e.get("quote_amount_raw"), "quote_amount_raw") <= 0:
                    raise ValueError("successful swap requires positive quote_amount_raw")
                if e.get("quote_mint") != quote_mint:
                    raise ValueError("quote mint mismatch; cannot mix assets")
            elif e.get("quote_amount_raw", 0) != 0:
                raise ValueError("TRANSFER cannot carry swap quote notional")
        if "token_account" in e:
            address(e["token_account"], "token_account")
        if e["event_id"] in unique:
            if unique[e["event_id"]] != e:
                raise ValueError("duplicate event_id with conflicting evidence")
            ignored_duplicates += 1
        else:
            unique[e["event_id"]] = e
    # Same Token Account owner must not silently change inside this fixture.
    owners: dict[str, str] = {}
    for e in unique.values():
        if e["tx_status"] == "SUCCESS" and e.get("token_account"):
            account = e["token_account"]
            if account in owners and owners[account] != e["wallet_owner"]:
                raise ValueError("token_account owner conflict; authority change unsupported")
            owners[account] = e["wallet_owner"]
    return {"mint": mint, "quote_mint": quote_mint, "quote_decimals": decimals,
            "start": start, "end": end, "as_of": as_of, "gaps": gaps,
            "complete": coverage["complete"], "source": src,
            "events": list(unique.values()), "duplicates": ignored_duplicates}


def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    data = validate(payload)
    result: dict[str, Any] = {
        "schema_version": "m01.result.v1", "status": "FIXTURE_RESEARCH_ONLY",
        "mint": data["mint"], "quote_mint": data["quote_mint"],
        "quote_decimals": data["quote_decimals"], "source": data["source"],
        "as_of": iso(data["as_of"]), "no_trading": True,
        "provenance": "normalized_fixture_not_raw_rpc",
        "ignored_duplicate_events": data["duplicates"], "timeframes": {}
    }
    # One owner counts once per window, no matter how many token accounts/actions.
    for minutes in WINDOW_MINUTES:
        duration = timedelta(minutes=minutes)
        slots = []
        by_bucket: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for event in data["events"]:
            index = int((parse_time(event["event_time"]) - data["start"]).total_seconds() // (minutes * 60))
            by_bucket[index].append(event)
        t = data["start"]
        index = 0
        while t < data["end"]:
            wend = t + duration
            w_events = by_bucket.get(index, [])
            unknown = (not data["complete"] or
                       any(g0 < wend and g1 > t for g0, g1 in data["gaps"]) or
                       any(e["tx_status"] == "UNRESOLVED" or
                           parse_time(e["available_at"]) > data["as_of"] for e in w_events))
            successful = [e for e in w_events if e["tx_status"] == "SUCCESS" and
                          parse_time(e["available_at"]) <= data["as_of"]]
            actors = {e["wallet_owner"] for e in successful}
            buys = {e["wallet_owner"] for e in successful if e["kind"] == "BUY"}
            sells = {e["wallet_owner"] for e in successful if e["kind"] == "SELL"}
            raw_buy = sum(e["quote_amount_raw"] for e in successful if e["kind"] == "BUY")
            raw_sell = sum(e["quote_amount_raw"] for e in successful if e["kind"] == "SELL")
            slots.append({
                "start": iso(t), "end": iso(wend),
                "data_status": "INCOMPLETE" if unknown else "COMPLETE",
                "active_wallet_count": len(actors) if not unknown else None,
                "buy_wallet_count": len(buys) if not unknown else None,
                "sell_wallet_count": len(sells) if not unknown else None,
                "buy_quote_raw": raw_buy if not unknown else None,
                "sell_quote_raw": raw_sell if not unknown else None,
                "failed_event_count": sum(e["tx_status"] == "FAILED" for e in w_events),
                "source_refs": sorted({e["source_ref"] for e in w_events})[:30],
                "_actors": actors if not unknown else None,
            })
            t = wend
            index += 1
        seen: set[str] = set()
        comparisons, candidates = [], []
        for i, slot in enumerate(slots):
            actors = slot.pop("_actors")
            if actors is None:
                slot["first_observed_count"] = None
                slot["returning_count"] = None
                continue
            slot["first_observed_count"] = len(actors - seen)
            # Returning excludes direct prior-window retention.
            previous_actors = slots[i - 1].get("_saved_actors") if i else set()
            slot["returning_count"] = len((actors & seen) - (previous_actors or set())) if i else 0
            slot["_saved_actors"] = actors
            seen |= actors
            if i == 0 or slots[i - 1]["data_status"] != "COMPLETE":
                continue
            old = slots[i - 1]
            old_actors = old["_saved_actors"]
            retained = old_actors & actors
            entered, exited = actors - old_actors, old_actors - actors
            delta = {
                "previous_start": old["start"], "current_start": slot["start"],
                "retained_count": len(retained), "entered_count": len(entered),
                "inactive_count": len(exited),
                "entry_share": round(len(entered) / len(actors), 6) if actors else None,
                "retention_share": round(len(retained) / len(old_actors), 6) if old_actors else None,
                "jaccard": round(len(retained) / len(actors | old_actors), 6)
                           if actors or old_actors else None,
            }
            comparisons.append(delta)
            flags = []
            if slot["buy_wallet_count"] > old["buy_wallet_count"] and slot["buy_quote_raw"] < old["buy_quote_raw"]:
                flags.append("BUYERS_UP_QUOTE_VOLUME_DOWN")
            if len(old_actors) == len(actors) and len(old_actors) >= 2 and not retained:
                flags.append("SAME_COUNT_FULL_MEMBER_REPLACEMENT")
            if (not actors and len(old_actors) >= 3 and i >= 2
                    and slots[i - 2]["data_status"] == "COMPLETE"
                    and slots[i - 2]["active_wallet_count"] >= 3):
                flags.append("SUSTAINED_ACTIVITY_THEN_STOPPED")
            if flags:
                candidates.append({
                    "window_start": slot["start"], "types": flags,
                    "comparison": delta,
                    "before": {k: old[k] for k in ("active_wallet_count", "buy_wallet_count", "buy_quote_raw")},
                    "after": {k: slot[k] for k in ("active_wallet_count", "buy_wallet_count", "buy_quote_raw")},
                    "source_refs": sorted(set(old["source_refs"] + slot["source_refs"])),
                    "interpretation": "descriptive_candidate_not_actor_identity_or_trade_signal",
                })
        for slot in slots:
            slot.pop("_saved_actors", None)
        result["timeframes"][str(minutes) + "m"] = {
            "windows": slots, "comparisons": comparisons, "candidates": candidates,
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline fixture-only wallet batch research; no RPC, no trading")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path, help="Optional report JSON path")
    args = parser.parse_args()
    try:
        report = analyze(json.loads(args.input.read_text(encoding="utf-8")))
        encoded = json.dumps(report, indent=2, ensure_ascii=False)
        if args.output:
            args.output.write_text(encoded + "\n", encoding="utf-8")
        print(encoded)
        return 0
    except (ValueError, TypeError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc), "no_trading": True}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())