# Blix 参考项目与未整体搬迁资产入口

本目录存放的是**对成熟项目的知识研究与复用经验**，不是这些第三方项目的完整代码仓库；用户后续只运行/使用Blix。原版保留在各自仓库，是否移植业务实现需要以后单独审查许可、依赖、安全、费用和功能重叠。**不要将第三方README的功能说明当Blix已具备或独立验收。**

## 已保留在Blix的全文历史研究
- [旧Grok 五项目专业知识审查](legacy-reference-project-knowledge-audit.md)：旧行业产品的真实研究问题与可复用逻辑。
- [旧Grok 多跳资金与供应商证据审计](multihop-funding-evidence-audit.md)：多跳识别、公共设施和反证。
- [旧Grok 成熟参考能力复用完整台账](legacy-reference-capability-ledger.md)：较长原始审计；先按具体项目名称或业务问题定向检索，不全文注入模型。

## 外部参考项目（当前保留原文和成熟思路，不整包复制）

| 参考 | 原始项目 | 首要知识用途 |
|---|---|---|
| Million | https://github.com/Kelows/million | Mint↔钱包发现、资金/交易候选、历史窗口与排除理由 |
| PumpTrace | https://github.com/AntC215/Pumptrace | Creator归因、证据分层、历史回补、调查报告 |
| Pulse | https://github.com/nirholas/pulse | 发行生命周期、历史档案、MCP/数据来源 |
| HoldTech | https://github.com/co-numina/holdtech | Holder集中度、钱包质量、快照演化 |
| PumpGrok | https://github.com/swcstudiospace/PumpGrok | AI任务说明、Skill组织、执行收据、安全隔离 |
| OKX OnchainOS | https://github.com/okx/onchainos-skills | 已包装链上只读调查及数据工作流 |
| pumpwatch | https://github.com/cinder-security/pumpwatch | 可复现发行样本及经济行为反证 |
| Why-Solana | https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over | 多跳方法、相关主体与共享服务区分 |
| 旧 Hermes | https://github.com/sunshihao001/- | 钱包角色、资金、筹码、指标推理与历史设计 |
| 旧 qb- | https://github.com/sunshihao001/qb- | 单Mint关键地址矩阵和复查组织 |
| 旧 meme- | https://github.com/sunshihao001/meme- | 经济机制、失败市场形态、策略候选 |
| ai-d | https://github.com/sunshihao001/ai-d | AI问题表征、知识适用、认知提取、目标演变 |

**完整65项参考登记**：仍以旧Grok [gpt-meme-project-index.v1.json](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json) 为来源，而不是仅依赖本页的示例短名单。

## 尚未全文迁入但不会丢失的老资产

- 旧Grok [system目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/system)：旧执行制度、长期进度、项目收束、专家手册、来源登记、原始152单元本体；**不把过去固定执行制度复制成Blix强制指令**。主册和机制研究方法已迁入。
- 旧Grok [legacy-snapshots目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/legacy-snapshots)：更早知识文件及理论副本，适合需求出现时专项核对，不是全部现行有效。
- 旧Grok [transfer目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/transfer)：历史教学与迁移实验；当Blix需要教学/工作交接时再评估。
- 旧Grok [experiments目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/experiments)：执行边界的历史实验资产。
- 历史工程 [PR #16](https://github.com/sunshihao001/grok/pull/16) 与 [PR #17](https://github.com/sunshihao001/grok/pull/17)：代码/离线实验和迁移实践应单独审查，不当作文档迁移就已完成产品能力。

此页为来源索引，不代表每个链接已实时验证、每个参考项目知识已审查完毕或旧知识全部完成迁移。可用[迁移清单](../MIGRATION.json)判断具体状态。
