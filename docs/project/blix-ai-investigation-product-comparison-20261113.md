# Blix AI 扩展｜完整调查业务链 × 成熟产品源码对照 × 设计否证（2026-11-13）

> **研究结论，不是实现验收。** 目标是重新审问此前的三栏“AI工作台+知识加载”是否值得作为产品主体。当前审查基准：`sunshihao001/grok` 的集成候选 `f9efe0305c040c3a0029db779f6ff2647d7b45fd`、PR #23（Draft、未合并、mergeable=false）；旧Grok/Hermes/qb-/meme-/ai-d 的已有来源继承与研究记录。资料来自原仓指定源码/测试、已有三次供应商真实归档的**历史复核报告**、Bubblemaps官方文档及外部开源项目代表性源码。**本轮没有重放原始RPC、没有启动Blix或外部程序、没有运行真实模型、没有付费API、没有下单、没有验证收益。** 既有报告中“真实归档”“离线合成测试”“源码可观察实现”“推论/建议”分别保留状态，禁止拼合成一条假真实资金闭环。

## 1. 先判断：什么才是要交付的能力

原用户目标不是“一个支持聊天和知识引用的页面”，而是以**完整原版Blix**为基石，面对代币、钱包、资金网络与市场事件，能够：
1. 发现和筛选有价值的观察对象；不遗漏被过滤或未进入AI队列的样本。
2. 由Mint反查真实关键地址，区分Pool/Vault/Token Account/Owner/中转服务与可能的行为钱包。
3. 追踪“首次买入→Token转给接收者→接收者后续卖出→SOL可能流向另一个Mint”，同时区分**可观察路径**、**具体资产库存来源**、**同控解释**。
4. 对市场结构/动机形成竞争解释，并根据新增证据改变调查目标；保留来源、快照与失败状态。
5. 针对实际参与或跟单问题，独立判断信号是否来得及看见、可否取得有效入/出报价、滑点/深度/费用、样本外价值。
6. AI 使用已承接的专业知识和Blix成熟能力，而不是复制一套行情终端、强制专家阶段或全量注入旧知识。

**设计否证标准**：若新工作台/知识检索相比原Coin/Bubble Map/Research并未改善调查覆盖、事实准确性、跨Mint连续性、历史重开或可参与性，则它只是第二个UI，不是专业扩展。

## 2. 固定同一真实 Mint：事实在第几环停止？

**历史样本**：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`；2026-11-01三次DEX Screener/RugCheck在线抓取的历史归档已经在 [single-mint-audit.md](single-mint-audit.md) 第7节记录原始SHA、GitHub Actions run/artifact与复查结果。这里借用**已复核的历史记录**，本轮未重新下载归档或校验最新有效性。

- **02:44→03:23 UTC**：报告价格约 -6.075%；主要PumpSwap池 Token储备 +1,443,150、SOL储备 -8.0596；方向符合净卖入池的候选解释，但尚需排除 LP 增减、刷新/缓存时间、费等；**不能确定具体卖家或Swap序列**。
- **03:23→03:26 UTC**：价格约 +2.169%；主要池 Token储备 -400,272、SOL储备 +3.66125；方向反转，但没有对应完整Swap/LP签名链。
- **主池 vs 旁池**：主池流动性约8.9万至9.1万美元，Orca旁池仅约48美元；价格差异不能直接推成可成交跨池利润。
- **身份重要反例**：RugCheck最大Holder Token Account的Owner与PumpSwap主池地址重合，且有AMM相关标识。该~5.9%供应商供给记录首先应视作**池设施候选**，不应当成私人鲸鱼控筹。
- **目前没有**此Mint的可复查“买方A原始签名→A向B的确切Token指令→B可归属的卖出→资金转给D→D买另一Mint”的完整链条。**跨Mint资本循环、幕后共同控制和当时的可跟随盈利都为UNKNOWN**。

因此，真实案例当前强项是**市场快照、池库存方向候选与设施/Holder交叉校核**。从“真实买家A”的链上签名这一步起，完整经济业务链就没有足够原始证据。不可把另一批 `test/economic-network.test.mjs` 或 `test/followability-replay.test.mjs` 的**合成A/B/C和纸面收据**冒充本Mint真实钱包交易。

## 3. 同一业务链：Blix已有/PR#23局部新增/真实缺口/成熟参考

| 场景 | 原版Blix已可观察的源码能力 | PR #23已做的局部增量 | **现阶段不成立或未验** | 对照参考与取舍 |
|---|---|---|---|---|
| ①发现Mint | `engine.js` / `triage.js` / `early.js` / `research.js` / `brain.js`；Pulse、Discover、现有筛选与历史观察 | `Intelligence.tsx`订阅同一`usePulse`看板，仅按展示优先顺序组织候选 | 并未拓展采集覆盖；新工作台不是独立机会发现引擎；漏掉/筛掉的对象与AI队列之外样本仍需对照 | **Pulse**的生命周期和归档、**Million**结构化拒绝决策/Shadow对照；不复制第二套扫描器 |
| ②关键地址筛选 | Coin Holder、Dev、`bubblemap.js`同时利用RugCheck图、首笔直接SOL资助、同Slot/发射群体；已修复fee payer误充资助的部分历史错误 | `mint-facts.mjs`仅读Token/Holder两条本地GET；`inspect-economic-mint.mjs`从已捕获RPC事件按Mint挑最多10名发送Owner | UI不同Holder口径/分母/来源、排序可能遗漏非Holder；发送者筛选也可能含Pool/路由/服务 | **PumpTrace** Creator/Wallet Intelligence；**Bubblemaps V2** Magic Nodes/Time Travel；**qb-**关键地址与设施矩阵 |
| ③Token转移A→B | `wallets.js`新增真实RPC交易捕获；`wtrack.js`显示部分被跟踪钱包的买卖/简单转账；BubbleMap展示关系候选 | `economic-events.mjs`保存完整`jsonParsed`交易+hash及CPI指令位置；`economic-network.mjs`用`sig:outer:inner`去重并保留BigInt raw量和Owner | **原`wtrack.parseTransfer`在Swap交易直接跳过、复杂多token动作可能返回null**；归档只覆盖已读钱包/签名而非全网所有A/B | **PumpTrace**可恢复补查；**Bubblemaps**跨Holder中转关系；不能把图连边代替Token动作 |
| ④B后续卖出 | `wallet_trades`和Wallet/Tracker可显示记录的卖出摘要 | `recipientOutcomes`在本地24h窗口内查B的`wallet_trades`卖出签名，附到对应Token转账候选；`economic-claim-trace`明确两种证据不同 | **查到B卖出不等于卖的就是本次A转入库存**；没有完整B历史/成本基础；`wallet_trades`以(sig,wallet,mint)主键压缩多动作概要 | **PumpTrace**历史活动窗口和卖出上下文、**Hermes**钱包角色迁移；先保留局部有卖出，不冒充库存确证 |
| ⑤SOL→另一个Mint | `wallets.js`钱包交易汇总和`wtrack`多Mint追踪；原版图最多部分资金来源多跳 | `crossMintCandidates`将本地“B卖出Mint1→捕获的SOL转给D→D买Mint2”按时间连接并去重，`compareCapturedCrossMintWallets`比较同地址两Mint样本 | 只是**时间顺序+局部交易/Transfer**；SOL可混同、服务地址/DEX/Payer未知；不能声称该笔卖出Lamports精确出资新Mint | **Million**从钱包资金对手扩张未知新地址，但其源码也承认交易所充值地址和新鲜度未完全验证；**Why-Solana**多跳与结构/优势分离 |
| ⑥机会是否真能跟 | `brain.js` Paper与历史outcomes、`early.js`留出窗口；`paper.js`独立纸面机制 | `followability-replay.mjs`按用户提供的纸面进出收据验信号可得、报价新鲜度、费用、滑点、库存连续性 | **未生成当时可靠的入出报价**，没有真实成交，也没证明策略样本外Alpha；`brain.js`的固定每边3%模型不能代替可成交报价 | **Million**决策日志/Shadow验证过滤规则的反事实，**dexterm**只读 Agent/纸面边界。不可直接引用历史倍数当可跟收益 |
| ⑦历史重开与修订 | 原版SQLite/Journal/Brain Playbook/Wallet；不同数据窗口和持久化不同 | `economic-snapshot-review.mjs`比较本地两次可见事件、修订和同地址跨Mint，不把回填误称新链上活动；`knowledgeUse`记录呈现给模型的来源 | 尚无从原版Coin页进入、跨会话可续的完整调查收据；AI输出仍未连接真实模型 | **PumpTrace**游标恢复，**FlowLens**案件/证据抽屉仅借业务设计（EVM代码不可直接用于Solana），**dexterm**按客户端权限暴露终端数据 |

### 三个容易被当前设计隐藏的源码事实

**(A) “只读GET”不必然“无副作用”。** `server/intelligence/local-reader.mjs`只允许本地`/api/token/<mint>`及`/api/holders/<mint>?top=25`，但`server/server.js`中Token GET本身可调用`lookupMint`、`adoptMint`、`vet`，进而引发新收录/数据库变化/供应商使用。**如果未来给AI接真实服务，不可仅凭`GET`和manifest`readonly:true`授权；需针对已有路径作副作用/缓存/费用检查或隔离快照读。**

**(B) “没有转仓显示”不等于“原始交易没有转仓”。** `wtrack.js`的`parseTransfer`只在交易符合“单Token且SOL净额很小”或“无Token且SOL变化足够大”时返回一条摘要；如`sol.parseSwaps(tx,addr).length`则`fromTx`跳过。PR #23已有原始RPC交易+指令保存，应该从后者读取**真实动作**、标记UI摘要覆盖，而不是另写一个会丢CPI的Tracker解析器。

**(C) “跨币共同地址”不是“资金流回路已闭合”。** 即使见到B曾卖Mint1、B/D有SOL转账、D买Mint2，除非能够提供签名、Slot、账户净额、费用、交易对价及时间约束，仍不能确定资金来源、同控制权或盈利。`economic-claim-trace.mjs`现有`cannotEstablish`正是对此设限，应该成为报告/UI中可点击的证据边界。

## 4. 外部成品的**独有产品思路**：接什么，不接什么

| 项目及定位 | 可直接参考的原始路径或官网 | **应该借用的能力认知** | **不应照搬/不可冒充** |
|---|---|---|---|
| [Million](https://github.com/Kelows/million) | `apps/api/src/opportunities/opportunities.service.ts`，`funding/funding.service.ts`，`common/decision-log.ts`，`trading/shadow.service.ts`，`.claude/skills/why-not-bought/SKILL.md` | Mint↔Wallet↔新Mint双向发现；“为什么跳过”持久决策与错过机会的对照；新钱包资助边先入候选不立刻订阅 | 有自动交易部分；不能整套接入签名/授权。FundingService注释明示交易所存款地址风险，不能宣称同控 |
| [PumpTrace](https://github.com/AntC215/Pumptrace) | `src/modules/wallet-intelligence/service.mjs` 与 `src/modules/backfill-manager.mjs` | 对象级报告、数据时间窗、游标/中断/限额/恢复，使同一钱包调查可以继续 | Helius/API费用、各源覆盖需要验证；其链上角色标签不是私钥归属的证明 |
| [Bubblemaps V2](https://wiki.bubblemaps.io/bubblemaps-v2/how-does-it-work) | 官方 [Magic Nodes](https://wiki.bubblemaps.io/bubblemaps-v2/magic-nodes)、[Time-Travel](https://wiki.bubblemaps.io/bubblemaps-v2/time-travel) | 将“现在不在Holder的中间地址”与“历史某时点的Holder/关系”带入图；图上有原始关系查询入口 | Blix**已有**BubbleMap，优先对照缺少的非Holder/历史维度；官方iframe/API可行性、许可和授权另核，不复制外部图 |
| [dexterm](https://github.com/dexterm-xyz/dexterm) | `packages/agents/src/tools.ts`、`gate.ts`、`spectator.ts` | 同一终端状态被Agent安全读取，权限和参数来自服务端门禁；操作者可看到模型/工具操作记录；不需要另建数据终端 | 不能直接假设其Agent能完成完整Solana资金归因；paper与真实执行分开 |
| [Pulse](https://github.com/nirholas/pulse) | `src/mcp/server.ts`、`src/report/daily.ts`、`src/intel/wallets.ts` | 原有市场档案与生命周期供Agent查询，日报先存后推送；市场失败/未入选样本影响发现评估 | 并非所有交易历史被无损保存，原Blix已存在行情流与发现UI |
| [FlowLens](https://github.com/tobenwarrior/FlowLens) | `src/components/Evidence.tsx`、`server/agent.ts`、`docs/mcp.md` | 将资金网络、交易凭据、可扩展调查案件和来源解释放在同一调查上下文 | 面向EVM、AGPL-3.0，**只借设计思想**，不能无许可直接嵌Solana业务源码 |

## 5. 旧知识的真正位置——不是强制“11个知识专题一起上”

- **Blix自身**：`brain.js`、`early.js`已有实际筛选与反馈；`coin.js`/`bubblemap.js`有真实业务产品，不应因AI扩展重新发明。
- **Hermes D04/D05/00c–00e**：提供“钱包角色→可观察行为→资金/库存→反证”以及未知异常问题生成；旧高概率同控、固定数值阈值和未经校准的利润判断只作为历史假设。
- **qb-**：单Mint调查矩阵、地址/设施登记、数据护照、缺口描述，帮助选择下一批值得补的地址，而不是搬旧GMGN命令执行脚本。
- **meme-**：价格/供应/库存关系及失败形态竞争解释。在此次真实样本优先区分Swap与LP变化；不把POC/AVWAP当Solana链上可证明资金成本。
- **ai-d**：将“我觉得某币被安排了”等普通话提升为可证伪问题，并优先调旧能力、在关键信息不足时停止“假完成”。这不是一个必须每次运行的独立AI管理层。
- **参考成品**：外部知识有“成熟直接复用/小改/只借业务思想/证据不够暂不用”四种命运；需按许可证、API副作用、时效、实际验收决定，不由相似UI名字决定。
- **当前`local-knowledge-loader.mjs`**：11个白名单来源按关键词选少量片段，`ai-workflow.mjs`现已在plan/followup/interpret阶段输入；`knowledgeUse`仍只表示**提供给模型**。其最多2个Mint事实读取工具和单Mint范围并未因知识接入升级为跨Mint Agent。需要用有/无知识、同事实、同预算的真实模型A/B去验增益；无增益可不启用。

## 6. 新的设计选择：原B视觉工作台降级为可选视图

**现在不宜定案为“三栏主界面+永驻聊天+第二张钱包图”。** 我选择的候选路线：

**首选：原版Blix的对象上下文式“调查工作”**。从原Pulse/Discover中的事件、Coin Mint、钱包或图谱关系可进入同一调查上下文；自动附带当前Mint/Wallet/观察时点/数据源，AI只有在需要时选知识与只读工具。调查对象带有证据收据、反证、未完事项及可继续观察对象。Coin原图和市场页不复制，必要时才打开侧边调查面板。该方案的“可继续”是**产品验收目标**，不是说现在已实现持久化调查案例库。

**条件触发：独立专业调查工作台**。只有实测发现“多Mint多地址连续取证”在原Coin/Wallet切换中确实造成大量上下文丢失、且独立界面能显著提高调查完成率，才将现有`#/intelligence`强化成专用调查台，而不是默认建设中心。

**后置：自主机会/跟单信号Agent**。原Blix的早期/趋势/跟随候选、跳过理由和历史结果应先做可得时间与报价审计；在未建立样本外优势前，不以LLM主观分数改变真实交易门控，更不自动开启原有签名/交易能力。

这不是三个强制阶段；它们可在不同使用场景并存。当前最值得验证的是**首选方案能否只复用原有数据而完成更深入的经济调查**。

## 7. 可执行的统一验收与停止条件

**真实 Mint 证据主线（上面固定的Mint）**：先读取三次归档与原始SHA，确定Pool/Owner/时间；再寻找02:44–03:26内主要池Swap/LP的确切签名及相关Owner。如果无法用已有已授权档案取得签名，明确停止在`POOL_INVENTORY_DIRECTION_CANDIDATE`，**不伪造钱包A/B、更不声称已跑完整链**；若已有签名，再按`sig+outer_i+inner_i+token_account+owner+asset_delta+slot+event_time+first_available_time`逐步扩展。

**离线规则/安全主线**：既有`test/economic-network.test.mjs`覆盖多CPI/BigInt/重复、转发和“不能同控”；`test/followability-replay.test.mjs`覆盖纸面信号时点、完整退出、费用等拒绝样例。这些是**验收规则的初步基础**，不能当真实Mint跑通。

**第一项新增价值验收**：在相同归档或固定真实追踪批次上，比较原Blix Coin/Wallet手工调查、Blix+确定性经济事件、Blix+按需知识/AI三者。至少逐项核查“关键地址召回与误报、原始可追溯签名覆盖、接收者后续事件覆盖、跨Mint假连接、缺口说明、完成耗时/API成本、是否产生错误交易价值判断”。**必须包含不成功/被筛选掉的对象**，不能只看漂亮案例。

**否决条件**：如果新增AI界面只多了文本和引用，不能比原版更准确/更容易持续调查，应停止继续扩UI；如果原始交易来源无法在安全受限环境取得，应先解决读源、恢复和覆盖，而非再追加知识检索；如果持久调查记录没有证明跨会话收益，不先建新的案例数据库。

## 8. 总裁决与真正下一项

- **保留**完整原Blix主体及Draft PR #23既有离线经济证据、来源可追溯、知识选择回归；这些已有不同价值。
- **暂缓**“三栏AI研究工作台为建设中心”“只接一个通用AI模型就能自主调查所有Mint”“扩大知识专题数量即专业化”的预设。
- **第一验证任务**：用固定真实Mint的**主池在指定42分钟的原始Swap/LP交易与地址证据**核查一项价格库存机制假说，并据此评估能否继续向接收钱包扩张。若没有原始数据，明确记录数据缺口，转而先用已捕获RPC的真实独立Mint验证钱包→接收卖出链，两个样本不得拼接。
- **第二验证任务**：在同一事实记录上测试“原Blix / 原Blix+经济证据 / 加AI知识选择”三版本；比较真实调查质量和使用代价。只有证明必要再改变UI入口。

**证据与风险标签**：这份报告属于`SOURCE_REVIEW + PRIOR_ARCHIVED_VENDOR_ANALYSIS + ENGINEERING_INFERENCE`，不是`REAL_RPC_END_TO_END`、`LIVE_RUNTIME`、`MODEL_AB`或`PROFIT_PROVEN`。设计能被下一次原始交易、主网覆盖或真实用户操作对照推翻。

## 9. 复查源与文档定位

- 当前实际代码：[PR #23](https://github.com/sunshihao001/grok/pull/23)；`server/intelligence/{mint-facts.mjs,mint-economic-evidence.mjs,economic-network.mjs,economic-claim-trace.mjs,ai-workflow.mjs}`；`server/{economic-events.mjs,bubblemap.js,wallets.js,wtrack.js,brain.js,early.js,server.js}`；`scripts/inspect-economic-mint.mjs`。
- 真实Mint历史：[单Mint三时点证据核查](single-mint-audit.md)；[跨模块来源与失败反例](mint-cross-module-evidence-audit-v0.2.md)；[全主体与交易机会审查](whole-product-cross-layer-audit-v0.1.md)。
- 本地知识来源/实际接入：[knowledge/README.md](../../knowledge/README.md)；[来源覆盖](../../knowledge/references/source-coverage-v0.1.json)；[知识全链追溯](../../knowledge/references/knowledge-lineage-lifecycle-20261113.md)；[建设台账](build-register.md)。
- 外部原始实现：Million、PumpTrace、Pulse、dexterm、FlowLens上述官方GitHub仓库指定文件；Bubblemaps [V2](https://wiki.bubblemaps.io/bubblemaps-v2/how-does-it-work)、[Magic Nodes](https://wiki.bubblemaps.io/bubblemaps-v2/magic-nodes)、[Time Travel](https://wiki.bubblemaps.io/bubblemaps-v2/time-travel)。外部资料适用性/当前付费功能与许可证仍需按未来使用方式分别复核。
