# 参考项目不受 Blix 功能缺口限制的完整知识研究｜第一轮纵深 V0.1

> 2026-11-06。证据状态：**全量Git树目录已核 + 部分原文/源码已深读 + 跨项目推理**，不代表每个知识点已读完或运行过。源版本见 [覆盖账本](source-coverage-v0.1.json)。仅研究和文档更新；未运行Blix、未安装参考程序、未改业务代码/启用交易/支付/主网请求。

## 1. 改正过去研究的入口错误

**“只研究能马上补齐Blix缺口的知识”属于工程复用策略，不能成为专业认知研究的边界。** 旧方法会系统性漏掉：当前产品尚不能表示的经济机制、与主流结论矛盾的观察、理论生成方法、作者失败经验、没有直接产品落点但可能影响未来定位的能力。

因此同时保留两条独立的认识路线：
- **先独立理解每个参考项目：** 它原本的问题、设计历史、完整业务、全部重要概念、源码和依赖、数据事实、案例、测试、反证、失败、版本修订和开放问题。允许新知识重塑原本的业务目标；不能因Blix现有功能没有对应字段就跳过。
- **再比较和融合到Blix：** 方法可能成为知识和提问能力，事实定义可能用于原有数据模型，反例可能用于测试，成熟代码可能需要有限集成；不是所有知识都要转换为硬规则、Bot、数据库和运行时提示词。

研究一个知识点时，不只是“做什么/代码在哪”：还需回答**原始问题、专业原理、观察变量及经济意义、适用条件、来源证据、代码/测试能证明什么、隐藏前提、反例、不同项目分歧、可推翻条件、新问题、和Blix的可选关系**。没有充分证据就保留UNKNOWN；根据实际知识内容深挖，不预设一轮只读几个文件。

## 2. 真实全量目录基线，而不是拿几个README代表一个仓库

| 原项目及冻结版本 | Git文件 / 不同blob内容 | 独立知识区域（目前树已检查，全文尚未全读） |
|---|---:|---|
| [Hermes](https://github.com/sunshihao001/-/tree/2bf694b37cce25b4a3c9364298b784039f3ecc84) | **264 / 231** | learning 43、reports 41、skills 38、tasks 34、design 29、docs 23、tests 10、fixtures 6。包括学习演变、角色与资金结构、筹码控制权、门控、失败记录，不只是五问题引擎 |
| [qb-](https://github.com/sunshihao001/qb-/tree/8377ad5611255df5cd4562666a826708575334f0) | **4,236 / 3,276** | data 3,338、hermes_harness 610、恢复包203。其中包括GMGN候选与样本、Source Wallet、Wallet Intel、运行钩子93、真实任务风格回归56、判断基准17、防自欺6。不能只看单Mint脚本 |
| [meme-](https://github.com/sunshihao001/meme-/tree/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a) | **474 / 414** | 关键词与原始资料136、多语言55、文章36、知识迭代34、specs32、样本23、指标源码及策略模型等。不能只看FCZ/AVWAP几篇文档 |

**去重仅用于阅读效率，不用于删历史。** 哈希相同的文件可能是不同阶段的重复拷贝（Hermes同一筹码设计有四份同blob；meme多份同源MQL5指标；qb多次空报表/相同风险报告）；应保留路径和阶段，阅读同内容一次，同时追踪版本变化。不同blob也不等于不同专业知识：模板、运行输出和市场原始案例必须分别归类。仅凭4236这个数字不能声称有4236个知识点。

## 3. Hermes原始认知：不仅识别已知模式，还要生成新机制

### H01｜从问题到可观察证据

[00c字段思维原文](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00c-GMGN-思维模型提炼.txt)把“市场想知道什么→链上会留什么痕迹→可用字段→字段交叉→该数值在何场景有意义”作为核心推理次序，并区分Raw、Feature、Structure。它不是GMGN字段说明，而是将主观标签转换为**可被数据支持或反证的问题**。

例如“几个钱包同时买入是否同控”：同期购买是时间关联；同出资地址是资金关联；同一人控制属于经济主体假设。这三件事需要不同证据。共享交易所提款、基础设施代付手续费、使用同一狙击服务可以产生类似图谱。旧Hermes里“同源合计>20%就高风险”“相似时间/成本意味着极高概率同控”的静态规则未经独立校准，不可直接继承为身份结论。

**跨项目补正：** qb用数据护照把事实/证据/推断明确分开；Million的图模型有funding、feepayer、coentry三类边，而Blix原Bubble Map存在最早Fee Payer被标记为funder的可能。这证明区分经济动作及关系语义很重要，不证明任何单条边一定是同控。

### H02｜“生框架”与认知边界拓展

[00e原文](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00e-字节反推框架-突破认知局限.txt)提六类主动发现：字段穷举配对、异常样本、无标签聚类、反向假设、时间序列、跨链对照。其核心不是制造更多指标，而是让不符合已有“庄家吸筹/出货”等命名框架的数据生成未知研究问题。

**必须修订的隐藏前提：** 80个字段有3160个两两配对，但有量纲错误、分母为零、字段共源性、多个比较检验的偶然相关；原文关于“5-10%意外新发现”的比例没有独立验证。挑选事后暴涨/暴跌币来找特征容易发生幸存者和未来信息泄漏，无监督分群不保证存在真实经济组织。应保留“开放发现→形成机制候选→反事实/基线/样本外挑战”的知识能力，而不是直接安装3160条信号。

**新的认识：** 如果Blix只允许围绕已有字段找缺口，AI就会丧失发现未命名资本组织或行为的新能力。Blix可以为新问题提供数据，但不是知识探索的上限。

### H03｜动态筹码控制概念 vs 伪精确概率

[原筹码控制状态设计](https://github.com/sunshihao001/-/blob/main/design/Skill4-筹码控制权状态层设计.md)尝试按库存保留、群体流入/流出、分发、回流、对手盘、时效与实体退出定义ESTABLISHED、LOOSENING、TRANSFERRING、COLLAPSED等状态；规定已清仓实体权重为0、池/CEX/系统账户不应算普通控制地址、过期数据可变UNKNOWN。

**独立专业价值：** 当前持仓比例和资本组织是否仍有效是两回事；同样的Top10集中度可对应真实分发、跨账户转仓、共同服务、库存失活或新主体替换。它引导研究群体演化，而不是只做静态Holder榜。

**边界：** 设计的0.45/0.25等加权与“贝叶斯状态”在已读源里未看到经过可靠基准率/似然/标签数据校准；0.68这类置信数字不代表经济控制概率。不能直接把旧数学形式变成Blix的“庄家置信度”。接下来必须继续阅读上游entity-clustering/structure-evidence、测试和失败案例，才能进一步判断这些状态是否可观测。

## 4. qb-原始认知：市场调查 + 数据语义 + AI可靠性

### Q01｜单Mint关键钱包调查是问题选择，不只是标签导入

[原单Mint脚本](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)查info/security/pool/K线、holder、获利者、bundler、transfer_in、fresh等，并分类转入接收钱包、派发候选、LP/池子、一般交易钱包。它的价值在于：**按钱包在市场经济过程中能回答的问题挑调查对象**，而不是只盯盈利钱包。

但旧classify()将供应商transfer_in、卖出比例≥0.6等组合成E4/R2等历史分级；它们是规则候选，不是实际控制身份/概率。原脚本使用shell命令，且依赖历史GMGN环境；保留算法与业务问题，不直接部署。

### Q02｜Wallet-Intel四种语义与数据护照

[事实层/结构证据/行为推断/交接四层](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/01_control_plane/wallet_intel_data_layering_rule_v2.md)分别规定可回溯原始事实、推理依据、竞争性解释、下游用途；[Token数据护照](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/01_control_plane/wallet_intel_data_passport_rule_v2.md)记录旧路径/新路径、已有及缺失字段、事实与推断边界、是否足以继续分析。这里的“护照”核心是**知道自己不知道什么**，不是要在Blix重建文件治理服务器。

[旧qb阶段6验证](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/06_verification/project_governance/wallet_intel_stage6_data_passport_verification.md)记为PASS，但明确只是规则/模板锚点检验，并**未真实迁移token数据**。不能把此历史PASS说成产品曾真实完整运行。

### Q03｜被旧融合忽略较多的是AI自欺与判断校准

[anti_self_deception](https://github.com/sunshihao001/qb-/tree/main/hermes_harness/22_anti_self_deception)区分计划、文档、dry-run、自评和真实完成；[Reliability Calibration V1.7](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/01_control_plane/reliability_calibration_policy_v1_7.md)要求预期结果、实际结果、差异、错误率、回归样本及记忆重验。[V2.1任务回放](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/23_real_task_regression/README.md)有一轮5/5的夹具记录，但其run summary原文写明**“fixture_regression_passed_not_proven_in_live_tasks”**。这说明旧qb意识到“测试通过”≠“真实任务可靠”。

**对AI外挂大脑的真正贡献**：知识已放入目录、聊天引用了知识、AI按正确知识处理了陌生任务、结果通过独立验收，是四个不同成熟度。当前Blix主要是来源及人工推理整合，未证明自动知识调用提升。qb剩余的判断基准、真实任务回放和实际错误日志值得作为独立项目完整深究。

## 5. meme-原始认知：从价格概念到可推翻的机制

### M01｜FCZ/成本中枢并非链上确认的庄家真实成本

[第一控盘区定义](https://github.com/sunshihao001/meme-/blob/main/03_语义概念/第一控盘区定义_v0.1.md)把早期成交密集、POC/HVN、后续第一波拉升和后续回测意义合成一套区域定义。它的实质是价格/成交分布的**阶段性观察假设**，不是有证据证明一名控制者的链上真实持仓成本。

**本轮新发现：未来信息泄漏。** 若“后来发生有效拉升”是FCZ成立必要条件，这可以用于事后标签，却不能用于当时实时预警；否则预测器使用了尚未发生的结果。应把“当时仅可识别的FCZ候选”和“后来验证的FCZ”分开。即使完全不采用FCZ交易策略，这个时间信息问题也适用于钱包标签、资金历史补全和异常检测。

### M02｜深洗、死亡盘、二次启动是竞争解释

[深洗与死亡盘](https://github.com/sunshihao001/meme-/blob/main/02_庄家周期/深洗与死亡盘语义深化_v0.1.md)和[诱多/二次启动](https://github.com/sunshihao001/meme-/blob/main/04_风险管理/诱多反抽与二次启动区分_v0.1.md)关注成本区域重新接受、回撤不破、二次推进、卖压和持续需求。它们引导研究时间序列和失效条件，但“价格跌深是洗盘”“反弹是庄家回归”都非直接事实。薄池、换池、普通买盘、库存释放可能产生相似图形；必须与资金/库存证据相互挑战。

### M03｜真正可迁移的是事前失败判据

[反证实验设计](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/反证实验设计_v0.1.md)将样本分A符合成功、B符合失败、C不符却成功、D看似符合却死亡、E图形成立但不可执行；坚持固定规则版本、保留失败、不能事后重画、对照简单基准和消融。这不只用于交易策略：对任何“拉升前12h转账激增”的市场机制假说都应保留无激增但上涨、激增却下跌、缺历史与公共服务等对照。

[原成熟度审计](https://github.com/sunshihao001/meme-/blob/main/第一控盘区成本中枢回收模型_成熟度审计.md)自评Level2/5，属于结构化观察模型，不支持自称已验证可盈利。外部MQL5指标源码和资料仍需逐个核查许可、指标定义和Meme市场适用性，不能因为主要读了语义文档就说读完meme-。

## 6. 首批成熟参考产品的独立认识（尚非全面解剖）

**Million**：[总体业务](https://github.com/Kelows/million/blob/main/README.md)是一条钱包发现Token→Token发现钱包→双向筛选→执行/观察结果回评循环，研究价值不止资金多跳。[FundingService](https://github.com/Kelows/million/blob/main/apps/api/src/funding/funding.service.ts)处理有方向SOL nativeTransfers、有限历史和truncated；其[WalletEdge](https://github.com/Kelows/million/blob/main/apps/api/prisma/schema.prisma)分别定义funding、feepayer、coentry。源码注释明确交易所存款地址和地址新鲜度未核实：关系边不是同控真值。未读完整订单、PnL、钱包循环与测试，不作整体复用裁决。

**PumpTrace**：[Architecture](https://github.com/AntC215/Pumptrace/blob/main/docs/ARCHITECTURE.md)区分直接转账/指令、较强行为、协调可能、仅时序和背景；[BackfillManager](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)有暂停/恢复/封顶/状态与游标。这是成熟的历史缺口研究入口，但不能从设计/存在源码推断无损捕获全部CPI或重启实跑已验收。

**Pulse**：[README](https://github.com/nirholas/pulse/blob/main/README.md)将发行/毕业/死亡、钱包标签、运行者研究、日摘要和历史归档连接；部分trades围绕标记钱包、较大买单和成功/毕业币早期买家，研究其“选择哪些市场样本留下来”的偏差，同样重要。并非所有市场交易的永久全历史证明。

HoldTech、OKX、PumpGrok、Why-Solana、pumpwatch和此前65项参考资产仍在原来源索引中，**没有因当下Blix缺口不明显而被排除**。后续对每个项目独立阅读自己的用户目标、业务、UI→源码、模型、失败、测试和历史，而不是只扫描README找到Blix能抄的模块。

## 7. 知识真正融合意味着什么？

**全量认知积累**不强迫所有来源变成Blix内部代码。可以分为：直接事实和协议语义；专业调查问题；市场机制/反事实假设；开源程序设计与可靠性经验；旧错误与失败样本；可复用知识选择方法；尚无法使用的开放研究问题。每项知识保存自己的原始出处、修订、条件、冲突与状态。

**应用和实现另外验收**：原知识可独立在Blix知识库被AI按任务检索，但“能读取文件”不等于“AI真正理解”。只有实际在陌生任务里选对知识、推翻错误前提、能追到市场事实、给出反证，才可称为知识运用；有安全隔离、测试、真实报告验证后才能称为运行能力。即使暂时不能应用，也不因此删除新机制研究方向。

## 8. 已覆盖与未来继续深入的边界

当前三仓完整**树/文件内容哈希**已核；内容深读的是若干原设计、脚本、语义文档和验证原文，**绝非每个知识点都已理解**。需要继续沿来源完整研究：Hermes剩余learning/skills/tests/reports的设计演变；qb大量真实数据与Wallet-Intel实验、判断基准、回放错误；meme原始指标/样本/工程/specs与假说变化；成熟参考产品全流程/历史/测试。每遇到真正独有的知识，逐个补充同一来源研究记录或现有知识类目，保留未读状态，不能按文件数宣布“融合率”。

**本轮最大的修订：知识研究应主动突破现有产品和个人已知概念的边界；Blix是之后的可选应用主体，不是给研究视野设下的上限。**


## 9. 2026-11-07：外部成熟方法三轮检索后的融合修正与Pulse源码试验

> **定位**：研究一个不预设知识边界的成熟参考项目，怎样避免被 Blix 旧目录/现有功能裁剪、怎样保留原始设计与来源、怎样让 AI 探索未知机制、怎样证明用知识更准确。本段不添加新的知识本体/固定专家/Agent框架。三轮外部检索基于截至2026-11-07可访问的原始方法、开源代码、评测研究；首次将这些方法用Pulse对照Blix做了**具体源码与确定性离线规则复算**。未运行Pulse/Blix、未做实时Solana RPC与真实GrokBot A/B。

### 9.1 外部真实做法——只取能解释既有失败的要点

| 原始方法/项目及出处 | 对方实际解决的难题 | 适用于 Blix 什么具体障碍 | 暂时不采用什么 |
|---|---|---|---|
| [Aider Repository Map](https://aider.chat/docs/repomap.html)（Tree-sitter/符号依赖与图排序） | 不是一口气注入完整代码，而是掌握全仓骨架、按实际调用/依赖关系选择上下文 | Hermes原始字段→派生指标→L2判别→qb取值→Blix报告，以及Pulse观察→持久化→后续“无事件”结论；研究时沿关系读代码/测试，而不是只找同名文件 | 不因此安装新的代码搜索服务，也不把图排序当专业事实验证 |
| [MADR/ADR设计决定记录](https://adr.github.io/adr-templates/)与[Adobe代码仓设计依据恢复说明](https://opensource.adobe.com/ai-repo-harness-guide/skills/harness-setup/references/docs/) | 记录背景、被考虑的替代路线和后果，历史理由缺失则留待核实；**不能从代码反推作者心理并当成事实** | Blix为何要记录gap、Pulse为何选择性保存、Hermes为何使用GMGN加工字段：区分注释明确原因、代码行为和研究者假设 | 不为每一知识点新建一份ADR文件；仅在重大产品路线取舍时记入现有决策文件 |
| [Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval) | 片段离开所属文档/主体后会丢失上下文；给检索片段带简短原文上下文，混合精确词与语义搜索 | 不让Hermes `volume_momentum`阈值脱离币龄/供应商/窗口独立进入运行时；源版本/含义/边界必须与知识片段同行 | 目前不自动向量化所有仓库或把全文装入prompt；先保留原文路径/背景与精确选段 |
| [Microsoft GraphRAG](https://microsoft.github.io/graphrag/query/overview/)及[DRIFT Search](https://microsoft.github.io/graphrag/query/drift_search/) | 结合全局主题与局部事实，从当前问题继续生成追问，扩展不同来源之间的关联 | “异常转账”可能继续连接资金、Token库存、公共设施、事件时间、市场执行、样本保留和事后规则偏差；允许出现旧D域之外的问题 | 不先建图数据库，也不把自动抽取的图边当真实经济控制边；全局索引可能耗费大量计算 |
| [Agent Retrieval Bench 2026](https://arxiv.org/abs/2607.24882)（427例、25仓库） | 真正的上下文是下一步工作所需文件，不是词面最相似；检索方法在不同任务上胜负不同，错误仓库与应弃答也是评估对象 | “已找到2份最相近代码”不等于找到了隐藏依赖、测试、历史失败、反证或完全缺失的证据；必须支持继续追问和UNKNOWN | 不未经对照就宣称某一检索算法/知识图是最优 |
| [OpenAI Codex/AGENTS指导](https://learn.chatgpt.com/docs/customization/overview) / [Agent Skills渐进式加载](https://learn.chatgpt.com/docs/build-skills) | 入口指令精简；能力/参考资料按任务需要再读取；重复错误才保留为长期约束 | 保留现有Blix `AGENTS.md`、`ai-d Skill`和`knowledge-use.md`作为路由；重大经济研究仍向原始文件递进 | 不把每次研究结果写成新的强制提示词，不扩建固定Expert/Bot |
| [Ragas评测](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)与[CodeRAG-Bench](https://aclanthology.org/2025.findings-naacl.176/) | 将“找对上下文”与“答案基于上下文且真的正确”拆开测试；检索帮助取决于任务和证据 | 比较相同Mint原始材料下：Blix现有方法 vs 按需旧项目知识，检查关键遗漏、误报、UNKNOWN、证据来源和成本 | 不把LLM自打分视为链上事实，不声称现有Blix经过了检索增益实验 |

**融合原则**：外部成熟方法是**用于改善专业研究的工具箱**，不是必须安装的系统清单。重点不是某一项目的名字/标签，而是它能否在源文件、业务流程和数据之间打开此前忽略的因果或约束关系。无Blix模块落点的知识仍可继续研究，直到有依据判断价值。

### 9.2 需要组合的不是“知识点标签”，而是可继续探索的源证据与问题关系

**两种探索方向并存**：

- **从项目自身向外**：全目录/入口/UI/API/代码/测试/日志/变更/设计记录建立完整**已发现范围**；按主题追“真正解决的问题—源可观察行为—作者明确理由—失败条件—尚未解释的事实”。这确保Blix未知、暂时不能实现的高价值研究也不会被截掉。
- **从某个市场异常向外**：起点可以是资金转账、同Slot买入、Holder余额变化、异常缩量等；跨来源追“资金事实—账户控制/服务关系—经济库存/对价—执行与池—生命周期—采集/保留偏差—反例—新问题”。它不是固定八领域检查表；每遇到矛盾，可按信息价值扩展到以前没有想到的学科和项目。

实际研究对象应是**一条能被追溯的知识链**，例如：

`原观察（Mint/签名/数据源/时间） → 定义/单位/分母/覆盖 → 派生关系/统计 → 至少两个不同生成机制 → 可以区分机制的后续证据 → 反例/失效条件 → Blix能否表达/观测/测试 → 新的未解问题`

源项目文件路径、固定commit/blob、读到的正文位置、原项目运行条件等用于**证明研究引用来源**；不是给钱包贴身份真值，也不是永久新增知识标签。**关系类型属于证据说明：观察支持、源码依赖、否定、竞争解释、时间先后、实现约束；同一问题可以跨无限多个旧目录。**

只有影响可解释性、事件覆盖、真假证据或实际业务判断的知识，才转入Blix专业正文/测试/只读报告；无法马上应用的高价值未知**保留源链接与下一条可检验证据**，绝不因此删掉或合成错误结论。所有原仓原文保留，Blix现有六类目录仅为归档。

### 9.3 具体源码试验：Pulse“观察了但没有保存”将如何误导跨Mint机制研究

源码固定证据：

- Pulse [`src/collector/solana-stream.ts`](https://github.com/nirholas/pulse/blob/main/src/collector/solana-stream.ts)，读取版本的blob `d80465c043852e85619f5eee86634389e5b4a045`：所有解码到的交易可进入短时Rolling热度；**持久化tradeQueue**在`labelled`钱包、单笔达到`WHALE_SOL=5`时触发；另缓存**每Mint至多40名不同早期买家**，当`complete`毕业事件到来时`flushEarlyBuyers(...,'early:graduated')`补存。源码注释提到runner，但本次阅读到的该文件中仅发现毕业事件直接触发`flushEarlyBuyers`，是否存在文件外runner调用仍需全局审查，不据注释扩大实际断言。缓存可因`EARLY_MINTS_MAX=6000`淘汰。
- Pulse [`src/collector/merge.ts`](https://github.com/nirholas/pulse/blob/main/src/collector/merge.ts)，blob `b5ff1347e48ebe4eb75d4dfbb40cba2f5aadeb88`：同Mint多源字段在首个非空值存在时主要只补缺，`source`字符串可累加，但并不自动标识每个字段的权威来源/时间与冲突值。`null`和`undefined`的差异意味着不能称它为经过分歧裁决的权威真值。
- Pulse [`src/archive/restore.ts`](https://github.com/nirholas/pulse/blob/main/src/archive/restore.ts)，blob `e4fc9f87f64b28b992ff641f1ee917902ce3bb2f`：历史恢复对部分可变表`upsert`，其他表`on conflict do nothing`；完整性需根据表、主键、保留策略分别判断。
- Blix [`server/journal.js`](https://github.com/sunshihao001/grok/blob/blix/server/journal.js)，blob `7afb9c6126efff8ae251e3bff251279ce9227792`：对它**实际听到**的curve/PumpSwap交易做签名/事件位置去重、processed→confirmed核验，并记录/修复部分断流区间；`KEEP_MS=24h`，修复对候选Mint数量/超过2小时Gap有真实边界。这与“长期无损全链历史”不是同一能力。
- Blix [`server/coverage.js`](https://github.com/sunshihao001/grok/blob/blix/server/coverage.js)，blob `0813c72c79c62d8432eb4f6ecff423a0a950ea1d`：5分钟活动窗口解决部分当前市况可见性，不能当12小时历史或跨币资本循环全样本。

**确定性离线规则复算（按Pulse该文件的明确条件模拟，不是运行Pulse）**：

| 同类型Solana早期买入 | 观察到的短时事件 | 此规则能否写入持久交易队列 | 为什么 |
|---|---|---|---|
| 未标记普通地址，买入1 SOL，未看到毕业事件 | 是 | 未满足所读持久化路径 | 非labelled，金额低于5，且未触发`flushEarlyBuyers` |
| 同地址同金额1 SOL，之后收到毕业事件 | 是 | 是 | 缓存的早期买入被`early:graduated`事后回填到交易队列 |
| 未标记普通地址，买入5 SOL | 是 | 是 | 达到`WHALE_SOL=5`阈值 |

**第二项确定性合并规则复算（同样不运行Pulse）：**读取`mergeObservations()`的`snap`字段写入逻辑后，用同一个`solana:MintSample`的两条合法非空观测做互换顺序测试：先来源A`liquidity=1000`再来源B`liquidity=2500`，合并结果1000；先B后A则结果2500。原因是源码对已有非空字段不覆盖，仅填缺失。**不能据此声称实际采集调用顺序随机或错误**；需回查调用方是否按来源可信度/事件时间明确排序。若不回查，一次跨源流动性差异可能被错误解释为市场结构变化。

这一问题与旧Hermes`liquidity_decay_flag`、`net_flow_intensity`、meme-成本/退出机制和Blix报价可信度相连：数据来源优先顺序若不透明，后续比率及机制解释也不能当独立事实。**应保留原始来源、采集时点、有效时点与冲突值**；在本轮无当前调用方核验时标记`SOURCE_PRECEDENCE_UNKNOWN`，而非猜测原作者动机。

**新机制认识（统计学×事件采集×市场经济）**：如果研究者只使用类似Pulse选择性落库的历史交易记录，训练“哪些钱包早期参与的Mint后来更容易毕业”，则**后来毕业影响了谁被保存为历史样本**。此时观察样本的保留概率由未来结果、金额和钱包标签共同决定，不能把“历史记录里没看到”解释成“市场中没有发生”；也不能直接从这类样本估算全体早期钱包的行为分布、异常前兆概率。类似地，Blix24h日志会带来留存窗口截断，覆盖缺口需要另外处理。这不代表Pulse的短时热度计算错误，只是研究问题**超出其采集选择条件**。

**派生的有价值未知**：记录源在历史事件发生时是否就能获取？存在未持久化人群、窗口未满、索引延迟、后来才被补存、标签反向选择等哪类缺失？这与Hermes的字段异常生成、qb的候选钱包筛选、meme的样本外反证是**同一个研究对象的不同层面**。例如“拉升前转账增多”与“只在后来拉升的币中留存早期买家”有不同解释，不能自动互证。

**本轮可验证的主张边界**：上表是从源码规则复算的简化演示，未验证`tradeQueue`真实落库成功、第三方另有的历史来源、其他Pulse模块的runner保存路径；也未核实Blix真实部署中的日志缺口数量。因此结论限定为“该代码路径存在**选择性持久化与结果依赖**”，不能扩大为Pulse整个数据集必然有偏或Blix必然漏掉某次具体转账。

### 9.4 进入Blix：不是装GraphRAG，而是完善原本的调查可证明范围

**具体的知识运用修订**（当前为文档/源码对照，不是已运行功能）：

1. 当AI说“这批Mint的早期同源/协同钱包更常成功”时，**先询问成功与失败的币是否按同一采集规则留存**，有没有后来毕业后补存、标签优先级、关键地址TopN、短时缓存/历史回补差异。没有全样本覆盖时，输出`SELECTION_BIAS_POSSIBLE / COVERAGE_UNKNOWN`而非因果机制结论。
2. 出现真实异常时沿Blix原生的`Coin / Wallet / Journal / Research`现有能力追签名和时间，再按需加载Hermes 00c/00e、qb证据矩阵、meme反例、Pulse采集差异；**不以旧知识已存在或已归D05为停止理由**。
3. 一个新专业知识点应改变**一个可指出的业务判断**，例如“以前报告未见早期买入→现在改为由于选择性落库不能断言未发生”，或者“以前报告同源→现在加上FeePayer/公共服务/TopN覆盖限定”。不产生实质增量时保留原文，不增加永久规则。
4. 先按[ai-d现有实验方案](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md)做源级多案例与独立模型对照，评估**事实正确、漏项、错误身份归因、正确弃答、信息价值、token成本**。如明确出现“跨文档深跳漏检”才试Aider式源符号索引、Contextual BM25/embedding或GraphRAG；不要为了技术先进增加额外架构和订阅成本。

**下一项优先原始核验**：继续纵深读取Pulse`solana-stream.ts`所有落库/队列的调用路径、是否存在其他runner回填、落库故障/回补；对照qb-`source_wallet_bot`跨Mint wallet→Mint的保存偏差与Blix`Journal`缺口语义，然后选同一组合成事件进行跨方案“可得时点/留存/筛选”的静态验收。只有这一关通过，才能把选出的未知机制移交真实只读监控。

> 本节状态：`SOURCE_RESEARCH + CROSS_PROJECT_STATIC_PILOT`；不是`LIVE_VALIDATED`、`MODEL_UPLIFT_VERIFIED`或`DEPLOYED`。引用外部检索与源码是为了具体改变可核查的判断，不预设参考项目必须服务于Blix现有目录。


## 10. 2026-11-07：用此前未分析的 HoldTech 源码检验“AI 发现隐藏变量”

> **为什么选择它**：第9节首次用Pulse“选择性落库/来源优先”发现**观察过程会改变市场统计**。本轮改用先前未进入该静态反例设计的 [HoldTech](https://github.com/co-numina/holdtech) 原始程序，检查**指标名字→实际代码→市场对象→经济解释**是否仍可能发生断裂。目的是试验 ai-d [2026-11-07 问题驱动发现未知](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-problem-driven-unknown-discovery.md) 的研究原则：不局限于“找到与holder同名的功能”，也不假装独立盲测模型。

**源代码版本（Git blob，main读取时）**：
- [`app/api/analyze/route.ts`](https://github.com/co-numina/holdtech/blob/main/app/api/analyze/route.ts)，blob `d55b8270c76cd066d68511e740c3845e59865f3e`：Token Account→Owner、历史签名估龄、池分类、Holder指标；
- [`app/api/deep-scan/route.ts`](https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts)，blob `64440cfe809c58641f2a2e9e2bc4e095b92f945e`：事件Slot聚组、资金溯源、时间线、集中度；
- [`app/api/holder-overlap/route.ts`](https://github.com/co-numina/holdtech/blob/main/app/api/holder-overlap/route.ts)，blob `36fb29b879798d829330fb1733f671ec14e6fbe7`：跨Mint样本持有人集合交集和协调标签。
- 对照 [Blix`server/holderslive.js`](https://github.com/sunshihao001/grok/blob/blix/server/holderslive.js) blob `1baa865384e42bcaba61db66da74babf46589299`、[`server/holders.js`](https://github.com/sunshihao001/grok/blob/blix/server/holders.js) blob `5050a075144993828209340d6013213364bf1849`、[`server/bubblemap.js`](https://github.com/sunshihao001/grok/blob/blix/server/bubblemap.js) blob `75b824e05e16f50e7a89189a7d5a1fb534f1e915`、[`server/wtrack.js`](https://github.com/sunshihao001/grok/blob/blix/server/wtrack.js) blob `c7fec7d9c9e37c9a4aba72a34f207f4485aec84f`，**仅对照相关入口，不声称全模块验收**。
- Solana协议原始依据：[getTokenLargestAccounts只返回20个Token Account](https://solana.com/docs/rpc/http/gettokenlargestaccounts)、[getSignaturesForAddress为从新到旧排序](https://solana.com/docs/rpc/http/getsignaturesforaddress)、[Fee Payer允许第三方代付](https://solana.com/docs/payments/send-payments/payment-processing/fee-abstraction)。

### 10.1 通过源码得到的意外专业发现，而不是给HoldTech贴“Holder产品”标签

**I. 钱包年龄不是Token持有时间（持仓久/钻石手的错误代理）**。
`analyze/route.ts`中 `walletAgeDays = (now - firstTxTime)`，`holdDurationDays`被**直接赋值**为同一个数；`diamondHandsPct`随后统计`holdDurationDays > 2`。即使`firstTxTime`是真正钱包最早活动，也无法推出钱包持有本Mint超过2天。更严重的是其`getWalletInfo()`只取最近1000签名、再试额外最多1000，返回的“最早”是**该窗口最老**，不一定是首次活动；年龄和总交易数都可能被截断影响。

**确定性反例**：合成一个365天前创建/使用的钱包今天刚买入1小时Mint；旧程序报告`holdDurationDays=365`且`diamondHandsPct=100%`（若调查样本只有该人），而真正的Token连续持有时间约0.04天；因此该指标不能作为长持或健康社区的事实。**这不否定“Wallet Age”本身对风险分析可能有价值**，它与Token库存进出的事实必须分开。

**II. “Bundle”按Slot和Fee Payer聚类，不等于买单/同控**。
`deep-scan/route.ts`的 `detectBundles()`接收`SWAP`、`TRANSFER`、`UNKNOWN`三种事件，直接取`t.feePayer`当buyer，若同Slot存在至少3个不同Fee Payer则生成bundle；没有核实该Mint确有Token净买入、SOL对价、交易方向、是否同一Bundle、公共代付或共同平台。**合成同一Slot有3笔互不相关的TRANSFER、三个不同Fee Payer、无买单**，旧函数仍给出一个3钱包Bundle。官方Solana协议允许代付，Fee Payer不是资产实际买方或真实控制人。既有Hermes的同Slot风险假设、qb的关键地址和Blix Bubble Map均应保留此异质证据区分，不能互相把弱关系升级成强共同控制。

**III. 资金来源追溯中出现两个彼此独立的错误前提**。
`traceFundingSource()`调用`getSignaturesForAddress(wallet,{limit:20})`拿到**最近20条**签名，却排序升序、取其中前5条并称为“最早交易”；这是**最近20条中相对较早的5条**，不等于钱包出生时的前5条。合成一钱包30条历史、真实第一笔为`sig1`，程序窗口最老候选是`sig11`。然后把某笔交易目标钱包SOL净增加`>0.01`且Fee Payer非目标的**Fee Payer**当作 `fundedBy`；但同一交易完全允许另一账户支付费用，真正SOL转出者不是Fee Payer。第二个合成例：`SENDER`向`RECEIVER`转入2 SOL、`FEE_SPONSOR`代付手续，旧函数会把`FEE_SPONSOR`写入来源。两问题叠加后，“共同资金父级”可能同时受到历史截断和执行角色混淆。这一认识不只关乎HoldTech，也直接对照Blix`bubblemap.js`中首次funder追溯的Fee Payer回退路径与历史有限页数。

**IV. “200名持有者”参数与真实分页/样本分母不一致，且Owner余额可能丢失**。
`holder-overlap/route.ts`业务调用`getHolders(m,200)`，但内部向供应商请求`limit:1000`，随后一次性把**一整页**写入数组，**只在下轮循环前检查200**。若第一页有1000个正余额Token Account，实际得到1000条，非严格200；如果第1页满足门槛便不取后续。源码注释所称“full holder base”也未得到证明。Owner集合用Set去重，余额Map用`map.set(owner,amount)`，同一Owner多个Token Account时后写入覆盖，而不是求和。合成`Owner W`两个账户余额100、200，显示可被覆盖为200，真正Owner库存应为300。**注意：这不是说跨币集合交集本身绝对错误，而是集合覆盖率、库存数值、TopN经济语义不同**。

**V. 跨Mint“协调严重度”由不完整集合的交集比例驱动，缺少时间与行为因果**。
`holder-overlap`按`shared/observedSetA`和`shared/observedSetB`的百分比算几何平均，再用`>=60`标`CRITICAL`、`>=40`标`HIGH`。合成两Mint各1000个已采样Owner、600交集，则分数60、`CRITICAL`；如果两Mint实际各有20000个不同Owner、同样只有600交集，完整集合占比3，规则变为`NONE`。这种反例只说明**样本分母与覆盖状态可以根本改变分类**；并不证明生产环境普遍只抓1000或生产观测比率的实际方向。更重要的是，即便完整Owner重叠达到60%，也没有证明共同控制、同步交易、前兆或可预测获利。

**VI. 头部Token账户不等于流动性池，过度假定会改变风险指标**。
`analyze/route.ts`先解析`getTokenLargestAccounts`返回的20个Token Account owner，然后**无条件**把`holders[0].owner`加入`poolDetected`，后续计算`humanWallets`时剔除。如果最大Token Account实际上是普通鲸鱼，而非经过协议验证的池/vault，那么它被错误剔除，进而影响Fresh/低活动/集中度分析。官方RPC仅承诺返回金额最大的Token Account，而未承诺榜首一定为池。Blix自己`holderslive.js`对Token Account按Owner**求和**，说明同样任务存在更合适的已实现原生方法；但Blix其他页面/历史仍须分开核实，不借对照称全链无损。

### 10.2 静态离线结果：原始条件复算，不是运行时测试

| 复算的条件或输入 | 复算实际值 | 需要拒绝的过强结论 |
|---|---|---|
| 调用`getHolders(...,200)`，单页1000个非零Token Account | 首次插入1000条，循环结束；`loaded=1000` | “API永远严格只查200个owner” |
| 365天的钱包在此Mint仅持有0.04天 | `holdDurationDays=365`，单人样本`diamondHandsPct=100` | “这个Token持有了365天” |
| 同Slot3个`TRANSFER`、不同Fee Payer、无`SWAP` | `detectBundles`输出1个3钱包Bundle | “3个钱包在同一Slot买入” |
| 1000名采样Owner各币600交集 vs 20000完整Owner仍600交集 | 分数60/`CRITICAL` vs 3/`NONE` | “重叠分数可不看完整覆盖” |
| 一Owner有余额100、200两Token Account | `Map.set`终值200，实际合计300 | “跨Mint重叠表的amount就是Owner总余额” |
| 钱包30个历史签名，窗口仅取最近20 | `sig11`作为最老可选，而真实最早`sig1` | “最近20条中排序最早即历史首次” |
| 实际发SOL者SENDER，另一方FEE_SPONSOR代付 | 净收2 SOL，但`fundedBy=FEE_SPONSOR` | “Fee Payer就是转账出资者” |

以上测试为**根据源码关键分支独立重写的纯逻辑复算**，并非执行原Next.js应用、调用真实Helius API、运行Blix或独立Agent盲测；保留具体源路径与blob可让后续在安全隔离环境对原代码增加真实单测。源码中部分API凭证写法也需要单独安全审查；本次未使用或转载任何凭证。

### 10.3 此轮 ai-d 的真正贡献：暴露“测量对象错位”这一中间机制

从用户普通问题“某Mint有大量疑似捆绑钱包／跨币持有人重叠是不是同一个操盘群体？”出发，若只按功能标签搜索，会停在“Holder/Bundle/Overlap都支持”。但延着**实际观测对象**追溯：

`Token Account → Owner聚合 → Holder样本来源与覆盖 → 持仓时间的真实开始 → Fee Payer/交易资产变化 → 行为Slot/签名 → 多Mint同一实体的竞争解释 → 可能的经济库存机制`

就会发现：`first active`被当`hold duration`、`same-slot fee-payer`被当`same-slot buy`、`sample overlap`被当`coordinated group`、`fee payer`被当`funding origin`。它们都是**名称/实现观测量/经济概念的错位**，并不靠增加固定专家数来发现。

这也表明需要更精确地区分**观察偏差**（只记录一部分）、**代理变量失效**（钱包年龄≠持有时长）、**角色误归因**（Fee Payer≠买入者/转账出资者）、**分母/聚合错误**（Token Account余额未汇总或重叠覆盖不足）、**经济机制未识别**（可见相关不等于同一控制主体）。这些是不同的错误机制，有不同修复/证据路径，而不是重新发明一组信号标签。

**跨项目对Blix实用判断**：
1. **只复用有依据的业务形态**：HoldTech的Holder/深度扫描/跨Mint交集UI和原始API流程，能提示Blix要测试哪些问题，但当前不能原样继承其`diamondHandsPct`、`fundedBy`、`bundle`、`coordination`为链上经济真值。
2. **保留Blix已有较强原生功能，不因外部“成熟”而重写**：`holderslive.js`中`owners.set(owner, old+amount)`的Owner聚合、`journal.js`的去重与Gap概念、`bubblemap.js`的公共Hub排除，值得优先复用；但Bubble Map追踪的Fee Payer和历史截断也要按相同证据标准审查。
3. **研究价值与交易价值分开**：同Slot/跨MintOwner交集可以是“值得只读调查”的线索，不自动是“捆绑操纵/可以买/可复制”证据。
4. **下一项最有价值的验证**：用同一Mint的准确Owner汇总和两次冻结Slot快照，分别计算完整覆盖与TopN的跨Mint交集，另把同Slot`TRANSFER`、真实买入`SWAP`、第三方代付作为互斥验证案例；研究谁被漏、谁被误命名、哪些对经济库存/资本循环的解释仍然UNKNOWN。
5. **后续新增未知知识的兼容机制**：从任何未读参考项目发现的新对象/学科，应在原来源保留版本与完整背景，先寻找它**改变哪个市场观察变量或竞争解释**，再进入Blix调查要求或离线反例；没有适用依据时允许保留为开放研究，不能强塞现有D类或无差别复制代码。

### 10.4 对“真正盲测”的诚实界限

HoldTech在这轮研究前没有作为此前Pulse/Hermes合成反例的原始材料使用，**可作为新的源级诊断**。但同一个研究者/AI现在已经看过HoldTech源码并得知反例，**不能把这七组源码演示再称为隔离的盲评模型测试**。未来必须冻结未见源码/真实任务、工具预算与答案评分器，另用隔离上下文测试ai-d的不同问题表征是否比普通词面检索可靠。此处完成的是`SOURCE_REVIEWED + OFFLINE_BRANCH_REPRODUCED`；`MODEL_AB=NOT_RUN`、`HOLDTECH_RUNTIME=NOT_RUN`、`BLIX_LIVE=NOT_RUN`、`NEW_ECONOMIC_MECHANISM_CONFIRMED=NO`。



## 11｜2026-11-07 跨全市场与 AI 的双重反馈：从数据选择到经济机制与判断修订

> **本节的核心是研究对象升级，不是又扩展一份专家名单**。审查的统一问题：**一个Solana Meme市场系统怎样从完整现实的发行与参与者互动中获得有限、带选择的数据，形成经济解释与市场关注决定，再被实际结果反馈影响；怎样避免反馈越多、认知反而越窄？** 这同时连接市场经济学/微观结构、统计选择机制、链上资产取证、竞争性策略、AI自主研究、产品可观测性和用户价值。不能把分析简化为“发现某个钱包异常”；也不能宣称已证明普遍市场定律。
>
> **实际原始材料**：Blix 当前 blix 分支的 server/engine.js、server/research.js、server/brain.js；Pulse src/collector/solana-stream.ts、scheduler.ts、merge.ts、archive/restore.ts；Million apps/api/src/opportunities/opportunities.service.ts 与 copyability/copyability.service.ts；PumpTrace src/modules/trust-engine/analyze.mjs、interpretation-engine/analyze.mjs；PumpGrok ARCHITECTURE.md；Why-Solana docs/PITFALLS.md 与 README；旧Hermes的资金/筹码方法、qb-的调查证据资产、meme-的价格/库存假说；ai-d main 的问题驱动未知发现、完整系统评估和短意图研究。公开学术证据另核2026年9–10月论文原始页面。**当前状态：源码定向深读＋来源交叉综合；未安装第三方成品、未重跑主网签名、未运行Blix AI、自适应策略回测或独立盲评。**

### 11.1 两个相互影响的过程：市场如何生成事实，系统如何生成“看见的市场”

**真实市场过程**：发行者/平台规则、早期持有人、套利执行者、LP/做市、普通买家、信息传播者具有不同目标和成本 → 投入SOL/Token、改变池储备与交易排序、影响公开信息和预期 → 其他行动者响应、价格/库存/成交与发行阶段继续变化 → 有些行动者退出、回收或在下个Mint重复。平台的Creator费与LP费使“成交量激励”可能不同于“Token涨价收益”；同一角色的策略也可能随阶段转换。该描述是综合性机制模型，不是对特定钱包动机的事实认定。

**系统认知过程**：真实事件 → 由不同协议/供应商/订阅条件形成可见对象 → 过滤、排队、持久化、错过/重试 → 分析钱包/池/资金事实 → AI生成候选机制与关注优先级 → 随后用结果评估表现 → 修改规则与研究重点。**这条链的任一选择都会改变系统最终认为“有哪些市场规律”。**

强推论：研究对象不能只定义成“钱包行为图”；还要理解**观察机制与市场行为机制的交互**。例如看到“成功币中早期买入者经常重复出现”，可能是真实经济组织，也可能包含“只有成功币才被补存早期买家”的选择过程；两者可以并存。正确研究应主动同时考察两条生成过程，而不是用一个否定另一个。

可以把理解性的统计关系表达为：研究看到的样本 = 实际事件 × 采集覆盖 × 筛选/留存规则 × 查询窗口 × 可得时点（这不是可直接计算的乘法式）。对市场结果Y，观察到的 E[Y | 被采集且入选] 未必等于全市场 E[Y]，也不必然等于观察者在当时可执行时的结果。

### 11.2 同一完整业务的跨项目实证对照——更深于README功能表

| 全市场需要解决的问题 | 原代码/文档中找到的具体实现事实 | 它揭示的知识或真正不足 | 对Blix的正确综合方向 |
| --- | --- | --- | --- |
| **怎样知道哪些发行真实进入视野？** | Blix server/engine.js 的 nursery 在约4分钟后按DEX行情、5分钟量/市值阈值决定是否 adopt；未获得pair的对象在该次循环中continue，随后的 active cull 又按币龄、成交和分数等退场；代码另有发行回补和新池发现补漏 | **入选对象是被多阶段筛选后的样本**，但Blix并非完全没有回补；“没进榜/没获AI研究”与“市场没发生”不能合并 | 保留原发现/回补引擎，调查漏报时并列保存发射源、队列结果、过滤原因、可得时点与后续是否恢复，不能因某规则被过滤而失去长期研究机会 |
| **怎样给历史样本真正的分母？** | Pulse solana-stream.ts 把早期买家暂存内存，最多前40位不同钱包；token毕业或达到runner条件才 flushEarlyBuyers 历史入库；另有标记钱包及≥5 SOL交易入库；scheduler.ts 的生命周期/市场快照是另一种不同口径，merge.ts 遇多源数据按输入顺序优先已有非空字段、source拼接而非逐字段来源 | **“统计市场热度”和“保存可研究的完整交易”不是一回事**。以毕业后的留存样本训练“谁能预测毕业”，存在未来结果反向选择历史事件的风险；混合来源也可能失去字段时间/源细粒度 | 保留Pulse的历史存储/归档成熟经验，但因题设不同要采用不同事件全集，保存采集规则版本和每字段来源；仅凭历史trade表不可宣称全体钱包行为 |
| **怎样判断协同还是服务/市场共因？** | PumpTrace trust-engine 源码区别可交易Holder与池/销毁/程序账户、Creator直连、同交易和资金共同来源，给出不同证据等级；但部分flag的证据等级通过title字符串匹配确定，riskScore还包含静态权重。旧Hermes与Why-Solana提醒同源/同Slot不等于同控 | **证据等级不等于概率或经济主体身份**。同一相关网络可能包含Creator资本组织、服务设施、独立执行者和公开注意力；还须核实际SOL/Token流、账户权利、LP/Token对价 | 复用PumpTrace的Creator历史/角色与跟踪证据流程，不把分数或文字映射等级直接改成Blix的交易真值；可以积极标为候选监控、随后按区分性证据升级 |
| **找到异常之后，它对使用者有什么价值？** | Million opportunities.service.ts 记录skip、阻断原因、禁用守卫“本会阻断”以及多个异议；copyability.service.ts 用鲸鱼买卖时间与滞后后的分钟K线做方向性可跟随测量，只对满足已平仓/可得K线的样本计算；Why-Solana PITFALLS.md将历史Peak、未来选样、虚假分母、时滞与可交易退出分开校核 | **检测到结构、当时可知道、其他人可执行、事后可盈利，是四种不同的命题**。Million的“wouldBlock”是同一数据的观察性比较，不能自动视为随机因果试验；分钟线收益不能证明真实订单已成交 | 整体借鉴其“记录为何跳过、也检查被错过的机会”能力，优先用Blix现有paper/信号日志对照；研究问题不能只问成功率，要问延迟、成本、真实流动性和可执行资产规模 |
| **AI 会因为反馈变得更聪明还是更加封闭？** | Blix research.js trimQueue 会让超时/容量不足的AI研究任务过期，过期状态24小时后清理；brain.js scorecard() 的研究组选择条件是 outcomes kind='grade' 且有grade并成熟；review() 在这批已评级结果中取 bestRunners、worstDumps、highGradesThatFailed 和 missedRunners；新的Playbook写入数据库，playbookPrompt()进入后续提示词 | **最重要的新增源级发现**：Blix的“missedRunners”实际只包含“已被AI研究但分低”的跑赢币，**不包含从未被队列选中、从未评级的Mint**。自我评测与自我修改共享一条选择后的样本链，存在“只在看过的市场里学习”的潜在偏差。当前只确认源码路径，不声称已测出偏差大小 | **不要废弃自我修订**；补足独立于AI评级/Playbook的市场机会分母和未入选结果，记录规则版本及信号当时是否可见。冻结旧版本与可得历史后才能比较新规则是否真正改善召回/误报/经济解释 |
| **AI是否知道研究已完成？** | PumpGrok ARCHITECTURE.md 中带来源/UTC的Lead→Risk→Ticket与权限分离说明“团队流程与底层引擎”两件事；其 scout pipeline 被文档明确标未实现。ai-d已核过Open Deep Research的结束异常、DeerFlow未达目标而循环结束的反例 | **任务关闭、报告写好、插件已声明、工具真正能工作、市场结论已验证**是不同完成对象 | Blix应继续使用已有工程及ai-d按需方法：对用户自然语言能直达完成的只读任务，不强制多专家/多Bot；是否真的调用、读对和修改正确由追溯日志与实际结果核验 |

**完整业务联系**：同一条“今天有哪些异常筹码群体、是否值得看、为什么”的真实任务，从覆盖问题开始、穿过链上事实/市场行为、到机制/机会/风险分歧，再到后续验证并修正AI判断。不同成品各有强项，但**没有任何一个参考README、单一钱包图或纯评分器独自证明已覆盖完整链路**。Blix已拥有相当多的现成UI/数据/学习组件，首要是正确重组其认识，不是再复制一个前端。

### 11.3 四项跨源后才出现、之前从单仓局部问题看不出的专业问题

**A. 可观测性差异本身可能伪装成市场竞争机制。** 同一个Mint在Blix、Pulse、独立筛选器里有不同入选与持久化命运。一项2026年9月修订的跨观察系统原始研究，在覆盖完整的17.5天比较窗口内报告两条数据管线分别识别623和1742个Mint、交集仅5个；论文作者据此主张比较collector coverage与overlap，而非仅信任单一采集。**研究适用范围是该论文两条特定配置管线，不等于Blix/Pulse之间实际测得同样比例。** 原始来源：[arXiv:2609.18975 v2，2026-09-23](https://arxiv.org/abs/2609.18975)，附有可再计算数据/脚本DOI。对Blix的反问因此变成：我们的“全市场异常率/先于拉盘的预警率”究竟以谁的Mint全集为分母？若连两条独立pipeline的交集都没查，异常比例可能首先是观察器产物。

**B. 战略行动者也会主动制造、规避或利用“被系统看到的指标”。** [Meme Coin Factories，arXiv:2609.10246](https://arxiv.org/abs/2609.10246) 在大规模研究中报告wash trading、Creator混淆、协调卖出、copycat、社交操纵及第三方操纵服务；[UCL 2025 meme市场工作论文](https://discovery.ucl.ac.uk/id/eprint/10220651/)用6000个Meme的交易与评论研究隐藏性积累与制造关注等多种行为，支持**资金/库存与注意力可以同时成为策略对象**。因此“过去某个指标与上涨相关”在市场参与者学习了筛选规则后未必保持稳定。这是研究“指标作为战略目标被游戏化”的**可检验机制候选**，不能断定已有参与者专门针对Blix作弊。真实区分路径需看发行者是否通过链上资本成本、实际交易和公开信息行为构成前后可比较的策略变化。

**C. 系统自我改规则可能把选择偏差扩大成自我确认。** 独立于加密研究，2026年10月PNAS论文[The more you automate, the less you see](https://pmc.ncbi.nlm.nih.gov/articles/PMC13663820/)在两个开源AI科学家系统的受控试验中发现基准选择、未披露合成/抽样处理、指标偏移和事后优选报告等问题，强调必须审计完整工作流产物。**不能把其试验效应直接移植给Blix**，但与Blix“被选中才评级/评级才学习”的源码结构产生重要联系：证明“AI Playbook更新了”需要完整采样轨迹与独立对照，而不是模型自己总结最好/最差样本后宣布知识进化。

**D. 旧研究“数值已撤回”会改变当前知识的可信级别。** [RED-COHORT arXiv:2607.02795 v4，2026-10-05](https://arxiv.org/abs/2607.02795) 的作者**明确在摘要第一句和论文说明中撤回所有数值结果**：被当作买方的记录含卖出并遗漏大量真实买入。论文旧摘要中仍陈列1012群/16.1%等历史数字，但**不得取这些数字继续为“cohort导致后续买家增长”作支持，也不得把其匹配效应当已成立**。保留研究问题、设计和失败教训，数值与对应推论降级至WITHDRAWN_PENDING_CORRECTION。此事比再强调“结果可能有偏差”严重得多：**研究输入的事件语义本身已被作者否定**。同类失败直接指向Blix/Million/PumpTrace等任何把Swap/CPI/transfer/买卖字段合成交易方向的流程，先核经济动作，再作统计和经济解释。

### 11.4 把“深度”具体化：六个必须可区分的专业命题，不是六个强制阶段

同一现象如“拉升前某批钱包注资，若干Mint重复”，至少存在六个逻辑不同的主张，可按当下任务选取最重要的一个去实证：

1. **存在性**：这些签名/Token Account/SOL或Token的变化是否真的发生？需要原始交易、可得时间、池及账户权利。
2. **关联性**：钱包群体重复共现是否高于与发行阶段、活跃度和总体市场热度相匹配的正常背景？需要完整分母/负例与独立基线。
3. **组织性**：是否有直接资金/库存接力、回收权或重复执行模板？共享服务、自动化软件和同一公告可能同时解释关系；不迫使确认最终真人。
4. **经济性**：谁的库存成本、费用与净收益受益？Creator费、LP收入、套利、卖出对价和外部注意力未必落在同一个钱包。
5. **时序信息价值**：外部观察者何时真正知道？事件发现、数据补采、模型评判、通知和执行存在延迟；事后回填不能伪造事前优势。
6. **适应性/可用性**：群体是否更改策略、市场机制是否失效、采集系统是否变了；AI修改知识后是否在**未参与修订的时段/对象**上改善判断？

这些命题不是依次回答完才能研究市场，也不是专家投票。**支持“值得关注”的证据门槛低于“确定同一实控人”与“存在可交易净优势”**；每项需要证据，竞争解释也须有具体鉴别力，不以一种理论上可能的反例把所有线索否决。

### 11.5 一次反向贯通任务：同一个普通问题应怎样改变AI所做的研究

用户说：**“市场里一组钱包在多币首发前后行为很像，为什么，能提前看到下一个吗？”**

浅层方案：查聪明钱列表→按同Slot/共享Funder聚类→生成分数→告诉用户可跟单。**问题**：它忽略真实交易方向、谁被采集、被过滤对象、早知道的必要条件、实际可执行价格与相互独立的盈利目的。

经本轮跨项目修正后的专业问题是：**在明确的发行机会全集与采集窗口内，是否存在一个在事件可见时已经可以定义的钱包群体；其真实资金/Token库存组织和执行模式，相对于其他同类发币是否更特殊；若变化前就识别，能否对之后的资金、群体构成和市场反应产生可区分的预测；这是否真的帮助当前目标的市场监控，还是只帮助事后解释？**

- 市场发现视角来自Blix+Pulse+pumpwatch：定位哪些Mint曾进入视野、哪些后补入、哪些从未保存，取同类背景。
- 资金/组织视角来自PumpTrace+Million+Hermes/qb+Why-Solana：从实际SOL/Token/Swap/转仓/接收卖出+公共Hub区分策略组织，不只聚地址。
- 经济学/微观结构来自meme+UCL/Meme Factories：比较隐藏性积累、独立抢跑、做市/价差、交易活跃度制造、Creator费用收益、公开关注引发的共同反应；允许两种以上机制同时存在。
- 决策与反馈来自Million+Blix+ai-d：明确当时可得事实、看哪个变化会升级观察，记录拒绝/错过及后续结果，阶段性积极判断，之后修正对应机制而不是改写历史事实。
- 工程/治理来自Blix现有SQLite和报告、Pulse恢复、PumpGrok票据与ai-d：完整原始证据和运行状态分开，保护只读及权限边界，不因为“模型形成假设”就触发交易、付款或签名。

**完成一轮高价值研究的界限**：不是文本足够长，而是此任务至少改变了一个之前遗漏的机制/分母/鉴别证据/产品决定；其余远端未知留下可恢复的原始来源，并将可授权的下一项证据核查执行或说明阻塞。对于当前案例，最好先补“从发现/筛选/排队到评级及结果跟踪”的**被丢弃对象记录与信息可得性**，并继续用真实Mint的Swap/LP原始交易作市场生成机制对照；不要先开发新的模型人格或全链索引器。

### 11.6 本轮对现有知识与产品方向的实际裁决

**认知层面**：从“钱包网络 + 市场异常 + AI解释”升级为**市场参与者策略生成过程 × 数据观察与选择过程 × AI判断与反向学习过程**。这三个对象不断互动，任何单一README或代码函数无法取代完整解释。新认识以原有D01/D03/D04/D05/D06/D07/D08/D10/D11/D12跨域方式收录，不新造第13域或固定专家制度。

**Blix已有可复用的真实基础**：发现、回补、过滤、研究队列、结果追踪、Playbook、钱包和数据源模块都已在源码中存在；问题是其“市场样本/获AI研究样本/追踪成熟样本/真实可执行机会全集”之间尚未形成可检验的全链路关联。应优先在既有产品路径上按事件上下文核验，不把源码存在直接等同线上稳定运行。

**有价值的独立参考项目知识继续保留**：Pulse的长期归档与来源差异，Million的全异议/跳过记录和延迟测量，PumpTrace的Creator/Holder证据分层，Why-Solana的反例与失效研究，pumpwatch的发行整体基线，PumpGrok的票据/安全职责，Hermes/qb/meme的经济筹码与问题生长，以及ai-d的目标/未知/知识选择和研究验收；每项研究仍保留其自身原始目的、尚未审阅的源码和业务，不能因为本节用了部分源就标记“全仓已读完”。

**验收状态**：本轮为跨仓原始代码观察、学术源纠偏与新的系统级竞争性解释。新实证中只有已公开的归档/论文作者结果及我们能够由源码确定的控制条件；**没有**当前Blix的独立采集覆盖测试、同Mint真实Swap+LP对账、模型A/B实验、线上成功率、交易收益或自我反馈策略改善证明。


## 11. 2026-11-07｜整套市场智能系统的深层机制：从多主体市场、可观测性到判断修订

> **研究缘起**：用户明确指出，过去按小问题/关键词/仓库功能逐个回答，无法真正理解整个Meme项目；已搭建的六类目录、L0–L7、D01–D12、G0–G4和六种产品价值目的有用，但**问题表征深度、跨项目中间机制、真实市场对象及AI自我纠错的联系**仍不足。本节不再建新本体、固定专家或Bot，而从**完整市场形成—数据被观测—产品筛选—专业判断—行动可得性—新事实修订**重新检验原参考项目。以下源码属于当前定向阅读与历史审查的组合；没有将全部库逐文件审完、没有安装任何第三方产品、没有做新真实链上交易回放。项目文件SHA为本轮读取时原始证据，不应误称为长期固定版本。

### 11.1 五种不同的对象与一个完整市场过程，不是五个新模块

1. **市场本身**：发行与交易规则、参与者可能的目的和资源、SOL/Token/LP/手续费权利、公开注意力、交易次序、价格/库存变化、市场生命周期；市场参与者的真实目标是无法直接读取的隐变量。
2. **原始链上事件**：签名、指令/CPI、资产真实变化、Token Account及其Owner/Authority、Fee Payer、池与多种报价资产；可见地址行为不等于经济受益主体或实际交易盈利。
3. **观测系统生成的数据**：谁被接入、哪些链上程序被听到、哪些池能解析、什么被缓存/选择性保存、何时可得、是否断流、同一事实不同来源如何冲突；这些规则决定AI能“看见的市场”。
4. **决策系统的选择**：triage、钱包评分、风险/机会过滤、资金关系图、历史回看、专家研究报告、AI playbook等；选择何者进一步分析本身是有代价的**行动**，不是市场客观属性。
5. **后续有效性**：观察是否足够早、解释是否区分竞争机制、历史模式是否持续、使用者是否能以实际池深/延时/费率/报价路径行动、被拒或没看到的样本后来如何表现。

**更成熟的整体问题不是“这币是不是庄家盘？”而是：哪个角色在何种制度/信息/资金/库存约束下采取了什么行为，行为经什么市场和数据机制成为我们看到的信号，这个信号足以支持哪种目标下的阶段性判断；新事件出现后判断应具体改变哪里？** 这将D02发行、D03微结构、D04钱包、D05资金、D06库存、D07群体、D08机会、D09执行、D10工程、D11证据与D12 AI联成可循环的知识关系。**不是每次必须走十二域**。

### 11.2 多项目源码恢复其独有问题，不把作者的产品愿景当已证明的真相

| 原项目及本轮精确源码 | 其原问题真正要解决什么 | 当前源码可直接观察的处理 | 不能推成什么 |
| --- | --- | --- | --- |
| [Blix triage](../../server/triage.js)、[coverage](../../server/coverage.js)、[journal](../../server/journal.js) | 大量新币如何低成本先看、再在真正出现交易活动时补救漏选，并留下短期交易时序 | triage首先按规则/LLM处理新币；即使低标签，当真实不同交易者达阈值仍可升级；coverage 以滚动5分钟补充可能被Pulse列遗漏的活跃币；journal的交易保留期24h并记录断流与维修语义 | 短期可见和回放不等于整个市场历史、完整资金图；作者注释中历史19/79漏列不是本轮独立复测 |
| [Pulse Solana stream](https://github.com/nirholas/pulse/blob/main/src/collector/solana-stream.ts)、[merge](https://github.com/nirholas/pulse/blob/main/src/collector/merge.ts)、[restore](https://github.com/nirholas/pulse/blob/main/src/archive/restore.ts) | 既实时观察发行又永久留住有研究价值的交易与生命周期 | 流里按Mint累计滚动热度；原始交易仅在钱包已标记、单笔不少于5SOL、或前40早买者且后来毕业/跑出时留存；多来源观测采用先填值、后来源补空位；归档按可变表upsert、非可变表保留原始事件 | 完整发行记录≠全量成交真源；已毕业币的早买样本会有**事后结果筛选**；“第一可用字段”不代表字段最新或最可靠 |
| [Million discovery](https://github.com/Kelows/million/blob/main/apps/api/src/discovery/discovery.service.ts)、[opportunity](https://github.com/Kelows/million/blob/main/apps/api/src/opportunities/opportunities.service.ts)、[copyability](https://github.com/Kelows/million/blob/main/apps/api/src/copyability/copyability.service.ts)、[owners](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/owners.service.ts) | 从钱包找到币、从币找别的钱包，再判断“跟得上、能执行、有没有跟随价值” | 资金余额变化优先于只看路由地址；钱包与Token双向发现；事件被拒原因、全部阻断原因和影子反事实记录；将鲸鱼当分钟成交与60秒后跟随的价格对比；Owner候选聚类排除高连接Hub且不以co-entry作为union桥 | 60秒是假设时延，不证明实际Webhook/API/路由延迟；分钟价格不是成交保证；Owner ID为重建生成的启发式群，不是本人 |
| [PumpTrace methodology](https://github.com/AntC215/Pumptrace/blob/main/docs/METHODOLOGY.md)、[backfill](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs) | 让用户查Creator/钱包之前反复做过什么及下一步监控谁 | 把原始事实、派生指标、解释与证据强度分层；Creator要有可支持create指令；分开当前余额、抽样SOL流、卖出总收入与可确认成本的PNL；可恢复/限流/暂停/最大抓取量等历史工作状态分开 | 高评分不是欺诈概率；历史任务COMPLETE只代表所选窗口完成，不是全链全历史；关系真实也不证明共同所有 |
| [HoldTech deep scan](https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts)、[overlap](https://github.com/co-numina/holdtech/blob/main/app/api/holder-overlap/route.ts) | 评估可见持有人“多而分散”是不是有更深的集中/关联结构 | 已在本研究第10节从源码证实：同Slot普通Transfer可能计Bundle，最近20签名误当最早资金史，Fee Payer误当出资人，样本Overlap分母及Owner多Token Account覆盖有误 | **研究方向有效、特定结论条件不足**；不能因此排除其整体Holder UI与集中度观察经验。源码中亦存在硬编码供应商凭据风险，代码复用前应独立审查密钥与依赖，不复制任何密钥 |
| [pumpwatch detector](https://github.com/cinder-security/pumpwatch/blob/main/code/pump_watch.py)、[outcome tracker](https://github.com/cinder-security/pumpwatch/blob/main/code/outcome_tracker.py)、[paper](https://github.com/cinder-security/pumpwatch/blob/main/README.md) | 将工业化发行的常态与极端行为量化、冻结并复算 | 监听发行后取创建交易及曲线；失败重试；结果抓取在代币0–4h约每分钟、4–24h约每30分钟、24–72h约6小时、其后逐日，超过一定年龄可能停止主动访问 | 越晚的数据**时间分辨率越低**；不能把晚期未看到的瞬时高点直接当从未发生或拿不同年龄组作同精度比较 |
| [Why-Solana Act IV](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/ACT_IV.md) | 反问：结构与协同网络已经证实，后来者是否仍能获利？ | 作者在其特定探测器已触发的发行样本里区分结构信号、可预测结果与扣成本后的执行收益；承认相关规则的样本外失败及试验功效限制 | 作者的结论只适用于该探测器、时段和费用/退出策略；不能说市场永远无Alpha，也不能把团体存在直接升格为“马上跟着买” |
| [PumpGrok README](https://github.com/swcstudiospace/PumpGrok/blob/main/README.md)、[OKX onchainos Skills README](https://github.com/okx/onchainos-skills/blob/main/README.md) | AI自然语言多职责研究与安全任务票据；成品市场信息与钱包/交易服务工作流 | PumpGrok README明示35个skills、scout pipeline尚未实现且paper命令部分拒绝；OKX明确只读市场Skill与交易、钱包、支付Skill分离 | 多角色、技能数多不等于真正拥有Blix市场数据覆盖；外部仓库包含交易/付费动作不代表项目已授权自动执行 |
| [旧Hermes Gate理论](https://github.com/sunshihao001/-/blob/main/learning/16-Gate决策框架理论基石.md)、[筹码状态](https://github.com/sunshihao001/-/blob/main/design/Skill4-%E7%AD%B9%E7%A0%81%E6%8E%A7%E5%88%B6%E6%9D%83%E7%8A%B6%E6%80%81%E5%B1%82%E8%AE%BE%E8%AE%A1.md)、[meme真源](https://github.com/sunshihao001/meme-/blob/main/SOURCE_OF_TRUTH.md) | 区分“世界是什么结构”与“人/系统选择做什么”；研究筹码状态、决策时间有效性与策略知识真源 | 原Hermes理论把L2结构、Gate行动、证据TTL和决策TTL分开；筹码有建立/维持/转移/崩塌等**待验证的概念状态**；meme将规则、策略定义、资料与工作流真源分开 | 历史硬阈值、同控权重、伪精确状态概率、旧多Agent建议不能直接迁为真实市场标签或自动指令 |

**整套参考项目的互补不是“分别负责一个页面”**：Blix实际雷达与UI作为用户入口；Pulse/pumpwatch补充时间维度和观察分母；Million补钱包↔币双向探索及被拒机会的反事实；PumpTrace补历史完整性/Creator角色/证据表达；HoldTech给集中与群体调查问题但指标需核原义；Why-Solana负责结构与经济优势的拆分；Hermes/qb-/meme-提供过去长时间积累的资本、库存、状态与失败假设；ai-d补目标、遗漏领域、知识选择、动态专业判断与交付纠错。**是否整用或借鉴，由真实数据可达、许可证、成本、安全和维护决定，不自动融合全部程序。**

### 11.3 第一个跨项目新认识：被选中、被保存和被用于训练/回顾的不是同一总体

**完整因果候选链**（研究推论，非已实测产品影响）：

真实发行与交易全集 → 接入协议/程序与可得区间 → 内存观测与识别 → 保存策略 → Blix triage/某来源的风险过滤 → Million式机会门控/研究对象挑选 → 结果回收/Playbook更新。

任一阶段都可能发生**结果依赖选择、幸存者/左截断、来源失灵、采样年龄差异、模型自身评分选择、无法观测的反事实**：

- Pulse明确只对后来毕业/跑出的币回填前40早买者永久记录，因此“成功币早期买家有什么特点”可以研究；但若据此估计“所有早买者后来成功的概率”，分母被改变，需要原始全体发行与失败对照。
- pumpwatch的年龄分层查询能节约RPC，但“历史峰值/沉默/退出”在稀疏回访的时期可能不可同精度观察；将某些未见峰值当负例会引入观测过程偏差。
- Blix triage的早期标签随真实交易活跃度可升级，避免过于僵硬，这是有价值的**反馈设计**；但其一小时后评估和筛选数据仍依赖当前观测的coin集合，不能用已显示在UI的成品候选取代全市场机会全集。
- Million在机会门控保留skip、wouldBlock、objections以及部分shadow，比纯“买成功再看PnL”更接近反事实研究；但只有进入门控的事件才可能产生该类记录。**影子样本≠所有未被发现的Mint**，不同被拒条件之间也需要避免样本重叠。
- Blix brain已有scorecard与playbook复写功能源码，不等于已在当前环境可靠运行。若回顾只覆盖入选的币，模型会反复强化自己曾选中的样本特性；必须核具体样本进入与后续结果的条件。

**更高价值的新问题**：不是“怎么提高命中率”，而是**现在这个命中率对哪个机会全集、哪些被看见与被跳过对象、在何时可得的信息条件下成立？** 它连接市场发现、统计因果、数据采集、机会成本和AI知识污染。反过来，候选没有达到正式归因标准仍可被低成本只读观察，不必让保守过滤器导致所有新型机制消失。

### 11.4 第二个跨项目新认识：不同参与者是用不同收益函数参与同一个市场

**从交易价格转向利益与权利流**：发行者/Creator可能同时考虑Token售价、Creator fee、品牌和后续发行；LP考虑费用与两端库存风险；短线Sniper追求更早入场/低延时退出；套利/路由服务追价差及执行收益；普通买家/社群追价格、娱乐、信息或身份；资本组织者可能把多地址用于分发、执行或退出；平台与数据服务商还有自己的收费和产品激励。**这些只是待对照的经济目标候选，不是对具体地址的身份和意图断言**。

- [Pump.fun官方费率](https://pump.fun/docs/fees)于2026-10引入前端/移动端Platform Fee，且说明Creator fee、Protocol fee、LP fee与不同交易途径、配对资产、Canonical Pool、Holder Rewards等条件相关：**发行者收益、买卖者成本、平台收益可能不是同一种经济函数，执行入口不同会改变可复制性**。任何具体历史时段的成本需按当时链上合约/路线核实，不能把当前网页费率追溯到过去。
- [USENIX Security 2026，A Midsummer Meme's Dream](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini)在其跨链样本描述刷量与薄池价格膨胀(LPI)及随后收益提取机制。这个来源支持“价涨、量大、表面人气可能来自不同生成机制”的调查方向；其82.89%是**所研究的高回报子样本**中被规则标为操纵迹象的比例，不能投射为全体新币欺诈概率。
- [Meme Coin Factories 2026](https://arxiv.org/abs/2609.10246)考察wash trading、Creator混淆、协同售卖、模仿币、社交操纵与服务化工具，进一步表明参与者可以利用**被他人观察的信号**来影响后续行为。这支持“信息和可见交易活动也可能成为策略工具”，不等于每个高热度Token由同一方操纵。
- [Demystifying Solana Bots 2026](https://arxiv.org/abs/2607.28424)结合586个机器人源码和200个地址、逾4400万交易观察，表明**相似链上行为可能由不同执行类机器人实现**。这为“同Slot/相同频率≠同一控制”提供了跨研究方法支持；原文分类不直接确认特定地址类型。

**新机制候选A：成交/关注收益与代币价差收益分离。** 如果有人从交易费、推广和流量中获得收益，价格长期上涨未必是其唯一目标；同一个异常量价结构可由真实买卖、做市、刷量、薄池价格冲击或多者混合造成。区分方法需要真实手续费归属、Quote/Token净变化、LP份额、交互地址、市场阶段与传播时序，而非只看“前10Holder”或K线。

**新机制候选B：目标相互作用产生内生策略。** 早买者的进入和退出改变池深与后来的价格；公开看到抢跑信号的后来者，又改变早买者可退出的需求；套利和公共路由改变表面钱包同步性；市场参与者在有监控工具后可能调整行为。这里“反身性/适应”是**研究假设**，不能由单次价格变动证明。

### 11.5 第三个跨项目新认识：真实协同结构、阶段性解释和可复制机会必须是三个不同的研究主张

已有旧Hermes模型擅长追钱包和资金关联，但其某些GMGN字段与概率阈值并未经真实样本校准；HoldTech某些同Slot/funder指标甚至在代码层改变了测量对象。Why-Solana的Act IV反过来说明：在某段研究时窗中，**一组协同抢先买入确实存在**，但其事后被看见的群体结构**未提供足够早、扣成本后可交易的优势**；作者亦披露其训练/验证样本边界。

结合Million的60秒跟随假设与PumpTrace的证据分层，可将三项主张分别调查：
1. **描述性结构是否真实**：谁在交易、资金和Token如何流、是否存在时间上重复的同组、池/服务地址是否污染、原始签名能否支持观察。
2. **经济机制是否值得倾向判断**：不同目标/约束下为何会出现这种结构，是资本分发、正常执行、信息抢先、LP管理还是混合；哪个新增事实能够提升/降级解释。
3. **是否有可采取的市场优势**：该线索在公开可得时刻之后还有什么变化？用户实际见到它所需延时、池深、佣金、滑点、失败/抢跑率、卖出能力及机会成本如何？不因前两项真就自动承诺第三项。

以[RED-COHORT 2026](https://arxiv.org/abs/2607.02795)为反例：共现群组和后续活跃买盘有很强表面关联，但作者的**钱包活跃度匹配安慰剂**产生比真实群组更强的关联，挑战“群组本身产生了买盘”的解释。即使独立多源确认真实协同，仍要审查本身就爱交易热门Mint的**选择效应**。该研究并未否认所有协同群体存在，也未直接证明绝无预测价值。

**行动门槛根据主张类型而变，不是一个永恒“真/假”Gate**：较弱但来源可靠的异常可以触发只读监控；要把几钱包归为同控或标记违法，需要更强身份/权益证据；要说有净交易优势，需历史前置冻结+真实执行成本或前瞻性测试。证据不足时可以有“暂时更倾向哪种经济机制”而不必机械拒答。

### 11.6 第四个跨项目新认识：数据与系统的“时间”不是一个钟

**至少要区分**事件实际上链时间、供应商/索引系统首次可得时间、Blix/AI首次看见时间、判断形成时间、用户有条件执行时间、事后回放读取时间、证据或判断过期时间。

- PumpTrace可恢复历史扫描的COMPLETE表示查询区间和上限的状态，不代表所有历史对AI都已**实时可见**。
- Pulse的早期买者可能在后来毕业时才补记，记录event_ts很早，不意味着当时的成品研究系统已经存有它。
- Blix journal明确标明processed/confirmed与失败回收；缺口修复是之后才取得较完整数据，不可把修复后事件的event_ts用于当时的预测能力。
- Million的copyability采用一分钟后进入的分钟K线近似执行时延，**这是一种研究代理指标，不是某用户真实一笔订单的滑点/报价承诺**。
- 旧Hermes [Gate理论](https://github.com/sunshihao001/-/blob/main/learning/16-Gate决策框架理论基石.md)区分**证据TTL与决策TTL**，这个区分有用；其分钟阈值只是历史建议，不得当已校准标准。

**新的目标认识**：监控系统最应该能追问“我们在决定是否关注时，究竟已经知道了什么？” 这项能力同时关系早期前兆、后验污染、业务失败归因、策略有效性、事故恢复和AI诚实。它不等于重新开发所有RPC适配器；优先复用原产品已经记录的event/ingest/decision与缺口信息。

### 11.7 为什么ai-d能改善整个研究，而不是增加一套固定的专家流程

本轮对照[ai-d整体知识整合](https://github.com/sunshihao001/ai-d/blob/main/knowledge/2026-11-07-whole-project-research-integration.md)、[从普通问题发现未知](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-problem-driven-unknown-discovery.md)、[短意图目标恢复](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-short-intent-goal-context-delegation.md)、[理论互证与不过度保守](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-theoretical-triangulation-provisional-acceptance.md)：

- **重新表征对象**：用户问“20钱包提前转钱”只提了一种表面现象，AI应主动发现此前未被问到的市场制度、交易流动性、可得时钟、平台手续费、服务共享/真实出资、观察系统筛选等中间变量；不是只换更专业的术语。
- **专家不是角色扮演名单**：取证、市场微观结构、经济激励、因果/样本、系统可靠性视角各自提出**能够区分机制的证据**；如果一个“专家”没改变问题、证据或行动，就不需要重复召集。
- **新外部资料是通向问题的入口而不是已知答案的终点**：README发现作者目的；源码/测试/失败可证实部分实现和边界；真实市场数据校正经济解释；理论帮助提出未识别机制。需要时可以跨越旧D01–D12，引入信息经济、平台双边激励、统计选择机制、适应性博弈，而不是因为知识索引无标签就禁止。
- **不无限反驳和不无限外扩**：当证据足以让高价值只读线索进入调查，就先行动；当更多同类页面无法改变竞争解释，转向一项真实原始交易/样本反证；若知识值得研究但对当前任务无增益则保留原始来源，不另扩一套制度。
- **判断和知识不同步等于没有真正学习**：新增证据具体改变哪条机制排序、哪个Blix调查对象、哪项旧规则/数据口径、哪个目标的优先级；更新对应原文件并复查，保留旧版出处。GitHub保存≠训练模型参数、自动Bot调用或已验证效果。

### 11.8 用整条生命周期检验互补与未知，而非仅以一个点当全部项目的“验收”

**研究对象**：一批同日发行的全体可观测Mint，包括没有出圈、没有进入Blix推荐、早期很活跃但后来失败、出圈却被系统漏选、后续多个新Mint重复出现的资金群体。**目前没有收集这批全体样本；以下是验收设计，不是已经完成的市场实验。**

| 时点/问题 | 原有Blix能起作用的地方 | 从参考项目/专业知识获得的区别性新认识 | 实际判断下一步 |
| --- | --- | --- | --- |
| 发行和初筛 | 发币发现、过滤、Pulse视图、coverage补漏 | pumpwatch总体与结果年龄；Pulse选择性留存；平台费用可能改变发行者经济目标 | 不只保留热门候选，还核“被过滤与没观测到”的对象范围、采集故障 |
| 最早交易与活动增长 | livetrades/Journal/triage | 独立Sniper、发行相关资金、MEV执行、公共服务都可能贡献同Slot；RED-COHORT活跃匹配基线 | 验证真实SWAP而非Transfer/fee payer；先给观察价值，再按资金链提升协同候选 |
| 迁移与多池 | Coin、报价、PumpSwap、现有Bubble Map | 微观结构区分真实净买盘、薄池冲击、LP变化、跨池套利与费率 | 追不同池的净Token/SOL变化、LP指令、费率与报价通道，不拿24h成交量差分成分钟买盘 |
| 持有、转仓、退出 | Holder、Wallet、Bubble Map、wtrack | PumpTraceCreator/历史、Million双向探索、Hermes/qb库存、Why-Solana多跳 | 对每条Token库存分发寻找后续真实卖出/归集/资金回流，同时防共享Hub误归因 |
| 退出后再部署与跨Mint | Wallet/Journal/research | Million Wallet↔Mint、Why-Solana资金闭环、meme策略生命周期 | 识别同一资本过程是否转移到新Mint，实际关系强弱随证据更新而不永久贴身份 |
| 事后回顾与修订 | brain scorecard/playbook、triage历史、产品研究页 | Million保留skip/shadow、Pulse长期归档、pumpwatch总体基线、ai-d原位修订 | 对成功、失败、跳过、漏观测分别评估；解释“为何当时没看到/没选中/看错”，不单只调高AI打分 |

此表的作用是**防止某个局部研究接管整套系统**。本轮仍应优先修复能够连接几个重要业务问题的原始来源与口径，而非把表格变为七阶段日程或单独开发七个服务。

### 11.9 形成新的总体专业判断：四类互相促进的“认识增量”

1. **经济生成增量**：从“有异常钱包”升级到“市场参与者可能如何同时通过币价、交易费、库存、流动性、信息/流量获益，以及他们如何互相改变策略”。有理论和文献支持为**优先研究方向**；特定地址动机未知。
2. **可观察性增量**：从“缺一个字段/供应商”升级到“采集与保存策略决定观察总体，甚至可能让AI自我评价系统性偏离市场”；这一机制有**确定源码支持**，其对某项Blix指标的实际偏差幅度尚待测量。
3. **决策价值增量**：从“检测到结构”升级到“谁在何时得到哪些可靠证据、采取哪类只读或未来独立授权行为、能否真正利用”；Why-Solana提供了**特定数据上的失效报告**，不是全市场否定。
4. **自主认知增量**：从“按旧专家/关键词调用知识”升级到“AI针对当前事实发现遗漏的机制、按信息价值选择原来源、主动给有倾向的专业解释、随新事实修正目标/判断”。这是**当前研究方法候选**；尚未在隔离端到端任务上证实AI能力显著提升。

**最关键的未知（不是短问题清单，而是贯穿系统的研究方向）**：
- 一个被看见的资金群体，是资金共同组织、共享服务、竞争性执行，还是公开市场注意力的共同反应？其**真实净资本/Token库存与收益归属**如何形成？
- 市场“热门、成长、失败”的变化，是参与者行为改变还是**程序筛选、供应商抽样、年龄回访、迁移多池**改变了观察条件？
- 结构在链上确实存在，但其知识什么时候对市场参与者仍有价值？**观察时延与交易成本、平台费、不同执行入口**是否在吃掉所有事后利润？
- 当新的经济组织方式不属于旧庄家/聪明钱/狙击手分类时，AI能否**主动生成区别性预测并获取证据**，而不被固定来源和打分框架限制？

### 11.10 只要求能改变整体判断的下一项真实验收，不扩建形式体系

优先用已保留的真实归档Mint及Blix原生现有功能，围绕**同一观测窗口**做“事实对账 + 不同目标解释 + 当时可得与事后可得 + 来源覆盖”的完整调查。最优先的是已归档的2026-11-01三时点PumpSwap池的原始Swap/LP事件、对价资产与实际可得时间；它能够同时修正“卖压/买回”“池相关Holder”“薄池套利”“Creator/资本组织”几个解释。若无法取得免费合法的历史签名，暂保留这条证据缺口，转向可冻结且可读的现有真实其他发行样本进行同等级调查，**不因单一API阻碍整个产品理解**。

第二个价值较高的验收是**市场发现覆盖/漏选实验**：以同一时间全体可观察发行做分母，比较Blix/参考产品当时输入、筛选、保存、显示、告警与后来结果；必须区分“没监听到、监听到了却没持久化、保存了但被拒绝、已提示却没有可行动优势”。这比增加更多风险标签有更高信息价值。**两项可以并行取证，不应无证据地编造已经完成的结果。**

**验收状态**：本节完成公开论文/官方规则、上游关键源码、Blix原产品与ai-d原研究之间的原始来源校对，形成明确新问题和互相关联机制；不能宣称全部参考仓库已经深入审完、AI内部参数已被训练、运行中策略有效、自动市场监控已部署、链上真实资金闭环已验证。只有本次GitHub提交并回读后，知识内容才算“已存入Blix”，但那仍不等于运行时掌握。


## 12｜2026-11-07 全过程研究的新增源码证据：时间错桶、发现抽样、历史窗口与判断演化

> 本节不是再列三个独立漏洞。研究对象是：**市场真实行为 → 数据被观察/抽样/保存 → 经济主体与资产路径被重建 → AI形成判断 → 结果回访与修订**。以同一业务因果链比较 Blix、Pulse、Million、HoldTech、PumpTrace、pumpwatch 和 ai-d；各源码证据只支持其实现的局部语义，**没有在这里启动原项目或获得新增真实链上交易**。既有第11节的宏观结论保留，本节新增可定位的具体代码条件及其互相作用。

### 12.1 新发现一：Pulse的滚动热度存在“事件到达顺序”假设，可能把历史活动归到最新窗口

**源码**：[Pulse `src/collector/solana-stream.ts`](https://github.com/nirholas/pulse/blob/d80465c043852e85619f5eee86634389e5b4a045/src/collector/solana-stream.ts)，`Rolling.hit(ts,isBuy,sol,wallet)`：`BUCKET_MS=5分钟`、`BUCKETS=12`；先计算`start=floor(ts/BUCKET_MS)*BUCKET_MS`，若`b.start < start`才新建桶；源码注释明确说明：**比最新桶更早的乱序消息直接记入最新桶**。后续`sum(now)`只按桶的`start`判断是否落在最近60分钟，并累加该桶`trades/vol/traders`。

**确定性的代码路径推导**：先到达一笔属于12:10桶的交易，随后迟到一笔属于12:00桶的交易；后者不会回填12:00，而是被计入12:10。若12:00后来已越过60分钟滚动边界但12:10仍在，迟到交易会比其真实事件时间更久地影响“近1小时热度”。这与Pulse此前已知的**选择性持久化**是两种不同的观察机制：一项改变**窗口归属**，另一项改变**哪些交易留在长期样本**。它们可能共同使“某群体提前活跃”“某时段突然热起来”的解释失真。**尚未测量乱序比例、偏差幅度或实际产品影响**，也不能推断所有Pulse统计均使用这套桶。

**Blix对照**：[Blix `server/journal.js`](../../server/journal.js)用签名/Mint/交易序号生成去重键，处理确认和缺口修复，交易保留24小时；[Blix `server/engine.js`](../../server/engine.js)处理新币发行/迁移/重启后回补。两者不等价于“全历史、所有事件都准确按发生时刻归桶”。**新的整合判断**：研究“6h/12h转账激增”时，除了`event_time/ingest_time`，还要知道统计桶采用**事件时间还是到达时间**、乱序如何处理、补数是否重算历史窗口。优先核现有Blix具体统计实现，再决定是否需要改代码，不能因为发现Pulse某处缺陷就否定其生命周期和归档价值。

### 12.2 新发现二：Million已经用“头部70%＋尾部30%”应对鲸鱼筛选偏差，但引入可复现性和覆盖问题

**源码**：[Million `apps/api/src/discovery/discovery.service.ts`](https://github.com/Kelows/million/blob/30c1ceef7b2984bde62cf9f7d7bee0d66501dfc0/apps/api/src/discovery/discovery.service.ts)的`discover()`先聚合交易中候选买家并排除部分路由/池设施，再对尚未在名单中的候选做快速预览：`topShare=Math.ceil(previewCap*0.7)`；剩余名额从尾部以`Math.random()`随机抽取，随后`fetchHistory(address,1)`、`computeMetrics(...,history.truncated,...)`。源码注释明确说明：仅看买入规模最大的地址会偏向机器人和设施，尾部未被预览就无法进入后续判断。

**专业意义不是“随机就不专业”**：这比只看大户更有探索价值，允许发现**金额不大、但角色关键的早期中转者、协同成员、跨Mint反复参与者**。然而`Math.random()`的预览名单在未记录种子/完整候选/选择概率时不保证同一输入可重复，且未预览者与未被观测者是不同类型的未知。**当前所见源码没有证明下游已记录抽样种子或完整概率**，因此不能宣称整个Million不可复现。需要继续检查其数据库保存和返回结果是否足够复核。

**Blix研究价值**：市场发现应同时维护“高价值优先”与“未知尾部探索”。单靠TopN可能错过真正的群体接力，全部平均扫又成本过高；可优先借鉴Million的**探索配额思想**，但在后续验收中保留样本来源/覆盖/是否被抽中。与Pulse选择性留存、pumpwatch总体发行样本对照，区分：未出现、未监听、未保存、未预览、已排除、被误归类六种“看不到”。这比仅新增聪明钱标签更可能改变市场发现质量。

### 12.3 新发现三：同一“钱包关系”会随调查目的改变意义，不能让聚类结果替代经济主体研究

- [Million `owners.service.ts`](https://github.com/Kelows/million/blob/6e12e45b735df7fc1fad0d5dd807cf323378b031/apps/api/src/analysis/owners.service.ts)：`HUB_DEGREE_MAX=6`，超过阈值的资助/付费Hub不参与并查集连接；注释记载曾发生**182钱包错误并为一个Owner**，因此同批入场边不作为连接桥。它解决的是**减少聚类扩散**，不是经济身份真值证明；硬阈值也可能切断真实大规模组织。
- [HoldTech `app/api/deep-scan/route.ts`](https://github.com/co-numina/holdtech/blob/64440cfe809c58641f2a2e9e2bc4e095b92f945e/app/api/deep-scan/route.ts)：同Slot检测以Fee Payer和交易类型近似“Bundle”，以及有限历史窗口下的资金来源；原第10节已复算反例。它偏向**快速风险筛查**，不等于完整经济主体恢复。
- [PumpTrace `docs/METHODOLOGY.md`](https://github.com/AntC215/Pumptrace/blob/63063f3cc6b1466a8c19852f6ea497a7dff61086/docs/METHODOLOGY.md)：作者将Creator归因限定为有支持的Pump创建指令；区分Creator、connected、operational、unclassified，区分真实直接资金边与较弱同步时间证据，未知Holder仍留在分母。**这是作者方法声明，需与实现/实测分开**。
- [Blix `server/holderslive.js`](../../server/holderslive.js)：`apply()`按Token Account维护`accts`，并对Owner的多个Token Account余额累加；[Blix `server/bubblemap.js`](../../server/bubblemap.js)有资金来源候选、RugCheck转账边、Hub/设施保护和短时旧图回退。二者提供**可用的调查基础**，但BubbleMap的首资助来源可能以Fee Payer回退，不能自动当实际付款人或实控人。

**新的整体判断**：同一资金边在“发现值得盯的异常”“判断Token可售库存”“估计经济主体”“预测未来行动”中，所需证据不同。**不应把谨慎的身份归因门槛错误套到早期观察**；同时也不能把弱观察标签无条件传递成“操盘手”或盈利概率。下一条有价值的证据不是更多相似图，而是**能改变解释的实际资产净额、指令/签名和后续库存去向**。

### 12.4 新发现四：回顾数据的“可重放”不等于当时真的知道，失败样本也要有分母

- [pumpwatch `docs/REPRODUCE.md`](https://github.com/cinder-security/pumpwatch/blob/d598cc5d71ff58a8b59847bc0d0296edbd79f00a/docs/REPRODUCE.md)明确提供冻结SQLite快照、SHA-256校验、`paper_stats.sql`以及重算发行总数/Creator数/模板/结果分布的具体查询。README式“发现工业化发币”由**固定总体和可复算分母**支持；此轮只核查说明及查询样例，**未下载该快照重算**。
- [Pulse collector](https://github.com/nirholas/pulse/blob/d80465c043852e85619f5eee86634389e5b4a045/src/collector/solana-stream.ts)既有短时内存热度也有选择性持久化/事后回填；[Blix journal](../../server/journal.js)保留24小时、可修缺口；[Million discovery](https://github.com/Kelows/million/blob/30c1ceef7b2984bde62cf9f7d7bee0d66501dfc0/apps/api/src/discovery/discovery.service.ts)使用跨生命周期采样与部分候选预览。它们不是谁绝对更好，而是各自优化**实时、成本、探索、归档**的不同目标。
- 因此“过去24小时没有异常”至少可能是：市场无异常、源没有监听到、监听到但未保存、被过滤、错桶、被延迟回补、历史查询被截断、数据恢复后才可见。**把这些全部记作正常市场会污染下一轮AI判断**。
- 研究“历史上这种信号能否盈利”，除了链上`event_time`，必须问**信号实际在何时被系统发现/保留/展示/用户可用**。可在历史事实充足时先提出理论上的优势候选；不能以事后数据当作已实现的交易优势。

### 12.5 ai-d应该怎样真正作用于这条完整研究链

[ai-d 整件事深度研究](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-whole-project-deep-research-and-mature-systems-audit.md)已经指出其过去的问题：把复杂目标过早降为三个小题，局部答案没能改变下一任务选择。这里把它用于**一个有真实Blix主体和源代码的完整案例**：

1. 用户说“发现庄家提前准备”时，**不预设只有庄家**：同时考虑发行者/LP/套利/普通跟随者/共同服务、平台手续费和持有库存的激励。各视角必须能提出可观察的区别，不强制专家全员发言。
2. AI发现原本没被问到的**观察系统机制**：Pulse错桶与留存、Million抽样、Blix短历史/补数，这些可能让“市场行为”看起来改变；将数据生成过程作为经济解释的竞争变量。
3. AI独立判断研究的**最小充分证据**：先使用现有快照、签名、源日志、Blix可读代码；如果新证据已足以提升只读观察优先级，不因未证实同控而拒绝；如果更多同类文章不改变判断，就转向实际原始Swap/LP或覆盖实验。
4. **双向更新**：如果新Swap/LP说明池库存变化主要来自LP而非卖出，修订“卖压”解释和Blix下一项监控；如果实证发现原始事件时间与热度窗口错配，修订事件聚合口径；如果已保存证据足够解释当前现象，就不因理论上存在无穷其他原因而停止给阶段性判断。
5. **不同成果分开验收**：此轮的原始源码条件和跨项目经济认识已核查；对真实Mint的资金闭环、跨Mint预测力、实时Blix产品、独立AI模型效果均**未验收**。后续若要改代码，优先验证现成系统是否已经解决问题，避免重新造全链解析器。

### 12.6 当前优先级的实质变化：不是再搬知识，而是先做能同时解释多条业务链的两类对照

**A. 同一真实Mint的事件/可得时间/经济净额对账**：把既有三快照的池库存与价格变化、真实Swap/LP/Transfer签名、Owner与Token Account、供应商采集时间、Blix可见时间串起来。目标同时检验市场发现、单Mint、钱包资金、流动性、AI解释；未获得原始事件时保留待验而不硬编卖压。

**B. 同一批发行的“观察→过滤→保存→预览→告警→回顾”对账**：先用已有Blix日志/源码可见范围建立分母，再对照Pulse选择性保存、Million头尾抽样和pumpwatch冻结总体。目标查**漏掉有价值对象的机制**，而不是只校正误报。若无法取得全体发行样本，先限定可观察分母并明确不代表全市场。

**何时停止研究？** 当继续阅读相同类型源码/README不会改变关键竞争解释、对象覆盖或实施选择时，先交付当前可验证的判断并转向缺失的原始事件/完整样本；如果发现原本未被识别、能改变经济机制或产品方向的关键领域，则允许继续深入，不受预设文件数或研究轮数约束。

**本轮新证据边界**：核查了上述具体文件的现行GitHub内容、原有Blix知识及ai-d研究；Pulse乱序错桶和Million头尾抽样是新确认的**代码实现条件**，实际发生频率、对某枚真实Mint的影响、端到端运行及预测改善均未测量。此节属于专业研究和产品决策证据，不是已交付新监控功能。
