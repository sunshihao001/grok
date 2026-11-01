"""Solana official public RPC: top 20 *token accounts*, optional parsed owner hints.

A narrow read-only adapter (no SDK, private key, broadcast or automatic payment).
RPC owners can be PDAs, custody, pool vaults or programs: NOT 20 verified people.
The public endpoint is rate-limited and NOT a production monitoring backend.
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
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

RPC_URL = "https://api.mainnet.solana.com"
MAX_RESPONSE = 2 * 1024 * 1024
MINT_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
TOKEN_PROGRAMS = {
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "TokenzQdBNbLqP5VEhdkAS6EPFrcWhhS6zVoBeDq",
}


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("unexpected RPC HTTP redirect")


def valid_address(value: Any) -> bool:
    return isinstance(value, str) and bool(MINT_RE.fullmatch(value))


def rpc_request(method: str, params: list[Any], *, opener: Callable[..., Any] | None = None) -> bytes:
    """Only four allowlisted, read-only JSON-RPC methods to one fixed HTTPS host."""
    if method not in {"getTokenLargestAccounts", "getMultipleAccounts", "getSignaturesForAddress", "getTransaction"}:
        raise ValueError("unsupported read-only RPC method")
    request_bytes = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method,
                                "params": params}, separators=(",", ":")).encode("utf-8")
    req = Request(RPC_URL, data=request_bytes,
                  headers={"Content-Type": "application/json", "Accept": "application/json",
                           "User-Agent": "grok-solana-meme-readonly-v0.1"}, method="POST")
    fetch = opener or build_opener(RejectRedirects()).open
    with fetch(req, timeout=12) as response:
        if getattr(response, "status", 200) != 200:
            raise ValueError("unexpected RPC HTTP status")
        raw = response.read(MAX_RESPONSE + 1)
    if len(raw) > MAX_RESPONSE:
        raise ValueError("RPC response too large")
    return raw


def decode_rpc(raw: bytes) -> tuple[int, list[Any]]:
    try:
        envelope = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid Solana RPC JSON") from exc
    if not isinstance(envelope, dict) or envelope.get("jsonrpc") != "2.0":
        raise ValueError("invalid RPC envelope")
    if "error" in envelope:
        # No silent success on e.g. 429, -32005 or unsupported mint.
        error = envelope["error"]
        code = error.get("code") if isinstance(error, dict) else None
        raise ValueError(f"RPC error (code={code})")
    result = envelope.get("result")
    if not isinstance(result, dict):
        raise ValueError("RPC response missing result")
    ctx = result.get("context")
    slot = ctx.get("slot") if isinstance(ctx, dict) else None
    value = result.get("value")
    if type(slot) is not int or slot < 0 or not isinstance(value, list):
        raise ValueError("RPC context slot/value invalid")
    return slot, value


def collect(mint: str, *, request_fn: Callable[[str, list[Any]], bytes] = rpc_request,
            retrieved_at: str | None = None) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Query a maximum of 20 accounts; only source-verified token owner hints.

    The two RPC requests are necessarily from potentially different slots.
    `minContextSlot` prevents the second read from being *older* than the first;
    it does NOT make an atomic snapshot.
    """
    if not valid_address(mint):
        raise ValueError("invalid Solana Mint address")
    ts = retrieved_at or datetime.now(timezone.utc).isoformat()
    first_raw = request_fn("getTokenLargestAccounts", [mint, {"commitment": "finalized"}])
    first_slot, top = decode_rpc(first_raw)
    if len(top) > 20:
        raise ValueError("unexpected largest-account list exceeds 20")
    rows: list[dict[str, Any]] = []
    addresses: list[str] = []
    for i, entry in enumerate(top):
        if not isinstance(entry, dict) or not valid_address(entry.get("address")):
            raise ValueError("invalid token account address in RPC result")
        amount = entry.get("amount")
        decimals = entry.get("decimals")
        if not isinstance(amount, str) or not amount.isascii() or not amount.isdigit():
            raise ValueError("invalid raw token amount")
        if type(decimals) is not int or not 0 <= decimals <= 255:
            raise ValueError("invalid token decimals")
        token_account = entry["address"]
        if token_account in addresses:
            raise ValueError("duplicate largest token account")
        addresses.append(token_account)
        rows.append({"token_account": token_account, "amount_raw_at_first_slot": amount,
                     "decimals": decimals, "ui_amount_vendor": entry.get("uiAmountString"),
                     "owner_candidate": None, "owner_status": "UNKNOWN_NOT_RESOLVED",
                     "source_path": f"getTokenLargestAccounts.result.value[{i}]",
                     "owner_source_path": None})
    raw = {"largest-accounts-raw.json": first_raw}
    owner_slot = None
    lookup_error = None
    if rows:
        try:
            second_raw = request_fn("getMultipleAccounts", [
                addresses, {"encoding": "jsonParsed", "commitment": "finalized",
                            "minContextSlot": first_slot},
            ])
            raw["account-owners-raw.json"] = second_raw
            owner_slot, accounts = decode_rpc(second_raw)
            if owner_slot < first_slot or len(accounts) != len(rows):
                raise ValueError("account lookup slot/count incompatible with largest accounts")
            for i, (row, account) in enumerate(zip(rows, accounts)):
                if not isinstance(account, dict):
                    row["owner_status"] = "UNKNOWN_ACCOUNT_NOT_FOUND"
                    continue
                parsed = account.get("data")
                if not isinstance(parsed, dict) or parsed.get("program") not in ("spl-token", "spl-token-2022"):
                    row["owner_status"] = "UNKNOWN_UNSUPPORTED_TOKEN_ACCOUNT_DATA"
                    continue
                info = (parsed.get("parsed") or {}).get("info")
                if not isinstance(info, dict) or info.get("mint") != mint:
                    row["owner_status"] = "UNKNOWN_MINT_MISMATCH"
                    continue
                if account.get("owner") not in TOKEN_PROGRAMS:
                    row["owner_status"] = "UNKNOWN_UNEXPECTED_TOKEN_PROGRAM"
                    continue
                owner = info.get("owner")
                if not valid_address(owner):
                    row["owner_status"] = "UNKNOWN_OWNER_MISSING"
                    continue
                row["owner_candidate"] = owner
                row["owner_status"] = "RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER"
                row["owner_source_path"] = f"getMultipleAccounts.result.value[{i}].data.parsed.info.owner"
        except (ValueError, HTTPError, URLError, OSError, TimeoutError, TypeError) as exc:
            # Keep the original proven top-token-account sample, but never guess owners.
            lookup_error = str(exc)[:160]
            owner_slot = None
    status = ("EMPTY_TOP_TOKEN_ACCOUNT_SAMPLE_COVERAGE_UNKNOWN" if not rows
              else "PARTIAL_OWNER_LOOKUP_UNKNOWN" if lookup_error
              else "RPC_TOKEN_ACCOUNTS_AND_OWNER_HINTS")
    report = {
        "schema_version": "grok.public_token_accounts.v0", "status": status,
        "mint": mint, "chain": "solana", "retrieved_at": ts,
        "source": {"provider": "Solana Official Public Mainnet RPC", "url": RPC_URL,
                   "methods": ["getTokenLargestAccounts"] +
                              (["getMultipleAccounts"] if rows else []),
                   "commitment": "finalized",
                   "raw_sha256": {k: hashlib.sha256(v).hexdigest() for k, v in raw.items()}},
        "rpc_slot_largest": first_slot, "rpc_slot_owner_lookup": owner_slot,
        "same_slot_atomic_snapshot": False,
        "returned_token_accounts": len(rows), "rows": rows,
        "owner_lookup_error": lookup_error, "no_trading": True,
        "limits": [
            "TOP_20_TOKEN_ACCOUNTS_NOT_TOP_20_DISTINCT_WALLET_OWNERS",
            "OWNER_CAN_BE_PDA_POOL_VAULT_CUSTODIAN_OR_PROGRAM_NOT_HUMAN_CONTROLLER",
            "SLOTS_MAY_DIFFER_BALANCE_AND_OWNER_NOT_ATOMIC_SNAPSHOT",
            "NO_COMPLETE_HOLDER_SUPPLY_OR_DEV_HISTORY_OR_SWAP_EVIDENCE",
            "PUBLIC_RPC_RATE_LIMITED_DEVELOPMENT_ONLY",
        ],
    }
    return report, raw


def markdown(report: dict[str, Any]) -> str:
    out = ["# Mint｜Solana原生RPC账户候选（只读）", "",
           f"Mint：`{report['mint']}`；状态：**{report['status']}**",
           f"采集时间：`{report['retrieved_at']}`（非交易事件时间）",
           f"RPC finalized slot：`{report['rpc_slot_largest']}`；Owner查询slot：`{report['rpc_slot_owner_lookup']}`",
           "", "**注意：这里是余额前20的Token Account，不是前20个真实持有人。Owner可能是LP池、PDA、托管或程序地址。**", ""]
    for row in report["rows"]:
        out.append(f"- Token Account `{row['token_account']}`；原始数量 `{row['amount_raw_at_first_slot']}`；"
                   f"Owner候选 `{row['owner_candidate'] or 'UNKNOWN'}`；"
                   f"证据：`{row['source_path']}`、`{row['owner_source_path'] or 'none'}`；"
                   f"状态：`{row['owner_status']}`")
    if not report["rows"]:
        out.append("- 未返回Token Account，覆盖未知，不能推出没有持有人。")
    if report["owner_lookup_error"]:
        out.append("- Owner查询失败，所有Owner保持UNKNOWN；错误：" + report["owner_lookup_error"])
    out += ["", "## 不能得出的结论", "",
            "- 账户Owner不是最终受益人，也不能直接证明同源、庄家或交易行为。",
            "- 不同RPC slot不能作为原子库存快照，也不是实时信号可见时点。",
            "- 没有Dev历史、完整持有人、Swap事件、交易收益或持续监控。", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read only: public top 20 Solana token accounts and owner hints")
    parser.add_argument("--mint", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report, raw = collect(args.mint)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for filename, blob in raw.items():
            (args.out_dir / filename).write_bytes(blob)
        (args.out_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (args.out_dir / "report.md").write_text(markdown(report), encoding="utf-8")
        print(json.dumps({"status": report["status"], "mint": args.mint,
                          "report": str(args.out_dir / "report.md"), "no_trading": True}, ensure_ascii=False))
        return 0
    except (ValueError, HTTPError, URLError, OSError, TimeoutError, TypeError) as exc:
        print(json.dumps({"status": "RPC_UNAVAILABLE", "reason": str(exc), "no_trading": True}, ensure_ascii=False),
              file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
