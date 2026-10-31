"""Read-only, conservative first-funder evidence reconciliation.

This is a contract over SOURCE-SUPPLIED candidate funding records, not an RPC
decoder or a beneficial ownership classifier. In particular UNKNOWN, missing,
high-degree and dust-only relationships NEVER become 'independent wallets'.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import re

RAW = re.compile(r"^(0|[1-9][0-9]*)$")
STATES = frozenset({"PENDING", "UNRESOLVED", "RESOLVED"})
METHODS = frozenset({"TRANSFER_INSTRUCTION_CONFIRMED", "NET_BALANCE_DELTA_HEURISTIC"})
TYPES = frozenset({"PUBLIC_CEX", "PUBLIC_BRIDGE", "PUBLIC_ROUTER",
                   "PRIVATE_CANDIDATE", "UNKNOWN"})
PUBLIC = frozenset({"PUBLIC_CEX", "PUBLIC_BRIDGE", "PUBLIC_ROUTER"})


def classify_first_funders(records: list[dict], *,
                           minimum_lamports: int = 1_000_000,
                           high_degree_fraction: float = 0.7) -> dict:
    """Create evidence states while preserving unknown and public infrastructure.

    A source label PRIVATE_CANDIDATE only means it was *not labeled public*
    by the supplied registry; it does not prove nonpublic infrastructure.
    High-degree sources are flagged as ambiguous, NOT assumed independent.
    """
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    if type(minimum_lamports) is not int or minimum_lamports < 0:
        raise ValueError("minimum_lamports must be a nonnegative integer")
    if type(high_degree_fraction) is not float or not 0 < high_degree_fraction <= 1:
        raise ValueError("high_degree_fraction must be a float between 0 and 1")
    seen: set[str] = set()
    source_counts: Counter[str] = Counter()
    validated = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("funding record is not a mapping")
        wallet, state = record.get("wallet"), record.get("state")
        if not isinstance(wallet, str) or not wallet or wallet in seen:
            raise ValueError("missing or duplicate wallet")
        seen.add(wallet)
        if state not in STATES:
            raise ValueError("unknown funding state")
        if state != "RESOLVED":
            if record.get("funder") is not None:
                raise ValueError("unresolved wallet cannot assert a funder")
            if state == "UNRESOLVED" and not record.get("reason"):
                raise ValueError("unresolved wallet must preserve the reason")
            validated.append((record, None, None))
            continue
        funder = record.get("funder")
        kind = record.get("source_type")
        method = record.get("trace_method")
        amount = record.get("amount_lamports")
        if not isinstance(funder, str) or not funder or funder == wallet:
            raise ValueError("resolved funder must be another nonempty account")
        if kind not in TYPES or method not in METHODS:
            raise ValueError("resolved funder requires source_type and trace_method")
        if not isinstance(amount, str) or not RAW.fullmatch(amount):
            raise ValueError("funding amount must be exact raw lamport string")
        if not isinstance(record.get("source_ref"), str) or not record["source_ref"]:
            raise ValueError("resolved source needs source_ref")
        if not isinstance(record.get("signature"), str) or not record["signature"]:
            raise ValueError("resolved source needs exact transaction signature")
        # A heuristic is only a candidate relationship. Never let it count as
        # instruction-proved shared funding evidence.
        if method == "TRANSFER_INSTRUCTION_CONFIRMED" and int(amount) >= minimum_lamports:
            source_counts[funder] += 1
        validated.append((record, int(amount), kind))

    by_wallet, counts, group_edges = [], Counter(), defaultdict(list)
    n = len(records)
    for record, lamports, kind in validated:
        state, wallet = record["state"], record["wallet"]
        output = {"wallet": wallet, "input_state": state, "status": None,
                  "confirmed_economic_independence": False}
        if state == "PENDING":
            output["status"] = "NOT_YET_SCANNED"
        elif state == "UNRESOLVED":
            output["status"] = "FIRST_FUNDER_UNKNOWN"
            output["reason"] = record["reason"]
        else:
            funder, method = record["funder"], record["trace_method"]
            output.update({"candidate_funder": funder, "source_type": kind,
                           "trace_method": method, "signature": record["signature"],
                           "source_ref": record["source_ref"],
                           "amount_lamports": str(lamports)})
            if method == "NET_BALANCE_DELTA_HEURISTIC":
                output["status"] = "FUNDER_HEURISTIC_UNCONFIRMED"
            elif lamports < minimum_lamports:
                output["status"] = "DUST_EDGE_NOT_DISCRIMINATING"
            elif kind in PUBLIC:
                output["status"] = "KNOWN_PUBLIC_INFRASTRUCTURE"
            elif kind == "UNKNOWN":
                output["status"] = "SOURCE_INFRASTRUCTURE_UNKNOWN"
            elif n and source_counts[funder] / n >= high_degree_fraction:
                output["status"] = "HIGH_DEGREE_SOURCE_AMBIGUOUS"
            elif source_counts[funder] >= 2:
                output["status"] = "SHARED_PRIVATE_FUNDER_CANDIDATE"
            else:
                output["status"] = "UNIQUE_OBSERVED_FUNDER_NOT_OWNER_INDEPENDENCE"
            if output["status"] == "SHARED_PRIVATE_FUNDER_CANDIDATE":
                group_edges[funder].append(wallet)
        counts[output["status"]] += 1
        by_wallet.append(output)
    return {"schema_version": "0.1",
            "result_type": "FUNDING_SOURCE_EVIDENCE_NOT_ENTITY_CLUSTER",
            "wallets_examined": n,
            "status_counts": dict(sorted(counts.items())),
            "wallet_states": sorted(by_wallet, key=lambda x: x["wallet"]),
            "shared_private_source_candidates": [
                {"source": funder, "wallets": sorted(members),
                 "evidence_status": "TRANSFER_INSTRUCTION_CONFIRMED_SOURCE_NOT_BENEFICIAL_OWNER"}
                for funder, members in sorted(group_edges.items()) if len(members) >= 2],
            "confirmed_independent_wallet_count": None,
            "normal_wallet_baseline_qualified": False,
            "beneficial_owner_verified": False,
            "no_trading": True,
            "warning": "Unknown/heuristic/public/high-degree/dust do not imply normality or control"}
