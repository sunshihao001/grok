"""Bounded no-key Solana wallet RPC sample, not continuous wallet monitoring.

Uses the existing fixed-host RPC transport. Saves signature and at most one raw
transaction; cannot classify BUY/SELL, economic owner, coordinated actors or PnL.
Public RPC may return 403/429 and is unsuitable for production monitoring.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any, Callable

from .public_token_accounts import RPC_URL, rpc_request, valid_address

SIG_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{64,100}$")
MAX_SIGNATURES = 3


def decode(raw: bytes, method: str) -> Any:
    try:
        value = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"invalid {method} JSON") from exc
    if not isinstance(value, dict) or value.get("jsonrpc") != "2.0":
        raise ValueError(f"invalid {method} RPC envelope")
    if value.get("error") is not None:
        err = value["error"]
        code = err.get("code") if isinstance(err, dict) else None
        raise ValueError(f"{method} returned RPC error code={code}")
    if "result" not in value:
        raise ValueError(f"{method} missing RPC result")
    return value["result"]



def execution_facts(tx: dict[str, Any], queried_wallet: str) -> dict[str, Any]:
    """Observe RPC execution/fee and final balances; not a DEX or CPI parser.

    Never turn a failed CPI into executed funding/swaps. Do not infer any
    economic owner from fee payer, signers or account inclusion.
    """
    meta = tx.get("meta")
    transaction = tx.get("transaction")
    msg = transaction.get("message") if isinstance(transaction, dict) else None
    keys = msg.get("accountKeys") if isinstance(msg, dict) else None
    if not isinstance(meta, dict) or "err" not in meta or not isinstance(keys, list) or not keys:
        return {"status": "UNKNOWN_INCOMPLETE_EXECUTION_META",
                "successful_swap": "NOT_ASSESSED"}
    if not all(isinstance(k, dict) and isinstance(k.get("pubkey"), str) for k in keys):
        return {"status": "UNKNOWN_ACCOUNT_KEY_FORMAT",
                "successful_swap": "NOT_ASSESSED"}
    fee = meta.get("fee")
    pre, post = meta.get("preBalances"), meta.get("postBalances")
    if type(fee) is not int or fee < 0 or not isinstance(pre, list) or not isinstance(post, list):
        return {"status": "UNKNOWN_INCOMPLETE_EXECUTION_BALANCES",
                "successful_swap": "NOT_ASSESSED"}
    if len(keys) != len(pre) or len(pre) != len(post) or any(
        type(x) is not int or x < 0 for x in pre + post
    ):
        return {"status": "UNKNOWN_INCONSISTENT_EXECUTION_BALANCES",
                "successful_swap": "NOT_ASSESSED"}
    payer = keys[0]["pubkey"] if keys[0].get("signer") is True else None
    if payer is None:
        return {"status": "UNKNOWN_FEE_PAYER", "successful_swap": "NOT_ASSESSED"}
    sol_changes = [
        {"account": key["pubkey"], "delta_lamports": b - a}
        for key, a, b in zip(keys, pre, post) if a != b
    ]
    # Token balance snapshots are not complete economic identities. Compare
    # account-index+mint+program+owner+raw amount, never floating-point UI values.
    def token_map(name: str) -> dict[tuple, str] | None:
        entries = meta.get(name)
        if not isinstance(entries, list):
            return None
        out = {}
        for entry in entries:
            if not isinstance(entry, dict):
                return None
            index = entry.get("accountIndex")
            amount = (entry.get("uiTokenAmount") or {}).get("amount")
            if type(index) is not int or not 0 <= index < len(keys) or (
                not isinstance(amount, str) or not amount.isdigit()
            ):
                return None
            key = (index, entry.get("mint"), entry.get("programId"), entry.get("owner"))
            if key in out:
                return None
            out[key] = amount
        return out
    before, after = token_map("preTokenBalances"), token_map("postTokenBalances")
    token_state = "UNKNOWN_INCOMPLETE_TOKEN_BALANCES" if before is None or after is None else (
        "UNCHANGED_REPORTED_TOKEN_BALANCES" if before == after else
        "CHANGED_REPORTED_TOKEN_BALANCES_NOT_A_SWAP_PROOF"
    )
    failed = meta["err"] is not None
    return {
        "status": "FAILED_ROLLED_BACK" if failed else "SUCCESSFUL_EXECUTION_UNCLASSIFIED",
        "rpc_error": meta["err"],
        "fee_lamports": fee,
        "fee_payer": payer,
        "wallet_in_transaction_accounts": queried_wallet in {k["pubkey"] for k in keys},
        "wallet_is_signer": any(k["pubkey"] == queried_wallet and k.get("signer") is True for k in keys),
        "wallet_is_fee_payer": queried_wallet == payer,
        "sol_account_deltas_from_meta": sol_changes,
        "token_balance_comparison": token_state,
        "transaction_committed_program_movements": False if failed else "NOT_CLASSIFIED",
        "successful_swap": False if failed else "NOT_ASSESSED",
        "unknowns": [
            "economic_controller_not_identified",
            "wallet_in_account_list_is_not_wallet_activity_proof",
            "instruction_trace_not_an_executed_transfer_without_success",
            "reported_token_balances_not_complete_token_movement_trace",
        ],
    }


def sample(wallet: str, *, limit: int = 2,
           request_fn: Callable[[str, list[Any]], bytes] = rpc_request,
           retrieved_at: str | None = None) -> tuple[dict[str, Any], dict[str, bytes]]:
    if not valid_address(wallet):
        raise ValueError("invalid wallet base58 address")
    if type(limit) is not int or not 1 <= limit <= MAX_SIGNATURES:
        raise ValueError("signature limit must be 1..3")
    now = retrieved_at or datetime.now(timezone.utc).isoformat()
    signature_raw = request_fn(
        "getSignaturesForAddress",
        [wallet, {"limit": limit, "commitment": "finalized"}],
    )
    signatures = decode(signature_raw, "getSignaturesForAddress")
    if not isinstance(signatures, list) or len(signatures) > limit:
        raise ValueError("invalid signature page or result exceeds requested bound")

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in signatures:
        if not isinstance(item, dict):
            raise ValueError("invalid signature list item")
        sig = item.get("signature")
        slot = item.get("slot")
        if not isinstance(sig, str) or not SIG_RE.fullmatch(sig) or sig in seen:
            raise ValueError("invalid or duplicate Solana signature")
        if type(slot) is not int or slot < 0:
            raise ValueError("invalid signature slot")
        seen.add(sig)
        blocktime = item.get("blockTime")
        if blocktime is not None and (type(blocktime) is not int or blocktime <= 0):
            raise ValueError("invalid signature blockTime")
        rows.append({
            "signature": sig,
            "slot": slot,
            "block_time_source_unix": blocktime,
            "err_vendor": item.get("err"),
            "confirmation_status_vendor": item.get("confirmationStatus"),
            "event_type": "UNKNOWN_NOT_DECODED",
        })

    raw_by_file = {"wallet-signatures-raw.json": signature_raw}
    raw_tx_status = "NOT_AVAILABLE_NO_SIGNATURES"
    raw_tx_error = None
    raw_tx_sig = None
    tx_slot = None
    economic_observation = {"status": "NO_TRANSACTION_OBSERVED", "successful_swap": "NOT_ASSESSED"}
    if rows:
        raw_tx_sig = rows[0]["signature"]
        try:
            tx_raw = request_fn("getTransaction", [
                raw_tx_sig,
                {"encoding": "jsonParsed", "commitment": "finalized",
                 "maxSupportedTransactionVersion": 0},
            ])
            raw_by_file["wallet-first-transaction-raw.json"] = tx_raw
            tx = decode(tx_raw, "getTransaction")
            if tx is None:
                raw_tx_status = "RPC_RETURNED_NULL_COVERAGE_UNKNOWN"
            elif not isinstance(tx, dict) or type(tx.get("slot")) is not int:
                raise ValueError("getTransaction invalid result/slot")
            else:
                tx_slot = tx["slot"]
                if tx_slot != rows[0]["slot"]:
                    raise ValueError("transaction slot inconsistent with signature")
                raw_tx_status = "RAW_TRANSACTION_AVAILABLE_NOT_ECONOMICALLY_DECODED"
                economic_observation = execution_facts(tx, wallet)
        except (OSError, ValueError) as exc:
            raw_tx_status = "RAW_TRANSACTION_UNAVAILABLE"
            raw_tx_error = str(exc)[:160]

    report = {
        "schema_version": "grok.public_wallet_rpc_sample.v0",
        "wallet": wallet,
        "chain": "solana-mainnet",
        "source": {"url": RPC_URL, "methods": [
            "getSignaturesForAddress", "getTransaction",
        ], "retrieved_at": now},
        "raw_input_sha256": {
            filename: hashlib.sha256(raw).hexdigest()
            for filename, raw in raw_by_file.items()
        },
        "result": "BOUNDED_RAW_SIGNATURE_SAMPLE_NOT_WALLET_HISTORY",
        "rows": rows,
        "transaction": {
            "signature": raw_tx_sig, "slot": tx_slot,
            "status": raw_tx_status, "error": raw_tx_error,
            "execution_observation": economic_observation,
        },
        "coverage": {
            "requested_latest_max": limit,
            "full_wallet_history": False,
            "all_wallet_roles_in_tx": "UNKNOWN",
            "swap_buy_sell_classification": "NOT_PERFORMED",
            "funding_and_owner_attribution": "NOT_PERFORMED",
            "continuous_monitoring": False,
            "provider_429_or_archive_gap_possible": True,
        },
        "no_trading": True,
        "no_payment": True,
        "grok_bot_called": False,
    }
    return report, raw_by_file


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="No-key public Solana wallet signature probe; not full monitoring")
    p.add_argument("--wallet", required=True)
    p.add_argument("--limit", type=int, default=2)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        report, sources = sample(args.wallet, limit=args.limit)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for name, raw in sources.items():
            (args.out_dir / name).write_bytes(raw)
        (args.out_dir / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({
            "status": "RAW_SAMPLE_ONLY", "signatures": len(report["rows"]),
            "tx_status": report["transaction"]["status"],
            "out_dir": str(args.out_dir),
        }, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({
            "status": "PUBLIC_RPC_UNAVAILABLE_OR_INVALID",
            "reason": str(exc)[:240],
            "no_false_empty_wallet_claim": True,
        }, ensure_ascii=False), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
