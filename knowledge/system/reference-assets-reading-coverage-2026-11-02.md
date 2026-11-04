# Solana Meme 原参考资产逐项审读覆盖账｜2026-11-02

> **任务承诺的边界**：用户要求每一个知识点都深入理解，不跳过重要旧资料。本账用于避免“搜到=学过、列到目录=审过、总结=复现”的误报。它不是另一套领域分类，不自动改变原65项参考登记、152项知识单元或证据准入规则。**仅标本轮实际阅读覆盖**；仓库内重复备份与机器原始数据必须区分，未核实者不能写“完成”。新阅读时应原位更新此账和对应Dxx专题，不要每轮另建一套表。

## 覆盖统计和结构

本轮通过GitHub Git Tree取到5个仓库的文件目录，不等于全文读完：
- Hermes：264个文件路径，231种不同blob SHA；
- qb-：4,236个文件路径，3,276种不同blob SHA；其中 `data/` 3,338项，`hermes_harness/` 610项，另有旧备份；
- meme-：474个文件路径，414种不同blob SHA；
- Why-Solana个人fork：944个文件路径，925种不同blob SHA；其中 `data/` 503项；
- grok知识PR分支：180个文件路径，180种不同blob SHA。

上述去重只是按完全相同内容的Git blob进行，不代表其余每个blob都是不同的“专业知识点”。每项需进一步分为：原始理论/报告、程序实现、测试与反例、历史更正、原始事件数据、衍生结果、模板/副本。**大量文件没有逐一打开，因此本轮绝不宣称“全量理解完成”。**

## 原65项逐项覆盖

| ID | 参考资产 | 原登记验证层级 | 本轮阅读状态 | 具体覆盖/未覆盖说明 |
|---|---|---|---|---|
| REF-001 | grok (当前正式项目) | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮读取知识PR、项目索引与运行指导（部分文件） |
| REF-002 | 原 Solana Meme / GMGN 交易研究与 Hermes Workflow OS（跨域历史知识源） | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮精读learning/05–16、00c–00e要点、筹码控制设计与部分程序；远未覆盖全部264文件; 续读Skill04设计与实际执行谓词，确认similar_sell_ratio与设计差异、confidence_score非校准、池排除测试范围 |
| REF-003 | qb- GMGN单Mint程序 | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮重读sikk_gmgn_token_report.py并核对主目录；4,236文件中大量为数据/备份，尚未逐项去重归并; 续核qb-对rat_trader、native_transfer资金来源及Token转入的实际分类谓词，待真实数据对照 |
| REF-004 | meme- 理论研究库 | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮审读SOURCE_OF_TRUTH、FCZ/深洗/死亡盘、策略状态机、反证/基准/消融；其余未深审 |
| REF-005 | Why-Solana-Memecoins-Are-Over (个人fork) | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 已连续审读coordination_detection、economic_mechanics、exit_destination、funder_network、known_group_reentry五专题各自的README/analysis_plan/results，按函数核查其主要分析/追踪/特征代码，及CD/EM/ED/FN/KG部分冻结和完整性文件；发现409→408分析层去重、G4语义边界、预注册matched检查修复；尚未逐行穷尽、全量复算或读取全部原始数据 |
| REF-006 | Why-Solana-Memecoins-Are-Over (上游) | REPO_VERIFIED | 局部审读 / 有明确证据范围 | 本轮核查上游FN_INTEGRITY、FN_FREEZE与README；上游全部实验未核 |
| REF-007 | Kelows/million | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮核读owners/funding/live相关源码，非安装运行; 续核owners.service.ts的182-wallet共入场事故、Hub阈值与Union-Find低度数服务节点误并边界 |
| REF-008 | co-numina/holdtech | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮核读deep-scan与holder-overlap源码；检测到公开明文API Key风险，未执行 |
| REF-009 | cinder-security/pumpwatch | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮核读pump_watch与creator_reputation源码，未执行 |
| REF-010 | OKX OnchainOS Skills+CLI | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮核验OKX Holder、Cluster List/Overview/Top Holders官方数据契约；未授权请求; 续核Token Cluster Top300/100限制与Wallet History六个月、单链每页20及示例契约不一致；未授权实测 |
| REF-011 | GMGNAI/gmgn-skills | SOURCE_AUDITED | 局部审读 / 有明确证据范围 | 本轮核读GMGN token/holder-analysis/portfolio/track官方Skills与字段；未授权请求; 续核gmgn-token的Token Traders历史非Holder范围、单次100条和first native transfer标签限度；未授权实测 |
| REF-012 | Solana Microscope | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-013 | FnZero Solana Parser SDK Python | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-014 | FnZero Solana Parser SDK Rust | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-015 | Carbon Indexing Framework | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-016 | solana-dex-parser-go | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-017 | solana-dex-parser TypeScript | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-018 | MadeOnSol SDK | SOURCE_AUDITED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-019 | Helius core-ai | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-020 | Yellowstone gRPC | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-021 | Raydium CP Swap | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-022 | Pump public docs | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-023 | Jito Solana Client | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-024 | Metaplex Token Metadata | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-025 | Solana Sniper Reverse Engineering | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-026 | MELT Dataset / Code | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-027 | Grokbot Playbooks | REPO_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-028 | Helius Enhanced/DAS/Parsed Events | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-029 | QuantBloc methodology / Base / MCP | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-030 | Triton / Fumarole / Old Faithful | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-031 | Bitquery Solana API/Token Holder | PAGE_VERIFIED | 局部审读 / 有明确证据范围 | 本轮比对Bitquery Coinpath历史研究结论，未在本轮执行完整接口重放 |
| REF-032 | DEX Screener | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-033 | Solana Official Docs | PAGE_VERIFIED | 局部审读 / 有明确证据范围 | 本轮按经济事件与账户权限对照既有Solana协议认识；未遍读官方全站 |
| REF-034 | Jito Docs | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-036 | Meme Coin Factories (ACM CCS 2026) | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-037 | A Midsummer Meme's Dream (USENIX 2026) | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-038 | RED-COHORT 2026 dataset | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-039 | Froggy V2 Scanner | PAGE_VERIFIED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-040 | Sputnik Parser / @sputniksol | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-041 | GMGN Terminal / CLI | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-042 | OnchainRadar | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-043 | Genesis Arbitrage | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-044 | ArbitrageScanner | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-045 | Synapse | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-046 | Axiom | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-047 | Photon | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-048 | TradeWiz | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-049 | Ray Bot | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-050 | Stratos | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-051 | Crypto GYM | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-052 | Eclipse Trencher | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-053 | taxiflip Axiom Dev Tracking教程 | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-054 | Arkham | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-055 | Nansen | HISTORICAL_NAMED_ONLY | 局部审读 / 有明确证据范围 | 结合此前Nansen钱包关系API资料，本轮未对该平台完整重新核验 |
| REF-056 | Ethtective | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-057 | Resonance | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-058 | BlockSec Phalcon | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-059 | CoinGlass | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-060 | solana-foundation/transaction-v1-examples | LINK_UNRESOLVED | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-061 | Meteora AMM | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-062 | PumpSwap | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-063 | Jupiter Aggregator | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-064 | Clanker | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-065 | Zora | HISTORICAL_NAMED_ONLY | 待本轮逐文件审读 | 仅继承索引记录，不代表本轮已阅读该资产的专业知识 |
| REF-066 | RugCheck | PAGE_VERIFIED | 局部审读 / 有明确证据范围 | 引用先前真实V0.1 RugCheck运行证据，本轮没有重新联网请求 |

## 未计入原65项但本轮需要保留的新增来源候选

- **Bubblemaps Data API v0.3.2**：本轮已读取官方 `openapi.json` 的map、holder、subgraph及数据结构，记录Magic Nodes/Time Nodes、聚合转账边和时间戳参数；尚未真实授权API调用。建议后续核验后正式决定是否进入原参考索引。
- **Bitquery Coinpath历史多跳示例**：已有官方资料入口，候选作为补充任意钱包多跳调查；本轮未执行请求、未核计费和真实Solana历史覆盖。
- **GMGN官方2026 Agent API新信息**：应在现有REF-011之下按接口现状更新旧“不能开放API”的历史说法，但不能把过往白名单说明和新Agent API说成同一服务。

## 具体知识点恢复顺序：以原业务因果链而非每项字母顺序

1. **钱包与经济角色的基础**：Hermes learning/10–12、qb关键地址矩阵、Solana owner/authority/fee payer账户语义；回答“地址是什么、行为是什么、经济主体未知在哪里”。
2. **资金、退出与多跳**：Why-Solana `exit_destination/`→`funder_network/`→`coordination_detection/`，与Million funding/owners、OKX/GMGN/Bubblemaps数据字段对照；回答“关系怎么来、何时丢失、为什么会被错误合并”。
3. **库存与资本回流**：Hermes Skill4、GMGN transfer_out/PnL、Why economic_mechanics/known_group_reentry、meme FCZ假设；回答“仓位何时真实转移、何时只是执行设施”。
4. **反证、长期有效性和业务决定**：Hermes 00c–00e/13–16、meme负对照/消融、Why历史冻结/空模型/未发现盈利结论；回答“怎样分清新的结构认识、有效监控与尚未证实的交易优势”。
5. **未在本轮读过的旧专业来源和65项剩余项目**：逐步逐项审读，不允许因当前主题集中多跳而假定其全部不相关；按研究问题重新调用，并保留遗漏审计状态。

## 2026-11-02 本轮续读补录

- 五专题已完成**问题—方案—主要代码—结果—竞争解释**的一轮系统性连读，但并非所有子函数/测试/原始缓存均已验收。保存入口：[legacy-meme-multihop-deep-audit-2026-11-02.md](legacy-meme-multihop-deep-audit-2026-11-02.md)中“五补”。
- 明确新发现：`known_group_reentry/code/kg_10_features.py` 的G4是当前Sniper**在历史中曾发生Token向外转移**，而非“同一Token接收钱包重复出现”的完整身份关系；`kg_30_analysis.py`包含将匹配基线条件加入最终判定的自我修正。
- 已核查CD/EM/ED/FN/KG冻结文件关键计数，但**未重新运行原仓库全部测试、未自行重放SOL交易历史**。不同来源的作者统计、平台标签和当前Meme V0.1运行成果仍严格隔离。
- 下一次阅读应沿具体代码缺口追查：`fn_30_analysis`的去重是否覆盖所有汇总、`exit_destination`高活跃节点历史删失、`economic_mechanics`时间可见性如何影响cluster、`known_group_reentry`模拟成本和数据可得时间，然后再扩展到旧qb的真实报告与标签，避免将尚未审过的其他资产标成“完成”。


- **2026-11-02 共享服务专项续读**：Hermes Skill04设计/源码/排除测试、qb- GMGN报表的实际分类分支、Million Owner聚类/资金边源码，Why-Solana `FN_posthoc.json`的408首跳目标地址签名分组，GMGN Token/Holder官方Skill、OKX Cluster/Wallet History官方契约及Bubblemaps OpenAPI已按本轮具体问题核验。独立JS合成两例检验算法推论，不是原仓实际数据重放。结果归位[L3深度研究§23](../domain/L3-actor-economic-mechanisms-deepstudy.md)与[本专项审计“五再补”](legacy-meme-multihop-deep-audit-2026-11-02.md)。仍未完成65项全量逐文件理解、旧代码运行验收和服务商客户群真实比例估计。

## 验收状态

- 本轮已产生 **[多跳与旧知识专业审计](legacy-meme-multihop-deep-audit-2026-11-02.md)**：包含真实代码、字段、非Holder关联、Hub反例、数字不一致、来源及经济边界。
- **尚未完成**：逐文件全量研究、全部65项资产的源码测试及版本比较、旧仓库全数据独立复现、Grok多跳运行及三平台同Mint授权数据对照。没有后台运行状态，也不存在已预约的后续交付。
- 读完一个知识点的必要条件：能准确复述原作者的专业问题；定位到源码/研究证据；说明观察与推断差别；指出具体失败与竞争解释；列出使用旧成果的条件；若发现旧结论错误，在原位置留下修订与来源。不以字数和新增架构为完成标准。


## 2026-11-04｜全量参考资产与同题主体比较的增量记录

**状态**：2026-11-04 /COMPARE 新增审查范围；不更改上方历史事实或原 REF 编号。用户要求选一个代码质量、产品架构、运维和扩展能力好的完整主体，再按缺口从其他成熟参考项目吸收能力。

- [全量对照报告](reference-full-compare-2026-11-04.md)：以同一 S1 市场发现、S2 单Mint取证、S3 跨Mint双钱包/同签名、S4 数据断流恢复、S5 工程功能扩展的任务比较 **18条整套产品/专项服务/基础设施路线**，覆盖数据/方法/源码/成本/可靠性/安全/实跑状态。
- [机器可读扩展索引](reference-expansion-compare-2026-11-04.json)：继承原登记 **65** 项（缺号 REF-035 不新增），按原 `historical_verification` 保留历史核查级别，另外新增 `NEW-01..17` **17** 项候选（原13+补录4），并含比较矩阵与验收合同。
- **重要恢复**：原 REF-012 **Solana Microscope** 不只是一个小工具：其 Carbon/IDL/Prometheus/Loki/Grafana、回填与检查点恢复，是可靠数据监控与运行工程的专业参考；但它单程序监控，不能直接替代全市场产品 UI。
- **重要补漏**：PumpGrok、BLIX、Pulse、dexterm、PumpTrace、Cielo、Bubblemaps、Kol Quest、Solbeam、MemeTrace、Meme Intelligence 等保持独立候选；BLIX开源 vs Hosted、Bubblemaps品牌 vs 第三方Bubbles、Axiom Pulse UI vs `nirholas/pulse` 不混同。
- **不可夸大**：本轮做了知识账/源码与公开资料核查，未安装/运行上述任何一套第三方完整成品、未执行真实主网统一验收。以后更新该索引时，明确归属为目录、源代码、单测、联网读取或完整用户产品验收，不把这些混成一种“完成”。

**原位修订原则**：原65项权威编号继续由 `gpt-meme-project-index.v1.json` 保管。本增补不是第二套本体，不覆盖 D01–D12，也不自动改变专家与运行框架。具体专业结论形成后回填原 Dxx 专题和对应产品工程文件。
