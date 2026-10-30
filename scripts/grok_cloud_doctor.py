#!/usr/bin/env python3
"""Local/cloud Grok runtime preflight: no network, installations, credentials or trades.

Checks the *current Python execution environment*. It cannot infer a user's actual
Grok Bot permissions, create Grok Bots, validate RPC data, or open a cloud browser.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

REQUIRED = (
    "AGENTS.md", "BOTS.md",
    "src/solana_meme_os/runtime_store.py",
    "src/solana_meme_os/bot_knowledge.py",
    "knowledge/bot-handoff.schema.json",
    "knowledge/transfer/curriculum.v1.json",
    "skills/research-intake/SKILL.md",
    "fixtures/bot-handoff-brief.fixture.json",
)
CHECK_MODULES = (
    ("knowledge_system", "solana_meme_os.knowledge_system"),
    ("bot_knowledge", "solana_meme_os.bot_knowledge"),
    ("knowledge_delivery", "solana_meme_os.knowledge_delivery"),
)


def _command(argv: list[str], cwd: Path, env: dict[str, str] | None = None,
             timeout: int = 15) -> dict[str, object]:
    try:
        r = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                           text=True, timeout=timeout, check=False)
        return {"exit_code":r.returncode, "stdout":r.stdout[:200000],
                "stderr":r.stderr[:2000]}
    except (OSError, subprocess.TimeoutExpired):
        return {"exit_code":None, "stdout":"", "stderr":"command not available or timed out"}


def inspect(repo: Path, run_audits: bool = False,
            run_tests: bool = False) -> dict[str, object]:
    repo=repo.expanduser().resolve()
    files={name:(repo/name).is_file() for name in REQUIRED}
    git=shutil.which("git")
    head=None
    dirty=None
    if git:
        r=_command([git,"rev-parse","HEAD"],repo)
        value=str(r["stdout"]).strip()
        if r["exit_code"]==0 and re.fullmatch(r"[0-9a-f]{40}",value):
            head=value
            # No filenames or uncommitted content leaves this process.
            s=_command([git,"status","--porcelain"],repo)
            dirty=bool(s["stdout"]) if s["exit_code"]==0 else None
    tools={name:bool(shutil.which(name)) for name in ("git","node","npm","npx","onchainos","gmgn-cli")}
    data:dict[str,object]={
        "status":"PREFLIGHT_NOT_GROK_PROVISIONING",
        "repo_path":str(repo),
        "git_commit":head,
        "git_worktree_dirty":dirty,
        "platform":platform.system(),
        "python_version":platform.python_version(),
        "python_supported":sys.version_info>=(3,11),
        "required_files":files,
        "tools_present":tools,
        "audits":{},
        "offline_unittest":None,
        "grok_bot_created":None,
        "grok_skill_installed":None,
        "rpc_live_data_verified":False,
        "monitor_routine_enabled":None,
        "trading_authorized":False,
        "explanations":[
            "This is an environment probe; no remote API or Grok account capability is authenticated.",
            "Grok Bot's cloud computer is separate from a user's local desktop.",
            "Binary availability does not mean provider configuration, payment, or data access works.",
            "An audited Git checkout and passing Python tests do not prove market validity."
        ]
    }
    if run_audits or run_tests:
        env=os.environ.copy()
        env["PYTHONPATH"]=str(repo/"src")
    if run_audits:
        audit_results={}
        for key,module in CHECK_MODULES:
            r=_command([sys.executable,"-m",module,"--audit"],repo,env)
            entry={"exit_code":r["exit_code"],"status":"FAILED"}
            if r["exit_code"]==0:
                try:
                    document=json.loads(str(r["stdout"]))
                    entry["status"]=document.get("status","EXIT_ZERO")
                except json.JSONDecodeError:
                    entry["status"]="NON_JSON_OUTPUT"
            else:
                entry["error"]="local audit failed; run command directly to review output"
            audit_results[key]=entry
        data["audits"]=audit_results
    if run_tests:
        r=_command([sys.executable,"-m","unittest","discover","-s","tests"],repo,env,timeout=75)
        output=str(r["stderr"])+"\n"+str(r["stdout"])
        match=re.search(r"Ran (\d+) tests",output)
        data["offline_unittest"]={
            "exit_code":r["exit_code"],
            "total":int(match.group(1)) if match else None,
            "passed":r["exit_code"]==0 and re.search(r"(^|\n)OK(\n|$)",output)!=None
        }
    if not all(files.values()) or not data["python_supported"] or head is None:
        data["status"]="MISSING_LOCAL_PREREQUISITES"
    if run_audits and any(x["exit_code"]!=0 for x in data["audits"].values()):
        data["status"]="LOCAL_AUDIT_FAILED"
    if run_tests and (not data["offline_unittest"] or not data["offline_unittest"]["passed"]):
        data["status"]="LOCAL_TEST_FAILED"
    return data


def main() -> int:
    parser=argparse.ArgumentParser(description="Read-only Grok cloud/local runtime preflight")
    parser.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument("--audits",action="store_true")
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    try:
        result=inspect(args.repo,args.audits,args.self_test)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result["status"]=="PREFLIGHT_NOT_GROK_PROVISIONING" else 2
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({"status":"ERROR","error":str(exc)}),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
