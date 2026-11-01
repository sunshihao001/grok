"""RugCheck's existing cached public token report, as a read-only vendor snapshot.

One fixed HTTPS GET. Token owners and creator fields are *vendor hints*, not
independently replayed economic control or validated trading recommendations.
No API keys, payment, signatures, transactions, refresh or subscription.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any, Callable
from urllib.request import Request, HTTPRedirectHandler, build_opener

ADDR = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")
HOST = "https://api.rugcheck.xyz"
MAX_BYTES = 2 * 1024 * 1024


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("RugCheck public GET redirected unexpectedly")


def source_url(mint: str) -> str:
    if not isinstance(mint, str) or not ADDR.fullmatch(mint):
        raise ValueError("invalid Solana Mint")
    return HOST + "/v1/tokens/" + mint + "/report"


def fetch_report(mint: str, *, opener: Callable[..., Any] | None = None) -> bytes:
    req = Request(source_url(mint), headers={
        "Accept": "application/json", "User-Agent": "grok-readonly-mint-v0.1",
    }, method="GET")
    fetch = opener or build_opener(RejectRedirects()).open
    with fetch(req, timeout=12) as response:
        if getattr(response, "status", 200) != 200:
            raise ValueError("RugCheck public GET returned non-200")
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("RugCheck report exceeds size limit")
    return raw


def compile_report(raw: bytes, mint: str, *, retrieved_at: str | None = None) -> dict[str, Any]:
    source_url(mint)
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeDecodeError) as exc:
        raise ValueError("invalid RugCheck JSON") from exc
    if not isinstance(data, dict) or data.get("mint") != mint:
        raise ValueError("RugCheck missing or mismatched token Mint")
    holders = data.get("topHolders")
    if holders is None:
        holder_status = "UNKNOWN_NOT_PROVIDED"
        holders = []
    elif isinstance(holders, list) and len(holders) <= 200:
        holder_status = "VENDOR_CACHED_SAMPLE_UNVERIFIED"
    else:
        raise ValueError("RugCheck topHolders response shape invalid or too large")
    # Provider labels distinguish pool/vault/locker accounts from ordinary wallets.
    known = data.get("knownAccounts") if isinstance(data.get("knownAccounts"), dict) else {}
    candidates = []
    for i, row in enumerate(holders):
        if not isinstance(row, dict):
            raise ValueError("invalid RugCheck topHolder entry")
        account = row.get("address")
        if not isinstance(account, str) or not ADDR.fullmatch(account):
            continue
        owner = row.get("owner")
        tag = known.get(owner) if isinstance(owner, str) else None
        if not isinstance(tag, dict):
            tag = known.get(account)
        kind = tag.get("type") if isinstance(tag, dict) else None
        if not isinstance(kind, str):
            kind = None
        candidates.append({
            "token_account_candidate": account,
            "owner_candidate": owner if isinstance(owner, str) and ADDR.fullmatch(owner) else None,
            "amount_raw_vendor": row.get("amount"), "pct_vendor": row.get("pct"),
            "insider_vendor": row.get("insider"),
            "source_path": f"root.topHolders[{i}]",
            "vendor_known_account_type": kind,
            "vendor_known_account_name": tag.get("name") if isinstance(tag, dict) else None,
            "role_interpretation": ("VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE"
                                    if kind in {"AMM", "LOCKER"} else "UNCLASSIFIED_TOKEN_ACCOUNT_OWNER"),
            "evidence": "CACHED_VENDOR_HOLDER_HINT_NOT_CHAIN_REPLAYED",
        })
    # A reported top-holder token account can be a pool vault rather than a
    # freely controlled wallet. Cross-check vendor's own markets before asking
    # an analyst to infer a large holder or a common controller.
    # This is INTERNAL VENDOR consistency, not an independent RPC check.
    pool_vault_matches = []
    markets = data.get("markets")
    if isinstance(markets, list):
        for mi, market in enumerate(markets[:100]):
            if not isinstance(market, dict):
                continue
            for side in ("A", "B"):
                vault = market.get(f"liquidity{side}")
                vault_info = market.get(f"liquidity{side}Account")
                if not isinstance(vault_info, dict) or vault_info.get("mint") != mint:
                    continue
                for holder in candidates:
                    if (vault == holder["token_account_candidate"]
                            and market.get("pubkey") == holder["owner_candidate"]
                            and vault_info.get("owner") == holder["owner_candidate"]):
                        pool_vault_matches.append({
                            "token_account": vault,
                            "market": market.get("pubkey"),
                            "market_type_vendor": market.get("marketType"),
                            "holder_path": holder["source_path"],
                            "vault_path": f"root.markets[{mi}].liquidity{side}",
                            "owner_path": f"root.markets[{mi}].liquidity{side}Account.owner",
                            "status": "VENDOR_INTERNAL_POOL_VAULT_MATCH_NOT_CHAIN_VERIFIED",
                        })
    graph_count = data.get("graphInsidersDetected")
    if type(graph_count) is not int or graph_count < 0:
        graph_count = None
    # '0 detected' and 'null network payload' NEVER prove no insider activity.
    insider_network_state = ("VENDOR_NETWORKS_NOT_PROVIDED"
                             if data.get("insiderNetworks") is None
                             else "VENDOR_NETWORKS_RETURNED_NOT_INDEPENDENTLY_VERIFIED")
    risks = data.get("risks")
    risk_rows = []
    if isinstance(risks, list):
        for i, row in enumerate(risks[:50]):
            if isinstance(row, dict):
                risk_rows.append({"name": row.get("name"), "level_vendor": row.get("level"),
                                  "score_vendor": row.get("score"), "value_vendor": row.get("value"),
                                  "source_path": f"root.risks[{i}]"})
    creator = data.get("creator")
    creator_tokens = data.get("creatorTokens")
    token = data.get("token") if isinstance(data.get("token"), dict) else {}
    result = {
        "schema_version": "grok.rugcheck_public_report.v0", "mint": mint, "chain": "solana",
        "status": "RUGCHECK_CACHED_VENDOR_REPORT_NOT_INDEPENDENTLY_VERIFIED",
        "retrieved_at": retrieved_at or datetime.now(timezone.utc).isoformat(),
        "source": {"provider": "RugCheck", "url": source_url(mint),
                   "input_sha256": hashlib.sha256(raw).hexdigest(),
                   "cache_policy": "FREE_REPORT_MAY_BE_STALE"},
        "vendor_detected_at": data.get("detectedAt"),
        "top_holders": candidates, "top_holders_status": holder_status,
        "top_holders_rows_returned": len(holders),
        "vendor_infrastructure_candidate_count": sum(
            r["role_interpretation"] == "VENDOR_KNOWN_INFRASTRUCTURE_CANDIDATE" for r in candidates),
        "unclassified_account_count": sum(
            r["role_interpretation"] == "UNCLASSIFIED_TOKEN_ACCOUNT_OWNER" for r in candidates),
        "creator_vendor_candidate": creator if isinstance(creator, str) and ADDR.fullmatch(creator) else None,
        "creator_tokens_vendor_count": len(creator_tokens) if isinstance(creator_tokens, list) else None,
        "creator_tokens_status": "VENDOR_SAMPLE_NOT_COMPLETE_HISTORY" if isinstance(creator_tokens, list)
                                 else "UNKNOWN_NOT_PROVIDED",
        "mint_authority_vendor": token.get("mintAuthority"),
        "freeze_authority_vendor": token.get("freezeAuthority"),
        "risk_score_vendor": data.get("score_normalised"),
        "risk_model_rows": risk_rows,
        "pool_vault_matches_vendor": pool_vault_matches,
        "graph_insiders_detected_vendor": graph_count,
        "insider_networks_status": insider_network_state,
        "insider_evidence_interpretation": "NO_INSIDER_ABSENCE_PROOF_FROM_VENDOR_DETECTION",
        "markets_vendor_count": len(data["markets"]) if isinstance(data.get("markets"), list) else None,
        "no_trading": True,
        "limitations": [
            "RUGCHECK_REPORT_CAN_BE_CACHED_AND_STALE",
            "TOP_HOLDERS_NOT_UNIQUE_BENEFICIAL_OWNERS",
            "CREATOR_VENDOR_ADDRESS_NOT_WALLET_CONTROL_PROOF",
            "VENDOR_RISK_SCORE_NOT_A_VALIDATED_SAFETY_PROBABILITY",
            "MARKETS_AND_HOLDER_METRICS_NOT_ATOMIC_WITH_DEX_OR_RPC",
            "NO_PROVEN_SWAP_HISTORY_FUNDING_CHAIN_OR_PROFIT",
            "ZERO_GRAPH_DETECTIONS_NOT_PROOF_OF_ZERO_INSIDERS",
            "VENDOR_INTERNAL_POOL_VAULT_MATCH_NOT_RPC_VERIFIED",
        ],
    }
    return result


def markdown(result: dict[str, Any]) -> str:
    out = ["# RugCheck｜公开Mint持有人与发行者候选（只读）", "",
           f"状态：**{result['status']}**",
           f"数据读取时间：`{result['retrieved_at']}`；供应商最早发现时间：`{result['vendor_detected_at']}`",
           "**注意：免费报告可能缓存；所有钱包、Dev、持仓和风险均为供应商候选，未独立复核。**",
           "", f"Holder状态：{result['top_holders_status']}；返回行数：{result['top_holders_rows_returned']}；"
           f"已标记AMM/Locker基础设施候选：{result['vendor_infrastructure_candidate_count']}；"
           f"其他未分类账户：{result['unclassified_account_count']}",
           f"Creator候选：`{result['creator_vendor_candidate'] or 'UNKNOWN'}`；历史同发币候选数：`{result['creator_tokens_vendor_count']}`",
           f"风险分（供应商模型，非概率）：`{result['risk_score_vendor']}`",
           f"Mint Authority：`{result['mint_authority_vendor'] or 'UNKNOWN_OR_NULL'}`；Freeze Authority：`{result['freeze_authority_vendor'] or 'UNKNOWN_OR_NULL'}`",
           "", "## 供应商内幕网络字段与池Vault证据", "",
           f"供应商图检测数：{result.get('graph_insiders_detected_vendor')}；"
           f"网络返回状态：{result.get('insider_networks_status', 'UNKNOWN')}。"
           " 0不等于已证明无内幕钱包，null也不等于无内幕关系。",
           "以下池Vault是RugCheck同份报告内部字段一致，仍不是独立链上复核。", "",
           *[f"- 持仓Token Account `{m['token_account']}` 与池 `{m['market']}` "
             f"匹配；证据：`{m['holder_path']}`、`{m['vault_path']}`、"
             f"`{m['owner_path']}`；`{m['status']}`"
             for m in result.get("pool_vault_matches_vendor", [])],
           "", "## 返回的持有人候选（只列部分）", ""]
    for row in result["top_holders"][:20]:
        out.append(f"- Token Account `{row['token_account_candidate']}`；"
                   f"Owner候选 `{row['owner_candidate'] or 'UNKNOWN'}`；"
                   f"供应商份额 `{row['pct_vendor']}`；"
                   f"角色 `{row['role_interpretation']}`（`{row['vendor_known_account_type']}`）；"
                   f"证据 `{row['source_path']}`")
    out += ["", "## 风险标签（仅作为待核验信息）", ""]
    for r in result["risk_model_rows"][:15]:
        out.append(f"- `{r['name']}` / `{r['level_vendor']}` / `{r['score_vendor']}`：`{r['source_path']}`")
    out += ["", "## 不得直接推断", "",
            "- 免费缓存快照不证明当前实时Token库存、实际受益人、庄家控制或Dev完整历史。",
            "- 缺失字段和空列表不等于市场无Holder、无风险或Dev没有历史活动。",
            "- 风险模型和Pool成交数据不等于跟单可盈利信号。", ""]
    return "\n".join(out)
