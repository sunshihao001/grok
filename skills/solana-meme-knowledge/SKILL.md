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

## Deep research without forced case-first verification

For *conceptual domain research* into economic agents, funding, same-control attribution, token holders, wallet roles and market mechanisms, read `knowledge/domain/L3-actor-economic-mechanisms-deepstudy.md` selectively for the relevant issue and the five existing E-L3 specialists' knowledge contracts. Use first-party Solana/Jito/protocol documentation to ground protocol facts; distinguish logically derived mechanisms from empirical hypotheses. **Do not demand a K2 token case or backtest before doing deep knowledge exploration**; cases and execution replay are a later empirical phase. Equally, do not treat mechanism research alone as verified smart-money identity, profitable alpha, or monitor release. No new agents or required 21-expert chain.

## Domain-depth knowledge: use the existing D01–D12 structure

After selecting domains with `knowledge/system/ontology.v1.json`, consult [knowledge/domain/README.md](../../knowledge/domain/README.md) and read **only the relevant specialist file**: `L1-L2-chain-market.md` (D01/02/03/10), `L3-wallet-actors.md` (D04/05/06/07), `L4-L5-copytrade-edge.md` (D08/09), or `L6-L7-investigation-cases.md` (D11/12). These are **domain_method_candidate** content to guide concrete observations and discriminating checks, not validated K2 market claims or approved trading rules. Preserve the existing 15 source cards and the F0–F6 boundaries; do not indiscriminately load all specialist files for every question.

For a wallet-copytrading question, never stop at wallet PnL or a provider smart-money label: explicitly separate real swap/transfer observations, wallet capital relationships, earliest follower data availability, actual two-sided quote coverage, and follower net outcome. For a new-token investigation, first resolve Mint/program/market stage/pool before interpreting wallet and holder statistics. Apply `knowledge/source-admission.v1.json` before external K1 retrieval; review-only sources may only be read during an explicit source audit and must not be treated as independently verified facts.
