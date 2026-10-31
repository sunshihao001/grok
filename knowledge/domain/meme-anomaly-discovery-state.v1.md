# Solana Meme｜P2.1–P2.4 异动发现方法融合目录 V1.0

**2026-10-31｜方法研究资产，非经链上独立复算的规律或正式告警规则。**

## 主研究问题

从不同时间窗口内钱包数量、成员组成、资金来源、转账、Swap、代币库存、执行延迟与跨 Mint 重复活动，发现可监控的连续关系和状态变化；不预设“庄家”、身份控制或可交易获利结论。

本文件从聊天研究中提取**可以复用的候选方法**，去掉重复表述。相关代码在独立 PR #16，知识版本修订在 PR #14；两条 PR 未合并前不要当作主分支正式能力。

## 1. P2.1 观察维度归并：候选初筛，不单独维护16篇知识

- **规模/金额维度**：群体扩张与收缩、钱包数量和总资金/平均金额背离、活跃度与外部净流不一致。
- **时间维度**：批次节奏、延迟执行、休眠地址苏醒、规律突然停止、执行间隔改变。
- **资金网络维度**：单源多目标分发、多源归集、短路径接力、内部资金循环和再部署。
- **钱包关系维度**：旧群体成员更替、角色变化、分裂/重组、跨 Mint 地址和融资关系复用。
- **市场经济维度**：买入人数与群体净持仓背离、流动性事件与群体变化、重复发行模板、成交笔数与实际资本投入区别。

以前 P2.1 提出16项名称是探索清单，**不是16条相互独立且实证有效的监控规则**。本文按机制合并后续重复概念。

## 2. P2.2 五个连续行为方法（候选）

| ID | 研究对象 | 关键变化 | 当前状态 |
|---|---|---|---|
| M01 钱包批次成员演化 | 同Mint连续时间窗口内的钱包集合 | 留存/新增/缺席/返回，与买卖金额背离 | **fixture-only代码已在 PR #16、CI通过；真实数据未接入** |
| M02 分发→延迟交易 | 融资到账后首次Swap/转账时距 | 延迟分布与执行人群比例变化 | 设计候选 |
| M03 拆分→接力→归集 | 时间有向资产流图 | 多跳路径、归集后再部署、公共Hub/混合资金排除 | 设计候选 |
| M04 群体替换与行为继承 | 原群体停止，新群体出现 | 直接/间接资金连边与执行动作变化 | 设计候选，不等于同控 |
| M05 群体库存与买卖背离 | 固定钱包集合的Token余额、Swap与内部转仓 | 买入地址上升但群体真实库存可能下降 | 设计候选，需确保集合边界稳定 |

**方法之间的联系**：M01提供规模和成员基准；M02提供收款到执行时序；M03提供资产流连边；M04对跨组关系形成候选；M05提供资产库存核算。不能将所有方法简单相加成“操盘分数”。

## 3. P2.3 五种前兆候选（不等于可预测）

- **P23-01 预部署**：资金分发后，收款钱包尚未执行目标Swap。注意SOL转账本身无法绑定未来Mint。
- **P23-02 执行加速/减速**：资金到账到交易的延迟分布改变；尚未走完观察期的收款不能作为“未执行”终值。
- **P23-03 渐进替换**：旧群体变少、新群体变多；须找资金/角色额外证据才能研究接力。
- **P23-04 库存迁移**：内部转仓、跨边界Token转移和真实Swap卖出分开。
- **P23-05 沉默与恢复**：原有行为序列中断或改变；须排除RPC断流、市场时段及协议事件。

**必要评价**：研究前兆时，必须保存在当时确实可见的 `available_at`，以及前兆出现但后续异动**没有发生**的负例。单靠事后行为链不能证明预警能力。

## 4. P2.4 五项跨Mint/跨群体方法（本轮增量）

| ID | 专题 | 监控所需新增关系 | 建议 |
|---|---|---|---|
| C01 | 跨币资本循环间隔 | Mint A退出资金—收款/归集/分发—Mint B交易的时间有向路径 | 优先 P2.5；需M03支持 |
| C02 | 同群体执行方式切换 | 同组钱包在不同 Mint 的收款→买入延迟、交易规模、退出方式 | 优先 P2.5；按币龄/池深分层 |
| C03 | 不同群体相似行为模板 | 不同地址群重复分发→买入→转仓→归集顺序 | 只作研究线索；排除共享机器人服务 |
| C04 | 钱包数量与资本投入背离 | 跨币买入钱包数、报价资产成交额、交易次数 | 可先复用 M01，不能称净资本流入 |
| C05 | 原有执行结构停止/迁移 | 已知群体行为停止，资金或角色在其他 Mint/协议恢复 | 优先 P2.5；须检查数据覆盖 |

这些候选不是新层级：横跨 D04/D05/D06/D07/D08，交易原语依赖 D01，事件时点与数据语义依赖 D10，正常对照/失败样本依赖 D11。

## 5. 外部来源与边界

- 用户参考的公开研究 `sunshihao001/Why-Solana-Memecoins-Are-Over`：`coordination_detection/results.md`、`funder_network/results.md`、`sniper_capital/results.md`、`post_detection_forensics/feature_dictionary.md`。此处只提炼研究问题与失败模式；研究样本被选择过，**外部报告不当作本项目已独立复验数据**。
- `okx/onchainos-skills` 中 `okx-dex-market` 已提供地址、聚类、Meme 和市场数据入口，但未证明可直接输出完整跨Mint资金图。
- Solana 原始交易需要区分 Token Account owner、fee payer、program/router、CPI、Swap 与转仓；同Slot不是同一操作者的证明。
- 含净资金/库存/交易盈利的判断必须明确观察集合边界、发生时间、可得时间和真实资产单位。

### 外部知识补充：区别协议原语、研究标签与行业黑话（2026-10-31）

**AMEND，非新增异常检测编号。** 本项目过去经常使用“捆绑钱包”“sniper”“同源融资”“bundle”等词，应查明每种词到底是协议对象、研究者自定的链上簇、还是供应商宣传标签。**Jito Bundle** 指 Block Engine 处理的最多5笔、顺序原子执行的交易组；同 slot 买入多笔、相似 tip 或相同资金来源并不单独证明真实 Jito Bundle。Jito 官方：https://docs.jito.wtf/lowlatencytxnsend/ 。外部研究的 sniper cohort/group snipe 应以其样本筛选和定义为准，参考 https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over 。

另须区别 Token Account owner、程序 owner、authority/delegate、fee payer；它们的共同出现不等于相同控制人。Solana 官方：https://solana.com/docs/tokens/basics/create-token-account 、https://solana.com/docs/core/transactions/transaction-introspection 。这项知识直接影响 M01 的钱包去重和原始交易适配器，以及 C02/C05 正常反例。未来按问题需要扩展真实术语和跨领域解释，只有改变数据定义或可证伪方法的新增认识才修订本专题；不要建立同义词词典或将行话当成证明。

### 最新协议边界：交易 v1 不能被当作不存在（2026-10-31）

[Solana 官方版本文档](https://solana.com/docs/core/transactions/versioned-transactions) 表明 v1 交易格式已激活（与 v0 的 ALT/费用模型不同）。P3-M01 当前仅支持 legacy/v0 的离线标准化，**v1 的拒绝与 INCOMPLETE 才是正确输出**。若上游索引未处理 v1、或因版本不支持将整区块当空块，会污染 M01 成员数量和 C05 的行为沉默结论。工程边界与模拟测试见 PR #16 中的 [原始适配器契约](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)。当前无真实数据对账支持，不升级为已支持 v1。

## 6. 工程交付：P3-M01 与研究分开

- **代码草案**：`https://github.com/sunshihao001/grok/pull/16`，包含 `src/solana_meme_os/wallet_batch_monitor.py`、14项新增离线测试、fixture、使用说明。
- **已核查**：GitHub workflow `monitor-tests` 在该PR最新SHA `73301ca892ff66e33d9abc5486ff3df5a4ca9422` 成功完成；本地新增14项合成测试亦通过。
- **未完成**：未经真实Solana RPC数据解析检验；不具备自动地址归属证明；不连接生产Grok监控、不下单；不能将测试通过升级成市场预测或真实盈利证据。

## 7. 历史 P2.4 研究缺口（已进入 P2.5）

**P2.4 概念探索已形成一轮结果，可进入 P2.5 方法筛选**；优先对 C01/C02/C05 做同等活跃度、同类发行阶段的比较方案。M01 的下一工程任务是用独立规范化器把真实链上交易解析为可审计的经济行为事件，并用人工标注小样本检查账本一致性；这是后续局部 P4，不必阻碍 P2.5 知识筛选。

**可复制下一轮输入**：

> 正式进入 P2.5「监控候选筛选和知识编译」，以 C01 跨币资金循环、C02 执行方式切换、C05 行为停止迁移为优先，重新读取最新专题与 M01 Draft PR。不要增加更多同义指标。对每项说明和既有 M01–M05 的区别、链上最小字段、正常反例、验证与实现代价，最终选定 1—2项作为 P3 的下一个原型，同时提出 M01 原始事件规范化的独立检查方案。每轮完成真实 GitHub 版本提交和同步状态核验，不能只在聊天中宣布完成。

## 8. P2.5 高价值方法筛选：C02 与 C05 进入局部 P3；C01 延后完整资金图（2026-10-31）

**变更动作**：`AMEND`，补充现有 C01/C02/C05 的事件契约、反例与分阶段实现顺序；未创设新领域。此前 C01/C02/C05 均为“A研究”，现在按数据可得性与最小实现性区分。属于**机制推断+监控设计候选**；没有在本轮取得真实 K2 市场样本，**不能称已验证的监控规律**。

### 8.1 候选筛选与实际新增能力

| 候选 | 现有 M01–M05 未覆盖的新能力 | 最小可观测字段/前提 | 关键竞争解释 | 本次决定 |
|---|---|---|---|---|
| **C01 跨币资本再部署** | 把 Mint A 的退出和 Mint B 的进入以**有时间顺序的同资产路径及余额可行性**关联，而不止统计跨币重复钱包 | A 的卖出经济事件、实际收到的 quote asset、SOL/WSOL转换、转账 source→dest、余额、slot、signature、`available_at`、B 的买入经济事件 | 高活跃公共Hub、交易所/托管路由、收款前余额足够支持B、混合资金、非同控制 | **保留重要候选；暂不直接建完整资金追踪**。先以1–2跳无公共Hub的正反例探索，依赖 M03/原始解析器 |
| **C02 同群体执行切换** | 比较**同一既有钱包集合**在不同Mint、不同发行阶段的资金到账→首买等待分布、买入拆单、参与比例和退出路径；寻找扣除市场环境后的改变 | 截止观察时刻冻结的组成员、各Mint首次可交易时刻/阶段、钱包收款、首Swap、报价金额、池深/成交活跃、已知机会、`available_at` | 不同币龄、池深、费用、路由、市场拥堵、机会选择偏差及群体按未来信息定义 | **首选进入局部 P3 设计**，先做可复核的跨币行为比较，不做收益预测 |
| **C05 既有行为沉默与迁移** | 从仅按时间检测“少交易”升级为按**符合条件的交易机会数量**检测“有机会却未参与”，再检查其他币/venue活动 | 群体历史行为基准、可交易Mint/venue候选列表、发行阶段、数据完整水位、参与事件、匹配机会数量、时间与来源 | 市场整体无机会、协议不可交易、采集断流、地址群已过期/被重新定义、服务停机 | **第二项进入局部 P3 设计**，先完成机会分母和 UNKNOWN 状态，再研究迁移 |

### 8.2 C01 必须增加“资金可行性”，不能把图连通性当资本身份

观察序列 `SELL(Mint A) → quote asset收到 → 中间地址F → 分发 → BUY(Mint B)` 仅能确认相应链上事件；必须检查：

1. **同资产及单位**：卖出所得是 SOL、WSOL还是其他 SPL？手续费、租金、WSOL wrap/unwrap 分开，不把代币转仓视为已卖出。
2. **时间次序与可得性**：中间每条边真实发生且 `available_at` 在声称检测时刻之前；同时记录不同节点交易是否为已确认/最终化。
3. **金额和历史余额可行性**：中间地址在接收 A 的退出款之前是否已拥有足以支持 B 分发的余额？若是，只能说存在可行资金路径，不能说 A 唯一资助 B。
4. **混合与公共Hub排除**：混合入账或高频公共地址应降低解释强度，必要时仅输出 `PATH_OBSERVED_SOURCE_UNRESOLVED`。

**仍不可直接得出的结论**：同一笔可替代 SOL 被“精确追踪”、同一控制人、庄家、可盈利跟单。

### 8.3 C02 从“同组重复出现”转成“环境匹配的行为变化”

**时间截断**：在比较 Mint B 前，固定钱包群体的定义和所掌握的地址关系；不能事后用 B 的买入倒推“当时已知是同一群”。若需要探索性事后分组，明确标 `RETROSPECTIVE_CLUSTER`，不得作为提前可发现信号。

**最小比较向量**（都标注有效样本量和不可观测比例）：
- `funding_to_first_swap_seconds`：收款至首次相关 Swap；未在观察截止前交易者右删失，不能填入无限或零。
- `participation_rate`：已知符合比较条件的群体地址中，有多少实际参与；初始群体及条件必须前置冻结。
- `ticket_size_distribution`：报价资产与 decimals 统一后，比较中位数/分散程度；不同报价资产不能直接相加。
- `buy_batching / exit_route`：拆单与卖出/转仓/归集应保留不同事件类型。
- `context`：发行到交易的币龄、曲线/迁移/AMM阶段、池深、市场活跃度、网络拥堵及程序/路由。

**最小反证**：用同一阶段和类似活跃度的其他钱包群/代币作为正常对照；若差异由阶段或池深解释，则本项不升为异常监控规则。

### 8.4 C05 新增关键分母：交易机会和完整观察

不能把“过去每小时交易 10 次、现在 0 次”直接当成群体停机或迁移。先定义用户希望观察的**机会**：例如既定协议、既定币龄与流动性范围内，满足群体过往参与条件的发行/交易机会。这个定义必须在观察未来行为之前固定。

- `eligible_opportunities`：比较窗口内有效、符合条件且已被完整采集的机会数。
- `participated_opportunities`：群体至少一个已知成员发生定义内的合格交易的机会数。
- `participation_rate = participated / eligible`：仅在 `eligible > 0` 且数据覆盖完整时有意义。
- `NO_OPPORTUNITY`：没有足够合格机会，**不是行为沉默**。
- `COVERAGE_UNKNOWN`：索引、RPC 或解析有缺口，**不能把未知当0**。
- `ELIGIBLE_BUT_INACTIVE`：机会存在且观察完整，但未检测到原有行为；**是研究候选，不是证明迁移**。
- `ALTERNATIVE_ACTIVITY_OBSERVED`：同时观察到该群体在其他Mint/venue的行为，需再检查资金/角色联系，不能直接宣称转移控制。

最小对照：同日类似钱包群参与率、相同机会集合上的其他群体行为，以及该群体历史上也未参与类似机会的负例。比“无交易时长”更有用的是**有机会但活动方式改变**。

### 8.5 进一步新发现：不只找重复，还要找条件改变后的反常表现

结合 C02/C05，可提出更有价值的研究问题：

> 在环境相近、交易机会可用、资金准备程度相近的条件下，同一群体原有的“融资→执行”模式为何开始缩短、停顿或换到另一个Venue？

这是一项跨组、跨币、跨时间的**条件对照**，而非声称新增“第17个异常信号”。对比中优先保存不同结果和反例，不把所有相似结构推成同控。保留 `OBSERVATIONAL_CANDIDATE` 状态。

### 8.6 与工程和后续知识的交接

- **M01 仍限 fixture-only**；已实现1/5/15分钟成员演化、描述性三种候选，14项新增离线测试及 GitHub CI 通过，见 Draft PR #16。不得称其可以直接处理 Solana 原始 `getTransaction` 或证明跨币方法。
- **P3-C02**：复用 M01 按 Mint/owner 的统计结果，新增按群体/发行阶段/机会匹配的跨 Mint 对比设计；先不自动贴“同控/庄家”标签。
- **P3-C05**：从离线的发行/机会清单与已知群体观察记录开始，完成分母、覆盖水位和缺失数据状态机；不要先做全市场告警。
- **P3-M01 原始解析器**：必须先解决账户索引及 LUT、outer/inner CPI、Token 与 Token-2022、TokenAccount/owner/fee payer区分、Swap经济动作归并、quote资产、WSOL/费用及可证明完整的窗口采集。详细审计在 PR #16 的 `docs/p24-m01-crossmint-research.md`。
- **升级条件**：P2.5 的筛选/交接目标已达成；下一阶段重点为局部 P3 接口设计+最小验证，P4 仍保留样本、误报与预测能力独立检验。生产策略/下单未授权。

**引用的规范来源**：
- Solana 交易数据和 CPI：[RPC JSON Structures](https://solana.com/docs/rpc/json-structures)、[Transaction Introspection](https://solana.com/docs/core/transactions/transaction-introspection)、[getTransaction](https://solana.com/docs/rpc/http/gettransaction)。
- TokenAccount、owner、ATA：[Tokens](https://solana.com/docs/tokens)；特殊代币行为：[Transfer Fees](https://solana.com/docs/tokens/extensions/transfer-fees)、[Transfer Hook](https://solana.com/docs/tokens/extensions/transfer-hook)、[Confidential Balances](https://solana.com/docs/tokens/extensions/confidential-transfer)。
- 现有实证与失败边界：参考仓库 `coordination_detection`、`funder_network`、`sniper_capital`；只把其当作外部报告与方法参照，**未在本轮重新计算原始样本**。
## 9. 局部 P3-M01：原始交易适配器实际实现与新的条件（2026-10-31）

**变更动作：AMEND 本专题原有 M01 工程交接，不新增“异常识别方法”或平行框架。**

1. **新增程序能力（fixture-tested）**：Draft [PR #16](https://github.com/sunshihao001/grok/pull/16) 的 `src/solana_meme_os/raw_tx_adapter.py` 可从**本地保存、人工标记为 fixture** 的 Solana `getTransaction` 形状 JSON 解析一组有限原语：顶层 System SOL 转账、顶层 SPL Token/Token-2022 Transfer/TransferChecked，保留签名、Slot、链上时间、提供者可得时间、token account 的 owner、authority 和 fee payer 的区别；对部分 `json` 编译交易解析 v0 静态账户 + `meta.loadedAddresses` 及已核实固定指令布局。规范与边界见 PR #16 的 `docs/p3-m01-raw-adapter-contract.md`。
2. **新增反例与错误处理**：Token CPI Transfer ≠ 独立 Swap；System CPI Transfer ≠ 用户充值；Token Account owner ≠ Fee payer/Delegate；WSOL wrap/unwrap、Token-2022 fee/hook 扩展、复杂 DEX/Router 协议、缺失元数据/地址映射均不能强推 BUY/SELL。对未知/无时点信息采用 fail-closed，不能由 Token 余额正负凭空生成买卖信号。Solana 官方 Token-2022 程序地址已按[官方 Token Programs](https://solana.com/docs/payments/how-payments-work)核对，源码防止填写错误 ID。
3. **测试边界**：适配器新增 **24项**离线单测，与既有 M01 的14项合计**38项**通过；本地已把原始形状 fixture → 适配器 → M01 串联跑通。它证明合成输入下的部分解析行为，不代表真实签名已逐笔验证、全部 Mint 事件已覆盖或实现 DEX 买卖语义。远端 GitHub CI 状态须以最新提交的实际工作流为准。
4. **C02 最小契约修正**：M01 窗口 JSON 只保留钱包人数，没有可复用的预冻结成员列表；若要跨 Mint 比较同一群体，必须从**历史时点冻结的地址集合＋原始标准化经济动作流**读取，不能从聚合计数恢复成员，更不能事后按谁买入成功定义群体。未执行钱包使用右删失而不是零延迟。
5. **C05 最小契约修正**：`NO_OPPORTUNITY`、`COVERAGE_UNKNOWN`、`ELIGIBLE_BUT_INACTIVE` 的区分依赖**独立机会索引和经证明的完整性**，一个交易回包或用户传入的 `coverage.complete=true` 无法证明全链零交易。C02/C05 目前只有工程数据契约及对抗性模拟场景，不是已实现的两个运行监控器。

**下轮能力交接**：在仍保持 fixture-only 的前提下，优先挑选少量官方原始交易或可核验公开签名，人工标注 Token owner、转账、复杂 CPI/Swap 的正确结果，然后与适配器逐条对账。复杂 DEX 优先参考 Solana 官方 `@solana/transaction-introspection` 及协议原始源码，避免自行推断链上复杂经济动作。尚不具备生产全链采集或 P4 大规模实证门槛。


### 9.1 公开 Solana RPC 样本与新的工程错误反证（2026-10-31）

**AMEND 原有 M01 条目；不是新的异常名称。** 见 [工程 PR #16 适配器契约](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)。

- **外部原始样本**：官方 Solana [getTransaction 文档源码固定版本](https://github.com/solana-foundation/solana-com/blob/4cb392f61c2ab0f8953cc314378aaf8256b7699a/apps/docs/content/docs/en/rpc/http/gettransaction.mdx) 提供两笔 Devnet 公开交易响应：legacy 直接 System SOL 转账（签名 `4ReKprwf…`，Slot 423108383，1 SOL）及 v0 ATA 账户创建（签名 `56rgv1Fq…`，Slot 423118809，含4条 inner CPI，postTokenBalance 为零）。后一笔的 `json`/`jsonParsed` 是**同一笔签名**的两种编码。本项目在PR #16保存三份原始格式记录、7项回归测试；CI通过。**仅代表官方已发布的 RPC 回包格式，不是本项目实时从独立节点重拉**。
- **支持与未知**：legacy 顶层 SOL Transfer 被正确列为单独的原生资金转移，未记目标 Mint BUY；ATA 创建暂不能完整分类，保守输出 `UNRESOLVED/INCOMPLETE`，无假买入。既不能把 CPI/租金记为Swap，也不能把“无解码事件”称为“没有市场活动”。官方文档没有 `available_at`，回归测试注入的该字段是**合成**，不能作为历史预警时点。
- **实际修正一：交易执行状态**。原代码若 `meta.err` 完全缺失，将其与 `err:null` 混为成功；现在必须检查字段存在，否则 `TRANSACTION_STATUS_UNKNOWN` 并阻止所有经济事件输出。
- **实际修正二：决策时点的数据泄漏**。原代码在生成 `funding_events` 后才检查 `available_at>as_of`，可能将未来才知道的融资事实输出给 C02。现在将时点判断提前到解析前，未来信息只记录 `EVIDENCE_ARRIVED_AFTER_AS_OF` 与 `INCOMPLETE`，不得进入资金事件/交易事件。
- **Token-2022 精度/权限边界**：[Transfer Fee](https://solana.com/docs/tokens/extensions/transfer-fees) 的指令转账毛额不等于净到账；[Transfer Hook](https://solana.com/docs/tokens/extensions/transfer-hook) 触发额外 CPI；[Confidential Balance](https://solana.com/docs/tokens/extensions/confidential-transfer) 可使真实金额不可见。保留 `gross/fee/net/UNKNOWN` 的区分，不把未知填零，也不声称已完整支持这些扩展。
- **交易格式与采集风险**：[v1](https://solana.com/docs/core/transactions/versioned-transactions) 若 RPC 调用没有 `maxSupportedTransactionVersion: 1`，可能导致 `getBlock` 整个响应失败；读取失败≠空区块。当前适配器仍只支持 legacy/v0，v1 输出明确不支持。C05 的“有机会未参与”需要独立的区块/机会覆盖水位，不能以两笔RPC样本或 fixture.complete 为证据。
- **工程验收**：该 PR 的6个测试文件现共定义71个 `unittest.test_*` 方法，最新 [monitor-tests CI](https://github.com/sunshihao001/grok/actions/runs/41216119575) 成功；这些是离线合同和来源格式回归测试，不是71个真实市场样本。协议级 BUY/SELL 与独立重拉真实RPC仍未完成。

**知识影响**：D01（指令、token、版本）、D05/D07（资金与群体）、D10（可得时间和缺失数据）、D11（误判和反证）。对 C02/C05 最重要的不是添加一个新钱包标签，而是确保状态未知、资金证据在当时可得和“整块数据缺失”不会伪装成零交易。下一步集中完成独立只读RPC签名对账和**一个**有官方IDL/源码支持的 Meme 协议Swap语义，不强行扩展全链。
