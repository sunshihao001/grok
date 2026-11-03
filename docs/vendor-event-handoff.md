# Vendor evidence → Grok review handoff (read-only)

This module is an executable, tested adapter for the existing Mint V0.1 report, **not** a live on-chain-event detector or a connected Grok Bot.

## Run with existing public report

1. Run the already implemented read-only Mint report:
   PYTHONPATH=src python -m solana_meme_os.mint_v01 <MINT> --rugcheck --out-dir .runtime/mint
2. Produce evidence-backed review tasks from the **same acquisition's raw bytes**:
   PYTHONPATH=src python -m solana_meme_os.vendor_event_handoff --report .runtime/mint/report.json --rugcheck-raw .runtime/mint/rugcheck-provider-raw.json --dex-raw .runtime/mint/dex-provider-raw.json --out-dir .runtime/grok-outbox/<unique-run-id>
3. Inspect evidence.json, provisional_monitor_opinion.md, and grok_task_*.md.

Create a **new out-dir per acquisition**; do not reuse an old outbox containing previous tasks.

The tool validates source hashes, Mint/chain and provider snapshot status. It generates:
- one pending **review task** per flagged RugCheck vendor risk label (not a verified on-chain incident);
- suppressed or unresolved top-holder candidates where pool infrastructure or missing ownership evidence makes a whale accusation unsafe;
- unobserved wallet/funding/RPC coverage and a "Grok NOT_EXECUTED" status.

There are **zero LLM calls** in this module. Nothing contacts OKX, Grok, a webhook, a wallet or any payment system. Claims of automatic live wallet monitoring, shared-funder control or Bot-to-Bot expert completion require distinct runtime evidence.

Check offline tests: PYTHONPATH=src python -m unittest discover -s tests -v

## Next product acceptance

Connect one independently verified Solana transaction signature with *all* wallet observations to the existing fixture-only wallet_batch_monitor. Verify replay, missingness, and provider cost. Only after this succeeds should a configured Grok Bot consume an evidence package and return an independently logged specialist response.

Source: engineering PR #16; evidence from GitHub Actions #41269179918; related domain knowledge PR #14 remains a separate, unmerged branch.


## 2026-11-03｜真实公共数据到Grok证据包：执行验收（非Grok运行）

已在工程Draft PR #16的**原有** `mint_v01` + `vendor_event_handoff` 两条Python命令上完成一次GitHub Actions真实联网端到端运行（两条命令均独立完成；没有调用Bot或LLM）。没有重新开发Grok后端。

- **运行记录**：[Actions #41570660069](https://github.com/sunshihao001/grok/actions/runs/41570660069)；公开真实运行输入Mint `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`；[证据ZIP Artifact #13200229610](https://github.com/sunshihao001/grok/actions/runs/41570660069/artifacts/13200229610)（保留至2026-11-17）。
- **报告与数据状态**：GitHub runner真实访问DEX Screener和RugCheck，两个来源均成功；`source_errors={}`；RugCheck当前返回20条Top Holder **Token Account候选**及Creator候选；公开Solana RPC没有调用，OKX没有调用。RugCheck是**可能缓存的供应商结果**，不是同slot链上事实。
- **两个程序的实际业务交接**：`mint/report.json`、`mint/report.md`和两份原始响应保存于Artifact；下一条命令根据原始响应SHA-256、链/Mint和来源状态生成 `grok-outbox/evidence.json` 及2条供应商风险标签人工复核候选；另有1项大额Holder**需抑制/解释的基础设施候选**（具体归因需看对应源字段）；所有钱包实际交易、资金网络及Bot判断仍未知。
- **自动验收**：日志出现`VERIFIED_MINT_SOURCES`和`GROK_HANDOFF_READY_NOT_EXECUTED`；`model_calls=0`、`auto_payments=0`、`coverage.wallet_transactions=NOT_OBSERVED`、`disposition=PREPARE_GROK_TASKS_ONLY_NO_BOT_INVOKED`。这只是**数据包可消费**，不代表Grok已经实际研究那两条风险标签。
- **离线跨模块测试**：新增 `tests/test_grok_mint_evidence_pipeline.py`，在模拟网络返回情况下依次执行原有两个CLI，独立核对原始响应Hash、Pool/AMM候选抑制、风险任务与不执行交易/模型的状态，并验证如果DEX原始来源缺失，第二个CLI会以**退出码2拒绝交接**。第一次测试把CLI预期的`SystemExit(2)`误写为`FileNotFoundError`，已按真实失败日志修复；当前[Actions #41570857512](https://github.com/sunshihao001/grok/actions/runs/41570857512)全部离线测试通过。另有`tests/test_grok_mint_handoff_integration.py`检查独立的端到端校验与篡改拒绝。
- **Grok云电脑未验收**：当前ChatGPT会话没有用户Grok云电脑控制权限；即使GitHub Actions的全部测试通过，也**不能**标为`GROK_CLOUD_MINIMUM_ACCEPTED`。Grok端需要严格按[现行Skill](../skills/solana-meme-monitor/SKILL.md)在其云电脑实际运行这两条命令、读取本次`evidence.json`并独立交付可复查的`grok_analysis.md`。目前状态是 `GROK_NOT_EXECUTED`。

**最小运维选择**：一个主Bot即可完成自然语言入口、X研究和调用现有Python脚本。不要默认创建六个Bot或开启Routine；稳定链上持续监听与多钱包实时事件输入在单Mint报告之后另行验证，不能由本次公共供应商快照假装完成。

