## V4｜确定性监控与动态研究的运行边界

采用 [双循环架构 V4](docs/dual-loop-research-runtime-architecture-v4.md)：快循环维护原始事件与监控事实（目前仅 M2 已归一化外部输入），慢循环按候选的**Mint+Slot / 来源+时间窗 / 跨 Mint 汇总 / 钱包级事件**生成限预算调查 Case，并由研究总师按需调用现有专家知识。新 `research_dispatch.py` 使用 `expert_router.py` 的专业角色与交接约束，但只输出调度**计划**，不运行真实专家、RPC、交易或对外告警。

一个市场现象可以同时拥有不同案例与竞争假设；共享签名不等于同控，但后续研究可复用该签名的核查证据。规则升级、源错误撤回、正常基准变动在研发/QA/人工审核回路处理，不由 Monitor Bot 自己热改生产规则。

# CONTEXT｜Solana Meme 全市场监控与机制研判

## 目标和边界

这不是以 GMGN 候选 Token 或钱包跟单为中心的七段脚本。研究对象包括全市场多个 Mint、交易/指令、钱包、Token Account、资金网络、时间窗和价格/流动性结构。目标是从可观察事件发现**正常与异常行为的差异、可能的协调与经济机制、风险及经过验证的机会**。跟单、开发者跟踪、风险预警和纸面交易均为具体应用。

只读/paper-only；不签名、不广播、不接管私钥或执行真实交易。当前 Grok 云端 Bot 未验证部署。

## 关键术语

- **Event / 事件**：保留 signature、Slot、instruction、地址/资产、数量、时间与来源的不可混同观察；余额减少不自动叫 SELL。
- **Window / 时间窗**：按 Mint/协议/全市场的明确范围聚合不同地址、交易和 SOL/Token 量，不以事后涨价选择观察起点。
- **Wallet / 地址**：链上账户或 owner；不自动等于自然人或最终受益者。Token Account 与 owner 必须分开。
- **Asset Graph / 资产图**：有签名支持的 SOL/Token 转移、Swap、LP 变化；资产边不自动等于控制关系。
- **Entity Hypothesis Graph / 主体假设图**：同控、共享服务商、独立机器人、共同公开事件等可竞争推断。
- **Coordinated Candidate / 协调候选**：基于时序、资金与重复性提出的机制假设；未经适当证据不能称确认的 Jito Bundle/庄家。
- **Normal Baseline / 正常基准**：同市场阶段、发行年龄、流动性、热度、活动水平下的比较人群与分母，缺失不得标“异常”。
- **Observed / Available / Received / Decision Time**：事件在链上发生、数据首次可得、系统实际收到、研究做出判断的时间；事后标签不能倒灌为实时特征。
- **Risk vs Trade Value**：行为异常、风险信号、未来预测和净执行收益必须分开评价。

## 专家协作与层级的正确理解

研究知识层、软件模块 M0–M7、Grok 开发 Bot 是三种不同对象。当前 [专家知识架构](docs/solana-meme-expert-knowledge-orchestration-v1.md) 以 17 类能力覆盖来源事实、经济主体、协同对照、市场状态、风险/执行和反证，并按实际事件动态召集；旧 Hermes 八层只作为历史职业分工参考，不应让未确认的实体归并阻断独立市场研究，也不能强迫将未知库存划归已知实体。

静态专家映射见 [`knowledge/expert-capability-map.v1.json`](knowledge/expert-capability-map.v1.json)；它尚不是 Grok 实际 Bot 调度代码。

## 模块语义

M0 市场采集 → M1 事件账 → M2 群体时间窗 → M3 资金/库存图 → M4 条件基准与反证 → M5 市场状态 → M6 风险/纸面机会 → M7 告警与复盘。

以上是**建设目标**，不是所有模块已实现。现有 `monitor.py` 为单 Mint 快照；`market_observatory.py` 接受外部归一化事件做聚合与候选识别；`position_audit.py` 是仓位统计一致性工具。数据接入、完整异常识别、真实 Grok Bot 均尚未完成。

## 历史兼容

原 Hermes 七个业务 Skill：candidate-entry、token-panel、wallet-roles、wallet-structure、evidence-chain、trade-gate、workflow-controller，属于**可迁移的研究与证据领域能力**，不再作为必须按顺序运行的系统总管线。旧 GMGN 原型也只是候选数据源。历史 `BLOCK/WATCH/PAPER_ONLY/NEED_MORE_DATA` 属旧决策语言；当前全局监控需要分别报告观察、待查、风险和纸面评价资格，生产规则没有自动改变。

请优先阅读 [总整合蓝图](docs/knowledge-system-integration-v1.md)、[Skill 入口](skills/README.md)、[Bot 职责](BOTS.md) 和 [来源](docs/sources.md)。
