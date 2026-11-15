# Blix 参考项目与未整体搬迁资产入口

## 2026-11-14｜外部参考统一归属：保留原始范围，不把作者简介直接搬成运行规则

当前Blix的[全域主述归位表](../README.md#2026-11-14全域专业归位总入口十二领域主述参考来源知识身份与产品验收)将每个专业问题交给D01–D12已有主文件；**本目录继续保存参考项目的原始证据、完整分类、来源差异、作者历史、源码反例、未读范围与跨源矛盾**。例如：

- Synapse全分类（14链上/3DEX事件/3买入形态/4HL主信号/5标签/5方法原则/4噪音及产品合规）在[原始转述清单](synapse-methodology-full-taxonomy-20261114.md)完整保留，跨信号机制在[第二轮](synapse-cross-signal-mechanisms-20261114.md)；分别引用D01/D04/D05/D06/D07/D09/D11，而不是复制整套表到每个领域或认定已接入。
- GMGN/OKX/Pulse/Million/HoldTech/PumpTrace/Cielo/Nansen/Arkham/Bubblemaps等成熟产品的目标、公开文档与部分源码，统一从[外部成品目标与业务比较](../../docs/project/reference-driven-goal-model-v0.1.md)及[覆盖状态清单](source-coverage-v0.1.json)恢复；对应经济知识回D主述，完整作者目标/市场条件保留此处引用。GMGN钱包历史PnL不等于Copyability，也不等于Blix已经买通付费API。
- Hermes/qb-/meme-/Why-Solana的特定源码、样本、旧规则失效与可迁移机制见[P1/P2对照](p1-p2-knowledge-reconciliation-20261113.md)、[独立来源纵深](source-knowledge-deep-study-v0.1.md)；旧主仓原文和未审目录不得丢失。研究点有价值但尚不能落在Blix代码时，继续作为知识或反证，而不是删除/硬改。
- 对每项来源继续区分`TREE_INVENTORIED`、`CONTENT_READ`、`DEEP_CONCEPT_STUDIED`、`OFFLINE_TESTED`、`CONNECTED_READONLY_RUNTIME`。完整源码树或多个相互引用的报告不是多份独立经济实证；用户转述、论文撤回、商业闭源不能因归位而“洗成”已核链上事实。

**扩展落地与运行状态**只在[产品扩展层](../../docs/project/intelligence-layer.md)及[工程台账](../../docs/project/build-register.md)，本来源目录不负责批准交易权限、替代数据提供方或报告成品验收。

## 2026-11-14｜GMGN与成熟参考项目机会优先的全局再梳理

[现有参考目标体系第13节（V0.4）](../../docs/project/reference-driven-goal-model-v0.1.md#13-2026-11-14gmgn--既有成熟产品--blix机会优先全局再整合v04)将GMGN官方 Wallet Radar、First70、Insider/Sniper、钱包Score/Style、跟单参数，与OKX/Million/Pulse/PumpTrace/HoldTech/Synapse及Nansen/Arkham/Bubblemaps/Cielo、旧Hermes/qb-/meme-等统一比较。**原项目知识覆盖不受当前代码适配限制；产品实施仍按真实缺口/增量价值选取**。最重要的新联系：多Mint共同持仓/交易不等于同控；钱包赚钱不等于用户可复制；卖出与转仓应由指令级证据核验。旧65项来源目录及之前全部Synapse分级原位保留，未重做另一套标签库或硬编码AI工作流。


## 2026-11-14｜Synapse 全分类纵深第二轮：机制与 Blix 源码断点

[Synapse 全分类跨信号机制研究与可证伪反例](synapse-cross-signal-mechanisms-20261114.md)继承前轮全部源分类，以 **M1–M6 六组经济机制**做多对多关联（不是新强制软件层），并对照 Million 源码、公开链上样本/论文、实盘失败复盘与 Solana 官方语义。最重要的 **Blix SOURCE_READ 纠偏**：原版 walletSignals→Mint→vet 已存在；实质待核处是 research AI 的原始钱包计数与 walletSignals 启发式独立组数不一致，以及 wtrack 对同笔 Swap+Transfer 跳过转账解析的漏项条件。三项合成反例已执行算术/去重断言，**不是主网实测或策略盈利证明**。优先修现有链路的证据语义和端到端验收，不重复建设市场/钱包筛选器。


## 2026-11-14｜Synapse 方法笔记完整信号与延伸分类

[Synapse Methodology 全分类提取与延伸研究目录](synapse-methodology-full-taxonomy-20261114.md)已经完整登记**用户 2026-11-10 转述笔记**的 14 类链上信号、DEX 3 类事件与 3 种买入形态、HyperLiquid 4 组信号与 5 个行为标签、5 项原则、4 组噪音、完整可视化和产品/合规要点。并额外建立 T01–T14 跨领域延伸研究导航，**原始分类与我们的延伸分类分开**，不再只截取直接适用于新发行 Solana Meme 的部分。跨市场内容保留研究资格；是否引入 Blix 运行时另按原有模块、数据可得性、权限、成本和实验效果判定。**仅完成知识与来源登记，尚未完成原站逐条核实或 Blix 运行实测。**


## 2026-11-13｜知识生命周期与来源追溯（唯一总入口）

[完整知识链：发现、获取、原意重建、承接、使用、反证和修订](knowledge-lineage-lifecycle-20261113.md)；[细分概念与静态追溯审查附录](knowledge-lineage-lifecycle-audit-20261113.md)。旧资料与代码的事实身份分别见下方既有台账。支持 `npm run audit:knowledge-trace -- --unit D05-K01`；只有源码/来源映射，不证明原始主张或模型任务已验证。

## 2026-11-13｜P1–P2原始来源对照、错误裁决与实际落地

[当前完整来源—D01–D12—原位知识修正对照账](p1-p2-knowledge-reconciliation-20261113.md)：汇总 Hermes wallet role/structure/证据、qb-95钱包真实留存、meme-结构策略、ai-d方法、Why-Solana多跳/Dust、Token Finder图谱与校准、Solana Holder Analyzer、Trading Portfolio、Google Skill Reach及Solana官方RPC/Token-2022；逐项列出**来源、错误假设、实际Blix实现、未验约束**，不只做参考项目功能目录。

仍未审阅的原参考项目完整范围以 [旧源覆盖状态](source-coverage-v0.1.json) 为准，不因有新总表而自动提升。对于商业闭源项目的公开描述仅保留业务问题，不宣称已读其生产算法。


## 2026-11-07｜整条市场过程的跨项目研究：从观察偏差到资金机制

[源码深研第12节](source-knowledge-deep-study-v0.1.md#12-2026-11-07-全过程研究的新增源码证据时间错桶发现抽样历史窗口与判断演化)以**同一个完整市场经济过程**连接Blix、Pulse、Million、HoldTech、PumpTrace、pumpwatch及ai-d，而非再拆几个小问题：新核查Pulse滚动热度把乱序旧事件归到最新5分钟桶的代码条件、Million头部70%＋尾部随机30%预览对探索/可重复性的权衡，结合Blix Journal去重/24h历史、Owner合并、资金边，恢复从市场发生、被观察、筛选、保存、经济解释、判断修订到回顾的整体证据链。核心产品决策是优先**真实Mint事件与当时可得时间对账**及**同批发行观察漏选对账**；保持有方向的只读线索，不把身份归因或可交易优势混为一谈。**源码条件已读，实际偏差频率、端到端运行和预测增益未验。**

## 2026-11-06 新增跨学科认知纵深

[Hermes逆向发现 × qb事实证据 × meme反证](../methods/hermes-reverse-discovery-deep-study-20261106.md)：以原始推理过程而非短标签理解项目；引入过程挖掘多对象事件、取证溯源、因果竞争解释与产品验证视角，生成跨钱包/跨Mint经济过程这一待证伪研究对象。**尚未实现或测试新功能**；[原目录覆盖状态](source-coverage-v0.1.json)继续保留未审范围。


本目录存放的是**对成熟项目的知识研究与复用经验**，不是这些第三方项目的完整代码仓库；用户后续只运行/使用Blix。原版保留在各自仓库，是否移植业务实现需要以后单独审查许可、依赖、安全、费用和功能重叠。**不要将第三方README的功能说明当Blix已具备或独立验收。**


## 2026-11-07｜HoldTech新源码试验：从功能名发现被误测的经济对象

[完整研究与七组确定性复算](source-knowledge-deep-study-v0.1.md#10-2026-11-07用此前未分析的-holdtech-源码检验ai-发现隐藏变量)核查HoldTech的Holder质量、跨Mint重叠、同Slot Bundle、钱包年龄与资金来源：发现持有时长被钱包年龄替代、Bundle可能由普通Transfer与Fee Payer触发、最近20签名被误称最早资金历史、跨Mint集合分母/分页与Owner余额合计失真，及“最大Token Account必是池”的未经证明假设。对照Blix原生Owner合并与Bubble Map风险。**仅源码分析及纯逻辑离线复算，非真实链上事实、非独立模型A/B。** 这体现ai-d“从普通问题追问真实测量对象和隐含条件”，不必新建标签或专家制度。

## 2026-11-07 外部成熟研究法与跨项目实证断层新发现

已将 [Aider源码上下文、ADR设计动机、Contextual Retrieval、GraphRAG、Agent Retrieval Bench、Agent Skills与RAG评测的三轮对照](source-knowledge-deep-study-v0.1.md#9-2026-11-07外部成熟方法三轮检索后的融合修正与pulse源码试验) 原位写入既有深研正文，并用Pulse`solana-stream.ts`、`merge.ts`、`restore.ts`对照Blix`journal.js`、`coverage.js`完成**选择性事件保存/回填的规则复算**。新专业问题：数据采集与样本保留的方式本身可能制造市场机制的伪相关；研究“早期资金/跨币异常”不能只查看已保存记录而不检查其保存条件。**没有启动软件、跑当前RPC或实测模型提升。**

研究边界仍开放：不根据目录/标签/当前Blix模块判定外部知识有无价值；每一轮可以沿事实、数据生成过程、资金、库存、行为、市场机制和反证不断发现此前未知的重要关系。六类知识目录仅用来存放和导航。

## 2026-11-06 研究入口纠正｜先独立理解项目，再决定如何融合 Blix

**本节修正此前“按 Blix 已知功能缺口筛选参考知识”的单向局限，而不取消成熟产品优先、事实核验和只读安全要求。** 参考仓库不是待拆的组件仓库，也不只是旧 D01–D12 分类的填空材料。它可能含有 Blix 尚未提出的问题、新的经济解释、异质的数据组织办法、工程失败经验、作者设计判断和与当前认知相矛盾的证据。

**研究与迁入分成两种不同工作**：
- **项目独立知识研究**：先恢复该项目原有的目标、用户业务、页面/API、源码流程、数据模型、依赖、时间窗口、测试/反例、设计权衡、历史演化及作者明确说明的理由；以实际模块/主张为单位渐进深读。发现原分类无法容纳的问题时，保留原名与跨域链接，不能因为目前 Blix 没对应模块就提前忽略。
- **跨项目认知合成**：对同一专业现象比较不同项目怎样定义、计算、验证和处理失败；寻找矛盾、独特假设及尚无答案的问题，结合可靠协议/理论/实例反证；区分代码可观察事实、作者主张、推定设计理由和独立验证。
- **Blix 产品吸收**：上述认识形成后，再分别决定保留为研究来源、补入原有 `foundations/mechanisms/methods/cases/ai/references`、修订旧主张、转反例测试、复用接口/程序、或提出改变产品方向的候选。**没有当前实现落点不等于没有研究价值；重复实现不等于重复知识。** 不自动引入交易/签名/支付或未经核验的第三方代码。

**覆盖要求不是“每个文件都新建一张卡”**：保留原项目完整目录清单，逐主题核查文档、实现、测试、历史与失败反馈；每条重要主张至少能回溯到代码路径/来源版本，说明它回答的问题、使用前提、竞争解释、限制、待补证据及知识关系。没有查过的标记未审阅，只有扫过目录的标记目录已发现；不把“全量扫描”说成“每个知识点已理解”。研究可循证据价值分批推进，保持业务交付并行，不要求先读完65个项目才能完善 Blix。

### 第一批跨项目源码试读：意外发现与延伸问题（仅 SOURCE_READ）

| 项目/原始代码 | 已观察到的独立知识点 | 值得继续验证的关系与未知 |
|---|---|---|
| [Million copyability.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/copyability/copyability.service.ts) | 以同池分钟K线对比鲸鱼实际进出时点及延后60秒进出，测算“可复制性”而不只计算历史钱包盈利；采样最近成交并限制成本。 | 真实净优势还受到传播延迟、滑点、容量、漏掉的样本和幸存者偏差影响；这套价格代理并非真实成交复现。对 Blix 的价值不限于钱包发现，还涉及信息时效与市场微结构。 |
| [Million decision-log.ts](https://github.com/Kelows/million/blob/main/apps/api/src/common/decision-log.ts) | 记录跳过/接受决策的阶段、代码和理由；异步写库失败被静默忽略，有保留期。 | “为什么没选中”与“是否完整记录所有判断”分开；日志缺口不能误当未发生。 |
| [Pulse merge.ts](https://github.com/nirholas/pulse/blob/main/src/collector/merge.ts)、[solana-stream.ts](https://github.com/nirholas/pulse/blob/main/src/collector/solana-stream.ts)、[restore.ts](https://github.com/nirholas/pulse/blob/main/src/archive/restore.ts) | 多源观察采用先到优先的补缺合并；部分乱序旧交易计入最新滚动桶；历史存档按可变状态upsert/事件去重恢复。 | 来源冲突如何可见、乱序时间是否产生虚假异动、快照与事件历史怎样分别保存及验收；不能只把Pulse当榜单服务。 |
| [PumpTrace backfill-manager.mjs](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)、[interpretation-engine](https://github.com/AntC215/Pumptrace/blob/main/src/modules/interpretation-engine/analyze.mjs) | 历史回补状态、游标与恢复边界细化；直接Creator Token转移可证明一条链上关系，不等于接收方身份。 | 数据覆盖改变何种主张可以成立；如何区分具体资金关系与“控制权”标签，评分阈值如何校准。 |
| [HoldTech holder-overlap](https://github.com/co-numina/holdtech/blob/main/app/api/holder-overlap/route.ts)、[deep-scan](https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts) | 以有限Owner样本构建跨币地址重合的几何均值评分并映射“协同”等级；深查中还研究同槽、资金与集中度。 | 重合地址的抽样偏差、公共服务/独立交易者与同控的竞争解释、误报率；不能将评分名称直接当经济主体真值。 |
| [PumpGrok ARCHITECTURE](https://github.com/swcstudiospace/PumpGrok/blob/main/ARCHITECTURE.md)、[SAFETY_INVARIANTS](https://github.com/swcstudiospace/PumpGrok/blob/main/docs/SAFETY_INVARIANTS.md) | 区分Agent指令包、工具注册、Paper回放、后台服务；项目列出不变量与测试归属，但部分文档为设计且候选发现命令标为未实现。 | 将“设计上要求/源码确有/测试存在/离线通过/真实运行”分开；研究可追溯的责任、回放与失败恢复，不只看其插件目录。 |

**本表是候选知识入口，不是五个仓库已完成逐文件深审、实际测试或项目融合。** 后续原点深读必须追踪这些知识点与其它模块/设计/变更的关系；必要时新增原本没有提出的专业研究问题，而不是仅把它们映射到 Blix 的已有页面。此前65项参考资产保持来源登记，不自动宣布其余项目审查完成。

## 已保留在Blix的全文历史研究
- [旧Grok 五项目专业知识审查](legacy-reference-project-knowledge-audit.md)：旧行业产品的真实研究问题与可复用逻辑。
- [旧Grok 多跳资金与供应商证据审计](multihop-funding-evidence-audit.md)：多跳识别、公共设施和反证。
- [旧Grok 成熟参考能力复用完整台账](legacy-reference-capability-ledger.md)：较长原始审计；先按具体项目名称或业务问题定向检索，不全文注入模型。

## 外部参考项目（当前保留原文和成熟思路，不整包复制）

| 参考 | 原始项目 | 首要知识用途 |
|---|---|---|
| Million | https://github.com/Kelows/million | Mint↔钱包发现、资金/交易候选、历史窗口与排除理由 |
| PumpTrace | https://github.com/AntC215/Pumptrace | Creator归因、证据分层、历史回补、调查报告 |
| Pulse | https://github.com/nirholas/pulse | 发行生命周期、历史档案、MCP/数据来源 |
| HoldTech | https://github.com/co-numina/holdtech | Holder集中度、钱包质量、快照演化 |
| PumpGrok | https://github.com/swcstudiospace/PumpGrok | AI任务说明、Skill组织、执行收据、安全隔离 |
| OKX OnchainOS | https://github.com/okx/onchainos-skills | 已包装链上只读调查及数据工作流 |
| pumpwatch | https://github.com/cinder-security/pumpwatch | 可复现发行样本及经济行为反证 |
| Why-Solana | https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over | 多跳方法、相关主体与共享服务区分 |
| 旧 Hermes | https://github.com/sunshihao001/- | 钱包角色、资金、筹码、指标推理与历史设计 |
| 旧 qb- | https://github.com/sunshihao001/qb- | 单Mint关键地址矩阵和复查组织 |
| 旧 meme- | https://github.com/sunshihao001/meme- | 经济机制、失败市场形态、策略候选 |
| ai-d | https://github.com/sunshihao001/ai-d | AI问题表征、知识适用、认知提取、目标演变 |

**完整65项参考登记**：仍以旧Grok [gpt-meme-project-index.v1.json](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json) 为来源，而不是仅依赖本页的示例短名单。

## 尚未全文迁入但不会丢失的老资产

- 旧Grok [system目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/system)：旧执行制度、长期进度、项目收束、专家手册、来源登记、原始152单元本体；**不把过去固定执行制度复制成Blix强制指令**。主册和机制研究方法已迁入。
- 旧Grok [legacy-snapshots目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/legacy-snapshots)：更早知识文件及理论副本，适合需求出现时专项核对，不是全部现行有效。
- 旧Grok [transfer目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/transfer)：历史教学与迁移实验；当Blix需要教学/工作交接时再评估。
- 旧Grok [experiments目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/experiments)：执行边界的历史实验资产。
- 历史工程 [PR #16](https://github.com/sunshihao001/grok/pull/16) 与 [PR #17](https://github.com/sunshihao001/grok/pull/17)：代码/离线实验和迁移实践应单独审查，不当作文档迁移就已完成产品能力。

此页为来源索引，不代表每个链接已实时验证、每个参考项目知识已审查完毕或旧知识全部完成迁移。可用[迁移清单](../MIGRATION.json)判断具体状态。

## 完整研究不以Blix当前缺口为准入条件（2026-11-06）

[参考项目全域认知纵深第一轮](source-knowledge-deep-study-v0.1.md)与[来源覆盖账本](source-coverage-v0.1.json)独立记录各原项目的全部知识区域、已深读概念和尚未深入的资料。**完整学习与代码集成是两条不同判断轴**：未知新机制、反例、失败经验即使暂时无法映射到Blix，也不能被直接排除；只在落实代码时才优先考虑现有功能复用和最小改动。文档“树已盘点”不等于“知识已读透”。
