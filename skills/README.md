# Grok Skills｜知识架构 V2.0 下的能力入口

Skills 是可移植的任务规范，不等于实际 Grok 云端已安装。知识体系的层级和各轴定义以 [知识架构 V2.0](../docs/knowledge-architecture-v2.0.md) 为准；研究主线见 [V5](../docs/economic-mechanism-discovery-charter-v5.md)，运行组织见 [V4](../docs/dual-loop-research-runtime-architecture-v4.md)。

| Skill | 所在能力 | 职责 | 不负责 |
|---|---|---|---|
| [solana-meme-system-intelligence](solana-meme-system-intelligence/SKILL.md) | 全局领域研究入口 | 理解市场问题、调度领域知识、提出竞争机制与反证，组织市场监控/研判 | 自行伪造链上事实或下单 |
| [solana-meme-knowledge](solana-meme-knowledge/SKILL.md) | 知识检索与来源治理 | 根据问题查 15 张种子卡、30 条来源指针、原始历史快照与专题研究；保留未知 | 用关键词匹配代替深度理解 |
| [solana-meme-expert-writing](solana-meme-expert-writing/SKILL.md) | 深度研究与知识转换 | 原文精读、概念拆解、跨领域机制推演、证伪设计、研究写作 | 把漂亮文章当作验证 |
| [solana-meme-monitor](solana-meme-monitor/SKILL.md) | 只读监控操作 | 执行已有单 Mint 或规范事件输入程序、报告来源和状态 | 未经验证的异常/同控/交易结论 |

## 专家能力不等于 Skills 或 Bot 数量

17 个专家能力、12 个领域、40 条类型化交接边由机器映射驱动；它们可在同一 Research Manager 中按事件和缺失证据动态调用，不要求 17 个独立云 Bot。初期物理架构以一个只读 Monitor + 一个按需 Research Manager 为目标。见 [专家交互 V2](../docs/knowledge-expert-interconnection-v2.md)。

## 使用方式

- 新问题/市场现象：system-intelligence，确定对象、时间、竞争解释和证据缺口。
- 已知知识问题：knowledge Skill 检索源与卡片，继续读取原文，不被当前目录限制。
- 新机制/深度研究：expert-writing Skill 配合 V5，必须给出竞争解释、判别性证据和 reject_when。
- 已有数据监控：monitor Skill 仅执行匹配输入契约的程序；真实来源未接通时必须标 UNKNOWN/NOT_CONNECTED。

旧跟单规范仍作为专题研究资产，不能覆盖全局知识层级。
