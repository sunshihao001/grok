# Role-based knowledge reserves (initial research)

**This is a skill-and-knowledge curriculum, not evidence that Grok Bots are installed, trained or financially validated.** The complete source map lives in [bot-knowledge-profiles.v1.json](bot-knowledge-profiles.v1.json), with 7 separate role files under `bots/profiles/`.

## Why not seven copies of the full corpus?

- Common K0: role, no-trade limits, source reliability, the D01–D12 atlas, F0–F6 evidence gate, and a minimal roster.
- Local K0: a few historically documented conceptual cards **plus** explicit false-inference boundaries. Bot 03 needs wallet mechanics; Bot 04 needs an execution economist's objective, not just wallet tags.
- K1: few (typically 2–5) on-demand **pinned source documents** selected by research mechanism, from `knowledge/source_index.v1.json`. A source is guidance or externally reported evidence, never automatic truth.
- K2: query-specific raw source ledger, with `event_at`, `available_at`, `decision_cutoff_utc`, signature/slot, coverage, errors, comparison population and negative controls; **not yet implemented as verified live corpus**.

## Important distinctions

The user-owned `meme-` source contains an approved multi-Agent/multi-strategy direction and a counterexample-first design. These matter to B01/B04/B05/B06 and must not be buried as a single FCZ strategy. The original Hermes snapshot contained illustrative wallet thresholds and a fabricated uncalibrated 0.8 confidence calculation; treat these as anti-patterns requiring independent tests, not production truth.

B03 can discover funding-cluster structures and exclude hub confounders; B04 must measure incremental predictiveness and executable profit. B05 separately challenges both; B06 separately replays cases. B07 has no authority to invent rules and must not spend runtime calling six research Bots per token.

## Explicit source IDs to add (selected, not bulk migration)

`meme-falsification-experiment` and `meme-multistrategy-direction` from pinned `meme-`, plus `external-post-detection-results` and `external-reentry-negative` from the external adversarial study. Their file existence was checked at the pinned commits. This increases K1 pointers from 17 to 21 **without importing source text**.

## Quality and governance

All `resident_knowledge` entries are **competency targets**, not proven claims; every one identifies a mechanism and a prohibited inference. For each Bot, `legacy_card_ids` reuse existing curated cards, `read_on_demand_source_ids` point to pinned K1 documents, `k2_required_fields` define primary fact requirements, and `consumes_from/produces_for` define upstream and downstream handoffs. The single monitor reads frozen versions only. Add examples and real replay cases gradually; a source index pointer, snapshot or generated text never counts as a passed market experiment.
