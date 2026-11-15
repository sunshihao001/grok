# Blix 原生知识 × 旧 Grok 知识：对应、去重与收录清单 V0.1

**2026-11-14｜多路线知识闭环补充：** 本文件负责概念、领域与原始知识的**横向对应与源级反证**；真正的四入口、多业务条件交接、反馈回路、责任层与逆向路径，统一由[现有Blix跨层锚点V0.5](../docs/project/cross-layer-anchor-map-20261113.md#2026-11-14多路线概念承接知识业务工程三重闭环v05)说明，并由现有领域模型的`cross_axis_alignment.businessRouteGraph`提供只读结构视图。`npm run audit:knowledge-trace -- --routes`检查静态引用和反馈路径；**不是**链上图谱已实跑或所有知识自动进入AI上下文。旧D01–D12、K1–K9与ai-d来源仍维持原权威，知识闭环必须回到O1–O6的实际Meme业务。

**2026-11-14｜当前知识主述责任与成品对应：** [完整D01–D12主述/来源归位](README.md#2026-11-14全域专业归位总入口十二领域主述参考来源知识身份与产品验收)只定义已有专业知识的归属和证据边界；本跨表仍负责旧Grok×Blix重叠、概念关系与跨域映射，不复制十二份正文，也不把Synapse/GMGN知识登记等同真实AI接口激活。[扩展成品路线](../docs/project/intelligence-layer.md)以真实代码/运行测试为准。

> 2026-11-06 | 本文件严格依据 [Blix 原生体系](BLIX-NATIVE-ATLAS.md) → [旧 Grok 原体系](OLD-GROK-ATLAS.md) 的阅读顺序，之后才作接收裁决。**不变更业务代码、不安装Bot/依赖、不运行网络或交易。** 现在的结论是知识与功能的映射，不是已完成的AI主动调用。

## 2026-11-13｜结构收束 V0.2：从知识分层到七类跨层能力、五种逻辑视图

**原来的层级与关系不用推翻。** 原G0–G4目标、O1–O6业务、K1–K9知识生命周期、D0–D9工程依赖、L0–L7深度、D01–D12专业领域、10观察轴、11关系、旧152索引都保留。现在只在**同一个现有结构上**引入新的观察关系：七类认知责任S1–S7、五种项目逻辑视图N-G/N-K/N-D/N-C/N-V。权威内容按[Blix实际映射](../docs/project/cross-layer-anchor-map-20261113.md#7-2026-11-13-全面术语引入后的结构收束不是加更多标签v02)和[ai-d通用概念与严格区分](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#11-2026-11-13-体系收束从关键词集合走向可解释可验证的项目关系v02)分别维护，不复制成第二套本体。

| 七项能力 | 在既有知识/业务结构中的落点 | 关键关系 |
|---|---|---|
| S1方向保持 | GOAL/EVOLUTION/EVIDENCE；G0–G4和O1–O6 | derives_from、requires、changes_decision |
| S2结构理解 | DEPTH/DOMAIN/KNOWLEDGE_OBJECT/SEMANTIC/ECONOMIC；D01–D12 | broader/narrower、semantic_match、applies_to |
| S3映射对齐 | SEMANTIC/KNOWLEDGE_OBJECT/EXECUTION | semantic_match、implemented_by；不能将近义误认同一身份 |
| S4双向追溯 | GOAL/EVIDENCE/TIME/EXECUTION；D1–D5 | derived_from、observed_economic_event、tested_by |
| S5契约约束 | SEMANTIC/ECONOMIC/EXECUTION/EVIDENCE；权限和数据边界 | applies_to、implemented_by、tested_by；禁止从UNKNOWN越级 |
| S6证据保障 | EVIDENCE/ECONOMIC/TIME/EXECUTION；D9、O5 | supports、contradicts、tested_by |
| S7运行演化 | EVOLUTION/GOAL/TIME/EXECUTION/EVIDENCE；O6 | revised_from、changes_decision |

**五张网络只表达不同视图**：N-G目标、N-K知识、N-D数据事实、N-C工程、N-V验证反馈；跨图连接优先落在**能改变判断的具体主张**和“有实际输入/输出的运行收据”，不能凭文件提到同一关键词就建立强技术依赖。对一项变更只查有证据的上游/下游，未核消费者标REVIEW_CANDIDATE，不将推测写为DIRECT_IMPACT。

**机器可读但仅静态**：原[DOMAIN-MODEL.v1.json](DOMAIN-MODEL.v1.json)的cross_axis_alignment原位补充interpretationCapabilities和networkViews，保留原十轴十一关系及schema_version，现有只读命令 npm run audit:knowledge-trace -- --axes 能报告这些结构；[知识追溯测试](../test/knowledge-lineage-trace.test.mjs)新增结构兼容与术语映射断言。**这只验证模型文件的内部一致性，不证明AI理解、实际动态影响分析或主网调查。**

**知识增加却不提升价值的风险修正**：若新增锚点没有改善某个O1–O6目标的正确判断、遗漏提醒、真实数据或测试覆盖，就不继续扩术语/轴/表；借鉴Doorstop（需求追溯）、OpenMetadata/DataHub（语义与下游血缘）、OpenLineage（Run/Job/Dataset）、NASA/OMG（双向追溯）、W3C PROV/SHACL（来源与约束）、ADR（设计依据），按场景选择，不同时部署全套成品。详细外部依据和反例只在两个权威正本维护。

## 2026-11-13｜知识映射进入实际P1/P2产品后的纠正

前文的2026-11-06快照只代表**当时**的静态知识整合；当前 Draft PR #23 已有若干可执行离线专业能力。新事实请优先读取 [P1/P2 12领域 × 源码 × 反例清单](references/p1-p2-knowledge-reconciliation-20261113.md)，再回原领域正文，不能将旧“尚未修改业务代码”当成现时结论。

- D01/D10：既有经济证据SQLite、签名/指令索引、分页与UNKNOWN；不是全版本Solana交易完整事实。
- D04–D07：Token Transfer图、钱包可观察gross/net、分发候选、局部历史快照、跨Mint重复地址；不是SOL funding整图、真实库存、控制权、动态在线监控。
- D08/D09：仅在可信时间/报价/完整纸面成交收据下审核模拟可跟随性；没有实际或样本外盈利结论。
- D11/D12：原先按需知识已出现带版本来源的本地选择器和离线反例，仍需模型使用效果A/B评估。
- 旧Hermes阈值、qb同源与全退标记、meme-结构语义、外部产品标签仍按**来源候选**保留，必须用当前原始签名/账户/覆盖和竞争解释核对。

这些是对旧交叉表的**时间版本升级**，不是重新划分D01–D12、修改原始152单元的状态或新增一套知识路由制度。


## 一、唯一主体、两种截然不同的知识

- **Blix 原生知识优先**：产品需求、已有 UI/API/模块/数据库/部署/故障/测试，以当前 `blix` 为事实真源；旧Grok不应替代本地数据语义或现有功能。
- **旧 Grok 专业知识补充**：以 `main` 早期卡/快照/只读方法 + PR14领域研究 + PR16工程证据 + PR17集成经验为来源。保留原文件及commit/blob信息；旧研究的“专家”“层级”“阶段”不等于Blix必须再建的工程组件。
- **知识被收录和能力被激活是两件事**：完整保留、能够检索 ≠ 被模型正确理解；源码存在 ≠ 可运行；运行 ≠ 已验证真实经济解释。

## 二、旧 Grok 的12领域怎样归到 Blix 既有分类与产品位置

| 旧研究域 | Blix 现有知识主类（允许跨类引用） | Blix 当前业务/代码入口 | 迁入时采用什么形式 |
|---|---|---|---|
| D01 链上协议 | `foundations` | `solana.js`、`coin.js`、`holderslive.js`、事实检查 | 原文保留+协议最新版本核验，错误单位/账户归因转测试候选 |
| D02 发行生命周期 | `foundations` / `mechanisms` | `engine.js`、`launchlab.js`、`creator.js`、`coin.js` | 按发行程序、迁移和多池含义与原生业务关联 |
| D03 微结构与价格 | `mechanisms` | `candles.js`、`quote.js`、`pumpswap.js` | 经济解释和计算前提，不把模型形态当利润 |
| D04 钱包行为角色 | `methods` / `mechanisms` | `wallets.js`、`wtrack.js`、`walletpage.js` | 角色调查法、来源与选择偏差；旧GMGN标签只作候选 |
| D05 资金组织/主体 | `mechanisms` / `methods` | `bubblemap.js`、`wallets.js`、`coin-flow.js` | 资金/手续费/LP/服务边区分，保留替代解释 |
| D06 筹码和库存 | `mechanisms` / `foundations` | `holders.js`、`holderslive.js`、`coin.js` | 供应分母/Owner/Pool/可售与总库存分层 |
| D07 行为时序与跨币 | `methods` / `cases` | `wtrack.js`、`journal.js`、`notify.js` | 连续观察、成员变化、历史缺口和事件时间区别 |
| D08 策略及未知机会 | `mechanisms` / `cases` | `research.js`、`triage.js`、`brain.js` | 仅研究候选与反证，禁止把旧Alpha推论直升交易信号 |
| D09 执行与风险 | `foundations` / `mechanisms` | `quote.js`、`fee-ledger.js`、`price-sanity.js` 等 | 为研究提供价格冲击、费用和可交易性语义；现阶段不执行交易 |
| D10 数据与工程 | `foundations` / `cases` / `references` | `db.js`、`coverage.js`、`heliuskeys.js`、`health.js` | 数据缺失、重复、限流、缓存、成本和恢复与Blix事故记录对照 |
| D11 实证与反证 | `cases` / `methods` | `test/`、`journal.js`、`research.js` | 原研究方法/负例，未来使用真实案例时核对来源与冻结时间 |
| D12 AI知识进化 | `ai` | `AGENTS.md`、`server/intelligence/`、`mcp/` | 意图→知识适用→只读事实→解释；不复制旧多Bot/阶段工作流 |

**L0 的来源、版权、冲突、证据等级、权限**跨上述所有类别执行，是知识收录标注与审查原则，不必建额外一个庞大 L0 体系。旧 `Dxx-Kxx` 编号由已有 [152项路由](../docs/project/legacy-knowledge-routing.v1.json) 保留。

## 二（增补）｜原有六类目录不够全面：吸收旧 Grok 的“专业层次＋跨域关系”

这里补足原分类仅说明“资料存在哪”的局限。完整映射已写入可读取的 [DOMAIN-MODEL.v1.json](DOMAIN-MODEL.v1.json)：沿用旧 `ontology.v1.json` 的八层、十二域和15项专业关系，另加入 Blix 的 G 目标、现成业务代码、已收录全文入口及**尚未解决的问题**。

| 旧知识层 | 该层真正有用的认识 | 本体对应领域与 Blix 现有资产 | 对 Blix 的补强价值/边界 |
|---|---|---|---|
| **L0 来源与治理** | 来源版本、冲突、适用条件、未知和权限 | `MIGRATION.json`、原始审计与来源索引，贯穿D01–D12 | 统一“已收录 ≠ 已证明”；外部许可、供应商标签、过时知识不被静默升级 |
| **L1 原始事实与时间** | 协议对象、资产转移、单位、Slot/可得时间、来源覆盖 | D01、D10；`solana.js`、`coin.js`、`coverage.js` | 重点补不同API/Holder/钱包事件的含义一致性；已存在路径不等于事实完整 |
| **L2 市场环境与价格机制** | 发币/迁移/多池、流动性、微结构与报价 | D02、D03；`engine.js`、`launchlab.js`、`quote.js` | 从只看热门、K线、涨幅转向解释市场约束与阶段；阶段边界需实证 |
| **L3 钱包、资本和库存** | 账户角色、资本提供者、行为群体、库存和跨币演化 | D04–D07；`wallets.js`、`bubblemap.js`、`holderslive.js`、`wtrack.js` | 旧Grok最深积累之一；补共享基础设施/真实控制者不可识别、历史资金边限制 |
| **L4 经济/策略假说** | 从行为结构产生可证伪的机会与风险解释 | D08；`research.js`、`brain.js`，`mechanisms/` | 研究不再只给标签，但旧FCZ、跟随等不自动进入生产评分 |
| **L5 实际执行经济学** | 深度、滑点、费用、实际退出容量和净收益条件 | D09；`quote.js`、`fee-ledger.js` | 只用于风险与价值判断，不代表允许交易 |
| **L6 实证与反证** | 冻结时点、基线、失效、负样本、跨时间验证 | D11；`test/`、`cases/`、Blix历史事故 | **横贯每个有争议的认识**，不是所有研究最终才走一步 |
| **L7 AI 知识与持续演化** | 知识选择、专家问题表征、验证、经验修订与可恢复状态 | D12；`AGENTS.md`、`server/intelligence/`、`ai/` | 借旧Grok与ai-d的知识方法；不复制22Bot/固定Skill链 |

### 基于 G2 四类用户业务的交叉覆盖，而不是只看文件数

| 业务结果 | 相关知识必须覆盖的层与领域 | 最需要深化的实际问题 |
|---|---|---|
| 全市场发现/过滤 | L1/L2/L3 + L6；D01/02/03/07/10/11 | 发行池变化、候选漏检、数据回补与异常误报 |
| 单 Mint 资金与库存调查 | L1/L2/L3 + L6；D01/02/04/05/06/10/11 | 账户Owner/Pool、真实资金边、转移/卖出、供应/库存口径 |
| 跨 Mint 群体监控 | L1/L3 + L6；D04/05/06/07/10/11 | 角色/成员随时间变化、资金接力、公共Hub和监控覆盖 |
| 经济机制与风险机会研究 | L2/L3/L4/L5 + L6；D03–D11按问题选择 | 资本预算/需求/库存/价格形成、竞争解释、真实净价值、可推翻条件 |

**共同的 AI 层**：G1-AI/L7/D12 负责自然语言目标→选择知识→调用已经授权的Blix能力→核查结果；**尚未在实际Grok云端检验**。L0来源管理与D10工程可靠性跨所有业务出现；这不要求把L0/D10/D11全文常驻在模型上下文。

### 旧层级值得吸收、需要改造和不该继承的边界

- **直接吸收**：L0–L7的专业深度、D01–D12领域广度、15项跨域依赖/反证关系、事实与推论分离、原始出处与版本证据；它们填补了“Blix只有文件类型分类”的结构缺口。
- **改造后吸收**：L7 原本包含多Bot/单Monitor方向，改为Blix单一主体＋未来Grok云电脑的可选AI协作方式；D08策略不强制先经过D05/D06/D07，是否需要由具体假说决定。
- **不自动继承**：固定P阶段、22个常驻专家Bot、无校准的同控概率/交易阈值、将多领域连边视为已证因果、把文档完整度当成运行成熟度。

**覆盖判断不能靠已迁17份就宣告全面**。当前 [DOMAIN-MODEL.v1.json](DOMAIN-MODEL.v1.json) 对每个领域保留一个主要旧知识入口、相关Blix模块与明确的未解决缺口；状态是 `SOURCE_LINKED_NO_END_TO_END_VERIFICATION`。后续吸收 Hermes、qb-、meme- 与各成熟成品时，首先看它补哪条**目标—层次—领域—问题**，已有实现则只加相应知识与反例，不创建第二套功能。

## 三、现有接收情况：别重复搬迁17份全文

2026-11-06 初批 [MIGRATION.json](MIGRATION.json) 记录**17份旧研究副本**，分类为 `foundations=2, mechanisms=5, methods=5, cases=1, ai=1, references=3`。其中旧 PR14 `knowledge/domain/` 的主要研究正文已进入Blix；一份 Hermès 00c 与一份 ai-d 知识也进入相应类型。

**已做的结构核验**：PR #14 的 `knowledge/domain/` 除 README 外共10份专业正文，均能在上述17份迁入清单中找到对应原路径；17份Blix目标文件均存在，且文件中均能找到登记的原始 blob SHA 与来源链接。这个检查证明**文件与出处的一致性**，不证明逐字对比/引用链完整，也不证明专业结论已经验证。

### 2026-11-06 补充：已处理旧 main 15张专业卡与21份快照来源

**不再是“只登记、未处理”**：已把旧 `main/knowledge/catalog.v1.json` 的15张卡**原文完整复制**为 [Blix专业判断卡](methods/legacy-grok-core-cards.v1.json)，把21份原始历史快照的来源、固定提交与原blob记录**原文完整复制**为 [历史来源清单](references/legacy-snapshot-sources.v1.json)，并在 [知识领域模型](DOMAIN-MODEL.v1.json) 中为D01–D12建立卡ID入口。已确认旧仓库21个快照文件路径都存在，但**快照本身未复制**；不能把“21个来源已确认”说成“21份全文已迁入”。

**真正新增的是表达结构**：15卡按业务条件提供所需证据、竞争解释、推断限制、下一步核查；此前17份更多是专业研究正文，二者重叠但在使用方式上互补。15卡历史状态：3项源端契约、11项旧方法、1项未经验证的策略假说；即使与Blix本地模块对应，也不是已校准规则。卡内旧 `snapshot_path` 尚未改写为Blix路径，引用全文应通过快照来源清单或旧 main 对应文件。

| 专业目标 | 本次获得的结构化知识入口 | 适用边界 |
|---|---|---|
| 市场发现、发行与安全 | `candidate-entry`、`market-lifecycle`、`token-security`、`liquidity-depth` | 热度不等于质量，流动性美元数变动不等于撤池 |
| 钱包、资金和筹码 | `wallet-roles`、`funding-graph`、`sybil-wash`、`concentration`、`deployer-history` | 地址结构不证明同控，GMGN标签需原始事实核验 |
| 原始数据与字段 | `gmgn-field-combinations`、`gmgn-raw-prototype` | 不自动绑定过时GMGN数据、旧阈值或资金服务 |
| 机制研究与反证 | `evidence-synthesis`、`research-states`、`reclaim-theory` | 证据状态≠交易建议，历史FCZ/POC不具实证优势 |
| AI可靠性 | `anti-false-completion` | 离线通过≠云端已运行≠真实市场效益 |

### 旧快照精读后的可继承与应拒绝内容（第一批）

已实际抽读旧 `main` 21份来源快照中的6份原文：`domain-contracts/handoff-schema.md`、`solana-learning/field-forensics-toolbox.md`、`solana-learning/L15-GMGN.md`、`method/anti-fake-completion.md`、`method/calibration.md`、`theory/knowledge-source-map.md`。仅记录以下有依据的处理判断，**不据此声称审完21份**：

| 历史原文 | 旧资产的优点 | Blix的接收裁决 |
|---|---|---|
| [原交接契约](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/domain-contracts/handoff-schema.md) | 分开 `evidence`、`counter_evidence`、`missing_fields`、`downgrade_reasons`、`blocker_reasons` 和状态；下游不得默默填0或删除反证 | **提炼方法**，作为Blix AI报告与未来安全工具契约的设计参考；**不复制**旧S01–S07顺序、`/root/sikk-gmgn`路径、GMGN-CLI依赖；未经校准的`confidence_score`不应假装概率 |
| [字段与链上思维工具箱](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/solana-learning/field-forensics-toolbox.md) | 不依赖平台标签的首买时间、持仓集中、资金对手、交易行为等问题模型；字段反推原则有可迁移价值 | **只吸收问题模型**。原文存在明确高风险旧断言：`<2秒基本是机器人或内部人`、共同Binance出金即`同一庄家`、`<3秒大概率同控`、`时间戳不会骗人`。这些并非经独立校准、也忽略公共基础设施与数据时间误差，**拒绝将这些阈值/控制权断言升级为Blix规则** |
| [GMGN字段组合](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/solana-learning/L15-GMGN.md) | 将流动性、市场热度、Holder、风险、钱包质量与社交作为不同维度，提出承接力、扩散力、控制力、伪装力、退出力问题 | **吸收跨维度的研究问题**，不照搬固定乘法、风险密度阈值或旧GMGN API口径；应首先查Blix现有`quality.js`/`engine.js`及原始数据 |
| [校准方法](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/method/calibration.md) 与 [反假完成](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/method/anti-fake-completion.md) | 明确“运行校准流水线≠现实世界可靠性改善”“文档≠执行/实测” | **继承验证原则**，不把Hermes专属Harness、旧程序状态当Blix已经实施 |
| [meme-来源真源地图](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-snapshots/theory/knowledge-source-map.md) | 区分项目规则、知识原文、Skill与桥接层；冲突可追溯 | **继承分离原则**；旧项目的固定文件权威等级不应覆盖Blix现有产品/证据真源 |

**关键实质增量**：本次确认“先保存来源，再按成熟度筛掉旧强断言”不是保守形式主义，而是避免把旧知识污染带入Blix的必要步骤。已有15张核心卡对同源资金、同步行为和策略假说的表达较为审慎，**应优先作为历史研究的条件化入口**；快照中的高风险具体断言则保存原文供反证，不作为默认结论。后续逐份精读其余15份快照，不按来源数量衡量知识成熟度。

**后续实质工作（更新）**：21份快照已完成首轮内容筛查；仍需要深入核验PR14的系统性研究与Hermes/qb-/meme-独有资产，重点核对实际专业增量与现有Blix知识重合，不能据此声称21份全部完成逐行验证。

本轮不会为了“融合”再次复制同一文件，也不重新生成152张知识卡。若要断言“全文迁移完毕”，应同时复核文件尾、原blob SHA、正文与迁入头部；旧源中的指令始终是历史内容，而非本分支强制指令。

**仍未被17份覆盖的主要旧资产，按原价值逐批处理：**

| 来源/资产 | 为什么要保留 | 建议动作（本轮不直接搬） |
|---|---|---|
| `grok@main/knowledge/catalog.v1.json` 15张核心卡 | 有 `mechanism`、`required_evidence`、`alternative_explanations`、`inference_limit` 等比目录更具体的知识条件 | 与已迁入的专业正文去重；**保留原JSON并将有独立方法价值的字段选入现有正文/索引** |
| `grok@main/knowledge/legacy-snapshots/` 21份快照 | 包含旧Hermes/交易研究的历史方法与状态 | 清点 SHA/许可/是否已有全文，不覆盖新研究 |
| PR14 `knowledge/system/` 多个原始索引/覆盖与专家注册表 | 包含152项、22视角、65参考资产与未研究缺口 | 现已有152路由，不重复建体系；65资产的验证状态/原始入口要保存；需要时精准读取专家原文 |
| PR14 `knowledge/transfer/` 与训练反馈材料 | 体现知识如何跨Bot/来源交接、哪些动作未验证 | 按 `ai` 或 `cases` 提炼过程经验，不复刻课程制度 |
| PR16交易解析、Mint报告与离线测试 | 有交易语义、真实缓存数据源边界与RPC429失败 | 先归到 `foundations/cases/references` 的**来源清单**，代码是否采用另行评估 |
| PR17目标、合并冲突与知识导航 | 历史工程融合尝试与误归因防线 | 只继承有价值的决策/失败经验，不重建旧Grok工作流 |
| Hermes 00b–00e、旧 Skills/learning/calibration | 深层字段→经济机制推演、角色、资金、筹码与失败经验 | 与现有 `methods/mechanisms` 去重后选最有价值原文，保留旧阈值未校准警告 |
| qb-、meme- 原项目 | 关键钱包矩阵、资金接力、FCZ/POC等机制与反例 | 后续 **分别深入审查原目录再纳入同一Blix六类**，不是另起两套体系 |
| Million/PumpTrace/Pulse/OKX/Why-Solana等 | 有成熟程序、证据/历史/费用边界，许可各异 | `references` 先收可复核**独立研究与源码链接**，未经许可核对不全量搬第三方资料 |

### 21份旧历史快照：按已定融合方法完成首轮内容筛查

**执行范围及限度**（2026-11-06）：旧 `main` 快照来源清单共有21项。本轮核对了此前剩余15项的原文标题、章节、任务定义及主要判断，与此前已做针对性阅读的6项合并，完成**21/21首轮内容筛查**；这不是逐行代码审计、独立市场复算或证明研究方法有效。全部原文继续由 [带SHA的来源目录](references/legacy-snapshot-sources.v1.json)追踪；不以目录数量冒充实际迁移。

| 来源（旧main相对路径） | 发现的内容与对Blix的独立增量 | 收录裁决 |
|---|---|---|
| `solana-learning/L05–L09.md`（5篇） | 生命周期、GMGN三类入口、安全权限、Rug形式、流动性深度；与`candidate-entry`、`market-lifecycle`、`token-security`、`liquidity-depth`四卡及既有正文大幅重叠 | **保留来源LINK**；不复制重复知识或旧Skill顺序。只在Blix的发现、Pool、Creator事实存在明确空缺时补充相应专题 |
| `solana-learning/L10–L12.md`（3篇） | 钱包角色、同源资金、Sybil与交易行为；与`wallet-roles`、`funding-graph`、`sybil-wash`、`concentration`四卡及已迁入机制正文重叠 | **保留来源LINK**，核心的角色候选/竞争解释已入库；不能把同槽/同CEX资金/Holder标签当共同控制 |
| `solana-learning/L13–L14.md`（2篇） | `evidence` / `counter_evidence` / `missing_fields` / 研究降级状态的判断方法，旧阶段最高仅PAPER_ONLY | **方法已由`evidence-synthesis`、`research-states`卡覆盖**；保留状态分离与证据缺失思想，不恢复固定交易Gate或授权 |
| `domain-contracts/wallet-roles.md`、`wallet-structure.md`、`evidence-chain.md`（3篇） | 出入参、钱包候选清单、结构关系、反面证据、降级字段及跨步骤数据契约比一般知识正文更具体 | **提炼为Blix未来报告与只读工具的契约候选ADAPT**：保留角色、来源、证据、时间、未知及失败字段；不复制旧GMGN CLI/旧绝对路径、不自动绑定旧`confidence_score`。尤其拒绝`5分钟≥3钱包=协调`、相似卖出比例=同操作者及主观0.8等未校准判断 |
| `theory/first-control-zone.md`、`structure-risk-fields.md`（2篇） | FCZ/POC/AVWAP 概念、正反表现、观察样本及解释字段；现有`reclaim-theory`和Blix`strategy-and-execution-economics.md`已有对应假说 | **保留为未经验证的理论来源LINK**，其中正/负/缺失证据字段可为机制研究提供参考，不作为可部署的控盘标签或交易规则 |

此前已针对性阅读的另外6项，继续采用 [第一批裁决](#旧快照精读后的可继承与应拒绝内容第一批)：`field-forensics-toolbox`、`L15-GMGN`、`handoff-schema`、`calibration`、`anti-fake-completion`、`knowledge-source-map`。不另建一套快照目录。

**融合判断现已固定、后续只按问题应用**：
1. **先确认目标与Blix原生能力**：相关G2业务、已有模块、已有文档及错误/空缺，不重做原产品。
2. **按 L/D 读旧来源并作去重判断**：同类知识已经由旧15卡或首批17篇准确覆盖则仅保留出处；内容独特且已审查才考虑复制原文。
3. **做三种处理之一**：`LINK`（已有覆盖/历史背景）、`ADAPT`（新颖的领域机制/方法及边界补到现有知识）、`TEST_CANDIDATE`（真实事故/规则风险可以设计离线反例）；`PROMOTE_RUNTIME`必须另经实现、测试与云电脑安全验收。误判和过时阈值一律注明`REJECT_UNVERIFIED_RULE`。
4. **以实际知识覆盖和未来业务结果收束**：每次只更新现有分类、交叉索引、来源清单；没有可验证新价值则停止，不反复创建框架、规划文档或新专家体系。

**本批结果**：21/21首轮内容筛查，19份Blix已迁入文件保持不变；15卡原文与21快照来源清单均已保留，**21快照正文仍未全量复制**。筛查结论不能代替运行时知识使用或完整业务验收。下一项价值增量应优先来自 **Hermes/qb-/meme- 未被现有正文覆盖的独有专业知识**，然后再按同样方法评估成熟参考项目。

## 三（补充）｜参考成品不能只做功能复用裁决

**阶段性纠偏（2026-11-06）**：之前采用的 `COPY / LINK / ADAPT` 分类和“同类功能已有则不重复搬”容易被误用为**停止研究**。它们只是**归档/代码复用决策**，不代表参考项目的知识已经研究透彻。全面知识研究不得受到“每次只读1–3份”“只看一个小问题”“只吸取可立即改代码的内容”的人工限制。

已实际形成 [跨项目钱包关系、资金、库存、历史深层研究](references/wallet-relations-cross-project-knowledge-20261106.md)。源码对照 Blix/Million/PumpTrace 发现：三者名义上的“钱包关系”分别偏可视化连通、候选Owner合并、类型分层与风险解释；还存在费用代付与直接出资、同Slot与同控、基础设施过滤与供应分母、15分钟展示和历史回填等不同认知问题。**只比较是否有钱包关系图会遗漏这些专业差异。**

之后对每一参考项目采取**范围覆盖与知识纵深并行**：先掌握完整业务与相关代码/文档/测试/设计变更，再按知识对象追溯原理、因果与条件、失败/反例、不同领域联系；将有增量的认识归入Blix现有专业内容。部分源码已读不等于全项目完整研究；暂不复制代码不等于放弃研究该项目的知识。不能把新增知识强行限制在旧D01–D12，必要时提出专业领域扩展并说明与目标G0–G4的关系。

## Hermes×qb-×meme-×ai-d：不能被文件归档和旧标签限制的纵深认识（2026-11-06）

**新成果**：[Hermes多维度、异常与逆向机制纵深研究](methods/hermes-reverse-discovery-deep-study-20261106.md)，依据Hermes 00b/00c/00d/00e及部分37L1/16L2研究、qb原报告Python、meme原术语和反证文档、ai-d跨行业问题表征，以及认知科学、统计多重检验、取证来源等原始资料。既保存[00d原文](methods/hermes-multidimensional-reasoning-original.md)、[00e原文](methods/hermes-reverse-discovery-original.md)，又逐项区分其探索思想与旧身份/交易阈值断言。

**重要的补全与矛盾**：
1. `00c` 从要解释的市场事实反推数据；`00d` 换研究维度发现新对象；`00e` 从异常反推原框架尚未想到的问题。三者可以双向触发，不应串行强制或合成一张“已知模式”标签表。
2. qb-原脚本真正稀缺的不是E4/R2钱包评级，而是**关键钱包×Token/SOL来源×基础设施上下文×未来复查计划**的完整调查产品。原脚本Top25筛选、`or 0`缺失口径和供应商标签直接升级身份仍有信息丢失风险。
3. meme-的“非例/误判/事前规则/失败样本/消融”使Hermes的开放异常发现不沦为事后编故事；未经验证的FCZ/策略名不进入Blix默认交易判断。
4. ai-d的跨学科视角应按**问题需要的独立信息价值**调用，不是同时召集固定多行业专家；链上法证、经济微结构、网络识别、异常统计、认知科学、软件证据的差异在于各自提出的可区分问题。
5. 不急于分类或宣告“重复”，也不以`D01–D12`和六类目录限制新发现：新异常可保留为未解释对象并提出竞争假设，待证据与专业机制成熟后再完善主体知识定义。

**当前未完成**：00b字段当前GMGN契约逐项验证、37L1/16L2所有推理链逐条跨源反证、Hermes grill-sessions/Skill4的设计演化、qb报告每列真实数据合约与遗漏调查、meme多方案失败样本实证、模型实际按需调用质量验证。后续继续沿[深研报告第八节](methods/hermes-reverse-discovery-deep-study-20261106.md#八下一轮最有价值的研究从方法进入可区分机制的证据链)的相互关联主题深化，而不是再创建一套知识等级。

## 四、真正融合时的低成本做法

**从内容而非旧目录名出发**，选择以下处理之一：

1. **Blix已有同类功能时，仍须深入学习参考项目的知识** → 对照原问题、设计取舍、事实语义、经济模型、反例、代码、测试及历史失败。确属重复的**代码或正文**可以不再复制，但不同的专业认识与更成熟的论证仍应纳入或修正 Blix。不能以“已有类似功能”为停止研究的理由。
2. **旧 Grok有成熟理论、没有验证成品** → 归为 `mechanisms` 或 `methods`，保留原始理由、条件、冲突和真实验证状态；不冒充可执行脚本。
3. **旧项目有真实重要案例或失败** → `cases` 优先保留签名/时点/来源、错误解释与反证，不把案例归纳直接提升为规律。
4. **外部成熟项目提供更完整流程** → `references` 记录其代码路径、许可证、数据依赖、实际覆盖、与Blix现有实现差异，先决定复用知识/接口/算法/整体，不预设复制。
5. **ai-d提供AI通用方法** → `ai` 记录问题表征、知识适用、信息价值、持续纠错，不把它当第二个产品或强制多Agent。

**知识类型和使用范围不同**：专业观点可以先纳入Blix文本库供按需研读，实际代码优化等到真实任务指出缺口时再做。这符合“只用Blix一套产品、先梳理再建设”的目标。

## 五、当前整合结果与检查标准

- **已完成**：Blix自身产品知识的独立地图、旧Grok(main/PR14/PR16/PR17)的分版本目录地图、六类型与12域对应、17份迁入资料的来源清单复用及待补资产判定。
- **未完成**：旧Main快照的逐行独立验证、PR14/16/17尚存系统性与工程资产的去重、Hermes/qb-/meme-独特知识提炼、成熟参考项目深审、真实运行时知识检索与AI质量实证。
- **不执行**：不启动Blix、Grok云电脑、签名/交易/支付、真实供应商接口，不将旧CLI或历史Bot原样安装。
- **下一轮执行顺序（更新）**：已有15卡和21快照首轮检查完成 → 从Hermes/qb-/meme-原目录提炼此前未覆盖的独有方法或反例 → 检查成熟参考成品独有的专业经验 → 确有原创实质内容才归入Blix原有六类并更新 [MIGRATION.json](MIGRATION.json)；不以复制文件数作为进度。

> **统一判定**：Blix的“知识体系”不是纯文档库，而是 **它自己已运行代码所表达的事实与规则 + 原始工程经验 + 分类迁入的专业研究 + 明确的证据和限度**。旧Grok是专业来源，不是Blix的新架构。

## 2026-11-06 对旧“按Blix缺口研究”的限定修订

此交叉表是**知识理解之后的产品映射工具**，不是参考项目的阅读过滤器。独立原始研究见 [source-knowledge-deep-study](references/source-knowledge-deep-study-v0.1.md)；逐来源文件树与阅读进度见 [source-coverage](references/source-coverage-v0.1.json)。完整研究包含原本目标、概念、源码、测试、经验、未知问题；即使目前Blix无法应用，也保留在原来源，待未来证据修改认识。代码融合仍要遵守安全/许可/成熟复用约束；未验收的新机制仍标为候选。


## 2026-11-13｜多轴层级互联：目标、概念、知识、证据、经济机制、实现与验证

> 本节复用现有 DOMAIN-MODEL.v1.json 中 G0–G4 目标、L0–L7 深度、D01–D12 领域、六类文件用途和来源/证据/时间轴，以及已有知识生命周期主文和P1–P2核查账。不是新的层级树、专家制度或运行时状态机。以下跨层结果是已检查资料的分析推导，未经真实模型A/B或主网归因验证。

### 1. 不同“层级”属于独立维度，而非一条单向阶梯

| 维度 | 已有对象 | 核心提问 | 易错提升 |
|---|---|---|---|
| 目标 | G0–G4、V-A–V-F、参与者潜在目标 | 为什么研究、为谁解决什么问题？ | 把AI推测的庄家目标当作用户授权/事实 |
| 概念 | Token Account、Owner、authority、fee payer、Pool、经济主体、库存 | 哪一种对象，和什么相同/相关/不同？ | 同一地址=同一人；收到Token=完成卖出 |
| 专业深度 | L0–L7，L0治理与L6反证横贯 | 观察→机制→策略→执行，哪些升级有证据？ | 命名某机制便声称真实控制/利润 |
| 专业领域 | D01–D12 | 哪种知识解释该问题，其他领域如何制约？ | 只看资金网络，忽略微观结构、数据质量与执行 |
| 知识生命周期 | SOURCE、OBSERVATION、CONCEPT、CLAIM、METHOD、CASE、IMPLEMENTATION、EVALUATION、REVISION | 已获取、理解、承接、使用、验证到何种程度？ | 文件已迁入=模型已掌握/真实可用 |
| 时间/数据 | event_time、first_available、capture、decision_cutoff、outcome_window、知识版本 | 何时发生、何时可知、何时可行动？ | 历史回补=刚发生；事后买入价格=可跟价 |
| 实现/权限 | 原Blix代码/UI、PR23只读工具、SQLite、模型、CI | 真实执行了什么、允许做什么？ | CI绿灯=生产正确；知识文档获得交易权限 |
| 证据/效果 | RPC、原源码、作者声称、合成测试、主网、模型A/B、样本外 | 什么成立、强度与适用范围怎样？ | 将相关性、论文陈述、纸面收益升级为因果与Alpha |

**连接策略**：保留不同维度的独立身份，一次具体调查按信息价值关联少数必要元素；不要求所有G×L×D×状态格子都被填满。

### 2. 三组关系不能被当作同一种“边”

- **概念语义关系**：上位/下位、相关、近似、同义。Token Account Owner与最终经济受益人相关，但不等价。借鉴 [W3C SKOS](https://www.w3.org/TR/skos-reference/)；多语言关键词只对齐含义，不凭翻译做金融归因。
- **推理与来源关系**：从原交易、源码、作者主张到结论，记录支持/反驳/假设/失效边界。借鉴 [W3C PROV-O](https://www.w3.org/TR/prov-o/) 的实体/活动/主体及修订关系，与 [Toulmin论证模型](https://owl.purdue.edu/owl/general_writing/academic_writing/historical_perspectives_on_argumentation/toulmin_argument.html) 中证据、结论、推理桥梁、限制与反驳。
- **工程执行关系**：输入、程序、这次运行、输出、测试和授权必须拆开。借鉴 [OpenLineage](https://openlineage.io/docs/spec/facets/) 的Job、Run、Dataset区分；源代码存在不代表特定数据已运行过，运行成功也不等于解释正确。

**不可隐式升级的边**：shared funder→same controller；same slot→Jito bundle；Token transfer→Swap sell；gross/net transfer→现存可卖库存；重复地址→同一经济受益人；纸面Pnl→真实跟单超额收益；知识被选中→模型正确理解。

### 3. 一条实际调查如何穿透现有层

用户问题：“A买入、Token转到B、B后来出现卖出，是分仓出货吗？还能跟单吗？”

| 层级连接 | 证据和调查 | 当前有意义的结果 |
|---|---|---|
| 用户目标G2-MINT / L0 / D10 | 锁定Mint、钱包与时间窗口，授权只读；确定RPC源与覆盖 | 明确调查对象；缺历史不能解释为0 |
| L1 / D01：可观察事件 | Token Account、Owner、sig、outer/inner CPI、slot、raw量、Token-2022手续费 | 确认的仅是特定Token转移，不是同控 |
| L2 / D02/03：市场环境 | bonding curve/毕业/多池、LP、路由、价格和可成交深度 | 排除部分公开服务与市场共同原因；未有原始Swap不得冒充出货 |
| L3 / D04/05/06/07：经济结构 | B后续卖出摘要、SOL直接出资、Fee Payer、库存来源、跨Mint重复 | “随后观察到卖出”与“出售刚收Token”是不同命题；身份UNKNOWN |
| L4 / D08：竞争机制 | 分仓、普通转仓、托管、做市、池子或公共路由的不同可区分证据 | 产生优先补查的签名/余额/业务路径，而非硬标签 |
| L5 / D09：跟随执行 | 发现信号首次可见、两侧报价、费用、延迟、失败样本、退出 | 原钱包盈利不等于跟随者可复制的净利润 |
| L6 / D11：反例与对照 | 同Slot正常热门币、公共Hub、历史回补、Token2022复杂CPI、盲审样本 | 找出哪条解释被推翻；不会因反证不存在就夸大 |
| L7 / D12：AI能力 | 按具体问题检索D01/D04/D05等知识、解释限制、决定下一项补查 | 当前仅局部离线代码与知识路由；模型正确选择仍待A/B |

### 4. 从跨层连接新产生的认识（假设与已知范围分开）

1. **账户动作≠经济角色**：同一地址可先后扮演接收、路由、托管、手续费支付等角色，必须按事件/时点标角色，主体归属另外取证。这会改善Wallet分类而不需要新增一套专家团队。
2. **多项相似信号可能是同一个公共原因**：同槽、相近成本和共同服务钱包可能都来自同一个热门发行事件，三者不是三份独立同控证据。优先比较不同Mint、非公共服务的重复关系。
3. **多跳gross≠独立需求或库存**：A→B→C可能重复累计同一Token，必须把Token流、真实Swap对价、LP、池库存与可卖余额分开，不把资金关系图当真实PnL。
4. **数据可见时间是市场机制判断的一部分**：前12小时转账激增可能是事前资本准备、做市/派发，也可能是事后回补/采样变化。事件、首次可见、采集、决策时间必须对齐。
5. **领先钱包优势不自动传递给观察者**：原钱包执行时点与用户收到信号、有效quote及成交时点不同。应把“可观察→可复制→费用后盈利”分开验收。
6. **知识会随市场/协议/来源变化失效**：撤回旧研究数字、供应商数据合同变更或发现公共设施，应该影响下游AI片段、风险标注、测试和候选排序；不静默覆盖原来源。

### 5. 会得到的五类可检查产物

- **概念消歧**：自然语言“捆绑”“刷子”“庄家”“跟单”能触发不同专业问题，而不是提前固定单一标签。
- **纵向主张证据链**：从一个报告主张追到原RPC签名+指令位置+归档SHA、源码路径/版本、所用专业方法、合成测试与未覆盖情况。
- **横向竞争机制图**：同一发现联系协议、库存、价格、参与者激励、数据工程与替代解释，产生更有鉴别力的下一次补查。
- **局部修订与依赖影响**：若发现共享交易所资助，降低对应关系归因，同时保留已观察转账，检查下游聚类、报警和策略是否错误继承旧解释。
- **产品与模型能力对照**：同任务、同Mint、同工具和预算，比较原Blix、按需知识AI、改进知识路由的事实准确率、错误提升、未知状态、任务成本和误报漏报。

### 6. 启停标准与实际边界

跨层联系的价值不由新增术语数量决定。只有产生不同的问题、能区分竞争解释的新证据、可测试的产品行为、可追责的知识修订或更好的真实任务表现，才有增量。来源仍未审的继续保持未审；不把所有理论强迫转换代码，不用新框架重复原 DOMAIN-MODEL。

**当前真实状态**：G/L/D与生命周期结构已存在；PR23离线经济图和证据链逐项推进。主网完整历史、公共服务归因、Coin页面运行、真实模型A/B及跟单样本外效果未完成。跨层映射本身是分析成果，不是这些缺口的运行验收。


### 7. 2026-11-13 关系型认知修正｜从层级清单到可审查的专业主张

**已有层级不变，新增的是跨轴关联的解释契约。** [`DOMAIN-MODEL.v1.json`](DOMAIN-MODEL.v1.json) 的 `cross_axis_alignment` 将原 G0–G4（目标）、L0–L7（知识深度）、D01–D12（专业领域）与概念、知识对象、经济事实、证据、时钟、工程执行和反馈演化明确为 **10个互不替代的观察轴**；这是结构说明而不是额外10层软件、10个Bot、自动推理图数据库或每任务强制10步。

**与上轮提出的七类视角怎样对齐？** 七类是便于理解的**研究视角**，十轴是把交叉依赖拆细后的**审查坐标**，不是“七层升级十层”，也不是两个竞争知识体系；可多对多映射：

| 上轮七种观察视角 | 对应现有十轴 | 不能混淆的地方 |
|---|---|---|
| 概念与语义 | `SEMANTIC` + `KNOWLEDGE_OBJECT` | 同义/近似、专业概念、具体主张分开 |
| 知识与认知 | `DEPTH` + `DOMAIN` + `KNOWLEDGE_OBJECT` | 知识深度不保证来源可靠；同领域有竞争解释 |
| 现实对象与经济机制 | `ECONOMIC` + `TIME` | 地址/账户/经济受益人、转账/卖出及发生/获知时间分开 |
| 证据与可信度 | `EVIDENCE` + `TIME` | 原事实、作者说法、推论、CI、主网验收分开 |
| 业务与决策 | `GOAL` + `DOMAIN` | AI提出的新问题不自动变成用户授权 |
| 工程与执行 | `EXECUTION` + `EVIDENCE` | 代码、调用、测试和真实服务结果分开 |
| 演化与治理 | `EVOLUTION` + `GOAL` + `EVIDENCE` | 修订具体主张，不篡改源数据/用户目标 |

这层对应是**可交叉、可不选、可被证据修正**的观察关系，不设置“一旦进入L3必须先做L1–L2”的固定阶段；研究价值来自跨轴发现新问题并证伪，而不是强制填满全部单元。

**真正的连接单位优先是“会改变判断的专业主张”**，不是“某文件里有一个关键词”。同一条主张可以链接多种对象，各边有不同的证据门槛：

| 对齐问题 | 应当连的两端 | 正确关系类型 | 不允许越级 |
|---|---|---|---|
| 这个普通词是不是专业术语？ | 用户表达 ↔ 专业概念及其上下位 | `semantic_match` | “相近”不等于经济身份相同 |
| 结论从哪里来？ | 主张 → 原文件版本或原交易 | `derived_from`；具体证据 `supports` 或 `contradicts` | 两份转述同源报告不等于独立验证 |
| 该认识适合这个Mint吗？ | 方法/主张 → 数据、钱包角色、费用、观察窗口 | `applies_to` | 旧Hermes阈值不能变成普适规则 |
| 哪段代码体现了它？ | 方法/主张 → 已存在的Blix文件与输入/输出 | `implemented_by` | 编码完成不等于真实主网有效 |
| 哪次执行检验了它？ | 实现 → 测试、具体Commit、真实运行 | `tested_by` | 合成CI不等于实盘交易或全历史 |
| AI确实用了它吗？ | 版本化知识片段 → 真实任务轨迹/模型判断 | `selected_for_context` | 允许加载不等于选中，选中不等于用对 |
| 新证据如何纠正？ | 反例/新观测 → 原主张、下游判断、实现测试 | `changes_decision`；`revised_from` | 不能篡改原始记录或自动提升权限 |
| 钱包A向B转账 | 原始签名/指令 → Token账户与Owner及金额 | `observed_economic_event` | Token流动不等于Swap卖出、同一控制者 |

#### 7.1 同一个问题如何穿透层级而不混同证据

例如用户问“**A转Token到B，B后来卖出，是庄家分仓出货吗？**”

- **现实事实（D01、L1）**：找到 `sig + outer_i + inner_i + mint` 对应的转账、Owner、原始数量与时间，区分池/程序；如可查，记录原RPC归档哈希及来源。这里只能确认**捕获到的特定转账**。
- **经济机制（D04–D07、L2/L3）**：接收钱包后续有卖出摘要仅是时序候选；需验证卖出对应的Token库存、Swap对价与先前持仓；也必须比较托管、做市、公共设施、普通转仓等解释。
- **数据时间（D10）**：Slot事件时间、历史首次可见、归档采集、用户实际得到信号时间分开；“新补查”不得解释成“刚发生”。
- **方法与业务（D08/D09）**：即使原钱包盈利，跟随者的可见信号/报价/滑点/成交能力和样本外净收益仍须独立验收。
- **程序/验证（D11/D12）**：当前 `server/economic-events.mjs`、`server/intelligence/economic-network.mjs`、`test/economic-network.test.mjs` 能证明**特定离线固定样例下的转账关系行为**，不证明真实控制权；`local-knowledge-loader.mjs` 只提供有来源的参考材料，不能将模型文本直接提升为链上事实。
- **反馈和局部修订**：若后续证据显示B属于公共池，保留真实转账，但降低/撤销“私有分仓”候选；查哪些图谱、报告和知识引用依赖了旧判断，必要时更正对应代码/测试，不改变未受影响事实。

由此形成的**新认识是带前提的专业调查候选**：例如跨钱包活动可能涉及不同经济角色，单看单钱包买卖方向会漏掉接收方。新认识本身必须有可区分的证据或反例，不能直接宣称找到了庄家或稳定交易机会。

#### 7.2 防止知识越积越多却越来越不准

- **文件级来源、主张级证据、一次模型调用、程序实现、真实运行是五张不同账**，不可合成一个百分比。当前 152个旧单元只做了文件级144映射、8历史索引；11本地候选源不等于11条已验证模型能力。
- **知识关联的产生不要求立刻实现**：可能是术语澄清、竞争解释、新调查目标、测试、现成程序复用、原位知识修订；不强迫所有理论转交易算法。
- **横向关联不能无限扩张**：相同Mint、相同资料和固定时间截点下，若增加关系没有改变可检验事实、重要未知、错误率、成本、补查选择或用户可理解的判断，则标记“仅有关联，暂无业务增量”，停止重复扩张。
- **授权属于用户/系统边界而非知识边界**：图谱节点、旧专家指令、外部README和模型上下文不能授予签名、交易、付费或发布权限。
- **真正需要A/B的是实际使用效果**：原Blix事实基线 vs 有限相关知识 vs 多层关联解释，比较事实误报/漏报、完整历史、关键未知发现、补查是否有用、时间和费用。模型写得更长不是成功。

**验证入口**：`npm run audit:knowledge-trace -- --axes` 输出当前结构轴、关系类型和禁止越级的校验口径；旧 `--unit` / `--target` 保留文件级双向来源核查。这个工具不会自动推断同控或运行真实模型。所有可证伪结果继续登记在现有 [建设台账](../docs/project/build-register.md)，不另开“层级项目”。


## 2026-11-14｜旧 Grok × Hermes 的“纠偏机制”源码复核：不是重复移植整套工作流

**取证基线**：旧Grok `sunshihao001/grok@main` [fa10e491](https://github.com/sunshihao001/grok/tree/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a)；旧Hermes `sunshihao001/-@main` [2bf694b3](https://github.com/sunshihao001/-/tree/2bf694b37cce25b4a3c9364298b784039f3ecc84)。以下区分**源码实现、文档约定、历史运行报告、Blix是否已有机制**，与旧快照/卡片/本文件现有纵深知识不重复复制。

| 重要纠偏能力 | 旧原项目中可核对的具体机制 | 对当前Blix的可复用判断与不应继承项 |
|---|---|---|
| **判断时点校准/防前视** | [Grok research.py](https://github.com/sunshihao001/grok/blob/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a/src/solana_meme_os/research.py) `evaluate_observations` 拒绝缺source_ref、缺观察/可得时间以及决策时点尚不可得的资料；[test_research.py](https://github.com/sunshihao001/grok/blob/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a/tests/test_research.py)有合成负例 | 作为O1/O5最早可见与可跟随性契约反例；先对照已有followability-replay与source-readiness，不另写一套交易时钟检查器；此处验证输入一致性而非真实供应商时效 |
| **观察状态隔离及可恢复监控** | [Grok monitor.py](https://github.com/sunshihao001/grok/blob/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a/src/solana_meme_os/monitor.py) 要求live与fixture不共用状态、live不能过时或未来、只接受新时点，原子替换状态并附带source/ref；[test_monitor.py](https://github.com/sunshihao001/grok/blob/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a/tests/test_monitor.py)核部分边界 | 用于O6监控与恢复负例；Blix当前已有原生source/SQLite/签名游标，不搬Python monitor，也不把原子写文件误认为全网漏包已补全 |
| **问题表征、竞争解释与反证** | [Grok knowledge/method.md](https://github.com/sunshihao001/grok/blob/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a/knowledge/method.md) 把“Top10集中上升”与“庄家吸筹”拆开，并要求竞争假说、新证据判别、证据不足不升级结论；[knowledge.py](https://github.com/sunshihao001/grok/blob/fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a/src/solana_meme_os/knowledge.py)输出来源绑定的追问而非交易信号 | 继承到O2–O4知识选择与AI只读解释；并与现有owner/库存批次UNKNOWN检查对应，不把15历史卡片当封闭机制全集 |
| **来源缺失责任与业务降级** | [Hermes missing_data_policy.md](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/docs/missing_data_policy.md) 区分严重度、source_skill/source_command/recovery_action/decision_impact；[phase_state.py](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/skills/common/phase_state.py)保存阶段与恢复入口 | 将“缺什么/谁负责补/何时重审/影响哪个业务主张”沿现有Blix源/解析/AI层传递，不复制固定S01–S07流水线或并行钱包游标 |
| **测试错误归因，而不是错误修业务代码** | [Hermes pytest_failure_attribution.md](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/pytest_failure_attribution.md)记录多模块共用`run`导入导致整套pytest假失败，原报告将错误归于测试隔离并安排修正；[pytest_baseline_after_fixes.md](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/pytest_baseline_after_fixes.md)记录13 passed | 属于跨层纠偏RCA的正例：先区分测试环境/源/解析/逻辑/业务，不因CI红即篡改钱包判断。历史报告不是我们本轮重新执行pytest |
| **契约与实现互相校验（旧负例）** | [Hermes handoff contract](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/docs/cross_skill_handoff_contract.md)要求保留`counter_evidence`与`missing_fields`；但[meme-evidence-chain/run.py](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/skills/meme-evidence-chain/scripts/run.py)当前计算时`counter_evidence_count:0`为常量、基础`counter_evidence:[]`未被填入，`calculate_confidence`由0.8基数及固定加减得出，未见样本校准 | **不能搬旧置信度、旧控制者阈值或反证完整性主张**；把“宣称有反证但实际输出空/数值置信度未经校准”作为数据契约与报告反例测试的候选 |
| **门控过度保守也需纠偏** | [Hermes历史batch 4币分析](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/batch_20260526T123011Z_need_more_data_analysis.md)记录4币都NEED_MORE_DATA，并将候选原因列为SM证据空、行为UNKNOWN、结构风险高、门控阈值；不能单凭此证明市场实际没有机会 | 对O5同时检查“证据不足/规则太严/上游解析不足/来源缺失”几个竞争解释，不能为减少UNKNOWN放松真实风险，也不能用全部UNKNOWN冒充慎重有效 |

**此次跨项目收束的真正新增认识**：Grok的**意图/证据时间/反证**与Hermes的**交接责任/状态恢复/失效归因**构成互补；Blix已有的源/经济/知识/AI能力应沿现有S1–S7、O1–O6和单一数据源责任实现，不引入旧Hermes硬编码S01–S07阶段、3终端审批制、未校准分数或交易接口。尤其应以**文档契约→实际源码→测试负例→可观察输出→反向修订主张**检验旧参考，而不止把旧文档当权威。

**证据等级与下一步**：本轮为旧Grok/Hermes **历史源码+文档+离线测试存在性+历史报告审查**，未重新运行完整旧Hermes、未验证其2026-05历史批次链上真实性、未证明旧评分模型有效；不是Blix上线效果。后续优先在现有Blix evidence/AI只读报告测试上审“反证字段真有内容还是仅存在结构”“缺失源责任是否传给下游”“真实可得时点是否被满足”，只对确有缺口的位置做有限修复。
