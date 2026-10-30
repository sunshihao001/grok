---
name: wallet-funding-forensics
description: Explore wallet roles, source-of-funds graph, coordinated buys, exit-wallet transfer and competing hub explanations with primary chain evidence.
---

# wallet-funding-forensics

**Status:** draft skill *template*. Phase 1: **Paper-Only**. This is not proof of installation or review in the Grok UI. Role owners: B03.

## When to use

Explore wallet roles, source-of-funds graph, coordinated buys, exit-wallet transfer and competing hub explanations with primary chain evidence.

## Inputs and approved access

B02 source-linked wallet events with signatures, slots and time; mint/pool phase; null/control addresses where available.

## Source-aware steps

1. Separate deployer, funder, router, sniper, holder and exit address roles; allow roles to change over time. An address is not a person.
2. Construct time-respecting directed funding edges. Distinguish direct funder, one-hop/two-hop transfer, service/CEX hub, aggregator, bridge, exchange settlement and unknown.
3. Quantify coordinated timing using actual event times and denominator. Use matched random/well-known public-service control, not an arbitrary 5-minute group rule as proof.
4. Check ownership/concentration only after LP, DEX pool, CEX custody, supply changes and token-account ownership are accounted for. A large Top10 share is not confirmed common control.
5. Identify cross-token redeployment/exit-cycle patterns at observable as-of times, preserve uncertainty about real owner, and independently reproduce any external group recurrence claim.
6. Return B03 `structural_hypothesis` plus at least one benign competing mechanism and a discriminating source query; F3 can be complete without any F4/F5 profitability claim.

## Output contract

Graph citations, group membership as a hypothesis, time window, null comparisons, contradictions and explicit unknown owner status.

Emit a versioned Bot handoff conforming to `knowledge/bot-handoff.schema.json` and the role-specific `knowledge/bot-knowledge-profiles.v1.json` (never silently assert externally reported material was locally reproduced). Request a peer review where the F Gate requires it. Handoff files are research artifacts, not authorization to trade or release new Monitor rules.

## Stop and approval policy

No raw edges or time/role ambiguity => missing-data report; CEX/common hub alone cannot establish same controller.

All tasks are read-only/paper-only. No private keys, signing, swap, order placement or on-chain broadcast. Independent research cannot grant itself Monitor rule release. Grok private skills must be added/enabled by the user after testing; they are not automatically registered by this GitHub directory.
