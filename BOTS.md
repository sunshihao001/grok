# Bot Architecture — Grok Bot Edition

## Overview

Multiple specialized **Development Bots** iterate on rules, skills, and evidence logic.
One **Monitoring Bot** is the finished product that consumes the frozen rules for ongoing Solana meme monitoring (paper-only / research).

All Bots share the same computer (user's) and can read this repo. State and artifacts go into `state/` or Bot memory / artifacts.

## Recommended Bot Set

### Development Phase (iterate rules)

1. **Rule Architect Bot**
   - Purpose: design and refine skill contracts, evidence schemas, gate logic.
   - Iterates on `rules/`, `design/`, CONTEXT.md.

2. **GMGN Data Bot**
   - Purpose: prototype and refine GMGN data ingestion, field mapping, byte-combination reasoning.
   - References qb- and design/phase1-research/.

3. **Wallet Structure Bot**
   - Purpose: iterate wallet-roles, wallet-structure, chip-control, same-source detection.
   - Theory from meme- knowledge base.

4. **Evidence & Gate Bot**
   - Purpose: evidence-chain, trade-gate, negative-gate, paper validation.
   - Ensures Safe Mode and auditability.

5. **QA / Fixture Bot**
   - Purpose: maintain fixtures, test cases, acceptance criteria.

### Production

6. **Meme Monitor Bot** (final product)
   - Purpose: run the frozen Phase 1 pipeline on candidate tokens or trending lists.
   - Output: structured reports, gate decisions, Telegram-style summaries.
   - No development rights; only executes approved rules.

## Workflow

- Dev Bots propose changes via PRs or direct commits to feature branches.
- Human or Review Bot freezes versions (tag or `rules/frozen/`).
- Monitor Bot pulls latest frozen rules.

## Safety

All Bots inherit the Solana Meme Safety Boundary from AGENTS.md / CONTEXT.md.
No Bot may access private keys or broadcast transactions without explicit future human approval.

## Knowledge responsibilities (Grok Edition)

The above six roles remain unchanged. All six read `knowledge/README.md` and the source-pinned catalog before specialist work; **none treats the historical corpus as verified signal data**.

- Rule Architect: choose the relevant knowledge mechanisms and formulate falsifiable hypotheses, including what evidence could disprove them. Do not freeze models solely because they exist in the source archive.
- GMGN Data: own field-level raw source/units/time validity; produce a traceable normalized observation, not label-based identities.
- Wallet Structure: compare financing, time behavior, role candidates and alternative benign explanations.
- Evidence & Gate: preserve contradictory evidence, missing observations and stopping rules; distinguish report state from trades.
- QA / Fixture: challenge legacy claims, build controls and real-case replay, track false alerts and sample leakage.
- Meme Monitor: **read the knowledge lenses attached to observation output**, fetch relevant new evidence, avoid causal claims from a single metric. Remain non-developing and read-only.

Each cross-Bot handoff should contain `knowledge_ids`, pinned source URLs, applicability conditions, actual observed evidence, alternative explanations, missing evidence and the outcome of independent checking.

## On-demand research packet handoff

- Rule Architect chooses hypothesis / population / refutation plan, without reusing published thresholds as trading rules.
- GMGN Data Bot and Wallet Structure Bot retrieve only relevant source docs through the `research` intake packet and verify actual time-of-knowledge for source fields.
- Evidence & Gate Bot requires a denominator, counter-example/null model and source-linked factual ledger, and never calls an observed cluster 'profitable alpha'.
- QA / Fixture Bot tries selection bias, out-of-time features, shared infrastructure and sensor failures before promoting research claims.
- Meme Monitor remains one read-only runtime Bot. It must not ingest third-party documents wholesale or update approved rules by itself.
