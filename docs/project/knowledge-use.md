# 按实际问题使用专业知识、AI研究与可证伪证据

**新认知入口**：[Hermes生框架、qb数据护照、meme反证与多对象经济过程](../../knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md)。根据任务需要用因果、过程挖掘、取证等问题视角生成竞争解释，未审来源保留UNKNOWN；不是新增固定专家、硬标签或运行时强制Prompt。


**主体认识优先入口**：先看[主体能力与旧知识内化深审 V0.2](blix-knowledge-activation-ceiling-v0.2.md)（按业务判断上限、旧方法适用、不能继承的规则），再按需回查下述来源。

**主体认识优先入口（原基准）**：[Blix 已有业务能力 × 旧 Grok 专业知识继承基准](blix-heritage-capability-baseline-v0.1.md)。面对实际业务先定位 Blix 已有 UI/数据/逻辑，再按需要调用 PR #14 的原专业正文或 Hermes/qb-/meme- 的机制，不全文搬迁、不把旧历史程序当作已在 Blix 运行。

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
