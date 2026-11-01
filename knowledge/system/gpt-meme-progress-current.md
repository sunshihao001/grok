# GPT「跟单」｜唯一活跃研究恢复点（2026-10-31，P3-M01）

> **2026-11-01｜继续研究：真实经济归因与资金路径的源码级反证（当期最新，仍不编程）**：已审读Million固定源码的交易报价/Token净额/费用赞助者归因/资金网络/轮转账本，并与HoldTech、OKX、pumpwatch及旧Hermes/qb-比较。**新增真实源码事实**：Million的orchestratedDeltas在Fee Payer自身无Token变化时把第一个SOL交易关联执行者的Token delta归给Fee Payer；Discovery的buyersOf与metrics.txDeltas使用不同的SOL/WSOL计数口径；Owner Graph将SOL双向资金边规范成长期无向边且所审重建路径未清理失效证据；Token轮转在多Mint收款时对原成本均分。其潜在“谁买/花多少/谁关联/赚多少”错误是专业机制推断，未有本项目独立真实主网误报统计。来源、竞争解释、反例和适用边界已AMEND到[现有E-L3-02资金经济专题](../domain/L3-E-L3-02-capital-organization-incentives.md)。下一研究应从一笔原始交易的签名/指令/CPI/费/各Token Account前后余额恢复客观事实，并特别研究何种链下受益关系原则上不可识别；不新增专家/监控规则，不进入代码、部署或付费查询。

> **2026-11-01｜当前用户指定研究主线（不编程）**：先吃透同行成品，不把产品交付计划当本轮自动行动。按自适应持续推进/V2知识研究方式，已从固定源码 `Kelows/million@c89ad07c` 沿 `crawler→discovery→wallets→live→flows→MCP` 审查观察分母，发现除既有 `LiveEvent.signature UNIQUE` 外，**资金流UI支持30/60/120分钟、但LiveEvent只保留15分钟且每5分钟清理；eventsToday复用短存活表；deepSample按时间bucket抽样仍可能truncated=false；名册订阅/高流量退订使样本按活跃程度有选择地缺失**。对照HoldTech有限holder分页、OKX工作流覆盖和pumpwatch分阶段观测；来源、反证、竞争解释已回填现有 [异常发现方法专题](../domain/meme-anomaly-discovery-state.v1.md) 的“Million全业务链深入源码对照”节。证据等级=源码审读+跨源理论解释，**没有运行Million全套、没有独立实盘漏报率、没有新增功能、没有Grok上线**。**当前研究下一步**：深入区别“交易签名、钱包视角经济事件、token/quote资产腿、时间窗口、订阅覆盖”的信息保存与损失，对照Million、OKX、HoldTech及官方协议；从真实API数据契约与已有测试寻找反例，再决定哪些同源关系/群体规则具备可信的监控语义。旧产品V0.2待实施，但不是这轮任务。用户只表达方向，AI负责专业问题构造、研究综合和最后可复制输入。

> **2026-11-01｜仅纠正思考与执行方式，原研究记录完整保留**：本文件恢复此前全部研究记录、论证、参考项目、知识联系与工程证据。过去的P阶段、下一轮模板、固定专家全覆盖等可作为方法或历史状态参考，**不再自动强制执行**；并不意味着废弃D01–D12、152研究问题、22专家知识、跨领域机制或开放探索。根据用户当前目标选择深研、机制发现、专业判断、产品整合或工程测试，研究本身可以是独立目标。当前实际工程进度以本文最新2026-11-01记录及PR#16实测为准，免费V0.1基础版已验，V0.2关系能力为当前有价值的产品缺口而非所有研究必须转向的任务。

> **最新收束（2026-11-01）**：先读[《全项目专家去污染与收束审计》](whole-project-convergence-audit-2026-11-01.md)，涵盖最新22专家、65参考、152项与历史104项的裁决、知识M01/P3-M01命名冲突及真实公开DEX池快照的严格边界。本文标题仍保留2026-10-31的历史创建日期；本文内各段有先后版本，**以最新实际PR #14/#16源码和2026-11-01验收证据为权威**。当前优先是安全获得完整只读Mint报告所需数据，而非重回过时P2.2研究任务；知识侧B01仍可并行深化。不得将GitHub CI或厂商池统计提升为真实钱包经济或收益验证。

> **2026-11-01 产品实施路线收束（最新）**：根据用户要求，停止继续扩展方案，**以[工程PR #16《四阶段成品交付计划》](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/product-delivery-plan-v01.md)为产品优先级真源**：V0.1真实Mint报告→V0.2钱包/资金→V0.3异常监控→V1.0 Grok入口。当前已完成真实公开池数据，但**完整钱包/Dev报告尚未真实验收**。GPT知识分支仍按既有D01–D12/152单元/22专家持续回填，只有对当期成品功能有实质帮助才深入；不要求先学完所有单元，也不重起规划。旧文件里“继续研究P2.2/先开发FnZero解析器/扩大架构”只能按历史研究口径读取，不应覆盖此产品交付顺序。用户只负责必要账户/授权，不选择技术栈。

> **2026-11-01｜V0.1实际运行升级与持续推进（最新状态）**：工程[PR #16](https://github.com/sunshihao001/grok/pull/16)已将现成免费[RugCheck Token Report](https://api.rugcheck.xyz/swagger/index.html)与DEX Screener真实公开池整合为一条`mint_v01.py --rugcheck`只读命令。真实[GitHub Actions #41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)读取同一Mint**5池、20条供应商Holder Token Account候选、Creator候选**，保存报告/原始响应和SHA，并发现**1条Holder候选owner与PumpSwap池地址重合**，结合供应商knownAccounts=AMM将其降为基础设施候选；其余19条只是未分类账户，不是19个人。官方公共RPC另一次实际尝试因HTTP 429限流，真实Owner解析未成功，已不作为默认路线。**V0.1基础真实只读多来源报告可验收，不等于完整Dev历史/资金同源图、独立链上钱包控制验证、Grok云电脑或盈利**。按[四阶段产品计划](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/product-delivery-plan-v01.md)，下一产品主任务**V0.2真实钱包与资金关系**：先复用RugCheck insider graph或Million funding/owners，核实一条来源明确的实际关系、误归因及数据更新；OKX增强仍待安全授权，无需阻塞免费基础能力。知识库REF-066 RugCheck来源状态已提升为PAGE_VERIFIED并挂真实运行证据；先前65参考登记等级统计是**当时快照**，不能视为修改后的实时分布。

**当前权威**：GitHub `sunshihao001/grok`，知识分支 `knowledge/whole-spectrum-20261030-v1`（Draft PR #14）中的本文件；工程分支 `research/p24-cross-mint-m01-batch-monitor-20261031`（Draft PR #16）。PR 均未合并，主分支没有这些草案增量。

**持续研究与写作方式**：继续使用 [《持续研究与知识同步 V2》](gpt-meme-continuity-v2.md) 与 [《专业研究写作 Skill V2》](gpt-meme-research-writing-skill.v2.md)，新结果先对照已有 [唯一监控方法专题](../domain/meme-anomaly-discovery-state.v1.md)，用 `AMEND` 修订，不把每个回答复制为新专题。

## 本轮新增：按需外部专业知识补全（V2 原位置修订）

已把此前有用的“AI先理解、行业真实语言/黑话恢复、跨学科知识发现、外部证据主动反证”融合到 [持续研究V2](gpt-meme-continuity-v2.md) 和 [研究写作Skill](gpt-meme-research-writing-skill.v2.md)。当当前知识不能解释现实事件、技术字段歧义或新反例可能改变设计时，主动选择官方文档、源码、论文、GitHub 实现、实际操作者反馈等来源，而不是强制搜索固定数量平台。所得术语须转为可观测数据和反例才入库。已将 Jito Bundle 与同 slot“bundled buyers”的区别修订进 [现有监控方法专题](../domain/meme-anomaly-discovery-state.v1.md)。此补充不改变既有 P3-M01 代码已完成的范围，也不提前宣布 P4。


## 本轮 V2 机制修订：检索与参考项目长期复用（2026-10-31）

**修订范畴：研究方法增强，不是 P3-M01 工程/真实链上能力升级。** V2 现加入：跨官方协议、开源源码/tests/issues、供应商字段、X/Reddit/Telegram实践与失败、必要论文/跨学科的递进检索；对每个重要研究方向比较项目适配、替代实现、数据可得性、正常解释与成本，输出 CONTINUE/PIVOT/PAUSE/REJECT；常驻参考池按实际业务问题反复重访 Hermes/qb-/meme-/Why-Solana/OKX 与外部新候选，记录继承/更正/不可采用与再次触发条件。**所有持续研究的最终输出必须落到下一步最有价值的执行任务，且最后一项是可复制提示词。**

新增可复用竞争实现入口：Solana 官方 transaction-introspection + transaction-v1-examples、0xfnzero/sol-parser-sdk、Raydium CP-Swap、Yellowstone、Helius/Bitquery能力文档、实际开发者索引断流讨论。它们是本轮检索/阅读的源候选，不等于这些库已在当前 Python 适配器安装运行或其市场效果已实测。P3-M01 继续维持 fixture-only、legacy/v0部分转账、v1 fail-closed 和未知事件不当作零交易的真实边界。

**主研究方向依然是**：对少量真实公开签名核验当前解码语义 → 比较官方/成熟解析器与自制适配器的可靠性/成本 → 选择一个协议的经济 BUY/SELL 解码；知识主线同时继续 qb/Hermes 关键钱包和库存/时点机制，不让通用协议课程挤占 Meme 业务目标。Grok S1 云电脑仍独立待验收。


## 当前研究/工程状态

- **P2.1—P2.5**：概念探索、跨钱包/跨Mint方法比较和优先级筛选已经完成一轮；C02（同群体执行方式变化）和 C05（机会校正的沉默/迁移）获准进入局部 P3；C01（跨币资金再部署）保留候选，暂不做完整图。
- **P3-M01**：原有 `wallet_batch_monitor.py` 已有 1/5/15 分钟窗口分析与14项离线测试。
- **本轮真实新增**：在 Draft [PR #16](https://github.com/sunshihao001/grok/pull/16) 增加 `src/solana_meme_os/raw_tx_adapter.py`、24项离线对抗性测试、合成 `getTransaction` 形状 fixture、[原始解析与 C02/C05 合同](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)、11个合成合同场景。**此前38项本地离线测试通过；此后新增v1失败封闭及7项官方示例回归，六个测试文件当前共71项测试方法，GitHub monitor-tests CI对最新工程提交成功**。适配器→M01 模拟数据串联运行成功。
- **现有能力边界**：原始交易适配器只接受 `mode=fixture`；支持顶层 System Program SOL Transfer，以及顶层 SPL Token/Token-2022 的 Transfer/TransferChecked；`jsonParsed` 与部分已核对格式的 `json`/v0 loadedAddresses；区分 Token Account owner/authority/fee payer；保留 signature、slot、`available_at`、指令路径。单笔 CPI Token/SOL 转移不被猜作 Swap/用户充值。未实现 Pump.fun/Raydium/Meteora/Jupiter 的 BUY/SELL 协议级解析。
- **未知状态**：错误/缺少 TokenAccount owner、Meta/CPI/lookup、Token-2022 扩展或晚到证据均 reject/mark unknown；当前未知使整个 fixture 的 `coverage.complete=false`，是保守粗粒度设计，不是已经完成按 Slot 的采集水位。Fixture 的 `complete=true` 也不是对真实链上全部交易的独立证明。
- **C02/C05**：已有最小字段合同、11个模拟对抗场景，但**未实现两套运行监控器**。M01 聚合 JSON 只有人数统计，C02 必须另外持有 `frozen_group_members` 及原始标准化经济事件流；C05 必须另外有独立合格机会索引和可验证的窗口覆盖。

### 官方资料发现的版本边界（2026-10-31）

新外部核查确认 [Solana Versioned Transactions](https://solana.com/docs/core/transactions/versioned-transactions) 官方文档称 v1 已激活，v1 不使用 ALT，而是以内联账户和 transactionConfig 表示新的交易配置。现有 PR #16 原始适配器仍仅支持 legacy/v0；**version=1 应输出 UNSUPPORTED_TX_VERSION 且使窗口覆盖不完整，不得误记为没有交易**。工程 PR #16 已加入针对 v1 的明确 fail-closed 合成测试，等待/核查 GitHub CI；未实现 v1 解码或真实交易验证。后续官方 introspection 已有支持v1的实现参考：https://solana.com/docs/core/transactions/transaction-introspection 。此修订不更改 P3 当前阶段判断。

### 本轮公开文档样本核查与两项重要修正（2026-10-31）

**已落地、可回读**：PR #16 的 `fixtures/official-solana-gettransaction-samples.json` 固定保存Solana官方 getTransaction 文档提供的**2笔Devnet签名、3份响应编码**，以及 `tests/test_official_gettransaction_examples.py` 的7项回归。Legacy原生SOL transfer（签名 `4ReKprwf…`）正确计为1 SOL独立资金事件、不产生买入；v0 ATA Create（`56rgv1Fq…`）的 json/jsonParsed 均无假BUY，但因尚未完整支持账户创建/CPI经济语义而报告未知。**没有独立 RPC 再抓取**；官方样本未提供历史可得时间，测试注入的 `available_at` 仅是fixture时点，不适合证明前兆实时性。来源固定到 [官方文档commit 4cb392f](https://github.com/solana-foundation/solana-com/blob/4cb392f61c2ab0f8953cc314378aaf8256b7699a/apps/docs/content/docs/en/rpc/http/gettransaction.mdx)。

**修正两个真实代码错误**：
1. `meta.err` 缺字段过去被当作 `err:null`（成功）；现改为 `TRANSACTION_STATUS_UNKNOWN` 并阻止事件输出。
2. `available_at>as_of` 过去仅降级覆盖，但资金事件可能已经输出；现调整为先阻断，禁止未来证据渗入 `funding_events/events`，并标记未知。

**新外部技术约束**：v1配置错误可导致 `getBlock` 整块失败；Token-2022 TransferFee、TransferHook和ConfidentialBalance对净到账、CPI与可见金额有直接影响。参见 [现有监控方法专题 §9.1](../domain/meme-anomaly-discovery-state.v1.md) 与 [P3-M01工程契约](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)。**代码没有因此自动支持v1/Swap/特殊Token-2022**。最新工程提交 `d79eafe647542b29745b2a814850be4000d9ccd8` 的 [GitHub CI](https://github.com/sunshihao001/grok/actions/runs/41216119575) 已成功；PR#14/#16仍未合并。

**阶段**：P3 源语义验证继续；已有**官方文档响应格式**核查，未完成**独立RPC重取＋同一签名跨提供者对账**；不进入 P4 大规模实证。下一步优先独立只读重取这两笔签名（`maxSupportedTransactionVersion:1`、固定commitment、记录真实 fetched_at），再选一个协议和一类Swap做可核验解码与不支持样本测试。

## 下一步优先顺序

1. **独立只读 RPC 对账**：对官方文档两笔已公布Devnet签名，由经授权的可用节点使用 `getTransaction`、`maxSupportedTransactionVersion:1` 与固定 `commitment` 读取真实响应，记录采集时间、请求参数、可用性和差异。当前环境对 RPC POST/完整私有历史不可直接取回，因此不得称本轮已完成独立节点核查；无需接私钥。
2. **一个 Meme 协议、一个 Swap 类型**：先固定官方 program ID 与 IDL/源码、指令 discriminator 和CPI/余额校验，在明确正反例下才添加 BUY/SELL 解析。优先已有开放实现；未找到原始交易、转账和资产语义时宁可 `UNRESOLVED`。
3. **C02/C05 依赖**：冻结群体成员、维护资金/动作 as-of 记录；独立定义发行机会和覆盖水位，避免因 v1 整块失败或未知CPI产生虚假群体沉默。

## 阶段晋级判断

**P3 局部实现成立；允许启动小规模只读真实交易语义核查，但不标为 P4 已完成。** 正式进 P4 的前提：可信真实签名和标准答案可复核、支持/拒绝覆盖率已报告、真实缺失区间不会产生假零、正常对照及未触发样本可定义。模型目前不能声明生产实时监控、同控推断或交易盈利。

## 下一轮可直接复制输入

```text
继续 Solana Meme 项目 P3-M01，按照 V2 知识闭环执行。读取唯一进度、现有知识专题第9.1节和 Draft PR #16 的 raw_tx_adapter.py、official-solana-gettransaction-samples.json、测试与工程契约，勿重建系统。

优先取得官方文档中两笔Devnet签名的独立只读RPC回包（使用 maxSupportedTransactionVersion:1、固定 commitment），保留真实 fetched_at、数据来源、返回状态并与仓库保存的官方样本逐字段对账。若环境不能GET/POST该数据，明确报告阻碍；不要将合成 available_at 当成真实取得时间或把缺失meta/未知版本当0事件。

接着选择一个具体 Meme 协议、一种 BUY 或 SELL 类型，研究固定 program ID/IDL/源码与可公开核验签名，以最小独立协议适配器正确区别顶层、CPI、Token账户owner/delegate、费用、WSOL/Token2022特殊金额；给对抗性正负例，只允许可解释的成功动作进入 M01，未知保留 UNRESOLVED。C02/C05 只在可信 as-of 事件与独立完整性可得时继续。

只把新证据和修正写回已有工程合同及M01知识专题；提交GitHub PR#16/#14、回读复核、同步个人 Library 同名镜像并更新本唯一恢复点。不得签名、下单、部署正式监控；最后报告已实际完成的代码/来源/CI、未支持范围、是否进入P4和下一轮输入。
```

## 同步状态声明

GitHub 知识源在 PR #14；实现和测试在 PR #16；GPT Library 的当前便携版和原型目录已生成镜像，**Library 不等于 ChatGPT Project 文件/Instructions 已修改**。此处记录状态以经实际核查的提交、工作流和文档为准；当前没有链上实际测试、Grok Bot 正式部署或自动交易。

## 2026-10-31｜D04钱包角色实务知识补充（并行于P3-M01）

从 GMGN Skills、Birdeye、Cielo、Nansen、Bubblemaps、Watchtower、MadeOnSol SDK、HoldTech 部分公开源码补充不同钱包标签的来源语义与实际局限。核心新增认知：Sniper在GMGN和Cielo定义不一致；Bundler同笔原子交易/Jito Bundle/同Slot群体需要分开；KOL身份绑定与真正主动买入不是一回事；Smart Money盈利窗口与可复制交易分开；地址标签应按身份、执行、库存、历史表现/关系多维并存，并包含来源版本、覆盖、观察窗口及未知。

已修订 knowledge/domain/L3-wallet-actors.md 的原专题与 rolling-reference-knowledge-integration.md 常驻参考池；只属于公开来源核查+源码局部审阅，尚无真实钱包样本独立标签验证，也不代表P3-M01已能解析DEX BUY/SELL。下一优先任务：按当前原始交易适配器能力，选择一个可核对的早期钱包标签使用场景，开展供应商定义→原交易→现持仓/转仓的只读语义对照；尤其先解决Swap经济动作和owner/funder分离，不急于编写万能自动标签分类器。

## 2026-11-01｜功能复用优先与真实项目审计（P3-M01方向复核）


**新增持久资产**：[`reference-capability-reuse-ledger.v1.md`](reference-capability-reuse-ledger.v1.md)。实际读过 HoldTech 主要API路由和部分源码，核查 holder-overlap /deep-scan /funding /analyze /bundler-feed /smart-money /deployer-profile /extension 与架构规格；并比较FnZero Python/Rust SDK、pumpwatch发行者SQLite模块、GMGN Wallet Skills和MadeOnSol接口。阅读源码不等于已执行。

**方向结论：保持Meme经济监控目标，调整默认工程方法为 REUSE_FIRST。** M01目前仅fixture-only且未实现协议级DEX买卖；优先固定FnZero Python解析库并隔离对照现有M01测试与人工交易语义，必要时以Solana官方introspection补版本/CPI核查。不要直接把HoldTech运行代码移植：部分源码用fee payer猜买家和融资者、把钱包年龄当持仓时长、默认最大Holder为pool，且存在疑似硬编码API/Redis凭证、根目录无常规LICENSE文件。以后可将其Holdings、持有人交集、聚集可视化、Dev历史等**分模块**纳入本项目的只读分析。

**当前未完成**：没有调用第三方实时/付费API、没有导入第三方依赖、没有修改PR#16原始适配器与测试；完整许可证/安全审核、外部SDK fixture比较和真实链上语义仍待完成。下轮首选“FnZero Python解析器与M01现有官方fixture的离线对照 + 负例”，并回访HoldTech剩余功能的实际实现/已发布状态，结论写回功能台账。现有P3与S1阶段位置不因文档审计而升级。



## 2026-11-01｜P3-M01 立即纠偏：现成解析器优先，冻结自写底层

**用户指出**：继续扩展我们自己的Solana原始解析属于重复造轮子。查到本知识分支事实上已建立[功能复用台账](reference-capability-reuse-ledger.v1.md)，并事先把 `0xfnzero/sol-parser-sdk-python` 列为P0。这次改为落实既有决策，不再把手写 `raw_tx_adapter.py` 的71项旧离线测试当成扩展理由。

- **已执行**：工程 PR#16 的 `raw_tx_adapter.py` docstring 标记 `LEGACY FIXTURE COMPARATOR ONLY`；停止新写Base58/CPI/Token-2022/DEX版本解析，保留旧回归和fail-closed行为作为第三方库对比基线。原工程数据契约已写明方案变化。**本轮未移除功能或改 M01 窗口算法，不代表第三方SDK已被接入/通过测试。**
- **现成组件原始源码核查**：FnZero Python v0.10.0 固定SHA `cffb6c8` 提供 `parse_rpc_transaction`、RPC签名示例和 `parse_status` 语义；Carbon Rust固定SHA `134647d` 有 Pump.fun Buy/Sell/TradeEvent及其他DEX、离线回放/历史RPC示例，MIT许可证。Solana官方 `transaction-introspection` 可用于账户/指令树对照。完整逐项选择、风险和来源已写入唯一[功能复用台账](reference-capability-reuse-ledger.v1.md)；**都还未在本项目安装/运行/做同样数据对照**，FnZero Python仓库未找到根目录LICENSE文件，使用代码前核对许可。
- **历史底层SDK候选（已由下方成品级决策取代）**：在隔离、无交易账号/私钥的环境固定 FnZero Python版本，用原有 `official-solana-gettransaction-samples.json`+FnZero发布的DEX正例+本项目负例，运行同输入比较；核验 owner、mint、实际成交额、费用、CPI、状态未知与证据时间。必要时以Carbon现成解码器对照；**比较之后只保留一个主要底层组件**，向 M01 做最薄字段转换，禁止再次自研Solana协议解码器。测试要保留失败样本及不支持声明。
- **阶段**：继续P3局部工程，不进入P4。知识状态 `SOURCE_CODE_INSPECTED`、工程方案 `PIVOT_METHOD_KEEP_GOAL`，第三方复用状态 `NOT_INSTALLED_OR_TESTED`，Grok正式监控和实盘为 `NOT_DEPLOYED`。GitHub PR#14/#16尚未合并；GPT Library与Project文件附件须分别核实。

**历史下一轮输入（已失效，请使用文末成品复用输入）**：继续P3-M01，不造轮子。先读取最新进度、功能复用台账、工程PR#16和FnZero Python固定源码。使用隔离本地只读环境按既有fixtures和外部项目的可公开核查DEX正例，对 FnZero `parse_rpc_transaction` 做实际安装运行、输入输出/状态及许可证检查；与现有手写解析器和必要时的Carbon做同输入对照。不得再添加自写协议/指令解码；只在明确事件字段和误判界限后考虑小型字段映射。报告真实测试/失败/成本，更新原PR与知识、GPT Library镜像，最后决定可直接复用还是需换现成方案；不下单不签名。

## 2026-11-01｜整套成品项目优先：修正把复用缩成 FnZero 解析器的错误

**项目主线纠偏**：历史讨论中曾明确参考已完成的 **Kelows/million、HoldTech、pumpwatch、Why-Solana** 和 OKX 现成工作流；当前功能台账遗漏了 **Million 这个功能完整的相似产品**，先后把工作误导向自研底层交易解析器、再误导向只比较 FnZero/Carbon。修正后以现有 [《外部功能复用台账》](reference-capability-reuse-ledger.v1.md) 的**成品项目整体/业务级能力对照**为优先，仍保留原Hermes/qb-/meme-的专业知识和P3-M01历史有效测试。不新建项目框架，也不立即宣布全面迁移至Million。

**已核实际代码（未本地运行）**：
- [Million固定SHA](https://github.com/Kelows/million/tree/c89ad07caaf70773d40b45943e136eadc4f946a5) 已有 NestJS/SQLite+Prisma API、Helius数据入口、钱包↔Token发现crawler、funding/owners关系、live/flows实时观察、copyability/backtest、screener与paper执行，以及14工具MCP和Agent Skills；这比单SDK更接近目标成品。MIT许可已查，但代码含`EXECUTOR=local`实盘执行路径，禁止在本项目启用；Helius密钥/成本、持久性、Grok兼容与关系归因需后续审核。
- [HoldTech固定SHA](https://github.com/co-numina/holdtech/tree/a75e214bf1ee0a8803eb7d93336be98c481c2db9) 包含holder-overlap、deep-scan、deployer-profile、bundler-feed等成品路由，已有许可证与硬编码凭证风险，禁止直接跑原样；[pumpwatch固定SHA](https://github.com/cinder-security/pumpwatch/tree/156a91ab63740ab0ce8700434ff33844d00de519) 可运行只读发行者检测、状态跟踪和SQLite历史；[OKX现成工作流](https://github.com/okx/onchainos-skills/tree/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25) 有新币筛选、Smart Money信号、钱包分析、WS监控、Token研究；用户此前提到的Froggy/Sputnik多为工具功能与专业词汇来源，不能当作已获开源代码。Why-Solana维持review_only用于取证/证据反证。

**现在的唯一优先任务**：不用先新写解析器，也不先单独做FnZero SDK对照。以一个完整**只读业务场景**核查 **Million 是否能直接从一个 Mint 发现关键钱包→持续跟踪这些钱包→展示群体资金/执行变化→输出机器可读取状态或MCP结果**，并与 OKX成套工作流、HoldTech关键分析、pumpwatch Dev监控的既有功能比对；要求记录已可直接运行/需连接数据/仅部分源码/误归因/危险权限。之后才决定 `WHOLE_APP_RUN`、`EXISTING_API_WRAP`、`MODULE_REUSE`、`COMPONENT_ONLY`、`KNOWLEDGE_ONLY`；**不要预先决定要 fork 还是重写，避免多个产品重复搭建。**

**执行边界**：本轮已读关键源码、登记到现有台账和参考池，但未安装/部署外部成品、未验证Grok云电脑环境/付费API/实时正确性，状态是 `SOURCE_CODE_INSPECTED / PRODUCT_REUSE_AUDIT_PENDING`，不是已拥有这些功能。M01/C02/C05仍在局部P3，不触发自动交易、钱包密钥或生产部署。

**下一轮输入（取代历史FnZero-only输入）**：先恢复Million、HoldTech、pumpwatch、OKX、Why-Solana及旧Hermes/qb-的现有项目映射，审阅一个完整只读Mint→关键钱包→持续观察→群体关系报告的现成实现和安全运行要求；若能在隔离环境运行则以原生API/MCP/CLI做最小业务验收，不开发同名功能。记录每一步是否已存在和缺失，比较Grok与成品可直接复用的程度；合适才决定是否封装、保留或替换模块。更新现有台账、知识和进度，下一轮才讨论需要写的极少量胶水。


## 2026-11-01｜Mint→钱包群体监控：完整成品源码验收完成，运行待验证

**本条为当前最高优先级，取代上文历史FnZero-only SDK和“直接开发M01原始解析器”的下一轮建议。** 实际完成的是同一个Mint→候选钱包→持续观察→群体关系→只读解释的**跨项目现有业务源码审计**，并非运行了一个真实Mint。

- **唯一完整产品优先候选：Million** [固定提交](https://github.com/Kelows/million/tree/c89ad07caaf70773d40b45943e136eadc4f946a5)。已经核其discovery、crawler、wallets、live、flows、funding、owners、copyability、backtest、API Controllers、14个MCP工具；这是自托管已连成体系的Solana钱包监控与研究系统，比孤立FnZero解码器符合本轮目标。**不自动fork、不预先迁移**。
- **明确的代码质量差异**：Million的discovery.buyersOf以接收Token和SOL/WSOL/稳定币支出猜BUY，非协议级肯定；live.ingestWebhookTxs按签名仅将同一交易分给第一个订阅钱包，C02群体视角会漏同笔其他钱包；实时原始事件默认15分钟/最多5000条；funding限制3页/50条链接，Owner节点关系存在feePayer/共同融资启发式，coentry被正确避免作union桥，ownerId不是永久经济身份。**这些是直接源码可复查的限制，不是实盘测得误报率。**
- **其他成品不丢**：HoldTech的holder-overlap、深扫、Deployer API需处理疑似凭证暴露和错误feePayer买家归因（原样运行阻断）；pumpwatch的read-only发行者检测/SQLite跟踪已是真实代码，但其getTransaction maxSupportedTransactionVersion=0对v1存覆盖风险；OKX已提供新币/Smart Money/钱包监控WS完整工作流，需服务权限、费用和配额核实。Why-Solana继续review_only作跨币/Hub反证与代码来源，qb/Hermes/meme旧业务知识继续作为入选/归因标准。细节证据与按功能状态见[唯一外部复用台账](reference-capability-reuse-ledger.v1.md)对应日期条目。
- **与grok现实比较**：工程PR#16仅有fixture-only M01单币窗口、保守旧交易适配器和确定性观察器；没有持续钱包↔Mint发现/实时事件/Agent整套应用，故不能再新增同类模块。原项目保留历史窗口/时点/证据覆盖/C02和C05问题，而不是替代Million已做好的工程功能。
- **本地真实运行记录**：使用先前项目存档m01_proto_offline_20261031.zip，在隔离路径本地运行旧M01单元测试，14 tests in 0.840s OK。此为旧基线测试，**不是第三方成品的实际运行，也没有运行工程PR#16当前全量测试**。本容器Node22.16不满足Million要求的Node24，而且无GitHub DNS网络、未授权Helius额度及单Mint数据；第三方项目**没有安装、没有启动、没有连接实际市场/监控Grok**。
- **安全与阶段**：当前结果为SOURCE_IMPL_AUDITED / PRODUCT_RUNTIME_PENDING，项目仍局部P3；Million的EXECUTOR=local真实签名能力不得启用，其local API无认证与Web可能LAN监听需隔离，Helius/OKX付费及持有人/钱包标签不能默认为可信。GitHub PR#14/#16仍是Draft、未合并。GPT个人Library摘要如实记录，项目Instructions/附件未被直接修改。

**新识别的严格只读阻碍**：Million trading.service.ts 在 onModuleInit() 启动每5秒周期逻辑，默认PAPER模式遇到机会也会模拟开仓并写入状态；禁用EXECUTOR=local仅防止真实签名/下单，不等于进程纯只读。下一轮需先检查完整服务启动副作用及开放端口，而不是直接用带实时数据的npm start宣称安全运行。

**下一步只做一件事**：在确有Node24、网络、私有回环隔离及经授权只读Helius配额后，运行Million原生成品的无密钥/不下单健康检查；用一个公开Mint小样本逐次验证GET /discovery/token/:mint、GET /live/status、GET /live/flows、GET /funding/:address、MCP get_flows等**现成读取接口**，记录真实结果、覆盖/截断/费用、同签名多钱包遗漏；暂不自动做钱包订阅/修改/重建/付费。对照OKX完整监控工作流和HoldTech/pumpwatch已存在接口，之后才选择直接使用整个成品还是选择小模块。不要继续自造钱包监控功能。


## 2026-11-01｜成品级功能复用审计：固定 Mint 的五步只读业务链

**本轮按V2实际执行**：重新读取 [完整功能复用台账](reference-capability-reuse-ledger.v1.md)、[滚动参考池](rolling-reference-knowledge-integration.md)、PR#16现有M01和旧qb-/Hermes/meme-/Why-Solana知识；**未重新规划项目、未开发新功能**。审核目标固定为 Why-Solana[公开资料](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/docs/RESULTATS.md)列出的Mint `87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump`；它只是未来对照用的真实链上地址引用，**本轮没有外部独立RPC/Helius返回的Mint数据**。

**成品级结论（源审已读，不代表运行）**：
- [Million](https://github.com/Kelows/million/tree/c89ad07caaf70773d40b45943e136eadc4f946a5) 具备完整API链：`GET /api/discovery/token/:mint`→`POST /api/wallets/import`→`PUT /api/wallets/:address/subscribe`→`GET /api/live/events/status/flows`→`GET /api/funding/:address`及`POST /api/owners/rebuild`，另有Agent/MCP与策略决策日志，**比只开发FnZero解析器更贴近目标。** 不过其`LiveEvent.signature @unique`和webhook「首个匹配钱包认领」丢失同交易多钱包参与视角；`ownerId`聚类不是证实的经济同控且重新聚类ID不稳定；live窗口仅15分钟/5000行，不具备按slot完整机会数据。其默认Paper执行器会自动模拟成交、`EXECUTOR=local`切换真实交易；本项目严格只读不能照搬运行。无认证API和Web可被局域网访问，不能暴露公网。
- HoldTech现有`deep-scan`、`holder-overlap`、`deployer-profile`是可考虑的现成补充，但`holder-overlap`的POST层实际每Mint只取至多200持有人；feePayer代替买家的交易分类不满足本项目；源码有疑似硬编码第三方密钥，**禁止原样运行**。pumpwatch已实现只读Pump.fun发行监控、结果跟踪和SQLite creator统计，属于可复用**发行者支线**，无需另造。OKX `onchainos`已提供直接WS钱包监控和新币/聪明钱等工作流但服务权限/费用未测试；Why-Solana仍`review_only`用以反证，旧qb-/Hermes/meme-作为业务质量标准。
- [本地执行记录] 现有`/mnt/data/m01_proto_offline_20261031.zip`独立解压到`/tmp`后，**14项unittest全部通过**，运行`wallet_batch_monitor`自带fixture，结果`FIXTURE_RESEARCH_ONLY/no_trading=true`、1m有3类行为候选，5m/15m无候选。这**不是PR#16当前71项CI的重新本地运行**，也不是任何外部成品已跑通。

**为什么本轮没有运行Million或连接Helius**：本地仅Node22，Million需要Node24；容器不能解析Github的Git远端，且没有经授权的Helius密钥/免费额度，代码带自动Paper/Local执行与开放API边界，未构造安全隔离运行态。没有为测试擅自安装依赖、启用付费API、密钥或云端监控。当前状态严格为`SOURCE_CODE_AUDITED / EXTERNAL_RUNTIME_UNVERIFIED`。官方[Helius定价](https://www.helius.dev/pricing)与项目内部credit常量也可能不是同一计费口径，不能臆断成本。

**对grok真正缺少的能力判断**：不再优先自研发现、订阅、funding、holder overlap或MCP——源码中已有可复用实现。需要补的是**确保上游成品能保留多钱包同笔经济动作、时间版本、机会覆盖及证据来源**的正确性核验；C02/C05作为本项目专业分析合同继续保留，未启动数据实证。没有完成严格只读完整Mint任务，也不进入P4。

**下一步最有价值的任务（接管本恢复点）**：在有Node24、外部成品源码/依赖以及获授权只读Helius或OKX额度的**隔离环境**，先检查Million只读安全（无交易执行、无公网端口、MCP仅查询），用固定Mint原生API验证「发现→钱包活动→资金与候选关联→只读报告」每一步返回、失败、费用与覆盖；逐项用OKX现成命令及HoldTech/pumpwatch功能对照，决定**整套运行、封装已有API、局部复用还是维持知识参考**。严禁为了跑测试先行复制有硬编码密钥的HoldTech，或用合成数据伪装已验证成品。完整源码/风险/接口与再核触发见[唯一复用台账](reference-capability-reuse-ledger.v1.md)。PR#14/#16仍Draft未合并；Library镜像进度依最后实际同步操作为准。

**✍️ 下一轮可复制输入**：继续现有Solana Meme项目V2，以已审的Million`c89ad07`、HoldTech`a75e214`、pumpwatch`156a91a`、OKX和Why-Solana及旧qb-/Hermes/meme-为基准，不重新设计架构。优先在隔离且只读的具备Node24和授权数据源的环境，对固定公开Mint做一次完整Million原生API业务验收：钱包发现/来源→订阅与交易事件→资金边与群体关系→证据完整性和可解释性；特别测试同笔多钱包丢失、ownerID不稳定、15分钟保留、未知是否被当零、默认自动Paper引擎隔离。比对现成OKX/Holder/Dev工作流，记录接口输入输出/真实费用/失败，只有成品确实不满足才写最少必要胶水。更新已有复用台账、参考池和本恢复点；如无法安全运行说明阻碍，不冒充生产效果。

## 2026-11-01｜增量：FnZero/Carbon许可与源码入口审查、HoldTech四项离线反例
- **源审**：FnZero Python已有按交易签名的RPC解析、mainnet fixture tests，`parse_transaction_from_rpc`以 `max_supported_transaction_version=0` 请求，但另一示例用 `maxSupportedTransactionVersion:1`；版本入口需逐一比较。Python仓库README标MIT但根目录无LICENSE、pyproject无license字段；Carbon源码有完整MIT许可。Pumpkit有Telegram成品监控，但根LICENSE为all rights reserved，不可直接复制。继续核查Million整体业务流程与OKX工作流的适用性，**整套成品优先于仅评估FnZero SDK**。
- **本轮实际本地运行**：Node标准库环境按HoldTech `detectBundles` 和 `extractBuyTimeline` 的判定逻辑手工独立复现四个合成负例，四项断言通过；对应Transfer误称买入/同Slot误称Bundle/fee payer合并真实买方等语义风险。**未运行原HoldTech项目、没有真实RPC、未运行FnZero或当前PR#16最新全套源码**。
- **限制与回填**：终端无法通过DNS访问GitHub，不能完成FnZero↔M01 SDK运行对比；实际审查与结果回填到 `reference-capability-reuse-ledger.v1.md`，生成GPT Library便携报告。P3-M01仍处于fixture-only，来源CI成功不能替代真实数据。下一项最高价值任务是Million严格只读整套业务流程验收，FnZero作为后续语义缺口补强，不能反过来。

## 2026-11-01｜外部复用方案离线验证（本轮）

本轮已执行的能力核查：从GPT Library的P3-M01便携快照恢复Python包、2份测试与fixture，实际在隔离目录运行**38项离线单元测试全部通过**，且`raw_tx_adapter → wallet_batch_monitor` CLI成功；此结果**只代表Library快照**。核查当前PR#16工程head `3ee17255f4c849d6be4ede93e6ee7e516a068de1` 的GitHub `monitor-tests` CI为success，未独立在本地运行其全部最新测试。

FnZero Python源码审阅确认`sol_parser/rpc_parser.py`接受RPC JSON并输出事件与解析状态、示例支持`maxSupportedTransactionVersion=1`。但尝试在隔离环境拉取仓库/查询PyPI遇DNS不可达，**FnZero SDK未安装，和M01的真SDK对照仍BLOCKED**。其Python仓库根目录缺常规LICENSE文件，尚待进一步许可审核。读取Go `DefaultPerson/solana-dex-parser-go`（MIT、v1/Jupiter、Go集成成本、默认未知DEX启发式需审）与TypeScript `cxcx-ai/solana-dex-parser`（MIT）为竞争候选；Helius Parsed Events/Streams 为付费对照选项。pumpwatch提供可复用SQLite发行历史和重试逻辑，但原源码getTransaction固定maxSupportedTransactionVersion=0，不宜认为覆盖v1。

独立三组合成规则反例说明HoldTech现有same-slot + fee payer条件可能在纯TRANSFER/UNKNOWN或独立买家场景产生Bundler候选；**只运行规则重现而非HoldTech本身**。更新持久功能台账`knowledge/system/reference-capability-reuse-ledger.v1.md`，现在不改变P3-M01业务能力/工程代码，不引入私钥、收费源或签名。

**方向**：REUSE_FIRST继续，核心是找到对真实交易负例可靠的成熟DEX解析实现，制定最小 M01 可选桥接，而不是扩大自制解析器。下一首选：在具备SDK依赖与授权许可的可联网隔离环境执行FnZero Python与M01同输入对照；若其准确性/许可不达标，转向MIT Go/TypeScript项目。并行仅做pumpwatch/HoldTech不依赖私钥的具体功能审查，避免项目失焦。

## 2026-11-01｜当前优先任务更正：先验收成品Mint报告，再做长期只读监控

**纠正上段仍以FnZero优先的时间顺序**：经本轮实际重新读取OKX `cli/src/commands/workflows/token_research.rs`，`onchainos workflow token-research --address <mint> --chain solana`有已经写成的Rust CLI整套Token Report→Holder/Cluster/TopTrader/SM→条件性Dev/Bundle链路；失败保持null。**第一项完整业务最短路径应先验证OKX整套单Mint只读报告，而不是先安装第三方DEX解析器。** FnZero保持待触发的交易解码候选。

**成本新增关键约束**：OKX官方当前Free订阅 Basic/Premium各100K/月、**不含WS**；Starter $99/月支持WS。Helius Free 1M credits/月/10 RPS；实时运行和API计费需实际授权确认，不自动支付。Million全成品（Node24）有自动Paper及可切至`EXECUTOR=local`的真实交易执行，不能将普通安装等同严格只读。源码`LiveEvent.signature @unique`+webhook首命中退出会丢同签名多钱包视角；本轮用内存SQLite独立复现UNIQUE第二条插入失败（**不是Million本体测试**）。

**本轮实际本地复验**：基于之前Library版P3-M01，Python 38/38单测通过，并成功运行raw_tx_adapter→wallet_batch_monitor离线合成Token Transfer流；仍`FIXTURE_RESEARCH_ONLY`，既无真实链上数据也无Grok云电脑验收。当前不能执行OKX/Million在线成品（Node版本、授权服务密钥和环境限制）。功能台账[新增成品优先与成本/安全/多钱包约束](reference-capability-reuse-ledger.v1.md)，原S1阶段和PR #14/#16 Draft状态未升级。

**下一轮唯一优先执行任务**：在有已授权且可审计的OKX只读Key、禁用自动支付的隔离环境，对固定Mint执行`onchainos workflow token-research`、保存逐接口原始响应/费用/时点/UNKNOWN；若无法验证权限，在离线环境检查工作流自身的Rust unit tests及假输入输出。再基于同Mint决定Million是安全部署整套、封装只读子系统还是仅作知识参考；只因实际经济事件缺口才转向FnZero/Carbon，禁止把问题退化成持续自研解析器。

## 2026-11-01｜用户确认的人机分工与21专家统一项目审查

**长期核心需求（来自用户直接指令）**：用户并非程序员或产品设计师，只能以自然语言描述目标、现象与期望，需要GPT作为专业“外挂大脑”自主利用已有专家知识完成跨领域项目分析、产品化任务定义、最优现成方案复用、工程与数据风险核查、整合与必要执行；不能让用户负责专业架构和技术路线选择。**这是一条关于AI责任和知识调用方式的指令，不是希望得到21段专家套话。**

**实查现有体系**：`knowledge/experts/registry.v1.json`已有21位E-L0-01至E-L7-02，涉及D01–D12；`expert-mechanism-research-method.md`原来按单机制1–3名主/挑战者开展深研。这种设置适合单专题，但覆盖完整产品业务链时需**先21专家全覆盖检查→再挑有真实分歧的专家深化→一份统一的业务、技术、数据、证据、实施结论**；已经回写到建议Project Instructions与原专家方法中。仍然没有部署21个Bot。

**针对当前任务的综合专业结论**：L0/1指出OKX字段/采集时间/交易Owner语义与Million同签名多钱包漏记；L2/3指出Mint阶段、LP/自由库存、资金服务Hub与真实控制和KOL/SM标签混淆；L4/5指出异常≠信息优势、监控阶段不应自动交易；L6指出需要分母、负例、独立数据验收；L7把这些归并到最少必要实施顺序：**首先直接用现有OKX Token Research做一个Mint的只读报告验收→其次安全验Million成品数据连续性与同签名多钱包修正需求→缺经济事件语义时才调用成熟FnZero/Carbon→用既有D04–D11知识给出带证据/未知的群体说明→Grok运行端在既有S1审批下交付**。未实际运行第三方整库、无已授权API、无生产监控；保持原PR Draft边界。

**知识系统防碎片措施**：此原则的唯一主规范位置是`knowledge/system/expert-mechanism-research-method.md`、简短项目入口是`gpt-meme-project-instructions.v1.md`；所有具体外部功能仍复用`reference-capability-reuse-ledger.v1.md`，D04–D07专业知识保留在L3专题，其他现有领域按需回填。不再另起新专家注册表、产品方法框架或机器人编组。

**待验**：将GitHub建议指令由操作者更新到ChatGPT Project Instructions并核对附件版本；GitHub/Library保存不等于账户Memory即时更新，也不表示已在Grok云电脑部署。下一轮核心是用“全域专家覆盖+冲突深入”的方式执行一个Mint成品只读报告验收，不再从零规划系统。

## 2026-11-01｜首次21专家全项目联合审查：统一实施判断

本轮已在现有注册表完整复核E-L0-01至E-L7-02共21位专家及D01–D12正式目录，且直接复查旧Hermes `CONTEXT.md`、qb- `sikk_gmgn_token_report.py`、meme- `SOURCE_OF_TRUTH.md`、现有工程Draft PR #16和OKX/Million/pumpwatch等原始业务源码。没有创建新专家、本体或Bot；审查专业冲突后已在[唯一外部复用台账](reference-capability-reuse-ledger.v1.md)记录21项逐一覆盖的技术/经济/实证检查。

**专家知识成熟度提醒**：实际读取`gpt-meme-project-index.v1.json`发现D01与D07仍标`declared_research_gap`，其他域主要是`legacy_seeded_unverified`；21专家覆盖审查只是专业问题检查，并不表示21位专家所述假说均经真实市场验证。应当以成熟外部源码和真实事件补齐D01交易真实性、D07群体时序的关键事实链，不把知识目录完整当能力完整。

**统一产品/工程结论**：最终目标是Meme全市场可解释监控，但第一完整验收必须是**一枚Mint在明确时点的可审计只读报告**，第二步是同Mint后续钱包活动/持仓两时点与多钱包群体变化；两者不等同于全市场覆盖。优先运行现有OKX Rust `token-research`成品业务流（需用户授权只读Key/禁止自动x402支付），再评估Million发现/订阅/funding/flows是否能保留同一签名多钱包与完整余额演化，必要时只做小修补；FnZero仍是确认有DEX协议语义缺口时使用的成熟解码候选。原qb单币关键地址矩阵是第一报告输出的可复用业务模板，不再把用户推回手动产品设计。

**新改变结论的事实**：pumpwatch `record_launch` 的`seen_at`取本地`time.time()`，历史回填时24h/7d统计不一定代表链上创建频率；Million`RosterPosition.qty Float`与递增账本不能自动保证任意Token原子数精度、Token-account Owner和源缺口一致性；Solana Foundation新增MIT开源`solana-microscope`（Program级监控、Carbon解码、Prometheus/Loki/Grafana、RPC/Yellowstone回补检查点）可作为D10长期可靠性资产，但它是一Program监控系统，依赖较重，**本阶段不部署**；Helius DAS/Parsed Events可作为真实数据独立对照，费用另算。五种关键冲突包括：供应商标签≠同控、同Tx多钱包漏记、持有人≠自由库存、异常≠可跟随优势、按需Mint研究≠全市场持续覆盖。

**版本/执行边界**：本轮是源码/规范/外部公开文档审查和GitHub落库，不是外部SDK或OKX/Million/Grok Bot的实盘数据测试。PR #14的base是`research/actor-economic-mechanisms-20261030`，PR #16的base是`main`，两条均Draft，不能假设两路功能已合在main。PR #16之前GitHub `monitor-tests` CI success，只说明离线合同测试通过。既往38项Python成功属于**上轮**Library旧快照；本轮不冒充重新实跑。

**下一项只做完整业务链的外部成品验收，而不是继续自研基础解析**：先在可联网、具备明确权限、无签名/自动支付的隔离环境对一枚固定Mint执行OKX `token-research`并保存真实response、slot/时间、失败、额度、标签定义；若当前环境不具Key，先基于OKX CLI现成`assemble()`测试对null/结构/业务缺口做离线审查，不要求用户选择技术实现。然后审查Million同签名A/B钱包关系、Token Account余额精度及历史恢复。合并/跨分支集成与Grok运行另行检查，不因为文件更新宣布成品部署。

## 2026-11-01｜优先交付能跑的成品：最薄OKX Mint报告已写代码（最新）

**用户目标纠偏**：成熟项目不可能一轮完成，当前最重要的是先用成熟业务流程搓出**真实可运行的第一版**，之后逐步增强，而非先完善全市场、21专家框架或整合所有开源仓库。正式产品主体仍为`sunshihao001/grok`，外部项目是可替换的业务能力来源。全项目21专家检查继续服务于成品交付和证据缺口，不成为阻断首版的额外会议。

**本轮真正做的工程代码**：工程Draft PR #16 `research/p24-cross-mint-m01-batch-monitor-20261031` 新增`src/solana_meme_os/mint_report.py`、`tests/test_mint_report.py`和`fixtures/okx-token-research-demo.json`，无需调用RPC/OKX服务器、无钱包权限、只接受用户提供的**现成OKX Rust CLI `token-research` JSON结构**`{ok:true,data:{workflow,address,chain,core,structure,launchpad}}`，验证Mint/链/成功状态，保存不擅自编译标签的Markdown和JSON，`null`表示未知，快照处理时点不冒充链上事件时点。提供`--fixture`防止将演示当真实。**本地真实运行6/6新增离线测试；把新增文件覆盖进此前Library P3-M01离线快照后联合跑44/44通过**（不是重拉当前PR#16所有最新测试）。源文件经GitHub create_file+fetch_file逐项回读一致，README和`docs/next-steps.md`已添加运行方式和明确验收。无实时数据实测。

**现在的产品路径**：先实现`Mint→OKX完整按需查询→可读报告`的第一份**真实**报告，这一步需用户已授权的只读API及安全环境，禁用自动支付/交易，记录API失败/null、来源时间和用量。再用两个不同时点报告接入当前Grok observation监控的**经验证指标**，随后才按目标需求评估Million钱包持续订阅、pumpwatch Dev历史、FnZero DEX解析。拒绝把多套成品整库拼起来或为产出“专业感”先开发UI和多Bot。第一版尚不是全市场实时运行平台。

**暂不采用Million作为首版母体的技术事实**：其`AppModule`、`LiveModule`、`OpportunitiesModule`直接/间接依赖`TradingModule`；`EXECUTOR=local`签名交易且default paper有自动仓位逻辑，不能简单删去交易按钮视为安全；`LiveEvent.signature @unique`和Webhook首钱包`break`还造成群体观察漏记。全量fork只读化的实际修改面比调用OKX现成Token Research宽。此结论仍可被未来安全运行试验推翻。

**下轮最值行动**：直接在可用联网隔离环境以**真实Mint**运行已安装且获授权的OKX CLI，将其原始`{ok,data}`保留，调用新`mint_report.py`生成可追溯的Markdown/JSON，实测实际API成本/字段/失败并判断是否进入`V0.1 REAL-MINT REPORT`。若无法运行则继续完善离线契约验证、暂不启动新功能开发；21专家只针对输出中数据/经济语义的关键差异介入。

## 2026-11-01｜V0.1业务摘要升级：12项测试通过，真实数据接入仍待授权

**运行成果（新增）**：在工程Draft PR #16继续复用原`mint_report.py`薄适配层，不新建系统。现在能从符合OKX官方字段契约的`token-research`JSON中生成首屏业务摘要：返回样本内关键钱包、持仓原始字符串、fundingSource关系候选、Cluster异常研究指标、TopTrader样本行数、Dev/Bundle是否有供应商数据、请求/行情时间的来源路径；原数据完整保留，任何资金边或聚类均不认定同控。使用新合成字段样例实际生成Markdown和JSON，新增12/12单测通过；与本地已保留的**旧Library版**P3-M01联合50/50单测通过（不是对最新GitHub整仓完整重跑）；源码/测试/fixture已在PR #16落库并逐个读回相等。**仍为合成演示，没有任何真实Mint的OKX API返回**。

**真实验收阻断**：本轮本地容器DNS外网连接失败，`onchainos`CLI未安装，无OKX授权会话；项目无需在未授权条件下尝试安装全部OKX交易/支付工具。GitHub连接可审代码而不等于在Grok云电脑运行。官方OKX[holder文档](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-holder)最多返回100个候选，样本不代表全链持有人，fundingSource只是供应商提示；[cluster文档](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-cluster-overview)的相同资金来源比率/新地址比率等是统计口径，不是真实控制证据。当前不能宣布V0.1真实Mint成品，也不能拿费用免费额度当已验成本。

**产品路线不变**：先从用户已授权的只读OKX工作流取得真实JSON并跑完报告；若失败才考虑替代成熟数据源，明示费用与覆盖；完成后再做同Mint两时点与Million钱包连续事件。D01（真实交易/owner）和D07（时序观察）是未来需要优先补足的专业知识，不迫使首份快照报告提前拥有完整全市场情报。

## 2026-11-01｜全量65参考资产登记 + 专家集成职责增补（最新）

**本次用户要求**：不能只围绕OKX/Million，也不能让历史的重要程序/论文/实务工具在新会话消失。已从GitHub现有台账、原索引及之前确有记录的材料线索重新恢复项目参考池，**在原`gpt-meme-project-index.v1.json`增加`reference_assets.items`共65项**。5项原先固定`source_repos`保持不变；65项涵盖旧grok/Hermes/meme-/qb-/Why-Solana、OKX/Million/HoldTech/pumpwatch、DEX parser/Carbon/Yellowstone/Raydium/Jito、MadeOnSol、MELT/RED-COHORT/CCS/USENIX、QuantBloc、Froggy/Sputnik和早期工具名称等。每项有REF编号、准确项目身份或未核实标记、URL（证据不足不猜）、主要可复用功能、优先级、主责专家和重访触发条件。精确审查统计为：`SOURCE_AUDITED=17 / REPO_VERIFIED=10 / PAGE_VERIFIED=11 / HISTORICAL_NAMED_ONLY=26 / LINK_UNRESOLVED=1`；**登记不能推出65项已安装、可复用或者市场主张成立**。完整清单和示例见[现有功能复用台账](reference-capability-reuse-ledger.v1.md)最后一节。

**专家职责审查结果**：原21位覆盖Solana技术、经济身份、库存、异常、反证、知识综合和持续故障，但**跨成熟产品整合/许可证/第三方支付安全/依赖/最小可交付验收**没有明确负责人，属于当前V0.1进度无法继续的重要缺口；已在原注册表**最少新增E-L7-03「开源成品集成与产品交付专家」**并与B01/B07既有能力关联，索引`expert_ids`与`counts.specialists`同步为**22**。它不是新Bot、没有新增L/D门类或生产授权；现有专家机制研究方法和项目指令也已同步修订。其他新专家暂不加，未来必须有可证实的专业失败场景再考虑。

**对成品路线的影响**：由E-L7-03主导先审查每个候选的真实可运行端到端价值，E-L0/L1/L3/L6针对来源、钱包/库存、因果和反证独立挑错。**仍以grok为唯一项目、OKX按需Mint完整工作流为V0.1真实数据优先来源、现有`mint_report.py`为最薄可读报告适配**，不是要一口气部署全部参考资产或重新设计系统。新增QuantBloc可用于未来跟单信息差研究，但不能因新资料中途改变首份真实Mint报告的硬阻断：目前本地只做合成演示，OKX授权/真实数据/费用/连续Grok运行尚未验收。

**当前分支状态**：仅在知识Draft PR #14更新索引/专家/台账/方法，在工程PR #16记补充任务；未合并main、不触碰交易、不声称上线。后续每次发现新项目先查`reference_assets`是否已有同一实体，若有就增量更新证据/版本/重访触发；找不到才登记新REF；**历史只有名字的线索不自动提高验证等级**。

## 2026-11-01｜V0.1首批真实Mint交易池报告交付：两个Mint、12池，完整钱包/Dev仍未验收

**这一轮真正新增的实务进展**：工程Draft PR #16已经有`src/solana_meme_os/public_pair_report.py`，它**仅使用无需密钥的DEX Screener公开只读GET**，固定域名、拒绝重定向、最大2MiB、12秒超时、校验chain/Mint、出错/空返回不下结论，并通过`mint_v01.py`提供单Mint统一入口：无预存OKX JSON→真实公开交易池数据，有已获授权的OKX `token-research` JSON→原有`mint_report.py`的完整候选分析展示。没有任何交易/签名/付款或自动运行OKX客户端。GitHub Actions[真实联网运行41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009) 成功读取两枚公开Mint的**5个+7个实际交易池**，保存原始供应商JSON、Markdown/JSON报告和SHA256；Action Artifact已下载并在当前执行容器独立比对哈希和池内Mint匹配。长期证据见[工程实测记录](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/evidence/v01-real-public-pair-readonly-2026-11-01.md)，Action提供临时ZIP下载30天，临时联网CI步骤已移除，常规CI恢复离线。

**业务等级严禁混淆**：已验证`REAL_PUBLIC_POOL_SNAPSHOT`（真实池/DEX/供应商24h交易/流动性）**不等于**`REAL_COMPLETE_MINT_REPORT`（钱包Owner、Holder、资金边、Dev历史、真Swap、库存和异常）。未获得OKX授权工作流真实JSON，不能声称OKX实时接口运行过；本地无公网DNS，网络执行来自GitHub托管CI环境，**更不等于Grok云电脑已上线**。早先对BONK样本公开接口返回`[]`被保存为`COVERAGE_UNKNOWN`，不是没有流动性；同Mint作为base和quote的不同池必须避免错误价格归属或池统计当钱包交易。

**E-L7-03+E-L0/L1/L3/L6联合实施建议**：不再为了实时数据“接更多API”而扩大功能范围。下一最值步骤为用已授权、安全隔离、x402付款能力禁止的环境**真实运行现成OKX token-research→保存原始JSON→用现有mint_report消费→与本次公开池数据对照关键字段**。源码审查发现OKX `cli/src/client.rs`具有自动x402收款配置、402后签付款逻辑，**不能认为执行只读查询等于绝对不会支付**，在未确认无付款能力前不得让本项目自动执行OKX CLI。若授权确实无法获取，才研究65项台账中能真正提供Holder+Dev的成熟替代完整工作流。所有新能力在工程Draft检验并回写，无交易、无主分支合并。

## 2026-11-01｜V0.1真实Holder/Creator候选与跨源池库存反证（当前恢复点）

**实际完成**：在工程PR#16，已通过[真实GitHub Actions 41268982018](https://github.com/sunshihao001/grok/actions/runs/41268982018)取得同一Mint的DEX Screener公开交易池和RugCheck缓存报告：20条Holder候选、Creator候选，原始响应与SHA已从Artifact重新下载核实；独立[RPC运行41268871079](https://github.com/sunshihao001/grok/actions/runs/41268871079)收到HTTP 429，故没有链上Token Owner独立确认。OKX完整token-research的授权真实结果仍未获取，Grok云电脑仍未部署。

**新增可执行的经济反证**：RugCheck首位Token Account供应商占比约5.88%，其报告的Owner候选与DEX返回的PumpSwap池地址`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`精确相同。这不是确定真实Vault或庄家身份，而是**不可直接统计为自由鲸鱼持仓**的结构性提醒。已修改工程`mint_v01.pool_related_holder_observations`，在真实来源齐备时报告地址全等及来源路径，保留`NOT_CHAIN_VERIFIED`和反例；离线CI运行120项通过。已回填原D01/D03与D04–D07知识，完整实际案例在[工程证据文件](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/evidence/v01-pool-vault-holder-cross-source-2026-11-01.md)。

**下一项唯一高价值能力**：在授权且无自动签名/支付风险的环境取得OKX原始token-research完整JSON，或通过稳定的只读RPC/DAS独立核验该Token Account与Pool/Vault结构。先把真实账户经济角色验证正确，再实现历史Dev/资金网络，不扩建专家知识框架、不重复开发行情接口。
