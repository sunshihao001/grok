# Grok Bot setup — smallest real handoff (current)

> **Status:** Engineering PR #16 contains a tested public Mint report and an offline, hash-verifying evidence handoff. This GitHub document **does not** provision a Grok Bot or prove a Grok cloud run. Historical `BOTS.md` describes an optional six-role development arrangement, not six required deployed Bots. Current acceptance needs **one** Grok Bot with a terminal and reviewed GitHub source.

## First acceptance: Grok actually calls the existing program

1. In Grok's persistent cloud computer, obtain the reviewed engineering branch `research/p24-cross-mint-m01-batch-monitor-20261031` from `sunshihao001/grok`. Before executing it, inspect its commit SHA and use only the approved read-only modules. Python 3.11+ is required; there are no transaction wallets, signer credentials, or paid integrations in this test. Do not merge either Draft PR.
2. Have Grok read [`skills/solana-meme-monitor/SKILL.md`](../skills/solana-meme-monitor/SKILL.md). You can ask in natural language: **“分析 Mint EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump，运行现有只读程序，检查来源，分析风险，并保存运行证据。”**
3. Grok首先运行**当前唯一的产品入口**，不要求用户自行拼接两条底层命令：

   ```bash
   PYTHONPATH=src python -m solana_meme_os.product EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump
   ```

   程序自动建立新目录、调用现有Mint采集和来源核验，返回`run_status.json`及报告路径。**exit 0**表示`READY_FOR_GROK_REVIEW_NOT_EXECUTED`；**exit 4**表示仅有部分供应商报告；**exit 2/3**表示错误、全部数据源失败或来源核验拒绝。不能把部分报告算成完整Grok证据包。
4. Grok从返回的目录读取`mint/report.json`、`mint/report.md`；只有`evidence.json`真实存在且校验通过才进行多源研究。程序本身不调用Grok、不部署Bot、不交易。
5. Grok **independently** reads evidence and original source files, supplies competing explanations and missing observations, and writes its answer **separately** to `grok_analysis.md`. It must not claim vendor risk tags are live transaction alerts or that the 19 unresolved accounts are 19 individual controllers.
6. Review the **actual Grok execution evidence**: cloud computer command log, checked-out SHA, the output directories, provider acquisition times/coverage, Grok's resulting analysis, and ability to reopen the saved files. A GitHub Actions success only validates the Python side, not Grok.

After that acceptance, use the *same* Grok Bot to call an approved read-only Million/OKX existing workflow for a wallet candidate, or study market/X discourse. Add a Routine only when a real repeated observation source and missingness/restart behavior have been tested. A long-running WebSocket listener should remain a separate bounded, supervised service, not a Grok LLM loop.

## Developer-only checks, already possible without Grok

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

[`tests/test_grok_mint_evidence_pipeline.py`](../tests/test_grok_mint_evidence_pipeline.py) uses mocked vendor HTTP bytes to execute **both original Python CLIs**. The one-command user product entry is independently checked in [`tests/test_product_entry.py`](../tests/test_product_entry.py) for complete/partial data, validation rejection and directory isolation. Neither test is a Grok cloud execution. [`docs/vendor-event-handoff.md`](vendor-event-handoff.md) documents the same two-step interface.

For operational expansion, `BOTS.md` and `routines/monitor.md` remain historical/optional design references: **do not create six Bots or enable a live Routine simply because those files exist.** Secrets stay in a least-privilege environment; all Bots share the same Grok cloud computer and should never receive private keys or automatic wallet/transaction permissions.

Official Grok Bot documentation: https://docs.x.ai/grok-bot/get-started and https://docs.x.ai/grok-bot/skills-routines-and-automations.
