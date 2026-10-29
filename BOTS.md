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
