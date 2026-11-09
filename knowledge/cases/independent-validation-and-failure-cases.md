> **Blix 旧知识全文迁入｜案例评估及反证方法** · 原来源：[knowledge/domain/L6-L7-investigation-cases.md](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/domain/L6-L7-investigation-cases.md) · 原文件blob SHA `f16d28ff7357dd2b6047929792580f89f972307c` · 原研究领域 D11,D12 · 验证状态 **SOURCE_COPIED / RESEARCH_NOT_RUNTIME_VALIDATED**。旧文件的研究阶段、阈值、假说和引用保持其原意义；不作为现行全局指令。

---

# L6–L7｜把专业知识变成可复盘的案例与 Grok 只读调查流程

> 对应 D11、D12。此处不增加新的 Agent 职位、哲学术语或学术框架；仅明确**Grok 已经展开的市场知识怎么参与一次真实调查、怎样避免错误继承、怎样形成下一次能复用的内容**。

## D11｜验证与反证：专业案例至少要回答这些市场问题

### D11-01｜观察对象必须事前固定

跟单研究通常存在多个可能分母：全市场新发 Mint、某平台某时段实际可交易 Mint、某个候选源推送的所有 Mint、指定钱包有活动的 Mint、成功出现某种信号的 Mint。

这几个总体完全不同。若只研究“后来涨得好、还出现在排行榜上的币”，无论专业解释多么详细，都不能代表真实监控会遇到的市场。

每个案例保留：`universe_definition`、`token_mint`、`source_event`、`observation_bucket`、`eligible_at`、`decision_cutoff`、`source_coverage`，以及`NO_SIGNAL`、`DATA_MISSING`、`UNTRADEABLE`等反例。

### D11-02｜一个钱包机制，至少准备四类对照

1. **正常对照**：同阶段、同池深度、同市场环境下没有特定钱包行为的币。
2. **外观近似的反例**：同样同步/同源/Top10 高，却没有出现研究对象所期待的结构或结果。
3. **成功但未触发案例**：大涨但不存在当前钱包信号或原有策略条件。
4. **数据缺失/路由失败案例**：正确标记无法评价，不能当作“该钱包没信号”。

研究重点不是最大化命中率，而是识别**哪些证据实际上改变了判断**。

### D11-03｜历史回放必须模拟当时知道什么

- 如果钱包资金网络在两小时后才被完整解码，不能把全图作为当时第 10 秒的特征。
- 如果 token 被标为开发者相关地址是后来某次数据更新得到的，必须记录当时该标签是否已经存在。
- 如果某币在未来 15 分钟涨过 2 倍，不能依据这个结果反向挑选窗口、成本锚、钱包。
- 如果供应商服务断连，必须保留采集失败记录而不是从后来链上回填出“完美监控”。

### D11-04｜把“判断错误”分成不同原因

`DATA_DEFINITION_ERROR`（字段/单位错误）；
`IDENTITY_INFERENCE_ERROR`（把公共资金路径当成同控）；
`MECHANISM_ERROR`（解释不成立）；
`PREDICTION_ERROR`（结构存在却无可重复预测增量）；
`EXECUTION_ERROR`（策略理论有效但实际入退场失败）；
`COVERAGE_ERROR`（资料没有完整覆盖市场）；
`RESEARCH_LEAKAGE`（使用未来信息）。

不同失败类型要求不同修复，不应一律“再加一个过滤条件”。

## D12｜Grok 中如何使用这些知识

### D12-01｜用户问一个币：调查顺序

输入例：“这个刚迁移的币，几个钱包同时买入，Top10 也在涨，是什么情况？”

1. **先路由知识**：D02 迁移阶段、D03 池深度、D04 钱包行为、D05 资金源、D06 持仓结构、D07 同步与市场事件；D10 一直检查字段和时间。
2. **说清已知**：有哪些 Mint、pool、签名、交易、余额、原始时间、供应商响应；没有 K2 就说明是待查事实。
3. **生成竞争解释**：独立资金、共享服务、团队协作、做市/聚合器、数据口径问题；不先选“庄家”。
4. **查最能区分的证据**：若当前只有 Top10%，先核对 owner 与 pool 地址；若是同源资金，先查是否公共 HUB；若是交易同步，先用同市场普通行为对照。
5. **到策略层需要另有证据**：只有在提问涉及跟单时，才继续 D08/D09 的事前可见性与买卖成本。结构解释问题不必强行寻找可盈利策略。
6. **报告**：事实、解释候选、反证、缺失项、下一项只读检查以及 `BLOCK/WATCH/PAPER_ONLY/NEED_MORE_DATA` 的研究状态；不输出真实交易指令。

### D12-02｜用户问一个钱包：调查顺序

输入例：“这个钱包最近盈利很好，要不要跟？”

按 D04 检查历史 PnL 口径和逐笔真实交易；D05 检查其与资金网络及部署者关系；D07 检查市场阶段与重复行为；D08 比较钱包和跟单者的可见时点；D09 检查双向成交和成本。**不能直接把钱包历史胜率翻译成跟单建议。**

输出应至少有：

`wallet_behavior_summary`、`observed_trade_evidence`、`provider_pnl_caveats`、`funding_relationship_candidates`、`earliest_follower_visibility`、`execution_unknowns`、`disconfirming_cases`、`recommended_read_only_check`。

### D12-03｜如何保留每次研究的经验

研究案例不应只存“最终分析报告”。每份经验最好保留：

- **问题与当时背景**：当时为什么注意到该币/钱包、来源是什么？
- **可见证据**：当时真实取得哪些字段，无法取得什么，是否为历史回填？
- **机制候选**：一开始哪些解释合理，怎样选择查询？
- **决定性反证**：哪项新证据推翻了看似合理的解释？
- **程序表现**：源码/规则版本，是否发生漏检、误报、超时、重复记录。
- **后续观察**：市场后来怎样，哪些属于不应回填到事前判断的信息？
- **可转移边界**：此经验适用于哪个发行平台、阶段、流动性范围与数据提供者？

统一指向现有 `knowledge/case-template.md`；未来只有通过复盘/独立检查，才考虑从案例中提炼新的 `knowledge/catalog` 卡或规则。

### D12-04｜给 GPT 开发 / Grok 运行的实际边界

- GPT 阶段开发交易解析、资金图、案例回放和证据审查程序；源代码、测试、知识和可复算样本在 GitHub 形成可审阅提交。
- Grok 首先运行固定版本的只读程序，读取已审批知识，输出带来源及异常的结果。Grok 上的 Bot 实例数与知识深度没有必然关系。
- 外部 K1 文档受 `source-admission.v1.json` 管控；被标为 `review_only` 的来源只能专项人工复核，不能默认进入研究。历史知识卡没有自带市场有效性。
- 缺 K2 原始数据时，保留 `UNKNOWN` 与具体下一次查询要求，不靠新增术语制造完整性。
- 没有通过独立发布门槛的盈利/自动交易规则，不进入 B07 监控的冻结规则层。

## 一条完整案例如何跨过现有框架（示意，无真实数据）

| 阶段 | 专业问题 | 核心证据 | 当下能说什么 |
|---|---|---|---|
| D01–D02 | 这是哪个 Mint？处在哪个阶段？ | 签名、program、curve/pool 事件 | 确认市场对象和生命周期 |
| D03 | 深度和成交价格是否真实？ | reserve、双侧报价、LP 变动 | 能否解释流动性风险 |
| D04–D05 | 哪些钱包买入，资金有关联吗？ | 各钱包交易+转账图 | 行为事实和候选关系 |
| D06–D07 | 经济筹码和时序如何变化？ | owner 快照、净转移、市场事件 | 结构假说及其他解释 |
| D08 | 是否出现可能可复制的跟单窗口？ | event/available/quote clocks | 仅形成可检验假设 |
| D09 | 扣除实际可估成本后怎样？ | 买卖路线、规模、退出失败 | 纸面经济分析 |
| D10–D11 | 数据和结论有漏洞吗？ | 覆盖、反例、历史回放 | 检验与降级 |
| D12 | 下次怎样复用？ | 完整案例、代码、规则版本 | 知识和任务回写 |

**重点**：D01–D09 是要让 AI 真正懂市场；D10–D12 是保证这些知识不会在历史解释、数据污染和程序运行中被误用。当前优先产物应是能调查真实钱包/代币的知识单元，不是额外创建 Agent 框架或学术论文综述。

## 相关现有入口

- `knowledge/system/ontology.v1.json`：本体 D01–D12 与 L0–L7。
- `knowledge/catalog.v1.json`：15 张旧卡，仍保留。
- `knowledge/case-template.md`：案例模板，未来可放 K2。
- `knowledge/source-admission.v1.json`：研究来源默认准入规则（前序 Draft PR）。
- `src/solana_meme_os/research.py`：按需参考资料检索原型，尚非完整专家判断引擎。
- `src/solana_meme_os/monitor.py`：只读状态观察原型，尚未证明其具备稳定行情接入与盈利能力。


## 2026-11-09｜纯知识转化：判断是否值得相信，与任务是否结束是两个问题

> 来源包括 [qb-/Hermes 判断治理](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/15_judgment_governance/README.md)（blob f17421786c23f46beb89e658e02eff8a4aba8873）、[可靠性校准](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/16_reliability_calibration/README.md)（blob 143f89e1ec3c4920aaea4b5d8286c0a1090c596c）、[防文档即完成审计](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/22_anti_self_deception/document_only_audit.md)（blob 27bafe4f573f4e81ce83307b448ea037f9f9aa6a）及[meme-反证方法](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/反证实验设计_v0.1.md)。这些都是可独立吸收的**知识与判断方法**，不要求复制原Harness结构。

### 三种不同的“完成”不能相互替代

**任务完成**：文件已写入、代码已合并、测试执行结束，是工作状态事实；**判断被充分支持**：问题、来源、证据及竞争解释能支持特定结论，是认识上的条件；**结果已改善**：同等任务下实际减少误报、漏报、用户指挥次数或产生可靠新发现，是对照验证后的效果。旧qb的judgment governance与anti-self-deception区分这些层次：一个任务流能走到最终状态，并不证明这次运行值得进行、判断有依据或记忆值得留存。

**真正能迁移的不是22个子目录，而是用失败结果修正判断的思想**。例如旧qb记录“95条钱包摘要/4个候选同源组”，只证明数据文件里有这些项目，不能推出95笔真实Swap均已重建或已确认4个同控主体。Blix迁入一份知识文件同样只证明它保存了内容，不证明AI实际运用它。

### 失败样本不是附属材料

meme-的反证思想可用来检查任何“专业发现”：
- 正例：结构候选出现且后续证据支持提出的可观察机制。
- 反例：结构候选出现，但原签名/库存/实际交易显示所推断机制不成立。
- 漏报：模型未发现某关系，但留出证据确实证明该关系存在。
- 不可判定：上游资料缺失或观测定义不一致，不能因无数据就算成负例。

**一个新的风险**：过度保守也是失败模式。只要无法证明最终身份就全部拒绝继续调查，会漏掉确有价值的候选关系；相反，未经核验就给“庄家”标签又产生误报。正确目标是同时评估**证据正确性、候选发现力和补证信息价值**。

### 对 ai-d / Blix 的双重意义

对 Blix：将上述认识用于专业调查报告、独立核验、错误归因复盘、旧知识失效修订；保留实际市场样本与具体版本时点。对 ai-d：将“文档写完≠模型学会”“对照得分高≠真实可靠”“想出了很多解释≠真正发现新机制”作为通用AI自检问题。旧qb的校准文档明确说明dry-run只是证明校准流程能走通，不证明真实可靠性提升。**此节是知识研究与来源审查，不等于Blix已经具备可运行的失败追踪系统。**


## 2026-11-09｜知识推断关系审计：多项一致不等于独立证据

**原始理论来源**：[Hermes 13 多信号融合/Evidence Chain](https://github.com/sunshihao001/-/blob/main/learning/13.md)（blob `f192a8fb138d6632b74a04e3a0becb9220824a66`），[14 Trade Gate 与 Downgrade](https://github.com/sunshihao001/-/blob/main/learning/14.md)（blob `31f3c483e36a4a33168293c1687082d273d64fae`），[meme-复杂策略成熟度审计](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/策略成熟度质疑审计与商业诊断_v0.1.md)（blob `ca3771516dcf13f1dbe0a7fd7a4b79d4c57c92ce`），[qb-判断治理](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/15_judgment_governance/README.md)（blob `f17421786c23f46beb89e658e02eff8a4aba8873`）。跨学科方法参照 [NIST对自相关测量不宜使用独立样本公式的说明](https://www.nist.gov/programs-projects/uncertainty-analysis-autocorrelated-measurement-data) 与 [Solana getTransaction 的原始账本结构](https://solana.com/docs/rpc/http/gettransaction)。这些参考并非直接证明链上检测器的统计增益。

### 1. 什么可能在知识迁移时被误当成了“独立证据”？

旧Hermes 13篇把“多个Skill一致”列为置信度的来源。但三个Skill可能全部读取同一个GMGN聚合快照、同一笔Swap或同一组资金边；它们**是同一观察的不同变换**。共识不是新增的独立观察。meme-风险项如 failed_reclaim、bull_trap、death_market 等可能都由同一段价格跌回锚点计算出来；如果给每个名称再累计一次风险分，会产生**同源证据重复加权**。

| 可观察原始事实 | 可能派生的多个名称 | 正确的知识解释 |
|---|---|---|
| 同一笔地址A给B的资金候选转移 | 同funding、关联群体、资金接力风险 | 可以形成三个不同问题，但默认仍只是一条未确认的原始边；需要后续真实签名/时间/对价才能证明不同主张 |
| 同一段价格序列发生下跌后反弹失败 | failed_reclaim、bull_trap、death_market 候选 | 多种模型可能同时描述形态，不等于存在三个独立市场失败原因；同一时窗/锚点的派生依赖应能追溯 |
| 同一供应商的holder_count和top10占比 | 多钱包分散、筹码集中、Sybil风险 | 分母、Token Account/Owner、公用池或CEX分布可能共同影响全部指标；须找独立的链上/历史反证 |

原教材强调支持、反证、missing和downgrade同时记录，这是值得保留的知识；需要补充 **claim → derived field → primitive observation/provider → sampling window** 的依赖关系，避免“名称多=证据强”。对于两个真正独立的新观察，支持关系可以加强，但必须先弄清它们是否共享原始来源、共因或误差。

### 2. 判定动作与市场解释的损失函数不同

原 Hermes 14篇为研究/纸面执行分出 BLOCK、WATCH、PAPER_ONLY、NEED_MORE_DATA。它解释了**约束行动**的重要性；但若把“交易不宜继续”直接复制为“研究不宜继续”，便会遗漏风险高却研究价值高的市场样本。只读研究可用 INVESTIGATE/NEED_EVIDENCE/UNDECIDABLE 等语义描述进度（仅文字示范，**不新建枚举/API**），而不能套用历史交易Gate给市场身份判定。

**过度肯定和过度保守必须一起检查**：四个同源候选组的跨组桥接未获链上时序确认，不能称已确认资金接力；但因此完全不调查桥接地址，也会漏掉一个有信息价值的线索。失败记录应同时覆盖误报、漏报、过度故事化、过度拒绝、历史信息泄漏、来源重复加权。

### 3. 如何验证该知识是否真的影响 Blix？

以冻结的旧qb- 4TKY 资料做相同任务的对照：一组仅看到同源组和风险标签，另一组加上原始证据依赖与Hermes/meme-反证要求。独立验收应查：能否发现跨组桥接；能否指出61条边未给金额时间；会否把同一数据变换当不同证据；是否避免把“全退出”当已见Swap；能否提出下一项高价值只读补查。不能因为结果文字更丰富就判定AI变强。**本轮是来源审查与知识修订，没有执行模型A/B、链上签名复算或Blix运行时验收。**


### 4. qb-判断基准比README更有价值，但不能冒充真实验证

本轮又向下读了 [qb-判断治理模板](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/15_judgment_governance/templates/judgment_governance_state_template.json)（blob `62905b4a4d2863ab79f338b6e0092a7c94f2fd1d`），以及 [fake closure样本](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/15_judgment_governance/benchmark_cases/fake_closure_dry_run_as_real_completion.json)（`60455e789690c60a421e7a613e5a74aaad1b7c2d`）、[benchmark 001](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/21_judgment_benchmark/benchmark_cases/bench_v2_001.json)（`c531c65e07cde839ca9a70d56b30cea2c1dd22ca`）和 [可靠性状态模板](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/16_reliability_calibration/templates/reliability_calibration_state_template.json)（`39ba0714f14eb8af5af7a82064554c80e16ff1c6`）。

- **实质知识**：纠错不仅是在最后说UNKNOWN；原模板对问题真实性、根因、证据充分性、真正独立的验证、认知成本、可撤回性、记忆过时与后续偏差修正提出不同的审查问题。对普通AI项目可用于检验“复杂度是否值得”和“知识是否因历史错误影响下一次研究”。
- **具体例子**：fake_closure样本列明正确处理需要真实执行证据、独立验证、验证可失败、dry-run单独标记；不接受文件存在/模型自述作为系统已完成。
- **证据级别**：原`21_judgment_benchmark/README.md`明确称其为**benchmark skeleton**。样本`bench.v2.001`只包含任务名称及预期判别，不能把它视为模型已通过真实回归。状态模板`overall_passed=false`是初始内容，不是一次真实测试输出；预设`evidence_sufficiency.threshold=0.7`也不是跨任务已校准的专业证据阈值。

**Blix迁移修正**：保留上述判断思维，不复制整套Hormes Harness的空模板与固定自评分数；把`模型是否发现正确的新问题`、`工具是否提供真正新来源`、`产品是否实现并通过独立反例`分别检查。**本轮只审阅了原数据/模板，未执行这些benchmark。**


## 2026-11-09｜知识反证案例：先挑赢家、再标结果，研究结论何时不能迁移到真实市场？

> 该案例承接 D11“先冻结观察对象、失败样本、时间窗”，不新增独立验证框架。来源和详细反证见[跨项目深入研究第14节](../references/source-knowledge-deep-study-v0.1.md#14-2026-11-09-新增跨项目实证样本入选--结果成熟--数据缺失如何共同制造市场规律)。

**原始具体证据**：Why-Solana 的[源脚本与公开 JSON](https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over/blob/070d2a6e6dcb89efe18d01091a8040eb323e1099/code/a4_selection_bias.py)测得中性基准2,740个发行中的32个毕业（1.168%），历史作者选中11个案例11/11毕业；前者是基准发行抽样框，后者已由结果挑选。CryptoBot 对MELT标签[复查](https://github.com/elalamiimed/CryptoBot/blob/1be592d71020738510b25e3bed7a2f5def13ff0a/reports/cohort_survivorship_20260927/FINDING.md)发现41,470个带标签币全有迁移后记录；因此该标签样本的内部关联不能自动推出所有新币的盈利概率。**这些数据是不同作者、不同时间/定义的证据，不能合并计算一个全市场胜率。**

**此前认知容易漏掉的一层**：即使事前没有“挑赢家”，结果计算时也可能再次选择。ian05012 [`label_returns.py`](https://github.com/ian05012/solana-memecoin-dataset/blob/7070d00e1e4492f8604d988549d91785cc5f43f7/scripts/label_returns.py)将“6小时取不到任何K线”直接写入24h和3d未来结果的零标签，并设`labeled=1`。离线SQL分支已复算：即便以后有价格，常规未标注查询也不会回访。这揭示**缺价格数据、未满观察期、确认失败和真实可交易结果**是四个不同状态。

**可以立即改变的专业判断**：调查一个币是否异常时，不必因为其样本不具代表性就停止；研究全市场胜率、币种“普遍规律”、钱包策略优越性时，必须知道被过滤的分母、未到结果期限者和仅在幸存币上计算出的指标。这里应输出“只适用于被观察到的样本”，而非一律驳回研究或强行计算校准概率。

**可反驳的后续问题**：同一天、同发行阶段的未入选币若被低成本抽取少量复核，其资金来源、钱包重复出现率和最终结果是否显著不同？若相同，则某些选择偏差担忧可能被降低；若不同，应追查是市场机制、观测渠道还是标签成熟差异。**未用Blix真实运行做上述对照**；研究的完成标准是能观察到影响结论的差异，而不是增加第N份理论报告。
