# Blix 专业知识｜唯一运行主体的分类接收入口

## 2026-11-14｜全域专业归位总入口：十二领域主述、参考来源、知识身份与产品验收

**目标**：将当前分散于旧Grok、Hermes、qb-、meme-、Why-Solana、Synapse、GMGN/OKX及其他成熟项目的知识，按照现有 `G0–G4目标 / L0–L7深度 / D01–D12领域 / K1–K9知识演化 / D0–D9工程 / O1–O6业务` **原位归属**。下表是“哪份正文负责阐述哪类专业知识”的**唯一主述导航**，不是新本体、新运行时规则或再次简写覆盖原文。跨域知识允许引用多个主述位置；原始来源和未知研究必须继续保存，不能为消除重复而丢失反例。

### 一、D01–D12专业知识完整归属：一处主述，多处证据

| 领域 / 知识深度 | 主述正文（新知识优先补这里） | 必须理解的原理、问题和过滤 | 来源与代码事实怎样分开 |
|---|---|---|---|
| **D01 Solana链上事实 · L1** | [协议、市场与来源基础](foundations/solana-chain-and-market.md#2026-11-14全域归位d01-协议事实d02-发行生命周期d10-数据可信度当前主述) | Signature、Slot、版本、ALT、外内CPI、Token2022、TokenAccount/Owner/Authority/Fee Payer、SOL/WSOL、Swap/Transfer/LP及净额；拒绝身份或经济动作越级 | [官方协议与P1/P2反证](references/p1-p2-knowledge-reconciliation-20261113.md)；`economic-events.mjs`只是已捕获子集 |
| **D02 发行与生命周期 · L2** | [协议、市场与来源基础](foundations/solana-chain-and-market.md) | 发行平台、曲线、毕业、迁移、池/LP、权限、Creator历史；“有Token”“有报价”“能出售”分开 | 原`engine/coin/creator`；Pulse、pumpwatch、PumpTrace原来源另存 |
| **D03 市场微观结构 · L2** | [价格形成与市场机制](mechanisms/market-price-mechanism-research.md#2026-11-14全域归位d03-市场微观结构的完整判断并关联d02d06d08d09) | 价格、池深、真实买卖对价、做市/刷量、库存卖压、薄池报价；FCZ/POC/AVWAP只是观察结构 | meme-理论与Blix `quote/pumpswap/quality`；不得直接复制为Alpha |
| **D04 钱包行为与角色 · L3** | [钱包角色与库存](mechanisms/wallet-roles-and-inventory.md#2026-11-14全域归位d04-钱包角色--d06-筹码库存的多维判断) | Sniper/Bundler/KOL/Dev/Transfer-in/服务钱包、First70、长期角色变化、真实买卖；分开标签、地址与控制者 | Hermes/qb/GMGN角色源；原`wallets/wtrack`，扩展仅局部 |
| **D05 资金网络与经济主体 · L3** | [资本组织与激励](mechanisms/capital-organization-and-incentives.md#2026-11-14全域归位d05-资本组织资金来源和经济主体的证据阶梯) | 入金、Fee Payer、公共Hub、多跳/Dust、跨Mint地址重合、协调行为、经济受益/控制，必须按证据阶梯判断 | Why-Solana/Hermes/Million/Synapse；Token转移图≠完整SOL资金图 |
| **D06 筹码与库存 · L3** | [钱包角色与库存](mechanisms/wallet-roles-and-inventory.md) | 供应量分母、Pool/Vault/Token账户、可卖资产、转仓、LP、同批成本、接收后卖出摘要；不能以转账当卖出 | qb/GMGN/Holder工具与`economic-claim-trace.mjs`；库存批次仍待真验 |
| **D07 市场时序/群体 · L3** | [异常与群体发现](methods/anomaly-and-cohort-discovery.md#2026-11-14全域归位d07-事件群体时序与跨mint演化的知识主述) | 6/12h、同Slot/Jito、分发push/领取pull、群体更替、回填与真实新活动、跨币时序；先基线后假说 | Synapse完整信号在来源目录；原`coverage/wallets`与快照审查各有范围 |
| **D08 机会假说与策略 · L4** | [策略与执行经济](mechanisms/strategy-and-execution-economics.md#2026-11-14全域归位d08机会机制d09跟单执行经济的统一专业判断) | 钱包先动与信息优势、机制/风险条件、研究优先级vs交易准备度、信号可见时点、样本选择 | 原`triage/research/early/brain`已存在；GMGN/Million作者演示不等于策略收益 |
| **D09 可执行性与风险 · L5** | [策略与执行经济](mechanisms/strategy-and-execution-economics.md) | 真实买卖报价/规模、手续费、滑点、优先费、MEV、失败成交、卖出深度、止损/退出、净收益 | `followability-replay.mjs`只有纸面验收；原版交易能力保留但不获AI交易授权 |
| **D10 来源/可靠性 · L0/L1横贯** | [协议、市场与来源基础](foundations/solana-chain-and-market.md) | 市场全集、供应商字段/权限、断流/429、游标、首次可见、存档哈希、缓存、跨源语义、缺样 | `sources/db/coverage`和[来源覆盖账](references/source-coverage-v0.1.json)不证明全市场在线覆盖 |
| **D11 实证与反证 · L6** | [独立检验与失败案例](cases/independent-validation-and-failure-cases.md#2026-11-14全域归位d11-证据保障反证与效果检验的统一解释) | 负例、未入选样本、幸存者偏差、真实签名/供应商回放、样本外、风险与实际测试分级 | 原始样本与CI/运行收据独立；RED-COHORT撤回数值不得重用 |
| **D12 AI推理/知识进化 · L7** | [意图与知识使用](ai/intent-knowledge-selection-and-reasoning.md#2026-11-14全域归位d12-从零散知识到主动专业判断的实际职责) | 从口语意图发现未知、选择知识/工具、竞争解释、反证、修正、停机/成本；K1–K9不变成9个Bot | ai-d为跨领域方法真源，`local-knowledge-loader`仅11主题候选；真实模型增益未验 |

**各领域不是封闭分工**：如“新钱包接收后卖出”至少贯通D01、D04、D05、D06、D07、D09、D10、D11、D12；主事实先找D01和原始签名，资金解释转到D05，库存问题到D06，是否适合跟随到D08/D09。每个领域明确自己**承担哪种推断/过滤责任**，不复制同一来源全文到十二份文档。

### 二、已有参考与历史知识应当存哪里、如何使用

| 资产类别 | 保留的独特知识范围（不是功能名表） | 来源主存放与下游连接 | 当前证据位置 |
|---|---|---|---|
| 原版Blix | 市场采集/初筛/数据持久化、钱包发现与反向Mint、Pulse、价格/质量、Paper、交易、原AI、网页与运维 | [原生能力全图](BLIX-NATIVE-ATLAS.md)、[产品能力表](../docs/project/capability-map.md)，各D主述引本体源码 | 源码已读；隔离冷启动/重启已验，不等于联网市场 |
| 旧Grok及PR#14 | L0–L7、D01–D12、152历史映射、22专家视角、原65参考资产、历史判断/反例 | [历史主册](foundations/legacy-grok-domain-core.md)、[原Grok地图](OLD-GROK-ATLAS.md)、[迁入表](MIGRATION.json)及[DOMAIN-MODEL](DOMAIN-MODEL.v1.json) | 历史研究状态保留，不能把索引记为已逐条实证 |
| Hermes | 钱包/同源/筹码/角色、资金的经济职能、00c/00d/00e多维与反向生问题、历史自纠偏 | [Hermes原文](methods/hermes-multidimensional-reasoning-original.md)、[纵深研究](methods/hermes-reverse-discovery-deep-study-20261106.md)、D04–D07正文 | 原仓树/部分关键文件深读，不是264文件全部深审 |
| qb- | 单Mint关键钱包矩阵、95钱包历史报告、分母/数据护照、角色与`full_exit`语义反例 | [P1/P2源级对照](references/p1-p2-knowledge-reconciliation-20261113.md)，D04/D06/D10/D11 | 原项目大量文件未逐项审阅，特定旧样本仅限原时间窗 |
| meme- | FCZ/POC/AVWAP、深洗、二次启动/死亡盘、机制失败判据、价格≠成本 | [D03主述](mechanisms/market-price-mechanism-research.md)、[D08/D09主述](mechanisms/strategy-and-execution-economics.md)、[Hermes×meme深读](methods/hermes-reverse-discovery-deep-study-20261106.md) | 理论与原模型不得直接变交易规则 |
| Synapse笔记 | **14/14链上信号、3/3 DEX事件、3/3买入形态、4/4 HyperLiquid主信号、5/5标签、5原则、4去噪与产品合规**；14项我们提出的延伸研究 | [保留全部原始转述分类](references/synapse-methodology-full-taxonomy-20261114.md)、[跨信号研究](references/synapse-cross-signal-mechanisms-20261114.md)；按对象引用D01–D11 | **USER_PARAPHRASE**，HyperLiquid不自动迁至Solana，未验证供应商内部阈值 |
| GMGN / OKX | 多Mint/Wallet Radar、First70、动态钱包角色与评分、PnL vs copyability、跟单执行参数、只读market skills和独立wallet/trade边界 | [GMGN与参考全景](../docs/project/reference-driven-goal-model-v0.1.md#13-2026-11-14gmgn--既有成熟产品--blix机会优先全局再整合v04)，D04/D05/D08/D09 | 官方/公开Skill语义与Blix真实接入、费用/参数、收益验收必须分开 |
| Pulse、Million、HoldTech、PumpTrace、Why-Solana | 全发行样本/失效记录，钱包↔Mint联动，Holder/同槽与公共服务反例，Creator历史与回填，多跳及样本偏差 | [外部来源入口](references/README.md)、[深度研究与未读范围](references/source-knowledge-deep-study-v0.1.md)、[来源覆盖清单](references/source-coverage-v0.1.json) | 已审部分源码/反例，不把README当实跑 |
| Cielo、Nansen、Arkham、Bubblemaps、pumpwatch、PumpGrok及剩余参考 | 通知/钱包历史、实体解释、关系图可视化、发行总体、有限Agent与任务收据；未审仍需完整保留 | [原65资产索引](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json)、[参考项目全景](../docs/project/reference-driven-goal-model-v0.1.md)、[覆盖清单](references/source-coverage-v0.1.json) | 部分未深入/未运行/商业闭源，不以命名数量冒充完成 |
| ai-d通用认知 | 普通表达→专家问题表征→知识获取/原理理解/跨源关系→实施→验收→原位修订；七类跨层能力与九阶段 | [ai-d知识九阶段](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/knowledge-lifecycle-nine-stages.md)、[Blix D12专项](ai/intent-knowledge-selection-and-reasoning.md) | 通用认知与AI运行时学会/使用正确是两件事 |

**历史原文归档原则**：原`methods/hermes-*`、`actor-economic-mechanisms-deep-study.md`、`legacy-grok-domain-core.md`、完整Synapse分类及`references`中的研究报告不删、不压缩替代；主述正文只写已理解的机制、适用条件、具体反证和使用边界。没有研究完的旧资料留在[来源覆盖账](references/source-coverage-v0.1.json)而非标“已归并已读”。

### 三、从知识到项目应用：五种身份不得混同

1. **SOURCE** 原始资料或供应商声称：保留原名、原文与版本；转述标明转述。
2. **KNOWLEDGE/CLAIM** 专业解释、竞争假说和反例：属于对应D领域及L深度，注明适用场景与不可推断范围。
3. **DATA_FACT** 可复查Signature/原始行情和时间覆盖：必须有来源、哈希/字段、时点、缺口，不能靠文本生成。
4. **IMPLEMENTATION** Blix原版或PR23的具体模块/输入输出/权限：详见[产品扩展层](../docs/project/intelligence-layer.md)，知识文档本身不启用代码。
5. **VERIFICATION** 某提交的离线测试、历史回放、联网只读（`CONNECTED_READONLY_RUNTIME`）、前瞻影子及运维：事实以[工程建设台账](../docs/project/build-register.md)为准，不将绿色CI冒充主网可交易盈利。

**正确的使用路径**：用户问题→对应G目标和O结果→Blix现有市场/钱包/归档事实→按需求查1–3个D主述与原始证据→明确竞争解释/缺失与下一项信息价值→只读报告、必要回放→新证据修订。不是固定让每个币经过12领域，也不是把11主题加载器当全部知识库。

**当前不足**：以上实现了知识**主述责任与引用归位**，没有把65个参考成品/152历史单元逐条重读、更没有把全部知识转成运行时可用规则。成品发展不靠继续扩标签，转到[扩展层成品路径](../docs/project/intelligence-layer.md#2026-11-14成品化实施主线知识已经归位之后)与[当前运行台账](../docs/project/build-register.md)进行分级验收。

**2026-11-13｜纠偏与反证新的权威入口：** [Blix全项目偏差类型、根因归属和实例验收](../docs/project/cross-layer-anchor-map-20261113.md#12-2026-11-13纠偏的专业扩写从修一处错到首个失效环节职责与全链结果-v03)对应[ai-d通用纠偏认识](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#13-2026-11-13纠偏能力的深层扩写纠错校准根因修复与学习v03)。按问题查原知识/原采集/原代码/真实反例，不能因为一次错误就否定完整理论、发明固定新流程或由AI侧复制上游源端。

**知识关系结构已收束（2026-11-13）**：[ai-d完整概念库与专业术语差异](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#11-2026-11-13-体系收束从关键词集合走向可解释可验证的项目关系v02) ↔ [Blix七类能力/五种网络/六项业务目标的实际映射](../docs/project/cross-layer-anchor-map-20261113.md#7-2026-11-13-全面术语引入后的结构收束不是加更多标签v02) ↔ [原INTEGRATION-CROSSWALK的结构归位](INTEGRATION-CROSSWALK.md#2026-11-13结构收束-v02从知识分层到七类跨层能力五种逻辑视图)。**原模型只原位增加机器可读的关系视图，不新增D01–D12/十轴/十一关系，也不启用自动推理**。运行 npm run audit:knowledge-trace -- --axes 可静态核对。

**2026-11-13｜知识进入代码后的跨层锚点：** [Blix多层锚点与变更影响实例](../docs/project/cross-layer-anchor-map-20261113.md)，对照[ai-d通用方法](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md)。这里的锚点关联专业主张、数据契约、代码不变量、测试与真实验收；并非新专家制度或重复D01–D12知识体系。初版只映射少数源级已核的高价值例子，不宣称自动全仓传播或已经生产验收。

**2026-11-13｜通用知识生命周期与业务整体重梳理**：以 [ai-d 九阶段知识形成与应用锚点](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/knowledge-lifecycle-nine-stages.md) 作为“规划→获取→接收→理解→关联→整合→转化→验证→进化”的跨项目知识工作视角；以 [Blix 全项目 V2.0 建设总蓝图](../docs/project/blix-ai-workbench-master-plan-v1-20261113.md) 为六大业务目标、已有专业资产、真实数据源/执行依赖和验收的当前总入口。**D01–D12、L0–L7、10轴11关系及已有知识来源保持不变；九阶段不再造九个目录，旧知识可以保留纯理论价值但工程状态必须另行验收。**

**多层知识结构修正（2026-11-13）**：保留原 `G0–G4` 目标、`L0–L7` 深度、`D01–D12` 领域及6类存放目录，不把“概念—知识—经济事实—证据—工程—反馈”再建成另一套平行层级。具体的**10个相互独立的观察轴、11种带证据边界的关系、6种不允许越级的推断**见 [原 `DOMAIN-MODEL.v1.json` 的 `cross_axis_alignment`](DOMAIN-MODEL.v1.json) 与 [原知识交叉对应表第7节](INTEGRATION-CROSSWALK.md#7-2026-11-13-关系型认知修正从层级清单到可审查的专业主张)。`npm run audit:knowledge-trace -- --axes` 可检查这一结构；它只读且**不是**自动推理、模型验效或主网钱包身份确认。真正有价值的连接以可追查的**专业主张**为中心：谁提出、哪些数据支持/反驳、哪些条件成立、现有Blix哪里实现、哪次测试证明到何处、新证据如何纠正。旧152单元、21迁入、21快照索引与11候选源的事实身份不因此改变。

**知识追溯的唯一总入口（2026-11-13）**：[知识从获取、理解、承接到实际判断的完整链路](references/knowledge-lineage-lifecycle-20261113.md)；[术语、静态来源映射与双向核查附录](references/knowledge-lineage-lifecycle-audit-20261113.md)。这两篇共同指回原有迁入、覆盖和代码台账，不是独立的新知识库。可运行 `npm run audit:knowledge-trace` 查看静态对应，但不能由索引推断模型已学会。

> 建立于 2026-11-06。**这是已迁入资料的分类与检索入口，不是重新建立一个专家体系，也不是运行时AI已经掌握的证明。** 源文件旧版保留；本文仅管理Blix持有的副本、出处及使用方式。



## 2026-11-09｜新增知识进展：从“观察选择有偏”追到真实数据的标签生成与后验可识别边界

这次不是增加一套统计学知识目录，也不改动Blix原版产品功能。前几轮已经发现Blix市场入选、AI评级及参考项目的选择性观察；**本轮专门补上被忽略的“结果如何被写成真值”**。对照[Why-Solana可复算的样本偏差](https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over/tree/070d2a6e6dcb89efe18d01091a8040eb323e1099)、[CryptoBot迁移幸存者审计](https://github.com/elalamiimed/CryptoBot/blob/1be592d71020738510b25e3bed7a2f5def13ff0a/reports/cohort_survivorship_20260927/FINDING.md)及[ian05012原始采集与标签源码](https://github.com/ian05012/solana-memecoin-dataset/tree/7070d00e1e4492f8604d988549d91785cc5f43f7/scripts)，找到一个具体的源级分叉：**6小时无K线可直接写入尚未到期的24小时、3天负标签，之后常规队列不会重访**。已用同条件离线SQL分支复算，未运行外部采集产品或真实Solana交易。

这一认识已经不是孤立的“幸存者偏差”提示，而是贯穿四条业务的专业约束：**发行总体是什么；Mint/钱包如何被采入、排除和深查；结果是否成熟或缺失；统计能回答市场的什么问题**。尤其要区分：研究样本内经济机制、全市场普遍性、可执行交易收益三个不同命题，不让一个结果数字替代三者。

- **完整知识研究和来源限制**：[跨项目深研第14节](references/source-knowledge-deep-study-v0.1.md#14-2026-11-09-新增跨项目实证样本入选--结果成熟--数据缺失如何共同制造市场规律)。
- **已经修订的专业正文**：[D11 失败样本与可迁移性](cases/independent-validation-and-failure-cases.md#2026-11-09知识反证案例先挑赢家再标结果研究结论何时不能迁移到真实市场)、[D03 价格高点与实际可执行收益](mechanisms/market-price-mechanism-research.md#2026-11-09价格结构研究的新边界最大后验高价不是可执行收益)。
- **来源已登记**：[按原仓与版本核验的来源覆盖](references/source-coverage-v0.1.json)；这是新读到的代码/研究案例，**不是AI运行时知识已激活、真实收益或模型识别率提升证明**。现有原Blix Pulse、钱包、AI、账户和交易业务保持原样。
- **下一项高信息价值验证**：用Blix现有已存发行/AI评级/历史结果的一个冻结时间窗，检查**入选/未入选、结果未成熟、缺价格、确认负结果**的不同分母；若原始发行分母无法可靠恢复，停止夸称总体效能，优先复用成熟来源而非自己发明一个统计答案。

## 2026-11-09｜旧项目的纯知识已开始进入专业正文（不等于运行时激活）

**本次修订的是原知识本身，而非又建参考索引或功能标签。** 过去“独立深读参考项目→迁入Blix能力”遗漏了无需立即形成程序的纯理论、概念与研究方法。本轮保留旧Hermes/meme-/qb-原稿，修正其不可靠的概率/标签推论，将四条有独立价值的知识脉络直接写进原有专业正文：

| 旧原始研究中的独立认识 | Blix 已修订的唯一专业正文 | 不照搬的历史部分 |
|---|---|---|
| Hermes“量什么/能伪/能算/本质”的字段反推、统计行为分析 | [方法：观测语义、可复现性与经济解释](methods/hermes-feature-to-market-structure.md#2026-11-09纯知识转化字段审查可制造性与观察边界) | “两秒同步=同控”“同一交易所出金=庄家”等未经校准判别；未经证据支持的数值阈值 |
| Hermes五力模型 + Gate认识论 | [机制：调查价值、交易价值、承接/扩散/库存和决策时效](mechanisms/wallet-roles-and-inventory.md#2026-11-09纯知识转化候选研究价值与交易价值不是一个目标) | 把比喻式五力公式当价格/收益方程；把缺数据一律BLOCK套进只读研究 |
| meme-AVWAP锚点、FCZ、积累/派发语义 | [机制：成本锚点是市场代理、事前与事后认识分离](mechanisms/market-price-mechanism-research.md#2026-11-09纯知识转化成本锚与观察时点不把-k-线当链上身份) | 将POC/AVWAP自动称为特定主控人的真实成本；按未来上涨回填当下预测 |
| qb-判断治理、校准、自欺审计 + meme-反证方法 | [案例与认识论：任务完成、判断有据、实际改善是三个独立命题](cases/independent-validation-and-failure-cases.md#2026-11-09纯知识转化判断是否值得相信与任务是否结束是两个问题) | 文档完成=功能运行、dry-run通过=真实可靠、只积累正确例而不记录失败 |

**纯知识允许暂时没有产品落点**：原始来源、未使用概念及新问题保持可检索；按问题真正需要时，可供AI理解和跨行业推理，但不因它没有代码接口就删除，也不默认全量注入系统提示词。见 [来源覆盖与这批语义转换记录](references/source-coverage-v0.1.json)、[ai-d对纯理论吸收的通用方法](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/organization-protocol.md)。

**下一步不是再增加知识分类**：检验一轮真实调查问题是否能够正确选用上述知识，主动发现新经济问题、区别观测/因果/决策与缺数据、避免错误阈值，并与不加载旧知识的分析对照。**这些专业正文已被实际修改，但并未让Blix当前运行时AI自动读到，也没有测得模型提升。**


**连续理论与证据依赖补审（2026-11-09）**：进一步定向核查旧Hermes 10–14从钱包角色→同源关系→Sybil/Wash/协调→证据链→行动Gate的原推导，以及meme-的Spring/SOS/LPS完整时序和qb-的原判定样本。**新的认识**不是多贴三个风险标签，而是多个标签可能由同一笔交易、同一供应商快照或同一价格序列派生，不能充当多份独立验证；交易禁止与只读研究停止也不是一个决定。已原位修订[钱包与协同机制](mechanisms/wallet-roles-and-inventory.md)、[价格形成与阶段序列](mechanisms/market-price-mechanism-research.md)、[反证/判断治理](cases/independent-validation-and-failure-cases.md)，并在[来源覆盖台账](references/source-coverage-v0.1.json)中登记定向审阅状态、未证事项和风险锚点；[ai-d跨领域评测](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md)增加非独立证据的失败场景。**均为静态知识修订，尚未实测模型或Blix运行时收益。**

## 2026-11-13｜最新 P1–P2 知识融合与现实能力对照（优先读）

**新的单一入口**：[P1–P2专业知识全域核查、矛盾修正与代码对应](references/p1-p2-knowledge-reconciliation-20261113.md)。已核对本地D01–D12、Hermes/qb-/meme-/ai-d/Why-Solana与代表性GitHub源码、Solana官方协议；原有152单元和65参考资产的未审状态不被改成完成。

这一次不只归档：已经在**原领域文件**追加当前知识修正（[链上/协议](foundations/solana-chain-and-market.md)、[钱包与库存](mechanisms/wallet-roles-and-inventory.md)、[资金](mechanisms/capital-organization-and-incentives.md)、[价格机制](mechanisms/market-price-mechanism-research.md)、[时序群体](methods/anomaly-and-cohort-discovery.md)、[跟单与执行](mechanisms/strategy-and-execution-economics.md)、[反证](cases/independent-validation-and-failure-cases.md)、[AI知识选择](ai/intent-knowledge-selection-and-reasoning.md)）；旧研究原文和历史版本仍保留。

**现行代码状态**：Draft [PR #23](https://github.com/sunshihao001/grok/pull/23) 已有离线 Token Transfer事件/钱包流入流出、跨Mint同地址与快照差、纸面跟单有效性审核，以及受限本地知识选择。它们是**代码+离线回归**，而不是“主网全历史、共同控制、盈利优势、动态监控或Coin页真实AI代理已完成”。最新GitHub CI详见[建设台账](../docs/project/build-register.md)。

**快速使用**：真实问题先定位现有Blix数据与原始交易 → 依据问题选择相关领域专业知识 → 检查事实分母、时间、覆盖、反例 → 用确定性代码计算可证明事实 → 模型仅解释竞争机制与下一次补查。不要把所有原文塞入AI提示词；当前 `local-knowledge-loader.mjs` 有受限的**11个候选专题**，实际一次只会选少数源，检索准确率尚待真实模型A/B确认。

**重大纠偏**：同源/同Slot≠同控，Token转移≠卖出，转账总量≠真实独立新增需求，跨Mint重复地址≠资金闭环，历史回填≠最新市场行为，纸面模拟≠可实现Alpha。原问题仍有研究价值，但要查到可证伪交易与竞争解释后才能提升判断。


## 2026-11-07｜跨市场与AI双循环的整体机制研究（先于局部知识调用）

当问题不只是“某个地址/指标对不对”，而是**市场为何这样运行、AI应怎样建立可持续改变的专业判断**，先读[跨参考项目深度研究第11节](references/source-knowledge-deep-study-v0.1.md#11-2026-11-07-跨全市场与-ai-的双重反馈从数据选择到经济机制与判断修订)。原始证据把 **Blix发现/排队/Playbook反馈、Pulse选择性保存、Million跳过与可跟随成本、PumpTrace资金/Holder证据、Why-Solana假设失效、PumpGrok任务限制、Hermes/qb-/meme-经济机制、ai-d问题发现** 放进同一个完整市场调查问题中；同时核对了外部观察系统交集研究与 RED-COHORT 2026-10 数值撤回。

**真正新认识**：市场行动者的经济策略、采集系统选择性观察和AI自我修订是三种会相互影响的过程。单个钱包簇和AI评分不是完整对象；尤其Blix的自评“missedRunners”仅在**已评级**对象中寻找低分跑赢币，不涵盖未进AI队列的Mint，这是需要通过真实数据检验的研究盲区。**不因此否定Blix完整产品能力**；按原始事实、采集条件、失败/被过滤分母、市场机制和结果可得时点深入，而非只加新关键词或多专家。

**重大文献纠错**：[RED-COHORT arXiv:2607.02795 v4](https://arxiv.org/abs/2607.02795) 已撤回早期买家/群体效果的全部数值结果；原文可作为失败方法案例，但不能继续用历史数字证明群体行为的效应。源的局部结论和Blix现成运行能力需分别核验。此节是跨仓源码和公开研究审查，**未运行Blix/交易/模型盲测**。

## 2026-11-07｜快速知识整合与按问题进入（当前优先入口）

**这次整合做的不是再搬一个知识库**：保持已有六类资料目录、L0–L7、D01–D12及152条旧路由原样，新增[统一知识模型里的六类目标＋七条按任务的知识路由](DOMAIN-MODEL.v1.json)，把刚研究的[各参考成品真正想解决的目标](../docs/project/reference-driven-goal-model-v0.1.md)、市场行动者激励和[ai-d问题形成/知识选择方法](ai/intent-knowledge-selection-and-reasoning.md)接到Blix现有业务。**这是可查找的知识导航，不等于运行时AI自动调用。**

**快速调用不是强制流程**：收到口语问题先确定用户是想发现机会、调查风险、追资金库存、观察市场、解释机制还是让AI代办；可以多选但不需要全部跑一遍。根据当前任务读**最有信息价值的原文**，查相关源码/事实、竞争解释与下一项能改变判断的证据。若发现新领域或无法归类的市场机制，应保留来源并允许更新知识关联；不因旧分类没有位置就停止探索。

| 当前问题（自然语言） | 首先研究的现有知识 | 参考来源的独特问题/Blix落点 | 最容易遗漏、需要积极检查的条件 |
| --- | --- | --- | --- |
| **“今天有什么盘值得关注？”** | [异常与群体发现](methods/anomaly-and-cohort-discovery.md)＋[价格机制](mechanisms/market-price-mechanism-research.md) | Blix Discover；Pulse生命周期与遗漏样本，pumpwatch正常基线，Million发现回顾 | 是否能及时看到、哪些被筛掉、真实交易池深、不能只事后挑成功盘 |
| **“这个币的Holder是不是假热闹？”** | [钱包角色/库存](mechanisms/wallet-roles-and-inventory.md)＋[链上事实](foundations/solana-chain-and-market.md) | Blix Coin/Holders/Bubble Map；HoldTech测量口径、PumpTrace Creator历史、qb单币调查 | Token Account≠Owner≠经济主体；池地址、Fee Payer、TopN截断；支持线索也不能无依据一票否决 |
| **“提前6/12小时转账激增，是否有人组织？”** | [Hermes反向问题生成与旧公式反例](methods/hermes-reverse-discovery-deep-study-20261106.md)＋[资本激励](mechanisms/capital-organization-and-incentives.md) | Blix Journal/Wallet；Hermes时序与筹码、Million持续发现、Pulse历史存储 | 资产净变化/真实签名、观察时钟、覆盖空窗、公共服务；区别准备资金和已经买入 |
| **“转给新地址后卖了没有？跨币又去哪了？”** | [多跳资金核查](references/multihop-funding-evidence-audit.md)＋[经济主体机制](mechanisms/actor-economic-mechanisms-deep-study.md) | Blix Wallet/Track；Million双向发现、Why-Solana多跳、Hermes库存循环 | 真Token转入与下游卖出、SOL/WSOL、跨Mint时序、共享资金Hub，实际群体与未知身份分开 |
| **“价格跌后反弹，是卖压还是做市？”** | [三份真实快照调查](../docs/project/single-mint-audit.md)＋[市场微观机制](mechanisms/market-price-mechanism-research.md) | Blix Coin；对照真实DEX/RugCheck样本与其他池、LP/Swap机制 | 原始交易签名、LP增减、滚动24h量≠短期量、极薄旁池价差不等于可交易利润 |
| **“以前有效的行为现在不灵，是否发现了新机制？”** | [跨参考源码深研](references/source-knowledge-deep-study-v0.1.md)＋[机制/执行经济](mechanisms/strategy-and-execution-economics.md) | Blix Research；Why-Solana结构与优势分离、meme-阶段与失败研究、pumpwatch全样本对照 | 机制变化还是采样变化；同Slot/同源不独占解释，既不乱报也不漏掉强异常 |
| **“继续项目，你自主整合并验证。”** | [多层目标体系](../docs/project/reference-driven-goal-model-v0.1.md)＋[ai-d知识认知](ai/intent-knowledge-selection-and-reasoning.md) | Blix已有功能优先；按需引入ai-d目标推理、外部成熟成品、旧项目失败经验 | 选目标→核来源→复用→可逆交付→回读；GitHub写入、代码通过、真实市场/模型效果必须分别证明 |

**不同“目标”的必要区别**：Blix用户的V-A至V-F是**产品使用目的**；发行者、套利者、LP、sniper、普通参与者的动机是**待推断的市场隐变量**；取证、微观结构、统计、经济学和工程是**按问题激活的专业视角**。可分别提出同时成立的阶段性结论，不必固定专家名单或对所有观点投票。详细[多主体目标研究](../docs/project/goal-map.md)与[主体目标实践对照](../docs/project/reference-driven-goal-model-v0.1.md)。

**可追溯性与状态**：原文全文与旧版各自原位保存；[原历史来源映射](MIGRATION.json)、[参考项目已读与未审范围](references/source-coverage-v0.1.json)、[152旧研究项路由](../docs/project/legacy-knowledge-routing.v1.json)分别负责资料出处和覆盖。索引、静态源码分析、离线反例、旧归档真实供应商事实、原始RPC经济事件、Blix实际运行与已验证收益**不能互相替代**。不同来源的局部失败不等于整体成品无用；新的正面证据也应及时提升只读调查优先级。

**整套系统的机制深研（2026-11-07）**：已把[从市场参与者目标→真实链上事件→数据采集选择→产品判断→执行时效→结果修订的完整跨项目研究](references/source-knowledge-deep-study-v0.1.md)回填到原参考项目深研正文。研究直接交叉检查Blix、Pulse、Million、PumpTrace、HoldTech、pumpwatch、Why-Solana、PumpGrok、OKX、Hermes、meme-及ai-d的代表性源码/原文，不只是原作者功能清单；新增四类认识：参与者收益目标多样、选择性保存改变学习样本、结构与可交易价值分开、事件/可得/决策时间不同。按[来源覆盖记录](references/source-coverage-v0.1.json)确认已读范围，**未宣称全部参考仓库审完或真实链上/运行时已经验收**。日常问题先用下表按需定位，不全文注入。

## 推荐理解顺序：先 Blix，后旧 Grok，再做对应

- **Hermes多维推理、反向异常发现与ai-d跨行业视角**：[旧项目知识纵深研究（2026-11-07）](references/hermes-reasoning-ai-d-cross-domain-study-20261107.md)。与qb-、meme-原始实现对照；含未审范围、反证和下一轮任务，非运行时已融合。

1. [Blix 原生产品与知识总图](BLIX-NATIVE-ATLAS.md)：先弄清 Blix 自己的业务、UI、数据、AI、工程经验和证据边界，不把它当空白工程。
2. [旧 Grok 内部目录与知识总图](OLD-GROK-ATLAS.md)：独立梳理旧 `main`、PR #14/#16/#17、知识卡/专业正文/实验/训练/工程资产，不混同运行状态。
3. [两套知识的对应与去重](INTEGRATION-CROSSWALK.md)：在现有六类知识目录内判定迁入、链接、提炼或保留，不机械复刻旧目录。
4. [已迁入来源清单](MIGRATION.json)：按源路径和版本核对首批17份研究原文与后续2份结构化来源资产；以后以实际文件为准更新，旧档案不能冒充现行产品指令。

## Blix 的完整知识结构：继承旧知识的长处，不只按文件夹分类

**六类目录只决定资料放在哪里，不代表完整专业本体。** 现在已将旧 Grok 的 L0–L7 八个知识层、D01–D12 十二领域、15项跨域关系及证据状态，按 [G0–G4 项目目标](../docs/project/goal-map.md) 编入 [Blix 统一知识层级模型](DOMAIN-MODEL.v1.json)。来源是旧 [PR #14 ontology](https://github.com/sunshihao001/grok/blob/eeb40b050369e4525919500f144325c9a9fc8b74/knowledge/system/ontology.v1.json)，已经过 Blix 单主体目标修订，**非直接把旧工作流变成运行指令**。

| 观察维度 | 要回答的问题 | 采用的内容 |
|---|---|---|
| **G0–G4 目标** | 为什么研究、服务哪项业务与用户价值？ | Blix整体市场智能/AI协作→发现、单Mint、跨Mint、经济机制 |
| **L0–L7 知识深度** | 从哪些事实走到市场机制、资本主体、假说、经济约束、反证和AI演化？ | 继承旧Grok的分析层次和跨层禁忌；**不是八个必须依次运行的步骤** |
| **D01–D12 领域** | 有没有遗漏重要的Solana Meme专业知识？ | 12领域是完整性检查表；152个旧编号沿用既有路由表 |
| **六类资料目录** | 这一份原文的主要用途是什么？ | `foundations/mechanisms/methods/cases/ai/references`，文件只放一处、多领域可引用 |
| **来源/证据/版本** | 内容是原始链上事实、作者报告、研究假说还是经实测验证？ | 保留源、原SHA、时间、反例、未确定和失效条件 |

**最重要的继承**：旧本体中的依赖边和证据警戒，例如“共享资金不证明共同控制”“集中持仓不保证价格上涨”“历史可见不等于实时可得”；D10可靠性与D11反证按当前问题贯穿检验，不强制每次全文加载。以 [跨体系覆盖与缺口清单](INTEGRATION-CROSSWALK.md) 查看 Blix 原生能力怎样与旧研究互补。

## 简单规则：先按用途分类，再按业务领域找

| 目录 | 收什么 | 在Blix中主要用来干什么 |
|---|---|---|
| [foundations](foundations/) | Solana账户/交易、市场数据定义、协议与数据契约 | 核对事实，避免错误统计 |
| [mechanisms](mechanisms/) | 市场、钱包、资金/筹码、价格与执行的专业机制及假设 | 从观察提出经济解释并反证 |
| [methods](methods/) | 专业调查程序、专家提问方法、钱包筛选、异动发现 | 决定任务查什么、怎么查 |
| [cases](cases/) | 历史案例、实验、失败模式、反例、评估方法 | 比较旧判断与新证据 |
| [ai](ai/) | 问题表征、知识选择、跨领域研究、主动纠错 | Blix AI怎样使用知识和工具 |
| [references](references/) | Million/PumpTrace/Pulse/OKX等成熟项目的原始来源与优先核查处 | 对照成熟实现，不无许可拷贝第三方代码 |

**两个交叉维度**：一份文件只有一个主要归档目录，但同时有旧的 D01–D12 研究领域、内容类型和使用条件；旧152项原子索引继续由 [既有路由表](../docs/project/legacy-knowledge-routing.v1.json) 提供，**不重建152份文件**。原作者自己的分类和概念研究保留在源文件全文中。

## 接收一份旧知识的轻量规范（无需拆成几十张卡）

1. **保留原文**：尽量全文迁入而不是重写摘要；记录原始仓库、分支/提交或 blob SHA、原路径和来源状态；旧文件中的相对链接指回其原仓库。
2. **区分知识性质**：协议事实、专业机制/假说、调查方法、经验/反例、AI方法、项目参考。研究假说不自动升级为事实。
3. **区分日常调用与系统深研**：日常问题优先按相关性选取少量资料，避免无效上下文；**对参考项目做完整知识学习时，不设1–3份文件、单一问题或固定轮数的上限**。先掌握完整项目的业务、知识对象、源码结构、设计取舍、测试、失败与演化脉络，再逐知识对象追溯相关原文、机制、竞争解释与跨项目联系。读到足以解释适用边界和未解决问题才停止；不能只凭已有Blix同类功能或资料重复而结束研究。
4. **不强迫代码合并**：知识迁入仅使文件可直接从Blix读取；是否形成工具、Skill、产品功能由实际任务和后续验收决定。
5. **尊重授权与权限**：本知识区不执行代码、不接入供应商、不配置钱包/交易/付费；未来云电脑运行时需单独做环境及只读权限验收。
6. **版本优先**：源文有历史阶段、原研究方向和旧工具限制，均原样保留；新目标以Blix项目入口为准，历史文件不成为全局强制指令。

## 参考项目知识深研：以专业认识为主，不以搬迁文件数量为主

**研究范围不能被Blix既有分类束缚。** 六类目录是归档方式；G0–G4是目标；L0–L7是分析深度；D01–D12是现有领域覆盖基线。发现新的重要专业问题，可修订知识域与联系，而不是把新内容塞进不合适的旧分类。

**完整项目先贯通再深入**：先看“为什么设计、完整业务如何工作、代码/数据/界面/测试/历史如何配合”，再把其中每条值得学习的专业知识从问题、设计假设、真实实现、因果/统计依据、失败模式、反例、版本适用性和替代方案逐层展开。这里的“每条”指**项目中可辨认的知识主张/模型/决策/故障经验**，不是机械逐行注释源码；对未深入的部分保留明确未覆盖状态。

**跨项目不止比较同名功能**：比较的是其背后的对象定义、经济事实口径、时间语义、算法边界、数据完整性、错误假设和设计来源。Blix拥有类似功能不是拒绝学习的理由；新增认知可以改变已有产品设计的判断，也可提出新的研究领域与对象。不同项目中相同名称的“owner”“funding”“cluster”未必同义。

**吸收必须产生可指出的知识增量**：例如修正一个旧假设、补充一条过去忽略的经济机制、发现已有业务的遗漏条件、吸收经验证的失败处理方法，或明确一个新研究对象。改进归入已有合适的专业正文或经审查的新主题文档，并从本总入口能找到；保留来源及真值级别。不要将“LINK/COPY/ADAPT/REUSE”状态自身当作研究成果。

**分清两种停止**：一个来源可以暂时不复制代码、不进入运行时，但**不意味着停止学习其知识**。只有完整范围已核查且价值/证据/适用关系清楚，才把对应知识对象标为充分研究；局部检查不能冒充整仓审查。

第一份 [跨项目知识深研成果：钱包关系、经济主体与历史完整性](references/wallet-relations-cross-project-knowledge-20261106.md) 对照 Blix、Million、PumpTrace 源码，示范不局限于功能清单的学习方式；该研究并不代表三个项目的全部知识点已经审完。

## 本轮重点：Hermes多维推理、异常发现与反向生成机制

- [Hermes 00c 原有8种问题/结构推理思想](methods/hermes-feature-to-market-structure.md)；
- [Hermes 00d 多维度研究原文](methods/hermes-multidimensional-reasoning-original.md) 与 [00e 反向发现原文](methods/hermes-reverse-discovery-original.md)：历史内容完整保留，包含探索性推论及未经校准的阈值，**不能直接做Blix风险/主体标签**；
- [Hermes×qb-×meme-×ai-d 原始纵深研究 V0.3](methods/hermes-reverse-discovery-deep-study-20261106.md)：已深入核对00c–00e、两部大型L1/L2文档、历史Grill与设计记录，恢复37项L1和16项L2的原始研究用途，并用两份固定合成fixture复核qb字段契约缺口；含多行业专业反证、Blix具体业务落点及ai-d对照评估边界；
- [完整领域模型](DOMAIN-MODEL.v1.json) 已在D01–D12的相关问题入口关联上述研究，不意味着强制每轮读全部文档。

**知识学习不应被早期分类压平**：新异常未有充分身份/原因证据时，保留有来源的观察及竞争解释，不急着叫“庄家/内幕/吸筹/操纵”；也不能因为“Blix已有对应功能”“暂时没有可实证标签”就丢掉高价值研究对象。识别来源与知识成熟度不等于给市场实体贴真值标签。

**当前源文件迁入数是21**（此前19 + 新增Hermes 00d/00e原文2份）；本轮纵深研究为新产生的Blix分析成果，不计入旧来源迁入数。原始00b、37L1与16L2规格保持源端版本和路径；本轮已检查其整体结构与关键推理链，但仍未逐项完成现行GMGN接口和真实市场反证，旧Hermes/qb-/meme-全仓也未逐知识点验证。


**2026-11-07 新增可复算认识**：V0.3现已补入[第11节源公式反例与同输入证据合同](methods/hermes-reverse-discovery-deep-study-20261106.md#11-2026-11-07旧推理公式的反例复算与知识进入blix的检验)：旧Hermes的早期24倍假动量、供应商可疑交易占比重叠、AMM储备价值比错误spread代理；qb优先名额/字段别名、meme`real_pending`样本资格冲突。实用边界同步进入[Blix知识使用入口](../docs/project/knowledge-use.md)与[ai-d实验设计](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md)。**这些是独立数学/静态检查，不是实时识别率提升或正式策略规则。**

**研究范围继续展开，而非只纠正三个公式**：[Hermes×qb×meme 纵深研究第12节](methods/hermes-reverse-discovery-deep-study-20261106.md#12-2026-11-07取消先验标签边界后的跨旧项目完整认知连接) 已将旧资料中的七条相互依赖的专业认识连成完整研究链：市场发现与交易决策边界、资本组织/钱包/库存/对价、事件与证据时间、meme 的价格结构与真实链上成本、字段与测量可靠性、失败样本与机制成熟度、AI问题生成与独立验收。**这不是七个新标签或七个强制阶段**；源项目独有的任何高价值内容均继续进入研究，不因当前Blix没有对应模块而忽略。查看[按原文件的审阅深度与未审范围](references/source-coverage-v0.1.json)，勿将目录扫描或摘要当全部知识已掌握。

**继续向qb-留存的原始调查产物下钻**：同一份Mint归档记录95条钱包、4组候选资金关联与后续核查缺口，且“零余额”“100%卖出”“全部退出”并不等价；旧Markdown/JSON汇总也存在不同版本口径。由此连回Hermes的钱包/库存/资本组织、meme的派发/承接解释和ai-d的证据审查方法。阅读[完整第13节及原数据来源](methods/hermes-reverse-discovery-deep-study-20261106.md#13-2026-11-07qb真实留存文件核查反推全链经济身份与库存知识)，并由[Blix业务知识调用入口](../docs/project/knowledge-use.md)使用；此为源资料静态核查，尚未主网复算或接入实时AI运行时。

## 第二批：继承旧 Grok main 的专业判断卡与历史来源

- [原始15张专业判断卡](methods/legacy-grok-core-cards.v1.json)：原样保留旧 `knowledge/catalog.v1.json`，每卡包含 `mechanism`、`required_evidence`、`alternative_explanations`、`inference_limit`、`next_check` 和来源信息。**3张`source_contract`、11张`documented_legacy_method`、1张`unverified_hypothesis`；全部是历史知识候选，不是实盘认证。**
- [21份历史快照的固定来源目录](references/legacy-snapshot-sources.v1.json)：已核查旧 `main/knowledge/legacy-snapshots/` 下21份快照路径存在，来源分布为Hermes 16、meme- 3、qb- 2。**本批仅复制来源清单，快照原文尚未迁入 Blix；卡内 `snapshot_path` 仍指旧仓库的相对路径。**
- [综合知识层级模型](DOMAIN-MODEL.v1.json) 已将15张卡按适用领域映射至D01–D12，避免反复创建额外专家层级；原文可能与已经迁入的17份研究有重叠，保留原出处与不同表达目的。
- **旧轮迁入文件总数当时为19**：首批17份正文 + 1份完整结构化卡目录 + 1份历史快照来源清单。不是17+15+21=53份完整原文；未做模型自动知识调用或链上实测。

## 当前迁入进度

- 本次迁入首批**旧 Grok 全文研究**及少量高度相关的 Hermes、ai-d 知识。
- 批次、实际写入路径和来源状态由 [MIGRATION.json](MIGRATION.json) 追踪；未迁入的大型旧研究和参考项目仍有原文链接，不视为丢失。
- 业务阅读入口：[Blix总览](../docs/project/README.md)、[知识使用方式](../docs/project/knowledge-use.md)、[已知语义缺口](../docs/project/mint-cross-module-evidence-audit-v0.2.md)。

> 不应以“已经复制X份文件”声称 AI 判断水平已经提升；迁移完成和实际应用验收是两种任务。

## 重要修订：先完整学习独立知识，再决定如何应用

现有六类目录属于**知识存放位置**，不是决定哪些专业知识值得研究的门槛；Blix能力缺口仅影响最终是否迁移/修改代码，不限制参考项目独立研究。见[跨原项目深层研究与认知增量](references/source-knowledge-deep-study-v0.1.md)和[按版本的阅读覆盖状态](references/source-coverage-v0.1.json)。不得因没Blix对应模块、无法立即转为规则、或旧项目包含未经验证假说就停止研究其原设计；同时不得把假说当已验证市场事实。
