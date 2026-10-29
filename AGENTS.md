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

## Staged KB-001 intake (incremental)

- Preserve the existing 15-card catalog, 21 historical snapshots, knowledge.py API and associated tests. Do not overwrite established knowledge or treat archived text as confirmed.
- Consult `docs/knowledge-intake.md` and `knowledge/registry.v0.json` for source-pinned incremental packs; read `knowledge/packs/KB-001-evidence-bounds.md` on relevant evidence-boundary tasks.
- `reference_only` means explanation and disconfirmation prompts, never an executable gate or proven return.
