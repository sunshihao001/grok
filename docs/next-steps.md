# 研发路线 V2｜按证据瓶颈而不是文档数量推进

**当前架构主规范**：[知识体系架构 V2.0](knowledge-architecture-v2.md)。本路线将知识成熟度、产品能力和运行部署分开验收。当前只读/纸面，不涉及实盘。

## P0｜知识架构与检索一致性（本轮）

- [x] 建立 L0–L7 八层知识架构，明确五张图、S0–S7研究阶段、M0–M7产品能力和V4运行循环的区别。
- [x] 24张知识卡：保留15张原卡，新增R005/R006/R007和KX-01–KX-06共9张。
- [x] 对齐30个固定来源指针、14个参考项目/论文、17个专家、12个领域、8个研究阶段、9个场景、40条交接、17个外部方法和8个HX假说。
- [x] 增加跨注册表完整性测试 tests/test_knowledge_architecture.py。
- [ ] 等待本次架构修改的 GitHub Actions CI 完成；成功后再勾选最终验收。
- [ ] 盲测新卡的检索召回和错误引用率；关键词命中不等于语义理解。

## P1｜M1 原始链上事实与经济语义（最高优先级）

**目标**：先能准确回答一笔交易到底发生了什么，而不是先建“庄家分”。

- 定义Canonical Event Ledger的正式Schema：signature、slot、transaction index、instruction path、program/version、account roles、raw units、pre/post balance、source、observed/available/received times。
- 接入一个真实、只读、可回放的Solana来源；明确分页、历史边界、速率限制、延迟、缺失Slot和重试。
- 独立复核R006/R007关键签名：Meteora remove-liquidity、Token CloseAccount/WSOL、直接System Transfer。
- 将System Transfer、Token Transfer、Swap、LP、CloseAccount、fee claim、bridge/program receipt等拆成可组合事件；保留未知事件和余额残差。
- 对BUY/SELL方向做分层抽样的instruction-level核验，形成分类错误表。
- 交付覆盖报告和原始证据引用；不能只给一份漂亮的标准化JSON。

**验收**：随机与重点签名均能从原始RPC复算；SOL/Token整数单位和账户变化可解释；UNKNOWN和缺失明确；不同来源的重复/冲突可追溯。

## P2｜M2增量窗口与M3资产/经济关系图

- 将离线M2聚合器接入经验证的事件账，加入幂等checkpoint、晚到事件修订和断线回放。
- 分开交易数、指令/资产事件数、owner数、Token Account数、资金发送者/接收者数。
- 建立G_event事实图和G_economic两张子图：资产流图与主体假说图独立。
- 实现owner去重、first-funder coverage、公共hub、角色时间线、Token库存和跨Mint重复角色。
- 不以单一连通分量或共享funder强行定义真实主体。

**验收**：同一事件窗口能重放；资产图金额守恒；公共服务商、未知历史和独立机器人反例不会被误归为同控。

## P3｜M4正常机器人生态与异常基准

- 建立未经过当前检测器筛选的发行/事件总体，保留未触发样本。
- 按协议、发行阶段、流动性、热度、钱包活跃度、公共服务商程度和采集覆盖匹配。
- 对资金扇出、same-slot、多通道群体、跨Mint角色复用做null/permutation、时间留出和告警预算对照。
- 对比简单阈值、纯图、条件基准、专家主动反证；报告误报/漏报、覆盖和漂移。
- 不能用R007的40钱包cohort或外部单一研究窗口校准全市场概率。

## P4｜M5市场结构、机制因果与用途评估

- 连接Token权限/开发者、LP/池深、库存、价格冲击、外部需求和生命周期。
- 将异常发现、风险预警、开发者网络监控、市场状态、预测和paper交易分别定义指标。
- 检验自身买单对价格的机械冲击，不能用自己推价解释自己预测准确。
- 只有决策时点、真实报价、成交失败、费用、MEV、容量和退出路径齐备后，才研究paper edge。

## P5｜V4 Grok云端运行与部署验收

- 在实际Grok环境验证Skill加载、只读来源权限、Python运行时、持久存储、任务触发、重试、退出恢复和审计。
- 初期一个只读Monitor + 一个按需Research Manager；17类专家作为能力动态调用。
- 先做影子运行/人工复核，记录延迟、漏数、重复、误报和人工推翻率。
- 用户单独批准前不创建/启用Routine、不发送外部通知、不发布生产规则。

## 完成度不能用这些代替

- 文档/Skill/专家数量；
- CI成功代替真实RPC复算；
- M2候选代替M4异常校准；
- R005/R006/R007派生源表代替原始链上事实；
- 机制假说代替跨期验证；
- 纸面回测峰值代替可成交净收益；
- GitHub分支文件代替Grok云端部署。

**下一条最有价值的工程工作**：建立M1原始事件Schema和一段真实只读RPC回放，优先复核R006/R007中最能区分直接注资、LP释放和账户关闭的签名。M1不成立，后面的图和异常模型就没有可靠地基。
