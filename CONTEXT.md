# CONTEXT｜知识架构 V2.0 与项目研究上下文

本项目当前的研究主线为 **V5 经济机制生成、跨领域认知合成与主动反证**；运行组织采用 **V4 事件驱动快慢双循环 + 独立反证回路**。知识层级、研究阶段、软件模块、专家能力和成熟度是不同坐标轴，统一定义见 [知识架构 V2.0](docs/knowledge-architecture-v2.0.md)。

## 核心目标

从真实 Solana 事件还原交易/指令/账户/资产变化，建立钱包群体与经济行为片段，比较公共基础设施、独立机器人、共同市场刺激、共享资金和疑似同控等竞争解释；以正常基准、反事实和高判别价值原始证据修正机制；只有独立验证后才评价风险、预测和纸面净经济价值。跟单仅是应用分支。

## 当前知识资产

- 12 个知识领域、17 个专家能力、40 条类型化交接边；
- 15 张历史种子卡、21 个 Hermes 快照、30 条按需来源指针；
- 8 个待验证/工程方法假说，R001–R007 专题研究；
- V5 机制研究宪章、V4 快慢循环 ADR、V2 专家交互图。

以上是可追溯的设计和研究资产，不等于所有领域 K3/K4，更不等于已部署的多 Agent。按单个命题标注 K0–K4，定义见 V2.0。

## 五张图必须分开

1. `G_event`：链上事实与来源。
2. `G_economic`：资产流与经济主体假说，未知可保留。
3. `G_knowledge`：命题、机制、竞争解释和反证。
4. `G_expert`：专家交接、来源血缘与 Claim 依赖。
5. `G_decision`：异常、风险、预测与纸面经济价值的不同状态。

## 五种结构轴不可混淆

- L0–L7：知识资产层级；
- S0–S7：每个研究 Case 的证据推进阶段，可跳转/回溯；
- M1/M2 等：软件组件及其输入输出；
- V4：快循环、慢循环、反证回路的运行组织；
- K0–K4：单个 Claim/方法的证据成熟度。

17 个专家是专业能力，不是 17 个 Bot。初期物理运行建议一个只读 Monitor 和一个按需 Research Manager；目标 Grok 环境是否支持实际技能调用仍须实测。

## 当前代码事实

`market_observatory.py` 对已规范化事件做窗口聚合；`research_dispatch.py` 输出有限调查计划；`expert_router.py` 和 `expert_interaction.py` 做确定性路由/交接合同检查；`mechanism_discovery.py` 对指定源表做矛盾筛查；`monitor.py` 是独立的单 Mint 快照流程；`position_audit.py` 是外部派生表差额审计。完整边界和缺口见 V2.0、V4、V5 文档。

**安全边界**：只读/纸面；不读取私钥、不签名、不广播、不下单、不自行启用 Routine。未知不是零；同 Slot 不是 Jito Bundle；资产边不是受益人身份；离线测试不是外部效度。

## 主要入口

- [知识架构 V2.0](docs/knowledge-architecture-v2.0.md)
- [V5 机制发现宪章](docs/economic-mechanism-discovery-charter-v5.md)
- [V4 双循环运行架构](docs/dual-loop-research-runtime-architecture-v4.md)
- [专家交互 V2](docs/knowledge-expert-interconnection-v2.md)
- [知识成熟度和能力缺口](docs/knowledge-maturity-and-gaps-v1.md)
- [下一阶段工作](docs/next-steps.md)
