"""Opt-in, read-only Solana Mint market-pair snapshot via public DEX Screener.

An alternative when OKX token-research credentials are unavailable, NOT a
replacement for OKX holder, funding, developer history, or transaction evidence.
No wallet, API key, POST, transaction, or automatic payment code exists here.
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
from urllib.request import Request, build_opener, HTTPRedirectHandler

MINT_RE = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
HOST = "api.dexscreener.com"
MAX_BYTES = 2 * 1024 * 1024


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("unexpected redirect from public read-only provider")


def source_url(mint: str) -> str:
    if not isinstance(mint, str) or MINT_RE.fullmatch(mint) is None:
        raise ValueError("invalid Solana Mint (base58 length 32–44)")
    return f"https://{HOST}/token-pairs/v1/solana/{mint}"


def fetch_pairs(mint: str, *, opener: Callable[..., Any] | None = None) -> tuple[bytes, str]:
    """Fetch a capped single public GET; never attach secrets or follow redirects."""
    url = source_url(mint)
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "grok-readonly-mint-v0.1"}, method="GET")
    fetch = opener or build_opener(_RejectRedirects()).open
    with fetch(request, timeout=12) as response:
        if hasattr(response, "status") and response.status != 200:
            raise ValueError(f"provider HTTP status {response.status}")
        raw = response.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError("provider response too large")
        return raw, url


def compile_pairs(raw: bytes, mint: str, *, retrieved_at: str, source: str) -> dict[str, Any]:
    source_url(mint)
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("provider returned invalid JSON") from exc
    if not isinstance(data, list):
        raise ValueError("unexpected DEX Screener response; expected list")
    if len(data) > 200:
        raise ValueError("provider returned excessive pairs")
    result = []
    seen = set()
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError("invalid pair entry")
        if row.get("chainId") != "solana":
            raise ValueError("cross-chain pair in Solana response")
        base, quote = row.get("baseToken"), row.get("quoteToken")
        if not isinstance(base, dict) or not isinstance(quote, dict):
            raise ValueError("pair has no base/quote token fields")
        if mint not in (base.get("address"), quote.get("address")):
            raise ValueError("pair does not contain the requested Mint")
        pool = row.get("pairAddress")
        if not isinstance(pool, str) or MINT_RE.fullmatch(pool) is None:
            raise ValueError("missing or invalid pool address")
        if pool in seen:
            continue
        seen.add(pool)
        is_base = base.get("address") == mint
        # DEX Screener priceUsd measures the BASE token; never transpose it to the quote.
        result.append({
            "pool": pool,
            "dex": row.get("dexId"),
            "target_token_role": "BASE" if is_base else "QUOTE",
            "token_symbol": (base if is_base else quote).get("symbol"),
            "price_usd_for_target": row.get("priceUsd") if is_base else None,
            "price_status": "VENDOR_BASE_PRICE" if is_base else "UNKNOWN_QUOTE_TOKEN_PRICE",
            "pool_liquidity_usd": (row.get("liquidity") or {}).get("usd") if isinstance(row.get("liquidity"), dict) else None,
            "pair_transactions_24h": (row.get("txns") or {}).get("h24") if isinstance(row.get("txns"), dict) else None,
            "pair_volume_24h_usd": (row.get("volume") or {}).get("h24") if isinstance(row.get("volume"), dict) else None,
            "pool_created_at_ms": row.get("pairCreatedAt"),
            "source_path": f"root[{i}]",
            "data_basis": "DEX_SCREENER_POOL_LEVEL_VENDOR_METRICS_NOT_WALLET_EVENTS",
        })
    return {
        "schema_version": "grok.public_pair_preview.v0",
        "mint": mint,
        "chain": "solana",
        "status": "PUBLIC_PROVIDER_PAIR_SNAPSHOT_UNVERIFIED_ONCHAIN" if result else "NO_PAIRS_RETURNED_COVERAGE_UNKNOWN",
        "provider": "DEX Screener",
        "source_url": source,
        "retrieved_at": retrieved_at,
        "vendor_data_time": None,
        "raw_input_sha256": hashlib.sha256(raw).hexdigest(),
        "returned_pair_count": len(result),
        "pairs": result,
        "not_available": {
            "key_wallets": "UNKNOWN_NOT_PROVIDED",
            "holder_balances_and_owners": "UNKNOWN_NOT_PROVIDED",
            "funding_relationships": "UNKNOWN_NOT_PROVIDED",
            "developer_history": "UNKNOWN_NOT_PROVIDED",
            "bundles_and_collusion": "UNKNOWN_NOT_PROVIDED",
            "verified_trades_and_inventory": "UNKNOWN_NOT_PROVIDED",
        },
        "no_trading": True,
        "notes": [
            "This is real provider pair data ONLY if fetched successfully from the live API.",
            "Retrieved-at is local time, not an on-chain event timestamp.",
            "Pool creation time is not necessarily Mint creation time.",
            "DEX Screener pair buy/sell counts do not identify buyer wallets or swaps.",
            "A missing or empty response does not prove no pools or no transactions.",
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    out = ["# Solana Meme｜真实公开数据池快照（限功能版）", "",
           f"Mint：`{report['mint']}`", f"状态：**{report['status']}**",
           f"数据源：{report['provider']}", f"请求地址：`{report['source_url']}`",
           f"取得时间：{report['retrieved_at']}（不是链上事件时间）",
           f"原始响应SHA256：`{report['raw_input_sha256']}`", "",
           "**此报告仅验证DEX池数据来源，不代表已完成钱包/资金/Dev研究。**", "",
           f"## 返回交易池（{report['returned_pair_count']}）", ""]
    if not report["pairs"]:
        out += ["没有返回交易池；原因及数据覆盖未知，不能断言该Mint没有池。", ""]
    for p in report["pairs"]:
        out += [f"### {p['dex']} · `{p['pool']}`", "",
                f"目标Mint角色：{p['target_token_role']}；报价（仅目标作为base时）：{p['price_usd_for_target']}",
                f"池流动性USD：{p['pool_liquidity_usd']}；池24小时成交量USD：{p['pair_volume_24h_usd']}",
                f"池24小时交易次数（供应商）：{p['pair_transactions_24h']}",
                f"池创建时间(ms)：{p['pool_created_at_ms']}（**不等于Mint创建时间**）", ""]
    out += ["## 未提供的重要业务能力", ""]
    out += [f"- {k}: {v}" for k,v in report["not_available"].items()]
    out += ["", "本工具未进行签名、转账、交易、付款或钱包连接。", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Public read-only DEX Screener pair preview for a Solana Mint")
    p.add_argument("--mint", required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        raw, url = fetch_pairs(args.mint)
        report = compile_pairs(raw, args.mint,
                               retrieved_at=datetime.now(timezone.utc).isoformat(), source=url)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "provider-raw.json").write_bytes(raw)
        (args.out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "report.md").write_text(render_markdown(report), encoding="utf-8")
        print(json.dumps({"status": report["status"], "pairs": report["returned_pair_count"],
                          "raw": str(args.out_dir / "provider-raw.json"),
                          "report": str(args.out_dir / "report.md"), "no_trading": True}, ensure_ascii=False))
        return 0 if report["pairs"] else 2
    except (ValueError, HTTPError, URLError, OSError, TimeoutError, TypeError) as exc:
        print(json.dumps({"status":"UNAVAILABLE", "reason":str(exc), "no_trading":True}, ensure_ascii=False), file=sys.stderr)
        return 3

if __name__ == "__main__":
    raise SystemExit(main())