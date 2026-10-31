## V4｜最佳运行方式：事件双循环、预算化调查、证据回流

优先阅读 [双循环运行架构 V4](../../docs/dual-loop-research-runtime-architecture-v4.md)。选型结论：**确定性 M1/M2 快循环 + 按需专家慢循环 + 独立 QA/知识更新回路**；常态 Bot 不用逐笔启动 17 专家，也不允许一个模型凭摘要覆盖原始证据。初期一个只读 Monitor 与一个动态 Research Manager 即可承载大多数任务；实际云环境 Bot 并未创建。

使用 `PYTHONPATH=src python -m solana_meme_os.research_dispatch --input .runtime/observatory-report.json --max-cases 4 --max-source-checks 12 --max-per-case 4` 对**已经生成的 M2 报告**提出预算化调查计划。Case 分别依据 Mint/Slot、资金源/窗口或明确的 cohort 聚合，不因 Mint 或资金源同名就制造一个巨大的时间外故事。多案例重复引用的签名可复用核查预算，未知 Kind 仍进入开放发现。命令不会调用 RPC、安装 Grok Bot、运行专家模型或执行交易。

适用边界：当前 M2 接收外部已归一化的四类事件，非实际全链覆盖；研究规划、独立结论撤回和真实交易解析是不同运行层。**模型不能把检测候选称统计异常或经济同控**；要进入纸面机会研究，另需决策时点、独立对照、真实报价与成本的验证。

---
name: solana-meme-system-intelligence
description: |
  Solana Meme 市场全局监控与链上行为专家研判技能。
  当任务涉及多钱包批量转账、捆绑/协同买入、异常账户群、资金来源和回收、
  疑似关联操盘、多币种重复地址、开发者历史、Sybil/刷量、筹码/流动性变化、
  市场阶段、事件预警、交易条件及跨项目深度知识转化时使用。
  跟单只是下游应用之一。本技能执行研究分析与监控设计，不执行真实交易。
---

# Solana Meme System Intelligence｜全局监控与机制研判 Skill V1.0

> **唯一定位：** 建设面向市场事件、钱包群体、资金网络、代币结构与可验证机会的综合监控与研判能力。不是“寻找聪明钱包并跟单”的单一 Bot。
>
> **核心认知：** 先复原**谁、何时、以什么资产、经过什么交易和账户变化、与谁发生关系**；然后寻找超出合理基准的行为结构；再研究它可能由什么机制产生、它怎样影响未来市场、什么条件下才具备纸面交易价值。
>
> **边界：** 本 Skill 是研究/系统规范和知识调用入口。仓库存在文件≠Grok 云端已安装；本阶段只读、纸面模拟，不下单、签名或广播。

## V3｜知识叠加产生新的经济机制：明确判错，不以“谨慎”压制研究

开始任何开放式市场现象研究前，参阅 [经济机制合成与认知判真 V3](../../docs/economic-mechanism-synthesis-and-judgment-v3.md) 和 [6 个待验证跨领域机制假设](../../knowledge/mechanism-synthesis-hypotheses.v1.json)。V3 不是17名专家投票，而是让一个领域创造另一个领域原先没有的解释、预测或反例，包括**跨地址角色不变量、时序资金行为指纹、市场自身冲击剥离、主动选择高判别价值证据、动态正常基准和从专家矛盾发现漏掉的交易机制**。

**必须果断判断**：
- **逻辑/协议被反例推翻**：直接指出规则错误。例如 `UNKNOWN_FIRST_FUNDER→ECONOMICALLY_INDEPENDENT`、`TOKEN_DECREASE→SWAP_SELL`、`NO_SYSTEM_TRANSFER→NO_SOL_RECEIPT`、`SAME_SLOT→JITO_CONFIRMED` 都不是有效的充分推断；不许包装成“有一点不确定但整体可用”。
- **有证据、但经济实体/因果关系未充分识别**：提出多个明确竞争机制，并找出最能区别它们的新签名/基准；不许停止在泛泛的“需要验证”。
- **统计机制在明确样本被推翻**：撤销该范围结论，而非给出更复杂但无法复算的分数。
- **结构机制有效但没有交易净优势**：可保留市场监控/风险用途，不能反过来说所有研究毫无价值。

**研究优势验收**：在相同历史时点、数据覆盖、调用预算和样本外发行上，比较单钱包特征、资金图、复合时序图、上下游市场机制以及主动反证专家方法；复杂专家系统如不能提升事实准确率/机制反证效率/可用市场信息中的某个明确指标，就简化，而非把复杂度本身当结果。新机制允许超出 V3 六项候选，不受 15 张知识卡、17 类专家或 40 条静态连接限制。

## R006｜从 SOL 余额进入真实经济来源，不局限于 System Transfer

[R006 40 钱包 × 905 条派生 SOL 流入审计](../../knowledge/research/R006-sol-receipt-economic-semantics-v1.md) 实际核对了旧项目的数据表和分类脚本：40 钱包中仅 21 个覆盖钱包起点，原标签 61 条 `financement` 并不都是直接 System Transfer（其中 8 条涉及 LP 撤回、NFT/跨链业务）；844 条 `produit_de_vente` 含部分非 SWAP 主类型。这不是“平台数据一定错误”，而是说明**研究业务标签与链上实际资产变化必须分开**。SPL `CloseAccount`/WSOL 释放可使接收者 SOL 增加而无 System Transfer，必须沿外/内指令 + 余额差 + Token 账户状态联合核验。

新增 [只读跨程序现金流标签审计器](../../src/solana_meme_os/cashflow_semantics.py) 和 [6 项本地实际运行通过的测试](../../tests/test_cashflow_semantics.py)。静态来源索引新增 `h2w6-original-inflow-table`、`h2w6-funding-label-generator`、`h2w6-sol-balance-method`；专家连接 L39 `chain→graph` 解决多程序收款机制，L40 `data→statistics` 解决分类与覆盖分母。**本轮尚无真实 Solana RPC 独立逐签名核验，不得用该 905 条派生表直接判同控或盈利。**

## R005｜真实跨项目源码分析如何反向修正专家推理（2026-10-31）

先读 [R005 原始资金来源跨项目法证案例](../../knowledge/research/R005-crossproject-funder-semantics-v1.md)：`solana-holder-clusters` 的 `funders.ts` 遇历史不足返回 `null`，但 `clusters.ts` 把该 `null` 放入 `independent[]`；其另一处以“交易最大SOL余额减少者”猜测付款地址；`Degen-Scanner` 保留查询失败计数为零的候选持有人进入后续追查。**可观察性失败≠真实独立、低活跃或同控**。

运行层研究修正：[只读首次资金状态合约](../../src/solana_meme_os/funder_evidence.py) 将 `FIRST_FUNDER_UNKNOWN`、`FUNDER_HEURISTIC_UNCONFIRMED`、`KNOWN_PUBLIC_INFRASTRUCTURE`、`HIGH_DEGREE_SOURCE_AMBIGUOUS`、`SHARED_PRIVATE_FUNDER_CANDIDATE` 等分开输出。此模块消费已归一化候选，未实现 RPC 解码和实时采集。[`tests/test_funder_evidence.py`](../../tests/test_funder_evidence.py) 为 11 项**已写入但尚未实际执行**的合成单元测试。

新增专业交接 L37 `data→wallet` 要求保留完整历史查询状态；L38 `wallet→statistics` 要求未知/公共服务/高连接源在正常样本统计中单列。一次错误标签必须能够要求 QA 重新审核上游来源，而不是被综合异常评分掩盖。

## 同类异常钱包项目的新增知识入口（2026-10-31）

以 [多项目异常钱包取证方法研究](../../docs/anomaly-wallet-reference-expansion-v1.md) 为入口，结合 [14 个来源分级与专家映射](../../knowledge/reference-project-discovery.v1.json) 阅读，不把搜索到的仓库全部并入生产能力。

新增四条跨专业证据连接：
- `token → graph`：开发者/Creator Fee 的**实际领取路径**进入经济资本循环；
- `graph → token`：资金网络的跨发行重复，反向要求核实开发者与公共服务商角色；
- `chain → statistics`：BUY/SELL 分类必须由指令审计通过后才能作为协同检测和正常对照输入；
- `graph → statistics`：排除公共 Hub，加入同频率、同类市场热度及等预警预算的图/null 对照。

优先级：独立复算 RPC 资金法证（CyberLeek）、首次资金源未知与公共 hub 过滤（solana-holder-clusters）、开发者→上游→买家→归集（Degen-Scanner）、2026 年最新多通道 prospective group 研究的真实反例；对 README 的“同控/内幕/庄家评分”只记录为供应商主张。旧 RED-COHORT 早期数值已被 2026-10 公开撤回，绝不能作为钱包协同检测的有效校准证据。

## V2.0｜跨层专家连接与真实反证协议（2026-10-31）

新增 [知识与专家连接结构 V2.0](../../docs/knowledge-expert-interconnection-v2.md)，正式把领域分析从“先后层级”升级为**带来源、时点、依赖及反证路径的专业交接网络**：
- [专家连接图（目前 40 条，首版为 32 条）](../../knowledge/expert-interaction-graph.v1.json)：每条规定发送方/接收方、交接的证据对象、使用条件及何种反证触发回溯；
- [12 条外部方法出处](../../knowledge/external-method-sources.v1.json)：Solana/Jito、Flink/Beam、W3C PROV、OpenTelemetry、微软专家协调、因果/漂移研究，均说明“可借鉴什么、不能证明什么”；
- `src/solana_meme_os/expert_interaction.py`：研究型静态图校验、专家交接建议及 claim 撤回的依赖影响范围规划；`expert_router.py` 在路由结果中返回 `typed_expert_handoffs`。

关键约束：专家说法必须带 `claim_id / evidence_refs / depends_on_claim_ids / decision-time availability` 等必要事实，**独立专家引用同一个供应商标签不会生成新的独立证据**。若一条原始事件被重新分类，应将依赖其结果的事件统计、资金网络、风险和纸面研究标记为争议或重新计算。经济资金图可以有真实回流环；用于证明某条结论的血缘不允许循环自证。以上是数据协议与局部只读代码，不是已经运行的多 Bot 自动回溯系统。

## 新增：从知识卡到专家交叉推理的实际路由

面对复杂新问题，首先阅读：
- [全市场专家知识协作体系](../../docs/solana-meme-expert-knowledge-orchestration-v1.md)：12 个知识领域、17 类能力、8 阶段与真实职责；
- [专家知识与场景映射](../../knowledge/expert-capability-map.v1.json)：`source_cards`、`source_ids`、必需观察、交付产物、竞争机制和不同事件的协作组合；
- [知识成熟度审计](../../docs/knowledge-maturity-and-gaps-v1.md)：区分原始方法已读、研究协议已成、真实复算和独立市场验证；
- 只读专家路由：`PYTHONPATH=src python -m solana_meme_os.expert_router --event FUNDING_FANOUT --event SAME_SLOT_MULTIWALLET_BUY --question "这组钱包是否独立？"`。输出调用的知识/专家建议，不执行实际专家模型，也不判断操盘或交易机会。
- [R002 专家交叉反证案例](../../knowledge/cases/R002-expert-cross-examination-v1.md)：说明事实、资金/筹码、统计基准和执行经济如何互相改写结论。

**专家不是 Bot 数量，也不是固定下游传话链。** 按事件和不确定性召集相关能力，至少让一种专业假说受到另一种独立机制检验。若链上指令不支持某个卖出标签，事件统计必须撤回；若没有正常同类基准，不允许发布已证异常；若同控关系未知，不必暂停市场流动性与独立协同观察。新机制可新增知识领域，不能受现有 15 张卡或五种事件路由限制。

## 0｜进入技能前先判断任务对象，而不是把所有事改写为跟单

识别用户真正问的是：
- **市场扫描**：新发行、迁移、异常热度与资金流向哪些代币值得看？
- **群体事件**：同一秒/Slot/窗口有哪些钱包做了什么？交易和转账的具体数量、资产与资金规模？
- **钱包角色**：地址可能是交易者、机器人、资助者、临时执行者、开发者相关账户、库存接收者或共享基础设施？
- **网络机制**：不同钱包是否共享非公共资金边、重复组合、统一执行和可回溯库存路径？
- **市场互动**：群体买卖是否先于/伴随/滞后于价格、池深、持有人结构和叙事变化？
- **机会与否决**：在可观察时点、足够流动性和可承受成本下，是否存在继续观察或纸面研究的必要？
- **跟单**：仅当目标明确是复用某钱包行为时，调用钱包可跟随性专题 R001/R003；它不是研究默认入口。

**重要：** 用户提出“疑似庄家”时，理解为寻找有可核实协调迹象的**经济实体假设**，不得声称已识别实际个人、违法操纵意图或必然价格方向。

## 1｜研究开始要读什么，按问题逐层调用

Grok 当前应读取 `AGENTS.md`、`CONTEXT.md`、`BOTS.md`、`knowledge/method.md`、`skills/solana-meme-monitor/SKILL.md`，必要时读取 `src/solana_meme_os/monitor.py` 和 `rules/monitor.v0.json`，确认*现有可运行能力*和理想设计的差距。

有选择地继承：
- 原 Hermes `learning/10.md`（钱包行为）、`learning/11.md`（资金溯源）、`learning/12.md`（Sybil/刷量/协同）、`docs/trading_system_stage_layer_design_v2.md`（分层与 Gate 思路）；
- `meme-` 市场周期、成本区与失败样本；检查任何要求“后续上涨确认”的定义是否含事后信息；
- `qb-` 只读工具原型及字段映射经验；平台钱包标签不等于已验证身份；
- `Why-Solana-Memecoins-Are-Over` 的 `coordination_detection/analysis_plan.md`、`economic_mechanics/`、`exit_destination/`、`funder_network/`：学习精确定义样本、保留分母、与 null 对照、识别基础设施和重复资产路径；
- `okx/onchainos-skills` 的市场与 Memepump 只读能力作为**候选采集接口**；API 的声明不是实际运行数据，也不能假设可覆盖所有历史区块。

需要最新 RPC 和 bundle 语义时参考 [Solana RPC JSON Structures](https://solana.com/docs/rpc/json-structures) 与 [Jito Bundles](https://docs.jito.wtf/lowlatencytxnsend/)。外部材料只做来源绑定与原创分析，注意许可；禁止整仓复制。

## 2｜监控的最小单位是“带时间和出处的事件”，而不是钱包标签

优先建立可审计的 **Canonical Event Ledger**，一条记录代表一个独立观察到的链上或数据源事件；不因属于同一地址而合并。

每条事件至少回答：

**标识与时间：**
`signature, slot, transaction_index?, instruction_index?, chain, program_id, observed_at, available_at?, received_at, source_ref, provider`。如果同 Slot 内无法从数据源取得可靠交易顺序，则显式 UNKNOWN；区分区块估计时间与系统接收时间。

**参与者与资产：**
`signers[], fee_payer?, source_owner?, source_token_account?, destination_owner?, destination_token_account?, mint, token_program, decimals, amount_raw, amount_ui, asset_type, quote_amount_raw?, quote_mint?`。

**行为及证据：**
`event_kind` 仅在来源充分时区分 `SOL_TRANSFER / SPL_TRANSFER / SWAP_BUY / SWAP_SELL / MINT / BURN / LP_ADD / LP_REMOVE / PROGRAM_INTERACTION / UNKNOWN`；保留 `classification_source` 与 `classification_evidence`。Token balance delta != 必然卖出；同一 SOL 净变动也可能包含费用、租金与其他指令。

**可得性：**
`observed_at` 代表链上相关事件时点，`available_at` 是信息最早能通过指定源获取的时点（无历史采样则未知），`received_at` 是我们实际获得它的时点。拒绝把后来的历史查询结果伪装成当时已知。

**数据质量：**
`RPC_status, parsed_instruction_coverage, missing_fields[], source_conflicts[], raw_event_ref, parser_version, de_dup_key`。同一个签名在多个数据源重复返回，不得重复计算为多个独立交易。

正常指标先来自正确事件账本，不能建立在缺失字段默认零或平台不可核对标签上。

## 3｜多钱包批量异动：写出明确的“多少、何时、多少资金、如何关联”

面对一段异常窗口，先生成一份可复算的**群体行为时序**：

1. 确定观察范围：`mint / pool / wallet cohort / program / market-wide`；开始与结束时点。避免从涨价结果倒过来选择起点。
2. 逐事件列明交易签名、Slot 和时间；区分已确认交易、转账、Swap、同 Slot 但不同 tx、同一 tx 多个指令、可能的 Jito Bundle。
3. 计算 `unique_wallet_count`、`transactions_count`、`transfers_count`、`swap_buy/sell_count`、`funded_SOL`、`buy_SOL`、`net_flow_by_mint`、`amount_distribution`、`first/last_activity`、`span_slots`、`burst_interarrival`、`funding_to_action_delay`。各项标注独立地址、交易、Token Account 或实体簇究竟用哪一个做分母。
4. 记录共同资金来源、重复转账金额、同 Slot/相邻交易位置、相同程序/交易路由、再次出现的地址组合和仓位接收者。
5. 重要变化给出可回放证据清单：**多少个地址、哪几笔交易、在哪个窗口、多少 SOL/Token、相较什么基准偏离多少**。
6. 若事件量很大，允许先输出高信息量聚合并链接明细；不省略异常判断所需的原始 signature 和时间区间。

**关键语义：** “同 Slot 多笔交易 / 相近时序 / 同额下注”可属于**协调候选**，不能直接写成“已验证 Jito Bundle”。Jito Bundle 有专门的原子执行和提交语义；没有可验证的 bundle 来源数据就标 `BUNDLE_UNVERIFIED`，只描述链上事实。

## 4｜正常与异常的判别：不是绝对标签，而是条件基准下的偏离

钱包“正常”必须以**同类基准**定义：新币刚创建、热门币高频交易、机器人执行和低流动性冷门币，不应共用一个阈值。

研究流程：
- **定义总体**：所有可观测代币/窗口，或明确指定的条件群体；对样本覆盖和未命中数量保留分母；
- **建立同类对照**：相近发行年龄、池子流动性、市场热度、协议、交易时段、钱包历史活跃度和交易规模；
- **选择统计模型**：根据问题使用置换、保持钱包频率/群组规模的图重连、资金来源随机化或时间抖动等 null；重要的是保留会自然制造同步的公共原因；
- **排除机械相关**：以“4 个钱包同 Slot ≥5 SOL”选中的样本，不能再把“4 钱包同 Slot ≥5 SOL”当作区分异常的独立证据；
- **异常解释分级**：`BASELINE_CONSISTENT`（与对照相容）、`STATISTICAL_DEVIATION`、`COORDINATION_CANDIDATE`、`REPEATED_NETWORK_PATTERN`、`CONFLICTING`、`INSUFFICIENT_EVIDENCE`。
- **反证优先**：共享 CEX / 执行服务、热门公共事件、对冲/套利、同步止损、重复 RPC 回报和扫描选择偏差等，应真正影响判断。

即使某模式通过统计检验，也只说明**当前观测总体下行为不同寻常**；恶意、操盘和实际受益人身份仍属独立论证。不能将统计置信度自动表达为“有 97% 概率是庄家”。

## 5｜疑似不同操盘钱包：从地址角色进到资金/库存的两层图

建立并保持分离的两张图：

**G_asset（已确认资产图）：** SOL 资助、Token 转移、Swap 真实输入输出、资金归集、接收地址库存、LP 变化，每条边有签名、资产、数量、Slot、时间。

**G_hypothesis（主体假设图）：** `POSSIBLY_SHARED_OPERATOR / SHARED_INFRASTRUCTURE / COMMON_PUBLIC_TRIGGER / UNRESOLVED`，每个解释有独立支持、削弱证据及适用窗口。

研究角色不限于“正常/庄家”二选一：`fresh_wallet`、`sniper_candidate`、`funder`、`relay`、`token_receiver`、`market_maker_candidate`、`repeat_executor`、`liquidity_provider`、`ordinary_trader_candidate` 等。一个地址可以多角色，而且角色随时间变化。

需要追踪的复杂结构：
- **一对多注资**：来源 A 在发币前后短时向 N 个地址供给相似 SOL；
- **多对一库存汇集**：N 个地址将 Token 汇入少量接收地址；
- **回流闭环**：下游市场卖出获得 SOL → 资金归集 → 同一钱包群或新钱包在其他币种重用；
- **跨发行重复出现**：地址簇、金额与节奏的重复组合，但不把同一热门服务商错误归并为受益实体；
- **反身行为**：买卖、资金回流与其他人的价格反应相互影响。

不能只因单次共同资助或交易同步就认定同控；更不能用机器人对正常者的“分类结果”反过来当同控的独立证据。

## 6｜市场全局监控不是单一代币报告

系统应允许从以下事件触发研究，而不只接受用户先输入 Mint：

`NEW_LAUNCH`、`TOKEN_MIGRATION`、`WALLET_BURST`、`FUNDING_FANOUT`、`SYNCHRONIZED_TRADES`、`REPEATED_CLUSTER`、`TOKEN_CONSOLIDATION`、`SOL_RECYCLING`、`LP_WITHDRAWAL`、`HOLDER_CONCENTRATION_CHANGE`、`BUY_SELL_IMBALANCE`、`LIQUIDITY_REGIME_SHIFT`、`CROSS_TOKEN_CLUSTER_ACTIVITY`。

一个市场事件应能反向关联：涉及的 Mint、钱包群体、共同资金路径、可能的下游接收者、市场状态与先前案例。反过来，点击钱包也能看到它参加过哪些代币、扮演哪些角色、哪些关系是已证实与待证实。

跨币种分析的优势可能不是跟单，而是识别**重复操作方式、资金再部署、集中退出、异常群体切换目标、风险传播**。

## 7｜发现异常之后，什么情况才值得研究交易？

这一层不是“异常越大越买”，必须分开输出：

- **发现层**：某个窗口有明确异常（有签名、窗口、数额和统计对照）。
- **解释层**：协调执行、共用基础设施、自然需求扩散、库存重组等竞争机制谁更符合事实。
- **风险层**：Token 安全、程序权限、流动性与退出、疑似派发、数据质量、集群库存和市场阶段。
- **预测层**：在事件**当时可见**的证据里，哪些变量能够区分后续走势/风险？需样本外评估。
- **经济层**：市场报价、实际延迟、深度、滑点、费用、失败和退出政策下，能否得到正净期望？
- **行动层**：`IGNORE / WATCH / INVESTIGATE / RISK_WARNING / PAPER_EVALUATION_CANDIDATE / PAPER_NOT_JUSTIFIED`；现阶段无真实下单状态。

可能需要研究的情境有：新发行中有可验证的独立外部需求、筹码和流动性结构支持后续价格承接；或经历极端回撤后出现供需改善；或疑似集中派发带来应当规避的风险。但任何方向都不自动成立，更不能因为一个“疑似庄家”群体买入便认定可跟随。

同时区分两种 Gate：
1. **数据/证据 Gate**：有没有资格判定行为？缺字段不能判正常，也不能判庄家。
2. **研究与纸面交易 Gate**：有无足够可得的预测信息、流动性、风险容忍度及独立样本支持？结论只能属于 paper-only。

## 8｜监控报告的写作范式：从事件事实到机制，而不是六段套话

每次报告根据问题深浅，自然覆盖：

**① 已发生什么：** 时间区间、Mint 与钱包/交易数量、涉及 SOL/Token 和交易类型，突出最重要的变化。

**② 为什么异常：** 与哪种正常背景比较？统计上是否仍偏离？样本如何选出？注意这些价格与钱包是否相互驱动。

**③ 可能的经济机制：** 谁可能出资、谁可能执行、Token 去了哪里？共享基础设施、独立机器人和同控的独特预测是什么？

**④ 会带来什么：** 对流动性、抛压、筹码状态、市场阶段与之后风险可能产生什么影响？区分已发生变化和未来假说。

**⑤ 应做什么：** 继续观察哪些地址/签名/时间窗；什么可触发下一轮研究；何时认为解释失败、降级或退出关注？

输出一个**认知增量**：与上次监控相比，我们究竟更理解了哪个机制，而不只是发现了更多地址。

没有足够数据时输出具体的缺口，例如“缺 12 个地址的上游资金签名”，而不是“需要更多数据验证”。

## 9｜三个案例训练和反证（不要求每次都全做）

**案例 A：同 Slot 多钱包。** 与公共热门发行、Jito 可能的 bundle、同一 funder 控制群比较；需要区块交易顺序、共同资金图和独立同阶段基准。不得直接称确认捆绑或操盘。

**案例 B：30 秒内 N 地址收到相似 SOL 后集体买入。** 先对资金端签名、金额和相对发币时间进行一致性检查；排除 CEX/通用分发器；寻找不同发行的重复群体与非公共路径，才能提升协调性解释。

**案例 C：多个早期钱包将代币转往少数接收者。** 这是库存转移证据，不是已发生卖出。跟随 Token 到 AMM 出售、SOL 回收及下一次注资，验证是库存执行网络还是共享托管服务。详见 R002/R003，只将其用作这个模块的实例，而非全系统主轴。

真实事件须有可复核签名、Slot、来源和已知边界。若使用思想实验，必须明确 `SYNTHETIC`。

## 10｜研究成果怎样进入 Grok

**A. 领域知识**：事件定义、钱包/市场角色、异常机制与反例，索引到原始来源。

**B. 观察技能**：从钱包和交易数据重建批量窗口、资金图、仓位路径、市场状态，不把缺失当零。

**C. 专题能力**：Sybil 与协同、刷量、开发者重复行为、资金回收、迁移和流动性风险、交易机会的条件机制。

**D. 验证机制**：记录样本总体、未触发事件、基线、误报/漏报、时间泄漏和可执行的 paper PnL。

**E. 报告能力**：对每个重要预警都提供事件清单、替代解释、最有鉴别力的下一条证据和研究状态。

注意：当前 Grok `src/solana_meme_os/monitor.py` 仅以单 Mint 快照的 `liquidity_usd` 和 `top10_holder_pct` 做两类变动检测，`events[]` 被当作来源事件登记；**尚无**多钱包滚动窗口、经济图与跨发行扫描的真实实现。既有 R001–R004 与新增离线 `position_audit.py` 是专项研究资产，不能被称为完整监控引擎。

未经单独设计、测试和批准，不修改 `rules/`、真实 Bot 或运行时监控配置。

## M2 源码研究入口：可运行聚合模块（尚未接入真实市场）

- 实现：`src/solana_meme_os/market_observatory.py`；
- 合成样例：`fixtures/market-observatory-synthetic.json`；
- 测试：`tests/test_market_observatory.py`；
- 字段与 CLI：[`docs/market-observatory-m2-v0.1.md`](../../docs/market-observatory-m2-v0.1.md)。

调用 `PYTHONPATH=src python -m solana_meme_os.market_observatory --input fixtures/market-observatory-synthetic.json --allow-fixture`，可以针对输入记录输出时间窗口汇总、同 Slot 钱包买入、批量注资、代币归集、跨 Mint 重复活动等**事实与候选**。不具备真实 RPC 数据接入、统计正常基准、实体同控判断或交易盈利判定；不因代码存在就声明已在 Grok 云端监控运行。Python 测试已编写，仍待运行容器执行确认。

## 11｜真实案例研读入口\n\n参见 [钱包群体监控实例](references/wallet-cluster-monitoring-example.md)：以一条真实公开事件的四钱包创建 Slot 买入、Token 转移和另一条 funder 短时注资案例为例，具体展开“多少钱包、何时转多少、如何做竞争解释以及为什么不能直接判同控”。该案例是研究源记录的交叉读取，不是本项目新的实时预警。\n\n## 12｜专业质量与停止规则

合格的领域研究至少能回答：**事件是什么、对象与分母是什么、何时可见、它与合理正常机制区别在哪、怎么证明自己可能错、下一步能复原什么真实行为。**

必须停止或降级的情形：
- 只有平台的“bundled”标签，没有交易序列或独立 bundle 证据；
- Token 减少被误称卖出，SOL 流向被误称同一受益人；
- 所有指标只是同一个创建 Slot 的机械结果，拿它们做“多维确认”；
- 被筛入样本的性质又被拿来当显著发现；
- 真实市场数据缺失却制造正常/异常比例；
- 未完成独立测试却宣布发现“可以交易”的模式。

**认知引导词：** 从单笔交易看群体协同，从地址网络复原资本结构，从异常行为理解市场反馈，在可证伪机制中寻找真正可观察、可迁移的交易研判能力。
