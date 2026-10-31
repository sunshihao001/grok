# Source audit — 2026-10-29

These observed main-branch commits pin the source inventory at initialization. Re-check history before any later import.

| Role | Repo | Observed main commit |
|---|---|---|
| Hermes business workflow | [sunshihao001/-](https://github.com/sunshihao001/-) | 2bf694b37cce25b4a3c9364298b784039f3ecc84 |
| Strategy theory | [sunshihao001/meme-](https://github.com/sunshihao001/meme-) | 5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a |
| GMGN & Hermes prototype | [sunshihao001/qb-](https://github.com/sunshihao001/qb-) | 8377ad5611255df5cd4562666a826708575334f0 |

## Verified starting points

- Original Hermes source: CONTEXT.md, design/phase0-workflow-contract.md, docs/cross_skill_handoff_contract.md, skills/common/gmgn_client.py, skills/meme-workflow-controller/scripts/run.py and associated rules/tests. The actual controller uses /root/sikk-gmgn paths: it is **not portable as-is**.
- Meme source: SOURCE_OF_TRUTH.md, AGENTS.md, numbered knowledge subdirectories. Its MQL5 first-control-zone/POC/AVWAP model is a **research hypothesis**, not proven Solana on-chain strategy.
- qb source: sikk_gmgn_token_report.py, hermes_harness/README.md and hermes_harness/HERMES_RUNTIME_SYSTEM_INDEX.md. The reporting script uses GMGN CLI and heuristic wallet labels. The Hermes Harness is a different general-purpose runtime, not the Solana business pipeline.

**Unverified:** live authenticated GMGN response shape, field units, rate limits, Bot cloud CLI setup, performance, and runtime scheduling.

Official Grok Bot docs checked at initialization:
- https://docs.x.ai/grok-bot/overview
- https://docs.x.ai/grok-bot/bots
- https://docs.x.ai/grok-bot/chat-and-collaboration
- https://docs.x.ai/grok-bot/skills-routines-and-automations

Official docs support specialized Bots, cross-Bot messaging, shared cloud filesystem, reusable Skills, and scheduled/event-triggered Routines. GitHub content alone does not create those Bot objects.

## Expanded provenance for market-wide integration (checked 2026-10-31)

Legacy source pins below remain valid **as previously observed versions**, not necessarily the latest main commits. This branch's integration also reads:

| Role | Repo | Pinned commit (source reading) |
| --- | --- | --- |
| Coordination, funding graph, downstream inventory and negative-results methods | [Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | `9a7ad51d56328e91e67e3f531d6744307d0ee68b` |
| Candidate read-only token/wallet/market tools | [okx/onchainos-skills](https://github.com/okx/onchainos-skills) | `73904b636a0f022dcc13b6d7a0dd2ed3b3195f25` |
| Grok integration branch | [sunshihao001/grok](https://github.com/sunshihao001/grok) | `docs/cognition-knowledge-conversion-v1` (moving draft; never cite a branch name as frozen source revision) |

Pin an exact source file and commit for each imported claim. Technical tool descriptions are *candidate adapters*, not evidence of live data coverage. Original Hermes, meme- and qb- domain knowledge remains in source, and 21 bounded historical snapshots are preserved in Grok without importing Hermes runtime.

Current full source selection list: `knowledge/source_index.v1.json` (**30 pinned pointers**); program policy: `src/solana_meme_os/research.py`. See [knowledge architecture V2.0](knowledge-architecture-v2.0.md) for the distinction between source discovery, reviewed sources and live data connectors. For market-wide roles and per-source limitations see [integration](knowledge-system-integration-v1.md).
