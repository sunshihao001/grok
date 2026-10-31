# Monitor Routine | PAUSED DESIGN ONLY — NOT ACTIVE

This file documents a **possible future scheduled run**; it does not configure a Grok Routine. User approval and tested input permissions are required before any creation or activation.

## Preconditions before scheduling

1. A real, approved source delivers validated and timestamped normalized Solana events; source coverage/lag and budget documented.
2. The selected version of event observatory / per-Mint snapshot code passes offline and real-data read-only tests with replayable evidence.
3. Baseline availability and alert words distinguish candidate behavior from statistically validated anomaly, confirmed bundle and economic identity.
4. Secrets, notifications, storage, quotas, concurrency, duplicate alerts, recovery and failure mode have been reviewed in the target Grok environment.
5. A human explicitly approves a scoped schedule and recipients. Never assume this file or a GitHub commit authorizes a recurring task.

## Proposed operator handoff when prerequisites are satisfied

Ask the final Monitor Bot for a **paused draft** limited to an approved observed-mint and event scope, using reviewed source adapters and skills. On each run capture provenance, window, transaction count, distinct wallets, SOL/Token sizes, candidate graphs, counterexamples, missing data and a source-linked report; do not compute an unvalidated '庄家 probability'. Verify dedupe, time zone and one-time test before separate user approval to enable.

Absolutely no orders, private keys, sign/broadcast, automated rule changes or notifications without approval. Historical scheduled 30-minute cadence was only a proposal, not the correct frequency for Slot/second-level bursts; actual sampling must follow latency and coverage evidence.
