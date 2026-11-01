---
name: independent-case-replay
description: Perform blinded independent Solana case replay, time/cluster holdout, data-failure regressions and economically honest post-trade analysis.
---

# independent-case-replay

**Status:** draft skill *template*. Phase 1: **Paper-Only**. This is not proof of installation or review in the Grok UI. Role owners: B06.

## When to use

Perform blinded independent Solana case replay, time/cluster holdout, data-failure regressions and economically honest post-trade analysis.

## Inputs and approved access

Preregistered hypothesis, frozen code/rule, complete case selection manifest, raw snapshots, signed source hashes and outcome windows.

## Source-aware steps

1. Before reading outcomes lock train/validation/test time ranges, wallet group clusters and failure criteria. Capture reasons for excluded/missing samples.
2. Replay each case using only timestamps and source values available by decision cutoff; fail if event time and available_at are conflated.
3. Include losers, ineligible tokens, false alerts, censored windows and untradeable routes. Compare with simple and matched baseline, with clustering and multiple tests.
4. Run negative controls and ablations, and inject stale/empty/error-provider fixtures; distinguish technical failure from actual absence of events.
5. Audit position size, fill assumption, slippage, fees, latency and exit tail under worse scenarios; report coverage-adjusted net distributions and confidence intervals.
6. Execute repository tests and produce B06 `qa_report`, but do not claim actual live market validity solely from CI. Record human-review and rollback prerequisites for any release.

## Output contract

Reproducible test command, sample manifest, independent outcomes, null comparisons, economic sensitivity, failure and rollback packet.

Emit a versioned Bot handoff conforming to `knowledge/bot-handoff.schema.json` and the role-specific `knowledge/bot-knowledge-profiles.v1.json` (never silently assert externally reported material was locally reproduced). Request a peer review where the F Gate requires it. Handoff files are research artifacts, not authorization to trade or release new Monitor rules.

## Stop and approval policy

OOS contaminated, sample missing, too little power, unfillable orders or unverified sources => fail or INSUFFICIENT, never PASS from fixtures.

All tasks are read-only/paper-only. No private keys, signing, swap, order placement or on-chain broadcast. Independent research cannot grant itself Monitor rule release. Grok private skills must be added/enabled by the user after testing; they are not automatically registered by this GitHub directory.
