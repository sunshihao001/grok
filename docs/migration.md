# Hermes → Grok Bot: explicit migration choices

| Existing artifact | New role | Current decision |
|---|---|---|
| Seven business Skills: candidate-entry, token-panel, wallet-roles, wallet-structure, evidence-chain, trade-gate, controller | Research and evidence contract | Reference and gradually port; **not deployed** |
| Hermes /HER_START, runtime hooks, patched upstream CLI | Grok message, private Skill, Routine, GitHub handoffs | **Not binary/API compatible** |
| Hermes gmgn_client.py and qb GMGN reporting script | Subprocess read-only raw GMGN adapter | Partial; mapping needs verified raw samples |
| meme- first-control-zone reclaim theory | Candidate observable hypotheses | Never automatically convert into watch/trade rules |
| Hermes fixture acceptance | Deterministic offline regressions | Tests do not establish live accuracy |
| Hermes phase state | Snapshot, event de-dup and run history | Only minimal single-writer baseline implemented |

## Iteration order

1. Recover real GMGN fields, units, event IDs and source timestamps; preserve raw samples privately.
2. Select **one measurable problem** (wallet funding pattern, deployer history, or structure change), not a broad catalogue of bot functions.
3. Map source data into verified normalized observations; compare replay against old contracts and direct on-chain evidence where feasible.
4. Draft rules with failure cases, independent verifier, baseline comparisons and coverage/false-alert reporting.
5. After human acceptance, supply a versioned observation Skill to a single Monitor Bot. Test a one-time real run, then create and test its Routine.
6. End development sessions/Routines when the monitor is stable. Keep source references and rule change process available for later maintenance.

**Not done now:** provisioning cloud Bots; live GMGN authentication; live monitoring, automatic order placement, trading/returns claims.
