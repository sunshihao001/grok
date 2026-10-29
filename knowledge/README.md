# Solana Meme knowledge is the core; Grok is the host

**Purpose:** preserve the expert learning, domain research, adversarial perspectives and practical lessons from three earlier projects while discarding Hermes-specific *runtime* assumptions. A working Bot without validated external knowledge is only orchestration.

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
