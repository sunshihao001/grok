# Design Overview — Grok Bot Edition

## One-sentence system

GMGN data → specialized Grok Bots (dev iteration) → evidence-grade wallet research → gated judgment → paper validation → (future) semi-auto.

Runs on Grok Bots instead of Hermes skill runtime. Lightweight, interruptible, recoverable, auditable.

## Phase roadmap (same as Hermes)

| Phase | Name | Status | Scope |
|-------|------|--------|-------|
| 0 | Workflow Contract | Design done | Directory / Schema / State / Rules / Prohibitions |
| 1 | Research Pipeline | Design done | Skills + Controller |
| 2 | Paper Trading | Not started | Paper simulation + review |
| 3+ | Auto / Semi-Auto | Forbidden until human freeze | — |

## Skill pipeline (Phase 1)

```
Candidate token (CA or trending)
  → meme-candidate-entry
  → meme-token-panel
  → meme-wallet-roles
  → meme-wallet-structure
  → meme-evidence-chain
  → meme-trade-gate
  → workflow summary (BLOCK / WATCH / PAPER_ONLY / NEED_MORE_DATA)
```

Full skill contracts live in the original Hermes repo (`design/phase1-skill-*.md`).
This repo will host the Grok-adapted versions and iteration history.

## GMGN integration

Reference:
- Original design research: sunshihao001/- / design/phase1-research/
- Tool prototype: sunshihao001/qb-
- Theory: sunshihao001/meme-

Bots may call external tools or scrape only in Safe Mode; never sign or broadcast.
