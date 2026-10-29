# Grok cloud Bot knowledge installation checklist — v0.1 (not executed)

## What is actually installable?

This repository provides **configuration artifacts**: `bots/profiles/B0*.md` role startup instructions, `knowledge/bot-knowledge-profiles.v1.json` curated expertise syllabus, `knowledge/source_index.v1.json` for retrieval and `knowledge/bot-handoff.schema.json` for reproducible work.

These files do not by themselves create Bots on Grok's cloud computer, activate app connections, install private Skills, grant access to RPC, or schedule a Routine. The owner must carry out those steps in their Grok Bot account. Do not confuse ChatGPT's connector connection with Grok Bot's app permissions.

## Ordered manual activation

1. In Grok Bot, create B01, B02 and B05 using the [official Bot creation path](https://docs.x.ai/grok-bot/bots). Copy each `bots/profiles/B0*.md` *role instructions* into the corresponding Bot's first setup task or configured files/context. Use its instructions to load the minimal K0 files and specific source links from the repository.
2. Prepare one shared repo workspace and **separate task directories/branches**, no wallet keys. Ensure every Bot that can see the computer is allowed to see every file and signed-in session; do not use Bots as credential isolation.
3. Register reusable private skills in the Grok Bot Skill library, explicitly enable them for roles as required, and test one manual invocation. The repository `skills/` files are **instructions/templates**, not proof they are installed. See https://docs.x.ai/grok-bot/skills-routines-and-automations .
4. Have B01 assign a simple source discovery question to B02/B05 with an explicit `decision_cutoff_utc`; compare the produced handoff JSON to the schema and verify its cited commits/transactions are accessible.
5. Verify B02 real read-only GMGN/RPC data and the unit/time conversion; if no legitimate raw access is granted, stop at K0/K1 research and record `K2_UNAVAILABLE`.
6. Only after early contracts pass, configure B03, B04 and B06. Ask B04 to work from a preregistered hypothesis, B05 to challenge it independently, and B06 to replay untouched cases. Do not elevate old FCZ research, GMGN hints, uncalibrated confidence or external negative papers into automatic rules.
7. Create B07 last. Configure a read-only Skill, a human-approved frozen rule version and a **paused** Routine; test input source, time zone, output, duplicate suppression, error handling and single-writer behavior before enabling.
8. Record exact bot IDs, skill library names/versions, configured source connections, test evidence, observed failures and next review in a private deployment ledger **without secrets**.

## Expected limits

- Shared cloud computer means all Bots in the account can access its files, browser sessions and terminal credentials.
- The cloud Bot may have no RPC/GMGN access until separately connected; no fake response or “success” status should be generated.
- Excerpts from external written studies with CC BY-NC-ND terms must be referenced rather than redistributed as rewritten text.
- A readable source and a passing unit test do **not** imply positive Alpha, live monitoring, data integrity or safe trade execution.
- Phase 1 remains research-only / paper-only.

## Enforced publication boundary

Before enabling B07, ensure no development Bot writes to B07's runtime state, normalized live input buffer or frozen rules. B02's field/schema evolution is delivered via reviewed PR and explicit release, not via a live B02-to-B07 Bot chat.
