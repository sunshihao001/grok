"""Offline cross-Mint holder-OWNER candidate overlap using saved V0.1 reports.

Inspired by existing holder-overlap business flows, NOT copied code.
This tool never calls an API, identifies people, or infers coordinated control.
A vendor top-holders list is a partial, potentially stale SAMPLE.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from .public_token_accounts import valid_address


def _report(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) > 5_000_000:
        raise ValueError("saved report exceeds safety limit")
    value = json.loads(raw)
    if (not isinstance(value, dict) or value.get("no_trading") is not True
            or not valid_address(value.get("mint"))):
        raise ValueError("expected a saved read-only Solana Mint report")
    rug = value.get("rugcheck_public")
    if rug is not None and not isinstance(rug, dict):
        raise ValueError("unexpected RugCheck section")
    holders = rug.get("top_holders") if rug else None
    if holders is not None and (not isinstance(holders, list) or len(holders) > 200):
        raise ValueError("invalid vendor top-holders sample")
    source = rug.get("source") if rug else None
    source = source if isinstance(source, dict) else {}
    return {
        "mint": value["mint"],
        "file": path.name,  # do not expose arbitrary private file paths
        "saved_report_sha256": hashlib.sha256(raw).hexdigest(),
        "retrieved_at": rug.get("retrieved_at") if rug else None,
        "vendor_detected_at": rug.get("vendor_detected_at") if rug else None,
        "rugcheck_source_sha256": source.get("input_sha256"),
        "rugcheck_status": (rug.get("top_holders_status") or "UNKNOWN_NOT_PROVIDED")
                           if rug else "UNAVAILABLE",
        "holders": holders,
        "pool_related_holder_candidates": value.get("pool_related_holder_candidates") or [],
        "cross_source_pool_owner_matches": value.get("cross_source_pool_owner_matches") or [],
    }


def _owner_sample(value: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, int]]:
    """Deduplicate by vendor owner; reject known pool-vault/locker candidates."""
    records: dict[str, dict[str, Any]] = {}
    counts = {"rows": 0, "no_owner": 0, "infrastructure": 0, "unclassified": 0}
    holders = value["holders"] or []
    excluded_accounts = set()
    excluded_owners = set()
    for r in value["pool_related_holder_candidates"]:
        if not isinstance(r, dict):
            continue
        if valid_address(r.get("holder_token_account")):
            excluded_accounts.add(r["holder_token_account"])
        if valid_address(r.get("holder_owner_vendor")):
            excluded_owners.add(r["holder_owner_vendor"])
    for r in value["cross_source_pool_owner_matches"]:
        if isinstance(r, dict) and valid_address(r.get("address")):
            excluded_owners.add(r["address"])
    for row in holders:
        counts["rows"] += 1
        if not isinstance(row, dict):
            continue
        owner = row.get("owner_candidate")
        token_account = row.get("token_account_candidate")
        if not valid_address(owner):
            counts["no_owner"] += 1
            continue
        if (row.get("role_interpretation") == "VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE"
                or str(row.get("vendor_known_account_type") or "").upper() in {"AMM", "LOCKER"}
                or token_account in excluded_accounts or owner in excluded_owners):
            counts["infrastructure"] += 1
            continue
        counts["unclassified"] += 1
        item = records.setdefault(owner, {"owner_candidate": owner, "token_account_candidates": [],
                                          "vendor_paths": [], "label": "UNCLASSIFIED_OWNER_CANDIDATE"})
        if valid_address(token_account) and token_account not in item["token_account_candidates"]:
            item["token_account_candidates"].append(token_account)
        item["vendor_paths"].append(row.get("source_path") or "UNKNOWN_HOLDER_PATH")
    return records, counts


def compare_saved_reports(paths: list[Path]) -> dict[str, Any]:
    if not 2 <= len(paths) <= 5:
        raise ValueError("compare 2 to 5 saved Mint reports")
    values = [_report(p) for p in paths]
    mints = [r["mint"] for r in values]
    if len(set(mints)) != len(mints):
        raise ValueError("distinct Mint reports required")
    samples: dict[str, dict[str, dict[str, Any]]] = {}
    summaries = []
    for v in values:
        records, counts = _owner_sample(v)
        # Missing or empty vendor sample cannot support a zero-overlap conclusion.
        usable = v["rugcheck_status"] == "VENDOR_CACHED_SAMPLE_UNVERIFIED" and bool(v["holders"])
        summaries.append({
            "mint": v["mint"],
            "saved_report_sha256": v["saved_report_sha256"],
            "rugcheck_source_sha256": v["rugcheck_source_sha256"],
            "rugcheck_status": v["rugcheck_status"],
            "retrieved_at": v["retrieved_at"],
            "vendor_detected_at": v["vendor_detected_at"],
            "sample_usable": usable,
            "sample_counts": counts,
            "unclassified_unique_owner_candidates": len(records),
            "source_is_vendor_cache_not_chain_owner_proof": True,
        })
        samples[v["mint"]] = records
    comparisons: list[dict[str, Any]] = []
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            a, b = summaries[i], summaries[j]
            owners_a, owners_b = samples[a["mint"]], samples[b["mint"]]
            comparable = a["sample_usable"] and b["sample_usable"]
            common = sorted(set(owners_a) & set(owners_b)) if comparable else []
            both = [
                {"owner_candidate": owner,
                 "mint_a": {"mint": a["mint"], **owners_a[owner]},
                 "mint_b": {"mint": b["mint"], **owners_b[owner]},
                 "interpretation": "SAME_VENDOR_OWNER_ADDRESS_IN_TWO_SAMPLED_MINTS_NOT_COMMON_OPERATOR_PROOF"}
                for owner in common
            ]
            comparisons.append({
                "mint_a": a["mint"], "mint_b": b["mint"],
                "comparison_status": "PARTIAL_VENDOR_SAMPLE_COMPARISON" if comparable else "UNKNOWN_SOURCE_COVERAGE",
                "shared_owner_candidates_count": len(common) if comparable else None,
                "shared_owner_candidates": both,
                "sampled_owner_count_a": len(owners_a) if comparable else None,
                "sampled_owner_count_b": len(owners_b) if comparable else None,
                "overlap_absence_proven": False,
                "same_economic_controller_proven": False,
                "sampling_bias": "RUGCHECK_TOP_HOLDER_CACHED_NON_RANDOM_PARTIAL_SAMPLE",
            })
    return {
        "schema_version": "grok.cross_mint_vendor_owner_overlap.v0",
        "status": "OFFLINE_VENDOR_CANDIDATE_COMPARISON_NOT_ENTITY_ATTRIBUTION",
        "read_only": True, "network_calls": 0, "no_trading": True,
        "source": "SAVED_MINT_V01_REPORTS_NOT_LIVE",
        "reports": summaries, "pairs": comparisons,
        "limitations": [
            "Vendor top-holders are partial and may be stale or retrieved at different times.",
            "Address overlap is an observed vendor candidate, not identity, beneficial ownership, funding flow, insider collusion or a profitable trading signal.",
            "Pool/AMM/locker candidates are excluded when detected, but unknown service infrastructure remains possible.",
            "No matches means not seen in sampled records; it never proves independent ownership.",
            "Owner labels come from a provider, not independent RPC state verification.",
        ],
    }


def markdown(report: dict[str, Any]) -> str:
    lines = ["# 多Mint持有人Owner候选重叠｜已存报告只读对照", "",
             "**不是资金同源图，也不能据此判定同一个庄家。**", "",
             "## 数据覆盖"]
    for r in report["reports"]:
        counts = r["sample_counts"]
        lines.append(
            f"- Mint \u0060{r['mint']}\u0060：{r['rugcheck_status']}；"
            f"Holder样本{counts['rows']}行，已排除基础设施{counts['infrastructure']}行，"
            f"未分类Owner候选{r['unclassified_unique_owner_candidates']}个；"
            f"来源获取时间\u0060{r['retrieved_at'] or 'UNKNOWN'}\u0060"
        )
    lines += ["", "## Mint两两比较"]
    for pair in report["pairs"]:
        lines.append(f"### {pair['mint_a']} × {pair['mint_b']}")
        if pair["shared_owner_candidates_count"] is None:
            lines.append("- 无法比较：一个或两个来源缺失/不可用；**不是零重叠**。")
        else:
            lines.append(f"- 已观测样本中相同Owner候选：**{pair['shared_owner_candidates_count']}**。"
                         "只代表这些有限样本的地址相同。")
            for row in pair["shared_owner_candidates"]:
                lines.append(f"  - \u0060{row['owner_candidate']}\u0060："
                             f"{', '.join(row['mint_a']['vendor_paths'])} ↔ "
                             f"{', '.join(row['mint_b']['vendor_paths'])}")
    lines += ["", "## 限制与竞争解释"]
    lines.extend(f"- {x}" for x in report["limitations"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare saved vendor holder candidates, no API")
    parser.add_argument("reports", nargs="+", type=Path, help="2 to 5 saved report.json files")
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--out-md", type=Path)
    args = parser.parse_args(argv)
    try:
        result = compare_saved_reports(args.reports)
        if args.out_json:
            args.out_json.parent.mkdir(parents=True, exist_ok=True)
            args.out_json.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        if args.out_md:
            args.out_md.parent.mkdir(parents=True, exist_ok=True)
            args.out_md.write_text(markdown(result), encoding="utf-8")
        print(json.dumps({"status": result["status"], "pairs": len(result["pairs"]),
                          "report": str(args.out_md) if args.out_md else None,
                          "no_trading": True}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, UnicodeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc), "no_trading": True},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
