---
name: research-intake
description: Normalize Solana Meme research question, route ontology and pinned sources, and create an evidence-ready task brief without inventing market facts.
---

# research-intake

**Status:** draft skill *template*. Phase 1: **Paper-Only**. This is not proof of installation or review in the Grok UI. Role owners: B01, B02, B03, B04, B05.

## When to use

Normalize Solana Meme research question, route ontology and pinned sources, and create an evidence-ready task brief without inventing market facts.

## Inputs and approved access

Natural-language question; objective EXPLAIN/PREDICT/ECONOMIC; population, as-of decision time; optional transaction sources.

## Source-aware steps

1. Read AGENTS.md, the ontology and knowledge/system/filter-policy.v1.json. Establish objective, affected market phase, population, decision_cutoff_utc and outcome window only if predicting.
2. Run `PYTHONPATH=src python -m solana_meme_os.research --question "具体研究问题"` with `--decision-at` when applicable. Treat literal keyword routing as a shortlist, not complete cognition.
3. Run `PYTHONPATH=src python -m solana_meme_os.bot_knowledge --bot B01 --question "具体研究问题"` (substitute actual Bot ID). Read only 2–5 relevant K1 pinned source documents, with license-aware citations; expand when challenged by conflicting evidence.
4. Write a task-specific B01 `research_brief` handoff containing population, source IDs, candidate knowledge IDs, competing mechanisms, missing data and target F gates. Source citation is not chain proof.
5. Assign only the needed Bot(s): B02 data, B03 actor graph, B04 prediction/economics; B05 must independently scrutinize important claims. Do not summon all Bots by default.
6. Use `PYTHONPATH=src python -m solana_meme_os.bot_knowledge --validate-handoff <file>` before handoff; it checks format, not correctness.

## Output contract

Auditable task brief, 2–5 source candidates, task-specific missing evidence list, precise F0/F1 status and follow-up owner.

Emit a versioned Bot handoff conforming to `knowledge/bot-handoff.schema.json` and the role-specific `knowledge/bot-knowledge-profiles.v1.json` (never silently assert externally reported material was locally reproduced). Request a peer review where the F Gate requires it. Handoff files are research artifacts, not authorization to trade or release new Monitor rules.

## Stop and approval policy

If question lacks an as-of, origin or coverage, label research-only; no source match => SOURCE_DISCOVERY_REQUIRED. Never infer a trade.

All tasks are read-only/paper-only. No private keys, signing, swap, order placement or on-chain broadcast. Independent research cannot grant itself Monitor rule release. Grok private skills must be added/enabled by the user after testing; they are not automatically registered by this GitHub directory.
