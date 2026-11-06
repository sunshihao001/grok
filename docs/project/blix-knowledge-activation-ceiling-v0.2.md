# Blix 主体实际能力与旧 Grok 知识内化｜纵深审查 V0.2

> 日期：2026-11-06。Blix 分支审查基准 `bbeb31a541c73cc2a5b95688faa71d56ad3ae6b6`；历史 Grok main `fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a`，Hermes `2bf694b37cce25b4a3c9364298b784039f3ecc84`，qb- `8377ad5611255df5cd4562666a826708575334f0`，meme- `5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a`，知识 PR #14 `eeb40b050369e4525919500f144325c9a9fc8b74`，Why-Solana `9a7ad51d56328e91e67e3f531d6744307d0ee68b`。**当前仅 SOURCE_READ / HISTORICAL_DRAFT，不是程序验收、模型自动学习或真实经济结论**。没有执行代码、调用链、启动Bot、安装依赖、修改业务代码或支付。
>
> 已有[主体能力与旧知识继承基准](blix-heritage-capability-baseline-v0.1.md)和[知识与证据应用](knowledge-use.md)已覆盖总览和三类案例。本文件只补真正欠缺的：**主体业务上限、旧知识方法的具体专业转化、哪些旧假设不能照搬、以后参考成品应按什么缺口比较。**

## 1. 对 Blix 能做到的程度，给出有边界的判断

| 用户真实业务 | 当前 Blix 已实现的源码路径 | 能做的最强静态判断 | 尚缺或未证实 |
|---|---|---|---|
| **市场自动发现** | `web/src/pages/Pulse.tsx`、`Coins.tsx`、`server/engine.js`、`quality.js`、`coverage.js` | 发现→市场指标→候选过滤→图表与信号，原产品已有比较完整业务链 | 全Solana多平台覆盖/漏检、7×24稳定率、实时准确性 |
| **Mint 单币调查** | `Coin.tsx`、`coin.js`、`holders.js`、`holderslive.js`、Dev、AI、Bubble Map | 现成完整页面可展示交易、Creator候选、持仓、价格和标签 | 不同来源/Slot/分母、完整历史资金/库存、真实控制权 |
| **关系/资金图** | `bubblemap.js` RugCheck网络、首笔funder、同Slot、公共Hub排除与最长4跳 | 对头部Holder构造**候选**关系图、部分群体持仓比例 | 直接SOL资助与代付手续费混淆、历史截断、非Holder及跨币资本闭环 |
| **钱包追踪** | `wallets.js`、`wtrack.js`、`walletpage.js`、Tracker UI | 对已追踪地址观察买卖/部分转账与PnL；`wtrack.js` 单成员限额200钱包 | 自动发现所有相关地址、CPI多腿无损、B收到Token再出货的完整归因 |
| **近期事件与历史** | `coin-flow.js` 5分钟焦点Mint窗口/最多32焦点、`journal.js` 部分成交约24h、`wtrack.js`活动约7天 | 有短窗口统计、链上/供应商事件、保留及缺口机制 | 跨Mint 6/12小时**全链资金**连续记录、跨场所完整与断流补数验收 |
| **AI研究和Web/Grok入口** | `triage.js`、`research.js`、`brain.js`、React/经典Web、HTTP/SSE/MCP | 交易候选、叙事、纸面回访和网页交互的成熟源码；无需再造市场网站 | AI自发理解未见经济机制、旧知识自动调用与实际增益、Grok Bot云端可靠运行 |

**判断**：Blix是“已有完整市场终端＋部分专业钱包调查能力”，不是空架构；未来的跨Mint经济主体研究、资本循环、持续异常与可证伪机制，是在现有业务上深化的真实缺口。**不采用没有实测依据的完成率百分比**。代码存在≠本fork已在安全环境运行。

## 2. 原有 Grok 知识已经保留了什么，为什么不能再整体迁移一次？

- [main 15张来源固定的专业知识卡](https://github.com/sunshihao001/grok/blob/main/knowledge/catalog.v1.json)：包括市场入口与生命周期、钱包角色、同源、Sybil/Wash、集中度、Dev、GMGN字段、证据综合、研究状态、未验证的策略理论与防假完成。每项有适用证据、竞争解释和边界；可以作为**按问题找原文的入口**。
- [main 21份原始知识快照与manifest](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/manifest.json)：固定原文和Commit、未经全部独立审阅；适合回查概念和旧设计，**不能当现行真值**。
- [main 17项来源索引](https://github.com/sunshihao001/grok/blob/main/knowledge/source_index.v1.json)：提供 Why-Solana、Hermes、qb-、meme- 的定向来源；不需要复制外部仓库。
- [PR #14 专业主册与12域/152问题/22知识视角](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-core.v1.md)：从D01账户事实、D02生命周期、D03市场微观结构、D04钱包角色、D05资金网络、D06筹码/控制、D07时序、D08策略、D09执行、D10数据、D11反证到D12 AI。这是**专业问题全景与来源导航**，152条标记为 `mapped_unverified`，不是152条已验证结论。
- [PR #16](https://github.com/sunshihao001/grok/pull/16) 是历史Python单Mint真实供应商预览和fixture批量监控；一次实测5池、20个Token Account候选和1个AMM交叉命中**不是**Blix产品验收。[PR #17](https://github.com/sunshihao001/grok/pull/17) 是旧路线知识工程协同Draft；不能整个合并Blix。
- **状态分开**：已有`SOURCE_LINKED`的导航 ≠ `KNOWLEDGE_APPLIED`的专业判断 ≠ `RUNTIME_INTEGRATED`的程序 ≠ `VERIFIED_VALUE`的可靠改进。

## 3. 重点：原 Hermes 的“专业认知内核”实际是什么？

**一｜问题驱动而非字段驱动。** [00c 思维模型原文](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00c-GMGN-思维模型提炼.txt)提出：先问要理解什么市场事实→该事实留下什么可观察痕迹→哪个字段实际测到→怎样组合→什么分母/窗口让组合有意义。其 Raw/Feature/Structure、必要/增强/警告和“可说/不可说”有价值。

在 Blix 上，“Top10增加=庄家吸筹”就应被重构为：**变化的到底是Token Account还是Owner？供应量/Pool排除/Slot是否一致？存在真实的Token转入、净买入还是重新计数？** `holders.js`和`coin.js`的分母与来源不同，未统一前不能从数值跳到控制身份。

**二｜同样的数据，观察不同经济关系。** [00d 多维度原文](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00d-GMGN-多维度推理扩展.txt)从钱包角色演化、资金同源与行为时差、价格冲击、生命周期等重问同一组GMGN数据；这不是要新建四种Bot。对 Blix，`wallets.js`看钱包交易、`bubblemap.js`看关系、`journal.js`看部分成交，必须追问**Token库存从谁转到谁、谁承担成本、谁获得卖出SOL、是否跨Mint再投入**，这些才是经济主体问题。

**三｜超越已有标签产生未知机制。** [00e 异常与反向推演原文](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00e-字节反推框架-突破认知局限.txt)提出反向假设、异常对照、时间序列、无标签分组与跨环境比较。可帮助发现“同群体成员替换”“库存与价格背离”“交易链停顿后恢复”等候选机制。

**必须主动否定的旧捷径**：00d里“同源+成本近+同期买→极高概率同一实体”、00e里小样本或穷举字段配对就会产生某比例新发现、旧Hermes Evidence Chain固定0.8基准置信度，均未经过独立校准；都只能当**假设与待证问题**。不能迁入Blix确定性标签/自动交易门控。

## 4. qb- 与 meme- 的知识应怎样真正“进入”Blix

### qb-：调查组织与对象选择，不是旧GMGN脚本搬家

[主脚本](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)确有八表 + Markdown：分析深度、代币基础、结构指标、**关键地址矩阵、基础设施名册、低权重地址范围、复查计划**、摘要。它还将LP地址从普通钱包排名排除，把转入后卖出的地址当作优先复查候选。

**对Blix的明确价值**：已有Coin与Bubble Map应能把“当前头部Holder”深化为**关键地址/设施、Token接收与转出、资金关系、证据缺口、后续跟踪计划**，让用户少自己挑钱包，而不是复制qb的CSV/UI脚本。旧`classify()`主要依赖GMGN标签与启发式E2/E3/E4，不能当真实身份/概率。脚本含`subprocess.run(...,shell=True)`，不得在当前环境直接运行。

### meme-：构造供需/价格/库存的竞争解释，不证明庄家身份

[原成熟度审计](https://github.com/sunshihao001/meme-/blob/main/第一控盘区成本中枢回收模型_成熟度审计.md)把POC/AVWAP回收、深洗、二次启动评为**结构化观察模型 Level 2/5**，并承认自动检测、阈值、回测未完成。它的MQL5背景不等于Solana链上真实经济成本。

**对Blix的明确价值**：围绕Coin市场图表/流动性和旧钱包库存，研究价格上涨但老地址转出、集中度下降却上涨、Pool变薄后价格冲击等**对立解释**；不由K线形态推出幕后共同控制或预测盈利。

### Why-Solana：只取有信息价值的研究问题，细节留到参考项目阶段

[研究方法](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/METHODOLOGY.md)和[经济循环](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/economic_mechanics/README.md)提示：初始资金→同槽买入→Token转到退出钱包→SOL回流→另一Mint再出资，可能形成可重现的资本循环；但**有结构不代表知道控制者、更不代表可复制盈利优势**。其样本和结果不能外推为所有Mint的真相。

[作者书面分析许可](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/LICENSE-CONTENT.md)为CC BY-NC-ND 4.0，代码另有MIT；本文只概括研究问题并附链接，**不全文搬运其文章**。

## 5. 从“文件已放进主体”升级到“主体能够应用知识”还差什么？

| 连接层次 | 应负责的东西 | 当前状态 |
|---|---|---|
| **发现入口** `AGENTS.md`→`docs/project/README.md`→`knowledge-use.md`→旧资料 | 按用户实际业务选对应知识，持有原来源 | **已有；本轮深化源码和方法** |
| **知识适用与推理**（对话研究或未来Bot） | 明确事实、所需字段、适用条件、错误捷径、竞争解释、补查价值 | **本轮给出专业示例；Bot自动调用未验** |
| **产品实际输出** `Coin/Wallet/Bubble Map/Research` | 把必要知识转成报告字段、解释、缺失与可追溯链上事件 | **当前未修改代码/未集成新界面** |
| **实证反证与修订** | 同任务对照、真实Mint/反例、历史回补、纠错与可执行性 | **未验收；不能宣称模型学会** |

三个应用样例：
- **“10个钱包同步买，是不是一个人？”** → Blix同Slot/首funder + Hermes与D04-D06的角色/资金/公用设施反证 + qb基础设施名单；正确输出“有关联候选，但控制者UNKNOWN”，不能直接给“庄家概率”。
- **“拉升前12小时转账多了？”** → Blix已跟踪地址活动、Journal与局部5分钟流 + Hermes00d的行为演化、meme的市场阶段假说 + D07缺口/时间；完整跨Mint资金记录不足时不能判断“吸筹已确认”。
- **“A买了、转B卖出，收益去新币C？”** → Blix当前交易/转账、Coin、Bubble Map + qb关键地址矩阵 + Why资本循环研究；须追每段交易签名/Token账户/对价/净SOL/资金路径及跨币时间，不以钱包连线替代资产闭环。

**本轮真正的路线认识**：优先复用Blix整个产品，用旧知识提高现有事实的解释质量；真正缺的不是另一个资金图，而是**跨模块原始经济事件与时间连续性、候选假设的实证反证、持续观察的可靠历史**。

## 6. 下一步深入解剖外部参考项目的正确入口

现在已有足以挑选参考项目的问题，不必按65资产名单逐仓库介绍：
1. **实际资金闭环/非Holder地址**：先看 Million、Why-Solana 等哪些真正追Token转移→退出钱包→SOL回流，并处理CPI/公共服务/历史截断；对比Blix 4跳图，区分真实能力和仅可视化。
2. **跨Mint群体监控与长时保存**：看 Million、HoldTech、Pulse 是否有整套成员变化、失败恢复和告警；不因都叫“监控”就并行复制第二套程序。
3. **成熟供应商/部署成本**：看OKX/Helius/其他只读接口覆盖与配额、时间/Slot、钱包历史；直接使用或轻适配优先。
4. **最终业务/网页**：保留Blix现有React/UI，只有外部成品完整业务实证更好时再考虑替换单环节；对照许可、鉴权、付费与安全。

**最有价值的下一项静态研究**：追踪一条贯通用户任务 `发现Mint→A初买→转Token给B→B出售→SOL资金转向下一个Mint`，检查Blix已有各模块在哪一段缺源、缺时间或丢失经济动作。再用这一明确缺口决定外部成熟项目的深度解剖对象，而不是先堆项目清单。
