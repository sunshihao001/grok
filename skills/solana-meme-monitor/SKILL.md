---
name: solana-meme-monitor
description: Read-only source-linked Solana Meme snapshot and normalized multi-wallet event monitoring, with provenance, freshness, deduplication and uncertainty reporting.
---

# Solana Meme Monitor | Read-only runtime handoff

**Role:** execute approved monitoring logic, not research by inventing market facts. The top-level domain reasoning belongs to [market intelligence](../solana-meme-system-intelligence/SKILL.md); deep original-source analysis belongs to the writing and knowledge Skills. This file describes two currently separate input contracts.

## A. Single-Mint snapshot (existing implementation)

Inputs: approved token Mint, normalized observation JSON, rules/monitor.v0.json, state directory. Validate source, units, timestamp, freshness and fixture/live flag. Run `PYTHONPATH=src python -m solana_meme_os.monitor --input OBSERVATION.json --state-dir .runtime`. `--allow-fixture` is only for explicitly synthetic samples. It records liquidity/top10-holder deltas and source event IDs, not wallet clustering.

## B. Multi-wallet event observatory (development implementation)

Inputs: **already normalized source-linked events** with event kind, signature, instruction index, Slot, block time, applicable Mint/owner and raw asset units. Run `PYTHONPATH=src python -m solana_meme_os.market_observatory --input fixtures/market-observatory-synthetic.json --allow-fixture` for a strictly synthetic demonstration.

Outputs: bounded time-window aggregates and candidate facts for same-Slot multiwallet buys, funding fanout, token consolidation, funding-to-buy and cross-Mint re-use when supported by supplied events. Aggregate wallet counts and total lamports cannot establish common control or statistical abnormality. Raw chain RPC retrieval, Jito bundle provenance, representative normal baseline, trade execution and cloud scheduling are **not provided by this code**.

**Never pass normalized event output into the old monitor.py as if it used the same schema**. They are separate interfaces until an explicit, tested adapter exists.

## Reporting and stopping

Report: exact observation population, Mint(s), start/end and Slot, distinct wallets and transactions, Token/SOL amounts with units, source references, candidate mechanism, competing ordinary explanation and missing evidence. Keep `OBSERVED`, `COORDINATION_CANDIDATE`, `UNKNOWN`, `RISK_WARNING` and `PAPER_RESEARCH` conceptually separate; no live trading states are authorized.

Reject: stale/ambiguous source, invalid raw unit, duplicated conflicting events, unavailable decision-time data, unsupported owner identity, unsupported Jito Bundle, forced profit claims. No private keys, signing, broadcast, swaps or routine activation.

Offline regression command: `PYTHONPATH=src python -m unittest discover -s tests -v`. Test success does not prove live data or economic validity. Real Grok Skill availability and cloud runtime need independent confirmation.
