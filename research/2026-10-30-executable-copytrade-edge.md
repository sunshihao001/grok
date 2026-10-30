# 专家研究 R-2026-10-30-01｜从链上关联到可捕获跟单 Alpha：时间、信息增量与交易执行三重断层

**研究日期**：2026-10-30（研究设计，非交易实测）  
**定位**：原创方法论/可证伪实验协议，未独立复算市场研究；**不是已有正收益策略**。  
**目标**：最先消除“结构信号 → 盈利”推理中可测的薄弱环节，然后决定哪些方向值得花成本做 K2 真数据。

## 0. 一句话主张与范围

**研究者能事后看见的链上事实 ≠ 跟单者在决策时拿得到的信息 ≠ 跟单者能够以报价兑现的收益。**

把三道断层分开：

1. **信息时间断层**：事件在链上发生，与索引器/RPC/解码器实际向研究系统提供它的时间不同；事后链上回溯不能重建实时可见时间。
2. **预测增量断层**：同源/同控候选即使存在，也未必比市场现有价格、流动性、发币阶段、时间状态等基准更能预测未来。
3. **经济兑现断层**：预测即使成立，价格发现可能早于信号抵达；成交、滑点、抢跑/优先费、无法卖出和极端损失决定可捕获的净收益。

这三个断层必须分别设计 null model、实验对象和失败标准。不要把“发现钱包群组”误当“发现可赚钱钱包”。

## 1. 外部经验事实：支持风险判断，不支持先验定论

### 1.1 被选中警报研究的边界

第三方 `Why-Solana-Memecoins-Are-Over` 在 2026-08-21 至 09-29 的限定检测警报中有 1,657 项样本；检测器定义包含创建 slot 内至少四个 ≥5 SOL 的 snipers，研究承认约 930 小时中至少 600 小时没有监测，并存在检测未追踪的候选。该样本不能用作“所有发币”的自然分母。详见固定版本 `external-post-detection-results`。

该作者报告：检测器相对创建块的中位报警延迟约 11.8 秒；报警价格相对所研究群组早期成交价的中位倍数约 3.7。部分 TEST 子集的 15 分钟翻倍率从 31.0% 到 45.7%，但对应特定 $500、报警后 10 秒入场、模拟冲击/费用/退出模型的平均净收益约为 -23.3%。

**精确解释**：特定报警规则、市场样本、回测设定下，检测到显著结构和高于基准的收益事件概率，并未兑现正净收益。不能外推为所有 Meme 结构、所有规模、所有执行链路均负收益，更不能把假设模拟价写成实际 fills。

### 1.2 重复群组的“相关但非增量”反例

固定来源 `external-reentry-negative` 报告 G1 KNOWN 原始 15 分钟 +50% 命中率在 TRAIN/VALIDATION 相对 UNKNOWN 分别高出约 18/28 个百分点。但按当前 snipers 数、SOL、供应、溢价和市值匹配后，VALIDATION 差异 +15.9 pp 的群组置信区间 [-4.2,+32.9] 跨零。基准模型加群组的验证 log-loss 优化 -0.0023 [-0.0121,+0.0084] 也跨零。其主策略 VALIDATION 的已知群组净收益约 -17.3%，并报告试验的 96 个组合扣成本后均亏损。

**关键研究含义**：钱包复现次数可能是“当前市场状态/发行条件”的代理，而不是一条独立信息。增量检验应同时控制当前可见的规模、建池状态、支付价差和流动性，且分组应按操作者/钱包网络与时间组合进行 OOS，而不能随机打散同一操作者。

上述数字均是外部文章**所报告**，本项目 `local_replication=not_attempted`。不要将外部论文的表达移入项目作为本地复现结果，也不得搬运受版权约束的文章内容。

## 2. 官方基础事实：决策时间与资料可得时间

- Solana `getTransaction` 返回交易 `slot`，`blockTime` 可能为 `null`；需要指定 commitment/transaction version，未查到时可能返回 `null`。`blockTime` 不能替代本地收到消息的精确时间。https://solana.com/docs/rpc/http/gettransaction
- `getSignaturesForAddress` 按新到旧返回已确认签名信息，包含可空 `blockTime`；它适合回顾查询，不能凭返回签名认定当时已经可见。https://solana.com/docs/rpc/http/getsignaturesforaddress
- `logsSubscribe` 返回带 context slot 的日志通知；一个 Pubkey 的 `mentions` 订阅限制、provider/断连/重订阅与具体 commitment 均影响可观测性。https://solana.com/docs/rpc/websocket/logssubscribe
- 官方区分 `processed`、`confirmed`、`finalized`：更新鲜的信号通常承受更高回滚风险，不能混合不同 commitment 直接比较提前量。https://solana.com/docs/rpc
- Solana 官方索引指南说明 RPC 查询有限流/历史分析与解析能力约束；复杂交易的余额前后差额未必能还原中间逐笔转账。https://solana.com/docs/payments/accept-payments/indexing
- Jupiter 近期 Swap V2 文档以 `/swap/v2/order`（获取候选报价/交易组装）与 `/swap/v2/execute` 为一种路径；不提供 `taker` 时可只询价，**报价并非真实成交**。不要把旧 `/swap/v1` 的字段和计费推断自动映射到 V2。https://developers.jup.ag/docs/swap/index 和 https://developers.jup.ag/docs/swap/order-and-execute
- Jito 的优先费、tip 与交易落地行为取决于路径；不可直接设为固定常数，研究要保存目标区块、报价时刻及费用实际值。https://docs.jito.wtf/lowlatencytxnsend/

## 3. 时间证据标准：最小可复验事件账本

对每个“本可以参与”的候选信号保存两套时间：**事件发生时间**与**数据被本系统获取的时间**。在 K2 实证时至少保存：

```text
mint
tx_signature / slot / chain_commitment / source_provider
event_at_utc (如可核查的 block-time；允许 null，并标明估计误差)
provider_received_at_utc (实时 WebSocket/RPC 的实际收到时间)
parsed_at_utc (本地数据解释完成时间)
feature_available_at_utc (该特征对策略引擎实际可用的最早已记录时间)
decision_cutoff_utc (候选规则预注册的决策时间)
signal_emitted_at_utc (完成推断)
quote_requested_at_utc / quote_received_at_utc / quote_provider
quote_input_raw_units / quote_output_raw_units / route_ref
capture_mode = live_recorded | historical_backfill
source_ref / raw_hash / provider_error / missing_reason
```

标准：任何 `capture_mode=historical_backfill` 的事件，若没有当时真实采集日志证明 `feature_available_at`，即便 `blockTime<decision`，也**不能作为已证实的历史入场特征**。`available_at` 不得早于 provider 接收与解析完成，且必须不晚于决策时点。缺时间不能填 0。产生重组/回滚时保留原先 processed 观测记录与最终审计状态，严禁悄悄用 finalized 结果替换早期 live context。

当前配套 `src/solana_meme_os/asof_audit.py` 仅做事件日志的**确定性时间门槛校验**；它不能证明外部系统真实发送了这些时间，不能自动判定交易所身份、市场因果或获利。

## 4. 研究总体与单位设计

**抽样单位**：每个市场中第一次满足预注册条件的 `mint × event_type × decision_bucket`，避免同币每分钟数次报警被当独立样本。保留全部报警、未报警、失败和未覆盖候选，并记录状态：

- `IN_SCOPE_AND_OBSERVED`
- `IN_SCOPE_NO_SIGNAL`
- `OUT_OF_SCOPE_PREDEFINED`
- `SOURCE_UNAVAILABLE`
- `CENSORED_OUTCOME`
- `ROUTE_UNAVAILABLE`

**分母**：来自预先固定的市场 universe（如选定发行平台的一段连续时窗），不能只用检测器挑出的成功币。记录 WebSocket 断连、RPC 429/403、索引器缺失、交易无法解析、未创建可交易路由等缺口。缺失通常并非随机，不能把未观测当“信号为假”。

**防泄漏分组**：时间顺序外，加钱包/非 hub 资金簇/操作群组分组，重复操作群组不得跨训练与保留测试集合伪造独立性。测试时间段在特征、阈值、成本假设、买卖规则定稿前冻结。

## 5. 四个可证伪但未证明有效的研究方向

### H-A｜可见时点价格吸收（优先级 P0）

**命题**：对已知钱包/资金群组，原始行为从 `event` 到 `available` 期间被市场价格吸收的幅度，解释了为什么明显结构和高峰值不转化为跟单净利。

- 指标：按实际收到日志的相对时间对齐 `event → provider → parsed → decision → quote`，测量价格变化、价差、买卖路由可得率及净收益；按 provider、commitment、发布平台、初始流动性分层。
- 比较：当时可获得的无钱包信息基准、同流动性/时间/市值配对、延迟分桶；增量看 `Δlogloss / 净收益差`，不能只比较 MFE。
- 反证：若可见性经实测延迟后仍能稳定在不同群组/时期带来正净经济增量，则原假设（优势被消耗）被削弱。
- 停止：连续可重现区间中“当时没有该数据”或“无双侧有效路线”应停止对该分支做买入策略优化；研究记录保留。

### H-B｜群组退出后的**独立承接**（P1，新机制假设）

**命题**：从共同资金群组离场，转为新的非关联资本吸收其供给的过程，可能在**后于第一轮操作者利润兑现的时段**出现独立可观察的结构。它不必依赖复制早期 group entry。

- 可视化量：预先指定的一段时间内，已识别的同源资金簇净卖出、非关联买方净吸收、可卖池深度与价格恢复。
- 关键护栏：只能以当前时点已经确认的退出/承接作为特征，不能用事后高点/全程结束位置给“阶段”命名。聚类 CEX 共享服务与重复市场买入必须排除。
- 负对照：看似承接但实际为同一资金簇换地址、同样流动性但无承接、承接有且继续阴跌。
- 失败条件：独立资金参与度无法在当时区分，或模式仅在未来标签下成立，或出场流动性不足。

### H-C｜跨币资金再次部署的前置信息（P1）

**命题**：反复使用的非公共资金者/钱包组在前一币退出后重新集结，会提供下一事件的时间信息，但在下一 mint 尚未被识别前**不能凭资金回流选定要买的币**。

- 分离两个任务：预测“何时可能再次出现一场行动”（活动过程）和预测“下一枚具体 mint 的未来净收益”（可交易标的）；
- 前者可以是运营预警/研究调度价值，不能混成后者；直到 mint 与群组关联在实时可见信息中成立，策略才能生成标的。
- 反证：匹配重复交易服务、普通 CEX 提现周期与市场总体热度，若不超出基准则不具独立预测增量。

### H-D｜风险排除比收益预测更有价值？（P1）

**命题**：即使结构信号无法产生正净期望，某些独立风险特征可以减少尾部损失或避免明显不可执行的交易；可能比追求 2x 命中率更稳定。

- 必须用相同资金预算、机会总体和覆盖率比较“无过滤/风险过滤/简单流动性基准”，计算机会成本及漏报。
- **注意**：过滤负收益策略不代表过滤后就有正收益。仅可报告回撤、不可成交率、机会覆盖、净收益等相互独立的指标。
- 反证：相对简单深度/年龄/流动性门槛无增量，或仅因为交易减少导致总亏损减少。

## 6. 实验顺序：先否定不可能，后做复杂研究

### Stage 0：概念审计（当前完成）
限定问题、来源、研究边界、时间字段、四个新/待检验假设、负例与停止条件；没有真实市场结果。

### Stage 1：K2 实时观测可得性（未执行）
B02 在授权只读来源上采集连续 24–72 小时的小规模观察窗口（该窗口仅为**工程试运行建议**，不能代替显著性或完整市场样本要求），记录 coverage、时钟偏差、错误和 commitment 差异；对同一 raw 交易双源解析，明确买入/卖出/手续费 token decimals 与原始单位。此处不需要任何订单或私钥。

**前置硬门槛**：来源覆盖与事件时间有效性经审阅。当前 `gmgn_collect.py` 的 normalized metrics 仍为空，不能充作实时可交易报价。

### Stage 2：负对照与选择偏差检查（未执行）
B03 确定 funding graph 的 CEX/HUB 排除，B05 制作同频时段/相似规模的非信号样本与无法观察负例。冻结原始事件、样本入选算法、测量缺失。

### Stage 3：F4 增量验证（未执行）
B04 固定 target/baseline/time split，独立 B06 检查 wallet-group leakage、先筛后验和多重检验，报告 incremental PR-AUC/log-loss/calibration 与统计功效。不要借用其他论文的显著性作为本项目显著性。

### Stage 4：F5 经济兑现（未执行）
对于 F4 合格候选，按每笔 `entry_quote/exit_quote` 的时点、amount、路由可得性、成本和退出失败记录计算净收益分布；多仓位、延迟、流动性变化、尾部压力测试。用“只询价”的 paper quotes 不能声称可用相同成交价真实落地。

### Stage 5：独立复验与发布提议（未执行）
B05/B06 对独立数据复跑，记录失效/滚动漂移。只有经人工审阅冻结的只读观察规则才可交给 B07；Phase 1 绝不实盘交易。

## 7. 分阶段止损与信息价值决策

推荐先做 H-A（时间可见性），并以它作为所有策略的必要测量基础：

- 如果数据从来无法按时获得：先研究信息渠道，不做收益预测回测。
- 如果能获得，但可执行交易从不存在：保留结构研究价值，停止该路由的盈利宣称。
- 如果能交易但没有 F4 增量：H-A 或 H-C 不能自动升级，转检 H-B/H-D 等互补机制。
- 如果发现预测增量但经济为负：保留其市场解释价值，研究风险/执行约束是否可改善；**不得通过试验后参数挑选写盈利结论**。
- 如果 OOS 含独立 group 验证后具有稳健正净收益：再提出严格 paper-only 规则候选，不能因此让 B07 直接自动升级。

## 8. 角色分工与可交接成果

| Bot | 负责 | 输出证据 |
|---|---|---|
| B01 | 界定 H-A–H-D 目标/样本/版本并控制研究预算 | 预注册研究问题、样本/时间冻结记录 |
| B02 | RPC/GMGN 双源、原始签名、provider 收到时间、解码与费用/报价来源 | immutable raw + UTC 可见性日志、错误/覆盖账本 |
| B03 | 非公共 funding graph、群组退出/承接/再部署候选及负对照 | 图结构证据+hub排除/未识别项 |
| B04 | F4 预测增量与 F5 成本执行模型 | 预注册分析脚本、样本外与净收益分布 |
| B05 | 攻击时点、抽样偏差、替代解释和报价与 fill 混淆 | 不依赖 B04 评语的反证报告 |
| B06 | 盲测、不同 group/time replay、可重现计算、失败注入 | 可再现 QA 和候选发布前审查 |
| B07 | 只能在人工批准后读取 frozen paper rules | 只读监控，不参与研究规则生成 |

## 9. 下一轮精准问题（本轮尚无答案）

1. 对任意订阅到的 SOL Meme launch，实际可见的最小时间下界是多少？依赖 provider/commitment 吗？
2. 有多少目标 mint 在结构成立时**买入和卖出双侧路由皆可获取**？
3. 动态动态 fee/tip、交易拥塞和 market depth 是否随信号强弱上升（内生成本）？
4. 是否存在“第二阶段独立承接”可被**当时**区别于操作者换地址/虚假交易？
5. 在覆盖同样信号数量和总风险预算时，风险过滤是否在 OOS 降低尾部损失而非仅减少交易？

这些问题将作为后续研究 backlog，不假设任何问题已经得到验证。

## 10. 知识引用与证据状态

**内部固定来源（K1 文档指针，不是已经复现）**：
- `external-post-detection-results` → `sunshihao001/Why-Solana-Memecoins-Are-Over` commit `9a7ad51d56328e91e67e3f531d6744307d0ee68b`, `post_detection_edge/results.md`。
- `external-reentry-negative` → 同 commit，`known_group_reentry/results.md`。
- `time-safe-features` → 同 commit，`post_detection_forensics/feature_dictionary.md`。
- `meme-falsification-experiment` → `sunshihao001/meme-` commit `5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a`, `09_规则与回测/反证实验设计_v0.1.md`。
- `meme-multistrategy-direction` → 同 commit，`docs/project_ai_context/12_DIRECTION_SHIFT_MULTI_AGENT.md`。

**外部最新权威来源（未纳入 K1 固定提交，访问时仍需检查版本）**：Solana RPC, Indexing 和 Jupiter Swap V2/Jito 官方文档 URL 见 §2。第三方版权分析只保留短数据性摘要并引用原文，不拷贝报告长段落。

**研究结论状态**：`proposed`、`local_replication=not_attempted`、`market_evidence=not_evaluated`。本报告中所有假设都是候选研究设计，不是做多/做空建议。  
