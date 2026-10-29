#!/usr/bin/env python3
"""Offline-only acceptance check for a cloned Solana Meme Workflow OS repo.

Does not connect to wallets, GMGN, external APIs or create Grok Bots/Routines.
Runs only deterministic local read-only research commands and fixture cases.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "AGENTS.md", "BOTS.md", "CONTEXT.md",
    "knowledge/catalog.v1.json", "knowledge/source_index.v1.json",
    "knowledge/legacy-snapshots/manifest.json", "rules/monitor.v0.json",
    "src/solana_meme_os/knowledge.py", "src/solana_meme_os/research.py",
    "src/solana_meme_os/monitor.py", "fixtures/observation-1.json",
    "fixtures/observation-2.json", "tests/test_monitor.py",
)


def run(*args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args], cwd=ROOT, env=env,
        text=True, capture_output=True, timeout=120, check=False,
    )


def check_json(name: str, args: list[str], env: dict[str, str], validator: Any) -> dict[str, Any]:
    try:
        proc = run(*args, env=env)
        if proc.returncode:
            return {"name": name, "passed": False, "reason": f"exit_{proc.returncode}",
                    "stderr_tail": proc.stderr[-500:]}
        parsed = json.loads(proc.stdout)
        if not validator(parsed):
            return {"name": name, "passed": False, "reason": "unexpected_output_schema"}
        return {"name": name, "passed": True}
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, TypeError, ValueError) as exc:
        return {"name": name, "passed": False, "reason": type(exc).__name__}


def assess() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    required_missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    checks.append({"name": "required_files", "passed": not required_missing,
                   "missing": required_missing})
    checks.append({"name": "python_3_11_plus", "passed": sys.version_info >= (3, 11),
                   "python_version": sys.version.split()[0]})
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if not required_missing and sys.version_info >= (3, 11):
        try:
            proc = run("-m", "unittest", "discover", "-s", "tests", "-v", env=env)
            checks.append({"name": "offline_unit_tests", "passed": proc.returncode == 0,
                           "result_tail": (proc.stderr or proc.stdout)[-1200:]})
        except (OSError, subprocess.TimeoutExpired) as exc:
            checks.append({"name": "offline_unit_tests", "passed": False,
                           "reason": type(exc).__name__})

        checks.append(check_json("knowledge_lookup", ["-m", "solana_meme_os.knowledge",
            "--question", "这批钱包资金同源吗？"], env,
            lambda j: j.get("route_status") == "MATCHED_REFERENCE" and bool(j.get("references"))))

        checks.append(check_json("on_demand_research", ["-m", "solana_meme_os.research",
            "--question", "同源资金是不是交易所hub，如何排除共同基础设施？"], env,
            lambda j: (j.get("reference_status") == "SOURCES_INDEXED"
                       and bool(j.get("sources")) and j.get("research_status") == "EVIDENCE_REQUIRED"
                       and not j.get("observations", {}).get("accepted"))))

        with tempfile.TemporaryDirectory(prefix="grok-cloud-fixture-") as tmp:
            state_dir = str(Path(tmp) / "state")
            args = ["-m", "solana_meme_os.monitor", "--allow-fixture",
                    "--state-dir", state_dir]
            checks.append(check_json("fixture_baseline", [*args, "--input",
                "fixtures/observation-1.json"], env,
                lambda j: j.get("status") == "FIXTURE" and j.get("no_trading") is True))
            checks.append(check_json("fixture_deltas", [*args, "--input",
                "fixtures/observation-2.json"], env,
                lambda j: (j.get("status") == "FIXTURE" and j.get("no_trading") is True
                           and {"LIQUIDITY_DROP", "TOP10_SHARE_RISE"}.issubset(
                               {a.get("type") for a in j.get("alerts", [])})
                           and bool(j.get("knowledge", {}).get("interpretation_candidates")))))
    failed = [x["name"] for x in checks if not x["passed"]]
    return {
        "readiness": "OFFLINE_READY" if not failed else "OFFLINE_NOT_READY",
        "scope": "offline_fixture_and_knowledge_only",
        "checks": checks,
        "failed_checks": failed,
        "gmgn_cli_on_path": bool(shutil.which("gmgn-cli")),
        "gmgn_live_mapping_verified": False,
        "grok_skill_published_verified": False,
        "grok_routine_running_verified": False,
        "warning": ("Passing checks do NOT verify live market data, GMGN field semantics, "
                    "source recency, economic edge or Grok Bot provisioning."),
    }


def main() -> int:
    result = assess()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["readiness"] == "OFFLINE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
