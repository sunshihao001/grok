# 同一 Mint 跨模块事实一致性｜深入静态审查 V0.2

> 2026-11-06；源码基准 `891df69746a3b5d80b3d670b8f88ccd84cb29380`；审查范围：`server/server.js`、`holders.js`、`holderslive.js`、`coin.js`、`bubblemap.js`、`jup.js`、`intelligence/mint-facts.mjs`。**SOURCE_READ** 表示已读源码；**INFERRED_RISK** 表示由源码推导的风险；**NOT_TESTED** 表示未以真实交易/运行环境复现。未启动服务、未调用 RPC、未改业务代码。此文件深化既有 [全局反向审查](external-brain-completeness-audit-v0.1.md)，不另造框架。

## 核心结论

**现在不能把 `/api/token/:mint`、`/api/holders/:mint`、`/api/coin/:mint`、`/api/bubblemap?mint=` 的数字与关系直接合成一份“全链、同一时间、经济主体级”调查报告。** 四者的覆盖、分母、观测时间、身份归属和历史证据不同。更应保留现有 Blix 整体产品并补充可验证的证据语义，避免复制新网站或第二套市场数据处理。

## 1. 逐路径核对：同一个问题如何产生四种回答

| 入口 / 核心代码 | 直接事实来源 | 实际口径 | 关键缺失 |
|---|---|---|---|
| `GET /api/holders/:mint` → `holdersFor` (`server.js:1520-1521`, `holders.js:106-135`) | Blix trade feed 本地账本 | 观察到的账户余额、交易计数、`genesis/partial`，份额以 `knownSupply || 1e9` 为分母 | 不证明全链历史；`partial:false` 仅是该账本自己的完整性判断 |
| `GET /api/token/:mint` → `tokenDetail` (`server.js:609-641,1647-1680`) | Token DB、近期发行、实时统计、上述 `holdersFor` | `holders` 是本地 ledger；同一响应还含研究、钱包交易、paper positions | Token/Holder 不等于 Coin 页面所选最终持仓来源 |
| `GET /api/coin/:mint` → `coinPage` (`coin.js:328-437`) | ledger → Jupiter → 链上 live → RugCheck 依条件覆盖 | 页面展示的 Holder 可由链上快照、Jupiter、RugCheck 等替代；局部 ledger 的份额固定除以 `1e9` | `partial:false` 可仅表示当前余额快照，不表示交易/资金路径完整；各源未统一Slot |
| `GET /api/bubblemap?mint=` → `bubbleMap` (`server.js:1446`, `bubblemap.js:175-328`) | `coinPage` 的 Holder、RugCheck insider graph、首笔资金候选、同Slot买入、Fomo标签 | 最多100基础 Holder + 最多40额外 Fomo；资金追踪最多前50；关系最长4跳 | 关系网络是**样本与规则生成的候选结构**，不是全量经济主体控制图 |
| `intelligence/mint-facts.mjs` | **只读**读取 `/api/token` 和 `/api/holders` | 保留 ledger 的 `partial`、`since`、`last`，且标明未经独立链上核实 | **没有**读取 `coinPage` 的链上替代 Holder、Bubble Map、原始交易，不能称作完整 Mint 调查 |

**已发生的认知修订**：现有 `mint-facts` 不是“同一 Mint 所有事实的统一入口”，而是“两个本地 API 的谨慎摘要”。继续扩建 AI 分析前，应先解决这两个入口与 Coin 页面实际展示来源之间的证据差异。

## 2. 四个有明确输入输出的反例（未运行）

### R1｜历史截断后长期漏关联：强源码证据

- `bubblemap.js:39`：`PAGES=3`；`:109-129`：3页×1000签名未到历史末尾返回 `""`。
- `:53-66`：SQLite `bubble_funders(wallet PRIMARY KEY, funder NOT NULL, t)`；空字符串表示“追过但未找到”。
- `:133-151`：只有 `funderOf(wallet) === undefined` 才再次追踪，空字符串不会重新查。
- `:313`：UI `untraceable:true`，但无法区别“历史超过3000”“确实无符合规则的转账”“最老交易缺失”等原因。

**反例输入**：钱包 W 有超过3000笔历史，真正首笔出资人 F 在第3001笔之前。**预测**：第一次追踪写入空值；第二次即使有更好RPC/时间也不追踪；图中 W-F 不连线。**反证方式**：使用确定性RPC夹具验证页数/缓存；另用真实签名确认F存在。**建议**：将结果状态区分 `FOUND`、`HISTORY_TRUNCATED`、`NO_MATCH_WITH_COMPLETE_HISTORY`、`PROVIDER_FAILURE`；仅对可补查状态有限重试，不能将缺失解释为“无关系”。

### R2｜首笔 Fee Payer 被解释成资金来源：高价值新增风险

- `bubblemap.js:119-129`：优先找最早交易中的 system transfer 接收方；**若找不到**，返回该交易第一个 `accountKey`（Fee Payer）作为 `funder`。
- Fee Payer 支付交易手续费，**不等于**向目标钱包提供了可用 SOL 资本；还可能是第三方代付、账户创建方或公共服务。
- `bubblemap.js:228-235`：此候选被用来生成 `funded` 关系边；图可将“付手续费”解释成“提供资金”。

**反例输入**：交易中 P 支付手续费、目标 W 通过不同交易或不同资产取得资本，最早交易没有可解析的 system transfer 给 W。**预测**：P 仍被记为 W 的 funder；两个被同一 P 代付手续费的钱包可能被连接。**反证方式**：原始交易比较 P 的 fee payer、pre/post SOL 余额、实际转账和 token movements。**建议**：`DIRECT_SOL_FUNDING` 与 `EARLIEST_TX_FEE_PAYER` 必须拆成不同证据类型，后者不得单独升级为经济资本关联。

### R3｜同 Mint 的 Holder 百分比冲突：强源码证据

- `holders.js:120-135`：份额分母 `knownSupply(mint) || 1e9`。
- `coin.js:34,208,341,355,554`：账本 Holder、钱包行、Dev、群体仍以固定 `SUPPLY=1e9` 计算。
- `coin.js:380-391`：链上 Holder 使用 `J.supply || supplyFor(mint,t)`；`bubblemap.js:175-185` 使用 Coin 页面 Holder 的 `pct`。
- **反例输入**：真实供应量5亿，持仓1亿，`knownSupply=5e8`。**预测**：`holdersFor` 显示20%，`coin.js` 的 ledger walletLine 显示10%；Bubble Map 如果用这一页，继承10%。这里是可计算的源码预测，不是线上复现。
- **建议**：每个百分比输出需包含分母数值与来源；修复分母前，不应把多个来源百分比用于控制权或库存变化的自动结论。

### R4｜当前持仓被误读为历史完整：强源码证据

- `holderslive.js:128,151` 使用 `processed` 快照与订阅，`:163,208` 对外返回的是 `at`，未输出本次快照 Slot、确认级别或完整订阅序列范围。
- `coin.js:385-391`：若 chain live 取代账本，返回 `trades:0`、`since:null`、`genesis:false`、`partial:false`。
- `coin.js:522`：Jupiter 备份 Holder 也可 `partial:false`，却不证明早期交易全量。
- **反例输入**：Blix 在发行后才看到某币，但链上当前余额快照成功。**预测**：Coin 页面可显示 `partial:false`；用户或下游 AI 误把它理解成“历史资金完整”。
- **建议**：把 `balanceCoverage`、`tradeHistoryCoverage`、`fundingHistoryCoverage`、`slot/commitment` 分开，绝不由单一 `partial` 代替。

## 3. 另外三项跨层误差放大器

**S1｜后备前20 Token Account 的样本偏差**：`bubblemap.js:375-395` 使用 `getTokenLargestAccounts` 的前20 Token Account，随后才按 Owner 合并。该集合不是前20 Owner；更不是经济主体样本。多个Token Account属于同一Owner时，其他重要Owner可能排除在外。即使最终比例以链上总供应量为分母，也不能证明 Holder 头部完整。

**S2｜图上的连接不等于同一控制**：`bubblemap.js:205-312` 把 RugCheck transfer、首笔funded、同Slot block、dev/bundle launch 等混合成可达图；公共服务会尽力过滤，但路径最长4跳和最短树仅是**结构算法**，不是控制权识别算法。同Slot可能是热门交易时段；Fee Payer候选进一步放大误判。应保留每条边的原始签名、时间、类型与竞争解释，不能只用“聚类百分比”给出庄家归因。

**S3｜采样与时间的双重边界**：`bubblemap.js:33-45` 只读最多300 Holder、展示最多100基础+40附加，追踪前50资金来源；`holderslive.js:128,151` 的 `processed` 与 `bubblemap.js:378-388` 的 `confirmed` 及 Jupiter/RugCheck 缓存混合，图中未给所有边统一Slot。不能将“未看到异常”写成“市场不存在异常”。

## 4. 优先级与真实产品路线判断

| 决策 | 判断 | 推翻/升级所需证据 |
|---|---|---|
| 继续使用 Blix 作为单一产品主体 | **保留**。现有UI、采集、Holder、Bubble Map和钱包能力已有可复用路径 | 安全隔离、持续运行、费用或完整任务验收出现不可接受问题 |
| 立刻重建钱包图/新数据库 | **不做**。问题首先是证据语义、历史覆盖和误归因 | 现有数据模型确实无法记录原始事件与追溯，且成熟替代整体成本更低 |
| 把 `mint-facts` 当作完整单Mint调查 | **否**。它只读两条本地API，且并非Coin页面最终Holder口径 | 已有一致性契约、链上原始交易证据、跨模块反例测试与用户报告验收 |
| 优先修正哪个风险 | **R1 + R2**：错误的“没关联”和错误的“有资金关系”同时存在；再处理R3分母与R4历史完整性 | 夹具显示错误分支不可达、生产数据有独立防护或真实事件反证 |
| 现在是否运行完整 Blix | **否**。保留既定只读静态研究边界 | 另行确认安全隔离与真实运行授权 |

## 5. 可以交给后续工程验收的具体反例

1. **Funder截断**：模拟三页各1000签名、真实最早交易在更前面；不得返回 `NO_FUNDER`；再次执行应可继续补查。
2. **Fee Payer非资助人**：最早交易 P 代付手续费但无向 W 的资本转入；不得生成 `DIRECT_SOL_FUNDING` 边。
3. **供应量非10亿**：同一1亿持仓、5亿总量；所有 Holder/Dev/Bubble Map 都必须使用一致的20%分母，或明确各自口径且不合成。
4. **当前余额与历史缺口**：快照有完整Owner余额、早期交易未知；余额可报告，资金/成本结论必须 `UNKNOWN`。
5. **前20账户不等于前20Owner**：一个Owner拥有多个大账户；不得标记 `TOP_20_OWNERS_COMPLETE`。
6. **不同确认级别**：`processed`与`confirmed`冲突时，不得以单一时间戳宣称同一快照。
7. **公共设施与同Slot**：共享手续费代付、交易服务或同Slot买入不得单独推出共同控制。
8. **API一致性**：`/api/token` Holder 与 `/api/coin` Holder 来源不同，报告必须明确展示二者的来源及不一致，不得悄悄选择更“漂亮”的数字。

**尚未执行上述测试**。它们是明确、可核查的未来验收输入，不是伪造通过记录。

## 6. 研究停止条件与下一步

这轮静态源码已足以改变产品集成优先级：**先核查并纠正错误事实和资金边的传播，再谈 AI 自动结论、跨Mint监控与Grok云端调用。** 下一次不必重复“全面扫描所有文件”；只有在确认已有安全、依赖和只读隔离条件后，才将上述反例做成离线测试。真实Mint、长时间运行、Grok云端、通知可靠性仍是未验收。

相关资料：[全局目标](goal-map.md)、[单Mint验收](single-mint-audit.md)、[现有能力层](intelligence-layer.md)、[API/MCP/SSE契约](api-mcp-sse-contract-v0.1.md)、[安全边界](read-only-safety.md)。

## 2026-11-09 修订结果：R1/R2已转为工程修复候选，原V0.2保留作为错误基线

**修正对象**：[PR #23](https://github.com/sunshihao001/grok/pull/23) 的 `server/bubblemap.js`，以及新 `server/bubble-funding-evidence.mjs`。V0.2第2节R1/R2描述的是**修复前代码路径**，不能再当成当前Draft实现。R3分母不一致、R4余额快照误当历史完整、S1Token Account采样偏差、S2多来源连线与同控区别仍为开放问题。

- **R1 截断缓存**：由旧 `""` 标记修改为 `HISTORY_TRUNCATED`、签名、持久cursor与限期继续扫描；最早可访问历史仍不等于全链完整。旧表记录默认 `UNVERIFIED_LEGACY`，不能用于新增有资金关联的结论。
- **R2 Fee Payer误认资金**：仅由成功的原始System `transfer`/`createAccount` 指令确定直接SOL转入候选；费支付者只记录 `FEE_PAYER_ONLY`，绝不单独产生 `funded`。同交易多个独立资金发送者返回 `MULTIPLE_DIRECT_SOL_SENDERS`，不任选单一funding钱包。
- **节点与网络颗粒度**：Bubble Map对每个被追踪holder返回资金来源`status/signature/feePayer/historyCursor`，每张图增加连接候选而非经济主体同控的明示解释；原有多跳结构和UI布局保留。

**验证**：通过新增 `test/bubble-funding-evidence.test.mjs` 的隔离RPC和SQLite旧缓存反例，及 [Node24全量+安全+证据验证](https://github.com/sunshihao001/grok/actions/runs/42564963740)（该固定提交确实成功）。未跑真实公开RPC或完整Blix主服务，没有生产性钱包/群体实测。以后依据最新提交的CI更新此结论，**不能再引用上面历史的“尚未执行所有反例”概括R1/R2**。
