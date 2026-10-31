# Solana Meme knowledge is the core; Grok is the host

**Purpose:** preserve the expert learning, domain research, adversarial perspectives and practical lessons from three earlier projects while discarding Hermes-specific *runtime* assumptions. A working Bot without validated external knowledge is only orchestration.

## Project scope update (2026-10-31)

**This knowledge base serves market-wide Solana Meme event, wallet-cluster, funding-network, market-structure and risk research; copy trading is one specialist use case.**

Existing 15 resident concept cards and 21 historical snapshots are a bounded legacy baseline, not a full market ontology. The on-demand registry now has **22 curated source pointers** across legacy Hermes, meme-, qb-, Why-Solana and OKX read-only documentation.

Primary knowledge pathway: observed events and time windows -> wallet/asset networks -> conditional normal baseline and competing mechanisms -> market structure and risk -> independently tested prediction/paper economics.

Start from [system integration](../docs/knowledge-system-integration-v1.md) and [system-intelligence Skill](../skills/solana-meme-system-intelligence/SKILL.md), then selectively read original source files. Monitor and event-observatory code do not establish abnormality or trader identity.

## Expert knowledge routing (2026-10-31)

The initial 15 cards and 22 source pointers are now mapped into [17 expert disciplines, 12 domains and five dynamic investigation scenarios](expert-capability-map.v1.json). The map is a **knowledge coordination contract**, not an implemented Grok multi-agent runtime. The optional deterministic `python -m solana_meme_os.expert_router --event FUNDING_FANOUT` suggests source-bound expert panels; it is not independent analysis or an automated strategy. For actual cross-disciplinary source and counterexample reasoning, read [expert orchestration](../docs/solana-meme-expert-knowledge-orchestration-v1.md) and [R002 cross-examination case](cases/R002-expert-cross-examination-v1.md). Experts can question or invalidate prior conclusions and introduce new ontology instead of forcing every question through the old eight-layer gate.

## Evidence-connected knowledge architecture V2 (2026-10-31)

- [Cross-layer expert connections](../docs/knowledge-expert-interconnection-v2.md): open-world, evidence-driven expert collaboration rather than eight mandatory sequential gates.
- [Typed interaction graph](expert-interaction-graph.v1.json): 32 directional handoffs across all 17 disciplines, with evidence artifacts, refutations and re-evaluation triggers.
- [External method sources](external-method-sources.v1.json): 12 checked references from official chain/stream/provenance/agent specifications and relevant causal/drift research, linked to graph edges.
- `src/solana_meme_os/expert_interaction.py`: deterministic read-only checking and transitive challenge impact planning. Neither expert routing nor claim dependency calculation is proof of real agent orchestration.

## What has been migrated

The initial catalog has 15 source-pinned cards in `knowledge/catalog.v1.json` covering:

- **Market mechanics:** pump-style token/pool lifecycle, mint/freeze/security, reserve depth, liquidity withdrawal vs repricing, GMGN discovery streams.
- **Actors and relations:** wallet role candidates, deployer history, early buyers/snipers, financing graphs, CEX infrastructure exclusions, Sybil/wash/coordination alternatives, holder concentration and entity-control differences.
- **Interpretation discipline:** multi-source evidence chain, contradictory evidence, missingness, research-only gates and source/unit verification.
- **Legacy hypotheses:** first-control-zone/POC/AVWAP reclaim. Useful for research but not validated as a Solana signal.
- **Reliability:** Hermes Harness anti-fake-completion and calibration learning, independent of Hermes command/hook machinery.

Each unit is a **portable knowledge candidate**, with a pinned original GitHub commit + path, `mechanism`, `required_evidence`, `alternative_explanations`, `inference_limit`, `next_check` and status. These are not a claim that sources are empirically validated; source traceability and truth are different things.

## How knowledge changes runtime behavior

- **Simple user request** → `python -m solana_meme_os.knowledge --question "这批钱包资金同源吗"` returns relevant knowledge and missing verification work.
- **Monitoring snapshot** → `python -m solana_meme_os.monitor ...` now appends `knowledge.interpretation_candidates` to observed changes. The cases must be evaluated against real source data.
- **Research/QA Bots** → read the same cards, scrutinize source evidence and develop independently testable alternatives.
- **Monitor Bot** → cannot promote a hypothesis to a real trade/risk conclusion; it can only report observed changes, provenance, missing inputs and plausible mechanisms.

Literal keyword routing is a reproducible **minimum interface**, not deep understanding. Grok's real language understanding needs an actual configured Bot that reads these cards and selectively retrieves primary evidence. It must be free to discover **new** mechanisms rather than being trapped by this list.

## Three status labels

- `source_contract`: known source's proposed input/output epistemic separation; not an externally certified standard.
- `documented_legacy_method`: a method or proposed workflow documented in historical source, not yet evaluated on market outcomes.
- `unverified_hypothesis`: a historical strategy or causal hypothesis requiring source data, representative positive and negative cases and independent review.

Do not confuse any label with 'empirically proven'.

## Beyond this first wave

A complete repository-wide migration has **not** happened. The first wave now includes **21 exact historical Markdown snapshots** in `knowledge/legacy-snapshots/` with a source manifest, plus 15 curated and actively routed cards. These snapshots preserve domain explanations, proposed methods and historic design contracts without any Hermes executable runtime. Most original data, notebooks, historical case evidence, tags and the full Hermes project remain in their source repos. Missing real case replay, authoritative field mappings, blind evaluation and release-calibration loops are listed in `docs/next-steps.md`.

Recommended future package structure: `knowledge/catalog.v1.json` (indexed), `knowledge/cases/` (original on-chain observations and labelled outcomes, without secrets), `knowledge/claims/` (tested and superseded claims), and `knowledge/evaluations/` (comparison against no-knowledge Bot). Do not create empty folders or call them implemented.

## Entry-point commands

    PYTHONPATH=src python -m solana_meme_os.knowledge --question "GMGN热门能证明这币安全吗？"
    PYTHONPATH=src python -m unittest discover -s tests -v

References: `docs/sources.md`, `knowledge/legacy-audit.md` and `skills/solana-meme-knowledge/SKILL.md`.

## Second wave — do not bulk migrate

New model: keep the resident 15 cards and 21 prior snapshots as a bounded historical baseline, but use `knowledge/source_index.v1.json` to consult external specialist sources **on demand**. The repo now indexes 22 curated source entries, including methodological references from `Why-Solana-Memecoins-Are-Over`, without importing its licensed analysis into Grok. Run `python -m solana_meme_os.research --question ...` to create an evidence intake packet; see `docs/on-demand-research-design.md`. The goal is better judgment, not maximizing token count or the number of copied files.

## Expanded anomalous-wallet source research (2026-10-31)

[Fourteen screened source projects / studies](reference-project-discovery.v1.json) are categorized by actual README/source-code/methods review depth, ability to transfer into Solana source or network evidence, and explicit false-positive risks. [Research report](../docs/anomaly-wallet-reference-expansion-v1.md) distinguishes forensic signature replays, developer funding monitors, holder graph methods, time-safe academic comparisons, source-label retractions, and marketing-only risk scores. Four typed relationships (L33–L36) were added to the [expert interaction graph](expert-interaction-graph.v1.json), now **36** entries, with no live monitoring rule or Bot deployment change.
