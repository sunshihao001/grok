# Blix 原生知识 × 旧 Grok 知识：对应、去重与收录清单 V0.1

> 2026-11-06 | 本文件严格依据 [Blix 原生体系](BLIX-NATIVE-ATLAS.md) → [旧 Grok 原体系](OLD-GROK-ATLAS.md) 的阅读顺序，之后才作接收裁决。**不变更业务代码、不安装Bot/依赖、不运行网络或交易。** 现在的结论是知识与功能的映射，不是已完成的AI主动调用。

## 一、唯一主体、两种截然不同的知识

- **Blix 原生知识优先**：产品需求、已有 UI/API/模块/数据库/部署/故障/测试，以当前 `blix` 为事实真源；旧Grok不应替代本地数据语义或现有功能。
- **旧 Grok 专业知识补充**：以 `main` 早期卡/快照/只读方法 + PR14领域研究 + PR16工程证据 + PR17集成经验为来源。保留原文件及commit/blob信息；旧研究的“专家”“层级”“阶段”不等于Blix必须再建的工程组件。
- **知识被收录和能力被激活是两件事**：完整保留、能够检索 ≠ 被模型正确理解；源码存在 ≠ 可运行；运行 ≠ 已验证真实经济解释。

## 二、旧 Grok 的12领域怎样归到 Blix 既有分类与产品位置

| 旧研究域 | Blix 现有知识主类（允许跨类引用） | Blix 当前业务/代码入口 | 迁入时采用什么形式 |
|---|---|---|---|
| D01 链上协议 | `foundations` | `solana.js`、`coin.js`、`holderslive.js`、事实检查 | 原文保留+协议最新版本核验，错误单位/账户归因转测试候选 |
| D02 发行生命周期 | `foundations` / `mechanisms` | `engine.js`、`launchlab.js`、`creator.js`、`coin.js` | 按发行程序、迁移和多池含义与原生业务关联 |
| D03 微结构与价格 | `mechanisms` | `candles.js`、`quote.js`、`pumpswap.js` | 经济解释和计算前提，不把模型形态当利润 |
| D04 钱包行为角色 | `methods` / `mechanisms` | `wallets.js`、`wtrack.js`、`walletpage.js` | 角色调查法、来源与选择偏差；旧GMGN标签只作候选 |
| D05 资金组织/主体 | `mechanisms` / `methods` | `bubblemap.js`、`wallets.js`、`coin-flow.js` | 资金/手续费/LP/服务边区分，保留替代解释 |
| D06 筹码和库存 | `mechanisms` / `foundations` | `holders.js`、`holderslive.js`、`coin.js` | 供应分母/Owner/Pool/可售与总库存分层 |
| D07 行为时序与跨币 | `methods` / `cases` | `wtrack.js`、`journal.js`、`notify.js` | 连续观察、成员变化、历史缺口和事件时间区别 |
| D08 策略及未知机会 | `mechanisms` / `cases` | `research.js`、`triage.js`、`brain.js` | 仅研究候选与反证，禁止把旧Alpha推论直升交易信号 |
| D09 执行与风险 | `foundations` / `mechanisms` | `quote.js`、`fee-ledger.js`、`price-sanity.js` 等 | 为研究提供价格冲击、费用和可交易性语义；现阶段不执行交易 |
| D10 数据与工程 | `foundations` / `cases` / `references` | `db.js`、`coverage.js`、`heliuskeys.js`、`health.js` | 数据缺失、重复、限流、缓存、成本和恢复与Blix事故记录对照 |
| D11 实证与反证 | `cases` / `methods` | `test/`、`journal.js`、`research.js` | 原研究方法/负例，未来使用真实案例时核对来源与冻结时间 |
| D12 AI知识进化 | `ai` | `AGENTS.md`、`server/intelligence/`、`mcp/` | 意图→知识适用→只读事实→解释；不复制旧多Bot/阶段工作流 |

**L0 的来源、版权、冲突、证据等级、权限**跨上述所有类别执行，是知识收录标注与审查原则，不必建额外一个庞大 L0 体系。旧 `Dxx-Kxx` 编号由已有 [152项路由](../docs/project/legacy-knowledge-routing.v1.json) 保留。

## 三、现有接收情况：别重复搬迁17份全文

2026-11-06 初批 [MIGRATION.json](MIGRATION.json) 记录**17份旧研究副本**，分类为 `foundations=2, mechanisms=5, methods=5, cases=1, ai=1, references=3`。其中旧 PR14 `knowledge/domain/` 的主要研究正文已进入Blix；一份 Hermès 00c 与一份 ai-d 知识也进入相应类型。

**已做的结构核验**：PR #14 的 `knowledge/domain/` 除 README 外共10份专业正文，均能在上述17份迁入清单中找到对应原路径；17份Blix目标文件均存在，且文件中均能找到登记的原始 blob SHA 与来源链接。这个检查证明**文件与出处的一致性**，不证明逐字对比/引用链完整，也不证明专业结论已经验证。

本轮不会为了“融合”再次复制同一文件，也不重新生成152张知识卡。若要断言“全文迁移完毕”，应同时复核文件尾、原blob SHA、正文与迁入头部；旧源中的指令始终是历史内容，而非本分支强制指令。

**仍未被17份覆盖的主要旧资产，按原价值逐批处理：**

| 来源/资产 | 为什么要保留 | 建议动作（本轮不直接搬） |
|---|---|---|
| `grok@main/knowledge/catalog.v1.json` 15张核心卡 | 有 `mechanism`、`required_evidence`、`alternative_explanations`、`inference_limit` 等比目录更具体的知识条件 | 与已迁入的专业正文去重；**保留原JSON并将有独立方法价值的字段选入现有正文/索引** |
| `grok@main/knowledge/legacy-snapshots/` 21份快照 | 包含旧Hermes/交易研究的历史方法与状态 | 清点 SHA/许可/是否已有全文，不覆盖新研究 |
| PR14 `knowledge/system/` 多个原始索引/覆盖与专家注册表 | 包含152项、22视角、65参考资产与未研究缺口 | 现已有152路由，不重复建体系；65资产的验证状态/原始入口要保存；需要时精准读取专家原文 |
| PR14 `knowledge/transfer/` 与训练反馈材料 | 体现知识如何跨Bot/来源交接、哪些动作未验证 | 按 `ai` 或 `cases` 提炼过程经验，不复刻课程制度 |
| PR16交易解析、Mint报告与离线测试 | 有交易语义、真实缓存数据源边界与RPC429失败 | 先归到 `foundations/cases/references` 的**来源清单**，代码是否采用另行评估 |
| PR17目标、合并冲突与知识导航 | 历史工程融合尝试与误归因防线 | 只继承有价值的决策/失败经验，不重建旧Grok工作流 |
| Hermes 00b–00e、旧 Skills/learning/calibration | 深层字段→经济机制推演、角色、资金、筹码与失败经验 | 与现有 `methods/mechanisms` 去重后选最有价值原文，保留旧阈值未校准警告 |
| qb-、meme- 原项目 | 关键钱包矩阵、资金接力、FCZ/POC等机制与反例 | 后续 **分别深入审查原目录再纳入同一Blix六类**，不是另起两套体系 |
| Million/PumpTrace/Pulse/OKX/Why-Solana等 | 有成熟程序、证据/历史/费用边界，许可各异 | `references` 先收可复核**独立研究与源码链接**，未经许可核对不全量搬第三方资料 |

## 四、真正融合时的低成本做法

**从内容而非旧目录名出发**，选择以下处理之一：

1. **Blix已有完整同类能力** → 在现有本地知识/代码说明里加入来源和反例；不复制另一套业务规则。
2. **旧 Grok有成熟理论、没有验证成品** → 归为 `mechanisms` 或 `methods`，保留原始理由、条件、冲突和真实验证状态；不冒充可执行脚本。
3. **旧项目有真实重要案例或失败** → `cases` 优先保留签名/时点/来源、错误解释与反证，不把案例归纳直接提升为规律。
4. **外部成熟项目提供更完整流程** → `references` 记录其代码路径、许可证、数据依赖、实际覆盖、与Blix现有实现差异，先决定复用知识/接口/算法/整体，不预设复制。
5. **ai-d提供AI通用方法** → `ai` 记录问题表征、知识适用、信息价值、持续纠错，不把它当第二个产品或强制多Agent。

**知识类型和使用范围不同**：专业观点可以先纳入Blix文本库供按需研读，实际代码优化等到真实任务指出缺口时再做。这符合“只用Blix一套产品、先梳理再建设”的目标。

## 五、当前整合结果与检查标准

- **已完成**：Blix自身产品知识的独立地图、旧Grok(main/PR14/PR16/PR17)的分版本目录地图、六类型与12域对应、17份迁入资料的来源清单复用及待补资产判定。
- **未完成**：全部旧Main/PR14/16/17逐文件深读和重叠去除、Hermes/qb-/meme-全目录逐项知识迁移、参考项目逐源码复用裁决、自动运行时检索与AI质量实证。
- **不执行**：不启动Blix、Grok云电脑、签名/交易/支付、真实供应商接口，不将旧CLI或历史Bot原样安装。
- **下一轮执行顺序**：先核对旧 `main` 15卡/21快照与当前17份的语义覆盖 → 收录真正未覆盖的原知识 → 深入Hermes/qb-/meme-原目录 → 再按同六类纳入成熟参考知识；每批更新已有 [MIGRATION.json](MIGRATION.json)，以来源和去重结果而非新建目录数作为进度。

> **统一判定**：Blix的“知识体系”不是纯文档库，而是 **它自己已运行代码所表达的事实与规则 + 原始工程经验 + 分类迁入的专业研究 + 明确的证据和限度**。旧Grok是专业来源，不是Blix的新架构。
