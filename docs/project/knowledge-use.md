# 按实际问题使用专业知识、AI研究与可证伪证据


**多轴认知对齐（2026-11-13）**：从简单问题进入专业知识时，按实际问题选择 G目标、L知识深度、D专业领域及概念、经济事件、主张证据、数据可见时间、Blix代码运行、修订反馈等相关视角；不是每次调用固定十步。详见 [现有知识交叉表](../../knowledge/INTEGRATION-CROSSWALK.md#7-2026-11-13-关系型认知修正从层级清单到可审查的专业主张) 和 [现有DOMAIN-MODEL](../../knowledge/DOMAIN-MODEL.v1.json)；可只读执行 `npm run audit:knowledge-trace -- --axes`。其中 `semantic_match`、`observed_economic_event`、`supports`、`implemented_by`、`tested_by` 属于不同关系：概念相似不能证明同控，转账不能证明卖出，离线测试不能证明主网正确，知识被选中不能证明模型用对。遇到重要结论要反向追 `结论→原始签名/来源版本→推导条件/竞争解释→当前代码/测试→修订影响`，避免词面关联泛化为经济因果。

**知识获取、承接和实际调用的唯一总入口（2026-11-13）**：[Blix知识全链追溯](../../knowledge/references/knowledge-lineage-lifecycle-20261113.md)；[详细术语、来源映射和双向查账附录](../../knowledge/references/knowledge-lineage-lifecycle-audit-20261113.md)。两个文档是同一研究的主文与附录，不取代原D01–D12、P1–P2核查或建设台账。`npm run audit:knowledge-trace` 可查旧源单元→本地承接→AI可选来源；不证明模型确实用上或用对，不要求所有普通问题走固定流程。

**新认知入口**：[Hermes生框架、qb数据护照、meme反证与多对象经济过程](../../knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md)。根据任务需要用因果、过程挖掘、取证等问题视角生成竞争解释，未审来源保留UNKNOWN；不是新增固定专家、硬标签或运行时强制Prompt。


**主体认识优先入口**：先看[主体能力与旧知识内化深审 V0.2](blix-knowledge-activation-ceiling-v0.2.md)（按业务判断上限、旧方法适用、不能继承的规则），再按需回查下述来源。

**主体认识优先入口（原基准）**：[Blix 已有业务能力 × 旧 Grok 专业知识继承基准](blix-heritage-capability-baseline-v0.1.md)。面对实际业务先定位 Blix 已有 UI/数据/逻辑，再按需要调用 PR #14 的原专业正文或 Hermes/qb-/meme- 的机制，不全文搬迁、不把旧历史程序当作已在 Blix 运行。

## 2026-11-14｜从完整专业知识主述进入实际问题：选择、过滤、报告与验收

**优先入口**：[十二领域的唯一主述与全来源归位表](../../knowledge/README.md#2026-11-14全域专业归位总入口十二领域主述参考来源知识身份与产品验收)。历史Hermes/qb-/meme-与Synapse、GMGN、Pulse/Million/HoldTech等原始知识不再由本页各写一套简化定义：原文保留在`knowledge/methods/`及`references/`，专业主张在对应D01–D12正文，通用AI九阶段以`ai-d`为真源，代码/运行事实以`build-register.md`为准。

| 用户实际表达 | 优先主述和原始事实 | AI如何升级问题与过滤 | 当下可实现的输出边界 |
|---|---|---|---|
| “看看现在有哪些币可能值得参与” | 原Blix Pulse/Triage/Quality/Early + D02/D03/D08/D09/D10/D11 | 先源时点、覆盖、未选样本，再分`research_priority`/指定规模下的`trade_readiness`，必要时转钱包/资金研究 | 当前AI只是最多12浏览器候选调查选择；没有全市场同源增益或实际净收益证明 |
| “这币庄家在哪里、哪些钱包联动” | 现有Coin/Holder/BubbleMap + D01/D04/D05/D06/D07/D10/D11 | 从账户身份→资金可行性→Token/Swap/LP→竞争解释，不把同Slot、共同Fee Payer或平台标签当同控 | 局部原始交易/转仓图；私人控制、完整历史或同批卖出UNKNOWN |
| “A买入转给B，B把币卖了吗” | 已捕获签名、指令位置/余额前后 + D01/D04/D06/D11 | Swap、Transfer、接收者后续卖出各自成事实；只在可对账的库存批次和对价下升级判断 | 当前`economic-claim-trace`有局部转账事实与本地卖出摘要，不能确证同批 |
| “这组钱包以前买别的币吗，能不能跟” | 原Blix钱包事件 + D05/D07/D08/D09/D10 | 先区分地址重合、真实资金接力、共享设施，再区别钱包PnL和跟随者净可执行 | 跨Mint时间候选与纸面否决；不能当策略Alpha或真实交易指令 |
| “模型是不是使用了以前研究的知识” | D12、原11来源白名单、K1–K9与具体模型工具轨迹 | 核哪段原文确实被提供/使用，何处改变了工具选择、假说或错误；比较无知识/有知识同任务同预算 | 目前可列知识来源hash/阶段，但没有真实模型独立A/B增益证明 |

**不靠写更长报告提升判断**：一个有价值的案例最少可回查对象/窗口/来源→原始事实→具体主张/竞争解释→业务结果与限制→当前代码和测试→新事实修订。若真正需要新领域，先追原资料、给出现有D领域不能容纳的理由；不因词面不同新增第13领域。单次任务可跳过不相关知识，没有证据时可以输出`UNKNOWN`或拒绝进一步调用。

**成品交付位置**：[扩展产品成品化/验收主线](intelligence-layer.md#2026-11-14成品化实施主线知识已经归位之后)。知识整理属于K6；真实模型用对是K7/K8；市场长期效果和自动回访是O5/O6。三者的状态不混淆。

## 2026-11-13｜当前P1/P2知识如何真实调用、怎样不误用

最新原始来源、冲突与能力核查见 [P1/P2全域知识对照账](../../knowledge/references/p1-p2-knowledge-reconciliation-20261113.md)。**历史章节中的“没有Blix运行时代码变更”仅针对其写作时点**；现在Draft PR #23已有只读离线工具、专业图谱、快照审查、纸面可跟随性审核与按需知识装载。但**尚未连接Coin页真实模型/API与主网全历史**。

| 问题场景 | 先用的事实与知识 | 当前可执行 | 不能自动下的结论 |
|---|---|---|---|
| 一个Mint的关键钱包、转仓与接收卖出 | [D01协议](../../knowledge/foundations/solana-chain-and-market.md)、[D04钱包库存](../../knowledge/mechanisms/wallet-roles-and-inventory.md) | `npm run inspect:network-offline -- --db EXISTING.sqlite --mint MINT` 的本地原始转账/图谱 | 转账=卖出、接收方售出原转入Token、地址=同一操作者 |
| 同源/多跳/跨Mint群体 | [D05资金来源](../../knowledge/mechanisms/capital-organization-and-incentives.md)、[多跳审计](../../knowledge/references/multihop-funding-evidence-audit.md) | 离线相同地址重合、不同签名与指令位置、资料回补对比 | Pool/交易所共享服务=控制群体、跨Mint地址重合=资金真实流向 |
| 市场异动/6小时转账激增 | [D03价格机制](../../knowledge/mechanisms/market-price-mechanism-research.md)、[D07群体](../../knowledge/methods/anomaly-and-cohort-discovery.md) | 两份本地快照新可见/丢出样本/数据修订分开 | 新入库=刚链上转账，或曾撤回的论文数字=实证预测 |
| 看中某个高收益钱包想跟单 | [D08/D09成本与策略](../../knowledge/mechanisms/strategy-and-execution-economics.md)、[D11反证](../../knowledge/cases/independent-validation-and-failure-cases.md) | `npm run audit:followability-offline -- --input PAPER_RECEIPTS.json` | 旧成交价=跟随可成交价，纸面收益=样本外Alpha |
| AI要学会如何研究 | [D12知识与意图](../../knowledge/ai/intent-knowledge-selection-and-reasoning.md) | `local-knowledge-loader.mjs` 受限源选择 + `ai-workflow.mjs` 离线模拟 | 已阅读/已注册152项=AI已掌握或真实调用正确 |

**最低使用原则**：先区分来源主张、原始链上事实、离线测试和未证实解释；Token Account、Owner、fee payer、Pool、Vault、私钥控制、经济收益权逐层审查；对同一Mint要求签名、Slot、外内指令位置、金额原始单位、事件/获取/首次可见时间与历史覆盖。未知是准确状态，不是默认忽略所有异常。

**知识路由不是强制执行顺序**：模型根据普通问题可探索新领域，既有Dxx与受限11源仅为当前检索入口；资料中包含旧规则、撤回数值、过时假说时不允许直接注入产品判断。正确性由同任务无知识/有知识的证据、反例、工具费用及模型A/B验证。新增资料若不能改变专业问题、代码或误报，不继续为凑数量加规则。


## 通用 ai-d 完整能力的接入入口（2026-11-06）

**Blix 消费入口**：[ai-d-cognitive-core Skill](../../.grok/skills/ai-d-cognitive-core/SKILL.md)，上游唯一来源：[ai-d Cognitive Core Skill](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/.agents/skills/ai-d-cognitive-core/SKILL.md)。它开放七项完整的长期认知能力——目标理解、专业知识、未知发现、方案判断、实际交付、证据反证与长期迁移——并指回原始资料，不把知识体系复制成又一套 Blix 目录或强制全流程。

**真实状态**：已验收两个 GitHub 仓库的 Skill 文件、AGENTS 入口、上游原文和本地专业文件的静态可达性；但尚未在 Grok Bot 云电脑私人 Skill 库安装，亦未证明 Bot 实际调用了全部来源。Grok CLI 的 `.grok/skills/` 发现路径不等于 Grok Bot 原生私人 Skill 的注册；后者在该环境启用后还需要安全任务测试。日常市场调查首先遵循 Blix 自身目标与只读限制，需要专业研究、任务判断或跨领域知识时再读取 ai-d 对应原文，不默认全文加载。

## 知识来源与正确定位
| 入口 | 贡献 | 限制 |
|---|---|---|
| [ai-d PR #1](https://github.com/sunshihao001/ai-d/pull/1) | 多层目标/七并行能力、目标纠偏、知识选择、专家认知提取、研究后再思考 | Draft；未证明自动 Agent、跨模型提升或专家技能已经迁移 |
| [grok PR #14](https://github.com/sunshihao001/grok/pull/14) | D01–D12、旧专家视角、152问题与65资产的历史入口 | 登记不等于全部已验 |
| [grok PR #16](https://github.com/sunshihao001/grok/pull/16) | 原始交易解析、单 Mint 真实供应商预览与离线监控研究 | **不是 Blix 已集成的真实持续监控** |
| [grok PR #17](https://github.com/sunshihao001/grok/pull/17) | 目标演变、UI信息设计、知识导航、业务集成研究 | Draft，非 Blix 当前代码 |
| [Hermes](https://github.com/sunshihao001/-)、[qb-](https://github.com/sunshihao001/qb-)、[meme-](https://github.com/sunshihao001/meme-) | 钱包角色、资金循环、单 Mint 报告、经济机制与旧失败经验 | 不自动视作安全可运行成品 |
| [Why-Solana](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | 同源/多跳/群体协同、公共设施排除、选择偏差与反证 | 结构关系不等于真实经济主体或收益优势 |

旧知识保留原位，禁止为“让 AI 理解”将所有 Markdown 全量注入上下文或从头复建专家制度。

## 专家认知怎么进入实际产品
ai-d 最新研究区分 **知识摘要 → 问题表征/判断方法 → 经外部任务检验的实际能力迁移**。当分析一个 Mint，AI 应先明确当前用户问题和经济机制；仅提取相关研究里的必要线索、决策依据、适用/失败条件，并用交易事实及对照反证验证，不能假装理解专家不可观察的内心过程。

## 常见问题与正确知识调用
- “12小时钱包转账突然增多” → 先查可得历史、钱包名单变化、签名/资产净变化；再比较资金准备、做市、出货、Dust、公共Hub、数据回补等机制。
- “捆绑钱包占多少” → 分同Slot、真实可确认Bundle、初期买入供应占比、当前持仓；分母/窗口/Pool/Owner必须明确。
- “A买入、B接收、C卖出” → 交易签名、指令位置、Swap/Transfer和接收路径；不能直接把三地址确认为同控。
- “要新增一个专业模块” → 先研究原 Blix 是否已有；外部成熟整用/薄接口/有限适配/内置四种路线按成本与证据选择。

## 输出与数据证据的最低语义
区分 `USER_CONFIRMED`、`SOURCE_READ`、`AUTHOR_REPORT`、`SUPPLIER_RETURN`、`OFFLINE_TEST`、`LIVE_READ_ONLY`、`PRODUCTION_VERIFIED`、`INFERENCE`、`HYPOTHESIS`、`UNKNOWN`。保留来源、签名及事件位置、Slot、事件和采集时间、资产单位、覆盖/缺口、正常竞争解释、可推翻条件；无数据不能当0活动。

**每项重要成果后再想一次**：有没有比原方案更成熟的产品/算法/机制解释？新认识改变哪个上层目标或执行选择？比较少量实质方向并推荐首选；若没有增量，就继续当前路线，不为凑选项创造伪问题。


## 已核原始知识的实际激活：三种问题，不是复制旧规则（2026-11-06）

本节从旧研究**直接读过的原文**反向连接现有 Blix 源码，补足 [主体能力/知识基准](blix-heritage-capability-baseline-v0.1.md) 中尚属概括的映射。只证明**原文已读、机制适用性进行了人工源审查**，不证明模型已自动学会、知识路由已上线或资金归因实测通过。

### A｜“这些钱包一起买，是不是一个人在控制？”

**应按需读取原文**：
- [旧 Hermes 钱包角色](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-03-wallet-roles.md)：有 wallet roles、`native_transfer_from`、关键钱包标签、证据和反证字段；**GMGN 标签是输入候选，不是身份真值**。
- [旧 Hermes 钱包结构](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-04-wallet-structure.md)：把同 `native_transfer_from`、五分钟内买入3钱包、卖出比例相似定义为调查组；这些是**筛查阈值**，不是经过独立校准的共同控制证据。
- [PR #14 D04–D07 深入知识](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/domain/L3-wallet-actors.md)：节点/边角色、共享服务、Dust、市场共同事件、经济受益人和可卖库存的竞争解释。

**Blix 现成入口**：`server/coin.js` Holder/Dev、`server/bubblemap.js` RugCheck/first-funder/同Slot/四跳图、`server/wallets.js` 聚类及 `wtrack.js` 钱包活动、`web/src/pages/Coin.tsx`。不要先写第二套聚类。

**原文改变的判断**：先确认具体 `funded` 边究竟是 SOL 转账，还是 `bubblemap.js:119-129` 的 Fee Payer 代理；查看是否公共交易所/分发服务，以及同Slot是否受共同市场事件影响。正确结论可为“观察到共享出资候选与同步买入；共同控制 **UNKNOWN**”。**禁止**直接使用 Hermes 的“同源=一个团队”或 Blix graph cluster=实际庄家作为既定事实。

### B｜“这个 Mint 的关键钱包、池和成本应该怎样调查？”

**应按需读取原文**：
- [旧 qb- 单 Mint 报告程序](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)：输出 `04_key_address_matrix.csv`（关键地址）、`05_infrastructure_registry.csv`（公共设施）、`06_low_weight_scope.csv`（低权重范围）、`07_review_plan.csv`（复查计划）等完整工作产品，**是业务问题与报告设计参考**。源码用 `subprocess.run(..., shell=True)` 调旧 GMGN 命令，**绝不未经审查直接运行**。
- [原 Grok D01/D06/D10 主册](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-core.v1.md)：Token Account/Owner/程序、供应量、钱包角色与数据时点的区分。
- [PR #16 受限适配器契约](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)：原始 RPC、`available_at` 与未支持事件需要分离；离线 fixture 并非完整 Swap 归因。

**Blix 现成入口**：`server/holders.js` ledger、`holderslive.js` 链上 Owner 快照、`coin.js` 多供应商/Dev/Pool、`bubblemap.js` 后备前20 Token Account，再看 `web/src/pages/coin/tabviews.tsx` 的结果位置。

**原文改变的判断**：将 `Pool/AMM/vault`、Token Account 与真实 Owner 分开；按源报告持仓分母、快照 Slot/确认级别、历史交易覆盖和成本缺失。将 “被观察到的持仓”与 “可归于某经济主体的可卖库存”分开。不要用旧 qb- 的优先级分数、GMGN 标签或 Blix `partial:false` 自动产出确定的成本/控盘概率。

### C｜“拉升前12小时转账激增，是吸筹还是要出货？”

**应按需读取原文**：
- [旧 meme- 深洗与死亡盘](https://github.com/sunshihao001/meme-/blob/main/02_%E5%BA%84%E5%AE%B6%E5%91%A8%E6%9C%9F/%E6%B7%B1%E6%B4%97%E4%B8%8E%E6%AD%BB%E4%BA%A1%E7%9B%98%E8%AF%AD%E4%B9%89%E6%B7%B1%E5%8C%96_v0.1.md)：Wyckoff/POC/AVWAP 的恢复、失败和需求语义只是价格结构**待检验假设**，不是操盘者身份或真实成本的证据。
- [Hermes 筹码状态设计](https://github.com/sunshihao001/-/blob/main/design/Skill4-%E7%AD%B9%E7%A0%81%E6%8E%A7%E5%88%B6%E6%9D%83%E7%8A%B6%E6%80%81%E5%B1%82%E8%AE%BE%E8%AE%A1.md)：时间对齐、过期立即 UNKNOWN、排除Pool/CEX/系统账户是**有价值的条件判断**；其状态概率和权重公式未经当前链上实证校准，不迁入生产评分。
- [Grok PR #14 D05/D07/D11](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/domain/L3-wallet-actors.md)：时序角色、共同事件基线、公共资金服务与反证；[PR #16 离线钱包批次](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)：窗口在 `coverage.complete` 不足时不能证明“没有活动”。

**Blix 现成入口**：`server/journal.js`、`wtrack.js`、`wallets.js`、`coin-flow.js`、`server/health.js`、`research.js`。先查是否真的观察到6/12h连续签名/资产净变化，调查集是否改变、是否发生缓存回补，再考虑供需/资金准备/拆分接力/出货/普通做市等解释。

**原文改变的判断**：如果某个时间段 RPC 断流，不能从零条事件推出“钱包沉默”；如果价格形态像“深洗”，也不能从K线替代真实仓位/资金证据。合理报告是观察事实、数据覆盖、多个机制假设及可推翻条件。

### 防污染：一处旧知识明确不应直接带入

[Hermes Evidence Chain 原设计](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-05-evidence-chain.md) 的 `calculate_confidence` 用固定 `base=0.8` 加减启发式权重，并把同源占比等用作 `CONTROLLED` 的候选条件。该设计可借鉴“证据/反证/降级/缺失字段都应出现在报告”，但**不能把其0.8或阈值复制成 Blix 的概率标签**；没有真实基准、校准和独立反例，精确数值会制造虚假确定性。

### 什么叫“已把知识放进主体”，当前到了哪一级？

- **已完成 SOURCE_READ + LINKED**：AI入口 `AGENTS.md` → `docs/project/README.md` → 本文件 / 主体继承总图 → 上述精确原来源 → Blix现有业务代码。具体可回查原文，旧知识仍留在原仓库，**不需要迁移复制152题、22专家和65资产**。
- **尚未完成 APPLIED_AND_VERIFIED**：没有运行的同 Mint 调查样本验证这三条调用链是否提高了结论质量；没有将上述推断写入 Blix 运行时的数据结构、UI、MCP、持续告警；没有真正的 Grok Bot知识调用。
- **后续按用户新指令**：先让这三条主体业务—知识链清晰、确认重要的专业缺口，再按“能够改善哪个业务判断”去解剖 Million/Why-Solana/HoldTech/OKX 等成熟实现。不能以研究项目的名称或功能个数代替复用判断。


## 首批资产整合决策：把旧研究和成熟成品作用于现有Blix（2026-11-06源码对照）

**目标**：只建设、运行 Blix 一个产品；旧 Grok/Hermes/qb-/meme-和 ai-d 为知识与方法来源，参考成品为业务实现与失败经验来源。以下是从**具体原始代码**而不是项目介绍得出的第一批可行动判断。状态仅 `SOURCE_REVIEWED`，**未拷贝模块、未修改业务程序、未运行真实Mint**；此前152条映射与65资产索引保持原位，不重建新体系。

| 当前Blix真实问题 | 原始证据/可复用资产 | 精确落点与迁移决定 | 第一次验收反例 |
|---|---|---|---|
| Bubble Map资金边将直接出资与代付手续费混合；查无最老记录会持久负缓存 | [Blix bubblemap.js](../../server/bubblemap.js) `readFunder`、`bubble_funders`；[Hermes 00c](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00c-GMGN-思维模型提炼.txt)事实→特征→结构；Grok D01-K03、D05-K01/02/03/09/10 | **第一优先，限定修改原模块**：未来应让资金边明确 `DIRECT_SOL_TRANSFER` / `FEE_PAYER_ONLY` / `UNRESOLVED_TRUNCATED` / `UNKNOWN` 的证据语义与历史覆盖；只有经真实交易证实的边才能用于相应资金关联推断；保留源引用、可重新补查策略。**不是**让 AI 靠提示词给现有错误关系图“解释一下” | 交易只有第三方Fee Payer且无对目标钱包的入金：不得生成“已证实资助”；最老签名超3页时不得永久认定无关系 |
| 同一个Mint的Creator/持仓/池子在不同页面口径和来源不同 | [qb-单Mint八表](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)关键地址/基础设施/复查组织；[PumpTrace trust-engine](https://github.com/AntC215/Pumptrace/blob/main/src/modules/trust-engine/analyze.mjs)按Owner/TokenAccount/程序分类与不同证据强度；Grok D06、D10 | **复用报告构造与验证语义，不搬旧GMGN脚本/新UI/未经校准风险分**。优先对照 `coin.js`/`holders.js`/`holderslive.js`/`bubblemap.js`；区分池/程序/Owner、数据源、供应量分母、观察时点 | 前20 Token Account对应少于20个Owner；池子是大Holder但不是个人钱包；两源分母不一致时明确UNKNOWN |
| 从一批值得关注的Mint发现隐藏地址，再经地址找出其他Mint | [Million discovery.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/discovery/discovery.service.ts) 已通过pool/venue过滤、按买入净额挑候选并试探性分析头部与尾部；[funding.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/funding/funding.service.ts) 显示方向、对手、次数、金额并声明截断 | **有限吸收算法经验/研究缺口，不整套复制Million**：Blix已有`wallets.js`+`wtrack.js`+`bubblemap.js`，先比对其候选发现是否识别非Holder/非头部接收地址、公共设施误报和跨Mint重复；如实际优于原生，再决定薄适配 | 聚合池在同交易中大额收到Token不能被选为鲸鱼；仅最近窗口的样本不可标成“最早获利钱包”；一个公共资金入口的许多接收者不能被当一人 |
| 不完整历史却被AI解释为“连续12小时无异动” | [PumpTrace backfill-manager.mjs](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)有QUEUED/RUNNING/PAUSED/RATE_LIMITED/CAP_REACHED/COMPLETE及重启恢复；旧PR#16的`available_at`、C05覆盖限制 | **优先学习恢复语义并比较现有Journal/WTrack能力**，不直接接入PumpTrace服务/第二数据库；只有当前模块无法做到时才有限引入能保存cursor和缺口的成熟模式 | 429、重启、超cap或索引断流，不得产生“无事件”的错误结论；历史补到后不得当新发生的资金激增 |
| AI知道152个题目但仍无法自主判断应调用哪项知识 | [ai-d工作流部件](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/research/workflow-components-and-boundaries.md)、[Hermes 00c](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00c-GMGN-思维模型提炼.txt)、[Blix原152路由](legacy-knowledge-routing.v1.json) | **不再扩建专家目录**。一条任务首先识别事实问题与必要证据，再检索少量Dxx-Kxx原文、判断适用/冲突，调用Blix已有只读能力，输出支持和反证及缺口；将调用过程做可复核记录。此处仍是任务设计，现有`mint-facts`不具备自动知识检索/工具调度 | 给出“同步买入=同控”作为故意错误假设，模型应主动查D05公共服务/共同市场因素，并在证据不足时回答UNKNOWN |

**本轮复用裁决**：
1. 第一批重点不是哪个参考项目最强，而是**Blix原资金边类型与历史完整性**。旧Grok/Hermes指出专业错误，PumpTrace提供恢复候选，Million提供下一轮跨币发现实现对照。
2. `meme-`的Wyckoff/POC/AVWAP、旧Hermes概率/阈值与PumpTrace数值风险分只保留为有条件的研究假说，不作为未经校准的同控身份、交易信号或精确置信概率。
3. `Pulse`的长期市场档案、`HoldTech`的Holder质量与快照轨迹、`pumpwatch`的冻结研究样本、`OKX`的现成只读工作流、`PumpGrok`的任务契约/收据是下一批比较对象；先对照Blix已存在的功能和真实缺口。保留65资产索引避免遗漏，但**登记不等于已经全部核验和融合**。
4. 未来任何迁入必须分类标记：**来源已读** / **已选具体代码接口** / **离线回归通过** / **真实只读验收通过**。当前仅达到前两项的候选判断。保持暂停启动、签名、交易、付费及自动联网测试的既定边界。


## 2026-11-07｜Hermes原始推理链如何在Blix的只读研究中真正改变提问

**研究真源**：[Hermes × qb × meme 深度研究V0.3](../../knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md#10-2026-11-07-原始推理链纵深补审00c00e两部大稿与-grill-原始记录)，含冻结原始文档、两部37 L1/16 L2规格、实际字段契约静态复核与合成fixture同输入诊断；[现有核心来源目录](../../knowledge/README.md)保留原文和未审范围。本段是**知识运用建议**，不代表\`server/research.js\`、\`brain.js\`或Grok Bot已自动学会使用。

### 当现有筛选标签回答不了异常时，保留研究入口

- **问题可能是“研究什么”而非“买不买”**。当前\`server/triage.js\`会按叙事/规则及实时交易活动升级部分Mint，\`server/coverage.js\`的短窗runners补已知范围缺口；\`server/research.js\`关注短期需求和交易判断。这些均不等同于解释六小时/十二小时的异常资金、库存、行为机制。允许只读研究继续观察“现有信号不支持参与”的对象，**绝不因此绕过安全门禁或产生交易动作**。
- **Hermes 00d**：在同一个Mint上改变专业问题，例如从“哪些是SM”改问“为什么同样的资金流在不同时间导致不同库存、角色或价格结果”。根据问题选源，不要求固定下载GMGN全部230字段。
- **Hermes 00e**：针对无法解释的异常或反例主动生成替代机制（公共设施、独立跟随、重复记账、缓存回补、真实接力等），而不是任意把变量配对后给新庄家模式命名。
- **qb-调查**：将候选机制落回Mint/钱包/Token Account/事件/Slot/时窗/资金源/下一次复查；接口别名要先核。旧Hermes \`native_transfer.address\`、qb \`native_transfer.from_address\`、旧fixture \`native_transfer_from\`不互换；空字段不能当作“无资金关系”。
- **meme-反证**：记录机制成立但后果相反、机制不成立却发生相似后果、数据不完整和计算成本等反例；提前冻结条件，不允许失败后通过重新命名“真吸筹/假吸筹”排除失败。
- **ai-d适用性**：检查新源到底改了哪个观察要求/竞争解释/产品决定；必要时选取数字取证、因果推断、过程挖掘、会计与统计学等相关问题视角，不强制固定专家，不能拿看起来复杂的分析替代实证。

### 两个已静态核查、尚未实跑Blix的反例

- Hermes合成\`场景05-信号冲突\`：20个Holder都有平铺资金来源\`native_transfer_from\`，按qb旧嵌套读取逻辑是**20/20读不到**；旧期待\`SM积累\`但结构critical，最终\`WATCH\`。新知识不能自动将它改为“庄家吸筹”或“安全买入”，应额外核取各来源真实转账、SM实际净交易、风险触发依据和来源字段契约。
- Hermes合成\`场景04-数据缺失\`：20个Holder原输入就没有资金来源，旧期待\`NEED_MORE_DATA\`；不能把它当“资金互不相关”或“资金来源为0”，也不能虚构未知机制。优先确定缺失发生在哪一层。

**验证边界**：目前是固定源文件与合成fixture的静态诊断；没有Blix当前数据源实测、独立A/B模型结果、真实Mint同一输入运行。其操作价值须通过后续只读业务验收而非新增标签数量证明。


## 2026-11-07｜Hermes三项旧指标的可复算失效：知识进入Blix之前的硬边界

本段针对Blix现有业务调用的知识修正来自 [Hermes×qb×meme纵深研究第11节](../../knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md#11-2026-11-07旧推理公式的反例复算与知识进入blix的检验)，与 [ai-d跨学科评测](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md) 相互关联；**知识已写入并不表示`server/research.js`已自动检索这些文件，更不表示实盘性能提升**。

用户要求“发现不符合旧模式的异动、主动深入追资金/库存、寻找未知机制”时，AI应把**异常研究资格**与**交易/安全筛选资格**区分。低社会热度、可疑指标缺失或无法立即落入某一庄家类别，仍可能值得只读研究；但此原则不允许绕过数据访问权限、真实费用或交易风险隔离。

**三项旧Hermes派生信号不可原样升格到Blix**：

1. `L1-B2 volume_momentum`：当币龄不足1小时且1h/24h量来自同一全部历史时机械等于24，不能按旧阈值触发“异常爆量”；应对比观测覆盖和相容时间基线。
2. `L1-E4 insider_activity_composite`：供应商`rat/bundler/entrapment`标记可能重叠或时窗不同，相加不是去重后的异常成交占比；不能把超过0.5称“内幕主导”，应保留源方定义和交集UNKNOWN。
3. `L1-C5 spread_quality_proxy`：在CPMM中USD计价的base/quote储备价值比通常接近1，与报价冲击/滑点并不等价；Blix既有`server/quality.js`和Quote/具体池型的可观测结果优先，禁止用旧代理虚构真实价差。

**调查信息的另外三条硬约束**：qb的`priority()`给Pool类加100并只取前25名，不能由“基础设施已单列”推断关键钱包召回充分；旧Hermes场景05确有20个平铺来源字段，但qb嵌套访问得到0，此时属于**读取合同不匹配**而非链上无资助；meme的20条`real_pending`样本即使`is_real_sample=true`也不能视为已确认实证。

**业务解释形态**：向用户报告该Mint实际可证据支持的观察、原始字段/事件与时间覆盖；提出多个机制候选和可区分的下一条证据；明确哪些旧阈值在当前币龄/池型/账户来源下禁止应用，哪些问题因缺失合同或回补而`UNKNOWN`。知识可以增加对未知经济现象的研究深度，不能用研究的开放性降低证据证明责任。

本次结果是**离线逻辑反例+固定mock字段访问+旧源码核查**，没有改变Blix交易/AI运行时程序，没有做独立A/B模型调用，也没有当前GMGN/链上实际响应验证。只有回归样本和现场结果证明更好时，才应把相关功能规则写入生产。


## 2026-11-07｜旧知识跨项目“真的能用”需要先消解qb留存Mint的语义矛盾

**新实查结果**：<https://github.com/sunshihao001/qb-/tree/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump> 包含真实留存的95条标准化钱包/候选证据，不是一个空的知识仓库。静态读取发现4个候选同源组、10个成员，但\`group_confidence=unknown\`；51/95个判断仍建议链上追证；43个地址在交接中列出字段缺口。旧\`data_quality_score=1.0\`同时存在这些缺口，所以**不能把局部质量指标当链上真实完整度**。

从95条钱包数据中，\`is_full_exit=true\`有54条、\`current_balance=0\`有57条、\`sold_pct=100\`有53条；4条“已全退”却没有观察到卖出量，另3条“100%卖出”却不标全退。**这不自动证明程序Bug，更不能把54条理解为54个经济主体已经出售退出**；转仓、观察窗缺失、字段来源不同等必须与原始Token Transfer和Swap记录区分。Top10\`51.019219%\`明确是“跟踪钱包余额中的比例”，不能读成总供应量51%。

同目录\`summary_overview.md\`记录94钱包且无交易数据，\`summary_overview.json\`记录95钱包和非零交易；后续目录Manifest只保证复制/迁移，并未保证报告来自同一时点或同一统计版本。**分析时先标版本/截止时间，不能融合冲突汇总作为同一事实。**

完整证据及追溯：[Hermes×qb×meme纵深研究第13节](../../knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md#13-2026-11-07qb真实留存文件核查反推全链经济身份与库存知识)；阅读状态和未审见[参考项目覆盖](../../knowledge/references/source-coverage-v0.1.json)。把此认识用到Blix时，应优先让用户区分**钱包不再有余额、真正Swap卖出、Token转移、群体净库存变化、实际经济受益人是否退出**；研究开放、主体归因审慎。当前没有Blix运行时集成或主网独立验证。


## 2026-11-07｜跨领域机制研究：一个异常不能被一个标签截断

用户明确纠正：**不以知识分类、专家标签、某个程序模块或单一来源作为研究边界**。Blix的六类目录、D01–D12、L0–L7和G0–G4只负责检索与追溯；它们不能限制对一个市场现象的完整经济解释，也不能以“已映射/已归档”宣布研究结束。此要求与 [Hermes完整反向发现研究](../../knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md) 联动，不创建另一套专家制度或阶段流水线。

**实际问题贯通示例：某Mint拉升前6–12小时出现大量转账。** 不只查“异常转账”：
- **资金事实与会计**：查SOL/WSOL、Token Account/Owner、fee payer、内部CPI、资产净变化、签名级去重、转账与Swap是否同笔；用qb-单Mint程序的地址矩阵和原始RPC/解析器检验，不把地址/同源当同控。
- **经济仓位与库存**：查接收地址何时买入、是否仍持有、是否跨Mint转移、是净建仓还是循环/归集；查LP/池子/程序地址和公共出入金设施。Hermes的来源汇聚只是候选，必须有库存和对价证据。
- **市场机制与时间**：对照meme-的生命周期、成本中枢、分发/接力/出货和失败形态；对照Blix的实时活动、价格可信度和历史覆盖；区分币龄、池型、时窗与历史回补。先检验旧公式的可测量性，不能直接复用错误`volume_momentum`、`spread_quality_proxy`、重叠标签求和。
- **竞争解释**：共同控制、公共设施、独立跟随、做市/套利、机械刷量、信息扩散、数据缺口等可能产生相似表象。每种解释要提出至少一个**能与其他解释区分的后续观察**，允许`UNKNOWN`和新机制假设，而不是强制贴“庄家/内幕/吸筹”。
- **Blix实际转化**：先问现有`coverage/triage/research/coin/holders/bubblemap/wallets/wtrack`分别观察到什么、哪些事实被丢失、哪条边被误归因、哪条有历史缺口；研究发现可用于“需要继续观察”而不等于“可以交易”。只在真实输入合同、离线反例、来源覆盖、运行验收成立时考虑最小代码修正。

**如何判定研究有意义**：一项来自Hermes/qb-/meme-/成熟成品的知识即使暂时无法运行，也值得深入，只要它能①纠正一个事实口径/错误因果推断，②揭示未观察的经济主体、库存或资本循环，③提出能被数据推翻的不同机制，④改善异常的发现/追踪/解释/安全，或⑤指出真实业务无法闭合的缺口。反过来，单纯把同一内容标注多个D域、创建专家卡或多写文件**不构成知识增量**。

**本轮已证实的具体限制**：Hermes三项旧L1有可复算的测量失效；qb旧字段读取与固定mock不一致；meme历史样本实证状态冲突。**尚未证实**：这些失效在现行GMGN/Blix真实运行中发生的频率、旧推理对未来事件的预测力、跨项目知识是否提升模型真实准确率。不要用本节取代这些尚需真实验证的问题。


## 2026-11-07｜按照ai-d最新问题生成研究重新理解“参考知识如何进入主体”

> **本节主要修正分析判断，不是改变Blix软件结构。** 源研究：ai-d @ `84b9d3fe4e22d6c1621623cf26deb4b3ab5092e7` 的[未知知识发现](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-problem-driven-unknown-discovery.md)、[认知增强](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-human-ai-cognitive-augmentation-foundations.md)、[任务委托/技能成长](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-human-ai-delegation-performance-learning.md)；更宽阔的上位愿景在[Draft PR #1](https://github.com/sunshihao001/ai-d/pull/1)不自动覆盖Blix业务。把“已有研究知识→实际正确调用”作为主要证据缺口，而不是通过扩充专家/目录来应对。

### 1. 重新定义问题：不能把“融合”仅理解为导入、索引或外挂Skill

**用户原话**：“参考项目中我不知道的知识，怎样全部深入研究并结合到现有Meme主体？” 对Blix的专业问题不止“哪份Markdown放在哪里”，更是：

- 参考项目原本在**回答哪些我们还没问出来的市场/工程问题**？其源码、数据/算法、历史失败、测试分别揭示什么？
- 相同市场观察是否可能由**真实经济活动、数据采集/保存/来源冲突、AI解释失误**三类不同过程产生？哪些现有知识的**中间变量**被漏掉？
- 每个新增观点能否让Blix的市场发现/单Mint/跨Mint/机制调查**新增一条可区分的解释、发现一个原本遗漏的重要对象、纠正一个错误事实或阻止误导**？否则是否仍值得保留原始研究但暂不激活？
- 用户希望AI**代办高专业门槛工作并交付**，而不是无条件接受讲课或逐步审批。是否需要学习是另一个任务目标；重大方向/交易/签名仍按权限由人决定。

**知识融合的深浅层次不同**：原仓库完整覆盖与深入理解（来源认知）；证明知识适用于当前问题（选择）；让它改变具体调查要求与竞争解释（推理）；Blix调用可观察事实并在报告/测试中验证（产品能力）；真实运行带来的收益/成本（验收）。目前主要位于前3层，原源码静态反例不能让后2层自动完成。

### 2. 用同一问题进行一次“问题升级”而不是再给旧知识分类

**假设任务**：用户问“为什么某些后来毕业或拉升的Mint，看起来都有早期专业钱包进场？是不是提前布局的同一操盘手？”

**旧问题表征**：查看聪明钱标签、同源资金与同步入场→聚类钱包→生成“早期协同”标签。失败：把归档记录看作随机且完整的链上样本，未问**这些事件为什么留存、何时入库**。

**问题重表征**：比较两种机制：
- `H_market`：真实存在先于行情的资金组织/库存准备与可重复执行过程；预期有事件时间先行、独立钱包/经济主体证据、连贯库存对价、在未后来成功的Mint中也用相同规则观察。
- `H_observation`：后续毕业/价格结果影响历史保存、筛选、标签、回补或索引，使“成功样本早期钱包更活跃”成为**选择性观察的产物**；预期不同保留条件下同一类事件是否入库会变化。
- `H_mixed`：市场确有行为差异，但留存机制放大或扭曲其观察幅度；需要同时测量原始全样本与保存样本，不可先验排除。

**A–B–C 机制桥接（不是凭关联造真理）**：
- A = 报告里看到的“成功Mint历史早期买家较多”；
- B = [Pulse `solana-stream.ts`](https://github.com/nirholas/pulse/blob/main/src/collector/solana-stream.ts)的观察→选择性持久化/后来毕业触发早期买家补存条件（已读源码，普通小单可能仅存在短时内存，超过规则或毕业时另存；实际样本和其他入口仍待全局查）；
- C = 数据分析里的**结果依赖型样本选择**可能造成伪相关；
- A→B 和 B→C 只是**可检验的中间关联**，不能无对照证明实际某次暴涨是由采样造成或否定真实操盘。

**值得执行的具体反证**：固定同一早期买入（非已标记钱包、金额低于5 SOL），仅改变后续是否毕业，按源持久化分支观察记录是否有区别；查其他可能回填路径、过期/淘汰、实际存储成功及Blix自己的存储路径。此前已做条件复算，`LIVE_PULSE_RUN=NOT_RUN`。对Blix [`journal.js`](../../server/journal.js)需另外核24小时保留、gap修复限制、所监听的交易类型；Pulse的交易采集规则**不能推出Blix或Solana原始SOL转账必然以相同方式漏记**。跨项目类比若没有对应对象/机制就是假连接。

**由此改变的结论**：调查报告从“未见早期资金→无准备行为”修为“在当前可见交易历史/选择/保存条件下未见，完整性与其他事件需另查”；若无法排除观察偏差，不能把某个长期模式认作经济主体控制或预测优势。这是可靠的**调查问题和限定语修订**，不是新增“伪庄家”标签。

### 3. 将未知分为四种认识责任，但不是永久知识标签

| 面对的未知 | 本项目实际例子 | 允许声称什么 | 不能声称什么 |
|---|---|---|---|
| 明确知识缺口 | 缺最新GMGN/OKX字段合同 | “供应商合同未核” | 旧字段名一定还有效 |
| **隐含问题缺口** | Hermes `native_transfer.address` vs qb `from_address` vs mock平铺字段 | “历史代码与固定样本存在可复算字段不兼容” | 链上真的没有资金来源 |
| **新跨行业机制联系** | Pulse结果依赖持久化 ↔ 统计样本选择；Hermes资金异常与多源优先顺序关系 | “代码规则可造成该种潜在偏差，需查具体调用和留出样本” | 仅凭类比断言任意Mint假信号 |
| 开放世界未知机制 | 新资本组织或此前没识别的Token库存/资金过程 | “发现可检验的候选假说与区分证据” | “AI发现市场已证实的新规律或Alpha” |

这张表是为了**分清需要什么证据**，不是要求模型只能研究四类知识。真正新学科、机制、代码来源在研究中允许追加；分类仅用于追溯而非限制发现。

### 4. 动态专家与人机分工：从谁来回答，变成何种证据能改变结论

- 对**历史异常**，需要数据工程/统计视角补入选择性留存、事件时间与可得时间；对**钱包同控**，需要数字取证、图/实体解析、经济仓位与反证；对**预测优势**，需要市场微结构/样本外统计/执行成本。不是召集固定22位专家或新Agent席位。
- ai-d最新文献将“AI在场帮助完成工作”“人的无AI独立学习”“人机组合优于最强单方”明确区分。Blix的成功目标首先是**成果交付及市场解释可靠性**，不能把用户能否独立写代码当作前提；需要时解释选择，但不无条件将代办改成教程。
- **AI主动性**意味着在用户授权内自主查原始资料、指出错误前提、选择能改变结论的观察、写入知识并回读；不是擅自启动生产服务、升级交易权限或把研究想法变成新的人生/产品目标。

### 5. 从“聪明叙述”进入可比较的能力检验

复用[ai-d评测现有设计](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md)：冻结同一实际或合成的历史源数据、代码版本、模型、工具和成本，比较**普通词面查找、按需相关专业知识、问题重构后按线索引入跨行业中间机制、过量历史/固定专家反面基线**。事先隐藏实际失败原因；用此前未读过的案例留出测试。

**评价的不是问题数量或回复长度**：看是否定位真实隐藏变量、有没有未经证据支持的新关联、是否误把未保存说成未发生、是否产生可复算的差异、是否真正改变调查/只读产品输出，额外工具/上下文/人类负担多少；更复杂却错因果更多应降级。

**本次状态**：ai-d新研究来源已核；Pulse/Blix/Hermes/qb/meme的旧源码静态反例已存在。**没有新增真实行情回放、没有独立隔离模型A/B、没有Blix运行时检索实验。** 本节属于“认知方法与产品判断修订”而非产品实现。下一次具体实施优先：找一组未用于当前设计的独立源码或冻结数据案例，检验能否在不知道答案前发现观察机制/市场机制的区别，随后才考虑是否需要增加任何检索/报告代码。


## 2026-11-07｜HoldTech新样本：从“同币、同Slot、同钱包”继续找可核验的隐藏条件

这次选 [HoldTech原始源码](https://github.com/co-numina/holdtech)，在 [参考项目全域纵深研究第10节](../../knowledge/references/source-knowledge-deep-study-v0.1.md#10-2026-11-07用此前未分析的-holdtech-源码检验ai-发现隐藏变量) 做了**七项源级确定性反例复算**。这不是已部署的新知识推理代码，不是模型独立盲评，不启动原程序/付费API/真实钱包分析。它具体说明：**不能把功能名/指标名当观测事实，也不能把观测事实直接当经济机制**。

**面对同Slot/Bundle**：先问哪些真是`SWAP`买单、真实Token和SOL净变化、交易Fee Payer/Token Owner是否相同、是否存在共享代付/公共基础设施、是哪一个池/发行阶段；HoldTech `detectBundles()`会把3个不同Fee Payer的`TRANSFER`/未知事件聚成Bundle，故不能直接照搬它的“同期买入/同控”结论。Blix自己的`bubblemap`资金边也有Fee Payer角色风险，应同标准审查。

**面对持仓强度和“钻石手”**：钱包首次链上活动时间只代表钱包历史下界/估计，不代表**此Mint首次持有、持续未卖或经济库存成本**。HoldTech `holdDurationDays = walletAgeDays` 的代码可使一个365天老钱包刚买1小时也被记作长期持有。Blix若复用专业知识，应优先追Token Account/Owner资产变化与历史覆盖，缺失则`HOLD_DURATION_UNKNOWN`，而不是把老钱包等同老筹码。

**面对跨Mint群体重叠**：先查输入是Token Account还是Owner，Owner多Token Account是否求和，查询是否完整/有分页截断、快照时点是否一致、是否混入池/CEX/服务、共同持有是否在两币同一时刻可见；HoldTech`getHolders(m,200)`内部请求一次1000个账户后才判定循环边界，不能假定200恒定分母。合成600/1000重叠算60`CRITICAL`，而相同交集对各20000完整Owner仅3，且持有人交集本身不证明协同或共同控制。

**面对历史第一资金来源**：HoldTech`getSignaturesForAddress(limit:20)`得到最近20条而非出生以来最早20条；它将净入SOL交易的Fee Payer当作funder，也可能把第三方手续费代付误为SOL出资。Blix现有`bubblemap.js`的相关回退规则不可因外部项目采用相似方法就获得额外背书。真正来源需追资产净增、真实SOL转出指令、时间/签名/分页覆盖，并保留公共服务竞争解释。

**这次认知如何变为产品判断**：上述现象可以作为只读调查触发器，却不得直接写成“操盘手/内幕钱包/同步吸筹/真实利润”等身份或交易信号。现有Blix`holderslive.js`有按Owner汇总Token Account的实现，应保留作为对照而非重复造轮子。适用的跨项目知识要实际改变一条调查问题、证据口径或测试；不能因为“目录已关联”就宣称AI自动应用。

**证据状态**：原始HoldTech源码/Blix对应模块已核、官方Solana Fee Payer/RPC语义已对照、七组简化逻辑反例已复算；未对原程序或Blix执行独立单元测试、实链监控、同输入模型A/B。**新经济市场机制尚未被证实**。


## 2026-11-07｜认知校准：反证不等于否定，未知不等于无行动

> 用户直接纠偏：先前基于Hermes/Pulse/HoldTech的研究过度集中于识别错误与不允许宣称的事实，容易形成**反向确认偏误**——只找反例，提前降低值得调查的高价值异常。此处对旧条款做**范围修正**而非否定：数据口径、角色区别与原始证据核查仍保留，但不能用“尚不能证明经济主体”替代对证据强弱的积极判断。

**真正的研究问题不是“这条线索有没有反例所以应否定？”而是“当前证据使哪些解释相对更值得相信、还有哪项证据最能改变排序、现在是否值得继续观察或深入调查？”**

同一市场异常可以同时满足：`OBSERVATION_VERIFIED`（事件真）、`COORDINATION_PLAUSIBLE`（多条件支持的行为协调候选）、`SAME_CONTROLLER_UNRESOLVED`（同一控制主体未证实）、`WATCH_PRIORITY_HIGH`（值得只读优先监控）。这些是**报告语言示范而非新增必须实施的程序字段或固定置信度等级**；不以`UNKNOWN`抹去已有积极证据。无需每轮按固定表格覆盖所有疑点，证据强且重复的结论应简明直说。

**一个从弱到强的完整例子（设计假设，不是实际Mint）**：
- 仅3个不同Fee Payer在同Slot`TRANSFER`：只能称“同Slot事件关联，待识别动作与资产”，不能直接称共同买入。
- 若解析出3笔**独立可追溯的真实Token净买入/报价资产支付**，时间接近，且钱包由同一**明确可定位的SOL实际转出地址**提前注资：与普通无关转账相比，**“存在协同行为”成为优先假设**，可主动提升调查/监控优先级。需要区分该来源是否公共服务，但“可能是公共服务”不能在无具体证据时一票否决。
- 若在多个Mint进一步观察到可重复的**先分发Token库存→接收地址分批卖出→资金回收或再部署**、一致的经济时序和资金/库存守恒：资金组织/库存接力假设继续增强，值得形成有依据的机制候选；可比较独立钱包和正常服务的基线。
- 若链上交易重放、可靠服务标签或账户权限关系反而表明共享Fee Payer只是公共代付、钱包独立执行、库存未转移，则**根据新证据下调特定假设**，但不因此否定此前存在真实同步买入等事实。
- 无论哪一步，**“异常值得调查”与“已认定犯罪/操纵/幕后身份”以及“具有可交易Alpha”均为不同主张**；只读监控可以用更低证据门槛，身份定性和涉及真实资金的决策需更高要求。

**正反证对称，拒绝双重标准**：
1. 支持证据也要审来源、角色、覆盖、时间、数据选择；反证也必须指出它**实际上能解释/推翻什么**，不能凭某个理论替代解释的可能性就撤销正面发现。
2. 已知成熟项目有局部指标或资金角色误归因，不代表其整体产品无用；保留可用的市场观察、Holder/Bundle候选、历史工程经验，限制的是不成立的**具体解释**。
3. 不要求每次调查穷尽其他机制，不用“假设永远可能”阻止推进。比较**下一条核验能否改变机制排序或只读监控行动**，无进一步信息价值则收束成阶段性倾向结论。
4. 不凭空输出“80%可能同控”等未经校准的概率；可以用“弱线索/多项独立支持/较强候选/仍存在重要替代解释”等自然语言描述，注明何种证据会升级或降级。
5. 保留主动发现新机制的探索空间，不因现有反例集规定了旧错误类型就只会寻找同一类问题。**反证和新假设生成是双向循环，而非只有拒绝权的审核流程。**

**在Blix已授权范围内应主动完成的行为**：来源核查、跨项目比较、只读条件复算、候选对象调查方法与文档修订、核验写回；不得自动启动未授权的实盘交易、签名、付费API或生产部署。此处没有改业务代码，也没有声称验证实时预警的准确率。

**用什么验收修正有效**：新增对照任务不能只测试“避免误报”，还要测试“避免**过度保守导致漏掉真正强异常**”：相同原始证据下记录有价值线索召回、错误归因、结论强度是否与证据相称、调查优先级是否合理、额外核查成本。若过度怀疑使系统大量丢失有价值线索，即使答得谨慎也应判失败。


## 2026-11-07｜多种目标版本怎样改变同一Mint的调查结论

[项目目标图的“多主体目标与多专家视角”专项修正](goal-map.md)进一步将“不同主体的经济动机”和“专家按问题采用的解释视角”分开；不是新增四套Bot、四个专用报告或新的固定权限。**核心任务从“给钱包打一个角色”扩展成“在某种市场环境中，哪些可能目标能够生成当前观察；哪些预测能区别它们；哪种认识对当前用户最有价值”。**

**同一条市场场景的动态多目标演示（虚构示意，非已回放Mint）**：Mint M发行后，12个地址短时间买入；其中6个收到实际直接SOL转入；随后多个地址将Token转往接收地址，接收地址在交易量上升后卖出。

- **链上取证者**希望判断真实SOL发出者、Token库存是否完整转移、接收地址和公共设施角色。若真实资金/Token路径连贯，则可以积极提“资金组织/库存接力”的高优先候选，不能因未证明幕后身份就抹掉线索。
- **经济机制研究者**问为何组织要提前分配库存、在什么流动性与需求约束下集中或分批退出、交易活动是否是工具还是目标；注意Pump.fun Creator fee可能使价格利润和交易量收益同时存在，但单看fee制度不能推导意图。
- **短线市场参与者**关心发现延迟、代币库存、池深、滑点与实际退出能力。即使确认一个有组织的群体，也可能因成员早于公众、出货更快、流动性不足而**没有可复制优势**；反之，同控身份未知但持续资金异动真实，仍值得观察。
- **市场微观结构分析者**会查交易与价格变化的因果时序、池间价差、套利与MEV/代付，从而解释部分共同Slot/价格变化；要有原始多池/对价证据才可使其超越假设。
- **统计和数据质量视角**核两个时点是否使用相同采集、Owner聚合、Token转移/Swap口径和可得时间；如果没有完整覆盖，**限制的是某项比例/预测结论**，不是因此否定全部真实观察。
- **长期机制发现视角**会追相同实际SOL来源是否跨Mint参与，组织成员与角色是否变化，独立用户入场如何反馈到前一群体的退出策略。若新事实超出已有候选，允许新增机制而非强行塞入“庄家/狙击手”标签。

**如何综合这些不同目标而不在内部投票**：
- 对**当前事实**，不同视角共享签名、Slot、SOL/Token资产变动、Owner/fee payer/pool、可得时间、供应商及覆盖，不能各自编造。
- 对**经济解释**，允许多个并存的目的与互相制约的行动者；每种假设对应自己的区分性后续观察，比如直接资金链/库存回流支持组织、跨无关发行者重复抢首块支持独立狙击、跨池快速对冲支持套利。若两个解释都能解释同一事实，不是假定两派专家必须争个输赢，而是选择有信息价值的差异证据。
- 对**市场行动**，直接采用“下一步应该监控谁、看哪个变化、何时需要重新排序”这样可执行的只读调查输出；并不自动把“发现群体结构”变成买入建议。
- 对**目标变更**，用户选择的市场情报目标仍优先；新增“机会优先、风险优先、机制优先、研究新领域优先”只是可能的使用问法，当前不形成互不相容的新系统版本或默认交易策略。

**外部原始依据/边界**：[Jito原子Bundle文档](https://docs.jito.wtf/bundles/)明确Bundle与同Slot不是同一类证明；[Pump.fun费用与Creator fee](https://pump.fun/docs/fees)支持除Token买卖外的激励考察；[Bitquery 2026-10市场调查](https://bitquery.io/investigations/pump-fun-snipers-bundles)对block-0买家用了开发者相关/跨开发者sniper等区分及Jito抽样，属于第三方有条件分类，非具体钱包身份真值；[Meme Coin Factories](https://arxiv.org/abs/2609.10246)支持操纵市场信号的多种机制确实值得调查；[逆向规划的多主体研究](https://ojs.aaai.org/index.php/AAAI/article/view/4574)只提供从行为假设推断隐变量的概念方法，未在本项目实证校准。

**当前状态**：认知综合与现有Blix业务语义对照完成，尚未更改运行时代码、生成真实Mint的参与者目标推断或验证市场获利。以后阅读其他参考项目时，要看它**提供了新的参与者目标/收益约束、区分性机制、专业解释、还是新的产品使用目标**；不能因目前没该类标签就剪掉新发现，也不能因为专家观点不同而将全部归为UNKNOWN。


## 2026-11-07｜把多目标从理论接到真实归档Mint的三时点变化

[**真实案例：三份GitHub Actions归档的原始DEX与RugCheck数据逐文件SHA复核、价格/池库存变化复算和多专家目标比较**](single-mint-audit.md#2026-11-07真实单-mint-三次归档快照多参与者目标与动态证据修正) 使用同一真实Mint的2026-11-01 02:44、03:23、03:26 UTC三次供应商快照，跨越约42分钟：

- 主PumpSwap池Token余额`57,331,535 → 58,774,685 → 58,374,413`，SOL余额`465.47 → 457.4104 → 461.07165`，价格`$0.0008148 → $0.0007653 → $0.0007819`。前段呈现**卖入池方向特征**，后段呈现**相反的买入回补方向特征**。这是应**积极调查并按新证据更新**的候选解释，不应因“没证明庄家”直接删掉；但LP变更、费用、供应商时间差仍可能解释一部分或全部。
- RugCheck头部Token Account的Owner与PumpSwap池地址跨源一致，持仓比例为供应商约5.88%/5.97%，与DEX池库存快照不同步；不能将该数字当独立鲸鱼集中度，也不能跨源直接差分成真实链上出货。
- 旁边Orca池流动性约`$47.7`，主PumpSwap池约`$89k–91k`；03:23两池`priceUsd`差约1.57%，但**观察到价差不等于可执行套利利润**。市场机会视角关注执行报价/滑点，取证关注签名/池Vault，发行者激励研究关注真实Creator和费用，数据工程关注取数时间与快照一致性。
- **真实验收层次**：已取得三次源归档而非合成交易模拟，并离线复算供应商值；没有原始Solana交易/LP指令的全周期归因、没有Blix本体实跑、没有量化策略Alpha验证。下一条决定性证据是这42分钟的真实Swap/LP事件及事件签名。**停止再扩充专家视角列表，优先推进会改变经济解释的原始事实**。
