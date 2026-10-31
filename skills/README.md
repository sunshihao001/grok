# Skills adapted for Grok Bots

本目录是可移植的技能契约与研究方法资产。**文件存在不代表 Grok 云端已经安装、加载或执行。** 当前总架构以 [知识体系架构 V2.0](../docs/knowledge-architecture-v2.0.md) 为准。

| Skill | 职责 | 边界 |
|---|---|---|
| [solana-meme-system-intelligence](solana-meme-system-intelligence/SKILL.md) | 全市场事件、钱包群体、资金/库存网络、开发者、正常基准、经济机制和风险研判 | 顶层领域研究能力，不是实时采集器或交易机器人 |
| [solana-meme-expert-writing](solana-meme-expert-writing/SKILL.md) | 深读原始知识、跨领域机制重构、竞争解释、反证和专业研究写作 | 不替代真实数据查询、回测或程序执行 |
| [solana-meme-knowledge](solana-meme-knowledge/SKILL.md) | 按问题检索知识卡和固定版本来源，保留未知与证据边界 | 关键词路由是检索提示，不是语义推理 |
| [solana-meme-monitor](solana-meme-monitor/SKILL.md) | 已批准输入的只读快照/规范事件监控与报告 | 只报告可观察事实和候选，不确认同控或交易信号 |

## 正确的任务路由

- 常规事实/知识问题：knowledge Skill 检索，再根据原始来源回答。
- 市场现象/钱包群/资金流/机制研究：system-intelligence Skill；按需调度17类专家能力。
- 需要深度原文精读、跨项目融合和可证伪论述：expert-writing Skill。
- 已有规范输入的监控执行：monitor Skill；单Mint快照和多钱包事件输入是两个不同接口。

## 当前知识资产

24 张知识卡、30 个文件级来源指针、17 个专家能力、12 个知识领域、9 个典型路由场景、40 条类型化交接。详情见 [knowledge/README](../knowledge/README.md) 和 [机器可读架构](../knowledge/architecture.v2.json)。

M2 事件观察器只消费外部已经规范化的事件；当前没有真实全市场 RPC 接入、正常基准模型或 Grok 云端持续执行。禁止真实交易、签名、广播和未经批准的规则/云端配置变更。
