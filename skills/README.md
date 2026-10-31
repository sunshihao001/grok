# Skills adapted for Grok Bots

本目录包含 Grok 项目采用的独立技能契约。技能文件是 GitHub 中的设计与研究资产，**文件存在不代表 Grok 云端已经安装或执行**。

| Skill | 职责 | 与其他技能的区别 |
| --- | --- | --- |
| [solana-meme-system-intelligence](solana-meme-system-intelligence/SKILL.md) | 全市场钱包异动、捆绑/协调候选、正常与异常基准、经济网络、市场结构及纸面机会的专家研判 | **顶层领域能力**；不是普通跟单或单币种监控引擎；[范围及阶段目标](../docs/solana-meme-marketwide-monitoring-scope-v1.md) |
| [solana-meme-expert-writing](solana-meme-expert-writing/SKILL.md) | 深读系统各领域原始知识、重构监控机制、跨项目推演与专业研究写作；钱包可跟随性只是众多研究单元之一 | 面向专家研究文章与认知深化，不是普通关键词检索；附 [深入写作方法](solana-meme-expert-writing/references/research-writing-playbook.md) 和 [实际示范](solana-meme-expert-writing/references/wallet-copyability-worked-example.md) |
| [solana-meme-knowledge](solana-meme-knowledge/SKILL.md) | 基于已有知识卡与来源索引，按问题选择适用的知识并保留不确定性 | 适合常规知识调用；无法替代原文精读和新机制研究 |
| [solana-meme-monitor](solana-meme-monitor/SKILL.md) | 只读行情快照与变动监控、证据和状态记录 | 负责观察与报告，不负责推导未经证实的交易策略 |

## 研究与写作使用方式

当任务是“分析哪些钱包在何时批量注资/买入、是否异常、可能怎样关联、有什么市场含义”时，以 `solana-meme-system-intelligence` 为入口；当任务要求写完整深度研究文章，再结合 `solana-meme-expert-writing`。根据研究问题，按需调用 `solana-meme-knowledge` 检索参考文件。

建议的任务表述：

> 使用 `solana-meme-system-intelligence` 深入研究“同一批钱包为什么在某个时间窗口进行集中资金转入、买入与库存转移”。先明确时间、Mint、地址数、交易数和 SOL/Token 规模；再将同 Slot 协调、共享资金基础设施与同控执行的解释置于同类基准和反证中。延伸至流动性/筹码结构、跨 Mint 重复行为和纸面交易资格；使用 `solana-meme-expert-writing` 形成完整专业文章。

当研究需要真实数据或 Grok 的实际监控输出时，按相应能力另行操作；没有数据不能编造已执行的验证。禁止在本阶段触发真实交易、签名、广播和自动部署。

项目总入口：[跨源知识整合](../docs/knowledge-system-integration-v1.md)、[全市场监控范围](../docs/solana-meme-marketwide-monitoring-scope-v1.md)。旧 [跟单专题规范](../docs/solana-meme-copytrade-cognition-conversion-v1.md) 和历史钱包研究仍保留，但不作为整个系统的最高目标。

## M2 离线聚合原型（2026-10-31）

新增 [多钱包群体事件观察器](../docs/market-observatory-m2-v0.1.md)：从明确来源的规范化事件集合计算时间窗口、批量转账、同 Slot 买入、Token 汇集与跨 Mint 活动。**该模块尚未连接真实 Solana RPC 或 Grok 云端，不会自动发现全市场所有新币**；没有正常基准时仅输出候选，不给“异常/庄家/盈利”的确定标签。
