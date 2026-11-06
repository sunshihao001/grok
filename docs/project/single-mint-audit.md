# 单 Mint 深度调查｜Blix 现成能力与缺口登记（2026-11-06）

> 当前为静态源码路径审查，不是实际 Mint 调查报告；**严禁把 Blix 原生 Holder 标签直接升级成经济主体身份。**

## 已知产品入口

| 用户动作 | Blix 现有入口 | 所需进一步核验 |
|---|---|---|
| 在市场候选中找到 Mint | `server/engine.js`、`server/coin-screen.js`、`/api/tokens` | 发现与筛选覆盖、候选新鲜度 |
| 查看 Mint 基本调查 | `/api/token/:mint`、`server/coin.js`、`/api/holders/:mint` | Pool/LP、owner与Token Account、报告时间 |
| 查询关联买入/交易 | `server/wtrack.js`、`server/wallets.js`、`/api/wtrack/feed` | 同一交易多 Token 动作；历史分页与签名完整性 |
| 检查市场事件和历史 | `server/journal.js`、`/api/journal`、`/api/signals` | Journal约24h且仅部分venue，不代表12h所有资金转账 |
| 查看现有研究 | `/api/research`、`/api/research/:mint`、`server/research.js` | AI结果来自什么数据、有无公开引用与反证 |

## 必须补充的能力（来源与优先级）

1. Creator/同源资金：PumpTrace 现成调查和回填优先；发起者、fee payer、owner 不能混为一人。
2. Wallet → Mint → Wallet 双向发现：Million 现成服务；对同一交易多个订阅钱包需要完整核验。
3. Bundle/持仓集中：HoldTech、OKX、Bubblemaps 作为相互校核；同Slot≠确认的Jito Bundle。
4. 资金/库存多跳及跨 Mint 行为：Why-Solana、旧 Hermes/qb-/meme-、FnZero 方法；公共 Hub、Dust、SOL/WSOL 及Token-2022 必须单独处理。
5. 6h/12h 异常：优先验证 Helius/Bitquery 是否能查询完整历史，保留查询游标、时间覆盖、事件位置、数据缺口、净库存变化及群体成员演化。

## 决策优先级

**先保留 Blix 原 Mint 页面和数据库**，将额外事实通过完整只读业务服务/API 交付。若需要后续内置，必须证明接口复用无法满足完整业务需求，再最小改造。未获安全验收不得启动主服务或调用需要费用的API。

## 下一步可推翻条件

- 如果 Blix 的原生 Mint 路由不能在严格只读和无额外费用环境中获取有用数据，就不能直接宣称该业务已运行。
- 如果外部服务无法提供完整历史或结果口径不一致，就保留 UNKNOWN，不能编造“内幕群体占比”。
- 如果一次真实 Mint 调查可以完全借助外部成品/API 完成且低成本，优先避免新增同类解析器或数据库。
