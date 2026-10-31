"""Conservative, offline Solana getTransaction -> M01 event adapter.

Never fetches RPC, signs, or trades. No DEX BUY/SELL inference from balance deltas.
Only direct System Program funding transfers and top-level SPL Token Transfer / TransferChecked
are decoded. Inner CPI token transfers are unresolved, NOT counted as standalone Swap.
Unsupported/missing evidence fails closed and downgrades completeness.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any

from .wallet_batch_monitor import parse_time, iso, validate as validate_m01

TOKEN = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
TOKEN_2022 = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
SYSTEM = "11111111111111111111111111111111"
WSOL = "So11111111111111111111111111111111111111112"
TOKEN_PROGRAMS = {TOKEN, TOKEN_2022}
ADDRESS = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
B58 = {c: i for i, c in enumerate("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")}
MAX_TXS = 10_000


def _addr(value: Any) -> bool:
    return isinstance(value, str) and ADDRESS.fullmatch(value) is not None


def _amount(value: Any) -> int:
    if type(value) is int and value >= 0:
        return value
    if isinstance(value, str) and value.isascii() and value.isdigit():
        return int(value)
    raise ValueError("amount must be an unsigned raw integer")


def _decode58(raw: str) -> bytes:
    if not isinstance(raw, str) or not raw:
        raise ValueError("base58 instruction data missing")
    n = 0
    for char in raw:
        if char not in B58:
            raise ValueError("invalid base58 instruction data")
        n = n * 58 + B58[char]
    n_zeros = len(raw) - len(raw.lstrip("1"))
    data = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    return b"\x00" * n_zeros + data


def _keys(rpc: dict[str, Any]) -> tuple[list[str], list[bool], bool]:
    msg = rpc["transaction"]["message"]
    raw = msg.get("accountKeys")
    if not isinstance(raw, list) or not raw:
        raise ValueError("missing accountKeys")
    parsed = isinstance(raw[0], dict)
    if any(isinstance(k, dict) != parsed for k in raw):
        raise ValueError("mixed account key representations")
    keys = [k.get("pubkey") if parsed else k for k in raw]
    if not all(_addr(k) for k in keys):
        raise ValueError("invalid account address")
    signers = [k.get("signer") is True for k in raw] if parsed else []
    if not parsed:
        required = msg.get("header", {}).get("numRequiredSignatures")
        if type(required) is not int or not 1 <= required <= len(raw):
            raise ValueError("invalid transaction signer header")
        signers = [i < required for i in range(len(raw))]
        lookups = msg.get("addressTableLookups", [])
        loaded = rpc.get("meta", {}).get("loadedAddresses") if isinstance(rpc.get("meta"), dict) else None
        if lookups and not isinstance(loaded, dict):
            raise ValueError("address lookup table entries not resolved")
        if isinstance(loaded, dict):
            additional = loaded.get("writable", []) + loaded.get("readonly", [])
            if not all(_addr(k) for k in additional):
                raise ValueError("invalid loaded address")
            keys.extend(additional)
            signers.extend([False] * len(additional))
    return keys, signers, parsed


def _owners(meta: dict[str, Any], keys: list[str]) -> tuple[dict[str, tuple[str, str]], bool]:
    """Resolve token-account address -> (mint, owner), never fee payer or delegate."""
    owners: dict[str, tuple[str, str]] = {}
    conflict = False
    for side in ("preTokenBalances", "postTokenBalances"):
        values = meta.get(side)
        if values is None:
            continue
        if not isinstance(values, list):
            return owners, True
        for bal in values:
            if not isinstance(bal, dict):
                conflict = True
                continue
            idx, mint, owner = bal.get("accountIndex"), bal.get("mint"), bal.get("owner")
            if type(idx) is not int or not 0 <= idx < len(keys):
                conflict = True
                continue
            if not _addr(mint) or not _addr(owner):
                # Do not invent owner from fee payer or instruction authority.
                continue
            account = keys[idx]
            value = (mint, owner)
            if account in owners and owners[account] != value:
                conflict = True
            owners[account] = value
    return owners, conflict


def _decoded(ix: dict[str, Any], keys: list[str]) -> tuple[str | None, str | None, dict[str, Any] | None, str | None]:
    """Return program, type, info, and a parse error without guessing DEX semantics."""
    if not isinstance(ix, dict):
        return None, None, None, "MALFORMED_INSTRUCTION"
    pid = ix.get("programId")
    if pid is None and type(ix.get("programIdIndex")) is int:
        index = ix["programIdIndex"]
        pid = keys[index] if 0 <= index < len(keys) else None
    if not _addr(pid):
        return None, None, None, "UNRESOLVED_PROGRAM_INDEX"
    parsed = ix.get("parsed")
    if isinstance(parsed, dict):
        typ, info = parsed.get("type"), parsed.get("info")
        if not isinstance(typ, str) or not isinstance(info, dict):
            return pid, None, None, "UNSUPPORTED_PARSED_IX"
        return pid, typ, info, None
    if pid not in TOKEN_PROGRAMS | {SYSTEM}:
        return pid, None, None, "UNRECOGNIZED_PROGRAM_INSTRUCTION"
    try:
        data = _decode58(ix.get("data"))
        accts = ix.get("accounts")
        if not isinstance(accts, list) or not all(type(j) is int and 0 <= j < len(keys) for j in accts):
            return pid, None, None, "UNRESOLVED_COMPILED_ACCOUNTS"
        addresses = [keys[j] for j in accts]
        if pid in TOKEN_PROGRAMS:
            if len(data) == 9 and data[0] == 3 and len(addresses) >= 3:
                return pid, "transfer", {"source": addresses[0], "destination": addresses[1],
                                         "authority": addresses[2], "amount": str(int.from_bytes(data[1:9], "little"))}, None
            if len(data) == 10 and data[0] == 12 and len(addresses) >= 4:
                return pid, "transferChecked", {"source": addresses[0], "mint": addresses[1],
                                                "destination": addresses[2], "authority": addresses[3],
                                                "tokenAmount": {"amount": str(int.from_bytes(data[1:9], "little")),
                                                                "decimals": data[9]}}, None
        if pid == SYSTEM and len(data) == 12 and data[:4] == b"\x02\x00\x00\x00" and len(addresses) >= 2:
            return pid, "transfer", {"source": addresses[0], "destination": addresses[1],
                                     "lamports": int.from_bytes(data[4:12], "little")}, None
    except ValueError:
        return pid, None, None, "INVALID_COMPILED_IX"
    return pid, None, None, "UNSUPPORTED_COMPILED_IX"


def _which_mint(info: dict[str, Any] | None, owner_map: dict[str, tuple[str, str]]) -> str | None:
    if not info:
        return None
    if _addr(info.get("mint")):
        return info["mint"]
    for key in ("source", "destination"):
        if info.get(key) in owner_map:
            return owner_map[info[key]][0]
    return None


def _transfer(ix: dict[str, Any], keys: list[str], owner_map: dict[str, tuple[str, str]],
              mint: str, signature: str, slot: int, when: str, avail: str,
              source_ref: str, fee_payer: str, outer: int, inner: int | None) -> tuple[dict | None, dict | None]:
    pid, typ, info, err = _decoded(ix, keys)
    if pid in TOKEN_PROGRAMS:
        if info is None:
            return None, {"reason": err or "UNKNOWN_TOKEN_IX", "path": [outer, inner]}
        imint = _which_mint(info, owner_map)
        if imint != mint:
            # A missing mint inside an otherwise transfer-shaped instruction can hide target transfers.
            if imint is None and typ.lower().startswith("transfer"):
                return None, {"reason": "TOKEN_MINT_UNRESOLVED", "path": [outer, inner]}
            return None, None
        if inner is not None:
            return None, {"reason": "CPI_TOKEN_MOVEMENT_NOT_SWAP", "path": [outer, inner]}
        if typ in {"initializeAccount", "initializeAccount2", "initializeAccount3", "syncNative",
                   "initializeImmutableOwner", "approve", "revoke", "closeAccount"}:
            # Administrative token instructions are not independently counted as Swap/Transfer.
            return None, None
        if typ not in {"transfer", "transferChecked"}:
            return None, {"reason": "UNSUPPORTED_TOKEN_2022_OR_TOKEN_OP", "path": [outer, inner]}
        src, dst = info.get("source"), info.get("destination")
        src_details, dst_details = owner_map.get(src), owner_map.get(dst)
        if not src_details or src_details[0] != mint:
            return None, {"reason": "TOKEN_SOURCE_OWNER_UNKNOWN", "path": [outer, inner]}
        if typ == "transferChecked":
            token_amount = info.get("tokenAmount")
            if not isinstance(token_amount, dict):
                return None, {"reason": "TOKEN_AMOUNT_UNRESOLVED", "path": [outer, inner]}
            raw = token_amount.get("amount")
        else:
            raw = info.get("amount")
        try:
            amount = _amount(raw)
        except ValueError:
            return None, {"reason": "TOKEN_AMOUNT_UNRESOLVED", "path": [outer, inner]}
        if not _addr(src) or not _addr(dst):
            return None, {"reason": "TOKEN_ACCOUNT_ADDRESS_UNKNOWN", "path": [outer, inner]}
        event_id = f"{signature}:outer:{outer}"
        event = {"event_id": event_id, "signature": signature, "slot": slot,
                 "event_time": when, "available_at": avail, "source_ref": source_ref,
                 "kind": "TRANSFER", "tx_status": "SUCCESS", "wallet_owner": src_details[1],
                 "token_account": src, "quote_amount_raw": 0,
                 "transfer_amount_raw": amount, "source_token_account": src, "destination_token_account": dst,
                 "destination_owner": dst_details[1] if dst_details and dst_details[0] == mint else None,
                 "authority": info.get("authority"), "fee_payer": fee_payer,
                 "token_program": pid, "instruction_path": [outer],
                 "interpretation": "direct_token_movement_not_economic_swap_or_human_identity"}
        return event, None
    if pid == SYSTEM and typ == "transfer" and info:
        src, dst = info.get("source"), info.get("destination")
        try:
            lamports = _amount(info.get("lamports"))
        except ValueError:
            return None, {"reason": "SOL_AMOUNT_UNRESOLVED", "path": [outer, inner]}
        if not _addr(src) or not _addr(dst):
            return None, {"reason": "SOL_ENDPOINT_UNKNOWN", "path": [outer, inner]}
        if inner is not None:
            # CPI SOL transfers can be protocol rent, settlement or pool movement, not independent funding.
            return None, {"reason": "CPI_SOL_MOVEMENT_NOT_USER_FUNDING", "path": [outer, inner]}
        # Separate funding stream; never create M01 mint-specific transfer from native SOL.
        return {"funding_id": f"{signature}:{outer}:{inner if inner is not None else 'outer'}",
                "kind": "SOL_TRANSFER", "source_wallet": src, "destination_wallet": dst,
                "lamports": lamports, "signature": signature, "slot": slot,
                "event_time": when, "available_at": avail, "source_ref": source_ref,
                "fee_payer": fee_payer, "instruction_path": [outer] if inner is None else [outer, inner],
                "interpretation": "native_sol_movement_only_no_mint_link"}, None
    # Unknown DEX program: only mark target mint if balance evidence shows a change.
    return None, None


def normalize(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict) or payload.get("schema_version") != "m01.raw.v1":
        raise ValueError("schema_version must be m01.raw.v1")
    if payload.get("mode") != "fixture" or payload.get("chain") != "sol":
        raise ValueError("fixture-only Solana adapter")
    txs = payload.get("transactions")
    if not isinstance(txs, list) or len(txs) > MAX_TXS:
        raise ValueError("transactions must be a list of at most 10000")
    result = {key: payload[key] for key in
              ("chain", "mode", "mint", "quote_mint", "quote_decimals", "coverage", "as_of", "source")}
    result["schema_version"] = "m01.v1"
    result["events"] = []
    audit: dict[str, Any] = {"status": "FIXTURE_ONLY_PARTIAL_SEMANTICS",
                             "transaction_count": len(txs), "unresolved": [], "funding_events": [],
                             "unsupported": [], "no_rpc_calls": True, "no_trading": True,
                             "coverage_attestation": "fixture_asserted_not_independent_chain_completeness"}
    as_of = parse_time(result["as_of"])
    starts, ends = parse_time(result["coverage"]["start"]), parse_time(result["coverage"]["end"])
    seen: set[str] = set()
    for item in txs:
        if not isinstance(item, dict):
            raise ValueError("transaction envelope must be object")
        signature, ref = item.get("signature"), item.get("source_ref")
        if not isinstance(signature, str) or not signature or not isinstance(ref, str) or not ref:
            raise ValueError("signature and source_ref required")
        if signature in seen:
            raise ValueError("duplicate signature envelope; deduplicate at ingest")
        seen.add(signature)
        available = parse_time(item.get("available_at"))
        rpc = item.get("rpc")
        if not isinstance(rpc, dict):
            raise ValueError("rpc transaction record required")
        slot, epoch = rpc.get("slot"), rpc.get("blockTime")
        if type(slot) is not int or slot < 0:
            raise ValueError("invalid slot")
        if type(epoch) is not int or epoch < 0:
            audit["unresolved"].append({"signature": signature, "reason": "BLOCK_TIME_UNKNOWN", "source_ref": ref})
            result["coverage"] = {**result["coverage"], "complete": False}
            continue
        dt = datetime.fromtimestamp(epoch, timezone.utc)
        if not starts <= dt < ends or available < dt:
            raise ValueError("event time outside coverage or available before block")
        when, avail = iso(dt), iso(available)
        meta = rpc.get("meta")
        if not isinstance(meta, dict) or not isinstance(rpc.get("transaction"), dict):
            audit["unresolved"].append({"signature": signature, "reason": "MISSING_META_OR_TRANSACTION", "source_ref": ref})
            result["coverage"] = {**result["coverage"], "complete": False}
            continue
        version = rpc.get("version", "legacy")
        if version != "legacy" and (type(version) is not int or version != 0):
            audit["unresolved"].append({"signature": signature, "reason": "UNSUPPORTED_TX_VERSION", "source_ref": ref})
            result["coverage"] = {**result["coverage"], "complete": False}
            continue
        raw_signatures = rpc["transaction"].get("signatures")
        if not isinstance(raw_signatures, list) or not raw_signatures or raw_signatures[0] != signature:
            raise ValueError("RPC signature mismatch")
        try:
            keys, signers, parsed = _keys(rpc)
        except (ValueError, KeyError, TypeError) as exc:
            audit["unresolved"].append({"signature": signature, "reason": "ACCOUNT_KEYS_UNRESOLVED",
                                        "detail": str(exc), "source_ref": ref})
            result["coverage"] = {**result["coverage"], "complete": False}
            continue
        fee_payer = keys[0]
        owner_map, conflict = _owners(meta, keys)
        if conflict:
            audit["unresolved"].append({"signature": signature, "reason": "TOKEN_OWNER_CONFLICT", "source_ref": ref})
            result["coverage"] = {**result["coverage"], "complete": False}
            continue
        msg = rpc["transaction"].get("message")
        outer = msg.get("instructions") if isinstance(msg, dict) else None
        if not isinstance(outer, list):
            audit["unresolved"].append({"signature": signature, "reason": "MISSING_OUTER_INSTRUCTIONS", "source_ref": ref})
            result["coverage"] = {**result["coverage"], "complete": False}
            continue
        if meta.get("err") is not None:
            audit["unsupported"].append({"signature": signature, "reason": "FAILED_TRANSACTION_NO_ECONOMIC_ACTION",
                                          "source_ref": ref})
            continue
        inner = meta.get("innerInstructions")
        if inner is None:
            # If token balance changed, lack of CPI trace prevents any claim that there is no swap.
            inner = []
            if any(b.get("mint") == result["mint"] for b in
                   (meta.get("postTokenBalances") or []) + (meta.get("preTokenBalances") or []) if isinstance(b, dict)):
                audit["unresolved"].append({"signature": signature, "reason": "INNER_TRACE_UNAVAILABLE", "source_ref": ref})
                result["coverage"] = {**result["coverage"], "complete": False}
        if not isinstance(inner, list):
            raise ValueError("innerInstructions invalid")
        decoded_target = False
        for index, ix in enumerate(outer):
            event, issue = _transfer(ix, keys, owner_map, result["mint"], signature, slot,
                                     when, avail, ref, fee_payer, index, None)
            if event:
                if "event_id" in event:
                    result["events"].append(event)
                    decoded_target = True
                else:
                    audit["funding_events"].append(event)
            if issue:
                audit["unresolved"].append({"signature": signature, "source_ref": ref, **issue})
                # Fail closed for ambiguous token event; may involve target mint.
                result["coverage"] = {**result["coverage"], "complete": False}
        for group in inner:
            if not isinstance(group, dict) or type(group.get("index")) is not int or not isinstance(group.get("instructions"), list):
                raise ValueError("malformed innerInstructions")
            outer_idx = group["index"]
            if not 0 <= outer_idx < len(outer):
                raise ValueError("inner instruction outer index out of range")
            for index, ix in enumerate(group["instructions"]):
                event, issue = _transfer(ix, keys, owner_map, result["mint"], signature,
                                         slot, when, avail, ref, fee_payer, outer_idx, index)
                if event:
                    if "event_id" in event:
                        # Should never happen: CPI token transfers are not standalone economic actions.
                        raise ValueError("inner token transfer incorrectly admitted")
                    audit["funding_events"].append(event)
                if issue:
                    audit["unresolved"].append({"signature": signature, "source_ref": ref, **issue})
                    result["coverage"] = {**result["coverage"], "complete": False}
        # A target-mint balance changed but no trusted direct event, or there are
        # other complex economic actions: never guess buy/sell from the delta.
        balances = (meta.get("preTokenBalances") or []) + (meta.get("postTokenBalances") or [])
        has_target = any(b.get("mint") == result["mint"] for b in balances if isinstance(b, dict))
        if has_target and not decoded_target:
            audit["unresolved"].append({"signature": signature, "source_ref": ref,
                                        "reason": "TARGET_MINT_ECONOMIC_ACTION_UNCLASSIFIED"})
            result["coverage"] = {**result["coverage"], "complete": False}
        if available > as_of:
            audit["unresolved"].append({"signature": signature, "source_ref": ref,
                                        "reason": "EVIDENCE_ARRIVED_AFTER_AS_OF"})
            result["coverage"] = {**result["coverage"], "complete": False}
    audit["decoded_target_transfers"] = len(result["events"])
    audit["coverage_downgraded"] = not result["coverage"]["complete"]
    # Enforce the precise downstream M01 event contract; reject bad payloads.
    validate_m01(result)
    result["adapter_audit"] = audit
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline raw getTransaction adapter; never contacts Solana RPC")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        transformed = normalize(json.loads(args.input.read_text(encoding="utf-8")))
        encoded = json.dumps(transformed, ensure_ascii=False, indent=2)
        if args.output:
            args.output.write_text(encoded + "\n", encoding="utf-8")
        print(encoded)
        return 0
    except (ValueError, TypeError, OSError, KeyError, OverflowError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc), "no_trading": True}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())