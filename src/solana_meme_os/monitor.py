"""Read-only, deterministic observation monitor. Never executes transactions."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

from .knowledge import contextualize

ADDRESS = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
METRICS = {"liquidity_usd", "top10_holder_pct"}


def timestamp(raw: str) -> datetime:
    if not isinstance(raw, str):
        raise ValueError("observed_at must be ISO-8601")
    t = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError("observed_at requires timezone")
    return t.astimezone(timezone.utc)


def validate(observation: dict, rules: dict, now: datetime, allow_fixture: bool) -> tuple[str, str]:
    if observation.get("schema_version") != "1.0" or observation.get("chain") != "sol":
        raise ValueError("unsupported schema_version or chain")
    addr = observation.get("token_address", "")
    if not isinstance(addr, str) or not ADDRESS.fullmatch(addr):
        raise ValueError("invalid Solana token_address")
    mode = observation.get("mode")
    if mode not in {"live", "fixture"}:
        raise ValueError("mode must be live or fixture")
    if mode == "fixture" and not allow_fixture:
        raise ValueError("fixture input requires --allow-fixture")
    source = observation.get("source")
    if not isinstance(source, dict) or not source.get("ref") or not source.get("tool"):
        raise ValueError("source.tool and source.ref are required")
    metrics = observation.get("metrics")
    if not isinstance(metrics, dict) or set(metrics) - METRICS:
        raise ValueError("metrics must be a mapping with known metric keys")
    for key, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value < float("inf"):
            raise ValueError(f"invalid numeric metric: {key}")
        if key == "top10_holder_pct" and value > 100:
            raise ValueError("top10_holder_pct must be between 0 and 100")
    events = observation.get("events", [])
    if not isinstance(events, list) or any(not isinstance(e, dict) or not e.get("id") or not e.get("kind") or not e.get("source_ref") for e in events):
        raise ValueError("events require id, kind, source_ref")
    if len(events) > 1000 or len({e["id"] for e in events}) != len(events):
        raise ValueError("too many or duplicate event IDs")
    observed = timestamp(observation.get("observed_at"))
    if mode == "live":
        lag = (now - observed).total_seconds()
        if lag > rules["max_age_minutes"] * 60 or lag < -300:
            raise ValueError("live observation is stale or from the future")
    return addr, mode


def process(observation: dict, rules: dict, state_dir: Path, now: datetime | None = None, allow_fixture: bool = False) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    addr, mode = validate(observation, rules, now, allow_fixture)
    state_dir.mkdir(parents=True, exist_ok=True)
    state_file = state_dir / f"{addr}.json"
    previous = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else None
    result: dict[str, Any] = {"status": "FIXTURE" if mode == "fixture" else "OBSERVED", "token_address": addr,
              "observed_at": observation["observed_at"], "rule_version": rules["version"],
              "rule_status": rules["status"], "alerts": [], "missing_fields": sorted(METRICS - set(observation["metrics"])),
              "source": observation["source"], "no_trading": True}
    if previous:
        if previous.get("mode") != mode:
            raise ValueError("fixture and live observations cannot share a state directory for the same mint")
        old_time = timestamp(previous["observed_at"])
        new_time = timestamp(observation["observed_at"])
        if new_time <= old_time:
            result["status"] = "IGNORED_NON_NEWER"
            result["knowledge_context"] = contextualize(result)
            return result
        old = previous["metrics"]
        cur = observation["metrics"]
        if old.get("liquidity_usd", 0) > 0 and "liquidity_usd" in cur:
            fraction = (old["liquidity_usd"] - cur["liquidity_usd"]) / old["liquidity_usd"]
            if fraction >= rules["liquidity_drop_fraction"]:
                result["alerts"].append({"type": "LIQUIDITY_DROP", "from": old["liquidity_usd"],
                         "to": cur["liquidity_usd"], "fraction": round(fraction, 6), "interpretation": "observation_only"})
        if "top10_holder_pct" in old and "top10_holder_pct" in cur:
            change = cur["top10_holder_pct"] - old["top10_holder_pct"]
            if change >= rules["top10_holder_rise_pp"]:
                result["alerts"].append({"type": "TOP10_SHARE_RISE", "from": old["top10_holder_pct"],
                         "to": cur["top10_holder_pct"], "percentage_points": round(change, 6), "interpretation": "observation_only"})
    seen = set(previous.get("seen_events", [])) if previous else set()
    for event in observation.get("events", []):
        if event["id"] not in seen:
            result["alerts"].append({"type": "NEW_SOURCE_EVENT", "event_id": event["id"],
                       "kind": event["kind"], "source_ref": event["source_ref"], "interpretation": "unverified_observation"})
            seen.add(event["id"])
    result["knowledge_context"] = contextualize(result)
    next_state = {"observed_at": observation["observed_at"], "metrics": observation["metrics"],
                  "seen_events": sorted(seen)[-1000:], "source": observation["source"], "mode": mode}
    # Source-linked domain knowledge is attached as competing questions, not automatic conclusions.
    from .knowledge import for_observation
    result["knowledge"] = for_observation(result)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=state_dir, prefix=".tmp-", delete=False) as fh:
        tmp = Path(fh.name)
        json.dump(next_state, fh, ensure_ascii=False, indent=2)
    try:
        os.replace(tmp, state_file)
    finally:
        tmp.unlink(missing_ok=True)
    with (state_dir / "runs.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(result, ensure_ascii=False) + "\n")
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="Read-only Solana Meme observation monitor")
    p.add_argument("--input", required=True, type=Path, help="Normalized observation JSON")
    p.add_argument("--rules", type=Path, default=Path("rules/monitor.v0.json"))
    p.add_argument("--state-dir", type=Path, default=Path(".runtime"))
    p.add_argument("--allow-fixture", action="store_true", help="Permit fixture data, never label it live")
    args = p.parse_args()
    try:
        observation = json.loads(args.input.read_text(encoding="utf-8"))
        rules = json.loads(args.rules.read_text(encoding="utf-8"))
        if rules.get("status") != "experimental":
            raise ValueError("unexpected rule status; review before use")
        print(json.dumps(process(observation, rules, args.state_dir, allow_fixture=args.allow_fixture), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "ERROR", "error": str(e), "no_trading": True}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
