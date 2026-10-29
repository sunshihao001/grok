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
