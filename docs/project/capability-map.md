# Blix 产品地图与外部能力的正确补全

**从目标出发选择能力**：[《参考成品逆向构建的多层目标体系 V0.1》](reference-driven-goal-model-v0.1.md)说明不同参考项目原始目的、同一Blix多种业务目标、市场参与者及专业视角、现有模块承接与验证出口。本表继续只负责具体产品能力和源码落点，不重复目标图，也不意味着表中功能均已集成。


**源码已确认存在 ≠ 本项目已运行验收。** 不预设要把所有参考仓库复制进来；优先完整复用已有接口或方法。

| 用户问题 | Blix 当前源码入口 | 真实缺口/需核查 | 最有价值的外部参考 |
|---|---|---|---|
| 找到值得调查的新币并过滤明显风险 | `server/engine.js`、`server/coin-screen.js`、`server/quality.js`、原 Pulse/Discover UI | 风险筛选不等于非诈骗保证；数据覆盖与筛选代价 | Pulse、OKX、RugCheck、pumpwatch |
| 对真实 Mint 查 Creator、Holder、早期资金 | `server/wallets.js`、`server/holders.js`、`docs/API.md`、Coin Sheet | Token Account/owner、Pool/LP、Creator历史、同槽不等于Bundle | PumpTrace、HoldTech、旧 qb- |
| 钱包买入、转仓、新接收地址卖出 | `server/wtrack.js`、`server/wallets.js`、`server/solana.js` | 原始交易/CPI/多动作、资金净变化、SOL/WSOL、多跳公共Hub | Million、Why-Solana、FnZero、Hermes |
| 横盘前6/12小时钱包群体活动异常 | `server/journal.js`、`server/journalfeed.js`、`server/health.js` | Journal默认仅保存约24小时的部分池交易；不同场所和历史完整性、群体成员基线待验证 | Helius、Bitquery、PumpTrace Backfill、Blix本身的缺口修复 |
| 跨 Mint 追踪群体成员、接力与重复 | 现有钱包订阅与 Smart Money 发现 | 动态群体成员、历史资金路径、库存关系及跨币重复仍需完整业务验证 | Million、旧 Hermes、Why-Solana |
| Grok/AI 判断异常与潜在经济机制 | `server/ai.js`、Research、Picks、现有报告 | 区分原始事实、竞争性解释、反证、样本外预测与执行成本 | ai-d、meme-、D01–D12、PumpGrok 治理 |
| 产品管理、UI、稳定性和安全 | `server/server.js`、`web/`、`public/`、`server/health.js`、`docs/API.md` | 只读/自动研究付费隔离、外部API、Node>=24.16、云电脑休眠 | 原 Blix 事故记录、Pulse、PR #17 UI 设计 |

**已有 UI 优先**：Discover / Pulse / Trackers / Signals / Research / Health 等是真实产品入口；深化调查优先为 Mint/钱包详情中的可展开证据，不因概念图新建六个页面。原 UI 规范见 `design.md` 和 `web/src/shell/Rail.tsx`。

**参考资产可提供五种价值**：业务功能、算法方法、工程设计、专业经济解释、失败教训。跨语言可调用服务不等于必须翻译源码；若数据口径或许可不兼容，先标明阻断。完整参考范围仍指向原 [65项资产登记](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json)，后续新增项目应补充来源而不是删掉旧条目。

## 2026-11-14｜能力地图的当前解释：原版与AI扩展各尽其责

[专业知识D01–D12主述](../../knowledge/README.md#2026-11-14全域专业归位总入口十二领域主述参考来源知识身份与产品验收)已统一每种市场事实/资金/策略/AI领域的知识责任；[扩展产品成品路线](intelligence-layer.md#2026-11-14成品化实施主线知识已经归位之后)负责将源码和真实验收挂到现有业务入口。历史“仅`mint-facts`且未接UI”是2026-11-06截面：当前PR23已有`mint-economic-evidence`、知识加载、`ai-workflow`、本地HTTP/SQLite预检、Intelligence页面和Coin深链接；没有完成主网单Mint/交易机会/长期监控运行。

| 分工责任 | 已存在能力 | 优先验收与不得重做 |
|---|---|---|
| **原版Blix市场数据与初筛** | `engine`、`sources`、`early`、`triage`、`quality`、`research`、`brain`、`wallets`和Pulse | 先同源候选/被拒/首可得/断流事实，不另造AI扫描器 |
| **原版证据与存储** | 原SQLite、钱包/交易历史、部分Holder/Pool/BubbleMap | 同一个Mint/时窗核数据完整与角色语义；源端缺口原位置修 |
| **专业AI只读** | `server/intelligence`、本地HTTP、有限知识/工具、经济索引只读 | 只在明确Mint/权限/预算下按需调用，不签名、交易、自动收费 |
| **用户操作界面** | Coin→Intelligence深链、原Wallet/原图表与AI工作台 | 处理不在Pulse看板中的任意Mint、不误选；本机4421/4547可交互 |
| **实证与成品效果** | 原版/扩展离线回归、隔离冷启与重启、纸面拒绝不当交易 | 实Mint端到端、模型对照、真实时效/报价、Case长期修订及远端授权运维 |

**保留原则**：交易、账户、原AI、Paper、部署功能是原版产品资产，不能为AI研究权限隔离而删除。AI模型无权越过原版启动门禁、调用不安全GET的隐含副作用、任意付费外部源或凭知识文本创建交易指令。

## 扩展层实际落点（2026-11-06）
当前只增加 **一个** 统一扩展层 [server/intelligence](../../server/intelligence/index.mjs)；第一个能力为 Mint/Holder 事实读取，详见 [渐进式整合说明](intelligence-layer.md)。已具备按需加载入口、allowlist、来源与 UNKNOWN、独立单测；**尚未接入运行中的 UI/服务器，真实数据和安全启动未验收**。
