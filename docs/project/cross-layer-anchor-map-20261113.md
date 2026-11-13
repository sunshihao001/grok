# Blix × AI 工作台｜多层锚点与跨层变更影响映射 V0.2

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


## 7. 2026-11-13 全面术语引入后的结构收束：不是加更多标签（V0.2）

**来源和权威分工**：新增的全部专业概念及各自边界以[ai-d通用七类核心能力/概念归位表](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#11-2026-11-13-体系收束从关键词集合走向可解释可验证的项目关系v02)为唯一跨领域理论入口；Blix只保留**适用业务、实际源码/数据/测试及剩余验收缺口**。继承已有G0–G4目标、O1–O6业务、K1–K9知识阶段、D0–D9共享工程前置、L0–L7深度、D01–D12专业领域、原DOMAIN-MODEL的十轴十一关系和INTEGRATION-CROSSWALK。绝不把这些指标互相取代，也不增建七个模块/九个Agent/五个新数据库。

### 7.1 新概念的完整业务落点（七类能力统管全部术语）

| 汇总能力 | 本次归位的所有关键概念/搜索入口 | 对齐现有Blix轴、专业知识、业务与代码位置 | 待修复/未证实 |
|---|---|---|---|
| **S1 方向保持** | 锚定Anchoring、Goal Alignment、需求分解Decomposition、需求管理、ADR、决策背景与取舍 | G0–G4及O1–O6；goal-map、V2总蓝图、build-register、原版保护测试；关联D0/D9 | 当前PR23 Draft冲突；业务最终价值和原版完整运行未验 |
| **S2 结构理解** | 分层Layering、抽象Abstraction、聚合Aggregation、本体Ontology、领域模型、限界上下文Bounded Context、MBSE/SysML | DOMAIN-MODEL十轴及专业D01–D12/L0–L7；TokenAccount/Owner/Authority/Pool/经济实体分别解释；knowledge/README、wallet-roles-and-inventory、economic-events | 原Blix各个来源的真实字段/账户语义尚未统一实证 |
| **S3 映射对齐** | 映射Mapping、结构/语义/关系/跨层/动态映射、Alignment、Linking、Knowledge Graph、实体消歧、语义对齐 | INTEGRATION-CROSSWALK、第1–6节已有主张级关系、economic-claim-trace关联专业知识与原始证据；O2/O3/O4 | 静态链接不是实际AI知识使用或经济主体归因 |
| **S4 双向追溯** | 依赖Dependency、Traceability、Provenance、Data Lineage、Knowledge Lineage、Digital Thread、OpenLineage Run/Job/Dataset | D1–D5数据来源/采集/档案与D9验收；经济交易SHA256、钱包窗口、audit:data-readiness:offline、claim trace；O1–O5 | 真实sourceFirstAvailable和完整数据血缘未被可复查业务闭环验证 |
| **S5 契约约束** | Data/Semantic Contract、不变量Invariant、Assertion、Constraint Propagation、Consistency/Coverage、SHACL、架构规则检查 | D2–D5数据/经济解析、D6工具权限、D9测试；BLX-D-PULSE-FRESHNESS、BLX-K-INVENTORY-PROVENANCE、BLX-C-READONLY和对应现有代码/测试 | 概念与注释不等于程序强制；需对每个真实接口建立有意义的负例 |
| **S6 证据保障** | Verification/Validation、Cross-check、Statistical Cross-validation、Triangulation、Falsification、Claim–Argument–Evidence、Assurance Case、回归与负例、样本外 | D9验收及原Blix VS确定性解析VS AI的对照；O3资金身份、O5跟随性、O6修订；followability-replay及经济反例测试 | 仍缺真实Mint主链证据复核、前瞻样本外和真实模型增益；不可将静态/模拟“升级” |
| **S7 运行演化** | Impact Analysis、Change Propagation、Observability、Versioning、Drift Detection、Feedback Loop、Continuous Improvement、Rollback、变更管理 | D8增量案件/恢复、D9 CI、O6监控与反馈；build-register与blix原历史组件 | 新AI Case长期监控NOT_RUNNING；无自动影响分析/线上漂移测量 |

**术语没有遗漏，但不是每个词都成为新能力**：每个专业词至少被归入一个S类、已有轴及业务对应。没有独立实证的术语关系标为研究解释，不能在代码中当作事实/权限。七类统管的全部词和严格区别见ai-d主文第11节；此表专用于Blix落点。

### 7.2 五种逻辑网络怎样共享一个业务事实

| 逻辑网络 | 主对象/最重要关系 | 本仓已有位置 | 不能忽略的断点 |
|---|---|---|---|
| **N-G目标网络** | 用户目的→O1–O6业务结果→已确认权限与回退条件 | goal-map、V2蓝图、状态及建设台账 | O5实际参与机会优先，不能被无业务效用的新知识图吞并 |
| **N-K知识网络** | D01–D12专业概念/机制→主张/反证→适用条件 | knowledge目录、DOMAIN-MODEL、INTEGRATION-CROSSWALK | 来源作者主张与官方事实、AI候选不同 |
| **N-D数据事实网络** | Source→真实交易/Pool/钱包/时点→SQLite归档/转换/覆盖 | sources/engine/wallets、econ_transactions、econ_instructions、wallet_sig_windows | 采集、处理和first_available不足，不能证明全网实时覆盖 |
| **N-C工程网络** | 业务需什么→现有函数/接口实现→明确权限和运行版本 | 原版Blix和server/intelligence；PR23集成候选 | 同名函数不代表实现同一业务语义，侧车只读不可自动访问交易GET |
| **N-V验证反馈网络** | 主张→正反测试→真实历史/前瞻→修订/撤回 | test目录、CI、build-register、原知识修订日志 | 源码+合成测试不等于真实mainnet/持续运行/可盈利 |

**五张网络是不同观察视图，不是新数据库。** 一项业务结论通过有语义的关系连接至原数据、知识、代码与检验结果；不为每个节点强制生成新JSON对象，也不因为两份文件都有“wallet”词语就建强依赖。

### 7.3 六项业务结果对应的核心“锚点网络”

| 六环业务结果 | 至少要连接的S类能力 | 最容易遗漏的上游与下游 | 阶段性可检验结果 |
|---|---|---|---|
| **O1 市场机会发现** | S1/S2/S3/S4/S5/S6/S7 | 多发射源+DEX覆盖、provider时点、市场候选分母、Pulse不超过12观察名单、被拒对象、后续报价；原版Triage/Early能力 | 同一源窗口的候选及未选记录、首可见、断流/延迟；未验证全覆盖就限制结论 |
| **O2 关键钱包识别** | S2/S3/S4/S5/S6 | Holder与非Holder、Token Account/Owner/Pool/Vault、共享Funder、Wallet历史分页、动态角色；不是“钱包排行榜” | 每条角色关联有来源签名/字段和公共设施反例 |
| **O3 资金与库存** | S2/S3/S4/S5/S6/S7 | Token-2022、inner CPI、SOL/WSOL、Swap+Transfer/LP、资金净额和同批库存不明；经济凭据→AI报告 | 原始签名与库存变化能局部复算，接收卖出与同批出货分开 |
| **O4 跨Mint群体** | S2/S3/S4/S5/S6/S7 | 多跳跟踪、共享Hub、时点先后、资产批次/金额守恒、成员变化与重复经济主体解释 | 能重放路径且保留多个竞争解释；不凭同Slot/Jito直接认定同控 |
| **O5 可参与性/跟单** | S1/S3/S4/S5/S6 | signal_first_available、历史路由报价、交易尺寸、池深、滑点/费用/退出失败、幸存者偏差 | 具备完整模拟收据才算纸面可评价，前瞻样本外与真实Alpha另验 |
| **O6 监控/修订** | S1/S3/S4/S5/S6/S7 | 案件持久化、数据水位/重播、变化影响、重算、错误归因撤回与成本限额 | 真正第二次新市场事件触发同Case更新、不能把回填当新事实 |

这张表**不是强制让每条AI调查走六次流程**；只是在计划某环或判断“是否完成”时检查它依赖的跨层能力是否已具备。重要新知识可以反向改变O1/O2的筛选问题，但重大业务目标和资金授权仍由用户决定。

## 8. 三个跨层案例怎样落实而不膨胀架构

### 案例A：Pulse时间字段变更

如果有人改动browserRecordedAtMs或首次可见字段，要从BLX-D-PULSE-FRESHNESS向上检查O1发现/O5纸面可参与性，向下核对pulse-discovery.mjs、test/pulse-ai-discovery.test.mjs、followability-replay及来源数据时钟；断言是否仍能避免“事后可见当事先可用”。当前脚本仅核“浏览器观察输入”，**缺provider时点和真实市场宇宙**，所以下游真实验收不能标绿。

### 案例B：Token转入后有卖出摘要

如果更改economic-claim-trace.mjs的本地sell证据类型，追到wallet-roles-and-inventory的库存机制、econ_transactions源Hash、实际余额前后、claim trace离线测试，再检查跨Mint与可参与性输出是否抬升到“卖出同批/同控”。若无法重建库存批次，必须仍是UNKNOWN。这是**知识锚点约束结论而非强制每次新建钱包角色标签**。

### 案例C：AI知识文件已更新但模型没用对

若调整local-knowledge-loader或知识目录，沿K阶段的原来源→当前知识版本→提供给模型→实际工具选择→报告主张→真实反例和同预算对照检查。knowledgeUse=PRESENTED_TO_MODEL_NOT_VERIFIED_USED只能证明展示给模型，不等于模型已在决定时正确应用。此处应记录验证需求，不因关键词相同就自动给模型更大权限。

## 9. 成熟成品与标准：全部登记但严格按场景选用

| 参考来源 | 核实得到的有效机制 | 对Blix的当前判断 |
|---|---|---|
| [NASA Requirements Management](https://www.nasa.gov/reference/6-2-requirements-management/) / [OMG SysML v2](https://www.omg.org/sysml/sysmlv2/) | 需求→系统结构/行为/实现→验证的双向追溯与一致性 | 借鉴跨层关系，不引入完整系统工程工具 |
| [NIST Digital Thread](https://www.nist.gov/programs-projects/digital-thread-smart-manufacturing) | 产品生命周期的信息连续/跨系统模型思路 | 理解从想法到实际运行的一条项目历史“线程”；目前属于类比借鉴 |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) / [OpenLineage](https://github.com/OpenLineage/OpenLineage) | 来源实体/活动 + Run/Job/Dataset/Facet可验证处理链 | 最值得用于真实RPC归档与解析/结论来源，**静态知识路由不是运行事件** |
| [Doorstop](https://github.com/doorstop-dev/doorstop) | 需求与测试可追溯、版本控制记录 | 借鉴检查方法；无需为每个函数创建需求YAML |
| [OpenMetadata](https://github.com/open-metadata/OpenMetadata) / [DataHub](https://github.com/datahub-project/datahub) | 业务语义、元数据、字段级血缘、下游影响和可查询关系 | 当前原Blix数据链优先，可借鉴变更影响，不部署大型平台 |
| [W3C SHACL](https://www.w3.org/TR/shacl/) / [pySHACL](https://github.com/RDFLib/pySHACL) | 图约束验证 | 可借鉴语义断言；没有RDF业务不急于引依赖 |
| [ArchUnit](https://github.com/TNG/ArchUnit) | Java源码依赖与架构规则测试 | 借鉴架构回归思想，不将Java工具直接装入JS/TS |
| [ADR](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html) / [OpenTelemetry Stability](https://opentelemetry.io/docs/specs/otel/versioning-and-stability/) | 重大选择背景与结果记录、字段语义稳定 | Blix重要设计选择/字段契约才记录，不为每次小改造新文件 |

上述是**源码/文档层借鉴**，不证明已部署这些成品、更不代表性能或商业价值已由它们验证。仓库及源码许可证仍需按实际移植对象核查；本轮没有移植第三方代码。

## 10. 结构修正裁决与项目下一轮的真实验收

**原位保留**：G0–G4、O1–O6、K1–K9、D0–D9、L0–L7、D01–D12、DOMAIN-MODEL十轴十一关系及已有152历史索引；知识源以原文件/旧知识登记保持，可视图通过本页和现有crosswalk关联。

**明确不建**：S1–S7模块库、五套图数据库、自动“锚点推理”Agent、全文件标签网络、未得到源证据的同控图、零证据强推断、未经用户授权的付费模型或交易入口。

**变更后的最低核查方法**：
1. 说清具体变更服务哪个O1–O6，以及它对应的S类能力和现有文件。
2. 查上游来源、主张、范围、时点与权限；列出直接依赖和“只是可能受影响”两类。
3. 审已有代码/数据契约的实际行为、现有原版功能与关键负例；没实现的不能靠标注说已实现。
4. 只修改有证据的受影响位置、做必要回归与真实场景复现，写明仍未解的UNKNOWN。
5. 如果这套追溯增加的审查时间远超识别真正错误的价值，减少锚点；不为术语数量建新架构。

**一项可证伪的下一轮实证**：选已知源时点或库存归因中的一个**真实Blix代码变化**，在同一版本/任务范围下，与“只看当前文件”方法对照，记录找到的真正下游、误报的伪依赖、新增反例、修复后的真实业务输出和工时成本。没有可接入真实历史数据时只能先完成源码与离线核验，并如实标记受阻。

当前完成级别：NEW_KNOWLEDGE_ALIGNED + SOURCE_TO_CODE_MAPPING + NO_NEW_RUNTIME；不是动态影响分析已实现，也不是六项业务已完成。


## 11. 2026-11-13｜数据源优先纠偏：职责所在处修复，拒绝AI下游重复采集

**用户新增锚点：**“尽量不要直接做数据源应该做的，因为没有提高数据源。”本轮把“数据源、源接入、确定性解析、AI解释”分成不同责任，不把查一枚Mint的缺口补丁当源端能力升级。通用知识归位于[ai-d第12节](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#12-2026-11-13新纠偏数据源主权与职责归属不要在ai下游重做上游)。

### 11.1 已核对的真正上游与下游边界

| 所有者 | 现有Blix实际代码 | 下一项应检查/提升的能力 | 下游不能冒充 |
|---|---|---|---|
| 外部提供商 | server/sources.js调用公开价格与池数据，并由PumpPortal WS接收发行/迁移；Solana RPC由server/rpc-stream.js等读取 | 源实际覆盖、时间定义、历史查询/补查可用性、额度与许可；不足时比较换源/组合而非自建虚构Feed | browser记录时间≠提供商firstAvailable；没有捕获≠没有发生 |
| 原版市场接入与采集 | server/sources.js::pumpStream、server/rpc-stream.js、server/coverage.js和原版engine/livetrades | WS断流和重新订阅后的真实缺口有没有标记与恢复？原市场“覆盖”是否只依赖当前采样/有限窗口？首次收到时刻是否被持久保留？ | AI端不能再复制一个发行流、独立抓全市场替代缺陷 |
| 既有持久化/回放 | server/economic-events.mjs 原始RPC存储；server/wallet-signature-coverage.mjs 原有钱包签名窗口与游标 | 历史签名缺口、原文哈希、丢包重试、窗口覆盖、补查后是否正确回填权威档案；不新建第二套水位 | 只读报告人工拼一段交易不等于源库补全 |
| 原经济解析与归因 | 既有deterministic解析、经济网络与claim trace | 将原始交易解析为确定性经济事实；CPI、Token-2022、SOL/WSOL、Pool、重复记账仍由该层负责 | 数据源不负责推断共同控制或库存批次；AI不能用推理替代解析 |
| 只读AI研究工作台 | server/intelligence/pulse-discovery.mjs、mint-economic-evidence.mjs、research-http.mjs | 只查询受限、已有来源；标注源质量、未知和竞争解释，提出应由源层处理的改进请求 | 不在独立sidecar私自新建RPC收集、全市场索引器或“补齐”缺失数据 |

### 11.2 当前源码可观察、尚未实跑的三处源层风险

- **PumpPortal订阅**：server/sources.js::pumpStream具有90秒停滞重连和指数退避，但当前可见代码中看不到“断线前后漏掉了哪些新Token”的持久缺口水位或历史补查。因此“连接恢复”不等于“发行覆盖已恢复”。需要源端真实数据/供应商接口核实后补修。
- **RPC流**：server/rpc-stream.js主动在延迟超过阈值时重连，源码注释明确新的订阅从tip重新开始、跳过期间交易。它优化实时性但**可能牺牲完整性**；需要确定数据源能否补查以及如何记录该不可见区间，不得让AI在回测里把空窗当没有交易。
- **钱包签名**：server/wallet-signature-coverage.mjs已有原子化发现和缺口/锚点观察，并明确初次25签名只是部分历史；应在这一现成游标体系继续补来源覆盖与恢复，而不是在每个Mint分析器创建独立钱包历史索引。

以上是SOURCE_CODE_OBSERVED，不是证明真实漏包率、提供商缺陷或完整市场分母；外部供应商真实历史能力需现场核实。

### 11.3 修改下轮执行重心

**禁止的捷径：** 为了通过“一枚Mint完整报告”临时从另一套路径拼历史、把未核的供应商时点塞进AI、在AI sidecar写平行Feed/水位或让模型猜缺失资金与行情。这些都是错误职责归属。

**正确的实施对象：** 先对照原版采集职责和第三方API能力，选择一个影响O1/O2/O3/O5多个业务的**源端公共缺口**，在拥有该职责的源接入/持久化层修补，并通过同范围断流/历史回填/时效/重复率正负样本与真实或可复核原文验证。必要的只读Mint报告仅用于发现首个断点和证明源端改善是否传递到AI。

**优先级**：安全/原版基线仍是R0；原R1不再理解为“先让AI报出一个漂亮的真Mint报告”，而应为“R1 source capability fit → capture/recovery gap → source-owned fix → bounded proof → AI consumer recheck”。R2+业务建设仍按真实依赖推进。

**实际完成条件**：至少标明来源的覆盖和不可见空窗，能证明某项源层缺陷在已有组件上被修复，且同样输入时不只一个下游调查改善。若数据源本身不提供必要原文，先按证据和成本评估切换/组合供应商并标BLOCKED，不擅自购买或创造不存在的事实。

**这次记录仅是目标与技术责任纠偏**，没有真实供应商调用、没有修复第三方服务、没有改变运行代码，亦不能宣称源端能力已经提高。
