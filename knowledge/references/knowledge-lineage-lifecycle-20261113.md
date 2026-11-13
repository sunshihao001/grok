# Blix 知识全链追溯：获取、原意重建、承接、融合、使用、反证与修订（2026-11-13）

> **用途**：对现有 Blix/Grok/Hermes/qb-/meme-/ai-d 的知识来源、判断形成、产品继承和实际验收做统一解释及可复查示例；不是新专家制度、新运行时状态机或“所有知识已验证”的声明。原始知识只维护原位置，本文件只提供**链路与裁决索引**。P1–P2 专业证据细目仍在 [现有专项](p1-p2-knowledge-reconciliation-20261113.md)，逐来源审阅进度仍在 [覆盖账](source-coverage-v0.1.json)，实际代码/CI及未结阻断以 [建设台账](../../docs/project/build-register.md) 为准。
>
> **本轮核查**：对照本仓 \`MIGRATION.json\`、\`DOMAIN-MODEL.v1.json\`、\`legacy-knowledge-routing.v1.json\`、\`source-coverage-v0.1.json\`、\`local-knowledge-loader.mjs\`、\`economic-events.mjs\`、\`economic-network.mjs\`、本地测试和 PR #23；并回读 [ai-d知识组织规范](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/organization-protocol.md)、[ai-d知识总入口](https://github.com/sunshihao001/ai-d/blob/main/knowledge/INDEX.md)、[Hermes证据链](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-05-evidence-chain.md)、[Hermes钱包结构](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-04-wallet-structure.md)、[qb-旧钱包事实](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_fact/wallet_fact_report.md)、[meme-真源地图](https://github.com/sunshihao001/meme-/blob/main/SOURCE_OF_TRUTH.md)。公开成熟参照：[W3C PROV-O](https://www.w3.org/TR/prov-o/)、[OpenLineage模型](https://github.com/OpenLineage/OpenLineage/blob/main/spec/OpenLineage.md)、[DVC版本机制](https://doc.dvc.org/user-guide)、[Google Skill Reach](https://github.com/google/skill-reach)。对外部代码与文档的观察只支持其公开设计/实现，不表示在Blix安装或完整运行。

## 一、真正要追溯什么：知识不是一个文件或一句结论

以下对象不可互代：

| 对象 | 要追溯的核心问题 | 示例 | 最常见误判 |
|---|---|---|---|
| **意图/问题** \`QUESTION\` | 谁提出、原话/目标是什么、什么尚未确认？ | “这些钱包是否一起出货” | AI提出的解释被记成用户已批准的事实 |
| **原始来源** \`SOURCE\` | 作者、版本、路径、发布日期、许可证、访问与覆盖？ | 一版Solana RPC协议或Hermes Skill源文件 | README或转载=已经独立验证 |
| **原始数据/观测** \`OBSERVATION\` | 链上签名、指令、单位、时点、采集覆盖、缺失、不同供应商？ | RPC交易 \`sig + outer_i + inner_i\` | 数据缺口当成零事件 |
| **概念/术语** \`CONCEPT\` | 定义、上/下位、同义、不可混淆的相邻概念？ | Token Account/Owner/Fee Payer | 相关概念被当作同一个对象 |
| **主张/解释** \`CLAIM\` | 是谁的主张、被哪项证据支持/反驳、有何前提？ | “同资金源可能有协调行为” | 作者假说=链上已经确认控制者 |
| **机制/方法** \`METHOD\` | 为什么有效、在哪些条件下失败、怎样比较替代方法？ | 解析转账、聚类、成本追踪 | 固定阈值/通用函数跨场景无条件复用 |
| **案例/反例** \`CASE\` | 原输入、时间、结果、历史版本、另一解释、如何复现？ | qb-一个Mint的95地址报告 | 选中成功案例推断全市场规律 |
| **能力/实现** \`IMPLEMENTATION\` | 选用了哪段程序、数据合同、依赖、许可、权限？ | Blix已有 \`economic-events.mjs\` | “复制源码”=服务上线 |
| **判断/决定** \`DECISION\` | 由谁授权、依据、竞争选项、为何选/暂不选？ | 只读复用已有SQLite而非重建DB | AI建议自动升为产品强制制度 |
| **验收/运行** \`EVALUATION\` | 测什么、在哪个commit、合成/真实、过了哪些测试？ | Node24 CI、真实Mint审查、模型A/B | 离线CI=真实主网正确率 |
| **修订/撤回** \`REVISION\` | 旧判断为何错、什么证据替换它、下游受何影响？ | Fee Payer不等于实际SOL资助 | 新文档悄悄覆盖旧说法，失去反证链 |

**来源可定位≠主张真实；主张理论上有条件成立≠当前样本已观测；源码运行成功≠经济因果已证；检索命中≠模型用对。** 这些是不同维度的状态，而不是一条单向升级的百分比。

### 1.1 外部成熟概念应该怎样取用

- **Provenance（来源/加工溯源）**：W3C PROV把 **Entity**（文件/主张/数据）、**Activity**（研究/解析/修改）、**Agent**（作者/执行者）及\`derivedFrom\`、\`wasRevisionOf\`等关系分开。Blix只需保留这些思想：为什么一条主张经何人/何活动从哪个版本形成；不必安装RDF知识图。
- **Data/Process Lineage（数据与处理谱系）**：OpenLineage区分 **Job**、**Run**、**Dataset** 与输入/输出版本。适合区分“某程序理论可运行”和“这一运行真的读了这批RPC、产生了这个输出”；不意味着引入其生产事件采集平台。
- **Versioning / Reproducibility（版本与可复现）**：DVC借Git和数据/流水线版本记录重现实验。Blix目前优先用现有 Git SHA、source blob SHA、SQLite原始交易hash、签名/测试case，只有大规模版本数据成为真实瓶颈才考虑引入DVC。
- **Concept system（概念组织）**：上位/下位、别名、相邻概念、因果/证据关系必须分开。同义词扩展便于搜索，但“钱包同源”和“经济共同控制”不是同义词。
- **Knowledge retrieval and use（知识检索与应用）**：Google Skill Reach把召回、误触发、与其他技能冲突、多轮选择分开；对Blix意味着知识片段是否命中、是否正确引用与是否改善判断要分别测试。
- **Evidence synthesis（证据综合）**：论文、源代码、作者叙述与真实链上事件可相互约束，却不天然是互相独立的证据；多份转载或同源AI回复不能算多项独立验证。

## 二、整条知识链：不是固定闯关流程，而是能向前也能反查的联系

| 环节与概念 | 必须了解的内涵 | 最小保留对象 | 何时转入下一处理 |
|---|---|---|---|
| 0. 问题形成 \`framing\` | 用户原意、研究者追加问题、目标适用范围；不要被现成标签锁死 | 目标来源/约束/核心未知 | 问题已足够确定；也允许探索中修订 |
| 1. 发现 \`discovery\` | GitHub仓库→README/源码/测试/Issue/历史，评论/论文/书/官方等多源；同义、多语言检索，找反方 | 检索词、候选源、排除理由、未覆盖部分 | 找到高信息价值来源或明确缺口 |
| 2. 获取与固化 \`intake/snapshot\` | URL、仓库/ref/commit/blob、页面日期/获取时间、许可证、原始摘要或本地只读副本；保存版本，不一定复制全文 | \`SOURCE\`版本和可定位路径 | 可回到原文与代码相同版本 |
| 3. 来源原意重建 \`reconstruction\` | 原作者要解决什么、架构/取舍/限制、API数据合同、代码与文档冲突、真实测试和未公开部分 | 来源的问题、设计推测与代码观察分栏 | 不再只知道“它有哪些功能” |
| 4. 知识提取 \`extraction\` | 概念、事实、主张、机制、方法、隐含前提、反例、失败方式；区分作者说和我们推 | \`CLAIM\`+证据/替代解释/边界 | 能表述至少一种可推翻条件 |
| 5. 对照与新认识 \`synthesis\` | 多项目同义/矛盾、不同测量定义、反事实、桥接理论；不强行消除不一致 | 关系 \`supports/contradicts/related/depends_on\` | 产生可复查的新问题或修正 |
| 6. 吸收/承接选择 \`adoption\` | 四种命运：**只保存源**、**吸收到原知识正文**、**迁移方法/可复用代码**、**暂拒/撤回仍留痕**；纯理论不强求功能落点 | 决策、源/目标路径、取舍、许可/权限 | 有清楚承接位置，或明确保持OPEN |
| 7. 原位组织与检索 \`organization/retrieval\` | 一项主知识维护一个位置，多入口关联；按当前问题只取相关片段、注明版本/撤回，不全文灌模 | Blix D01–D12/六类目录/11个可选源 | 任务确实需要该知识 |
| 8. 产品应用 \`application\` | 修改事实合同、测试、独立只读工具、报告或AI解释；区分知识内化与单纯函数移植 | 代码commit、调用轨迹、输出字段、来源 | 可以复现相关行为和错误边界 |
| 9. 验证 \`validation\` | 静态源核/离线fixture/CI/实链RPC/模型A-B/样本外分别验，不能混等级 | 明确输入、截止时间、输出、对照与失败 | 该项主张在其声明范围内足够可信 |
| 10. 反馈修订 \`revision\` | 新协议、价格市场变化、测试失败、证据撤回与目标演变；分析下游受影响项 | \`supersedes/invalidates/tested_by\`、修正记录 | 新来源使旧认识降级、复审或复开 |

**并非每个问题必须执行十一段。** 一笔已有签名可直接事实核验；独立学术问题可以止于机制研究；单个Bug可以只改既有测试。生命周期只要求结果能够按需追到上游，不要求每次写11份报告。

## 三、完整可逆追溯：从用户结论往回走，不能只保存资料清单

一个较可靠的关系链：

\`\`\`text
用户当前问题/授权
  ├─ uses → 项目问题表征（Mint、钱包、时间范围、判断对象）
  ├─ retrieved → 原专业知识片段@source hash
  │   └─ derived_from → 已阅读原文@原仓commit / 官方协议@版本
  ├─ observed_from → 原RPC/供应商事实@签名+指令位置+slot+时间+采集源
  │   └─ transformed_by → Blix解析器@代码commit → 中间事件@来源/未知
  ├─ supports/contradicts → 具体候选主张（非对整个文档背书）
  ├─ interpreted_by → AI解释@模型版本/提示上下文/工具调用/费用
  └─ tested_by → 固定fixture / GitHub CI / 真实主网 / 模型A-B
       └─ superseded_by → 新证据/修订记录（旧版保留而不再默认应用）
\`\`\`

### 3.1 追溯的六种不同目的

| 追溯问题 | 必须查的对象 | 返回“还不清楚”的常见原因 |
|---|---|---|
| **出处溯源**：这个结论谁先提出？ | 原仓SHA、作者、文档和实际主张段落 | 只有AI总结或转述，没有原文 |
| **证据溯源**：它为什么成立？ | 签名、指令、行情、样本、失败反例 | 只有标签/推断或未覆盖的链上历史 |
| **加工溯源**：数值怎样计算？ | 数据合同、公式/源码commit、去重规则、来源窗口 | 来源单位、分母、fee或Owner不明 |
| **知识承接溯源**：借来了什么？ | 原意、差异、改动、落点、许可、拒绝部分 | 只写“吸收了项目”，没有迁移判断 |
| **执行溯源**：这次程序实际做了什么？ | 工具参数、源与输出hash、运行ID/CI、授权 | 只有文件存在或模拟输出 |
| **修订影响追溯**：旧观点改了什么？ | 替代/反证关系及依赖它的报告、测试、知识入口 | 只更新单段落，旧路由/标签仍在用 |

尤其要避免三个常见的概念混淆：**同义关系不是因果关系、继承某种研究思维不是复制一段源码、获取足够的信息不是已经证明解释正确。**

### 3.2 如果要为某项重要结论留下最小记录

一般采用现有知识正文中的一小段即可，不需要为每条知识都建JSON：

\`\`\`yaml
question: 这条关系是不是同一主体控制？
source: 原仓路径@commit 或 RPC签名/slot/指令位置
claim: 观察到钱包A向B的Token转移
type: OBSERVED_FACT
method: 复用现有economic-events原指令解析；保留Owner/Token Account差异
supports: 存在链上转移边
alternatives: 转仓、路由/池、公用托管、普通第三方
cannot_prove: A与B属于同一经济主体；B卖出的必然是此次转入的库存
used_in: 本地Mint专业调查报告facts.network
tested_by: test/economic-network.test.mjs（合成离线测试）
runtime_validation: UNKNOWN
revision_trigger: Token-2022费用/Owner冲突/多CPI或缺历史证据
\`\`\`

一个来源可能支持几条相互独立的主张，一条主张也可能有多个不同来源。不能用一个文件的“已审核”状态替代文件中所有结论的真实性。

## 四、现有五条知识来源怎么承接，哪些该保留或拒绝

| 原来源、原问题 | 可保留的认识 | Blix内当前承接位置 | 被拒绝/降级的错误继承 | 此次可确认状态 |
|---|---|---|---|---|
| [Hermes钱包结构Skill](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-04-wallet-structure.md)：同源/同时/相似卖出 | 将钱包关系拆成资金、时序、行为证据的**候选生成方法** | [D04钱包角色](../mechanisms/wallet-roles-and-inventory.md)、[D05资金组织](../mechanisms/capital-organization-and-incentives.md)、Blix原Bubble Map与新Token边 | 5分钟、3钱包、同源强关联的旧阈值未经过现在的市场基线校准；Fee Payer不能当SOL资助 | \`SOURCE_READ / METHOD_ADAPTED\`，非共同控制实证 |
| [Hermes证据链Skill](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-05-evidence-chain.md)：综合证据与反证 | \`evidence/counter_evidence/missing_fields/downgrade\`、短期有效性与交接问题 | [D11反证](../cases/independent-validation-and-failure-cases.md)、PR23只读报告未知字段 | \`baseConfidence=0.8\`、\`CONTROLLED\`或\`DEV_EXITED\`旧阈值不能直接当校准概率或经济事实 | \`SOURCE_READ / PARTIAL_METHOD_ADAPTED\` |
| [qb-真实留存95钱包调查](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_fact/wallet_fact_report.md)：关键钱包与库存 | 原本问题：关键钱包类型、跟踪余额、同源候选与未回补字段。保留多表调查和覆盖缺口 | [D04/D06库存](../mechanisms/wallet-roles-and-inventory.md)、[P1/P2核查](p1-p2-knowledge-reconciliation-20261113.md)、本地Mint流向报告 | \`data_quality_score=1.0\`不能代替完整链上覆盖，\`full_exit=54\`不能直接说54位主体卖出，Top10 51.019219%分母只是被跟踪钱包 | \`REAL_RETAINED_CASE_READ / CURRENT_MARKET_REVALIDATION_PENDING\` |
| [meme-策略真源](https://github.com/sunshihao001/meme-/blob/main/SOURCE_OF_TRUTH.md)：规则、知识与桥接层区分 | 版本/适用性/真源优先级、价格结构作为研究假说；有些理论值得保存但不必上线 | [D03价格机制](../mechanisms/market-price-mechanism-research.md)、[D08/D09跟单](../mechanisms/strategy-and-execution-economics.md) | 不能把AVWAP/FCZ价格锚解释成庄家实际成本，或把图形回收当样本外Alpha | \`SOURCE_READ / CONCEPT_ADAPTED_NOT_ALPHA_VALIDATED\` |
| [ai-d知识组织规范](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/organization-protocol.md)：人机协同知识保存和去噪 | SOURCE/CONCEPT/CLAIM/METHOD/CASE/DECISION/EVALUATION与复查、关系、停止；问题先于资料类型 | [D12](../ai/intent-knowledge-selection-and-reasoning.md)、现有 \`local-knowledge-loader.mjs\` | ai-d通用方法不是Blix当前已完成AI训练；固定P1–P8不是市场业务顺序，不新增强制专家团队 | \`METHOD_READ / LIMITED_LOCAL_ROUTING_TESTED\` |
| [Solana协议与真实RPC](https://solana.com/docs/rpc/json-structures) | 交易格式、Account/Owner、CPI、资产变化、版本与缺口约束 | [D01](../foundations/solana-chain-and-market.md)、\`economic-events.mjs\`、\`economic-network.mjs\` | 完成一个Transfer解析≠所有版本/Token-2022 Fee/Hook/Swap经济归因都正确 | \`PROTOCOL_SOURCE_READ / OFFLINE_COVERAGE_PARTIAL\` |

现有 [\`MIGRATION.json\`](../MIGRATION.json) 把**完整迁入的旧知识**和只登记的原始源分开；[历史卡](../methods/legacy-grok-core-cards.v1.json) 与 [21快照来源清单](legacy-snapshot-sources.v1.json) 是另一种用途，不能把15卡+21索引算作36份全部逐字审查过的专业结论。旧 \`legacy-knowledge-routing.v1.json\` 的152问题映射、65参考登记是导航结构，不能当作审计完成数。

## 五、当前实际发生过的“错误→修正→能力”链

### A. Fee Payer 误当资助者

- **原始问题**：Hermes/一般钱包关系思路需要识别初始资金来源，部分数据可见Fee Payer/同源候选。
- **专业反例**：付交易费和直接向目标地址转SOL是两种不同链上经济事实。公共程序、服务商、代付者可导致虚假“资金同源”。
- **代码落点**：Blix已存在的 [\`server/bubble-funding-evidence.mjs\`](../../server/bubble-funding-evidence.mjs) 与 [\`test/bubble-funding-evidence.test.mjs\`](../../test/bubble-funding-evidence.test.mjs) 区分直接SOL证据、只有Fee Payer、截断历史与未知。
- **承接裁决**：保留原始问题及多跳调查方法，**不继承“Fee Payer代表同控/实际转资”的旧推断**；新图中未核对的公共设施仍保持UNKNOWN。
- **验收边界**：离线测试与已存在源码可以复查，不以此宣称本Mint实际操控方已识别。

### B. “转入接收钱包又出现卖出”如何追到原始证据

- **来源/问题**：[qb-旧关键钱包矩阵](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_fact/wallet_fact_report.md)、Hermes证据链与“转仓不等于出售”。
- **数据输入**：已有 SQLite \`econ_transactions\` 保留原始RPC与sha256；\`econ_instructions\` 按签名+外/内指令位置存Token转移；\`wallet_trades\` 是局部交易摘要，不能强行与Transfer双计。
- **加工**：[\`scripts/inspect-economic-mint.mjs\`](../../scripts/inspect-economic-mint.mjs) 提取受限本地发送地址/接收地址；[\`economic-network.mjs\`](../../server/intelligence/economic-network.mjs) 以BigInt保存gross转移、方向和净转移，避免重复计数。
- **解释**：本地接收方“后来有卖出摘要”只支持\`LOCAL_SELL_SUMMARY_OBSERVED\`，**不支持“卖的是刚转入库存”**；Pool/Router/Token-2022费和全历史缺口明确列出。
- **复验**：[\`test/ai-economic-workflow.test.mjs\`](../../test/ai-economic-workflow.test.mjs)、[\`test/economic-network.test.mjs\`](../../test/economic-network.test.mjs) 为合成归档/离线规则回归，DB前后hash校验；真实Mint全链运行还未完成。

### C. “前兆变多”如何避免历史回补伪信号

- **历史观点**：旧研究关注6/12小时钱包转账激增、同步、群体时序。
- **冲突因素**：同一Mint本地数据库补查了一批旧交易，后续报表会出现“新增可见”，但链上事件实际可能早就发生。
- **落点**：[\`economic-snapshot-review.mjs\`](../../server/intelligence/economic-snapshot-review.mjs) 区分本地新增可见、已知记录不再在样本中、原交易数据修订；跨Mint重复地址仍只是候选。
- **不应推出**：刚发生的新链上转账、隐藏控制者正在拉盘或群体真实出货。
- **下一证据**：采集时间与链上事件时间/首次可见时间、连续完整样本、未上涨Mint、实时数据遗漏率。

### D. 旧知识如何真的被AI调用，而不只是“资料存着”

- **知识真源**：现有[11种受限来源](../../server/intelligence/local-knowledge-loader.mjs) 的原文件、SHA来源指纹、适用修正与撤回警示。
- **选择阶段**：自然语言的专业同义词/证据缺口启发式选源；\`test/local-knowledge-loader.test.mjs\` 有正例/负例；不默认加载所有历史文档。
- **使用阶段**：模拟模型在 \`ai-workflow.mjs\` 中可接收证据/有限知识，提供竞争解释与下一条核查；不允许知识文本赋予工具权限。
- **真正尚缺**：同一问题固定数据、模型、预算的无知识/旧路由/新路由 A/B；评估引用是否对应具体源段、是否误用已撤回数值、是否减少错判。即使路由测试16/16，也不能宣称模型已掌握152条知识。

## 六、现有知识资产状态：什么完成了，什么只是登记

| 已存在资产 | 正确的“完成”意义 | 不可升格的声称 |
|---|---|---|
| [21项\`MIGRATION.json\`](../MIGRATION.json) | 部分历史研究正文/卡/来源清单按类别被登记或复制（以单项\`status\`/来源说明为准） | 21项经过市场事实验证 |
| [152项路由、65项参考资产](../../docs/project/legacy-knowledge-routing.v1.json) | 旧问题域和参考资料拥有统一导航 | 152项专业知识都核验、65项源码全读 |
| [\`source-coverage-v0.1.json\`](source-coverage-v0.1.json) | Hermes、qb-、meme-与8项外部成品的树级清单和选择性精读状态 | 目录扫描等于整仓理解 |
| [现有知识树](../README.md) | D01–D12可按领域定位与原位补正 | 资料被本地Agent正确检索或具有实盘效果 |
| [\`local-knowledge-loader.mjs\`](../../server/intelligence/local-knowledge-loader.mjs) | 11个本地可选专业源的受限词面路由 | 动态全领域检索、模型使用正确率已提高 |
| PR #23经济证据、网络、快照和纸面回放 | 可读离线源/测试候选，具体提交需看当前SHA CI | 真实主网、控制权、PnL、生产服务已经验收 |
| [旧PR与当前blix分支](https://github.com/sunshihao001/grok/pull/23) | 可追溯的开发历史和选定集成候选 | 代码已合并；目前PR仍Draft且存在合并冲突 |

**完整性有多个分母**：仓库文件树覆盖率、原文阅读覆盖率、逐主张核对率、冲突与反例覆盖率、产品代码落点覆盖率、运行验收覆盖率、真实市场适用覆盖率。不能给一个“知识已吸收xx%”伪精确数字。

## 七、把不同旧台账的状态统一看懂，不暴力改名

\`MIGRATION.json\`、\`source-coverage-v0.1.json\`、\`build-register.md\`、\`DOMAIN-MODEL.v1.json\` 属于**不同事实轴**，不应简单合并为一个总状态：

| 状态轴 | 可见的原有表达 | 正确问题 |
|---|---|---|
| **来源覆盖轴** | \`TREE_INVENTORIED\` / \`CONTENT_READ\` / \`DEEP_CONCEPT_STUDIED\` / \`NOT_REVIEWED\` | 我看到原本哪些资料、深入到了哪？ |
| **承接轴** | \`SOURCE_COPIED\` / \`ORIGINAL_REFERENCED_NOT_COPIED\` / \`SOURCE_LINKED\` / \`METHOD_ADAPTED\` | 原研究被保存、链接、改写或否决了什么？ |
| **主张轴** | \`AUTHOR_REPORT\` / \`SOURCE_READ\` / \`SUPPLIER_RETURN\` / \`INFERENCE\` / \`HYPOTHESIS\` / \`UNKNOWN\` | 这项具体认识由什么支持、能推多远？ |
| **代码/运行轴** | \`CODE_INSPECTED\` / \`OFFLINE_TEST\` / \`LIVE_READ_ONLY\` / \`PRODUCTION_VERIFIED\` | 这段程序和实际服务被验证到哪一级？ |
| **AI使用轴** | 词面路由测试、\`RESEARCH_NOT_RUNTIME_VALIDATED\`、\`MODEL_AB_NOT_TESTED\` | 模型能否找对并用对，较原来是否更好？ |
| **权限/目标轴** | \`USER_CONFIRMED\` / 仅AI建议 / 只读 / 未授权交易 | 这项研究或执行是否有合法和用户授权？ |

**一次证据更新只改变相应状态轴。** 新CI过绿不意味着作者主张的经济控制关系已被证实；撤回某篇论文数字也不意味着已经复制的源码凭空消失。新协议冲突时，标明影响的旧主张、引用它的知识正文和运行规则，分别调整。

## 八、知识不断增长时最容易误入的七个死角

1. **按已有Blix缺口筛资料**：会漏外部项目本身有价值但暂时无功能落点的理论、方法、失败历史。独立理解原项目，再作产品取舍。
2. **只看README/论文摘要，不读源码与测试**：作者意图、实际行为、测试范围及运行覆盖可能不同；Issue、PR、评论也可提供重要反证。
3. **将文档分类当知识理解**：有Dxx、Lx、专家编号、152映射不说明理解主张条件或竞争解释。
4. **过度克制变成不敢形成任何新认识**：理论与跨来源机制互相支持，可以得出“有条件成立/值得调查”的正面结论；只是不能冒充主网事实或确定收益。
5. **把理论知识全都逼成代码**：有些概念能改变研究问题、风险识别或未来决策，即便当前没有算法也应被保存。
6. **只看局部结果，忽略变化影响**：旧\`same_funder=control\`失效时，后续聚类图、风险评分、策略、AI解释是否仍依赖它？应向下游查。
7. **为了完整而无限搜**：本轮资料不会影响当前争论、未知的判断、方法/验收或长期研究方向时可暂停；登记未审和重新开启条件，避免研究长期在原地打转。

## 九、下一次真正可检验的三个深度任务

这些是优先证据差距，不强制每轮全部执行。

| 实验 | 具体输入与对照 | 能证明什么 | 尚不可声称 |
|---|---|---|---|
| **一项主张的端到端追踪** | 从“同源是否同控”反查Hermes原文→Blix资金边源码/签名→实际报告→更正/回归 | 识别错误继承链、缺失环节和可修位置 | 共同控制准确率 |
| **一次真实 Mint 专业调查** | 同一Mint RPC、Token账户、指令/时间与当前 BubbleMap / 新经济图对照，记录服务池误归因 | 数据采集与业务图之间的事实质量差异 | 全市场历史完整与盈利优势 |
| **知识调用A/B** | 相同10–30个盲审自然问题：无知识/旧路由/现行路由，固定模型与工具预算，连失败样本 | 检索正确、引用准确、实际专业误报及额外费用 | 一次小样本证实所有长期知识有效 |

**停点与授权**：这一轮的主要交付是现有知识全链概念和真实来源/代码对应，不触发产品合并、真实付费模型、自动交易或上线。记录中的“尚未实测”不是未来禁止研究的理由；必须说明究竟还差哪条有价值的证据。
