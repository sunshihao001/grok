"""Import saved OKX OnchainOS DEX JSON without calling CLI or triggering payment.

This parses *candidate* market fields only. It does NOT certify source authenticity,
time-of-knowledge, public address identity, execution prices or positive market edge.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

from .monitor import ADDRESS

MAX_BYTES = 2 * 1024 * 1024
OPERATIONS: dict[str, dict[str, tuple[str, ...]]] = {
    "token_price_info": {
        "price_usd":("price",),
        "market_cap_usd":("marketCap",),
        "liquidity_usd":("liquidity",),
    },
    "memepump_token_details": {
        "market_cap_usd":("market","marketCapUsd"),
        "top10_holder_pct":("tags","top10HoldingsPercent"),
        "bonding_pct":("bondingPercent",),
    },
}
PINNED_SKILL = "okx/onchainos-skills@73904b636a0f022dcc13b6d7a0dd2ed3b3195f25"


def _stamp(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("provider received time requires ISO8601 string with timezone")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid provider received timestamp") from exc
    if dt.tzinfo is None:
        raise ValueError("provider received timestamp lacks timezone")
    return dt.astimezone(timezone.utc).isoformat()


def _get(data: dict[str, Any], parts: tuple[str, ...]) -> Any:
    value: Any = data
    for part in parts:
        if not isinstance(value, dict) or part not in value:
            return None
        value=value[part]
    return value


def _decimal(value: Any, field: str) -> str | None:
    if value is None or value=="":
        return None
    if isinstance(value, bool) or not isinstance(value,(str,int)):
        raise ValueError(f"{field} must be a decimal string or integer, not float/bool")
    try:
        number=Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"{field} is not numeric") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field} must be non-negative finite")
    if field.endswith("_pct") and number > 100:
        raise ValueError(f"{field} exceeds 100")
    return str(number)


def parse_snapshot(raw: bytes, operation: str, token_address: str,
                   provider_received_at_utc: str | None = None,
                   ingested_at_utc: str | None = None) -> dict[str, Any]:
    if operation not in OPERATIONS:
        raise ValueError("operation not in reviewed read-only parser allowlist")
    if not isinstance(token_address, str) or not ADDRESS.fullmatch(token_address):
        raise ValueError("invalid Solana token mint")
    if not isinstance(raw, bytes) or len(raw)>MAX_BYTES:
        raise ValueError("raw response must be bounded bytes <= 2 MiB")
    try:
        document=json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid JSON provider response") from exc
    if not isinstance(document, dict):
        raise ValueError("expected OKX JSON object envelope")
    received=_stamp(provider_received_at_utc)
    ingest=_stamp(ingested_at_utc) if ingested_at_utc is not None else datetime.now(timezone.utc).isoformat()
    result={
        "status":"UNVERIFIED_PROVIDER_CAPTURE",
        "provider":"OKX OnchainOS",
        "provider_skill_source":PINNED_SKILL,
        "operation":operation,
        "chain":"solana",
        "token_address":token_address,
        "sha256":hashlib.sha256(raw).hexdigest(),
        "raw_bytes":len(raw),
        "provider_received_at_utc":received,
        "ingested_at_utc":ingest,
        "provider_request_time_ms":None,
        "address_confirmed":False,
        "candidate_numeric_fields":{},
        "missing_fields":[],
        "source_authenticated":False,
        "eligible_as_decision_feature":False,
        "eligible_as_live_monitor_input":False,
        "payment_authorized":False,
        "next_action":"Verify captured source, as-of delivery and exact field mappings with independently timed raw records."
    }
    # Provider may automatically sign a paid x402 request after a prior account opt-in:
    # NEVER execute onchainos here, and never retry based on notifications.
    notices=document.get("notifications",[])
    if notices is not None and (not isinstance(notices,list) or notices):
        result["status"]="PROVIDER_NOTIFICATIONS_REQUIRE_HUMAN_REVIEW"
        return result
    if document.get("confirming") is True:
        result["status"]="PAYMENT_CONFIRMATION_REQUIRED_STOP"
        return result
    if document.get("ok") is not True or document.get("error") or document.get("_error"):
        result["status"]="PROVIDER_RESULT_UNAVAILABLE"
        return result
    data=document.get("data")
    if not isinstance(data,dict):
        result["status"]="UNSUPPORTED_PROVIDER_DATA_SHAPE"
        return result
    address=data.get("tokenContractAddress",data.get("tokenAddress"))
    if address is not None:
        if not isinstance(address,str) or address!=token_address:
            result["status"]="PROVIDER_ADDRESS_MISMATCH"
            return result
        result["address_confirmed"]=True

    request_time=document.get("requestTime")
    if request_time is not None:
        if (isinstance(request_time,bool) or
                not isinstance(request_time,(str,int)) or
                not str(request_time).isdigit()):
            raise ValueError("provider requestTime must be Unix milliseconds string/integer")
        result["provider_request_time_ms"]=int(request_time)
    for field,path in OPERATIONS[operation].items():
        value=_decimal(_get(data,path),field)
        if value is None:
            result["missing_fields"].append(field)
        else:
            result["candidate_numeric_fields"][field]=value
    return result


def main() -> int:
    parser=argparse.ArgumentParser(description="Offline inspect of saved OKX read-only DEX JSON; no CLI/network/payment")
    parser.add_argument("--input",type=Path,required=True)
    parser.add_argument("--operation",choices=tuple(OPERATIONS),required=True)
    parser.add_argument("--address",required=True,help="Solana mint, never token symbol")
    parser.add_argument("--provider-received-at",help="Only if backed by independent contemporaneous capture log")
    parser.add_argument("--output",type=Path,help="Optional untracked metadata file path; not live monitor input")
    args=parser.parse_args()
    try:
        raw=args.input.read_bytes()
        result=parse_snapshot(raw,args.operation,args.address,args.provider_received_at)
        if args.output is not None:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            # No executable tool command, signing, wallet action or provider API call.
            args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,TypeError) as exc:
        print(json.dumps({"status":"ERROR","error":str(exc),"payment_authorized":False},ensure_ascii=False),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
