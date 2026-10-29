# CONTEXT — Solana Meme Workflow OS (Grok Bot Edition)

Glossary and domain language. Adapted from Hermes version for multi-Bot iteration.

## System Terms

- `Solana Meme Workflow OS`: GMGN-entry + wallet-intel + evidence-chain + gated paper-only Solana meme research workflow.
- `Grok Bot Edition`: Multi-agent version using specialized development Bots for rule iteration + one production monitoring Bot.
- `Phase 1`: research pipeline only; no live trading.
- `Safe Mode`: forbids real orders, private key access, signing, transaction broadcast, swap, auto deploy.
- `Evidence Pipeline`: every decision preserves evidence, counter-evidence, missing fields, confidence, downgrade reasons, blockers.
- `Phase State`: JSON state for interrupt/resume/audit (local to Bot or shared via repo/artifacts).

## Skill Terms (core pipeline)

- `meme-candidate-entry`: validates candidate token address and creates initial run state.
- `meme-token-panel`: collects token info, security, pool, K-line summary.
- `meme-wallet-roles`: classifies wallet behavior; GMGN labels are hints only.
- `meme-wallet-structure`: analyzes holder concentration, same-source funding, coordinated timing, structure risk.
- `meme-evidence-chain`: combines into narrative evidence chain.
- `meme-trade-gate`: produces gate decision from evidence and rules.
- `meme-workflow-controller`: orchestrates skill order and summary.

v2 extensions (from freeze candidate): structure-evidence, chip-control, lifecycle-classifier, negative-gate, paper-validation-and-attribution.

## Gate Decision Terms

- `BLOCK` / `WATCH` / `PAPER_ONLY` / `NEED_MORE_DATA`
- Future: `SEMI_AUTO_READY` / `AUTO_READY` (forbidden in Phase 1)

## Bot Roles (this edition)

- Development Bots: iterate rules, skills, evidence logic (multiple specialized).
- Monitoring Bot: finished product that runs continuous or on-demand monitoring using frozen rules.

See `BOTS.md` for details.
