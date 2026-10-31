# Project Agent / Bot Rules — Solana Meme Market Intelligence OS

**Canonical architecture:** [Knowledge Architecture V2.0](docs/knowledge-architecture-v2.0.md), with machine-readable registry at knowledge/architecture.v2.json. V5 is the research method; V4 is the runtime organization. Do not use the historical V1 integration document as the current master.

## Scope and epistemic rules

- Primary scope: market-wide Solana Meme event, wallet-cluster, asset/capital flow, developer, market-structure, conditional-baseline and risk research. Copy trading is a subordinate use case.
- Distinguish source assertion, source-derived table, raw RPC observation, normalized event, derived metric, behavior candidate, statistical deviation, mechanism hypothesis, risk, prediction and paper result.
- UNKNOWN is a first-class state. Never turn missing history, RPC failure, incomplete paging or unresolved owner into zero, normal, independent or same-owner.
- Preserve exact signatures, instruction paths, Slot, transaction index when known, units, window boundaries, source versions, observed/available/received/decision times.
- Token transfer is not necessarily a swap; balance delta is not a unique sender; common funder is not a beneficial owner; same Slot is not a confirmed Jito Bundle.
- Do not claim statistical abnormality without an appropriate unselected population, denominator, matched baseline and public-infrastructure controls.
- The five graph models remain separate: market facts, economic assets/entity hypotheses, mechanism knowledge, expert/source provenance and purpose-specific decision utility.

## Safety boundary (hard)

Phase 1 is read-only research / paper-only.

Forbidden for all Bots:
- real orders, wallet signing, transaction broadcast or private-key access;
- GMGN swap/multi-swap/cooking create;
- auto deployment, auto Routine activation or unapproved external notifications;
- claims such as “confirmed operator”, “confirmed insider”, “guaranteed pump” without the exact supporting evidence.

## Required reading

1. docs/knowledge-architecture-v2.0.md
2. CONTEXT.md and BOTS.md
3. For research design: docs/economic-mechanism-discovery-charter-v5.md
4. For runtime boundaries: docs/dual-loop-research-runtime-architecture-v4.md
5. For domain/source details: knowledge/README.md, knowledge/catalog.v1.json, knowledge/source_index.v1.json, docs/sources.md
6. For task-specific source documents and code; never bulk-load the whole corpus as a substitute for understanding.

## Knowledge use and release

- Knowledge cards are retrieval aids, not authoritative truths. Read their exact source file/commit and check assumptions against the current event.
- Experts are research disciplines, not independent votes or necessarily separate Agents. Multiple experts citing one source do not create independent evidence.
- Research stages S0–S7 are not software modules M0–M7. Runtime V4 loops are a separate design.
- Any material claim must retain evidence refs, source/version, times, counter-explanations and dependencies.
- A source correction triggers claim impact review; never silently overwrite prior claims.
- Significant rule/skill/knowledge changes require a concise report under reports/ and a regression check.
- Do not claim tests passed unless GitHub Actions or a local environment actually ran the exact commit.
- A release requires representative real data, counterexamples, error attribution, independent review and rollback notes.

## Demand-driven source reasoning

Use research.py for source discovery and expert_router.py for deterministic capability suggestions only. These tools do not perform semantic analysis, fetch RPC, run expert Agents or authorize trading. If the current index does not cover a mechanism, expand research rather than force-fit it into an existing card or expert.
