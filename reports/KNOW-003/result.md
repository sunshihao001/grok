# KNOW-003｜参考仓库深挖与科学研究准入层

2026-10-29 · draft feature branch · reference_only / synthetic_fixture · HUMAN_ACCEPTANCE_PENDING

## 复核过的证据与边界

- [Reference upstream](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) pinned to commit 9a7ad51d56328e91e67e3f531d6744307d0ee68b; document/file SHA pins in knowledge/registry.v0.json.
- Surveyed research: coordination_detection, funder_network, post_detection_edge, post_detection_forensics, entry_zone, sniper_capital, known_group_reentry, alpha_patterns, ACT_IV, methodology, pitfalls and temporal leakage audit.
- Main transferable finding: real coordinated wallets and a statistically better success-rate classifier **do not imply** a follower can capture positive net returns. Detection may be later than the economic opportunity, while the operator controls the pre-alert inventory.
- Nulls have to fit the actual unit and sampling frame. For one shared-funder criterion the source found it fired on 88.9% of random groups of 40. The original finding is specific to that test, not a universal false-positive estimate.
- Do not overstate: original alpha_patterns is exploratory/not fully independent OOS, some data are unpublished; this PR has not independently rerun original chain studies or demonstrated any trading alpha.

## Additive implementation

1. KB-003 and deep architecture in docs/research-evolution-os.md.
2. A fail-closed synthetic-only audit with pre-registration, feature/availability ordering, missingness and realized cashflow by TEST cohort.
3. Negative and adversarial fixture tests, including synthetic high win-rate/negative realized net.
4. Add one explicit RESEARCH_PROPOSAL trigger in knowledge registry. Keep existing runtime monitor, source cards and KB-001/002 unchanged.
5. Cite source revision/sha and original authored analysis; reference materials are not copied.

## What remains deliberately undone

True matched controls, degree/time-preserving null implementations, feature selection lock/independent forward test, raw RPC+GMGN verified collection, quote-level execution simulation, outcome-independent sampling and Grok cloud bot deployment. Source repository results are not republished. Review order: PR #3 -> PR #7 -> this stacked PR.

## Acceptance evidence

CI: PYTHONPATH=src python -m unittest discover -s tests -v — GitHub Actions 40847971329 passed (44 tests, OK) on commit 4225ec1a14945edea04207124c8b6ce1c93f465d. This is offline-contract validation ONLY; no live-trading validation.

First CI on 61bea482 failed due to an incorrectly truncated source blob SHA; corrected via 4225ec1a, then 44 tests passed. This fail-closed behavior is retained as provenance safety.

CI URL: https://github.com/sunshihao001/grok/actions/runs/40847971329
