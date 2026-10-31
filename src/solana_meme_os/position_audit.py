"""Offline, read-only cross-table audit of published Solana Meme research data.

Checks source-table *windows*, not raw chain transaction authenticity or profit.
Run: PYTHONPATH=src python -m solana_meme_os.position_audit --buys data/v03_onchain.json --flows data/v07_exit.json --slots data/v04_slot_order.json
"""
from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path

TOL = Decimal("0.01")  # published tables round Token UI amounts to two decimals


def amount(value: object) -> Decimal:
    if isinstance(value, bool) or value is None:
        raise ValueError("missing/invalid token amount; never replace unknown with zero")
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid token amount") from exc
    if not d.is_finite() or d < 0:
        raise ValueError("negative or non-finite amount")
    return d


def records(doc: dict, name: str) -> dict[str, dict]:
    if not isinstance(doc, dict) or not isinstance(doc.get("lancements"), list):
        raise ValueError(f"{name}: missing lancements list")
    out = {}
    for row in doc["lancements"]:
        if not isinstance(row, dict) or not isinstance(row.get("mint"), str):
            raise ValueError(f"{name}: invalid mint")
        mint = row["mint"]
        if mint in out:
            raise ValueError(f"{name}: duplicate mint: {mint}")
        out[mint] = row
    return out


def wallets(rows: object, key: str, name: str) -> dict[str, dict]:
    if not isinstance(rows, list):
        raise ValueError(f"{name}: {key} not a list")
    out = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get(key), str):
            raise ValueError(f"{name}: missing {key}")
        owner = row[key]
        if owner in out:
            raise ValueError(f"{name}: duplicate {key} {owner}")
        out[owner] = row
    return out


def audit(buys: dict, flows: dict, slots: dict | None = None) -> dict:
    initial = records(buys, "buys")
    later = records(flows, "flows")
    if set(initial) != set(later):
        raise ValueError("unmatched mint set; do not silently drop cases")
    slot_records = records(slots, "slots") if slots is not None else {}
    if slots is not None and set(slot_records) != set(initial):
        raise ValueError("slot records do not match mint cohort")

    cases = []
    counts = {"outflow_exceeds_creation_buys": 0, "within_tolerance": 0,
              "outflow_below_creation_buys": 0, "transfer_equals_creation_buys": 0,
              "has_reported_sell": 0}
    for mint in sorted(initial):
        buy = wallets(initial[mint].get("buys"), "wallet", f"{mint}:buys")
        flow = wallets(later[mint].get("wallets"), "wallet", f"{mint}:flows")
        if set(buy) != set(flow):
            raise ValueError(f"{mint}: wallet sets differ; inspect separately")
        entries, total_bought, total_transferred, total_sold = [], Decimal(0), Decimal(0), Decimal(0)
        for owner in sorted(buy):
            b = amount(buy[owner].get("tokens"))
            t = amount(flow[owner].get("tokens_transferes"))
            s = amount(flow[owner].get("tokens_vendus"))
            delta = t + s - b
            entries.append({"wallet": owner, "creation_buy_tokens": str(b),
                            "reported_transfer_tokens": str(t), "reported_sell_tokens": str(s),
                            "excess_outflow_vs_creation_buys": str(delta),
                            "conditional_minimum_unseen_inflow": str(max(delta, Decimal(0))),
                            "explanation": "UNDETERMINED_NO_CHRONOLOGICAL_LEDGER"})
            total_bought += b
            total_transferred += t
            total_sold += s
        diff = total_transferred + total_sold - total_bought
        if diff > TOL:
            status = "OUTFLOW_EXCEEDS_CREATION_BUYS"
            counts["outflow_exceeds_creation_buys"] += 1
        elif diff < -TOL:
            status = "OUTFLOW_BELOW_CREATION_BUYS"
            counts["outflow_below_creation_buys"] += 1
        else:
            status = "WITHIN_TOLERANCE"
            counts["within_tolerance"] += 1
        if abs(total_transferred - total_bought) <= TOL:
            counts["transfer_equals_creation_buys"] += 1
        if total_sold > TOL:
            counts["has_reported_sell"] += 1
        slot = slot_records.get(mint)
        cases.append({"mint": mint, "status": status,
                      "creation_buy_tokens": str(total_bought),
                      "reported_transfer_tokens": str(total_transferred),
                      "reported_sell_tokens": str(total_sold),
                      "excess_outflow_vs_creation_buys": str(diff),
                      "conditional_minimum_unseen_inflow": str(max(diff, Decimal(0))),
                      "source_sell_is_confirmed_swap": False,
                      "asset_path_closed": False,
                      "economic_owner_confirmed": False,
                      "net_trade_edge_verified": False,
                      "creation_slot": (slot.get("slot") if slot is not None else None),
                      "block_contiguous_reported": (slot.get("contigu") if slot is not None else None),
                      "external_to_group_vwap_ratio_reported": (
                          slot.get("ratio_premier_externe_sur_operateur") if slot is not None else None),
                      "wallets": entries})

    return {"schema_version": "0.1", "kind": "CROSS_SOURCE_DERIVED_TABLE_RECONCILIATION",
            "source_window_warning": "creation-slot buys vs later token-account lifetime; excess != chain violation",
            "raw_rpc_checked": False,
            "profit_or_alpha_verified": False,
            "ui_token_tolerance": str(TOL),
            "cohort_size": len(cases), "counts": counts, "cases": cases}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--buys", type=Path, required=True)
    parser.add_argument("--flows", type=Path, required=True)
    parser.add_argument("--slots", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    def load(path: Path) -> dict:
        with path.open(encoding="utf-8") as f:
            return json.load(f, parse_float=Decimal)
    result = audit(load(args.buys), load(args.flows), load(args.slots) if args.slots else None)
    body = json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")


if __name__ == "__main__":
    main()
