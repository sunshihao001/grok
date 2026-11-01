# Solana Meme 只读监控成品｜最小分层交付计划 V0.1

> **现行产品方向（2026-11-01）**：V0.1免费多来源真实Mint基础预览已实测，当前实际交付缺口是V0.2钱包与资金/Token关系。阶段号表示产品里程碑，不是AI每轮必须执行的固定流程。旧段落如把OKX完整授权数据当作免费V0.1启动前置，均仅指可选增强版，不应阻断V0.2。
>
> **执行入口（2026-11-01）**。这是一个**产品任务清单**，不是新知识系统、新Bot架构或专家扩编。用户只需要自然语言说明期望的功能和必要授权；GPT承担选型、代码、接口、依赖、安全、测试和验收。**先让现成功能真正跑起来，再按缺口扩展**。每次只推进一个未完成的产品验收，不再因研究持续添加新规划。
>
> **唯一产品目标**：输入 Solana Meme Mint，获得可解释的只读报告；持续观察关键钱包与资金/Token活动，发现群体异常和跨Mint重复活动；最终通过 Grok 用简单自然语言查看结果。跟单收益研究是可选的后续判断，不是当前实现门槛。当前不交易、不签名、不自动支付/收费、不部署未审代码。

## 1｜产品功能拆成六块，避免把专家/知识目录当产品

| 功能模块 | 用户实际看到什么 | 现成可复用的第一选择 | 当前拥有 |
|---|---|---|---|
| M1 Mint概况 | 一个Mint的发行/池/流动性、权限、候选Holder/Dev、来源与缺失范围 | 已写`mint_v01.py`+`public_pair_report.py`；OKX `token-research`成熟工作流/报告消费`mint_report.py` | **DEX公开池 + RugCheck缓存Holder/Creator候选已真实联网**；OKX增强报告未验收 |
| M2 关键钱包 | 关键地址、持仓、买卖/转账、首次/最近活动、来源、疑点 | OKX钱包/Holder结果、Million现成发现/钱包服务；旧qb矩阵作报告语义参考 | 已有供应商字段报告渲染、原型，**无完整真实数据链** |
| M3 资金与实体关系 | 资金来源、群体转账、可疑同源、Dev与跨Mint复用、公共Hub反例 | Million funding/owners/flows；HoldTech holder-overlap、pumpwatch creator候选 | 源码部分审读，**尚未部署/真实验收** |
| M4 异常监控 | 观察1/5/15分钟窗口，钱包群数量/资金/转账改变与告警记录 | Million live feed、现有`wallet_batch_monitor.py`离线算法 | **fixture-only**，无真实连续采集 |
| M5 专业解释 | 现象、证据、最可能解释及替代解释、未知、风险、是否值得继续观察 | Hermes/qb-/meme-专业知识、当前22专家视角与152单元索引 | 知识/方法研究已有，**不是已证预测或自动可靠归因** |
| M6 Grok入口 | 一条自然语言指令→报告/状态/历史记录 | 已有Grok命令入口/运行手册、Million MCP可参考 | **Grok云电脑S1验收未证实** |

六模块属于同一个成品，**不用六个独立Bot**。可复用优先级是“已经能提供整个业务功能的成熟工作流 > 完整项目的安全子服务 > 许可明确的现成解析器 > 最小胶水代码”，不默认自研协议索引器、网页和新框架。

## 2｜四阶段，按可检查的结果依次推进

### V0.1｜真实Mint只读报告（免费基础版已实测；完整增强版待验）
**用户操作**：给一个真实Mint，执行一条命令，得到`report.md`+`report.json`+原始来源和获取时点。

- [x] **M1公开池能力**：在工程PR #16，`mint_v01.py`无OKX JSON时访问DEX Screener只读GET；GitHub Actions在2026-11-01真实查询**两个Mint、5+7个池**，保存原始JSON、SHA256和来源。**只是公开池快照，不是完整Mint钱包情报**。
- [x] **M1报告消费器**：`mint_report.py`可以读取已保存的OKX `token-research` JSON，渲染候选Holder、fundingSource/Cluster、Dev/Bundle字段的可用性与UNKNOWN；目前仅fixture测试。
- [ ] **主验收**：使用**明确授权且无钱包/签名/x402自动付款**的隔离环境，真正取得一次OKX现成`token-research`完整原始JSON，固定Mint和采集时间；本仓库只**消费保存的JSON**，不调用有潜在自动付款能力的CLI。若数据源拿不到，转向65项参考里真实具有Holder/Dev业务数据的安全现成方案；不能自动付费或让用户挑复杂技术路线。
- [ ] **同Mint报告对照**：将已取得的真实钱包/Dev/来源字段与真实公开池快照合成**一份用户可读的结果**；不同供应商字段不强行统一、缺失不填0；保存SHA、查询时间、运行错误/来源覆盖。
- [ ] **V0.1验收**：新Mint可重复执行；在结果中看到池、关键Holder候选、资金来源提示、Dev可用信息（无源则明确UNKNOWN）；能分别回查真实来源；空结果/限额/错误可明确失败；没有交易/签名/付款。**若某项没有可用数据，只能验收“池基础版”，不能称完整钱包版。**

**停止新增开发条件**：只要上述主验收达成，即宣布V0.1，不再为“更全面”继续开发新API/图形页面。

### 2026-11-01｜V0.1基础报告真实通过（阶段状态修订）

- [x] **免密成熟成品来源已运行**：`mint_v01.py --rugcheck`使用RugCheck已存在的公开缓存报告，与DEX Screener真实交易池合并，真实Mint获得5池、20个Token Account/Holder供应商候选、Creator候选以及源JSON、哈希、时间。详见[实测证据](evidence/v01-real-rugcheck-holder-2026-11-01.md)和[Actions 运行](https://github.com/sunshihao001/grok/actions/runs/41269179918)。
- [x] **一项重要误判已在程序修正**：Holder候选Owner与同Mint DEX池地址重合（且供应商knownAccounts标AMM）自动标明基础设施候选；返回20条中1条已标AMM，19条未分类，**不可当19个独立人类钱包**。
- [x] **官方公共RPC替代路线已实际尝试**：受HTTP 429限制，保留可选只读适配，不用无结果反复重试。
- [ ] **完整增强型Mint情报未验收**：没有独立链上Owner/历史、资金来源图、完整Dev系列、单笔Swap和Grok长期运行。OKX有安全授权时可以增强；**不让付费Key成为基础免费成品推进的硬前置**。

**阶段裁决**：`V0.1 REAL_VENDOR_READONLY_MINT_PREVIEW_ACCEPTED`（真实供应商多源只读预览），**不是**`V0.1 COMPLETE_CHAIN_VERIFIED_INTELLIGENCE`。实际业务的下一阶段现在可以转向V0.2真实钱包与资金关系，复用成熟项目而不是继续写Mint概况适配器。

### V0.2｜钱包与资金关系（先单Mint，后跨Mint）
- [ ] 从V0.1已拿到的Holder/钱包开始，先选**一个有来源的地址集合**，输出每地址可审计的Token持仓、交易/转账候选、历史窗口。
- [ ] 优先整套审Million的发现/资金/owners服务和依赖；安全可运行就薄封装，不适合才从HoldTech/pumpwatch或已登记替代中取可许可的具体功能。
- [ ] 资金关系只输出**证据边+不确定性**；公共Hub/交易所/自动执行服务不得误判为同一庄家；转账不等于买卖；把Owner/Token账户/fee payer区分。
- [ ] **验收**：选定真实Mint及钱包，获得可以复查来源的地址列表/资金或Token活动/关系图（表格也可以）；至少提供一个被标为UNKNOWN或反证的例子。无需提前实现全面“庄家识别”。

### V0.3｜持续观察与异常提醒
- [ ] 优先以Million的直播/钱包流为现成业务候选；隔离交易执行能力，确认一条签名涉及多个钱包不会被错误去重。
- [ ] 把**经过确认的真实钱包事件**输入现有`wallet_batch_monitor.py`，复用已有1/5/15分钟聚合，不重写第二个时间窗引擎。
- [ ] 先实现一个观察清单、一次重复采集、一个异常规则和一次重启恢复；增加跨Mint和同群体时序时必须保留市场公共事件对照。
- [ ] **验收**：同一观察组经至少两次实际采集或实际事件更新可产生可追溯的变化报告；有漏数/失败/断连时显示UNKNOWN而非无交易；不自动交易、不输出未经证明的买卖指令。

### V1.0｜Grok自然语言入口与只读交付
- [ ] 完成Grok云电脑固定SHA运行和依赖/费用/日志/退出恢复的S1实际验收，不用GitHub Actions代替Grok环境。
- [ ] 接入`分析 <Mint>`、`监控 <Mint>`、`查看异常`三个实际可用的用户命令（语言接口可调整，底层复用V0.1–V0.3已验程序）。
- [ ] **验收**：在Grok真实运行环境完成一次“用户命令→真实来源→报告/异常→再次查询”的完整只读流程；能显示数据时点与覆盖范围；错误后有停机与恢复证据。

## 3｜哪些事情不用现在做

- 不继续扩建专家、把152项按序研究完、将65项全部安装进系统；知识按实际功能缺口调用并更新原Dxx-Kxx。
- 不从零重写DEX解析/Token索引/钱包资金图，不为了完整而先建漂亮UI、数据库集群、复杂Bot群。
- 不把K线作为主依据；不因开源README称“支持”就当本项目已实际运行。
- 不处理真实交易、私钥、签名、自动收费或x402付款；未经授权的API/许可证/成本即使用现成程序也不能自动开启。
- 不把GitHub CI、合成fixture、公开池快照、完整持有人情报和盈利策略混称一个“已完成”。

## 4｜按任务驱动的实际交付，不再按固定阶段机械推进

AI承担产品负责人和工程整合者的工作：根据用户的目标、当前能运行的代码、专业未知和实际权限，自行决定需要源码调查、现成方案复用、最薄适配、测试、问题修正还是直接交付。用户不需要选择技术栈或规划研究步骤。只有重要授权、安全、费用或不可逆操作需要用户决定。

当前**默认最有价值的实际行动**是 V0.2：从已验V0.1同Mint的真实候选地址出发，优先审现成RugCheck内幕关系或Million funding/owners等只读业务能力，取得一条可回查的资金或Token活动关系，并记录时点、源、反例和UNKNOWN；如果实际数据源受限，按可靠证据重新选型，不能造无来源的关系或继续空转规划。

不强制每轮写状态模板、下一轮提示词、新知识卡或一份研究报告。已有知识按需检索；取得能改变结论的证据才修订；真实输出满足验收就结束该项任务。

**OKX `token-research`真实完整JSON**仍是可选的增强报告来源，需单独确认授权和收费隔离；它不是免费V0.1或V0.2业务能力的必要前置。

## 5｜进度证据与权威来源

- **工程真源**：本文件、工程Draft PR #16的`src/solana_meme_os/`、`tests/`、`docs/evidence/v01-real-public-pair-readonly-2026-11-01.md`；未合并`main`。
- **知识/参考真源**：知识Draft PR #14的`knowledge/system/gpt-meme-project-index.v1.json`（65资产）、`reference-capability-reuse-ledger.v1.md`、`whole-project-convergence-audit-2026-11-01.md`。不把旧104/152目录冲突带入产品实施。
- **正式“完成”**：产出与对应阶段的验收一致。数据供应商返回空/源断流属于覆盖未知；真实网络来自GitHub运行器不等于Grok已部署。

### 2026-11-01｜联合集成PR #17与免密钱包原始交易证据（更新）

- **统一工作树**：工程PR #16与知识PR #14原文件在[Draft集成PR #17](https://github.com/sunshihao001/grok/pull/17)联合验证；来源索引冲突（17旧指针/21新指针）已协调，研究程序和知识导航在该候选分支共存。**不代表原PR已合并main，也不代表Grok已安装**。
- **真实新增数据证据**：使用`public_wallet_rpc_sample.py`在GitHub Actions[41314447575](https://github.com/sunshihao001/grok/actions/runs/41314447575)对RugCheck供应商Creator候选`9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y`调用Solana公共RPC `getSignaturesForAddress`+ `getTransaction`；**真实取回1条签名与1份交易响应**，slot `464112229`，退出码0；没有Key、签名、付款或交易。
- **原始证据指纹**：`wallet-signatures-raw.json` SHA256 `6541d8d4aa25188f5784db2a06e107aff9cffdc4760a8cec893c749407c08fb3`；`wallet-first-transaction-raw.json` SHA256 `46017459e1b9d1673dd8d1f2f055b322c98451111ba7434615c4775a91bdbba2`；已独立下载GitHub Artifact #13086538862并重算哈希一致。
- **安全与完整性边界**：这只证明有限度的真实主网原始数据获取，不是交易语义解码、真实资金网络、连续监控或原Creator身份独立核验；公开RPC是共享限流服务，不适合未经测试直接长期生产采集。是否使用Helius免费密钥/OKX授权需后续按费用和权限实际验证。
- **联合验收**：[GitHub CI 41314658703](https://github.com/sunshihao001/grok/actions/runs/41314658703) 284项离线测试全通过；用户问法到专业领域和可用代码路径已能导航，但Grok Bot实际专家调用与线上运行仍未验证。
- **唯一高价值后续缺口**：真实交易的多钱包/Token可观测事实重建与完整时间窗，复用可信解析/事件服务，随后向Grok发送有证据的异常任务；不自行制造BUY/SELL，也不让新代码重复实现已成熟的DEX解析器。

### 2026-11-01｜真实源→原专业知识→UI状态→Grok任务：同一运行证据

- [在线读数与任务生成](https://github.com/sunshihao001/grok/actions/runs/41315827203) 使用现有Mint `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` 重新调用公开DEX Screener/RugCheck后，依次运行既有 `mint_v01.py` 和 `vendor_event_handoff.py`，两条程序均退出码0。取得**本次2条DEX池记录、1条RugCheck供应商待核查标签、1条大额Holder池Vault降级候选**；不同获取时点的池数不能当作同一快照相加。
- [真实运行Artifact #13086832994](https://github.com/sunshihao001/grok/actions/runs/41315827203) 保存原始响应、报告、`evidence.json`、按现有导航实际读到原知识片段与SHA的 `review_context.json`、七类UX状态JSON及待执行Grok任务。离线CI [41315656644](https://github.com/sunshihao001/grok/actions/runs/41315656644) 288项测试通过。实际运行原始DEX与RugCheck文件哈希与证据包完全一致。
- 已证明：**公开供应商读数→原有知识按需调用及定位→现有UI信息状态→任务文件输出**。未证明：供应商标签为真实欺诈、真实钱包交易异常、经济主体归因、持续数据源、Grok Bot-to-Bot执行、Token成本优势；相关视图保留`NOT_OBSERVED/NOT_EXECUTED`。
- 交付原则：反证池/vault候选，不将“疑似大户”当人；供应商标签按不可信数据编码，不执行其携带的指令；旧任务输出目录复用一律拒绝。**下一必需的产品事实是交易级、钱包级事件同时完备的只读归因和历史覆盖**，而不是再添加一种知识层级或注册更多Bot。


- **修复后第二次真实回放**：[GitHub Actions #41316172134](https://github.com/sunshihao001/grok/actions/runs/41316172134)，提交`13a05718511733001fc460d504a6db2cd2536d98`，`data_fetch_exit=0`、`triage_exit=0`、原始RugCheck/DEX SHA重新校验通过，任务文件的换行已核对正确。其时点 `2026-11-01T14:26:12Z` 有**2条**供应商待核查标签（`Copycat token`、`Low Liquidity`）及1条池基础设施大户降级候选。先前 `2026-11-01T14:22:00Z` 的同Mint样本为**1条**标签；两份RugCheck原始SHA分别为`3ceb24570b851e4bb26ac5e01afa5fea07ef01468cecc40cbf577c9cca718741`及`285d32ece63f7ab86521babad5951e4051f2c9c4a98b359aac959661221f1e23`。**仅能确认供应商快照有变化，不能单凭标签增加推断链上真实风险恶化或其变化原因。** 两次采样均非实时交易事件监控；Grok专家未调用。


### 2026-11-01｜优先复用成熟交易解析器：真实失败交易纠偏

- 复查公共RPC取证原始Artifact [Actions #41314447575](https://github.com/sunshihao001/grok/actions/runs/41314447575)：签名`4ZbrvjMtWEnaa9iPVLedJmbQrMnjDhVR9p2aV47pF81URq6Yuwn2Vfqsnp7QfyMJwZSPSyrvWWYr4rTwGWMZYUmj`，slot `464112229`，**v0 交易执行失败**，meta.err=`InstructionError[2,Custom(1)]`；曾尝试在CPI创建Token账户，但失败原子回滚。Meta显示手续费付款人`7Ej1sc9rwXZdxe9ZGcvCf8QrryFyjR6wj3emKnJXEdY9`的SOL余额净减少 **7000 lamports**，其余28个原始账户SOL余额未变，5个报告的Token账户余额未变；被查Creator候选`9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y`只是账户列表项，非该笔交易的签名者/fee payer。**此交易不可视为成功Swap、转账、资金图边或该候选地址发起动作。** Solana官方原子回滚规则与此吻合。
- [FnZero Python](https://github.com/0xfnzero/sol-parser-sdk-python) 最新主分支pyproject版本`0.10.0`，`examples/parse_tx_by_signature.py`、`sol_parser/rpc_parser.py`可处理RPC交易与DEX协议，`tests/test_signed_transaction_replay.py`对真实失败事件有不生成DEX事件的回归；**以后只读适配其公开接口并实测，不扩展本仓库旧`raw_tx_adapter.py`自写协议解码**。
- [Solana官方交易指令解析](https://solana.com/docs/core/transactions/transaction-introspection) 在JS客户端处理ALT/v0/v1/CPI指令树；成熟实现适合替代协议指令重写；但使用`jsonParsed`不能直接喂其`decodeTransactionFromRpcResponse`，要用base64/json RPC。无需因为该库存在就新增全Node后端。
- [Million](https://github.com/Kelows/million)适合钱包发现和资金关系候选，不能把`FundingService`的`nativeTransfers`边当成经济实控；同时`live-feed.service.ts`的单签名事件持久化及webhook首个钱包break会漏掉其他钱包观察。[Cluster Tracker](https://github.com/garrett0524/cluster-tracker)同样使用单`signature`唯一冲突键；这两个现成系统的**事件存储必须经过同笔多钱包完整性测试**才可用于本项目。[Solana Microscope](https://github.com/solana-foundation/solana-microscope)适合借鉴签名回补/断线和历史记录免触发新告警。
- 本轮只添加`public_wallet_rpc_sample.py`已有只读采样入口的**执行是否成功/fee payer/最终余额观测**，不添加自制DEX解析器、交易策略或Bot。该观察不证明经济主体或Swap路径。下一阶段以FnZero/官方工具真实解析多笔不同交易并对照实际RPC余额，而非扩建架构。


### 2026-11-01｜复用研究转化为可执行的外部SDK对照

- 原参考：`0xfnzero/sol-parser-sdk-python` v0.10.0，固定仓库SHA `cffb6c808c9b7975fc83428c0613fb4c3fa173b5`，上游真实签名保存素材`tests/fixtures/signed_dex_replay_20261009.json`（Raydium CPMM多腿、Raydium CLMM/Orca/Meteora跨协议、失败PumpSwap路由）；[原上游测试](https://github.com/0xfnzero/sol-parser-sdk-python/blob/cffb6c808c9b7975fc83428c0613fb4c3fa173b5/tests/test_signed_transaction_replay.py)。FnZero README声称MIT，尚需在正式分发前单独确认许可文件和依赖合规。
- 现有`raw_tx_adapter.py`继续只作历史fixture对照，不新增DEX协议解析；新增`src/solana_meme_os/sdk_upstream_replay.py`仅在隔离运行中依赖现成SDK并验签，比较RPC元数据执行成功状态、DEX leg、已提交DEX事件、所有报告的Token Account前后余额。**Token账户Owner提示不是经济控制者；保存消息签名不证明RPC执行metadata可信。**
- 专项GitHub workflow：`.github/workflows/one-shot-fnzero-signed-route-verification.yml`独立安装固定PyPI版本并从固定GitHub SHA取原样样本，无交易、无付款、无模型调用。**未取得成功的Actions证据前，这项只能标待实测**。若SDK复用通过，再选真实主网RPC当前取证样本测同交易多钱包观察及修复时间窗输入；不要将“通过上游fixture”误称长期在线监控。


- **FnZero 已真实运行通过**：[专项GitHub Actions #41317955580](https://github.com/sunshihao001/grok/actions/runs/41317955580)，固定`sol-parser-sdk-python==0.10.0`和上游源提交`cffb6c808c9b7975fc83428c0613fb4c3fa173b5`。Artifact #13088032337 真实下载回读、ZIP CRC=OK，原样签名Corpus SHA256 `b1c61a81470ffb37f4acf0f116c2d5dfc7e4adc2dd35a247b2c48956814aa073`与报告相符；所有3笔交易的Ed25519已验证。SDK从两笔**成功**交易解析共6个DEX事件（各3个route legs）；一笔**失败**PumpSwap交易保留1个route intent，但执行DEX事件=0，Token Account报告净变化=0，fee=18144 lamports。对应的账户观察分别为15/13/7条、owner提示5/6/5个；**这些绝不等于5/6/5个独立买家**。工具不做网络RPC追验或Grok调用。项目[全量离线CI #41317955519](https://github.com/sunshihao001/grok/actions/runs/41317955519) **296项通过**。
- **判定变更**：区分(1)签名交易、(2)多个DEX CPI route legs、(3)实际成功的DEX执行事件、(4)Token Account逐户净余额、(5)有证据的经济主体和协同机制。这五个观察层次绝不可用一个通用“买入事件”计数替代。下一次实务验证应使用**两笔来源独立的成功Swap及多钱包活动样本**和FnZero API复核，比较钱包级观察的完整性及事件时间、RPC可见时间，不应再次自研低级解码器。


### 2026-11-01｜Million整体只读运行验收（真实阻断，不再凭README推断）

- **固定源及可回查运行**：`Kelows/million@c89ad07caaf70773d40b45943e136eadc4f946a5`，完整API依赖隔离构建并启动：[GitHub Actions #41322677288](https://github.com/sunshihao001/grok/actions/runs/41322677288)。严格空`HELIUS_API_KEY`、`EXECUTOR=paper`、爬虫默认禁用，无钱包私钥、Webhook、转账或自动付款；先`npm ci --ignore-scripts`避免上游安装脚本副作用，再显式完成Prisma/SQLite编译启动。API在本次试验中仅绑定回环并只执行GET。
- **真实原始结果**：Artifact #13090220633（`pinned-million-no-key-readonly-smoke`，ZIP CRC和文件已核验）含`health.json`、`crawler.json`、`live-status.json`、`discovery-body.json`、`probe-result.json`及源提交SHA。健康接口正常但`heliusConfigured=false`；爬虫`enabled=false`；实时订阅`connected=false`；在已验Mint `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` 上执行原生`GET /api/discovery/token/:mint?pages=1&mode=recent&minSol=1`得到HTTP **503**，明确缺`HELIUS_API_KEY`。**零真实买家/钱包候选被验证**；运行时HTTP接口可用 ≠ 业务数据可用。
- **源码与业务取舍**：Million有原生Mint→接收Token且付出报价资产的买家候选→预览质量→扩展钱包→持续状态反馈闭环，但整个API还依赖Paper/Live交易模块，无认证的本地API与`EXECUTOR=local`切换风险使其不适合直接暴露给Grok。优先作为可选、隔离的只读发现服务，不复制它的大量交易业务代码。LiveFeed按签名唯一事件和webhook第一匹配钱包处理，有漏记同交易多钱包视角风险；不能把整个LiveFeed账本当成完整经济事实。
- **数据费用**：源码`crawler.service.ts`记载Enhanced调用按10积分计、历史发生预算计算失准；Discovery一个GET可能触发多个钱包预览请求。实际Helius 2026现行计价、免费额度及个人账户授权仍未核查，未经额度确认不得自动开爬虫、深度扫描或启用持续订阅。
- **下一验收门槛**：有隔离的数据凭据和限额后，先用Million现成`GET /discovery/token`按一个真实Mint限量获取原始买家候选，独立排除池/路由并标注历史截断；再仅选一个候选检查Funding/时间窗，记录所有网络请求及实际费用。若仍无Key，继续从已有公开链上记录验证地址语义，但**不要声称Million发现已接通**。
