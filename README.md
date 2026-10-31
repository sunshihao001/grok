# Solana Meme Market Intelligence OS — Grok Edition

**项目目标**：从全市场 Solana 链上事件重构钱包群体与资产行为，复原资金/库存/开发者关系，建立条件正常基准与竞争经济机制，再将经过验证的发现转化为市场监控、风险研判和独立的纸面交易研究能力。跟单只是一个下游专题。

**当前状态**：研究与工程草案；只读/纸面。GitHub 文档、离线代码和 CI 不代表实时全市场覆盖、Grok 云端部署或交易收益已经成立。

## 从这里开始

1. **[知识体系架构 V2.0](docs/knowledge-architecture-v2.0.md)** — 唯一总入口：L0–L7 知识层、五张图、S0–S7 研究阶段、M0–M7 产品能力，以及当前知识资产盘点。
2. **[机器可读架构索引](knowledge/architecture.v2.json)** — 机器可核对的层级、模块状态和资产数量。
3. **[V5 经济机制研究宪章](docs/economic-mechanism-discovery-charter-v5.md)** — 从事实矛盾生成新机制、竞争解释和主动反证。
4. **[V4 快慢双循环运行架构](docs/dual-loop-research-runtime-architecture-v4.md)** — 快速确定性监控、预算化深研与独立审计回路。
5. **[17 专家/12 领域映射](knowledge/expert-capability-map.v1.json)**、[40 条专家交接图](knowledge/expert-interaction-graph.v1.json)。
6. **[知识成熟度与缺口](docs/knowledge-maturity-and-gaps-v1.md)**、[开发路线](docs/next-steps.md)、[来源审计](docs/sources.md)。

## 当前知识资产

- 24 张可检索知识卡：原有 15 张 + 本轮将 R005/R006/R007 与 KX-01–KX-06 转成 9 张来源绑定卡。
- 30 个固定版本文件级来源指针，覆盖 8 个仓库；另有 14 个参考项目/论文的成熟度目录，二者不是同一口径。
- 17 类专家能力、12 个知识领域、8 个研究阶段、9 个典型场景路由、40 条专家交接。
- 8 个待检验机制假说 HX01–HX08；21 份历史知识快照。
- 7 份研究单元：R001、R001B、R002、R003、R005、R006、R007；当前仓库没有 R004 文档。

这些数量代表资产登记规模，不代表掌握深度或市场验证程度。

## 当前已有程序能力（局部实现，不等于端到端系统）

| 模块 | 当前作用 | 核心限制 |
|---|---|---|
| monitor.py | 单 Mint 规范化快照差分 | 不是全市场钱包扫描 |
| market_observatory.py | 已归一化事件的时间窗/群体候选聚合 | 没有原始 RPC 采集与正常基准 |
| position_audit.py | 历史派生仓位表口径审计 | 不证明经济仓位闭合或利润 |
| cashflow_semantics.py | 审计派生 SOL 流入标签和历史覆盖 | 不解码真实 RPC |
| funder_evidence.py | 保留未知/公共 Hub/启发式 first-funder 状态 | 输入必须已规范化 |
| mechanism_discovery.py | 从派生源表发现次数/金额反转与覆盖张力 | 不是全市场异常检测 |
| knowledge.py / research.py | 知识卡与来源指针检索 | 确定性路由，不是深度推理 |
| expert_router.py / expert_interaction.py | 专家路由建议、交接校验与撤回影响规划 | 不运行多 Agent |
| research_dispatch.py | 对 M2 结果生成限预算研究计划 | 不执行 RPC 或专家模型 |

## 离线检查

Python 3.12 环境：

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m solana_meme_os.knowledge --question "LP撤出与SOL流入的经济语义"
PYTHONPATH=src python -m solana_meme_os.expert_router --event FUNDING_FANOUT --question "是否存在公共资金基础设施？"
```

所有 fixture 均为合成数据。测试成功只证明代码合同和回归，不证明真实链上数据准确性。

## 核心边界

- 同 Slot ≠ Jito Bundle；Token Transfer ≠ Swap；余额差 ≠ 资金来源/受益人。
- 行为候选、统计异常、经济同控、市场风险、预测价值和净交易收益分别验证。
- 不访问私钥、不签名、不广播、不下单，不自动部署 Bot/Routine。
- 研发 Bot、17 类专家和目标运行入口是不同层级；初期只需要一个只读 Monitor + 一个按需 Research Manager。
