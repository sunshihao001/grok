# How a specialized Bot turns a knowledge card into a useful judgment

**Example user message:** "这币前十突然多了十几%，是不是庄在吸筹？"

1. **Represent the question:** 'top10_holder_pct increased' is an address-level share observation; 'the dealer is accumulating' is an unverified causal inference. The user wants to understand the actor configuration and whether an event changes monitoring priorities.
2. **Knowledge selection:** `concentration`, `funding-graph`, `wallet-roles`, `sybil-wash`, plus `evidence-synthesis`. Prioritize where card mechanisms differ, not just text keyword overlap.
3. **Get evidence:** compare fixed-definition holder snapshots, token supply, pool/CEX exclusion, transfer edges and timing, deployer history, market events. If inaccessible, record UNKNOWN.
4. **Competing explanations:** genuine concentration by independent investors, migration/LP address effects, CEX custody, denominator changes, controlled group and sample/indexer errors.
5. **Contradictions and discriminating information:** Which source would separate the cases? The transfer/holder graph, rather than a repeated vendor tag, usually has more diagnostic value.
6. **Decision:** report observation and 1–3 hypotheses, strongest disconfirming fact, limits and next *read-only* verification step. Avoid saying 'insider' or 'confirmed dealer'. A trade gate is not a trading command.
7. **Feedback:** after new evidence, append a source-linked case with time, hypothesis and observed result; independent reviewer decides whether a new catalog card/rule revision is justified.

**Do not let a matching knowledge entry limit exploration.** If a user asks a novel question, look for unrepresented market mechanisms and source evidence, with the developer Bots, rather than fitting it into one of 15 cards. Confidence scores require calibration, not LLM self-rating.
