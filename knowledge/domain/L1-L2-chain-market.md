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
