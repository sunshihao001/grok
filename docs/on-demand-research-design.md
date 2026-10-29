# Knowledge on demand: prevent empty AI without bulk-importing repositories

Status: `ENGINEERING_BRIDGE_V0` (verified with offline tests only; no Grok cloud Bot has been observed running it)

## What changed after reviewing Why-Solana-Memecoins-Are-Over

Reference: https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over
Source pinned at `9a7ad51d56328e91e67e3f531d6744307d0ee68b`.
Author of the study: Benjamin Da Cunha. The repo's source code under code/ is MIT; written analysis under README/docs is CC BY-NC-ND 4.0. **Do not import its analysis verbatim or publish remixes; this project stores bibliographic pointers and an independently written methodology adaptation only.**

Lessons from direct reading:

1. `docs/METHODOLOGY.md` demands a definition, population, measurement, limitations and repeatable verification for important claims.
2. `docs/PITFALLS.md` openly documents failures due to selection bias, denominator drift, post-event data leakage, wrong control groups, infrastructure hubs and broken monitoring.
3. `coordination_detection/results.md` can identify statistically non-random funding/buy timing with null models **without** establishing identity/intent.
4. `post_detection_edge/README.md` and `docs/ACT_IV.md` distinguish structural detection from feasible net expectancy: a surviving statistical predictor still had negative return after costs in its declared trade simulation.
5. `post_detection_forensics/feature_dictionary.md` assigns feature observation cutoffs, while `temporal_leakage_audit.md` rejects fields not available at the decision.
6. `alpha_patterns/README.md` separates exploration from locked validation and documents null and negative findings. Extensive feature searches without clean holdouts can generate persuasive false patterns.

### Avoid the wrong lessons

- **Do not clone this project's conclusions as a Solana alpha rule.** Its population consists of alerts **already selected by a bundle-snipe detector**; the results are not claims about all Solana token launches.
- Do not interpret strong structural evidence as direct proof of a profitable copy-trade.
- Do not copy large public corpora, frozen outcome snapshots, wallet maps or licensed articles into grok. The user has explicitly prioritized selective knowledge use, not full migration.
- A frozen historical source may be outdated for current markets; pinning gives reproducibility, not currency.

## A three-level knowledge arrangement

**K0 — resident context (small):** the project's research goal, forbidden actions, epistemic levels, short process instructions and 15 local concept cards. No giant prompt.

**K1 — source router (on demand):** `knowledge/source_index.v1.json` points to relevant original Hermes, meme-, qb- and external methodological documents at specific commits. `src/solana_meme_os/research.py` creates a source/evidence packet for a question. `--fetch-excerpts` can obtain short read-only previews in memory; it neither clones nor stores these sources. File cannot substitute for an external analytical model or live market data.

**K2 — primary evidence (case-specific):** actual transaction signatures, pool data, raw GMGN outputs, temporal cutoffs, observed outcome and negative controls. These must be collected at investigation time. At present this project has **no verified live K2 market data**; fixture observations remain fixture-only.

## Investigation contract

1. Write the user's concrete question and the *decision timestamp*. Do not translate 'track profitable wallets' into a vendor-tag filter without first defining what net profitability and execution window mean.
2. Select at most a few relevant sources; inspect them and their counterexamples. If no source matches, record `SOURCE_DISCOVERY_REQUIRED`, expand research rather than hallucinating.
3. Create a source-linked evidence ledger: raw fact, provider derivation, interpretation, alternative explanation, excluded confounders and missing fields.
4. **Time-of-knowledge gate**: observed_at and available_at must not be later than decision_at. Explicitly reject missing timestamps or post-event labels.
5. State a falsifiable hypothesis, define denominator and real negative/null control, and test distinctness from other established factors.
6. Keep explanatory ability (what happened) separate from predictive ability (what happens next), and predictive ability separate from realizable net return.
7. Capture failed ideas in a dated case/negative-result record, not permanent hard-coded dogma. Human approves any new production monitor rules.

### Commands

    PYTHONPATH=src python -m solana_meme_os.research --question "同源资金是不是交易所基础设施，如何排除？"
    PYTHONPATH=src python -m solana_meme_os.research --question "跟单信号什么时候已知？" --decision-at "2026-10-29T07:00:05Z"
    PYTHONPATH=src python -m solana_meme_os.research --question "钱包协调是否有可执行优势？" --fetch-excerpts

Optional evidence file is a JSON array of objects with `claim`, `source_ref`, `observed_at`, `available_at`. The last flag makes network requests to pinned public GitHub files; it can fail and is not required for offline tests. Do not commit raw third-party licensed source previews or private market/API credentials.

This command produces a *research intake packet*, **not a market conclusion or trading instruction**. Real Grok comprehension, tool selection, validation and execution of external research remain to be tested in the Bot environment.

## Acceptance to prove this solves 'empty AI'

Use blinded, source-linked cases, including questions deliberately **outside** the 15 concept cards:

- can the Bot recover the right original facts or is it reciting generic advice?
- can it identify one alternative mechanism and a discriminating next data query?
- does it reject lookahead features, missing data and shared infrastructure false positives?
- does it preserve failure/negative evidence, not just successes?
- does the knowledge-enabled Bot produce materially better source accuracy and fewer false claims than a no-knowledge or prompt-only baseline?

Measure source accuracy, decision-time validity, unsupported claims, false alerts and unresolved items. Then run an independent reviewer and real on-chain replay. Until this comparison is run, **do not claim that the AI is now genuinely expert**.
