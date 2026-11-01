"""Read-only verified vendor-snapshot triage -> durable Grok analysis outbox.

This is NOT a live on-chain transaction detector, a wallet graph, an LLM client,
or a trade/alert score. No network, webhook, payment or wallet access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

ADDR = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
MAX_INPUT_BYTES = 3 * 1024 * 1024
REVIEW_LEVELS = {"warn", "danger", "error", "critical"}


def _raw(path: Path) -> bytes:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("input exceeds size cap")
    return path.read_bytes()


def _obj(raw: bytes, name: str) -> Any:
    try:
        return json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError(f"invalid JSON: {name}") from exc


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def triage(combined_raw: bytes, rug_raw: bytes, dex_raw: bytes) -> dict[str, Any]:
    """Only classify vendor labels after matching raw bytes and source identities."""
    report = _obj(combined_raw, "report")
    rug = _obj(rug_raw, "rugcheck")
    dex = _obj(dex_raw, "dex")
    _require(isinstance(report, dict) and isinstance(rug, dict) and isinstance(dex, list),
             "invalid report/source shapes")
    mint = report.get("mint")
    _require(isinstance(mint, str) and bool(ADDR.fullmatch(mint)), "invalid mint")
    _require(rug.get("mint") == mint, "mint mismatch: RugCheck")
    _require(report.get("schema_version") == "grok.mint_v01_combined.v0", "unsupported report schema")
    _require(report.get("status") and report.get("no_trading") is True, "report is not a read-only source")
    sources = report.get("source_status") or {}
    _require(isinstance(sources, dict) and sources.get("rugcheck_public_report") ==
             "RUGCHECK_CACHED_VENDOR_REPORT_NOT_INDEPENDENTLY_VERIFIED", "unexpected RugCheck source status")
    _require(sources.get("dex_public_pairs") == "PUBLIC_PROVIDER_PAIR_SNAPSHOT_UNVERIFIED_ONCHAIN",
             "unexpected DEX source status")
    r_report = report.get("rugcheck_public") or {}
    d_report = report.get("dex_public") or {}
    _require(isinstance(r_report, dict) and isinstance(d_report, dict), "missing normalized reports")
    _require((r_report.get("source") or {}).get("input_sha256") == _sha(rug_raw),
             "RugCheck source hash mismatch")
    _require(d_report.get("raw_input_sha256") == _sha(dex_raw), "DEX source hash mismatch")
    _require(d_report.get("mint") == mint and r_report.get("mint") == mint, "normalized mint mismatch")
    _require(d_report.get("returned_pair_count") == len(dex), "DEX pair count mismatch")
    for p in dex:
        _require(isinstance(p, dict) and p.get("chainId") == "solana" and
                 (isinstance(p.get("baseToken"), dict) and p["baseToken"].get("address") == mint or
                  isinstance(p.get("quoteToken"), dict) and p["quoteToken"].get("address") == mint),
                 "DEX pair has wrong chain/mint")

    processed_at = report.get("processed_at")
    _require(isinstance(processed_at, str) and processed_at, "report acquisition time missing")
    source_proofs = {
        "report_sha256": _sha(combined_raw),
        "rugcheck_sha256": _sha(rug_raw),
        "dex_sha256": _sha(dex_raw),
        "rugcheck_raw_source": (r_report.get("source") or {}).get("url"),
        "dex_raw_source": d_report.get("source_url"),
    }
    suppressed: list[dict[str, Any]] = []
    investigations: list[dict[str, Any]] = []

    holders = rug.get("topHolders")
    known = rug.get("knownAccounts")
    markets = rug.get("markets")
    _require(isinstance(holders, list) and isinstance(known, dict) and isinstance(markets, list),
             "RugCheck lacks required holder/market shapes")
    pool_addrs = {p.get("pairAddress") for p in dex if isinstance(p, dict)}
    for i, h in enumerate(holders[:200]):
        if not isinstance(h, dict):
            continue
        pct = h.get("pct")
        if isinstance(pct, bool) or not isinstance(pct, (int, float)) or pct < 5:
            continue
        token_acct, owner = h.get("address"), h.get("owner")
        internal_vault = any(isinstance(m, dict) and any(
            m.get(f"liquidity{x}") == token_acct and
            (m.get(f"liquidity{x}Account") or {}).get("mint") == mint and
            (m.get(f"liquidity{x}Account") or {}).get("owner") == owner and
            m.get("pubkey") == owner
            for x in ("A", "B")) for m in markets)
        known_type = (known.get(owner) or {}).get("type") if isinstance(known.get(owner), dict) else None
        if owner in pool_addrs and internal_vault and known_type == "AMM":
            suppressed.append({
                "candidate": "APPARENT_LARGE_HOLDER",
                "outcome": "POOL_INFRASTRUCTURE_EXPLANATION_SUPPRESSES_WHALE_ALERT",
                "pct_vendor": pct, "token_account": token_acct, "owner_vendor": owner,
                "evidence_paths": [f"rugcheck.topHolders[{i}]", "rugcheck.markets[*].liquidity{A|B}Account", "dex[*].pairAddress"],
                "limits": "vendor match, not independent RPC verification or LP beneficial ownership proof",
            })
        else:
            # No completed on-chain owner proof: keep this as an unresolved candidate, not an alert.
            suppressed.append({"candidate": "APPARENT_LARGE_HOLDER",
                               "outcome": "INSUFFICIENT_IDENTITY_EVIDENCE_NO_AUTOMATIC_WHALE_ALERT",
                               "pct_vendor": pct, "token_account": token_acct,
                               "evidence_paths": [f"rugcheck.topHolders[{i}]"],
                               "limits": "owner and pool role must be independently resolved"})

    risks = rug.get("risks")
    if risks is None:
        risks = []
    _require(isinstance(risks, list), "invalid vendor risk list")
    for i, entry in enumerate(risks[:50]):
        if not isinstance(entry, dict) or entry.get("level") not in REVIEW_LEVELS:
            continue
        name = entry.get("name")
        if not isinstance(name, str) or not 0 < len(name) < 120:
            continue
        event_type = "VENDOR_RISK_LABEL_REVIEW"
        event_id = hashlib.sha256((mint + "|" + event_type + "|" + str(i) + "|" + _sha(rug_raw)).encode()).hexdigest()[:24]
        investigations.append({
            "event_id": event_id, "mint": mint, "event_type": event_type,
            "source_kind": "VENDOR_RUGCHECK_CACHED_LABEL_NOT_ONCHAIN_EVENT",
            "vendor_label": name, "vendor_level": entry["level"],
            "vendor_score_unvalidated": entry.get("score"),
            "first_available_at": processed_at, "chain_slot": None,
            "chain_transaction_signature": None,
            "evidence_paths": [f"rugcheck.risks[{i}]"],
            "evidence_ref": "evidence.json",
            "review_state": "NEEDS_INDEPENDENT_CHECK_NOT_CONFIRMED_FRAUD",
            "candidate_specialist": "market_mechanism",
            "critic_condition": "Only if the specialist makes a causal or economic-control claim",
            "no_auto_trade": True,
        })

    return {
        "schema_version": "grok.vendor_triage.v1", "mint": mint, "processed_at": processed_at,
        "data_kind": "REAL_CACHED_VENDOR_SNAPSHOT_NOT_LIVE_TX_STREAM",
        "source_proofs": source_proofs,
        "coverage": {
            "token_snapshot": "VENDOR_CACHED_NOT_ATOMIC",
            "wallet_transactions": "NOT_OBSERVED",
            "funding_graph": "NOT_OBSERVED",
            "independent_rpc_owner": "NOT_VERIFIED",
            "insider_networks": "VENDOR_NETWORK_NOT_PROVEN_ABSENT",
        },
        "suppressed_candidates": suppressed,
        "investigations": investigations,
        "model_calls": 0, "external_calls_in_this_step": 0, "auto_payments": 0,
        "disposition": "PREPARE_GROK_TASKS_ONLY_NO_BOT_INVOKED",
    }


def write_outputs(out: Path, packet: dict[str, Any]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "evidence.json").write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for item in packet["investigations"]:
        (out / f"grok_task_{item['event_id']}.md").write_text(
            "# Grok 主 Bot｜真实供应商风险标签的只读研究任务\n\n"
            f"Mint: `{packet['mint']}`\nEvent ID: `{item['event_id']}`\n"
            "先读取同目录 evidence.json，并使用原始 RugCheck/DEX 报告核验字段与SHA。"
            "此事件只是供应商风险标签，不是已证实的链上异常交易。\n\n"
            "请独立识别问题、调用 `market_mechanism` Bot 或相关知识视角查明风险标签含义。"
            "只有出现重大控制权、内幕或操纵结论时才调用独立反证 Bot。"
            "须提交：可核查事实、竞争解释、缺失证据、是否值得继续观察、下一可观测事件。"
            "所有未知保持未知；不得以风险分断言诈骗、必跌或可交易。"
            "不得交易、签名、付款或自动安装未经审查的工具。\n\n"
            f"初步标签：`{item['vendor_label']}`；路径：`{item['evidence_paths'][0]}`。\n",
            encoding="utf-8")
    txt = ["# 程序生成的临时观察结论（非 Grok 分析结果）", "",
           f"Mint：`{packet['mint']}`", "",
           f"已完成原始数据哈希核验。待专业研究标签数：{len(packet['investigations'])}。",
           f"已抑制/降级大额 Holder 误报警候选数：{len(packet['suppressed_candidates'])}。", "",
           "当前没有真实单笔 SWAP、资金闭环或连续监控证据，不能据此判断庄家控制或可跟单收益。",
           "Grok Bot 尚未运行，专家意见和反证报告均为 **NOT_EXECUTED**。", ""]
    (out / "provisional_monitor_opinion.md").write_text("\n".join(txt), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Verified vendor snapshot -> Grok outbox (no network)")
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--rugcheck-raw", type=Path, required=True)
    p.add_argument("--dex-raw", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        packet = triage(_raw(args.report), _raw(args.rugcheck_raw), _raw(args.dex_raw))
        write_outputs(args.out_dir, packet)
    except (ValueError, OSError) as exc:
        p.exit(2, f"TRIAGE_REJECTED: {exc}\n")
    print(json.dumps({"status": packet["disposition"], "mint": packet["mint"],
                      "review_count": len(packet["investigations"]),
                      "suppressed_count": len(packet["suppressed_candidates"]),
                      "out_dir": str(args.out_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())