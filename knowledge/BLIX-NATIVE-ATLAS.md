# Blix 原生知识与产品能力总图 V0.1

> 2026-11-06 | 主体 `sunshihao001/grok@blix`；本文件先梳理 **Blix 自己已经拥有的知识、实现与证据边界**，不从旧 Grok 反向规定 Blix 的目录。基于 GitHub 目录/代表性源码/原产品文档与已有跨层审计的静态核查；**没有启动服务、链上实测或云电脑验收**。使用时须对照当时的 Git 提交复查更改。

## 1. 先把“Blix 自身知识”理解成四类来源

- **原生产品事实**：`README.md`、`docs/HOW-IT-WORKS.md`、`docs/API.md`、`design.md` 与可达 UI（React + 经典 `public/`），回答“已有产品声称做什么、用户在哪里看到”。原作者说明属 AUTHOR_REPORT，和源码事实分层。
- **可观察实现**：`server/` 核心 Node.js、`web/src/`、`worker/`、`mcp/`、`bin/`、`scripts/`，回答“数据/处理/缓存/任务/授权/显示究竟经过什么”。代码存在不等于已经云端实跑成功。
- **经验与证据**：`docs/` 里的真实事故、供应商配额/延迟/报价异常经验，`test/` 的离线反例与断言，`docs/project/` 的本项目源审与疑点。测试定义不等于全部通过、更不等于链上复现。
- **迁入的研究**：`knowledge/` 当前六类文件是旧 Grok/Hermes/ai-d 等**外部于 Blix 原产品的研究副本**。这些研究必须清楚标出原来源，不可冒充原 Blix 算法或事实。

## 2. 原生产品的业务知识地图：从用户界面到真实模块

| 业务面 | 已有 UI/入口 | 代表性模块 | 原生知识与需要保持的界限 |
|---|---|---|---|
| **市场发现与过滤** | `web/src/pages/Pulse.tsx`、`Coins.tsx`、`Launch.tsx`、`Picks.tsx`、`Feed.tsx` | `server/engine.js`、`pulse.js`、`firehose.js`、`quality.js`、`rules.js`、`poolwatch.js` | 发行/成交/价格/筛选/评分/预警如何流动；原作者的“安全筛选”不是全市场准确率证据 |
| **单 Mint 详情与历史** | `web/src/pages/Coin.tsx`、`coin/`、`Devs.tsx` | `coin.js`、`coinindex.js`、`early.js`、`creator.js`、`cointape.js`、`coin-flow.js`、`pumpswap.js` | Mint/Creator/Pool/交易/余额/迁移关联；不同供应商和历史窗口不可默默合并 |
| **持仓与钱包关系** | Coin 内 Holder/Bubble Map；`Wallets.tsx`、`Trader(s).tsx`、`Tracker.tsx` | `holders.js`、`holderslive.js`、`bubblemap.js`、`wallets.js`、`wtrack.js`、`clusters.js`、`walletpage.js` | Token Account 与 Owner、池和公共设施、同源候选与真实出资、钱包群体不能混为现实共同控制 |
| **群体/叙事与观察** | `Narratives.tsx`、`XTracker.tsx`、`Research.tsx` | `narratives.js`、`xtrack.js`、`journal.js`、`journalfeed.js`、`notify.js`、`health.js` | 观察事件、异常、时序、告警状态；监控缺口和历史回补不能等同“无活动” |
| **AI 与候选研究** | `AiPicks.tsx`、`Research.tsx` 及 Coin 中 AI 入口 | `ai.js`、`grok.js`、`triage.js`、`research.js`、`brain.js`、`running-ai.js` | 原有 AI 偏市场候选与报告；它们并不等同用户所要的全业务自主知识选择系统 |
| **行情与执行经济学** | 原 `Trader.tsx`、`Practice.tsx` 及经典交易页面 | `jup.js`、`jupiter.js`、`quote.js`、`price-sanity.js`、`fee-ledger.js`、`paper.js`、`tradeapi.js`、`txtrade.js` | 价格/报价/滑点/费用/持仓与成交结果的口径；**现阶段只读研究，不启动签名、广播、自动交易或自动付费** |
| **研究数据接口** | `docs/API.md`、`mcp/blix-mcp.mjs` | `server/server.js` HTTP/SSE、`public/mcp-tools.js`、`server/intelligence/index.mjs` 与 `mint-facts.mjs` | 已有 HTTP 和工具清单；MCP 只开放其过滤的读取工具，不代表下层 HTTP 服务自动隔离所有写功能 |
| **身份、部署和运维** | `Account.tsx`、`Settings.tsx`、`More.tsx` | `server/accounts.js`、`access.js`、`webapp.js`、`db.js`、`dbcheckpoint.js`、`apicache.js`、`heliuskeys.js`、`worker/index.js`、`bin/supervise.mjs` | 本地/托管身份、数据库、RPC 限流、缓存、备份与更新；**Grok 云电脑持续运行能力尚未验收** |

这些是**源码/产品的导航映射**，不声称这里每个页面已在当前 fork 可直接访问，或者所有API已真实运行成功。细节可回查 [全主体跨层审计](../docs/project/whole-product-cross-layer-audit-v0.1.md)、[原生产品说明](../docs/HOW-IT-WORKS.md)、[API](../docs/API.md)。

## 3. Blix 自身已经积累的专业知识：不应被旧资料覆盖

### 3.1 数据事实与指标语义
- 价格、池深度、市值、报价、池选择、买卖笔数、Holder 及净额不是同一个事实层；`coin.js`、`holderslive.js`、`chart*`、`pool-identity.js` 等分别处理。
- `docs/HOW-IT-WORKS.md` 区分**价格回访**与真实利润：15m/1h/6h/24h 的 track record 没有真实成交、滑点和费用，不能当净收益。空池异常价格被隔离，属于有价值的原生工程经验。
- 原文明确“Early wallets”属于启发式；Blix `bubblemap.js` 已尝试过滤公共资金 Hub/交易所，并读取 RugCheck 网络。**仍有 Fee Payer 候选资金边与历史截断负缓存的静态风险**，见 [跨模块事实审计](../docs/project/mint-cross-module-evidence-audit-v0.2.md)。
- 不同界面使用的 Holders 口径、Pool 分母、事件窗口和历史完成度存在潜在差异；不从来源不足处推断实际经济主体。

### 3.2 产品质量与失败经验
`docs/` 含 `incident-2026-10-10-disk-full.md`、`chart-quote-incident-2026-10-11.md`、`chart-reliability-2026-10-11.md`、`jupiter-shared-quota-2026-10-12.md`、`metric-freshness-plan-2026-10-10.md` 等。这是 Blix **自己**的故障与设计资产；优先在 `docs/` 保留真实记录，不搬进旧 Grok 的“专家”分类。关联工程知识时引用原始文件和数据源时间。

### 3.3 测试与执行状态
`test/` 已有行情、钱包、Journal、费用、历史、RPC 限流、checkpoint、备份、API/安全、UI 数据等测试定义；`package.json` 提供 `test`、`test:intelligence`、`test:research-safety` 等命令。**本次只看了定义和目录，没有运行测试**。默认 `npm start` 增加 `scripts/read-only-audit.mjs --gate`，这是静态阻断而不是证明运行只读。

### 3.4 原生 AI 能力与用户要的 AI 能力不同
- 已有 `server/brain.js` / `research.js` / `triage.js`：市场筛选、候选分析与研究输出等既有流程，不能因此称作“全领域认知已内化”。
- 增量 `server/intelligence/index.mjs` 现只列出懒加载 `mint-facts`；`mint-facts.mjs` 只从本地 Token、Holder API 形成观察结果、来源和未知边界，不具备自动全库知识检索与交易资金完备性。
- `AGENTS.md` 与 `docs/project/` 指导项目目标与查阅顺序，是**工作说明**，不是新的实际模型训练或服务。
- 用户目标是只用 Blix，让 AI 以口语意图主动选相关知识和已有能力；此目标应作为未来接入的判断基准，不应倒过来改变 Blix 原生事实。

## 4. Blix 应拥有的两张互补知识地图

**A. 原生能力地图（本文）**：用户问题 → 现有页面/API → `server/` 处理 → 来源/缓存/历史 → 何种事实可信 → 已有测试/缺口。它反映 Blix **现有能力**，而不是旧专家体系。

**B. 专业研究地图（现有 `knowledge/`）**：研究原文按 `foundations`、`mechanisms`、`methods`、`cases`、`ai`、`references` 六种用途分类；`MIGRATION.json` 保留每份副本的原仓库、路径、blob SHA。此地图反映**迁入知识**，不是原生代码。

二者通过 [Blix项目知识使用](../docs/project/knowledge-use.md) 和 [旧研究152项业务路由](../docs/project/legacy-knowledge-routing.v1.json) 关联，不能互相取代。

## 5. 目前了解到了什么、还不能说什么

| 事项 | 来源状态 |
|---|---|
| 主要产品/页面/代码/数据/AI/工程路径 | SOURCE_READ + 既有跨层静态审计；不是全文件逐行审阅 |
| Blix 原作者已写的业务规则、错误边界及事故记录 | AUTHOR_REPORT / SOURCE_READ；未统一重放实验 |
| 当前 `knowledge/` 分类与旧资料来源追溯 | 已建目录和 `MIGRATION.json`，需要依据最新分支核对新增文件 |
| 所有 API 与数据源在 Grok 云电脑运行稳定 | UNKNOWN，未部署/未验收 |
| 不含签名、交易与付费的实际安全运行 | UNKNOWN，静态门禁不能代替权限强制隔离 |
| 旧知识已让 Blix 真实分析能力提升 | UNKNOWN，尚未实证对照 |

**下一步顺序**：读取 [旧 Grok 自身目录与知识原点](OLD-GROK-ATLAS.md)，然后看 [两套体系如何对应、哪些应迁入](INTEGRATION-CROSSWALK.md)。先理解来源，不在本阶段改 Blix 业务代码。
