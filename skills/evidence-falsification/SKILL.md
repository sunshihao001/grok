---
name: evidence-falsification
description: Independent adversarial review of Solana research claims, source errors, confounders, lookahead and economic assumptions.
---

# evidence-falsification

**Status:** draft skill *template*. Phase 1: **Paper-Only**. This is not proof of installation or review in the Grok UI. Role owners: B05, B06.

## When to use

Independent adversarial review of Solana research claims, source errors, confounders, lookahead and economic assumptions.

## Inputs and approved access

Existing B02–B04 immutable handoff + original refs, source coverage, hypothesis version, independent access to raw data.

## Source-aware steps

1. Reopen the cited evidence independently rather than repeating upstream summary. Check source metadata, Git commit, actual transaction, units and availability.
2. Separate observed fact from external report, platform label, economic control inference, causal claim and trade decision. Require null hypotheses that could explain apparent effect.
3. Audit target denominator, selected vs unselected population, missing alerts, leakage from future data, cross-operator train/test split and multiple-comparison search.
4. Check whether an apparent predictive signal remains after simpler baselines and execute-cost sensitivity; report any mismatch between a 2x hit, fill and net return.
5. Record strongest contrary examples and what observation would settle them; keep negative results even if headline narrative becomes less attractive.
6. Output B05 `adversarial_review`, not a self-approved F4–F6 PASS. Independent reviewer evidence and owner release are separate later steps.

## Output contract

Claim-by-claim adversarial ledger, contradictory primary refs, falsifier, F gate status and unresolved blockers.

Emit a versioned Bot handoff conforming to `knowledge/bot-handoff.schema.json` and the role-specific `knowledge/bot-knowledge-profiles.v1.json` (never silently assert externally reported material was locally reproduced). Request a peer review where the F Gate requires it. Handoff files are research artifacts, not authorization to trade or release new Monitor rules.

## Stop and approval policy

Unreproduced source or lack of independent K2 means INSUFFICIENT, not invented confidence.

All tasks are read-only/paper-only. No private keys, signing, swap, order placement or on-chain broadcast. Independent research cannot grant itself Monitor rule release. Grok private skills must be added/enabled by the user after testing; they are not automatically registered by this GitHub directory.
