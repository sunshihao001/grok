# Knowledge Base｜知识资产、来源路由与研究成熟度

**唯一知识架构入口**：[知识体系架构 V2.0](../docs/knowledge-architecture-v2.0.md)；机器可读索引：[architecture.v2.json](architecture.v2.json)。

本知识库服务 Solana Meme 全市场事件、钱包行为、资金/库存网络、开发者、市场结构、正常基准、机制研究和风险研判。跟单只是一个专项应用。

## 当前资产清单（2026-10-31）

| 资产 | 数量 | 用途 |
|---|---:|---|
| 常驻知识卡 | **24** | 原15张历史卡 + R005/R006/R007 与 KX-01–KX-06 的9张新增卡 |
| 历史快照 | **21** | 原 Hermes 知识与设计合同；不包含旧 runtime |
| 固定来源文件指针 | **30** | 8个仓库中的文件级commit/path；不是实时数据源 |
| 参考项目/论文目录 | **14** | 来源成熟度和采用边界；部分仅读 README/元数据或公开文档 |
| 外部方法出处 | **17** | Solana/Jito、流式处理、数据血缘、Agent、统计/因果方法 |
| 专家能力 | **17** | 研究纪律与交付契约，不是17个Bot |
| 专业领域 | **12** | 跨层知识分区 |
| 研究阶段 | **8（S0–S7）** | 单个Case的开放研究流程 |
| 典型场景路由 | **9** | 专家能力组合，不是封闭的事件字典 |
| 专家交接 | **40（L01–L40）** | 类型化证据交接和反证路径 |
| 机制假说 | **8（HX01–HX08）** | 研究候选，不是已验证市场规律 |
| 研究单元 | **7** | R001、R001B、R002、R003、R005、R006、R007；当前无R004文件 |

## 知识如何组织

- **L0–L7**：知识依赖层，从治理边界、本体、事实证据、行为结构、统计基准、经济机制、用途效力到知识治理。
- **G_event / G_economic / G_knowledge / G_expert / G_decision**：五张不同用途的图；不能把钱包资产流、同控假说和claim依赖混成一个图。
- **S0–S7**：研究阶段；可并行、跳转和回溯。
- **M0–M7**：产品能力；多数仍是目标能力，不代表代码已实现。
- **V5**：机制生成和主动反证方法；**V4**：快慢双循环运行组织。
- 17专家是研究能力；一个专家可以由知识卡、来源、算法和QA方法共同构成，不要求一人/一Bot。

## 重要文件

- [知识卡目录](catalog.v1.json)：每张卡有触发、机制、必需证据、竞争解释、推断边界、下一步和固定来源。
- [来源索引](source_index.v1.json)：按需读取30个固定版本文件；只允许已审查仓库。
- [来源索引说明](source-index-README.md)：来源类型、路由方法和覆盖边界。
- [12领域本体](domain-ontology.v1.json)：定义各领域的层级归属、核心对象/问题、必需证据、输出、反推边界、专家面板和主知识卡。\n- [专家能力映射](expert-capability-map.v1.json)：17专家、12领域路由投影、8研究阶段、9场景路由。
- [专家交接图](expert-interaction-graph.v1.json)：40条方向性关系、claim contract、反证/撤回约束。
- [机制假说登记](mechanism-synthesis-hypotheses.v1.json)：HX01–HX08，含预测、竞争解释、判别证据和拒绝条件。
- [参考项目发现](reference-project-discovery.v1.json)：14个来源项目/论文及成熟度分级。
- [外部方法来源](external-method-sources.v1.json)：17个架构/方法参考及其支持边界。
- [研究案例](research/)：保留R001–R003与R005–R007；[R002专家交叉反证](cases/R002-expert-cross-examination-v1.md) 是案例格式示范。
- [历史快照审计](legacy-audit.md) 与 [快照清单](legacy-snapshots/README.md)：保留历史知识，隔离无证据快捷推断。

## 研究报告与知识卡的区别

研究报告保存特定样本、原始来源、计算过程、限制和结论；知识卡提炼跨案例可迁移的机制和检查方法。报告不会自动成为知识卡，更不会自动成为生产规则。本轮新增9张卡的目标是让 R005/R006/R007 与六项 KX 研究成果可被常规知识路由发现。

## 研究/执行工具的真实边界

- knowledge.py：24张卡的关键词检索；不理解未被词面覆盖的新语义。
- research.py：固定来源指针检索；不是RPC接入器或实时数据服务。
- expert_router.py：专家/知识路由建议；不调用真实Agent。
- expert_interaction.py：交接图检查和claim撤回影响规划；没有持久claim数据库。
- research_dispatch.py：根据M2报告产生限预算研究计划；不执行RPC。
- mechanism_discovery.py / cashflow_semantics.py：对指定派生源表进行确定性审计；不证明原始链上事实。

## 证据与成熟度纪律

- 来源主张 ≠ 来源派生数据 ≠ 原始RPC事实。
- 资产边 ≠ 主体控制；观察候选 ≠ 统计异常；机制支持 ≠ 交易收益。
- UNKNOWN、历史缺口、查询失败和未扫描必须分开保存。
- 知识成熟度按单个命题/用途评估：K0主题发现、K1原文审阅、K2可检验协议、K3独立原始数据复算、K4跨期/样本外验证。不同用途（监控、风险、预测、纸面经济）在K4内分别设独立指标，不额外把K5/K6混入当前卡片成熟度字段。
- 当前许多专题处于K1–K2；真实RPC复算、正常总体和用途验证仍是主要缺口。

## 命令

```bash
PYTHONPATH=src python -m solana_meme_os.knowledge --question "历史覆盖不足能否证明钱包独立？"
PYTHONPATH=src python -m solana_meme_os.research --question "CloseAccount导致SOL流入时如何分解资金来源？"
PYTHONPATH=src python -m solana_meme_os.expert_router --event FUNDING_FANOUT --question "是否为公共服务商？"
PYTHONPATH=src python -m unittest discover -s tests -v
```

以上是离线检索/测试入口，不是云端部署或实盘能力。
