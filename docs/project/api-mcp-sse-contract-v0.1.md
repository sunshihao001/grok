# Blix HTTP / MCP / SSE → Coin 与钱包监控：跨层接口契约 V0.1

**2026-11-06，基准 blix cc468cca7df8916e57159171e481aa5512465fcc。仅 GitHub 静态源码/既有测试定义研究；未运行Blix、未安装、未查询主网、未部署或连接Grok Bot。证据级别 SOURCE_READ、SOURCE_INFERRED_RISK、UNKNOWN 分开处理。**

## 0. 为什么要研究
项目目标是市场发现→单Mint专业调查→跨Mint钱包群体监控→经济机制与反证。不能把HTTP接口有返回、MCP可以调用、SSE看到消息误当成完整事实调查。优先复用 Blix 已有业务，而非立即复制外部项目或重做网站。

## 1. 三类入口真正的边界
| 入口 | 目前实现 | 适合什么 | 不能保证 |
|---|---|---|---|
| HTTP | [server.js](../../server/server.js)、[API公开目录](../../public/api-docs.js)、[长文档](../API.md) | 最完整Coin/钱包/市场、操作及管理 | GET不保证零副作用，授权级别不一，含真实资产路径 |
| MCP | [工具目录](../../public/mcp-tools.js) + [stdio服务](../../mcp/blix-mcp.mjs) | AI自然语言查询部分HTTP信息 | 不是HTTP全覆盖，也不是安全隔离或完整证据合同 |
| SSE | /api/stream、feed/stream、fast/stream | 市场与成员实时事件、UI更新 | 没有持久事件ID/Last-Event-ID replay协议，断网后不能保证完整历史 |

源码列了20个MCP工具；当前 blix 分支通过 READ_TOOLS 排除2个write:true的纸面交易工具，公开18个读取工具。按业务分组：

- 市场：blix_overview、blix_pulse、blix_signals、blix_coins。
- Mint：blix_coin、blix_holders、blix_candles、blix_quote、blix_research。
- 钱包与社会：blix_wallets、blix_wallet、blix_fomo、blix_narratives。
- AI及系统：blix_briefs、blix_picks、blix_track_record、blix_health、blix_paper_desk。

**关键缺口**：blix_coin映射 GET /api/token/:mint，而非完整 GET /api/coin/:mint；blix_wallet映射 GET /api/wallet-page/:address，并非wtrack或本地已追踪钱包的所有记录；现有MCP**没有BubbleMap、wtrack/feed、转账完整历史或跨Mint群体演化工具**。但相应HTTP或业务源码有部分存在，不能说Blix完全缺少这些功能。

## 2. MCP虽然轻量，可能影响专业结论完整性
mcp/blix-mcp.mjs 的trim()对数组默认保留10条（max50）、长字符串裁到800字符、总响应超40000字符则硬截。静态风险：查询结果被缩短但AI误当“全部Wallet/Holder”，JSON硬截可能损坏结构；这不代表实际运行故障已发生。后续Bot需返回count/limit/next/hasMore、来源、观察时间与缺口，无法取得完整结果必须说明 UNKNOWN。

MCP默认BASE=http://localhost:4420，支持BLIX_URL；fetch请求没有自动带blixvip.com的登录会话。原厂账号与当前fork不是同一运行环境；指定官网地址不能自动访问其受保护的数据。readOnlyHint只是工具注解，后端GET仍可能花供应商配额或写缓存。特别是blix_wallets、blix_paper_desk在owner本地服务下可能涉及个人关注钱包与模拟账户数据，不能默认向任意Bot开放。

## 3. 单Mint实际接口链
| 用户页面或查询 | 主要路径 | 数据及副作用边界 |
|---|---|---|
| React Coin | token/:mint 15秒、coin/:mint 3秒、coin/:mint/trades 2秒、jup/:mint 5秒，另有SSE | Coin页面本身由多项独立来源组合，不是一份单表 |
| token/:mint | server.js tokenDetail，可lookupMint/adoptMint/vet | GET可能开始追踪与更新记录，非纯查询 |
| holders/:mint | holdersFor（交易驱动的部分账本） | 不等于Coin全部Holder来源，也未证实完整Owner |
| coin/:mint | coin.coinPage（Holder、Dev、交易者、价格、供应商聚合） | 源时间、覆盖、链上Owner、池身份需逐字段核查 |
| bubblemap?mint= | bubblemap.js（RugCheck网络、首笔funder、四跳、公共Hub排除） | 已经是成熟原生业务；GET可能动态读外部源；POST可触发makeBubbleMap |
| wallet-page/:address | walletpage.js链上钱包概况 | 不等于wallets.js、wtrack.js的交易/转账历史 |
| research/:mint | 已有模型结果；POST为重新发起研究 | GET只读已有结果，POST可能产生模型费用 |
| candles/:mint | 历史K线；server.js可repairCoin | K线不能还原原始资金路径；GET可能触发RPC补数 |

之前的mint-facts实验只读取token和holders两个API。基于现在对Coin及BubbleMap的理解，**不能直接把它升格为专业单Mint最终输出标准**；先核实已存在的完整业务接口，再讨论修改。

## 4. 三种钱包事实账本的不同含义

- [wallets.js](../../server/wallets.js)：wallet_trades主键(sig,wallet,mint)，服务Smart Money/PnL/跟踪。一个签名中同钱包同Mint发生多个动作时，不能保证逐动作持久化；solana.js解析多非报价Mint交易还可能跳过。
- [wtrack.js](../../server/wtrack.js)：wt_feed以(wallet,sig,mint)去重、wt_transfers以(wallet,sig,mint或空)去重。fromTx遇到可识别的Swap就不继续解析Transfer，因此**混合Swap+Transfer的交易可能不完整**；这仍是源码推论，未拿真实签名复现。
- [bubblemap.js](../../server/bubblemap.js)：RugCheck、Holder、最早可见Funder与四跳图的候选关系。共享出资人也可能是交易所、公共服务、分发钱包或正常跟风；**不能自动证明共同控制**。

这三者目前不是统一的经济主体数据库。未来只能在充分确认Token Account、Owner、费付款人、签名、指令位置、资产净变化、SOL/WSOL、Pool/LP和时间来源后，进行资金与库存关系综合。

## 5. SSE、WTrack轮询与历史回补：不能混成无缺口的24小时监控

| 链路 | 已实现的防丢机制 | 仍需谨慎 |
|---|---|---|
| server.js broadcast SSE | 每个event及JSON data即时发送 | 没有可重放event id；连接恢复不是历史完整性的证明 |
| React WalletTracker | [WalletTracker.tsx](../../web/src/components/WalletTracker.tsx)每20秒拉 wtrack?limit=300，并合并SSE；最近300交易、150转账 | 短缺口可能补上，高活动超窗口或源端本来缺失不能由UI补齐 |
| wtrack/feed?since=<id> | 服务器筛选id>since，按时间DESC和id DESC返回，默认200、上限500 | **外部客户端**如果新增超过limit便按最大id推进游标，较老未返回记录可能跳过；静态风险，不是当前React页面已证实故障 |
| journal/journalfeed | 部分Pump/PumpSwap成交有sig/mint/n去重、gap/repair、区块/签名补数 | Journal约24小时；不涵盖所有DEX/Token Transfer；不能代表6/12h完整资金路径 |
| WTrack Transfer | overview最近150条Transfer、独立表保留约7天 | 当前未见和feedSince等价的Transfer断线游标；窗口高频可能不够 |
| K线 | 长期价格汇总 | 无法重新还原交易参与人及完整资金对价 |

已有[test/wtrack.test.mjs](../../test/wtrack.test.mjs)覆盖历史晚到、重启、确认清理等测试定义，但未证明新增量大于分页上限时逐页完整恢复。当前React使用20秒轮询，不应把feedSince的潜在风险误报为网页已经漏单。

## 6. 安全、费用、通知也是接口合同的一部分

服务端[access.js](../../server/access.js)区分visitor/member/owner，member可访问自己的Tracker及纸面账户，owner允许更多接口。当前MCP排除两个纸面写工具，不等于HTTP交易/发币/Vault已经隔离。已有supervise.mjs可绕过npm start预检，故按用户现有指令**禁止启动当前完整原服务**。

GET /api/quote可能请求Jupiter；GET token可能adopt/vet；GET coin或BubbleMap可能请求链上与供应商，GET candles可修复缺口；因此必须区分无链上交易、无本地写入、无未经授权费用三个目标。

[notify.js](../../server/notify.js)已有Discord/Telegram、静默和冷却、发送记录；notifySignal在实际发送前先写pushed=1，成功后另标notified=1。若发送失败是否有自动重试/补发机制需要继续研究，不能承诺告警可靠到达。

## 7. 回到用户的五类实际问题

| 用户意图 | 复用候选 | 当前证据级别 |
|---|---|---|
| 发现今天重要候选、过滤垃圾盘 | pulse/signals/coins/health | 业务存在，覆盖/数量完整性需核实 |
| 调查一个Mint的Dev、Holder、资金图 | token/coin/holders/bubblemap/research | 业务较完整，MCP缺部分入口，经济身份无法仅靠标签证明 |
| 查买入→转新钱包→卖出 | wallet-page、wallets、wtrack | 混合动作解析、历史和对手方仍不完整 |
| 判断拉盘前6/12h资金活动 | journal、钱包活动、行情、补数 | 不足以证明全场所全钱包窗口完整；需要新事件事实/覆盖标记 |
| 跨Mint群体持续监控与异常通知 | wallets、wtrack、bubblemap、notify | 有成熟零件，不等于现成完整跨币群体历史和通知可靠性 |

## 8. 下一步优先顺序（仍然只读研究）

**首选**：同一个Mint的token/coin/holders/bubblemap逐字段来源、时间、owner、池与partial对照，确定已有完整调查能力的真实边界。
**其次**：WTrack的复杂交易、Transfer去重、历史补漏及大批次游标的反例设计，避免跨Mint异常被漏数据误导。
**最后**：在以上事实充分后才决定Grok Bot仅用MCP、增加有限的现有HTTP安全封装，还是需要成熟外部历史解析/资金调查服务。先评估真实缺口，不扩建重复模块。

**状态：SOURCE_READ + SOURCE_INFERRED_RISK；所有运行、调用、云电脑部署、完整经济事件验证均NOT_RUN / UNKNOWN。**
