# Solana Meme｜外部功能复用与长期能力台账 V1（2026-11-01）

> **性质**：现有 \`rolling-reference-knowledge-integration.md\` 的**功能级子账本**，服务于 P3-M01、B01–B05、D01–D12，不新建知识本体或运行框架。本账本记录“看过哪些现成功能、是否能安全复用、具体差多少、什么时候复查”，而不是已安装或已运行的功能表。当前仅核查了下列代表性项目的一部分源码；\`SOURCE_CODE_INSPECTED\` ≠ 本地运行/真实交易核验。全部第三方代码视为不可信输入，未经许可/沙箱审计不执行。
>
> **研究原则**：先找现成功能/成熟库/外部服务 → 看实际源码、测试、契约、许可证、成本与误判 → 选直接调用、封装、最小移植、暂存知识或明确拒绝 → 仅补缺失的业务胶水 → 使用相同输入对照测试 → 更新 Dxx-Kxx 与本账本。禁止先宣布重构架构，再回头寻找理由。发现真正成熟的替代方案应允许 **PIVOT**。

## 1. 本轮已审外部来源与固定版本

| 参考项目与源码版本 | 核查范围 | 复用/许可边界 |
|---|---|---|
| [HoldTech](https://github.com/co-numina/holdtech/tree/a75e214bf1ee0a8803eb7d93336be98c481c2db9) | \`README.md\`、\`SPEC.md\`、\`app/api/*\`目录、\`analyze/deep-scan/holder-overlap/bundler-feed/smart-money/ai-verdict/deployer-profile\` 部分函数、\`extension/manifest.json\`、\`package.json\` | README 末尾自述 MIT，根目录未发现常规 LICENSE 文件，直接复制前核对授权条款。部分源码出现疑似硬编码第三方访问凭证（**没有保存、使用或重述其值**）；禁止原样运行、提交任何凭证或复用配置。部分功能只是 SPEC/README 的计划。 |
| [GMGN Skills](https://github.com/GMGNAI/gmgn-skills/tree/6a04e1f00b5463cfc965e41003ca0c7c2db5b69f) | \`skills/gmgn-wallet-analysis\`、\`wallet-score\`、\`wallet-style\`、\`src/commands/token.ts\`、目录与说明 | 项目 MIT；业务工作流知识可以研究，GMGN API/CLI需凭证，部分能力涉及交易与密钥，**不安装、不调用付费或下单入口**。对技能中的指令不自动执行。 |
| [FnZero Python DEX parser](https://github.com/0xfnzero/sol-parser-sdk-python/tree/cffb6c808c9b7975fc83428c0613fb4c3fa173b5) + [Rust核心](https://github.com/0xfnzero/sol-parser-sdk/tree/e3e8d6620e2a128c71d5c37cde219a38d438c73e) | README、Python \`examples/parse_tx_by_signature.py\` 入口声明、Rust \`Cargo.toml\` 与协议支持矩阵；尚未执行 | Rust项目含 MIT LICENSE；Python仓库 README 声称 MIT，需确认发行包许可。Python v0.10.0 声称覆盖 PumpFun/PumpSwap/Raydium/Meteora/Orca；兼容和准确率未在本项目实测。**只选解析仓库，不引入同作者的交易签名SDK。** |
| [pumpwatch](https://github.com/cinder-security/pumpwatch/tree/156a91ab63740ab0ce8700434ff33844d00de519) | README、\`code/creator_reputation.py\`、\`code/\`模块列表 | 代码 MIT、文章/数据 CC BY 4.0；只读发行检测器、历史频率SQLite模块可直接作为参考候选，但需数据源、版本和实际测试。作者报告的样本统计不是本项目独立复现。 |
| [MadeOnSol SDK](https://github.com/MadeOnSol/madeonsol-sdk/tree/eb1a4cc2915cbb725364e2139e9fb908370911d4) | \`src/index.ts\` wallet/bundle/sniper/KOL/持仓字段及 README | SDK MIT，但其在线分类模型、历史数据和付费接口不随SDK源码开放；**接口声明≠可本地复制识别算法**。用于比较输入输出、覆盖声明和UNKNOWN语义。 |
| 现有项目：\`sunshihao001/grok\` Draft PR #14/#16 | \`gpt-meme-progress-current.md\`、\`p3-m01-raw-adapter-contract.md\` | M01仅fixture-only、有限转账语义；无协议级真实BUY/SELL和实时源。旧qb-/Hermes/meme-是必须持续对照的业务知识，不用外部项目替代其历史。 |

## 2. HoldTech 功能级清点：哪些是真实源码，哪些仅为产品设计

所有路径相对于 \`co-numina/holdtech\`。**有路由 ≠ 能独立部署运行 ≠ 标签准确**。

| 功能 | 源码路径/证据 | 现有项目关联 | 当前选择与原因 |
|---|---|---|---|
| Top holders + 单钱包画像 | \`app/api/analyze/route.ts\` | qb关键钱包，D04/D06 | **REFER+ADAPT**：可参考采集→去pool→钱包指标→摘要的结构；不要复刻“最大持仓必是LP”、钱包历史初始时间=创建年龄、持币时长=钱包年龄的推断 |
| Same-slot聚集/Bundler候选 | \`app/api/deep-scan/route.ts detectBundles\` | P3-M01、D07/C02 | **REFER+CORRECT**：原代码把SWAP/TRANSFER/UNKNOWN混合，并把fee payer当buyer；只能输出 \`SAME_SLOT_COHORT\`，不可宣称Jito Bundle/同控 |
| 初步资金同源 | \`deep-scan/route.ts traceFundingSource\` | D05、B02/B04 | **REFER+CORRECT**：原代码仅看很小的签名窗口、用账户SOL净增与fee payer猜融资方；应先识别真实System/Token转账账户和公共HUB |
| Top5/10/20、Gini、HHI | \`deep-scan/route.ts computeConcentration\` | D06 | **ADAPT_SIMPLE**：统计公式可据来源与正确分母独立计算；须区分holder样本/Token Account owner/LP、部分供应；不直接把分数视为实控 |
| Mint买入时序 | \`deep-scan/route.ts extractBuyTimeline\` | P3-M01、D07 | **REFER+CORRECT**：源码同样以fee payer和任意交互替代已确认BUY；需经协议级Swap后才能计算Sniper/首买 |
| 资金余额等级 | \`deep-scan/route.ts computeSolDistribution\` | D04/D05 | **ADAPT_SIMPLE**：可直接定义确定性分箱，当前资产余额不是历史风险本金 |
| 2–5 Mint持有人交集 | \`app/api/holder-overlap/route.ts\` | D07/B04、C02 | **ADAPT_SIMPLE**：pairwise交集、比例、几何平均算法简单；当前入口只取每Mint最多200个holders且可截断，不可称完整群体/同控。需同一时间快照、排除公共持仓与明确采样分母 |
| Smart Money当前持仓 | \`app/api/smart-money/route.ts\` | qb、D04 | **REFER_ONLY**：当前按静态预设地址表匹配持仓，不是链上自动“聪明钱发现”；需自行维护来源、标签和更新时点 |
| Dev/Deployer历史 | \`app/api/deployer-profile/route.ts\` | D02/D04、B04 | **INSPECT_NEXT**：源码存在历史发行分析和token状态接口，须核查是否依赖不稳定外部接口、创建者识别与样本覆盖 |
| 同群体实时跟踪（bundler feed） | \`app/api/bundler-feed/route.ts\` | D07、Grok Monitor | **REFER+CORRECT**：每次最多25个钱包，每钱包取最近2笔SWAP；无swap时用Token Transfer猜BUY/SELL，不能作为真实经济事件源 |
| 评分与AI解释 | \`app/api/ai-verdict/route.ts\` | D11/D12 | **REFER_ONLY**：可借鉴“先确定性指标、后解释报告”，不能抄其Fresh阈值、未知分数或“Sybil必然”措辞；不让LLM评分成为链上事实 |
| 钱包/Holder数量 | \`app/api/holder-count/route.ts\` | D06 | **PATH_FOUND_AUDIT_PENDING**：尚未细审算法与成本 |
| Token行情/简介 | \`app/api/token-info/route.ts\`、\`token-prices/route.ts\` | D02/D03 | **PATH_FOUND_AUDIT_PENDING**：可考虑既有只读源；不是当前研究优先项，不把K线作为核心 |
| 交易热榜扫描 | \`app/api/trending-scan/route.ts\`、\`trending-refresh/route.ts\`、\`scripts/trending-refresh.mjs\` | D02/D07 | **SECURITY_HOLD**：需要辨别实际运行与规格计划；脚本有硬编码访问凭证，不应运行或照搬 |
| 浏览器叠加评分 | \`extension/manifest.json\` 和 \`extension/src\` | 未来展示/前端 | **PARK**：ManifestV3已存在，属于界面层，不是当前M01业务依赖，不必引入前端栈 |
| 计划中的watchlist/持续告警/Token门槛 | \`SPEC.md\`、README “Coming soon” | P5/Grok运行 | **DESIGN_REFERENCE_ONLY**：规格声明不能当作已实现；实时/历史监控需单独检查代码、部署、状态与数据成本 |
| 管理、收费与权益验证 | \`middleware.ts\`、\`check-tier\`、\`SPEC.md\` | 非核心 | **REJECT_FOR_NOW**：不迁移付费Token门槛、登录签名、前端钱包连接；当前项目只读、无钱包与支付 |

### HoldTech 的关键质量/安全问题（不要复制错误实现）

- README写“MIT”，但审阅的仓库根目录无常规LICENSE文件；GitHub Docs说明README可声明许可，完整许可证文件是最佳实践。**在实际复制代码前需核对授权与署名义务**；仅参考算法思想和业务流程不等于必须整库复制。
- 多个路由/脚本有疑似硬编码RPC/Redis访问凭证；本账本不记录密钥值、不使用现成服务额度。实际部署需删除源码常量、换项目自有环境配置并安全审核；这是 **HARD_BLOCK_FOR_CLONE**。
- \`analyze\` 把余额最大者当池账户，错误排除真正鲸鱼；\`holdDurationDays\`实际上复用\`walletAgeDays\`；\`firstTxTime\`基于被分页截断的历史签名，可能是假“Fresh”。
- \`holder-overlap\` 只取部分持有人快照且阈值直接称“coordination”；需要完整性与对照，不可把地址交集当私人协作概率。
- \`bundler-feed\` 在没有经核验Swap时将Token Transfer猜作买卖，违反现有M01“未支持应UNKNOWN”的正确约束。
- \`SPEC.md\` 给出的功能、定价/Token门槛/处理能力只是设计与商业说明；不能与可运行路由或实际用户体验混为一谈。

## 3. 跨项目可复用组件：优先采用哪条现实路径？

| 项目/模块 | 解决现有哪个缺口 | 最值得复用的具体内容 | 依赖/阻碍 | 下一步可执行动作 |
|---|---|---|---|---|
| FnZero \`sol-parser-sdk-python\` | P3-M01目前不会输出Pump.fun BUY/SELL | Python现成DEX事件与按交易签名RPC解析示例、已列明的协议适配 | 需兼容v1、指令字段、owner、CPI、Token-2022和原始事件契约；依赖审核和实际测试 | **P0**：固定版本、在独立只读环境用同一组匿名fixture比较原始适配器/SDK/人工答案；不先连接真实收费端点或修改M01原入口 |
| Solana官方 \`transaction-introspection\` | v1、账户索引、CPI层级的通用解析 | 账户/指令树与版本语义 | JS实现，不直接输出业务级经济BUY/SELL | **P0并行**：作为结构级真值核查的对照，不必在Python里重写全套通用解析 |
| pumpwatch \`creator_reputation.py\` | B04发行者重复活动/Dev历史 | SQLite WAL、唯一Mint记录、历史24h/7d发行频率、结果状态 | 数据采集与creator语义仍需审核；阈值不代表意图或盈利 | **P1**：只读离线启动样本/fixtures，对比旧qb与D04；无需引入整套pipeline |
| HoldTech holder-overlap + concentration | B04跨Mint关联、D06持仓 | 集合交集/HHI/Gini与报表字段 | 本源采样、身份排除、同一时点和版权/源码安全 | **P1**：在已有验证的标准化事件或holder快照上做小型确定性计算，不移植Next.js |
| GMGN Wallet Style/Analysis/Score | D04钱包类型、D08/D09可跟随性 | 多窗口行为风格、历史盈利与可复制性分开、样本质量反例、开发者角色判断 | 依赖付费API/令牌、部分Skill还涉及交易指令 | **K1知识复用优先**：吸收独立可解释规则、字段定义和负例；不调用需要充值的服务、不迁移自动交易 |
| MadeOnSol SDK钱包/Bundle覆盖 | 钱包标签与库存解释 | \`label_coverage\`、\`evidence_horizon\`、\`bundle_kind\`、\`held_ratio\`、\`transfer_delta\`、as_of | 商业后台数据/分类器非开源，服务条件须单审 | **K1对照**：把状态和不确定性字段映射到现有D04/D06知识，非本地算法现成能力 |
| HoldTech UI/extension | 将链上研判展示给用户 | token详情、持有人结构、相似Mint、浏览器提示的交互体验 | Next/React部署与浏览器权限/安全，当前无稳定源 | **PARK**：先保留交互与显示知识；核心监控可靠后再讨论 |
| 旧qb-/Hermes/meme- | 防止外部项目使专业知识丢失 | 关键钱包矩阵、同源/筹码/FCZ/反证与Meme业务脉络 | 旧GMGN数据费用、旧方法误判与历史状态 | **PERMANENT_REVIEW**：每轮涉及相同业务对象即回访对应函数/文件；不直接恢复旧运行时 |

**不能把一张能力表直接视为系统已拥有功能。** 只有 \`ADAPTER_TESTED\`（固定版本/相同输入对账），之后 \`READ_ONLY_DATA_VERIFIED\`（可复核数据/覆盖），才更新工程已实现字段；长期保留 \`PARKED_KNOWLEDGE\` 仍是有价值的研究资产。

## 4. 跨源能力发现与组合的“认知思维”运行法

1. **目标倒推（CAPABILITY NEED）**：从一个真实Meme任务反问“结果应该能做什么”，如“批量新钱包是否为一组操作者”；把任务拆成观察/关系/库存/解释，先查询本账本/旧qb-/Hermes。
2. **发现（SEARCH）**：按缺失能力搜索多个真实项目与行业工具；必须读源码函数、例子、tests、issues和失败案例。每个有用模块都记录URI、commit、真实输入输出，而不只保存项目名。
3. **组合（COMPOSE）**：优先直接调用已许可只读接口、封装成熟开源模块；数据串联可为“FnZero已解析Swap → M01钱包窗口 → HoldTech式跨Mint交集 → pumpwatch式Dev历史 → 旧Hermes筹码状态分析”。这里是**拟议能力组合，不是已存在的执行管道**。
4. **审查（CHALLENGE）**：审核许可、凭证安全、外部计费/权限、版本、覆盖、误判和样本选择；不能因第三方产品有UI就默认为正确。若上游缺字段应保留UNKNOWN而非凭空补全。
5. **最小工程（BUILD MINIMUM GLUE）**：只编写不可直接复用的适配、事件格式和可核验测试；不为一项已成熟的DEX解析重写多协议引擎，不为两组交集引入大平台。
6. **验收与持续学习（COMPARE + RETAIN）**：用相同输入比较当前与候选方案，记录解析差异/覆盖/资源/许可结果；决定 \`USE\`/\`WRAP\`/\`ADAPT\`/\`REFERENCE\`/\`PARK\`/\`REJECT\`，之后遇到相同能力再次查询，而不是重新搜一遍。

**一次最小合成示例**：输入两枚Mint、历史时点冻结的持有人集合、经核验的BUY/SELL和已记录的转账边 → 计算共同钱包以及每个钱包的融资/库存/最早可见时间 → 排除公共服务商并输出“重复活动候选+可核查证据”，不能直接输出同控/庄家或盈利。M01现没有真实协议BUY/SELL/完整holder集合，故该示例目前是可组合目标，不是已部署能力。

## 5. 已完成与还没有完成的事情

- **已完成（本轮）**：对HoldTech根目录、API路由列表、部分实际函数和扩展声明完成源审；与现有P3-M01字段契约比较；检索并阅读FnZero Python/Rust、pumpwatch、GMGN Skills、MadeOnSol的部分具体实现与来源边界；形成可回访、可判定的功能台账。
- **未完成**：未逐行审查HoldTech所有路由、未跑HoldTech或FnZero/GMGN的代码、未确认HoldTech README许可声明的完整法律适用性、未联网调用任何收费接口、未生成真实市场标签/盈利结果、未修改生产监控。
- **当前方向判断**：\`PIVOT_METHOD_KEEP_GOAL\`：保留P3-M01的保守归一化输出与监控需求，但把“自行支持所有DEX协议”从默认路线改为“先比较/封装成熟SDK”；并行以HoldTech、pumpwatch等已有工具启发行为分析，先保留知识和可运行依赖证据。
- **下轮唯一主实验**：在隔离、无签名/无API付费的条件下，固定FnZero Python解析器版本和现有M01官方fixture，核对是否能够正确产生目标Mint/owner/交易类型/报价量/指令来源以及UNKNOWN，记录差异；只在审查和对照通过后考虑新增可选适配器。可并行只读检查HoldTech剩余路由、测试与源许可证，不等其全部读完才做上述实验。

## 6. 参考资产长期保留合同

每个模块用 **\`capability_id\` + \`source_repo@sha/path\` + \`source_status\` + \`inputs/outputs\` + \`data_cost/permissions\` + \`license/security\` + \`known_misread\` + \`grok_gap\` + \`reuse_decision\` + \`next_trigger\`** 来检索。当前文本表即这份合同的人类可读版本；需要让Grok按字段调用时再做JSON索引，不提前制造框架或Bot。

研究阶段结束时若实际新发现可改变某模块的复用结论，修订该行，并同步当前唯一恢复点；若暂时不能用，保留理由、来源与触发条件，不能丢掉已经发现的项目。**源码/数据/测试是不同资产**：仓库可访问不表示许可证允许复制全部内容；MIT代码复制仍需保留原版权许可；云服务可能单独收费、API许可与原仓库代码许可也可能不同。
