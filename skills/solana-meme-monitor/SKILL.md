---
name: solana-meme-monitor
description: Read-only Solana Meme Mint investigation and source-linked observation; run existing Python commands, verify evidence, and explain uncertainty. No trading.
---

# Grok 主Bot｜按需单Mint调查与观察（调用现有程序）

**实际运行门槛：** Grok云电脑中必须有已审查的 `sunshihao001/grok` 工程PR #16工作树、Python 3.11+及可访问的只读数据源。GitHub代码/Skill文件存在不等于Grok已经安装/执行；先记录 `git rev-parse HEAD`，不得把Actions结果充当Grok运行结果。

## 模式A：用户提出“分析这个 Mint”或“调查这枚 Meme”

**优先使用已实现的两个程序**，不是重新编写数据客户端、启动六个Bot或创建新后端。下面在仓库根目录执行；`MINT`必须是用户提供的Solana Mint地址，`RUN_DIR`每次取新的、未使用目录。

```bash
MINT="用户提供的真实Solana_Mint"
RUN_DIR=".runtime/grok-mint-$(date -u +%Y%m%dT%H%M%SZ)"
PYTHONPATH=src python -m solana_meme_os.mint_v01 "$MINT" \
  --rugcheck --out-dir "$RUN_DIR/mint"
PYTHONPATH=src python -m solana_meme_os.vendor_event_handoff \
  --report "$RUN_DIR/mint/report.json" \
  --rugcheck-raw "$RUN_DIR/mint/rugcheck-provider-raw.json" \
  --dex-raw "$RUN_DIR/mint/dex-provider-raw.json" \
  --out-dir "$RUN_DIR/grok-outbox"
```

- 第一步请求公开DEX Screener和可能缓存的RugCheck，只读、无需交易钱包。第二步**离线**比对原始响应SHA、链/Mint及数据状态，生成 `evidence.json`、`provisional_monitor_opinion.md`、按供应商风险项产生的 `grok_task_*.md`。这些是**供你审阅的程序任务**，不是Bot已研究完成。
- **不要在第一步成功但第二步失败时宣布端到端成功**；第二步需要双方真实源同时可用。如果缺少DEX/RugCheck任一原始文件、身份不一致、错误/限流，明确报 `UNAVAILABLE` 或 `EVIDENCE_HANDOFF_FAILED`，不要补造另一源或伪装为无风险。
- Grok本人必须实际读取 `mint/report.md`、`mint/report.json`、`grok-outbox/evidence.json`；根据现有知识按需调查X相关CA/Dev/叙事和市场外部解释。**区分**：供应商事实/标签、链上尚未验证的Token Account Owner、经济主体竞争解释、需要补的原始交易签名。没有X访问权限时只报告 `X_RESEARCH_UNAVAILABLE`。
- 对每项重要结论给出具体原始证据路径和采集时间，说明池/AMM不能直接算独立鲸鱼，供应商风险标签不等于已证欺诈，Token Transfer不等于Swap，未知钱包资金关系不得假装已经查到。
- 在Grok会话中返回实际执行的Git SHA、两步退出状态、原始数据源状态、生成文件路径、一次真实源码/证据判断，以及一个最有信息价值的下一步。只有**确实从Grok云电脑完成运行并读取任务**后，才可以标为 `GROK_CLOUD_MINIMUM_ACCEPTED`；否则始终 `GROK_NOT_EXECUTED`。

## 模式B：用户请求“观察变化/追踪钱包”

目前仅有 `solana_meme_os.monitor`（规范化观测输入）和 `wallet_batch_monitor`（fixture-only的1/5/15分钟经济事件聚合），**尚无真实、可靠的持续链上事件流**。

1. 先确认观察来自被允许的数据来源、时间/字段单位、Mint地址和覆盖范围；仅真实归因的交易事件才可交给批次监控。不能把模式A的供应商快照变成已确认的BUY/SELL。
2. 对已有合法观测文件运行：
   `PYTHONPATH=src python -m solana_meme_os.monitor --input OBSERVATION_PATH --state-dir .runtime`
   `--allow-fixture`只能用于明确标注为演示的离线测试。
3. 依据已记录的状态变化、来源和竞争解释输出观察报告。数据缺失或断开时报告UNKNOWN，不输出“该钱包停止交易”的肯定结论；不因Grok的Routine存在就称真实监控已上线。
4. 只有经过**真实观察两时点、缺失恢复和重复事件核验**，且用户要求持续扫描，才考虑已授权的Routine；Routine创建/启用与云电脑运行仍需在Grok端逐项验收。

**专业知识选择**：按当前任务调用相关D01–D12或已有专家视角即可，**不强制22位专家会诊、六Bot启动或固定阶段流程**。专业意见必须能改变经济解释或下一步核查。相关资料保存在 `knowledge/` 和旧参考仓库。

**安全边界**：仅只读网络查询、既有审核过的CLI和本地报告。禁止私钥、交易签名/广播、购买服务、自动付款、安装未经审查代码、未经用户授权的对外发布或把X营销利润当事实。

**工程测试（不是Grok云端验收）**：`PYTHONPATH=src python -m unittest discover -s tests -v`；真实GitHub Actions双来源采集与交接证据见 `.github/workflows/one-shot-public-rpc-holder-20261101.yml`。
