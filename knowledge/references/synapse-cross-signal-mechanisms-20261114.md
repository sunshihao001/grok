# Synapse 方法笔记第二轮：跨信号机制、源码断点与交易机会反证（2026-11-14）

**范围与证据**：完整承接 [第一轮全分类台账](synapse-methodology-full-taxonomy-20261114.md) 的 S01–S14、D01–D03、B01–B03、H01–H04、HT01–HT05、P01–P05、F01–F04 以及全部可视化/产品/合规信息。不再按当前 Solana Meme 产品适配程度删减知识。原 Synapse 来源仅为用户转述笔记（USER_PARAPHRASE）；原站 https://synapse-onchain.com/en/methodology 本轮无法直接访问（robots.txt），不冒充已核对官网全文。Blix 与 Million 为 SOURCE_READ；论文结论标记 PAPER_RESULT；计算反例标记 SYNTHETIC。本轮没有联网实跑 Blix、没有修改交易程序、没有实盘验证。

## 一、把原分类连成六组可纵深研究的经济机制（我们提出的横向组织，不是 Synapse 原名）

| 机制网络 | 原笔记分类的完整对应 | 实质性研究问题与延伸 |
|---|---|---|
| M1 资产托管、金库及交易所库存 | S01 Safe inflow；S02 Safe withdrawal；S04 CEX withdrawal；S05 CEX deposit；S14 Exchange proxy inflow；D03 Team sells；F01、F03 | 入库、提现、托管迁移与实际成交卖出如何区分？多签/团队/代理钱包归属怎样证实？初始库存、存留、卖出与未卖出分母如何确定？ |
| M2 新地址、共同注资和资本入口 | S03 Fresh cluster；S09 Stablecoin funding；H03 Fresh on HL；P04、F01、F02 | 首次链上活动与首次真实资本参与是否同一事？同源资金是共同控制、交易所、公共代付还是普通服务？是否真的转成买盘？ |
| M3 分发、领取、筹码组织和群体变化 | S07 Distribution(push)；S08 Claim(pull)；S10 Coordinated withdrawal；S11 Large transfer；S01、S02、D03、P02 | 分仓、领取、发币、迁仓与出货是否具有不同经济语义？接收地址后续是否真正在 DEX 卖出？跨 Mint 的群体怎样演化？ |
| M4 DEX 买卖、拆单、跟随与价格形成 | D01 DEX buys；D02 Team buys；B01 加仓序列；B02 协同买入；B03 大额买入；H01 Whale；H02 Small-cap cluster；HT01 TWAP、HT02 Grid、HT04 Large | 真实买卖对价与 Token Transfer 如何重建？群体交易是否独立？信息到达后是否已经过度拥挤，仍具净成本后交易机会吗？ |
| M5 上市、稳定币、跨链和永续衍生品风险 | S06 Binance Alpha；S12 Stablecoin depeg；S13 Listing (perp)；H03、H04 Liquidation & risk；HT03 Flip、HT05 Liquid.，并涵盖 H01/H02/HT01/HT02/HT04 | 上市、脱锚、强平、跨链桥入金等是否能传导到现货？标记价、资金费率、价格冲击、公开时点与可执行时点怎样对应？不得直接将 HyperLiquid 规则套用到 pump.fun。 |
| M6 去噪、事件一致性、表示与审计 | P01–P05；F01–F04；S11；全部 D/B/H/HT 复合标签；DEX Visor 气泡/钱包开关/时间同步；免责声明、匿名/localStorage、Telegram 登录、RU/EN/UA、多页面 | 同一个动作多标签如何去重？不同时间/数据源能否对齐？哪个观察是事实、哪个是解释？长期地址注册表是否排除公共服务？什么记录允许升级为交易评估？ |

所有 14 链上信号、3 DEX 事件、3 买入形态、4 HyperLiquid 主信号、5 行为标签、5 核心原则、4 噪音类及产品条目均在 M1–M6 中保有追溯入口。**源分类范围完整 ≠ 所有机制已经验证；研究优先级 ≠ 知识保留门槛。**

## 二、同一事件应允许四种不同结果

- **事实记录**：发生过可核验的 Transfer、Swap、Claim、委托或仓位事件，写清 signature、instruction position、mint、token account、owner、资产净变化、slot/event time/ingest time 和数据覆盖。
- **行为结构解释**：同源注资、同步建仓、分发、反复转移等形成暂定机制候选，同时保留共享平台/普通追涨/技术路由/历史缺口等竞争解释。
- **研究优先级**：即使流动性不足、价格异常或暂无法交易，也可能值得调查。
- **交易就绪/机会候选**：特定时点与订单规模下，价格可靠、可卖出、成本和延迟可接受，并且经过至少离线对照。前三种结果都不直接等于建议买入。

可以由市场新币、钱包事件、跨钱包资金网络、手动指定 Mint 四种入口触发；这些是可交叉的用户场景，不是四套程序或固定步骤。

## 三、真实 Blix 源码再次核查：重要纠正与新断点

| 位置与源 | 源码可观察事实 | 正确的产品判断 |
|---|---|---|
| [server/early.js](https://github.com/sunshihao001/grok/blob/blix/server/early.js) | 首笔后 30/60/120/300 秒特征，模型可升级 AI 队列 | 原版已有早期发现，不能重造 |
| [server/triage.js](https://github.com/sunshihao001/grok/blob/blix/server/triage.js) | 新币规则与轻量模型筛选、候选升级 | Synapse 应增加跨信号解释和补查，而非复制基础过滤 |
| [server/wallets.js](https://github.com/sunshihao001/grok/blob/blix/server/wallets.js) walletSignals + [engine.js](https://github.com/sunshihao001/grok/blob/blix/server/engine.js) | 已有跟踪钱包买入→adopt Mint→vet 安全→wallet/smart 告警；engine.start 实际挂接该函数；多钱包会调用 independent() 启发式去重 | **纠正上一轮可能形成的误判：不是没有钱包→Mint 发现链路。** 需要核查它与专业调查队列、跨Mint机制和 AI 输入怎样交接 |
| 同上 clusters() | 以最近 3 天同 Mint 两分钟内多次共同买入或共同第三方 fee payer 聚类，排除已知 Fomo fee payer | 关联组数不是独立经济主体真值；仅可声称启发式相关 |
| [server/research.js](https://github.com/sunshihao001/grok/blob/blix/server/research.js) gather | followedWalletsBought 使用 COUNT(DISTINCT wallet)；没有应用 walletSignals 里的 independent() 组折叠 | **发现 C1**：同一 Mint 的“跟踪钱包数”与“启发式独立组数”可能不一致。不得在 AI 深读中把 raw wallet count 叫独立聪明钱共识 |
| [server/wtrack.js](https://github.com/sunshihao001/grok/blob/blix/server/wtrack.js) fromTx | 当 sol.parseSwaps(tx,wallet) 返回任意 swap 时立即 return，不再解析 parseTransfer。转账提取仅处理指定的净变化形态 | **发现 C2**：Swap+Transfer 同笔交易的转仓腿可能不进入 wt_transfers；没有转账条目不代表没有转移。需要真实或确定性 fixture 验收，尚未证明具体主网漏检率 |
| [server/research.js](https://github.com/sunshihao001/grok/blob/blix/server/research.js) enqueue / scout | 研究队列主要从新币、临近毕业、刚毕业、原信号重读进入；walletSignals 负责 alert 而非在已读函数中直接调用 research.enqueue | **发现 C3**：被跟踪钱包触发安全告警，不等于该 Mint 已被赋予完整 AI 深度调查优先级。需进一步端到端核验，不宣称绝对没有其它入口 |
| [server/brain.js](https://github.com/sunshihao001/grok/blob/blix/server/brain.js) PAPER | 每边固定 3% 模拟成本，并假设可按纸面价格出售 | **发现 C4**：存在结构信号不等于可执行收益；盘口深度、动态滑点、队列延迟和退出失败需与信号一起考虑 |

**因此新增模块不应从零写“聪明钱共买提醒”。更有价值的是：统一原始地址数/关系组数/归因依据口径；确保 Swap+Transfer 不漏掉转仓；把钱包事件、调查请求和交易机会排序联通，而不重复来源数据处理。**

## 四、外部成品与反证：为什么相关信号不能自动升格为交易优势？

| 原始来源 | 经本轮检查能支持的认识 | 对 Blix 的增量 |
|---|---|---|
| [Million README](https://github.com/Kelows/million) 及 [decision-log.ts](https://github.com/Kelows/million/blob/main/apps/api/src/common/decision-log.ts)（源码） | 钱包找币、币找钱包双向闭环；记录按阶段、结果、代码、原因结构化写入；decision log 的数据库写失败会被吞掉 | 保留每一次候选升级、排除、放弃理由和记录失败状态，防止“没记录=没发生” |
| [Million copyability.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/copyability/copyability.service.ts)（源码） | 用鲸鱼成交时点及滞后 60 秒的分钟 K 线比较复制可行性，记录 skipped；分钟线只是代理 | 从“钱包赚过”转为“我们发现后能否跟随”，在延迟与成本后做筛选 |
| [ricoboost 策略复盘](https://github.com/ricoboost/meme-coin-trading-bot/blob/main/docs/STRATEGY.md)（作者声明，非独立审计） | 作者报告回测有效但实盘亏损，归因于信号拥挤、滑点、幸存者偏差、费用和退出困难 | 将早期共买、智能钱包共识同时当成可能“已经拥挤”的线索 |
| [Gafarov，2026-10-29，arXiv:2610.39458](https://arxiv.org/abs/2610.39458)（研究预印本） | 作者观察约 200,443 个 pump.fun 发行、15,854,121 笔曲线成交和 51,025,958 SOL 转账、23,710 个候选钱包群；在其研究样本的 32 种样本外跟随配置下没有盈利，复杂群体结构未超越简单基线 | 必须对照价格/交易量/曲线状态等原版 Blix 早期基线，而不是拿“识别团体”当盈利证据。约 88.3 小时样本期不能外推所有市场 |
| [ian05012 dataset](https://github.com/ian05012/solana-memecoin-dataset)（公开数据集说明） | 保存侦测时快照、资金边、钱包交易与之后回填的结果标签；样本来自 GMGN 观察而非全市场 | 研究同源注资、钱包共买与机会有效性时必须冻结当时信息，防止事后最高价/胜者筛选/标签尚未成熟造成假收益 |
| [Solana Token/ATA 官方机制](https://solana.com/docs/tokens/basics/create-token-account)（协议） | Token Account、拥有资产转移权限的 owner、创建 ATA 资金支付方及交易 fee payer 可以不同 | 同 fee payer 不证明共同出资/同一操盘手，链上资金边和权属不可混写 |

## 五、六条可证伪的机制研究方向（不是已经成立的结论）

| 假设 | 竞争解释 | 需要哪类反证及证据 | 对交易筛选的真正影响 |
|---|---|---|---|
| H1 新钱包同源注资后集中建仓 | 交易所提现、公共代付、跟风 | 真实 SOL/WSOL/稳定币出资、池买单、后续群体重复关系，排除共享服务 | S03 主要推动调查；只有证明独立新增信息才影响交易判断 |
| H2 分发/领取/转仓后同步卖出表明潜在供给压力 | 空投、营销分发、内部移库、做市调拨 | 起始库存、token 权属、接收钱包 Swap 签名、相关真实成交量 | S07/S08/S10 与 D03 连通，不能把余额下降叫卖出 |
| H3 同窗买入的群体共识领先市场价格 | 刷量、同控多地址、价格变化已领先、自动复制 | 群体数量按不同依据折叠，与同期成交量/买盘比率基线对照，模拟延迟和成本 | 若不优于原版热度指标则不新增买入评分 |
| H4 CEX/团队金库转入转出预测库存释放 | 内部资金归集、托管移库 | 可信角色标签、去向、交易签名、真实卖出/买回的时间关系 | S01/S02/S04/S05/S14 保持事实和意图区分 |
| H5 稳定币/跨链桥资金先于买入 | 套利、常规调拨、补充保证金 | 资金到达后的真实现货/永续委托、控制时间点、对照样本 | S09/H03 不自动成为 pump.fun 新币硬过滤 |
| H6 上市、脱锚、衍生品强平改变 Solana Meme 风险状态 | 公共宏观冲击、与目标市场无关联、事件晚于价格变化 | 上市真实时刻、标记价/强平价/计价币稳定性、Solana 现货传导 | S06/S12/S13/H01–H04/HT 各标签保留跨市场研究资格，不机械迁移 |

## 六、已执行的三个合成反例：可复核但不是链上实测

本轮使用隔离 Python 执行简单断言，结果 PASS：
- E1 单笔 tx1 同一指令命中 Fresh cluster / Distribution / Large transfer 三标签，另 tx2 命中 DEX buy：按标签计 4，按唯一 signature+instruction 计 2。证明同一事件多标签不得当四个独立行为。
- E2 三个钱包 A/B/C，其中 A/B 归入一个启发式关系组，C 为另一个：原始地址数 3，关系组数 2，但**真实独立经济主体仍 UNKNOWN**。证明启发式聚类不能自动宣布同控或独立人头数。
- E3 指数最早 1.0，钱包信号被发现时已到 1.8，实际退出 1.6，纸面买卖各 3% 成本：按 1.6×0.97/(1.8×1.03)−1，结果 **−16.29%**。即使早期资金方向被正确观察，晚到参与者仍可能亏损。

上述计算不是 Blix 已产生的真实样本，不说明事件误报率或交易收益；只能作为离线单测的反例规范。

## 七、从原知识到下一轮能落地的验收

优先复用现有模块与 PR #23 的经济证据候选，先做三个互相依赖的判断：
1. **同交易多腿**：同一 signature 包含 Swap + Token Transfer，检查 wallet_trades/wt_feed/wt_transfers 与经济证据报告能否保留买入、转出、接收方卖出各自的动作，去重但不漏。
2. **同 Mint 的两种“聪明钱数量”**：让三个地址中两个共享 fee payer 或反复同币共买，在 walletSignals 告警、research AI 输入、历史复盘中分别显示原始地址数、启发式关系组数及不确定性，而不是输出不一致的独立操盘手数。
3. **候选升级+时点冻结**：对照 A=原版 Blix Early/Triage/Research，B=在不重复基础筛选的前提下按需补充跨信号证据；同样工具预算、同一时点信息，记录所有被拒/漏选的 Mint、可卖出条件、延迟、执行成本和已验证结果，禁用事后最高价影响当时排序。

P1 再研究跨市场上市/永续/桥接/脱锚如何影响 Solana 流动性与时效；但 **S01–S14、D/B/H/HT 所有原类别的独立知识研究一直开放**，不能因近期代码优先级低而删除。

**风险锚点与停研条件**：若跨信号机制只增加名字和文档，不改善证据正确率、候选遗漏、流动性/价格判断或历史可执行收益，则保留为调查与解释知识，不强行让其成为交易评分规则。

**完成状态**：跨全分类机制分析、外部来源比对、Blix 源级新发现和三个合成算术反例；**未完成**主网数据回放、原站全文核验、AI 扩展可运行接入、实盘或利润证明。
