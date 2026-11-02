#!/usr/bin/env python3
"""Read-only audit of cross-operator timing in Why-Solana's published frozen dataset.

Reproduces the 16 historical shared-wallet sample with signature-level path times.
Does not identify beneficial owners, run RPC calls, or claim significance/alpha.
    python scripts/research/audit_frozen_cross_operator_time.py --out audit.json
    python scripts/research/audit_frozen_cross_operator_time.py --data-dir ./frozen --out audit.json
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
from urllib.request import Request, urlopen

REPO = "sunshihao001/Why-Solana-Memecoins-Are-Over"
COMMIT = "9a7ad51d56328e91e67e3f531d6744307d0ee68b"
BASE = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/funder_network/derived"
EXPECTED_SHA = "1a6cec6ae61b86e3f59f32cecdbba421d69450ba03849872c948bd4b87b2e573"
NAMES = ["fn_table.json.gz", "FN_FREEZE.json", "inventory.json", "FN_results.json"]


def read_file(name: str, local: Path | None) -> bytes:
    if local is not None:
        return (local / name).read_bytes()
    with urlopen(Request(f"{BASE}/{name}", headers={"User-Agent": "frozen-audit/1.0"}), timeout=25) as r:
        return r.read()


def audit(data: dict[str, bytes]) -> dict:
    frozen = json.loads(data["FN_FREEZE.json"])
    digest = hashlib.sha256(data["fn_table.json.gz"]).hexdigest()
    if digest != EXPECTED_SHA or digest != frozen["sha256_table"]:
        raise ValueError("Frozen dataset SHA-256 mismatch")
    table = json.loads(gzip.decompress(data["fn_table.json.gz"]))
    population = json.loads(data["inventory.json"])["population"]
    published = json.loads(data["FN_results.json"])["C"]["shared"]
    targets = {x["wallet"]: x for x in published}

    # Equivalent to the original study's overlapping downstream-branch deduplication.
    seen, downs = set(), []
    for path in table["downs"]:
        if len(path["path"]) < 2:
            continue
        a, b = path["path"][:2]
        key = (b.get("sig"), a.get("wallet"), b.get("wallet"))
        if key not in seen:
            seen.add(key)
            downs.append(path)

    grouped: dict[str, dict[str, dict[tuple, int]]] = {}
    for path in itertools.chain(table["ups"], downs):
        ops = population[path["primary"]]["operators"]
        for node in path["path"][1:]:
            wallet, when = node.get("wallet"), node.get("bt")
            if wallet not in targets or not when:
                continue
            for op in ops:
                # Dedup overlapping observations of an identical signature.
                key = (node.get("sig"), when, path["primary"])
                grouped.setdefault(wallet, {}).setdefault(op, {})[key] = when

    rows = []
    for wallet, original in sorted(targets.items()):
        events = grouped.get(wallet, {})
        if set(events) != set(original["operators"]):
            raise ValueError(f"Group membership does not match original report: {wallet}")
        candidate_pairs = []
        for a, b in itertools.combinations(sorted(events), 2):
            gap = min(abs(x-y) for x in events[a].values() for y in events[b].values())
            candidate_pairs.append((gap, a, b))
        gap, a, b = min(candidate_pairs)
        rows.append({
            "wallet": wallet,
            "original_operators": original["operators"],
            "nearest_cross_operator_gap_seconds": gap,
            "nearest_cross_operator_gap_hours": round(gap / 3600, 3),
            "nearest_pair": [a, b],
            "within_24h": gap <= 86400,
            "within_7d": gap <= 604800,
        })

    near = [row for row in rows if row["within_24h"]]
    return {
        "study_commit": COMMIT,
        "verified_frozen_sha256": digest,
        "primary_wallets": len(table["primary"]),
        "original_downstream_paths": len(table["downs"]),
        "deduplicated_downstream_paths": len(downs),
        "upstream_paths": len(table["ups"]),
        "published_shared_wallets": len(targets),
        "within_24h": len(near),
        "within_7d": sum(row["within_7d"] for row in rows),
        "unique_nearest_operator_pairs_within_24h": len(
            {tuple(row["nearest_pair"]) for row in near}
        ),
        "wallets": rows,
        "limitations": [
            "These are path transaction times, not observation/decision timestamps.",
            "The 24h and 7d bins are exploratory, not calibrated thresholds.",
            "No temporal null-hypothesis significance test was run.",
            "Source is author's frozen sample, not independent RPC re-collection.",
            "Shared path use does not prove common private-key control or owner.",
        ],
    }


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--data-dir", type=Path, help="Optional offline directory of four pinned source files")
    cli.add_argument("--out", type=Path, default=Path("frozen_temporal_audit.json"))
    args = cli.parse_args()
    result = audit({name: read_file(name, args.data_dir) for name in NAMES})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "wallets"}, indent=2))
    print("Saved:", args.out)


if __name__ == "__main__":
    main()
