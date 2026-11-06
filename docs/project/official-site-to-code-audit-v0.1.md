# Blix 官方功能 → 业务 → 工程源码核对 V0.1

日期：2026-11-06。此文为公开网页搜索与当前Blix分支源码的交叉研究，不是产品实跑。[官网完整113个规范页面目录](blix-public-pages-catalog-v0.1.md)；在线页面 https://blixvip.com/ 、https://blixvip.com/tools 、https://blixvip.com/guides 。

## 1. 产品定位
官网将Blix描述为发现(Discover) → 研究(Research) → 交易(Trade)。我们的目标进一步覆盖市场发现、单Mint资金与库存调查、跨Mint群体变化、经济机制与反证，以及可靠只读监控。原Web界面可以保留，交易和发币不在当前授权范围。

## 2. 功能—代码—认知差距

| 官网与功能 | 源码/业务路径 | 对今后整合的启发 |
|---|---|---|
| [Pulse、新币](https://blixvip.com/pump-fun-tracker)、[Screener](https://blixvip.com/solana-memecoin-screener) | web/src/pages/Pulse.tsx、Coins.tsx；server/engine.js、pulse.js、quality.js | 已有可复用市场发现；要测漏检/多池/价格新鲜度 |
| [Mint分析](https://blixvip.com/meme-coin-analyzer) | Coin.tsx、server/coin.js、holders.js、jupdisc.js | 已有Coin页面；注意Holder来源、时间及覆盖差异 |
| [风险扫描](https://blixvip.com/memecoin-risk-scanner) | quality.js、holders.js、snipe.js | Bundle/Dev/sniper是启发式候选，不是验证的共同控制 |
| [关联Bubble Map](https://blixvip.com/meme-coin-analyzer) | server/bubblemap.js、coin/BubbleMap.tsx | 已有RugCheck关系、首笔funder、四跳候选及公共Hub排除；不重复造轮子 |
| [钱包](https://blixvip.com/solana-wallet-tracker)、[PnL](https://blixvip.com/solana-pnl-tracker) | wallets.js、wtrack.js、walletpage.js、solana.js | 已有观察及盈亏，但多动作和历史窗口限制经济资金重建 |
| [AI/Picks](https://blixvip.com/ai-memecoin-picks)、[Narratives](https://blixvip.com/memecoin-narratives) | research.js、triage.js、brain.js、desk.js | 现有AI主要为市场交易研判；项目目标演化不是同一功能 |
| [警报](https://blixvip.com/memecoin-alerts) | server/server.js、wtrack.js、health.js、通知模块 | 有规则/通知但全天完整监控、历史回补尚未验证 |
| [API](https://blixvip.com/solana-api)、[SSE](https://blixvip.com/pumpfun-realtime-api)、[MCP](https://blixvip.com/mcp) | public/api-docs.js、public/mcp-tools.js、mcp/blix-mcp.mjs | Grok Bot可优先直接调用结构化只读接口；SSE无完整回放合同 |
| [交易API](https://blixvip.com/trade-api)、[发币](https://blixvip.com/create-memecoin) | accounts.js、hosted-accounts.js、tradeapi.js、Launch.tsx | 有真实资产路径；不得因旧MCP教程说只有纸面交易而忽略新交易API |

## 3. 官网本身值得吸收的专业限制

- [钱包指南](https://blixvip.com/solana-wallet-tracker)说明RPC限制及晚开始观察可能造成未知成本，未知不等于零。
- [风险指南](https://blixvip.com/memecoin-risk-scanner)说明早期买入与Bundle标签是调查线索，不自动证明内幕。
- [SSE指南](https://blixvip.com/pumpfun-realtime-api)说明流没有可靠的持久游标和完整replay；做长期跨币资金监控必须有独立历史与回补。
- 旧[AI Agent说明](https://blixvip.com/ai-trading-agent)聚焦只读和纸面交易，而较新[Trade API](https://blixvip.com/trade-api)描述交易权限密钥；可能是两类接口/时间不同，必须按实际授权路径审查。
- 官网托管账户、Blix域名、当前真实数据库及API服务配置不会因复制MIT源码而自动获得。128份页面声明也不代表128项待开发功能。

## 4. 方向修订

先把已有Coin、钱包、Bubble Map、API/事件等连接成同一Mint的事实链，明确数据与资金事实在哪一层丢失，再从Million、PumpTrace等挑真正能补缺口的成熟能力。网站页面用作问题与业务知识入口，不作为复制功能的清单。证据等级：官网产品声明PUBLISHER_CLAIM、代码SOURCE_READ、上线和实时性能NOT_RUN。