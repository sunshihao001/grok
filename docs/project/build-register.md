# Blix 滚动建设台账｜继承、修复、研究与验收

> 2026-11-08 初版。**这不是新的产品架构或专家体系**，仅作为当前 `blix` 主体的一个持续更新的工程事实清单；以后说“按照建设来”时，先更新状态和证据，再按信息价值/业务价值选下一项工作。旧知识和历史参考原位保留，不机械挪入本表。
>
> 主体：`sunshihao001/grok` 的完整原版 `blix` 产品。**2026-11-09 当前唯一集成候选为 [Draft PR #23](https://github.com/sunshihao001/grok/pull/23)，现已直接以 `blix` 为base，包含历史PR #18/#22能力而非待合并的平行产品；仍未合并/部署**。本表下方旧日期的PR #18状态为历史记录，必须以最新状态节和GitHub CI为准。

## 2026-11-09｜原版保留 + 专业二次开发：已实施的工程保障（最新）

**用户产品范围明确：原作者 Blix 全部功能都要保留。** 原版行情/行情图表、Discover/Pulse、Mint/Coin、Holder/Bubble Map、Wallet/Tracker、AI研究、账户、纸面与真实交易、通知、Web/Worker和运维组件均是产品目标，不是被只读研究替换的冗余功能。**安全运行授权**与**原版源代码完整保留**分别决定，不允许因临时禁止签名/交易/模型费用就静默移除原版。

### 与原始完整产品快照的可核查差异

- 原始导入基准：`e2c69d42dcdae7690f9d47e0d0e7e8257ed48326`，有767个原始文件。
- 2026-11-09 本轮集成候选：原始767个文件**全部保留路径**，其中28个预先选定的核心`server/engine/pulse/coin/holders/bubblemap/journal/brain/research/accounts/hosted-accounts/tradeapi`等、Web UI/Worker仍与原始快照**字节一致**。仅`server/server.js`、`server/wallets.js`、`server/wtrack.js`三个原有业务文件因扩展被修改，原有测试和业务行为需继续回归。
- 新增`test/fixtures/blix-import-baseline.json`保存完整路径基准及28个原版核心指纹；新增`test/original-blix-preservation.test.mjs`检查全部文件存在、关键模块指纹不变、原有产品脚本和扩展触点。**这不是交易可安全运行、所有UI可访问或功能实际正常的证明**；合法升级会在充分回归后显式更新保护指纹。
- [PR #23 初次 CI](https://github.com/sunshihao001/grok/actions/runs/42537444961)：Node24全项目**452/452**、安全**20/20**、经济证据**42/42**；[审计通过](https://github.com/sunshihao001/grok/actions/runs/42537444927)。本节提交后须再次检查新CI；此前CI只证明原PR分支代码，不能自动代表合并到最新blix的运行验收。
- **版本路线已收束**：PR #23 从依赖分支改为直接对照`blix`的累计Draft集成审查入口；旧PR #18/#22可留作沿革与源码证据，不重复合并同一状态机。未做合并、关闭旧PR、生产启动或实际交易。

### 本轮风险判断及下一件真正有交付价值的工作

原版主体已存在，继续为“是否需要一个完整市场终端”重新做架构研究属低价值重复；已有专业扩展完成离线CI，继续重复写解释也不能替代产品交付。**下一项是基于PR #23的累计差异做原版API/UI与新增调查业务的单Mint真实归档回放及运行安全边界验证**；其中涉及网络/RPC/付费/启动需先满足隔离与授权，不因源代码存在就自动调用。若已知原版功能回归失败，应优先局部修复而非新增同名子系统。知识研究仍独立推进，不充当所有产品功能的前置条件。

## 2026-11-09｜当前状态视图：产品、研发、知识、运行四线独立

> 本节是**当日当前状态**，覆盖下方历史轮次的旧状态描述；不删除旧日志。原Blix主体 `blix@3f8c829c`；专业能力集成候选为 [Draft PR #23](https://github.com/sunshihao001/grok/pull/23) `d53e37f9`，依赖PR #22→#18，未并入`blix`。**产品源码成熟度、代码测试结果、知识研究进度、运行可用性不允许互相替代。**

| 独立状态线 | 现有证据 | 当前结论／边界 |
|---|---|---|
| **A｜Blix原产品** | React/经典页面、Discover/Pulse、Coin、Wallet/Tracker、BubbleMap、Journal、AI Research、Radar/SQLite、MCP及账户产品业务代码 | **产品主体已成型，功能丰富**；仍不等于针对本用户的只读调查系统在目标环境已验收 |
| **B｜新增专业工程** | PR #18钱包RPC存证/失败重试；PR #22签名发现原子水位；PR #23合并去重、修正WTrack、Token-2022、离线Mint报告与跨Mint候选 | **Draft集成候选，CI通过而未合并**。[Node24 CI](https://github.com/sunshihao001/grok/actions/runs/42527921465)：全项目449/449、安全20/20、证据专项42/42；[审计通过](https://github.com/sunshihao001/grok/actions/runs/42527921460) |
| **C｜内部专业知识研究** | Blix `knowledge/MIGRATION.json`有21条已迁入来源；`legacy-knowledge-routing.v1.json`有152个旧研究单元/12领域的**路由映射**；旧Hermes/qb-/meme-/Why-Solana及ai-d有专业研究成果与反例 | **资料积累、分类和跨源研究有实质基础**；并非152项独立确认事实、全部源码已读，也并非AI运行时自动调用成功 |
| **D｜知识实际应用** | 旧Blix已有研究业务，`server/intelligence/mint-facts.mjs`已有本地事实摘要；部分链上知识已转化为新证据模型和反例测试 | **有局部转化**；未证明按用户自然语言自动挑选旧专业知识、完成整条Mint调查，并较无知识基线稳定增益 |
| **E｜目标环境与真实运行** | PR #23有安全受限的**本地离线SQLite报告CLI**，并测试未修改输入文件；原大Server含交易、签名、自动领取和模型费用路径 | **未进行目标Grok云端完整只读隔离、真实主网历史与长期运行验收**；旧服务门禁、GitHub CI通过均不等于已安全运行 |

**按业务场景判断（不是同一个完成百分比）**：

- **市场发现→Coin基础调查**：原产品页面、API、采集和Holder/Dev/BubbleMap等业务逻辑已经存在，接近成品的是此部分；实际覆盖、数据口径与本用户环境仍需实跑。
- **原始经济事件→钱包接收者→卖出/跨Mint**：PR #23对合成数据已通过跨模块与CLI测试；支持“候选/未观察到”而非证明同控或资本循环；真实v0/ALT、多CPI、Token-2022和公共设施反例没有完成主网验收。
- **6/12小时群体监控及经济机制发现**：原产品有Journal、Tracker、AI等零件，旧理论已有独特机制；尚无面向目标的完整、持续、真实数据、可解释和可恢复的业务闭环。
- **“只说一句话，AI自己研究和给出专业结论”**：ai-d方法、知识入口和Blix研究组件存在；其运行时自主正确选知识和使用后的真实价值仍待对照验证。

**当前真正的交付瓶颈**不是Blix原产品缺UI，也不是知识研究资料太少，而是**将PR #23候选与现有主体审慎收束、独立只读运行隔离、真实归档交易验收、最小业务入口对接**。旧PR #19/#21并行探索和旧表“待修复”不可自动诱发重造；PR #20文档台账和本表有重叠，今后宜收束，不以台账数量作为成果。内部经济机制研究可以独立持续，不充当每个产品发布的固定先决条件。

### 对风险锚点的裁决

**方向有效：保留Blix作为成熟主体。方法调整：从继续全面研究文档转到整合与真实业务验收。** 如果PR #23通过合并审查及安全隔离后的真实回放，就优先把它接到已有UI；如果真实归档发现无法正确还原或成本不可接受，再按缺口比较PumpTrace/Million或替代数据源，而不是预设要再造一套底座。

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
| B01 / P0 | 原始交易证据保留与重放 | **当前PR#23集成候选CI已验**：获取的RPC原文和指令位置被保存，签名/Token-2022加固已测试；主网/全历史未验 | 核验真实v0/ALT、Token-2022、新建/关闭账户与多CPI，记录所有不可解码项目 | `server/economic-events.mjs`、`test/economic-events.test.mjs`；Solana官方交易规范 |
| B02 / P0 | 钱包读签名的**处理成功水位** | **已部分修复、离线验收**：`econ_wallet_processing` 将 `CAPTURED/RETRY_REQUIRED/COMPLETE` 分开；`readSigs` 只在钩子与账本处理后写入；失败优先从本地RPC归档重试并有有限次数恢复查询。GitHub CI 对故障注入、缓存、共享签名、限次选择已通过；**未做完整服务重启/持续断流实跑** | 在严格隔离环境验证真正进程重启、定时任务恢复、数据库锁与告警副作用；防止重复报警；确认5次失败后的人工检查路径 | `server/wallets.js`、`server/economic-events.mjs`、`test/wallet-evidence-retry.test.mjs`；不把本次限定验收写成全历史完整 |
| B03 / P0 | **已知缺口≠历史完整**，持续回填/断点 | **PR#22已在候选分支部分修复并通过离线CI**：原子签名发现、持久化任务和覆盖窗口；PR#23继承；未证实全历史、长期429/WS缺口恢复 | 在单个钱包上登记 `[起止slot/签名边界、游标、总数、成功/失败、完整/截断原因]`；断流、429、重启后从同一锚恢复；不能把 `CAP_REACHED` 标 `COMPLETE` | 优先复用 Blix `wallets.pageSignatures`，PumpTrace `BackfillManager` 的可续传任务状态 |
| B04 / P0 | Swap + 转账、一个签名多个事件 | **已验证/限定范围 + 待修复**：新层能存多个原始指令；旧 `wallet_trades/wt_transfers` 仍按签名+钱包+Mint折叠；`wtrack.fromTx` 在命中swap时跳过转账 | 以买入1000转出400、同签名转给B/C、多池CPI作为回归；钱包摘要/监控不再把余额净变化说成实际买单数量 | `solana.parseSwaps`、`wtrack.fromTx`、`journal.tradeKey` |
| B05 / P0 | 接收方是钱包、池还是公共设施 | **待验证**：`recipientCandidates` 返回能够识别Owner的Token指令边；AMM Vault/池参与者也可能匹配；当前不能无条件称“接力钱包” | 加入已知池+普通接收方对照及来源证据。原始边保留，按 `pool/infrastructure/unknown/wallet-candidate` 明确分类；不得由同slot/fee payer推断共同控制 | `bubblemap` 池标签、`coin` 交易对、PumpTrace wallet intelligence |
| B06 / P1 | B卖完后仍可发现、按需跟进 | **待验证**：当前Holder快照不能代表历史接收方；新候选查询可见历史边，但无自动历史扩展 | 合成/真实事件：B当前余额0，仍能从历史找到A→B；对候选启动**显式有预算的只读历史调查**，不得无界递归或擅自监控所有钱包 | Million Wallet→Mint→Wallet 双向扩展，Blix现有Wallet页面 |
| B07 / P1 | 卖M→转SOL→买N 的资本解释 | **已验证/限定范围**：PR #18 合成时序能输出候选，不能证明同批SOL/同一经济控制 | 做时间、数量、手续费、账户前后余额约束，排除公共交易所/路由；用反例证伪“同源资金”；无法排除则标 UNKNOWN | `crossMintCandidates`；Why-Solana 对照/负例、Million 资金边 |
| B08 / P1 | Token Account/Owner/Authority等角色 | **待验证**：新层仅根据RPC pre/post token balance owner映射；本交易中新建/关闭、Owner变化、无法识别的CPI仍可能为 UNKNOWN | 使用RPC真值和合成反例：新建/关闭Token账户、Token-2022、ALT/v0；区分`accountIndex`、地址与Owner；冲突不强行回填 | 官方 Solana JSON-structures、transaction-introspection；已登记的M01适配器 |
| B09 / P1 | 全量RPC归档成本和故障恢复 | **阻断生产**：`econ_transactions.rpc_json` 无保留期/空间预算，表只增不减；没有持久化的批次级覆盖检查点 | 测量100/1000/10000交易空间与写延迟，设置明确上限、归档和恢复策略；断电/数据库锁后验收原始证据与游标一致性 | PumpTrace 原文分仓+持久任务；Blix `journal` 限期与gap/repair |
| B10 / P1 | 错误资金关联：Funder/fee payer | **待修复**：Bubble Map历史过长返回空并长期缓存；在找不到直接转账时退化为fee payer = funder | 3页截断/代付手续费离线反例；显示 `HISTORY_TRUNCATED` 和 `FEE_PAYER_ONLY`，绝不自动生成 `DIRECT_FUNDER` | `server/bubblemap.js:109-151`；既有 `mint-cross-module-evidence-audit-v0.2.md` R1/R2 |
| B11 / P1 | 同一Mint持仓与供应量口径 | **待修复**：`holders.js` 可用动态供应量；`coin.js` 多处1e9；链上快照 `partial:false` 不等于历史完整 | 5亿供应、1亿持仓的20%测试；各数据表都回传 `source/slot/observedAt/denominator/historyCoverage` | 既有V0.2审查R3/R4，不删历史结论 |
| B12 / P1 | 发现与真实市场样本 | **保留/待验收**：Blix已有Mint发现、Pool和发行生命周期；历史真实Mint的3份供应商快照存在，但没有真实交易签名序列 | 对 `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` 取**安全隔离的历史签名**，检验Pool库存变化是Swap还是LP、是否确有A→B | `single-mint-audit.md`、旧PR #16；优先复用现成采集 |
| B13 / P1 | AI/产品报告把事实连起来 | **PR#23已有独立只读SQLite报告CLI并离线测试**：可列接收方、后续卖出候选和UNKNOWN；尚未接到现有UI或研究运行时 | 一个Mint完整报告展示事件路径、签名/位置、已知/未知、覆盖缺口与竞争解释；不将示例假设写成“内幕已确认” | `server/intelligence/mint-facts.mjs`、旧Hermes/qb-/meme- |
| B14 / P0合并门槛 | 原有CI测试不一致 | **PR#23集成候选CI已全部通过**：Node24全项目449/449、安全20/20、证据专项42/42，审计通过；当前真正门槛转为未合并、安全隔离及真实业务验收 | 对比`blix`同基线确认8项归属；将修复放独立且最小化的工作项，避免为清绿灯伪改断言 | [PR #18测试运行](https://github.com/sunshihao001/grok/actions/runs/42419470824)、[Audit通过](https://github.com/sunshihao001/grok/actions/runs/42419470857) |
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


**外部站点 Uptime 另行登记（非 PR 回归）**：最新集成分支的 `tests` 与 `audit` GitHub Actions 为成功，但同一提交还出现名为 `uptime` 的失败任务。已检查 `.github/workflows/uptime.yml`：它通过 `curl` 检查 `https://blixvip.com/` 和 `https://origin.blixvip.com/img/...`，并可能用单独配置的 webhook 提醒，**不是本 PR 的 Node24 代码回归，也不是离线安全验证**。其网站/隧道为何不可达当前仍 `UNKNOWN`；应将其标记 `EXTERNAL_AVAILABILITY_FAIL / NOT_TRIAGED`，不把产品线下线等同于代码新回归，也绝不把 `tests+audit` 通过说成所有 Actions 都绿。不为了绿灯假改健康检查或未经授权启动原服务器。

**代码与真实验收**：集成候选 `3d2ed0e8bf5bfa2e341fc4dab2d1b0bb779909a2`；[Node24 全量、安全、经济证据 CI 全通过](https://github.com/sunshihao001/grok/actions/runs/42527683586)；[独立审计通过](https://github.com/sunshihao001/grok/actions/runs/42527683587)。不虚报实际链上覆盖、正式服务或 Grok Bot 云端已运行。原有 PR #23 仍是 Draft，且直接基于 PR #22 而非 `blix`；本次**没有合并**。

**下一轮只保留真正阻断运行的缺口：** 对一批带来源、slot、签名的真实公开 `getTransaction(jsonParsed)` 归档在隔离环境做同报告回放；检查 Token-2022、同笔 Swap+Transfer、多池、Owner缺失、历史截断及覆盖说明。随后评估独立只读进程和现有 UI 的最小对接，而不是直接把原服务安全门禁打开。若真实 RPC 原文获取受供应商额度/历史可用性限制，记录其为 `UNKNOWN/NOT_AVAILABLE`，不自动拓展付费数据源。

### 2026-11-09｜快速开发方法复盘 + 下一轮证据语义纠偏（R-06）

**当前起点复核（以本轮实时GitHub为准）**：PR #23 已直接以 `blix` 为 base，保持 Draft、mergeable；上一轮登记的 7 项 WTrack 红灯已在集成候选中修复。2026-11-08 23:59 UTC 的 [Node24 tests](https://github.com/sunshihao001/grok/actions/runs/42537815318) 和 [audit](https://github.com/sunshihao001/grok/actions/runs/42537815434) 均成功。**此前 446/439/7 是旧提交的历史事实，不能覆盖当前版本。** 外部 uptime 工作流失败属于另一独立可用性问题，尚未定位原因。此节写入后的新增测试须以新的 CI 重新确认，不能借用上一轮的绿色结论。

**从成熟工程团队的快速开发实践提炼出的适用方法（工程判断，不冒充 Blix 实跑事实）：**
- **以现有成品为底座、缩短反馈回路**：需求 → 一条可复现反例 → 最小代码修改 → 定向测试 → 全量/安全测试 → 评审集成；不是需求 → 全量知识搜索 → 新架构 → 多条平行 Draft。
- **小批量、单一集成真相**：优先复用既有模块、数据库、页面；一个改动只有一个负责的代码入口和唯一的验收来源。PR #18/#21 的重复处理状态是反例，PR #22/#23 的收束是改进。
- **失败优先、分层验收**：测试必须报告真实退出码与 SHA；离线解析、合成跨模块、只读进程、真实 RPC、长期运行各自独立。CI 全绿不能代替用户完成调查任务；历史红灯不能无限被合理化。
- **停止无收益的研究**：若新研究不能改变实现选择、具体失败用例、数据来源或产品判断，就暂停；反之，发现会造成误导性结论的事实语义错误，即使只有一行，也值得先修。

**上一轮遗留错误的更新**：R-01 已由旧7项失败转为「集成候选全量 CI 通过，仍待合并及运行」；R-02 不再以 PR #21 的平行状态机作为当前集成路线；R-03 已有真实 reporter/退出码修复，但后续 CI 仍须禁止掩盖失败；R-04/R-05 仍未因文档或测试完成而关闭。

**R-06 新发现：没有时间戳的 Token 转移被错误地输出为『未观察到卖出』。**
- **根因**：`recipientOutcomes()` 对缺少 `block_time` 的转账返回 `TRANSFER_TIME_OR_MINT_UNKNOWN`，但没有 `sellObservation` 字段；离线报告脚本用 `row.sellObservation || 'NOT_OBSERVED_IN_CAPTURED_WINDOW'` 回填默认值。这会把**无法建立后续观察窗口**误显示为**窗口内未观察到卖出**，即使本地已存在接收钱包卖出摘要。
- **实际修正**：在已有 `server/economic-events.mjs` 的缺失时间分支显式输出 `sellObservation:'TRANSFER_TIME_OR_MINT_UNKNOWN'`；不新增第二个报告器、不触发RPC/付费/交易；在 `test/economic-events.test.mjs` 加入 `blockTime:null` 且接收方有卖出摘要的反例，要求 `observedSells:[]` 和 UNKNOWN；并在 `test/offline-mint-report.test.mjs` 的真实 CLI 子进程验证同一缺失时间反例、执行前后 SQLite 文件 SHA256 不变，不凭空推断先后。
- **验收条件**：该反例与 `npm run test:evidence`、`npm run test:security`、`npm test` 在本次 PR #23 的**最新 SHA** 上全部通过。若 CI 红灯，继续局部修正；未跑完前仅称 `CODE_PROPOSED`。
- **知识/产品增量**：**未观察到行为**需要先有可信的观察窗口；**时间未知**是更上游的事实缺口，不能被下游默认值吞掉。该规则同样适用于 6h/12h 异动监控、历史截断与后续卖出判断。

**下一轮研究决策**：暂不扩大专家/知识架构，也不重扫全部参考项目。先用现有 `inspect-economic-mint.mjs` 和 `economic-events.mjs` 检查**时间未知、窗口截断、池/公共设施节点、交易原文覆盖**四种会直接误导单 Mint 调查的边界。每发现一个能复现的错误就先写回归、最小修复，再看是否值得引入 PumpTrace/Million 的历史补查能力。独立只读进程与真实公开归档回放仍是下一项大门槛；在安全隔离和成本边界确认前，不启动原服务器、不签名、不交易、不付费、不部署。

### 2026-11-09｜R-07／B10：最高严重度跨层误归因，已修正候选代码并做离线回归

**本轮自主排序**：比较了 B04（同签名Swap/Transfer的事件颗粒度）、B10（Bubble Map费用代付误当出资人）、B11（Holder分母）及 R-06（时间窗口）。优先B10，因为它不仅造成数字偏差，还把**交易手续费这一确定性技术事实，错误升级成资本来源，再通过多跳图放大为多个钱包的群体关系**；旧证据缓存甚至使错误随时间持续。B04、B11仍保留且是下一轮候选，不把本轮聚焦误认为已解决。

**错误传播路径及正确颗粒度对齐：**

| 层级 | 原始输入 / 已有问题 | 当前修正后的证据契约 |
|---|---|---|
| 交易元数据 | `accountKeys[0]`为Fee Payer；旧代码没有System转账就回退为funding钱包 | `feePayer`仅作为**费用支付者**元数据，`FEE_PAYER_ONLY`不能形成funded边 |
| 指令级经济动作 | 旧代码只取最早交易内一个表面接收记录，未校验类型/金额/失败/多出资者 | 成功交易的明确System `transfer` 或 `createAccount` 且收款人为目标、lamports>0，才有 `DIRECT_SOL_OBSERVED` 候选；同笔多个不同来源为 `MULTIPLE_DIRECT_SOL_SENDERS`，不任选一个 |
| 钱包历史覆盖 | 三页1000笔以上被旧代码记为 `""`，持久缓存后再也不查 | `HISTORY_TRUNCATED` + `cursor` + 最近已见签名；有界一小时后可继续补查，不能宣称完整历史或无资金来源 |
| 本地缓存 | 旧 `bubble_funders` 表无来源字段，曾混放历史截断、fee payer、直接转入 | **原表原位新增**status/signature/payer/cursor；旧记录自动为 `UNVERIFIED_LEGACY`，不加入图，复核后更新单一缓存记录；不删除原数据 |
| 网络结构/经济主体 | 同一个疑似payer可把多个wallet错误连成funded群体 | 仅 `DIRECT_SOL_OBSERVED` 可生成 `funded` 边；节点返回证据status、原签名、payer与截断水位；图返回 `WALLET_GRAPH_CONNECTIVITY_CANDIDATES_NOT_COMMON_CONTROL`。真实资金转入**仍不证明同控或内幕** |

**本轮实际改动**：`server/bubblemap.js`（复用原Coin/BubbleMap UI/API和单表缓存）、新增纯离线验证助手 `server/bubble-funding-evidence.mjs` 与 `test/bubble-funding-evidence.test.mjs`；注册到 `npm test` 和 `npm run test:evidence`。测试覆盖代付误归因、成功的SOL指令及CPI、失败交易、多个出资者、多页截断及续页、遗留缓存复核、无历史/原文缺失。**没有独立重造图谱服务或新钱包采集进程。**

**原版保护的有意变更**：原版 `server/bubblemap.js` 不再字节不变，这是经本轮错误反例审查的专业二次修复；`test/fixtures/blix-import-baseline.json` 已从28个不可改动指纹中将其转入 `reviewed_modified_original_modules`，改用原版且本轮未变动的 `server/solana.js` 保持28项保护；767项原版路径必须完整保留。**保护清单的变更不是略过回归，而是显式承认改动、用测试约束新契约。**

**执行反馈**：最初 [Node24失败](https://github.com/sunshihao001/grok/actions/runs/42564594476) 的唯一失败是原版字节指纹保护发现 `bubblemap.js` 改动，此项是真实保护门禁，不是代码解析器错误，也不能隐藏。完成意图审查和新反例后修订保护基线。之后 [e907cf7f的全量+安全+证据CI](https://github.com/sunshihao001/grok/actions/runs/42564963740) 各步骤真实成功、[Audit](https://github.com/sunshihao001/grok/actions/runs/42564963769) 成功。后续若有新提交仍须重新检查相应SHA，不把旧绿灯移植为最新验收。

**未完成和可推翻条件**：这是 `INTEGRATED_OFFLINE_TESTED` 的 **Draft PR #23**，不是主网真实资金来源的验证；没有运行含签名/交易/付费路径的主服务，也没有向用户展示真实UI。最早可读交易不是钱包经济生命史的全证明，RPC缺页/公共资助服务、跨交易资本混用和多来源融资仍只能标为候选/UNKNOWN。风险锚点判断：此项修复能消除假阳性群体连线，**比继续堆机制文档有更高的即时价值**；下一轮若 R3供给分母与B04混合交易的真实失败影响更大，应按最短反例测试重排，不再重复资金来源定义研究。

### 2026-11-10｜最高优先级的目标—入口冲突：Mint-first vs wallet-first（R-07）

**问题颗粒度对齐：** 已确认的产品验收是「在 Blix 选择一个 Mint → 自动展开已知钱包、转账、接收者后续行为及跨Mint候选 → 给出证据覆盖与未知」，而不是「用户先知道一个发送方钱包 → 输入 wallet+mint → 查看这个钱包的转账」。后者是有用的**局部钻取**，却不应成为单 Mint 调查的唯一入口。此前的 `inspect-economic-mint.mjs` 强制 `--wallet`，是产品目标与实现契约的高优先级偏离。

| 层级 | 产品契约 | 当前最小修正 | 尚未完成 |
| --- | --- | --- | --- |
| 用户入口 | 选择 Mint 即能开始调查 | CLI `--db EXISTING.sqlite --mint MINT` 可选 `--wallet`；旧 wallet+mint 精确钻取不破坏 | Blix Coin 页面按钮/API |
| 事实发现 | 自动识别**本地归档可观察**的发送方 | 只查询已归档成功交易、已解析且Owner无冲突的Token转移，按签名数排序，最多10个sender；每人最多20条边 | 全链签名发现、跨钱包历史自动回填 |
| 关系语义 | 池/服务/普通钱包不可混称同控 | 输出 `UNCLASSIFIED_OWNER_CANDIDATES_INCLUDING_POSSIBLE_POOLS_OR_SERVICES`，明确不证明交易者或共同控制 | Pool/Router/共享服务分类证据 |
| 观察覆盖 | 未发现 ≠ 不存在 | 输出选取数量、`truncated`、`lifetimeHistoryComplete:false`，保留转账时间未知状态 | 完整索引覆盖、长周期恢复 |
| 安全 | 不启动交易或费用路径 | 沿用只读SQLite CLI、只读模式、无RPC/签名/交易/付费；复用现有 `recipientOutcomes` | 真实主网与独立安全服务验收 |

**为什么本轮选择它而不是继续修单个解析细节：** 它直接决定普通用户能否从一个 Mint 开始完成 V0.1 的核心调查；不解决入口错位，即使单钱包算法完全正确，也不能形成目标产品。相反，贸然增加“庄家钱包”标签会把尚未分类的Pool/服务误当操盘实体，故本轮仅实现受限的证据发现，不作身份断言。

**代码改动**：复用 `scripts/inspect-economic-mint.mjs` 与 `server/economic-events.mjs`；新增 Mint-only 查询，保留 wallet-only 限定钻取，沿用旧只读输出与错误退出码。新增 `test/offline-mint-report.test.mjs` 的 Mint-only、时间未知和空库验收，验证输入 SQLite SHA256 不变。**本次改动仍只代表离线归档内的已知关系，不是完整市场发现、持仓分析或Blix UI功能。**

**验收与停止条件**：本次最新SHA的全量测试、安全测试、经济专项、独立审计全部真实成功后，R-07 仅可标记为 `MINT_FIRST_OFFLINE_TESTED`；UI集成、真实历史覆盖、池分类仍独立登记。若归档中没有已解析的Owner边，必须输出空候选及覆盖限制，而不是凭空生成钱包。下一步优先评估复用现有 Coin 页面已有 Mint 上下文，以最小API/只读隔离接入该报告；禁止为了接UI直接启动旧交易服务。


### 2026-11-12｜R-08：Mint-first 发送地址竞争与本地交易证据优先

**恢复基线**：在现有 [Draft PR #23](https://github.com/sunshihao001/grok/pull/23) 的原分支修改；PR #24 是独立未合并的 AI 候选。完整原版 Blix、交易和账户模块不动；没有启动主服务器、RPC、AI、签名或部署。

**可复现问题**：原 Mint-only 调查按已归档的 COUNT(DISTINCT sig) 排序，最多10个发送方。AMM池、公共服务或其他高频地址可能挤掉已有本地交易记录的钱包，令后续 AI 调查入口漏掉潜在线索。高频不等于池，有本地交易记录也不等于单人控制。

**实际代码及验收**
- [8ee364e](https://github.com/sunshihao001/grok/commit/8ee364e40644dbb0d280c11a572c0d6437ef8151)：在已有 SQLite 归档上优先选择存在 wallet_trades 记录的发送地址，之后按已归档签名数量排序；最多10个地址。新增局部互证计数与排序说明，保留 truncated、pool/service 未分类和 UNKNOWN。
- [4352b33](https://github.com/sunshihao001/grok/commit/4352b337b1e2b9a4ca7fa13fc0c45436e0c31228)：11个未分类竞争地址 + 1个本地已记录钱包的离线夹具，检验钱包不被前10挤掉、SQLite文件SHA256前后不变、没有升格任何地址身份归因。
- 最新 SHA 4352b337： [Node tests/security/evidence](https://github.com/sunshihao001/grok/actions/runs/43221579187) 通过；[audit](https://github.com/sunshihao001/grok/actions/runs/43221579209) 通过。仅证明离线CI，不代表主网运行。

**从外部项目吸收的具体知识与限制**
- [Token Finder](https://github.com/Danialsafarli/token-finder/blob/master/src/intel/graph.ts)：共资、同步买入、重复下单、跨Mint参与必须保留关系类型和独立事件依据；热门发行需排除普通拥挤行为，原固定阈值/置信度不应直接照搬。
- [Solana Holder Analyzer](https://github.com/non-contextual/solana-holder-analyzer/blob/main/src/transfer-scan.ts)：多跳BFS、高连接地址停止扩展、逐层预算值得复用；净额边不能替代逐笔交易与总流入/总流出。
- [Trading Portfolio](https://github.com/solana-foundation/trading-portfolio/blob/main/src/lib/portfolio/pnl.ts)：历史价格/成本覆盖不足时不应由语言模型补造钱包PnL。
- [FlowLens](https://github.com/tobenwarrior/FlowLens/blob/main/src/domain/graph-projection.ts)：有界展示图与完整证据保留分开；EVM代码与AGPL许可需独立审查。
- [Google Skill Reach](https://github.com/google/skill-reach)、[Vercel AI SDK](https://github.com/vercel/ai)：进一步评估AI是否正确选择专业知识、工具及调查停止条件，不以文本丰富作为能力进步。

**未完成与下一项最有价值工作**
1. 在相同真实Mint已归档数据上对照新旧排序，比较漏钱包、池/公共服务干扰、时间、覆盖及费用；当前仅离线对抗夹具。
2. 本地交易记录不证明真实交易者身份或共同控制；需要公共基础设施分类、多池/Token-2022和不同历史窗口的实证验证。
3. PR #24的AI助手仍为预览/离线适配，只有 mint-facts；未来应经受限只读数据通道复用 PR #23 的 Mint→Sender→Recipient→Sell/CrossMint 证据，不新建第二套交易捕获、重试和SQLite状态。
4. 不在没有权限隔离及实际费用核查前启动原版Blix服务器或模型供应商服务。


### 2026-11-12｜R-09：PR #24 AI工作流与 PR #23 经济证据离线贯通

**事实状态**：在现有 PR #23 集成分支中，复用 PR #24 的 model({stage}) 外部注入式 AI 编排，不合并或关闭独立 PR #24，也不启动原版 Blix 服务、真实模型、RPC、签名、交易、付费和部署。

**实际代码路径**：
- server/intelligence/index.mjs 在原 mint-facts 之外允许第二个只读能力 mint-economic-evidence，按需加载；两个能力共享现有允许列表，模型不能扩展工具权限。
- server/intelligence/mint-economic-evidence.mjs 将 PR #23 原 inspect-economic-mint.mjs 的本地证据报告转成保留签名、时间、钱包关系、卖出摘要、跨 Mint 候选、来源与 UNKNOWN 的工具输出；不声称控制权、接收Token库存卖出因果或完整历史。
- server/intelligence/offline-economic-reader.mjs 由受信调用方指定已有 SQLite 文件；固定子进程参数和 Mint-only 窗口调用既有 CLI，非模型输入的路径不可越权、没有 Shell、DB readOnly/query_only；原采集与重试数据库没有被复制。
- server/intelligence/ai-workflow.mjs 可在第一次读证据后，按模型明确 followup:true 请求第二次规划；后续计划重验授权、Mint、重复调用和总预算最多两次。非法后续规划保留首轮事实，不能执行不允许的命令；解释仍标为 UNVERIFIED_MODEL_INTERPRETATION。
- 移入 test/ai-workflow.test.mjs（原 PR #24），新增 test/ai-economic-workflow.test.mjs 的 Mint→A→B→B本地卖出摘要→AI推论离线 SQLite 路径、执行前后文件 SHA256、缺数据与非法后续规划反例；同步现有 Node24 完整测试和经济专项。

**已解决的内容**：AI 可通过授权接口使用既有 Mint/Holder 与归档转账关系，再根据第一轮证据请求另一项允许工具。现阶段只是被注入的模拟模型和合成归档；没有声称连接真实模型或动态请求链上数据。

**验收状态**：本节提交后的 GitHub CI（完整 npm test、security、evidence、audit）必须按新 SHA 核查。完成前为 CODE_SUBMITTED_NOT_VERIFIED，不能沿用此前 SHA 的绿色测试。

**未完成的真实阻断**：受控真实模型适配、Coin 页原有 AiCopilot 预览变成受授权执行入口、独立只读服务与真实主网 RPC 归档、Pool/Router 归因过滤、跨 Mint 长历史、任务恢复与预算。优先验证端到端的一次真实 Mint 调查质量，不再为已有程序另建状态机。


### 2026-11-12｜R-10：PR #23 / #24 实际接口磨合审计与缺口重排

**本轮结论（纠正 R-09 的“待 CI”状态）**：在已有 PR #23 的同一 Draft 分支中纳入 PR #24 的 `web/src/pages/coin/AiCopilot.tsx`、原 `Tabs.tsx` 的 AI assistant 入口和独立 Web 构建 workflow。界面使用原 Coin Mint 上下文、原有 AiGate、按需加载、切 Mint 重置，明确仅为 **Preview · agent not connected**；原版 AI read / Safety / 交易界面不被替换。AI 执行后台使用前轮已完成的只读双工具适配和两阶段有条件补查，但仍然没有实际 HTTP Agent API、真实模型或浏览器到后台的执行链。后端能力与前端展示代码处于**同一集成候选**，并不代表它们已经在运行时贯通。

**本轮明确修复的两个证据语义缺口**：
1. `mint-economic-evidence.mjs` 在原 SQLite 缺少经济证据表时从容易被误读的 `LOCAL_EVIDENCE_PARTIAL` 改为 `UNAVAILABLE`，显式指出“零接收钱包不证明没有转账”；有表但空的已捕获窗口仍是 `LOCAL_EVIDENCE_PARTIAL`，必须展示历史不完整和未知。
2. `ai-workflow.mjs` 当允许的工具执行失败时，把失败写进 `unknowns`，不只藏在 `evidence[].error`。离线单元测试覆盖缺失数据库、错误 Mint、空索引、截断、追加计划越权拒绝；AI 自己的自然语言结论仍是 `UNVERIFIED_MODEL_INTERPRETATION`。

**原版保护与测试真实性**：
- 将原版 `web/src/pages/coin/Tabs.tsx` 的有意修改登记到 `test/fixtures/blix-import-baseline.json` 的 reviewed_modified_original_modules；新增源保护回归确保老 `AI read`、`Safety`、`onRead={onPaper}` 和新 `AI assistant` 共存，保持 767 原始路径与 28 个受保护模块的原约束。前端独立 TypeScript/Vite 构建成功。
- 新保护测试初稿曾错误检查 `onPaper={onPaper}` 而触发 [Node CI 红灯 #43226874895](https://github.com/sunshihao001/grok/actions/runs/43226874895)；没有掩盖，改为实际源代码中的 `onRead={onPaper}` 后复核。最新**代码 SHA [d3c2de5](https://github.com/sunshihao001/grok/commit/d3c2de56f1a124b6ebd2fbd278f77ac8d1d91b36)** 的 [完整测试、安全与证据 CI #43226967098](https://github.com/sunshihao001/grok/actions/runs/43226967098)、[Web CI #43226966757](https://github.com/sunshihao001/grok/actions/runs/43226966757)、[Audit #43226966778](https://github.com/sunshihao001/grok/actions/runs/43226966778) **各自通过**。
- [外部 Uptime #43226954252](https://github.com/sunshihao001/grok/actions/runs/43226954252) 仍失败，属于原 Blix 网站可用性信号，尚未定位；不可称所有 Actions 全绿，也不可为通过而私自部署/改健康检查。

**剩余问题严重度与下一步（不视为已运行）**：

| 严重度 | 缺口 | 需交付的具体验收 |
|---|---|---|
| P0 | **Coin UI → 安全 AI 服务 → 模型执行** 未接通。当前按钮只能复制任务。 | 单独受控、鉴权的研究执行入口；页面真实调用一次、展示过程和结果；取消与重放；不借原交易/签名启动路径。 |
| P0 | **真实原始 Solana 数据完整覆盖** 未验证。SQLite 离线归档合成测试不代表历史真实。 | 对至少一个真实 Mint 的RPC原文归档进行复查；查 Token-2022/CPI/Owner/fee payer/SOL-WSOL/交易签名/时间窗口/多池与历史缺页。 |
| P0 | **供应商授权与费用/模型隔离** 未完成。 | 明确获授权的模型账号和数据来源，预算与并发/时限、权限边界、故障行为；模型无法借模型文本提升调用权限。 |
| P1 | **池、路由器、交易所等共享设施过滤** 不完整。 | 同一真实 Mint 上区分有本地交易记录的地址和公共服务；比较漏关键钱包与误关联，不以启发式排序宣称同控。 |
| P1 | **长期历史/跨 Mint 资金关系与库存/PnL** 仍局部候选。 | 同笔Swap/Transfer去重、流入流出、接收者转仓、历史价格/成本覆盖、跨Mint身份与资金路径，保留未能归因部分。 |
| P1 | **运行中断/任务记录与可视化** 不完整。 | 任务进度、取消恢复、证据签名点击、图谱节点选择、报告持久化、时间覆盖和供应商故障显示。 |
| P2 | **模型/知识调用效果评测与持续监控** 尚未形成真实质量基线。 | 同 Mint 固定模型与动态调用A/B、专业知识使用命中/误用、API预算、误报/漏报、真实持续运行。 |

**决策**：当前代码层面冲突已收束，不再平行开发复制一份 AI / 经济证据平台；实际价值门槛转移到 P0 的受限运行通路和真实交易证据覆盖。用户原版完整产品必须保留；无法安全启动旧服务器并不意味着删除交易代码。PR #23 与 #24 保持 Draft、未合并，已经将 #24 的特定 AI/UI 代码复用于 #23 候选，不等于 GitHub PR merge。下一轮先评估已有安全只读网关/服务可否复用，避免误启付费及签名路径，然后开展隔离真实 Mint 的完整调查验收。


### 2026-11-12｜R-11：Coin 自然语言 Mint 范围与任务长度磨合；Uptime 失败语义纠偏

**先于新增文件的差距审查**：PR #24 的 Coin AI assistant 页面已有确定的当前 Mint，并允许用户补充文字、钱包地址；但原 AI 编排仅通过目标文字匹配所有 Base58 地址，含“一个 Mint + 一个钱包”的正常任务会误判为多个 Mint 并拒绝。编辑器允许用户输入1600字及页面数据，原后台2000字符限制造成第二个真实接口错位。

**代码与反例（原 PR #23 分支原位修正）**：
- `server/intelligence/ai-workflow.mjs` 新增可信调用方提供的 `mint` 范围参数，模型收到的 `mints` 和任何实际可执行 `mint-facts` / `mint-economic-evidence` 调用严格受此单一地址限制。问题中另外提到钱包或跨Mint地址属于研究上下文，不得作为新的工具目标。老的无明确Mint参数调用仍按文字只识别一个地址，避免猜测。调用方范围是授权前提，不能由模型自己填任意 Mint。
- `test/ai-workflow.test.mjs` 新增双地址输入的正确选择和企图将已提及钱包“提升为允许调用的 Mint”零执行反例。
- 为同 PR #24 的 1600字符文本问题 + 既有页面来源快照，AI 输入限制从2000统一到4096；新增较长完整页面任务被接受、超长仍拒绝的边界测试。不放开模型/工具权限，不启用服务。
- 最新代码 SHA `f56c7859c850ee5fbb0b376cad0782640a39d5b9` 的 [完整Node/security/evidence测试](https://github.com/sunshihao001/grok/actions/runs/43228386019)、[Web TypeScript+Vite](https://github.com/sunshihao001/grok/actions/runs/43228386152)、[独立audit](https://github.com/sunshihao001/grok/actions/runs/43228386146) 逐项成功。仍只代表离线可复现契约测试，未作浏览器到实际模型执行演示。

**Uptime 误分类纠正**：历史台账曾把该工作流红灯理解为“外部Blix站点可用性失败”。本轮实际读取 [run #43227366764](https://github.com/sunshihao001/grok/actions/runs/43227366764) 的 GitHub 元数据为 `event=push`、`conclusion=failure`、`jobs.total_count=0`，没有执行 `curl` 检查。仓库原始 `.github/workflows/uptime.yml` 在 `blix` 与集成分支 blob SHA 相同，源文件只有定时或手动触发。**这个具体红灯不能证明站点离线或终端服务故障**；当前正确分类是 `WORKFLOW_NOT_STARTED_OR_INVALID / CAUSE_UNKNOWN`，后续需检查 GitHub Actions 工作流校验/触发与真正的 schedule/manual 日志，不为“绿灯”自行改站点健康探测或部署。

**仍未做好且不得宣称完成**：
1. Coin 页现在只是将 Mint 与上下文组成待复制文本；虽然后台现在支持可信选中 Mint 入参，尚无经过认证/权限隔离的 Coin→后端实际调用、执行进度、取消和结果回写。
2. 真实获授权的 GPT/Claude 模型适配、密钥保管、供应商预算与故障恢复尚未集成；当前只有模拟注入。
3. 离线经测试的经济证据链只覆盖已有 SQLite RPC 归档，未验证真实 Mint 交易与所有钱包历史；公共设施、Token-2022、CPI去重、SOL/WSOL、历史断流、跨Mint库存归因仍在P0/P1。
4. PR #23 整合了选定 PR #24 代码但两个GitHub Draft仍未合并；PR #24 的旧独立红灯不代表已整合的 PR #23 测试失败；反之通过的离线CI也不意味着生产运行。
5. Uptime工作流需要独立调查真实调度结果；目前不得根据当前无 Job 的 push 失败断言站点不可达。

**下一轮首选**：审查原有 Blix 可复用的鉴权/只读隔离服务，设计并验证 Coin→授权研究端点→经济证据/模型→前端报告的真实可执行链，同时严格隔离交易签名与自动付费。不要再建一套平行抓取/状态机。


### 2026-11-13｜R-12：P1–P2 专业网络、群体演化、知识使用、跟单研究实装与验收

**建设范围和理由**：原版 Blix Bubble Map/钱包、paper与本地SQLite数据和历史专业知识已经存在；本轮不再建第二套钱包采集器、交易执行器或专家目录。聚焦将 PR #23 已捕获的成功交易指令转成**可复查的资金关系与历史比较**，将旧知识转换为**按问题调用的参考**，再以**时间可见性/实际执行证据**约束跟单历史研究。未启动主Blix服务器、RPC、真实模型、签名、交易或付费接口。

**P1 实际代码与契约**
- `scripts/inspect-economic-mint.mjs` 原有单Mint报告新增 `outerI/innerI/mint`，保留精确签名+外层/内层CPI指令位置；不是仅按相同钱包对/net金额合并，避免重复、漏项和无法区别同笔多次指令。
- `server/intelligence/economic-network.mjs` 从**同一原始经济证据报告**投影有类型的 Token Transfer 事件/边、钱包可观察流入/流出/净转移、方向、时间、签名、多接收方分发候选；以 BigInt 原始量字符串计算防浮点误差，按同一指令位置去重，保留未知时间/数量、样本截断、冲突。资金图不是控制权图；原版 BubbleMap 不动。
- `server/intelligence/mint-economic-evidence.mjs` 将 graph 附加到现有 `facts.network`，进入此前已通过CI的两阶段AI只读工作流。卖出摘要按接收者的**不同签名**去重，同一跨币候选按原始 funding+buy+mint 组合去重；多跳的总转移量**不能**被解释为独立净流入、当前可卖库存、Swap卖出或获利。
- `server/intelligence/economic-snapshot-review.mjs` 比较两份本地归档的相同Mint事件：新增可见、未再被当前有限样本展示、同事件元数据更正三类分别输出；不把历史RPC补查当实时转账，不把样本遗漏当真实卖出。两个不同 Mint 之间只输出**地址重合候选**，不认定相同经济主体或资金出处。
- `scripts/inspect-economic-network.mjs` 与 `npm run inspect:network-offline -- --db EXISTING.sqlite --mint MINT [--previous-db ...] [--other-mint ...] [--goal ...]` 为已有离线证据的实际可运行调查入口，不接付费供应商，不写输入库。

**P2 实际代码与契约**
- `server/intelligence/local-knowledge-loader.mjs` 使用现存 `knowledge/mechanisms`、`knowledge/methods`、`knowledge/foundations` 与 `knowledge/cases` 文件，不重新复制专业知识；按用户自然语言问题、实际工具证据缺口选1–3个有来源、SHA256版本指纹、长度上限的片段；明确 `RESEARCH_NOT_RUNTIME_VALIDATED` 和 `trustedAsInstruction:false`，不让知识文本赋予交易权限。旧 RED-COHORT 文中**撤回定量结果**有显式模型上下文警示，禁止旧百分比被当作新实证。
- `server/intelligence/followability-replay.mjs` 和 `scripts/audit-followability-offline.mjs`：用显式提供的纸面成交收据做**跟单可评估性筛查**；区分原钱包链上事件时间与跟随者首次可见时间，拒绝事后提前进场、无退出/不完整库存、无费用和滑点、报价过期/未声明有效期的样本。仅在收据完备时计算模拟SOL净额与收益基点，并永久标为 `PAPER_SCENARIO_CALCULATED_NOT_LIVE`；即使所有模拟样本正收益也**不宣称样本外盈利/Alpha**。不触发原版交易程序。
- `test/economic-network.test.mjs`、`test/economic-snapshot-review.test.mjs`、`test/local-knowledge-loader.test.mjs`、`test/offline-economic-network-cli.test.mjs`、`test/followability-replay.test.mjs`、`test/offline-followability-cli.test.mjs` 新增合成离线反例：签名+多CPI、巨量raw、重放去重、流入卖出重复计数、图谱分发、回补/更正、跨币地址重合、知识来源与撤回、前瞻偏差、过期报价、缺执行、缺库不建文件、输入SQLite与研究JSON SHA256不变。均进入既有完整/专项Node24 CI。

**本轮验收边界**：上述是 GitHub可执行的离线源代码和fixture；该SHA成功与否以最新 GitHub Actions tests/audit/web 三项为准，不能提前视为生产功能。尚未对真实主网完整历史、具体Pool/Router类别、CPI/Swap真实Pnl、原Coin页图谱联动、模型知识选择质量、全天候监控和样本外收益提供独立证据。

**明确未完成的关键阻断（继续从这里，而不重复新建方法制度）**
1. P1：真实Mint全历史、多池/Token-2022/CPI事件与Swap/Transfer去重，公共基础设施分类，准确的归属可卖库存/PnL；部分功能源代码已有，依赖授权RPC/真实样本复查，不得用标签替代。
2. P1：将现有 `web/src/pages/coin/BubbleMap.tsx` 的原图形交互与 `facts.network` 的签名/时序/证据关联展示打通，需要通过只读独立服务/安全鉴权（P0）而不是从原交易主服务借未审权限。
3. P2：任务轮询/历史监控实际运行、费用与故障恢复、知识模型多轮选择的真实A/B评测、市场影响/策略样本外回测仍待真实输入与授权。当前快照比较是本地离线功能，不是已部署监控。
4. 原版市场/交易页面及服务保留；GitHub PR #23/#24均为Draft未合并。不要用离线CI绿灯宣传真实主网或Model/交易服务已经上线。


### 2026-11-13｜R-13：P1–P2所有高相关知识按原体系归位与来源反证（不宣称全65/152已审）

**用户目标**：将上轮已实现的 P1–P2（钱包网络/资金/库存/跨Mint/时序/监控/策略/知识选择）相关专业知识重新检索、对照、修正并放回Blix原有体系。**不再造第二套专家制度、补齐标签架构或重写交易程序**。

**实际检索来源及边界**：
- 本仓旧D01–D12资料、已有六类专业知识目录、`knowledge/README.md`、旧 `legacy-knowledge-routing.v1.json` 与 PR #23 当前源代码/测试；不改152单元原始映射历史。
- [Hermes role/structure/evidence/Skill4](https://github.com/sunshihao001/-)、[qb-原生95钱包留存](https://github.com/sunshihao001/qb-)、[meme-原真源与结构观察者门槛](https://github.com/sunshihao001/meme-)、[ai-d两领域源级结果](https://github.com/sunshihao001/ai-d)、[Why-Solana Dust/多跳](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over)；静态读取与旧源上下文一致性复核，不表示整个仓库逐行审查。
- GitHub外部源：Token Finder `graph.ts/test/intel-graph.test.ts/calibration/replay.ts`、Solana Holder Analyzer `transfer-scan.ts`、Solana Foundation Trading Portfolio `pnl.ts`和成本测试、Google Skill Reach 路由研究；Solana官方RPC JSON、Transaction Introspection、Token-2022 TransferFee/Hook及getSignaturesForAddress。每项具体可吸收与反例写于 [统一源账](../../knowledge/references/p1-p2-knowledge-reconciliation-20261113.md)。

**本次已写入而不止是对话输出**：
1. 新增一份集中的[来源—事实—旧错误—D01–D12—代码边界—下轮验收账](../../knowledge/references/p1-p2-knowledge-reconciliation-20261113.md)。该文件是现有 `knowledge/references/` 中的审查记录，不替代原领域正文。
2. 直接修订现有8份D01–D12专业正文：`foundations/solana-chain-and-market`、钱包/库存、资本组织、价格机制、异常群体、跟单执行、反证案例、AI知识与意图。对旧Hermes固定阈值、qb质量分/全退/Top10分母、meme结构策略成熟度、Dust/公共设施、Token-2022/交易v1、Token多跳gross、同地址跨Mint、历史回填及纸面收益作明确纠正，原文保留。
3. 更新 `knowledge/README.md`、`knowledge/references/README.md`、`knowledge/INTEGRATION-CROSSWALK.md`、`docs/project/README.md`、`docs/project/knowledge-use.md`、`docs/project/knowledge-to-capability-integration-v0.1.md`；旧“未改业务源码”的说明限定为当时历史状态，不再混淆当前离线交付。
4. `server/intelligence/local-knowledge-loader.mjs` 在原6项上增加多跳、关键钱包、市场价格机制、AI认知方法和本轮综合纠偏5项为**11个本地白名单候选**，仍最多按问题读取3份为默认；从文档带SHA与来源/撤回警示，不能让原文获得模型交易权限。检索旧章节时附带最新2026-11-13适用限制，避免“文档更新了但模型只读旧结论”。
5. 增加 `test/p1-p2-knowledge-integrity.test.mjs`、`test/local-knowledge-loader.test.mjs` 的源路径、12域覆盖、11本地白名单、同义/专业词路由、现行修正保留测试，加入完整 `npm test` 与 `test:intelligence`。

**已核验**：GitHub读取已确认所有源文件/更新目标存在、PR #23为 Draft 且head前进，未合并/部署/调用模型。**本轮最新提交未获得新的 Node test CI运行记录**；GitHub Actions 的test.yml只在PR事件/主分支push触发，且本轮连接器提交后只出现了Uptime push失败记录。现阶段严格记为 `CODE_AND_KNOWLEDGE_SUBMITTED / TEST_EXECUTION_NOT_CONFIRMED`，不借用旧 SHA `520b5a3` 的绿色结论。外部主网实跑/模型A/B也未完成。

**未完成、不是知识整合可凭文字填满的部分**：
- 所有参考资产与152旧单元的逐项源级覆盖，特别是未审商业内部算法与真实样本；来源清单不等于知识全核验。
- 真实链上Token-2022费与复杂CPI的正确经济核算、公共基础设施/资金类型判定、钱包真正库存与成本。
- Coin UI/只读研究服务真实连线、长历史监控/恢复、专业知识动态模型A/B、跨Mint群体样本外验证及跟单实际执行成本。
- 需要在有运行权限的环境执行 **npm run test:intelligence、npm test、npm run test:evidence、npm run test:security、Web build**；如新路由出现误选和旧知识片段覆盖不足，先修检索/对照，不扩张统一prompt。

**下一项优先**：先拿到本SHA的离线测试运行验收；再做同数据的“无知识→6源→11源”任务A/B与误归因分析，在此基础上再确定是否需要更多源码引用或知识路线。长期研究任务以后应按本R-13恢复，不重复做新的资料目录。


#### R-13 后验复核：来源与链接通过静态校验；最新CI缺席，PR合并存在冲突

- **本轮独立GitHub读回**：8/8现行D01–D12原始知识领域文件均包含2026-11-13适用修正与来源账；6/6知识/项目入口链接该来源账；D01–D12全部在对照账；11个本地白名单专业源路径在当前树可见；15份本轮新增/改动的知识/导航文档中未发现新的相对链接断链。词面路由样例按工具源码模拟，覆盖钱包资金/多跳/关键钱包/价格机制/AI认知/跨项目来源/群体与无关输入，**非Node实际执行结果**。新增Node测试本身已写入并且在package脚本注册，但不能据此标为“测试通过”。
- **范围未夸大**：\`knowledge/references/source-coverage-v0.1.json\` 记录本轮SOURCE_READ候选，保留原Hermes/qb-/meme-\`TREE_INVENTORIED_PARTIAL_DEEP_READING\`和\`exhaustive_content_review_completed=false\`；历史源目录并未整体完成逐项深审。
- **CI实况**：最新知识变更commit的GitHub check-runs为0、combined status pending，GitHub Actions只有\`uptime.yml\`的push失败记录（no web/Node/evidence/audit job）；本轮最新知识调用与整合测试 **TEST_EXECUTION_NOT_CONFIRMED**。不能沿用此前\`520b5a3\`的全绿CI为新SHA验收，也不能把无job的Uptime失败当网站一定离线。
- **新发现的实际合并阻断**：GitHub [Draft PR #23](https://github.com/sunshihao001/grok/pull/23) 当前 \`mergeable=false, mergeable_state=dirty\`，与最新 \`blix\` 不可直接合并。Blix基线在此PR原base commit之后有更改，至少触及\`knowledge/README.md\`、\`knowledge/cases/independent-validation-and-failure-cases.md\`、\`knowledge/mechanisms/market-price-mechanism-research.md\`、\`knowledge/references/source-coverage-v0.1.json\` 等共享路径。**本轮未尝试强制更新基线、覆盖原版变化或合并PR**；具体冲突块仍需在三方对照中逐项消解，之后再执行CI。
- **下一项优先**：在PR #23的旧分支成果与当下blix共享知识原文间做三方冲突裁决，保留两侧的新旧知识与来源；随后用Node24验证\`test:intelligence\`、全套Node/security/evidence和Web；待通过再做真实模型知识选择A/B及实际Mint/RPC专业调查。


### 2026-11-13｜R-14：P1/P2全知识整合后的路由反例与协议修正

**恢复状态/没有重复造档案**：R-13已完成 Hermes、qb-、meme-、ai-d、Why-Solana、Solana官方和代表性Github源码的本地知识核查及8份D01–D12原领域正文的原位纠正；入口为 `knowledge/references/p1-p2-knowledge-reconciliation-20261113.md`。本轮检查最新PR状态后不再创造第二套知识系统或重新复制152研究单元。旧来源和未审边界原样保留。

**知识调用可观察缺口**：对当前11本地白名单研究专题，以预先设定应命中领域的16个用户口语/专业问题测试静态词面路由。旧配置9/16有至少一项预期领域漏选（Token2022/Hook、Pool/Vault、CEX出金同控、历史回补、资料误选等）；新配置静态复算16/16命中预期领域。新增 `test/local-knowledge-loader.test.mjs` 的16正例、3无关词误触发负例。按需选源及SHA来源标记保持，不常驻加载全部正文，不把未经主网验证的旧知识当真值。**16个小样本是规则/路由静态测试，不是模型A/B、真实误召回率或NodeCI通过**。

**官方协议与可执行修正**：
- Solana官方 https://solana.com/docs/core/transactions/versioned-transactions 与 https://solana.com/docs/rpc/json-structures 确认主网已启用v1；`getTransaction`必须选择maxSupportedTransactionVersion=1，v1使用transactionConfig不支持ALT。本分支`server/solana.js`和`server/wallets.js`已经显式配置1，避免重复报告不存在的v1 opt-in缺口；真实v1解析完整度仍未知。
- https://solana.com/docs/tokens/extensions/transfer-fees 确认Token-2022的TransferCheckedWithFee/TransferChecked可能产生withheld fee。此前 `economic-events.mjs` 只识别transfer/transferChecked，本轮加入 `transferCheckedWithFee` 识别，并在 `test/economic-events.test.mjs` 加合成转账1000/扣费50/接收950的指令与余额对照。原RPC raw_json/feeAmount保存，报告中的`amountRaw`明确仍为**gross原始指令数量**；`economic-network.mjs`追加警告，不虚构net可卖库存。**Code submitted, current SHA GitHub Node24 CI未确认执行**；复杂Hook/CPI与真实2022协议交易仍待复核。
- 来源对照账已更新这一事实修正；Google Skill Reach的技能选择漏选/误选/冗余标准用于之后真实模型比较，不以“已搜到资料”替代知识实际选用。

**不可忽视的集成阻断**：PR #23目前和最新`blix`的 merge base 为`3bc1f7d4befc4e11e21d9a67fabbd5c4d259b1e7`，相对blix前进158个提交、落后35个提交，GitHub报告`mergeable=false`。主干也修改过`knowledge/README.md`、`knowledge/mechanisms/wallet-roles-and-inventory.md`、`knowledge/mechanisms/market-price-mechanism-research.md`、`knowledge/references/source-coverage-v0.1.json`等共享知识位置。本轮没有强制合并或覆写分支；需做原始共同祖先/主干/PR的三方冲突审查并保护两边有价值新增研究，之后在已支持CI的环境重跑Node24完整、intelligence、安全、经济及Web测试。

**下一项**：解决合并冲突、执行最新 SHA 正式测试；对一条真实2022费/Hook交易检查实际接收资产变化；用同一批真实任务对比无知识、旧11源、新11源的模型知识选择和专业错误率。未审152/65部分继续按原目录与信息价值深读，不把来源登记/静态覆盖视为全部知识已经验证。


### 2026-11-13｜R-15：知识获取→承接→实际应用→反向追溯完整概念与已有资产收束

**用户任务**：不要再限于P1/P2某个知识点，而应全面理解“来源如何发现、获取、继承、改造、合并、调用、验证、撤回，并从当前判断反查其原始出处”的完整知识生命过程。已核查本项目 `knowledge/MIGRATION.json`、`knowledge/references/source-coverage-v0.1.json`、`DOMAIN-MODEL.v1.json`、152单元路由、D12/AI知识调用源码、经济事件与资金图谱代码及测试，并回查旧Hermes证据链/钱包结构、qb-旧保留案例、meme-真源、ai-d知识维护规范。外部W3C PROV-O、OpenLineage、DVC、Google Skill Reach只作为概念/产品设计对照，不额外安装新服务。

**真正新增的研究与归位**：
- [完整知识生命周期与可逆谱系](../../knowledge/references/knowledge-lineage-lifecycle-20261113.md)：11类知识对象（问题、来源、观测、概念、主张、方法、案例、实现、决策、验收、修订）与不强制执行的来源发现/获取/版本/原意重建/跨源反证/吸收/归档/检索/程序应用/实测/反向修订；知识价值与当下代码落点独立。
- 明确区别**出处溯源、证据溯源、加工溯源、承接溯源、执行溯源、修订影响溯源**。同一文档可支持多条具体主张，不因文档被复制或目录扫描而认为每一主张受证据支持。
- 原位更新 `knowledge/README.md`、`knowledge/references/README.md`、`docs/project/knowledge-use.md`、`knowledge/ai/intent-knowledge-selection-and-reasoning.md` 的导航，继续以已有P1/P2专业来源核查和D01–D12原文件为知识真源，不复制历史项目全文。
- 本分支已有 `scripts/audit-knowledge-trace.mjs` 与 `test/knowledge-lineage-trace.test.mjs`，本轮**没有新建重复工具**，而是说明其可用的`--all / --unit / --target`与限度。该代码从现有manifest做**文件级双向静态映射**：历史152单元/21迁入记录/21源快照索引/11个AI知识候选源；不联机校验每个上游blob、不逐主张核验、不测试模型实用或主网真实表现。
- 代表案例已连通原始来源→拒绝旧错误→Blix已有代码/回归位置：Hermes“Fee Payer≠资助者”，qb-95钱包“零余额≠卖出”、Token转仓/接收方卖出只是摘要候选，旧meme价格结构≠真实成本、ai-d检索命中≠知识使用正确。不同对象的**来源已读/代码已有/合成测试/真实运行/经济事实**分开保留。

**验收状态**：所有新增/修改知识正文已写入本PR #23分支；GitHub回读及相对链接/静态审计待独立核查。不能借用旧CI当本轮改动通过。PR #23仍Draft未合并，先前检出的 `mergeable=false` 共享知识文件冲突未修，不强制并入`blix`。原版产品、签名/交易、付费模型、真实RPC和Grok部署均未触动。

**接下来仍未做好的实质性知识追溯**：152研究单元从原文段落到**具体主张**的逐项引用与反例；65参考资产的源码/测试/版本/Issue/评论完整审查；来源变更对下游代码/报告的自动影响追踪；知识选择→模型输出→实际链上结论的固定任务A/B。优先用单Mint“资金源→转仓→接收后卖出”做一次双向逐证据链追溯，不靠提高文件数量宣布专业知识已吸收完。

**本轮末复核/小范围运行时入口修正**：已回读知识全链说明及相关四个原入口，静态检查全部相对链接可达、Markdown代码格式正确；再次从现有清单计算21/21已登记本地目标存在、144/152旧单元映射、8个L0仅索引、21旧快照正文未本地导入、11/11本地AI允许源存在。复用现有 `test/knowledge-lineage-trace.test.mjs` 并增加知识说明入口完整性测试；在现有 `local-knowledge-loader.mjs` 的 **D12 ai-knowledge** 原11源路由内补充“知识追溯/承接/获取/形成/生命周期/修订”口语别名，并加3条对应回归用例，不新增模型权限或新的知识系统。对新问句按当前词面算法静态检查能命中D12；**截至本次检查最新SHA没有新的Node24 CI工作流记录，不能据此声称回归已在GitHub跑过**。PR #23仍有与最新blix的合并冲突；不强行合并或覆盖双方知识。


#### R-15 补记｜知识术语、静态双向溯源和可查缺口

**实际断点**：旧152单元索引、21迁入文件、21历史快照来源清单、11运行时知识白名单和产品真实执行属于五种不同证据身份。此前文件来源→当前承接→AI可选的双向映射不可直接核查，容易把来源扫描、复制、理解、实现与真实效果混为一谈。

**已完成研究成果**：以[知识全生命周期唯一总入口](../../knowledge/references/knowledge-lineage-lifecycle-20261113.md)为主；[细分概念与静态双向溯源附录](../../knowledge/references/knowledge-lineage-lifecycle-audit-20261113.md)进一步审查断链；对照旧Blix D01–D12、Hermes/qb-/meme-、ai-d的知识维护原则、W3C PROV-O来源关系、OpenLineage输入/输出/运行关系，梳理发现、获取、原项目逆向理解、主张与适用条件、承接、转代码/AI、验证、版本修订、停用与重开。未扩建第二个知识/专家/图数据库架构。

**实际代码**：scripts/audit-knowledge-trace.mjs 只读取已有 MIGRATION/legacy-routing/legacy-snapshots/source-coverage/AI知识加载器。支持 --unit D05-K01、--target knowledge/mechanisms/capital-organization-and-incentives.md 和 --all，输出来源文件/ref/blob→本地文件→旧关联单元→AI可选范围，标记未复查原始blob、未证明真实模型调用。test/knowledge-lineage-trace.test.mjs 回归 21迁入均存在、152旧单元中144为文件级本地关联、8个L0旧Atlas-only、21旧快照正文0本地、11白名单均存在、拒绝未知单元和越界文件路径。package.json 加入 npm run audit:knowledge-trace 和 npm run test:knowledge-lineage，完整npm test含此测试。

**本次边界**：目前是记录与本地路径级静态映射，不代表144条历史研究的语义逐条得到验证；21快照未导入不等于原始来源失踪；知识被允许加载不等于模型实际使用且正确。PR #23 与最新 blix 仍存在合并冲突，若最新版 CI未触发只能说明已提交/静态检查，不得宣称最新SHA正式通过 Node24。

**下一高价值修正**：解决共享知识文件分支差异，保持双方新增研究；对一条真实Mint调查记录从模型结论逆追原始交易→指令/owner→代码→知识来源/版本与反证，建立真实运行前后A/B验收。资料搜索若不改变重要解释、证据或业务决策则停止扩大范围。



**R-15补记｜42份历史原始Git blob身份复核（2026-11-13）**：本轮不只依赖已有manifest的source URL，使用GitHub连接器按记录的repo/ref/path重新读取21/21迁入项原始文件，返回blob SHA与全部21条登记匹配；又按固定source_commit逐项读取Hermes/qb-/meme- 21/21历史快照原始文件，返回blob SHA全部吻合。旧152单元Atlas、65资产索引和22专家注册表的原路径亦成功读取。核查结果及边界写回原有MIGRATION.json与legacy-snapshot-sources.v1.json；静态 audit-knowledge-trace CLI读取这些有日期的检查元数据，自身**不执行外部blob复验**。上游快照已证存在≠本地21份快照正文已导入（当前0/21），Git SHA吻合≠专业主张逐项审查/原始代码运行/模型效果。下一阶段应把精力投入“逐主张证据→Blix决策/模块→真实任务反馈”的丢失环节。



### 2026-11-13｜R-16：多维知识层级×业务经济机制×AI/工程跨层对齐

**用户意图**：不只追溯知识的获取/承接，而是将概念每个层级、G0–G4目标、L0–L7知识深度、D01–D12专业领域、来源/证据状态、资产主体/经济因果、时间可见性、Blix工程与权限及运行反馈相互解释、相互挑战；判断由此会产生哪些原本未识别的专业问题、反证和实际产品能力。

**原位成果**：已直接扩展原唯一知识生命周期总入口 [knowledge-lineage-lifecycle-20261113.md 第12节](../../knowledge/references/knowledge-lineage-lifecycle-20261113.md)，没有新建多份并行知识地图。对照现有 DOMAIN-MODEL.v1.json、P1/P2领域研究与旧 D12，梳理十种正交层级轴、五种协同推理（纵向/横向/斜向迁移/逆向追责/反馈）、知识来源图/经济事件图/运行血缘图的类型差异，以及多Mint共享资金、接收Token后卖出、6/12h前兆、跨Mint资金、跟单可复制性、知识实际应用的逐层问题和反证。参照W3C SKOS的概念语义、PROV-O的来源加工关系和OpenLineage的运行输入输出，只借鉴关系语义，未安装平台或扩权。

**产生的实质性候选认识**：市场异常与测量异常分离；钱包关系按证据类型/时间局部成立；资产转移、经济对价、库存成本分账；领先钱包获利与后续可执行获利分离；知识真实性/选中/实际正确使用分别评估；研究方向应由跨层解释断裂而不是文档数量决定。它们是推演和待验证测试要求，不能宣称已经发现统计意义上的同控率、预测优势或Alpha。

**验收与风险**：已提交GitHub并回读文档关键标题；本轮仅是概念/知识关系研究，不等于自动语义匹配引擎或主网实测。并发中的逐主张链上归档追溯代码修改在本轮并未全部验收，最新 Node24 CI 尚无可核实的完成记录，不借用旧CI冒充；PR #23仍Draft且 mergeable=false。近期Uptime失败没有检查Job，不能据此断言网站离线。

**下一个最有价值的验证**：冻结一条真实Mint的共享资金→Token转仓→接收后卖出调查，比较单域解释与跨层解释在同一证据/时间/费用条件下减少了哪些误归因，是否多找到真正可复核的证据；再将有效的专业主张绑定到指令/原始RPC/代码版本和旧知识来源。失效的跨层联系降级，避免固定多层框架占据AI上下文。


### 2026-11-13｜R-17：原知识模型的关系契约与原位回归修复

**原问题定位**：先前 R-15/R-16 已经说明知识全生命周期、七类通俗研究视角和十种横向/纵向知识轴，且已在原交叉表写了跨领域解释。然而 `DOMAIN-MODEL.v1.json` 里仍只有旧 G/L/D/存放/证据轴，并未结构化说明“概念关联 ≠ 经济关系 ≠ 来源支持 ≠ 实现依赖 ≠ 测试通过”，导致这些词可能被AI、程序和后续研究混为单一种“关联”。当前工具只有文件级双向索引，不是逐主张的可信度引擎。**选择原位修复，不另建本体/知识图谱/专家制度。**

**本轮具体改动**：
- `knowledge/DOMAIN-MODEL.v1.json` 保留原 `schema_version:1.0`、G0–G4目标、8个L层、12个D域和15个原领域链接；新增明确版本的 `cross_axis_alignment`：十种正交观察轴（GOAL、DEPTH、DOMAIN、KNOWLEDGE_OBJECT、SEMANTIC、ECONOMIC、EVIDENCE、TIME、EXECUTION、EVOLUTION），11种**有方向和禁止升级界限**的关系，以及6组资金/库存/跨币/知识调用/CI的专业主张证据门槛。状态为 `CONCEPTUAL_CROSS_AXIS_GUIDANCE_NOT_RUNTIME_REASONING_ENGINE`。
- `knowledge/INTEGRATION-CROSSWALK.md` 第7节把原七种通俗观察视角**多对多**对齐到十轴；进一步以Mint→Token转移→接收方后来卖出候选，横穿账户、经济机制、源码实现、证据、时间、AI/反馈，并明确共享资助、同槽、重复钱包、词面知识匹配均不能自动提升身份/盈利结论。
- 直接修订原 `knowledge/README.md`、`docs/project/knowledge-use.md`、`knowledge/ai/intent-knowledge-selection-and-reasoning.md` 导航与AI适用性，要求以真正影响判断的**具体主张**为核心做有限关联，不要求每轮填10层或全域研究。原历史知识与旧版本原文不删除。
- 复用 `scripts/audit-knowledge-trace.mjs` 增加 `--axes`，只读展示现有原模型的维度、关系、禁越级条件与示例；原 `--unit/--target/--all` 保留。给 `test/knowledge-lineage-trace.test.mjs` 增加静态模型与CLI契约测试，保护原8层/12域/152历史单元、链接与关系语义。
- **真实CI发现并修复了一个旧文档断点**：首次支分支GitHub Node24全套533例中532过、1例失败，指出 `knowledge-lineage-lifecycle-audit-20261113.md` 缺少明确“原始来源”定义。已原位补充原始Git版本/原始RPC事实/作者解释/程序验收四类不同的证据对象，保留回归断言。修复后 [Node24 CI #43364041758](https://github.com/sunshihao001/grok/actions/runs/43364041758) 为 success；未为过绿删除断言。
- 原 PR #23 `mergeable=false` 导致 `pull_request` Node CI 不触发，本分支只在已有 `.github/workflows/test.yml` 与 `audit.yml` 的 `push` 分支白名单中增列当前集成分支（主分支现有行为保留），使真正测试和Web/依赖审计可持续运行。已观察 [audit #43364153785](https://github.com/sunshihao001/grok/actions/runs/43364153785) 成功；最新提交的测试应再按实际run确认。Uptime无检查Job的失败不等于站点故障，不为绿灯改变健康探测。

**静态审查**：从GitHub回读7个关键现有文件，解析 DOMAIN-MODEL JSON、核查10轴唯一性/11种边类型/6组约束/原15个关系与12域8层不变，确认三份导航与章节锚点一致、根README误写的字面 `\\n\\n` 已修复；结果STATIC_CHECK_PASS。此静态检查只证明结构一致，Node CI只证明既定可复现样本，不代表150多个旧主张全部认知、实际模型A/B、真实Mint主网全历史、控制权或盈利判断。

**未闭合问题和优先顺序**：
1. **已有PR合并冲突**：PR #23仍Draft、`mergeable=false`，共享知识文件在`blix`主干和本分支存在双向修改，合流需三方比较并保留双方新增内容；本轮不隐式合并/覆盖。
2. **逐主张证据**：目前旧21迁入/152单元仍主要是文件级对应。高价值主张尚缺真正 `claim ↔ raw transaction/rpc ↔ inference ↔ implementation/test ↔ source version` 的完整端到端记录。
3. **真实有效性**：需要一条真实Mint（A买入→Token转仓→B卖出候选→跨Mint资金可能接力）固定原始输入的证据对照，验证多层知识能否提高正确性、反例覆盖和合理补查；不能只比较文字长度。
4. **模型与市场实测**：11个本地候选知识源的真实使用/错选记录及 Token-2022/CPI/公共设施/成本/多池仍待实际授权条件；不会让知识本身授权下单/模型费用/签名。

**停止锚点**：今后只当跨层关联改变具体重要专业判断、可核查证据、运行实现或减少重大误关联时再扩展关系；如果只是更多关键词和分层图，没有真实测试价值则停止，不重写原历史知识。


### 2026-11-13｜R-18：从知识分层转向交易机会优先的全主体源码核查

**用户方向确认**：既要发现「值得深度调查」的Mint，更优先找「具有实际交易机会」的Mint。知识来源/领域/证据/层级是按需支持，不是一条所有币都要走完的硬筛选管线。

**本轮实际源码交叉核查**：`blix@58bbff4f` 的Discover/Pulse、新币triage、traction、early逻辑回归、research AI结论、brain入场/风险守卫/scorecard、rules walk-forward、paper报价模拟、wallet smart跟随、React现行路由；PR #23 `ai-workflow`（仅Mint研究）和`followability-replay`（显式纸面收据、只读门禁）。新增审查与来源链接写在 [全主体审查第14节](whole-product-cross-layer-audit-v0.1.md#14-2026-11-13-补审交易机会优先原版选币闭环--ai-专业调查--可跟随性)。**原版已有完整候选→筛选→入场观察→纸面退出→效果反馈的源码骨架，不应重新发明第二套选币引擎。**

**新发现的优先缺口**：模型和信号“过去预测/触及涨幅”不能等同**用户信号可见时点后的可成交净结果**。原 `brain.js` 固定每边3%+市值比例代理与`paper.js`更接近实际路由报价的纸面机制需区分；`early.js`时序留出仍需独立后续窗口/特征时点与候选全集检验；不同胜率标签（先2x再-40%、退出净倍数>1.15）口径不同；低分、漏样本与报价失效不能从分母中消失。

**下一项工程验收**：复用原Discover/Pulse/brain/rules/paper及PR #23可跟随性门禁，在同一段冻结历史时间窗把「全候选→入选/拒绝→信号首次可见→报价可得→模拟进出→结果」逐条归档，早期/趋势/钱包跟随三种机会来源对照，不做真实下单。先用无新鲜报价/延迟入场/不可卖等确定性反例验证无法计算真实可交易收益，合成通过后再决定可用的真实归档与只读数据源。必要时只做薄适配，不新建总评分或固定多层Agent。

**状态/风险**：STATIC_SOURCE_REVIEW、DOC_UPDATED；尚无新代码/新测试/真实市场、主网/模型/账户运行验收。PR #23仍Draft且GitHub提示mergeable=false；当前分支与 `blix` 的共享知识变更须先三方合流，不能自动合并。任何最新CI必须按更新后的SHA单独核验；不把历史绿灯当作本提交通过。
