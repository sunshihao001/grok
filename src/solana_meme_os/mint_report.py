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



def _records(value: Any) -> tuple[list[dict[str, Any]], str]:
    """Return vendor rows without pretending that missing/truncated pages are complete."""
    if value is None:
        return [], "UNKNOWN_NO_RESPONSE"
    rows = value if isinstance(value, list) else value.get("list") if isinstance(value, dict) else None
    if not isinstance(rows, list):
        return [], "UNSUPPORTED_RESPONSE_SHAPE"
    return [row for row in rows if isinstance(row, dict)], "RETURNED_SAMPLE_ONLY"


def _available(raw: Any) -> bool:
    return raw not in (None, "", "--", "null")


def summarize_business(source: dict[str, Any]) -> dict[str, Any]:
    """Make evidence-linked candidate lists from documented vendor fields only.

    This is a *presentation* layer: it does not infer verified trades, beneficial
    owner identity, investor PnL, or the completeness of a holder sample.
    """
    holders = source["structure"].get("holders")
    rows, holder_status = _records(holders)
    wallets = []
    funding_edges = []
    for index, row in enumerate(rows):
        wallet = row.get("holderWalletAddress")
        if not isinstance(wallet, str) or not MINT_RE.fullmatch(wallet):
            continue
        item = {"wallet": wallet, "hold_amount": row.get("holdAmount"),
                "hold_percent": row.get("holdPercent"),
                "realized_pnl_usd_vendor": row.get("realizedPnlUsd"),
                "source_path": f"data.structure.holders[{index}]",
                "evidence": "OKX_VENDOR_HOLDER_ROW_NOT_OWNER_VERIFIED"}
        wallets.append(item)
        funder = row.get("fundingSource")
        if isinstance(funder, str) and MINT_RE.fullmatch(funder):
            funding_edges.append({"from_vendor_funding_source": funder, "to_wallet": wallet,
                                  "source_path": f"data.structure.holders[{index}].fundingSource",
                                  "interpretation": "VENDOR_FUNDING_HINT_NOT_COMMON_CONTROLLER"})
    # Vendor API can return a capped slice; no 'top holders in the market' claim.
    cluster = source["structure"].get("cluster")
    if isinstance(cluster, list) and len(cluster) == 1 and isinstance(cluster[0], dict):
        cluster = cluster[0]
    candidates = []
    if isinstance(cluster, dict):
        descriptions = {
            "clusterConcentration": "供应商聚类集中度等级",
            "holderSameFundSourcePercent": "供应商定义的持有人之间资金往来指标",
            "holderSameCreationTimePercent": "供应商定义的近似创建时间指标",
            "holderNewAddressPercent": "供应商定义的新地址比例",
            "rugPullPercent": "供应商模型风险字段（非链上事件概率验证）",
        }
        for key, meaning in descriptions.items():
            if _available(cluster.get(key)):
                candidates.append({"kind": "VENDOR_STATISTIC_FOR_REVIEW", "field": key,
                                   "value": cluster[key], "meaning": meaning,
                                   "source_path": f"data.structure.cluster.{key}",
                                   "verified_abnormal": False})
    launchpad = source.get("launchpad")
    dev = launchpad.get("devInfo") if isinstance(launchpad, dict) else None
    bundle = launchpad.get("bundleInfo") if isinstance(launchpad, dict) else None
    top_traders, trader_status = _records(source["structure"].get("topTraders"))
    # Keep vendor timestamps with their JSON path instead of inventing a single
    # snapshot timestamp (parallel subrequests can have different times).
    hints = []
    def visit(value: Any, path: str, level: int) -> None:
        if len(hints) >= 30 or level > 3:
            return
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ("requestTime", "time") and isinstance(child, (int, str)) and _available(child):
                    hints.append({"source_path": f"{path}.{key}", "raw": child})
                elif key in ("info", "price", "contract", "security", "advancedInfo", "priceInfo"):
                    visit(child, f"{path}.{key}", level+1)
        elif isinstance(value, list):
            for i, child in enumerate(value[:2]):
                visit(child, f"{path}[{i}]", level+1)
    visit(source.get("core"), "data.core", 0)
    return {
        "key_wallet_candidates": wallets[:30],
        "holder_sample_rows": len(rows),
        "holder_sample_status": holder_status,
        "holder_coverage": "UNKNOWN_NOT_WHOLE_CHAIN; OKX holder endpoint capped at 100 per request",
        "funding_source_hints": funding_edges[:30],
        "vendor_cluster_statistics": candidates,
        "top_trader_sample_rows": len(top_traders),
        "top_trader_sample_status": trader_status,
        "developer_history_vendor_status": "PRESENT_UNVERIFIED" if dev is not None else "UNKNOWN_OR_NOT_REQUESTED",
        "bundle_vendor_status": "PRESENT_UNVERIFIED" if bundle is not None else "UNKNOWN_OR_NOT_REQUESTED",
        "per_field_source_time_hints": hints,
        "unanswered": [
            "主网真实TokenAccount与owner/LP/vault映射未独立核对",
            "资金来源字段不能证明同一实际控制者或最终受益人",
            "未获得已确认DEX成交指令、跨钱包库存流与持续监控事件",
            "Dev/Bundler供应商标签、历史覆盖和报告数据时效未独立核对",
        ],
    }


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
            "sections": entries, "business_summary": summarize_business(source),
            "no_trading": True,
            "notes": ["Supplier labels do not prove common beneficial ownership.",
                      "Null or missing is unknown, never zero or safe.",
                      "No historical coverage, wallet change, or real-time monitoring is established by this report."]}


def markdown(report: dict[str, Any]) -> str:
    out = ["# Solana Meme｜Mint只读研究报告（初版）", "",
           f"Mint：`{report['mint']}`", f"状态：**{report['status']}**",
           f"文件处理时间：{report['processed_at']}（**不是链上交易时间**）",
           f"来源：OKX OnchainOS token-research；输入SHA-256：`{report['source']['input_sha256']}`",
           "", "本报告没有执行交易，也不证明链上钱包归属、收益或异常群体已获核实。", ""]
    business = report["business_summary"]
    out += ["## 第一版业务摘要（仅为供应商候选，未独立验证）", "",
            f"持有人返回样本行数：{business['holder_sample_rows']}；覆盖状态：{business['holder_sample_status']}",
            f"可识别的钱包候选：{len(business['key_wallet_candidates'])}；资金来源提示：{len(business['funding_source_hints'])}",
            f"Dev历史：{business['developer_history_vendor_status']}；Bundle：{business['bundle_vendor_status']}",
            "注意：前100名/接口返回样本不等于全体持有人；这里没有确认钱包同控或真实买卖。", ""]
    for item in business["key_wallet_candidates"][:12]:
        out.append(f"- 钱包 `{item['wallet']}`；持有量（供应商）：{item['hold_amount'] or '未知'}；"
                   f"持仓占比（供应商）：{item['hold_percent'] or '未知'}；证据：`{item['source_path']}`")
    if business["funding_source_hints"]:
        out += ["", "### 资金来源候选（不可直接归为同一控制主体）", ""]
        for item in business["funding_source_hints"][:12]:
            out.append(f"- `{item['from_vendor_funding_source']}` → `{item['to_wallet']}` "
                       f"（OKX字段 `{item['source_path']}`）")
    if business["vendor_cluster_statistics"]:
        out += ["", "### 异常研究候选：供应商群体指标（尚未确证异常）", ""]
        for item in business["vendor_cluster_statistics"]:
            out.append(f"- {item['meaning']}：`{item['value']}`（`{item['source_path']}`）")
    out += ["", "### 时间与未知项", "",
            "供应商时间证据（原始字段，不自动当成全局同步快照）："]
    if business["per_field_source_time_hints"]:
        for hint in business["per_field_source_time_hints"]:
            out.append(f"- `{hint['source_path']}` = `{hint['raw']}`")
    else:
        out.append("- 未提供可识别的供应商请求/行情时间；报告生成时间并非数据时间。")
    out += ["", *["- " + x for x in business["unanswered"]], ""]
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