> **Blix 旧知识全文迁入｜协议/市场基础** · 原来源：[knowledge/domain/L1-L2-chain-market.md](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/domain/L1-L2-chain-market.md) · 原文件blob SHA `da2bc12cce685bb6b681fe30569219ed43e61944` · 原研究领域 D01,D02,D03,D10 · 验证状态 **SOURCE_COPIED / RESEARCH_NOT_RUNTIME_VALIDATED**。旧文件的研究阶段、阈值、假说和引用保持其原意义；不作为现行全局指令。

---

# L1–L2｜链上事实、Meme 生命周期与真实市场结构

> 对应现有领域：D01、D02、D03，横切 D10。本文填充 `ontology.v1.json` 已定义的专业知识，不新增层级或 Bot。知识身份：`domain_method_candidate`；下文的字段为**规范化采集目标**，不是已接入的 OKX/GMGN 字段声明。任何基于真实行情的数值均需 K2 证据。

## D01｜Solana 链上基础：先把交易读对

### D01-01｜地址、账户与经济行为主体不是一回事

对一个 Meme token 至少辨认：Mint 地址、Token Program（传统 SPL 或 Token-2022）、Token Account/ATA、该账户的 token owner、发起交易的 fee payer、实际签名者、AMM vault、程序派生地址 PDA。一个钱包可能持有同一 Mint 的多个 token account；一个交易手续费付款方不一定是实际资产所有人。**数 token account 数量，不等于数独立持币人**；把 pool vault 或程序账户算入普通 Top10，可能扭曲集中度。

- **需要取得**：`mint`、`token_program_id`、`token_account`、`token_owner`、`fee_payer`、`signers`、`account_owner_program`、`account_role`、账户快照 `slot`。
- **不得推断**：同一 fee payer = 同一交易控制者；同一 token owner = 同一个自然人；ATA 刚创建 = 新的钱包主体。
- **下一项鉴别**：确认 token account 的 owner 字段和创建指令；识别 vault/PDA/托管地址，再进行钱包归并。
- **基础资料**：[Solana Token 官方定义](https://solana.com/docs/tokens)；[Token Account / ATA](https://solana.com/docs/tokens/basics/create-token-account)。

### D01-02｜一笔交易不等于一次买入；转账也不等于成交

Solana 的 `getTransaction` 可能涉及版本化消息、Address Lookup Table、外层指令、CPI 内层指令及前后余额。一次聚合器交换可能穿过多个池；同一笔交易中有多个 token 转移与费用，不能简单用“出现 SPL Transfer”识别一次买入。**Swap 的经济净额**应按照预先定义的交易主体、Mint 与账户余额变化重建，再按池事件和路由解释。

- **需要取得**：`signature`、`slot`、`err`、`message.accountKeys`/loaded addresses、`instructions`、`innerInstructions`、`preTokenBalances`、`postTokenBalances`、`preBalances`、`postBalances`、`meta.fee`。
- **区分**：买卖成交、账户间转仓、LP 注入/取出、ATA 创建/关闭、Token 铸造/销毁、费用、wrap/unwrap SOL。
- **错误防线**：交易执行失败不能记成已成交；同一聚合器路由跨多池不能重复累计“独立交易”；余额净差不一定能逐笔定位中间资金路径。
- **下一项鉴别**：原始 inner instructions + program ID + pool vault 变化三方对齐；无法归因则输出 `UNCLASSIFIED`。
- **基础资料**：[Solana Transaction Introspection](https://solana.com/docs/core/transactions/transaction-introspection)。

### D01-03｜时间语义决定能否跟单

`event_at`（链上发生/记录时间）、`slot`、`provider_received_at`、`parsed_at`、`feature_available_at`、`decision_at`、`quote_at` 是不同的时钟。历史上能在区块看到，不代表当时本监控端已经收到并解析。块时间可能为空或具有不确定性，不能默默补零。

- **关键问题**：钱包首买、我方首次可见、可形成信号、可取得报价之间，市场已经发生多少价格和深度变化？
- **必须分类**：`live_recorded`、`historical_backfill`、`synthetic_fixture`。
- **禁止**：把历史回填链上时间直接当作实时 `available_at`，或用未来完成的 cluster 标注解释早期买点。

## D02｜Meme 生命周期：不同阶段不是同一个市场

### D02-01｜Token 存在、可买、可卖与进入候选池

确认 Mint 存在只是资产事实；Bonding Curve 阶段的执行机制、毕业/迁移状态、AMM 池状态不同。不得假设所有新币都遵循固定的 pump.fun → Raydium 路径；以具体 launchpad、程序、事件为准。

- **观察**：`mint_created`、`launchpad_program`、`curve_state`、`migration_event`、`pool_created`、`pool_liquidity`、`first_successful_swap`。
- **辨析**：曲线完成不代表交易风险解除；出现 pool 不代表任意仓位都能退出；同符号不同 Mint 必须视为不同资产。
- **下游**：D03 根据阶段计算有效深度，D04 记录钱包在阶段内的实际位置。

### D02-02｜同一代币的生命周期切换会重置指标解释

新币前 30 秒、曲线后半段、刚迁移、迁移数小时后，成交结构和钱包行为的含义不同。热门榜历史、K 线、聚合器价格、Top holders 快照的起始窗口往往不同，不能不注明区间就直接比较。

- **输入**：`market_stage`、`stage_event_ref`、`stage_observed_at`、`stage_available_at`、`provider_coverage_from`。
- **举例**：迁移后美元流动性突然上升，可能源于新池建立，不能自动解读为独立资金“开始吸筹”。
- **可证伪问题**：一个候选信号是否仅因阶段切换产生，而非真正的买方行为变化？

### D02-03｜安全能力与资金风险分开

`mint_authority`、`freeze_authority`、Token-2022 的实际扩展、LP 变更与交易卖出失败是不同事件。权限被撤销可缩小某类风险，但不证明持有人或流动性安全；某次失败交易可能是路由/余额/滑点而非恶意锁卖。

- **观察**：Mint/Token Program/扩展集合、权限快照和变化签名、池地址与储备、可用卖出路线及其错误码。
- **不得推断**：一个“安全”平台标签即可排除全部风险。
- **基础资料**：[Solana Token Basics](https://solana.com/docs/tokens/basics)；[Token-2022 Permanent Delegate](https://solana.com/docs/tokens/extensions/permanent-delegate)。

## D03｜市场微观结构：价格高不代表跟得上，更不代表卖得掉

### D03-01｜报价、末笔成交与实际执行价格

`last_trade_price`、池中边际价格、聚合器 quote 和实际 fill 不是同一个价格。必须按买入/卖出方向、仓位金额和当时路线询价。Meme 的价格弹性会随池深度、交易方向、市场波动及拥堵改变。

- **必需**：`pool_address`、`quote_direction`、`quote_at`、`amount_in_raw`、`amount_out_estimated_raw`、`min_out`、`route_ref`、`provider`、`fee_estimate`。
- **区分**：研究历史 peak/MFE 只能说明价格曾显示过什么，不能说明某规模的订单可在该点卖出。
- **反例**：价格涨了 2 倍但当时卖出的可用 SOL 深度不足，跟单者净收益仍可能为负。

### D03-02｜流动性是储备和价格共同决定的状态

`liquidity_usd` 下降可来自池中数量变化、计价资产贬值、市场价格重估、路由更换或 LP 实际撤出；必须先把数量变化与美元估值变化分开。

- **取得**：按池和 slot 对齐的两侧 `reserve_raw`、token decimals、SOL/其他计价币价格、LP add/remove 交易、池类型。
- **不得推断**：单一 `liquidity_usd` 百分比告警就能证实 Rug 或大规模抛售。
- **下一项鉴别**：核查是否真有 LP 相关指令和实际可卖报价恶化。

### D03-03｜买卖压强与可成交买方不是一回事

高成交量、许多小额买入、价格快速上行可能同时存在，但这些不一定代表独立买方需求；同一主体可在关联地址间制造成交，套利/做市路由也可形成大量交易。

- **观察**：按钱包/实际 token owner 去重的净买入、单笔净额、持有持续时间、对手路由、成交后余额变化、交易失败率。
- **下一项鉴别**：D05 资金网络与 D06 经济持仓是否显示同一资金在来回循环？D07 是否只是市场共同事件驱动？

### D03-04｜MEV、优先费和竞争性执行

同一机会被多名监听者发现后，实际成交顺序和费用可能与历史平均不同。手续费、priority fee、tip 和价格冲击在高竞争时段可能同向上升。

- **重点**：事件可见延迟、交易落地概率、失败后已支出费用、目标仓位对价格的冲击。
- **禁止**：用固定通用滑点或固定小额手续费替代实际可得双向报价；纸面询价不能冒充真实 fill。

## D10｜数据源与完整性（贯穿上述所有领域）

### D10-01｜OKX / GMGN / RPC 各是什么来源

- **OKX**：当前优先研究其 `okx-dex-market` 只读能力（Token、Market、Signal、Social、Trenches、WS）；官方文档提供的命令和字段是**接入候选**，非已经运行的实际结果。
- **GMGN**：保留早期 `trending / trenches / signal` 的发现入口概念，但原始字段映射和订阅权限未验证，不作为当前必付费数据依赖。
- **Solana RPC**：可作为原始交易、账户和程序状态的关键比对来源，但 RPC 完整覆盖、时延和历史可用性仍需要实际测量。

### D10-02｜字段应有独立语义合同

每个字段至少记录：`provider`、`endpoint_or_command`、`source_json_path`、`raw_value`、`raw_unit`、`normalized_value`、`normalized_unit`、`decimals`、`window_start/end`、`provider_request_time`、`received_at`、`missing_reason`、`raw_hash`。

例：OKX 的某钱包 PnL 不等于用完整 swap/转账/空投/未实现头寸自行复算的已实现利润；供应商指标必须保留口径和覆盖边界。

### D10-03｜被漏掉的市场也是研究对象

断连、429、无池、未知路由、解码失败、缺少历史数据等必须保留为 `SOURCE_UNAVAILABLE` 等状态；不可默认当作 0、没有交易或信号失败。研究 denominator 必须包含未成功获取的候选。

## 本篇端到端实例（仅示意，无真实链上验证）

**现象**：某 Mint 在迁移后 90 秒进入热门榜，池的 `liquidity_usd` 较上一快照下降 25%。

正确处理顺序：

1. D01：核对 Mint、Token Program、池账户及事件签名，确认两快照来自同一经济市场。
2. D02：确认是否刚发生池迁移/重新建池；若是，不直接比较两个阶段。
3. D03：用原始储备与计价价格拆分美元流动性变动，核对双向报价。
4. D10：查实际请求时间、字段口径和遗漏；无法复算就保留 `NEED_MORE_DATA`。
5. 只有确认事件性质后才传给 D04–D09；监控告警不是“庄家撤池”的结论。

## 来源与证据地位

内部早期参考：`sunshihao001/-/learning/05.md`、`06.md`、`07.md`、`08.md`、`09.md`；本仓库 `catalog.v1.json` 的 `market-lifecycle`、`token-security`、`liquidity-depth`、`candidate-entry`、`gmgn-raw-prototype`。外部操作接口参考：`okx/onchainos-skills/skills/okx-dex-market/SKILL.md`。上述内部早期文档为机制候选，不作为已验证的收益来源。

## 2026-11-01｜D01/D03跨源地址与池库存的实务归属边界

真实Mint `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` 的RugCheck缓存Holder第一名Token Account（供应商5.877731%）其Owner候选与DEX Screener的PumpSwap池`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`地址完全相同。该**供应商字段精确匹配**可标池相关候选，但不能证明单一资产受益人、池Vault及LP的真实权益归属。特别不能将这个持仓比例直接加进“个人鲸鱼持币/庄家控盘”指标。需要同slot的Token Account Owner、池Vault、LP状态核查，此次Solana公共RPC曾返回429而未取得数据。

池级24小时买卖统计和价格不是钱包级Swap事实；`pairCreatedAt`不是Mint创建时间；RugCheck`detectedAt`不是区块事件时间。详细原始数据和交叉检验见[工程证据](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/evidence/v01-pool-vault-holder-cross-source-2026-11-01.md)。此条只升级“跨源身份误归因风险”的知识，不代表D01 Swap完整解析或经济控制已验证。


## 2026-11-13｜D01/D02/D03/D10：原始RPC与局部经济图谱的适用边界（当前候选PR #23）

本轮专业源级复核见[统一P1/P2知识对照账](../references/p1-p2-knowledge-reconciliation-20261113.md)。Solana 官方 [RPC JSON结构](https://solana.com/docs/rpc/json-structures)、[交易指令解析](https://solana.com/docs/core/transactions/transaction-introspection)、[Token-2022 转账费用](https://solana.com/docs/tokens/extensions/transfer-fees)和[Transfer Hook](https://solana.com/docs/tokens/extensions/transfer-hook)共同要求区分：**交易签名/指令/余额差**、Token Account/owner/authority、fee payer、实际成交对价、Token可用余额、真实经济控制方。官方新文档还描述了v1的transactionConfig结构及其不使用v0 ALT的差异，历史v0/legacy解释不能当成完整版本集合。

- **已在源码出现**：`server/economic-events.mjs`保留jsonParsed原文，索引outer/inner CPI与Token转账；`server/intelligence/economic-network.mjs`按sig+outer+inner生成只读图谱，BigInt输出已观察的raw转入、转出、净变化、事件签名。代码/合成测试存在，不代表支持所有程序和链上事实。
- **Token-2022限制**：raw transferAmount未必等于收方可动用库存；配置了TransferFee时费用会在目标账户扣留，TransferHook可额外触发CPI。不能仅凭当前图谱的raw数额计算可卖份额或把Hook相关内层事件都当独立外部交易。
- **SOL/WSOL/Swap限制**：原报告的Token Transfer边只证明局部指令上的资产移动；它可能发生在Swap内部。资产净变化、费用、rent、WSOL包/拆与池内储备应另以原始账本核对，不能用“多跳Token转移量”代替独立买入需求或完整利润。
- **历史窗口限制**：`getSignaturesForAddress`按地址返回有限签名页面，需按before/until检查分页和覆盖；“最早可见”不是钱包创建时间，局部空查询不是无交易。
- **下一项检验**：同一真实Mint比较raw/jsonParsed、CPI、Owner、Token-2022 fee/Hook、多池、SOL/WSOL和来源时点；通过前所有真实价格影响、完整余额、经济控制权仍为UNKNOWN。

本节是对历史知识的**现行适用修正**，不修改旧章节的历史身份。部署/真实模型API/主网确认均未因CI通过而自动完成。

## 2026-11-14｜全域归位：D01 协议事实、D02 发行生命周期、D10 数据可信度（当前主述）

**知识对象分开**：协议可以证明账户、签名、指令、余额与程序行为；市场阶段描述发行、曲线、迁移与池；数据源描述何时、通过什么接口、以什么覆盖范围观察上述对象。一个原版Blix页面显示了报价不等于同步观察到完整链上成交。此处是专业事实语义的主述；研究资料原文仍留在 `knowledge/references/`，运行代码/测试状态在 `docs/project/build-register.md`。

| 专业域 | 需要保持完整的知识链 | 过滤时必须保留的不同结果 | 原Blix/扩展承接 |
|---|---|---|---|
| **D01** 链上事实 | Signature→Slot/确认状态→消息账户/ALT→顶层与inner CPI→Token/Token-2022→TokenAccount/Owner/Authority/Fee Payer→资产净变化→Swap/Transfer/LP/系统SOL与WSOL→费用；失败交易亦独立标记 | 可核实的转账/调用、局部成交候选、身份不可识别、未取得指令数据；不把一笔多动作交易重复计为多个经济买盘 | 原 `solana.js`、`holders.js`；扩展 `economic-events.mjs`、`economic-claim-trace.mjs` |
| **D02** 生命周期 | 发射平台/权限→曲线可买卖与储备→接近毕业→迁移/新池→多池价差与深度→Creator/Dev历史、LP与代币权限变化 | “Token存在”“有报价”“实际可卖”“已迁移”“安全”是五种不同命题；事件来源错误不能靠AI重命名修复 | 原 `engine.js`、`launchlab.js`、`creator.js`、`coin.js` |
| **D10** 数据可靠性 | 来源权限和字段→WS/API/RPC原始消息→事件与获取/首可得时钟→原始保存/hash→去重、缓存、游标、断流与回补→版本/来源冲突→覆盖水位→消费端质量状态 | 未捕获≠不存在，首次本地收录≠最早市场可得，来源健康≠全历史完成，归档覆盖≠市场全集；保留 UNKNOWN/UNCOVERED | 原 `sources.js`、`livetrades.js`、`coverage.js`、`db.js`；扩展 `wallet-signature-coverage.mjs`、`scripts/audit-intelligence-source-readiness.mjs` |

**专业过滤条件**：先确定对象类型、具体市场阶段、数据提供方、链上/供应商时间、账户身份、池和原始单位，再使用结果；无须为了“完整”给每个Mint抓全历史，但不应把只捕获几笔的局部样本称为全链。Token-2022 转账费用和Hook的用户可用金额与原始transfer金额可能不同；一笔交易包含Swap+Transfer+LP时以签名/指令位置/owner净额核对，而不是按标签相加。**本句是审查规则，不是宣称所有协议变体已由现代码支持。**

**从外部知识归位**：Synapse的S06/S12/S13属于跨市场事件研究，S07 Push、S08 Pull可帮助区分Token移动的指令语义；其14信号、DEX/HyperLiquid和噪音分类的**完整原始转述**仍见 [全分类保留目录](../references/synapse-methodology-full-taxonomy-20261114.md)，不能直接当Solana协议事实。Pulse、pumpwatch用于发行全集/失败样本，PumpTrace用于Creator/历史，Solana官方协议与FnZero/Carbon解析器用于校准真实指令，GMGN/OKX只提供各自字段与产品语义（需核权限）。独立详细差异见 [跨项目对照](../references/p1-p2-knowledge-reconciliation-20261113.md)。

**运行边界与待验**：当前已通过原版Blix在完全封网容器中的新SQLite冷启动/二次重启/HTTP健康与Pulse返回，不是联网市场覆盖；尚缺一段**真实市场同一Mint**的来源原文、source-first-available、断流与补查、完整链上签名和多池对账。资料可检索、解析有离线测试和现场市场可靠运行属于不同等级。
