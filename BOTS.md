# Bot / Agent Roles｜V4 运行架构与研究职责

**原则**：专业能力不等于 Bot 进程。17 个专家是可动态调用的知识学科，不是要求创建 17 个云端 Bot。V4 当前推荐的最小物理运行方式是一个只读 Monitor + 一个按需 Research Manager，外加独立 QA/人工发布边界。六个历史开发 Bot 角色仅作为研发责任分工参考。

## 最小运行角色（目标设计，尚未证明 Grok 云端部署）

| 角色 | 职责 | 权限边界 |
|---|---|---|
| **Final Read-only Monitor** | 执行批准的来源采集与确定性窗口监控，输出来源可追溯的候选/覆盖状态 | 只读；不修改规则、不下单、不调用所有专家逐笔推理 |
| **Research Manager** | 接收用户问题/候选/矛盾，建立有预算 Case，读取专家映射并建议高价值只读取证 | 计划和研究；不伪造 RPC、不自行升级规则 |
| **Independent QA / Review** | 挑战源字段、统计基准、竞争机制和 Claim 依赖；提出撤回/复算影响 | 独立审查；不因主管意见而投票背书 |
| **Human Maintainer** | 审查知识版本、数据连接、阈值、外部告警和任何未来权限变更 | 唯一发布/授权门禁 |

## 17 个专家能力（不是 17 个 Bot）

由 `knowledge/expert-capability-map.v1.json` 定义：chief、data、chain、event、wallet、graph、adversarial、statistics、token、liquidity、inventory、regime、causal、risk、execution、review、knowledge。12 个知识领域和 40 条类型化交接边见 [知识架构 V2.0](docs/knowledge-architecture-v2.0.md) 与 [专家交互图](knowledge/expert-interaction-graph.v1.json)。

研究任务按事件类型、问题、缺失字段和可判别机制动态选择专家；至少区分提出机制者与独立挑战者。专家交接是 Claim Packet/证据请求，不是“多数专家投票”。

## 历史六个研发职责（兼容，不代表云端需创建）

1. Knowledge & Rule Architect：知识本体、来源/Claim、机制假说与规则治理。
2. Data & Event Engineer：RPC/供应商字段、时间、单位、事件正规化与覆盖。
3. Wallet & Capital Graph Research：角色、资金、库存和主体假说图。
4. Market Mechanism Research：Token、流动性、微观结构、阶段与竞争机制。
5. QA & Falsification：正常对照、负样本、误报、反证和依赖撤回。
6. Final Monitor：最终只读运行入口。

## 实际代码能力

- `expert_router.py`：专家知识面板的确定性选择。
- `expert_interaction.py`：类型化交接合同和 Claim 撤回影响计划。
- `research_dispatch.py`：有限 Case/签名调查计划。
- `mechanism_discovery.py`：指定派生源表中的矛盾/机制调查入口。
- `market_observatory.py`：外部规范化事件的 M2 聚合。
- `monitor.py`：独立的单 Mint 快照差分。

以上不是自动多 Agent 执行、真实 RPC 连接、持久 Claim 数据库或云端 Bot 部署。参见 [V4 ADR](docs/dual-loop-research-runtime-architecture-v4.md)、[知识架构 V2](docs/knowledge-architecture-v2.0.md)。
