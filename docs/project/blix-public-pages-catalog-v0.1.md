# Blix 官网公开页面索引 V0.1

**2026-11-06，SOURCE_ROUTE_INDEX。** 本文从 blix 分支用于生成官网的 worker/site 页面源码提取目录，并利用公开网络检索对部分重要页面进行交叉验证。不是逐页在线HTTP 200测试，更不是全文复制官网内容。

定义128次、原始路径126条；去掉别名覆盖的原始页面后，形成113个规范路径候选，另有23条重定向/同义别名。113个网页不代表113项不同业务功能，尤其SEO和竞品比较文章多次描述同一业务。

官网首页 https://blixvip.com/ 、独立动态Top Dev榜单 /devs、登录后终端 /app 并不属于这里的公开页面定义。完整产品能力归纳与运行边界见项目文档。

## 全部规范页面（按官网生成模块分类）

### 核心页面（10）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/api](https://blixvip.com/api) | Solana Memecoin Data & API Reference / BLIX | [pages.js:90](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L90) |
| [/axiom-api](https://blixvip.com/axiom-api) | Axiom Trade API: Is There One? The BLIX Alternative (2026) | [pages.js:334](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L334) |
| [/fomo-api](https://blixvip.com/fomo-api) | Fomo API (fomo.family): Is There One? Free Alternative 2026 | [pages.js:390](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L390) |
| [/gmgn-api](https://blixvip.com/gmgn-api) | GMGN API: Access, Limits and a Free Alternative (2026) | [pages.js:264](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L264) |
| [/guides](https://blixvip.com/guides) | BLIX Guides: Solana Trading, Wallet Research, APIs & MCP | [pages.js:632](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L632) |
| [/mcp](https://blixvip.com/mcp) | Solana MCP Server for Claude, Cursor & Codex (Free) / Blix | [pages.js:202](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L202) |
| [/memecoin-paper-trading](https://blixvip.com/memecoin-paper-trading) | Memecoin Paper Trading on Solana: Simulated Fills / BLIX | [pages.js:588](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L588) |
| [/pump-fun-api](https://blixvip.com/pump-fun-api) | Free pump.fun API: Launches, Trades, Holders, No Key (2026) | [pages.js:442](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L442) |
| [/pump-fun-tracker](https://blixvip.com/pump-fun-tracker) | pump.fun Tracker: Live New Pairs, Bonding & Migrations (Free) / BLIX | [pages.js:511](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L511) |
| [/solana-memecoin-screener](https://blixvip.com/solana-memecoin-screener) | Solana Memecoin Screener with AI Ratings & Narratives (Free) / BLIX | [pages.js:553](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages.js#L553) |

### 功能介绍（9）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/create-memecoin](https://blixvip.com/create-memecoin) | Create a Solana Memecoin on Pump.fun / Blix Coin Launcher | [features.js:148](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L148) |
| [/how-to-find-meme-coins-early](https://blixvip.com/how-to-find-meme-coins-early) | How to Find Meme Coins Early: A Solana Research Workflow / Blix | [features.js:211](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L211) |
| [/memecoin-alerts](https://blixvip.com/memecoin-alerts) | Memecoin Alerts: Launches, Wallet Activity & Signals / Blix | [features.js:128](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L128) |
| [/memecoin-risk-scanner](https://blixvip.com/memecoin-risk-scanner) | Memecoin Risk Scanner: Holders, Bundles & Exit Liquidity / Blix | [features.js:103](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L103) |
| [/memecoin-social-sentiment](https://blixvip.com/memecoin-social-sentiment) | Memecoin Social Sentiment & Narrative Research / Blix | [features.js:168](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L168) |
| [/pumpfun-realtime-api](https://blixvip.com/pumpfun-realtime-api) | Pump.fun Real-Time Data API: SSE, JavaScript & Python / Blix | [features.js:234](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L234) |
| [/solana-pnl-tracker](https://blixvip.com/solana-pnl-tracker) | Solana PnL Tracker: Realized, Open & Sellable Positions / Blix | [features.js:187](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L187) |
| [/solana-trading-terminal](https://blixvip.com/solana-trading-terminal) | Solana Trading Terminal: Research, Wallets & Execution / Blix | [features.js:13](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L13) |
| [/solana-wallet-tracker](https://blixvip.com/solana-wallet-tracker) | Solana Wallet Tracker & Smart Money Analytics / Blix | [features.js:83](https://github.com/sunshihao001/grok/blob/blix/worker/site/features.js#L83) |

### 专业教程（6）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/guides/compare-ai-crypto-research](https://blixvip.com/guides/compare-ai-crypto-research) | Compare AI Crypto Research: Grok, Claude & Evidence Quality / BLIX | [learning.js:114](https://github.com/sunshihao001/grok/blob/blix/worker/site/learning.js#L114) |
| [/guides/how-to-analyze-meme-coins](https://blixvip.com/guides/how-to-analyze-meme-coins) | How to Analyze Meme Coins and Pump.fun Tokens / BLIX Guide | [learning.js:22](https://github.com/sunshihao001/grok/blob/blix/worker/site/learning.js#L22) |
| [/guides/how-to-find-smart-money-wallets](https://blixvip.com/guides/how-to-find-smart-money-wallets) | How to Find and Track Solana Smart Money Wallets / BLIX | [learning.js:56](https://github.com/sunshihao001/grok/blob/blix/worker/site/learning.js#L56) |
| [/guides/pumpfun-bonding-curve](https://blixvip.com/guides/pumpfun-bonding-curve) | Pump.fun Bonding Curve, Graduation & Migration Explained / BLIX | [learning.js:180](https://github.com/sunshihao001/grok/blob/blix/worker/site/learning.js#L180) |
| [/guides/solana-memecoin-market-cap-liquidity](https://blixvip.com/guides/solana-memecoin-market-cap-liquidity) | Memecoin Market Cap vs Liquidity, Volume & Exit Value / BLIX | [learning.js:147](https://github.com/sunshihao001/grok/blob/blix/worker/site/learning.js#L147) |
| [/guides/token-holder-distribution](https://blixvip.com/guides/token-holder-distribution) | Token Holder Analysis: Distribution, Bundles & Wallet Links / BLIX | [learning.js:83](https://github.com/sunshihao001/grok/blob/blix/worker/site/learning.js#L83) |

### 终端对照（4）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/compare](https://blixvip.com/compare) | Compare Solana Memecoin Terminals: BLIX, Axiom, Fomo & Nio | [comparisons.js:14](https://github.com/sunshihao001/grok/blob/blix/worker/site/comparisons.js#L14) |
| [/compare/axiom-alternative](https://blixvip.com/compare/axiom-alternative) | Axiom Alternative for AI Research, API & Paper Trading / BLIX | [comparisons.js:54](https://github.com/sunshihao001/grok/blob/blix/worker/site/comparisons.js#L54) |
| [/compare/fomo-alternative](https://blixvip.com/compare/fomo-alternative) | Fomo Alternative for Memecoin Research & Wallet Analysis / BLIX | [comparisons.js:89](https://github.com/sunshihao001/grok/blob/blix/worker/site/comparisons.js#L89) |
| [/compare/nio-trade-alternative](https://blixvip.com/compare/nio-trade-alternative) | Nio.trade Alternative for Solana AI Research & MCP / BLIX | [comparisons.js:127](https://github.com/sunshihao001/grok/blob/blix/worker/site/comparisons.js#L127) |

### 竞品指南（6）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/compare/birdeye-alternative](https://blixvip.com/compare/birdeye-alternative) | Birdeye Alternative: Compare Research Workflows & Data Needs / BLIX | [competitor-guides.js:111](https://github.com/sunshihao001/grok/blob/blix/worker/site/competitor-guides.js#L111) |
| [/compare/bullx-alternative](https://blixvip.com/compare/bullx-alternative) | BullX & BullX Neo Alternative: Rebuild Your Trading Workflow / BLIX | [competitor-guides.js:23](https://github.com/sunshihao001/grok/blob/blix/worker/site/competitor-guides.js#L23) |
| [/compare/dexscreener-alternative](https://blixvip.com/compare/dexscreener-alternative) | DEX Screener Alternative for Solana Token Research / BLIX | [competitor-guides.js:81](https://github.com/sunshihao001/grok/blob/blix/worker/site/competitor-guides.js#L81) |
| [/compare/gmgn-alternative](https://blixvip.com/compare/gmgn-alternative) | GMGN Alternative: Wallet Research, AI Context & Paper Tests / BLIX | [competitor-guides.js:51](https://github.com/sunshihao001/grok/blob/blix/worker/site/competitor-guides.js#L51) |
| [/compare/jupiter-terminal-alternative](https://blixvip.com/compare/jupiter-terminal-alternative) | Jupiter Terminal Alternative: Swap Plugin or Research Terminal? / BLIX | [competitor-guides.js:142](https://github.com/sunshihao001/grok/blob/blix/worker/site/competitor-guides.js#L142) |
| [/compare/solana-terminal-comparison](https://blixvip.com/compare/solana-terminal-comparison) | Axiom vs Fomo, BullX, Photon & GMGN: Workflow Comparison / BLIX | [competitor-guides.js:172](https://github.com/sunshihao001/grok/blob/blix/worker/site/competitor-guides.js#L172) |

### 编辑/说明（1）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/about](https://blixvip.com/about) | About BLIX: Memecoin Research, Data & Editorial Standards | [editorial.js:3](https://github.com/sunshihao001/grok/blob/blix/worker/site/editorial.js#L3) |

### Pump.fun（14）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/pump-fun](https://blixvip.com/pump-fun) | pump.fun: How It Works, Fees, and How to Trade It / BLIX | [pages-pump.js:25](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L25) |
| [/pump-fun-analytics](https://blixvip.com/pump-fun-analytics) | pump.fun Analytics Dashboard: Volume, Holders, Trending / BLIX | [pages-pump.js:156](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L156) |
| [/pump-fun-api-javascript](https://blixvip.com/pump-fun-api-javascript) | pump.fun API in JavaScript & Node.js: Live Launches / BLIX | [pages-pump.js:516](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L516) |
| [/pump-fun-api-python](https://blixvip.com/pump-fun-api-python) | pump.fun API in Python: Launches, Holders, Quotes / BLIX | [pages-pump.js:434](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L434) |
| [/pump-fun-mcp](https://blixvip.com/pump-fun-mcp) | pump.fun MCP Server: Live Launch Data for AI Agents / BLIX | [pages-pump.js:228](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L228) |
| [/pump-fun-rug-checker](https://blixvip.com/pump-fun-rug-checker) | pump.fun Rug Checker: Bundles, Snipers, Dev History (Free) / BLIX | [pages-pump.js:639](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L639) |
| [/pump-fun-sdk](https://blixvip.com/pump-fun-sdk) | pump.fun SDK & CLI: Launches, Trades, Holders Without a Package / BLIX | [pages-pump.js:286](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L286) |
| [/pump-fun-signals](https://blixvip.com/pump-fun-signals) | pump.fun Signals & Alerts: Launches, Dumps, Smart Wallets / BLIX | [pages-pump.js:190](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L190) |
| [/pump-fun-terminal](https://blixvip.com/pump-fun-terminal) | pump.fun Trading Terminal with AI: Scanner, Chart, Trade / BLIX | [pages-pump.js:126](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L126) |
| [/pump-fun-trading-bot](https://blixvip.com/pump-fun-trading-bot) | pump.fun Trading Bot: Sniper Bots vs an AI Terminal (2026) / BLIX | [pages-pump.js:90](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L90) |
| [/pump-fun-vs-letsbonk](https://blixvip.com/pump-fun-vs-letsbonk) | pump.fun vs LetsBonk: Which Solana Launchpad in 2026? / BLIX | [pages-pump.js:680](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L680) |
| [/pump-fun-vs-moonshot](https://blixvip.com/pump-fun-vs-moonshot) | pump.fun vs Moonshot (Moonit): Solana Launchpads Compared / BLIX | [pages-pump.js:714](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L714) |
| [/pump-fun-vs-raydium](https://blixvip.com/pump-fun-vs-raydium) | pump.fun vs Raydium: PumpSwap, LaunchLab and Where Coins Trade / BLIX | [pages-pump.js:752](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L752) |
| [/pump-fun-wallet-tracker](https://blixvip.com/pump-fun-wallet-tracker) | pump.fun Wallet Tracker: Whales, Devs, Top Traders, PnL / BLIX | [pages-pump.js:605](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-pump.js#L605) |

### AI研究（11）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/ai-memecoin-picks](https://blixvip.com/ai-memecoin-picks) | AI Meme Coin Picks Today: Solana & pump.fun, With Reasons / BLIX | [pages-ai.js:139](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L139) |
| [/ai-memecoin-trading](https://blixvip.com/ai-memecoin-trading) | AI Memecoin Trading on Solana: How It Works in 2026 / BLIX | [pages-ai.js:20](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L20) |
| [/ai-trading-agent](https://blixvip.com/ai-trading-agent) | AI Trading Agent for Solana: Give Your Agent Live Memecoin Data / BLIX | [pages-ai.js:97](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L97) |
| [/ai-trading-bot](https://blixvip.com/ai-trading-bot) | AI Trading Bot for Solana Memecoins: What Works (2026) / BLIX | [pages-ai.js:63](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L63) |
| [/best-ai-for-crypto-trading](https://blixvip.com/best-ai-for-crypto-trading) | Best AI for Crypto Trading: Grok vs Claude vs ChatGPT / BLIX | [pages-ai.js:340](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L340) |
| [/best-crypto-ai-tools](https://blixvip.com/best-crypto-ai-tools) | Best Crypto AI Tools for Solana Memecoins in 2026 / BLIX | [pages-ai.js:375](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L375) |
| [/chatgpt-meme-coin-analysis](https://blixvip.com/chatgpt-meme-coin-analysis) | ChatGPT Meme Coin Analysis: Connect Solana Data to GPT (2026) / BLIX | [pages-ai.js:236](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L236) |
| [/claude-crypto-analysis](https://blixvip.com/claude-crypto-analysis) | Claude Meme Coin Analysis & Picks: Live Solana Data via MCP / BLIX | [pages-ai.js:200](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L200) |
| [/deepseek-meme-coin-picks](https://blixvip.com/deepseek-meme-coin-picks) | DeepSeek, Kimi & Qwen Meme Coin Picks on Live Solana Data / BLIX | [pages-ai.js:302](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L302) |
| [/gemini-crypto-picks](https://blixvip.com/gemini-crypto-picks) | Gemini Meme Coin Picks & Crypto Analysis with Gemini CLI / BLIX | [pages-ai.js:269](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L269) |
| [/grok-meme-coin-picks](https://blixvip.com/grok-meme-coin-picks) | Grok Meme Coin Picks & Crypto Analysis: Live X Search on Solana / BLIX | [pages-ai.js:173](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-ai.js#L173) |

### 市场交易（13）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/best-solana-trading-terminal](https://blixvip.com/best-solana-trading-terminal) | Best Solana Trading Terminal for Memecoins (2026 Comparison) / BLIX | [pages-trade.js:550](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L550) |
| [/meme-coin-analyzer](https://blixvip.com/meme-coin-analyzer) | Meme Coin Analyzer: Holders, Chart, Safety, AI Read / BLIX | [pages-trade.js:318](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L318) |
| [/meme-coin-finder](https://blixvip.com/meme-coin-finder) | Meme Coin Finder: Find Solana Gems Early with AI (Free) / BLIX | [pages-trade.js:226](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L226) |
| [/memecoin-analytics](https://blixvip.com/memecoin-analytics) | Memecoin Analytics Dashboard: Volume, Holders, Momentum, Live / BLIX | [pages-trade.js:358](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L358) |
| [/memecoin-narratives](https://blixvip.com/memecoin-narratives) | Memecoin Narrative Tracker: Solana Trends, Written Daily / BLIX | [pages-trade.js:436](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L436) |
| [/new-meme-coins](https://blixvip.com/new-meme-coins) | New Meme Coins on Solana Today: Live Launches with Holders & AI / BLIX | [pages-trade.js:259](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L259) |
| [/rug-pull-scanner](https://blixvip.com/rug-pull-scanner) | Rug Pull Scanner for Solana: Detect Rugs, Honeypots & Insiders / BLIX | [pages-trade.js:189](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L189) |
| [/smart-money-tracker](https://blixvip.com/smart-money-tracker) | Smart Money Tracker for Solana: Find the Wallets That Buy Early / BLIX | [pages-trade.js:130](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L130) |
| [/solana-memecoins](https://blixvip.com/solana-memecoins) | Solana Memecoins: How They Work and How to Trade Them in 2026 / BLIX | [pages-trade.js:504](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L504) |
| [/solana-swap](https://blixvip.com/solana-swap) | Solana Swap for Memecoins: One-Click Buy & Sell / BLIX | [pages-trade.js:464](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L464) |
| [/solana-whale-tracker](https://blixvip.com/solana-whale-tracker) | Solana Whale Tracker: Big Wallets, Buys and Sells Live (Free) / BLIX | [pages-trade.js:163](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L163) |
| [/trending-meme-coins](https://blixvip.com/trending-meme-coins) | Trending Meme Coins on Solana Right Now: Live Ranking with AI / BLIX | [pages-trade.js:291](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L291) |
| [/twitter-meme-coin-tracker](https://blixvip.com/twitter-meme-coin-tracker) | X (Twitter) Meme Coin Tracker: Posts to Coins in a Minute / BLIX | [pages-trade.js:401](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-trade.js#L401) |

### 开发者/API（8）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/crypto-mcp-server](https://blixvip.com/crypto-mcp-server) | Crypto MCP Servers for Trading & Data Agents (2026) / BLIX | [pages-dev.js:76](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L76) |
| [/crypto-trading-cli](https://blixvip.com/crypto-trading-cli) | Crypto Trading CLI for Solana Memecoins: curl, jq and AI CLIs / BLIX | [pages-dev.js:427](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L427) |
| [/developers](https://blixvip.com/developers) | Developer Access: BLIX API & MCP Connector With Your Account / BLIX | [pages-dev.js:39](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L39) |
| [/how-to-build-a-solana-trading-bot](https://blixvip.com/how-to-build-a-solana-trading-bot) | How to Build a Solana Trading Bot for Memecoins (2026 Guide) / BLIX | [pages-dev.js:480](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L480) |
| [/how-to-use-mcp-for-crypto](https://blixvip.com/how-to-use-mcp-for-crypto) | How to Use MCP for Crypto: Solana Data in Your AI / BLIX | [pages-dev.js:155](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L155) |
| [/memecoin-sdk](https://blixvip.com/memecoin-sdk) | Memecoin SDK for Solana: Trading Data in 20 Lines, Any Language / BLIX | [pages-dev.js:349](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L349) |
| [/solana-api](https://blixvip.com/solana-api) | Solana Memecoin API: Tokens, Trades, Wallets & Quotes / BLIX | [pages-dev.js:202](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L202) |
| [/wallet-tracking-api](https://blixvip.com/wallet-tracking-api) | Solana Wallet Tracking API: Swaps, PnL, Smart Money, Whales / BLIX | [pages-dev.js:303](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-dev.js#L303) |

### 竞品/替代（16）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/axiom-mcp](https://blixvip.com/axiom-mcp) | Axiom MCP Server, SDK & CLI: Axiom Trade Has None / BLIX | [pages-compete.js:243](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L243) |
| [/axiom-scanner](https://blixvip.com/axiom-scanner) | Axiom Scanner vs BLIX Pulse with AI Ratings / BLIX | [pages-compete.js:287](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L287) |
| [/axiom-trade](https://blixvip.com/axiom-trade) | Axiom Trade: Fees, Pulse, Setup and What BLIX Adds (2026) / BLIX | [pages-compete.js:173](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L173) |
| [/axiom-trading-bot](https://blixvip.com/axiom-trading-bot) | Axiom Trading Bot & Automation: What Exists (2026) / BLIX | [pages-compete.js:207](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L207) |
| [/axiom-vs-bullx](https://blixvip.com/axiom-vs-bullx) | Axiom vs BullX (2026): One Is Live, One Is Not / BLIX | [pages-compete.js:606](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L606) |
| [/axiom-vs-fomo](https://blixvip.com/axiom-vs-fomo) | Axiom vs Fomo (2026): Fees, Speed, Social, Keys / BLIX | [pages-compete.js:576](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L576) |
| [/axiom-vs-gmgn](https://blixvip.com/axiom-vs-gmgn) | Axiom vs GMGN (2026): Solana Speed vs Multi-Chain / BLIX | [pages-compete.js:666](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L666) |
| [/axiom-vs-photon](https://blixvip.com/axiom-vs-photon) | Axiom vs Photon (2026): Speed, Fees, Keys, Pulse / BLIX | [pages-compete.js:635](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L635) |
| [/fomo-app](https://blixvip.com/fomo-app) | Fomo App: Fees, Chains, Download, and BLIX Compared / BLIX | [pages-compete.js:19](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L19) |
| [/fomo-mcp](https://blixvip.com/fomo-mcp) | Fomo MCP Server, SDK & CLI: None Official. Use BLIX / BLIX | [pages-compete.js:92](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L92) |
| [/fomo-scanner](https://blixvip.com/fomo-scanner) | Fomo Scanner & Signals vs a Scanner with AI / BLIX | [pages-compete.js:130](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L130) |
| [/fomo-trading-bot](https://blixvip.com/fomo-trading-bot) | Fomo Trading Bot: There Is No Official One. What to Use Instead / BLIX | [pages-compete.js:61](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L61) |
| [/fomo-vs-bullx](https://blixvip.com/fomo-vs-bullx) | Fomo vs BullX (2026): Social App vs Suspended Terminal / BLIX | [pages-compete.js:695](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L695) |
| [/nio-trade](https://blixvip.com/nio-trade) | nio.trade: Chains, Cashback, and BLIX Compared (2026) / BLIX | [pages-compete.js:333](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L333) |
| [/nio-trade-api](https://blixvip.com/nio-trade-api) | nio.trade API, MCP, SDK & CLI: None Found. Use BLIX / BLIX | [pages-compete.js:366](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L366) |
| [/photon-alternative](https://blixvip.com/photon-alternative) | Photon Alternative: Solana Terminals with AI (2026) / BLIX | [pages-compete.js:419](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-compete.js#L419) |

### 代币创建（4）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/ai-meme-coin-maker](https://blixvip.com/ai-meme-coin-maker) | AI Meme Coin Maker: What AI Actually Does for a Launch (2026) / BLIX | [pages-create.js:59](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-create.js#L59) |
| [/create-pump-fun-coin](https://blixvip.com/create-pump-fun-coin) | Create a pump.fun Coin in One Screen: Launcher, Fees, Rewards / BLIX | [pages-create.js:17](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-create.js#L17) |
| [/how-to-create-a-meme-coin](https://blixvip.com/how-to-create-a-meme-coin) | How to Create a Meme Coin on Solana in 2026 (pump.fun) / BLIX | [pages-create.js:151](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-create.js#L151) |
| [/meme-coin-name-generator](https://blixvip.com/meme-coin-name-generator) | Meme Coin Name Generator: Names, Tickers & Taglines / BLIX | [pages-create.js:120](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-create.js#L120) |

### 帮助/工具中心（3）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/how-to-track-solana-wallets](https://blixvip.com/how-to-track-solana-wallets) | How to Track Solana Wallets (and Find Smart Money) in 2026 / BLIX | [pages-guides.js:16](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-guides.js#L16) |
| [/how-to-use-ai-for-crypto-trading](https://blixvip.com/how-to-use-ai-for-crypto-trading) | How to Use AI for Crypto & Meme Coin Trading (2026) / BLIX | [pages-guides.js:86](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-guides.js#L86) |
| [/tools](https://blixvip.com/tools) | Everything BLIX Does: Tools, Guides and Comparisons / BLIX | [pages-guides.js:147](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-guides.js#L147) |

### 交易API（8）

| 页面及原站链接 | 页面标题 | 当前分支的生成源码 |
|---|---|---|
| [/axiom-trading-api](https://blixvip.com/axiom-trading-api) | Axiom Trading API: No Official One. Trade Programmatically With BLIX / BLIX | [pages-tradeapi.js:310](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L310) |
| [/bullx-trading-api](https://blixvip.com/bullx-trading-api) | BullX Trading API: Trading Suspended, No API. Use the BLIX Trade API / BLIX | [pages-tradeapi.js:481](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L481) |
| [/fomo-trading-api](https://blixvip.com/fomo-trading-api) | Fomo Trading API: None Official. Trade pump.fun With the BLIX Trade API / BLIX | [pages-tradeapi.js:376](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L376) |
| [/gmgn-trading-api](https://blixvip.com/gmgn-trading-api) | GMGN Trading API: Swaps Through the OpenAPI vs the BLIX Trade API / BLIX | [pages-tradeapi.js:256](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L256) |
| [/jupiter-trading-api](https://blixvip.com/jupiter-trading-api) | Jupiter Trading API vs the BLIX Trade API for pump.fun Bots / BLIX | [pages-tradeapi.js:535](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L535) |
| [/photon-trading-api](https://blixvip.com/photon-trading-api) | Photon Trading API: None Public. Trade pump.fun Programmatically With BLIX / BLIX | [pages-tradeapi.js:423](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L423) |
| [/pump-fun-trading-api](https://blixvip.com/pump-fun-trading-api) | pump.fun Trading API: PumpPortal, pumpdev.io and BLIX Compared (2026) / BLIX | [pages-tradeapi.js:202](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L202) |
| [/trade-api](https://blixvip.com/trade-api) | Solana Trade API for pump.fun Bots: Your Wallet, Your Key, 2% a Trade / BLIX | [pages-tradeapi.js:137](https://github.com/sunshihao001/grok/blob/blix/worker/site/pages-tradeapi.js#L137) |

## 全部23条别名重定向

| 旧路径或搜索词入口 | 当前规范路径 |
|---|---|
| /memecoin-scanner | [对应文档](https://blixvip.com/solana-memecoin-screener) |
| /solana-token-scanner | [对应文档](https://blixvip.com/solana-memecoin-screener) |
| /meme-coin-scanner | [对应文档](https://blixvip.com/solana-memecoin-screener) |
| /pump-fun-scanner | [对应文档](https://blixvip.com/pump-fun-tracker) |
| /memecoin-signals | [对应文档](https://blixvip.com/memecoin-alerts) |
| /pump-fun-websocket | [对应文档](https://blixvip.com/pumpfun-realtime-api) |
| /memecoin-mcp-server | [对应文档](https://blixvip.com/mcp) |
| /memecoin-api | [对应文档](https://blixvip.com/api) |
| /bullx-alternative | [对应文档](https://blixvip.com/compare/bullx-alternative) |
| /gmgn-alternative | [对应文档](https://blixvip.com/compare/gmgn-alternative) |
| /dexscreener-alternative | [对应文档](https://blixvip.com/compare/dexscreener-alternative) |
| /birdeye-alternative | [对应文档](https://blixvip.com/compare/birdeye-alternative) |
| /jupiter-terminal-alternative | [对应文档](https://blixvip.com/compare/jupiter-terminal-alternative) |
| /how-to-analyze-meme-coins | [对应文档](https://blixvip.com/guides/how-to-analyze-meme-coins) |
| /pumpfun-api | [对应文档](https://blixvip.com/pump-fun-api) |
| /solana-mcp | [对应文档](https://blixvip.com/mcp) |
| /axiom-alternative | [对应文档](https://blixvip.com/compare/axiom-alternative) |
| /ai-meme-coin-picks | [对应文档](https://blixvip.com/ai-memecoin-picks) |
| /pumpportal-alternative | [对应文档](https://blixvip.com/pump-fun-trading-api) |
| /pump-fun-trade-api | [对应文档](https://blixvip.com/trade-api) |
| /solana-trade-api | [对应文档](https://blixvip.com/trade-api) |
| /solana-trading-api | [对应文档](https://blixvip.com/trade-api) |
| /memecoin-trading-api | [对应文档](https://blixvip.com/trade-api) |

## 验证和继续研究原则

- 静态路由存在 != 线上当前页存在，页面可检索 != 其所述市场功能已经运行和可用。
- 以官方源页面为认知入口；到相关 React UI、HTTP API、数据库和实际测试寻找更强证据。
- 网站文章同义重复须按真实业务功能归并，不能把页面数量当作待整合模块数量。
