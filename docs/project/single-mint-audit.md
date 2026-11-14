# 单 Mint 深度调查｜Blix 现成能力与缺口登记（2026-11-06）

> 当前为静态源码路径审查，不是实际 Mint 调查报告；**严禁把 Blix 原生 Holder 标签直接升级成经济主体身份。**

## 已知产品入口

| 用户动作 | Blix 现有入口 | 所需进一步核验 |
|---|---|---|
| 在市场候选中找到 Mint | `server/engine.js`、`server/coin-screen.js`、`/api/tokens` | 发现与筛选覆盖、候选新鲜度 |
| 查看 Mint 基本调查 | `/api/token/:mint`、`server/coin.js`、`/api/holders/:mint` | Pool/LP、owner与Token Account、报告时间 |
| 查询关联买入/交易 | `server/wtrack.js`、`server/wallets.js`、`/api/wtrack/feed` | 同一交易多 Token 动作；历史分页与签名完整性 |
| 检查市场事件和历史 | `server/journal.js`、`/api/journal`、`/api/signals` | Journal约24h且仅部分venue，不代表12h所有资金转账 |
| 查看现有研究 | `/api/research`、`/api/research/:mint`、`server/research.js` | AI结果来自什么数据、有无公开引用与反证 |

## 必须补充的能力（来源与优先级）

1. Creator/同源资金：PumpTrace 现成调查和回填优先；发起者、fee payer、owner 不能混为一人。
2. Wallet → Mint → Wallet 双向发现：Million 现成服务；对同一交易多个订阅钱包需要完整核验。
3. Bundle/持仓集中：HoldTech、OKX、Bubblemaps 作为相互校核；同Slot≠确认的Jito Bundle。
4. 资金/库存多跳及跨 Mint 行为：Why-Solana、旧 Hermes/qb-/meme-、FnZero 方法；公共 Hub、Dust、SOL/WSOL 及Token-2022 必须单独处理。
5. 6h/12h 异常：优先验证 Helius/Bitquery 是否能查询完整历史，保留查询游标、时间覆盖、事件位置、数据缺口、净库存变化及群体成员演化。

## 决策优先级

**先保留 Blix 原 Mint 页面和数据库**，将额外事实通过完整只读业务服务/API 交付。若需要后续内置，必须证明接口复用无法满足完整业务需求，再最小改造。未获安全验收不得启动主服务或调用需要费用的API。

## 下一步可推翻条件

- 如果 Blix 的原生 Mint 路由不能在严格只读和无额外费用环境中获取有用数据，就不能直接宣称该业务已运行。
- 如果外部服务无法提供完整历史或结果口径不一致，就保留 UNKNOWN，不能编造“内幕群体占比”。
- 如果一次真实 Mint 调查可以完全借助外部成品/API 完成且低成本，优先避免新增同类解析器或数据库。


## 2026-11-07｜真实单 Mint 三次归档快照：多参与者目标与动态证据修正

> **首次真正用历史原始归档推进此前的“多主体目标”讨论，而不是再用合成市场故事做示范。** 对象：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`。本轮从原GitHub Actions的三个**真实在线归档ZIP重新下载原始JSON**，独立打开、比对 SHA256、根据提供方原始数值重算差异。对原档案的数据级检查**不是**Blix自身生产运行或原始Solana RPC逐笔重放；尚未完整还原发行、流动性增减、买卖者或跨Mint生命周期。原线上任务均在旧Grok [PR #16](https://github.com/sunshihao001/grok/pull/16)的研究分支执行。

### 1. 原始证据、时点与可复核性

| UTC采集时刻 | 原GitHub Actions归档 | DEX Screener原始JSON SHA256 | RugCheck原始JSON SHA256 |
| --- | --- | --- | --- |
| 2026-11-01 02:44:23.396 | [run 41266389009，Artifact 13067198705](https://github.com/sunshihao001/grok/actions/runs/41266389009) | `240dca2d3df8cfbf9e0f09d806d61b2ae6040abc07bcebc4b9dd3e07f3d09897` | 本次未取 |
| 2026-11-01 03:23:31.969 | [run 41268982018，Artifact 13068437092](https://github.com/sunshihao001/grok/actions/runs/41268982018) | `a7f941d5f2caca8c9ebff9b908b4a58dfa1009150ed55e986cb222fcd81e4de9` | `9671b8edf008772892035b22eb952b205409bc2125cb0f8fa16db5dd1178de0c` |
| 2026-11-01 03:26:30.596 | [run 41269179918，Artifact 13068576712](https://github.com/sunshihao001/grok/actions/runs/41269179918) | `07178b1ab4be4fdc57ef2f89c7ee425abaa3e53dbb8ffaaf9a8b14fc330dfbd0` | `d6baa59b89cbbfc8f4489253e35457415a2e53e8e2076da40179733ba6137054` |

本轮计算所用原始文件定位：第一归档 `v01-{mint}/provider-raw.json`；第二归档 `{mint}/dex-provider-raw.json`和`rugcheck-provider-raw.json`；第三归档 `mint/dex-provider-raw.json`和`mint/rugcheck-provider-raw.json`。以上三个归档实际下载结果和内部JSON格式均已检查。**Artifact有保留期**：两项RugCheck归档标记到2026-11-15过期，首个公开池归档到2026-12-01过期，因此这里保留来源值、SHA和计算，以免将来把已过期Artifact误认为永久可访问；如需长期独立重放仍须获得合法的原始数据存档。

DEX提供的主要PumpSwap池地址`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`，`baseToken`为目标Mint、`quoteToken`为SOL包装资产Mint`So11111111111111111111111111111111111111112`。三次提供方`pairCreatedAt=1793393408000`，对应**2026-10-30 20:50:08 UTC**；这是**提供方的交易对创建字段**，不可等同独立链上验证的Mint首次发行时刻。后续快照约在此后30小时附近，**不是完整发行到消亡历史**。

### 2. 同一池的真实短时变化：不只“看见价格”，还看库存

| DEX同一池字段 | 02:44:23 | 03:23:31 | 03:26:30 |
| --- | ---: | ---: | ---: |
| `priceUsd` | `0.0008148` | `0.0007653` | `0.0007819` |
| `liquidity.base`，目标Token单位 | `57,331,535` | `58,774,685` | `58,374,413` |
| `liquidity.quote`，SOL单位 | `465.47` | `457.4104` | `461.07165` |
| `liquidity.usd` | `91,059.46` | `88,618.50` | `89,627.83` |
| `volume.h24`，美元**滚动24小时** | `5,326,458.55` | `5,169,626.55` | `5,160,957.39` |

- **02:44→03:23（39.14分钟）**：价格**-6.075%**；池内Token **+1,443,150**；池内SOL **-8.0596**；美元流动性**-2.681%**。**积极的候选解释**：符合向池中卖入目标Token、从池中获取SOL的方向；因此“短时卖压/库存转移”值得作为**优先调查假设**。
- **03:23→03:26（2.98分钟）**：价格**+2.169%**；池内Token **-400,272**；池内SOL **+3.66125**；美元流动性**+1.139%**。这与上一段呈现**相反方向**的库存与价格变化，符合部分买入回补。
- **全段约42.12分钟**：价格约**-4.038%**，但中途发生了明确反向变化。它支持“同一池的流动性和库存不是静止快照”的观察，**不能直接证明**谁卖给谁、哪几个钱包下单、是否存在同控组织。
- **需要排除的另一生成机制**：池中Token和SOL储备变化既可由Swap造成，也可能由**添加/撤出流动性、手续费、不同数据刷新时点或采样语义**造成。只有真实交易签名、Swap资产净流和LP事件才能把“符合卖压”进一步升级为可确认净交易方向。
- `volume.h24`下降**不是**“这42分钟交易量为负”或“卖出比买入多”的证据：它是不断向前滚动的24小时统计，不同快照的差值不等于窗口期间成交量；`txns.h24.buys/sells`同样是交易次数的滚动窗口而非钱包数。

### 3. 被原问题遗漏的两个真实因素：极薄旁池和不同时点的池库存

**A. 市场微观结构：多池不等于存在可执行价差。**
三次快照中的Orca配对池美元流动性分别仅`47.83`、`47.66`、`47.71`；同期PumpSwap主要池约`91,059`、`88,619`、`89,628`，**约1,860–1,904倍**。03:23两池供应商`priceUsd`差异约**1.568%**（Orca较高）；03:26约**-0.281%**，数值变化可以产生**套利/报价调整候选**，但极薄池深、不同报价资产、滑点/费率及非同Slot数据意味着不能宣称可套利收益。返回的其余3个Pump.fun配对记录目标Mint是quote一侧且在这三次数据中没有可用美元流动性；**5个返回交易对≠5个同质/有深度的市场**。

**B. 数据测量：缓存Holder变化不等于链上Token转移。**
03:23 RugCheck`topHolders[0]`为Token Account`BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i`，Owner`81jgrp...`，其余额`58,487,680.128453`枚，供应商比例`5.877731%`；同期DEX池`liquidity.base=58,774,685`（差约`-287,005`）。
03:26同一RugCheck字段`59,418,764.31705`枚、比例`5.971300%`；同期DEX池`liquidity.base=58,374,413`（差约`+1,044,351`）。
RugCheck内的`markets[0].liquidityAAccount.owner`也与该PumpSwap池地址一致；其`knownAccounts`标签为`AMM/Pump Fun AMM`。这**有力支持该头部持仓记录属于池相关基础设施候选**，而非独立人类鲸鱼。两来源存在差异，应理解为**来源、缓存及读取时点未统一**的待查现象，不允许跨源直接相减声称某钱包3分钟内转出或吸筹。

### 4. 同一真实市场事实，让不同目标产生不同的、可执行的研究判断

| 目标/视角 | 当前有证据支持的积极认识 | 尚缺的区分证据 | 当前最有价值的只读行动 |
| --- | --- | --- | --- |
| **市场参与者/机会** | ~42分钟内池价格与Token/SOL库存发生两次方向相反变化；需要关注短时流动性/买卖力量 | 原始交易/LP事件、观察时差、是否早于公开信号、滑点和净可执行价格 | **先作为候选观察**，追真实Swap与连续报价；不当成现成买卖信号 |
| **做市/LP和库存风险** | 主要池深约9万美元，旁池仅约48美元；资产库存变化方向值得复核 | LP增减、Swap费用、真实池储备slot、AMM类型 | 优先对同池两端库存和LP事件对账，避免把全部储备变化记作净买卖 |
| **套利/执行者** | 03:23供应商跨池价格一度相差约1.57% | 同slot执行报价、极薄池深、费用/优先费、跨报价币汇率、可路由成交规模 | 把价差列为**市场结构线索**，不判断已经存在正收益套利 |
| **发行相关参与者** | RugCheck给出Creator候选`9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y`及`Copycat token`警告；发行/交易激励可能并存 | Creator历史、实际初始库存、Creator fee流向、与池中Swap签名的资金关系 | 主动追Creator与活动资金的关联，既不默认同控也不将警告等同骗局 |
| **链上取证者/风险** | 头部Holder Owner与主要PumpSwap池地址跨两供应商**精确一致**；排除“单纯头部私人鲸鱼”的表面解释 | RPC真实Token Account/池Vault与归属、关键钱包签名、公共Hub | **优先标识为池相关持仓候选**并防止污染钱包关系图 |
| **数据工程/统计** | 三次真实抓取和原始SHA可核；两源对同一池余额在短期内不一致，24h成交量不能差分得出小窗口成交 | 同slot原始账户、完整事件水位、缓存刷新时钟 | 让数据可得时间、事件时间和快照范围成为报告解释的一部分 |
| **市场机制研究/长期发现** | 已有真实的价格—库存方向切换；“有交易组织”“普通买卖”“做市/LP变化”仍是可区分假说 | 真实交易指令、交互地址、资金去向和跨Mint重复 | 比较各解释对**后续资金/库存/参与者活动**的预测，而非仅贴“庄家”标签 |

**优先排序（不是概率分）**：最强**确认性来源判断**是“有活跃PumpSwap池的两端库存变化、跨源池相关头部Holder匹配”；值得积极跟查的**经济候选**是“净卖入池后部分反向买入”；当前较弱、**不可直接确认**的是“Creator主导出货”“跨钱包操盘”“真正可执行跨池套利”。既不能因为某种竞争解释在理论上可能存在就取消观察，也不能提前声明已经追到了具体资金组织者。

### 5. 这轮对Blix已有业务的实际改变和停止条件

1. **市场发现**：从“看到5个池、高成交量”升级到“区分主流动性池/极薄旁池/目标Mint作为quote的配对”，强调高成交量不是钱包数，更非真实净新资金。
2. **单Mint调查**：优先验证**池地址与Holder Owner的跨源匹配**，识别池库存，不把近6%供应商池相关持仓作为庄家仓位；同时从三份真实快照形成“库存变化与价格方向”的可观察候选。
3. **跨Mint监控**：该案例**未取得一个已验证的真实资金边或钱包接力**，所以不伪造跨Mint群组。但应从已经查出的Pool、Creator候选和原始交易入口确定下一项追踪对象，避免先猜幕后控制者。
4. **多目标/多专家综合**：无需强迫所有视角达成“这币值得买/是骗局”的唯一结论；可同时报告**短时库存方向线索、池相关持仓事实、Creator风险候选与缺失的执行证据**。在市场机会问法下优先研究执行时差和池深；在风险问法下优先研究Creator和池Vault；在机制问法下优先研究资金/库存形成原因。
5. **下一项最具信息价值的核查**：不用新造Blix市场终端，选择这个PumpSwap池在02:44→03:26的**实际Solana Swap与LP事件签名**进行只读归因；如能核明Swap带来主要资产变动，“净交易方向”推断增强；如LP变动解释大部分则修正；若发现钱包间直接资金/Token接力才进入群体目标推断。这也是本轮研究的**停止边界**：凭三份提供方快照不能继续凭推理得出交易者身份、资金闭环或预测Alpha。

**方法总结**：此前的“不同市场参与者目标”和“不同专家目的”不再停留在概念罗列；本次真实源揭示了市场参与者可能采取的不同经济行为，同时告诉我们**不同假设需要不同的可观察证据**。这次是三个真实快照的离线重读与计算（`ARCHIVED_VENDOR_SNAPSHOTS_REPLAYED`），**不是**`REAL_TX_SEQUENCE_RECONSTRUCTED`、`BLIX_PRODUCT_RUNNING`、`MODEL_AB_VERIFIED`或`TRADING_ALPHA_PROVEN`。

## 2026-11-14｜从即将到期的 GitHub Actions 重新取回原始数据：同次供应商观察中的两枚真实 Mint

> 2026-11-14 重新执行**实际文件下载、ZIP解包、JSON哈希复算**，而不是依据旧报告推测。有新的、此前总目标对照忽略的事实：首次 [GitHub Actions run 41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009) 的 ZIP 不仅含 BNB，还含 **SIS**，在同一自动任务中约 **0.13 秒**间隔读取 DEX Screener。两枚都是真实历史供应商查询对象；**没有证据称它们属于原版 Blix Pulse 实际候选名单**，不能把供应商同批数据冒充真正 A/B 模型选币或全市场行情。

### 归档逐项重新获取和核验（原始资料取回，非主网重放）

| GitHub Actions run / artifact | GitHub记录过期时间 UTC | 2026-11-14实际ZIP SHA256 | ZIP内来源原JSON SHA256 |
|---|---|---|---|
| [41266389009 / 13067198705](https://github.com/sunshihao001/grok/actions/runs/41266389009) | 2026-12-01 02:44:23 | \`afeb32206d063a2f1e2ab68dbc35f736a1caa3fe093f8ecb13691171ced05053\` | BNB DEX \`240dca2d3df8cfbf9e0f09d806d61b2ae6040abc07bcebc4b9dd3e07f3d09897\`; SIS DEX \`5cdeb33076e1df0a2efc24c1c3daf6b4cce4c3832ac131ddaf4f5ab105dbf7b4\` |
| [41268982018 / 13068437092](https://github.com/sunshihao001/grok/actions/runs/41268982018) | **2026-11-15 03:23:32** | \`e6ed61dbf11591f0e4ef2e7b9f8f42ad9cd1ecd1041963ce7920300afd0531c3\` | BNB DEX \`a7f941d5f2caca8c9ebff9b908b4a58dfa1009150ed55e986cb222fcd81e4de9\`; RugCheck \`9671b8edf008772892035b22eb952b205409bc2125cb0f8fa16db5dd1178de0c\` |
| [41269179918 / 13068576712](https://github.com/sunshihao001/grok/actions/runs/41269179918) | **2026-11-15 03:26:31** | \`f49e7c5fd5c7a8f9162f307d29d63b36bb4a2d97d244075b10cec71450767be0\` | BNB DEX \`07178b1ab4be4fdc57ef2f89c7ee425abaa3e53dbb8ffaaf9a8b14fc330dfbd0\`; RugCheck \`d6baa59b89cbbfc8f4489253e35457415a2e53e8e2076da40179733ba6137054\` |

**文件留存**：三份原始 ZIP、其内17个原始归档文件与SHA清单已打包到本轮ChatGPT产生的文件 \`blix-20261101-original-market-snapshots-preserved-20261114.zip\`；完整复合ZIP SHA256为 \`b8ade9d33bfc16cbbb43c78fa49415490f1860e08548bae06d4853ce2325bcf8\`。**本GitHub文档只保存可复核的来源索引与关键事实，不要把它说成已经把所有原始ZIP永久上传到了GitHub。** 原GitHub Actions artifact会依到期规则清理；需下载本轮备份包以便长期完整重放。

### 相同历史任务的双Mint，实际观察到什么

| 2026-11-01 UTC约02:44:23 | BNB · \`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump\` | SIS · \`FdKdpz11GsTofLaNiddrhxrsE4APZYSSfLFqQ9YKpump\` |
|---|---:|---:|
| 来源 \`retrieved_at\` | 02:44:23.396196 | 02:44:23.526475 |
| DEX Screener返回的配对数 | 5 | 7 |
| 主要PumpSwap池的Token价格USD | \`0.0008148\` | \`0.0005512\` |
| 主要PumpSwap流动性USD | \`91,059.46\` | \`64,871.47\` |
| Orca旁池价格USD | \`0.0008145\` | \`0.0004137\` |
| Orca旁池流动性USD | \`47.83\` | \`52.31\` |
| 主要/旁池美元流动性倍数 | 约\`1,904×\` | 约\`1,240×\` |
| Orca相对主池**展示价格**差 | 约\`−0.0368%\` | 约\`−24.9456%\` |
| 价格或流动性缺失的其他配对数 | 3 | 4 |
| 后续03:23、03:26真实快照 | **有**（BNB三时点，另有RugCheck两次） | **没有** |

**三种显著不同的分析结果**：
1. 单看“哪个Mint有更多交易池”会偏向SIS（7 vs 5），但这与有足够交易深度的市场数、交易机会和安全性不是同一指标。
2. SIS的Orca展示价比其PumpSwap低约25%，貌似大幅套利；**Orca池仅约52美元**，而报价不同源时钟、实际可成交路由、池状态和费用均未核实，因此**不能称为实际套利或可跟随盈利**。即使实时价差存在，也需要订单规模下的买卖双边有效报价。
3. BNB三时点价格及池储备变化允许提出卖压/LP/缓存不同步的竞争假说；后来两次RugCheck原始档显示最大Token Account \`BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i\` 的Owner为主池 \`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB\`，其\`markets\`及\`knownAccounts\`同样标为Pump Fun AMM，不能把该Holder误当成私人鲸鱼。**SIS没有此时间点的RugCheck档案，不能据此宣称其安全或风险相反。**

### 和“原版 Blix vs GMGN/Million/AI增强”测试如何真实对齐

- 这次终于得到**同一实际供应商观察批次中的两个真实Mint**，所以可以对照**市场字段解释和多池错误机会判断**，并用 \`test/fixtures/public-provider-two-mints-20261101.json\`（只含由原档复算的有限事实）及 \`test/public-provider-two-mint-history.test.mjs\` 复现拒绝把展示价差当已验证套利的边界。
- **仍然没有**当时完整Blix候选 Universe、过滤记录、原Blix信号首次对人可见、GMGN Radar历史钱包群体、独立真实区块交易/LP、双边尺寸化报价和完整跟单失败样本。这意味着原R-38的**同候选AI A/B算法或真正交易收益优势并未被这批真实数据验证**。
- 下一次应寻找/保存**真正具Blix Pulse或Wallet首次可见时间的同批候选和排除记录**，再使用已有A/B只读比较器；不能把本轮“供应商两枚Mint”强行填成假Pulse截图，不能把随时间变化的滚动24h交易量差分为短间隔买卖额。

**证据状态**：DOWNLOADED_SOURCE_ZIPS + VERIFIED_MEMBER_SHA256 + HISTORICAL_TWO_MINT_SAME_VENDOR_RUN + OFFLINE_TEST_FIXTURE；**不是** BLIX_REAL_A_B / CHAIN_VERIFIED_SWAPS / EXECUTABLE_ARBITRAGE / LIVE_MODEL / ALPHA_PROVEN。

