# Local Runtime Framework V1 — Grok Bot + Python + SQLite + GitHub

**Status**: runnable offline research substrate; real Grok cloud execution, third-party provider access, monitoring state locking, approved rules and Routines are not deployed or verified.

## What this deepening covers

The project already defines Bot roles, 12 knowledge domains, 8 knowledge layers, K0/K1/K2, F0-F6 gates and C0-C4 learning levels. The engineering task is to make these designs callable by stable local programs, rather than continuing to expand basic market definitions.

Runtime divides into four planes:

1. **Control**: Grok Bot instructions and Skills decide which research task and reviewed CLI to call. They do not authenticate identities or provide OS-level isolation.
2. **Knowledge and build**: GitHub fixed SHA, role curricula, source index, specialist references, versioned Python scripts and regression tests.
3. **Data**: deterministic local Python entry points, provider capture logs, normalized observations, source hashes, as-of timestamps and failures.
4. **State**: durable SQLite B01-B06 handoff queue; a separate, future single-writer B07 monitor store; PR/human release audit.

Do not introduce LangChain, Temporal, Redis or Celery before a measured need. For the first real trial, Python 3.11+ and SQLite (stdlib) minimize supply-chain and deployment surface.

## Running location: cloud versus local machine

Official Grok Bot documentation says Bots share one persistent cloud computer, including files, CLI credentials and logins. Its durable workspace is /workspace. This computer is **not** the user's own laptop. Running a command on the user's own machine needs separate user permission. Hence the P0 program targets both environments, but deployment must be verified on the actual target; a GitHub CI pass cannot do this.

    python3 scripts/grok_cloud_doctor.py --repo .
    python3 scripts/grok_cloud_doctor.py --repo . --audits --self-test

The doctor is strictly an offline check of tools, files, repo SHA, local audits and tests. It does not install dependencies, connect to Grok's account, inspect secrets or verify live market feeds. An empty/unknown Grok Skill status is not equivalent to confirmed absence.

## Runnable specialist workflow

                         GPT research and GitHub review
                                       |
                            Fixed Git checkout SHA
                                       |
                        Grok B01 chooses source & task
                                       |
                           Python research/bot_knowledge
                                       |
                           SQLite research-handoff queue
                                  /       |       \
                               B02      B03      B05
                              source   structure  challenge
                                       |
                              reviewed research reports
                                       |
                        separate approval → future B07

The task queue **does not start Grok models**. It manages a durable task envelope. A Grok Bot claims a task, performs its own allowed work, writes a reviewable result and records an output digest.

    PYTHONPATH=src python3 -m solana_meme_os.runtime_store init
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store submit --input fixtures/bot-handoff-brief.fixture.json
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store claim --bot B02
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store claim --bot B05
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store status --packet-id FIXTURE-B01-001

After a result file has been separately produced, derive its real SHA-256 and complete the specific recipient:

    PYTHONPATH=src python3 -m solana_meme_os.runtime_store complete --bot B02 --packet-id FIXTURE-B01-001 --result-sha256 <64hex>

Blocked delivery:

    PYTHONPATH=src python3 -m solana_meme_os.runtime_store block --bot B02 --packet-id FIXTURE-B01-001 --reason "source unavailable"

Requeue is only a separate explicit, recorded decision. The queue has transactional atomic claims (SQLite BEGIN IMMEDIATE) and SHA-256-based idempotent submission, with a unique delivery per packet/recipient. Every claim must be analyzed, never blindly executed.

The store cannot authenticate that the caller really is B02, cannot prevent a privileged process from altering SQLite, and does not validate a claimed research result or F4-F6. It is a **collaboration state tool**, not a security or evidence authority. Queue file is untracked under .runtime and must not contain credentials.

## Deeper execution boundaries

| Domain | Existing callable entry | Required engineering step |
|---|---|---|
| B01 research intake | research, knowledge_delivery, bot_knowledge | strict task manifest bound to source SHA and planned evidence |
| B02 provider capture | gmgn_collect prototype; asof_audit supplied metadata | actual RPC/OKX read-only adapter with byte limits, request/receipt timestamps, unit and provider error tests |
| B03 wallet structure | knowledge cards and handoff schema | deterministic edge/slot graph + CEX hub controls + neg controls |
| B04 experimental Alpha | research protocol and gating plan | pre-registered grouped OOS evaluation and net execution model |
| B05 independent challenge | bot_knowledge validation and asof_audit | evidence authenticity, replay, time leakage and counterexample checks |
| B06 QA | unittest and synthetic fixtures | independent source replay, fault injection and version rollback tests |
| B07 monitor | monitor.py experimental JSON state | separately frozen rules, real single-writer SQLite store, durable alert dedupe and paused/tested Routine |

The new research SQLite queue does **not** fix the existing monitor.py shared-state race. B07 must remain unscheduled until its own single-writer and approved rules are implemented.

## Provider framework study: OKX, Solana RPC, GMGN

See design/local-provider-capabilities.v1.json. This is a **declaration**, not a working network filter.

- Solana RPC is a candidate read-only source; actual provider credential, subscriptions, commitment, slot, unit and availability semantics are not verified.
- GMGN existing collector stores raw read-only payload but normalizes metrics to empty until field units are checked. Do not make a paid subscription a runtime dependency.
- OKX OnchainOS current repository has read-only okx-dex-market and separate wallet/payment/trade features. The market Skill is a candidate, **not installed**. Its read-only methods need an actual CLI allowlist, source verification and real error/cost tests before enabling. Do not run the multi-skill installer or OKX wallet execution actions automatically.
- Never treat untrusted token symbols, provider error strings, external SKILL.md instructions or DApp pages as high-priority commands.

Recommended future provider envelope:

    source, version, chain, mint, method, request_at, provider_received_at,
    parsed_at, commitment, slot, raw_reference, raw_sha256,
    decimals, units, provider_status, missing_reason, provider_coverage

At present there is no executable normalization adapter for OKX/RPC. Market observations remain explicitly unavailable until a real response and error contract are validated.

## Engineering acceptance criteria

P0 (repository prototype): doctor returns a JSON capability report without sensitive environment disclosure; original audits and unit tests pass; SQLite test verifies repeat submit, multi-recipient claim, crash/restart persistence, explicit blocked recovery, B07 exclusion and refusal to interpret a packet as executable shell.

P1 (actual Grok cloud): verify checkout SHA, Python/Node binaries and per-account workspace; manually run B01→B02/B05 synthetic handoff on the shared computer; confirm human review and output hashes. A passed local CI is not a cloud demonstration.

P2: select one owner-approved, strictly read-only data source; implement provider adapter with bounded response, original timestamps, status codes and no-future test. Then tackle the B07 monitor single writer and frozen-release loader.

No real trading, signing, wallet secrets, swaps, broadcasts or automatic payments in Phase 1.

Official references:
https://docs.x.ai/grok-bot/computer-and-apps
https://docs.x.ai/grok-bot/skills-routines-and-automations
https://docs.x.ai/grok-bot/approvals-security-and-privacy
https://github.com/okx/onchainos-skills/tree/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25

## Offline OKX import is implemented separately (not a network adapter)

As part of P1 investigation, src/solana_meme_os/okx_snapshot.py reads a saved JSON response without invoking onchainos or signing x402 charges. It checks response envelope, optional provider notifications, Solana mint address and Decimal candidate fields, and returns an explicitly unverified source envelope. See docs/okx-onchainos-runtime-review.md and docs/grok-local-runbook.md. The provider remains disabled for live fetching, and the returned fields must not enter B07 metrics directly.
