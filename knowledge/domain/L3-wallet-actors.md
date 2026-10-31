# L3｜钱包角色、资金网络、筹码与跨币行为：跟单研究的主体知识

> 对应 D04、D05、D06、D07（现有领域，不新增分类）。全部是结构化**调查知识**，不是交易标签真值或已验证的策略收益。D04/05/06 有旧卡基础；D07 目前无专属主卡，本篇先补专业内容而不伪称研究完成。

## 先用五位专家打开市场问题

[《L3 专家研究台》](L3-actor-expert-perspectives.md)是钱包行为、资金同源、筹码控制、开发者系列币、群体时序五个领域的**专家入口**：先展示专家会问什么、看出了什么、何处出现分歧，再按需进入下方的原理研究。现有 D04–D07 分类、事实/推断边界保持不变。

## 从领域概述进入深度专业研究

本篇是 D04–D07 研究导航。深入研究**账户权限 vs 经济受益、资金图关系非独立性、同步交易的共同外因、流动性与持有库存、钱包优势的不同来源**时，按需阅读 [《Solana Meme 经济主体与钱包行为机制｜深度研究 I》](L3-actor-economic-mechanisms-deepstudy.md)。其中的七条新机制是假说，不能以本篇观点自动创建监控规则。

## D04｜钱包角色：分析一个钱包“怎样参与市场”，而不是“它叫什么”

### D04-01｜建立钱包交易行为画像

同一个地址可以在不同代币中是早期买家、路由接收者、短线轮动者、分发/退出地址或长期持有人。标签必须附带 Mint、阶段与时间范围，不永久固定。

- **行为特征**：`first_seen`、`first_buy_delay_from_tradeable_market`、每笔原始输入/输出、买卖次数、净买入/净卖出、持仓时长、仓位变化轨迹、跨币并发头寸、发币/关联交易经历。
- **需要分开**：实际首次买入、数据源首次发现和钱包首次可见；盈利标注、活跃钱包、KOL、sniper、dev-linked 均是不同维度。
- **反例**：某钱包极早买入且卖在高点，也可能是自动化执行、机会筛选后幸存者、市场整体事件或历史样本选择结果。不能自动称内幕或可跟单。

### D04-02｜一组钱包质量指标，必须拆开看

1. **PnL 完整性**：是否覆盖卖出、持有、账户间转出、空投/赠与、未实现头寸、交易手续费？供应商胜率未必含所有交易成本。
2. **进入方式**：是曲线初期、迁移后、价格拉升中途，还是高位换手？决定跟随者的可见差距。
3. **离场方式**：一次清仓、分批卖出、跨地址转仓、LP/路由活动？不应把钱包转出直接记为“获利卖出”。
4. **行为稳定性**：近 7/30 天是否因市场状态切换而改变交易节奏？“表现最好的一小撮钱包”容易含幸存者和主动筛选偏差。
5. **可复制性**：若钱包先于本监控观察到的价格运动，其历史盈利不代表后来者有相同机会。

### D04-03｜开发者、创建者和系列币

区分 Mint authority、发行平台使用者、真正创建交易的签名者、后续管理员/相关收款地址、共同服务商。尝试沿已发生的部署与交易建立跨 Mint 序列：发行间隔、早期资金分配、关联买家、LP 变化、退出路径和历史完整覆盖。

- **候选知识**：系列发行、换地址重发、跨币买方重用、卖出后再次部署资金、重复创建者共用工具。
- **必须排除**：第三方代发、平台共用程序/工厂账户、被标为“creator”的公共地址、只选择已 rug 样本的偏差。
- **不能推断**：某个 dev 标签或历史 rug 比例足以预测下一枚 Mint 的涨跌。

## D05｜资金网络：把“同源线索”逐层升级为可解释关系

### D05-01｜图中节点与边的真实含义

- **节点**：链上 owner、token account、pool/vault、已识别的公共托管/交易所 HUB、未知地址、候选经济群组；不同节点类型不能混用。
- **边**：`source`、`destination`、`signature`、`instruction_index`、`asset_mint`、`amount_raw`、`slot`、`event_at`、`available_at`、`edge_type`；同笔多次内部调用须有去重合同。
- **关系层**：真实转账边 → 共同出资候选 → 时间/行为相似 → 可能的合作或代理服务 → 实际经济控制（最后一层需要更多独立证据，绝非前面自动证明）。

### D05-02｜同源钱包最容易被污染的三种情况

**共享服务枢纽**：许多无关用户通过交易所热钱包或支付服务转出资金，不能把下游钱包视为同控。

**账户中转**：看似 A→B→C 的 SOL 资金回流，可能是归集或服务结算，不是操作者循环狙击。

**小额 dust 关联**：大量地址收到极少量 SOL，可能是空投、试探、账户初始化、诱导性转账；不能用一次小额关系识别真实资金主体。

正确做法：先识别公共 HUB/已知池账户；将小额/时间窗口/可达关系单独保留；比较**同币交易行为**、转账顺序与多轮重用，再计算关联强度。证据不足时报告 `common_funder_observed`，而非 `single_owner_verified`。

### D05-03｜资金从哪里来，与下一次机会是否可见是两个问题

跨 Mint 追踪一组非公共资金地址的 SOL 回流与重新分发，可以解释资金循环。它可能帮助预测**一组地址活动将再次出现**，但在下一 Mint 尚未被实时识别前，不能据此推断“应该买哪一个币”。

- **记录**：`exit_token`、`exit_available_at`、`funds_return_to`、`source_excluded_as_hub`、`new_funding_available_at`、`next_mint_first_observable_at`。
- **反证**：普通交易所再充值周期、机器人服务批量账户补款、市场普遍活跃度、多个互不相关团队共用基础设施。
- **研究输出**：潜在再次活动的监测队列，尚不是购买信号。

## D06｜筹码结构：地址集中、经济集中和可卖供应要三分

### D06-01｜Top10、HHI 和真实市场供应

Top10 是**地址层面的持有快照**；经济主体可能由多个地址构成，也可能存在托管/池子地址。因此至少报告三套概念：`address_holder_concentration`、`candidate_entity_concentration`、`known_pool_or_custody_share`，并说明流通供应量和排除口径。

- **注意**：固定流通供应口径前，Top10 上升可能来自重新计量、池子迁移或分母变化。
- **可计算**：地址层 HHI `sum(share_i ** 2)`；经济主体 HHI 在身份/控制没有独立证据前保持区间或未知，不能把所有共享地址机械归并。
- **下一项鉴别**：D01 真实 owner、D05 资金边、D03 池子 vault/储备，排除重复与混入。

### D06-02｜“吸筹”和“派发”应转写为观察事件

- **可观察**：某地址集合净 token 增减、增减发生时间、转移/成交路径、买方新旧程度、卖方与买方的关联不确定性。
- **候选解释**：独立买方承接、同一主体分配、普通做市、资产托管变更、一次性风险退出。
- **缺失项**：无法独立确定买卖两侧的经济身份时，不能把买卖转手直接命名为“庄家完成吸筹/派发”。
- **验证切口**：流动性压力下降是否伴随真实独立资金进入？价格恢复是在新的可见资金推动后还是同一群组换地址后？

### D06-03｜池子份额与可卖压力

“Holder 比例降低”不能自动说明市场风险下降：某个 LP 或巨大持仓的钱包也许已改变退出能力，而 Top10 未反映；也可能大钱包卖给大量独立小户，使单地址集中下降，但真实需求不足。

- **观察**：可交易浮筹、已识别池/托管占比、净流向池子的 token、对 SELL quote 的冲击、持有时长分布。
- **拒绝快捷结论**：`Top10 < 某阈值` 并不足以得到“筹码健康”或“不会 Rug”。

## D07｜市场时序与跨币环境：不能只有单币单点快照

### D07-01｜同步交易：共同控制与共同事件有相同表象

多钱包在同一短窗口买入，可能来自一个机器人集群、执行服务、社群喊单、同时收到相同数据推送、套利触发或真正独立趋势资金。需比较同规模时窗、同一市场波动、同交易池及同一平台事件下的正常同步度。

- **需要**：`slot`、`event_time_precision`、`first_seen_by_provider`、钱包集、金额、交易程序、网络拥堵/池事件。
- **区分性信息**：是否共享非公共的前置资金边？是否在**不同 Mint 和不同时间段**重复形成相同序列？
- **禁止**：任何固定秒数阈值直接推出同控或内幕。

### D07-02｜一组钱包的时序角色会变化

初期跟随、随后分发、再次跨币进入、失去历史优势等是时间过程。应保留跨事件轨迹，而不是一次标签永久存档。

- **重要窗口**：首次出现 → 首次买入 → 多次加仓 → 首次减仓 → 净退出 → 资金回流 → 下次候选 → 观察者可见时点。
- **认知价值**：同一钱包在不同阶段的行为可能改变；某一阶段的积极买入并不能覆盖后来卖出的风险。

### D07-03｜叙事、关注和市场状态不等于真实独立需求

KOL 提及、社群消息、热门榜排名、推文传播、交易量、持币钱包数可作为注意力代理，但应和净资金流、真实交易者新增、持续持仓、有效买单深度对照。

- **时序**：先有价格快速上涨才出现热门榜，和先出现可信的公开事件再出现资金需求，完全不同。
- **对照**：同时间段整个 Solana Meme 市场是否都在上涨；某类新闻是否同步影响多个 Mint。
- **缺口**：当前 `grok` 没有专属 D07 主知识卡；这份调查方法不能宣称已有实时社交数据接入。

### D07-04｜从单币结构转向市场关系

跨币观察需要区分**共同参与者**、**同类叙事**、**资金切换**、**市场总体 beta**。例如 A 币退出后 B 币上涨，不证明 A 的资金进入 B；只有观察到相应转账与买入边、排除公共账户并满足时点要求，才能形成强关联候选。

## 跟单场景：同源 + 同步 + 集中究竟意味着什么？

假设系统发现：6 个地址在一个新币可交易的最初数秒内买入；它们的 SOL 可回溯到同一上游地址；Top10 持仓很高。

**第一次判断不应该是“庄家建仓、可以跟单”。**

应按以下顺序：

1. D04：这 6 个地址各自买了什么、净持仓怎样变化、是否与部署活动有关？
2. D05：共同出资者是否是已知公共服务商/交易所 HUB？转账是否真实在买入前出现？
3. D06：Top10 是否含 pool/vault/托管地址？真实独立持有人和可卖储备是什么？
4. D07：是否仅仅响应同一个上线或市场事件？相同行为在其他不相关币上多常见？
5. D08/D09：即便证明存在一个行动群组，其最早可见价格和可成交退出能否为**跟随者**留下净优势？

**正确知识输出**：事实清单、可解释关系强度的边界、至少两个竞争机制、能区分它们的下一项数据。尚未跨到可盈利结论。


## 2026-10-31｜来自真实工具与源码的钱包角色判读增量（D04/D05/D06/D07）

**证据界限**：本节是公开产品文档和部分仓库源码的对照，尚未通过本地RPC逐笔复核真实钱包标签；商业服务的标签算法若未开源，记录“供应商声称”而非已证真值。无需新增领域、本体或新Bot。

### A. 标签不是一种单一分类：四个正交问题

1. **身份/来源**：KOL、creator/dev、CEX/service、fund、已公开签名身份；问“地址属于谁/与谁有关”，链外身份须有额外证据。
2. **执行/策略**：sniper、bundler、MEV、DEX bot、flipper、arbitrage；问“怎样进入与执行”，不自动推出胜率、内幕或一个操作者。
3. **资产/经济角色**：early buyer、top holder、transfer-in、distributor、collector、LP、库存转移与持币状态；问“钱和Token到哪里”，余额变化不等于成交利润。
4. **历史表现/关系候选**：smart trader、fresh、dev-linked、same funder、suspected insider、wash candidate、multi-Mint cohort；问“有什么统计历史或关系”，标签必须有观察窗口、样本覆盖和正常解释。

同一地址可在同一个Mint/阶段带多标签，又可随Mint、时间和状态改变。应保存原始供应商标签、版本、其定义、原始事实、推断、证据链接、实际可得时点、有效范围及撤销历史。

### B. 实际来源的可操作差异与路径

| 来源 | 实际接口/规则与可用知识 | 不能直接继承 |
|---|---|---|
| GMGN 官方 Featured Icon + gmgn-skills token/traders/holders/track | smart_degen、renowned/KOL、sniper、bundler、dev、transfer_in、rat_trader等过滤；KOL与smartmoney是不同流，Sniper按早期block判读 | 不能把GMGN“bundler”与Jito真实Bundle直接等同，也不能把Smart Money标签当未来盈利 |
| Birdeye Holder Profile/Positions（2026-04-21） | bundler/sniper/insider/dev四类分别给钱包数、供应持仓比例、买卖量、PnL；Positions细化单地址；First Buyers（2026-07-08）提供buy_more/hold/sell_partial/sell_all | Bundler对2026-03-01前Mint仍在回补；前1000早买样本不是全部买家；标签口径未公开证明 |
| Cielo Finding Good Wallets | Flipper/MEV/Sniper/Human Operated/Gem Finder/High Winrate；其Sniper定义重视平均持仓不足2分钟，和GMGN早期区块定义不同 | 同名标签跨平台不可直接合并；短持仓不一定是发行初期首买 |
| Nansen Smart Money API | Smart Trader/Fund及30D/90D/180D窗口，行为与身份分离 | 历史盈利不等于跟随者可复制优势 |
| Bubblemaps V2 | 前250大Holder间的转账关系、历史分布和Supernodes过滤 | 图连接代表发生转账，不能证明私人同控；前250地址存在选择边界 |
| Watchtower Wallet Intelligence公开规则 | sniper=至少三次在创建slot或下一slot买入；bundler=至少两次发行同笔多钱包买入；flipper=至少五次闭合早期头寸且首买到首卖中位数小于120秒；记录标签历史 | 规则仅为供应商明示的启发式，不是本项目统计校准阈值；其索引仅覆盖已追踪币的一部分 |
| MadeOnSol SDK（读取接口+类型，非后台模型源码） | atomic_tx与same_slot分开；bundle的当前持币份额、wallet flags及label_coverage/evidence_horizon；is_bundler lifetime、is_dumper 42d，false不等于无行为；onchain holdings对照trade-derived并计算transfer_delta | 不可将SDK类型注释误认为算法已复现或全量历史覆盖 |
| HoldTech深度扫描源码 | 以Slot对交易分组、采用不同fee payer数发现潜在群组，追溯SOL来源和Top持仓集中度 | detectBundles包含TRANSFER/UNKNOWN并以fee payer近似buyer；同Slot>=3不能证明Jito Bundle/同控；fundedBy使用fee payer推断并非实际转账发出地址；历史取样/分页不足会造成fresh误判 |

核心源码路径：
- https://github.com/GMGNAI/gmgn-skills/blob/main/src/commands/token.ts
- https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts
- https://github.com/MadeOnSol/madeonsol-sdk/blob/main/src/index.ts
- https://watchtowersol.com/docs
- https://birdeye.so/data-api/blog/detail/token-holder-profile-token-holder-positions-complete-holder-intelligence-on-solana
- https://birdeye.so/data-api/blog/detail/new-api-token-first-buyers-identify-the-earliest-buyers-of-any-solana-token
- https://docs.cielo.finance/guides/copy-trading/finding-good-wallets
- https://docs.nansen.ai/api/smart-money
- https://wiki.bubblemaps.io/bubblemaps-v2/how-does-it-work
- https://docs.jito.wtf/lowlatencytxnsend/

### C. Bundler三个不同对象不可合并

- **MULTI_SIGNER_OR_ATOMIC_TX**：同一原子交易中多个有证据的参与者；必须读签名、真实指令、Token owner/authority；并非多签必然同一实控。
- **JITO_BUNDLE_VERIFIED**：需要能识别原始Jito Bundle成员关系的证据，官方最多五笔、同Slot原子排序；仅共同Slot或tip不足以证明真实Bundle。
- **SAME_SLOT_COHORT**：只证实时段/Slot聚集，应与池子创建、公共事件、交易机器人服务和正常热点买入竞争解释比较。

对于任意Bundler候选，除买入时点，应同步计算：涉及钱包集合（与fee payer分别记录）、实际BUY、初始份额、当前库存、去向、卖出与转仓区分、资金来源、历史跨Mint重复出现。无法确认解析或覆盖时保持UNKNOWN。

### D. KOL与Sniper实际场景的关键分叉

- **Sniper**：观察Mint创建→市场真正可交易→首次已证Swap→进入价格/Slot→后续卖出→跨Mint重复；早进只能说明速度/排序位置，不证明内幕、持续盈利或可模仿。
- **KOL**：先确认公开钱包绑定/签名来源，再区分主动Swap与被动Token空投；将公开帖子传播时间与交易发生/可得时间分别记账。持仓不代表推荐，公开发言与买卖时序相关不等于因果。
- **Smart Money**：历史PnL还需补齐转仓成本、未实现头寸、平台选择偏差、窗口和实际上可观测延迟；供应商评分不能直接覆盖本项目信号到独立净收益断层。
- **Dev/Insider候选**：创建者/程序权限/初始资金/同源/分发/库存和公开事件有多种解释，不能给现实个人贴确定内幕或诈骗标签。

### E. 与当前项目的真实转化优先级

**优先完成“事实与标签分离”小样本对照，而不是先造万能分类器**：
1. 将旧qb-关键钱包矩阵、Hermes learning/10~12与Skill4、GMGN Skills和Birdeye的标签字典逐项对应到本项目D04；保存不同平台同名标签的定义冲突。
2. P3-M01先保证Swap/Transfer/fee payer/Token owner区分，才能计算sniper或bundler。现有fixture-only适配器不支持协议级BUY/SELL，不能声称现在已能自动标记真实Sniper。
3. 从一个真实Mint选几类非个人身份的链上行为样本，人工核对已有供应商标签和实际指令/持仓/转仓；保留无法确认。C02研究跨Mint群体重复，D05/D06追资金/库存，D07记录时序。
4. 标签作为观察入口，不自动触发交易规则；只有在后续机会存在并早于价格反应可见时，才讨论交易信息价值。旧项目的历史经验不断作为对照而非一次性读完丢弃。

**当前方向判断：CONTINUE，优先源语义和钱包角色交叉核对；暂缓建设规模化自动钱包身份分类器。** 更换路线的关键证据，是某个成熟现成解析/标签系统可以用透明契约和真实样本证明具备显著更好覆盖、较低误报与可复用性。

## 来源和已知污染边界

历史机制来源：`sunshihao001/-/learning/10.md`、`11.md`、`12.md`、`design/phase1-skill-03-wallet-roles.md`、`design/phase1-skill-04-wallet-structure.md`；`sunshihao001/meme-/07_样本标注/` 的正反例设计；本仓库 `wallet-roles`、`funding-graph`、`concentration`、`sybil-wash`、`deployer-history` 旧卡。

旧文档中“共享 Binance 出金地址 = 同一庄家”“同步阈值证明内部人”等只能列为**被挑战的历史断言**。本篇保留其值得调查的行为问题，不恢复这种归因。后期 `Why-Solana` 结论不参与本篇的事实基础。
