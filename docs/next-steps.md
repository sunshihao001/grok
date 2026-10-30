# Release backlog

## Initialization (completed locally)
- [x] Source pins, agent roles, migration map and Grok Bot setup instructions.
- [x] Read-only source validation, per-mint state, observed deltas, event de-dup and JSONL log.
- [x] Explicit fixture/live separation and rejection of stale live input.
- [x] GMGN CLI raw-only read collector with no guessing of metric values.
- [x] Six offline tests; CI workflow authored.
- [ ] GitHub-hosted CI job result observed after push.

## Real monitoring prerequisites
- [ ] Capture real GMGN CLI JSON, field descriptions, timestamp semantics and units without committing secrets.
- [ ] Test mappings for liquidity and holder share, add authoritative chain references for events, measure drift and missingness.
- [ ] Add single-writer locking/recovery or SQLite before Grok scheduling/multiwriter workflows.
- [ ] Port wallet and deployer intelligence one tested observation at a time.
- [ ] Reproduce actual historical cases; measure false alerts, coverage, abstentions, and detect data leakage.
- [ ] Human-review rule thresholds and release notes; current numbers are **unvalidated examples**.
- [ ] Actually create Grok Bots, the shared Skill and a tested Routine within Grok app.

## Rule promotion packet
Problem, version, owner, raw sources/commits/times, units, proposed mechanism, competitive explanation, tested baseline, counterexamples, false alerts, regression commands/results, rollback and explicit human approval.

Rule Engineer passing local tests **does not** imply an economically valid or production-ready monitoring rule.

## Knowledge migration (preserved, with explicit uncertainty)
- [x] Import 15 source-pinned knowledge units covering Solana lifecycle, GMGN fields, wallet roles/funding, structure, risk, evidence and tool failure modes.
- [x] Connect a deterministic knowledge selection function to monitor observations and plain-language research question routing.
- [x] Add regression tests for relevant concept retrieval, source integrity, negative cases and missing-data behavior.
- [ ] Verify original external theoretical references, look for corrected recent primary sources, and distinguish stale assumptions from currently valid mechanisms.
- [ ] Import concrete real on-chain cases and source-linked failures, not only conceptual documents.
- [ ] Test whether Grok Bot with knowledge improves judgment vs a no-knowledge baseline using blinded examples; measure false alerts and missed events.
- [ ] Improve semantic applicability and source reading in an actual Grok Bot instead of claiming literal keyword routing is full expert reasoning.

## On-demand research architecture
- [x] Read the pinned Why-Solana-Memecoins-Are-Over research methods, error audits, structural-mechanism tests, economic edge failures and source licenses.
- [x] Add a small source index of 17 pinned documents instead of copying another entire research repository.
- [x] Implement bounded optional source preview and structured research intake with a decision-time availability check.
- [x] Add offline tests for source selection, authenticity/allowlist, time-of-knowledge rejection and no-edge claims.
- [ ] Run genuine source retrieval in a configured Grok Bot and inspect live handoffs; not the same as unit tests.
- [ ] Add real transaction datasets and delayed-outcome evaluation, including null baselines, execution costs and alerts not selected on winners.
- [ ] Compare Grok with/without the on-demand source workflow under blinded case review to test reduction in unsupported assertions.

## Knowledge structure V1 (branch proposal)

- [x] Eight layers, twelve professional domains, dependencies and typed links.
- [x] Existing 15 source-pinned knowledge cards mapped to primary domains; no legacy source code/runtime copied.
- [x] Four source pins including an independent adversarial research repository; three reported-only research units.
- [x] Offline structural validation and tests authored; CI execution still to be verified.
- [ ] Real GMGN/on-chain evidence and unsuccessful/untradeable cases, independent reproductions.
- [ ] Blind knowledge vs no-knowledge decision test, economic evaluation and human-frozen rules.

Start with `knowledge/system/README.md`. **Structure complete does not imply that content or market Alpha is verified.**

## Bot allocation and release

- [x] Specify 7 roles (6 on-demand development / 1 read-only monitor), mapped to knowledge domains and gates.
- [x] Add machine-readable roster + offline structural tests; note shared-computer limitations.
- [ ] Create B01/B02/B05 in the Grok app and test source-to-review handoff.
- [ ] Add B03/B04/B06 for wallet/Alpha/OOS cases with original evidence, then B07 after human-approved frozen rule and tested single-writer Routine.

## Role-specific deep knowledge and handoff preparation (initial research)

- [x] Seven Bot expertise curricula with epistemic boundaries, K0 cards, K1 pinned source pointers and minimum K2 evidence requirements.
- [x] Four selectively verified new K1 references, total 21 (no bulk source copying).
- [x] Seven detailed startup instructions, shared-cloud-computer manual activation guide and cross-Bot handoff map.
- [x] Offline handoff structure validator and negative-case tests (CI pass must be observed after the PR commits).
- [ ] Manually install/enroll private skills in Grok UI and test actual real Bot-to-Bot handoff.
- [ ] Collect real live read-only K2 observations and evaluate independent source/market accuracy in real Grok cloud tasks.
- [ ] Test B04/B05/B06 on blinded strategies/net economics; only a human may release frozen B07 rules.

## GPT/GitHub/Grok incremental knowledge loop (new, staged)

- [x] Draft-only C1-001 example tied to existing F0–F6 source policy, not duplicated evidence.
- [x] Minimal curriculum manifest, role/level filtering, static validation and regression tests.
- [x] Draft Grok read-and-feedback Skill template with explicit repository SHA and no rule release.
- [ ] Human-review and approve a lesson for study before normal `--bot` loads it.
- [ ] Actually connect Grok GitHub access; run one read-only preview and verify cited SHA/read paths.
- [ ] Collect Grok feedback and independently review its reasoning; only then write the next C1/C2 lesson.
- [ ] Only after repeated safe real tasks, save a verified private Skill and optionally add a scoped GitHub event Routine.

## Expert research R-2026-10-30-01 (stage 0, no market replication)

- [x] Primary source review: Solana RPC observability, external repeat-group negative experiment, Jupiter V2 quote-versus-fill path and legacy multi-strategy/falsification approach.
- [x] Proposed H-A time absorption, H-B independent secondary absorption, H-C future-mint identifiability, H-D controlled risk filter.
- [x] Static time eligibility validator with synthetic positive/negative cases, not authenticity proof.
- [x] Draft-only C2/C3 lessons linking to pinned external source pointers and current expert research.
- [ ] Human review of novel hypotheses, sampling universe and paper quote sources.
- [ ] B02 live read-only coverage/time-trace acquisition and units/decimals tests (K2 not present).
- [ ] B05 matched negative controls, operator time/group split and selection-bias check.
- [ ] B04/B06 independently evaluated preregistered F4 and F5; no positive net edge claimed.

## Local execution engineering P0, not market fundamentals

- [x] scripts/grok_cloud_doctor.py source and binary preflight, optional audit/test.
- [x] src/solana_meme_os/runtime_store.py SQLite WAL per-recipient task queue with digest idempotency and blocking/recovery.
- [x] Local handoff private Skill template (uninstalled) and disabled external provider capability declaration.
- [ ] Run P0 on real Grok cloud terminal and record exact SHA, permissions and command outputs.
- [ ] Perform B01/B02/B05 end-to-end synthetic packet with independent B05 challenge.
- [ ] Implement exactly one read-only source adapter, verify raw schema, units, errors, availability/receipt timing.
- [ ] Implement B07 single-writer monitor runtime and approved frozen rule loader (research SQLite queue is insufficient).
