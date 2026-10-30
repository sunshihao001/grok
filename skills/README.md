# Skills adapted for Grok Bots

本目录包含 Grok 项目采用的独立技能契约。技能文件是 GitHub 中的设计与研究资产，**文件存在不代表 Grok 云端已经安装或执行**。

| Skill | 职责 | 与其他技能的区别 |
| --- | --- | --- |
| [solana-meme-expert-writing](solana-meme-expert-writing/SKILL.md) | 深读参考项目、重建市场机制、跨源知识融合、原创专业研究写作与知识转换 | 面向专家研究文章与认知深化，不是普通关键词检索；附 [深入写作方法](solana-meme-expert-writing/references/research-writing-playbook.md) 和 [实际示范](solana-meme-expert-writing/references/wallet-copyability-worked-example.md) |
| [solana-meme-knowledge](solana-meme-knowledge/SKILL.md) | 基于已有知识卡与来源索引，按问题选择适用的知识并保留不确定性 | 适合常规知识调用；无法替代原文精读和新机制研究 |
| [solana-meme-monitor](solana-meme-monitor/SKILL.md) | 只读行情快照与变动监控、证据和状态记录 | 负责观察与报告，不负责推导未经证实的交易策略 |

## 研究与写作使用方式

当任务是“把参考项目的知识吃透”“将某个市场机制写成专业研究”“跨仓库形成新认知”时，以 `solana-meme-expert-writing` 为入口；根据研究问题，按需调用 `solana-meme-knowledge` 检索参考文件。

建议的任务表述：

> 使用 `solana-meme-expert-writing`，深入研究“某个盈利钱包为何不能直接跟单”。优先阅读原 Hermes 的钱包角色/结构资料、meme- 的筹码与市场结构理论及取证项目的方法和反例。提出互相竞争的解释，追问如何验证，写出完整专业论证，不仅输出总结或规划。允许提出新的市场机制，但要标记哪些仍未经证实。

当研究需要真实数据或 Grok 的实际监控输出时，按相应能力另行操作；没有数据不能编造已执行的验证。禁止在本阶段触发真实交易、签名、广播和自动部署。

研究规划和规范见 `docs/solana-meme-copytrade-cognition-conversion-v1.md`、`docs/cognition-conversion-v1-rollout-plan.md`、`docs/knowledge-assets-logic-audit-wave1.md`（在其所在分支可用时）。
