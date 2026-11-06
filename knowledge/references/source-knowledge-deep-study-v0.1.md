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
