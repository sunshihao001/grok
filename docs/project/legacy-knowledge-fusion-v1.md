# 旧 Grok 专业知识 → Blix 主体业务融合 V1.0

> 2026-11-06；仅文档映射，未改业务代码、未运行 Blix、未部署 Grok Bot。原 Grok PR #14 为 Draft；分类为检索导航，不代表152条结论已经实证。
> 原始权威来源：[知识索引](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json)、[152单元原始图谱](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/whole-domain-atlas.v1.json)、[22专家视角](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/experts/registry.v1.json)。

## 1. 融合不是复制

保留旧 Grok L0–L7、D01–D12、152研究问题（144个领域单元+8个L0治理单元）、22种按需专家视角、65项参考资产的**原始来源**。Blix 只负责按具体业务问题定位原来源及必要机制；不把旧标签或置信阈值直接变成运行结论，不建立第二套本体、第二张钱包图、另一套交易终端或固定22 Bot。旧知识中“来源事实、作者判断、研究假说、反例、代码验证”必须保留区别。

## 2. 按 Blix 已有业务落点映射12领域

| 旧领域 | Blix承载位置（不是新分层） | 应用时引入的专业判断 | 禁止直接迁移的错误 |
|---|---|---|---|
| D01 链上基础 | `server/solana.js`、`holderslive.js`、`journal.js` | 交易版本/CPI、Token Account/Owner/Authority、SOL/WSOL净变化、slot与时点 | 将一次转账算成一次交易；手续费付款者等同资助者 |
| D02 发行生命周期 | `engine.js`、`coin.js`、Pulse/Coin UI | 创建/可交易/曲线/迁移/多池分期，Dev与LP权限 | UI毕业标签等同链上迁移完成 |
| D03 市场微观结构 | `sources.js`、`coin.js`、`quality.js`、`jupiter.js` | 流动性、储备、成交量、报价路径、价格容量及套利 | 一个Mint只有单一价格与交易池 |
| D04 钱包行为与角色 | `wallets.js`、`wtrack.js`、`walletpage.js` | 早买/接收/转仓/卖出、PnL样本和角色时间性 | 供应商标签等于稳定经济身份 |
| D05 资金网络与主体 | `bubblemap.js`、`wallets.js`、`wtrack.js` | 直接资本转入、代付Gas、共享服务、资金循环、多跳竞争解释 | 同源、同Slot、可达路径直接等于同一控制 |
| D06 筹码与供求 | `holders.js`、`holderslive.js`、`coin.js`、Bubble Map | 供应量分母、账户合并/Pool排除、当前库存与可卖性 | 前20个Token Account等于前20个Owner |
| D07 群体时序 | `journal.js`、`wtrack.js`、`notify.js`、`health.js` | 1/5/15分钟行为、6/12小时异动、成员变化和断流 | 未观察到事件等于钱包沉默 |
| D08 策略机制 | `research.js`、`brain.js`、Picks | 将跟单/FCZ/事件驱动转为可证伪假说 | 研究候选等于可执行盈利策略 |
| D09 执行与风险 | `jup.js`、`quote.js`、`price-sanity.js` | 可卖流动性、冲击、成本、失败成交和净期望（研究用途） | 只看标价/回测价格认定能获利；不启用交易 |
| D10 来源与可靠性 | `coverage.js`、`db.js`、`heliuskeys.js`、`health.js` | 来源、采集/事件时间、缓存、缺口、去重、费用、安全 | `partial:false` 等同全链历史完整 |
| D11 实证与反证 | `research.js`、`journal.js`、测试与报告 | 竞争解释、同期基线、负例、样本外、冻结时点 | 历史成功案例等于预测优势 |
| D12 AI研究/知识进化 | `AGENTS.md`、`docs/project/knowledge-use.md`、`server/intelligence/`、MCP | 意图专业升级、选知识、调查、复核、再决定 | 复制全库或运行22专家即模型掌握 |

L0的8个治理单元作为横切前提映射到证据来源、版本、许可、权限、冲突、可复算与审查，不作为新页面。

## 3. 旧项目的专业内容怎样落地

- **旧 Grok PR #14**：专业问题、机制与反证主索引；以 Dxx-Kxx 回到原文，按上述表分配 Blix 业务，不将 mapped_unverified 升成 K2 实证。
- **旧 Grok PR #16**：原始交易适配、单Mint报告、离线群体窗口，仅在 Blix 事实入口缺口被证明后选择性复用；其旧实测与本分支运行完全分开。
- **旧 Grok PR #17**：跨知识/工程的继承经验；不是 Blix 已有代码。
- **Hermes**：钱包角色、资金边/Sybil/Wash、可卖库存、证据链；保留反证与对象分解，不搬固定7-Skill、同源强断言和未校准0.8置信度。
- **qb-**：单Mint关键地址矩阵、基础设施名册、转入接力与复查栏目；对照 Coin/Wallet 页面与报告，不运行旧脚本或默认要求付费GMGN。
- **meme-**：市场结构、成本区、深洗/死亡盘及失败实验，作为假说供 Research 对照，不作为链上控制权事实。
- **Why-Solana、Million等**：先保留研究入口与待比较点；不要因为有四跳/关系图就替换 Blix 自带 Bubble Map。
- **ai-d**：只承担自然语言目标升级、选源、方案比较、验收和纠错的方法；不覆盖 Solana 原始事实。

## 4. 三个跨层用例，用于检验知识真正被调用

**A. “这些钱包是否同一团伙？”** D01→D04→D05→D06→D11。先拿 `bubblemap.js` 原资金边及原始交易，区别直接SOL来源与首笔Fee Payer，排除Hub/共享服务，分开当前Token库存和经济控制；UNKNOWN可作为正确结论。

**B. “买入后转给新钱包出货了吗？”** D01→D04→D05→D06→D07→D10。对单签名多动作、Swap/Transfer、Owner与Token Account、时间和跨模块账本进行核对；资金与库存不能用一个页面的净额猜测。

**C. “拉升前12小时转账激增，有没有跨币重复？”** D07→D05→D10→D11→D08。需有完整机会/事件窗口、固定观察钱包集合、缺口与同期对照；分资金准备、正常服务、回填、转仓、出货等机制，不能由K线先判定庄家。

## 5. 知识达到什么状态才算融合成功

1. **ROUTED**：按Mint/钱包/群体/时序能找到原始单元、相关Blix模块和限制；本文件只达到这个层级。
2. **REASONING_APPLIED**：一次具体调查中，旧知识改变了问题选择、反证或结果表达，有可查前后差异。
3. **CODE_APPLIED**：现有业务代码/接口确实采用证据契约并通过离线反例；不靠Markdown声称完成。
4. **LIVE_VERIFIED**：安全隔离后，用真实Mint/原始交易/断流恢复完成独立只读验收。

当前重点：`bubblemap.js` 的最早 Fee Payer→funder 误归因、3页历史截断负缓存；`coin.js`与`holders.js`供应量分母冲突；当前余额快照与历史完整性混淆。先让旧知识修正这些实际判断，再深入解剖外部成品。安全隔离未验收，不启动交易、签名、付款或自动付费模型。

## 6. 来源保留原则

旧专业来源不迁走也不删除：[Grok知识PR](https://github.com/sunshihao001/grok/pull/14)、[工程PR](https://github.com/sunshihao001/grok/pull/16)、[集成PR](https://github.com/sunshihao001/grok/pull/17)、[Hermes](https://github.com/sunshihao001/-)、[qb-](https://github.com/sunshihao001/qb-)、[meme-](https://github.com/sunshihao001/meme-)、[ai-d](https://github.com/sunshihao001/ai-d)。完整65参考资产继续以原始 `gpt-meme-project-index.v1.json` 为权威。每项融合只在可验证任务中引入必要原文，不全量注入提示词。
