"""Joined, offline read-only Mint report and ORIGINAL expertise excerpts.

This adapter only reads a saved report.json produced by existing mint_v01.
No RPC, wallet, swaps, payment, model claims, or Grok Bot are invoked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from . import project_navigator


def build_brief(report_file: Path, question: str, *,
                intent: str | None = None,
                navigator_root: Path = project_navigator.ROOT) -> dict[str, Any]:
    """Expose actual report status and real original source sections together."""
    if not question or not question.strip():
        raise ValueError("a natural-language question is required")
    raw = report_file.read_bytes()
    if len(raw) > 5_000_000:
        raise ValueError("saved report exceeds safety limit")
    report = json.loads(raw)
    if not isinstance(report, dict) or report.get("no_trading") is not True:
        raise ValueError("expected a no_trading saved report.json")
    if not isinstance(report.get("source_status"), dict) or not isinstance(report.get("mint"), str):
        raise ValueError("saved Mint report missing required fields")
    navigation = project_navigator.load_navigation(
        navigator_root / "knowledge/system/knowledge-navigation.v1.json")
    route = project_navigator.shortlist(question, navigation, limit=2, intent=intent)
    sections: list[dict[str, Any]] = []
    paths_seen: set[str] = set()
    for choice in route["routes"]:
        # Prefer original specialized knowledge, never read all 152 questions by default.
        for path in choice["knowledge_paths_on_current_branch"][:2]:
            if path in paths_seen:
                continue
            paths_seen.add(path)
            section = project_navigator.relevant_knowledge_section(
                path, question, navigation, root=navigator_root, max_chars=900)
            sections.append(section)
            if len(sections) >= 3:
                break
        if len(sections) >= 3:
            break
    errors = report.get("source_errors", {})
    if not isinstance(errors, dict):
        errors = {"saved_report": "SOURCE_ERROR_SHAPE_UNAVAILABLE"}
    statuses = dict(report["source_status"])
    unknowns = [f"{key}:{status}" for key, status in statuses.items()
                if status in ("NOT_SUPPLIED", "NOT_REQUESTED", "UNAVAILABLE", "ERROR")
                or "UNKNOWN" in str(status)]
    # Real provider observations are relayed verbatim, not upgraded to identity.
    matches = report.get("pool_related_holder_candidates") or []
    if not isinstance(matches, list):
        matches = []
    return {
        "status": "OFFLINE_REPORT_PLUS_ORIGINAL_KNOWLEDGE_CONTEXT",
        "read_only": True, "live_api_called": False, "grok_bot_called": False,
        "question": question, "mint": report["mint"],
        "saved_report_status": report.get("status", "UNKNOWN"),
        "saved_report_sha256": hashlib.sha256(raw).hexdigest(),
        "source_status_from_saved_report": statuses,
        "source_errors_from_saved_report": errors,
        "unknown_source_coverage": unknowns,
        "pool_related_holder_candidates_unverified": matches[:12],
        "knowledge_route_candidates": route["routes"],
        "original_knowledge_sections": sections,
        "limitations": [
            "Offline inspection of an already saved vendor report; not a fresh query.",
            "Text selection uses lexical overlap; not a verified explanation or economic identity.",
            "TokenAccount/owner/pool matching cannot prove common controller or whale status.",
            "Expert IDs identify reference perspectives, not deployed or invoked Grok Bots.",
            "Missing or inaccessible sources are UNKNOWN, not negative evidence.",
        ],
    }


def render_markdown(brief: dict[str, Any]) -> str:
    lines = [
        "# Solana Meme｜只读报告与专业知识关联",
        "",
        f"Mint：\u0060{brief['mint']}\u0060",
        f"原报告状态：\u0060{brief['saved_report_status']}\u0060",
        "本次仅阅读**已保存**的报告与原有研究文档，**没有重新查询链上数据或调用Grok Bot**。",
        "",
        "## 原报告的数据来源",
    ]
    for name, state in brief["source_status_from_saved_report"].items():
        lines.append(f"- {name}: \u0060{state}\u0060")
    if brief["unknown_source_coverage"]:
        lines += ["", "## 尚不可确定或缺失"]
        lines.extend(f"- {u}" for u in brief["unknown_source_coverage"])
    lines += ["", "## 原知识文件中可供研究的段落"]
    valid = 0
    for s in brief["original_knowledge_sections"]:
        if s["match_status"] != "ORIGINAL_SECTION_LEXICAL_CANDIDATE":
            continue
        valid += 1
        lines += ["", f"### {s['source_path']}:{s['line_start']}-{s['line_end']}",
                  f"原始SHA256：\u0060{s['source_sha256']}\u0060",
                  "以下是原文件文本片段，**不是新生成的市场结论**：", ""]
        lines.extend("> " + line for line in s["excerpt"].splitlines())
    if not valid:
        lines += ["", "没有可靠命中的原文段落，需要AI进一步检索、提问或研究，而不是猜测。"]
    lines += ["", "## 使用限制"]
    lines.extend(f"- {x}" for x in brief["limitations"])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Join saved Mint report and original knowledge, offline")
    parser.add_argument("--report-json", type=Path, required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--intent", help="Explicit navigation intent; otherwise literal candidates")
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--out-md", type=Path)
    args = parser.parse_args(argv)
    try:
        brief = build_brief(args.report_json, args.question, intent=args.intent)
        if args.out_json:
            args.out_json.parent.mkdir(parents=True, exist_ok=True)
            args.out_json.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n",
                                     encoding="utf-8")
        if args.out_md:
            args.out_md.parent.mkdir(parents=True, exist_ok=True)
            args.out_md.write_text(render_markdown(brief), encoding="utf-8")
        print(json.dumps(brief, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "ERROR", "reason": str(exc), "read_only": True},
                         ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
