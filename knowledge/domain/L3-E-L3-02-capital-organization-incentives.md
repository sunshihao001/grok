# E-L3-02 资金溯源专家纵深研究｜一笔资金背后，到底是谁在做什么生意？

> **专家角色**：现有 E-L3-02「资金溯源与经济主体取证」，L3/D05 主导，按需联动 D01、D02、D03、D04、D06、D07、D08、D09。不是新增专家。  
> **正确阅读顺序**：先读本文中的专家追问和机制推演，再按问题阅读 [L3 专家研究台](L3-actor-expert-perspectives.md) 及 [经济主体原理底稿](L3-actor-economic-mechanisms-deepstudy.md)。  
> **研究边界**：本篇讨论可由协议权利、成本约束和市场机制推导出的知识，以及尚未实证的竞争假说。所有“设想/如果”都是**构造情境**，不是某个真实 Mint 的经历、已观测资金流或被证实的获利手法。没有实测阈值、资金归属真相或可直接发布的跟单规则。

## 专家先给一个不同的判断

“看到一条资金转账，我不会先问它是不是庄家。我先问：**这笔钱在整个生意里承担什么职责？由谁承担最终损失？谁有权决定它变成 Token，谁又可以从成交中拿走收入？**”

传统链上跟踪容易停在这三层：`地址 A → 给 B 转账 → B 早期买币`。这只能证明链上的转账与交易顺序。真正的经济研究要追到第四层：

**原始资金 → 可行使的权利 → 风险库存与现金流 → 市场行为激励 → 他人进入后的经济结果**。

如果不知道一笔钱到底是交易本金、执行费、服务结算、LP 流动性、平台分润还是托管资产，再漂亮的聚类图也可能把五种不同生意误认为一种“控盘”。

## 1｜第一次追问：同一笔 SOL，究竟承担哪一种经济职能？

“F 先给若干地址打款”是**链上动作**；以下才是专家真正关心的**生意用途**。

| 资金职能 | 资金之后可能做什么 | 参与者真正赚/亏什么 | 单纯同源图的典型误判 |
|---|---|---|---|
| 风险本金（principal capital） | 兑换 Token、承担价格波动、平仓回收报价资产 | Token 敞口的净盈亏 | 将资金提供者直接当成最终控制者 |
| 执行预算（execution sponsorship） | 付 base/priority fee、Jito tip、ATA 租金、失败交易费用 | 交易服务费、执行补贴或平台运营成本 | 费用支付者被误认为买入决策者 |
| 托管与归集（custody/settlement） | 用户入金、内部账户归集、统一链上提款 | 托管/结算收入，经济敞口可能属于用户 | 许多客户被画成一位“巨鲸” |
| LP 资本（liquidity provision） | 向池子投入两种资产、持有可赎回的 LP 权利 | 手续费、库存再平衡与无常损失等风险 | LP Vault 大额持仓被当作可自由砸盘的私钱包 |
| 发行/创建者收入（creator/protocol fees） | 根据可用池配置收取成交活动产生的费用 | 费收及分配，与 Token 持仓收益可以分离 | Dev 清仓被解释为不再有经济利益 |
| 运营返佣与服务收入（revenue sharing） | 机器人、发行工具、市场运营服务收取费用 | 服务收入扣成本，可能与币价不一致 | 多地址按周期回流被当作所有钱包共控 |

专家深挖时**不按地址永久赋予职能**：F 上午可能提供执行补款，下午也可能出资承担头寸，某个地址既可能是费用收款人又是交易员。职能应当限定 `事件 × Mint × 阶段 × 时间`，同一节点的不同边还可能具有不同经济意义。

### 专家发现的第一个隐藏机制：资金组织不必等于交易组织

如果 F 提供手续费、机器人服务提供策略执行、A/B/C 由不同用户实际承担仓位风险，那么三者的交易路径可以高度相似，**但三个用户并不必然共享买卖意图或收益**。

反过来，一个实际决策者可以使用多个资金入口、不同执行服务和独立收款地址，使简单的同源聚类完全失灵。

这两种组织结构在链上可能呈现相反的“聚类信号”，却都无法仅凭表面热度解释。

**新认知**：`same_funder` 测到的是一种资金关系；`same_executor` 测到的是执行关系；`same_authority` 只涉及特定协议授权；`same_beneficiary` 涉及最终利益。四者不能混成一个“关联度”。

## 2｜第二次追问：谁能移动 Token，谁承担亏损，Solana 上是否可见？

“看起来控制钱包”的人可能只有**执行权**，未必拥有资产收益；另一方面，一个实际受益人也可能把执行权限完全委托出去。

Solana 的几种具体机制正好展示这种分离：

**Token Account owner**：账户里保存一个授权 owner，可控制相应 Token Account 的转移；同一个 wallet 对同 Mint 可以有多个 Token Account。它与链上程序账户的 `program owner` 不是一个概念。[Solana Tokens](https://solana.com/docs/tokens)。

**ATA 的 payer**：别人可以为某 owner 创建/支付 ATA 的账户开销；`payer` 并不因此拥有该 Token Account 或成为被创建账户的最终受益人。[Create Token Account](https://solana.com/docs/tokens/basics/create-token-account)。

**Delegate**：Token Account owner 可批准另一个账户在授权额度内进行转移。这证明“一个地址可以操作另一地址的 Token”，但不证明双方具有同一终极受益人。[Spend Permissions](https://solana.com/docs/payments/advanced-payments/spend-permissions)。

**PDA**：可以由拥有正确种子的程序使用 CPI 代签。PDA 控制的资产与某个人类热钱包不是同一种节点。[Solana CPI](https://solana.com/docs/core/cpi)。

**Token-2022 Permanent Delegate**：某些 Mint 允许设置 Mint 级的永久代理权，可对该 Mint 的各 Token Account 授权转移或销毁，普通账户 owner 无法单独撤销。这意味着即使一个小钱包的 owner 完全独立，也不必然拥有排他的库存处分权；必须先确认 Token Program 和扩展是否启用。[Permanent Delegate](https://solana.com/docs/tokens/extensions/permanent-delegate)。

**手续费 payer**：Solana 交易的 fee payer 承担交易费，即使执行失败仍可能付费；它既不是自动的 Token 交易对手，也不是最终经济盈亏的身份证明。[Fee Structure](https://solana.com/docs/core/fees/fee-structure)。

### 专家由此推导的真正问题

以前的资金结构常问“这 20 个地址是不是一个人”；现在更重要的问题是：

- 这 20 个 Token Account 对应几个不同的 owner 或 PDA？
- 同一个 Token 是否受其他 delegate 或 Mint 级特殊权限约束？
- 参与者实际承担的是 Token 价格风险、LP 库存风险，还是只有固定执行成本？
- 是否存在**共同执行权但不同受益权**，或者**不同执行权但同一受益权**？

如果受益人与资金委托合同存在链下，公开账本可能根本无法唯一还原。专家必须承认**不可识别性**；不能拿一套人工设计的概率替代缺失事实。

## 3｜第三次追问：同一张资金图，能不能对应完全不同的“真实世界”？

设想：F 先给 A、B、C 充值，三者在某 Mint 开盘后相继换入 Token，之后部分资产沿某些地址回到 F。

**世界 A｜一个资本管理者在组织多个执行钱包**。F 管理本金，A/B/C 分批承担风险，退出后的部分资产归集后准备下次交易。其经济本质可能是“统一库存与资金周转”。

**世界 B｜一个公共出金/托管机构服务多个客户**。A/B/C 是独立决策者；F 既提供链上出金也可能接收客户充值。图上的回流可能是客户提现或平台结算。其经济本质是“许多独立风险主体共享结算”。

**世界 C｜交易工具商提供账户执行和费用代付**。A/B/C 的签名、时间、费用配置和路由非常相似，但实际风险属于不同客户；回到 F 的资金可能是服务费而非交易利润。其经济本质是“统一执行软件，不统一投资意图”。

**世界 D｜发行工具、LP 或费用收款网络**。F 的部分边不是本金，而是流动性注入、创建成本或费用分配。其经济本质是“交易基础设施和手续费收入”，与统一买入、拉盘并不是一个模型。

只要公开记录没有识别最终出资协议或受益分配，**同一组链上交易可以与多个经济结构相容**。这不是分析不够努力，而是原始记录没有包含所有链下关系。

### 什么样的新知识才能真正区分它们？

资金专家不再满足于“跨币观察一下”这类空泛建议，而是为每个世界追问**其经济组织必须持续解决的难题**：

- **统一资本管理**，必须分配有限风险预算：A/B/C 的新增仓位和外部回款能否被一个相对稳定的资金周转体系解释？是否出现跨多个 Mint 的资金归集与再配置？
- **公共托管服务**，必须处理大量无关用户的提款与充值：同一 F 在不同时间和不相关交易活动中是否承担广泛的资金服务职责？为什么其客户策略可能高度多样？
- **统一执行软件**，主要需要支付手续费、维持账户与获得客户指令：小额执行预算、同构指令和服务收入能否解释这些相似性，而不需要假设共享本金？
- **费用收取网络**，必须能在协议配置中取得收费权：手续费计提账户、收取指令、权利变更和 LP/协议分成是否提供了另外一套完全不同的解释？

这套追问的目的是识别**经济职责的必要约束**。不能因为某世界更符合直觉就强行给出“置信度 95%”。

## 4｜第四次追问：一组钱包的资产流动，是否真的创造了新增需求？

这里需要从“资金图”跨入**经济账本**。

设我们暂时把一组地址作为**待证实的经济群体 G**。以同一种资产为单位：

- G 内部从 A 转到 B 的 Token，只改变地址持有，不增加 G 的 Token 总库存；
- G 内部从 B 转到 C 的 SOL，只改变支付位置，不使 G 拥有更多 SOL；
- G 经由池子用 SOL 换取 Token，会增加 G 的 Token 风险敞口，并向池子提供报价储备；
- G 作为 LP 注入/赎回，会改变可用流动性及 LP 权利，而不是普通意义的方向性买入。

**关键区别**：内部转账在合并的“群体账本”中应当相互抵消。但因为群体 G 的边界本身可能错误，群体层面的净敞口只是一种**条件性计算**，不能把模型输出误当成已经证实的真正控盘比例。

### 看上去高成交，为什么可能没有相应的新增风险资本？

一个很活跃的参与者反复用 SOL 买入 Token、再卖回 SOL，会创造累计成交额；但在一定时间后其净 Token 库存可能接近原点。

另一个可能是多个独立长期持有人只买入而很少交易：累计成交额可能不如前者，却代表较持久的风险承担。

因此：

`累计成交额`、`净 Token 持仓变化`、`独立资本新入场`、`池中新增可用 SOL`、`最终可卖价值` 是**五个不同对象**。

**但不要进一步跳过一个关键限制**：Solana AMM swap 通常是钱包与池交互，不能用“一买一卖相抵”证明两位钱包之间已经在链上构成直接自成交；高换手既可能是套利、库存管理，也可能是其他行为。缺乏交易对手主体证据时，只能讨论 wash-like 候选。

### 重要的专业新问题：真正的“吸筹”要回答谁愿意继续承担库存风险

如果一个被称为“聪明钱群”的地址集合长期净增 Token，仍有三种可能：

1. 多个独立投资者确实在承担新风险；
2. 一个管理者拆分地址、集中承担相同风险；
3. 其他受益人把 Token 托管给这些地址，链上库存增加但经济风险主体未变化。

所以“吸筹”不能只等于一段时间内 Token 转入量大。专业知识要解释的是：**谁以什么对价承担了新增风险，风险从谁转向谁，后来者需要什么条件才有退出承接**。

## 5｜第五次追问：有些参与者赚钱，根本不需要 Token 上涨

这是原“Dev 清仓/持仓集中/巨鲸行为”三类知识很容易共同遗漏的部分。

### 不同参与者的收益函数

**方向性交易者**：收益大体来自持仓卖出所得减买入成本与费用，关键是入场成本、最终卖出容量与价格变化。

**流动性提供者**：收入可能来自交易费，承担池中两资产库存再平衡、价格偏离和流动性机会成本。在传统 CPMM 中，LP 与单纯持币的收益路径不同；不能把池里 Token 当作 LP 的单向看涨仓位。

**发行者/创建者**：在**允许并启用 creator fee 的具体池**中，可能通过交易活动获得独立于持币上涨的费收；净收益还受到平台/协议分成、发行和运营成本约束。

**机器人/交易服务商**：可以从服务费、执行费或其他合同收入中获益，其客户却承担 Token 方向性风险；独立执行结构可能在链上看似一个“团队”。

**协议和验证者**：可获得自身费用/奖励份额，其业务目标与散户的币价收益不是同一函数。

**研究升级**：一个币“交易热度高”，对不同主体可能产生完全相反的经济结果：LP 和收费方可能有业务收入，短线交易者承担换手成本，方向性持有人承担价格与退出风险。**同一市场现象不等于共同盈利方向**。

### 一手协议细节：Raydium CPMM 费用如何改变创建者的激励

Raydium 官方文档在 CPMM 中将 `trade_fee` 与**可选**的 `creator_fee` 分别计提。Trade fee 可分配给 LP、协议和基金；Creator fee 只有池启用时才生效，且有单独的费用计提、收取与可能的协议分享安排。费率在配置账户中，单位和费分成的分母不同；必须按池配置、版本和交易方向计算，不可从“这币在 Raydium”推断一定存在创建者费。[Raydium CPMM Fees](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/fees.mdx)、[CPMM Math](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/math.mdx)。

据此可以得出**条件性知识结论**：

- 如果创建者有实际可收取的 fee entitlement，`creator_hold_rate = 0` **不能**推出“没有任何经济获利渠道”；
- 如果池子没有启用对应配置，不能凭“创建者理论上能收手续费”就推断其确实拿到费；
- 成交额增加可能带来更多**毛费收**，但不直接证明**净利润**增加；
- 创建者若为了制造交易量而自己承担全部买卖费用、滑点与交易成本，可能亏损。**有收费权绝不等于自刷交易量有利可图**；需要独立核算全部成本与可回收的费用份额。

**交给 E-L3-04 的问题**：一个开发者在 Token 清仓后，是否仍可能有 LP、协议费、creator fee、委托或其他可核实的经济权利？哪些权利随毕业/迁移变化？这比“Dev 已经清仓所以安全”的单标签判断深入得多。

## 6｜第六次追问：领先钱包买入，不是静态信号，而是在改变后来者的交易价格

这是资金专家必须主动请 E-L2-02（AMM 价格机制）和 E-L4-02（跟单优势）进行交叉推演的地方。

### 一个纯理论的 CPMM 思维实验（不是某枚币的数据）

假设一个**无费、无套利、储备不变、单一传统恒定乘积 AMM**：

- 池有 (X=1,000,000) 枚 Token，(Y=100) SOL，(XY=k)；
- 最初边际价格为 `100 / 1,000,000 = 0.0001 SOL/Token`；
- 领先钱包先用 10 SOL 买入；
- 看到领先钱包动作的跟随者再用同样 10 SOL 买入。

按恒定乘积的理想买入公式：

`Token_out = X × quote_in / (Y + quote_in)`。

领先钱包得到约 **90,909 枚 Token**。它成交后，池子只剩约 909,091 Token 和 110 SOL；边际价格已升至约 **0.000121 SOL/Token**，比最初高 21%。

第二位跟随者的同样 10 SOL，只能得到约 **75,758 枚 Token**；相较于领先者**少约 16.7% 的 Token**，平均买入成本则高约 **20%**。两笔买入结束后池子约剩 833,333 Token 与 120 SOL，边际价格为 **0.000144 SOL/Token**。

这些数字是**模型中必然的库存和价格关系**，不代表 2026 年某个具体 Raydium/Launchpad 池的实际报价。现实中手续费、路由、虚拟储备、CLMM/曲线模式、套利、LP 增减及排序都会改变结果。Raydium CPMM 的真实费用分桶还需按其版本和配置处理。[Raydium CPMM Math](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/math.mdx)。

### 真正应该由专家追问的，是这段模型背后的资金关系

1. 原钱包的买入**先改变了价格**，跟随者之后才看到它；因此“原钱包的买入成本”不是跟随者可取得的成本。
2. 跟随者自己的买入**进一步改变池子储备**；他不是在交易发生后被动领取同一个收益，而是在参与改变市场状态。
3. 如果领先钱包随后卖出，其可卖报价可能受到后来买盘改变；**跟随者买入有可能改善早期持币人的卖出条件**，但不能据此断言原钱包有意诱导别人当接盘者。
4. 只靠更多跟随者互相推高价格，并不能证明存在持续的外部资金承接；最终还要面对真实的独立退出需求和池深度。
5. 在无费且没有任何其他状态变动的理想模型里，同一笔买入立即按相反方向完整卖回，理论上可以恢复原状态、收回原投入；**不能把单次买卖的报价冲击误写成无费模型必然产生单笔往返净亏**。现实中费用、时间差、套利和竞争交易才会使往返结果发生变化。

**真正的跟单深度问题**因此改变了：

不是“这个钱包有没有 Alpha”，而是——**它的 Alpha 有多少来自领先成交本身造成的价格优势？在我们得知它已经买入时，池子、其他追随者、它的剩余库存和未来独立需求还能怎样共同影响我们的盈亏？**

这甚至可以让专家提出一个不常见但合理的研究方向：**钱包信号的价值可能随监控它的人变多而内生衰减**。这是从 AMM 定价和关注度传播推导的**可研究机制**，并非已被证明的普遍经验规律。

## 7｜第七次追问：为什么“同一时间买”不足以揭示同一资金计划？

E-L3-05 会提出一个反击：一批地址在 Mint 开盘后近同时买入，很可能是**共同公开事件**驱动。

### 同步共因与同一决策是两种完全不同的因果结构

**共同事件模式**：

`公开 Mint / 曲线开放 / 榜单更新` → 多个独立机器人同时观察 → 相似时间买入 → 处于同一价格曲线上，所以成本也接近。

**共同资本模式**：

`同一资金预算与决策` → 分配到多个执行钱包 → 分批或同步买入 → 后续可能出现统一风险控制/资金回收。

**共享执行软件模式**：

`同一机器人服务` → 多用户按相同模板执行 → 相似金额/路由/手续费 → 不必共享最终受益。

同样的“近同时、近同价、同程序”可以由三套不同的因果路径产生。所谓“三项特征吻合”可能只是一个共同原因的三次投影，不能将它们当作三份独立证据相乘。

### Solana 与 Jito 对时序解释的专业限制

Solana 交易可以包含多条外层指令与 CPI；RPC 返回的 `innerInstructions`、`preTokenBalances`、`postTokenBalances`、`fee`、`loadedAddresses` 等有特定 schema，不同编码模式还会影响字段可用性。[Solana RPC JSON Structures](https://solana.com/docs/rpc/json-structures)。

Jito bundles 可由最多五笔交易组成，按序原子执行，并按账户锁冲突和出价竞争。这证明**不同执行者可以协调提交**，但“在同一个 slot”并不是“在同一个 bundle”；即使确为同一 bundle，也不能直接证明所有最终受益人相同。[Jito Low Latency](https://docs.jito.wtf/lowlatencytxnsend/)。

一个经济组织在链上的行动时点，还需要与服务商 `first_received`、本方 `available_at` 和决策时点分开。

**时序专家真正提出的问题**：这批地址的相似性是在控制公开事件和执行服务之后仍然存在，还是只是共享同一“新闻与开盘时钟”？

## 8｜四位专家分别挑战资金专家，才能让知识继续向下生长

### 挑战 A｜E-L3-01 钱包行为专家：“你说资金统一，那么它们承担的风险真的统一吗？”

资金专家看到 F 反复补款；钱包专家发现其中一些地址只维持手续费，有些地址短时买卖后归零，有些地址长时间持仓。**同一个上游资金节点下面可能有多种商业职能**。

**深入后的新问题**：哪些钱包是真正的风险账户？哪些只是操作/路由账户？一个地址高 PnL 是属于执行服务的技术能力，还是属于投资主体的策略选择？

### 挑战 B｜E-L3-03 筹码专家：“就算是一个资本管理者，凭什么说它能够控盘？”

资金统一不自动等于价格控制。持有 Token 库存、控制 LP 权利、控制 Mint/Delegate 授权、在薄池对边际价格有较强冲击，是不同的**市场影响通道**。

**深入后的新问题**：它拥有多大可处分库存；当前及可能变化的池储备承受得住多大交易；如果没有独立买方，它的账面财富转成 SOL 会发生什么？

### 挑战 C｜E-L3-04 开发者专家：“你一直找 Token 收益，有没有漏掉手续费权益？”

当某些池可配置 creator fee，Dev 清仓未必意味着经济关系已经切断；LP 份额、发行/运营服务、费用收款人也可能是持续收入源。反之，没有协议或链上收款证据，不能凭开发者标签推定存在此收入。

**深入后的新问题**：一个主体的目标函数到底是 Token 升值、交易额、LP 收费、服务客户，还是这些收入的组合？不同目标可能导致不同的行为时间线。

### 挑战 D｜E-L2-02 × E-L4-02 市场与跟单专家：“你找到组织了，但后来者为什么能赚钱？”

一个资金组织即使真实存在，也可能只证明**它过去如何买入**。从原钱包成交到跟随者收到信号之间，池子储备、竞争订单、外部套利及流动性已经变动。跟随者还可能面临不同出售成本。

**深入后的新问题**：我们观察到的信号究竟是一次**先前已完成的交易优势**，还是揭示了一个**尚未完全发生的后续市场阶段**？只有后者才有机会成为新的可复制研究假设。

## 9｜五条比“发现庄家”更深、但尚未验证的研究命题

### 命题 1｜服务节点越中心化，经济主体识别可能越困难

直觉上，找到共同源头似乎更确定；但当源头是广泛服务于不相关客户的 HUB，关联路径反而越缺乏对共同控制的区分力。**节点中心度不是控制概率**。

**竞争解释**：少数真实资本管理者也可能使用高度中心化的资金主节点。必须理解该节点的全部业务职能。

### 命题 2｜资金循环的“回收权”可能比一次出资关系更揭示组织方式

一次付费/充值很容易由公共服务解释；重复的本金分配与残余资产回收，在某些条件下更符合资本组织的持续周转。

**竞争解释**：托管结算与机器人服务费也会反复回收，且未必共享风险资本。跨 Mint 的周转模式只能增强机制解释，不提供私人身份的确定证据。

### 命题 3｜市场上存在“赚成交额的钱”和“赚币价的钱”两套激励

某些 LP/协议/创建者/服务商可以从交易活动得到收入，方向性持币者则依赖价格与可卖性。这些激励可以不同步。

**竞争解释**：创建者费可能未启用、收费权已经变更或成本大于收益；不能把毛费收推定净盈利。

### 命题 4｜同一批钱包的表面利润不能自动归属同一个经济主体

同一出资/执行服务背后可以有多位最终受益者；多个不同地址也可能由一个主体承担盈亏。把地址 PnL 简单求和可能重复计账、漏费用或错误归属。

**竞争解释**：若所有资产权利和资金回收均在公开链上，某些群体的内部净额确实可更完整地重建，但仍不等于身份验证。

### 命题 5｜领先者留下的不是固定“买入信号”，而是一个变化中的经济状态

先买者影响 AMM 储备，后来者也改变先买者的潜在退出条件。公开跟单行为可能反过来影响领先者的卖出环境。因此跟单策略研究需要把**信息传播和交易价格的内生变化**一起思考。

**竞争解释**：持续独立新增需求也可能使后续进入有利；不应把每个领先买入都解释为诱多。

## 10｜专家如何判断自己的研究已经触及深处？

不是看写了多少页，也不是看提出几个假设；而是看看能否给出**不同经济机制会导致的不同后果**。

对于“F 给多个钱包打款、一起买新币”：

- **只会说同源不一定同控**：仍停留在谨慎提示。
- **能拆解本金/手续费/托管/LP/费收**：开始识别不同业务。
- **能解释 Solana 的 Token owner、delegate、PDA、payer 与经济受益为什么分离**：已经理解链上权限与市场主体的错位。
- **能为不同经济组织指出其持续运营的约束和现金流路径**：开始具备真正的资金取证逻辑。
- **能解释这些组织如何改变 Token 风险敞口、池子储备、成交量与其他人的收益空间**：进入市场机制层面的知识。
- **能推导其他专家没有直接提出的交叉机制，并同时指出什么条件会使推导失效**：才称得上深入研究，而不是扩写定义。

此刻不需要假装我们已识别任何真实市场主体。理论研究可以先达到**解释能力、机制识别能力与新问题生成能力**；真实性和市场净收益属于后续不同任务。

## 11｜如何装回原有知识体系（不另造一套）

| 原有层/领域 | 本专题深化了哪一项专业能力 | 应由哪个已有专家承接 |
|---|---|---|
| L0/D10 | 供应商“同源”“聪明钱”“交易量”到底分别测到什么 | E-L0-02 |
| L1/D01 | Token Account owner、delegate、PDA、payer、指令与交易净额 | E-L1-01、E-L1-02 |
| L2/D02/D03 | 曲线/毕业/LP、CPMM 交易费与 creator fee、价格冲击 | E-L2-01、E-L2-02、E-L2-03 |
| **L3/D04** | 风险钱包/执行钱包/收益钱包的角色错位、钱包策略与 PnL | E-L3-01 |
| **L3/D05** | 资金职能、经济组织、公共 HUB 与资金回收、身份不可识别性 | **E-L3-02（主专家）** |
| **L3/D06** | 经济库存、资产处置权、LP 份额和可卖性 | E-L3-03 |
| **L3/D07** | 共同事件、共同服务与统一资本的不同因果时钟 | E-L3-05（联合 E-L3-04） |
| L4/D08 | 先买者经济优势与后入场的剩余信息 | E-L4-01、E-L4-02 |
| L5/D09 | 费用、仓位/价格冲击、两侧退出差异与拥挤 | E-L5-01、E-L5-02 |
| L6/D11 | 将理论竞争关系留待独立验证，而非用专家表态判定 | E-L6-01 |
| L7/D12 | 保存机制解释、边界、未解问题；禁止假设自动进入生产 | E-L7-01、E-L7-02 |

**知识使用顺序不是必须跑表中所有专家**：当研究任务是“谁承担本金”，从资金专家开始；研究“为什么钱包收益不能复制”，从 E-L3-01/E-L4-02 开始；只有当前主张确实需要其他机制时才请求交叉挑战。

## 一手依据与历史研究继承

**协议与市场技术来源**

- [Solana Tokens/Token Accounts](https://solana.com/docs/tokens)；[ATA 创建/owner 与 payer](https://solana.com/docs/tokens/basics/create-token-account)；[Spend Permissions（delegate）](https://solana.com/docs/payments/advanced-payments/spend-permissions)；[CPI/PDA](https://solana.com/docs/core/cpi)；[Permanent Delegate](https://solana.com/docs/tokens/extensions/permanent-delegate)；[Solana fees](https://solana.com/docs/core/fees/fee-structure)。
- [Solana RPC JSON Structures](https://solana.com/docs/rpc/json-structures)；[Jito Bundle 文档](https://docs.jito.wtf/lowlatencytxnsend/)。
- Raydium 原始官方文档（2026 年版本，具体部署配置可能变化）：[CPMM Math](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/math.mdx)、[CPMM Fees](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/fees.mdx)、[LaunchLab curve](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/launchlab/bonding-curve.mdx)。真实池参数应按池对应合约版本和链上配置另行核实；绝不直接照抄文档某时点的默认费率。

**历史知识来源与关系**

- `sunshihao001/-/learning/10.md`（钱包角色）、`learning/11.md`（同源）、`learning/12.md`（Sybil/Wash）、`design/phase1-research/00c-GMGN-思维模型提炼.txt`、`00d-GMGN-多维度推理扩展.txt`、`00e-字节反推框架-突破认知局限.txt`。
- `sunshihao001/meme-/docs/project_ai_context/12_DIRECTION_SHIFT_MULTI_AGENT.md` 中的多机制/多策略视角；继承它对单一 FCZ 路径的修正，不复制投票式共识。
- `grok/knowledge/domain/L3-wallet-actors.md`、`L3-actor-expert-perspectives.md`、`L3-actor-economic-mechanisms-deepstudy.md` 为本研究的导航与原理支持。
- 旧 `2 秒/同源/固定置信度` 直接推庄家和内情的断言，在本篇保持**被挑战状态**；本篇没有提出未经数据标定的替代阈值。

**当前研究产出是“更有深度的机制解释能力”，不是专家自动运行或市场交易策略。**

## 2026-11-01｜同行成品源码纵深：交易执行归因、SOL/WSOL成本、资金边时效与经济主体不可识别性

> **状态：SOURCE_CODE_INSPECTED + ECONOMIC_COMPETING_EXPLANATIONS；没有执行Million/OKX真实运行、没有独立链上交易回放、没有估计真实误报率。** 固定参考：[Million@c89ad07c](https://github.com/Kelows/million/tree/c89ad07caaf70773d40b45943e136eadc4f946a5)、[HoldTech@a75e214b](https://github.com/co-numina/holdtech/tree/a75e214bf1ee0a8803eb7d93336be98c481c2db9)、[pumpwatch@156a91ab](https://github.com/cinder-security/pumpwatch/tree/156a91ab63740ab0ce8700434ff33844d00de519)、[OKX工作流@73904b63](https://github.com/okx/onchainos-skills/tree/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25)。以下假设情境均不是实际Mint案例。本节深化原E-L3-02/D05，不新增专家/本体。

### 一、同交易中，手续费付款者为何会被记作资产买入者？

[Million: apps/api/src/analysis/metrics.ts](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/analysis/metrics.ts) 的 orchestratedDeltas(wallet,tx)：若被研究钱包是 Fee Payer 且自身无Token变化，遍历它与其他地址的 nativeTransfers；遇到第一个有Token变化的关联地址，返回该地址的资产变化并用于 Fee Payer 的钱包指标。这是识别“费用赞助者+执行钱包群”的有效**候选发现启发式**，却未独立验证最终成本承担、策略决策、授权权利及收益归属。第一个匹配地址还可能取决于转账列表顺序。

**竞争性经济世界（构造反例）**：P为多客户机器人服务商、代付手续费，客户E在同笔交易中买Mint X，双方存在服务费、租金退款或其他SOL转账；程序可能将E的Token净买入归给P。另一世界是P实际控制E、承担交易本金。二者可能产生相似的 Fee Payer/transfer/delta痕迹。**目前可见字段不足以唯一识别这两个世界**，尤其不能把“同交易赞助者”升级为“共同最终受益人”。

原文已区分same_funder/same_executor/same_authority/same_beneficiary；本次增量是指出一个真实代码路径正好**跨越这些关系层级**，不是重复抽象禁令。

### 二、同一个项目的两个“买入金额”函数却可能量度不同东西

- [Million metrics.ts::txDeltas](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/analysis/metrics.ts)：若有accountData，使用钱包的native余额净变化 + 所属WSOL Token账户净变化；避免把同一次wrap/unwrap中SOL与WSOL传输重复统计。原作者在[tools/check-accounting.mjs](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/tools/check-accounting.mjs)记录手算回归，并声称曾用36笔真实Swap检查；**未在本轮独立复跑36笔**。
- [Million discovery.service.ts::buyersOf](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/discovery/discovery.service.ts)：对于收到目标Mint的地址，叠加其负nativeBalanceChange和向外的WSOL/USDC/USDT tokenTransfers以推算报价SOL。它未复用txDeltas的去重方法。若同一经济支出同时出现在native净减与WSOL向外转账中，有**条件性双计风险**；即便没有双计，native净减还可能包含手续费、ATA租金和其他支出。
- 目标Token接收与账户SOL支付同时发生，也不必然证明这两条腿是有因果关联的Mint买卖；源码buyersOf()不针对每个买家解码关联的Swap指令。它更适合发现**候选买入账户**，不宜直接给真实成交价/成本背书。
- 已读会计检查脚本覆盖txDeltas及成本账本，没有直接检查buyersOf与orchestratedDeltas。**在一个模块中验证准确，不等于同仓另一个同名指标已验证**。

**专业意义**：同叫“买入金额”的界面指标，实际可能是现金流净额、Token流出报价、带费用的Native净变化或基于某个地址的代理推断。必须保存指标的生成方式、观测钱包、计费/租金处理及同交易资产腿。Solana RPC官方 [getTransaction](https://solana.com/docs/rpc/http/gettransaction) 与 [JSON结构](https://solana.com/docs/rpc/json-structures)提供pre/post余额、fee、innerInstructions、TokenBalance和Account owner作独立对照。

### 三、资金图如何把有向历史事实变成永久无向群体？

- [Million funding.service.ts](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/funding/funding.service.ts)保留转账方向in/out、firstAt/lastAt、双方金额，是值得学习的资金调查业务视图；目前只有有限页的SOL历史，不等于原始本金全历史。
- [Million owners.service.ts](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/analysis/owners.service.ts)的extractEdges将与研究钱包两方向的native transfer累积为同一种funding边，并用norm(a,b)把A→B和B→A归为同一无向关系；随后cluster()以某类边做Union-Find。这里的funding边并不保证“谁给谁融资”，更不能证明共同最终控制。
- [Million Prisma WalletEdge](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/prisma/schema.prisma)仅有a、b、type、weight、createdAt，无原始签名、资金方向、最后观察时点或证据有效期。extractEdges仅upsert、rebuild直接读取已有边；**在已查实现路径中没有过期撤销旧边的逻辑**。旧公共服务转账可能持续被用于当前主体聚类。Hub度数排除值得保留，但阈值及所见边数量会改变排除结果，实际误归因率仍未知。
- 这揭示一个时间性难题：**钱包关系在某个时点成立 ≠ 当前仍存在共同出资/控制关系**。关系群是证据时间区间内的候选网络，不是一个稳定自然人ID；失效边、时间反向、资产类型及Hub都可能改变答案。

### 四、Token轮换中的库存守恒 ≠ 单币成本或利润被真实观测

[Million ledger.ts](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/analysis/ledger.ts)的isRotation / rotationSteps识别少量报价变化下的Token-to-Token轮转，避免把账户租金退款误计为卖出所得，并将原Token成本基础移至新Token。这是源于真实会计失败的有价值修正。但当收到多个Mint时，当前实现把转出的成本**平均分给每个收到的Mint**；这个分摊是项目账本约定，未由各Mint成交价值唯一决定。由此生成的单币PnL不能自动称为链上独立确定的经济利润；Token-to-Token交易在市场执行层仍可能有滑点、费用、换仓损益和机会成本。先保留每资产净数量与实际对价，再讨论成本分摊规则和适用边界。

### 五、与已有参考的竞争性解释

- [HoldTech deep-scan](https://github.com/co-numina/holdtech/blob/a75e214bf1ee0a8803eb7d93336be98c481c2db9/app/api/deep-scan/route.ts)把同Slot的feePayer当buyer；在目标钱包SOL净增加时将交易message.accountKeys[0]（Fee Payer）当fundedBy。这是与Million不同但同样跨越费用付款和资产资金来源的代理假设，不能作为相互独立的身份确认。共享Slot也不足以确认Jito Bundle。
- [OKX token-research](https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/workflows/token-research.md)将holders、cluster、top-trader、Dev和发行信息分成不同报告步骤；标签出现在同一报告并不证明源数据和身份归因相互独立。暂无本项目的授权在线运行。
- [pumpwatch creator_reputation.py](https://github.com/cinder-security/pumpwatch/blob/156a91ab63740ab0ce8700434ff33844d00de519/code/creator_reputation.py)的seen_at来自本地首次记录时间而非实际Mint创立时点，已在旧D04/D07说明，继续作为发行时序反例。
- [原Hermes证据链](https://github.com/sunshihao001/-/blob/main/skills/meme-evidence-chain/SKILL.md)的source_field、missing_fields、counter_evidence及[旧qb单Mint报告](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)的基础设施/钱包角色分离应保留。旧GMGN标签属于历史供应商候选，不能自动恢复为事实。

### 本轮DIFF、状态与下一项值得研究的未知

**旧认识**：费用、授权、控制和经济受益要区分。**新增可检查源码机制**：Million在orchestratedDeltas中实际将另一钱包交易归给Fee Payer；discovery与metrics的SOL/WSOL计数语义不同；owners把双向资金事实折叠为长期无向关系；轮转时多Mint成本平均分摊。它们分别影响**谁在买、实际花了多少、谁与谁关联、谁赚了多少**，不能简单拼成“庄家得分”。

此轮只建立机制性证据与竞争解释，未做任何链上样本的独立归因或商业接口复跑。后续值得对照本项目已保存的官方RPC交易示例与Million作者测试，研究原始balance/fee/Token owner/CPI在何种条件下足以重建**资产层事实**、何种经济受益信息根本不可链上唯一识别；不要先开发归因算法。

知识关联：D01/D04/D05/D06/D07/D09/D10/D11；本节未改生产规则或自动交易，也不新增本体。
