"""Offline verification with pinned FnZero SDK, not our own Solana decoder.

Requires external sol-parser-sdk-python==0.10.0 only in isolated Actions.
No RPC, model, signing, trading or payment. Never infer economic controller.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import importlib.metadata
import json
from pathlib import Path

def account_views(meta, tx):
    """Keep every token account observation separate; missing is not zero."""
    keys = (list(tx["message"]["accountKeys"]) +
            meta.get("loadedAddresses", {}).get("writable", []) +
            meta.get("loadedAddresses", {}).get("readonly", []))
    if len(keys) != len(set(keys)) or any(
        len(meta[x]) != len(keys) for x in ("preBalances", "postBalances")
    ):
        raise ValueError("resolved account or SOL balance mismatch")
    def side(name):
        out = {}
        for entry in meta.get(name, []):
            idx = entry["accountIndex"]
            raw = entry["uiTokenAmount"]["amount"]
            if type(idx) is not int or not 0 <= idx < len(keys):
                raise ValueError("invalid token balance index")
            if not isinstance(raw, str) or not raw.isascii() or not raw.isdigit():
                raise ValueError("token amount must be raw integer string")
            k = (idx, entry["mint"], entry.get("programId"))
            if k in out:
                raise ValueError("duplicate token account balance")
            out[k] = (int(raw), entry.get("owner"))
        return out
    before, after = side("preTokenBalances"), side("postTokenBalances")
    observations = []
    for (idx, mint, program) in sorted(set(before) | set(after)):
        a, b = before.get((idx, mint, program)), after.get((idx, mint, program))
        owners_conflict = bool(a and b and a[1] and b[1] and a[1] != b[1])
        delta = b[0] - a[0] if a and b and not owners_conflict else None
        observations.append({
            "token_account": keys[idx], "mint": mint, "program": program,
            "owner_hint": b[1] if b else a[1],
            "pre_raw": a[0] if a else None, "post_raw": b[0] if b else None,
            "delta_raw": delta,
            "status": ("OWNER_HINT_CONFLICT" if owners_conflict else
                       "MISSING_SIDE" if a is None or b is None else "RAW_BALANCE_DELTA"),
            "economic_owner_proven": False
        })
    return {
        "resolved_accounts": len(keys),
        "token_accounts": observations,
        "sol_delta_accounts": [
            {"account": key, "delta_lamports": post - pre}
            for key, pre, post in zip(keys, meta["preBalances"], meta["postBalances"])
            if post != pre
        ],
        "all_wallet_economic_roles_proven": False,
    }

def verify(data: bytes):
    import base58
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from sol_parser import analyze_simulation_routes, decode_wire_transaction
    from sol_parser.rpc_parser import parse_rpc_transaction, rpc_get_transaction_result_dict_to_response
    version = importlib.metadata.version("sol-parser-sdk-python")
    if version != "0.10.0":
        raise ValueError(f"unexpected SDK version {version}")
    cases = json.loads(data)["cases"]
    if len(cases) != 3:
        raise ValueError("upstream corpus should contain exactly three signed cases")
    output = []
    for case in cases:
        wire = base64.b64decode(case["wire"], validate=True)
        tx, consumed = decode_wire_transaction(wire)
        if consumed != len(wire):
            raise ValueError("incomplete signed transaction")
        count = len(tx["signatures"])
        if not 1 <= count < 128 or wire[0] != count:
            raise ValueError("unexpected signature format")
        for i in range(count):
            Ed25519PublicKey.from_public_bytes(
                base58.b58decode(tx["message"]["accountKeys"][i])
            ).verify(base58.b58decode(tx["signatures"][i]), wire[1 + count * 64:])
        rpc = case["rpc"]
        exp = case["expected"]
        if (rpc["meta"]["err"] is None) != exp["succeeded"]:
            raise ValueError("RPC failed flag and expected execution disagree")
        route = analyze_simulation_routes(wire, {"result": {"value": rpc["meta"]}})
        if route.succeeded != exp["succeeded"] or route.signature != tx["signatures"][0]:
            raise ValueError("SDK status/signature mismatch")
        parsed = rpc_get_transaction_result_dict_to_response(dict(rpc, transaction=tx))
        if parsed is None:
            raise ValueError("SDK RPC conversion failed")
        events, error = parse_rpc_transaction(parsed, route.signature, None, 0)
        if error is not None or len(route.legs) != len(exp["legs"]):
            raise ValueError(f"SDK parsing error or wrong route count: {error}")
        for leg, known in zip(route.legs, exp["legs"]):
            if (leg.protocol, leg.pool, leg.input_mint, leg.output_mint) != (
                known["protocol"], known["pool"], known["input_mint"], known["output_mint"]
            ):
                raise ValueError("DEX leg identity mismatch")
            if leg.specified_amount != int(known["specified_amount"]):
                raise ValueError("specified instruction amount mismatch")
            if not exp["succeeded"] and (
                leg.actual_input_amount is not None or leg.actual_output_amount is not None
            ):
                raise ValueError("failed route cannot have executed amount")
        if not exp["succeeded"]:
            if events or route.transfers or route.native_token_actions:
                raise ValueError("rolled back trade incorrectly emitted economic event")
        elif len(events) != len(exp["legs"]):
            raise ValueError("RPC event count and actual DEX leg count disagree")
        accounts = account_views(rpc["meta"], tx)
        if not exp["succeeded"] and any(
            x["delta_raw"] not in (None, 0) for x in accounts["token_accounts"]
        ):
            raise ValueError("failed transaction shows nonzero settled token change")
        output.append({
            "case": case["name"], "slot": rpc["slot"],
            "signature": route.signature, "verified_ed25519_signatures": count,
            "rpc_success": exp["succeeded"], "sdk_route_leg_count": len(route.legs),
            "sdk_committed_dex_events": len(events),
            "raw_fee_lamports": rpc["meta"]["fee"],
            "route_protocols": [x.protocol for x in route.legs],
            "accounts": accounts,
            "economic_actor_count": "NOT_IDENTIFIABLE",
            "one_route_leg_not_equivalent_to_one_wallet_trade": True,
        })
    return {
        "sdk_version": version, "case_count": len(output),
        "signed_corpus_sha256": hashlib.sha256(data).hexdigest(),
        "source": "0xfnzero/sol-parser-sdk-python@cffb6c808c9b7975fc83428c0613fb4c3fa173b5",
        "cases": output,
        "coverage": "UPSTREAM_CACHED_MAINNET_RPC_NOT_LIVE_RECHECKED",
        "no_trading": True, "no_model_calls": True, "no_grok_invocation": True
    }

def main():
    p = argparse.ArgumentParser(description="Read-only signed FnZero SDK replay")
    p.add_argument("--fixture", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    report = verify(a.fixture.read_bytes())
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"cases": report["case_count"],
                      "sdk_dex_events": sum(x["sdk_committed_dex_events"] for x in report["cases"]),
                      "output": str(a.output), "grok_invoked": False}))

if __name__ == "__main__":
    main()
