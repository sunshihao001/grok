# Grok Bot setup — smallest real handoff (current)

> **Status:** Engineering PR #16 contains a tested public Mint report and an offline, hash-verifying evidence handoff. This GitHub document **does not** provision a Grok Bot or prove a Grok cloud run. Historical `BOTS.md` describes an optional six-role development arrangement, not six required deployed Bots. Current acceptance needs **one** Grok Bot with a terminal and reviewed GitHub source.

## First acceptance: Grok actually calls the existing program

1. In Grok's persistent cloud computer, obtain the reviewed engineering branch `research/p24-cross-mint-m01-batch-monitor-20261031` from `sunshihao001/grok`. Before executing it, inspect its commit SHA and use only the approved read-only modules. Python 3.11+ is required; there are no transaction wallets, signer credentials, or paid integrations in this test. Do not merge either Draft PR.
2. Have Grok read [`skills/solana-meme-monitor/SKILL.md`](../skills/solana-meme-monitor/SKILL.md). You can ask in natural language: **“分析 Mint EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump，运行现有只读程序，检查来源，分析风险，并保存运行证据。”**
3. Grok runs the **existing** `mint_v01` command with `--rugcheck` and a **new run directory**, as specified in the Skill. The output must contain `report.json`, `report.md` and fresh provider raw files when their requests succeed.
4. Grok runs **existing** `vendor_event_handoff` with raw files from the **same acquisition**. The CLI checks provider status, Mint and SHA-256; only valid data reaches `outbox/evidence.json` and `grok_task_*.md`. If a source is absent, stop and report it: a DEX-only report is acceptable as a limited snapshot but not as a complete handoff.
5. Grok **independently** reads evidence and original source files, supplies competing explanations and missing observations, and writes its answer **separately** to `grok_analysis.md`. It must not claim vendor risk tags are live transaction alerts or that the 19 unresolved accounts are 19 individual controllers.
6. Review the **actual Grok execution evidence**: cloud computer command log, checked-out SHA, the output directories, provider acquisition times/coverage, Grok's resulting analysis, and ability to reopen the saved files. A GitHub Actions success only validates the Python side, not Grok.

After that acceptance, use the *same* Grok Bot to call an approved read-only Million/OKX existing workflow for a wallet candidate, or study market/X discourse. Add a Routine only when a real repeated observation source and missingness/restart behavior have been tested. A long-running WebSocket listener should remain a separate bounded, supervised service, not a Grok LLM loop.

## Developer-only checks, already possible without Grok

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

[`tests/test_grok_mint_evidence_pipeline.py`](../tests/test_grok_mint_evidence_pipeline.py) uses mocked vendor HTTP bytes to execute **both real Python CLI entrypoints**, checks provider SHA-256 and rejects tampering; this is not a live API or a Grok runtime test. [`docs/vendor-event-handoff.md`](vendor-event-handoff.md) documents the same two-step interface.

For operational expansion, `BOTS.md` and `routines/monitor.md` remain historical/optional design references: **do not create six Bots or enable a live Routine simply because those files exist.** Secrets stay in a least-privilege environment; all Bots share the same Grok cloud computer and should never receive private keys or automatic wallet/transaction permissions.

Official Grok Bot documentation: https://docs.x.ai/grok-bot/get-started and https://docs.x.ai/grok-bot/skills-routines-and-automations.
