# Meme Autonomous Trading Intelligence — Agent Runtime Architecture v0.1

> 2026-11-16 · Current architecture baseline for the `blix` branch.
>
> This document supersedes the earlier assumption that NousResearch Hermes should automatically become the primary runtime. The architecture is now driven by the actual product objective: **move from Meme research toward evidence-based, execution-aware trading opportunities, with automation increasing gradually and safely.**

## 1. Final product objective

The project is not primarily a knowledge base, chatbot, wallet tracker, copy-trading bot, or generic research assistant.

The target is:

**An autonomous Solana Meme trading-intelligence system that continuously discovers market events, filters candidates, reconstructs evidence, evaluates actual tradeability, monitors changing conditions, learns from outcomes, and eventually can feed a controlled execution layer.**

The central business object is therefore an **Opportunity / Trade Candidate**, not merely a Token or Mint.

A token can be interesting without being tradable. A signal can be predictive without being executable. The system must keep these distinctions explicit.

## 2. Four-layer AI/runtime split

### GPT — high-intelligence coordination and judgement layer

GPT is the human-facing strategic reasoning layer.

Use it for:
- understanding ambiguous goals;
- coordinating Muse and Hermes;
- difficult multi-hypothesis reasoning;
- reviewing system-wide failures;
- deciding what research is worth doing next;
- evaluating major changes to trading logic;
- comparing architecture/options;
- resolving high-value UNKNOWNs.

GPT should **not** be called for every market event. It is a high-value escalation layer.

### Muse — primary operational runtime

Muse is the preferred high-frequency operating surface/runtime for the Meme system, subject to real-world validation.

Use it for:
- continuous operation;
- routine market monitoring;
- high-frequency candidate filtering;
- calling tools/MCP;
- executing already-validated workflows;
- maintaining current operational context;
- surfacing UNKNOWNs and escalation requests;
- presenting results to the user.

Muse does not need to become as intelligent as GPT. Its job is to run the current validated system cheaply and continuously.

### Hermes — research, correction and evolution layer

NousResearch Hermes Agent is not treated as the sole production brain. It is the backend research/evolution agent.

Use it for:
- deep investigations;
- falsifying current assumptions;
- finding repeated failure modes;
- researching new market mechanisms;
- testing whether existing signals still work;
- proposing knowledge/rule/workflow updates;
- producing evidence-backed change proposals;
- investigating UNKNOWNs escalated by Muse.

Hermes must not be reduced to a static knowledge repository. Its important role is **research → falsification → correction → proposed next version**.

### Blix — Meme business/data foundation

Blix remains the mature product foundation and should not be replaced by the AI layer.

It provides:
- market discovery;
- token/Mint state;
- market data;
- holders/wallet data;
- transaction/event evidence;
- safety checks;
- paper trading;
- quotes/execution-related information;
- UI/API/MCP;
- alerts;
- track record;
- operational health.

AI should use and extend these capabilities rather than rebuild them without a concrete reason.

## 3. Runtime flow

The intended flow is:

```
Market events
   ↓
Blix / raw chain / market sources
   ↓
Muse: cheap, high-frequency filtering
   ↓
Candidate / UNKNOWN
   ↓
Evidence reconstruction
   ↓
Opportunity evaluation
   ↓
Execution feasibility check
   ↓
Trade Candidate
   ↓
Monitor continuously
   ↓
Outcome / failure data
   ↓
Hermes research + falsification
   ↓
Change proposal
   ↓
GPT review for high-impact changes
   ↓
Validation
   ↓
New operational knowledge/workflow
   ↓
Muse uses the validated version
```

GPT can intervene at any point when the task exceeds routine runtime capability.

## 4. Trading funnel

The core pipeline is:

1. **Discovery** — detect new Mints, funding/buy events, unusual flows, wallet activity and market changes.
2. **Filter** — cheaply remove obvious low-quality, unsafe, illiquid or stale candidates.
3. **Investigation** — reconstruct wallet, transfer, funding, timing and cross-Mint relationships.
4. **Verification** — separate FACT, PLATFORM TAG, AI INFERENCE and UNKNOWN. Do not promote inference to fact.
5. **Opportunity** — determine whether current conditions create a meaningful market opportunity.
6. **Tradeability** — determine whether the opportunity can actually be entered/exited with acceptable liquidity, slippage, competition and timing constraints.
7. **Trade Candidate** — only after opportunity and execution checks pass.
8. **Monitoring** — continuously test whether the original thesis remains valid.
9. **Outcome** — record what actually happened.
10. **Learning** — use outcomes to falsify or improve the current logic.

The distinction between **Opportunity Score** and **Trade/Execution Score** is mandatory. A high opportunity score does not automatically mean a trade should be taken.

## 5. Evidence discipline

For every important candidate, preserve:

- Mint/address;
- event timestamp;
- raw source evidence;
- wallet addresses and roles;
- funding source and destination where reconstructable;
- buy/sell/transfer sequence;
- token-account/owner distinctions where relevant;
- SOL/WSOL distinctions where relevant;
- cross-Mint relationships;
- liquidity and execution constraints;
- competing explanations;
- failure risks;
- UNKNOWN fields;
- confidence;
- model/agent that produced the inference;
- later outcome.

Never treat a platform label or model inference as raw fact.

## 6. Autonomous escalation

Routine work should remain cheap.

A preferred escalation pattern is:

```
Muse
 ↓
Can routine rules/current knowledge answer?
 ├─ yes → continue
 └─ no → UNKNOWN / escalation
              ↓
           Hermes
              ↓
     Can evidence resolve it?
       ├─ yes → proposal/result
       └─ no → high-value ambiguity
                    ↓
                   GPT
                    ↓
              strategic judgement
```

This prevents expensive models from being used on every token.

## 7. Model-cost strategy

The system should eventually use model routing:

- deterministic code/rules for mechanical filtering;
- local/free/cheap models for extraction, classification and first-pass analysis;
- Hermes for deeper research and correction;
- GPT or another premium model only for high-value reasoning and system-level judgement.

The objective is not "use the strongest model everywhere". The objective is **use the cheapest reliable capability for each task and escalate only when evidence/value justifies it**.

## 8. Knowledge/version model

Knowledge is not a permanent instruction dump.

Use versioned proposals:

```
Current knowledge
   ↓
Observed failure / new evidence
   ↓
Hermes investigation
   ↓
Falsification
   ↓
Change proposal
   ↓
Validation/backtest/replay/sample test
   ↓
Knowledge/Workflow vNext
   ↓
Muse runtime
```

A proposal is not production truth until validated.

Avoid blindly adding new rules. Old knowledge can be rejected, downgraded, superseded or left UNKNOWN.

## 9. Autonomous trading progression

Do not jump directly to unrestricted live trading.

Recommended progression:

### Stage A — automated discovery
System finds and ranks candidates.

### Stage B — automated investigation
System reconstructs evidence and evaluates opportunities.

### Stage C — automated monitoring
System continuously checks thesis validity and execution conditions.

### Stage D — trade-candidate generation
System produces an explicit trade candidate with evidence, risks, invalidation conditions and execution constraints.

### Stage E — controlled human-approved execution
A user confirms the trade.

### Stage F — isolated automated execution
Only after sufficient empirical validation, introduce a separate execution engine with strict limits, kill switches, position sizing, slippage/liquidity checks and key/signing isolation.

AI reasoning should never have unrestricted access to funds or private keys.

## 10. What success means

The system is not successful because:
- it produces many AI summaries;
- it knows many Meme concepts;
- it finds many tokens;
- it has many agents;
- it has a large knowledge folder.

It is successful when it can demonstrate, with recorded evidence:

**discover → investigate → verify → decide → execute-feasibility → monitor → outcome → falsify/improve**

and progressively reduce false positives, missed opportunities and execution failures without hiding losses or uncertainty.

## 11. Current implementation priority

1. Preserve the existing Blix business/data capabilities.
2. Establish Muse as the operational runtime experimentally.
3. Connect Muse to Blix through stable API/MCP boundaries.
4. Keep Hermes on the VPS as the research/correction runtime.
5. Establish a controlled GPT gateway for high-value coordination.
6. Implement Opportunity and Trade Candidate records.
7. Implement evidence/UNKNOWN discipline.
8. Implement model routing and cost controls.
9. Build replay/track-record validation before changing trading logic.
10. Only then consider controlled execution automation.

This is an architecture baseline, not a claim that every integration above is already implemented. Each integration must be tested in the real environment before being treated as operational.
