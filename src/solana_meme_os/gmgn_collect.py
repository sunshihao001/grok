"""Opt-in, read-only GMGN CLI collector; no unverified field mappings."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
from .monitor import ADDRESS

READ_COMMANDS = [("info", ["token", "info"]),
                 ("security", ["token", "security"]),
                 ("pool", ["token", "pool"])]


def collect(address: str, output_dir: Path, cli: str = "gmgn-cli") -> Path:
    if not ADDRESS.fullmatch(address):
        raise ValueError("invalid Solana token address")
    responses = {}
    for key, command in READ_COMMANDS:
        args = [cli, *command, "--chain", "sol", "--address", address, "--raw"]
        response = subprocess.run(args, capture_output=True, text=True, timeout=30, check=True)
        value = json.loads(response.stdout)
        if not isinstance(value, dict) or value.get("_error") or value.get("error"):
            raise ValueError(f"GMGN {key} did not return a usable object")
        responses[key] = value
    output_dir.mkdir(parents=True, exist_ok=True)
    observed = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    raw_path = output_dir / f"{address}_{stamp}_raw.json"
    normalized_path = output_dir / f"{address}_{stamp}_observation.json"
    raw_path.write_text(json.dumps(responses, ensure_ascii=False, indent=2), encoding="utf-8")
    observation = {"schema_version": "1.0", "chain": "sol", "token_address": address,
                   "observed_at": observed, "mode": "live",
                   "source": {"tool": "gmgn-cli", "ref": str(raw_path)},
                   "metrics": {}, "events": []}
    normalized_path.write_text(json.dumps(observation, ensure_ascii=False, indent=2), encoding="utf-8")
    return normalized_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect only token info, security, pool; no trades")
    parser.add_argument("--address", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path(".runtime/incoming"))
    parser.add_argument("--cli", default="gmgn-cli")
    args = parser.parse_args()
    try:
        print(collect(args.address, args.output_dir, args.cli))
        return 0
    except (OSError, subprocess.SubprocessError, ValueError, json.JSONDecodeError) as exc:
        print(f"GMGN collection failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
