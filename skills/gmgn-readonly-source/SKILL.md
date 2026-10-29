---
name: gmgn-readonly-source
description: Collect and audit read-only Solana/GMGN observations, timestamps, raw field semantics and provider completeness.
---

# gmgn-readonly-source

**Status:** reviewed skill *template*, not proof of installation in Grok UI. Role owners: B02.

## When to use

Collect and audit read-only Solana/GMGN observations, timestamps, raw field semantics and provider completeness.

## Inputs and approved access

Mint/pool/transaction signature; as-of cutoff; permitted read-only GMGN or Solana RPC availability; expected field dictionary.

## Source-aware steps

1. Start from pinned market lifecycle and GMGN history, not historical numeric scoring thresholds. Identify chain, mint, pool and launch/DEX phase.
2. Use existing src/solana_meme_os/gmgn_collect.py or legitimate read-only RPC/CLI only after confirming command schema and consent. No swap, create, cooking, signing or transaction broadcast.
3. Preserve raw response reference/checksum, request/response time, slot, event_at, indexed_at if available, available_at and underlying provider version. Record failures and gaps, especially HTTP/CLI errors separately from empty markets.
4. Check units and decimal scales, USD/SOL conversions, dynamic token supply, pool vs holder accounts, percentages vs percentage points. Never guess unknown mapping.
5. Use `decision_cutoff_utc`: evidence available afterward is prohibited from predictive features even if the chain event occurred earlier. Detect source timeouts, pagination, RPC throttling and missing monitoring windows.
6. Return a B02 `evidence_observation` or `research_gap` handoff; mark simulated fixture distinctly. If primary source cannot be inspected, abstain.

## Output contract

Raw source manifest, normalized fields with units and availability, data completeness/known error table, upstream-to-downstream source links.

Emit a versioned Bot handoff conforming to `knowledge/bot-handoff.schema.json` and the role-specific `knowledge/bot-knowledge-profiles.v1.json` (never silently assert externally reported material was locally reproduced). Request a peer review where the F Gate requires it. Handoff files are research artifacts, not authorization to trade or release new Monitor rules.

## Stop and approval policy

No source / timezone / unit / data coverage => INSUFFICIENT; do not fill with zeros or secondary tags.

All tasks are read-only/paper-only. No private keys, signing, swap, order placement or on-chain broadcast. Independent research cannot grant itself Monitor rule release. Grok private skills must be added/enabled by the user after testing; they are not automatically registered by this GitHub directory.
