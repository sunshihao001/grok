---
name: solana-meme-knowledge
description: Select and apply source-pinned Solana Meme domain knowledge to plain-language problems and monitor observations, preserving alternative explanations.
---

# Portable expertise, not Hermes runtime

Inputs: user's plain-language question, new source-linked observation data, knowledge/catalog.v1.json, optional original source refs and read-only research tools.

1. Read `knowledge/README.md` and `knowledge/method.md` first. Inspect the relevant source-pinned cards and read their `snapshot_path` when available (see `knowledge/legacy-snapshots/manifest.json`); use them as hypotheses/method lenses, **not as automatic answers**.
2. Optionally preselect via `PYTHONPATH=src python -m solana_meme_os.knowledge --question "用户原话"`. It uses literal keywords only and is not the final expert selection; retrieve additional concepts if they better match the underlying mechanism.
3. Distinguish observed fact, upstream vendor inference, your hypothesis, counterevidence and unknown. For each hypothesis identify required evidence that would *disprove* it and source timeliness.
4. If a source or field is missing, decide whether additional investigation could change the conclusion; otherwise issue UNKNOWN/STOP and avoid misleading precision.
5. Return a useful conclusion with provenance, alternatives, next observation and limitations. Only a separate verified rule improvement PR can alter Monitor behavior.
6. For new insights create a proposed source-pinned card with failure cases. Do not rewrite source history or treat a bot-generated claim as validated truth.

Prohibitions: No automatic trades, private keys, swap, signing, broadcast or fake live claims. No dependencies on Hermes binaries, /HER_* commands, hooks or fixed local directories. Offline catalog checks do not prove live analytics.

## On-demand source selection and time-locked evidence

Begin a novel question with `PYTHONPATH=src python -m solana_meme_os.research --question "原始问题"`. Inspect the returned `sources`, then obtain **only** the needed pinned source documents; `--fetch-excerpts` is optional read-only GitHub preview and may be unavailable. Study `docs/on-demand-research-design.md` and `knowledge/source-index-README.md`. Cite original authors and source revisions.

A research packet without `observations.accepted` is NOT a verified market answer. When decision timing matters, pass `--decision-at` and evidence entries containing observed_at and available_at; reject later or missing data. Do not turn the Why-Solana study's detected structural patterns into copy-trading alpha: the external report contains examples of detectable patterns without proven executable profits (review-only; no independent local replication). New findings require negative controls, a frozen evaluation plan and evidence of costs/latency.

## Full-system knowledge use

Consult `knowledge/system/README.md` and `ontology.v1.json` for cross-domain prerequisites and `knowledge/system/RESEARCH.md` for the structural/predictive/economic separation. New external findings in `research-units.v1.json` are claims for adversarial investigation, never auto-published trading rules. `python -m solana_meme_os.knowledge_system --question "问题"` is only literal domain navigation.

## Per-layer specialist reasoning (internal research personas, not deployed Bots)

Consult `knowledge/experts/README.md` and `knowledge/experts/registry.v1.json` **after** selecting a concrete problem. Optionally call `PYTHONPATH=src python -m solana_meme_os.expert_brief --question "problem" --objective EXPLAIN` to obtain a deterministic 1–3-specialist brief, or `--expert-id E-L3-02` for a specific specialist. The selector does **not** execute 21 agents, reason over live Solana transactions, authorize rules, or fetch external sources. Read the chosen experts' specialist knowledge and `decisive_next_check`, ask a competing expert to challenge the underlying mechanism when needed, then retrieve only admitted K1 and real time-safe K2 evidence. Return fact, mechanism candidates, conflict, discriminating query, UNKNOWN/stop and source refs. B07 is frozen monitoring and may never dynamically change trading research rules.

## Project-origin first: use prior Meme trading expertise, not a generic DeFi syllabus

Read `knowledge/system/reference-projects-meme-knowledge-audit-20261030.md` before proposing the next mechanism-first Solana Meme study. The original business problems are key-wallet selection from qb- GMGN token reports (top holders, smart money, bundlers, transfer_in, realized/unrealized PnL), Hermes funding/sybil/chip-control and evidence/Gate, and meme- FCZ/deep wash/dead market/second launch plus its explicit multi-strategy pivot. Focus the lead expert on **what a specific Meme wallet role means at creation-slot/curve/migration, how capital and sellable inventory evolve, when the follower can actually know, and whether a later phase remains worth researching**. Generic CPMM/CLMM math is on-demand technical support, not the first research deliverable. First planned brief: `knowledge/domain/D04-D08-key-wallet-followability-research-brief.md`. Old D03 brief is now ancillary and its prior main-track label is superseded. Preserve review_only restrictions on Why-Solana and never claim source review verified live profitability.

## Mechanism-first, expert-deepening knowledge work (current research policy)

For broad theoretical Solana Meme research, apply `knowledge/system/expert-mechanism-research-method.md` **before** enumerating 152 units. Take one **economically meaningful core contradiction**, select one lead expert in the existing 21-lens registry, trace downward to protocol objects, rights, cash flows and state transitions, then reason upward to incentives, market impact, follower information and conditions where the conclusion fails. Bring in only cross-domain specialists whose different causal model changes the lead explanation; retain contradictions rather than majority voting. Backfill implications into the original Dxx-Kxx IDs and select next work by the largest unresolved causal bottleneck, not the next integer. Use `knowledge/system/mechanism-research-plan.v1.json` for current priority and `knowledge/domain/D03-market-price-mechanism-research-brief.md` for the first planned D03 inquiry. **Do not confuse a plan, domain map or theoretical example with completed investigation, verified Alpha or permitted monitor rule.** Keep source-admission, epistemic and operation approvals unchanged.

## Whole-domain expert research map (existing ontology, not a new workflow)

For broad knowledge work, start with `knowledge/system/whole-domain-expert-handbook.md` and `knowledge/system/whole-domain-atlas.v1.json`, NOT a case/backtest or an all-expert chain. Each of D01–D12 has 12 atomic research units, plus 8 governance units for L0. Select the smallest required domain subset and one lead expert via the existing `knowledge/experts/registry.v1.json`. For the user's precise question, use the matching unit's `expert_question`, `mechanism_to_study` and `forbidden_shortcut` as investigation lenses; then deepen with first-party references and meaningful competing mechanisms. The atlas marks every unit `mapped_unverified` and is **not itself an assertion that the unit is researched, source-verified, market-tested or tradable**. The domain's prior specialist files remain the content source; respect the source-admission policy, existing K0/K1/K2 layers and Frozen Monitor boundary. Never load all 152 units as a runtime prompt, generate new bots, or upgrade unknown observations into approved trade instructions.

## Fund capital organization: a deep specialist route, not a caution checklist

When the actual user's question concerns a common funder, alleged group wallets, coordinated capital, or a potential controller, start from existing `E-L3-02` via `knowledge/domain/L3-E-L3-02-capital-organization-incentives.md` after the broad expert desk. Do NOT stop with generic alternatives (CEX versus owner versus bot) or a fabricated confidence score. Ask what the transferred capital is **doing** (principal, execution sponsorship, custody, LP, creator/protocol fees, settlement), who bears the loss, who can authorize transfers, and who receives cash flow. Draw conditional consequences for token inventory, independent demand, AMM reserves, fee incentives and follower prices. Use the 1,000,000-token/100-SOL fee-free CPMM example only as declared theoretical intuition, never as live quote or strategy profitability. Distinguish an economic mechanism from an unobserved identity. Bring in only the specialist whose challenge could reveal a genuinely different causal or payoff mechanism. Use protocol/version-specific Raydium official docs, not fixed fee assumptions. Leave hypotheses theoretical until a separate empirical stage.

## Expert-first knowledge exposition (existing L0–L7)

When the user asks to **deeply understand** wallet roles, common funding, controller attribution, holder changes, creator series, or group timing, open `knowledge/domain/L3-actor-expert-perspectives.md` FIRST as a problem-driven five-expert desk. Pick ONE lead E-L3 specialist based on the market question; make their specialized economic judgment explicit and non-generic, describe at least two genuinely different mechanisms, and let a SECOND expert challenge a specific blind spot only when relevant. The answer should foreground what each specialist notices, why the mechanism matters and what new question it opens. Read `L3-actor-economic-mechanisms-deepstudy.md` only for the required supporting theory and primary references. Never present a long list of academic definitions as the answer, nor run all 21 specialists for rhetorical consensus. Preserve L/D mappings, source status, and no-live-alpha rules. Conceptual domain research does not require case-first K2 verification.

## Deep research without forced case-first verification

For *conceptual domain research* into economic agents, funding, same-control attribution, token holders, wallet roles and market mechanisms, read `knowledge/domain/L3-actor-economic-mechanisms-deepstudy.md` selectively for the relevant issue and the five existing E-L3 specialists' knowledge contracts. Use first-party Solana/Jito/protocol documentation to ground protocol facts; distinguish logically derived mechanisms from empirical hypotheses. **Do not demand a K2 token case or backtest before doing deep knowledge exploration**; cases and execution replay are a later empirical phase. Equally, do not treat mechanism research alone as verified smart-money identity, profitable alpha, or monitor release. No new agents or required 21-expert chain.

## Domain-depth knowledge: use the existing D01–D12 structure

After selecting domains with `knowledge/system/ontology.v1.json`, consult [knowledge/domain/README.md](../../knowledge/domain/README.md) and read **only the relevant specialist file**: `L1-L2-chain-market.md` (D01/02/03/10), `L3-wallet-actors.md` (D04/05/06/07), `L4-L5-copytrade-edge.md` (D08/09), or `L6-L7-investigation-cases.md` (D11/12). These are **domain_method_candidate** content to guide concrete observations and discriminating checks, not validated K2 market claims or approved trading rules. Preserve the existing 15 source cards and the F0–F6 boundaries; do not indiscriminately load all specialist files for every question.

For a wallet-copytrading question, never stop at wallet PnL or a provider smart-money label: explicitly separate real swap/transfer observations, wallet capital relationships, earliest follower data availability, actual two-sided quote coverage, and follower net outcome. For a new-token investigation, first resolve Mint/program/market stage/pool before interpreting wallet and holder statistics. Apply `knowledge/source-admission.v1.json` before external K1 retrieval; review-only sources may only be read during an explicit source audit and must not be treated as independently verified facts.
