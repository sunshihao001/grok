# Blix × AI 工作台｜多层锚点与跨层变更影响映射 V0.1

2026-11-13｜范围：**现有Blix产品＋PR #23只读AI扩展的少量高价值真实锚点**。来源：本分支源代码、现存合成测试与现有知识文档。**状态：ANCHOR_MAP_SOURCE_CHECKED；不是自动监控、全网链上实跑、已验证市场Alpha或新锚点运行框架。**

通用方法的唯一维护入口：[ai-d项目多层锚点与跨层一致性](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md)。本文件只为Blix指向**已存在目标、原知识、原代码与实际测试**，不重复搭一个专业本体，不新增代码与约束基础设施。

## 0. 怎样避免以前“有目标，但局部开发仍然偏离”

项目已确认六项业务结果O1–O6，以及“**实际可参与机会优先，专业资金调查为证据支撑；完整保留原版Blix；AI只读研究而不执行交易**”。本映射只给这些目标加**跨层可追查的实现与验收关系**：

目标 → 业务必须成立的结果 → 原始来源/知识主张 → 数据/设计条件 → 关键代码 → 正反测试 → 真实运行未解问题 → 新事实触发修正。

不把这一串当每个Mint必须严格走的操作流水线。一个实际研究可以从原始钱包、Mint、市场、跨币事件任意入口开始，按需要加载直接相关锚点。一个锚点不能因为界面显示了内容或合成测试绿色就提升为“整个业务完成”。

## 1. 已核对源码的七条优先锚点（稳定编号用于链接，不等于代码规范强制）

| ID / 性质 | 核心主张及上游目标 | 当前承载位置 | 检验与仍然欠缺的部分 |
|---|---|---|---|
| **BLX-G-OPPORTUNITY** 稳定目标 | 实际交易机会优先；深度调查并非直接买卖信号。O1–O6不因某个新功能而替代 | [目标](goal-map.md)、[总蓝图V2](blix-ai-workbench-master-plan-v1-20261113.md) | 有交易时效/价格/退出数据才能评估真实可参与性；**实际市场增益未验** |
| **BLX-D-PULSE-FRESHNESS** 数据语义，条件约束 | Pulse浏览器发出的有限候选、客户端发送时刻不能代表全市场覆盖/源头最早可见。关联O1、O5 | [Pulse候选代码](../../server/intelligence/pulse-discovery.mjs)、[来源前置审查](six-business-outcomes-dependency-audit-20261113.md) | [Pulse模拟反例](../../test/pulse-ai-discovery.test.mjs)检查最多12候选、输入/覆盖边界；**真实源Universe、provider firstAvailable、召回率未知** |
| **BLX-K-OWNER-IDENTITY** 专业事实与数据边界 | Token Account、Owner、公共Pool/Vault、资金出资和实际控制者不得混为一谈。关联O2–O4 | [钱包角色知识](../../knowledge/mechanisms/wallet-roles-and-inventory.md)、[RPC原始证据解析](../../server/economic-events.mjs) | [钱包证据与身份测试](../../test/wallet-evidence-chain.test.mjs)、[wallet identity](../../test/wallet-identity.test.mjs)含局部规则，**对全部真实账户控制人的识别未验** |
| **BLX-K-INVENTORY-PROVENANCE** 推论边界/代码不变量候选 | 转入Token与接收者后续本地卖出摘要不证明该批Token被卖出，也不证明成本基础。关联O2–O4、O5 | [钱包库存知识](../../knowledge/mechanisms/wallet-roles-and-inventory.md)、[claim trace](../../server/intelligence/economic-claim-trace.mjs)、[continuation](../../server/intelligence/investigation-continuation.mjs) | [claim trace离线测试](../../test/economic-claim-trace.test.mjs)将转账事实与卖出摘要分开；**未重建完整真实库存批次和成本** |
| **BLX-T-FOLLOWABILITY** 测量与商业主张边界 | 历史涨幅、链事件时间和行情观察不等于当时可执行交易；要有先可得信号、入出场报价、成本和可退出性。关联O1、O5 | [策略知识](../../knowledge/mechanisms/strategy-and-execution-economics.md)、[纸面收据验证器](../../server/intelligence/followability-replay.mjs) | [跟随性反例测试](../../test/followability-replay.test.mjs)检验未来函数/报价过时/退出缺失/费用不完整；**真实路由、价格、失败成交和前瞻收益未验证** |
| **BLX-C-READONLY** 用户授权/工程硬边界 | 独立AI只读服务不应将模型产生的文本转成任意SQL/RPC/签名/支付；只查显式选定Mint与已存在本地档案。关联所有业务结果 | [研究服务](../../server/intelligence/research-http.mjs)、[经济只读工具](../../server/intelligence/mint-economic-evidence.mjs)、[本机使用说明](ai-readonly-local-workbench.md) | [HTTP/安全测试](../../test/intelligence-workbench-http.test.mjs)、[本地源完整性测试](../../test/intelligence-source-readiness.test.mjs)；**真实远端鉴权/模型供应商成本与生产运维未验** |
| **BLX-P-ORIGINAL-PRESERVATION** 稳定产品约束 | AI扩展不能把原Blix市场、账户、交易、Wallet、Coin页面删除或无意重写；保留交易模块不意味着准许运行。关联全部业务 | [产品总图](blix-ai-workbench-master-plan-v1-20261113.md)、[现存守护测试](../../test/original-blix-preservation.test.mjs) | 原版关键路径和文件指纹的静态回归已配置；**实际真实部署兼容性与生产UI尚未验** |

**这七项是初始审阅样例，不能推导全部设计风险已有锚点**。第八个重要空白应公开保留：**BLX-R-CONTINUOUS-REVISION / 尚未实现**——现有[调查继续状态](../../server/intelligence/investigation-continuation.mjs)输出NOT_RUNNING_NO_AUTONOMOUS_WATCHER，不能把报告中的“持续观察”当自动Case和增量修订已跑通。它对应O6的计划锚点，后续需事件水位、案件状态、重审和重复回填反例。

## 2. 示范一：从“钱包同批库存”专业知识追到代码和测试

**上游语义**：钱包B收到A的Token，之后B发生卖出，不证明B卖出的就是从A刚收到的那批Token。若B原有库存或中途买卖，缺完整历史时成本与批次是UNKNOWN。

- 目标：O3资金库存还原、O4跨Mint解释的经济可信度，最终O5机会评价不能用虚构成本；
- 主知识：wallet-roles-and-inventory中的库存、地址/Owner、交易阶段与反证；必要时补经济事件原始签名；
- 来源/数据：已捕获RPC指令身份和原始JSON Hash、局部wallet_trades摘要；不能代替任意钱包全生命周期；
- 代码实际状态：economic-claim-trace明确输出本地卖出摘要，且反复声明其不能确认转入批次；investigation-continuation明确cost_basis_unknown；
- 测试实际状态：economic-claim-trace.test覆盖归档RPC收据与本地卖出摘要类型分开；目前尚不是完整库存守恒/同批售出实证测试；
- 若某人修改输出文本为“确认接收方出售转入筹码”：必须回查此锚点→该report字段→UI消费者→新增正负库存反例→真实交易原文补查，而非只改文案或让模型猜。

这意味着“有知识锚点”不仅是代码旁的评论，还必须保证**代码可观察输出和测试强度与知识主张一致**。现有claim trace实现属于局部锚定，不能冒充完成全链对账。

## 3. 示范二：数据首次可见时间的影响传播

**问题**：如果把browserRecordedAtMs或本地first_seen当provider最早可见时间，会同时扭曲市场发现的及时性、AI筛选结果、历史跟单回测与“早知道”的盈利假设。

影响范围（已知直接路径和需核消费者分开）：
- 来源：浏览器Pulse截面、原Blix数据库first_seen；**当前并未统一验证provider firstAvailable**；
- 代码：pulse-discovery.mjs的sourceFreshness、marketCoverage状态保持局部来源限定；
- 现有测试：pulse-ai-discovery.test确保限定样本语义，followability-replay.test拒绝无效先可得信号；
- 用户输出：不得称全市场自主发现，不得用事后价格算当时盈利；
- 下一次真实验收：指定一枚Mint和观测窗口，从WS/provider接收、原版持久记录直到模型可见时刻建立**实际时点链**；若来源本身没有可信最早时间，则继续UNKNOWN，不虚构。

如后续增加一个权威providerReceivedAt字段，需审查是否新加字段、是否替换旧含义、是否影响缓存/回放/策略对照。字段名相同但语义改变也属于需要回查的契约变更。

## 4. 当某个文件改变时，实际怎样用这份锚点

| 发生变化 | 先查锚点 | 应立即核实的下游 | 不能自动推出的结论 |
|---|---|---|---|
| Pulse候选筛选或数据字段变动 | BLX-D-PULSE-FRESHNESS | 采样范围、源时间、候选被拒记录、UI与followability信号时点；相关测试 | 新算法更早发现全市场机会 |
| RPC解析/Owner匹配逻辑变动 | BLX-K-OWNER-IDENTITY、BLX-K-INVENTORY-PROVENANCE | 指令身份、Owner冲突、公共Pool排除、经济网络、claim trace和相关反例 | 关联地址代表共同操盘者 |
| economic-claim-trace输出变化 | BLX-K-INVENTORY-PROVENANCE | 证据引用/可核签名、局部sell摘要、知识提示与UI术语、测试 | 已证明库存批次来源 |
| 纸面盈利计算/行情接口变化 | BLX-T-FOLLOWABILITY | 信号最早可见、quote时效、入出费用、退出、历史样本资格 | 真实可跟单净利润 |
| AI sidecar权限或模型提供商改变 | BLX-C-READONLY、BLX-P-ORIGINAL-PRESERVATION | 外部访问、费用、参数白名单、原版交易模块无导入、回归与回滚 | localhost单机测试可直接上线公网 |
| Case/监听功能提案或变更 | BLX-R-CONTINUOUS-REVISION | 增量水位、相同交易去重、历史回填、模型重新解释成本、通知授权 | 具有历史快照就等于持续监控 |

分类方法：确有代码调用/数据流证据 → DIRECT_IMPACT；基于专业机制推断的关联 → REVIEW_CANDIDATE；没有证据 → UNKNOWN_NOT_MAPPED。不要单靠同名术语生成数百条伪依赖。

## 5. 应先实施还是先继续画锚点？

**不为本轮在仓库内增设ANCHOR引擎、额外数据表、独立Agent、标签扫描/CI检查**。优先把真实研发中的一个修复请求当试验，看“比只读当前文件”是否少了关键遗漏、是否提前阻止错误语义；再由真实效果决定是否需要结构化ID或自动静态检查。

在代码中可少量注释指向某条最重要的知识/数据锚点，但注释本身不能强制行为。对于安全边界或重要经济不变量，必须继续用**源码限制、可自动执行的负例测试和真实业务收据**来担保。

下一项有实际信息价值的工作仍是已登记的R0/R1：在可授权的现有Blix数据副本上选同一真实Mint/窗口，追查从市场接收/时效/数据库→已捕获RPC原文→经济解释→AI读入的证据链。此时锚点用来减少错用时间、完整性、Owner与库存批次等几类重复错误。

## 6. 当前证据与不能宣称的完成项

- SOURCE_REVIEWED：目标、专业知识、关键代码和对应测试路径均已在本集成分支核对。
- OFFLINE_TESTS_EXIST：已有Pulse、claim trace、followability、只读安全与原版保留测试；本文件只是链接，不表示本轮重跑代码、亦非任何真实数据通过。
- NOT_VERIFIED：动态锚点影响查找工具、代码运行时自动强制所有锚点、真实链上库存与跨Mint原始签名、完整市场覆盖、实际可成交收益、跨任务模型质量增益和安全公网部署。
- 只读范围：本轮规划映射不更改交易、账户、签名、部署、收费API或当前用户权限。

**整个图谱的目标是减少犯错与返工，而不是让项目因锚点越来越多而失去开发速度。**
