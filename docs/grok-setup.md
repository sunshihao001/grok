# Grok Cloud Setup | Market-Wide Monitoring Handoff (Not Deployed)

GitHub files are designs and local Python code; they do not create Grok Bots, activate Skills, connect wallet/RPC services or schedule Routines. The final system consists of approved research/development roles and one read-only Monitor Bot; see BOTS.md and docs/knowledge-system-integration-v1.md.

## Preparation

1. Connect GitHub to the target Grok environment with least privilege; no shared keys or transaction signing.
2. Install a supported Python runtime in the user's authorized cloud computer and run the complete offline tests on the exact commit.
3. Load the market-wide domain Skill (skills/solana-meme-system-intelligence/SKILL.md) and use the expert writing, knowledge and monitor Skills only for their described responsibilities. Verify that the target Grok runtime actually detects and applies them.
4. Demonstrate the deterministic synthetic workflow: `PYTHONPATH=src python -m solana_meme_os.market_observatory --input fixtures/market-observatory-synthetic.json --allow-fixture`. Output is a test, not an actual Solana alert.
5. Separately connect approved real read-only event/market sources (Solana RPC, verified OKX or GMGN capabilities). Validate signatures, instruction types, Token/SOL units, source timestamps, rate limits, permissions, and missingness. Do not use a source label as verified chain identity.
6. Run one real-data, read-only event-window replay with a complete normal comparison and some deliberate negative cases. Confirm exact wallet/transfer counts, duplicate suppression, shared hub explanations and reporting latency.
7. Only after reviewed source, storage, permissions and failures, test one monitored run in a configured final Grok Bot. No automatic schedule merely because offline tests pass.
8. If subsequently desired, request a **paused** Routine using routines/monitor.md, review frequency for Slot/second-level event monitoring and source limits, inspect its Test result, and obtain a separate explicit approval before enabling.

## Environment boundaries

- Neither the old Hermes runtime nor the qb-/GMGN CLI is mandatory. Do not copy their secrets, hooks or absolute paths.
- Existing monitor.py consumes single-Mint snapshot JSON; market_observatory.py consumes a different multi-event schema. Never silently substitute one.
- Same-Slot group is a candidate, not confirmed Jito Bundle. Common funder is a hypothesis, not a beneficial owner claim.
- No real trading, private keys, signing, broadcast, production-rule self-upgrades or unapproved external notifications.

Official Grok documentation (verify current environment): https://docs.x.ai/grok-bot/get-started and https://docs.x.ai/grok-bot/skills-routines-and-automations.
