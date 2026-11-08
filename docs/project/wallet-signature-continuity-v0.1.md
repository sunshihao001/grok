# Blix｜钱包签名持续采集与恢复 V0.1（2026-11-08）

> **状态：FEATURE_BRANCH / OFFLINE_CI_PENDING / NOT_LIVE.** 这是已有经济证据加固PR #19之上的小幅续接，不属于已合并的 `blix`。没有运行原主服务、真实RPC、交易、签名、付费或部署。

## 为什么优先做，而不是继续建钱包图

既有 `wallets.pollOne` 把 `wallets.last_sig` 推进到最新轮询签名，再把签名加入仅存在内存的 `backlog`。若在二者之间崩溃，下次轮询可能只回看新水位以后的交易，使整个Mint/W1→W2关系链永久失去部分历史（除非另一条独立渠道重读）。`missingEvidence` 只比较已经产生钱包Trade的签名，不能发现这种完全未处理的签名。

## 最小增量

- 新增 `server/wallet-signature-coverage.mjs`。在原 `radar.db` 的独立小表记录签名发现、RPC已存、Reader已完成、链上失败、达到最大重试次数。它是**采集任务状态**而非新钱包图或经济事件表。
- `checkpointWalletPage` 将已发现签名和原 `wallets.last_sig` 水位在**同一个SQLite事务**提交；原钱包列表、限速RPC、stream、轮询读者、经济事件归档和UI不替换。
- 下次 `pollOne` 优先恢复本地未完成签名，再执行现有分页API；`readTx` 有已存 `getTransaction` 原文时优先回放，减少故障后的重复RPC。
- `INITIAL_SAMPLE_ONLY`：首次默认只取最近25个签名，**不能宣称钱包历史已完整**。后续 `INCREMENTAL_ANCHOR_REACHED` 也仅表示当前增量锚点已覆盖。
- `WINDOW_TRUNCATED_OR_ANCHOR_LOST`：分页上限/锚点消失导致“可能还有遗漏”。`gaps_seen`、`last_gap_at_ms`、`ever_initial_sample` 不被后来一次正常扫描清零。`READER_FINISHED` 仅表示旧摘要完成，不表示CPI与经济动作100%识别。
- 一笔已捕获RPC交易但尚未形成摘要，保留 `RPC_CAPTURED`，重试优先复用存档，不把“缓存原文”误说成“完成处理”。
- 超过三次重试时保存 `NEEDS_MANUAL_REPLAY` 与概括性错误类别；**不会自动无限重试、不保证缺口已经修复**。
- 初次扫描任务的 `quiet` 标志保留以供重启恢复，避免恢复历史扫描变成实时交易提醒。

## 离线验收与业务价值

`test/wallet-signature-coverage.test.mjs` 使用node:sqlite和临时DB覆盖：
1. 事务性签名+水位；
2. 在入队之前模拟进程重启并恢复；
3. SQLite写入故障回滚，水位保持不变；
4. 历史截断不得标记完整；
5. 后续正常扫描不能洗掉旧缺口；
6. 同钱包重读不重复计数；
7. RPC已存/Reader已处理的区分；
8. 超次重试的显式失败；
9. 不同钱包相同签名仍有独立处理状态；
10. 链上失败签名不进入可读交易队列。

**仍待验收**：
- 真实Node24 CI、完整旧WTrack/市场流水线回归。
- websocket签名触发的瞬时内存队列在轮询前崩溃仍可能存在盲区；不宣称所有签名已经被持久收集。
- `wallet_sig_jobs` 长期留存的空间预算、定期压缩和可重放归档；生产接入前需要解决。
- 原WTrack `fromTx` 的某些异常会被外围hook捕获而不传给Reader，故 `READER_FINISHED` 不等于所有下游消费者成功；需进一步显式ack与失败记录。
- 时间戳、Slot、确认状态、真实经济库存与资金路径的独立核验；局部扫描可能仅覆盖最新25笔。
- `NEEDS_MANUAL_REPLAY` 的有权限人工/自动回补入口未建，本轮只是避免静默丢失。
- 仍需要只读安全运行隔离。不要将本分支直接用于生产或声称主网实测。

## 研究依据与成熟复用
- Blix 原 `pageSignatures`、`wallets.pollOne`、`wallets.readTx` 与现有经济事件归档。
- [PumpTrace可续传回补任务](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)：保留cursor、CAP_REACHED与COMPLETE不同；不复制另一套执行引擎。
- [Million历史采集与truncated](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/helius.service.ts)：交易类型与分页范围各自影响可见性，不以短窗口推全历史。
- [现有Blix建设台账](https://github.com/sunshihao001/grok/pull/20)：BL-04/11/13；[功能分支的建设登记](https://github.com/sunshihao001/grok/blob/feat/blix-economic-evidence-20261108/docs/project/build-register.md)：B02/B03/B04/B09。两份登记各有作用，尚未统一合并。
