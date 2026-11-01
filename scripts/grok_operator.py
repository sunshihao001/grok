#!/usr/bin/env python3
"""Operate a GPT-built offline release on Grok cloud: one entrypoint, no live calls."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Any

from grok_cloud_doctor import inspect

ROOT=Path(__file__).resolve().parents[1]
SHA40=re.compile(r"^[0-9a-f]{40}$")
MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


def _stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _check(repo: Path, sha: str | None, tests: bool, require_pin: bool) -> dict:
    report=inspect(repo,run_audits=True,run_tests=tests)
    if require_pin and not sha:
        raise ValueError("RELEASE_SHA_REQUIRED")
    if sha and (not SHA40.fullmatch(sha) or report.get("git_commit")!=sha):
        raise ValueError("RELEASE_SHA_MISMATCH")
    if report.get("status")!="PREFLIGHT_NOT_GROK_PROVISIONING":
        raise ValueError("ENVIRONMENT_AUDIT_FAILED")
    if report.get("git_worktree_dirty"):
        raise ValueError("TRACKED_WORKTREE_DIRTY")
    return report


def _call(repo: Path, module: str, *argv: str) -> dict[str, Any]:
    env=os.environ.copy()
    env["PYTHONPATH"]=str(repo/"src")
    try:
        p=subprocess.run([sys.executable,"-m",module,*argv],cwd=repo,env=env,
                         capture_output=True,text=True,check=False,timeout=20)
    except (OSError,subprocess.TimeoutExpired) as exc:
        raise ValueError("COMMAND_TIMEOUT_OR_UNAVAILABLE: "+module) from exc
    if p.returncode!=0:
        raise ValueError("COMMAND_FAILED: "+module+" "+str(p.returncode)+" "+
                         p.stderr[:400])
    if len(p.stdout)>200000:
        raise ValueError("OUTPUT_TOO_LARGE: "+module)
    try:
        result=json.loads(p.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("NON_JSON_OUTPUT: "+module) from exc
    if not isinstance(result,dict):
        raise ValueError("NON_OBJECT_OUTPUT: "+module)
    return result


def demo(repo: Path, expected_sha: str | None, test_suite: bool = True,
         persist: bool = True) -> dict[str, Any]:
    """Run pinned, synthetic offline smoke test in an isolated temporary dir."""
    repo=repo.resolve()
    result={
        "status":"OFFLINE_DEMO_FAILED","run_mode":"SYNTHETIC_FIXTURE_ONLY",
        "timestamp_utc":_stamp(),"git_sha":None,
        "checks":{},"grok_app_connected":False,
        "real_provider_connected":False,"okx_cli_executed":False,
        "grok_skill_installed":False,"production_monitor_enabled":False,
        "trading_authorized":False}
    try:
        doctor=_check(repo,expected_sha,tests=test_suite,require_pin=True)
        result["git_sha"]=doctor["git_commit"]
        result["checks"]["knowledge_audits"]={
            k:v["status"] for k,v in doctor["audits"].items()}
        result["checks"]["test_suite"]=doctor["offline_unittest"]
        work=repo/".runtime"
        work.mkdir(parents=True,exist_ok=True)
        with TemporaryDirectory(prefix="grok-demo-",dir=work) as folder:
            state=Path(folder)
            db=["--db",str(state/"handoffs.sqlite3")]
            init=_call(repo,"solana_meme_os.runtime_store",*db,"init")
            submit=_call(repo,"solana_meme_os.runtime_store",*db,"submit",
                         "--input","fixtures/bot-handoff-brief.fixture.json")
            b02=_call(repo,"solana_meme_os.runtime_store",*db,"claim","--bot","B02")
            b05=_call(repo,"solana_meme_os.runtime_store",*db,"claim","--bot","B05")
            again=_call(repo,"solana_meme_os.runtime_store",*db,"claim","--bot","B02")
            if [init["status"],submit["status"],b02["status"],b05["status"],again["status"]] != [
                "INITIALIZED","SUBMITTED","CLAIMED","CLAIMED","EMPTY"]:
                raise ValueError("RESEARCH_QUEUE_DEMO_FAILED")
            status=_call(repo,"solana_meme_os.runtime_store",*db,"status",
                         "--packet-id","FIXTURE-B01-001")
            states={x["recipient_bot_id"]:x["status"] for x in status["deliveries"]}
            if states!={"B02":"CLAIMED","B03":"PENDING","B05":"CLAIMED"}:
                raise ValueError("RESEARCH_DELIVERIES_MISMATCH")
            result["checks"]["handoff"]={"status":"FIXTURE_PASS",
                                         "recipient_states":states}
            okx=_call(repo,"solana_meme_os.okx_snapshot",
                      "--input","fixtures/okx-price.synthetic.json",
                      "--operation","token_price_info","--address",MINT)
            if (okx["status"]!="UNVERIFIED_PROVIDER_CAPTURE" or
                okx["eligible_as_live_monitor_input"] is not False or
                okx["payment_authorized"] is not False):
                raise ValueError("OKX_OFFLINE_FAIL_CLOSED_ASSERTION")
            result["checks"]["okx_parser"]={"status":"FIXTURE_PASS",
                                              "source_authenticated":False}
            opts=["--allow-fixture","--rules","rules/monitor.v0.json",
                  "--state-dir",str(state/"monitor")]
            a=_call(repo,"solana_meme_os.monitor","--input",
                    "fixtures/observation-1.json",*opts)
            b=_call(repo,"solana_meme_os.monitor","--input",
                    "fixtures/observation-2.json",*opts)
            types={x["type"] for x in b.get("alerts",[])}
            if (a.get("status")!="FIXTURE" or b.get("status")!="FIXTURE" or
                not {"LIQUIDITY_DROP","TOP10_SHARE_RISE"}.issubset(types) or
                a.get("no_trading") is not True or b.get("no_trading") is not True):
                raise ValueError("MONITOR_FIXTURE_ASSERTION")
            result["checks"]["monitor"]={"status":"FIXTURE_PASS",
                                          "alert_types":sorted(types)}
        result["status"]="OFFLINE_DEMO_PASSED"
    except (OSError,TypeError,KeyError,ValueError) as exc:
        result["error"]=str(exc)
    if persist:
        try:
            out_dir=repo/".runtime"
            out_dir.mkdir(exist_ok=True)
            tmp=out_dir/"grok-operator-last.tmp"
            dest=out_dir/"grok-operator-last.json"
            tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            os.replace(tmp,dest)
            result["report_file"]=str(dest)
        except OSError:
            result["report_file"]=None
    return result


def main() -> int:
    p=argparse.ArgumentParser(description="GPT-built, Grok-operated, offline-only runner")
    p.add_argument("--repo",type=Path,default=ROOT)
    p.add_argument("--expected-sha",help="full SHA provided from GPT-reviewed GitHub version")
    p.add_argument("command",choices=("status","preflight","demo"))
    args=p.parse_args()
    try:
        if args.command=="demo":
            result=demo(args.repo,args.expected_sha)
        elif args.command=="preflight":
            data=_check(args.repo,args.expected_sha,tests=False,require_pin=False)
            result={"status":"OFFLINE_PREFLIGHT_PASSED","git_sha":data["git_commit"],
                    "environment":data,"trading_authorized":False}
        else:
            result=inspect(args.repo)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result["status"] in {
            "OFFLINE_DEMO_PASSED","OFFLINE_PREFLIGHT_PASSED",
            "PREFLIGHT_NOT_GROK_PROVISIONING"} else 2
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({"status":"ERROR","reason":str(exc),
                          "trading_authorized":False},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
