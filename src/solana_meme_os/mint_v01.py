"""One Solana Mint → read-only report. Mature OKX JSON or public DEX / RPC facts.

Public RPC token-account hints are opt-in; no keys, wallets, payments or trades.
Existing single-source CLI behavior remains unchanged for backwards compatibility.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from . import mint_report, public_pair_report, public_token_accounts, public_rugcheck_report


def combined(mint: str, out_dir: Path, *, okx_json: Path | None,
             fixture: bool, rpc_holders: bool, rugcheck: bool) -> int:
    """Independent evidence sections, never merge third-party wallet labels with RPC accounts."""
    now = datetime.now(timezone.utc).isoformat()
    try:
        public_token_accounts.valid_address(mint) or (_ for _ in ()).throw(
            ValueError("invalid Solana Mint address"))
        okx = None
        okx_raw = None
        if okx_json is not None:
            okx_raw = okx_json.read_bytes()
            okx = mint_report.compile_report(
                json.loads(okx_raw), mint, fixture=fixture,
                source_sha256=hashlib.sha256(okx_raw).hexdigest(), processed_at=now)
        pool = None
        pool_raw = None
        errors: dict[str, str] = {}
        try:
            pool_raw, endpoint = public_pair_report.fetch_pairs(mint)
            pool = public_pair_report.compile_pairs(pool_raw, mint, retrieved_at=now, source=endpoint)
        except (OSError, ValueError, TypeError) as exc:
            errors["public_pairs"] = str(exc)[:180]
        holders = None
        rpc_raw: dict[str, bytes] = {}
        if rpc_holders:
            try:
                holders, rpc_raw = public_token_accounts.collect(mint)
            except (OSError, ValueError, TypeError) as exc:
                errors["public_rpc_token_accounts"] = str(exc)[:180]
        rug = None
        rug_raw = None
        if rugcheck:
            try:
                rug_raw = public_rugcheck_report.fetch_report(mint)
                rug = public_rugcheck_report.compile_report(rug_raw, mint, retrieved_at=now)
            except (OSError, ValueError, TypeError) as exc:
                errors["rugcheck_public_report"] = str(exc)[:180]
        if okx is None and pool is None and holders is None and rug is None:
            raise ValueError("all read-only sources unavailable: " + str(errors))
        # Coverage is evidence-specific, and a saved OKX file is not live verified.
        result: dict[str, Any] = {
            "schema_version": "grok.mint_v01_combined.v0",
            "mint": mint, "chain": "solana",
            "status": "FIXTURE_WITH_PUBLIC_SOURCES" if fixture else
                      "READONLY_MULTISOURCE_CANDIDATES_NOT_FULL_MINT_INTELLIGENCE",
            "processed_at": now, "no_trading": True,
            "source_status": {
                "okx_saved_json": okx["status"] if okx else "NOT_SUPPLIED",
                "dex_public_pairs": pool["status"] if pool else "UNAVAILABLE",
                "solana_public_rpc_token_accounts": holders["status"] if holders else
                    ("UNAVAILABLE" if rpc_holders else "NOT_REQUESTED"),
                "rugcheck_public_report": rug["status"] if rug else
                    ("UNAVAILABLE" if rugcheck else "NOT_REQUESTED"),
            },
            "source_errors": errors,
            "okx_saved": okx, "dex_public": pool, "rpc_token_accounts": holders,
            "rugcheck_public": rug,
            "limitations": [
                "RPC_TOP_TOKEN_ACCOUNTS_NOT_VERIFIED_UNIQUE_HOLDERS",
                "DEX_PAIR_VOLUME_NOT_WALLET_TRADES",
                "OKX_VENDOR_LABELS_NOT_CONFIRMED_CONTROL_OR_PNL",
                "NO_DEV_HISTORY_WHEN_PROVIDER_HAS_NOT_RETURNED_IT",
                "CROSS_PROVIDER_TIMESTAMPS_NOT_ATOMIC_SNAPSHOT",
                "NO_WALLET_TRADING_AUTOPAYMENT_OR_MONITOR_DEPLOYMENT",
            ],
        }
        md = ["# Solana Meme｜Mint多来源只读报告 V0.1", "",
              f"Mint：`{mint}`", f"状态：**{result['status']}**",
              f"处理时间：`{now}`（不是统一链上事件时间）", "",
              "本报告仅将来源隔离并列展示，不会把池、Token Account及OKX钱包标签推断为同一经济主体。",
              "", "## 数据源实际覆盖", ""]
        for key, state in result["source_status"].items():
            md.append(f"- {key}: **{state}**" +
                      (f"（{errors[key]}）" if key in errors else ""))
        if pool:
            md += ["", "---", "", public_pair_report.render_markdown(pool)]
        if holders:
            md += ["", "---", "", public_token_accounts.markdown(holders)]
        if rug:
            md += ["", "---", "", public_rugcheck_report.markdown(rug)]
        if okx:
            md += ["", "---", "", mint_report.markdown(okx)]
        md += ["", "## 尚未完成的业务能力", "",
               "- Dev真实历史、资金闭环、协议级Swap、持续异常和可交易收益都需独立来源/验证。",
               "- RPC公共节点受限且没有生产SLA；任何一个来源失败时不得填0或宣称无事件。",
               ""]
        out_dir.mkdir(parents=True, exist_ok=True)
        if pool_raw is not None:
            (out_dir / "dex-provider-raw.json").write_bytes(pool_raw)
        for filename, blob in rpc_raw.items():
            (out_dir / ("rpc-" + filename)).write_bytes(blob)
        if okx_raw is not None:
            (out_dir / "okx-saved-input.json").write_bytes(okx_raw)
        if rug_raw is not None and rug is not None:
            (out_dir / "rugcheck-provider-raw.json").write_bytes(rug_raw)
        (out_dir / "report.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / "report.md").write_text("\n".join(md), encoding="utf-8")
        print(json.dumps({"status": result["status"], "mint": mint,
                          "sources": result["source_status"],
                          "report": str(out_dir / "report.md"), "no_trading": True}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc), "no_trading": True}, ensure_ascii=False),
              file=sys.stderr)
        return 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="V0.1 one Mint → sourced read-only report")
    parser.add_argument("mint", help="Solana token Mint address")
    parser.add_argument("--out-dir", type=Path, help="Default .runtime/mint-v0.1/<mint>")
    parser.add_argument("--okx-json", type=Path, help="Already saved, authorized OKX token-research JSON")
    parser.add_argument("--fixture", action="store_true", help="Explicitly mark synthetic saved OKX JSON")
    parser.add_argument("--rpc-holders", action="store_true",
                        help="Opt-in: public Solana RPC top 20 token accounts / parsed owner hints (rate-limited)")
    parser.add_argument("--rugcheck", action="store_true",
                        help="Opt-in: cached no-key RugCheck GET for vendor Holder, Creator and risk hints")
    args = parser.parse_args(argv)
    if args.fixture and not args.okx_json:
        parser.error("--fixture only applies to --okx-json")
    dest = args.out_dir or Path(".runtime") / "mint-v0.1" / args.mint
    if args.rpc_holders or args.rugcheck:
        return combined(args.mint, dest, okx_json=args.okx_json, fixture=args.fixture,
                        rpc_holders=args.rpc_holders, rugcheck=args.rugcheck)
    if args.okx_json:
        flags = ["--mint", args.mint, "--okx-json", str(args.okx_json), "--out-dir", str(dest)]
        if args.fixture:
            flags.append("--fixture")
        return mint_report.main(flags)
    return public_pair_report.main(["--mint", args.mint, "--out-dir", str(dest)])


if __name__ == "__main__":
    raise SystemExit(main())
