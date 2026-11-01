"""Mint → bounded candidate-wallet evidence using existing public adapters.

Not Million, not a Solana trading decoder, not continuous monitoring.
No vendor label or token-account owner is evidence of economic control.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable

from .public_token_accounts import valid_address
from .public_wallet_rpc_sample import sample

MAX_WALLETS = 2


def _digest(path: Path, expected: str) -> None:
    if not path.is_file():
        raise ValueError(f"missing original vendor evidence {path.name}")
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise ValueError(f"raw vendor source SHA256 mismatch: {path.name}")


def validate_sources(report: dict[str, Any], report_dir: Path) -> dict[str, str]:
    """Reject changed provider bytes. Never trust cached provider fields alone."""
    if report.get("schema_version") != "grok.mint_v01_combined.v0":
        raise ValueError("unsupported Mint report schema")
    mint = report.get("mint")
    if not valid_address(mint) or report.get("chain") != "solana":
        raise ValueError("invalid Mint or Solana chain")
    if report.get("status", "").startswith("FIXTURE"):
        raise ValueError("fixture Mint report cannot be treated as real")
    sources = {}
    rug = report.get("rugcheck_public")
    if rug:
        if rug.get("mint") != mint or rug.get("chain") != "solana":
            raise ValueError("RugCheck Mint/chain mismatch")
        d = rug["source"]["input_sha256"]
        _digest(report_dir / "rugcheck-provider-raw.json", d)
        sources["rugcheck-provider-raw.json"] = d
    rpc = report.get("rpc_token_accounts")
    if rpc:
        if rpc.get("mint") != mint or rpc.get("chain") != "solana":
            raise ValueError("RPC Mint/chain mismatch")
        for name, d in rpc["source"]["raw_sha256"].items():
            if name not in ("largest-accounts-raw.json", "account-owners-raw.json"):
                raise ValueError("unexpected RPC raw filename")
            stored = "rpc-" + name
            _digest(report_dir / stored, d)
            sources[stored] = d
    dex = report.get("dex_public")
    if dex:
        if dex.get("mint") != mint or dex.get("chain") != "solana":
            raise ValueError("DEX Mint/chain mismatch")
        d = dex["raw_input_sha256"]
        _digest(report_dir / "dex-provider-raw.json", d)
        sources["dex-provider-raw.json"] = d
    if not sources:
        raise ValueError("no verified raw Mint sources")
    return sources


def shortlist(report: dict[str, Any], *, max_wallets: int = 2) -> dict[str, Any]:
    if type(max_wallets) is not int or not 1 <= max_wallets <= MAX_WALLETS:
        raise ValueError("maximum wallet probes is 1..2")
    mint = report["mint"]
    dex = report.get("dex_public") or {}
    rug = report.get("rugcheck_public") or {}
    rpc = report.get("rpc_token_accounts") or {}
    excluded = set()
    for p in dex.get("pairs", []):
        if valid_address(p.get("pool")):
            excluded.add(p["pool"])
    for p in rug.get("pool_vault_matches_vendor", []):
        for key in ("token_account", "market"):
            if valid_address(p.get(key)):
                excluded.add(p[key])
    for p in report.get("pool_related_holder_candidates", []):
        for key in ("holder_token_account", "holder_owner_vendor", "matching_pool_address"):
            if valid_address(p.get(key)):
                excluded.add(p[key])
    for p in rug.get("top_holders", []):
        if p.get("role_interpretation") == "VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE":
            for key in ("token_account_candidate", "owner_candidate"):
                if valid_address(p.get(key)):
                    excluded.add(p[key])
    candidates = []
    seen = set()
    skipped = []
    def add(wallet: Any, kind: str, path: str, token_account: str | None = None):
        if not valid_address(wallet):
            skipped.append({"kind": kind, "reason": "INVALID_OR_MISSING_ADDRESS", "source_path": path})
            return
        if wallet == mint or wallet in excluded:
            skipped.append({"kind": kind, "reason": "MINT_OR_INFRASTRUCTURE_CANDIDATE", "source_path": path})
            return
        if wallet in seen:
            return
        seen.add(wallet)
        candidates.append({
            "wallet": wallet,
            "source_kind": kind,
            "source_path": path,
            "associated_token_account": token_account,
            "economic_identity": "UNKNOWN",
            "not_proven": [
                "WALLET_CONTROL_NOT_PROVEN",
                "TOKEN_ACCOUNT_OWNER_MAY_BE_PDA_CUSTODY_OR_AMM",
                "ADDRESS_ACTIVITY_NOT_SAME_AS_TOKEN_BUY",
                "CREATOR_VENDOR_HINT_NOT_DEPLOYER_PROOF",
            ],
        })
    # Deliberate diversity: a creator vendor hint, then a separately identified
    # RPC owner. Do not take multiple token accounts as multiple independent owners.
    if rug:
        add(rug.get("creator_vendor_candidate"), "RUGCHECK_CREATOR_VENDOR_HINT",
            "rugcheck_public.creator_vendor_candidate")
    for p in rpc.get("rows", []):
        if len(candidates) >= max_wallets:
            break
        if p.get("owner_status") == "RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER":
            add(p.get("owner_candidate"), "FINALIZED_RPC_TOKEN_ACCOUNT_OWNER_HINT",
                "rpc_token_accounts." + str(p.get("owner_source_path")),
                p.get("token_account"))
    for p in rug.get("top_holders", []):
        if len(candidates) >= max_wallets:
            break
        if p.get("role_interpretation") != "VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE":
            add(p.get("owner_candidate"), "RUGCHECK_HOLDER_OWNER_VENDOR_HINT",
                "rugcheck_public." + str(p.get("source_path")),
                p.get("token_account_candidate"))
    return {
        "mint": mint,
        "candidates": candidates[:max_wallets],
        "excluded_infrastructure_address_count": len(excluded),
        "skipped": skipped,
        "total_candidates_before_probe": len(candidates),
        "coverage": "TOP_ACCOUNTS_AND_VENDOR_HINTS_NOT_UNIQUE_PEOPLE_OR_ALL_BUYERS",
        "selection_strategy": "CREATOR_THEN_RPC_OWNER_THEN_VENDOR_OWNER_NO_DUPLICATES",
    }



def target_mint_observation(raw_tx: bytes | None, mint: str, wallet: str) -> dict[str, Any]:
    """Token balance presence ≠ swap or buyer proof; never treat latest tx as Mint trade."""
    unknown = {
        "status": "UNKNOWN_TARGET_MINT_COVERAGE_NO_COMPLETE_TRANSACTION_META",
        "mint_in_reported_token_balances": None,
        "queried_wallet_is_reported_mint_token_owner": None,
        "target_token_accounts_reported": None,
        "mint_trade_or_transfer_proven": False,
    }
    if raw_tx is None:
        return unknown
    try:
        envelope = json.loads(raw_tx)
        tx = envelope.get("result")
        meta = tx.get("meta") if isinstance(tx, dict) else None
        if not isinstance(meta, dict):
            return unknown
        pre, post = meta.get("preTokenBalances"), meta.get("postTokenBalances")
        if not isinstance(pre, list) or not isinstance(post, list):
            return unknown
        matching = []
        for entry in pre + post:
            if not isinstance(entry, dict):
                return unknown
            if entry.get("mint") == mint:
                matching.append(entry)
        if not matching:
            return {
                **unknown,
                "status": "TARGET_MINT_NOT_IN_REPORTED_TOKEN_BALANCES_OF_THIS_BOUNDED_TX",
                "mint_in_reported_token_balances": False,
                "queried_wallet_is_reported_mint_token_owner": False,
                "target_token_accounts_reported": 0,
            }
        return {
            **unknown,
            "status": "TARGET_MINT_IN_REPORTED_BALANCES_NOT_BUY_OR_CONTROL_PROOF",
            "mint_in_reported_token_balances": True,
            "queried_wallet_is_reported_mint_token_owner":
                any(e.get("owner") == wallet for e in matching),
            "target_token_accounts_reported": len({
                e.get("accountIndex") for e in matching if type(e.get("accountIndex")) is int
            }),
        }
    except (ValueError, TypeError, AttributeError):
        return unknown


def run(report_dir: Path, out_dir: Path, *,
        max_wallets: int = 2,
        request_fn: Callable[..., Any] | None = None) -> dict[str, Any]:
    report_path = report_dir / "report.json"
    report_bytes = report_path.read_bytes()
    report = json.loads(report_bytes)
    source_hashes = validate_sources(report, report_dir)
    selection = shortlist(report, max_wallets=max_wallets)
    if out_dir.exists() and any(out_dir.iterdir()):
        raise ValueError("out directory must be empty (stale evidence risk)")
    outcome = []
    blobs: list[tuple[Path, bytes]] = []
    now = datetime.now(timezone.utc).isoformat()
    for candidate in selection["candidates"]:
        wallet = candidate["wallet"]
        try:
            kw = {"limit": 1}
            if request_fn is not None:
                kw["request_fn"] = request_fn
            proof, raw = sample(wallet, **kw)
            for name, data in raw.items():
                blobs.append((out_dir / "wallets" / wallet / name, data))
            outcome.append({
                **candidate, "rpc_status": proof["transaction"]["status"],
                "retrieved_at": proof["source"]["retrieved_at"],
                "signatures_returned": len(proof["rows"]),
                "first_signature": proof["rows"][0]["signature"] if proof["rows"] else None,
                "raw_sha256": proof["raw_input_sha256"],
                "observation": proof["transaction"]["execution_observation"],
                "target_mint_observation": target_mint_observation(
                    raw.get("wallet-first-transaction-raw.json"), report["mint"], wallet),
                "signature_page_not_full_history": True,
                "error": proof["transaction"]["error"],
            })
        except (OSError, ValueError, TypeError) as exc:
            outcome.append({**candidate, "rpc_status": "RPC_UNAVAILABLE_NOT_ZERO_ACTIVITY",
                            "signatures_returned": None, "first_signature": None,
                            "raw_sha256": {}, "observation": None,
                            "target_mint_observation": target_mint_observation(None, report["mint"], wallet),
                            "error": str(exc)[:180]})
    payload = {
        "schema_version": "grok.mint_candidate_wallet_probe.v0",
        "mint": report["mint"], "processed_at": now,
        "mint_report_sha256": hashlib.sha256(report_bytes).hexdigest(),
        "upstream_raw_sha256": source_hashes,
        "selection": selection,
        "wallet_probe_results": outcome,
        "actual_wallet_activity_count": None,
        "candidate_economic_controller": "NOT_IDENTIFIED",
        "discovery_coverage": "NOT_MILLION_DISCOVERY_NO_HELIUS_KEY",
        "sampling": "ONE_FINALIZED_SIGNATURE_PLUS_MAX_ONE_TRANSACTION_PER_CANDIDATE",
        "continuous_monitoring": False, "trading": False,
        "grok_invoked": False, "payment": False,
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    for path, data in blobs:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    (out_dir / "candidate-observations.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Bounded evidence-only Mint candidate wallet activity")
    ap.add_argument("--mint-report-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--max-wallets", type=int, default=2)
    a = ap.parse_args(argv)
    try:
        output = run(a.mint_report_dir, a.out_dir, max_wallets=a.max_wallets)
        print(json.dumps({
            "mint": output["mint"],
            "candidates": len(output["wallet_probe_results"]),
            "rpc_results": [x["rpc_status"] for x in output["wallet_probe_results"]],
            "no_trading": True,
        }, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAILED_NO_FALSE_ACTIVITY_CLAIMS",
                          "error": str(exc)[:220]}, ensure_ascii=False), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
