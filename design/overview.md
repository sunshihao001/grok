# Design Overview｜Solana Meme Market Intelligence OS

本项目已经从单币 GMGN/跟单工作流，调整为**全市场链上事件的多尺度监控与专家研判**。旧 Hermes 七个业务 Skill 作为知识储备保留，不作为唯一运行时的固定七段管线。

## 系统通路（目标状态，不等于已部署）

```text
M0 来源发现：发行/迁移/交易/钱包/池子/跨 Mint 事件
   ↓
M1 正规化事件账：signature、Slot、instruction、资产单位、来源与时点
   ↓
M2 时间窗/群体监控：钱包数、转账数、买卖规模、时间集中、资金注入
   ↓
M3 资产图与主体假说图：资金、Token 库存、重复行为；共享 hub 反证
   ↓
M4 正常/异常基准：同类发行/流动性/阶段，控制公共事件和样本选择
   ↓
M5 市场结构：筹码、池深、价格、生命周期、流动性与风险演变
   ↓
M6 机会研究：预测、执行、退出及净成本的独立 paper-only 检验
   ↓
M7 解释与记录：事件摘要、证据链、未知、反例、审计与知识迭代
```

**先事实、后异常、再机制和机会**。同 Slot 是观察，不是直接确认 Jito Bundle；共同资金源是关系，不是同一受益人身份；后验钱包收益不是事前预测力。

## 真实代码与设计的区别

| 已有实现 | 当前输入与输出 | 不具备 |
|---|---|---|
| `monitor.py` | 已标准化单 Mint 观测 JSON→流动性/持仓差分及事件日志 | 多 Mint 链上行为聚类 |
| `market_observatory.py` | 已归一化多事件→窗口计数、same-slot、fanout、汇集与资金到买入候选 | 自行抓 RPC、真实 Bundle 识别、正常模型 |
| `position_audit.py` | 两个历史派生来源表→Token 口径差额 | 完整经济仓位/净利润 |
| `knowledge.py`/`research.py` | 已有概念与来源索引→研究线索 | 专家推理和原始交易验证 |

任何实验阈值、窗口参数与输出状态都需要和实际源验证，无法从 fixture 推断市场效力。

## 旧技能在新系统的位置

Hermes 的 candidate-entry 与 token-panel 是数据发现和检查；wallet-roles/structure 是 M2/M3；evidence-chain 是 M4/M7；trade-gate 是独立的 M6；controller 是编排思想，**不能把原 Hermes runtime 拷入 Grok**。meme- 的 FCZ 和策略知识放进 M5/M6 假设研究；QB/OKX 放进数据适配层；Why 项目是取证/反证方法来源。

## 阶段划分（避免虚假的“已经完成”）

- **P0 结构对齐**：文档、术语、来源、Skill、职责和权限一致；本分支目标。
- **P1 可信事件输入与离线窗口重放**：真实来源的指令/转账，覆盖、时点、单位、去重；基础聚合器及反例测试。
- **P2 资金图、正常基准与跨币关联**：在 P1 事实完整的基础上评估协调候选误报。
- **P3 市场状态与风险/纸面机会研究**：验证预测是否独立存在，区分风险预警与净经济可行性。
- **P4 Grok 云运行与审查**：云 Bot 实际加载、源权限、告警、失败恢复、例行任务测试及人工冻结。

真实交易在当前范围外；自动/半自动交易未授权。

见 [知识系统整合](../docs/knowledge-system-integration-v1.md)、[研发路线](../docs/next-steps.md)、[全市场监控定位](../docs/solana-meme-marketwide-monitoring-scope-v1.md)。
