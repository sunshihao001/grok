# 按实际问题使用专业知识、AI研究与可证伪证据

**主体认识优先入口**：先看[主体能力与旧知识内化深审 V0.2](blix-knowledge-activation-ceiling-v0.2.md)（按业务判断上限、旧方法适用、不能继承的规则），再按需回查下述来源。

**主体认识优先入口（原基准）**：[Blix 已有业务能力 × 旧 Grok 专业知识继承基准](blix-heritage-capability-baseline-v0.1.md)。面对实际业务先定位 Blix 已有 UI/数据/逻辑，再按需要调用 PR #14 的原专业正文或 Hermes/qb-/meme- 的机制，不全文搬迁、不把旧历史程序当作已在 Blix 运行。

## 知识来源与正确定位
| 入口 | 贡献 | 限制 |
|---|---|---|
| [ai-d PR #1](https://github.com/sunshihao001/ai-d/pull/1) | 多层目标/七并行能力、目标纠偏、知识选择、专家认知提取、研究后再思考 | Draft；未证明自动 Agent、跨模型提升或专家技能已经迁移 |
| [grok PR #14](https://github.com/sunshihao001/grok/pull/14) | D01–D12、旧专家视角、152问题与65资产的历史入口 | 登记不等于全部已验 |
| [grok PR #16](https://github.com/sunshihao001/grok/pull/16) | 原始交易解析、单 Mint 真实供应商预览与离线监控研究 | **不是 Blix 已集成的真实持续监控** |
| [grok PR #17](https://github.com/sunshihao001/grok/pull/17) | 目标演变、UI信息设计、知识导航、业务集成研究 | Draft，非 Blix 当前代码 |
| [Hermes](https://github.com/sunshihao001/-)、[qb-](https://github.com/sunshihao001/qb-)、[meme-](https://github.com/sunshihao001/meme-) | 钱包角色、资金循环、单 Mint 报告、经济机制与旧失败经验 | 不自动视作安全可运行成品 |
| [Why-Solana](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | 同源/多跳/群体协同、公共设施排除、选择偏差与反证 | 结构关系不等于真实经济主体或收益优势 |

旧知识保留原位，禁止为“让 AI 理解”将所有 Markdown 全量注入上下文或从头复建专家制度。

## 专家认知怎么进入实际产品
ai-d 最新研究区分 **知识摘要 → 问题表征/判断方法 → 经外部任务检验的实际能力迁移**。当分析一个 Mint，AI 应先明确当前用户问题和经济机制；仅提取相关研究里的必要线索、决策依据、适用/失败条件，并用交易事实及对照反证验证，不能假装理解专家不可观察的内心过程。

## 常见问题与正确知识调用
- “12小时钱包转账突然增多” → 先查可得历史、钱包名单变化、签名/资产净变化；再比较资金准备、做市、出货、Dust、公共Hub、数据回补等机制。
- “捆绑钱包占多少” → 分同Slot、真实可确认Bundle、初期买入供应占比、当前持仓；分母/窗口/Pool/Owner必须明确。
- “A买入、B接收、C卖出” → 交易签名、指令位置、Swap/Transfer和接收路径；不能直接把三地址确认为同控。
- “要新增一个专业模块” → 先研究原 Blix 是否已有；外部成熟整用/薄接口/有限适配/内置四种路线按成本与证据选择。

## 输出与数据证据的最低语义
区分 `USER_CONFIRMED`、`SOURCE_READ`、`AUTHOR_REPORT`、`SUPPLIER_RETURN`、`OFFLINE_TEST`、`LIVE_READ_ONLY`、`PRODUCTION_VERIFIED`、`INFERENCE`、`HYPOTHESIS`、`UNKNOWN`。保留来源、签名及事件位置、Slot、事件和采集时间、资产单位、覆盖/缺口、正常竞争解释、可推翻条件；无数据不能当0活动。

**每项重要成果后再想一次**：有没有比原方案更成熟的产品/算法/机制解释？新认识改变哪个上层目标或执行选择？比较少量实质方向并推荐首选；若没有增量，就继续当前路线，不为凑选项创造伪问题。


## 已核原始知识的实际激活：三种问题，不是复制旧规则（2026-11-06）

本节从旧研究**直接读过的原文**反向连接现有 Blix 源码，补足 [主体能力/知识基准](blix-heritage-capability-baseline-v0.1.md) 中尚属概括的映射。只证明**原文已读、机制适用性进行了人工源审查**，不证明模型已自动学会、知识路由已上线或资金归因实测通过。

### A｜“这些钱包一起买，是不是一个人在控制？”

**应按需读取原文**：
- [旧 Hermes 钱包角色](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-03-wallet-roles.md)：有 wallet roles、`native_transfer_from`、关键钱包标签、证据和反证字段；**GMGN 标签是输入候选，不是身份真值**。
- [旧 Hermes 钱包结构](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-04-wallet-structure.md)：把同 `native_transfer_from`、五分钟内买入3钱包、卖出比例相似定义为调查组；这些是**筛查阈值**，不是经过独立校准的共同控制证据。
- [PR #14 D04–D07 深入知识](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/domain/L3-wallet-actors.md)：节点/边角色、共享服务、Dust、市场共同事件、经济受益人和可卖库存的竞争解释。

**Blix 现成入口**：`server/coin.js` Holder/Dev、`server/bubblemap.js` RugCheck/first-funder/同Slot/四跳图、`server/wallets.js` 聚类及 `wtrack.js` 钱包活动、`web/src/pages/Coin.tsx`。不要先写第二套聚类。

**原文改变的判断**：先确认具体 `funded` 边究竟是 SOL 转账，还是 `bubblemap.js:119-129` 的 Fee Payer 代理；查看是否公共交易所/分发服务，以及同Slot是否受共同市场事件影响。正确结论可为“观察到共享出资候选与同步买入；共同控制 **UNKNOWN**”。**禁止**直接使用 Hermes 的“同源=一个团队”或 Blix graph cluster=实际庄家作为既定事实。

### B｜“这个 Mint 的关键钱包、池和成本应该怎样调查？”

**应按需读取原文**：
- [旧 qb- 单 Mint 报告程序](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)：输出 `04_key_address_matrix.csv`（关键地址）、`05_infrastructure_registry.csv`（公共设施）、`06_low_weight_scope.csv`（低权重范围）、`07_review_plan.csv`（复查计划）等完整工作产品，**是业务问题与报告设计参考**。源码用 `subprocess.run(..., shell=True)` 调旧 GMGN 命令，**绝不未经审查直接运行**。
- [原 Grok D01/D06/D10 主册](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-core.v1.md)：Token Account/Owner/程序、供应量、钱包角色与数据时点的区分。
- [PR #16 受限适配器契约](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)：原始 RPC、`available_at` 与未支持事件需要分离；离线 fixture 并非完整 Swap 归因。

**Blix 现成入口**：`server/holders.js` ledger、`holderslive.js` 链上 Owner 快照、`coin.js` 多供应商/Dev/Pool、`bubblemap.js` 后备前20 Token Account，再看 `web/src/pages/coin/tabviews.tsx` 的结果位置。

**原文改变的判断**：将 `Pool/AMM/vault`、Token Account 与真实 Owner 分开；按源报告持仓分母、快照 Slot/确认级别、历史交易覆盖和成本缺失。将 “被观察到的持仓”与 “可归于某经济主体的可卖库存”分开。不要用旧 qb- 的优先级分数、GMGN 标签或 Blix `partial:false` 自动产出确定的成本/控盘概率。

### C｜“拉升前12小时转账激增，是吸筹还是要出货？”

**应按需读取原文**：
- [旧 meme- 深洗与死亡盘](https://github.com/sunshihao001/meme-/blob/main/02_%E5%BA%84%E5%AE%B6%E5%91%A8%E6%9C%9F/%E6%B7%B1%E6%B4%97%E4%B8%8E%E6%AD%BB%E4%BA%A1%E7%9B%98%E8%AF%AD%E4%B9%89%E6%B7%B1%E5%8C%96_v0.1.md)：Wyckoff/POC/AVWAP 的恢复、失败和需求语义只是价格结构**待检验假设**，不是操盘者身份或真实成本的证据。
- [Hermes 筹码状态设计](https://github.com/sunshihao001/-/blob/main/design/Skill4-%E7%AD%B9%E7%A0%81%E6%8E%A7%E5%88%B6%E6%9D%83%E7%8A%B6%E6%80%81%E5%B1%82%E8%AE%BE%E8%AE%A1.md)：时间对齐、过期立即 UNKNOWN、排除Pool/CEX/系统账户是**有价值的条件判断**；其状态概率和权重公式未经当前链上实证校准，不迁入生产评分。
- [Grok PR #14 D05/D07/D11](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/domain/L3-wallet-actors.md)：时序角色、共同事件基线、公共资金服务与反证；[PR #16 离线钱包批次](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)：窗口在 `coverage.complete` 不足时不能证明“没有活动”。

**Blix 现成入口**：`server/journal.js`、`wtrack.js`、`wallets.js`、`coin-flow.js`、`server/health.js`、`research.js`。先查是否真的观察到6/12h连续签名/资产净变化，调查集是否改变、是否发生缓存回补，再考虑供需/资金准备/拆分接力/出货/普通做市等解释。

**原文改变的判断**：如果某个时间段 RPC 断流，不能从零条事件推出“钱包沉默”；如果价格形态像“深洗”，也不能从K线替代真实仓位/资金证据。合理报告是观察事实、数据覆盖、多个机制假设及可推翻条件。

### 防污染：一处旧知识明确不应直接带入

[Hermes Evidence Chain 原设计](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-05-evidence-chain.md) 的 `calculate_confidence` 用固定 `base=0.8` 加减启发式权重，并把同源占比等用作 `CONTROLLED` 的候选条件。该设计可借鉴“证据/反证/降级/缺失字段都应出现在报告”，但**不能把其0.8或阈值复制成 Blix 的概率标签**；没有真实基准、校准和独立反例，精确数值会制造虚假确定性。

### 什么叫“已把知识放进主体”，当前到了哪一级？

- **已完成 SOURCE_READ + LINKED**：AI入口 `AGENTS.md` → `docs/project/README.md` → 本文件 / 主体继承总图 → 上述精确原来源 → Blix现有业务代码。具体可回查原文，旧知识仍留在原仓库，**不需要迁移复制152题、22专家和65资产**。
- **尚未完成 APPLIED_AND_VERIFIED**：没有运行的同 Mint 调查样本验证这三条调用链是否提高了结论质量；没有将上述推断写入 Blix 运行时的数据结构、UI、MCP、持续告警；没有真正的 Grok Bot知识调用。
- **后续按用户新指令**：先让这三条主体业务—知识链清晰、确认重要的专业缺口，再按“能够改善哪个业务判断”去解剖 Million/Why-Solana/HoldTech/OKX 等成熟实现。不能以研究项目的名称或功能个数代替复用判断。
