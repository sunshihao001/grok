"""Discover count-vs-capital semantic inversions in *source-derived* SOL receipts.

This module does not infer a wallet's original beneficial owner, whether a
program actually executed a swap, or whether a position produced PnL. It
detects when counts within a broad source label conceal a different dominant
economic activity by value, then asks for discriminating signature checks.

Input: Why-Solana derived e2 funding JSON (wallets[].inflows[]).
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, InvalidOperation
import argparse
import json
from pathlib import Path

from .cashflow_semantics import audit_funding_table

SOL_PRECISION = Decimal("0.000000001")
ONE = Decimal(1)
ZERO = Decimal(0)


def _sol_value(value: object) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError("amount_sol requires a decimal number or decimal string")
    try:
        d = Decimal(str(value))
    except (InvalidOperation, ValueError) as err:
        raise ValueError("amount_sol must be decimal") from err
    if not d.is_finite() or d < ZERO or d.as_tuple().exponent < -9:
        raise ValueError("amount_sol must be finite, nonnegative and at most 9 decimals")
    return d


def _ratio(n: Decimal | int, total: Decimal | int) -> str:
    return format(Decimal(n) / Decimal(total), ".6f") if total else "0.000000"


def _sol(amount: Decimal) -> str:
    return format(amount.quantize(SOL_PRECISION), ".9f")


def discover_cashflow_mechanisms(
        document: dict, *,
        label: str = "financement",
        majority_share: Decimal = Decimal("0.5"),
        sample_limit: int = 5) -> dict:
    """Produce testable candidates when broad receipt *labels* mask source mix.

    "Non-system" and "System Transfer" are source metadata labels, not
    independently verified actual instructions or new external capital.
    """
    audited = audit_funding_table(document)
    if not isinstance(label, str) or not label.strip():
        raise ValueError("label must be a nonempty string")
    if isinstance(majority_share, bool):
        raise ValueError("invalid majority threshold")
    try:
        threshold = Decimal(str(majority_share))
    except InvalidOperation as exc:
        raise ValueError("invalid majority threshold") from exc
    if not threshold.is_finite() or not ZERO < threshold < ONE:
        raise ValueError("majority_share must be between 0 and 1")
    if type(sample_limit) is not int or sample_limit < 1 or sample_limit > 50:
        raise ValueError("sample_limit must be 1..50")

    groups: dict[str, dict] = defaultdict(lambda: {
        "rows": 0, "amount": ZERO, "examples": []})
    totals: dict[str, dict] = defaultdict(lambda: {"rows": 0, "amount": ZERO})
    wallets: dict[str, Decimal] = defaultdict(lambda: ZERO)
    records = []
    for wallet in document["wallets"]:
        for inflow in wallet["inflows"]:
            if inflow.get("nature") != label:
                continue
            amount = _sol_value(inflow.get("amount_sol"))
            kind = inflow.get("tx_source")
            tx_type = inflow.get("tx_type")
            if not isinstance(kind, str) or not kind or not isinstance(tx_type, str) or not tx_type:
                raise ValueError("source inflow must retain tx_source and tx_type")
            key = (kind, tx_type)
            # Dictionary keyed by source type to prevent a program label from
            # being treated as a separate economic owner.
            label_key = kind + "|" + tx_type
            groups[label_key]["rows"] += 1
            groups[label_key]["amount"] += amount
            bucket = "SYSTEM_PROGRAM" if kind == "SYSTEM_PROGRAM" else "OTHER_PROGRAM"
            totals[bucket]["rows"] += 1
            totals[bucket]["amount"] += amount
            wallets[wallet["wallet"]] += amount
            records.append({
                "wallet": wallet["wallet"], "signature": inflow["signature"],
                "tx_source": kind, "tx_type": tx_type, "amount": amount})
    sum_amount = sum((r["amount"] for r in records), ZERO)
    n = len(records)
    other = totals["OTHER_PROGRAM"]
    count_share = Decimal(other["rows"]) / Decimal(n) if n else ZERO
    value_share = other["amount"] / sum_amount if sum_amount else ZERO
    inversion = bool(n and sum_amount and
                     count_share < threshold and value_share > threshold)
    # Rank only for investigation. Never claim that highest value is highest
    # anomalous risk or a tradeable signal.
    targets = sorted(records, key=lambda r: (-r["amount"], r["signature"], r["wallet"]))
    examples = []
    seen = set()
    for record in targets:
        if record["signature"] in seen:
            continue
        seen.add(record["signature"])
        if len(examples) >= sample_limit:
            break
        examples.append({"wallet": record["wallet"],
                         "signature": record["signature"],
                         "source_label": record["tx_source"],
                         "type_label": record["tx_type"],
                         "source_amount_sol": _sol(record["amount"]),
                         "source_replay_status": "NOT_CHECKED"})
    breakdown = [
        {"source_type": key, "count": val["rows"],
         "source_amount_sol": _sol(val["amount"]),
         "count_share": _ratio(val["rows"], n),
         "value_share": _ratio(val["amount"], sum_amount)}
        for key, val in sorted(groups.items(), key=lambda x: (-x[1]["amount"], x[0]))
    ]
    largest_wallet = sorted(wallets.items(), key=lambda v: (-v[1], v[0]))[0] if wallets else None
    mechanisms = []
    if inversion:
        mechanisms.append({
            "id": "COUNT_VALUE_ECONOMIC_TYPE_INVERSION",
            "state": "OBSERVED_SOURCE_DERIVED_COMPOSITION_NOT_MARKET_ANOMALY",
            "observed": "A minority of other-program receipts dominates the value of the broad label",
            "logically_invalid_inference": f"{label} label => directly verified external wallet funding",
            "competing_hypotheses": [
                "Previously deployed LP capital was withdrawn/reallocated",
                "Other program receipts reflect bridge, marketplace, or collateral changes",
                "Transactions contain mixed effects; source whole-transaction label is incomplete",
                "A separately verified external transfer might still exist in the same transaction"],
            "discriminating_next_checks": [
                "Replay largest source signatures using getTransaction with outer/inner instructions",
                "Reconcile token/WSOL accounts, pool reserves, rent and native lamport deltas",
                "Determine economic position before and after each transaction, not merely net SOL received",
                "Contrast with ordinary LP/provider exits and wallets with complete history",
                "Check whether identified capital flows back into other Mint launch episodes"],
            "rejection_rule": "If raw transaction replay shows these receipts are correctly attributable to fresh independent external transfers, retire the source-value interpretation for this cohort",
            "trade_implication": "NONE_UNTIL_INDEPENDENT_OUT_OF_SAMPLE_AND_EXECUTION_TESTS",
        })
    return {
        "schema_version": "0.1",
        "result_type": "DERIVED_CASHFLOW_MECHANISM_DISCOVERY",
        "analysis_scope": "SOURCE_DERIVED_COHORT_NOT_ALL_MARKET",
        "focal_source_label": label,
        "wallets_in_cohort": audited["wallet_count"],
        "genesis_covered": audited["genesis_covered"],
        "genesis_uncovered": audited["genesis_uncovered"],
        "prebuy_covered": audited["prebuy_covered"],
        "prebuy_uncovered": audited["prebuy_uncovered"],
        "labelled_rows": n,
        "labelled_positive_sol_receipt": _sol(sum_amount),
        "system_program_labelled_rows": totals["SYSTEM_PROGRAM"]["rows"],
        "system_program_labelled_sol": _sol(totals["SYSTEM_PROGRAM"]["amount"]),
        "other_program_labelled_rows": other["rows"],
        "other_program_labelled_sol": _sol(other["amount"]),
        "other_program_count_share": _ratio(other["rows"], n),
        "other_program_value_share": _ratio(other["amount"], sum_amount),
        "source_value_dominance_inversion": inversion,
        "source_breakdown": breakdown,
        "largest_wallet_source_label_receipts": (
            {"wallet": largest_wallet[0], "source_amount_sol": _sol(largest_wallet[1]),
             "source_value_share": _ratio(largest_wallet[1], sum_amount)}
            if largest_wallet and sum_amount else None),
        "replay_priority_signatures": examples,
        "candidate_mechanisms": mechanisms,
        "provenance_status": "PUBLISHED_DERIVED_TABLE_NOT_REPLAYED_BY_THIS_MODULE",
        "abnormality_confirmed": False,
        "economic_controller_confirmed": False,
        "capital_injection_confirmed": False,
        "price_impact_confirmed": False,
        "hypotheses_tested_on_real_rpc": False,
        "no_trading": True,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--label", default="financement")
    args = p.parse_args()
    result = discover_cashflow_mechanisms(json.loads(
        args.input.read_text(encoding="utf-8")), label=args.label)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
