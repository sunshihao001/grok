# Blix｜持续建设台账与下一轮高价值研究（2026-11-08）

> **唯一目的：把发现、代码修正、尚缺验收、历史知识与新的研究方向放在同一条产品业务链，不让下一轮重头研究，也不让待修事项强迫每轮全部实施。** 本文是现有 [项目入口](README.md)、[交付边界](delivery.md)、[目标](goal-map.md) 的行动索引，不替代它们，不创建新的软件架构/专家体系/固定阶段制度。

## 0. 当前真实状态与证据等级

- 当前产品主体：`sunshihao001/grok@blix`，审查基点 `3bc1f7d4`。Blix 当前仍没有合并经济证据功能分支。
- [经济证据功能分支](https://github.com/sunshihao001/grok/tree/feat/blix-economic-evidence-20261108)：已实现本地完整 jsonParsed 交易归档与保守指令索引；没有证明真实历史全量。
- [经济证据加固 Draft PR #19](https://github.com/sunshihao001/grok/pull/19)：相对于功能分支提出签名校验、Token-2022 常量、Owner 冲突标记、本地接收钱包后续查询等。**不是已并入 blix 的功能。**
- [PR #19 Node24 CI](https://github.com/sunshihao001/grok/actions/runs/42481576097)：428项测试、421通过、7失败；其中经济证据专项21项通过。7项集中于原 `wtrack.test.mjs` 标签/分组/状态隔离；原 `wtrack.js` 缺少测试要求的 `saveGroup` 等接口，尚未在独立基线 CI 中完成对照，不把全部失败简单归因本次补丁。依赖审计 [成功](https://github.com/sunshihao001/grok/actions/runs/42481576062)。
- 证据级别：`SOURCE_READ`（读源码）≠ `ISOLATED_TESTED`（隔离单测）≠ `INTEGRATED_TESTED`（完整业务链测试）≠ `LIVE_VERIFIED`（真实链和长期运行）。`UNKNOWN` 是合格结论。**没有运行原 Blix 主服务、真实主网钱包调查、自动交易或云部署。**

## 1. 统一业务对象：一条链而非一批孤立缺陷

`发现 Mint A → 识别 W1 买入 → W1 把 Token 给 W2 → W2 后续卖出 → W2 向 W3 转 SOL → W3 买入 Mint B → 形成多种经济解释、反证与持续监控`。

需要一直分清五层：
1. **真实链上事件**：签名、slot、CPI/Token Account、资产余额、时间、确认状态。
2. **观测窗口**：哪种供应商、按哪类钱包或 Mint 收集、多久、是否丢失/截断、多久更新。
3. **候选关系**：直接转账、后续交易时序、群体聚合；还不能推成共同控制、原筹码卖出或资本闭环。
4. **经济解释**：库存转移、退出、补仓、公共池/交易所/代付/独立账户等竞争解释。
5. **产品体验**：Pulse/Coin/Bubble Map/Wallet/AI 在同一任务下能否让人查到事实、差异和 UNKNOWN。

## 2. 持续台账（研究对象可调整，编号用于追踪而非强制按序完成）

状态：`CODE_PROPOSED`=未合并代码；`STATIC_RISK`=有源码支持尚待反例；`RESEARCH`=需要进一步研究；`NOT_VERIFIED`=功能或结论未验收；`DEFER`=保留暂缓。

| ID / 关联场景 | 具体建设问题 | 当前证据／进度 | 下一次应完成什么、何时可关闭 |
|---|---|---|---|
| BL-01 市场→Mint | Pulse/Coins/Journal发现事件与可追溯 Mint 调查的触发和原始交易如何接通 | `RESEARCH`：市场来源有业务闭环，但经济证据只经钱包原始读取局部接入 | 输出现成调用路径与“发现后不触发原始交易采集”的反例；不预设全市场抓全量 RPC |
| BL-02 原始交易 | 原始 JSON 保存、签名一致性、Token-2022 ID、Owner 缺失/冲突、来源/commitment | `CODE_PROPOSED`：[PR#19](https://github.com/sunshihao001/grok/pull/19)，专项单测21项通过 | 合并前审差异、真实归档验证、迁移可恢复；“已提交”不能关单 |
| BL-03 执行完整性 | v0/v1与ALT、嵌套CPI、Token-2022手续费/扩展、SOL/WSOL、失败指令的完整经济动作 | `RESEARCH`：只存可解析指令索引，原文保留；复杂机制未反例验收 | 选择真实或离线可复现签名，比较事件索引、账户净变化、费用和库存，复用成熟解析器优先 |
| BL-04 钱包采集覆盖 | 只有被跟踪钱包的 `getTransaction` 才自动进入新经济证据；历史漏签名与断流 | `STATIC_RISK`：wallets 的 stream/poll 只订阅选中钱包；新证据无“全币全钱包”入口 | 建覆盖契约：目标钱包、发现来源、最老时间、截断、缺失、预算、错误/恢复状态 |
| BL-05 接收钱包发现 | Token接收 W2 从 Owner/Token Account 形成可复查边，未知Owner与服务节点不混同 | `CODE_PROPOSED`：功能分支 recipients，PR#19新增后续候选观察 | 通过混合Swap+Transfer、多接收者、关闭Token账户等离线对照；接收者不等于同控主体 |
| BL-06 后续卖出 | W2清仓后已不在当前 Holder 头部，如何查到历史卖出、是否卖出受让库存 | `CODE_PROPOSED / NOT_VERIFIED`：PR#19本地 `recipient-outcomes` 仅查询已有wallet_trades | 先比较 `walletpage`、`scanWallet`、现有账本与历史供应商；验证缺失应显示 `NOT_OBSERVED` 而非“没有卖出” |
| BL-07 跨Mint链 | W2卖 Mint A、转SOL给W3、W3买Mint B；独立钱包、共享服务和资金混用 | `CODE_PROPOSED`：cross-mint时间候选SQL已有；不追踪可替代lamports资本来源 | 用同金额不同来源及共享交易所的反例判断能否升级为真实资金链；未证实保持候选 |
| BL-08 Bubble Map误归因 | fee payer 误当 funder；超过3页历史缓存空字符串导致“永久无资金人” | `STATIC_RISK`：[同Mint审查](mint-cross-module-evidence-audit-v0.2.md) R1/R2 | 明确 FOUND/TRUNCATED/NO_MATCH/PROVIDER_FAILED 与 FEE_PAYER_ONLY；改前做确定性反例 |
| BL-09 Holder口径 | `holders.js` 动态供应量与 `coin.js` 固定1e9分母；多源Holder `partial:false`含义不一 | `STATIC_RISK`：[R3/R4](mint-cross-module-evidence-audit-v0.2.md) | 对同一Mint、slot、分母/资产单位、缓存年龄做来源表；一致性反例通过后才自动解读集中度 |
| BL-10 身份/聚类 | Top Token Account不等于Top Owner；Pool/DEX/creator/service和群体关系不是实际控制权 | `STATIC_RISK`：BubbleMap多跳图已存在，非从零缺少聚类 | 保留每条边原始签名/来源/负例，对公共设施和同slot伪关联做压力测试 |
| BL-11 历史保留 | Journal约24h、WTrack约7天、钱包页近期Swap；6h/12h异动、跨日研究和长历史覆盖不等价 | `RESEARCH`：不同数据层存在但没有统一覆盖水位 | 形成市场事件 vs 钱包原始交易 vs 历史库存的独立保留/补数策略；借鉴Pulse的归档理念 |
| BL-12 旧钱包模块测试 | 7项WTrack标签/分组/成员隔离测试未过；原实现缺失被测方法 | `NOT_VERIFIED`：[CI](https://github.com/sunshihao001/grok/actions/runs/42481576097)，尚欠基线同环境对照 | 与blix原基线做CI差异归因，确认产品实际入口后决定补功能或更正过时测试 |
| BL-13 重复与重试 | `wallet_trades(sig,wallet,mint)`聚合多事件；某些流标记已读/重试与原始记录提交边界 | `CODE_PROPOSED / STATIC_RISK`：PR#19调整readSigs；没有系统复测多源重复及断电 | 原始事件、钱包聚合、Journal、WTrack每层定义唯一键与重入预期，用断点失败注入核对 |
| BL-14 只读隔离 | 原Server仍含账户/交易/自动领取/付费AI；npm start门禁不覆盖所有启动入口 | `NOT_VERIFIED`：[原只读安全审查](read-only-safety.md) | 明确只读运行的进程/网络/权限/成本隔离，未经授权不启动；MCP白名单不等于Server全只读 |
| BL-15 UI与MCP | Coin、Wallet、BubbleMap、AI如何显示同一证据链；新证据GET仅本地接口且非产品UI | `RESEARCH`：已有页面与MCP，但新经济调查未贯通 | 使用已有页面验证最小可解释调查；不要新造第二个市场终端 |
| BL-16 AI专业认知 | Hermes、qb-、meme-、Why-Solana、22视角与ai-d方法能否改变同一Mint的判断 | `NOT_VERIFIED`：知识导航/材料存在不代表运行时检索或准确性提高 | 同一冻结事实做无知识/相关知识对照，看遗漏、误归因、反证质量、成本；不要机械堆专家 |
| BL-17 外部复用 | Million资金/钱包链、PumpTrace持久回补、Pulse归档、OKX/GMGN数据能力选择 | `RESEARCH`：相关成熟原源码已查，尚未实跑/比较真实数据成本 | 先对准 BL-04/06/11 的实际缺口，比较整用、小改和API接入，明确失败条件 |
| BL-18 运行可靠性 | 钱包stream/poll限额、429/错过水位、SQLite大小/重启、云端是否能长期执行 | `NOT_VERIFIED`：代码存在预算/漏记统计，但实际云电脑运行未验证 | 安全隔离后做历史缺失率、恢复、磁盘与额度验收；不拿单测当持续运行 |
| BL-19 监控与机制价值 | 多Mint同群体、6/12h异动、库存迁移、刷量、内幕同步和经济机制探索 | `RESEARCH`：相关理论与部分功能存在，缺真实稳定样本链路 | 先得到覆盖可信样本，再研究机制vs竞争解释、阴性对照、预测基线和可重复性 |
| BL-20 发布/权限边界 | 新feature与PR#19均未合入blix；各PR#14/#16/#17保留历史知识/工程但非当前Blix功能 | `NOT_VERIFIED`：当前分支与PR元数据核查 | 每轮同步分支/CI/权限/实际部署四种状态；不能用PR存在替代功能上线 |

**约束：** 状态不能因为写了新文档自动由 RESEARCH 变 DONE；只对会改变产品决策的点开展下一轮深研究。所有条目允许合并、降级、重排与关闭，但保留原始链接和推翻理由。

## 3. 下一轮真正研究：能否复用现成钱包历史，避免重造接收钱包扫描系统？

### 研究问题（跨业务，而非只改一行代码）
在不增加一个独立跟踪器、不读取全链历史、不启动交易进程的条件下，Blix 现有三个钱包观察入口和成熟项目历史服务，能否让 **“Mint A的W1转给W2，W2后来卖出/转移资金”** 得到可靠且有覆盖说明的解释？

### 本轮独立源码对照所得（SOURCE_READ，并非运行验收）

| 现成入口 | 源码能做的事 | 关键不足 / 对产品路线的影响 |
|---|---|---|
| [Blix `wallets.scanWallet`](https://github.com/sunshihao001/grok/blob/blix/server/wallets.js) | 对指定地址最近15个签名中的最多12笔成功交易执行readTx，支持临时查看而非长期跟踪 | 不能声称找遍W2历史；原readTx摘要不保证多动作/Token转账完整；未来可复用其RPC/限速入口，但不能无条件接入新候选 |
| [Blix `walletpage.js`](https://github.com/sunshihao001/grok/blob/blix/server/walletpage.js) | 任意钱包按需页面、Token holdings、最近Swap；优先Helius type=SWAP，后备签名/RPC并发；已有UI入口 | **最有价值的现成按需产品入口**，但只显示近期Swap摘要、Helius价格与成本且有额度消耗；并不能提供完全的直接Token转账证明 |
| [Blix `wtrack.js`](https://github.com/sunshihao001/grok/blob/blix/server/wtrack.js) | 用户/成员明确关注后，流与轮询持续看钱包，Wallet Reader共享链读取；有feed和transfer | 目前不会因自动识别Token接收者就订阅W2；旧转账摘要遇Swap可能直接跳过；更适合“调查升级为持续监控” |
| [Blix `replaywallets.js`](https://github.com/sunshihao001/grok/blob/blix/server/replaywallets.js) | 现成Mint维度回放补钱包，分页cursor存于SQLite，分批限速，按slot/time近似匹配Journal旧成交 | 是 **Mint级交易参与人补齐**，不是W2跨Mint全钱包历史；±时间+规模配对是候选，不能升级为原生交易签名的确定性归属 |
| [PumpTrace `backfill-manager.mjs`](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs) | 持久化job/cursor、暂停恢复、429重试、按时间窗和交易量上限、CAP_REACHED不是COMPLETE | 可借**业务级的可恢复历史回补语义**，不必整移新后台；其Helius取交易也有指定版本、过滤和配额限制 |
| [Million `helius.service.ts`](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/helius.service.ts)及[`funding.service.ts`](https://github.com/Kelows/million/blob/main/apps/api/src/funding/funding.service.ts) | 分SWAP/TRANSFER/ALL历史，分页、truncated；资金关联最多3页/部分候选预览，避免无限读 | “有资金链”需区分类型过滤与跨类型历史；hub/公共设施、截断和旁支交易导致假同控，不能原样搬模型 |
| [Pulse归档](https://github.com/nirholas/pulse/blob/main/src/archive/archive.ts) | UTC日文件、git版本归档和恢复机制；记录已完成日期 | 可借鉴可回放与断电恢复的思想，但Pulse选择性采集不是对每个Token的全链归档 |

### 本轮形成的两项新判断

**判断A：缺少接收钱包后续结果时，有两种完全不同的原因。** （1）W2确实有卖出，但尚未被Blix跟踪、钱包页/历史查询被截断、某场所解析不支持；（2）在被确认完整的时间范围内W2没有相关卖出。当前 `recipient-outcomes` 返回空结果不足以区分这两类。产品上应默认 `NOT_OBSERVED_IN_CAPTURED_WINDOW`，**不能显示成“W2没卖”**。

**判断B：最先值得复用的不是新的钱包订阅器，而是原有按需钱包页 + 受限历史补查语义。** 钱包页已有价格、仓位、交易与UI；PumpTrace有持久cursor和预算状态；Million给出交易类型覆盖的提醒。但直接把钱包页Swap摘要当成完整Token经济事件会丢失混合交易。因此推荐 **按需看已有事实 → 判断覆盖是否不足 → 对少量高价值W2进行带预算的原始历史补查 → 只有需要长期观察且获许可时升级到现有WTrack**。这是下一项可验证路线判断，未实施。

### 两条竞争路线及可推翻条件

- **路线1（优先验证）：复用Blix现有`walletpage/scanWallet`+已有经济证据表，在安全隔离环境针对选择的候选地址执行有限原始交易补查**。优点是保留Blix整套产品；风险是只靠最近交易和Swap过滤会漏历史转账，必须补覆盖水位/未观察字段。若真实归档证明该路径缺乏足够事件粒度或成本明显高于成熟服务，放弃它。
- **路线2（备选）：复用PumpTrace可续传的历史回补任务语义/程序，或结合Million分类历史查询**。优点是处理历史更深入、游标/成本较成熟；代价是新依赖、配额与不同归因口径。只有路线1在真实案例中失败时，才尝试有限引入；不必为了“成熟项目”整套搬运。

**目前暂停**：批量自动追踪W2、付费RPC、主服务启动、真实链或钱包实跑、修改交易/账户代码、AI自动付费研究、云端部署。代码修改可继续在独立审查分支做可逆且无外部效果的测试/文档，但本轮选择研究和记录，不继续扩大全面变更。

## 4. 下一次验收如何知道研究不只是说法？

至少选一个可复现签名集合或离线夹具，让同一链出现：
- W1买入Mint A且同笔向W2转Token；
- W2卖出（可能有中间Token账户转移或多池Swap）；
- W2向W3转SOL，W3买Mint B；
- 一笔同Slot、同交易所/公共设施造成的**反例**；
- 一条W2后续真实发生但不在已有Ledger里的记录，以及历史截断的**反例**。

沿 Blix已有对象验证 **事件数/去重、Owner/TokenAccount、指令/CPI、金额与库存、时间/slot、walletpage覆盖、补查游标、钱包是否被监控、各UI显示、竞争解释和 UNKNOWN**。允许最初只做静态来源契约与离线测试，不声称真实验收；只有可隔离环境且有明确授权才运行真实链调查。

**研究停止/转工程条件：** 已有足够源码证据判定路线1/2的优先级时，不再扩张项目清单；选择最小离线验收任务。若发现新的会改变产品方向的缺口（例如外部服务直接提供可信完整历史），立即修订本表与优先级，而不是机械按编号推进。

## 5. AI 后续如何使用这个台账（非固定提示词流程）

1. 先读用户目标与这份台账，恢复上一轮**做过什么、没验什么**，选择一条能连接市场、经济机制和工程结果的真实任务。
2. 先读 Blix实际UI→API→数据，再按信息价值查 **GitHub成品项目与源码/测试/失败记录**；仅当原理/标准/术语仍不确定时补官方协议、经典资料、论文，必要时参考X/Reddit的可复查实践。
3. 主动寻找对当前方案最不利的反例；新认知应改变调查问题、功能选择、可信度或验收，不以搜索次数/专家数量/写作篇幅计进度。
4. 能用授权内工具验证就验证；不能运行就标来源级别。记录：**本轮新增认识、改变的选择、仍未知、哪条台账状态变化、最有信息价值的后继实验**。
5. 允许新线索登记为研究候选；不要求全部项目同轮读完，更不以台账替代思考。重要的运行/资金权限由用户决定。

上述研究方法沿用 [ai-d 对GitHub成熟项目与研究深度/停止机制的源码审查](https://github.com/sunshihao001/ai-d/blob/main/research/2026-11-07-open-source-research-depth-scope-stop-audit.md)，只借方法，不增加Blix固定Agent制度。

## 6. 后续同步与修订规则

- 本文件放在 `blix` 的文档专用PR，便于与未合并的经济证据PR分离；被合并前只在本分支存在。**PR#19未合并并不妨碍这份全项目台账独立审阅/吸收。**
- 若变更涉及单个技术事项，在相应源文件/PR修正和验收后，更新此处状态、源码链接与验证等级；历史研究原文仍存于原文档，不复制冗长材料。
- 下一轮真正使台账有价值的，是在同一具体钱包链的真实数据或离线反例上，**更改一个错误假设、排除一种复用路线或证实一个可运行增量**。
