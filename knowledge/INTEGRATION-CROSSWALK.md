# Blix 原生知识 × 旧 Grok 知识：对应、去重与收录清单 V0.1

> 2026-11-06 | 本文件严格依据 [Blix 原生体系](BLIX-NATIVE-ATLAS.md) → [旧 Grok 原体系](OLD-GROK-ATLAS.md) 的阅读顺序，之后才作接收裁决。**不变更业务代码、不安装Bot/依赖、不运行网络或交易。** 现在的结论是知识与功能的映射，不是已完成的AI主动调用。

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

**剩余实质工作**：21份快照逐项判断何者提供17份正文和15卡没有涵盖的独立知识，优先看`handoff-schema`、`field-forensics-toolbox`、`calibration`等；随后核验PR14的系统性研究与Hermes/qb-/meme-独有资产。未发现独立增量的内容保留来源不重复复制。

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

## 四、真正融合时的低成本做法

**从内容而非旧目录名出发**，选择以下处理之一：

1. **Blix已有完整同类能力** → 在现有本地知识/代码说明里加入来源和反例；不复制另一套业务规则。
2. **旧 Grok有成熟理论、没有验证成品** → 归为 `mechanisms` 或 `methods`，保留原始理由、条件、冲突和真实验证状态；不冒充可执行脚本。
3. **旧项目有真实重要案例或失败** → `cases` 优先保留签名/时点/来源、错误解释与反证，不把案例归纳直接提升为规律。
4. **外部成熟项目提供更完整流程** → `references` 记录其代码路径、许可证、数据依赖、实际覆盖、与Blix现有实现差异，先决定复用知识/接口/算法/整体，不预设复制。
5. **ai-d提供AI通用方法** → `ai` 记录问题表征、知识适用、信息价值、持续纠错，不把它当第二个产品或强制多Agent。

**知识类型和使用范围不同**：专业观点可以先纳入Blix文本库供按需研读，实际代码优化等到真实任务指出缺口时再做。这符合“只用Blix一套产品、先梳理再建设”的目标。

## 五、当前整合结果与检查标准

- **已完成**：Blix自身产品知识的独立地图、旧Grok(main/PR14/PR16/PR17)的分版本目录地图、六类型与12域对应、17份迁入资料的来源清单复用及待补资产判定。
- **未完成**：全部旧Main/PR14/16/17逐文件深读和重叠去除、Hermes/qb-/meme-全目录逐项知识迁移、参考项目逐源码复用裁决、自动运行时检索与AI质量实证。
- **不执行**：不启动Blix、Grok云电脑、签名/交易/支付、真实供应商接口，不将旧CLI或历史Bot原样安装。
- **下一轮执行顺序**：先核对旧 `main` 15卡/21快照与当前首批17份研究正文的语义覆盖 → 收录真正未覆盖的原知识 → 深入Hermes/qb-/meme-原目录 → 再按同六类纳入成熟参考知识；每批更新已有 [MIGRATION.json](MIGRATION.json)，以来源和去重结果而非新建目录数作为进度。

> **统一判定**：Blix的“知识体系”不是纯文档库，而是 **它自己已运行代码所表达的事实与规则 + 原始工程经验 + 分类迁入的专业研究 + 明确的证据和限度**。旧Grok是专业来源，不是Blix的新架构。
