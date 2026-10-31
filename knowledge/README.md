# Knowledge Base｜知识架构 V2.0

**唯一结构规范**：[知识架构 V2.0](../docs/knowledge-architecture-v2.0.md)。本目录保存可复用领域知识、来源指针、专家映射、机制假说、案例和历史快照；它不是一个已被完整验证的市场真相数据库。

## 1. 当前资产清单

| 资产 | 数量 | 解释 |
|---|---:|---|
| 历史种子卡 `catalog.v1.json` | 15 | 第一批迁移知识，不是全域目录 |
| 历史快照 | 21 | Hermes 重要方法/合同片段，不是完整旧仓迁移 |
| 按需来源索引 `source_index.v1.json` | 30 | 原始来源、代码、工具文档和方法的 pinned pointers |
| 专家能力映射 | 17 | 专业能力，不是 17 个云 Bot |
| 知识领域 | 12 | 当前领域导航分类，允许扩展 |
| 专家交接图 | 40 | 类型化知识/证据交接设计，不是自动工作流 |
| 机制假说 | 8 | 待检验或工程方法提案 |
| 外部方法引用 | 12 | 架构/证据方法来源，不是市场策略证据 |

所有数字均为文件结构统计。是否掌握、是否真实复算、是否可用必须逐条 Claim 评估 K0–K4；参见 [成熟度核查](../docs/knowledge-maturity-and-gaps-v1.md)。

## 2. 五类知识对象

- **领域知识卡**：`catalog.v1.json`。已有 15 张旧知识种子卡；逐步增加 `domain`、`claim_ids`、`maturity`、`failure_modes`、`source_ids`、`supersedes`。
- **来源指针**：`source_index.v1.json`。仅用于按需定位特定仓库/提交/路径；不是实时 API，也不是所有条目已完整阅读。
- **专家能力与交接**：`expert-capability-map.v1.json`（17 专家/12 域/9 场景）和 `expert-interaction-graph.v1.json`（40 条交接边）。
- **机制假说**：`mechanism-synthesis-hypotheses.v1.json`（HX01–HX08），必须含预测、竞争解释、基准、判别证据和 reject_when。
- **研究案例/报告**：`cases/`、`research/`、`../reports/`。必须区分原始 RPC、外部派生数据、合成 fixture、方法参考。

## 3. 当前研究脉络

- [V5 机制发现宪章](../docs/economic-mechanism-discovery-charter-v5.md)：从数据矛盾生成可证伪机制；R007 是派生表复算，不是独立 RPC 确认。
- [V4 双循环架构](../docs/dual-loop-research-runtime-architecture-v4.md)：确定性快循环、预算化慢循环、独立反证回路。
- [专家交互 V2](../docs/knowledge-expert-interconnection-v2.md)：五张图、六类交接、Claim 版本与回溯。
- [专家知识协作 V1](../docs/solana-meme-expert-knowledge-orchestration-v1.md)：领域专家职责、S0–S7 研究阶段和动态路由的历史详细说明。
- [成熟度与能力缺口](../docs/knowledge-maturity-and-gaps-v1.md)：各专业领域的证据成熟度及下一项有效验证。

## 4. 如何调用知识

```bash
PYTHONPATH=src python -m solana_meme_os.knowledge --question "同一批钱包资金同源吗？"
PYTHONPATH=src python -m solana_meme_os.research --question "SOL 流入可能来自哪些程序和经济活动？"
PYTHONPATH=src python -m solana_meme_os.expert_router --event FUNDING_FANOUT --event SAME_SLOT_MULTIWALLET_BUY
PYTHONPATH=src python -m unittest discover -s tests -v
```

这些程序是确定性检索、规划或离线分析入口，不是自动专家推理、RPC 取证或真实交易执行。关键词匹配仅作候选召回；新问题必须允许开放发现，不能被现有 15 张卡或 9 个场景限制。

## 5. 来源升级政策

`reference-project-discovery.v1.json` 是筛选队列；`source_index.v1.json` 是固定版本的按需阅读入口；真实数据连接器是另一个工程对象。三者不得混称。

新来源升级至少完成：仓库/作者/许可证核验 → README/论文 → 具体代码/方法 → 版本锁定 → 可迁移命题和局限 → 原始证据或独立复算计划 → 适当专家和测试映射。不能因 README 提及某能力就标记为已接通。

## 6. 单个知识单元应达到的结构

`id, domain, question, claim_type, mechanism, scope, source_refs, raw_evidence_refs, observed_at, available_at, produced_at, required_fields, competing_explanations, baseline, discriminator, reject_when, maturity, validity_status, depends_on_claim_ids, supersedes, test_refs, owner_expert, next_action`

缺失字段写 UNKNOWN 并说明缺口；不可将缺失当零、平台标签当链上事实、专家重复意见当独立证据。
