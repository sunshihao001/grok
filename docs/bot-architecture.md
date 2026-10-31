# Grok Bots｜工程交接与边界

本项目设计为多个研发角色与一个最终的只读 Monitor Bot。**所有角色和技能都只是当前仓库的设计资产**；实际 Grok 云端创建、Skill 装载和 Routine 调度未验证完成。

## 权限和环境

- 研发角色：按任务读取原始知识、调查事件、提出测试与草案分支变更。实测权限取决于实际 Grok 环境；不能仅由设计假定共享电脑总是可用。
- Monitor：读取已经审批冻结的来源、代码与监控规则；不修改规则、不开发、不使用私钥、不下单。
- 状态与工件：仓库 `state/` 只存设计占位说明；真正运行目录、锁/并发、日志保留、隐私与失败恢复需要在目标环境单独实现。

## 研发交接

`question + scoped_event_ids + source_hash/commit + observed/available/received times + wallet/Mint/pool + measured_amounts + baseline_population + candidate_mechanisms + counterexamples + next_check + code/test_version`。

一轮交接不得把 `SAME_SLOT_MULTIWALLET` 直接升级为 `CONFIRMED_JITO_BUNDLE`，也不能将 `FUNDING_FANOUT` 直接升级为 `COMMON_BENEFICIAL_OWNER`。

## 运行入口

- **现有代码**：`solana_meme_os.monitor`（单 Mint 观测）、`solana_meme_os.market_observatory`（输入已归一化事件的窗口候选）。
- **待实现**：真实跨 Mint 链上数据发现、RPC 指令解释器、正常/异常基线和综合状态持久化。
- **未来用户入口（仅设计）**：按 Mint 查看、按 wallet 查看、按时间窗查看、查看跨 Mint 异常候选和定期报告。
- **知识入口**：领域 Skill + 知识来源路由 + 专题专家研究；系统不得被历史 15 张卡或旧七段流程限制。

最终发布需要真实环境测试、源覆盖报告、人工审批和清晰回滚；GitHub 文件本身不会创建云端 Bot 或 Routine。参见 [BOTS.md](../BOTS.md)、[Grok 设置](grok-setup.md) 与 [总整合蓝图](knowledge-system-integration-v1.md)。
