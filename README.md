# Solana Meme Market Intelligence OS — Grok Edition

**项目目标**：从真实 Solana 链上事件重构钱包群体、资金/库存路径和市场行为，提出竞争性经济机制，以正常基准和主动反证识别风险与可验证的监控价值。跟单是下游应用之一，不是系统本体。

**知识体系唯一层级规范**：[Solana Meme 知识架构 V2.0](docs/knowledge-architecture-v2.0.md)。它统一 L0–L7 知识层级，并严格区分 S0–S7 研究阶段、M1/M2 软件模块、V4 快慢双循环、17 专家能力及 K0–K4 成熟度。不要把它们混为一条流水线。

## 建议阅读顺序

1. [知识架构 V2.0](docs/knowledge-architecture-v2.0.md) — 全部知识资产、层级和下一步缺口。
2. [V5 机制发现宪章](docs/economic-mechanism-discovery-charter-v5.md) — 如何从事实矛盾产生新机制与主动反证。
3. [V4 双循环运行架构](docs/dual-loop-research-runtime-architecture-v4.md) — 快速监控、预算化深研和证据回溯如何分工。
4. [专家交互 V2](docs/knowledge-expert-interconnection-v2.md) 与 [17 专家映射](knowledge/expert-capability-map.v1.json) — 任务如何动态选择专业知识。
5. [知识成熟度与缺口](docs/knowledge-maturity-and-gaps-v1.md) — 哪些结论仍只是方法、哪些已复算、哪些仍缺真实数据。
6. [Skill 入口](skills/README.md)、[来源登记](docs/sources.md) 和 [开发路线](docs/next-steps.md)。

## 当前知识资产（不是完成度）

| 资产 | 当前数量 |
|---|---:|
| 历史概念卡 | 15 |
| Hermes 历史快照 | 21 |
| 按需来源指针 | 30 |
| 专家能力 | 17 |
| 知识领域 | 12 |
| 专家交接边 | 40 |
| 机制假说登记 | 8 |
| 外部方法引用 | 12 |

这些数量描述仓库结构，不代表全部已精读、已独立验证或已部署。具体成熟度必须按单个 Claim 评价。

## 当前代码边界

- `market_observatory.py`：对外部已规范化事件做窗口/群体候选聚合，不是全链采集器。
- `research_dispatch.py`：把 M2 候选组织成有限只读调查计划，不执行 RPC/专家或通知。
- `expert_router.py` / `expert_interaction.py`：确定性专家知识路由和类型化交接检查，不会启动 17 个 Agent。
- `mechanism_discovery.py`：对指定源表发现标签/金额/历史覆盖矛盾，不是链上真值证明。
- `monitor.py`：单 Mint 快照监控，和 M2 事件输入合同不同。
- `position_audit.py`：审计外部派生表的仓位数量差额，不等于经济仓位闭环。

**运行边界**：只读/纸面研究，不读取私钥、不签名、不广播、不下单。GitHub 文件不等于 Grok 云端部署。主分支不因本轮整理而改变。

## 离线检查

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

离线测试成功只说明测试覆盖到的代码路径通过；不代表真实 RPC 完整性、市场总体异常率、纸面净收益或云端运行通过。
