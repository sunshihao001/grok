# Blix｜签名发现的原子水位与断点补读（2026-11-08）

状态：NEW_BRANCH_ONLY / TESTS_PENDING / NOT_LIVE. 基线：PR #18 `d3da7c9c`（而非旧PR#19），以免重复实现已存在的Reader处理状态。

## 针对的真实源码缺口

原 `wallets.pollOne` 在SQLite写入最新 `wallets.last_sig` 后，才向进程内 `backlog` 放入返回的签名。若这两步之间退出，程序可能把从未读出的交易视为“已经越过的历史”；`wallet_trades`与`missingEvidence`都可能不知道这些签名存在。

## 这次的唯一增量

- `wallet-signature-coverage.mjs`：`wallet_sig_jobs`登记**已发现的签名**，`wallet_sig_windows`登记本次窗口/锚点/初始25笔局部采样/已出现过的截断，不把「没看到」当「没有交易」。
- `checkpointWalletPage`将签名索引与 `wallets.last_sig`更新纳入同一SQLite事务；崩溃前已经提交的签名可以从本地恢复，崩溃前未提交的last_sig不会提前推进。
- `pendingWalletSignatures`使用 PR#18 **原有且唯一**的 `econ_wallet_processing` 来过滤已完成/已由有界重试处理的事务；不另设第二套 `RPC_CAPTURED` / `READER_FINISHED`状态。
- `pollOne`先恢复本地未消费签名，再调用原有RPC分页；若调用失败，轮询外层仍会将已恢复队列交给Reader，不增加主动外部抓取。
- 保留首次扫描的 `quiet` 标记；单钱包旧gap不会因下一轮扫描成功而清零；同签名不同钱包可分别登记。
- 继续沿用 PR#18 已有的hook异常处理、本地RPC归档重放和消费状态，不复制第二套Reader。

## 验收及边界

隔离 `node:sqlite` 用例涵盖原子提交、模拟进程关闭再打开SQLite、故障回滚、初始扫描不等于全历史、截断gap永久保留、已有PR#18的CAPTURED/COMPLETE/RETRY_REQUIRED协调、同签名多钱包与链上失败事务。只有CI真实运行通过之后才标 `ISOLATED_TESTED`。

未解决：
1. websocket通知在下次轮询前丢失仍可能不进入签名清单；这里没有伪装为全量实时流。
2. 原始`getTransaction`来源/确认级别、CPI/Token-2022解析仍需与PR#19的证据加固对照，**绝不可用旧PR#19的readTx直接覆盖PR#18的新重试实现**。
3. 旧钱包`wallet_sig_jobs`长期增长的空间预算与归档，以及手动补查`CAP_REACHED`/缺历史状态没有完成。
4. 所有功能都仅为读链事实的工程支撑；原Blix包含交易/AI费用和账户自动路径，**未得到只读安全启动许可，也没进行主网持续运行测试**。
5. 这是围绕被跟踪钱包的持久采集；接收钱包历史仍需按需受限补查，不能自动把所有关联钱包持续订阅。

参考：[PR #18](https://github.com/sunshihao001/grok/pull/18)、[PR #19](https://github.com/sunshihao001/grok/pull/19)、[PR #20建设台账](https://github.com/sunshihao001/grok/pull/20)、[PR #21先行分支（尚有重复状态，禁止原样合并）](https://github.com/sunshihao001/grok/pull/21)，以及 [PumpTrace回补manager](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)。
