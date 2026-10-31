"""Audit source-derived Solana wallet inflow *labels*, not raw RPC facts.

Labels such as `financement` and `produit_de_vente` remain source claims.
A transaction with other program labels is a review candidate, not an error.
This module does not infer the true funding operator or net profit.
"""
from __future__ import annotations
from collections import Counter
import json
from pathlib import Path
import argparse


def audit_funding_table(doc: dict) -> dict:
    if not isinstance(doc, dict) or not isinstance(doc.get("wallets"), list):
        raise ValueError("expected source-derived wallets list")
    wallets = doc["wallets"]
    if any(not isinstance(w, dict) or not isinstance(w.get("wallet"), str)
           or not w["wallet"] for w in wallets):
        raise ValueError("invalid wallet entry")
    if len({w["wallet"] for w in wallets}) != len(wallets):
        raise ValueError("duplicate wallet")
    if any(type(w.get("genesis_reached")) is not bool
           or type(w.get("prebuy_window_reached")) is not bool for w in wallets):
        raise ValueError("missing explicit coverage flags")
    if "n_wallets" in doc and doc["n_wallets"] != len(wallets):
        raise ValueError("source wallet count disagrees with actual rows")
    genesis = sum(w["genesis_reached"] for w in wallets)
    prebuy = sum(w["prebuy_window_reached"] for w in wallets)
    if "n_genesis_reached" in doc and doc["n_genesis_reached"] != genesis:
        raise ValueError("source genesis count disagrees with actual rows")
    if "n_prebuy_window_reached" in doc and doc["n_prebuy_window_reached"] != prebuy:
        raise ValueError("source prebuy coverage disagrees with actual rows")
    nature = Counter()
    programs = Counter()
    by_pair = Counter()
    non_system_funding = []
    non_swap_sale = []
    n_debited = Counter()
    observed = 0
    seen = set()
    duplicate_like = []
    for w in wallets:
        inflows = w.get("inflows")
        if not isinstance(inflows, list):
            raise ValueError("wallet inflows must be a list; unknown is not zero")
        for x in inflows:
            if not isinstance(x, dict) or not x.get("signature"):
                raise ValueError("every recorded inflow needs a source signature")
            # Multiple inflows can exist in one transaction; de-dupe only an
            # identical source-derived entry, never all entries by signature.
            key = (w["wallet"], x["signature"], x.get("phase"),
                   x.get("nature"), x.get("source"), x.get("amount_sol"))
            if key in seen:
                # Without instruction index, same tx may legitimately contain
                # two equal transfers. Flag but never silently drop a row.
                duplicate_like.append({"wallet": w["wallet"], "signature": x["signature"]})
            seen.add(key)
            kind = x.get("nature", "UNKNOWN")
            program = x.get("tx_source", "UNKNOWN")
            tx_type = x.get("tx_type", "UNKNOWN")
            if not isinstance(kind, str) or not isinstance(program, str):
                raise ValueError("invalid event labels")
            observed += 1
            nature[kind] += 1
            programs[program] += 1
            by_pair[f"{kind}|{program}|{tx_type}"] += 1
            n_debited[str(x.get("n_debited_accounts", "UNKNOWN"))] += 1
            if kind == "financement" and program != "SYSTEM_PROGRAM":
                non_system_funding.append({"wallet": w["wallet"], "signature": x["signature"],
                                           "source": program, "type": tx_type})
            if kind == "produit_de_vente" and tx_type != "SWAP":
                non_swap_sale.append({"wallet": w["wallet"], "signature": x["signature"],
                                      "source": program, "type": tx_type})
    return {"schema_version": "0.1", "kind": "PUBLISHED_DERIVED_INFLOW_LABEL_AUDIT",
            "wallet_count": len(wallets), "genesis_covered": genesis,
            "genesis_uncovered": len(wallets) - genesis,
            "prebuy_covered": prebuy, "prebuy_uncovered": len(wallets) - prebuy,
            "source_inflow_rows": observed,
            "recorded_nature": dict(sorted(nature.items())),
            "recorded_program": dict(sorted(programs.items())),
            "nature_program_type": dict(sorted(by_pair.items())),
            "debited_account_count": dict(sorted(n_debited.items())),
            "duplicate_like_rows_needing_instruction_ids": duplicate_like,
            "funding_label_non_system_transfer_candidates": non_system_funding,
            "sale_label_non_swap_type_candidates": non_swap_sale,
            "classification_provenance": "SOURCE_DERIVED_NOT_INDEPENDENT_RPC",
            "non_system_is_error": False,
            "sale_label_is_confirmed_execution": False,
            "confirmed_original_funder": False,
            "economic_owner_verified": False, "net_trade_edge_verified": False,
            "no_trading": True}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    with args.input.open(encoding="utf-8") as f:
        result = audit_funding_table(json.load(f))
    payload = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")

if __name__ == "__main__":
    main()
