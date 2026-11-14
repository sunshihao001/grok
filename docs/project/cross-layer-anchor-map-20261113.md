# Blix × AI 工作台｜多层锚点与跨层变更影响映射 V0.3

2026-11-13｜范围：**现有Blix产品＋PR #23只读AI扩展的少量高价值真实锚点**。来源：本分支源代码、现存合成测试与现有知识文档。**状态：ANCHOR_MAP_SOURCE_CHECKED；不是自动监控、全网链上实跑、已验证市场Alpha或新锚点运行框架。**

通用方法的唯一维护入口：[ai-d项目多层锚点与跨层一致性](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md)。本文件只为Blix指向**已存在目标、原知识、原代码与实际测试**，不重复搭一个专业本体，不新增代码与约束基础设施。


## 2026-11-14｜以协调与协同为中心的 Meme 业务知识收束（V0.4）

> **定位**：本节收束现有 O1–O6 业务、D01–D12 专业知识、S1–S7 能力、五张跨层关系视图的协作逻辑。不是增加第13领域、第二套知识库、Agent体系、筛币流水线或数据源。跨领域方法归 ai-d，Meme 专业主述归原 D01–D12，具体模块/验收归 Blix 已有源码与建设台账。

### 1. 三种“协调/协同”必须分清

- **工作协调（orchestration）**：用户表达目的，AI按需组织已授权工具、知识与进一步问题；Blix原程序负责事实生产、存储与确定性核算。它要解决“谁负责、下一项查什么、何时停止”，而非让AI替代原供应商。
- **跨能力协同（complementarity）**：市场、钱包、资金、库存、价格、执行、证据、反证从**同一Mint/钱包和可对齐时点**相互补足，产生孤立标签不能给出的判断。不是12领域全文输入模型、七位专家投票或更多知识文件。
- **链上参与者协同行为（market coordination）**：同Slot/Jito、资金同源、Token转仓、跨Mint接力是**被调查的经济行为假说**，不是上述AI协调的实现方法；共享路由/CEX/正常跟风/回填都可能产生相似信号，不能直接推成同控或可盈利。

### 2. 业务结果优先：六项既有业务怎样协同

| 现有结果 | 业务问题与入口 | 协作责任与现有组件 | 按需知识 | 不可越级的输出 |
|---|---|---|---|---|
| **O1 市场发现** | Pulse/Discover或钱包买入发现什么Mint，哪个值得进一步调查？ | 原engine、triage、early、quality、wallets产出有来源候选；AI仅选择调查价值 | D02/D03/D07/D10/D11 | 最多12浏览器候选不等于市场全集，须保留首次可得与未入选分母 |
| **O2 钱包角色** | Dev、早买、KOL、Bundler、接收钱包究竟是谁？ | 原wallets、wtrack、BubbleMap及已有交易历史协同 | D01/D04/D05/D07/D10 | 标签、Token Account、Owner、实际控制者分别描述 |
| **O3 资金库存** | 买入→Token转仓→接收卖出及净资产变化有哪些？ | 原始RPC、经济存档、economic-claim-trace，只解释已捕获子集 | D01/D05/D06/D10/D11 | Token转移不是卖出；批次成本、SOL净额或同控不明则UNKNOWN |
| **O4 跨Mint群体** | 地址/资金/角色重复是否构成真正跨币接力？ | 原钱包监控与历史，按需跟进实际签名、时间、水位 | D04–D07/D10/D11 | 同地址、时间相关、真实资金路径、共同控制分级 |
| **O5 参与机会** | 指定时点和交易金额可否买入、可否退出、能否跟随？ | 原quote、Paper、Research、Brain，已有followability-replay辅助只读模拟 | D03/D06/D08/D09/D10/D11 | 研究优先级与交易准备度**分别输出**，涨幅/标签/纸面收益都不是可复制Alpha |
| **O6 监控修正** | 真正的新事件是否改变旧Case判断？ | 原Tracker/Journal及来源水位，未来持久化Case按需推理 | D05/D07/D10/D11/D12 | 回补不等于新信号；独立长期Case Watcher未获运行验收 |

这些是**可从市场、单Mint、钱包、跨币线索任意进入的业务路径**，不是要求每枚币依次通过六关。AI按信息价值选知识和工具；无真实历史、有效报价、费用、退出数据时，不得硬给机会等级。

### 3. 归位责任：原有知识与工程各在何处

| 内容身份 | 唯一主要承接位置 | 应避免的错误 |
|---|---|---|
| 产品目的、业务权重、授权边界 | docs/project/goal-map.md 与 blix-ai-workbench-master-plan-v1-20261113.md | 将知识阶段当业务层或改写用户实际目标 |
| D01–D12专业解释、机制、反例与历史原材料 | knowledge/README.md指向原八份主述；独有原文在knowledge/references及旧研究 | 造第二知识库、删独有反例、把作者主张冒充市场事实 |
| 通用AI协作、知识进化、专家表征与方法 | 独立sunshihao001/ai-d；Blix中的D12只负责Meme适配 | 把通用协作概念当链上交易信号或已实现运行能力 |
| 真实链上与报价事实、覆盖、首次可得、断流/回补 | 原Blix sources、engine、wallets、coverage、db及已有经济证据归档 | AI侧重采集、编造签名、补全历史、生成报价 |
| 跨模块职责、语义冲突、跨层影响和取舍 | **本跨层锚点文件** + docs/project/intelligence-layer.md | 新建平行Agent协调框架、数据层或固定过滤链 |
| 实施、回归、运行验证、失败、费用与发布状态 | 真实源码、测试、GitHub Actions和docs/project/build-register.md | 由文档映射或合成测试宣布主网业务完成 |

**错误首先回到真正责任层**：源断流查原采集；Swap+Transfer/Owner/WSOL错查解析；钱包同控解释错查D04/D05与反证；首次可见和行情错查来源/quote；AI选错目标/知识查原intelligence；Mint串币查Coin/Intelligence路由；安全与费用查现有门禁。知识文档不能“修复”数据源缺失。

### 4. 最小协作交接与冲突判定

同一调查在Blix各模块之间传递时，需要知道：**链及Mint/钱包身份、调查目的、时间窗口、来源与首次可得、原始签名/归档引用、覆盖和UNKNOWN、可用工具及费用权限、当前竞争假说、下一项可能改变判断的证据**。这是业务合同要求，不宣称现有代码已实现完整数据接口。

证据冲突时，先检查是否同一个Mint、Owner、池、Slot、事件类型、时间基准与捕获范围；其次看源的原始记录和签名；最后才由AI提出解释。数据不完整不得用模型“达成共识”。几种来源共同重复同一平台标签，不算三份独立验证。

### 5. 协同工作案例：资金异常不自动等于交易机会

用户在Coin打开一个Mint：原Pulse/Coin提供发行、成交、池与时点；经济档案说明钱包买入、Token转移、接收地址后续是否有被捕获的卖出；D04–D07协助判断转仓、分发、库存、共享服务与跨币候选；D03/D08/D09检查价格、可执行报价、流动性、滑点、费用和退出；AI只做有依据的解释、反证与下一步研究选择。

最终必须允许同时出现：**研究价值高但交易机会未知/不可参与**；或**交易条件值得进一步评估但同控假说无法成立**。分别提供research_priority与trade_readiness语义、来源、竞争解释、失败条件、UNKNOWN及是否具备只读复盘输入。不要把这两个业务结果揉成单一“聪明钱买入分数”。

### 6. 目前完成与尚缺的端到端闭环

- **已核对/离线验证**：十二领域归位，原Blix市场与钱包双入口，PR #23 Coin显式Mint隔离、4547只读研究端口、可不调用模型的POST /inspect、真实临时SQLite+HTTP+子进程合成验收，以及原版完全封网冷启/复启；这些是分开验收的能力。
- **未验证**：授权联网的同一Mint原Blix数据→完整真实RPC历史归档→用户真实浏览器端到端→当时可得报价、成本/退出→前瞻机会效果；完整自主Case监控、实用模型效果与已授权部署。PR #23仍Draft，具体CI须按实际HEAD确认。
- **下一项最有价值的联合验收**：首先从现存合法真实Mint归档校验身份、来源时点、Slot/Owner/CPI、捕获缺口；在原Coin→Intelligence→无模型/inspect完成真实只读报告；以同数据、同时点比较原版、确定性扩展与可选AI解释，确认是否减少错判而非增加文件和标签。若现有归档不可用，应如实停止在UNAVAILABLE，不以第三次合成样本充当进展。

**收束标准**：能追踪一项实际Mint结论由哪个原始事实、哪个专业机制、哪个模块、何种反证与哪级验证共同产生，反向从误判找到第一处错误责任；不能改善业务判断或实际验收的新概念不扩建。

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

- **PumpPortal与完整市场采集链（补充源码反证后修正旧判断）**：server/sources.js::pumpStream本身负责90秒停滞重连和指数退避，但这**不等于原版Blix没有发行补查**。server/engine.js已有 `fillLaunchGaps()`（通过livetrades.js链上create事件交叉发现）和 `backfillLaunches()`（近期pump.fun列表查询；启动后有界8页、运行中45秒周期有界4页；429停止，限速）以及其他最近代币来源。仍未知的是断流窗口是否存在**有凭据的事件级完整覆盖、水位及遗漏证明**，近期列表补币也不能恢复全部当时交易、原始时间与首次可见机会；应先验已有机制在具体故障条件下是否有效，再决定哪个现有源模块需要增强，不得重复开发另一套。
- **RPC流**：server/rpc-stream.js主动在延迟超过阈值时重连，源码注释明确新的订阅从tip重新开始、跳过期间交易。它优化实时性但**可能牺牲完整性**；需要确定数据源能否补查以及如何记录该不可见区间，不得让AI在回测里把空窗当没有交易。
- **钱包签名**：server/wallet-signature-coverage.mjs已有原子化发现和缺口/锚点观察，并明确初次25签名只是部分历史；应在这一现成游标体系继续补来源覆盖与恢复，而不是在每个Mint分析器创建独立钱包历史索引。

以上是SOURCE_CODE_OBSERVED，不是证明真实漏包率、提供商缺陷或完整市场分母；外部供应商真实历史能力需现场核实。

### 11.3 修改下轮执行重心

**禁止的捷径：** 为了通过“一枚Mint完整报告”临时从另一套路径拼历史、把未核的供应商时点塞进AI、在AI sidecar写平行Feed/水位或让模型猜缺失资金与行情。这些都是错误职责归属。

**正确的实施对象：** 先对照原版采集职责和第三方API能力，选择一个影响O1/O2/O3/O5多个业务的**源端公共缺口**，在拥有该职责的源接入/持久化层修补，并通过同范围断流/历史回填/时效/重复率正负样本与真实或可复核原文验证。必要的只读Mint报告仅用于发现首个断点和证明源端改善是否传递到AI。

**优先级**：安全/原版基线仍是R0；原R1不再理解为“先让AI报出一个漂亮的真Mint报告”，而应为“R1 source capability fit → capture/recovery gap → source-owned fix → bounded proof → AI consumer recheck”。R2+业务建设仍按真实依赖推进。

**实际完成条件**：至少标明来源的覆盖和不可见空窗，能证明某项源层缺陷在已有组件上被修复，且同样输入时不只一个下游调查改善。若数据源本身不提供必要原文，先按证据和成本评估切换/组合供应商并标BLOCKED，不擅自购买或创造不存在的事实。

**这次记录仅是目标与技术责任纠偏**，没有真实供应商调用、没有修复第三方服务、没有改变运行代码，亦不能宣称源端能力已经提高。


## 12. 2026-11-13｜纠偏的专业扩写：从“修一处错”到“首个失效环节、职责与全链结果” V0.3

通用理论唯一正本为[ai-d多层锚点第13节：纠偏、根因与双环学习](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#13-2026-11-13纠偏能力的深层扩写纠错校准根因修复与学习v03)。Blix在此只登记**真实业务影响、已观察代码、待证风险、修复组件和验收**，不复制又一套认知理论/知识领域或新建全仓纠偏服务。

### 12.1 先判断“哪里出了错”，不能看到AI输出不好就调Prompt

不同问题走不同责任路径：

- **目标/意图不符**：从O1–O6和用户真实输入反向检查是否将“发现机会”误缩成有限候选选币/异常标签；这是任务定义与采样覆盖问题，不只是模型语气。
- **知识/语义不符**：Token Account、Owner、费付方、池子与经济控制者、同批库存来源，必须在原专业知识和确定性解析中核实；不靠模型角色扮演升级证据。
- **数据源/采集不符**：断流、丢事件、时间缺口、429、签名窗口、不完整市场候选，在原来源/采集/持久化层调查与修复，消费端只降级与回报质量状态；禁止在AI sidecar复制一套源。
- **工程设计不符**：原版Blix已经有相同职责模块却重复实现时，优先复用/改其所有者；必须证明引入新功能优于原版且不破坏原版。
- **代码/测试不符**：单位、重复记账、时间边界、受限只读调用应通过确定性负例、契约测试及需要时的真实数据重放解决。
- **验证声称过度**：Static/Offline/Test/Actual-source/Live-AI/Prospective-alpha有不同证明范围，测试通过不意味着生产收益；分层改写主张与验收。
- **工作方式本身不符**：如果三轮仍在新建知识、锚点和计划，没有纠正真实行为，应转向最高信息价值的可执行受限任务，不能创建下一版更长的制度。

### 12.2 候选纠偏对象清单（不是已经确诊的所有BUG）

| 优先级/证据 | 观察到的情况及可能偏差 | 责任所有者与正确修正方向 | 可核验的纠偏证据 |
|---|---|---|---|
| **P0 / 源码可见与用户纠偏** | 将AI的12个Pulse浏览器候选称作“完整市场自主发现”会误设O1目标 | 原版市场源/采集/候选框和AI标注各按职责；先声明真实Universe、源时间与拒选样本，必要时修原版数据采集 | 真实来源覆盖/时效记录；缺失情况正确降级，不只改变候选文案；source unknown保留 |
| **P0 / 源码可见，真实影响待测** | server/rpc-stream.js重连从链头订阅，源码明确承认可能跳过消息；不能把“源恢复连接”等同于“缺口历史已恢复” | 原版RPC采集/源存储；先确认供应商历史可补、现有补查路径与游标边界 | 断流→缺口检测→受控补查/标记→恢复收据；同样缺口可被多个业务消费者识别 |
| **P0 / 专业语义与现有离线测试** | “A转B，B后卖”不能证明B卖的是同批库存，需防止AI从局部sell摘要推出控制/成本基础 | 既有economic-events、economic-claim-trace及库存领域知识；不创建平行模型账本 | 正负库存反例、原始签名/指令身份、覆盖与UNKNOWN保留，必要时独立主网验证 |
| **P1 / 已有部分补查，完整性待测** | sources.js有WS重连；**engine.js::backfillLaunches与fillLaunchGaps已存在**，但近期列表/链上交叉发现不证明事件级无缺口或交易历史补齐 | 先测试原版engine + livetrades + sources在断流/重启、429情况下的真实覆盖；只增强证实不足的源所有者，不能让AI再建全市场源 | 已有补查发现遗漏Mint的签名/时点/恢复收据；对不能补的窗口保留SOURCE_GAP，不称全量/实时重建 |
| **P1 / 源码可见，风险已标注** | wallet_sig_windows有原子游标但historyComplete:false、初次抽样不全；若下游把“查询完”写成“全历史完整”会错 | 现有wallet-signature-coverage.mjs及econ_wallet_processing，先做范围可证的采集，不再建AI专属钱包签名索引 | 锚点达成/断点/首次抽样分别报告；有限窗口重放不误报完整历史 |
| **P1 / 离线测试存在，独立效果未知** | 纸面回放能完成确定性损益算术，但不能说明信号当时真实可见、退出可成交或策略样本外有效 | 已有followability-replay.mjs和原市场时点/报价源；实际机会评价由证据承接 | 真实来源的报价时间、可执行规模、成本/退出、负样本；没有则UNKNOWN |
| **P1 / 项目状态可核** | PR#23 Draft且与blix冲突；原版文件静态保留不等于全产品真实运行兼容 | 原版合并基线、权限与回归所有者；冲突定位后有依据地修改 | 最新SHA下相关CI、真实原版场景、部署/数据隔离验证；不把uptime与Node测试混级 |
| **持续 / 用户反复指出的研究偏差** | 研究/锚点数量增加，但AI是否更准确理解、真正执行、减少返工尚未经公平对照 | ai-d通用认知，Blix实际任务验收；停止重复写框架 | 同任务/同源/同预算对照，正确识别漏项、误报、花费时间与实际可复查产物 |

**状态解释**：SOURCE_CODE_OBSERVED不等于已经发生损失；USER_FEEDBACK是需求与协作层事实，不是独立模型实验；PROFESSIONAL_RISK是基于语义的潜在错误；UNKNOWN需要指定数据/源码/权限才可确认。排序是本轮研究推荐，未取代总规划R0–R6，不意味着已授予改动原版交易/付款/部署权限。

### 12.3 “因果纠偏”示范：RPC重连漏交易，三层连锁错误

**观察**：原RPC订阅在落后时会主动重连且从tip重新开始。**可能出现**客户端未捕获的交易窗口。它不自动意味着这几秒实际存在相关交易，也不证明某家供应商不提供补历史。

- 第一层**症状**：某Mint报告中没有某笔交易；下游若称“无交易”便混淆“未捕获”和“确认不存在”。
- 第二层**直接因素**：RPC Stream的实时优先重连；需要检查历史补查、持久gap和签名覆盖的各自职责。
- 第三层**系统性因素**：下游读取的数据契约若不携带不可见窗口、时间水位和完整性声明，任何报告、选币、回测都容易重新引入错误。
- **即时限制**：未核完整性前报告UNCOVERED/UNKNOWN，停止给出完整市场/资金声明。
- **源端纠正候选**：确认源API实际能力→采用原版源归属记录中断窗→按许可实现可界定的历史补查/重放，或在无法补查时保留缺口。
- **预防候选**：增加源记录、恢复与业务消费者之间的契约断言/负例，不允许静默将gap转为零事件。
- **实际验证**：在相同可控制输入下证明缺口被记录，成功补查或诚实不可恢复，并让多个下游共同受益。真实外部历史可用性仍待核验。

**实际已经找到一个需要撤回的旧诊断**：原先只检查`sources.js::pumpStream`，曾将“该文件没有补查”概括为“Blix发行补查待建”；复核`engine.js::backfillLaunches`、`fillLaunchGaps`及`livetrades.js`后，确认原版已具备**有界发行列表回填、链上交叉发现和短时间状态恢复**。因此已撤回“缺少发行补查本身”这一宽泛判断，剩余问题严格缩小为**现有补查是否足以解释特定断流窗口、重建事件/交易历史和证实最早可得时间**（未验证）。钱包侧`wallets.js::pollOne`、`pageSignatures`与`wallet-signature-coverage.mjs`也已有补查和持久化gap观察。这是纠正**错误的技术诊断**，不是证明市场覆盖已足够或新增运行能力。

### 12.4 纠偏不能变成新的项目偏移

- 不增加P9/P10领域、不新增纠偏Agent/长Prompt/单独数据源、不把这八行候选视作全项目“发现八个已确证缺陷”。
- **初次出现且可逆的局部错误**可直接改并回归；**高风险、反复、跨层、数据源公共影响的偏差**才检查供应商→我方采集→存储→解析→AI→用户结果的路径。
- 应辨别“当前结论错误”“数据不足不能判断”“用户目标本身在演化”“业务权限不足”，不把所有不同意见都判成BUG。
- 以**可检验纠正效果**关闭，而不是以删除警告、修改术语或绿色离线测试代替所有真实验收。
- 未来一旦真实新证据反对已记载判断，沿锚点直接修原责任层及受影响测试/知识；若AI自己的修正建议带来新限制，依据实际任务回退。

**下一项高价值工程**仍是R0源归属/安全核对及R1上游源能力修复：优先选择能证明改善多个Blix用户场景的采集/恢复问题。现阶段本章节是SOURCE_AUDIT + CORRECTION_CANDIDATES_REGISTERED；没有启动数据源、付费API、交易或真正修改运行逻辑。


### 12.5 预防性纠偏：对重要公共风险提前预演，但不能把风险候选报成已发现BUG

补强上述错误登记方式：对跨多个业务、后果严重、难以及时发现的环节，借鉴[ASQ FMEA](https://asq.org/quality-resources/fmea)从功能、失效模式、下游后果和现有检测手段进行预先审查。该审查**不证明缺陷已发生**，不能生成无依据的发生概率，也不应替代实际功能研发与原上游数据源修复。

| 风险候选及状态 | 一旦发生会污染哪类业务 | 最合适的早期防线及验证 |
|---|---|---|
| **RPC重连缺可追踪水位**（源码存在从tip重连取舍；真实漏包待验） | O1市场时效、O2钱包、O3资金经济事实、O5回放 | 在已有原版RPC/持久化职责处检查记录缺口及能否真实补查；用人为断流反例证明消费者至少知道不完整 |
| **Pulse有限采样冒充全市场**（已确认代码是候选子集） | O1机会发现、O5机会筛选评估 | 输入/来源合同明确Universe、firstAvailable与UNKNOWN；独立真实源样本做覆盖比较，不在AI端建平行市场采集器 |
| **Owner/TokenAccount/同批库存混淆**（专业已知风险，未确定真实误判率） | O2地址分类、O3库存、O4跨币关系 | 原协议语义与确定性经济解析的负例；原始签名引用、历史缺口传播与UNKNOWN输出 |
| **纸面回放被解释为可实现盈利**（现有回放明确只是纸面） | O5是否值得参与 | 当时可得报价、入出场执行条件与未成交/退出失败反例，缺源数据就阻止“已验证收益”主张 |
| **新纠偏越过原版与只读权限**（流程风险候选） | 原版交易入口、整个AI工作台 | 既有原版保护、安全与只读测试；不得因研究便利直接开放签名/付费/生产数据写权限 |
| **完成度错级与纠偏自我膨胀**（项目多轮反馈） | 所有业务目标与下一步判断 | 将SOURCE_OBSERVED、OFFLINE_TESTED、REAL_RUNTIME等按主张限定；同任务看是否减少真实遗漏，未改善则停止扩规则 |

预防与实际纠错如何汇合：若后来出现真实事件，保留对应签名/观测/代码版本，并把“潜在失效模式”升级为“已发生事实或有界反例”，确认首个可修责任层、修复后回归与同类复发范围；反证若证明有其他模块已补好缺口，应撤销旧的缺陷推断。

**项目优先级不因FMEA自动重排。** 先R0基线/权限和R1真实数据源职责与恢复；再沿真实业务价值实施。此补充为风险识别与验收设计，**不涉及源代码、供应商或主网运行改变**。

### 12.6 真实源码纠偏：旧签名锚点缺失时的错误“扫描到边界”判断（R-33）

| 关系层 | 已核事实 | 仍不能宣称 |
|---|---|---|
| O2/O3/O4 业务 | 钱包签名窗口不应把未知历史扫描边界判作已覆盖，否则资金和跨Mint后续调查可能依赖错误完整度 | 未证明任何具体主网交易被漏掉 |
| 上游源层责任 | [server/wallets.js](../../server/wallets.js)::pageSignatures原先使用`first || !lastSig`设reached初值，若first=false、lastSig=null且每页50签名直至pages用尽，曾错误返回true | 未提高外部RPC实际事件覆盖或第三方接口质量 |
| 现有状态拥有者 | [server/wallet-signature-coverage.mjs](../../server/wallet-signature-coverage.mjs)::checkpointWalletPage保存窗口及gap，未建立AI第二套水位；修复后会得到未验证边界状态 | 仍无法证明钱包终身历史完整 |
| 代码修复 | 非首次扫描初始化reached=false，仅短页/已观察到旧anchor后才可确认；同时日志从“确定丢过旧交易”改为“可能缺旧事件” | “有风险”不是“已确认发生漏包” |
| 负例和正例 | [test/wallet-evidence-chain.test.mjs](../../test/wallet-evidence-chain.test.mjs)新增连续满页达到预算→false；短页/有上次锚点→true；现有wallet-signature-coverage测试检查风险持久化 | 合成回归不是供应商真实重放 |

**这是一次完整但有边界的跨层纠偏**：从O2/O3的真实可信数据要求，反追到源层扫描逻辑，修改属于该职责的原函数，再以可重复的确定性输入复查返回状态和已有接入者。此处没有创建新的纠偏引擎、数据源或AI推理规则。详见[Blix建设台账R-33](build-register.md)。
