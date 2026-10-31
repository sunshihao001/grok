# Grok Bot 分工｜知识架构 V2 与双循环运行

**总目标**：围绕全市场 Solana Meme 事件、资金/库存网络、钱包群体、开发者与市场机制，构建可追溯的只读监控和专家研判。跟单是下游专题。

## 架构分离

- **L0–L7**：知识架构层，见 docs/knowledge-architecture-v2.0.md。
- **S0–S7**：单个 Case 的研究阶段。
- **M0–M7**：最终产品能力和软件模块。
- **17 类专家 / 12 个知识领域 / 40 条交接**：研究能力与交接契约，不是 Bot 数量。
- **V4 双循环**：快循环处理大量事件，慢循环按需形成调查计划，审计回路负责反证/知识治理。

当前目标是**一个只读 Monitor + 一个按需 Research Manager**。六个开发 Bot 是工程责任分组；不要求全部云端常驻。所有实际 Grok Bot 创建、Skill 装载、RPC 权限、持久化和调度仍需在目标环境实测。

## 六个工程责任组

| Bot（设计角色） | 职责 | 需要调用的专家能力 |
|---|---|---|
| 1 Rule & Knowledge Architect | 维护 L0–L7、来源/证据状态、规则版本和发布门槛 | chief、knowledge、review |
| 2 Data & Event Bot | 来源、RPC、指令解码、时间、覆盖、规范事件 | data、chain、event |
| 3 Wallet & Network Bot | 钱包角色、资产图、资金循环、公共hub与跨Mint关系 | wallet、graph、adversarial、inventory |
| 4 Market Mechanism Bot | Token/开发者、微观结构、生命周期、竞争机制和风险 | token、liquidity、regime、causal、risk |
| 5 QA & Falsification Bot | 反例、正常基准、源纠错、claim撤回、独立审查 | review、statistics、chain、data |
| 6 Final Monitor Bot | 只读运行已批准的冻结规则，保留事件/告警/来源状态 | 已批准的知识和确定性模块 |

## 专家能力与实际运行

17 个专家 ID 见 knowledge/expert-capability-map.v1.json；9 个典型研究场景由 expert_router.py 提供静态路由建议。knowledge/expert-interaction-graph.v1.json 有 40 条类型化 handoff，expert_interaction.py 可校验交接并规划 claim 撤回影响；这些都是本地确定性工具，不是实际 Agent-to-Agent 执行。

## 双循环数据通路

- **快循环**：M1 来源/事件（当前未完成）→ M2 规范事件窗口（已有离线输入原型）→候选。
- **慢循环**：research_dispatch.py 根据候选产生限预算 Case 与建议核验项；目前不执行 RPC 或调用真实专家模型。
- **审计回路**：源冲突、分类更正、基准漂移、反例和版本回溯；当前为设计和局部确定性工具。

任何专家交接必须区分原始事实、派生指标、假说、未知和反证。不能将上一个专家的推断包装成下一位专家的原始观察。

## 发布纪律

不访问私钥、不签名、不广播、不下单、不自动激活 Routine、不自动修改生产规则。GitHub 文档/CI成功不代表云端 Bot 已部署。真实 RPC、持续运行、错误恢复和告警误报率需独立验收。见 [知识架构](docs/knowledge-architecture-v2.0.md)、[V4运行架构](docs/dual-loop-research-runtime-architecture-v4.md) 和 [下一步路线](docs/next-steps.md)。
