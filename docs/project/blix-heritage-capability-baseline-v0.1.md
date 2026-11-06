# Blix 现有产品能力 × 旧 Grok 专业知识继承｜主体理解基准 V0.1

> 时间：2026-11-06。当前主体：`sunshihao001/grok` 的 `blix` 分支，基准 `a5f8b162657a453b697f5ab7614d55c618f1e638`。研究方式：GitHub 源码/README/官网生成器、旧 Grok PR #14/#16/#17、Hermes、qb-、meme- 的代表性原始文件和历史验收文档交叉审查。**没有运行 Blix，没有复制历史代码、合并 PR、启用 Bot、安装依赖、连接模型或调用真实链上接口。**
>
> 用户目前要求的次序是：**先知道 Blix 大概能够做什么 → 让主体按真实业务理解历史 Grok 的专业知识 → 找到需要完善的实际功能与业务位置 → 最后再逐个深入解剖新的成熟参考项目。** 本文不是第13个知识领域、不是新架构、也不是先验确定最终扩展层。

## 1. 产品定位：Blix 是已有完整终端，不是等待重新设计的空壳

Blix 原作者的完整业务是：**Discover → Enrich/Safety/Score → Signal/Narrative/AI → Coin/Wallet/Trade → 历史回访/风险/Health**，拥有 React + 经典网页、Node Radar、SQLite、Cloudflare Worker、HTTP/SSE/MCP、Wallet Tracker、Journal、价格与成交通路、Bubble Map、用户/交易路径。

我们长期想建设的产品是：**市场发现/垃圾过滤 → 单 Mint Creator/资金/库存调查 → 跨 Mint 群体与异常持续观察 → 多种经济机制解释、反证和可验证价值**。Blix 的前半段、展示层和不少监控基础都已具备；后半段需要专业事实、连续历史和归因研究，而不是重做交易终端。

**不可以把一句“Blix 已有功能”理解为“当前 fork 已通过主网、24/7 和 Grok Bot 真实运行验收”。** 原项目作者的功能与部署说明是 `AUTHOR_REPORT`；本分支代码是 `SOURCE_READ`；本项目后续真实验收仍 `NOT_RUN`。

## 2. 当前主体的大致能力范围（业务结果，而非逐文件清单）

| 实际用户问题 / 功能 | Blix 当前已实现的源码/产品路径 | 当前可判断的程度 | 不应擅自声称已做到 |
|---|---|---|---|
| 找当天新币、迁移/热门、自动过滤垃圾盘 | `web/src/pages/Pulse.tsx`、`Coins.tsx`、`server/engine.js`、`sources.js`、`quality.js`、`coverage.js` | **成熟业务骨架**：发现、多个栏目、筛选、价格/风险、市场状态与信号 | 对全Solana每种发行平台和每个池毫无遗漏；所有风险盘都能挡住 |
| 观察交易、池、价格、历史与市场异动 | `server/livetrades.js`、`pumpswap.js`、`coin.js`、`journal.js`、`candlestore.js` | **原生多来源观察和历史**：价格、成交流、K线、流动性与行情回访 | 全量链上经济动作、长时间完整跨池成交、可真实成交的策略收益 |
| 输入 Mint、查看 Holder/Creator/Dev/早期交易者 | `Coin.tsx`、`coin/Tabs.tsx`、`server/coin.js`、`holders.js`、`holderslive.js` | **成熟页面与部分真实链上能力**：多数据来源与部分 Token Account→Owner 汇总 | 一个接口就能证明从发行以来所有仓位与控制权；`partial:false` 等于完整历史 |
| 查钱包活动、PnL 和 Smart Money | `server/wallets.js`、`walletpage.js`、`wtrack.js`、`solana.js`、Tracker/Wallets UI | **可追踪和展示的一组业务通路**，但不同账本/解析口径 | 原始交易所有CPI/多腿/SOL-WSOL已无损解析、盈亏全都可归属、群体等于人 |
| 看疑似同源资金/捆绑/持仓群体 | `server/bubblemap.js`、`web/src/pages/coin/BubbleMap.tsx` | **比原先认识更强**：RugCheck graph、首笔funder候选、最多4跳、Hub过滤、群体持仓 | 全历史资金闭环、共同控制、内幕身份、正常共享服务全部排除 |
| 新币AI研究、叙事、候选追踪、事后回顾 | `server/triage.js`、`research.js`、`brain.js`、`desk.js` | **原生市场分析闭环**：快筛、研究、评分、结果回访、Playbook | 能自主把整个项目从目标理解做到部署验收；经济机制已因果验证 |
| 钱包与市场通知、持续数据与状态 | `server/server.js`、`notify.js`、`wtrack.js`、`health.js`、SSE、SQLite | **有监控、通知和工程基础**；保留期限、刷新与数据源不同 | 已验收全天跨Mint连续资金路径、告警无误报/无漏报、Grok云电脑常驻 |
| 现有 Web/API/MCP、运营/配置/账户 | `web/`、`public/`、`server/webapp.js`、`worker/`、`mcp/`、`settings.js` | **已有可用产品结构/工具接口**，不需再造网站 | 本fork自动拥有官网域名、原厂服务/数据、24h部署或隔离了真实交易 |
| 真实交易、发行和账户 | `accounts.js`、`hosted-accounts.js`、`tradeapi.js`、`Launch.tsx` | **存在真实资产功能**，可当原产品安全审查对象 | 用户授权了签名、交易、自动发币、付款或模型费用 |
| 跨 Mint 经济主体、资本循环、前兆与机制研究 | 钱包观察/事件/群体基础可复用；尚无统一完整经济事件层 | **部分底座 + 大量研究空缺**；必须利用旧 Grok 理论和真实外部证据 | 已经是完整专业资金侦察系统、有确定庄家识别或可复制Alpha |

> 上表的“成熟”指**原 Blix 已有较完整设计与代码链**，非本用户环境实跑成熟度评分。当前 `blix` 的只读安全门禁尚未覆盖 `bin/supervise.mjs` 等所有启动路径，故不能按作者原README直接启动。

### 从用户体验而非代码数量衡量主体

一个用户可以从 Pulse 发现币 → 打开 Coin → 看 Dev/Holder/交易/风险/Bubble Map → 观察钱包/加入Tracker → 查看 AI 研究、警报和历史。**这个端到端产品路径在源码中已经存在。** 真正未证实的是：这些路径是否能独立可靠地回答“谁的经济资本在什么时候经哪些账户/池转移、库存如何变化、跨币是否仍是同一经济关系”。

## 3. 必须恢复的“旧 Grok”不是一份相同形态的工程

| 已核对的真实旧来源 | 保存了什么 | 当前真实状态 | 对Blix怎样使用 |
|---|---|---|---|
| [PR #14 知识](https://github.com/sunshihao001/grok/pull/14) | [D01–D12专业主册](https://github.com/sunshihao001/grok/blob/eeb40b050369e4525919500f144325c9a9fc8b74/knowledge/system/gpt-meme-project-core.v1.md)、8层/152问题、22知识视角、65参考资产、机制与反证、全项目收束审计 | **OPEN DRAFT，未合并**。152是研究问题/导航单元，非152条独立验证的市场机制 | **专业问题索引与解释方法的上游真源**，按业务需要选段研究，不全文复制或强制22专家 |
| [PR #16 工程](https://github.com/sunshihao001/grok/pull/16) | Python单Mint报告、地址/池交叉验证、归因失败防护、`wallet_batch_monitor.py` 离线1/5/15分钟群体观察 | **OPEN DRAFT，未合并**；2026-11-01曾在GitHub Actions真实请求供应商，5池+20 Holder Token Account候选；离线Monitor仍非真实长期监控 | **已有证据处理和原型的可选复用来源**；不能把它当Blix内置服务 |
| [PR #17 非破坏性集成](https://github.com/sunshihao001/grok/pull/17) | 知识导航、专业来源和工程PR协同、目标演变记录、角色交接设计 | **OPEN DRAFT，未合并**；基于旧Python产品线，并非Blix新主体 | **继承经过整理的业务/知识连接思想**，不把旧集成分支整个合并进Blix |
| [旧 Hermes `sunshihao001/-`](https://github.com/sunshihao001/-) | [学习10–12](https://github.com/sunshihao001/-/tree/main/learning)、钱包角色/同源、Sybil/Wash、证据链、盘口与LP知识、筹码控制设计 | 研究文件与Python Skills存在；置信度和决策阈值有未校准示例 | 接入 **Coin/Wallet/Bubble Map分析的概念与反证**，不继承固定7 Skill强制流程和未经证实的高置信结论 |
| [旧 qb-](https://github.com/sunshihao001/qb-) | [`sikk_gmgn_token_report.py`](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py) 的多表单Mint报告：关键地址矩阵、基础设施名册、低权重范围、复查计划；历史项目有数据与快照 | 有脚本与大量归档，**不是当前GMGN免付费/在线可用证明**；脚本调用外部命令的执行风险需另审 | **复用“一个Mint应该调查哪些对象、如何写报告”的业务设计**，不要未经审查启动旧流程 |
| [旧 meme-](https://github.com/sunshihao001/meme-) | [成本区/深洗/死亡盘/二次启动](https://github.com/sunshihao001/meme-/blob/main/02_庄家周期/深洗与死亡盘语义深化_v0.1.md)、[失败样本/样本外反证](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/反证实验设计_v0.1.md) | 主体是市场结构、MQL5与策略研究，**不是Solana链上经济归因真值** | 作为 **市场阶段的竞争解释与反证模型**，须结合真实链上库存、池深度及资金行为，不能只从K线断言庄家成本 |
| [历史 Why-Solana](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | 多跳资金、同源、发行/退出、群体与资本循环的研究/源码 | 有 [Grok旧专项审查](https://github.com/sunshihao001/grok/blob/eeb40b050369e4525919500f144325c9a9fc8b74/knowledge/system/legacy-meme-multihop-deep-audit-2026-11-02.md)，但仍属外部参考review_only | 先保留旧总结和反例，**下一轮才进入外部项目逐项解剖** |

**关键时间对齐**：这三个 Grok PR 的运行、知识索引和原型，都不能自动升级为 `blix` 分支的产品能力；尤其旧Python Mint实测是 **2026-11-01 GitHub Actions** 的供应商预览，不是2026-11-06 Blix/Web/Grok Bot实跑。

## 4. 怎样让 Blix “理解”原有研究：按业务落点接入，不把Markdown当程序

下面是**知识在现有产品里应该解决什么具体问题**，不是要求立即写新代码。各项旧知识留在上表原始仓库，由本项目的一份索引连接。

| Blix 原有用户业务/组件 | 应主动选用的旧知识 | 引入后更专业的正确问题 | 现有代码层可能需要的未来连接 |
|---|---|---|---|
| **Pulse / Discover** | D02发行生命周期、D03市场微观结构、D07时序、Hermes 05–09 | 新币为何值得升级调查？Curve/迁移/池与真实卖出容量、排名来源、漏检/噪声是什么？ | `engine.js`、`quality.js`、`coverage.js` 现有候选规则与数据来源，先查后改 |
| **Coin / Creator / Dev** | D02/D04/D05/D06、qb- 单Mint对象矩阵、Hermes角色 | 谁是已知Creator、Fee Payer、Token Owner、池/公共设施、接收/分发者？哪些只是候选关联？ | `coin.js`、`holders.js`、`holderslive.js`、`dev-identity.js`，报告来源与角色置信边界 |
| **Holder / Bubble Map** | D01/D04/D05/D06/D11、Hermes同源/筹码设计、qb-基础设施名册 | 资金连接是**直接SOL转入、代付费、共享公共服务、同Slot，还是行为关系**？余额覆盖与历史是否一致？ | `bubblemap.js`、`wallets.js`；要保留原始交易证据、覆盖、边类型及UNKNOWN |
| **Wallet Tracker / Smart Money** | D04/D05/D07/D08、Hermes 10–14、PR#16 M01 离线群体演化 | 买入、转仓、接收、卖出谁先谁后？一个签名多腿是否漏记？样本间钱包成员变化是什么？ | `wallets.js`、`wtrack.js`、`solana.js`、现有API；先确定解析和持久时间窗 |
| **跨Mint和群体异常** | D05/D06/D07/D10/D11、PR#16批量监控、Grok旧P2.1–P2.5、qb复查 | 一群钱包在多个Mint反复出现，是同一资本、公共机器人、发币系列还是偶然同市场？库存、成员和时间有何变化？ | 复用原钱包/事件记录；**尚无经真实主网验收的完整跨Mint动态调查产品** |
| **AI Research / Picks / Narratives** | D03/D08/D09/D11/D12、meme-死亡盘和反证实验、Hermes Evidence Chain、ai-d专家问题表征 | 哪些观察是事实，哪些是多种机制假说？怎样用真正的新数据推翻？是否有样本外/执行价值？ | 原`research.js`、`brain.js`的市场研究保留；**不硬套买卖阈值或AI虚构置信度** |
| **Journal / Health / Alerts** | D01/D07/D10/D11、旧Grok证据合同与断流反例 | 连续6/12小时的事件有没有缺口、重复、错误时间分桶、不同池遗漏？不在线时告警怎么办？ | `journal.js`、`wtrack.js`、`health.js`、Web/监控服务，判断历史保存策略 |
| **用户的自然语言→系统动作** | D12、PR#17目标演化、ai-d人机协作研究 | 用户一句话到底在问市场、资金、机制还是部署？调用哪些已有功能后还需什么证据？何时停止研究？ | Grok Bot未来的**只读指令入口**，不等于把旧多Bot配置与22专家全部部署 |

### 为什么单纯将知识文件复制到仓库不够？

“主体明白”至少分为：
- **可发现**：AI从Blix现有业务入口能定位到对应的旧原始研究和原代码，而不只会搜索关键词。
- **可适用**：针对某个具体Mint或异常，能解释旧机制与当前数据的**适用条件、替代解释和失效条件**。
- **可交付**：有需要时把理解转化为现有页面的**明确来源、字段、调查流程与结论**，而不是再增加一套平行报告。
- **可纠正**：当Blix事实、历史研究和供应商标签冲突，知道应该修改哪条认知，而不是不加辨别地相信哪个来源。
- **可验证**：真实业务/离线反例/用户可观察输出可证明新增知识带来增量；**目前仍未测试此迁移效果**。

这不要求建设新的12域或把旧全部Markdown载入上下文；先使用已有[专业知识入口](knowledge-use.md)与本页**按问题定位原文**即可，未来只在确需改代码时做小范围适配。

## 5. 两个实例：知识究竟会改变 Blix 的什么判断？

### 场景 A：10个新钱包同时买入，并出现同源出资

1. **Blix原生**：Pulse观察到上涨，Coin/Holder看到部分早期钱包，Bubble Map可能形成同funder/同Slot候选边。
2. **Hermes/D04/D05深化**：早买、钱包新鲜、共享发币服务、代付费、转仓与经济受益人要分开。**首笔Fee Payer不是直接资本来源的证明**。
3. **qb-深化**：从Top Holder扩展成“地址主档、基础设施、资金/Token边、低权重和复查对象”矩阵，不只给出十个地址。
4. **PR#16/P2时序深化**：比较这些钱包在1/5/15分钟窗口中的成员增减、转账接力和不同币上的重复，但其原型当前为fixture-only。
5. **AI合理结果**：写“有同步早买与资金候选结构，是否同控未知”，附反证如公共服务、共享Gas代理、正常市场热度；指出需要补哪些具体交易/历史。
6. **不该做**：直接声称“10个庄家小号、控盘X%、可以跟单”，或照搬Hermes未校准置信度公式。

### 场景 B：某Mint拉升前12小时钱包转账增多

1. Blix原有事件日志与钱包跟踪可发现**被观察账户**的部分行为，但Journal原始成交默认仅24h，钱包活动默认约7天，数据未必涵盖全部资金转账。
2. Hermes 的资金流与角色演化、Grok D05/D07/D10 强化“同钱包集合、相同窗口、真正资产净变化和历史覆盖”；qb-对象矩阵帮助找隐藏接收与出货钱包。
3. meme-的“吸筹/深洗/死亡盘”只能作为**经济机制候选**；必须对照资金净流入、Pool流动性、后续卖压、社交热度以及普通盘基线，不能由K线形状确定资本组织。
4. AI结论应该允许“可能为资金准备、普通做市、历史回补或公共服务行为；证据尚未足够”，同时提出信息价值最高的补查。
5. 若发现跨Mint群体重复，调用PR#16/Million等历史知识**研究适用性**，而不是直接认为外部Python原型已在Blix持续运行。

## 6. 需要恢复、需要改写、不能直接继承的知识

| 分类 | 示例 | 理由 |
|---|---|---|
| **直接恢复为研究能力** | Token Account/Owner/Authority、生命周期/池、角色是候选、同源不等同控、库存和出货、缺失/缓存/费用边界、正反样本与竞争解释 | 影响真实业务质量，跨模型、跨代码库仍适用 |
| **改写为可证伪假设** | Hermes同源风险“高概率”、qb-标签式钱包分类、meme-第一控盘成本区/深洗/死亡盘、结构预测未来机会 | 原材料存在强阈值、启发式或跨市场语义不一致，不能直接做生产判定 |
| **保留但不恢复为默认执行** | Hermes固定7 Skill、旧GMGN付费调用、旧Grok固定P1–P6研究顺序、22专家逐轮参与、PR#17多Bot架构、历史自动交易Gate | 易重复建设、增加调用污染或扩大授权；当前仅要求理解Blix和只读专业研究 |
| **旧的可复用工程候选** | PR#16 `mint_v01`、`public_rugcheck_report`、`wallet_batch_monitor`、旧qb报告生成 | 源码存在，局部有供应商实跑或离线单测；需要对比Blix原生API/数据再决定是否适配，不自动合并 |

## 7. 下一次深入解剖参考项目时的决策基准

**先不要全量遍历外部项目。** 当前Blix和旧Grok知识已给出具体业务缺口；之后按信息价值选择外部成熟成品，先问：
1. 它能否替代Blix现有的一个**完整业务环节**，而不只是多一个漂亮的图/指标？
2. 它是否补齐我们真正缺的**原始历史、经济事件、跨Mint连续性、费用/恢复、经济主体竞争解释**？
3. 它与Blix的接口、许可、配额、安全隔离、前端体验和数据口径能否组合？
4. 直接整用、限制性改造、薄接口组合和只借专业机制中，哪条对目标价值最好？

后续候选仍保留 Pulse、Million、HoldTech、PumpTrace、OKX、GMGN、pumpwatch、PumpGrok、Cielo、Nansen、Arkham、Bubblemaps，以及Why-Solana、旧Hermes/qb-/meme-的原始清单。**它们是待审，不意味着本轮已逐一完成最新版全代码解析。**

## 8. 本轮已确认事实与边界

- `blix` 的原产品源码/网页/接口充足，历史Grok知识也非空白；**差距主要在专业事实语义、证据与完整跨Mint业务，而不在“是否先造一个UI/目录”**。
- PR #14/#16/#17 均为 `open draft`、未合并到 `blix`。旧Python线在2026-11-01有**一次真实公开供应商Mint基础报告证据**（五个池、20 Token Account候选、1 AMM基础设施匹配）；不等于Blix已运行、钱包资金回路已验证。
- 当前只读安全及云电脑生产环境仍未通过；之前提交的`server/intelligence/mint-facts.mjs` 只有Token/Holder两个本地GET，**不应宣称是完整单Mint专业调查系统**。
- 本轮完成的是**源码与历史知识恢复、业务映射和产品路线判断**，没有编写/修复运行模块、没有运行单测、没有连接Grok Bot；文档链接让未来AI更容易按实际问题调用原来源，不能证明它已经自动学会全部知识。

**本轮最重要的路线改变**：下一步先围绕Blix已有Coin/Wallet/BubbleMap，将旧Grok的“钱包角色—资金—库存—行为时序—证据/反证”主线与现有数据事实对应，再决定是否补API/存储/算法。**参考项目深入解剖排在这个基线之后，不因某个外部仓库功能多就马上接入。**
