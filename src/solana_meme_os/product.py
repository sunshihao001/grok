"""One-command read-only product entry: Mint report -> verified Grok evidence.

Only orchestrates existing collectors. No trades, signatures, automated
payments, LLM calls, WebSocket service, or provider key installation.
"""
from __future__ import annotations

import argparse
import contextlib
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import sys
from uuid import uuid4

from . import mint_v01, public_token_accounts, vendor_event_handoff


def _status_file(directory: Path, receipt: dict) -> None:
    (directory / "run_status.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def run(mint: str, directory: Path) -> int:
    """0: sources verified; 4: useful partial report; 3: failed; 2: invalid input."""
    if not public_token_accounts.valid_address(mint):
        print(json.dumps({"status": "INVALID_MINT", "mint": mint, "no_trading": True}), file=sys.stderr)
        return 2
    try:
        # Never overwrite previous evidence. Multiple Grok invocations get separate receipts.
        directory.mkdir(parents=True, exist_ok=False)
    except OSError as exc:
        print(json.dumps({"status": "RUN_DIRECTORY_UNAVAILABLE", "reason": str(exc),
                          "no_trading": True}), file=sys.stderr)
        return 2

    mint_dir = directory / "mint"
    outbox = directory / "grok-outbox"
    receipt = {
        "schema_version": "grok.product_run.v1",
        "mint": mint,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "STARTED",
        "no_trading": True,
        "grok_executed": False,
        "payment_executed": False,
        "wallet_transactions": "NOT_OBSERVED",
        "funding_graph": "NOT_OBSERVED",
        "paths": {"report_json": None, "report_md": None, "evidence_json": None},
        "source_status": {},
    }
    try:
        # Collector is existing production code, not an alternative source parser.
        with contextlib.redirect_stdout(io.StringIO()):
            code = mint_v01.main([mint, "--rugcheck", "--out-dir", str(mint_dir)])
        if code != 0 or not (mint_dir / "report.json").is_file():
            receipt["status"] = "COLLECT_FAILED"
            receipt["collector_exit"] = code
            _status_file(directory, receipt)
            print(json.dumps(receipt, ensure_ascii=False))
            return 3

        report = json.loads((mint_dir / "report.json").read_text(encoding="utf-8"))
        if report.get("mint") != mint or report.get("no_trading") is not True:
            raise ValueError("Mint report identity or read-only status mismatch")
        receipt["source_status"] = report.get("source_status") or {}
        receipt["source_errors"] = report.get("source_errors") or {}
        receipt["paths"]["report_json"] = str(mint_dir / "report.json")
        receipt["paths"]["report_md"] = str(mint_dir / "report.md")
        dex = mint_dir / "dex-provider-raw.json"
        rug = mint_dir / "rugcheck-provider-raw.json"
        if not dex.is_file() or not rug.is_file():
            # A valid DEX-only or RugCheck-only report is still useful, but
            # it is NOT a verified two-source handoff and does not invoke Grok.
            receipt["status"] = "PARTIAL_MINT_REPORT_NO_GROK_HANDOFF"
            receipt["missing_sources"] = [
                name for name, path in (("DEX", dex), ("RUGCHECK", rug)) if not path.is_file()
            ]
            _status_file(directory, receipt)
            print(json.dumps(receipt, ensure_ascii=False))
            return 4

        try:
            packet = vendor_event_handoff.triage(
                (mint_dir / "report.json").read_bytes(), rug.read_bytes(), dex.read_bytes()
            )
        except (OSError, ValueError) as exc:
            receipt["status"] = "EVIDENCE_REJECTED"
            receipt["reason"] = str(exc)
            _status_file(directory, receipt)
            print(json.dumps(receipt, ensure_ascii=False))
            return 3
        vendor_event_handoff.write_outputs(outbox, packet)
        receipt["status"] = "READY_FOR_GROK_REVIEW_NOT_EXECUTED"
        receipt["paths"]["evidence_json"] = str(outbox / "evidence.json")
        receipt["review_count"] = len(packet["investigations"])
        receipt["suppressed_count"] = len(packet["suppressed_candidates"])
        receipt["disposition"] = packet["disposition"]
        _status_file(directory, receipt)
        print(json.dumps(receipt, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        receipt["status"] = "PRODUCT_RUN_FAILED"
        receipt["reason"] = str(exc)
        _status_file(directory, receipt)
        print(json.dumps(receipt, ensure_ascii=False), file=sys.stderr)
        return 3


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="One Solana Mint -> read-only report and verified Grok review packet"
    )
    parser.add_argument("mint", help="Real Solana Mint; no wallets or keys needed")
    parser.add_argument("--out-dir", type=Path, help="New, unused run directory")
    args = parser.parse_args(argv)
    directory = args.out_dir or (
        Path(".runtime") / "product-runs" / args.mint /
        (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8])
    )
    return run(args.mint, directory)


if __name__ == "__main__":
    raise SystemExit(main())
