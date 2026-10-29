# Project Agent / Bot Rules — Solana Meme Workflow OS (Grok Edition)

## Safety Boundary (Hard)

Phase 1 is read-only research / paper-only gating.

**Forbidden for all Bots**:
- real orders
- private key access
- wallet signing
- transaction broadcast
- gmgn-cli swap / multi-swap / cooking create
- auto deploy
- claims like “确定庄家”, “确定内幕”, “一定会涨”

## Roles

See `BOTS.md` for the multi-Bot development + single Monitor design.

## Required Reading Before Work

- `CONTEXT.md`
- `BOTS.md`
- Relevant design docs (link back to original Hermes repo for full history)

## Completion

Every significant rule or skill change should produce a short result note under `reports/`.

## Knowledge-preserving migration (mandatory)

- **Do not import Hermes startup, CLI, control hooks, absolute paths, memory store or runtime behavior.** Prior Hermes and qb- repositories are evidence/source archives, not Grok OS dependencies.
- Start with `knowledge/README.md` and `knowledge/catalog.v1.json`. Use `PYTHONPATH=src python -m solana_meme_os.knowledge --question "普通语言问题"` as a retrieval triage tool; this is not a substitute for reasoning or research.
- For each claim, select knowledge **by relevance and mechanism**, then test whether required inputs exist. Never copy the rule's conclusion just because keywords match.
- Label historical claims as documented_legacy_method / unverified_hypothesis / source_contract. Historical provenance does NOT validate financial effectiveness.
- A rule release requires actual market/source data, counterexamples, error attribution and independent review. Revisions go to a reviewed PR, not automatic self-upgrade.
- When retrieval has no match, explicitly expand research, add sources and a candidate card; never hallucinate missing knowledge.

## Demand-driven source reasoning

For ambiguous research tasks run `PYTHONPATH=src python -m solana_meme_os.research --question "原始问题"` and review `docs/on-demand-research-design.md`. Never fill a prompt with the entire corpus or mistake keyword matching for understanding. Use sources selectively and challenge them using original primary data. Record decision_at, observed_at, available_at; no future-info features. Treat statistical pattern detection, causal explanation and positive net executable expectancy as three independent evidentiary claims.

## Unified knowledge-system constraints

Read `knowledge/system/README.md`, `ontology.v1.json`, `MIGRATION.md`, and `RESEARCH.md` for knowledge/rule work. The taxonomy is structurally complete while the evidence remains incomplete. Never auto-promote an external study, keyword match, historic wallet category, or unvalidated strategy to Monitor rules. Preserve research population, cutoff, counterexamples, source validity, costs, unknowns, and independent review. Run `PYTHONPATH=src python -m solana_meme_os.knowledge_system --audit`.
