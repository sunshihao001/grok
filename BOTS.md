# Bot architecture V1.1 — 7 roles, 1 final monitor

**Recommendation: 6 on-demand specialist development Bots + 1 production read-only Monitoring Bot.** They are proposed roles, not already-created Grok app instances. See [machine-readable roster](design/bot-roster.v1.json), [12-domain ontology](knowledge/system/ontology.v1.json) and [F0–F6 gate policy](knowledge/system/filter-policy.v1.json).

## Role allocation

| Bot | Specialism | Domains | Gate ownership |
|---|---|---|---|
| B01 主控/知识架构 | Define objective, as-of time, knowledge routing, hypothesis and task handoffs | D08,D12 | F0–F1 |
| B02 链上数据 | GMGN, RPC, raw transaction, units and data availability | D01,D02,D03,D10 | F2 data producer |
| B03 钱包与资金结构 | Wallet behavior, funding groups, chip control candidates and market sequences | D04–D07 | F3 mechanism proposer |
| B04 Alpha与交易经济学 | Prediction, preregistration, entry/exit, cost and net executability | D03,D07,D08,D09 | F3–F5 hypothesis owner |
| B05 证据反证审查 | Challenge original facts, confounders, bias, models and claims | D10,D11 | F2–F5 independent gate |
| B06 独立QA与回测 | Blind replay, OOS, negative controls, tests and rollback | D09,D10,D11 | F4–F6 independent QA |
| B07 最终监控 | Only consumes approved frozen rules; produces read-only alerts | Just-in-time relevant topics | F6 frozen release only |

**D01–D12 are knowledge subjects; F0–F6 are research/evidence checks. Neither dimension should become a separate Bot for every category.**

## Decision flow, not seven permanently running processes

- **Explain funding links**: B01 → B02/B03 → B05, stop at F3. Do not run an expensive trade simulation for a purely structural question.
- **Find a profitable copy-trade**: B01 → B02/B03 where relevant → B04 (prediction and net execution) → B05 challenge → B06 independent OOS/real-case replay. F5 must be evidenced; a 2x hit rate or wallet cluster is not enough.
- **Observe approved tokens**: B07 runs alone, consulting the frozen rule version and matching source evidence; ambiguous cases are recorded as research gaps instead of being converted into trades or auto-approved rule changes.
- **Release rule**: B06 prepares audit; B05 independently challenges it; a **human** approves frozen version and rollback; only then may B07 load it.

## Cloud-computer deployment constraints

Official Grok Bot documentation: https://docs.x.ai/grok-bot/computer-and-apps and https://docs.x.ai/grok-bot/approvals-security-and-privacy.

All Bots for one user share a persistent cloud computer, browser logins, filesystem and credentials. **Separate Bot identities are not a permissions/security boundary.** Coordinate tasks via versioned Git branches and isolated working dirs; use single-writer state/locking; never put private keys or trading secrets into the shared computer. Distinct Bot memories are not a source of verified market facts.

## Practical staged creation

1. Configure **B01, B02, B05** first and test one source-backed real-data research handoff.
2. Add **B03, B04, B06** to test specialized market mechanisms, losses and positive/negative OOS controls.
3. Create **B07** after a human-approved frozen paper-only ruleset, state concurrency work and an end-to-end Routine test.

No source repository or knowledge migration is allowed to bypass primary data, timestamps, independent falsification or manual release. Phase 1 prohibits live orders, signing, swap or broadcast.

## Deep knowledge initialization and handoff (initial research)

Each role has a detailed [startup instruction and syllabus](bots/profiles/) and a machine-readable [K0/K1/K2 knowledge reserve](knowledge/bot-knowledge-profiles.v1.json). Use the [single source-aware handoff contract](docs/bot-knowledge-integration.md) and [offline validator](src/solana_meme_os/bot_knowledge.py). B02's data-contract proposal is **not a direct production message**: only a human-approved frozen collector/rule release may be consumed by B07. Grok Bot objects and private skills still require manual configuration in the Grok application; repository CI does not provision the computer.

## Executable local handoff prototype

Research Bot task delivery is now modeled by the SQLite queue in src/solana_meme_os/runtime_store.py. The runtime performs atomic per-recipient claims and explicit complete/block/requeue but **never runs Grok models or third-party commands**. All Bots on one cloud computer can access the filesystem; role IDs are declarations, not OS permissions. B07's monitor state/rule loader remain separate and unimplemented for production. See docs/local-runtime-framework.md.
