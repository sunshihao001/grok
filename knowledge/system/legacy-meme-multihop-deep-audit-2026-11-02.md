# Solana Meme 历史专业知识纵深审读｜多跳资金、经济主体与成品数据对照（2026-11-02）

> **性质**：对旧知识的来源恢复、原始方法解构与证据差异记录；不是新本体、新交易策略、新功能验收，也不自动升级参考来源的证据等级。与原 L0–L7/D01–D12 保持对应。个人 fork 的 Why-Solana 仍为 `review_only`；作者历史统计不等于本项目独立链上重放。**本文件仅宣称下文所列内容已阅读/核查，不宣称读完全仓。**逐项覆盖见 `reference-assets-reading-coverage-2026-11-02.md`。

## 一、研究核心结论

1. **多跳链上可达 ≠ 经济控制权识别**：真实签名可证明SOL转移或资产净变动；资金混合后不可能将所有后续同质化SOL唯一归回原入账；公共服务节点、多个账户权限和不同受益人使“同控”不可从连通性自动推出。
2. **信息上限由节点选择/采样/数据含义决定，不单由追踪跳数决定**。Why-Solana限定最多5跳，但其更重要的选择是7天窗口、Hub停止、只读部分后续交易、每个下游中介只继续最大转出，其余保留侧边不递归。因此增加hop未必找回隐藏小分支。
3. **现有成熟平台并非一个意义上的“聚类真值”**：OKX侧重当前Top Holder集群/交易者指标；GMGN侧重Token历史Trader、Holder、首次SOL来源和标签；Bubblemaps侧重Holder图、非Holder Magic Nodes和时间节点。聚类算法、查询边界和时间基准不同，冲突本身可能比共识更有研究价值。
4. **复用时要保持原来的市场问题**：Why-Solana关心跨群体资本归集/回流，Million关心实时订阅与关系组，Hermes/qb关心关键地址和后续追查，meme关心市场形态与反证。这些问题有联系，但不能用“庄家标签”消灭其不同经济语义。

## 二、Why-Solana 五跳专项：逐文件核查

**已读源与职责**：
- `funder_network/analysis_plan.md`：在读资金流之前冻结问题、对象和试验边界；62主要钱包来自exit研究，24个预定义“operator”是分析标签不是最终人的身份；对高活跃钱包采取抽样而非全体普查；数据限制在TEST开始之前。
- `funder_network/code/fn_00_inventory.py`：存在并列入专项源码；**本次未逐函数核验**，不称已完成。
- `funder_network/code/fn_trace.py`：`MAX_HOPS=5`、`HOP_WINDOW=7*86400`、`UP_PAGES=3`、`HUB_N=3000`、`MIN_SOL=0.1`、`HOP_TX=5`；从旧缓存优先读签名和交易；保留RPC故障/预算不可读取状态；上游从历史最早签名寻找初始资金变化，下一跳通过交易最大原生SOL净损失者构造资金源候选；下游取时间窗内部分成功交易中的SOL转出，选最大金额一条继续扩展，其他只进`side`。
- `funder_network/code/fn_10_collect.py`：先按短历史与高活跃分组；前者读部分退出后事件，后者按首次/中位/末次sweep锚点抽样；建立上下游分支，再广度迭代最多五层；到达既有可见角色/Hub/回路/预算/时间界限即停。
- `exit_destination/code/ed_trace.py`：`txflow`取SOL/WSOL与Token所有者净余额变化，并将普通SOL转移与含Token变化的交易分开；用最大正向原生余额变化给出下游接收者候选；外层及CPI指令并入但不等于每种复杂协议已做了完全经济解码。对流动性、费用、混合交易及系统转账存在适用边界。
- `funder_network/code/fn_20_build.py`：以缓存离线重建，SHA冻结表；检查交易签名重复、时间方向、地址格式、Hub误标等；禁止读取价格文件。但检查结果以JSON/输出呈现，函数末尾未看到对非空`failures`主动抛异常。
- `funder_network/code/fn_30_analysis.py`：实现资金去向A–G分类、跨operator汇合、网络连通组件、资本再循环、空模型置换和时间稳健性；不同关系（有序资本移交、共享设施、共同终点）分开报告。
- `funder_network/code/fn_40_posthoc.py`：作者见结果后追加的Hub敏感性、共同签名接收方、跨群体桥接节点分析；**事后研究不得倒称预注册预测**。
- `funder_network/results.md`、`derived/FN_FREEZE.json`、`derived/FN_INTEGRITY.json`、`derived/FN_results.json`：实际核对了研究报告与部分机器结果和原始自检记录。

**重要数据约束**：`funder_of`是最大SOL净损失账户的候选规则，不能推导唯一资本出资人；`Down.step`最多沿一条最大转出继续，不能推出未抽到的支线不存在；`retained`仅意味在有限采样内未找到后续达门槛的转出；`HUB_N`是历史活动量阈值，不能单独证明账户是CEX。

**原始材料内部待核差异（本轮发现，需优先复查）**：
- `FN_FREEZE.json`记录 `primary=62, ups=55, downs=409, reads=1058, calls=3553, fails=0`；报告与`FN_results.json:B`下游分类总计408条。**已找到差异原因**：`fn_30_analysis.py`的`Data.__init__`按`(第一跳交易签名, primary钱包, 第一跳接收钱包)`去重，并报告`dropped_duplicates=1`；源码注明重叠抽样锚点。最终统计以去重后408条为准。
- `FN_INTEGRITY.json`仍记录“duplicate signature in a wallet's reads”4个钱包及“one transfer starts two branches”1例，且`price_file_opened=false`。分支重复已被分析层显式去重；原始重复签名仍在自检记录中，尚未核验其对其他统计的影响。自检不能称零异常，但也不能将409→408误判为未处理的数据错误。
- 上述自检文件在上游 `searadacunha/Why-Solana-Memecoins-Are-Over` 当前公开仓库中也有相同记录，本轮未运行完整历史缓存，因此并未独立判定统计后果。

**作者报告、非本项目复验**：结果自述55上游链、408下游分支、13个有序跨组序列/8个桥接地址、115/119间接回流至同一作者定义的operator狙击钱包；研究也列明Hub与未观测分支的限制及“SOL同质，无法证明同一lamports”的边界。数据结果可作为机制候选，不能当经济主体或可盈利策略真值。

## 三、旧知识具体继承和需修订之处

| 原始位置 | 原来真正要解决的问题 | 本轮新增理解/修订 |
|---|---|---|
| Hermes learning/05 | 发币、曲线、毕业、池状态和候选入口 | **发行阶段**决定钱包和数据可见性；不能把所有早期转账等同毕业后DEX交易 |
| learning/06 | GMGN trending/trenches/signal三种信息入口 | 榜单发现、发行发现、交易行为触发的观察分母不同，均非自动交易理由 |
| learning/07–09 | Mint/Freeze权限、Rug不同路径、LP和滑点 | 合约风险、可卖库存和实际退出容量互相有关但不等价 |
| learning/10–12 | 角色、同源、中转、Sybil/Wash、协调 | 同源/同步可识别**结构线索**，不能唯一识别同一经济主体；继续追踪行为角色的变化 |
| learning/13–14、16 | 证据链、降级与决策Gate | 保留“发现→判断→行动”区分；未经统计校准的概率、阈值不作生产真值 |
| learning/15、design/phase1-research/00c | 从市场问题反推原始字段和组合 | 必须延伸到**最有信息价值的下一项查询**，不能停在指标生成 |
| design/phase1-research/00d | 用资金来源、成本、时间综合推断同控 | 其“三重合极高概率同一实体”缺独立校准，且特征可能共因，需改为可反证候选 |
| design/phase1-research/00e | 异常、无标签聚类、对立框架生成 | 保留开放探索，但数千字段组合易产生选择偏差和共线冗余；需独立样本与证据成本评估 |
| design/Skill4-筹码控制权状态层设计 | 库存剩余、分发、状态有效期与实体权重 | 强项是分清持续持币、转移、退出；公式中贝叶斯状态/置信度和阈值为未校准设计 |
| qb- sikk_gmgn_token_report.py | 单Mint关键地址矩阵、LP隔离、中转/派发/接收、资金与Token来源/去向 | 已有“发现→保留关系边→继续查节点”意图，但没有验收完整多跳连续调查 |
| meme- 03_语义概念、02_庄家周期 | FCZ、POC/AVWAP、深洗、死亡盘 | 价格上的“控盘成本”是竞争假设，不能代替链上实际资本成本和库存归因 |
| meme- 09_规则与回测 | 失败样本、简单基线、消融、样本外 | 任何新增多跳关联评分也必须对照“无需多跳”的简单基线，验证新增解释力 |
| Why-Solana coordination_detection | 共同出资、时间同步、重复钱包、统计空模型 | 研究样本首先按4个以上创建slot买家筛出，不可外推全市场发生率 |
| Why-Solana exit_destination/economic_mechanics | 退出、回收、重复资本使用、群体经济职能 | 资金闭环可能支持重复执行结构，但仍需区分共享执行服务与私人受益 |
| Why-Solana known_group_reentry | 旧群体再次出现与后续市场表现 | 历史识别强不等于新增可交易优势；分离研究价值和盈利结论 |
| Million owners/funding/live | Helius历史、关系候选、实时钱包订阅 | Hub/共同入场分离；前三页/50资金边等是覆盖限制；一签名多钱包可能漏视角 |
| HoldTech deep-scan/holder-overlap | 同slot候选及Holder交集 | 代码将`feePayer`作为买家候选，可能误归因；源码曾含明文第三方API凭据，禁止运行其配置或使用该凭据 |
| pumpwatch pump_watch/creator_reputation | 发行监听、重试、Creator本地历史 | `maxSupportedTransactionVersion=0`不覆盖未来v1；本地`seen_at`为采集时间，不等于链上创建时间 |

## 四、OKX、GMGN、Bubblemaps：实际数据契约与多跳边界

### OKX
- 官方 `/api/v6/dex/market/token/cluster/list`：只涉及该Token **Top300 Holder** 范围的集群，返回上限Top100集群；聚类字段含成员/持仓/成本等，**不是任意外部地址的多跳全部邻居**。
- 官方 `/api/v6/dex/market/token/cluster/overview`：`holderSameFundSourcePercent`的中文解释为前1000持仓地址中“有互相的主流币往来行为占比”；**不能光凭字段名字解释成已核实的共同最上游出资者比例**。字段口径和分母必须以接口核查。
- 官方 Holder提供`fundingSource`、`avgBuyPrice`、`realizedPnlUsd`等，可作为深挖地址种子。更早已存在`token-research`等成品工作流，实际账户权利、费用/自动x402付款隔离仍待验收。

### GMGN
- 官方 `gmgn-token`/ `gmgn-holder-analysis`列出Token Holder/Trader、`native_transfer`、`token_transfer_out`、`maker_token_tags`、`avg_cost`、已/未实现PnL、`start_holding_at`、`account_address`等。区分`address`与`account_address`，并剔除`addr_type`基础设施。
- `native_transfer`是钱包首次原生资产入账信息，不是已完成五跳上游历史扫描；`token_transfer_out`在官方技能中为最近一次转出对象，不能代表完整Token库存路径。可借助`token traders`找出当前不持仓但历史活动重要的地址。
- `gmgn-holder-analysis`明确注意“买入次数0可能是未索引，而非零成本”、供应量分母与浮动筹码分母差异及空数据不得评为无风险。这些专业失败经验应优先继承。平台的风控等级和阈值仍非本项目校准真值。

### Bubblemaps
- 官方 `bubblemaps/api-docs` 的 OpenAPI v0.3.2：`GET /v0/tokens/map/{chain}/{token_address}`可带`timestamp`、`limit`、`use_magic_nodes`、`use_time_nodes`及`return_nodes/relationships/clusters`。
- `NodesDataV0`含`top_holders`、`magic_nodes`和`time_nodes`；能发现不在主要持有人名单中的部分中介与时间关系。但它不是无限制的全链资金图，且该图由请求的Holder范围和算法决定。
- 关系的`GroupedTransferV0`结构包含`from_address`、`to_address`、`total_value`、`total_transfers`、`first_date`、`last_date`、`token_key`；**这是聚合的关系边，不在该结构直接提供逐笔signature**，需要另行补原始交易核验。
- `POST /v0/relationships/subgraph`请求显式给出2–1000个地址，并返回这些地址间关系；它并非不受限制地自动搜索全世界相关地址。若对外部Magic Node要继续探索，仍需调查扩展策略。

### 互补关系而不是标签投票
- OKX / GMGN先找到Token Holder、早期Trader、Sniper、Bundler和历史钱包候选。
- Bubblemaps增加部分非Holder中介、时间节点和静态/历史关系图。
- Why-Solana研究方法在有限预算下追查候选节点的上游/下游，并说明何时停止。
- 供应商不一致时，优先核实“观察时间、Holder/Trader分母、Token Account owner、共用服务、关系边是否逐笔可验证”，不要将多个标签简单累加成同控概率。
- 未来需深入研究Nansen、Bitquery Coinpath等真正提供多跳服务的具体接口，但不能未经权限/实测就把文档能力写成项目已拥有能力。


### 补充：成熟平台官方字段说明也有需要实际响应澄清的口径问题
- GMGN官方不同Skills对`native_transfer`嵌套字段的叙述不完全一致：`gmgn-token`在共同首次资金来源示例中使用`native_transfer.address`，`gmgn-holder-analysis`的字段表写`native_transfer.from_address`。这只是**文档/脚本口径差异**，尚不能确认当前真实JSON采用哪一种；集成时必须取得原响应并核对，不可直接复制其中任一名称。
- OKX `cluster/overview`的`top100HoldingsPercent`等在文档中标成百分比，而示例JSON为`0.68776`之类小数；不应在未核对实际响应/页面口径前决定乘以100或按已经是百分比显示。类似`holderSameFundSourcePercent`不能因其英文名便认为是“上游同源真值”。
- 这些口径差异意味着**成熟平台并不免除数据字典与真实响应验收**。它们是辅助经济事实调查的高价值来源，但在没有API授权与同Mint原始JSON时不能给出已验证准确率。

## 五、对三类关键问题的研究判定

### 多跳后哪些关系仍可识别
**通常可在完整数据窗口中核查**：每一跳有签名、区块时间、地址、资产种类的直接链上转移；特定地址两端的时间有序可达；已知钱包跨Mint反复参与；一些共享签名/权限关系。

**必须加条件**：SOL在中介地址与其他入账混合后，入出账大小或时间相似不证明同一资本单位继续移动；“看起来连通”不等于有相同受益人；从高活跃公共设施出来的资金无法仅用公开链上数据穿透其内部账簿。

### 非Holder隐藏关系如何发现
1. 除当前Holder外，同时看历史Trader、归零钱包、收到Token转移的钱包、首次资金来源与退出接收地址；必要时从双方方向展开。
2. 使用Bubblemaps Magic/Time Nodes调查Top Holder外的连接，但不将时间节点直接解释为控制权。
3. 在预算内使用多跳上游/下游；重点扩展具有“前后时序、非公共服务、重复跨Mint活动、资产库存变化”的分支，而不是总选最大金额分支。
4. 每轮保存“不在Holder内、但通过什么签名、什么时间、什么经济关系被发现”的新增地址。若供应商未提供签名，标记为待核实关系，而非事实边。

### 如何区分共同控制与共享服务
- 直接共享Hub/首次入金只是弱证据。看该地址服务的Token范围、客户范围、时间分布、是否共同签名/授权、资本是否按固定闭环归集和再部署。
- “收到资金时实际签名”可能排除一部分被动交易所入金模式，但仍可能是托管/自动执行服务；对私下控制权不作确定判决。
- 分离三种命题：共同资金来源、共同执行服务、共同最终受益；同一证据并不同时证明三者。
- 与普通交易机器人、公开发行事件、同平台其他独立钱包做负对照，避免将相似性直接转成身份概率。

## 六、覆盖缺口和下一次最有信息价值的工作

**本轮未完成**：旧qb仓库4,236文件逐一阅读（其中3,338在data及大量备份）；Why-Solana 944项中的全部测试和原始数据逐项独立重放；全部65项参考资产的深读；OKX/GMGN/Bubblemaps新账户真实授权请求；Grok云电脑多跳监控。任何“全量已学透”的表述均不成立。

**已形成的新可核查问题**：
1. 409→408已由`fn_30_analysis.py`的分析层去重解释。应复核四个重复签名钱包是否影响其他统计，检验最终去重路径与冻结表的对应关系；缺原缓存时不能声称独立重放。
2. 用同一Mint，对照OKX Holder/Cluster、GMGN历史Trader和Bubblemaps Magic Nodes的**新增地址集合**，计算不同供应商的独有地址及共同地址，并检查地址本身是否为池/公共服务。
3. 将Why-Solana的“只追最大分支”与“在同预算内追信息价值更高的非Hub分支”做方法对照；先比较新增有效关系，避免按新增地址总数评优。
4. 每项知识回填原Dxx专题时记录“旧结论→新增证据→修订理由”，不把指标数、专家数、跳数或文档量当进步。

## 七、可回溯来源
- [Why-Solana five-hop code](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/code/fn_trace.py)、[collection](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/code/fn_10_collect.py)、[integrity](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/derived/FN_INTEGRITY.json)、[freeze](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/derived/FN_FREEZE.json)
- [Hermes learning](https://github.com/sunshihao001/-/tree/main/learning)、[Hermes research](https://github.com/sunshihao001/-/tree/main/design/phase1-research)、[qb report](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)、[meme anti-falsification](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/反证实验设计_v0.1.md)
- [Million owners](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/owners.service.ts)、[HoldTech deep-scan](https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts)、[pumpwatch](https://github.com/cinder-security/pumpwatch/blob/main/code/pump_watch.py)
- [OKX cluster API](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-cluster-list)、[OKX overview](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-cluster-overview)、[GMGN skills](https://github.com/GMGNAI/gmgn-skills)、[Bubblemaps OpenAPI](https://github.com/bubblemaps/api-docs/blob/main/openapi.json)
