"""Minimal, read-only Mint report from an existing OKX OnchainOS token-research result.

This program does not install, invoke, or authenticate to OKX and never uses a
wallet, trading endpoint, or chain RPC. Supplying a saved result is explicit.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

MINT_RE = re.compile(r"[1-9A-HJ-NP-Za-km-z]{32,44}")
SECTIONS = (
    ("代币与市场基础", "core", "info"),
    ("报价与流动性", "core", "price"),
    ("合约与权限信息", "core", "contract"),
    ("供应商安全检查", "core", "security"),
    ("持有人", "structure", "holders"),
    ("地址群体（供应商标签）", "structure", "cluster"),
    ("Top Trader（供应商标签）", "structure", "topTraders"),
    ("Smart Money信号（供应商标签）", "structure", "signals"),
)


def compile_report(envelope: dict[str, Any], mint: str, *, fixture: bool,
                   source_sha256: str, processed_at: str) -> dict[str, Any]:
    if not MINT_RE.fullmatch(mint):
        raise ValueError("invalid Solana Mint address")
    if not isinstance(envelope, dict) or envelope.get("ok") is not True:
        raise ValueError("source is not a successful OKX CLI JSON result")
    source = envelope.get("data")
    if not isinstance(source, dict) or source.get("workflow") != "token-research":
        raise ValueError("expected OKX workflow token-research data")
    if source.get("address") != mint:
        raise ValueError("Mint differs from the OKX response address")
    if str(source.get("chain")) not in {"501", "solana"}:
        raise ValueError("expected the Solana chain (501)")
    if not isinstance(source.get("core"), dict) or not isinstance(source.get("structure"), dict):
        raise ValueError("missing OKX core/structure objects")
    if all(source["core"].get(k) is None for k in ("info", "price", "contract", "security")):
        raise ValueError("all OKX core fields are null; not a meaningful report")
    # Preserve vendor values and nulls exactly. No derived owner/control/trade facts.
    entries = []
    for title, parent, field in SECTIONS:
        value = source[parent].get(field)
        entries.append({"title": title, "source_path": f"data.{parent}.{field}",
                        "status": "UNKNOWN" if value is None else "PRESENT_UNVERIFIED",
                        "value": value})
    launch = source.get("launchpad")
    entries.append({"title": "发行平台/Dev/Bundle（供应商信息）", "source_path": "data.launchpad",
                    "status": "UNKNOWN_OR_NOT_APPLICABLE" if launch is None else "PRESENT_UNVERIFIED",
                    "value": launch})
    return {"schema_version": "grok.mint_report.preview.v0", "mint": mint, "chain": "solana",
            "status": "FIXTURE_DEMO_ONLY" if fixture else "VENDOR_JSON_NOT_CHAIN_VERIFIED",
            "processed_at": processed_at, "chain_event_time": None,
            "vendor_data_time": None, "source": {"provider": "OKX OnchainOS",
            "workflow": "token-research", "input_sha256": source_sha256},
            "sections": entries, "no_trading": True,
            "notes": ["Supplier labels do not prove common beneficial ownership.",
                      "Null or missing is unknown, never zero or safe.",
                      "No historical coverage, wallet change, or real-time monitoring is established by this report."]}


def markdown(report: dict[str, Any]) -> str:
    out = ["# Solana Meme｜Mint只读研究报告（初版）", "",
           f"Mint：`{report['mint']}`", f"状态：**{report['status']}**",
           f"文件处理时间：{report['processed_at']}（**不是链上交易时间**）",
           f"来源：OKX OnchainOS token-research；输入SHA-256：`{report['source']['input_sha256']}`",
           "", "本报告没有执行交易，也不证明链上钱包归属、收益或异常群体已获核实。", ""]
    for entry in report["sections"]:
        out += [f"## {entry['title']}", "", f"来源字段：`{entry['source_path']}`",
                f"数据状态：**{entry['status']}**", ""]
        if entry["value"] is None:
            out += ["未知或未提供；不等于0。", ""]
        else:
            payload = json.dumps(entry["value"], ensure_ascii=False, indent=2)
            # Avoid implying a shortened display is full source evidence.
            if len(payload) > 2400:
                payload = payload[:2400] + "\n... [显示已截断，完整数据见report.json]"
            out += ["```json", payload, "```", ""]
    out += ["## 当前尚不能得出的结论", "", "- 不能根据供应商Cluster/Bundle标签直接判定同一经济主体。",
            "- 不能把Token Transfer或持有人余额变化自动认定为BUY/SELL。",
            "- 本报告尚未构成持续钱包监控、真实库存对账或异常交易信号。", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Offline-only report adapter for OKX token-research JSON")
    p.add_argument("--mint", required=True)
    p.add_argument("--okx-json", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--fixture", action="store_true", help="Mark synthetic source data; never claim live")
    args = p.parse_args(argv)
    try:
        raw = args.okx_json.read_bytes()
        envelope = json.loads(raw)
        result = compile_report(envelope, args.mint, fixture=args.fixture,
                                source_sha256=hashlib.sha256(raw).hexdigest(),
                                processed_at=datetime.now(timezone.utc).isoformat())
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.out_dir / "report.md").write_text(markdown(result), encoding="utf-8")
        print(json.dumps({"status": result["status"], "mint": args.mint,
                          "report_json": str(args.out_dir / "report.json"),
                          "report_md": str(args.out_dir / "report.md"),
                          "no_trading": True}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc), "no_trading": True}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())