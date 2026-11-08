# Blix 滚动建设台账｜继承、修复、研究与验收

> 2026-11-08 初版。**这不是新的产品架构或专家体系**，仅作为当前 `blix` 主体的一个持续更新的工程事实清单；以后说“按照建设来”时，先更新状态和证据，再按信息价值/业务价值选下一项工作。旧知识和历史参考原位保留，不机械挪入本表。
>
> 主体：`sunshihao001/grok` 的 `blix`。本表目前随 [Draft PR #18](https://github.com/sunshihao001/grok/pull/18) 保存在功能分支，**未合并、未部署**。PR基线 `3bc1f7d4`；本表的状态不能代替对最新提交的重新核验。

## 风险锚点｜在下一轮研究前判断“值得研究”与“研究方法是否有效”

> 此条来自用户 2026-11-08 新增要求，服务于产品价值与真实进展；**不是另设固定阶段、专家委员会或让 AI 更保守**。通用原理维护在 [ai-d 研究锚点](https://github.com/sunshihao001/ai-d/blob/main/README.md)，此处只保留 Blix 的具体决策和证据。

在继续投入某一条工作线时，判断：**(1) 值不值得**：解决后是否确实改变“发现Mint→买入→转移→接收方卖出→跨Mint”以及最终产品价值；**(2) 做法是否正确**：有没有最短的可证伪实验/完整成品可复用，而不是重复搜索、继续罗列模块或堆 AI 文档；**(3) 有没有新进展**：本轮相比上一轮新增了何种事实、可运行代码、反例或决策；**(4) 该怎样转向**：继续、换方法、实施验收、暂停或停止，下一轮何种观察会推翻选择。**只有无实质增量的研究轮次需要明显调整；不强制在每个普通问答里填表。**

### 本轮选择实判（2026-11-08）

| 比较路线 | 对核心业务目标的价值 | 当前证据 / 判断 | 决策 |
| --- | --- | --- | --- |
| **B02 已读处理水位与失败重试** | 高：已有RPC但下游漏记会中断接收钱包及买卖关系 | `wallets.readTx` 在 `readSigs.add` 后才执行下游钩子，存在“源数据已经保存但钱包侧未完整处理”的可推导失败；独立故障注入能直接区分假设 | **先做短程确定性故障注入和可核查最小修复；有效则验收，失败则调整实现** |
| **B03 历史覆盖/游标** | 高：不发现签名则任何解析器都无法还原交易 | `missingEvidence` 仅列已知交易行缺原文，不能发现未知签名；PumpTrace已有可续传作业可借鉴 | **保持P0，B02后用真正漏签名的反例选择有限改造/成品复用**；不先扩建采集系统 |
| 直接做更多跨Mint网络图/AI提示词 | 当前边际价值低：上游缺事实时只会漂亮地放大错误 | 已经拥有候选API与AI研究入口，新增概念不能弥补交易缺口 | **暂停，待事实链与来源/覆盖可靠后恢复** |
| 重扫全部参考项目/重建一套后端 | 当前边际价值低：已有Blix主体与Journal、Wallets、成品回填参照 | 再重复做全目录摘要不会直接验证漏记是否存在 | **停止重复梳理，除非有新证据说明主体无法承载** |

**推翻点**：如果B02失败注入证明现有日志/事务已经有效恢复下游，B02降级，不为预设错误继续写代码；如果最小改动导致更多重复记账、报警或性能损失，则改为成熟队列/持久事件消费模式；如果B03实际采集成本或RPC额度不可接受，优先使用成熟托管数据或离线归档，不盲目无限回填。

**方法风险诊断**：当前方向**有价值**，但“再补一批文档、归纳更多专家方法”不是解决当前工程缺口的有效办法。因此本轮直接把B02转化为故障注入与修复，B03继续保持关联待办；不把是否有更多登记项当成进度。

## 状态约定（防止“计划=做完”）

- **已验证/限定范围**：测试或源码证明具体事项，须写明环境；不能推导生产已运行。
- **待修复**：有具体代码路径与可构造的反例，尚无已验收修复。
- **待验证**：可能的重要缺口，仍需要离线反例、真实RPC签名、运行日志或成本测量。
- **阻断**：会影响合并/安全部署，优先说明阻断条件。
- **保留**：已有可复用成果，不因本轮关注其他点而删除或重新开发。

## 业务链与滚动事项

| ID / 重要性 | 阶段与问题 | 当前事实 / 状态 | 下一项可核查动作（通过条件） | 已知位置或复用 |
|---|---|---|---|---|
| B01 / P0 | 原始交易证据保留与重放 | **已验证/限定范围**：PR #18 以完整 `jsonParsed` RPC 对象归档，外层/CPI逐位置索引；13项新增CI通过；不代表全链覆盖 | 核验真实v0/ALT、Token-2022、新建/关闭账户与多CPI，记录所有不可解码项目 | `server/economic-events.mjs`、`test/economic-events.test.mjs`；Solana官方交易规范 |
| B02 / P0 | 钱包读签名的**处理成功水位** | **已部分修复、离线验收**：`econ_wallet_processing` 将 `CAPTURED/RETRY_REQUIRED/COMPLETE` 分开；`readSigs` 只在钩子与账本处理后写入；失败优先从本地RPC归档重试并有有限次数恢复查询。GitHub CI 对故障注入、缓存、共享签名、限次选择已通过；**未做完整服务重启/持续断流实跑** | 在严格隔离环境验证真正进程重启、定时任务恢复、数据库锁与告警副作用；防止重复报警；确认5次失败后的人工检查路径 | `server/wallets.js`、`server/economic-events.mjs`、`test/wallet-evidence-retry.test.mjs`；不把本次限定验收写成全历史完整 |
| B03 / P0 | **已知缺口≠历史完整**，持续回填/断点 | **待修复**：`missingEvidence` 只比较现有 `wallet_trades` 与 `econ_transactions`；漏掉根本没识别成 trade 的签名。内存集合和部分分页不等于永久覆盖证据 | 在单个钱包上登记 `[起止slot/签名边界、游标、总数、成功/失败、完整/截断原因]`；断流、429、重启后从同一锚恢复；不能把 `CAP_REACHED` 标 `COMPLETE` | 优先复用 Blix `wallets.pageSignatures`，PumpTrace `BackfillManager` 的可续传任务状态 |
| B04 / P0 | Swap + 转账、一个签名多个事件 | **已验证/限定范围 + 待修复**：新层能存多个原始指令；旧 `wallet_trades/wt_transfers` 仍按签名+钱包+Mint折叠；`wtrack.fromTx` 在命中swap时跳过转账 | 以买入1000转出400、同签名转给B/C、多池CPI作为回归；钱包摘要/监控不再把余额净变化说成实际买单数量 | `solana.parseSwaps`、`wtrack.fromTx`、`journal.tradeKey` |
| B05 / P0 | 接收方是钱包、池还是公共设施 | **待验证**：`recipientCandidates` 返回能够识别Owner的Token指令边；AMM Vault/池参与者也可能匹配；当前不能无条件称“接力钱包” | 加入已知池+普通接收方对照及来源证据。原始边保留，按 `pool/infrastructure/unknown/wallet-candidate` 明确分类；不得由同slot/fee payer推断共同控制 | `bubblemap` 池标签、`coin` 交易对、PumpTrace wallet intelligence |
| B06 / P1 | B卖完后仍可发现、按需跟进 | **待验证**：当前Holder快照不能代表历史接收方；新候选查询可见历史边，但无自动历史扩展 | 合成/真实事件：B当前余额0，仍能从历史找到A→B；对候选启动**显式有预算的只读历史调查**，不得无界递归或擅自监控所有钱包 | Million Wallet→Mint→Wallet 双向扩展，Blix现有Wallet页面 |
| B07 / P1 | 卖M→转SOL→买N 的资本解释 | **已验证/限定范围**：PR #18 合成时序能输出候选，不能证明同批SOL/同一经济控制 | 做时间、数量、手续费、账户前后余额约束，排除公共交易所/路由；用反例证伪“同源资金”；无法排除则标 UNKNOWN | `crossMintCandidates`；Why-Solana 对照/负例、Million 资金边 |
| B08 / P1 | Token Account/Owner/Authority等角色 | **待验证**：新层仅根据RPC pre/post token balance owner映射；本交易中新建/关闭、Owner变化、无法识别的CPI仍可能为 UNKNOWN | 使用RPC真值和合成反例：新建/关闭Token账户、Token-2022、ALT/v0；区分`accountIndex`、地址与Owner；冲突不强行回填 | 官方 Solana JSON-structures、transaction-introspection；已登记的M01适配器 |
| B09 / P1 | 全量RPC归档成本和故障恢复 | **阻断生产**：`econ_transactions.rpc_json` 无保留期/空间预算，表只增不减；没有持久化的批次级覆盖检查点 | 测量100/1000/10000交易空间与写延迟，设置明确上限、归档和恢复策略；断电/数据库锁后验收原始证据与游标一致性 | PumpTrace 原文分仓+持久任务；Blix `journal` 限期与gap/repair |
| B10 / P1 | 错误资金关联：Funder/fee payer | **待修复**：Bubble Map历史过长返回空并长期缓存；在找不到直接转账时退化为fee payer = funder | 3页截断/代付手续费离线反例；显示 `HISTORY_TRUNCATED` 和 `FEE_PAYER_ONLY`，绝不自动生成 `DIRECT_FUNDER` | `server/bubblemap.js:109-151`；既有 `mint-cross-module-evidence-audit-v0.2.md` R1/R2 |
| B11 / P1 | 同一Mint持仓与供应量口径 | **待修复**：`holders.js` 可用动态供应量；`coin.js` 多处1e9；链上快照 `partial:false` 不等于历史完整 | 5亿供应、1亿持仓的20%测试；各数据表都回传 `source/slot/observedAt/denominator/historyCoverage` | 既有V0.2审查R3/R4，不删历史结论 |
| B12 / P1 | 发现与真实市场样本 | **保留/待验收**：Blix已有Mint发现、Pool和发行生命周期；历史真实Mint的3份供应商快照存在，但没有真实交易签名序列 | 对 `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` 取**安全隔离的历史签名**，检验Pool库存变化是Swap还是LP、是否确有A→B | `single-mint-audit.md`、旧PR #16；优先复用现成采集 |
| B13 / P1 | AI/产品报告把事实连起来 | **待实施**：现有 `mint-facts` 只从少数本地API取信息，新证据未进报告、MCP与UI | 一个Mint完整报告展示事件路径、签名/位置、已知/未知、覆盖缺口与竞争解释；不将示例假设写成“内幕已确认” | `server/intelligence/mint-facts.mjs`、旧Hermes/qb-/meme- |
| B14 / P0合并门槛 | 原有CI测试不一致 | **阻断**：PR #18的GitHub Actions 420项中412过、8失败；新13项全部通过。8项与引入新测试前一致，包括旧状态断言及7项WTrack测试 | 对比`blix`同基线确认8项归属；将修复放独立且最小化的工作项，避免为清绿灯伪改断言 | [PR #18测试运行](https://github.com/sunshihao001/grok/actions/runs/42419470824)、[Audit通过](https://github.com/sunshihao001/grok/actions/runs/42419470857) |
| B15 / P0安全门槛 | 运行/交易/付费隔离 | **阻断**：本轮只静态、离线测试和GitHub代码写入；原Blix仍有交易、签名、费用路径 | 单独验收只读隔离、配置/密钥、请求成本和监控后，再考虑真实Mint主网只读回放、云端上线 | `docs/project/read-only-safety.md`；绝不把PR通过等同生产可启动 |

## 2026-11-08｜继承检查与下一轮综合研究（第一轮已完成）

**核查输入**：PR #18源码/13项CI结果、旧 `mint-cross-module-evidence-audit-v0.2.md` 和 `single-mint-audit.md`；Blix `wallets.js/wtrack.js/bubblemap.js/solana.js`；成熟参考工程 PumpTrace 的 `src/modules/backfill-manager.mjs`、Million 的 `apps/api/src/crawler/crawler.service.ts`，Solana 官方 `getTransaction`/JSON结构及 transaction-introspection。

**发生的专业认识变化**：

1. **“保留原文”与“历史采集完整”分属两个独立验收坐标**。PR #18确已保存被获取的 `jsonParsed` 响应对象，但如果根本没发现某笔签名，`missingEvidence` 就无法列出它。原来“欠缺补查”要升级为“独立的签名历史覆盖登记”，不能只比较Trade表的有无。
2. **连续性需要三层状态**：`signature discovered` → `raw transaction captured` → `economic events indexed/consumed`。`readSigs` 的内存标志不能同时代表这三层成功。PumpTrace的 `QUEUED/RUNNING/RATE_LIMITED/CAP_REACHED/COMPLETE/ERROR` +游标持久化、重启恢复，证明成熟成品已有更稳妥方法。
3. **不宜直接复制一套PumpTrace/Million后端**。Blix自身已有 `pageSignatures` 分页、Journal签名事件去重与gap/repair；最小路线是补持久水位和失败重试语义。Million的**单次信用额度约束、停机后状态可见、垃圾钱包过滤**可用作候选扩展约束。
4. **不要夸大Solana v0/ALT障碍**。官方规范确认 `jsonParsed` 的 `accountKeys` 可包括地址表加载地址；当前 `keyOf` 可读取其pubkey。不过未经实测的Token账户新建/关闭、CPI层级/stackHeight、部分解码指令仍然需要独立验收。若要解析更完整的原始线格式，优先评估官方 `@solana/transaction-introspection`，而不是臆造全套解码器。
5. **产品价值检验必须贯穿三场景**：发现Mint后追踪所有签名是否有覆盖水位；单Mint以指令确定Token的真实接收方并辨别池；跨Mint仅在收集到卖出、SOL转移和后续买入三种独立事实时给出可证伪候选，不将时序网络等同经济主体。

### AI选择的下一件实施工作

**优先 B02 + B03（一个连续目标）**：在已有Blix wallet reader上做**处理状态/签名覆盖水位与恢复**，而不是先做美观的跨Mint关系图。

- 先造确定性失败：RPC原始交易保存成功，后续钩子/摘要写入故障；重试不得因 `readSigs` 误判完整，也不得重复记账。另造一页历史缺口：`wallet_trades` 中没有某签名，但签名API实际返回它；系统须登记未捕获，不可报“完整”。
- 复用原 `wallets.pageSignatures` 和 `journal` 机制，按信息价值借鉴PumpTrace的有限任务和游标；优先**少量增补**，不要重建另一个采集服务。
- 停止条件：两条失败先能复现，修复后离线测试可证实（多钱包相同签名、429/超时、重启、被截断、未完全完成四类反例），且不启动交易或不明付费接口。若在既有DB模型下不可实现，才追加最少的状态表。
- **本轮已形成真实工程增量**：故障注入复现“RPC已保存但下游处理失败”的路径；新增 `econ_wallet_processing` 持久状态、已保存原文重放、watching钱包有界重试选择与轮询挂钩，CI离线用例已通过。不能据此认定真实重启/429/长期监控通过。
- **下一项改为 B03 的独立漏签名反例**：先用 `pageSignatures` 证明某签名未形成任何 `wallet_trades`，再设计受限的覆盖水位与游标；如接入成本高于直接复用PumpTrace/托管源，允许转向，不沿当前方案强推。

**本表维护原则**：只在同一表里原位改变条目的状态、证据和下一动作；重要反例或外部新证据改变排序时允许提前跳转。完结的条目保留链接和条件，不删除；每次最多执行当前最有价值的一两项，其他问题留在台账内自动继承。


### 风险锚点的首个实际检验｜2026-11-08

- **价值判断**：B02直接影响单Mint调查和接收钱包监控的证据连续性，值得修；B03同样重要，但不能用B02已完成来掩盖“从没发现的签名”。
- **方法改变**：停止只讨论“应该有重试机制”，转为可复现的“下游hook故障→持久RETRY_REQUIRED→使用旧RPC归档重放→COMPLETE”，并新增筛选自动重试候选的有界条件。与原来从源代码提出的可能风险相比，现有GitHub CI已对故障链完成测试。
- **可检查产出**：新增4项钱包Reader直接测试与2项重试选择测试，连同前13项经济事件测试，合计19项新增测试全部通过；最新全项目CI为426项418过8失败，仍保留基线故障。静态审计通过。
- **仍未证实**：本次没有启动Blix生产服务，没有真实钱包RPC或故障重启完整实测；旧WTrack业务输出/自动跟踪接收方/全链历史覆盖尚未完成。
- **继续价值阈值**：下轮若只是增加相似“断点续查应该如何做”的文章而不能获取明确的漏签名反例、游标状态或成熟成品成本比较，则标记“方法无增量”，改研究途径；若B03被现有服务完全解决，则停止自建重试服务。

## 原始出处

- Blix：`server/economic-events.mjs`、`server/wallets.js`、`server/wtrack.js`、`server/solana.js`、`server/bubblemap.js`，以及本仓库 `docs/project` 的既有审查文件。
- [PumpTrace backfill-manager](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)
- [Million crawler](https://github.com/Kelows/million/blob/main/apps/api/src/crawler/crawler.service.ts)
- [Solana JSON 结构](https://solana.com/docs/rpc/json-structures)
- [Solana Transaction Introspection](https://solana.com/docs/core/transactions/transaction-introspection)


## 2026-11-09｜快速开发纠偏登记（继承 2026-11-08 PR #23）

本节只对**上一轮已经发生、已经定位的工程失误**做原位登记；不新增另一套 AI 方法论或重做分阶段架构。审查的固定起点为 [PR #23](https://github.com/sunshihao001/grok/pull/23) `26b354851b6a29624bb3273e312915a4f0f59f4f`（此 SHA 为本轮初始基线，后续按实际提交更新）。`blix` 主分支、其他研究分支会继续变化，不能再把它们当作同一版本。

| 记录 | 上轮具体错误/失败证据 | 修正原则及本轮处理 | 完成判据 |
|---|---|---|---|
| R-01 遗留红灯被长期合理化 | PR #23 全量 Node24 CI 446 项中 439 过、7 失败；基线同名失败只能排除**新增回归**，不是发布许可。[精确指纹](https://github.com/sunshihao001/grok/actions/runs/42491184903) | 先用已经存在的 `test/wtrack.test.mjs` 作为红色用例，核对源代码的真实功能缺口；只修缺口，不伪造断言、不标“发布通过” | 全量 `npm test` 真正退出码 0；否则保留 blocker |
| R-02 重复设计与分支堆叠 | PR #21、#18 独立建立重试状态；PR #22 才收束，PR #23 再整合，历史 PR 仍未合并 | 使用 PR #23 作为**唯一当前集成工作分支**，不再新建重复状态机制，保留 `econ_wallet_processing` 单一处理状态 | 新功能不创建并行的捕获/消费状态表，合并前做一次整体差异审查 |
| R-03 测试证据展示不严谨 | 曾因 `continue-on-error` 将失败步骤显示为成功；用非 TAP 输出却按 TAP 解析，得到空失败指纹 | CI 正常失败不可屏蔽；记录每次运行的 ref/SHA、退出码、测试量及原始 Actions URL；诊断脚本必须匹配实际 reporter | 全量与专项测试分别真实检查，任何失败不得用“成功步骤”概括 |
| R-04 过早把隔离测试当产品运行 | PR #23 只跑 Node24/SQLite 合成路径，没有实测 RPC/真实钱包、长期重启和部署，只读安全门禁拒绝启动旧服务器 | 状态严格分离 `ISOLATED_TESTED`、`INTEGRATED_TESTED`、`LIVE_VERIFIED`；先有与交易/签名/付费隔离的运行入口再考虑主网验收 | 不以 CI 成功声称主网、UI、完整钱包历史和真实同控 |
| R-05 研究代替交付 | 多轮知识整理与大量 Draft PR，未让主体形成统一、可发布版本 | 优先实测反馈→根因→最小代码修复→真实回归→记录，并对新研究规定必须改变现有决策或测试 | 每轮至少一条可以在仓库内检查的新验证、修复或有根据的停止决定 |

**本轮快速开发方法（借鉴成熟工程做法，不能机械套用）：** 以仓库为事实来源，选一个明确阻断；锁定 PR SHA；对照现有失败测试与真实 API；小范围更改后运行 `test/wtrack.test.mjs`→`npm run test:evidence`→`npm run test:security`→`npm test`；任何失败立即回到首个可重现根因，不继续大规模搜索或同时开多个重叠 PR。代码级问题参考 [obra/superpowers 执行与验证](https://github.com/obra/superpowers/blob/main/skills/executing-plans/SKILL.md) 的完成契约，[OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) 的仓库事实源/反馈循环与 [Anthropic 长任务工程](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) 的跨轮工件继承；这些是工程方法类比，不是 Blix 的运行证据。

**本轮所选改动：B14/R-01。** WTrack 测试对命名组、成员隔离、开发者分类、备注持久化和导入/导出提出明确契约；现有 `server/wtrack.js` 还没有相应数据库列与接口。先按原测试进行最小完整业务修复，而不是删掉测试或仅改状态文档。若单项修复导致旧 UI/成员权限变化，保留失败日志并复核实际产品契约。R-04 的安全隔离和真实链上测试仍为独立后续门槛。

### 2026-11-09｜R-01 第一轮验收结果与下一最短交付路径

- **提交**：`f14dd66561209bfc503920f6767a14775c1c1aa3`，在 PR #23 集成分支修复原有 WTrack 分组/标签/备注/导出导入契约；未修改原断言使其失效。
- **真正的外部执行结果**：[Node 24 全量/安全/经济证据同一 run](https://github.com/sunshihao001/grok/actions/runs/42527333948)，三个步骤均为真实 `success`；[独立审计](https://github.com/sunshihao001/grok/actions/runs/42527333985) `success`。先前 7 个 WTrack 红灯已经在该候选版本消除，未再做静态推断代替回归。
- **验证范围**：`INTEGRATED_TESTED`，仍非 `LIVE_VERIFIED`，也非已合入 `blix` 主体。新增 WTrack 分组功能的现有 API/UI 接入范围未在此次独立实跑证实。
- **本轮技术结论**：长期红灯不是必须接受的“历史噪声”。排除回归与关闭发布阻断是两件事；先利用原测试还原既有契约，直接修正实现比重复讨论风险更快。
- **下一真正的产品缺口（承接 B13/B15）**：只读报告不能依靠启动带交易、自动领收益和模型费用路径的原主服务。优先检查是否能用现有 `economic-events.mjs` 与 SQLite 档案，直接生成**无网络、无签名、无新后台**的单 Mint 证据报告；用一条具体离线交易链验收。若现成脚本已完全解决，则不再开发第二个入口。此方向可以被可运行的既有脚本或成本证据推翻。


### 2026-11-09｜R-04 第二轮：独立只读报告的可运行验收

**发现的问题**：PR #23 的经济事实已经能在 SQLite 内形成接收方、后续卖出、跨Mint时序候选；但只通过测试或原服务 API 访问，不等于在安全边界内可直接得到可阅读的单 Mint 调查结果。原 `server/server.js` 仍含交易/签名/自动费用路径，不能为查看结果直接启动。

**本轮修正（同一 PR #23 分支，非新成品）：**
- 复用现有 `server/economic-events.mjs` 的 `recipientOutcomes` 和旧数据表，新增单独的 `scripts/inspect-economic-mint.mjs`。运行 `npm run inspect:evidence-offline -- --db EXISTING.sqlite --wallet BASE58 --mint BASE58`，打开**已经存在**的 SQLite 为 read-only，且设置 `PRAGMA query_only=ON`；只向标准输出打印有限的元数据与候选关系，不启动主服务器、RPC、交易、签名、模型及后台任务。
- 报告明确显示 `knownSenderMintCaptures`、本地签名窗口、`lifetimeHistoryComplete:false`、`sellObservation` 与 UNKNOWN；卖出与跨币关系只为候选，不能证明转入库存卖出、同控或资本来源。
- `test/offline-mint-report.test.mjs` 对一个带 RPC 原文索引的合成 SQLite 验证 A→B Token 转移、B 后续卖出、未知覆盖以及**文件 SHA256 执行前后不变**；另测空数据库与缺失数据库 fail-closed。**这是隔离数据回放，不是主网实测。**

**代码与真实验收**：集成候选 `3d2ed0e8bf5bfa2e341fc4dab2d1b0bb779909a2`；[Node24 全量、安全、经济证据 CI 全通过](https://github.com/sunshihao001/grok/actions/runs/42527683586)；[独立审计通过](https://github.com/sunshihao001/grok/actions/runs/42527683587)。不虚报实际链上覆盖、正式服务或 Grok Bot 云端已运行。原有 PR #23 仍是 Draft，且直接基于 PR #22 而非 `blix`；本次**没有合并**。

**下一轮只保留真正阻断运行的缺口：** 对一批带来源、slot、签名的真实公开 `getTransaction(jsonParsed)` 归档在隔离环境做同报告回放；检查 Token-2022、同笔 Swap+Transfer、多池、Owner缺失、历史截断及覆盖说明。随后评估独立只读进程和现有 UI 的最小对接，而不是直接把原服务安全门禁打开。若真实 RPC 原文获取受供应商额度/历史可用性限制，记录其为 `UNKNOWN/NOT_AVAILABLE`，不自动拓展付费数据源。
