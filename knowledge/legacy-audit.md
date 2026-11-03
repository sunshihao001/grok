# Audit: concepts worth preserving versus claims that cannot be inherited as fact

Historical origin: `sunshihao001/-` learning/ and design/, `sunshihao001/meme-` semantics/risk, `sunshihao001/qb-` GMGN script and Hermes Harness anti-self-deception records. The pinned paths and revisions are recorded in `knowledge/catalog.v1.json`.

## Keep as methods and questions

1. GMGN trending/trenches/signal are *distinct discovery surfaces*; none is inherently a verified profitable signal.
2. Wallet identity and control inference should combine funding, timing, transaction content, holder and deployer history. Labels are defeasible hypotheses.
3. Pool liquidity and effective exit depth differ; distinguish LP reserve transfers from USD repricing, routing and market microstructure.
4. Chain evidence must retain competing explanations, missing variables, data validity windows and source dependence.
5. Feedback should compare earlier predictions or monitored hypotheses against later observed outcomes, not model self-scores.

## Quarantine as unvalidated causal shortcuts

- Historical `learning/01-04-基础理论/04-链上本质思维工具箱.md` says near-instant buys are 'basically bots or insiders'; a 2-second threshold has no demonstrated specificity and bots need not be internal.
- 'Shared Binance withdrawal funder = same owner' confuses shared exchange infrastructure with identity; custody paths need exclusion.
- 'Synchronized sells prove common controller' is invalid without controlling for market/news/automation responses to the same event.
- 'Price correlation >0.8 means same operation' confuses common market exposure and causality.
- Historical evidence chain starts from arbitrary confidence 0.8 and increments based on signal weights; no calibrated predictive dataset justifies interpreting it as actual probability.
- Theory repo's 'first control zone' is preliminary and susceptible to hindsight selection; do not infer a single hidden 'dealer' from a price range.
- GMGN `smart_degen` / `bundler` / `rat_trader` are vendor categories, not verified owner or economic-intention labels.

## When to promote to operational reasoning

Define observational units and data source; freeze before outcome; test failure/negative and ordinary control cases; report coverage, missingness, false alerts, alternate explanation and out-of-sample transfer. Rules must be reversible and versioned. Preserve historical text for study, not as the new Grok OS's default truth.

## 2026-11-02 REF-002 source-code audit addendum

**Reference identity correction:** REF-002 `sunshihao001/-` is a **Solana Meme / GMGN trading research and knowledge source**, with learning/05–16, first-principles research, strategy/market/actor/structure design, executable historical Skills and fixture tests; not merely the deprecated Hermes runtime. [Project origin audit](system/reference-projects-meme-knowledge-audit-20261030.md) had already made this point on 2026-10-30 and [legacy snapshots manifest](legacy-snapshots/manifest.json) already retained 16 documents from this repo. The former REF-002 source-index role and P1-only trigger were inconsistent with those audits and have been corrected **in place** to P0 in [65-asset index](system/gpt-meme-project-index.v1.json). This is a retrieval/priority failure, not proof that the old knowledge was never saved.

**Code-level results from pinned [old Skill04](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/skills/meme-wallet-structure/scripts/run.py):**

- `_coordinated_buy_groups` groups at least 3 holders by `start_holding_at // 300` without checking the confirmed swap transaction. The output is a same-5-minute **holder-start-time candidate**, not proof of coordinated purchases.
- `_distribution_groups` groups addresses when cumulative `sell_amount_percentage > .5`, regardless of actual selling timestamps, counterparties or funding ties. It cannot establish coordinated distribution.
- `_suspected_controllers` gives `strong` evidence to a source funding >=3 wallets whose combined reported holding exceeds 5%; public CEX/service-funder counterexamples remain untested. The `confidence_score` starts from .8 and applies a missing-data deduction; it is **not** a calibrated probability of economic ownership.
- [Old fixture E2E](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/tests/test_fixture_e2e_pipeline.py) explicitly avoids live GMGN. Implementation/fixture tests are not evidence of current real-wallet attribution performance.

**Revised inheritance:** keep the early market-fact → on-chain-trace → feature → competing-mechanism exploration, [2026-05-26 grill](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/grill-sessions/2026-05-26-grill-bytes-to-framework.md), wallet/role/capital/inventory research, counter-evidence and missing-data design; retire universal short-time/ratio thresholds and causal actor claims until independently evaluated. [Why-Solana PITFALLS P10/P12/P13/P14/P15](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/PITFALLS.md) provides competing empirical-method examples, not a ready-made calibrated production rule. Details, uncertainty and the newly corrected navigation gap belong to the *existing* [L3 economic actor study §16](domain/L3-actor-economic-mechanisms-deepstudy.md); no new taxonomy or runtime is authorized.
