# Bot-to-Bot integration, shared knowledge, context and evidence — V0.1 Research

## 1. System of record, not Bot memory

```text
                 User research objective
                           │
                  B01 task and as-of
                           │
                  Ontology D01–D12
                           │
              K0 resident role curriculum
              K1 selective pinned retrieval
              K2 per-case live original evidence
                           │
           ┌───────────────┼────────────────┐
           B02             B03              B04
      original data   actor/capital graph  predictive/economic model
           └───────────────┼────────────────┘
                          B05
                  independent evidence challenge
                           │
                          B06
                    independent OOS/replay
                           │
                  human F6 approval
                           │
                B07 single frozen Monitor
                           │
            alerts + unknowns → B01 research queue
```

B03 only starts when actor/structure questions are relevant; B04 is needed only when a predictive/economic question is in scope. B05 operates throughout empirical investigation. B07 **does not call all six development Bots on every ticker**. The graph describes knowledge flow, not a permission boundary.

## 2. Files, skills and sources on Grok's cloud computer

Official documentation: https://docs.x.ai/grok-bot/computer-and-apps , https://docs.x.ai/grok-bot/bots and https://docs.x.ai/grok-bot/skills-routines-and-automations .

The seven Bots share a **single persistent cloud computer**; separate screens do not imply separate files or credentials. Bot memories/conversations can be distinct. All reproducible research truth stays in signed/versioned repo files and immutable task-specific evidence references. Do not rely on an Agent's saved memory for changing market facts.

Suggested project working layout on the shared cloud computer (not presumed installed):

```text
/workspace/grok/                 # one pinned repo checkout per reviewed branch
/workspace/research/B01/...      # task-scoped scratch, not shared mutable truth
/workspace/research/B02/...
/workspace/research/B03/...
/workspace/research/B04/...
/workspace/research/B05/...
/workspace/research/B06/...
/workspace/monitor-state/        # only B07 is permitted writer by workflow
```

Isolation by directory/branch prevents routine file conflict but **not unauthorized access**. Secrets and production signing keys do not belong in this environment. Share common skills through Grok's private Skill library as available, then explicitly enable for each Bot; GitHub markdown files do not automatically register the skill. Prove a one-off run before creating a Routine.

## 3. Inter-Bot data contract

Use `knowledge/bot-handoff.schema.json` and `python -m solana_meme_os.bot_knowledge --validate-handoff <file>`. Every packet binds `task_id`, `producer`, `recipients`, `objective`, `population`, `decision_cutoff_utc`, `domain_ids`, `knowledge_ids`, `source_refs`, `observations`, `alternatives`, `counterevidence`, `missing`, `gate_results` and `next_action`.

- **Source reference** must resolve to an approved K1 source ID or a task-specific immutable primary-source artifact, with commit/version or transaction signature.
- **Observed fact** needs `event_at` and `available_at` no later than the decision cutoff; otherwise it is an outcome-only fact or must be labelled post-decision and kept out of entry features.
- **Independent gate**: a PASS requires real evidence references, independent reviewer and a corresponding separate review packet; a Bot cannot pass its own F4/F5/F6.
- **Unknown is first class**: empty evidence arrays without an explicit `missing` reason cannot be read as a negative observation.
- **No confidence fabrication**: no arbitrary self-scored percentages. Frequency/statistical probabilities require measured outcomes and calibration evidence.
- **K2 data classification**: fixture, real_observation, externally_reported or synthetic_illustration. They never silently convert into one another.
- **Rule changes**: a B06-reviewed research packet is still only a proposal. Human F6 approval is required, after which B07 reads a frozen immutable rule hash.

## 4. Communication route and what is not automatic

Groks can message one another or work in groups; cloud filesystem and direct Bot handoff can carry a manifest. No API-level bot orchestration is implemented in this repo. B01 owns task IDs and asks specialized Bots for only their specific evidence objects. A task manifest records parents, responsible Bot, input checksums, outputs, review state and next task. Sending a packet does not mean downstream Bot accepted the claim.

### Research-driven discovery loop

`RESEARCH_GAP → B01 assigns source discovery → B02/B03 evidence → B04 candidate research → B05 falsification → B06 OOS → human update`.

When data or authorization is missing, the path stops at `INSUFFICIENT`, with a concrete next source query. Research candidates do not enter B07 automatically.

### Operating capacity and priorities

Keep K0 short (~one shared policy plus role curriculum); initial K1 selection is top 2–5 relevant pinned sources, then expand only for conflicting evidence. Don't summon every Bot; an evidence F3 wallet question can finish with B01/B02/B03/B05. Preserve a finite budget for RPC costs, rate limits, cloud-computer parallelism and human review, but do not invent specific throughput ceilings.

## 5. Initial acceptance criteria — not claims of achieved deployment

A. B01 must route 6 different ordinary questions to minimal required roles including one outside 15 cards, and explicitly record unknowns.

B. B02 must inspect true read-only RPC/GMGN response and reject wrong decimals/timezone, no slot/source, 429/403 mapped to empty and stale records. Ensure positive and negative cases.

C. B03 must distinguish direct funding vs public CEX hubs vs indeterminate service patterns, with matching negative control; no real identity assertion.

D. B04 must preregister a candidate with entry cutoff, baseline, costs, latency, market regimes, exit tail and untouched period; not claim net profitability from peak returns.

E. B05 must detect planted lookahead, selected denominator, imagined confidence, and invalid market evidence, with reasons.

F. B06 must reproduce failures and performance on independently selected on-chain cases, test cost sensitivity and unknown coverage; a passing CI is necessary but not sufficient.

G. B07 must run a **paused and tested** read-only Routine with single-writer state, source links, correct UTC conversion and a human-approved pinned ruleset; currently not achieved.

One real case including at least one matched negative and one untradeable case should produce traceable evidence chain from B01→B06 before investing in broad repetitive migration.

## 6. Immediate next research experiment

**Theme:** Wallet cohort recurrence, relay/funder edge and *net executable* copy trading. Source documentation includes `external-reentry-negative` and `external-post-detection-results`. Define two cohorts (detector alerted vs non-alerted). Match by time, launch platform, market cap and liquidity where observable. Track raw signatures, snapshot coverage, decision cutoff, queue delay and sell-side exit depth. Let B03 establish structural role; B04 compute increment over baseline and economic distributions; B05 attack selection bias; B06 run untouched OOS and record negative cases. Do not claim the outcome in advance.
