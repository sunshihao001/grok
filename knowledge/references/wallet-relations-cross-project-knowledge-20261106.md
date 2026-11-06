# 跨项目深层知识研究｜钱包关系、经济主体、库存口径与历史完整性（2026-11-06）

> **范围与状态**：本篇以 Blix 为单一产品，直接对照 Blix、Kelows/million 与 AntC215/PumpTrace 的原始源码、设计注释及相关代码路径，研究**为何同一种表面功能产生不同认知**。知识研究状态 `SOURCE_CODE_STUDIED / STATIC_COMPARISON`，**不是对三个项目全部源码的完整审查**；没有启动程序、联网验证链上事实、安装依赖、运行交易或更改 Blix 业务代码。静态推论可能由其他调用链及真实数据修正。

## 0. 研究对象不是“有没有关系图”，而是这些关系图究竟断言什么

项目表面都支持“钱包/群体/风险分析”，但至少存在五种**不能合并成一个 `owner` 真值的对象**：

1. **链上观测边**：某签名/指令内发生的真实 SOL 或 Token 转移，必须保存来源、签名、时间和动作类型；接触过不代表同一资金或同一人。
2. **账户或程序事实**：Token Account / owner/authority / fee payer / mint /池Vault/服务地址是不同字段；相同地址角色可因程序与时间变化。
3. **关系候选**：共同出资、相同Fee Payer、同Slot参与、同步买卖、共同持仓，均可形成不同类型、不同效力的关联。
4. **经济主体假说**：共同资本预算、执行代理、共享服务、独立投资人、真实同控制者均是竞争解释；钱包连通不充分证明现实身份。
5. **业务结论**：可观察风险、库存影响、未来异常与可复制交易优势又是新一层判断；不能从关系图直接跳到真实盈利。

这种**从证据对象定义到经济机制**的区分，才是从参考项目吸取的专业认识，不只是迁入关系图算法。

## 1. 同一个“钱包群组”，三套产品内部语义不同

| 项目、源码事实 | 设计中真正解决的问题 | 深层限制和反例 | Blix应吸收的专业知识 |
|---|---|---|---|
| **Blix** [`server/bubblemap.js`](https://github.com/sunshihao001/grok/blob/blix/server/bubblemap.js) | 将持仓、RugCheck transfer network、首次出资候选及同区块/发行标签连为**可视化候选关系图**；最多四跳寻找连接，Kruskal最短边构造可视图，识别部分交易所Hub和分发者 | `readFunder` 在无明确SOL转入时以最早交易 fee payer 回退，可能把**代付费者当出资人**；最多向前取3页×1000签名，历史过长/无结果统一缓存为`""`；同slot `2–6` 买家只是一种弱行为关系；多跳连通的传递性可能膨胀候选群组 | 保留现成关系图和原作者解决“111地址收到同一空投钱包导致67%假聚类”的工程经验，但“关系连通群”与“同一经济主体”必须分开理解；区分资金边/手续费/标签/时序和历史缺口 |
| **Million** [`owners.service.ts`](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/analysis/owners.service.ts) | 从已有钱包分析中创建 funding/fee-payer/co-entry 边，用低成本Union-Find形成可查询的 `ownerId` 候选 | 其代码明确**禁止co-entry参与Union-Find**，因曾出现182钱包被误合并事件；另外仍用 `FUNDING_MIN_SOL=1`、`FEEPAYER_MIN_SHARE=0.15`、`HUB_DEGREE_MAX=6` 启发式；funding与fee payer仍可跨节点合并，`ownerId` 每次重建不稳定；无链下身份真值 | **可吸收“弱关联边不允许成为主体合并桥梁”**的认知与历史反例，而不是搬Union-Find；即使采用funding+fee-payer，也应按真实转账、代付和基础设施严格区分 |
| **PumpTrace** [`trust-engine/analyze.mjs`](https://github.com/AntC215/Pumptrace/blob/main/src/modules/trust-engine/analyze.mjs) | 先将 Creator/其直接转出候选、曲线、PumpSwap/程序控制和未知钱包分类，再计算持仓结构与关系证据强度 | 直接Creator转币只证明转移，不证明受赠者同控；程序与已登记服务识别有漏标/过时可能；`CONFIRMED_ON_CHAIN_LINK`表示**链上关系存在**而非实控身份确认；风险加权分数为代码规则，未见本次源读能证明其概率校准 | 借鉴**先确认链上账户类型/剔除基础设施，再解读持仓和主体**；把“直接事实/较强行为/可能协调/只有时序”分级，但不复制原风险阈值或把“high confidence”读成控制权概率 |

**综合认识**：三套代码实际上处理三种不同任务——Blix主要是**展示关联可见性**，Million尝试**压缩成群组身份**，PumpTrace提供**来源与账户类型支持的风险解释**。三者不能拿“是否支持wallet clustering”一项功能标签比较完。来自经济主体识别/图论的逻辑区别是：`关系可达`、`同一行为机制`、`共同控制`不是等价关系；多条弱边通过传递闭包不自动成为一个强结论。

## 2. “资金来源”背后有至少四个完全不同的问题

### 2.1 原始资金动作与费用代付
- **Blix**：在当前可达的最早交易中先找 System Program 明确转入的钱包，找不到便取交易 `accountKeys[0]` Fee Payer。**两者含义不同**；后者可能是代付/公共执行者，并不确定提供钱包的交易本金。
- **Million `funding.service.ts`**：读取Helius `nativeTransfers`，区分 `in` 与 `out`，按对手方汇总金额、次数、首末时间，最多3页交易，返回 `truncated`、`analyzedTxCount`、`fetchedAt`，最多50个对手并自动预览至多12个。作者注释称 `out` 是同一行动者新地址候选，且**未做数据新鲜度核验**；因此转账事实与“同一行动者”仍是两层。
- **Million Owners**：`metrics.topFeePayer.share >= 0.15` 创建 `feepayer` 关系边，这是执行关系证据，不是直接资金转入；而与 `funding` 边一并被 `cluster()` 用于并集，可能使弱异质关系合流。
- **PumpTrace**：将 `creatorTransfers` 的直接代币转移作为 `CREATOR_LINKED` 类别证据，而不是从同区块/共同代付直接判断主体。其风险仍可能因链上直接关系≠实控者而高估。

### 2.2 经济问题的层次
即使确实看到地址A付给B 10 SOL，也只能说明观察时间窗内资金从A到B，**不能自动确定** A/B 的共同受益人、资金本来源、最终用途、是否由服务平台替客户执行、是否形成同一经济头寸，更不能视为相同Lamports一路追到卖出钱包。Solana交易的多个指令/CPI和SOL/WSOL边界必须在实际事件重建时单独处理。

### 2.3 有价值的复用决策
保留Blix `bubblemap.js`，**知识层面应把边的来源与语义独立辨识**：`DIRECT_SOL_TRANSFER`、`TOKEN_TRANSFER`、`FEE_PAYER_ONLY`、`CO_ENTRY`、`VENDOR_NETWORK`、`INFERRED_FUNDING`，并记录时间、历史完整度/可得时点。**这是建议的语义清单，不声称这些字段已经存在或要求立刻改代码。**

## 3. 同一种“集中度”包含两个分母、不同的供应定义

[PumpTrace classifyHolder/buildTrustAnalysis](https://github.com/AntC215/Pumptrace/blob/main/src/modules/trust-engine/analyze.mjs) 的顺序：

1. 根据账户标签、Creator、曲线地址、Incinerator、PumpSwap、程序控制等识别账户类型；
2. `excludedFromTradable` 过滤部分基础设施账户；
3. 分别计算 `rawTop10SupplyPct`、`tradableTop10SupplyPct`、`infrastructureSupplyPct`、`connectedTradableSupplyPct`。

**易错语义**：代码中的 `tradableTop10SupplyPct` 是“剔除被标记基础设施后的前十地址，其`supplyPct`原值之和”，**不是自动重新以全部非基础设施余额为100%归一的前十集中度**。其报告一处明确称“% of total supply”，但其他命名/文字可能让消费者误读为“占可交易供应”。此外被识别为基础设施，不代表该资产永不可交易；只是此模型特定分析边界。 

Blix `holders.js`/`holderslive.js`/`coin.js` 和 Bubble Map 对池、Owner和Holder已经有不同口径，未来对比时必须明确：**总发行量、已发行量、经济可流通量、可实际卖出库存、Top Token Account、Top Owner 和关联主体持仓**不是可以互换的分母。仅对照“支持Top10占比”会损失这一整条专业链。

## 4. 时间和历史：三套项目的“监控能力”不能只比较有无WebSocket

| 项目源码事实 | 它真实要解决的时间问题 | 新的知识边界 |
|---|---|---|
| Blix `server/coverage.js` | 5分钟滚动实时交易窗口，解决原作者报告的“较晚活跃但不在New/Final/Migrated栏”的覆盖遗漏；代码上`moving`仍是规则判断 | 用于**当前市场发现**，不是历史全样本统计、12小时转账完整度或长期因果研究 |
| Blix `server/wtrack.js` | Wallet Tracker活动记录与确认扫查；实时`processed`可能消失，6秒至2分钟后`confirmed`清除错误/未知事件；`FEED_KEEP_DAYS=7` | 已有某种纠错/恢复经验，但确认丢弃、保留期限和真实到达时间应另分析，不能把未保留当未发生 |
| Million `live/live-feed.service.ts` | 15分钟 `LiveEvent` 展示窗口、最多5000事件；支持WS/Webhook、死连接检测和频繁交易者降噪 | **短期feed不等于历史审计账本**；追6/12小时资金/群体需要不同持久数据范围，不因WS活着就完成 |
| PumpTrace `backfill-manager.mjs` | 90天默认回填窗口、显式上限和游标；`PAUSED`、`RATE_LIMITED`、`CAP_REACHED`、`COMPLETE`、`ERROR` 等状态；重启时重排可恢复任务 | **“采集过程”本身应成为可解释证据**：截断、配额、暂停和已覆盖区间与真正“没有事件”分开。能回填也未必原事件经济语义正确 |

由此得到的综合认识：**完整监控是事件时间、首次可获时间、抓取时间、落库时间、缺口水位、重试状态、历史回补与模型解释的共同产物**。只读系统若没有这些口径，无法把“拉升前12小时没有大额转账”当可靠反面事实。

## 5. 参考产品设计差异反向揭示的五个值得继续研究的未知问题

1. **关系图中的链式连接是否放大身份假象**：如果A与B仅共享出资渠道，B与C仅同步入场，连通性并不产生A=C的共同控制。需要原始边分级、排除高连接公共设施、对照正常市场热点和不同关系类型的误聚类实验。Million的182地址事件是可检查的作者源码注释，不是本项目独立重演。
2. **资金“第一来源”是否因不完整历史而错误固定**：Blix最多3页历史，`bubble_funders.funder=""`可能把“截断/无法判定/真无转入”混成同一状态并持久缓存。查无历史不应自动生成不可变的第一资金起源；需要后续源证据、重试与失效规则。当前仅静态发现，没有复算链上实证。
3. **基础设施分类改变了怎样的经济分母**：PumpTrace排除程序/Curve账号，Blix的TopHolder/Bubble Map另有来源与池标签。相同数字名称可能代表“总发行量的份额”而不是“可交易钱包份额”，经济含义有差别。
4. **谁是钱包群体的经济受益人、执行者、服务运营者**：共同fee payer、同交易签名、直接Creator分发、共同资金预算可能对应不同角色和合约。Solana链数据通常不足以唯一断言现实控制者；后续需竞争解释。
5. **稀疏观测与事后回填会怎样影响异常前兆**：G2“发现→Mint→跨Mint→机制”全过程的时间可观测性，无法靠单一15分钟界面或保存7天的Tracker完成保证；必须分清样本选择、抓取水位与模型输入截止时间。

这些认识同时作用于 D01（交易/账户）、D03（流动性）、D04–D07（钱包/群体/库存/时序）、D10（数据完整性）、D11（反证）和 D12（AI知识选择），**不能因为一个功能目录相似就宣告知识“已覆盖”**。

## 6. 对 Blix 的知识吸收结果：保留已有能力，但升级对其语义的理解

| 本轮知识增量 | 当前证据 | 归属/产品落点 | 是否建议立刻融合代码 |
|---|---|---|---|
| 图可达、行为关联与经济同控是不同命题 | Blix `bubblemap.js`；Million `owners.service.ts`误聚类注释；PumpTrace证据分类 | `mechanisms` + `methods`；Blix Bubble Map/Wallet观察与AI解释 | **否**。先保留语义差异及反例；要引入新Owner逻辑应有真实误报对照 |
| Fee Payer不是入金证据；实际SOL转账也不是唯一受益人证据 | Blix `readFunder`；Million `funding.service.ts`；PumpTrace Creator转币 | `foundations` + D05；钱包/资金来源陈述与未来事件规范 | 否；应先核原始CPI/余额变化和多跳案例 |
| 原始Top10与剔基础设施Top10的口径须明示 | PumpTrace `buildTrustAnalysis`；Blix Holder/Pool实现 | D06持仓/库存、D03池与市场退出能力 | 否；如未来界面更改，先厘清分母 |
| Feed、回填、历史水位属于不同层次的持续性 | Blix `coverage/wtrack`；Million `live-feed`；PumpTrace `backfill` | D07/D10/L6；持续监控、历史与前兆研究 | 否；需真实部署前验时间/存储成本 |
| 未校准风险权重和固定阈值不能作为事实证明 | Million `0.15 / 1 SOL / degree 6`、PumpTrace `riskScore`、Blix同slot2–6启发式 | D11反证、D12知识有效性 | 否；应作为研究候选/反例而非结论 |

**知识吸收方式**：此文为成熟项目跨源专业认知的新正文，融入 Blix 既有 `references/` 以免改写旧研究原稿。相关 D04–D07 / D10–D11 的专业知识升级入口可从 [Blix总知识目录](../README.md) 与 [原生/旧知识对应](../INTEGRATION-CROSSWALK.md) 调用。**不是开设新的独立知识架构，也不是把参考代码整体融合。**

## 7. 未研究到的项目知识与接下来深入研究的真正范围

这次**只完成四套源码（Blix、Million、PumpTrace含Backfill）中若干关系/资金/库存/监控核心实现的交叉深审**，不能说Million/PumpTrace整仓或所有参考项目已理解透彻。

后续面向完整参考项目，先清点它的业务/页面/功能/数据/算法/测试/架构/历史/失败/经济假说范围；将“已经研究且能解释”“只是看到源码”“仅来源索引”“已反证/过时”清楚区分。重要的每条知识均追到完整上下游及替代路线，允许跨项目持续深化；不存在“一个项目每轮只能取几个点”的硬限制。

**当前优先相邻专题**：Million 的原始钱包指标/PnL、发现逻辑、Owner边关系及部署副作用；PumpTrace 的历史交易/Creator身份、角色证据、风险分数公式、Backfill持久化；对照Blix的单Mint事实、Wallet与连续事件口径。之后将Pulse、HoldTech、OKX、pumpwatch和历史Hermes/qb-/meme-同等纳入，防止把单一钱包聚类误当全项目研究。

> 资料与源码来自各自原仓库，均为只读静态分析；新的机制/问题链是本项目的分析推论，未成为可运行功能或实证Alpha。
