"""Single read-only Mint entry: richer saved OKX report, else public pool-only snapshot.

No OKX binary or payment/wallet code is executed by this entrypoint.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import mint_report, public_pair_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="V0.1: a Mint to a read-only report, with explicit source coverage")
    parser.add_argument("mint", help="Solana token Mint address")
    parser.add_argument("--out-dir", type=Path, help="Optional output folder; default .runtime/mint-v0.1/<mint>")
    parser.add_argument("--okx-json", type=Path, help="Already saved and authorized OKX token-research JSON")
    parser.add_argument("--fixture", action="store_true", help="Explicitly label synthetic saved OKX JSON")
    args = parser.parse_args(argv)
    if args.fixture and not args.okx_json:
        parser.error("--fixture only applies to --okx-json")
    dest = args.out_dir or Path(".runtime") / "mint-v0.1" / args.mint
    if args.okx_json:
        flags = ["--mint", args.mint, "--okx-json", str(args.okx_json), "--out-dir", str(dest)]
        if args.fixture:
            flags.append("--fixture")
        return mint_report.main(flags)
    return public_pair_report.main(["--mint", args.mint, "--out-dir", str(dest)])


if __name__ == "__main__":
    raise SystemExit(main())