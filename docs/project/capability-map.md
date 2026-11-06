# Blix 产品地图与外部能力的正确补全

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

## 扩展层实际落点（2026-11-06）
当前只增加 **一个** 统一扩展层 [server/intelligence](../../server/intelligence/index.mjs)；第一个能力为 Mint/Holder 事实读取，详见 [渐进式整合说明](intelligence-layer.md)。已具备按需加载入口、allowlist、来源与 UNKNOWN、独立单测；**尚未接入运行中的 UI/服务器，真实数据和安全启动未验收**。
