# Blix 全主体跨层源码研究｜业务→UI→API→数据→可靠性→整合判断 V0.1

> 审查日期：2026-11-06；基准：sunshihao001/grok 的 blix 分支提交 96e1f9f6540bc814ca01fe62f3ce6e70267014f9。**STATIC_SOURCE_REVIEW**。仅查询仓库目录树、指定原始源码、原作者设计/故障文档和现有测试定义。未运行 Blix、未请求 Solana 主网/API、未安装依赖、未使用钱包或模型、未执行测试、未验证云电脑。不要把下面任何静态判断称作 LIVE / PRODUCTION 验收。

## 0. 研究为什么做：关联既有目标，而不是再造架构

以 [可修订目标锚点](goal-map.md) 为准：G0 减少用户专业负担、理解市场风险与潜在价值；G1 从原始跟单问题发展为市场智能产品；G2 市场发现、单 Mint 调查、跨 Mint 监控、经济机制/竞争解释；G3 Blix 为当前主体、其他成熟项目只在证据指出真实缺口时整用或有限适配；G4 **本阶段只读研究全主体**。

审查不采用“按仓库文件依次介绍”的方法，而是逆向追踪：**真实用户场景 → 可达页面 → API/SSE → 后端业务/依赖 → 外部供应商 → 原始/派生存储 → 来源/覆盖/可靠性 → 未来整合位置**。原作者关于设计动机的注释要与代码事实区分；未观察的真实运行继续标 UNKNOWN。该方法参考 [ai-d 目标导航研究](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/planning/goal-navigation-v0.1.md)，但没有证明任何 Agent 已自主掌握这些知识。

## 1. 产品边界：不是一个 server.js，也不是一个页面

仓库树完整列出约 785 个文件，**仅代表目录树覆盖**；本轮重点检查了主要用户页面和相关服务文件，而不是逐行审核 785 个文件。区分：
- React 新 UI：web/src/main.tsx 按 hash 路由选择页面，web/src/shell/Rail.tsx 定义可见导航；页面如 Coins、Pulse、Coin、Tracker、Wallets/Traders、Narratives、AiPicks、Feed、Account、Launch、More/Health。
- 经典 UI：public/index.html、public/app.js、public/coin.js 等仍存在；React main.tsx 的 NotPorted 和旧路由重定向说明“源码有页面”不等于“新 UI 可到达”。
- Radar：server/server.js 单 Node 业务进程，集合 HTTP/SSE、市场订阅、研究任务、存储和后台调度。
- 页面服务：server/webapp.js 负责 React 构建产物、代理、缓存与成员/访客分流；server/apicache.js 在 Radar 延迟或中断时提供带年龄的缓存。
- 远程边界：worker/index.js Cloudflare Worker 与 webapp 的签名成员验证/权限判定；部署不同启用路径不同。
- 账户与真实交易：server/accounts.js、server/hosted-accounts.js、server/tradeapi.js 与外部 Vault；与当前用户明确只读目的不一致，应做风险隔离。
- 持久化：node:sqlite 的 radar.db、candles.db 等，历史归档、写前日志、后台 checkpoint、备份，另有若干独立状态文件/缓存。
- 新增实验层：server/intelligence/ 当前仅按需加载 mint-facts，不应先验认定它就是最终调查数据模型，更不能把它误记为已接入主 UI 或真实主网。

**架构总览（逻辑关系，非部署实测）：**
~~~mermaid
flowchart TD
  U["React/经典 UI"] --> W["webapp.js 页面/代理/缓存"]
  C["Cloudflare Worker"] --> W
  W --> R["server.js Radar 与 SSE"]
  W --> A["accounts.js / 真实钱包服务"]
  A --> V["独立 Vault（可能加载，未授权）"]
  R --> M["市场/钱包/研究业务模块"]
  M --> P["Solana / Pump / Jupiter / RugCheck / 其他来源"]
  M --> D["SQLite / 时序账本 / 本地缓存"]
  R --> AI["模型/订阅/自动研究"]
  X["intelligence/ 按需实验层"] -. "现阶段只按需读取本地原有接口" .-> R
~~~

## 2. 业务—源码—证据的全局矩阵

| 场景和用户看见的结果 | 当前 React/经典入口 | 关键 API、推送与核心代码 | 对应事实、数据和限制 | 当前判断 |
|---|---|---|---|---|
| ① 发现热门、新币、噪声过滤 | web/src/pages/Coins.tsx Discover、Pulse.tsx Pulse | /api/discover、/api/tokens、/api/pulse、SSE；server/engine.js、sources.js、quality.js、pulse.js、coverage.js | PumpPortal、市场索引、链上事件、tokens/snapshots；漏检和多发行平台仍需校核 | 已有完整业务骨架，优先复用 |
| ② 从候选进入 Mint | web/src/pages/Coin.tsx、coin/Header.tsx | /api/token/:mint 15s；/api/coin/:mint 3s；/api/coin/:mint/trades 2s；/api/jup/:mint 5s；coin.js、holders.js、jupdisc.js | Mint 信息、市场、持仓、Dev、交易与来源混合；不同接口不可混用为同一事实口径 | 需做分字段来源与完整度对照 |
| ③ Holder/关联与 Bubble Map | Coin 页面内 coin/Tabs.tsx、coin/BubbleMap.tsx | /api/holders/:mint、/api/bubblemap?mint=...；holders.js、holderslive.js、coin.js、bubblemap.js | 流水账与链上余额、RugCheck insider 网络、首笔资金来源及同区块/发射标签；最多四跳候选，非控制权证明 | **比此前估计成熟；不能再按“缺少多跳功能”直接移植外部项目** |
| ④ Dev/Creator 历史及关联 | Coin 的 Dev tab、top-dev 页面 | /api/coin/:mint 中 dev；server/coin.js、devboard.js、dev-identity.js、engine.js | 已观察的发行历史与 creator 候选；不等于完整实际控制者历史 | 优先确认源定义、时间覆盖与遗漏 |
| ⑤ 两类钱包观察 | Top wallets/Traders、Tracker 浮窗 | /api/wallets、/api/wallet/:addr、/api/wallet-page/:addr、/api/wtrack、/api/wtrack/feed；wallets.js、walletpage.js、wtrack.js | wallets/wallet_trades 与 wt_wallets/wt_feed/wt_transfers 是不同业务账本；时间、归属和唯一键可能不同 | 先比对重复/互补，禁止盲并 |
| ⑥ AI 研究、候选评分与自我复盘 | AiPicks、Narratives、Coin/AI tab；旧 Research.tsx 文件 | /api/research、/api/research/:mint、/api/picks、/api/narratives；triage.js、research.js、brain.js、grok.js | 交易候选、叙事、X/web 信息与结果 Playbook；不是项目目标自主演化 | 复用市场研究，不与 ai-d 项目研究角色混淆 |
| ⑦ 市场事件、价格与历史复盘 | Feed、Coin Chart、Practice、Health | /api/feed/*、/api/candles/:mint、/api/journal、/api/replay/:mint；journal.js、journalfeed.js、candlestore.js、coin.js | 原始/近原始成交、长期 K 线、近期钱包活动、缺口回补；保留期限不同 | 必须按证据类型评估时序能力 |
| ⑧ 账户/实盘交易/发币 | Account、Coin QuickTrade、Launch | /api/account/*、/api/v1/*、/api/launch/*；accounts.js、hosted-accounts.js、tradeapi.js、webapp.js | 真实资金动作/权限/付费风险；与当前只读市场调查无关 | 静态审查，**不执行、不默认授权** |
| ⑨ 运行、用户权限和服务恢复 | Health、Settings、API/MCP 文档 | /api/health、/api/settings、/api/stream；health.js、access.js、webapp.js、apicache.js、db.js、bin/supervise.mjs、worker/ | 缓存、单线程压力、断流/重启、SQLite WAL、Worker 身份与成本，可能隐藏实际数据年龄 | 决定以后运行安全和可靠性上限 |

**重要 UI 事实**：web/src/main.tsx 把旧 research、picks、signals、pulse hash 入口重定向到 Pulse；不能以 Research.tsx 文件存在就断言新站有可用 Research 主页面。Coin.tsx **实际嵌入** BubbleMapTab（含 side panel）、CoinTabs、QuickTrade；新整合应优先研究这几个已存在组件。

## 3. 单 Mint 业务纵切：已进入多个事实层

用户从 Discover 点击一个 Mint 后：
1. web/src/pages/Coin.tsx 读取 token、coin、trades、jup 的多个接口并订阅 SSE/LivePrice。
2. server/server.js 的 /api/token/:mint 在未知/未跟踪代币时可调用 lookupMint、adoptMint、vet；这是 GET **可能引起存储/外部请求**的例证。
3. /api/coin/:mint → coin.coinPage → build，从 token row、launchIndex、Holder Ledger、市场成交 ring、Jupiter、RugCheck、实时钱包/价格聚合，返回 holders/traders/early/dev/info。
4. 同一 UI 的 /api/holders/:mint → holdersFor 只返回 Blix 当前 trade-driven holder book；该 book 可能未从首笔开始，可能后续通过 getProgramAccounts 重新 seed，超过 SEED_MAX=6000 的币还可能不进行该类全量 seed。
5. coin.js 可能择优采用 chain live holder、Jupiter holder 或 RugCheck 统计；标签 source/partial/checked 的语义必须保留。coin.js 在使用 Jupiter holders 时可能产生 partial:false 的对象，这并不证明完整资金历史。
6. Coin/BubbleMap.tsx → /api/bubblemap：读取 coinPage 的 top holders，叠加 RugCheck 网络、funder trace、同区块及 launch 关联，实时显示候选群体。
7. Coin/Tabs.tsx 中的 AI read 可 POST /api/research/:mint，触发研究队列，可能消耗模型额度；**操作上只读调查不等于财务上无成本**。

**决策：** 之前增加的 mint-facts 仅使用 token + holders 两个接口，可以做初步来源报告，但它不覆盖上述 Coin 页面完整的 holders/Dev、bubblemap、钱包资金与价格信息。暂不扩建；先将真实源契约比对完再决定是否保留、改造或直接复用 Coin 原接口。

## 4. 重大新增发现：Blix 已有真实的多源关系图（P0）

[server/bubblemap.js](https://github.com/sunshihao001/grok/blob/blix/server/bubblemap.js) 当前包含以下**源码功能**：
- Top holders 原生来自 coinPage；必要时 RPC getTokenLargestAccounts + getMultipleAccounts，按 Owner 汇总部分 Token Account，且区分可能的 Pool/程序。
- 以 RugCheck insiders/graph 为候选网络（含中间地址），按约3分钟刷新；自建每个钱包“最早交易的转入 SOL/fee payer”候选 funder 存入 bubble_funders。
- 为查最早交易最多翻3页 getSignaturesForAddress（每页1000），成功判定后读取一笔最早交易；每日追踪上限 DAY_WALLETS=2500，单 Mint 初期重点追踪最多50个 holder。
- 从 transfer/funded/launch/block 四种候选边构图；避开部分已知交易所、资金 Hub 和分发钱包；最多穿透4跳；用生成树和聚类计算群体持仓比例。
- 可附加 Fomo 识别或按持仓数量近似匹配的个人档案；UI 标注来源且使用可视化。

**这些已经存在，不能把 PumpTrace、Million 或 Bubblemaps 的“同类功能”当从零开始需要构建。**

**但需要反证的专业边界**：
1. 最早可见交易的 payer/转入方 **不一定是经济控制者**；至多是资金关联候选。3页以内找不到的历史，代码用空字符串持久记录“已追踪但未找到”，可能使未来有更好历史数据时仍沿用负缓存（源码推论，未实测）。
2. “共享 funder”及“同区块首次买入”都允许公共服务或正常跟风的解释；代码的 HUB/DISTRIBUTOR 阈值可抑制已知误判，不能消除所有误归因。
3. 首次 RPC、RugCheck 和深度余额读取可能发生在 GET BubbleMap/coinPage 的后台，依赖外部配额；对静态接口权限的“只读”定义需要分开**不交易/无持久写入/无付费请求**三个维度。
4. 现有图更偏单 Mint 当前头部持仓关系；**跨 Mint 群体动态演化、资金净库存、完整多动作事件、真实归属证据**仍未由这段源码证明。
5. Bubblemaps/trench.bot 在 UI 中部分是外部链接或嵌入；不能据此断言已经融合其全部数据和算法。

**未来整合方向变化：优先核验已有 Bubble Map 的覆盖、误判和历史补查，再与外部成熟成品做“差异补足”，而不是移植第二个 Bubble Map。**

## 5. 两套 Wallet 路径与经济事实模型的区别（P0）

| 路径 | 核心状态 | 典型用途 | 丢失/推断风险 |
|---|---|---|---|
| server/wallets.js | wallets、wallet_trades、wallet_hits、winners | 已跟踪钱包的交易、PnL、Smart Money 和共同买入分组 | wallet_trades 主键 (sig,wallet,mint)，不能表示同签名同钱包同币的多次动作；历史轮询出现漏读会记 missed，但不代表补齐 |
| server/wtrack.js | wt_wallets、wt_feed、wt_transfers | 用户分组钱包监控、成交/转账活动和实时 Feed | wt_feed 唯一键 (wallet,sig,mint)，wt_transfers 按 (wallet,sig,mint) 去重；依赖解析的动作粒度；默认7天修剪 Feed 和 Transfer |
| server/bubblemap.js | bubble_funders + 缓存关系图 | 当前 Mint 的头部钱包共同资金/网络/群体持仓 | funder 是历史代理线索、最多四跳候选，来源并不保证完整 |
| server/walletpage.js | 可查链上钱包页面数据 | 非必须已关注的钱包信息展示 | 资料来源和资产覆盖仍须对照 |

wallets.js 的 clusters() 以过去3天“至少3个共同币且相距2分钟内买入”或部分共享 fee payer 进行群体合并；特殊共享付款地址做过滤，**不是确认经济主体同一**。一旦通过传递关系合并，也可能出现 A-B、B-C 有线索而 A-C 无直接关系的群体。

solana.js 的 parseSwaps() 用钱包净 SOL/WSOL/USDC/USDT 和非报价代币变化判断买卖；发现多个非报价 Mint 变化直接跳过。wtrack.js 的 parseTransfer() 从净额与其他 Owner/账户余额推测单个转账对手。这两类解析对于实用交易 Feed 有价值，但**不满足完整 Solana 经济事件（v0/v1、ALT、CPI、多腿、Token Account/Owner/Authority、SOL/WSOL 和费用）的还原标准**。

原项目已有部分 journal 去重：journal.js tradeKey(sig,mint,n) 允许同交易多条同 Mint 成交，且 test/journal.test.mjs 存在对应测试；但这**不能推导钱包账本或跨模块也保留了逐条腿**。要逐层查“原始交易事实 → 交易列表 → 钱包交易 → 关系图”，不能只看一个模块是否有去重。

## 6. 时间、完整性和持久化，决定专业研究边界

| 存储/表现 | 代码观察 | 对调查结论的影响 |
|---|---|---|
| journal.js j_trades + gap/repair | KEEP_MS=24h；部分 pump.fun/PumpSwap 成交；tradeKey(sig,mint,n) | 适合当日成交/价格回补，不等于所有交易场所全部转账历史 |
| candlestore.js / candleroll.js | 滚动汇总长期 K 线，异步 worker，能修复部分变更桶 | K 线保存价格和量，不会恢复完整签名/对价/钱包转移路径 |
| wtrack.js wt_feed / wt_transfers | FEED_KEEP_DAYS=7 | 7天内活动也受是否已观察/解析到的影响；更早活动不能靠此表恢复 |
| wallets.js wallet_trades | 按订阅钱包解析和去重，初始扫描与分页上限 | “没有交易记录”可能是没跟踪、RPC受限、解析跳过或真实无交易 |
| holders.js 内存 books + 重新 seed | genesis/partial/seeded；大 Holder 数和 RPC 限制影响全量快照 | partial:false 是该账本规则下的状态，不代表所有时间点完整 |
| webapp.js apicache.js | 缓存最长可能保留30分钟以保障页面在 Radar 故障时可显示；x-blix-age 暴露年龄 | **展示有值 ≠ 当前真实值**；需要同时传 source event time、received time、cache age |
| bubblemap.js lastGood/negative funder | 失败时最后图可作为 stale 回传，funder 的空结果持久化 | 图可能较旧或部分追踪，不能忽略来源 read/traced/last t |
| db.js / dbcheckpoint.js | SQLite WAL、独立 checkpoint、恢复与硬盘预算设计 | 生产真实故障证明需要关注长期存储成本；不能说“有 SQLite 就持久可靠” |

**反例意识**：6/12小时资金活动增加，可能是“资金准备”也可能是观察钱包成员增加、RPC恢复历史回补、供应商补数、Dust/公共服务、资金迁移、普通做市与正常交易。没有窗口覆盖、签名、实际净资产与对照基线，不能作确定性操盘归因。

## 7. AI 系统的真实上限：市场研究与项目演化需要分开

原生 triage.js → research.js → brain.js 形成“筛选 → 多源研究 → 评分/候选 → 15m/1h/6h/24h 事后追踪 → Playbook 自评修订”，并包括 narrative scout。**这已有比较完整的市场研究业务闭环**，不是简单空白 LLM 入口。

但 brain.review() 修改的主要是交易研究规则和参数，不自动完成：
- 用户目标在 G0–G4 的演化识别、重新定义与人类授权；
- 跨参考仓库完整分析、工程选型和真实测试；
- 完整链上经济事实与竞争机制的独立核查。

因此，“AI 全局协作能力”主要来自外部工作方式和 ai-d 的方法验证，**不能把其职责直接塞给原生 brain.js 的买卖评分 Playbook**。未来可复用 research 的证据收集和来源字段，但机制假设及产品战略必须另受事实和目标约束。

## 8. 工程与安全的跨路径矛盾（高优先级，静态确认）

- 当前 package.json 的 npm start 预先调用 scripts/read-only-audit.mjs --gate，默认阻断尚未隔离的旧主服务。但 **bin/supervise.mjs 直接 spawn server/server.js**，没有调用这个 npm 门禁；同一 supervisor 还可启动相邻目录的 blix-vault。**因此“npm start 被阻断”不是全启动路径安全证明**。
- server/server.js 在 listen 回调里集中启动数据抓取、市场研究、自评、多个 background task，并能自动改写设置，检测 Grok 订阅/计费；即使 UI 隐藏真实交易按钮，进程仍可能有其他副作用。
- server/webapp.js 动态 import accounts.js，账户管理与市场读请求共享进程/权限边界；/api/account/* 和 /api/v1/* 属于高风险业务范围。
- server/access.js 区分 visitor/member/owner，但成员某些路由允许交易、发币；权限检查是否覆盖所有网络入口，须分别检查 Worker、WebApp、Radar、MCP，不能只看 memberMay/visitorMay。
- 某些 GET 调用 coinPage、Bubble Map、tokenDetail 及市场数据补充会触发网络或存储/缓存变化，不意味着链上签名，却可能耗费付费供应商/模型额度。需将**链上不可写**、**本地不可写**、**不产生费用**和**服务可读取**四种约束分开。
- 2026-10-10 的原项目磁盘事件：历史文档记录 WAL 约16.2GB、磁盘满、约29次服务重启及后续 checkpoint/存储预算修正。属于 **AUTHOR_REPORTED_DEPLOYMENT_INCIDENT**，不是本分支已经完成云端可靠性测试。

**本轮严格未修改启动、交易、网络、钱包或任何运行代码。**

## 9. 静态测试定义也发现需要修复的版本冲突

- package.json 目前 npm test 明确列出49个测试文件，仓库树中均存在；这里只证明**文件路径一致**，不证明测试执行/全部通过。test/journal.test.mjs 中确有 journal 同事务多动作、断流修复等专项测试。
- 当前 docs/project/state.json 的 next.SAFE = STATIC_AUDIT_ONLY_NO_RUNTIME、next.MINT = PAUSED_UNTIL_USER_AUTHORIZES_EXECUTION，而 test/project-goals.test.mjs 仍断言旧值 STATIC_AUDIT_BLOCKED 和 NOT_RUN。**静态文本已相互矛盾**；未来测试执行前应更新测试预期，而不是撤销用户“暂停运行”的决定。
- GitHub Actions 的 test.yml 对 main push 和 pull_request 运行；不能推定 blix 普通 push 自动跑了完整 test。
- 本轮未运行 npm、Node、GitHub Actions 或 Blix。测试定义与历史作者记录只代表各自的证据级别。

## 10. 未来外部成熟成品的正确比较入口（研究候选，不是已经完成集成）

| 外部参考 | 原本想借鉴什么 | Blix 目前已具备什么 | 真正应调查的差异 |
|---|---|---|---|
| Million | 钱包发现/跨币关系/资金路径 | wallets + wtrack + bubblemap 三条已在 | 历史回补、跨 Mint 动态群体、逐事件对价和库存、成本、安全 |
| PumpTrace | Creator/首发和多跳历史 | Coin Dev / bubblemap 已有首笔 funder/四跳候选 | 是否能查询超出前三千签名、延伸至中间出资人、对照可证伪控制线索 |
| HoldTech / Bubblemaps | 同槽/持仓集中/关系群体 | Bubble Map、Holder 账本、Pool 排除、外链 | Slot 与真正 Bundle 区分、关联证据、供应口径、历史跨度 |
| Pulse | 整体可运行市场分析、数据摄取/恢复 | Blix 已有完整 Discover、Pulse、Journal、UI | 数据覆盖、故障恢复、部署成本；不按名称合并同类 UI |
| OKX、RugCheck、Jupiter | 成熟数据/业务接口 | 原生已使用部分 RugCheck/Jupiter 等数据 | 外部字段定义、API/费用/配额、历史可用性、同一字段多源冲突 |
| Hermes、qb-、meme-、Why-Solana | 资金循环、钱包角色、行为经济解释、反证 | 原生有部分快速 heuristic | 哪些专业问题能改变已有事实归因和决策；不复制整个旧架构 |
| ai-d | 目标演化、知识选择、专家问题表征、项目自我纠错 | 原 brain.review 为交易研究 Playbook | 区分业务研究 AI 与工程协作 AI，实际任务能否提高判断与交付 |

上表是**依据当前 Blix 源码划分的对照问题**，并非对外部项目最新版的重新运行或逐行核查。下一步只有在差异可能改变整合决策时才追查这些上游来源。

## 11. 最重要的结论、反证和路线变化

**已确认（SOURCE_READ）**：
1. Blix 是一个复合产品：前端双路径、Radar、WebApp/Worker、钱包账户/Vault、数据库与多条市场/AI业务。
2. 单 Mint 已有 Coin 页面、持仓多源优先级、Dev、Bubble Map 多跳关系候选、实时价格和交易、AI read。
3. Wallets、wtrack、Bubble Map 和 Journal 是不同事实账本，不可直接视为一个统一的经济事件数据库。
4. 现有部分链上解析/存储粒度不能保证多动作交易和全历史钱包资金路径。
5. 启动路径与状态测试断言存在静态不一致，不能用“已有保护文件”替代整体安全结论。

**竞争解释与需要推翻的假设**：
- “功能多”不代表“专业经济调查完整”；反之，某些原生关系图功能已远超先前假设，盲目移植成熟项目可能降低价值。
- 钱包关系图的资金路径可能来自共同控制、共享服务、公开跟单、交换/归集和数据错配；必须让证据推翻不合适解释。
- 按需加载 intelligence 模块便于增量研发，但不能解决早期交易事实丢失、权限绕过或供应商覆盖；**扩展层不是应先行扩建的固定答案**。

**暂时未知（UNKNOWN）**：真实用户路径在当前可运行部署中的可达性、UI 与数据全部字段契约、跨交易场所覆盖率、完整经济事件重建能力、真实网络费用、长期数据库规模、云电脑部署安全、相对外部成熟方案的实际性能。不能凭文档补齐。

## 12. 下一项研究，按照信息价值而非机械阶段

**优先 A｜把单 Mint 核心事实与关系图彻底对齐（只读研究）**：从 UI CoinTabs/BubbleMap/Dev → 所有 API → source/partial/checked/time → Holder Ledger/Owner → funder/4-hop → wallet_trades/wt_transfers → journal gaps。输出一份字段口径与重复/缺失关系表，明确哪些结果能直接用、哪些必须补底层事实。

**随后 B｜以市场发现和跨 Mint 监控为横轴**：审查多发行平台和多 Pool 的进入/迁移、候选丢失、钱包来源/成员演化及断流回补，检查 A 的问题如何放大为跨币误判，而不是单独新增一个功能。

**并行关键风险审查 C｜所有启动和数据权限路径**：审查 supervisor 绕过安全门禁、GET 的额度/后台副作用、用户与账户隔离、状态测试不一致。此处为静态结论，不运行和不改代码。

**决策触发条件**：在知道原生 Bubble Map、Coin 聚合和钱包账本的实际数据契约后，再决定新能力应通过原接口、按需扩展层、独立历史查询服务还是成熟项目整用。新证据可能深化 G2 或推翻某条 G3 技术路线，**不自动替换用户的 G0/G1**。

**本轮新增认知**：我们最需要建设的不是“更多钱包工具”，而是**同一经济调查对象跨源、跨时间、跨账本的事实一致性与可反证解释**。它既减少重复开发，也直接决定业务输出的可信程度和未来长期研究的上限。

## 13. 源码回查索引（供下一轮 AI 精确回到问题）

- 产品路由：[web/src/main.tsx](https://github.com/sunshihao001/grok/blob/blix/web/src/main.tsx)；[web/src/shell/Rail.tsx](https://github.com/sunshihao001/grok/blob/blix/web/src/shell/Rail.tsx)
- Coin 使用路径：[web/src/pages/Coin.tsx](https://github.com/sunshihao001/grok/blob/blix/web/src/pages/Coin.tsx)；[server/server.js](https://github.com/sunshihao001/grok/blob/blix/server/server.js)；[server/coin.js](https://github.com/sunshihao001/grok/blob/blix/server/coin.js)
- 原生关联网络：[server/bubblemap.js](https://github.com/sunshihao001/grok/blob/blix/server/bubblemap.js)；[web/src/pages/coin/BubbleMap.tsx](https://github.com/sunshihao001/grok/blob/blix/web/src/pages/coin/BubbleMap.tsx)
- 钱包/持仓与原始交易：[server/holders.js](https://github.com/sunshihao001/grok/blob/blix/server/holders.js)；[server/wallets.js](https://github.com/sunshihao001/grok/blob/blix/server/wallets.js)；[server/wtrack.js](https://github.com/sunshihao001/grok/blob/blix/server/wtrack.js)；[server/solana.js](https://github.com/sunshihao001/grok/blob/blix/server/solana.js)
- 交易事件与保留：[server/journal.js](https://github.com/sunshihao001/grok/blob/blix/server/journal.js)；[server/journalfeed.js](https://github.com/sunshihao001/grok/blob/blix/server/journalfeed.js)；[server/candlestore.js](https://github.com/sunshihao001/grok/blob/blix/server/candlestore.js)
- 服务/权限/测试：[server/webapp.js](https://github.com/sunshihao001/grok/blob/blix/server/webapp.js)；[bin/supervise.mjs](https://github.com/sunshihao001/grok/blob/blix/bin/supervise.mjs)；[server/access.js](https://github.com/sunshihao001/grok/blob/blix/server/access.js)；[test/project-goals.test.mjs](https://github.com/sunshihao001/grok/blob/blix/test/project-goals.test.mjs)
- 原作者历史背景：[docs/HOW-IT-WORKS.md](https://github.com/sunshihao001/grok/blob/blix/docs/HOW-IT-WORKS.md)；[docs/incident-2026-10-10-disk-full.md](https://github.com/sunshihao001/grok/blob/blix/docs/incident-2026-10-10-disk-full.md)

**注意：索引是重新研究的定位入口，不是让未来模型一次全量读取全部文件。研究时按问题选择最有信息价值的路径。**


## 14. 2026-11-13 补审｜交易机会优先：原版选币闭环 × AI 专业调查 × 可跟随性

**用户目标纠偏**：最终同时需要「值得调查的代币」与「有实际交易机会的代币」，明确以后者为主；前者是来源之一和按需深度调查支撑，不把知识分类变成固定业务筛选关卡。本补审是 `blix` 及PR #23源码静态审查，**不是市场运行、策略有效性或盈利证明**。

**锁定审查基线**：`blix@58bbff4ff8915c627ada820175cd96b8f1fd64a8`；PR #23 集成候选审查起点 `c58f612848f219008e5b5a6354f5d2559a1ef6b8`，仍Draft，`mergeable=false`。之前章节的2026-11-06快照只是历史结论，不覆盖本节源码更新。

| 市场任务 | 原Blix复用位置/可见行为 | 证据与真正需要核验的事情 |
|---|---|---|
| 发现候选及初筛 | `Coins.tsx` Discover热榜、新币/已迁移池、mcap/liq/vol过滤；`Pulse.tsx` New Pairs/Final Stretch/Migrated、rugGuard；`engine.js` nursery/来源/信号/结果 | 数据源实际发现率与断流漏失、过滤前全集和过滤后样本都须留存；UI过滤不等于安全或正收益 |
| 从大量新币选择值得研究的对象 | `triage.js` 快速规则+LLM slop/meh/maybe/promising；live buyers可覆盖低评分；`pulse.js` traction 排名与热度触发AI队列 | 拒绝只按叙事或LLM打分；需要看不同进入路径的成本、漏检和候选基数 |
| 早期与趋势交易机会 | `early.js` 30/60/120/300s检查点、按时间70/30训练/测试、门限；`research.js` 借traction与经济/叙事事实作判断；`brain.js` pickGate/earlyPick/entryBlock/entry_watch/退出复盘 | `early.js`“unseen 30%”是源码策略而非外部复验：最终模型再用全部样本拟合，阈值来自训练样本；需要独立后续时间窗、明确候选全集及当时可用特征。LLM pWin为模型判断，不能直接当校准概率 |
| 钱包跟随机会 | `wallets.js` smart money发现、钱包监控、wallet_trades；`WalletTracker.tsx`观察、快捷交易入口 | 上游钱包交易时间≠跟随者首次看到信号时间；旧交易解析同签名折叠、漏捕获与共享funders会产生误报 |
| 交易可行性、报价与成本 | `brain.js` 默认固定每边3%成本、按mcap比例模拟出入；`rules.js` 规则网格及walkForward；`paper.js` 用户纸面台使用曲线/路由真实报价逻辑 | **两种纸面机制不可混称**：brain的固定成本/市值代理 ≠ 真实可成交报价、深度、滑点、延迟与失败；`rules.js`过历史价带不等于已进行全策略实盘验收 |
| 反馈与历史反证 | `engine.js` Signals 15m/1h/6h/24h，`brain.js` outcomes/evidence/scorecard/playbook，`early.js`胜者发现 | 价格上涨幅度、触及2x先于-40%、纸面退出正收益、realized PnL是**四个不同标签**，不可互换；缺失报价/被淘汰候选可能形成幸存者偏差 |
| AI扩展已有边界 | PR #23 `ai-workflow.mjs`仅一个指定Mint、最多两个已批准只读能力调用；`followability-replay.mjs`检查用户提供纸面收据的可跟随性；Coin助手仍预览未连模型 | 不能将单Mint工作流冒充全市场自主机会Agent；**复用现有followability门禁**，其目前不生成历史可执行报价或验证Alpha |

**重要纠正**：
1. 原版`brain.js:188-216`的 `pickGate` 已默认 `aiInGate=false`，注释记载历史126次候选中AI buy/avoid反向表现。样本和数值未独立复核，不能宣称现有策略胜过基准，但更不能把AI评分再次作为统一购买决策真值。
2. `server/early.js:186-216`具有时序留出与门限检查，属于应复用的工程优势；仍需后续滚动时窗、特征时间可得性、样本缺失、selection bias、模型更新时点的外部复核。
3. `server/brain.js:487-503`部分历史胜率分组以纸面收益倍数>1.15计“win”；`server/early.js:36-39`的WIN则是30分钟内「先到2x还是先跌40%」。不要在UI或AI中把这两套指标混成同一概率。
4. React `web/src/main.tsx:193-205`已将旧 `signals/research/picks` 路由重定向到Pulse，`ai-picks`独立入口仍在；不能按源文件名认定旧Signals/Research在新UI可直接访问。
5. 原版 `server/paper.js`的按曲线/路由报价纸面交易与`brain.js`固定3%代理应建立可复查对照，不以旧条件获胜替代“用户可在信号出现后复制”的证据。

**下一项最高价值的单一工程验收（建议，尚未实施）**：
- 冻结同一段历史市场时间窗，在原Discover/Pulse/early/triage/brain产生的**全候选集合**上，保留「被观察→被过滤→入研究队列→发出信号→首次可见→可得报价→纸面进/出→结果」各时间和来源；包含未入选和失败样本。
- 在**原有**`brain`+ `rules`+ `paper`的数据契约上，以PR #23 `followability-replay`的明确时序/报价/费用/库存/缺失拒绝语义为门禁，比较至少三类来源：早期信号、traction趋势、钱包跟随；不新建第二个行情扫描器或交易引擎。
- 必须分别报告「潜在机会候选率」「历史信号覆盖/延迟」「可成交纸面收据覆盖」「扣费用的结果分布」「实际未被证明之处」；以未入选的同窗口候选或简单规则为对照，以后续独立时窗为样本外。示例收据/静态CI不能替代历史市场收据或正期望。
- 先选一个明确的失败反例：信号时点后无法获得有效报价，或已有候选价格上涨但真实卖出流动性不够。测试应**拒绝计算可交易收益**，而不是给出漂亮的价格倍数。成功后才评估AI按需调用钱包经济证据是否改善对照结果。

**当前动作边界**：本节仅补充审查/执行约束；没有修改原Blix选币阈值、信号、主服务、订单、钱包、模型或付费调用，也没有替PR #23解决合并冲突。保持原版完整产品与只读独立研究环境的区别。
