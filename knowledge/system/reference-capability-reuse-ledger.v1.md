# Solana Meme｜外部功能复用与长期能力台账 V1（2026-11-01）

> **最新已实测复用（2026-11-01）**：为避免“只审了源码/只写方法”长期阻碍成品，工程PR #16直接调用已登记REF-066 [RugCheck现成Token Report](https://api.rugcheck.xyz/swagger/index.html)的**免费缓存GET**，与DEX Screener现有池报告合并。真实[GitHub Actions #41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)获得同Mint5池、20条TopHolder Token Account候选、Creator候选；**1条holder owner实际匹配PumpSwap池地址且供应商标AMM**，现成标签不能直接当独立鲸鱼/庄家。原始响应和SHA校验见[工程实测](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/evidence/v01-real-rugcheck-holder-2026-11-01.md)。缓存数据非独立链上复算，Dev全历史与资金边未知，公共Solana RPC曾因429拒绝。本台账旧“未实现真实Mint关键钱包来源/OKX唯一硬前置”的说法仅适用于完整增强版；**当前免费V0.1已可输出真实供应商候选，下一任务V0.2资金和群体关系**。本次REF-066已由历史提名修订为已核查官方页面+真实运行证据，仍不升级为直接经济控制事实。

# Solana Meme｜外部功能复用与长期能力台账 V1（2026-11-01）

> **性质**：现有 `rolling-reference-knowledge-integration.md` 的**功能级子账本**，服务于 P3-M01、B01–B05、D01–D12，不新建知识本体或运行框架。本账本记录“看过哪些现成功能、是否能安全复用、具体差多少、什么时候复查”，而不是已安装或已运行的功能表。当前仅核查了下列代表性项目的一部分源码；`SOURCE_CODE_INSPECTED` ≠ 本地运行/真实交易核验。全部第三方代码视为不可信输入，未经许可/沙箱审计不执行。
>
> **研究原则**：先找现成功能/成熟库/外部服务 → 看实际源码、测试、契约、许可证、成本与误判 → 选直接调用、封装、最小移植、暂存知识或明确拒绝 → 仅补缺失的业务胶水 → 使用相同输入对照测试 → 更新 Dxx-Kxx 与本账本。禁止先宣布重构架构，再回头寻找理由。发现真正成熟的替代方案应允许 **PIVOT**。

## 2026-11-01｜成品项目整体能力复用：纠正仅评估解析SDK的偏移

**纠偏动作：AMEND 本功能台账，非新架构。** 用户此前已将 Kelows/million、HoldTech、pumpwatch、Why-Solana、OKX 等作为完整项目或完整工作流参考。此前本台账虽已列HoldTech多项业务能力，但没有登记 **Kelows/million** 这个高度相似的自托管成品；随后错误地把“FnZero Python交易解析”当作唯一下一项实验，遗漏了“已有整套钱包监控/发现/跟单/AI命令入口可否直接复用”的上层问题。**本节取代下文旧句“下轮唯一主实验为FnZero SDK”所表达的优先级；FnZero仍是组件候选，不再代表全系统技术选型。**

### 按整个成品/业务功能检查，不按SDK或论文先拆碎

| 既有参考及已核验源码 | 已有成品能力（项目自己实现，非本项目已部署） | 与我们的能力交接 | 实际限制和先验证什么 |
|---|---|---|---|
| **[Kelows/million](https://github.com/Kelows/million/tree/c89ad07caaf70773d40b45943e136eadc4f946a5)**，MIT | **完整自托管应用**：`apps/api/src/crawler/` Token↔钱包持续发现；`discovery/`大买家；`funding/`资金来去；`analysis/owners.service.ts`关系图/候选群组；`live/live-feed.service.ts`/`flows.service.ts`钱包WS及群体进出资金；`copyability/`跟随延迟；`backtest/`、`screener/`、`opportunities/`、`trading/paper.executor.ts`纸面研究；`packages/million-mcp`现成14个Agent工具及`.claude/skills`口语化操作。均已核查实际文件/业务服务实现。 | **最高优先：先作为整体参考运行基线**，与现有grok的发现→观察→关系→监控→解释功能逐项对照。能用完整流程时不要独立重建；可以选择保留其原服务/API或按许可证复用合适模块。M01/C02/C05只扩展它缺失的专业判断。 | Node24/NestJS/Prisma/Helius依赖，是否适合Grok云电脑待核；Hub排除和co-entry阈值是启发式，`ownerId` rebuild不稳定，不能定论同控；有`EXECUTOR=local`真实交易开关，本项目只读要求**明确禁用**，不能安装后自动启动交易。**未本地部署**。 |
| **[co-numina/holdtech](https://github.com/co-numina/holdtech/tree/a75e214bf1ee0a8803eb7d93336be98c481c2db9)**（此前审过） | Next.js成品：`app/api/{analyze,deep-scan,holder-overlap,deployer-profile,bundler-feed,smart-money,holder-count}`等已实现业务路由；可追踪持有人/跨币交集、资金候选、Slot群体和发行者历史，附UI/扩展。 | **与Million形成能力对照/补充**，尤其群体持有比例、交集和代币结构；不再为这些功能先造新模块。 | 旧台账记录过fee payer误判买家/融资、holder和时间口径问题、疑似硬编码服务凭证及根目录LICENSE边界。**不直接运行不拷配置**；按具体路由安全审计后再挑选。 |
| **[okx/onchainos-skills](https://github.com/okx/onchainos-skills/tree/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25)**，MIT | `workflows/{new-token-screening,smart-money-signals,wallet-analysis,wallet-monitor-ws,token-research}.md` 加对应`onchainos` CLI：新币、Dev、bundle、Smart Money、地址WS事件与筛选等成套现成业务命令；非仅接口名称。 | **优先验证现成只读工作流是否已满足某项监控目标**，不写额外采集循环；可能作为Grok运行时只读数据能力。 | 文档/命令存在≠当前账户接口可用、免费、低延迟或覆盖完整；某些workflow标注`okx-agentic-wallet`依赖，**只审查/执行read-only命令**，不授权交易、签名或支付。尚未调用实测。 |
| **[cinder-security/pumpwatch](https://github.com/cinder-security/pumpwatch/tree/156a91ab63740ab0ce8700434ff33844d00de519)**，代码MIT | 已有`code/pump_watch.py`（只读pump.fun日志订阅、429重试与并发限制）、`outcome_tracker.py`、`creator_reputation.py`（SQLite发行历史）、`run_watchdog.sh`、可复算SQLite数据与脚本。 | **现成发行者/新币监控支线**；可复用它的整条检测→状态→发行者累计工作流，先评估而非另造。 | RPC依赖与历史/覆盖限制；发行者身份及作者样本统计未在本项目复算；尚未本地部署。 |
| **[sunshihao001/Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/tree/9a7ad51d56328e91e67e3f531d6744307d0ee68b)**（review_only） | `code/{03_split_detector,04_early_buyers_funding,06_hub_map,07_harvest_creations,09_bundle_snipe,a7_cross_token_links,r1_burst_window,rpc_client}.py`等完整研究脚本、反例、回测和可复核历史资料。 | **专业取证/异常发现模块与反证基线**；对照资金图/新币同步/跨币，保持研究代码与生产监控不同身份。 | 历史样本和作者假说不能原样当实时信号或已复制净优势；固定来源准入`review_only`、复算和许可证均须遵守。 |
| **旧[qb-](https://github.com/sunshihao001/qb-) / [Hermes](https://github.com/sunshihao001/-) / [meme-](https://github.com/sunshihao001/meme-) + Froggy、Sputnik** | 前三者已有单Mint关键钱包报告、资金/库存分析流程、阶段/反证知识；Froggy/Sputnik是实际功能/字段研究来源，不等于已开放全部程序代码。 | **复用以前已经形成的专业认知和字段需求，作为评估外部成品的标准**；不能因拿Million做基线就丢弃业务研究。 | 旧GMGN有费用限制；Froggy/Sputnik API/源码与运行授权未核；历史代码不等于当前可运行。 |

### 相同问题先找成品，而不是继续拆底层

- **发现/长期看钱包**：Million crawler+discovery+live + 自带MCP；OKX wallet-monitor-ws。先比较实际部署、覆盖与成本，再决定用哪一种；M01原型只保留其特有的成员窗口行为价值。
- **钱从哪里来/群体怎样变**：Million funding+owners+flows、HoldTech deep-scan/holder-overlap、Why-Solana资金图/跨Mint脚本。重用已有图/交集/事件流，项目只需对含混归因、时序与反例做专业增量。
- **监控新币/开发者**：pumpwatch整条发行者工作流、HoldTech deployer-profile、OKX memepump新币/Dev/bundle命令。先对比同一Mint的输入输出和真实时效。
- **判断是否值得跟**：Million copyability+backtest+decision log、旧qb/Hermes库存与执行时点知识。纸面测量与真实可执行报价/净收益分离，不依赖K线作为研究主线。
- **AI简单命令操作**：Million的14个现成MCP工具和Skills可提供操作模型。先确认Grok云电脑是否实际能调用现成API/MCP，再考虑最薄命令封装；不必先设计新多Bot结构。

**执行优先改为**：先同目标对比并尝试**完整成品只读功能**（优先Million的功能闭环、OKX现成工作流），如果不适合运行，再选其**可单独复用业务模块**（HoldTech/pumpwatch/Why-Solana），之后才评估**底层SDK**（FnZero/Carbon）；只要仍满足用户的独立专业知识和风险边界，允许保留现有grok薄运行包装。不得未经对照就推断“应全面迁移至Million”。

**本次证据级别**：已核仓库文件/源函数/明确工作流命令、许可证和限制，尚**没有安装/运行Million、OKX或pumpwatch，也没有证明Grok环境兼容或数据计费**。下一轮最有价值的交付是将**一个完整只读业务任务**（例如“一个Mint→发现前期参与钱包→追群体后续活动→解释群体买卖与不确定性”）用成品能力完成对照，明确哪一步根本无需我们再开发；而不是再单独安装一个交易解析器。

## 2026-11-01｜单Mint到钱包群体：成品业务链路源码验收

**本轮只审查，不开发、不开监控、无真实Mint或授权Helius额度。** 目标为“输入一个Solana Meme Mint→发现买家/持有人→追踪钱包活动→资金/群体关系→输出解释和未知”。代码存在不等于已部署、已实证。参考SHA：Million c89ad07caaf70773d40b45943e136eadc4f946a5；HoldTech a75e214bf1ee0a8803eb7d93336be98c481c2db9；pumpwatch 156a91ab63740ab0ce8700434ff33844d00de519；OKX 73904b636a0f022dcc13b6d7a0dd2ed3b3195f25；Why-Solana 9a7ad51d56328e91e67e3f531d6744307d0ee68b。

### 现成业务功能分段检查（实际阅读对应程序）

| 任务段 | 现成实现与路径 | 关键边界/可复用状态 |
|---|---|---|
| Mint→候选买家 | [Million discovery.service.ts](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/discovery/discovery.service.ts) 的 find/buyersOf；GET /discovery/token/:mint；crawler.service.ts 的钱包↔Token持续发现 | 有代码、候选上限30或深采60；buyersOf按Token接收+SOL/WSOL/USDC/USDT支出估计“买入”，不是完整协议级确认；历史采样和池子排除不是全量。不可将其当所有Mint的真实买家真值。 |
| 持续钱包订阅 | Million wallets.controller.ts 的钱包导入、分析、订阅；live/live-feed.service.ts 的Helius WebSocket/Webhook及GET /live/status、GET /live/events | 现成服务与断线恢复；WebSocket默认最多25个订阅，Webhook另有依赖；原始LiveEvent默认15分钟或最多5000条便清除，不等于可做历史C02/C05完整窗口。分析/订阅会变更数据库、消耗API额度；本轮未调用。 |
| 群体增减仓、分发 | Million live/flows.service.ts；GET /live/flows；analysis/ledger.ts | 已汇总钱包数、候选owner数、买卖方向和片段；但 ingestWebhookTxs 对一笔签名只处理**第一个命中的已订阅钱包**并退出，可能遗漏同一交易的其他钱包视角；processTx以Token及SOL/USD净变化推断BUY/SELL，不能直接当作DEX逐指令成交确认。 |
| 资金与钱包候选关系 | Million funding/funding.service.ts（GET /funding/:address）、analysis/owners.service.ts（POST /owners/rebuild）；HoldTech deep-scan/holder-overlap | Million有真实SOL转账边、最多3页/50链接并报告截断，聚类带Hub排除，co-entry故意不用于直接连接候选控制组；ownerId重建后不稳定，funding和feePayer都不能证明同控。HoldTech把feePayer当买家、用同Slot推组；跨Mint holder-overlap每Mint只取前200个，不能宣称全量。 |
| 发行人/新币观察 | pumpwatch code/pump_watch.py、creator_reputation.py、outcome_tracker.py；HoldTech deployer-profile；OKX workflows/new-token-screening.md | pumpwatch已有read-only订阅、429退避、SQLite发行历史与结果追踪，是真成品流程；其 getTransaction 的maxSupportedTransactionVersion=0，面对v1需明确覆盖风险。HoldTech内多处有疑似硬编码第三方访问凭证，禁止拷贝、运行原配置或使用其中密钥。OKX现成工作流需CLI/账号能力，未实测。 |
| AI接口与可解释输出 | Million packages/million-mcp/index.mjs 有14个API工具，及 .claude/skills/* 自然语言使用流程；OKX workflows/INDEX.md、wallet-monitor-ws.md、smart-money-signals.md | 现成get_status/get_flows/get_decisions/find_token_buyers/analyze_wallet等，**也存在update_rules/import_wallets/set_wallet_subscription等写动作**，不能笼统叫只读MCP。Grok云电脑调用MCP/本地HTTP是否可行尚未验证。OKX钱包WS工作流的Input表默认max10、后文CLI备注max200，实际限额以真实服务验证为准。 |
| 反证与旧业务知识 | Why-Solana code/a7_cross_token_links.py、06_hub_map.py、docs/PITFALLS.md；旧qb的sikk_gmgn_token_report.py；Hermes learning/10.md、11.md、12.md；meme多策略历史 | Why的跨Mint金额/钱包/融资时段和Hub检测已是现成研究代码，准入维持review_only；qb已有完整单Mint关键钱包矩阵和报告；Hermes强调角色是推断而非事实，meme强调跨市场状态的多视角。不可因换用Million丢弃这些专业判断。 |

### 实际能力对照与安全状态

- **最大完整产品候选是Million**：它已把Mint发现、钱包装载、持续交易流、资金与候选关系、群体资金流、决策记录、Agent MCP接在一起。先整体试验原生只读API，**不是直接fork/迁移**。附带Node24、NestJS/Prisma/SQLite与Helius配额依赖；含设置EXECUTOR=local即可使用真实密钥签名交易的分支，用户当前阶段绝不启用。项目自述API没有认证，网页可能在本地网络开放；隔离前禁止公网/不受信任网络暴露。
- **HoldTech**：支持holder overlap与结构深扫，但feePayer买家误判、分页截断、硬编码凭证/版权边界是直接运行阻碍，只作为经过隔离审计后选择的业务模块候选。
- **pumpwatch**：完整只读发行/creator历史监测成品支线，较Million更专一；必须先确认v1版本、数据可得时点、去重和链上完整性。
- **OKX**：已有新币筛选、Smart Money、钱包分析、WebSocket监控的命令式工作流。先试只读CLI或经授权的数据API；不安装交易/钱包签名/支付能力，接口真实费用/权限未知。
- **Why-Solana与原qb/Hermes/meme**：承担跨Mint关系、异常钱包反证、库存与可跟随性专业知识，研究脚本不能直接升级为生产监控真值。
- **Grok现有程序**：工程PR#16的src/solana_meme_os仅有fixture-only wallet_batch_monitor（1/5/15分钟窗口）、冻结的raw_tx_adapter、单观察规则monitor、固定来源research与历史GMGN接口。不具备Million级别的发现→订阅→长期事件流→MCP业务系统。与现成系统重复的属于计划中的钱包发现/资金关系/群体统计/接口，**应先停止开发同类模块**。保留M01的事前时点、覆盖缺失、群体成员变化指标及C02/C05独立正常反例作为本项目专业差异。

### 执行证据及不可伪称的运行结果

**已实跑的只是本地已有旧项目离线样本**：容器内用户历史文件m01_proto_offline_20261031.zip在隔离目录解压，运行 PYTHONPATH=src python -m unittest discover -s tests -q，14 tests in 0.840s, OK。**不是第三方Million/OKX/pumpwatch运行，也不是当前GitHub全部71项测试本轮重跑。**

第三方成品本轮均未实际启动：此环境Node v22.16.0，但Million明确要求Node24；curl GitHub显示DNS解析失败，无法下载/安装依赖；未提供Helius配额或指定Mint作为真实外部核查对象；HoldTech另有泄露密钥风险；OKX服务须先核验费用/授权。故当前证据级别仅为SOURCE_IMPLEMENTATION_READ/PRODUCT_RUNTIME_UNVERIFIED，不得把网页截图、README、自述胜率或仓库CI当本地完成。

**新增安全发现（源码级）**：Million apps/api/src/trading/trading.service.ts 的 onModuleInit() 在启动时设置每5秒tick；openFromOpportunity会在达标机会发生时按executor模式建立仓位，默认是PAPER。**不设置EXECUTOR=local只能防止真实密钥签名，不代表整个程序没有后台交易模拟/SQLite写入或行情API消耗**。下一轮严格只读验收必须先审计启动副作用，优先无外网、空白数据库和健康查询；在没有纯只读运行保障前，不得将“默认paper”当作“严格只读安全”。

**下一项唯一有价值的工作**：在可联网、Node24、隔离且不暴露端口的环境，以Million成品为整体只读候选，不启用EXECUTOR=local、不提供签名密钥。先跑它自己的无交易健康检查，针对经允许的公开Mint调用GET /discovery/token/:mint、GET /live/status、GET /live/flows、GET /funding/:address及只读MCP get_flows，保存输入输出/错误/真实可得时点/费用。暂不自动调用钱包导入、订阅、重建owners或更改规则。重点测试**一签名两被观察钱包**、缺失历史、空区块/v1、公共Hub、CPI/转仓非成交与WS静默。这一项才能判定WHOLE_APP_RUN / WRAP_EXISTING / MODULE_ONLY / REJECT，不能先写新解析器或新Mint监控程序。

### 2026-11-01｜固定 Mint 业务链代码审计：现成功能与不可直接信任的结果

**本轮验收问题**：以一个真实公开 Meme Mint 作为只读请求对象，沿“Mint→关键钱包→追踪交易→资金/群体→不确定性解释”核查现有系统源代码。示例目标选自 Why-Solana [`docs/RESULTATS.md`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/docs/RESULTATS.md) 列出的 Mint `87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump`，**仅为未来同输入对照锚点**；当前没有通过RPC/Helius独立重新读取该Mint，也不能使用作者研究结论当我们的真实观测。

| 业务步骤 | **具体已有代码和可调用接口**（不是自造） | 复用审计结果 / 风险 |
|---|---|---|
| ① Mint 找关键钱包 | Million `GET /api/discovery/token/:mint?minSol=...&mode=recent\|deep` → `discovery.service.ts::find/buyersOf` → Helius `fetchHistory`，排除已知AMM地址、按买入SOL排序、限制候选和预览；OKX `workflow token-research/new-tokens` 可直接提供安全/Holder/SM字段。 | **WHOLE_APP_SOURCE_PRESENT**，但Million的`buyersOf`由Token入账和SOL/稳定币支出近似构造买入，不是对每一笔Swap的协议级执行确证；`fetchHistory`按页截断，不能说找到“全部首买”。需要Helius密钥和实际账单，未调用。 |
| ② 纳入观察与持续交易 | Million `POST /api/wallets/import`、`PUT /api/wallets/:address/subscribe` → `live-feed.service.ts` WebSocket/Webhook→`GET /api/live/events`/`status`。OKX `workflows/wallet-monitor-ws.md` 已有 `onchainos ws start/poll/list`。 | **WORKFLOW_SOURCE_PRESENT**：Million常规WS只关注一组订阅钱包；`HELIUS_API_KEY`缺失则不连接。Webhook遍历命中钱包，但因`LiveEvent.signature @unique`、`if(existing)break`和`break // first touching wallet claims it`，**同一签名涉及多个被追踪钱包时只保留一个钱包视角**。对C02同Tx参与人数/同步执行是**关键阻断**；不可把它的event计数当成真实多钱包数。 |
| ③ 群体活动流/候选关联 | Million `GET /api/live/flows?minutes=15` → `flows.service.ts` 汇总已保存的 buy/sell、wallet、ownerId、SOL；`GET /api/funding/:address` → 真实SOL转账对手；`POST /api/owners/rebuild` → 资金/fee-payer候选边+coentry参考边+hub排除。HoldTech `/api/deep-scan`、`/api/holder-overlap` 提供同Slot和持有者交集。 | **BUSINESS_ANALYSIS_SOURCE_PRESENT**：Million已主动禁止`coentry`作为union-find桥；但`funding/feepayer`边仍是启发式，`ownerId`重建不稳定，不能叫verified same controller。Million `orchestratedDeltas`还会在fee payer下关联外部executor资产变动，需核验真实Token Account owner。 |
| ④ 连续窗口/真正“没有活动” | Million `live-feed.service.ts` 保留`LiveEvent`最多**15分钟**或**5000行**，每5分钟清理；`flows`聚合最近窗口。Grok现有`wallet_batch_monitor.py`产生1/5/15分钟换人、增减、暂停候选并保留`source_refs`、`data_status`。 | Million的feed是**展示窗口，不是历史审计记录**；没有当前可核实的按slot完整采集水位，无法对C05证明“有机会但未交易”。C02应保留原始逐钱包事件与历史as-of cohort。现有M01对此有独有的研究合同，但只支持离线标准化fixture，不能宣称已接Million。 |
| ⑤ 可解释只读输出/AI接口 | Million `GET /api/opportunities/decisions`、`/api/live/flows`、`/api/wallets/cohorts`和`packages/million-mcp`14个工具；`.claude/skills`有命令式说明。pumpwatch `code/{pump_watch,outcome_tracker,creator_reputation}.py` 提供发行事件+SQLite持续记录，Why-Solana研究脚本提供资金图与反例。 | **PRESENT_WITH_SCOPE_GAPS**：Million决策日志解释的是**交易规则/纸面决策**，不自动具备本项目要求的资金控制、正常反例、来源可得时间的完整专家解释。MCP中混有`update_rules/import_wallets/set_wallet_subscription`等状态修改工具，不能宣称默认是只读接口；应使用只读方法白名单。 |

**特定竞品问题与部署边界，已核实源码**：

- **Million安全/运行**：[AGENTS.md](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/AGENTS.md)和[部署指南](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/docs/GUIDE.md)要求Node24、Helius Key；本审计容器仅Node22且没有Github下载网络/Helius密钥，无法运行完整成品或测试Grok云电脑。其HTTP API**无身份认证**、Web前端对局域网开放；绝不直接公网暴露。真实交易仅在`EXECUTOR=local`选择，但默认Paper Executor仍会自动产生**模拟交易/资金状态**，所以默认paper≠严格只读；本项目目标为严格只读，不能未经隔离直接启动Agent或MCP。未经批准不得支出API额度。
- **Million事件内容**：`apps/api/prisma/schema.prisma::LiveEvent`只保存`wallet,signature,ts,kind,mint,sol,usd,createdAt`，缺少完整Token Account owner/authority、instruction path、抓取覆盖证明，`createdAt`也不能自动等同可交易者当时真实取得时点；`private processTx`以净Token变动、SOL变动近似买卖。能复用**持续数据流和看板**，但原始事件并不能原样作为C02/C05真值。
- **HoldTech**：[holder-overlap/route.ts](https://github.com/co-numina/holdtech/blob/a75e214bf1ee0a8803eb7d93336be98c481c2db9/app/api/holder-overlap/route.ts)底层`getHolders`虽能分页，上层实际调用`getHolders(m, 200)`——**每币至多200个Token账户持有人**、最多展示50个重合钱包；交集百分比不能冒充所有持有者。deep-scan将`SWAP/TRANSFER/UNKNOWN`合并为买方群候选、用`feePayer`识别买家；`getTransaction`还限制v0。源码含疑似硬编码第三方密钥，**不复制/使用/复述密钥值**，严禁直接运行原样或导出其配置。
- **OKX**：[wallet-monitor-ws.md](https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/workflows/wallet-monitor-ws.md)已有WS会话操作命令；CLI字段`--wallet-addresses`可接受较多地址，但该业务workflow表中另列默认Max10，实际服务配额/计费/功能要用账户环境另核。不安装全套钱包、支付或交易技能，不用“read-only wallet monitor”暗中启动有付款授权的操作。
- **pumpwatch**：[pump_watch.py](https://github.com/cinder-security/pumpwatch/blob/156a91ab63740ab0ce8700434ff33844d00de519/code/pump_watch.py)内有429退避/重试与并发控制；`outcome_tracker.py`按币龄分级检查后续状态；`creator_reputation.py`将发行历史保存在SQLite。它是**单独的新币/发行者监控成品**，不等于跨钱包群体系统；需要RPC HTTP/WS才能运行真实监测。
- **Helius实际成本**：Million `crawler.service.ts`按内部常量给Enhanced调用记账，但官方[费用/积分页](https://www.helius.dev/pricing)说明积分规则按API种类和产品更新；另有[Helius开源文档](https://github.com/helius-labs/core-ai/blob/main/helius-plugin/skills/build/references/enhanced-transactions.md)给出更高的Enhanced调用示例积分。**内部预估与现行供应商计费须独立对账，不能据README宣称免费持续监控**。本轮未调用付费接口。

**本轮实际执行的隔离测试（本仓库旧原型，不是外部成品）**：从原已生成`/mnt/data/m01_proto_offline_20261031.zip`释放到随机`/tmp`目录，不联网执行`PYTHONPATH=src python3 -m unittest discover -s tests`：**14项通过**；另用自带`fixtures/wallet-batches-demo.json`执行M01 CLI，输出`FIXTURE_RESEARCH_ONLY`、`no_trading=true`；1分钟窗口产生3个示例（买家增/量减、全换员、短时停顿）候选，5/15分钟无该类型候选。**它是旧归档快照的14项测试，不是当前PR#16包含的71项最新测试，也不是任何真实Mint或Million的运行证明。**没有执行外部应用或调用RPC。

**成品复用决定（本轮）**：**`MILLION=WHOLE_APP_REFERENCE_FIRST; READ_ONLY_RUN_BLOCKED`**（有完整源码和端点、尚未可安全运行；严格只读与多钱包同Tx归属未满足）；**`HOLDTECH=SELECTIVE_BUSINESS_REUSE_WITH_SECURITY_HOLD`**；**`PUMPWATCH=READY_TO_EVALUATE_STANDALONE_READONLY_WORKFLOW`**；**`OKX=EXISTING_READONLY_WORKFLOW_UNVERIFIED`**；**`WHY-SOLANA=REVIEW_ONLY`**。不要将这些标签解读为已安装/取得最新数据或验证统计正确。

**只需做的下一项真实交付**：在可联网、可隔离且有明确可用只读数据额度的运行环境，**先做Million原生能力端到端只读验收**，输入上述固定Mint，返回原生`discovery`、钱包`funding`、`live/status`、`live/flows`、候选关系与来源/截断状态；事先确保交易模块不能签名、外部API不对公网开放且模拟执行副作用隔离。对照OKX现成WS及HoldTech同Mint接口。**如果缺乏这些前提，停止在源码审查结果处，不构建另一个模拟的完整系统来冒充验收。** 先判断已有功能能否按需组合，再考虑薄接口或必要业务增量。
 

## 1. 本轮已审外部来源与固定版本

| 参考项目与源码版本 | 核查范围 | 复用/许可边界 |
|---|---|---|
| [HoldTech](https://github.com/co-numina/holdtech/tree/a75e214bf1ee0a8803eb7d93336be98c481c2db9) | `README.md`、`SPEC.md`、`app/api/*`目录、`analyze/deep-scan/holder-overlap/bundler-feed/smart-money/ai-verdict/deployer-profile` 部分函数、`extension/manifest.json`、`package.json` | README 末尾自述 MIT，根目录未发现常规 LICENSE 文件，直接复制前核对授权条款。部分源码出现疑似硬编码第三方访问凭证（**没有保存、使用或重述其值**）；禁止原样运行、提交任何凭证或复用配置。部分功能只是 SPEC/README 的计划。 |
| [GMGN Skills](https://github.com/GMGNAI/gmgn-skills/tree/6a04e1f00b5463cfc965e41003ca0c7c2db5b69f) | `skills/gmgn-wallet-analysis`、`wallet-score`、`wallet-style`、`src/commands/token.ts`、目录与说明 | 项目 MIT；业务工作流知识可以研究，GMGN API/CLI需凭证，部分能力涉及交易与密钥，**不安装、不调用付费或下单入口**。对技能中的指令不自动执行。 |
| [FnZero Python DEX parser](https://github.com/0xfnzero/sol-parser-sdk-python/tree/cffb6c808c9b7975fc83428c0613fb4c3fa173b5) + [Rust核心](https://github.com/0xfnzero/sol-parser-sdk/tree/e3e8d6620e2a128c71d5c37cde219a38d438c73e) | README、Python `examples/parse_tx_by_signature.py` 入口声明、Rust `Cargo.toml` 与协议支持矩阵；尚未执行 | Rust项目含 MIT LICENSE；Python仓库 README 声称 MIT，需确认发行包许可。Python v0.10.0 声称覆盖 PumpFun/PumpSwap/Raydium/Meteora/Orca；兼容和准确率未在本项目实测。**只选解析仓库，不引入同作者的交易签名SDK。** |
| [pumpwatch](https://github.com/cinder-security/pumpwatch/tree/156a91ab63740ab0ce8700434ff33844d00de519) | README、`code/creator_reputation.py`、`code/`模块列表 | 代码 MIT、文章/数据 CC BY 4.0；只读发行检测器、历史频率SQLite模块可直接作为参考候选，但需数据源、版本和实际测试。作者报告的样本统计不是本项目独立复现。 |
| [MadeOnSol SDK](https://github.com/MadeOnSol/madeonsol-sdk/tree/eb1a4cc2915cbb725364e2139e9fb908370911d4) | `src/index.ts` wallet/bundle/sniper/KOL/持仓字段及 README | SDK MIT，但其在线分类模型、历史数据和付费接口不随SDK源码开放；**接口声明≠可本地复制识别算法**。用于比较输入输出、覆盖声明和UNKNOWN语义。 |
| 现有项目：`sunshihao001/grok` Draft PR #14/#16 | `gpt-meme-progress-current.md`、`p3-m01-raw-adapter-contract.md` | M01仅fixture-only、有限转账语义；无协议级真实BUY/SELL和实时源。旧qb-/Hermes/meme-是必须持续对照的业务知识，不用外部项目替代其历史。 |

## 2. HoldTech 功能级清点：哪些是真实源码，哪些仅为产品设计

所有路径相对于 `co-numina/holdtech`。**有路由 ≠ 能独立部署运行 ≠ 标签准确**。

| 功能 | 源码路径/证据 | 现有项目关联 | 当前选择与原因 |
|---|---|---|---|
| Top holders + 单钱包画像 | `app/api/analyze/route.ts` | qb关键钱包，D04/D06 | **REFER+ADAPT**：可参考采集→去pool→钱包指标→摘要的结构；不要复刻“最大持仓必是LP”、钱包历史初始时间=创建年龄、持币时长=钱包年龄的推断 |
| Same-slot聚集/Bundler候选 | `app/api/deep-scan/route.ts detectBundles` | P3-M01、D07/C02 | **REFER+CORRECT**：原代码把SWAP/TRANSFER/UNKNOWN混合，并把fee payer当buyer；只能输出 `SAME_SLOT_COHORT`，不可宣称Jito Bundle/同控 |
| 初步资金同源 | `deep-scan/route.ts traceFundingSource` | D05、B02/B04 | **REFER+CORRECT**：原代码仅看很小的签名窗口、用账户SOL净增与fee payer猜融资方；应先识别真实System/Token转账账户和公共HUB |
| Top5/10/20、Gini、HHI | `deep-scan/route.ts computeConcentration` | D06 | **ADAPT_SIMPLE**：统计公式可据来源与正确分母独立计算；须区分holder样本/Token Account owner/LP、部分供应；不直接把分数视为实控 |
| Mint买入时序 | `deep-scan/route.ts extractBuyTimeline` | P3-M01、D07 | **REFER+CORRECT**：源码同样以fee payer和任意交互替代已确认BUY；需经协议级Swap后才能计算Sniper/首买 |
| 资金余额等级 | `deep-scan/route.ts computeSolDistribution` | D04/D05 | **ADAPT_SIMPLE**：可直接定义确定性分箱，当前资产余额不是历史风险本金 |
| 2–5 Mint持有人交集 | `app/api/holder-overlap/route.ts` | D07/B04、C02 | **ADAPT_SIMPLE**：pairwise交集、比例、几何平均算法简单；当前入口只取每Mint最多200个holders且可截断，不可称完整群体/同控。需同一时间快照、排除公共持仓与明确采样分母 |
| Smart Money当前持仓 | `app/api/smart-money/route.ts` | qb、D04 | **REFER_ONLY**：当前按静态预设地址表匹配持仓，不是链上自动“聪明钱发现”；需自行维护来源、标签和更新时点 |
| Dev/Deployer历史 | `app/api/deployer-profile/route.ts` | D02/D04、B04 | **INSPECT_NEXT**：源码存在历史发行分析和token状态接口，须核查是否依赖不稳定外部接口、创建者识别与样本覆盖 |
| 同群体实时跟踪（bundler feed） | `app/api/bundler-feed/route.ts` | D07、Grok Monitor | **REFER+CORRECT**：每次最多25个钱包，每钱包取最近2笔SWAP；无swap时用Token Transfer猜BUY/SELL，不能作为真实经济事件源 |
| 评分与AI解释 | `app/api/ai-verdict/route.ts` | D11/D12 | **REFER_ONLY**：可借鉴“先确定性指标、后解释报告”，不能抄其Fresh阈值、未知分数或“Sybil必然”措辞；不让LLM评分成为链上事实 |
| 钱包/Holder数量 | `app/api/holder-count/route.ts` | D06 | **PATH_FOUND_AUDIT_PENDING**：尚未细审算法与成本 |
| Token行情/简介 | `app/api/token-info/route.ts`、`token-prices/route.ts` | D02/D03 | **PATH_FOUND_AUDIT_PENDING**：可考虑既有只读源；不是当前研究优先项，不把K线作为核心 |
| 交易热榜扫描 | `app/api/trending-scan/route.ts`、`trending-refresh/route.ts`、`scripts/trending-refresh.mjs` | D02/D07 | **SECURITY_HOLD**：需要辨别实际运行与规格计划；脚本有硬编码访问凭证，不应运行或照搬 |
| 浏览器叠加评分 | `extension/manifest.json` 和 `extension/src` | 未来展示/前端 | **PARK**：ManifestV3已存在，属于界面层，不是当前M01业务依赖，不必引入前端栈 |
| 计划中的watchlist/持续告警/Token门槛 | `SPEC.md`、README “Coming soon” | P5/Grok运行 | **DESIGN_REFERENCE_ONLY**：规格声明不能当作已实现；实时/历史监控需单独检查代码、部署、状态与数据成本 |
| 管理、收费与权益验证 | `middleware.ts`、`check-tier`、`SPEC.md` | 非核心 | **REJECT_FOR_NOW**：不迁移付费Token门槛、登录签名、前端钱包连接；当前项目只读、无钱包与支付 |

### HoldTech 的关键质量/安全问题（不要复制错误实现）

- README写“MIT”，但审阅的仓库根目录无常规LICENSE文件；GitHub Docs说明README可声明许可，完整许可证文件是最佳实践。**在实际复制代码前需核对授权与署名义务**；仅参考算法思想和业务流程不等于必须整库复制。
- 多个路由/脚本有疑似硬编码RPC/Redis访问凭证；本账本不记录密钥值、不使用现成服务额度。实际部署需删除源码常量、换项目自有环境配置并安全审核；这是 **HARD_BLOCK_FOR_CLONE**。
- `analyze` 把余额最大者当池账户，错误排除真正鲸鱼；`holdDurationDays`实际上复用`walletAgeDays`；`firstTxTime`基于被分页截断的历史签名，可能是假“Fresh”。
- `holder-overlap` 只取部分持有人快照且阈值直接称“coordination”；需要完整性与对照，不可把地址交集当私人协作概率。
- `bundler-feed` 在没有经核验Swap时将Token Transfer猜作买卖，违反现有M01“未支持应UNKNOWN”的正确约束。
- `SPEC.md` 给出的功能、定价/Token门槛/处理能力只是设计与商业说明；不能与可运行路由或实际用户体验混为一谈。

## 3. 跨项目可复用组件：优先采用哪条现实路径？

| 项目/模块 | 解决现有哪个缺口 | 最值得复用的具体内容 | 依赖/阻碍 | 下一步可执行动作 |
|---|---|---|---|---|
| FnZero `sol-parser-sdk-python` | P3-M01目前不会输出Pump.fun BUY/SELL | Python现成DEX事件与按交易签名RPC解析示例、已列明的协议适配 | 需兼容v1、指令字段、owner、CPI、Token-2022和原始事件契约；依赖审核和实际测试 | **P0**：固定版本、在独立只读环境用同一组匿名fixture比较原始适配器/SDK/人工答案；不先连接真实收费端点或修改M01原入口 |
| Solana官方 `transaction-introspection` | v1、账户索引、CPI层级的通用解析 | 账户/指令树与版本语义 | JS实现，不直接输出业务级经济BUY/SELL | **P0并行**：作为结构级真值核查的对照，不必在Python里重写全套通用解析 |
| pumpwatch `creator_reputation.py` | B04发行者重复活动/Dev历史 | SQLite WAL、唯一Mint记录、历史24h/7d发行频率、结果状态 | 数据采集与creator语义仍需审核；阈值不代表意图或盈利 | **P1**：只读离线启动样本/fixtures，对比旧qb与D04；无需引入整套pipeline |
| HoldTech holder-overlap + concentration | B04跨Mint关联、D06持仓 | 集合交集/HHI/Gini与报表字段 | 本源采样、身份排除、同一时点和版权/源码安全 | **P1**：在已有验证的标准化事件或holder快照上做小型确定性计算，不移植Next.js |
| GMGN Wallet Style/Analysis/Score | D04钱包类型、D08/D09可跟随性 | 多窗口行为风格、历史盈利与可复制性分开、样本质量反例、开发者角色判断 | 依赖付费API/令牌、部分Skill还涉及交易指令 | **K1知识复用优先**：吸收独立可解释规则、字段定义和负例；不调用需要充值的服务、不迁移自动交易 |
| MadeOnSol SDK钱包/Bundle覆盖 | 钱包标签与库存解释 | `label_coverage`、`evidence_horizon`、`bundle_kind`、`held_ratio`、`transfer_delta`、as_of | 商业后台数据/分类器非开源，服务条件须单审 | **K1对照**：把状态和不确定性字段映射到现有D04/D06知识，非本地算法现成能力 |
| HoldTech UI/extension | 将链上研判展示给用户 | token详情、持有人结构、相似Mint、浏览器提示的交互体验 | Next/React部署与浏览器权限/安全，当前无稳定源 | **PARK**：先保留交互与显示知识；核心监控可靠后再讨论 |
| 旧qb-/Hermes/meme- | 防止外部项目使专业知识丢失 | 关键钱包矩阵、同源/筹码/FCZ/反证与Meme业务脉络 | 旧GMGN数据费用、旧方法误判与历史状态 | **PERMANENT_REVIEW**：每轮涉及相同业务对象即回访对应函数/文件；不直接恢复旧运行时 |

**不能把一张能力表直接视为系统已拥有功能。** 只有 `ADAPTER_TESTED`（固定版本/相同输入对账），之后 `READ_ONLY_DATA_VERIFIED`（可复核数据/覆盖），才更新工程已实现字段；长期保留 `PARKED_KNOWLEDGE` 仍是有价值的研究资产。

## 4. 跨源能力发现与组合的“认知思维”运行法

1. **目标倒推（CAPABILITY NEED）**：从一个真实Meme任务反问“结果应该能做什么”，如“批量新钱包是否为一组操作者”；把任务拆成观察/关系/库存/解释，先查询本账本/旧qb-/Hermes。
2. **发现（SEARCH）**：按缺失能力搜索多个真实项目与行业工具；必须读源码函数、例子、tests、issues和失败案例。每个有用模块都记录URI、commit、真实输入输出，而不只保存项目名。
3. **组合（COMPOSE）**：优先直接调用已许可只读接口、封装成熟开源模块；数据串联可为“FnZero已解析Swap → M01钱包窗口 → HoldTech式跨Mint交集 → pumpwatch式Dev历史 → 旧Hermes筹码状态分析”。这里是**拟议能力组合，不是已存在的执行管道**。
4. **审查（CHALLENGE）**：审核许可、凭证安全、外部计费/权限、版本、覆盖、误判和样本选择；不能因第三方产品有UI就默认为正确。若上游缺字段应保留UNKNOWN而非凭空补全。
5. **最小工程（BUILD MINIMUM GLUE）**：只编写不可直接复用的适配、事件格式和可核验测试；不为一项已成熟的DEX解析重写多协议引擎，不为两组交集引入大平台。
6. **验收与持续学习（COMPARE + RETAIN）**：用相同输入比较当前与候选方案，记录解析差异/覆盖/资源/许可结果；决定 `USE`/`WRAP`/`ADAPT`/`REFERENCE`/`PARK`/`REJECT`，之后遇到相同能力再次查询，而不是重新搜一遍。

**一次最小合成示例**：输入两枚Mint、历史时点冻结的持有人集合、经核验的BUY/SELL和已记录的转账边 → 计算共同钱包以及每个钱包的融资/库存/最早可见时间 → 排除公共服务商并输出“重复活动候选+可核查证据”，不能直接输出同控/庄家或盈利。M01现没有真实协议BUY/SELL/完整holder集合，故该示例目前是可组合目标，不是已部署能力。

## 5. 已完成与还没有完成的事情

- **已完成（本轮）**：对HoldTech根目录、API路由列表、部分实际函数和扩展声明完成源审；与现有P3-M01字段契约比较；检索并阅读FnZero Python/Rust、pumpwatch、GMGN Skills、MadeOnSol的部分具体实现与来源边界；形成可回访、可判定的功能台账。
- **未完成**：未逐行审查HoldTech所有路由、未跑HoldTech或FnZero/GMGN的代码、未确认HoldTech README许可声明的完整法律适用性、未联网调用任何收费接口、未生成真实市场标签/盈利结果、未修改生产监控。
- **当前方向判断**：`PIVOT_METHOD_KEEP_GOAL`：保留P3-M01的保守归一化输出与监控需求，但把“自行支持所有DEX协议”从默认路线改为“先比较/封装成熟SDK”；并行以HoldTech、pumpwatch等已有工具启发行为分析，先保留知识和可运行依赖证据。
- **历史组件级实验候选（已被2026-11-01上方成品复用审计取代，不再是当前唯一主任务）**：在隔离、无签名/无API付费的条件下，固定FnZero Python解析器版本和现有M01官方fixture，核对是否能够正确产生目标Mint/owner/交易类型/报价量/指令来源以及UNKNOWN，记录差异；只在审查和对照通过后考虑新增可选适配器。可并行只读检查HoldTech剩余路由、测试与源许可证，不等其全部读完才做上述实验。

## 6. 参考资产长期保留合同

每个模块用 **`capability_id` + `source_repo@sha/path` + `source_status` + `inputs/outputs` + `data_cost/permissions` + `license/security` + `known_misread` + `grok_gap` + `reuse_decision` + `next_trigger`** 来检索。当前文本表即这份合同的人类可读版本；需要让Grok按字段调用时再做JSON索引，不提前制造框架或Bot。

研究阶段结束时若实际新发现可改变某模块的复用结论，修订该行，并同步当前唯一恢复点；若暂时不能用，保留理由、来源与触发条件，不能丢掉已经发现的项目。**源码/数据/测试是不同资产**：仓库可访问不表示许可证允许复制全部内容；MIT代码复制仍需保留原版权许可；云服务可能单独收费、API许可与原仓库代码许可也可能不同。


## 2026-11-01｜P3-M01 按已有台账纠偏：禁止继续自研底层解析（AMEND）

**修正的错误**：PR #16 `raw_tx_adapter.py` 在此前已确认成熟解析器候选之后，仍持续自写Base58、账户索引、v0/v1检查、CPI与部分SPL/Token-2022解码，并以增加离线单测证明方向。它的fail-closed测试有价值，但这不能证明值得继续建设另一套协议解析器。当前项目本来就有 **FnZero Python为P0候选**的审核结论，应先落实该方案，而不是重新做同样的检索和实现。模块现标为 **LEGACY_FIXTURE_COMPARATOR**，冻结底层功能扩写；不得删失原单测或声称已迁移。

**本轮新增的实源码核查（固定源码版本）**：

| 现成实现 | 实际读到的代码/组件 | 跟本项目的具体映射 | 限制与下一步 |
|---|---|---|---|
| [FnZero Python v0.10.0](https://github.com/0xfnzero/sol-parser-sdk-python/tree/cffb6c808c9b7975fc83428c0613fb4c3fa173b5)（维持台账P0） | `sol_parser/rpc_parser.py` 已有 `parse_rpc_transaction`；`examples/parse_tx_by_signature.py` 使用结构化RPC并设置 `maxSupportedTransactionVersion=1`；`docs/cross-language-sync.md` 按 `parse_status` 分开 `ExecutionConfirmed` / `InstructionDecoded` / `Unresolved`；区分指令限额与成交事实 | Python最少改动，可取成熟的Pump.fun/多DEX事件输入并做现有M01 m01.v1映射（须验证原始事件字段和可靠性） | 本轮**源码审阅，未安装/运行**，README宣称MIT但仓库根目录未查到LICENSE文件，直接复用前核对分发许可；不引入同作者交易SDK |
| [Carbon（Rust）](https://github.com/sevenlabs-hq/carbon/tree/134647d8071675bb316f55c18511e961d4d0361b)（P0对照候选） | `decoders/pumpfun-decoder/src/instructions/buy.rs`/`sell.rs`、`events/trade_event.rs`，以及PumpSwap、Raydium、Meteora、Token-2022等现成解码器；`datasources/stream-message-datasource` 可接历史回放；`examples/transaction-crawler-rpc`/ `versioned-decoders` 有成熟管线和版本切换示例 | 可代替未来自己维护多DEX解码；特别适合已有索引/流式需求；官方代码生成并有实例 | MIT许可证已读；**未安装/跑测试**；Rust与Python M01的连接有成本，先以同样输入对比FnZero，不能因解码器数量多就迁移整栈 |
| [Solana官方transaction-introspection](https://solana.com/docs/core/transactions/transaction-introspection) | `decodeTransactionFromRpcResponse`+`walkInstructions` 已解决账户/ALT、outer+inner CPI、legacy/v0/v1；生成的Program client再解析Token语义 | 结构级权威、用于第三方库失败原因核验 | 不能自动推导已执行买卖经济结果；JS调用是否必要待FnZero/Carbon同样样本比较 |

**历史FnZero-only实验方案（仅当成品级对照确实缺少协议解析时才启动）**：保持`wallet_batch_monitor.py`原逻辑与fixture不变，在隔离无密钥环境以同一组已知Solana文档RPC样本及FnZero自带经核查的DEX正例，对照锁定版本FnZero（必要时对比Carbon）输出的指令、BUY/SELL、mint、owner、实际quote成交、`parse_status`、CPI位置、UNKNOWN；审计包/许可证、开发依赖、执行开销。只有SDK已经能稳定输出所需字段时，才写最薄的“供应商事件→既有M01标准事件”映射；不准重写DEX解析、无需三套混合框架。

**状态**：`SOURCE_CODE_INSPECTED` / `IMPLEMENTATION_FROZEN`；**不是** `ADAPTER_TESTED` 或 `READ_ONLY_DATA_VERIFIED`。已有单测仍属于本项目自写Legacy基线。方向改为`PIVOT_METHOD_KEEP_GOAL`，不更改P3研究目标与C02/C05优先级；后续该台账为唯一复用判定入口，不另建框架。

## 2026-11-01｜源码级扩查与隔离对照结果（增补，不替代前文）

### 本轮实际审查范围和执行证据

- **外部成品**：FnZero Python `sol_parser/rpc_parser.py`、`examples/parse_tx_by_signature.py`、`tests/test_pump_execution.py`、`tests/test_pump_upgrade_mainnet.py` 与固定主网回归材料；HoldTech `deep-scan/analyze/holder-overlap/bundler-feed/smart-money/deployer-profile` 的关键源码；pumpwatch `creator_reputation.py`、`pump_watch.py`、`outcome_tracker.py`；此外核对 Carbon 官方主仓、Kelows/million discovery/copyability/funding 子模块、OKX read-only skill，以及 pumpkit/LICENSE。
- **工程基线**：PR #16 最新提交 `3ee17255f4c849d6be4ede93e6ee7e516a068de1`；`raw_tx_adapter.py` 已在文件头声明 `LEGACY FIXTURE COMPARATOR ONLY`，源码继续无真实BUY/SELL；该 SHA 对应的远程 `monitor-tests` CI 为 `completed/success`，**CI并非本轮本地运行、也未包含FnZero对照**。
- **受限**：当前隔离终端 `git ls-remote` 无法解析 github.com，`sol_parser`、`solders`、`solana` 均未安装；无法克隆依赖、执行真实FnZero解析或复跑整个M01。因此本轮仍**未完成FnZero↔M01实际输出一致性测试**，禁止将 `SOURCE_COMPATIBILITY_REVIEW` 写作 `ADAPTER_TESTED`。
- **实际执行的局部负例**：在本地Node.js标准环境以HoldTech公开 `deep-scan/route.ts` 的两个关键算法逻辑为依据，手工独立复现`detectBundles`及`extractBuyTimeline`的条件和迭代；四项隔离断言**全部通过**（这是“源逻辑复现”，**不是运行HoldTech项目原始TS代码**）。场景：(1) 同Slot三个普通TRANSFER仍输出1个“bundle”；(2) 三个TRANSFER交互被归入“首买”时间线；(3) 三个真实买家共享一个fee payer时输出0个潜在bundle；(4) 三个普通同Slot SWAP会被输出bundle，不能因此认定有Jito原子Bundle。无RPC、密钥或交易。独立脚本和结果仅存于本轮交付文件，未接入监控。
- **FnZero真实差异**：`examples/parse_tx_by_signature.py` 使用 `maxSupportedTransactionVersion:1`，`sol_parser/rpc_parser.py` 的 `parse_transaction_from_rpc()` 仍向客户端传 `max_supported_transaction_version=0`。其`rpc_get_transaction_result_dict_to_response`在 `meta` 缺失时构造默认空meta，而M01在关键状态未知时拒绝完整解释。需先选正确RPC入口并保留完整性/失败状态，不因SDK返回空事件就写“无交易”。
- **许可证和风险更新**：FnZero **Python**仓库README声称MIT，但固定版本仓库根目录无 `LICENSE`，且 `pyproject.toml` 未列license；与有实际MIT `LICENSE`的FnZero Rust项目不可混为一谈，**暂不复制Python源码，接入前确认授权**。Carbon `sevenlabs-hq/carbon` 的主仓有MIT `LICENSE`，提供Pump.fun/PumpSwap/Raydium/Meteora等解码器，但Rust运行时需评估与当前Python的桥接。 `nirholas/pumpkit` 虽有已实现的Telegram/launch/tracker API与部署说明，其仓库 `LICENSE` 明确声明所有权利保留、未授权不得复制/修改：**KNOWLEDGE_ONLY，禁止移植其源码**。
- **现有项目二次复用**：Kelows/million（MIT） `apps/api/src/discovery/discovery.service.ts` 有从币发现大额交易者、过滤公共基础设施的现成逻辑；`funding/funding.service.ts` 使用 `nativeTransfers.fromUserAccount/toUserAccount` 和截断标记（比HoldTech用feePayer猜资金来源更合理，但仍会遇公共账户）；`copyability/copyability.service.ts` 使用滞后一个分钟周期的纸面可跟随性比较，其K线/分钟价格代理不符合本项目当前不依赖K线的主体路线，只作为方法及缺陷知识。禁止从同仓`trading`引入签名/自动交易。
- **pumpwatch**：`creator_reputation.py` 用SQLite维护mint/creator/24h/7d频次，`outcome_tracker.py` 分年龄区间随访，`pump_watch.py`包括限并发、RPC重试与WS失败恢复；已实现业务逻辑但未本轮实际运行，适合按需复用“已知功能+防故障方法”，不能直接将作者标签阈值转为真实操控结论。

### 可复用决策（当前真实状态）

| 候选功能 | 当前决策 | 转换所需的最小工作 | 转换阻碍 |
|---|---|---|---|
| FnZero Python RPC/DEX解析 | `EVALUATE_FIRST`，尚非`WRAP_READY` | 确定源码许可、选 `parse_rpc_transaction` 入口、与M01相同官方/真实交易逐项核对owner/mint/quote/side/fees/CPI/v1/UNKNOWN | 终端无法取包；Python库无根LICENSE；部分RPC helper版本参数不同 |
| Carbon现成协议解码器 | `ALTERNATIVE_MIT` | 指定一个Rust decoder和read-only边界，离线基准对照；只在FnZero不可用或质量不足时投入桥接 | 语言栈和集成开销 |
| HoldTech持有人交集/集中度 | `ADAPT_SMALL` | 在已知完整性与同一时点的holder集合上复用纯统计；公共池/托管排除 | 部分源码归因有误，许可未清晰落盘 |
| HoldTech Bundler/首买/资金源 | `REFERENCE_ONLY_CORRECT` | 保留“同Slot候选/融资网络”功能意图；真正买卖需真实Swap，资金源需真实转账路径 | 已执行4个对抗负例，不能原样迁移 |
| pumpwatch发行者/分龄随访 | `POTENTIAL_MODULE` | 只读SQLite历史记录和可靠状态恢复，复查mint/creator准确性后再接M01 | 数据源、签名时点、观测窗口 |
| Kelows/million发现/资金模块 | `EXAMINE_AS_WHOLE_FLOW` | 比较已有qb关键钱包矩阵→million发现/筛选→资金trace→监测队列的一条完整链 | 依赖Helius/Nest/Prisma；执行交易代码必须彻底隔离 |
| pumpkit监控/Telegram布局 | `KNOWLEDGE_ONLY_LICENSE_BLOCK` | 可研究事件流、提醒设计、健康检查等公开事实 | 许可证禁止未经许可复制/修改 |

**整体项目优先**：`WHOLE_APP_FIRST / COMPONENTS_IF_NEEDED`。先验收已有百万级成品结构的 Million 原生只读 Mint→钱包发现→监控→资金/群体→解释业务链与 OKX 可行性。只有业务链缺某项关键事实时才进入 P3-M01 组件选择；FnZero/Carbon 作为其交易语义的 **候选补强**，并非全局主选系统。现有 M01 保留严格时点和覆盖语义作为对照。当前没有实际新接入第三方功能。

**下次触发**：首先在合法隔离条件满足后完成 Million 整套只读业务流程与 OKX 已成型工作流的同一Mint对照，重点考察一签名多钱包归属/签名副作用和持续覆盖。若其原生Swap与事件语义无法满足D04/D05/M01，再单独复跑FnZero固定版本的 `tests/test_pump_upgrade_mainnet.py` 与M01同一输入比对；先厘清Python许可和v1入口，才考虑最小可选适配器。

## 7. 2026-11-01｜P3-M01现成DEX解析器第二轮审查与离线验证

### 已执行记录与严格边界

- 本轮从 GPT Library 中`/跟单/P3-M01_离线原型_2026-10-31/`恢复 `raw_tx_adapter.py`、`wallet_batch_monitor.py`、两份测试及两份fixture，在`src/solana_meme_os/`与`tests/`恢复原包结构；Python 3.13.5执行 `PYTHONPATH=src python -m unittest discover -s tests -v`，**本地实跑38项、38项通过**。随后实际执行`raw_tx_adapter → wallet_batch_monitor` CLI，输出`FIXTURE_RESEARCH_ONLY`报告，1笔合成Token TRANSFER不被误当BUY/SELL。
- **此测试只证明此前Library快照的38项回归，而非GitHub PR#16当前71项或FnZero任何测试**。当前PR#16头 `3ee17255f4c849d6be4ede93e6ee7e516a068de1` 的远端 `monitor-tests` CI显示success，但未在本地恢复其全部最新文件运行。不能用此宣称SDK接入或真实交易验证。
- 本地环境尝试`git ls-remote`和`pip index versions sol-parser-sdk-python`，DNS无法连接GitHub及包索引。**FnZero运行测试BLOCKED_BY_ENVIRONMENT**，没有安装SDK、没有调用主网RPC/商业API或签名；失败是本轮环境而非SDK功能不正确。
- 独立用三组**合成规则反例**复现HoldTech公开`detectBundles`的筛选条件（同Slot+3个不同fee payer，SWAP/TRANSFER/UNKNOWN均进入），三组都能触发`same_slot`候选。此实验执行的是规则的独立重现，**不是运行HoldTech源码**；证明当前规则未区分真实BUY/普通TRANSFER和UNKNOWN，不能证明真实Jito Bundle或同控。
- 无真实链上样本/同输入的第三方解析结果对照，本轮的最终状态仍是 **SOURCE_AUDITED + LOCAL_BASELINE_TESTED**，不是`SDK_ADAPTER_TESTED`。

### 新增对照候选（保留真正已实现的功能及不能继承的部分）

| 方案 | 固定来源 | 证据核查 | 选择 |
|---|---|---|---|
| FnZero Python `sol-parser-sdk-python` v0.10.0 | [repo@cffb6c8](https://github.com/0xfnzero/sol-parser-sdk-python/tree/cffb6c808c9b7975fc83428c0613fb4c3fa173b5)；`sol_parser/rpc_parser.py`、`examples/parse_tx_by_signature.py`、`tests/test_signed_transaction_replay.py` | `rpc_get_transaction_result_dict_to_response(result)`接收结构化getTransaction；`parse_rpc_transaction`输出`(events,error)`，失败交易返回空事件；示例`maxSupportedTransactionVersion=1`；tests存在签名/ALT/CPI回归。源码此转换路径中的pre/post token balances初始化为空数组，不能直接假定可使用它重建所有钱包余额。README MIT但Python库根目录没有独立`LICENSE`，许可归属/发行包待查。 | **P0 WRAP CANDIDATE / BLOCKED runtime+license**：与Python同语言、最小接口可能最好，但不宣称兼容或已安装 |
| [Go DEX Parser](https://github.com/DefaultPerson/solana-dex-parser-go) | `DefaultPerson/solana-dex-parser-go`，源文件`dex_parser.go`、`example_test.go`、`tests/`、`LICENSE` | 可直接接受RPC JSON、明示v1、Jupiter多跳/汇总、流动性、Pump新币、Bot与tip；有MIT许可证。其默认`TryUnknownDEX`可能依据Transfer启发式解析未知交易，对M01严格UNKNOWN策略存在潜在冲突，复用时必须禁用或单独审计。Go→Python需进程/协议转换成本。 | **P0 ALT / WRAP SERVICE LATER**：更丰富事件和明确许可，但高跨语言成本、未知解析风险 |
| [TypeScript DEX Parser](https://github.com/cxcx-ai/solana-dex-parser) | `cxcx-ai/solana-dex-parser`，源码与`LICENSE` | 已实现的DEX、Jupiter路由、交易/流动性解析候选，有MIT文件。需要JS运行时，与Python项目集成成本。 | **P1 ALT**：Go/Python均不满足时比较；不要三个SDK全接 |
| [Helius Parsed Events/Streams](https://www.helius.dev/blog/parsed-events-and-streams) | 官方2026-09-03发布：解析多种协议的REST/WS接口 | 商业服务，公开说明在付费套餐开放；平台支持不代表我们有额度，字段/覆盖/时间/费用需独立审计。 | **PAID_BENCHMARK_ONLY**：将来有授权/预算时作为独立结果对照，不把它当免费前置 |
| [Solana transaction-introspection](https://solana.com/docs/core/transactions/transaction-introspection) | 官方工具 | 版本/ALT/CPI的链上结构核查，不代替协议级Buy/Sell语义；JS运行时 | **STRUCTURAL_ORACLE**：作为结构事实对照，不重复造账户索引逻辑 |
| [pumpwatch发行探测器](https://github.com/cinder-security/pumpwatch) | `code/pump_watch.py`与`creator_reputation.py`；MIT | 提供只读`logsSubscribe`、错误重试/并发限制/SQLite累积发行画像；但`getTransaction(maxSupportedTransactionVersion=0)`，在支持v1时有明显覆盖风险，需修订/检验；作者论文统计仍非本项目实证 | **P1 REUSE SUBSYSTEM**：只在版本检查后复用探测器/历史模块，不把“观察不见”当“无发行” |
| [HoldTech](https://github.com/co-numina/holdtech) | 前一轮固定SHA`a75e214b`、`app/api/deep-scan/route.ts`与`holder-overlap/route.ts` | 可复用同Slot候选、跨Mint持有人交集、集中度、Dev发行历史的业务流程，但归因弱、采样不完整，含疑似硬编码访问凭证，根目录无常规LICENSE。 | **DESIGN_AND_ALGORITHM_ONLY**：不能整库clone运行或直接把其风险标签当事实 |

### 对接合同与最小胜出标准

- **输入**：同一份结构化`getTransaction`+真实/fixture证据；保留原签名、slot、协议、交易状态、`available_at`（由我们的独立采集器给出，不由blockTime替代）、账户owner及证据完整性。
- **输出桥接（并非已实现）**：第三方`Trade`/DEX`Swap` → 仅在`success+目标Mint方向+真实owner/quote mint/amount+可信指令来源`全部明确时构造M01`BUY/SELL`；其余`UNRESOLVED`。路由多跳不能重复当作多个独立BUY；余额变化/Token Transfer不自动当成交，分离观察到的Token移动与经济成交。M01原始TRANSFER/SOL funding仍独立保留。
- **对照样本**：一个普通转账、一个Pump.fun实际Buy、一个Sell、一个Jupiter多跳、一个CPI、一个失败tx、一个v0 ALT、一个v1、一笔Token-2022费用和一个缺失账户。先核查样本真实性/来源/许可及每类已知结果，不得用制造的预测答案给SDK打分。
- **实际可执行胜出条件**：SDK在相同输入上覆盖高于当前适配器，且关键假阳性为0、真实账户/金额/版本正确、未知显式保留、无需私钥/交易API/不可控付费，依赖/许可与成本可接受。若不满足则停止接入，不因为品牌/README强行复用。

### 与知识及长期方向的关系

这一发现将D01交易解析、D04执行角色、D05资金/Owner归属、D06真实库存、D07时序覆盖和D10采集可靠性直接连接。**新的认知是功能复用必须跨越“第三方业务事件→本项目可审计经济事实”的语义桥，且数据采集完整性是独立于解析准确率的前提。** Yellowstone重放窗口可能有界，流断开后需要检查点和回补，不能依据单次SDK空输出推断某群钱包沉默（与C05一致）。

本轮结论：**CONTINUE REUSE_FIRST**，但FnZero从“已可直接接入”降为“高优先候选、待独立运行+许可核查”；新增Go/TypeScript备选及Helius付费基准，保持不开发万能DEX解析器。

## 2026-11-01｜第一条Mint业务链复用验收：OKX单次报告 vs Million长期监控（新增源码与成本审查）

### 本轮决定：先验证完整业务流程，不让FnZero组件测试取代Mint交付验收

**仍是SOURCE_AUDITED + LOCAL_FIXTURE_BASELINE_TESTED，不是外部成品已部署。** 当前外部源固定版本与历史审计保持：OKX `73904b636a0f022dcc13b6d7a0dd2ed3b3195f25`、Million `c89ad07caaf70773d40b45943e136eadc4f946a5`、HoldTech `a75e214bf1ee0a8803eb7d93336be98c481c2db9`、pumpwatch `156a91ab63740ab0ce8700434ff33844d00de519`、FnZero Python `cffb6c808c9b7975fc83428c0613fb4c3fa173b5`。本轮重访现有文件，没有创建新框架或替换工程代码。

| 用途 | **确实读到的成品代码入口** | 边界与选择 |
|---|---|---|
| **第一版单Mint按需报告** | [OKX `cli/src/commands/workflows/token_research.rs`](https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/cli/src/commands/workflows/token_research.rs)，有真正的 `fetch_and_assemble`、`run`、`assemble`，不只是prompt：token report、holder/cluster/topTrader/signals并行；`protocolId`非空才检索memepump Dev/Bundle/SimilarToken；个别失败保留`null`，核心全失败返回error；源码包含聚合单测。 | **首选 WHOLE_WORKFLOW_VALIDATE**：`onchainos workflow token-research --address <mint> --chain solana`，授权Key和实际响应尚未验收。null≠安全，不直接把标签升级为经济主体。workflow可能触发多条Premium接口而不是一次计费。 |
| **持续追踪和发现** | [Million `discovery.service.ts`](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/discovery/discovery.service.ts)、`live-feed.service.ts`、`flows.service.ts`、`funding.service.ts`、`owners.service.ts`、`schema.prisma` | **SECOND WHOLE_APP_SAFETY_REVIEW**：真实API业务已存在，但Token收到+报价资产流出是买入代理指标；`LiveEvent.signature @unique`且Webhook首个命中后`break`，同签名多钱包观测信息丢失；owners是候选，重建ID可能变化；事件保留很短。**当前不能当完整群体真实证据。** |
| **发行者完整子流程** | [pumpwatch `pump_watch.py`](https://github.com/cinder-security/pumpwatch/blob/156a91ab63740ab0ce8700434ff33844d00de519/code/pump_watch.py) + `outcome_tracker.py` + `creator_reputation.py` | **P1 WHOLE_READ_ONLY_SUBFLOW**：已实现日志订阅/重试/SQLite发行记录；`maxSupportedTransactionVersion=0`可能漏v1。不能把超窗/错版的空输出标成“没有发行”。 |
| **持有人图与功能交互** | [HoldTech `app/api`](https://github.com/co-numina/holdtech/tree/a75e214bf1ee0a8803eb7d93336be98c481c2db9/app/api) 现有分析、holder-overlap、deep-scan、deployer-profile | **DESIGN_ONLY**：wrong fee payer/holder-age/pool归因，根无常规LICENSE、疑似硬编码服务凭证，阻断整库运行/直接复制。 |
| **DEX成交语义兜底** | FnZero Python、MIT Go/TS与Carbon成熟解析器 | **P2 GAP_TRIGGER**：只有在OKX/Million外部业务事件具体缺少owner/Swap/multi-hop/版本等关键原始证据，才用固定测试选一个SDK封装，禁止重新手写通用DEX解析器。 |

### 新的安全/实际成本事实（纠正旧「OKX免费就能实时WS」的隐含前提）

- OKX当前官方[行情 API 费用](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-api-fee)：有Key的Free订阅每月 Basic 100K、Premium 100K；Premium含token holder/topTrader、cluster、signal、memepump dev/bundle；**Free不支持WS订阅频道**，Starter约**99美元/月**。注意`token-research`会在一个工作流中调用多个Premium接口，成本=实际API调用次数（需读取真实日志），不是“一次工作流=1次Premium”。WS地址数量和数据权限须再验。
- [Helius价格](https://www.helius.dev/pricing)：Free 1M credits/月、10 RPS；Developer 49美元/月、10M credits/月、50 RPS。归档/DAS/Webhook与增强服务计价不相同，真实钱包扫描的每Mint请求量尚未记录；不允许自动升级/支付。必须为每种方案分别记录`number of RPC/API calls, credits, 429, truncation, latency`，不能从“SDK开源”推断“数据零成本”。
- Million[ trading.module.ts ](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/trading/trading.module.ts)中`EXECUTOR=local`可执行真实签名交易，默认paper会对满足条件的机会自动模拟下单；主入口`main.ts`没有完整认证层，仅按代理请求头限制隧道访问，不可认为公网安全。**只读审查前不得部署可访问交易端点**。
- OKX [wallet-monitor-ws.md](https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/workflows/wallet-monitor-ws.md)的输入表格写10钱包，实际CLI `cli/src/commands/ws.rs`最多200个地址；**文档值冲突**不证明服务配额可达200，实际以`ws channel-info`与订阅结果为准。

### 新的独立测试（当前会话执行，不是第三方代码运行）

- 本地现有`/mnt/data/solana_reuse_test/work` Library旧P3-M01快照：再跑 **38/38 Python unittest OK**，且实际串联`raw_tx_adapter → wallet_batch_monitor`：合成Mint中的一笔Token Transfer输出`FIXTURE_RESEARCH_ONLY`、`no_trading=true`、Buy/Sell均0。原fixture自己声明coverage.complete，**不是链上完整性证明**；不能称真实监控完成。日志`2026-11-01-baseline-recheck.txt`、输出`2026-11-01-monitor-out.json`。
- SQLite内存独立结构复现 `Million Prisma LiveEvent.signature UNIQUE`：同签名sig_X向wallet_A与wallet_B各插入一条，第二条被UNIQUE约束拒绝，仅1条存活。测试文件 `million_contract_probe_2026-11-01.py` 与结果 `million_contract_probe_results.json`。**不是执行Million的Node服务**，但与源码的Webhook首命中退出共同证明其数据模式不保留每钱包参与视角。后续不能仅把`signature`改成复合键而忽略同笔多token多指令，应有`signature/observed_wallet/instruction_path`关系及经济事件唯一性定义。
- 当前Node22、无Node24，且此前环境到GitHub的DNS不可用；未获得Helius/OKX已授权Key或Grok运行终端。**本轮未运行OKX、Million、HoldTech、pumpwatch、FnZero的完整实例**，未获取真实主网Mint报告或计费读数。PR#16已有GitHub CI不能代替这项验收。

### 最短实施顺序（只读，无支付/签名/下单）

1. **单Mint报告**：同一个旧研究候选Mint `87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump`，先在有经用户授权、禁用自动x402支付的环境运行OKX CLI `workflow token-research`。记录每个API的原始响应引用、获取时点、权限、计费调用次数、500/429/null、holder样本分母及截断；不从旧研究推断当前实时状态。
2. **全成品只读安全验收**：仅在隔离Node24环境验证Million只读GET路径和无交易路径可达性，控制绑定地址/无交易密钥/禁止对外写入端点；重点复核同签名多钱包、历史断流/补齐、公共Hub、owner重建、CPI/转仓非成交。若不能确保仅只读，不能直接部署整库，考虑复用数据查询/发现模块。
3. **差异补齐**：对单Mint快照与长期监控同一业务对象比较，需持久保留钱包Owner、TokenAccount、钱/Token净流量、明确交易类型、库存快照、同源关系和UNKNOWN/覆盖状态；有真实解析缺口才选FnZero或其他SDK做一个最小桥接。先复用pumpwatch Dev历史，不新建发行者探测器。
4. **Grok交付**：Grok S1云电脑验收未完成；先拿**一个公开Mint+同一观察时点**的可信报告、再拿一个增量窗口，才讨论定时运行。验收标准：输出不编造真实买卖/同控/收益，费用有实际调用记录，相关钱包的多视角事件不丢，缺失索引输出UNKNOWN。

**跨原知识单元落点**：D01/D02协议/发行阶段，D04钱包标签，D05真实资金来源，D06库存与LP，D07同签名群体时序，D08/D09信息与可跟性，D10实际观察/成本，D11/D12反证和解释。旧Hermes/qb-/meme-/Why-Solana审稿与FnZero/Carbon/GMGN/MadeOnSol参考仍常驻，不删除；不增加新D层或自造「内核」。

## 2026-11-01｜首次21专家联合项目审查：统一产品判断与最小可交付路线

**性质**：在现有V2/专家注册表基础上对实际源码、方法和公开供应商契约进行`PRODUCT_AND_SOURCE_REVIEW`；不是21个Bot运行、真实市场实证或外部成品已部署。按21专家全覆盖→关键分歧深入→唯一统一判断完成。研究对象仍为“输入Mint→关键钱包→资金与真实交易→库存/群体异常→可解释只读监控”。项目最终可扩展为全市场事件发现；**单Mint按需研究≠全市场覆盖**，是更低成本且可测的第一验收范围。

### 结论与对先前实现计划的修正

**PIVOT_IMPLEMENTATION_KEEP_DOMAIN**。当前不用再编另一套解析器或21专家框架，也不把OKX+Million+FnZero全部整合成单一大系统。正确顺序：
1. **第一个完整交付：按需Mint报告**：优先审阅/在授权环境运行 OKX [现成token-research工作流Rust实现](https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/cli/src/commands/workflows/token_research.rs)（token report→holder/cluster/topTrader/signal→条件性Dev/Bundle）；把原始供应商数据、null原因、时间、计费保留。旧[qb-单Mint关键地址矩阵程序](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)已经定义了研究报告的业务栏目，可作为**结果验收模板而非照搬GMGN执行器或标签阈值**。
2. **第二个交付：一个Mint的两时点与一段增量钱包观察**：评估 [Million](https://github.com/Kelows/million/tree/c89ad07caaf70773d40b45943e136eadc4f946a5) 原生发现/钱包订阅/funding/flows的整套可用性；其 `apps/api/prisma/schema.prisma` 有 `LiveEvent.signature @unique` 且 `live-feed.service.ts::ingestWebhookTxs` 首个命中钱包即break，**当前不具备同交易多监控钱包的完整群体证据**；`RosterPosition.qty Float`以及分析快照→live增量来源需要数量精度和漏帧对账。禁止把完整成品能启动当成可信产出。需看最小修复是否能在许可和安全边界内完成。
3. **只补真实的差距**：现成pumpwatch创作者历史、HoldTech holder-overlap、已有Why-Solana资金图/旧Hermes业务分析继续作为候选。需要协议成交事实时才对照FnZero Python/Carbon/Go现成SDK；不增加手写DEX解码。数据覆盖若是主要缺口，优先从服务商/DAS索引和持久流获取而不是写解析器解决不了的问题。
4. **全市场与Grok运行视为后续扩展阶段**：需额外有市场级Mint发现/采集范围、钱包集合随时间更新、每个源的覆盖水位、故障重放和资源预算。不能把一个Mint的按需报告宣称为“全市场监控”，也不能把GitHub Draft/fixture成功当Grok部署。

### 21位专家完整覆盖（每位对应实际有意义的失效机制；不以投票决定结论）

| 专家ID | 审查出的特有问题或未确认条件 | 对业务/工程方案的实际影响 |
|---|---|---|
| E-L0-01 | 需要固定数据源、版本、观测/回补时点；GitHub源码与旧报告不是当时链上事实 | 要求每个报告字段给来源与可追溯版本；不以旧K1当K2 |
| E-L0-02 | OKX字段可能null且各接口分母不同；cluster/Smart Money/Bundler是供应商语义 | 按来源原义保留字段、null和采样范围，不统一翻译成同控 |
| E-L1-01 | Million对交易BUY/SELL用余额净差启发式，签名唯一导致同Tx多钱包视角丢失 | 同签名每个观察钱包需有独立可见关系；与Swap真实指令事实分开 |
| E-L1-02 | pumpwatch seen_at是本地record_launch时钟，非Mint创建时间；回补后统计会失真 | 发行时间与采集首次发现时间分别记录；可得时间不得由链上blockTime代替 |
| E-L2-01 | 发行曲线、迁移和多池阶段会改变观察分母 | 单Mint报告必须标识阶段和池/协议，不能跨阶段直接比较数值 |
| E-L2-02 | 价格/市值和池可卖深度不同；LP余额非自由持有库存 | 保留报价池及真实流动性/LP权限差异，避免Top10当可卖能力 |
| E-L2-03 | Token-2022权限、转账费和交易失败可能误导安全/净到账 | 未知扩展或Token权限未核，报告降级而非默认安全 |
| E-L3-01 | qb-单币关键地址矩阵可继承；高PnL与真实交易风格/可跟性不同 | 先保留真实钱包角色/样本覆盖，不让GMGN标签成为最终身份 |
| E-L3-02 | Million funding/owners与HoldTech同Slot只是图关系，可能是公共Hub/代付交易费 | 将资金来源、手续费支付、同控主体、经济受益分开 |
| E-L3-03 | Million RosterPosition用Float qty和来源分析→live滚动更新，未证明token原子单位精确或仓位连续 | 当前持仓快照与事件净变要独立对账，保留精度、缺口和托管/LP排除 |
| E-L3-04 | pumpwatch SQLite creator历史按本地写入时间聚合；创始人/授权者可能不同 | 复用发行数据库模式，但显式分开发行时间、采集时间和creator/权限身份 |
| E-L3-05 | 同Slot群体可由公共发行事件/热门榜触发 | 用相对于市场公开事件的时序及跨Mint复现判别，而非同秒就标协调 |
| E-L4-01 | 只有已筛选钱包/热门币会产生幸存者偏差；M01样本complete仅fixture | 记录可观察总体、排除理由和未命中样本；不能当全市场覆盖 |
| E-L4-02 | 系统检测到交易不等于外部观察者还能以原价参与 | 只读阶段不发出盈利承诺；若研究跟单保存alert可得时点 |
| E-L4-03 | FCZ/二次启动机制仍属旧meme-研究假说，不能覆盖第一条Mint监控 | 保留反向陷阱和结构候选，不作为一期强制K线/策略规则 |
| E-L5-01 | 观察到价格不是可执行进出报价，Jupiter多腿不能重复记独立交易 | 将双向quote/滑点留为未来可跟性验收，不放进一期只读前置 |
| E-L5-02 | 高成本WS与数据服务、漏掉的机会和失败退出均有机会成本 | 先使用可授权的按需Mint查询；真实调用/事件成本再决定何时开启连续流 |
| E-L6-01 | HoldTech同slot规则可误把纯Transfer与独立买家当Bundler候选 | 为每一条异常输出能区分竞争解释的负例查询 |
| E-L6-02 | 历史回放与AI自评分不能证明监控及时有效 | 同Mint双时点、独立源复核、错报/漏报、非信号分母和覆盖日志必需 |
| E-L7-01 | 旧Hermes/qb-/meme-/21专家已有体系，若另建架构会继续碎片化 | 只把统一判断回填原Dxx、参考池与现有进度/工程文件 |
| E-L7-02 | Million默认paper且有EXECUTOR=local真实签名开关；Grok云电脑尚未验收 | 独立安全沙箱，不暴露API；只读运行、故障恢复/回补、状态一致才升级 |

### 最具决定性的跨领域分歧（有不同经济机制与裁决条件）

**A. 成品报告 vs 可审计经济事实（L0/L1/L3/L6）**：OKX Rust workflow确实实现完整Token数据聚合；但Cluster、SM、Dev、Bundle是按供应商定义取得的字段，不证明共同控制/已获利。Million `buyersOf`以收到Mint Token+资产净支出近似BUY，也不等于完整DEX成功执行。统一输出保留`source/field_definition/unit/sample_coverage/observed_at/unresolved`，真正Swap由明确签名、owner、quote和协议事件确证，缺则UNKNOWN。**需判别的反例**：同Slot独立机器人、公共Hub、普通Token转仓、聚合器CPI/路由。
  
**B. 成品长期流 vs 群体异常不可漏数（L1/L3/L4/L7）**：Million`LiveEvent.signature @unique`与Webhook`break`对同Tx多监控钱包导致结构漏记，且有限保留期无法支撑历史C02/C05；这比“新增10种钱包标签”更影响目标。最小反例：同签名A/B两钱包均发生Token动作，必须同时保留观察主体视角又仅将一笔链上经济成交计一次。记录slot/签名/指令路径/钱包角色和订阅时点；缺失/断线不得被当0成交。

**C. 持有人快照 vs 可卖经济库存（L2/L3/L5）**：Solana官方[Token文档](https://solana.com/docs/tokens)区分Mint/Token Account/owner；Million`RosterPosition.qty Float`与live增量不是任意Token-2022原子单位或全部Token Account的真实钱包净持仓保证；LP/vault/托管/未成功转账应分离。需要至少两时点相同Mint与Owner的资产快照、供应量分母、Token账户映射、变化原因和缺失标记；不自动把Top10变化称为庄家减仓。

**D. 发行历史与观察时间（L1/L3/L6）**：[pumpwatch `creator_reputation.py`](https://github.com/cinder-security/pumpwatch/blob/156a91ab63740ab0ce8700434ff33844d00de519/code/creator_reputation.py) `record_launch` 中 `seen_at=int(time.time())` 是**本地入库时间**，不必是Mint创建的链上时间；`creator_reputation` 用它计算24h/7d。实时无间断运行下可能接近；一旦RPC重试或历史回补则会偏移。复用SQLite历史结构时须区分发行事件的`blockTime`与首次观测/入库时间，不会把回补批次误判为Dev高频当下发币。

**E. 完整基础设施 vs 最低实际维护量（L5/L7）**：新增审查[Solana Foundation `solana-microscope` @20a516b](https://github.com/solana-foundation/solana-microscope/tree/20a516b2066ec4f13e0b76926b11f666ffd0f49a)（MIT）：已实现Carbon+RPC/Yellowstone、检查点/重试、Prometheus/Loki/Grafana可审计告警、解码失败指标；但文档明确一次部署监控单个Program，不是给定Mint的跨协议钱包关系成品；全套部署需求约2vCPU/4GiB/40GiB，作者估算云主机约$50/月，外部RPC/Geyser费用另算。**PARK_RELIABILITY_PATTERN**，可复用其检查点/重放/观测设计；一期不为它迁移整套Rust和监控平台。发现数据丢帧或准备部署长期订阅时重新审查。

**F. 实时吞吐 vs 研究增益（L4/L5/L6）**：供应商服务不能简单当无限免费基础设施。[OKX行情费](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-api-fee)当前Free Basic/Premium各100K/月、**不含WS**，Starter $99/月支持WS；[Helius](https://www.helius.dev/pricing) Free 1M credits/月、10RPS，Developer $49/月、10M credits/月，但不同endpoint计费与请求限速不同；[Helius Token APIs](https://www.helius.dev/solana-token-apis) 已有DAS账户快照、历史与Parsed Events，这提示**不必为每个指标自己重建索引器**。应对按需与实时分别按`每Mint请求/时间/结果覆盖`计费、保存限速和失败，不以订阅功能存在认定可长期承受。

### 新增可复用资产：按本项目需要定位，而非笼统“有用的开源仓库”

| 资产 | 已实现的真实功能 | 必要条件/许可/风险 | 决定及重新启用 |
|---|---|---|---|
| [Solana Microscope](https://github.com/solana-foundation/solana-microscope) | 程序事件订阅、Carbon解码、RPC回补/持久检查点、观测/告警/仪表盘；MIT许可证文件 | Rust/Docker/Prometheus/Loki/Grafana；单Program非Mint钱包分析；主机/RPC费用；没有运行/测试 | **REFERENCE_FOR_D10**。当监控持续化且需要故障恢复/日志观测时比较其最小可靠性方案，优先复用其已实现思路或成品仅用于适合的单Program监控 |
| [Helius DAS/Token APIs/Parsed Events](https://www.helius.dev/solana-token-apis) | 按owner查询Token余额、资产元数据、按地址/签名检索与结构化解析 | 商业服务具体调用积分/覆盖/限额必须读文档和得到授权；Parsed Events部分能解结构，不保证经济同控 | **ALT_DATA_ORACLE**。当OKX缺Token-2022/时间一致性/历史与账户细节，可选少量同Mint独立对照，绝不自动启用付费服务 |
| [Triton Yellowstone Fumarole/Old Faithful](https://triton.one/open-source) | 有恢复游标/持久流/历史归档的实际供应商方案；项目公布可靠性与重放能力 | 管理版商业授权、条件/服务可用性/保留期限待逐项核；不能把广告中的服务水平当独立实测 | **RELIABILITY_ALT**。未来出现断流/历史回补实际缺口再调研，不作为当前按需报告的新增依赖 |

### 按一套统一业务报告验收，不另造系统架构

**第一个报告的最小具体输出**：`mint; source_version/observed_at/coverage; launchpad_and_phase; key_wallets(owner token accounts supplier labels); funding_edges(economic_role_unknown_when_unsupported); executed_trades(separate_transfer); holder_snapshots/denominator/LP exclusions; multiwallet_events_and_missing_spans; competing_explanations; evidence_links; cost_and_failure_log; no_trading`。这只是业务结果字段清单，实际接口契约应从成熟程序真实输出确定，不提前创造自制全新schema。

**立即验收三例**：
1. **普通Token转账**：钱包收到Mint Token，但无明确Swap；不得标为BUY/盈利。
2. **同签名双钱包**：两个订阅钱包同一Tx发生不同动作；必须都保留观察视角，不得将该签名倍乘为两笔真实链上swap。
3. **历史回补的发币记录**：同一天入库的多个旧Mint，Dev24小时“链上发币次数”不能等于入库次数；时间未知则不能出实时频率结论。
随后扩充：池迁移/多池、Token-2022、断线缺口/回放、空响应/null/429、同Hub跨Mint以及两时点库存核对。必须有真实输入和来源才可升级为`READ_ONLY_DATA_VERIFIED`。

**本轮证据等级及禁止声明**：已直接恢复全21位专家和D01–D12索引，重新审阅原Hermes `CONTEXT.md`、旧`qb-/sikk_gmgn_token_report.py`、`meme-/SOURCE_OF_TRUTH.md`、当前P3-M01 PR #16的代码/通过的GitHub CI与本轮外部源码；无第三方成品实际安装运行、无用户授权OKX/Helius密钥、无Grok云电脑部署。既往38/38离线Python通过仅为Library旧快照，不是本轮重新执行的实时测试。PR #14/#16仍Draft且**不同base**：#14基于`research/actor-economic-mechanisms-20261030`、#16基于`main`；不能因为分别成功就认为主分支已有合并后的能力。GitHub工程与知识联调验收仍待进行。

### 对现有D01–D12的成熟度审计（不因专家参与自动升级）

已实际读取`gpt-meme-project-index.v1.json`、`whole-domain-atlas.v1.json`和`knowledge/experts/registry.v1.json`：现有**21位专家均为知识型视角而不是已部署Bot**；全域知识图标为`exhaustive_scope_inventory_not_complete_research`；其中**D01（Solana链上基础）和D07（市场行为与时序）在索引仍是`declared_research_gap`**，其余领域目前为`legacy_seeded_unverified`。这说明全领域目录完整，并不意味着能力都已完成或真实市场规律已被证实。因D01交易归属与D07群体时序恰好是当前成品完整性最依赖的两域，必须优先用外部成熟源码/真实数据增强，不能让假“知识完备”降低研究深度。

**业务与D域在原体系内对齐**：Mint的协议/曲线和真实Swap对应D01–D03；关键钱包/资本来源/库存/跨Mint群体对应D04–D07；异常有用性/跟随者可执行优势对应D08–D09；源覆盖、反证和AI专业知识转换对应D10–D12。各域只存**对既有机制的新证据与反证**，本台账负责成品代码/许可/接口/重访条件，`gpt-meme-progress-current.md`只存唯一当前决策与未完成状态。禁止三处复制同一篇评估，确保只有一个产品判断真源。

**本次路线决策**：`CONTINUE_DOMAIN / PIVOT_IMPLEMENTATION_SEQUENCE / REUSE_FIRST / READ_ONLY_ONLY`。先用OKX成熟Token Research取得可核查单Mint事实报告，再决定Million成品的多钱包与持续性是否值得修补；只有发现明确协议语义缺口才拿FnZero/Carbon替代。全市场监控、AI规则自主更新、交易执行全部留到另有实际依据的后续阶段。相关D01–D12新认识只表示提出了可检验专业问题，不改变原有单元研究成熟度。

## 2026-11-01｜从候选成品到第一块可运行拼装：OKX结果适配已实际落地

**复用路线判断：WHOLE_WORKFLOW_FIRST + THIN_REPORT_ADAPTER**。重新阅读当前Grok`src/solana_meme_os/monitor.py`（只接受手动输入的标准化Observation JSON）、OKX`cli/src/commands/workflows/token_research.rs`与`cli/src/output.rs`，确认后者有Rust CLI真实业务函数`run/fetch_and_assemble/assemble`，输出壳层为`{ok:true,data:{workflow:'token-research',address,chain,core,structure,launchpad}}`；原Grok监控器**不能直接接收这一结构**。因此不是“装好两个项目就合成成品”，缺的是一段严格对齐语义的适配。

**本轮完成的最小工程成果**：已在[工程Draft PR #16](https://github.com/sunshihao001/grok/pull/16)创建`src/solana_meme_os/mint_report.py`、6个单测、明确标记`SYNTHETIC_DEMO`的样例JSON。只读取已有OKX格式文件，不自主联网、签名、交易或支付；保存`report.md`和`report.json`，锁定Mint和Solana链、CLI成功状态、UNKNOWN/null、源JSON SHA256及独立处理时点；**不凭字段存在宣称同控/成交/覆盖完整**。本地新增6/6通过、与旧Library快照相加44/44通过，已回读GitHub文件内容；并未对OKX付费API/真实Mint/Grok云电脑做实际运行。README提供`--fixture`演示命令，运行文件仍在工程Draft，不在main。

**为什么不先fork Million作成品母体**：核查`apps/api/src/app.module.ts`、`live/live.module.ts`、`opportunities/opportunities.module.ts`的模块导入显示TradingModule为多个服务的实际依赖，并非简单按一个“read-only开关”即可完全去掉交易路径；`LiveEvent.signature`唯一性会丢一签名多钱包。它仍是后续高价值的长期追踪/前端项目，但一期拆卸成本/安全性/业务归因的风险大于OKX现成单MintCLI。

**下一次复用启动条件**：在无自动x402付费、无钱包签名且用户已授予相应权限的环境真正取得一次OKX `token-research` JSON，将源JSON完整保留、核对过错返回/字段类型/API用量，再用上述薄适配生成**一份真实Mint报告**。通过才称`V0.1 REAL-MINT REPORT RUNNING`；下一能力优先两次快照比较而非建多Bot或图形控制台。Million/Pumpwatch/FnZero继续按既有源码和重访条件保留，不删源不另建新框架。

## 2026-11-01｜OKX业务字段契约实测：薄报告已提取关键钱包与资金候选

**源码证据**：OKX`cli/src/commands/token.rs::fetch_holders`调用`/api/v6/dex/market/token/holder`最多100，返回从HTTP API`data`拆出的`list`内容（也保留可能的`{list:...}`分页结果）。官方[持有人接口](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-holder)定义`holderWalletAddress`、`holdAmount`、`holdPercent`、`fundingSource`和PnL指标；文档的默认顺序可能是收益维度，不能直接称为“按余额最大的前N位”。[Cluster概览接口](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-cluster-overview)含`clusterConcentration`、`holderSameFundSourcePercent`、`holderSameCreationTimePercent`、`rugPullPercent`等厂商指标，字段名百分比不等于真实经济主体概率。**这改变了产品报告**：必须展示返回钱包候选、供应商资金线索、聚类统计各自证据和未知，不把统一标签生成为已验证庄家或交易信号。

**真实工程改进**：[PR #16 `mint_report.py`](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/src/solana_meme_os/mint_report.py)增加纯读取`business_summary`：返回钱包候选+源路径、fundingSource提示、Dev/Bundle可用性、TopTrader样本行数、原始供应商requestTime/time字段与UNKNOWN覆盖状态；`report.md`展示可读首屏，`report.json`保留全部原始section。新合成fixture和扩展测试在相同工程分支；**12/12新增模块单测 + 本地旧Library版M01联合50/50通过**。该测试不是OKX SDK/外部API真实执行，也不是在PR #16远端Grok云电脑运行。

**V0.1唯一剩余硬阻断**：已授权只读API、可联网/安装OKX CLI的隔离环境及真实Mint结果。目前本地外网DNS不可用，CLI不在PATH，未获取Key或Grok运行终端；若SDK存在x402自动付费特性，必须禁用/隔离支付与钱包凭证，不能为“真实验收”私自付款。后续验实际费用、requestTime、返回形状和覆盖样本后才升级业务状态。其余Million/HoldTech/pumpwatch/FnZero仍在原台账长期保留，当前不为了“完整”把它们全量合并。

## 2026-11-01｜全量参考资产登记入口（已完成首轮去重，防止下轮遗忘）

**唯一机器可检索真源**：[`knowledge/system/gpt-meme-project-index.v1.json`](gpt-meme-project-index.v1.json) → **`reference_assets.items`**。该字段已实际登记 **65项**（已去除Raydium重复别名）且每项包含稳定REF编号、名称、类别、原始URL（未验证不填）、核查等级、预期业务价值、集成优先级、主责专家及**下次何时重新调查**。之前的 `source_repos` 5项是历史研究固定源清单，不是全量参考资产目录；两者用途不同，旧5项原封保留。用户的要求是“**所有过去提过的来源都能找回来**”，不是让65个来源同时成为部署依赖。

**首轮证据等级人数/数量**：65项中 `SOURCE_AUDITED=17`（至少读过某些真实源码/业务流程，**不等于整库全面审计、安装或真实运营**）；`REPO_VERIFIED=10`（仅GitHub库存在/元数据确认）；`PAGE_VERIFIED=11`（原始/官方网页已确认）；`HISTORICAL_NAMED_ONLY=26`（历史讨论提到，准确身份或链接尚未逐项核实）；`LINK_UNRESOLVED=1`（历史曾提到`solana-foundation/transaction-v1-examples`，本次未检索到有效仓库）。**明确区分源码已读、服务存在、真实运行、源码许可、市场数据验证和研究结论成立。**

### 已登记资产分类与入口

| 资产类型 | 数量 | 首轮完整登记名称（实际细节、复用条件与证据状态以JSON真源为准） |
|---|---:|---|
| 自己的项目/历史资产 | 5 | [grok (当前正式项目)](https://github.com/sunshihao001/grok)、[原Hermes Workflow OS](https://github.com/sunshihao001/-)、[qb- GMGN单Mint程序](https://github.com/sunshihao001/qb-)、[meme- 理论研究库](https://github.com/sunshihao001/meme-)、[Why-Solana-Memecoins-Are-Over (个人fork)](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) |
| 成熟业务成品 | 6 | [Kelows/million](https://github.com/Kelows/million)、[co-numina/holdtech](https://github.com/co-numina/holdtech)、[cinder-security/pumpwatch](https://github.com/cinder-security/pumpwatch)、[OKX OnchainOS Skills+CLI](https://github.com/okx/onchainos-skills)、[GMGNAI/gmgn-skills](https://github.com/GMGNAI/gmgn-skills)、[Solana Microscope](https://github.com/solana-foundation/solana-microscope) |
| SDK / 解析组件 | 8 | [FnZero Solana Parser SDK Python](https://github.com/0xfnzero/sol-parser-sdk-python)、[FnZero Solana Parser SDK Rust](https://github.com/0xfnzero/sol-parser-sdk)、[Carbon Indexing Framework](https://github.com/sevenlabs-hq/carbon)、[solana-dex-parser-go](https://github.com/DefaultPerson/solana-dex-parser-go)、[solana-dex-parser TypeScript](https://github.com/cxcx-ai/solana-dex-parser)、[MadeOnSol SDK](https://github.com/MadeOnSol/madeonsol-sdk)、[Helius core-ai](https://github.com/helius-labs/core-ai)、[Yellowstone gRPC](https://github.com/rpcpool/yellowstone-grpc) |
| 链上协议与官方工程 | 12 | [Raydium CP Swap](https://github.com/raydium-io/raydium-cp-swap)、[Pump public docs](https://github.com/pump-fun/pump-public-docs)、[Jito Solana Client](https://github.com/Jito-Foundation/jito-solana)、[Metaplex Token Metadata](https://github.com/metaplex-foundation/mpl-token-metadata)、[Solana Official Docs](https://solana.com/docs/core/transactions/transaction-introspection)、[Jito Docs](https://docs.jito.wtf/lowlatencytxnsend/)、solana-foundation/transaction-v1-examples、Meteora AMM、PumpSwap、Jupiter Aggregator、Clanker、Zora |
| 数据服务与工具平台 | 11 | [Helius Enhanced/DAS/Parsed Events](https://www.helius.dev/solana-token-apis)、[QuantBloc methodology / Base / MCP](https://quantbloc.com/methodology)、[Triton / Fumarole / Old Faithful](https://triton.one/open-source)、[Bitquery Solana API/Token Holder](https://docs.bitquery.io/docs/blockchain/Solana/solana-token-holders/)、[DEX Screener](https://dexscreener.com/)、GMGN Terminal / CLI、Arkham、Nansen、BlockSec Phalcon、CoinGlass、RugCheck |
| 学术/实证研究 | 6 | [Why-Solana-Memecoins-Are-Over (上游)](https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over)、[Solana Sniper Reverse Engineering](https://github.com/Sorghobrayan-dotcom/solana-sniper-reverse-engineering)、[MELT Dataset / Code](https://github.com/git-disl/MELT)、[Meme Coin Factories (ACM CCS 2026)](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html)、[A Midsummer Meme's Dream (USENIX 2026)](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini)、[RED-COHORT 2026 dataset](https://zenodo.org/records/21765387) |
| 实务工具/资料渠道 | 16 | [Froggy V2 Scanner](https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101)、Sputnik Parser / @sputniksol、OnchainRadar、Genesis Arbitrage、ArbitrageScanner、Synapse、Axiom、Photon、TradeWiz、Ray Bot、Stratos、Crypto GYM、Eclipse Trencher、taxiflip Axiom Dev Tracking教程、Ethtective、Resonance |
| Grok运行经验 | 1 | [Grokbot Playbooks](https://github.com/sit-in/awesome-grokbot-playbooks) |

### 由全部参考项目反过来审查21位专家的实际发现

- **已覆盖的专业领域**：交易与归属E-L1-01/02；发行/池/权限E-L2；钱包/资金/Dev/库存E-L3；异常/可跟随优势E-L4；可卖性和实际执行E-L5；数据反证与盲评E-L0/E-L6；知识综合E-L7-01；持续运行与故障隔离E-L7-02。
- **确实遗漏的职责**：谁统一比较**整套现成产品**、开源许可、版本依赖、交易/支付路径、接口相容性、改动范围、运行成本、MVP交付和可回退集成？旧E-L7-01负责知识综合，E-L7-02负责监控故障，**没有谁明确负责“从成熟代码形成真正可用成品”**。这个空缺已经导致过去把研究/解析器测试当成项目推进。
- **最小、可解释的增补**：在原专家注册表添加 **`E-L7-03 开源成品集成与产品交付专家`**，现有数量由21→22；它是知识视角而不是Grok Bot，不新增L/D层级、Bot或独立流程。负责把E-L0、E-L1、E-L3、E-L6各自发现的事实与缺陷转成“采用哪项整套成熟程序/最薄适配/真实MVP验收”的**一个统一产品决定**。只有将来新项目产生无法被现有22位专家解释的真实机制，才申请新专家；避免人数膨胀。
- **关键发现**：新登记的[QuantBloc方法文档](https://quantbloc.com/methodology)直接区分钱包本人成绩与跟单者在block+2之后的可得成绩，且明确限制Pump.fun/PumpSwap覆盖；这是**E-L4-02跟单信息差研究的现成外部方法基准**，比简单“胜率高的钱包值得跟”更符合项目知识目标，但仍须区分供应商公开方法与自己独立复算。另有[MELT](https://github.com/git-disl/MELT)已提供行为数据/风险标注及CC-BY-NC许可；[USENIX Meme's Dream](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini)、[ACM Meme Coin Factories](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html)、[Zenodo RED-COHORT](https://zenodo.org/records/21765387)已登记为**研究证据/反例来源而非可直接运行监控器**。
- **对产品路线的影响**：继续以`grok`为单一产品主体、OKX`token-research`为V0.1整套按需业务源；Million用于钱包持续监控但需修多钱包漏记/移除交易耦合；pumpwatch给Dev历史；FnZero/Carbon给明确DEX解析缺口；Solana Microscope给故障恢复经验。HoldTech只是有许可证/误归因限制的备选，不能随意直接复制。QuantBloc研究的是监控之后的可复制性，不阻碍V0.1先运行。**不因登记65项就一次性整合65项**。

### 后续每轮统一使用方式

从用户的自然语言问题反查`reference_assets.items`，根据`role/priority/when_to_review`选择最少必要来源，先判断能否复用完整程序；逐项实际执行/测试后回填**同一项**的验证等级、源码SHA、实际失败原因和下一次重访条件。具体设计与反证只记录在本台账与已有Dxx专题；资产存在与是否运行的事实字段由索引记录，避免另建重复的选型总表。**首次登记的历史线索并未全部独立核实，未核实的URL宁愿空缺也不能猜。**

## 2026-11-01｜V0.1真正运行的第一个真实外部数据成品：DEX Screener（范围严格受限）

**审查启动条件**：此前OKX CLI没有安装/已授权会话，本地容器DNS失败；为避免把SDK或fixture称为真实交付，只从已注册65项资产中的REF-032（DEX Screener，`PAGE_VERIFIED`）使用官方[公开GET Token Pools API](https://docs.dexscreener.com/api/reference)。没有改变OKX完整Mint研究优先级、没有付费或自动执行外部钱包程序。

**具体运行路径**：`grok`工程PR #16新增`src/solana_meme_os/public_pair_report.py`及`mint_v01.py`，优先吃已有OKX `token-research` JSON，缺OKX授权才走公共数据池快照（**不是伪造OKX的Holder JSON**）。在[GitHub Actions实际运行41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009)及最终[raw数据Artifact运行41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009)中，一枚Mint`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`实际返回5池；另一`FdKdpz11GsTofLaNiddrhxrsE4APZYSSfLFqQ9YKpump`返回7池，供应商`DEX Screener`时间是抓取时间2026-11-01T02:44:23Z附近。实际原始JSON已下载，并与报告内SHA256逐字节一致、每条池的目标Mint base/quote匹配；完整真实证据为[工程实测文档](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/evidence/v01-real-public-pair-readonly-2026-11-01.md)。初期BONK样本公开API返回空列表，清楚标`COVERAGE_UNKNOWN`而不是断言无市场。

**跨专家发现**：E-L7-03强调真正调用与代码存在是两种状态；E-L1-01/E-L0-02指出同一Mint在PumpSwap、Orca、Pump.fun同时存在base和quote两种方向，`priceUsd`通常是base价格，而不是用户输入Mint保证的价格；`pairCreatedAt`是池创建不是Mint创建；`txns.h24.buys`是**供应商每池聚合笔数**，不是钱包交易/真实信号；E-L3-02说明池流动性不能代替钱包筹码与经济同控；E-L6-01要求将BONK空响应作为负例覆盖缺失，而非真实无流动性。公共池来源**不含Holder、Owner、fundingSource、Dev/Bundle，也不提供单笔Swap确定证据**。

**安全阻断更新（OKX自动支付）**：直接阅读[OKX cli/src/client.rs](https://github.com/okx/onchainos-skills/blob/main/cli/src/client.rs)，`get_with_headers/post_with_headers`含`ensure_payment_config`、`maybe_sign_payment`和HTTP 402重试签名付款流程。故`onchainos workflow token-research`虽然是*数据查询操作*，但客户端可能产生付款行为。当前`grok`只接受已有授权保存的OKX JSON，不自动执行外部CLI；必须先有安全隔离和付款隔离契约，再谈真实OKX完整工作流。没有授权时公开备用路径不应自动升级付费服务。

**实际业务状态**：`V0.1 PUBLIC_PAIR_DATA_REAL_VERIFIED`✅；`V0.1 FULL_WALLET_DEV_FINANCIAL_REPORT`❌；`GROK_BOT_DEPLOYED`❌。后续必须先查现成完整OKX/替代来源的真实权限和原始钱包结构，再补最薄接入，不再自主发明整套Mint索引器。

## 2026-11-01｜RugCheck真实Mint Holder和Creator数据已获，池库存归因负例

- **已经真实执行**：工程PR #16在[GitHub Actions 41268982018](https://github.com/sunshihao001/grok/actions/runs/41268982018)只读查询RugCheck缓存完整报告与DEX Screener实时公开池数据，成功取得20条Holder候选和Creator候选。RugCheck原始SHA256 `9671b8edf008772892035b22eb952b205409bc2125cb0f8fa16db5dd1178de0c`；DEX原始SHA256 `a7f941d5f2caca8c9ebff9b908b4a58dfa1009150ed55e986cb222fcd81e4de9`，已独立下载核对。
- **实际跨源反证**：RugCheck首位Token Account的Owner候选恰是DEX返回的PumpSwap池地址（供应商份额5.877731%）。这提示某些“Top Holder”是池相关账户候选，不能按单一私人鲸鱼归因；还需Solana RPC核验，当前公共RPC HTTP 429。工程PR #16已加入严格地址全等提醒及负例测试，正式CI120项通过。
- **经济来源限制**：RugCheck`creatorTokens=null`，故不能声称Dev无发币史；供应商风险分及Copycat标签不是交易收益/同控证明；缓存`detectedAt`不是Mint创建时间，DEX报价时点也不是原子同slot。只有实际返回的供应商事实可用于报告。
- **复用决策**：RugCheck是现有65项台账中已有的候选业务源，无需新的专家/解析器。以OKX现成完整`token-research`为目标，当前无已授权只读会话，且CLI具有x402付款相关逻辑，不应在未隔离时自动调用。RugCheck填补部分Holder/Creator**候选**，仍缺经过独立链上核实的Owner、资金图、完整Dev历史、已确认Swap及库存。
- 原始数据、精确地址、时间与假设边界见[真实工程证据](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/evidence/v01-pool-vault-holder-cross-source-2026-11-01.md)。


## 2026-11-02｜回到原参考的完整业务工作法：跨项目复用裁决

> **背景**：用户指出长期围绕单个多跳细节循环研究使全局认知和成品进展过慢。本次直接回读其已登记的旧Hermes、qb-、meme-、Why-Solana及Million、OKX、HoldTech、pumpwatch的设计原件、源码和历史报告。此处**只记录新核查的业务流程和差异**；前文既有功能表、许可证/安全审查、Dxx知识与65项资产保持原位。未直接运行第三方成品、未访问收费API，也未将README功能宣称为当前Grok已部署。

### 1. 按原参考的实际工作流，而非按其GitHub目录学习

| 来源及直接证据 | 原项目怎样从问题走到下一步（已看源码或业务方案） | 我们应整套继承的业务能力；必须隔离的前提 |
|---|---|---|
| [旧Hermes Phase0合同](https://github.com/sunshihao001/-/blob/main/design/phase0-workflow-contract.md)、[Skill07控制器](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-07-workflow-controller.md) | 候选入口→Token面板→钱包角色→结构→Evidence Chain→Paper Gate；每Mint有`phase_state`、`missing_fields`、`counter_evidence`、TTL与失败续跑。 | **保留状态/来源/反证/可恢复性**，不是恢复六Skill固定顺序，旧`confidence_score`不具统计校准，也不能把Gate规则直接当实盘。历史`docs/v2_skill_gap_analysis.md`又按8层提出新模块，这种层数扩张不等于实际产品提高。 |
| [qb-历史一键管道真实报告](https://github.com/sunshihao001/qb-/blob/main/data/gmgn_candidates_live_run/orchestrator/pipeline_report.md)、[单Mint脚本](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py) | 2026-05-04旧运行报告列出**5个候选、4个K线与纸面信号、状态机5币、1个钱包结构BLOCK、1个PAPER_READY被报价安全层进一步确认**；落地原始GMGN响应、状态日志、关键地址矩阵、基础设施目录、研究计划、manifest。 | **继承候选→关键地址→状态变化→复核计划及运行证据组织**；这是旧项目留下的实际结果文件，不等于当前CLI权限仍有效、每个钱包标签已被真实链上验证或真实下单。旧脚本`price`/Dev字段与现GMGN官方嵌套契约不一致已在参考审计单独反证。 |
| [OKX新币筛选](https://github.com/okx/onchainos-skills/blob/main/workflows/new-token-screening.md)、[Token Research](https://github.com/okx/onchainos-skills/blob/main/workflows/token-research.md)、[Wallet WS](https://github.com/okx/onchainos-skills/blob/main/workflows/wallet-monitor-ws.md) | 新币榜→安全/Dev/Bundle补充→单Mint价格/权限+Holder/Cluster/Trader/信号→可选连续钱包WS；业务流程已有合成CLI入口、依赖降级和条件步骤。 | **优先验证现成全景/Dev/群体查询可否拿到安全只读合法结果**，无需先造采集器；限制：文档≠已授权/免费/实时，同类字段必须核实实际响应，隔离可能签名与自动x402付款的CLI路径。 |
| [Million README完整循环](https://github.com/Kelows/million/blob/main/README.md)、[crawler](https://github.com/Kelows/million/blob/main/apps/api/src/crawler/crawler.service.ts)、[discovery](https://github.com/Kelows/million/blob/main/apps/api/src/discovery/discovery.service.ts)、[live](https://github.com/Kelows/million/blob/main/apps/api/src/live/live-feed.service.ts)、[copyability](https://github.com/Kelows/million/blob/main/apps/api/src/copyability/copyability.service.ts) | 钱包产生新Token候选，Mint交易又发现新钱包→安全筛查/历史钱包分析→自动扩展观察名单→实时订阅→表现反馈。`crawler`按API credits/循环限制，初次发现按Token不同历史时间采样、优先补未探索Mint；`discovery`预览**约70%大额候选+30%尾部随机**；`crawler`承认截断历史PnL有“缺买入但有卖出”的偏差，不按预览利润直接吸收，随后用持续观察判断。`copyability`以约60秒后一根分钟K线衡量跟随衰减。 | **最强的自驱式发现→监控→反馈整体业务参照**。但`live`的同一签名唯一事件使“触及多个观察钱包”的关系可能丢失；`owners`的联合图曾存在182-wallet误并；历史`copyability`一分钟K线是代理模拟而非真实报价成交与退出容量。含`trading`模块、Helius/Node24/数据库/可能付费，不可未经隔离整套部署。 |
| [HoldTech界面和扫描](https://github.com/co-numina/holdtech/blob/main/README.md)、[scan-core](https://github.com/co-numina/holdtech/blob/main/app/lib/scan-core.ts)、[deep-scan](https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts)、[trending脚本](https://github.com/co-numina/holdtech/blob/main/scripts/trending-refresh.mjs) | 单Mint→Holder质量/年龄/集中度/Bundle时间→资金来源→页面解释，另有本地定期扫描写Redis、前端按缓存展示Trending。业务上把复杂数据呈现给普通用户。 | **参考UI/报告组织与缓存-展示分离**，但不复制其运行配置：公开源码含硬编码的第三方API与缓存凭证（本文件不复述密钥）；`deep-scan`以`feePayer`当买家，有错误归因风险；`scan-core`预设第一名Holder为池地址候选，不是已核池权威真值。 |
| [pumpwatch只读监控](https://github.com/cinder-security/pumpwatch/blob/main/code/pump_watch.py)、[outcome tracker](https://github.com/cinder-security/pumpwatch/blob/main/code/outcome_tracker.py)、[README](https://github.com/cinder-security/pumpwatch/blob/main/README.md) | pump.fun发行事件→本地Creator信誉/历史→SQLite观察→按币龄动态轮询、429重试与运行失败恢复→跟踪后续结果；README给独立复现入口。 | **发行与Dev历史的完整支线+时效和失败恢复**；仅适用于其识别的发行程序/版本，`seen_at`不自动等于区块创建时间，其v0交易请求不能证明覆盖未来版本。 |
| [Why-Solana Methodology](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/METHODOLOGY.md)、[PITFALLS](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/PITFALLS.md) 与五专题源码 | 跨发行/钱包群体/资金/退出/跨Mint/净收益连续提出假设；`PITFALLS`记录**15个待反驳主张中11个未通过原作者验证**，并显式记录一个错误数据链导致的假阴性；有样本分母、Null、Hub、不可成交峰值、看未来、失败读取的修复经验。 | **把主动找错嵌入整条市场判断链**，不是每个细节单开一套新框架。作者报告数字不等于本项目独立复现，来源`review_only`。 |
| [meme-真源](https://github.com/sunshihao001/meme-/blob/main/SOURCE_OF_TRUTH.md)、[FCZ定义](https://github.com/sunshihao001/meme-/blob/main/03_语义概念/第一控盘区定义_v0.1.md)、[基准比较](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/基准策略对比实验设计_v0.1.md) | 将第一控盘区、深洗、POC/AVWAP、死亡盘看作可讨论的市场形态与成本假说，制定简单POC/AVWAP/Liquidity Sweep基线及失败样本。 | **竞争性市场机制词汇+如何验证复杂策略是否真优于简单方法**；价格接受区不直接等于操盘手真实成本，原模型的“控盘区”需要独立经济证据支持。 |

### 2. 从几套完整流程逆推出当前项目真正缺的环节

现有PR#16（非主分支）已凭真实DEX Screener+RugCheck获取两个Mint的池快照及一个Mint的Holder/Creator候选（其中Top Holder的供应商Owner精确匹配池地址），并能生成只读基础报告；RPC曾429，真实Owner独立核验与完整资金边仍未成功。其`mint_v01`、`vendor_event_handoff`、`wallet_batch_monitor`、`raw_tx_adapter`目前是**不同合同和有限样本/离线逻辑**，不应称全链路已经打通。

| 实际用户目标 | 旧参考已具备的整个工作法 | 当前项目仍需证明的最小事实 | 优先对照/复用方式 |
|---|---|---|---|
| 从市场中发现值得调查的Mint | OKX new-token-screening、pumpwatch发行监听、Million crawler、HoldTech定期Trending缓存 | 真实候选Mint发现时点、来源与覆盖；不是只有输入一个已知Mint | **先复用现成发现流，保留直接输入Mint入口**，不建第N个榜单 |
| 一个Mint查关键钱包、Dev与市场状态 | OKX token-research、qb单Mint关键地址矩阵、HoldTech成品页面、RugCheck基本报表 | 真实Dev历史、Holder/Trader与基础设施筛分、池/价/库存来源时钟 | 现有`mint_v01`先消费合法保存的成品/公开JSON，产出同一业务视图，按缺失记录UNKNOWN |
| 关键钱包→发现更多Mint/隐藏地址 | Million Discovery/Crawler、qb转入/转出中继、GMGN历史Trader、Why资金路径/跨组 | 当前系统还没有基于真实市场经济事件持续扩展新钱包和跨Mint名单的验收 | **优先Million的整个只读发现机制/调用合同作对照**，不先写新五跳、同控聚类或自研解析器 |
| 市场异动、执行服务与库存变化 | Million live/flows、OKX wallet monitor、pumpwatch多时间追踪、Why Null/Hub | 同一签名多钱包视角、真实Swap vs Transfer、事件时间/接收时间、两时点库存、失败恢复 | 仅当证据合同合格才进入现有M01报告；不允许供应商缓存标签冒充真实链上BUY/SELL |
| 异常解释、反证及是否值得行动 | Why PITFALLS/已冻结比较、meme简单基线、Million shadow/copyability、Hermes Evidence Chain | 能否排除公共服务和普通市场，是否有样本外预测增量与可执行净收益 | **结构解释/后续预测/交易经济分开**；只读风险报告不因没有交易Alpha而失败 |

### 3. 最高信息价值的三个参考源码发现

1. **“找钱包”的偏差不只来自聚类算法，也来自采样**。Million在Discovery中明确将约30%的预览预算随机覆盖大额队列以外的钱包；初始候选仍来自有限的交易时间窗口，`deepSample`只是按时间检查点抽样而非全历史枚举。应比较“只看最大买家”与“保留尾部探索”的**新有效地址**，而非只计钱包总数。
2. **“聪明钱盈利”在早期数据中可能是历史删失的结果**。Million`crawler`源码写明：截断历史可能留下卖出而缺少买入，造成不可靠的盈利表现，故候选不再按预览PnL准入；它用持续观察和后续闭环降低这一风险。其`copyability`使用一分钟后K线比较，并非成交报价/真实净值。这个经验同时修正D04钱包价值、D07时间、D08跟单信息和D11验证。
3. **“看起来完整的成品”也有源码级安全和语义失败**。HoldTech有可用的Holder仪表盘组织方式，却在公开脚本中留下凭据、把Fee Payer当买家并把Top1默认当池候选。真正值得重用的是可隔离的业务视图/缓存分层，不是盲目安装全部代码。相反，Why明确保存反证失败史；外部成品的`README`、API宣称、界面截图需要源码和测试共同审阅。

### 4. 本轮实际裁决与停止继续无效研究的条件

- **全局产品参考优先级**：就长期市场监控与发现反馈而言，Million的**双向发现循环**作为首要完整流程对照；就可快速形成真实单Mint/新币报告而言，OKX完整Skill/CLI优先验证（在已授权、无付费/签名条件下），现有免费RugCheck+DEX基础版不因此废弃；pumpwatch补发行者循环；HoldTech借鉴界面和Holder分析但不直接部署旧源码。
- **知识参考优先级**：旧Hermes/qb保留业务问题和运行状态经验，meme-保留市场阶段/价格/库存及反证假说，Why-Solana保留可追溯专业调查方法和历史失败，全部按原D01–D12就地参与具体研究；**不是**只研究多跳或先读完65项才动工。
- **禁止误判的就绪状态**：源码可读≠程序安装；文档描述可持续监控≠当前Grok已部署；单Mint供应商快照≠链上完整交易事实；一根60秒K线收益≈模拟代理≠真实可成交净利润；界面有“Pool”标签≠该地址已独立验证池Vault身份。
- **先验收的完整业务证据，而非新增的知识层**：用现有真实Mint `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`和原保留JSON，形成Mint/Dev/Holder/池到至少一条**真实来源经济行为或观察关系**的连续证据，并对照可授权成熟流程能否直接获得。无真实资金/执行/交易时保留明确空缺而非把Fixture包装成完成。若单来源能完整满足，保留全成品；只有隔离安全/费用/语义不合适时再拆成熟模块。
- **新研究真正有边际价值的条件**：至少改变一个跨领域判断（例如池库存≠私人持仓；历史PNL≠可跟随收益）或直接减少未交付业务的真实证据缺口。单个签名/多跳问题已不能改变顶层复用/市场解释时，主动暂停深挖转向发行、流动性、监控或市场经济新机制；不建立新专家/分类/阶段流程。

**本轮交付范围**：完整业务源码、设计与历史数据报告交叉阅读和可复核复用裁决。没有运行用户本机/云电脑上的整套Million、OKX或HoldTech，没有新Mint实网采集、Grok部署、钱包私钥/签名、交易或付费调用；仍需真实授权来源与工程隔离才能证明整个业务已运行。

