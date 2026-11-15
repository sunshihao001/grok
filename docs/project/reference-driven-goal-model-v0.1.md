# Solana Meme 市场智能系统｜参考成品逆向构建的多层目标体系 V0.1

> 2026-11-07 · 本文是现有 [goal-map.md](goal-map.md) 的**深度展开和跨项目目标归纳**，不是另立主目标、另建专家组织、另建软件或把历史G0–G4废弃。用户提出的新要求是：从各参考项目**实际主要目标与工作方式**提炼不同产品目的，再利用独立 [ai-d](https://github.com/sunshihao001/ai-d) 的目标理解、问题生成和专业知识迁移方法，建设同一Blix主体的多层、并行、可演化目标。**具体细分和优先级是AI提出的可修订候选，不冒充用户逐项确认。**
>
> 当前建设主体：`sunshihao001/grok@blix`。当前授权：只读调查、公共来源/现有归档核查、知识和项目文档修订；**不启动主服务、云电脑、不安装未经审查软件、不连接交易钱包、不签名、不付款、不自动交易、不改Blix业务代码**。下文写“可做/应该做”的内容属于**产品能力目标**，并非已在Blix验收完成。
>
> **来源标识**：`AUTHOR_GOAL` = 原作者或服务商公开说明的目的；`SOURCE_READ` = 已检查的可见源码/目录与局部实现；`ARCHIVED_DATA` = 本项目已有真实旧快照/在线运行归档；`OUR_INFERENCE` = 我们从上述事实作的产品认知合成；`NOT_VERIFIED` = 尚未独立运行或对经济机制验证。**作者目标≠源码能力≠上线真实性≠实盘优势**。

## 1. 先回答“我们在建设什么”，不要先按工具建栏目

**长期唯一主体目标（可深化，用户已确认方向）**：使同一套系统长期观察和理解 Solana Meme 市场，主动发现重要的市场变化、参与者行为和资金/库存结构，生成有依据的竞争性经济解释；利用新事实纠正和深化判断，为**市场机会观察、风险识别、专业调查、机制与可验证优势研究**提供可追溯、适时、可靠的支持。用户只需普通语言，AI主动研究和处理授权内事务。

**不是**“只做跟单/挑币”、“只做链上取证”、“只写学术研究”、“只有 AI 打分”、“复刻任何一个开源作者的交易产品”。Blix是当前可修订的**实现基石**，而非强行限定市场目标的理论边界。终端内可存在不同用途，但底层事实需尽可能共享，不因不同目标另造多个相互矛盾的系统。

```text
用户与项目价值：更早发现值得理解的变化，更准确认识风险、机制和潜在机会
    ├─ 市场世界：发行者／交易者／套利／LP／服务与社群的目标、资源、竞争和合作
    │   └─ 发行→持有与资本组织→交易/流动性→价格/库存变化→退出/再部署→长期演化
    ├─ 观察世界：链上事件、地址角色、Token/报价资产、池、叙事、采集时钟与遗漏
    ├─ 专业解释：市场微观结构、资金取证、行为经济、统计因果、产品工程等按需参加
    ├─ 统一Blix产品：发现→单Mint调查↔钱包调查↔跨Mint群体→监控→研究/回顾
    └─ ai-d通用能力：恢复目的→发现遗漏问题→按需找知识/参考成品→权衡→实施/核验→修订
```

这些不是必须逐个执行的阶段：一个钱包、一条资金路径、一批同Slot交易或一个长期市场现象都可以直接成为起点；同一个对象可同时服务数种目的。

## 2. 参考项目的原始目标与实际工作：先恢复其逻辑，再考虑融入

这里按“**原项目最想让用户完成什么**”排序，而不是按代码库数量或平台营销优劣。源码核查只覆盖列明的特定文件，未全量实跑。原项目自身的交易和支付功能**不自动成为我们的授权范围**。

| 来源/入口 | 原项目最主要目标（AUTHOR_GOAL） | 实际围绕什么组织业务、现成可学方法（部分 SOURCE_READ） | 对Blix现阶段的价值／不可直接继承之处 |
| --- | --- | --- | --- |
| **[Blix原项目](https://github.com/blixvip/blixtrade)**；[本分支README](../../README.md) | 一套面向Meme交易者的本地/托管实时市场终端；发现、分析、模拟及独立授权后的交易 | Pulse四列/发行流、Live数据、Coin Sheet/Holder ledger、RugCheck安全、钱包追踪、信号/AI Research、Paper、15m/1h/6h/24h回看、通知/健康页；源码入口 [capability-map](capability-map.md) | **保留主UI/实时数据与产品底座**；原README的AI打分、跟单或交易工作流不能自动视为已验证的机制/盈利或本项目已运行。 |
| **[Pulse](https://github.com/nirholas/pulse)**；[README](https://github.com/nirholas/pulse/blob/eea24c2357d65428427880fa873bb62441857dac/README.md) | 记录整个发行/爆发/死亡周期，让市场长期历史可用于钱包评分、复盘与情报报告 | 生命周期表、周期性快照、发行与毕业、钱包记分、KOL/Smart标签、每日报告、PGlite/Postgres、Git JSONL归档/恢复、MCP；[solana-stream](https://github.com/nirholas/pulse/blob/d80465c043852e85619f5eee86634389e5b4a045/src/collector/solana-stream.ts)只选择性永久保存标签/大额/合格早买 | **全市场基线、观察时钟与恢复能力**；不得把选择性留存的trade样本当全体交易，也不能从幸存者反推必有前兆。 |
| **[Million](https://github.com/Kelows/million)**；[README](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/README.md) | 用户口语指挥AI，钱包找币、币再找钱包，筛选可复制行为，跟踪后续表现 | Wallet↔Token 双向发现、Helius历史/实时流、机器人/池过滤、Owner候选聚类、Copy/Consensus/Ladder、原因日志、纸面与影子持仓、结果反向评价钱包；[Prisma数据模型](https://github.com/Kelows/million/blob/e28e2b3d82d253a7d9ed63b76b51daa383876fca/apps/api/prisma/schema.prisma)有observed/forward/skip原因记录 | **闭环发现与发现延迟/漏选回顾**最重要；其`ownerId`是启发式归组，自动交易器与签名部分不启用，原作者也明确过去PnL不能可靠预测未来收益。 |
| **[PumpTrace](https://github.com/AntC215/Pumptrace)**；[Architecture](https://github.com/AntC215/Pumptrace/blob/1fa070bed079e0d7e54c1bd4f12efa6e35a451c1/docs/ARCHITECTURE.md) | 回答“钱包/发行者反复做了什么、谁可能影响Token供应、之后监控什么” | Creator verified launches、首次卖出、发行生命周期、Wallet brief、Insider/资金/Token关系、证据权重、实时关注与提醒、NDJSON、可恢复历史Backfill、JSON/PG存储 | **单Mint深度调查、Creator历史及证据链/回补**；关系候选不等于真实同控，供应商授权和历史成本需另审。 |
| **[HoldTech](https://github.com/co-numina/holdtech)**；[README](https://github.com/co-numina/holdtech/blob/main/README.md) | 从持有人质量判断代币的“表面活跃是否真实”，给集中度、资金群体和风险评估 | Holder分析、Gini/HHI、Wallet age、同Slot/共同资金来源、跨Mint持有人重叠、可视化和AI verdict；[三个API源级反例](../../knowledge/references/source-knowledge-deep-study-v0.1.md) | **Holder、Bundle、Owner重叠的调查视角和UI**；部分代码把wallet age当持仓时长、Fee Payer当funder、抽样重叠当协调，**不排除整体流程复用，仅拒绝不成立的特定归因**。 |
| **[PumpGrok](https://github.com/swcstudiospace/PumpGrok)**；[README](https://github.com/swcstudiospace/PumpGrok/blob/main/README.md) | AI/Grok Bot 承接的多角色Meme研究和交易前准备工作台，含严格安全/人类确认 | 当前作者说明10席、35 Skills、ticket/ledger、安全宪法、只读CLI与回放paper模式；[marketplace](https://github.com/swcstudiospace/PumpGrok/blob/main/.grok-plugin/marketplace.json)含占位URL，README说明`scout pipeline`未实现且部分paper命令拒绝执行 | **自然语言委派、可追溯任务、审核与工作分工参考**；不是比Blix成熟的完整实时行情/资金历史引擎，**不能因席位多就新建固定专家系统**。 |
| **[OKX OnchainOS Skills](https://github.com/okx/onchainos-skills)**；[README](https://github.com/okx/onchainos-skills/blob/main/README.md) | 让AI使用成品市场数据、链上研究与交易/支付工具，通过现成workflow完成多步任务 | `okx-dex-market`只读数据，Token Research/New Tokens/Wallet Analysis/Smart Money 等工作流；另有可签名/支付的独立 Skills | **优先评估整套只读Token与钱包研究流程**；与付费`x402`、发交易、钱包签名分离，真实接口覆盖、价格与可用权限仍需逐项验证。 |
| **[GMGN](https://docs.gmgn.ai/index/quick-start)** | 新币筛选、市场热度、Smart Money/KOL/狙击手与交易者终端 | 新交易对、合约/持仓及钱包活动、观察提醒、Trader/Insider/新币入口；字段/标签和产品UI能帮助提业务问题 | **业务体验、发现入口、专业问题库**；供应商标签、可用API成本及动态口径不能直接作为链上真值，历史项目已决定不依赖付费GMGN作为第一数据前提。 |
| **[Cielo](https://docs.cielo.finance/readme)** | 持续观察感兴趣的钱包和链上事件，筛选推送重要活动 | 自选钱包与Token、实时活动流、类型/规模过滤、Discord/Telegram通知 | **事件通知/订阅/用户个性化重要性**，不等于多跳经济主体真值；监控覆盖与成本需实查。 |
| **[Nansen](https://nansen.ai/about-us)** | 用钱包画像与Smart Money发现市场机会，形成研究到执行的连续路径 | Wallet labels、Token God Mode、钱包分析、PnL/排行榜、实时资金动向；[官方Solana介绍](https://academy.nansen.ai/en/help/articles/9214978-solana-on-nansen) | **地址/群体画像与资金观察的成熟交互模式**；标签是厂商归因，可用性、免费UI与API权限不同。 |
| **[Arkham](https://codex.arkm.com/the-intelligence-platform)** | 聚合链上与链下信息，将地址网络解释成可追踪的实体与交易活动 | Entity标签、交易历史、对手方、组合资产与网络可视化 | **实体归因、网络调查与对象追踪的产品逻辑**；其实体标签不是Solana协议事实，应保留证据来源与可能错误。 |
| **[Bubblemaps](https://bubblemaps.io/v2)** | 用可视化钱包网络揭示持有人集中、转移关系及历史变化 | Holder bubble图、资金流、集群、Token历史与多链探索 | **关系图/历史库存呈现**；视觉连通不自动等于共同控制。Blix本身已内建Bubble Map，优先研究差异而非照搬第二份。 |
| **[pumpwatch](https://github.com/cinder-security/pumpwatch)**；[README](https://github.com/cinder-security/pumpwatch/blob/main/README.md) | 对pump.fun工业化发行行为做可复现的只读观察研究 | Detector、outcome tracker、不可变SQLite快照、SQL复算、发行者/模板统计；论文样本捕获42,562次发行（2026-07观察期，作者报告） | **全市场正常/异常基线、工业化行为模式、样本与复现实证**；发行频率高不自动证明恶意/操纵或赚钱。 |
| **[Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over)** | 从原始资金、组队和交易机制验证2024与2026的变化，并尝试推翻“能靠结构获利” | 发行前融资/首Slot行为/多跳资金/协同团队/资金循环/对照与样本外研究；原README明确区分**结构信号成立**与**未找到足够早的可交易预测优势** | **经济机制发现与真正的预测检验方法**；不能把作者单个历史收益或研究结论当当前市场稳赚规律，也不因某项Alpha失败就否定资金结构研究。 |

**原有历史项目不删**，但它们的研究目的不应被当作当前产品已经完成的功能：

| 历史来源 | 原项目核心方向（按原文件） | 现在最有价值的继承 |
| --- | --- | --- |
| [Hermes旧仓`sunshihao001/-`](https://github.com/sunshihao001/-)（[旧设计入口](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/README.md)、[V2认知](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/updated_project_cognition_v2_20260526.md)） | 以GMGN数据与Hermes Skills组织候选→安全→钱包/资金/库存→门控→纸面验证；持续判断结构侧还有多少筹码、退出压力和我们是否成为退出流动性 | **专业问题重构、筹码/阶段/资金机制、正反证、纸面回顾**；不复活其固定Phase/六Skill强制顺序及旧数据商依赖 |
| [qb-](https://github.com/sunshihao001/qb-)（[控制面](https://github.com/sunshihao001/qb-/blob/8377ad5611255df5cd4562666a826708575334f0/hermes_harness/01_control_plane/README.md)） | 单Mint调查、关键钱包和GMGN报表；后期重点建设数据语义、数据护照、判断校准、真实任务防自欺工作流 | **真实Token报告字段/Owner与Token Account处理、证据保全、错误识别**；项目目录巨大，已读一部分不代表全部专业内容完成审查 |
| [meme-](https://github.com/sunshihao001/meme-)（[真源地图](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/SOURCE_OF_TRUTH.md)） | 控筹区、成本中枢、市场阶段、深洗与二次启动、策略假设、指标语义和回测概念研究 | **把价格/库存/阶段解释变成可反驳的经济假说和策略条件**；MQL5技术框架或价格形态推测不应自动变成Blix“庄家真成本” |

**研究覆盖实情**：Blix原仓已做大范围UI→代码静态查阅；外部成熟项目只完成以上列出的README/特定源文件深入检查，没有对每个项目全库阅读/本地生产运行。旧三仓已做目录盘点、选取部分深读；覆盖状态以 [source-coverage-v0.1.json](../../knowledge/references/source-coverage-v0.1.json) 为准。**横向目标借鉴的广度不能冒充全部源码的深度。**

## 3. 纵向目标层级：原G0–G4仍有效，但G2下有真正不同的目标类型

| 现有层级 | 当下应回答什么 | 更成熟的目标内容 | 衡量有没有做到：举例，不设虚假硬阈值 |
| --- | --- | --- | --- |
| **G0 人的价值** | 为什么要在信息噪声极高的Meme市场建它？ | 用较低指挥负担看懂重要变化，及时形成风险与机会认识，避免明显虚假结构与无谓损失；用户保有重大价值/资金选择 | 不必懂API就能准确提出疑问、找到证据、判断下一步；相比纯行情页增加具体有用决定 |
| **G1 统一长期使命** | 什么产品能力值得长期积累？ | 持续自修正的Solana Meme市场智能与专业研究能力：**市场发现、结构调查、经济机制解释、历史学习、机会/风险评估**并行 | 同一个Mint/钱包能沿市场→资金→持仓→群体→回顾追踪；结论可由新事实修正 |
| **G2 横向价值目标** | 面对哪类市场问题，用户具体要什么不同结果？ | V-A 市场参与/机会；V-B 风险/取证；V-C 资金/库存/经济主体；V-D 全市场/长期演化；V-E 机制与新未知；V-F AI委派/产品可靠性 | **同一数据不同问题得到不同有效输出**，不存在“一份AI分数回答所有问题”；任何视角改变的必须是问题/证据/行动而非仅改标题 |
| **G3 产品承接与来源决策** | 怎样在已选Blix内实现上述能力，不重造轮子？ | Blix原UI/实时引擎是主体；Pulse生命周期/归档、Million双向发现、PumpTrace调查/回补、OKX只读研究、Bubblemaps/Holder和ai-d认知方法**按需整用/有限适配/对照** | 明确保留哪个原功能、外部来源能直接解决什么、需要什么账号/价格/依赖、源码与UI如何接，避免复制不兼容模块 |
| **G4 当前可检查任务** | 本轮到底交付什么改变？ | 只读源级验证、归档Mint复算、调查口径/问题模型、现有文档/测试；当前暂停生产启动和真实交易 | 有具体报告或测试、来源与失败、写回且回读；文档不是运行验收，运行不是经济机制验证 |

### G2：同一主体下六类并行价值目的（不是六个App，也不是六个必须常驻的专家）

| 目的 | 用户可能说什么 | 真正的专业任务 | 应输出什么 | 最有用原项目 |
| --- | --- | --- | --- | --- |
| **V-A 市场参与者/机会** | “今天值得重点盯哪几个？现在变化意味着什么？” | 去掉垃圾盘→识别异常与阶段→核来源和时延→量化可观察资金/库存、池深、卖出能力、负例；选出优先跟踪对象 | **关注候选**、为什么现在观察、哪些变化会升级/降级；无授权不自动下单 | Blix、GMGN、OKX、Million、Nansen、Why-Solana |
| **V-B 风险与独立调查** | “这个盘是不是有人在安排？怎么辨别？” | Creator历史、池/LP、Mint/Freeze、钱包实际资产变化、关联资金、同Slot的真实经济动作与竞争解释 | **风险路径**、有证据异常、哪些只是供应商标签/服务节点、改变判断的下一证据 | PumpTrace、HoldTech、Bubblemaps、Arkham、qb- |
| **V-C 资本组织与库存** | “大户出货是卖了还是转给别的钱包？资金去了哪里？” | 从Token Account/Owner经CPI、SOL/WSOL/Token转移到资金出资、库存接力和跨Mint循环；留意服务共享节点 | **可追踪的钱包/资金/库存序列**，协同候选与不同控制解释 | Million、Why-Solana、Hermes、PumpTrace、Blix |
| **V-D 全市场与长期观察** | “哪些变化正在全市场发生？我们之前错过了什么？” | 生命周期、冷门基线/失败样本/成功样本、资金与钱包行为分布、持久历史/时间窗口、断流与补档 | **可持续监控的市场事实与新异常**，历史回看、采集缺口、同类对照 | Pulse、pumpwatch、Blix、Cielo |
| **V-E 机制发现与专业研究** | “除了庄家，还有哪些新形成价格/收益的机制？” | 从参与者利益、资本约束、信息位置和执行条件生成竞争假说；跨源/跨学科找中间变量；用可区分证据和样本外表现验证 | **阶段性倾向机制解释**、开放未知、什么时候会被反驳或升级 | Why-Solana、meme-、Hermes、Pulse、原始研究 |
| **V-F AI协作与系统演化** | “我只说简单的想法，你去研究和做到能用。” | 目标恢复、问题重表征、选择专家知识与成品、授权内实施、质量回归、变更和知识管理 | **可验收的产品/研究结果**，清楚做了什么、能用到哪、下一价值更高的问题 | ai-d、PumpGrok、Million agent playbooks、Blix原有研究/健康面板 |

**关键：不同目的允许同时成立与部分冲突。** 同一池价格/库存反向变化，V-A可判为高优先关注对象，V-B可暂时找不到共同控制，V-E可优先研究Swap-vs-LP，V-D可将其记录为可比较的生命周期事件。不同意见不是全体弃答，也不需要固定22位专家投票。

## 4. 横向市场世界：研究“为什么行为出现”，不把参与者目标当已观察真相

真实参与者的目标是**隐变量**；同一钱包可在不同Mint、时间和权限下承担不同角色。

| 市场行为者（可能是不同经济主体，亦可能有角色重叠） | 可以考虑的目标/约束假说 | 更具区分力的市场观察 |
| --- | --- | --- |
| 发行者/Creator/营销和社区组织 | 长期活跃、社区传播、平台Creator fee、保留Token价值、退出持仓，乃至某些操纵目的（不能预设） | 发币历史、Creator费来源、初始分配与权限、市场关注、实际资金/Token流、跨币重复 |
| 发行相关多地址组织/资本群 | 分配库存、降低单地址暴露、执行协同买卖、分批退出、资金回收与再部署 | 直接资产转出、资金/库存可对账、同Slot真实买入、接收后出售、资金回流与下一Mint |
| Sniper与早期独立交易者 | 争取执行先后与可成交位置、承担失败与滑点风险、尽快退出 | 跨不相关发行者抢早、独立资金、手续费/失败率、真正可见时延与卖出结果 |
| 套利者/MEV与路由系统 | 价差、交易排序与路由收益，可能低净库存敞口 | 多池即时价差、对冲方向/净资产变化、Jito排序、同Slot指令而非只看时间 |
| LP/池与撮合设施 | 交易流动性、手续费、风险库存管理、价格/池深约束 | Pool/Vault/LP权利、流动性增减、两端储备、资金/Token出入 |
| 普通投机者、社群、KOL | 利润、娱乐、身份/叙事、注意力或影响力；不必相互独立也不等同共控 | 公开信息时间、交易者覆盖、持续真实买卖、异质资金来源及卖出时序 |

**不应预设“庄家在盘里所以一切由同一目标驱动”。** 价格、钱包关系和库存变化是多主体目标互相作用的结果；还须分辨**真正经济过程**与**数据观测/选择性保存**造成的假象。专业调查任务是比较多个目标假设对后续资金/Token变动、收益归属和时间序列的不同预测，并根据证据调整优先顺序。

## 5. 专业视角：谁能提出真正不同的问题，而不是组建专家编制

| 按任务启用的视角 | 提出的专业问题 | 能增进哪个目标 | 容易越界/忽略什么 |
| --- | --- | --- | --- |
| 链上取证、Solana协议/经济事件解析 | 谁真正转出了哪种资产；Fee Payer/Owner/Authority/LP谁是谁；内层CPI怎样去重？ | V-B、V-C，所有事实底座 | 图上有边≠同控；成功转账≠获利卖出 |
| 市场微观结构与执行 | 池中买卖如何形成价格、库存与滑点；时滞/费用/可卖规模影响谁的收益？ | V-A、V-E | 看到报价变化≠看到了净新资本或可执行套利 |
| 资本组织与制度/激励 | 发行方、平台、LP、Sniper如何因费用与收益约束选策略，谁承担谁的成本？ | V-C、V-E | 从行为结果猜目的，不能自称读懂意图 |
| 统计学、因果和科学研究 | 成功/失败盘是否同样被观察、出现多大比例、对照什么机会全集？ | V-D、V-E、V-A | 只会反驳却漏掉高价值早期异常 |
| 产品、数据工程和SRE | 真实数据在哪里、历史是否可恢复、通知是否到达、费用/隐私/安全能否承受？ | V-F及所有业务 | 只修工程变量而忽略市场研究价值 |
| 决策与风险管理 | 当前证据够不够支持**观察/进一步调查**？什么时候支持更强主张？ | V-A、V-B、V-F | 把风险控制误成永远不产生倾向判断 |

**ai-d方法要义**：专家不是名字或提示词表演；由问题构造**必要的专业视角**，需要时可加入未在表内的新学科，只有能改变解释、下一证据或行动的视角才真正启动。[ai-d问题导航](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/planning/goal-navigation-v0.1.md)（Draft方案）、[ai-d知识入口](https://github.com/sunshihao001/ai-d/blob/main/knowledge/INDEX.md)与[未知发现研究](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-problem-driven-unknown-discovery.md)提供上层研究方法，Meme领域的目标优先级仍由用户项目决定。

## 6. 目标转化为Blix具体业务能力：每项有承接位置、来源、验证出口

| 子目标与完整业务任务 | 优先复用现有Blix主体 | 外部项目改变了什么判断/值得用什么 | 当前真实完成边界与后续验收 |
| --- | --- | --- | --- |
| **O1 全市场发行/垃圾过滤/异常候选**：不是只查排名，而是可解释筛出一批观察目标 | 原Pulse/Discover、`server/engine.js`、`sources.js`、`quality.js`、`triage.js` | Pulse历史基线、pumpwatch工业化发行频率、OKX/GMGN筛选和风险工作流 | UI/实时源有源码；Blix主服务尚未在当前研究环境实跑。验收：新Mint生命周期、source覆盖、假阳性/重要漏报、筛选前后总体样本一致 |
| **O2 单Mint产品级调查**：从Token进场、池/Holder/Creator到重要钱包 | `server/coin.js`、`holderslive.js`、`bubblemap.js`、Coin页 | PumpTrace Creator/回补、HoldTech持仓结构、OKX Token Research、qb 单Mint报告 | 当前四个Mint相关API口径未统一，参见[mint-cross-module](mint-cross-module-evidence-audit-v0.2.md)；[真实三快照研究](single-mint-audit.md)证明部分公开来源可核，不是完整实链单Mint报告 |
| **O3 钱包与资金关系/库存接力**：谁收/谁发/哪种资产，是否跨地址转仓再卖 | `server/wallets.js`、`wtrack.js`、`bubblemap.js`、`solana.js` | Million Token↔Wallet与边图，Why-Solana多跳，PumpTrace直接转账与角色，Hermes筹码状态 | 源级路径存在；真实跨Mint完整资金守恒、同控关系与签名级验证尚未完成；验收需交易签名、Token Account/Owner、SOL/WSOL、CPI及服务Hub |
| **O4 跨Mint群体演化与持续监控**：群体成员变化、接力/迁移、6h/12h前兆 | `wtrack.js`、`journal.js`、`coverage.js`、现有研究/通知 | Million动态发现+反馈、Pulse时间序列持久化、PumpTrace可恢复回补、Cielo提醒；Why-Solana关系和失败基线 | 不能把Blix约24h局部Journal当全链资金历史；验收覆盖空窗、成员变动/公共Hub、历史分页、重启/补档及通知真正送达 |
| **O5 市场机制与开放未知**：为什么出现价格/库存/行为变化；哪些假设后来被新证据改变 | `research.js`、`brain.js`、研究报告及旧D01–D12 | Why-Solana结构 vs预测的实证分离、meme机制假说、Hermes问题生长、ai-d专业研究选择 | 需要原始事实/竞争解释/可区分后验观察；目前**没有**证明自主AI发现了新的可重复盈利机制；验收基于新来源能否改变合理解释与前瞻性预测 |
| **O6 多视角市场决策支持/结果回顾**：值得看、值得查、应避免什么以及为什么 | Blix Signals/Picks/Paper/Track record/Research | Million影子跳过机会与copyability、PumpGrok任务/票据、OKX现成research流程、Nansen/Arkham等成熟UI | 原Blix记分和paper结果**不能**替代净可交易利润；研究只读，真实成交/授权/资金行为不启动。验收预测时点、漏检、正确示警、延迟与滑点、真实成本的分离 |
| **O7 可靠的观察与长期知识演化**：断流/缓存/供应商变更/模型错误不能伪装成市场变化 | Blix原有SQLite、`health.js`、`apicache.js`、`journal.js`、`server/intelligence/`静态入口 | Pulse PGlite+归档恢复、PumpTrace游标回补、pumpwatch冻结样本、qb审计和ai-d目标/经验治理 | 既有Intelligence层按静态代码查见，**没有挂到真实运行中的Blix server/UI验收**；验收事件发生时间与可得时点、覆盖、同一Mint多来源、故障恢复及写回回读 |

**避免两种极端**：
- 不是以“目前Blix缺什么”来裁剪所有来源研究：外部成熟项目可能发现新的参与者收益机制、失败原因或数据对象，即使暂时没有接口也保留并研究。
- 也不是因为每个参考项目各有长处，就把每个软件或数据库装进Blix：优先整用已存在功能，许可、运行成本、权限、数据真源、维护与安全达到实际条件时再确定集成。**PumpGrok和ai-d提供的是AI任务承接方法，不能替代市场数据引擎；OKX/GMGN/Helius等提供的数据服务不能替代经济解释。**

## 7. 用一个真实案例把“市场目标、专家目标和产品输出”贯通

[现有归档Mint三快照](single-mint-audit.md#2026-11-07真实单-mint-三次归档快照多参与者目标与动态证据修正)：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`。2026-11-01 02:44→03:23→03:26 UTC同一PumpSwap池的Token库存`57,331,535→58,774,685→58,374,413`，SOL库存`465.47→457.4104→461.07165`，价格`0.0008148→0.0007653→0.0007819`美元。供应商归档数据已重读并记录来源SHA，**并非原始RPC签名重放**。

同一个事件，**目标版本与决策**实际不同：
- **O1/V-A市场参与**：短时资金/库存方向出现变化，是值得观察的线索，先查持续性与执行时差、池深；**可积极提升观察优先级**，但不能凭它下交易保证。
- **O2/V-B调查**：RugCheck头部Token Account Owner与DEX主要PumpSwap池地址精确匹配，优先把约6%供应商持仓标为**池相关库存**，不是个人鲸鱼；查来源时点和Vault属性。
- **O3/V-C资本组织**：有池库存变化，**还没有证据指向某个接收地址转仓/群体接力**；下一个高价值证据是本时间段的真实Swap、LP变化与对应账户资产净变。
- **O5/V-E机制**：争夺解释的是“真实买卖流导致的两端库存变化、LP进出或数据不同步”，而不是问所有专家哪位看涨；有相反证据后更新解释。
- **O7/V-F运行知识**：两供应商对同一池的余额不同、24h滚动量不能差分当小窗口，需保留源/时间/可得性；不是因存在来源差异就取消全部方向性观察。

这说明**同一份可核查事实能同时支持“值得监控”“池不是大户”“交易主体未识别”“库存候选需查Swap/LP”**，这些结论不互斥。完整签名若出现新证据，分别更新相应主张，而不是重做全套统一打分。

## 8. ai-d真正用在Meme的地方：目标恢复、专业问题生成、判断演化，而非强制提示词

```text
普通意图
“有很多钱包提前准备资金，这币是不是有人在安排？值不值得注意？”
      ↓
恢复用户当前目的：是“实时机会”？“同控调查”？“机制研究”？（可同时存在）
      ↓
重建问题：参与者是谁、资金和Token如何移动、什么是值得早知道的变化？
      ↓
按需找专业机制：协议事件／资金图／库存／微观结构／激励／统计基线
      ↓
恢复原有Blix产品能力 + 精选成熟成品 + 对照旧Hermes/qb-/meme-
      ↓
输出 真实观察＋有倾向性的竞争解释＋最有区分价值的下一证据
      ↓
在只读授权内研究、监控设计/离线核查/产品文档更新，验收后修订
```

**该流程是理解原则的说明，不是要求每条问题执行七道审批。** 应从问题规模、已知条件和下一证据价值适应性裁剪。专业意见不需要投票，服务不同目标的判断也不必合并为同一份风险分。

### 四个 ai-d 修正，直接改变了原有项目工作习惯

1. **目标既有层级，也有并列及冲突**：G0–G4解释上下位；V-A至V-F解释同一系统中不同用途；原项目与我们的关系可为`supports/refines/alternative_to/parallel_to/conflicts_with`。新参考项目的目标不因名字相近自动获得主体地位。涉及改变用户长期目的时给出候选方案，不自行定案。
2. **专家视角必须产生增量**：不因为旧专家数目多而逐个叫齐；找出此前遗漏的条件、激励、关系或预测差异，必要时跨出原D01–D12。**“看了源码/用了术语”不是认知提升的验收**。
3. **积极判断与反证对称**：正常解释仅在有实际解释力时才改变倾向，不因“可能另有原因”就取消有价值警报；同样不能把Token Account/Owner或Fee Payer编成幕后人。只读研究线索需要的证据门槛可低于同控法律身份、实盘投资收益。
4. **长期知识更新靠真实结果，而非文档数量**：每次新证据更新它能改变的目标、业务能力或机制假设，同时保留原始来源、适用时间、可能误导的旧结论；没有实质变化，不增新全局规则。缺数据时保留下一核查入口，允许阶段性倾向结论。

## 9. 本轮完成的是目标重建；下面才是可验收的产品差距

| 重点 | 已有的可靠事实 | 目前差距 | 明确的验收方向 |
| --- | --- | --- | --- |
| **市场发现作为产品入口** | Blix原UI、筛选/信号/研究源码可追溯 | 本地/云端实际供数、完整覆盖、重要异动的漏检率未核验 | 同一真实时窗重播候选及事件，核“被过滤的Mint/重要异常去了哪里” |
| **真实单Mint调查** | 2026-11-01旧工程PR #16在Actions成功获取5池/20条RugCheck候选，并找到Pool-Owner跨源相等；本轮已有三快照研究 | 尚未获得已授权原始Solana RPC逐笔完整Swap、Creator/关键钱包真实资金历史 | 单Mint从交易所/池/Holder→真实签名/Token与SOL两端资产变化→源与时间对齐 |
| **Wallet→Mint→Wallet与跨Mint监控** | Million有双向发现与数据模型；Blix有跟踪与局部Journal | 同一经济主体、历史重启补档、钱包库存接力和6h/12h完整覆盖未验 | 冻结同一批已证据化钱包，真实交易追踪、群体成员改变与遗漏报告 |
| **机制与潜在优势** | Why-Solana原报告有深度结构研究与针对“可交易优势”的负结论，旧meme-有机制假说 | 本项目未验证独立的新机制预测；还未比较纯结构 vs 行为变化 vs 可得时点 vs 真实执行成本 | 在记录触发规则之前定义观察时点和机会全集，后续以新样本检验机制的解释力与可执行性 |
| **AI专业工作质量** | ai-d来源研究与Blix知识入口静态可达；已建立若干源码级反例 | 未做独立模型A/B、Grok Bot实际技能调用、AI自动修正长期知识的运行验收 | 对同一未见资料比较简单词面检索、问题驱动知识选择与过量上下文；同时考察漏报和误报 |
| **工程运营/安全** | Blix有health/日志/SQLite等源码，PumpGrok/OKX有成品操作设计 | 未审安全启动、外部成本、实用通知/睡眠恢复 | 在单独授权的隔离环境优先只读健康/恢复/失败重试验收，**绝不提前连接签名/交易** |

**目前最优先且不需要再扩建体系的下一项实际工作**：围绕同一个已归档真实Mint，选出**一项能够最大幅度区分“池库存变化由Swap还是LP变化主导”**的只读证据任务，找到时间段内实际协议交易/余额事件并复核；若已有归档源不含签名，就承认缺口，不能再从三张供应商快照推断更多地址意图。此事同时服务V-A/V-B/V-C/V-E，信息价值明显高于再建设一张专家登记表。

## 10. 未来目标版本如何变，不使知识系统重新成为束缚

- **确认不随便改变的**：用户最终市场智能大目标、当前Blix建设主体、只读不付款签名交易的已授权边界、原始证据诚实、重要价值选择在人。
- **可根据研究动态改变的**：目标V-A至V-F的粒度/数量、先研究哪个行为者、数据商/成品取舍、产品入口的深度、监控口径与对比基线。
- **每个明确转向只记录**：旧目标、建议目标、为何有新证据、两者是支持/深化/替代/冲突、预期改变哪一个用户结果、待核验什么。无新证据不用为了“维护体系”强制生成记录。
- **闭环产物**不是“AI变聪明”的口号，而是这次采用不同参考项目的知识后，是否让一次完整市场调查或一个可运行的只读监控结果更准确、更早、更有解释力，且能指出它仍不会的部分。

**总裁决**：把“市场参与者/不同专家视角/参考项目作者的产品目的”统一理解为**同一市场事实的不同目标层、问题生成器与竞争性机制**；以Blix为实现基石，继承真正可用的成熟工作流和历史研究，不把多个上游目标混成一个万能评分，也不把多视角变成六个固定专家或六个软件产品。


## 11. V0.2｜把目标体系落实为“目标—能力—事实—判断—验收”

> **本次定向复核**（2026-11-07）：重新读取`nirholas/pulse` README blob `edce1417a163d0ab88d5711867ce78a76c1257fc`、`Kelows/million` README `8565c9bdf83a98ad832d4fb452b0456b69bb6374`、`co-numina/holdtech` README `1f59e219232a37048c631e810a6f6d54f43653d6`、`AntC215/Pumptrace` README `850c6a0c44e5206ce580032d076ca0d1f3b8defd`、`cinder-security/pumpwatch` README `eae2f78137fdcf237a31bcb0fc8d679d771fe3ee`、`Why-Solana` README `c04b189116c794cdb33fa1fe2cd8130844cc2802`；并核对`ai-d@main`的[短意图目标恢复研究](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-short-intent-goal-context-delegation.md)和[成熟整体系统研究](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-whole-system-benchmarks-before-component-exploration.md)。这里是**README层的原始目标再次核对**，不能宣称六仓所有实现或上线能力已完整验收。V0.1既有全部参考项目和G0–G4保留；本节**只补以前“目标层有了，怎样影响具体任务”这一缺口**。

### 11.1 从参考项目恢复其“产品追求”，不要只抄功能

| 原成品的核心产品目的（原README作者陈述） | 该目的隐含的研究对象与成功条件 | 转成我们系统的**目标修正**，而不是功能抄袭 |
| --- | --- | --- |
| **Pulse**：记录发行、爆发、衰亡、钱包评分与长期归档 | 观察对象不仅是当日热门币，还包括失败、未上榜、曾被过滤的发行；成功需有可回看历史和明确留存规则 | **目标增加“发现之外的市场记忆与反事实基线”**：今天为何没发现、当时可见什么、被采集策略漏掉什么？注意其README虽称监测每次发行，但`trades`描述明确是标签/大额/合格早买的选择性保存，不能推成全量成交 |
| **Million**：自然语言操控钱包追踪和交易者发现、跟随结果反馈 | Wallet↔Token发现可双向生长；系统还需记住被跳过的机会、延迟与结果，不只显示胜出案例 | **目标增加“调查对象自动扩展＋错过与失败的反馈学习”**：从一枚Mint发现钱包，再从钱包找到其他Mint，并复查当初的筛选理由；其自动交易部分不进入当前只读授权 |
| **HoldTech**：对持有人“质量”做X光，判断表面热度是否由少数相关地址构成 | 需要把账户分布、资金来源、年龄和同Slot等放到同一调查上下文；README中“一个人50钱包”是作者动机叙述，**不是仅凭同源同Slot即可确定的真实身份** | **目标增加“市场表象与底层资本组织差异”**，并把来源可共享的基础设施、样本偏差和归属不确定性保留为解释条件 |
| **PumpTrace**：交易前回答“Creator/钱包反复做了什么、谁影响供应、接下来监控什么” | 重要的不是某次分数，而是Creator可核的历史、钱包资金与Token权利、生命周期变化及可追溯的下一监控对象 | **目标增加“从一次调查形成可持续的对象级研究”**：事件证据→参与者历史→持仓/资金路径→后续需要验证的变化 |
| **pumpwatch**：用可复算、冻结样本研究工业化发行的分布 | 不能只盯成功盘；需要发行总体、正常背景分布、研究可重复和无法推断的目的边界 | **目标增加“机会全集与常态基线”**：异常要相对于可观察的发行总体而非只相对于热门榜单 |
| **Why-Solana**：解释旧交易机制为何失效、新资金组织如何变化，并主动检验是否仍有可交易优势 | 结构存在、能够较早看到、可以盈利是三个不同的判断；作者明确存在“群体可观察但优势已消失”的结果 | **目标增加“市场机制的生命周期与失效发现”**：不仅识别模式，还要发现模式何时失效、资金组织如何改变、是否有先于事件的可得证据 |

**从这些来源共同生成的新专业目标**：不再只是“自动发现异常并打分”，而是**维护一份会更新的市场世界模型**：观察哪些发行与资金行为、为什么只看到了这些、不同主体可能为何行动、哪些机制跨时间重复或失效、哪些发现会改变真实监控与研究优先级。这里的“世界模型”指**可追溯事实、关系、竞争解释和修订**，不是已实现的专门AI模型或必须新建数据库。

### 11.2 主体目标之间不是平铺的功能清单，而是依赖、反馈和张力

```text
用户价值/重大选择（G0）
└─ 统一市场智能目的（G1）：发现、理解、调查、监控、修正
   ├─ 市场覆盖与历史记忆（Pulse/pumpwatch）──→“没有看到”究竟是无事件还是漏采？
   │                                      ↓
   ├─ 发现与对象扩展（Blix/Million）──────→Mint↔钱包↔其他Mint的新调查对象
   │                                      ↓
   ├─ 经济事实与关系调查（PumpTrace/HoldTech/旧Hermes/Why-Solana）
   │                                      ↓
   ├─ 参与者目标、库存、交易与机制解释（meme-/Why-Solana/专业知识）
   │                                      ↓
   ├─ 机会/风险/研究三种不同的阶段性判断──→决定优先看什么、补哪项证据
   │                                      ↓
   └─ 后续事件/失败/反证与反馈───────────→修正覆盖、发现规则、经济解释及目标优先级
                         ↑
         ai-d负责恢复目标、选择知识、发现遗漏问题、判断继续/实施/暂停及验收
```

箭头表示**信息与决策依赖**，不是必须串行执行的七步、七个微服务或七个常驻专家。市场参与者目标属于**研究对象的隐变量**；参考作者目标属于**外部产品设计证据**；我们的V-A至V-F属于**用户使用目的**。三者不能合并成一个“专家评分”。

三个需要长期保留的张力：
1. **早发现 vs 确证归因**：异常可以先进入调查队列；同控身份或盈利主张需要更强证据，不用因暂时不能确证就否定观察价值。
2. **全市场覆盖 vs 运行成本**：Pulse/pumpwatch提醒必须知道被过滤的发行与丢弃事件；不意味着当前要购买全链历史或自建昂贵索引。应明确覆盖边界，先利用成熟成品与可负担数据。
3. **自动研判 vs 用户控制**：ai-d允许AI自主提出专业问题、修改研究假设和执行只读调查；不自动改变长期价值选择、交易授权或付费边界。

### 11.3 四条实际业务链：目标必须落到用户得到的结果

| 用户简单表达 | AI主动恢复的目标/遗漏问题 | 首先复用的主体及外部知识 | 可以检查的**阶段性成果** | 明确的“不能冒充完成” |
| --- | --- | --- | --- | --- |
| “今天有哪些盘值得盯？” | 不是简单涨幅排行：发现对象的完整性、异常发生时可见性、过滤规则漏检和真实池深；V-A+V-D | Blix Discover/Signals，Pulse生命周期/失败样本，pumpwatch基线，OKX候选研究 | 带源/时间的候选与被过滤分母；明确值得盯的变化、后续触发条件和失效条件 | 热榜成功盘≠全市场筛选有效；现有Blix静态源码≠已运行实时市场 |
| “这币是不是有人提前安排？” | 不是先贴庄家标签：Creator、池相关Holder、直接资金/Token转入、同Slot真实买入、服务Hub及行为变化；V-B+V-C+V-E | Blix Coin/Bubblemap，PumpTrace历史与回补，HoldTech Holder，Why-Solana资金路径，旧Hermes/qb | 一份能追到签名/账户/来源的**倾向性调查**，区分资金组织候选与公共服务解释，指出最有价值的下一条验证 | 同一Funder/同Slot/Holder图边≠确定同一经济主体 |
| “为什么这些钱包在卖出前转仓？” | 追接收者后续出售、库存是否守恒、资金是否回流或跨Mint再部署；同时检查LP/Swap和数据断流；V-C+V-E | Blix Wallet/Journal，Million双向发现，PumpTrace关系，Why-Solana多跳和历史样本 | 交易签名、指令位置、资产变化、候选路径与反向解释；可以有明确“高度值得追踪” | Transfer≠Sale；未知历史窗口不能变成零活动；关系不等于可交易优势 |
| “以前有效的模式为什么现在不灵？” | 是经济机制变了、参与者策略变了、竞争使优势消失，还是采集/留存策略变了？V-D+V-E+V-F | Why-Solana失效研究，Pulse历史快照，pumpwatch总体基线，meme-机制研究，ai-d问题生成 | 冻结旧解释及其预测，比较不同时段/市场条件/可得时点，明确更新了哪条判断 | 事后解释成功≠预测能力；数据采集差异≠市场结构变化 |

**把“不同专家视角”落在任务内部**：协议/取证决定事实能否成立，微观结构决定库存与成交如何形成，经济学决定参与者激励与竞争解释，统计学决定样本/基线是否足够，产品工程决定实际是否可持续获取。只调用能改变当前问题的专业视角，避免每次强制列齐22位专家。

### 11.4 ai-d应负责的不是“再写一套提示词”，而是四种关键判断

1. **目标恢复与可纠正的意图升级**：用户只说“继续”“研究这个币”，AI从既有G0/G1、当下事件、用户限制推断最有价值的任务；只有不同理解会导致重大授权/价值差异才问用户。对应[短意图研究](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-short-intent-goal-context-delegation.md)。
2. **从参考项目中寻找以前没意识到的问题**：例如Pulse的选择性保存提示“历史缺失”可能来自采集规则；HoldTech提示“高持有人数”可能是共享资金服务；Why-Solana提示“发现结构”不等于“发现优势”。对新来源保持开放，不把V-A至V-F当知识上限。
3. **竞争解释中的有方向判断**：真实库存/价格变化可以使“值得调查卖压”优先于纯随机解释；但新Swap/LP证据若推翻则更新。**不因可能存在另一解释而无限保守，也不把理论交叉支持升级成真实链上验收**。
4. **成果验收与知识原位修订**：GitHub文档、来源读取、离线规则测试、Blix真实运行、独立市场事实、可交易优势是不同的完成条件。成熟整体Agent研究提醒：功能名存在≠用户一条指令已走完整链路，见[ai-d成熟整体研究](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-whole-system-benchmarks-before-component-exploration.md)。

### 11.5 当前主体建设真正要先完成什么

**第一优先**：在Blix已有市场/单Mint入口上，证明同一真实Mint的**观察→调查→动态判断修订**能贯通，而不是把研究文档当成可用系统。已归档三时点DEX/RugCheck样本证明可以形成“池Token/SOL库存方向变化、头部Holder为池相关候选、跨源不同步”三个不同结论；下一项决定性核查是相应时间段的原始Swap和LP事件，或找到可用的已授权历史记录。

**第二优先**：用Pulse/pumpwatch的研究目的核对市场发现的**覆盖和漏报**；用Million/PumpTrace的目标核对从Mint到钱包再到其他Mint的**连续调查能力**。在真实样本和成本允许时优先整用成品，不提前重新造钱包图或历史索引。

**第三优先**：同一条调查随新事实修订**证据、经济解释、监控优先级和结果回顾**。只有出现明确产品缺口时再考虑Blix最小工程改动。用户重大目标与交易权限不自动改变。

**本轮验收边界**：完成了六个开源项目README原始目标再核对、ai-d两份当前研究的交叉核查，并把它们具体映射到四条可检验业务链；**没有**安装或运行这些六个成品、没有修改Blix业务代码、没有完成原始Swap/LP核对，也没有证明AI模型性能改善。不能把本节的目标修订写成“功能已交付”。


## 12. V0.3｜目标上移：不能只监控市场，还要理解观察市场的系统怎样改变判断

**本次跨仓新增认识**（完整来源与逻辑：[原始代码、外部原始研究及ai-d交叉深审](../../knowledge/references/source-knowledge-deep-study-v0.1.md#11-2026-11-07-跨全市场与-ai-的双重反馈从数据选择到经济机制与判断修订)）：Blix的真正主体目标，不应只理解为“发现Mint→调查钱包→监控群体→输出解释”，还应包含对**谁能进入观察、为何被保留、谁被AI研究、哪些结果反馈修改Playbook、市场参与者是否反向适应信号**的长期认识。上位目标不变，但其专业解释深度增加。

从不同来源提取的**设计选择与改变的判断**：
- Blix现有 engine.nursery/cull、research.trimQueue、brain.scorecard/review 已形成“市场选择—分析—追踪—自修订”的闭环；**自修订只用已评级样本，missedRunners不能发现从未被评级的遗漏对象**。因此不能把自评提升等同全市场机会发现能力提升。
- Pulse的早期买家历史在Runner/Graduated条件下选择性落库，市场生命周期统计与钱包交易全体统计不能混同；Million同时保留被拒绝机会的异议及模仿延迟，提供了**如何寻找错过机会与可执行性差距**的成品启发。
- PumpTrace比较Creator/池/Holder可交易供应，Why-Solana PITFALLS记录大量原判断在异常数据、未来选样、公共Hub与执行时点下失效；PumpGrok提供可追责任务/审批概念，但没有完成所有实时市场业务代码，不能替换Blix原主体。
- ai-d应帮助识别**问题结构里尚未出现的影响因素**（例如信息可得时点、平台收入激励、不同数据系统的入选分母），而不是简单把六类目标再转成六个AI专家或六套固定Prompt。
- 2026-09的 [arXiv:2609.18975 v2](https://arxiv.org/abs/2609.18975) 报告两条特定独立管线在完整17.5天窗口内仅5个Mint交集（各自623、1742个），证明**观察范围的巨大差异可能来自采集设计**。这些数字来自论文，不代表已实测Blix与Pulse的交集。
- 2026-10的 [arXiv:2607.02795 v4](https://arxiv.org/abs/2607.02795) 撤回此前“群体提升买家流”相关**全部数值结果**；是必须更新旧参考知识证据状态的直接案例，不能用历史百分比继续推导本项目的预测价值。

**G2六种用途的共同能力**因而增加：看得见/看不见什么；为什么如此；现有经济解释何时被新事实改变；哪些被跳过的对象可能推翻当前判断；某个结构在当时是否有足够可得信息及可执行条件。不是六个新模块；它们共享原Blix数据/报告事实，按不同用户目标输出不同的倾向性结论。

**目前优先实证问题**：对同一发行窗口，追溯发生→被源捕获→nursery/active→AI排队/取消→评级/未评级→后续事实/机会；然后围绕已归档Mint复核真实Swap/LP，对应市场与观察两个机制。若无法获得数据，则把数据缺口与可替代方案明确列出，不能凭长报告补出“未选中对象”的历史结果。尚未改业务代码、做独立模型A/B或Blix线上监控验收。

## 13. 2026-11-14｜GMGN × 既有成熟产品 × Blix机会优先：全局再整合（V0.4）

> **本节为原有 G0–G4、多参与者 G2、D01–D12 及外部产品完整来源目录的**原位升级**，不是第十三个专家领域、新总评分器、新交易软件或代替前面内容。本文重启点来自用户：“把GMGN这些有用的项目和类似之前看过的项目再进行结合，重新梳理一遍”。保持：**实际可参与的交易机会发现优先、深度调查支撑、Blix原版完整保留、AI依授权主动研究、当前仅只读/离线**。
>
> **证据分层**：\`OFFICIAL_FEATURE\`=产品官方文档/README（可说明作者声称做什么，不证明实时效果）；\`SOURCE_READ\`=本轮重新打开仓库真实 README 或 Skill 原始文件；\`BLIX_SOURCE_READ/CI_PRIOR\`=Blix仓库实际代码和此前明确SHA的离线CI；\`USER_PARAPHRASE\`=上传的 Synapse 方法笔记，不能当官网全文；\`INFERENCE\`=本项目跨产品研究提出的机制和产品建议；\`UNKNOWN\`=未运行平台/市场/AI效能测试或接口实际鉴权。2026-11-14 当前 PR #23 仍 Draft、未合并且 mergeable=false；PR #24 仍独立 Draft。主研究记录在 blix，PR #23 的工程进展在其独立 [build-register.md](https://github.com/sunshihao001/grok/blob/integration/blix-evidence-readonly-20261108/docs/project/build-register.md)；**不要把两个分支的文件默认为已经合并**。

### 13.1 产品重新定位：五个不同问题，不能让任一外部产品替代总目标

| 用户实际问题 | 推荐参照的产品逻辑 | Blix 现有基础 | 最有价值的增量，不是再做同类页面 |
|---|---|---|---|
| **哪些 Mint 刚刚值得关注？** | GMGN New Pair/Trending/Discover、OKX New Token Screening、Pulse生命周期/负例、pumpwatch发行全集 | Discover/Pulse、engine/triage/early/research/quality/brain | 比较“原版发现到的全候选、被拒候选、后来的结果”，增加来源覆盖和事件可见时点核查；钱包触发候选入口**已经**存在 |
| **什么钱包/群体在买，为什么？** | GMGN Wallet Radar/First70/Insider/Sniper/Bundler、Million Wallet↔Mint、HoldTech holder overlap、Nansen 标签 | wallets/wtrack/bubblemap/holders/walletSignals | 关联地址数 vs 启发式组数 vs 真实经济主体分别呈现；从Mint发现钱包、从钱包关联其他Mint；公共服务和跟风是竞争解释 |
| **Token 从哪里来，是否转仓后卖出？** | Synapse 14 类信号和 DEX Visor、PumpTrace Creator/直接转移、Bubblemaps Time Travel/Magic Nodes、Hermes/qb- | 钱包汇总、Bubble Map；PR#23原始RPC归档/指令级 Token 转移/后续卖出摘要 | 把Swap、转移、接收者后续卖出分列；交易事件身份按签名+指令去重；未掌握同批库存与资金去向时明确 UNKNOWN |
| **好钱包能不能跟，参数该怎么选？** | GMGN wallet-score（Track Record vs Copyability）、GMGN Copy Trade 参数、Million followability/跳过决策、OKX Wallet Analysis | 原 Wallet PnL/Paper/Brain/Track Record，PR#23 followability-replay 纸面收据 | 钱包胜率/历史利润≠用户在收到信号后的净可成交收益；以信号首次可见→买入/卖出报价→延迟、滑点、池深、费用、失败状态检验；只模拟和讨论，不实际跟单 |
| **这次推论怎样随着新证据更新？** | Cielo 自选地址事件、Pulse 历史档案、PumpTrace 游标/回补、Million Decision Log/Shadow、Arkham实体网络 | Journal/SQLite/Health/AI Research；PR#23调查继续状态是只读快照 | 对“为什么选/为什么跳过/什么时候才知道”提供可追溯理由；持续监听、历史恢复、实时业绩尚需真正验证，不能用一次AI文案替代 |

**裁决**：GMGN的“交易终端产品体验”、Million的“钱包-代币双向发现和跳过理由”、Pulse的“市场记忆”、PumpTrace/Hermes/qb-的“证据化行为调查”、Synapse的“行为信号与时间轴”、OKX的“已包装只读工具调用”、Nansen/Arkham/Bubblemaps的“成熟交互”、meme-/Why-Solana的“机制与反证”，在同一Blix里可**按问题互相支持而不互相接管**。\`research_priority\` 与 \`trade_readiness\` 是两个待对照的**分析结果维度**，不是要求第二套程序化硬过滤，且不代表PR#23已有生产字段。

### 13.2 GMGN 专项逆向：重新恢复完整业务知识，而不只是复制“聪明钱”标签

| GMGN 原产品能力与官方来源 | 应恢复的专业问题与内部分支 | 现有项目对应位置 / 避免的错用 |
|---|---|---|
| **GMGN Discover、New Pair、Trending**；[Quick Start](https://docs.gmgn.ai/index/quick-start.md) | 按发现渠道、代币生命周期、市场活动、交易量/持仓变化、叙事信息发现Mint；观察信号出现在趋势之前还是之后；未选中样本去哪了 | 原版 Pulse/Discover/Early/Triage 已在做，重点对比来源Universe、到达时点、被拒记录，不能再建一份市场扫描器 |
| **GMGN Wallet Radar**；[官方文档](https://docs.gmgn.ai/index/wallet-radar.md) | 多Mint共同交易/共同持仓→反向发现高利润/早期入场地址；\`Most Bought\`、\`Highest Profit\`、\`Earliest Bought\`、\`Shared Holdings\`；文档支持最多10个Mint同时研究 | Million \`Wallet↔Mint\`、qb-关键钱包矩阵、Blix钱包关联图；**跨币重复地址≠同一个团伙**，需钱包角色、资金源和不同市场阶段对照。Radar报告结束需要“何时快照/跟踪列表更新” |
| **GMGN Insider/Sniper/First70**；[官方文档](https://docs.gmgn.ai/index/insider-traders-snipers-first-70-buyers.md) | \`first 70 buyers\`、发射初期狙击、未见公开买入但持币的潜在Insider、初始持仓/后续加仓/部分卖出/转出、总供应分母；官方明确其持仓状态非实时保证，\`Sell Part\`部分语义存在转移与卖出难辨 | 与 Synapse S03/S07/S10、HoldTech同槽、新鲜地址、Hermes筹码库存相联；以PR#23指令级转账解决**有证据的可分部分**，不能把GMGN \`insider\` 标签当法律内幕事实 |
| **GMGN Token Skill**；[公开Skill源码](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-token/SKILL.md) | \`smart_degen\`、\`renowned\`、\`fresh_wallet\`、\`dev\`、\`sniper\`、\`rat_trader\`、\`bundler\`、\`transfer_in\`、\`dex_bot\`、\`bluechip_owner\`；同一个钱包可有多角色、且角色随时间变动 | Blix Holder/钱包标签扩展的**问题表征**；强行把所有来源标签汇总相加会重复计分。\`bundler\`标签不自动证明 **Jito Bundle** 的具体提交/原子交易关系；需原交易或Bundle来源独立核实 |
| **GMGN钱包详情、历史收益与节奏**；[官方钱包页](https://docs.gmgn.ai/index/wallet-detail-page.md) | 7D/30D PnL、已实现/未实现、平均成本/持有时长、交易次数、\`Sold > Bought\`、\`Didn’t buy\`（转入候选）、10秒买卖机器人/吸引跟随者的模式 | Blix Wallet/Track Record + Hermes/qb；必须区分钱包自身盈亏、转入资产导致的错误成本、快进快出使跟随者赶不上 |
| **GMGN wallet-score / wallet-style**；[评分Skill源码](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-wallet-score/SKILL.md)、[风格源码](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-wallet-style/SKILL.md) | 关键独立问题：\`track-record\`（钱包本身战绩） vs \`copy-tradeability\`（跟单者能获得多少）；包括速度、延迟、滑点/费、回测代理、Dev声誉；以**中位数可复制窗口**替代简单平均持仓时长作为节奏描述候选 | 对接 Million copyability、Blix PR#23只读 followability replay；其评分加权/阈值为作者启发式、回测是近似，未复现本市场优势；**不直接迁移其数字阈值或买入建议** |
| **GMGN Copy Trade参数**；[官方操作说明](https://docs.gmgn.ai/index/copy-trade-copy-smart-money-automatically-earn-sol.md) | 固定金额/最大跟随额、比例跟卖/独立止盈止损、下单频率、创建时间、池流动性、市值上限/下限、源钱包金额、交易平台、加仓次数、优先费、Anti-MEV、滑点、失败/重试；文档Lightning低确认可能逆序/重组/重复 | **把参数作为只读演练维度**，先比较信号时效、池容量、复制延迟与费用，别在Blix附加新的交易执行器。收费与产品参数可能随时间变动，必须使用实际版本；禁用真实签名/买卖 |
| **GMGN Agent Skills / API**；[官方技能入口](https://gmgn.ai/ai)、[公开Skills仓](https://github.com/GMGNAI/gmgn-skills) | 已包装Token、市场、钱包、持仓、交易员、监控、风险调查工具；学它的**任务级组合和字段语义**，非先安装所有Skills或默认开启Trading | 优先现有Blix/OKX只读能力。GMGN付费/API配置**不是初期依赖**；历史项目暂不充值使用GMGN，公开文档及源码足以做这一轮业务语义研究 |
| **X Tracker、SnipeX、新闻/社交**；[完整官方目录](https://docs.gmgn.ai/index/llms.txt) | 传播/项目公告/X变化与链上入场是否在时间上相关？如何发现新Mint合约、区分广告或营销推动与独立需求？ | Blix Social/Research/Narratives已有候选；AI可调用相关知识与事实做交叉解释，不能靠社交热度或KOL标签单独证明有收益 |

**GMGN真正能提升本项目的三个产品认知**：
- **跨 Mint 的不同价值**：共享持仓、最早买入、买入频率和已实现盈利回答的是**不同问题**。同一批“同时买入”可以是协同、同一服务、跟风或相同策略；**谁先发现某Mint** 与 **谁具备可复制节奏**可能是不同钱包。
- **Wallet Score 不是一个单值**：历史稳定盈利、是否具备信息优势、跟随者看到信号后的净可成交性、是否可能是制造跟单行情的Dev/刷子，都应分开思考。强行做“大综合聪明钱分数”会丢掉关键区分。
- **参数是经济条件，不只是按钮**：例如固定金额/最大金额改变订单冲击；市值、流动性和币龄门槛改变样本选择；优先费与滑点改变净收益；Lightning更快也存在重新组织/确认风险。观察到交易不等于能按钱包成交价复制。**无需提供真实资金参数、无需运行订单即可先做有效模拟和方法反证。**

### 13.3 完整成熟参考图：原项目贡献的“不同能力”，不是再拼装十几套程序

**核心产品层（全部已复核指定README/页面；没有全部独立部署）**

| 来源 | 研究对象与已查资料 | 影响哪个业务判断 | 组合时的反证/迁移条件 |
|---|---|---|---|
| [Blix原版](https://github.com/blixvip/blixtrade) + 本仓原版保护测试 | 市场、钱包、价格/安全、AI、Paper、界面/数据 | **唯一既定产品主体** | 已有项目不能重复实现；React实际入口、原版保护manifest及数据源故障需核 |
| [GMGN](https://docs.gmgn.ai/index/llms.txt) + [gmgn-skills](https://github.com/GMGNAI/gmgn-skills) | 交易终端场景、Wallet Radar、First70、钱包标签/节奏、Copyability、参数 | 从“钱包标签”升级为“是否可跟随”“关联 Mint 是怎样发现的” | 官方营销与Skill规则不等于验证收益/控制权；访问、费率和授权另验 |
| [OKX OnchainOS](https://github.com/okx/onchainos-skills) | \`okx-dex-market\` 只读Token Research/New Tokens/Wallet Analysis/Smart Money；独立 \`okx-agentic-wallet\` | 现成调查任务与专业数据接口语义，减少AI自己发明API | 严格将只读市场研究与签名/付费/交易Skill隔离；需要真实数据时再评估权限/费用 |
| [Million](https://github.com/Kelows/million) | Wallet↔Mint动态发现、Copy/Consensus/Ladder、影子机会、跳过理由、可复制性 | 钱包动态扩展、群体信号、前瞻可复制性、失败反馈 | 源码启发式 owner/group≠同控，Shadow/Paper不是真实成交；原版已有钱包触发需查增量 |
| [Pulse](https://github.com/nirholas/pulse) | 全发行生命周期、失败市场、周期快照、名单出现记录、钱包评分、PGlite/Postgres | 分母与全市场负例，市场“首次看见” vs 事实发生 | 源码仅选择性永久保存部分trade；旧事件归入新时间桶风险不能外推为实测误差率 |
| [PumpTrace](https://github.com/AntC215/Pumptrace) | Creator已验证历史、直接关系、钱包简报、游标回补、持仓与风险 | 开发者历史、来源证据强弱、对象级监控与状态改变 | Creator关联≠同控；其历史恢复做法可参考，不能重建PR23已归档的相同事件 |
| [HoldTech](https://github.com/co-numina/holdtech) | 同slot/同资助、钱包“年龄”、Holder质量、Gini/HHI、跨Mint overlap | 表面分散持仓 vs 资金集中组织 | 本项目历史源码审查已发现账户年龄/持仓时间、公共Fee Payer等对象定义风险；不能用评分当控制事实 |
| [Synapse用户笔记](../../knowledge/references/synapse-methodology-full-taxonomy-20261114.md) + [纵深研究](../../knowledge/references/synapse-cross-signal-mechanisms-20261114.md) | **14个链上信号、DEX三事件/三形态、Hyperliquid四主信号/五标签、五原则、四噪音**全量保留；跨信号的资金/库存/时间图 | 从“异常标签”转为资金托管→注资→分发→真实买卖→卖出压力的经济过程候选 | 笔记为用户转述，未逐条验证站点/阈值；HL永续不硬迁移pump.fun；任何低当前适用项继续保留研究资格 |
| [Cielo](https://docs.cielo.finance/wallet-tracking/my-wallets) | 钱包自选追踪、交易类型/阈值过滤、首次交易事件、通知 | 何种钱包/资产变化值得通知和再次调查 | 未测试通知覆盖/延迟，不能当完整本地资金史 |
| [Nansen](https://academy.nansen.ai/en/help/articles/9214978-solana-on-nansen) | Wallet labels/Smart Money/Token God Mode/Wallet Profiler、时序观察 | 地址角色、资金方向、钱包历史/当前画像 | 标签是来源归因；Solana免费UI≠API免费，免费需注册，付费Pro功能另议 |
| [Arkham](https://codex.arkm.com/the-intelligence-platform) | 实体标签、对手方、地址关系及跨链图 | 地址网络解释、关系证据可见性 | 平台Entity不是Token Account Owner的协议字段，控制权可能UNKNOWN |
| [Bubblemaps V2](https://bubblemaps.io/v2) | Holder气泡、Time Travel、Magic Nodes、连接扩展 | 资金/Holder变化的视觉解释与历史演化 | Blix已有Bubble Map；关系连通≠同控，优先增量证据说明而非复制整套图 |
| [pumpwatch](https://github.com/cinder-security/pumpwatch) | 冻结发行样本、发行者工业化模式、可复算统计 | 新币市场背景、常态异常与“错过候选”分母 | 作者窗口/样本选择有限；高频发行不直接说明恶意或盈利 |
| [PumpGrok](https://github.com/swcstudiospace/PumpGrok) | Skill/票据/风险否决/纸面任务收据 | AI的职责与只读任务边界 | README \`scout pipeline\`未实现；不照搬十席专家组织、未验证的自动任务链 |
| [OnchainRadar历史参考](https://app.onchainradar.ai/hyperliquid/positions) | 历史研究聚焦Smart Wallet/Team Wallet/Wallet Flow/持仓/清算/TWAP | 跨产品“资金/仓位快照＋行为事件＋持续复查”问题意识 | 本轮目标页面工具访问失败；**只保留先前研究假说，不以本轮不能访问的页面断言现行功能** |

**既有研究与专业方法资产，仍同等保留**：
- [Hermes](https://github.com/sunshihao001/-) ：钱包角色、原始资助/共同来源、库存/可卖筹码、异常与反证的知识推理；有设计完成/尚未实现的区分。
- [qb-](https://github.com/sunshihao001/qb-)：单 Mint 关键地址矩阵、转仓、Owner/Token Account 语义、历史95钱包报告的分母；不能把被跟踪钱包余额占比误叫全供应占比。
- [meme-](https://github.com/sunshihao001/meme-)：FCZ/POC/AVWAP/阶段与二次启动的价格结构问题、失败形态；成本中枢假说不等于真实庄家成本。
- [Why-Solana](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over)：多跳、Dust≠资金支持、共享服务与同控区分、结构信号可被观察≠能够样本外盈利。
- [ai-d](https://github.com/sunshihao001/ai-d)：普通语言目标恢复、关键未知发现、来源选择、专业知识按需调用、矛盾/竞争解释与可检验交付，不是另一个交易算法。
- **协议与数据源候选**：Solana官方交易/Token-2022、Pump协议、Raydium/PumpSwap/Jupiter、Jito、FnZero/Carbon/Helius/Bitquery/DEX Screener/RugCheck；它们承担原始交易事实、机制、历史深度或报价功能，**只能依据实证缺口再决定引入，不让AI程序逐例重复数据供应商的工作**。
- **其余资料没有删除**：[历史65项参考总目录](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json)仍保留 MELT、RED-COHORT、Carbon、Solana Microscope、Axiom/Photon、QuantBloc、CoinGlass 等完整候选及当时来源状态。\`HISTORICAL_NAMED_ONLY\` 不能因现在列名便升级到已核源码。\`RED-COHORT\` 早期部分定量结论已被撤回，不能继续当因果/收益实证。

### 13.4 跨产品发现的四个新组合问题（INFERENCE），不是“更多标签”

| 跨来源关系 | 新的专业问题 | 为什么与实际机会有关 | 可推翻它的反证 |
|---|---|---|---|
| GMGN Wallet Radar × Million Wallet↔Mint × qb/Hermes 关键钱包 | **“哪种跨币重复”才说明可迁移的早期发现能力？** 同时交易多个热门币可能只是机器人/市场共因 | 可能更早从地址发现未在榜单的 Mint | 随机同交易频率匹配钱包也有同样重复；历史赢家筛选产生幸存者偏差 |
| GMGN First70/Bundler/Transfer-in × Synapse S03/S07/S10 × PR23经济证据 | **筹码由多个地址持有、转出和卖出时，谁真正增加了可卖供应？** | 识别看似分散、实际有可观察库存接力的风险；保护跟随者 | 交易属于池/服务/空投，转仓没有真实卖出；历史窗口漏采或同一笔双计 |
| GMGN wallet-score/Median Copy Window × Million Copyability × Blix Paper × OKX Wallet Analysis | **“优秀钱包”与“适合我们跟单的钱包”是否是两类人？** | 直接影响跟单候选、行情时效、费用后净结果 | 原领先者收益已在信号公布前实现，传播延迟/滑点后无利润；大额无法卖出 |
| Pulse/pumpwatch负例 × Blix早期筛选 × Nansen标签 × Cielo事件订阅 | **信号看似有效是否来自“只看已进入榜单/已追踪地址”的选择偏差？** | 帮助减少被错过的机会与假阳性，验证全市场召回 | 不同数据源观察全集不同，真实时间顺序或资金流中断、标签事后补全导致预测失效 |

**更深一层的对象划分**：钱包可以买入、卖出、接收或转出；一个钱包还可能是程序、池、交易所、委托钱包或团队服务；同一经济动作可能多次触发标签。**交易动作、资产余额、钱包关系、资金来源、市场流动性、行为模式、可交易结果**必须可以互相连接，但不必强行合为同一个评分。AI的价值在于在特定任务下选择哪些联系能够改变判断，并指出哪些尚不可得。

### 13.5 三种真实使用方式：每条都可以从用户当前页面直接进入

**场景 A：AI挑选有交易机会的Mint（优先）。** 从原Blix New/Running/FinalStretch/Migrated/Pulse已知候选和已有钱包活动进入；AI按候选目标依次获取必要的**当时可见**市场、风险、钱包及行为证据；发现明确市场机会前，明确价格/流动性/资金结构和跟随延迟的冲突。最终给出：\`当前值得观察 / 需要补查 / 暂不适合参与 / 可进入只读纸面比较\` 及原因；不是直接命令下单。**比较 A 原版 Blix vs B 参考知识按需增强** 的提前量/漏检/成本/安全否决。这里“按需获取”不是必须先通过14个固定阈值。

**场景 B：在 Blix 打开某 Mint → AI专业扩展调查。** 结合原Coin/Holder/Bubble Map/Wallet、PR23指令级转移、GMGN的First70/Insider问题、PumpTrace Creator历史、HoldTech库存风险、Synapse Distribution/Claim/CoordinatedWithdrawal。显示重要地址、可观察来源、从Pool买入到A转B、B后续卖出以及未知；**不能因B卖出就断定卖的那批Token来自A**。若市场池深不足，可以仍然“值得研究”但“没有目前可交易证据”。

**场景 C：寻找可以跟的钱包 → 反向发现 Mint 并复盘。** 候选可来自GMGN Wallet Radar思路、原Blix跟踪钱包、Million发现、用户指定、旧qb与Hermes方法；区别7D/30D PnL、样本数、持仓中位节奏、是否开发者/刷量/狙击/共享平台、首次可见时点，模拟跟随者下单规模、流动性、费用和退出。形成“观察/只读模拟/排除”而非单个成功率排名；定期复核高质量钱包是否行为变型或转仓给新地址。**目前没有真实钱包跟随盈利验收。**

### 13.6 交付与源码承接：改变之前的错误优先级，不预设新架构

| 负责位置 | 已有/已验证到哪一步 | 应优先深化什么（不重复数据源） | 禁止偷换成 |
|---|---|---|---|
| **Blix原版 \`server/engine.js\`, \`early.js\`, \`triage.js\`, \`quality.js\`, \`research.js\`, \`brain.js\`, Wallet/Track Record/Paper** | 源码已有发现→初筛→研究/钱包告警→风险→纸面跟踪的路径；原版保护测试覆盖关键文件 | 原版成为 A 对照；先对所有入选/被拒候选留样本与时点；不要先动受保护的原版Research | “全系统还缺候选发现，重新写一套GMGN扫描器” |
| **PR#23原事件/经济证据与只读报告** | 原始 RPC、指令位置、转入接收者、局部卖出候选；已用合成 mixed Swap+Transfer 检查 WTrack 摘要边界，原地址数 vs 关系组不等于同控；CI仅按指定SHA有效 | 用现有原始证据供 AI 解释GMGN/Synapse行为分类；进一步检验混合动作源语义、池/公用设施过滤和历史窗口 | “真实接收者卖出的就是刚转入的库存”“任何外部钱包图已经确证共控” |
| **PR#23 \`server/intelligence/ai-workflow.mjs\`、\`Intelligence.tsx\`、\`followability-replay.mjs\`** | 具只读模型任务及本地取证契约；先前本地SQLite离线案例验收；真实模型/API和市场优势未完整验证 | 不增加全量固定Agent链，让模型按问题调用已有可用数据、知识与证据；单任务标注研究理由、机会可行性与必要反证 | “AI会思考，所以自然拥有实时外部数据/资金追踪/预测优势” |
| **外部 GMGN / OKX / Helius /其它数据商** | 已核公开功能及部分Skill/源码，**未用付费 GMGN 或真实交易授权** | 能解决真实缺失字段时单独做源语义、准确率、限流、费用和许可比较；OKX只读工作流可先做候选接口契约对照 | “平台叫smart就独立同控”“已经打开文档=已接入可运行” |
| **知识根源与历史参考** | 本文前12节＋Synapse全分类原目录＋65源索引/D01–D12仍在 | 在真实任务中按需取对应原文、源码、反例，反馈差异到原目录 | “把研究越拆越细、文件越建越多就是能力提升” |

**下一次验收的最短可交付改动**（业务价值排序，不构成机械强制流程）：

1. **同一候选全集的发现时点对照**：记录原Blix从何处发现、什么时候首次可见、有没有进入AI队列、拒绝理由及随后24h结果；用GMGN Wallet Radar/Million的**多Mint-钱包反查**思路只读补充解释，不能拿后来的盈利钱包回写过去的发现。
2. **用同一 Mint 做“两个不同结果”验收**：研究价值 vs 交易就绪。已有Synapse/GMGN钱包行为与原风险/池报价在冲突时允许结论分叉；示例“异常筹码集中但池太浅”只应提升调查、不应提升买入。
3. **按钱包历史战绩与可跟随性分开评估**：先检查原 Paper 和 PR23 纸面收据数据的费用、延迟与卖出完整性；缺入场和退出的**实际可得报价**时维持未验证，不产生净收益承诺。
4. **只在证明有真实增量时把旧知识变成按钮/代码**：如果现有Blix已经提供数据与地图，则AI引用并核对即可；如果是源头漏交易/价格/Pool/账户归属，则回到对应原源职责修复，不在AI报告里补数据。

**本节已完成**：重新阅读 GMGN官方多Mint/First70/Copy Trade 文档与公开 Skills、OKX Skills、Pulse/Million/HoldTech/PumpTrace/pumpwatch/PumpGrok及旧 Hermes/meme-原始项目关键文件，结合既有 Blix 实际源码和PR23工程状态，完成跨项目“功能→经济机制→具体判断→Blix承接→验证缺口”原位映射。**未做**：重新审完65项资产、各平台真实登陆/付费API数据、GMGN/OKX实测对照、真实Mint全签名/同批库存、前瞻策略收益、实盘、系统部署。这是研究与认知合成，不是功能/盈利验收。

### 13.7 本轮直接核对的主要资料（固定定位）

- GMGN：[Quick Start](https://docs.gmgn.ai/index/quick-start.md)、[Wallet Radar](https://docs.gmgn.ai/index/wallet-radar.md)、[Insider/Sniper/First70](https://docs.gmgn.ai/index/insider-traders-snipers-first-70-buyers.md)、[Copy Trade参数](https://docs.gmgn.ai/index/copy-trade-copy-smart-money-automatically-earn-sol.md)、[Wallet detail](https://docs.gmgn.ai/index/wallet-detail-page.md)、[gmgn-token](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-token/SKILL.md)、[gmgn-wallet-score](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-wallet-score/SKILL.md)、[gmgn-wallet-style](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-wallet-style/SKILL.md)。
- 开源原始源码/设计：[OKX Skills](https://github.com/okx/onchainos-skills)、[Million](https://github.com/Kelows/million)、[Pulse](https://github.com/nirholas/pulse)、[PumpTrace](https://github.com/AntC215/Pumptrace)、[HoldTech](https://github.com/co-numina/holdtech)、[pumpwatch](https://github.com/cinder-security/pumpwatch)、[PumpGrok](https://github.com/swcstudiospace/PumpGrok)、[Hermes](https://github.com/sunshihao001/-)、[meme-](https://github.com/sunshihao001/meme-)；qb-沿用此前已明确路径的[关键钱包样本](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_fact/wallet_fact_report.md)，本轮未重新打开其全仓根目录。
- 服务方产品文档：[Cielo](https://docs.cielo.finance/readme)、[Nansen Solana](https://academy.nansen.ai/en/help/articles/9214978-solana-on-nansen)、[Arkham平台](https://codex.arkm.com/the-intelligence-platform)、[Bubblemaps V2](https://bubblemaps.io/v2)；Synapse原站未完成方法细节的独立核验，严格区分用户转述内容。
- 本项目已核：[原Blix全主体源码审查](whole-product-cross-layer-audit-v0.1.md)、[先前业务对照](blix-ai-investigation-product-comparison-20261113.md)、[Synapse完整分类](../../knowledge/references/synapse-methodology-full-taxonomy-20261114.md)、[当前目标图](goal-map.md)、[PR#23 R-35/R-36](https://github.com/sunshihao001/grok/blob/integration/blix-evidence-readonly-20261108/docs/project/build-register.md)。

## 14. 2026-11-14｜半自动市场智能目标升级（V0.5）

> **目标升级，不是运行验收。** 用户希望在完整原版 Blix 内，从“打开Mint后问AI”发展为**半自动、事件驱动、可持续的Meme市场智能研究与机会评估**：只需给目标、关注范围及必要授权，系统能自行观察、初筛、选择性补查、调用专业知识与现成工具、保留证据和反证、只读模拟、对重要变化提醒并接受人工决定。实际交易、签名、资金管理、自动跟单和新增付费权限不在本次授权内。继承既有G0–G4、O1–O6、D01–D12、L0–L7和K1–K9，不将知识层级机械变成选币流水线或新增多个Agent编制。

### 14.1 上位目标与人机边界

| 原目标 | 新增/深化内容 | 不应误解为 |
|---|---|---|
| G0 用户价值 | 普通口语交代任务，AI替人持续观察和研究；重要取舍/资金操作由人决定 | 用户需要逐步点每个币或学会编程 |
| G1 产品定位 | **Blix半自动Meme市场智能研究与机会决策**；Intelligence是工作台入口，AI协同引擎是内部能力 | 再建一套交易终端、浏览器插件或独立知识系统 |
| G2 六业务 | 市场/钱包双向发现、单Mint钱包/资金调查、跨Mint群体变化、机制解释、机会可跟随性、持续观察与复盘保持完整 | 必须按六个阶段对每个Mint挨个执行 |
| G3 专业判断 | 分开给出调查价值与机会可参与性；事实由只读工具/可靠数据给出，AI按需选知识、决定补查、竞争解释、反证 | 模型或平台标签可以生成链上事实和确定盈利结论 |
| G4 验收 | 真实首次可见时间、候选母集、跳过理由、暂停/恢复、预算、证据链、只读模拟、后续复盘与AI增益对照 | 离线代码通过、读到知识、12个浏览器候选选中1个便是半自动成品 |

**默认自动化的对象**：已授权的只读数据查询、低成本筛选、按预算补查、变化检测和研究报告。**默认人工决定的对象**：扩大付费/运行范围、交易签名/买卖/付款、向外发布或部署、改动高风险规则。将来如研究逐笔人工确认的交易票据，须独立设计审批与执行隔离；原版 Blix 交易功能保留，但不向新增AI研究工作流开放。

### 14.2 参考成品提供的真正半自动机制

| 来源与核查入口 | 机制 | 迁移到Blix的决策 |
|---|---|---|
| [Million机会服务](https://github.com/Kelows/million/blob/main/apps/api/src/opportunities/opportunities.service.ts)、[Mint反找钱包](https://github.com/Kelows/million/blob/main/apps/api/src/discovery/discovery.service.ts) | 钱包买入触发候选，Mint发现新钱包；过滤、拒绝理由、决策日志及Shadow对照 | 复用原Blix walletSignals→adopt→vet、Wallet/Pulse/Brain；补全候选母集/被拒样本/影子复盘，不复制其交易引擎或把地址簇认作同控 |
| [Pulse周期任务](https://github.com/nirholas/pulse/blob/main/src/collector/scheduler.ts) | 多源事件和快照、生命周期、来源故障与周期任务 | 借观察时钟、负样本、覆盖/故障口径，不搭第二套行情采集器 |
| [PumpTrace回补管理](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)、[观察任务](https://github.com/AntC215/Pumptrace/blob/main/src/modules/watchlists/worker.mjs) | 游标、队列、暂停恢复、限流、重要变化重检 | 优先复用PR23已有经济交易归档/重试/检查点，新增对象级Case接续而非重复状态机 |
| [GMGN Wallet Radar](https://docs.gmgn.ai/index/wallet-radar)、[钱包评分](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-wallet-score/SKILL.md) | 多Mint反查钱包；钱包自身成绩与跟单可行性分开 | 保留钱包角色/持仓/资金与复制延迟/容量两个不同问题，不照搬未实证权重及实际Swap技能 |
| [OKX OnchainOS只读技能](https://github.com/okx/onchainos-skills/tree/main/skills/okx-dex-market) | Token、钱包、榜单、Smart Money、Meme流事件的结构化工具 | 只在现有Blix数据缺口确实需要且获许可时适配；研究与交易Skills隔离 |
| [HoldTech](https://github.com/co-numina/holdtech)、[PumpGrok](https://github.com/swcstudiospace/PumpGrok)、[旧Hermes](https://github.com/sunshihao001/-) | Mint页面自动检测与分析、风险否决与任务票据、Skill交接及恢复 | 复用原Coin/Intelligence和有限服务能力；避免复制Chrome插件、十席Bot和固定七步工作流 |
| Cielo/Nansen/Arkham/Bubblemaps、Synapse、旧Grok/qb-/meme-/Why-Solana | 对象订阅、关系与时序可视化、专业机制、反证 | 保持原作者功能与历史证据来源，不因参考项目被收录就视作已接入API或获得真实经济归因 |

### 14.3 同一引擎的四类半自动使用方式

**入口A：指定Mint/Wallet/Group。** 用户打开原Coin/Wallet或输入简短目标，系统对目标自动选有限的只读查询、专业知识和反证；缺数据或额度不足则记录UNKNOWN并可恢复，不让用户逐步指挥。

**入口B：市场/钱包事件自动发现。** 原Blix新发、迁移、异动、已观察钱包买卖、资金或库存变化进入同一候选集合，事件与来源去重；先运行确定性安全/时效/流动性检查，再由AI按信息价值决定研究哪些对象、哪些不选。允许“没有值得调查/提醒的对象”。

**入口C：持久观察与重要变化。** 用户开启Mint、钱包或群体Watch后，新交易、新接收钱包卖出、跨Mint资金候选、流动性变化或反证更新才能触发再分析；要有去重/限频/配额/故障暂停与恢复。未开启外发通知时只留本地Case，不擅自发送。

**入口D：只读机会演练与影子研究。** 冻结当时可见信号、报价、滑点、延迟、费用和退出约束，跟踪已选和未选对象；对比同一候选全集、同样时间/成本的原Blix和AI增强，不得用未来高点倒填信号。用户保留继续深查、观察、忽略与停止的决策权。

这些是**可选入口和运行自主程度**，不是四个必须顺序执行的开发阶段。原有交互式AI调研是起点，不是半自动目标的全部。

### 14.4 三重业务闭环：发现、调查、反馈

~~~text
原Blix市场事件 ─┐
原Blix钱包事件 ─┼─> 去重的Mint/Wallet/Group候选与首可见时间
已关注对象新证据┘                   |
                                 v
               数据质量+低成本确定性初筛
                                 |
                     AI决定是否值得补查
                                 |
             选择专业知识/原有工具/竞争解释
                                 |
              +------------------+-------------------+
              |                                      |
       Investigation Value                    Opportunity Viability
        调查价值/持续研究                      可参与性/只读演练
              +------------------+-------------------+
                                 |
                  新事实→复核→纠偏→修订下一次选择
~~~

- **发现循环**：钱包找Mint、Mint找钱包、市场事件找Mint、旧Case找新Mint；不能把同源市场事件重复投票，也不能把共享服务当共同控制。
- **调查循环**：D01–D12和旧Hermes/Grok/qb/meme的知识以“适用条件→需要什么证据→哪项现有工具→竞争解释→可推翻条件”参与任务，不把全文和固定层级一口气交给模型。
- **反馈循环**：保存未入选却后来大涨的对象、入选后失败的对象、事实被反证和数据源断流的Case；区分判断错误、观察延迟、漏采、执行成本和外部市场变化。

### 14.5 一个可交付的半自动Case与告警契约

最少保存：task/case ID、目标Mint/钱包/群体、入口与触发事件、事件发生时刻、供应商首次可知时刻（不可得则UNKNOWN）、链上签名与资产/Pool/Owner语义、来源及归档覆盖、被选/跳过原因、模型/知识/工具版本、权限预算、调查价值、机会可参与性、竞争解释与缺失字段、下一次重查条件、Case暂停/恢复及后续结果。

**仅实质高价值新候选触发机会提醒**；消息应包含Mint、信号时间、可核查证据、资金/钱包、流动性/执行限制、竞争解释、失败风险与UNKNOWN。无可靠候选不推送常规“机会报告”。普通健康/离线故障状态与机会通知分开。外发渠道在用户单独授权前不启用。

### 14.6 现有代码承接、验证门槛与最短实施顺序

| 新目标 | 现有可见底座 | 尚需真实验收 |
|---|---|---|
| 自动候选 | 原Blix engine/triage/early/walletSignals、PR23 Pulse有限选题 | 当前浏览器最多12币不是全市场自主发现；须核对候选母集/被拒/第一可见时间 |
| 模型按需研究 | PR23 intelligence/index、ai-workflow、知识加载、Mint事实与本地经济报告 | 仅有限白名单能力；需有许可的真实Mint归档、正确的读接口安全隔离、UI→事实→模型→报告验收 |
| 对象级持续任务 | 原Tracker/SQLite/Journal、PR23经济ledger与检查点 | 独立AI Case的持久任务、增量触发、配额、重开/监控、告警仍未证实上线 |
| 只读机会评价 | 原Brain/Paper、PR23 followability-replay | 有效的实际首次可见、当时入/出报价、成本与退出流动性；不能把纸面算术当真实盈利 |
| AI增益与纠偏 | 现有测试/案例/旧专业知识 | 同样本同成本对照：及时性、漏/误选、研究覆盖、误归因、净可参与性、每次研究的模型/API支出 |

**首先要完成的最短真实闭环**：一条已获授权的真实Blix市场/钱包事件 → 自动进入候选 → 只读工具和知识选择 → 证据化调查与两个独立价值判断 → 本地可重开的Case卡片 → 新事实引起复核。若数据/模型/运行条件不足，停在明确的不可用状态，优先修现有来源事实链，不能用更多AI文本代替真实数据。完成这条再扩大自动订阅、通知和多Mint研究规模。

**来源与状态说明**：本节是目标和设计决定，外部项目只核查了列出的README/代表性源码；本轮未安装它们，也未执行交易、真实模型调用或全市场数据采集。PR23/PR24仍需按最新状态核对；不把本节文档更新视为产品已经上线。
