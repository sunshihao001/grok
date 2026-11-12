# P1–P2 专业知识全域核查、矛盾修正与能力对应（2026-11-13）

> 这是 Blix 原有知识系统的**来源—冲突—已实现能力—未验证事项**对照账，不是新专家制度或新交易产品。历史研究原文不覆盖，实施/CI状态以 [滚动建设台账](../../docs/project/build-register.md) 与 [PR #23](https://github.com/sunshihao001/grok/pull/23) 为准。本次实际检索：本仓 P1/P2 相关知识、源码及测试，Hermes、qb-、meme-、ai-d、Why-Solana、若干 GitHub 成品源码与 Solana 官方文档。**不等于逐行核验全部152历史知识单元与65参考资产，不等于真实主网或模型A/B验收。**
>
> 范围仅限当前整体目标：市场发现→单 Mint 关键钱包/资金/库存/市场机制调查→跨 Mint 群体变化→跟单可行性研究→AI 知识选择/评估。知识能合理增加调查问题，但不能改变执行权限，不能跳过数据覆盖和真实时间校验。

## 一、来源真源：从“已迁入”改为“能解决什么、何处不能用”

| 来源（原始路径） | 可吸收专业知识与代码/案例 | 必须修正的错误前提 | 归位 |
|---|---|---|---|
| [Hermes 钱包角色](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-03-wallet-roles.md) | TopHolder、Smart Money、KOL、sniper、bundler、fresh、dev、卖出方向是不同观测维度，旧 GMGN 命令是来源描述 | GMGN标签不是私钥或经济主体真值；旧付费访问条件不自动继承 | [D04/D06钱包库存](../mechanisms/wallet-roles-and-inventory.md) |
| [Hermes 钱包结构](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-04-wallet-structure.md) | 共同 `native_transfer_from`、5分钟共买、卖出比例相似与持仓集中是候选关系生成思路 | “同资助=同控”、300秒/3钱包等硬阈值未经 Blix 市场基线校准 | [D05资金组织](../mechanisms/capital-organization-and-incentives.md) |
| [Hermes 证据链](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-05-evidence-chain.md) / [旧筹码控制状态](https://github.com/sunshihao001/-/blob/main/design/Skill4-%E7%AD%B9%E7%A0%81%E6%8E%A7%E5%88%B6%E6%9D%83%E7%8A%B6%E6%80%81%E5%B1%82%E8%AE%BE%E8%AE%A1.md) | 证据链、反证、过期状态回 UNKNOWN、CEX/pool不贡献私有控制库存 | `CONTROLLED`、`DEV_EXITED`、控制得分/概率不是自动获得的链上事实 | [D11/D12验收](../cases/independent-validation-and-failure-cases.md) |
| [qb- 95钱包留存报告](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_fact/wallet_fact_report.md) / [同源组](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_fact/same_source_groups.json) | 95钱包、4同源候选组10成员；Top10 51.019219%是**被跟踪钱包余额分母**；旧“full_exit=54”与质量分1.0为原项目字段 | `data_quality_score=1.0`不保证真实RPC历史；`group_confidence=unknown` 不能改成同控概率；余额为0/“全退”不等于Swap卖出 | [D04/D06/D10](../mechanisms/wallet-roles-and-inventory.md) |
| [meme- 策略真源](https://github.com/sunshihao001/meme-/blob/main/SOURCE_OF_TRUTH.md) / [结构观察者门槛](https://github.com/sunshihao001/meme-/blob/main/specs/mql5-fcz-reclaim-model/structural_observer_vs_quant_system_gate.md) | FCZ、POC/AVWAP、Wyckoff、深洗/死亡盘、结构重新接受可作观察与反证问题 | 结构成本锚不是真实操作者成本，GMGN数据与模式形态不能自行证明有效跟单Alpha | [D03市场机制](../mechanisms/market-price-mechanism-research.md)、[D08/D09策略](../mechanisms/strategy-and-execution-economics.md) |
| [ai-d 两领域源级复核](https://github.com/sunshihao001/ai-d/blob/main/evaluation/2026-11-07-two-domain-practice-results.md) | 资料可达→源码事实→离线回归→真实运行→模型隔离A/B各有不同证据身份 | 文档存在不等于模型调用正确，静态复核不等于真实主网任务正确 | [D12认知选择](../ai/intent-knowledge-selection-and-reasoning.md) |
| [Why-Solana Dust vs Funding](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/code/r1_dust_vs_funding.py) / [本仓五跳审查](multihop-funding-evidence-audit.md) | 转账金额、手续费与后续买入能力要同时检查；Dust和大规模分发不等于有效出资 | 原项目 Dust/出资具体SOL门槛是研究场景阈值，不能用于任意费率、价格和地址角色 | [D05资金路径](../mechanisms/capital-organization-and-incentives.md) |
| [Token Finder图谱](https://github.com/Danialsafarli/token-finder/blob/master/src/intel/graph.ts) / [反误关联测试](https://github.com/Danialsafarli/token-finder/blob/master/test/intel-graph.test.ts) | `FUNDED`、`SHARED_FUNDER`、`TOKEN_TRANSFER`、`COORDINATED_ENTRY` 等边型分离，热门开盘同槽与公共设施反例 | `CROWD=8`等固定值和项目置信度须本地重校，不是普适同控规则 | [D04–D07](../mechanisms/wallet-roles-and-inventory.md) |
| [Token Finder 校准回放](https://github.com/Danialsafarli/token-finder/blob/master/src/calibration/replay.ts) | 过去被排除/被选中对象的结果、判定反转、按 `MEASURED`/`PROXY`/`UNKNOWN` 标覆盖 | 对已被保存的幸存盘回放，容易遗漏没采集到的失败 Mint；非执行价格回测不能叫可交易收益 | [D11反证](../cases/independent-validation-and-failure-cases.md) |
| [Solana Holder Analyzer](https://github.com/non-contextual/solana-holder-analyzer/blob/main/src/transfer-scan.ts) | 分层BFS、终止公共设施扩展、限额与渐进图谱 | 多跳 Token 的 gross 重复经过同一资产，不是独立新增买盘；净额视图不能替代原始事件 | [D05](../mechanisms/capital-organization-and-incentives.md) |
| [Trading Portfolio 成本代码](https://github.com/solana-foundation/trading-portfolio/blob/main/src/lib/portfolio/pnl.ts) / [成本覆盖测试](https://github.com/solana-foundation/trading-portfolio/blob/main/tests/portfolio-pnl-basis.test.ts) | 已有买入记录能解释的余额与未知成本的余额要分开；钱包归集仅按显式集合 | 转入Token没有买入成本，不得按其他交易平均摊平；同源不意味共用利润 | [D06/D08](../mechanisms/strategy-and-execution-economics.md) |
| [Google Skill Reach](https://github.com/google/skill-reach/blob/main/docs/concepts/how-it-works.md) | 评估知识/Skill是否被正确调用，术语相似并不等于模型不会选错 | 增加知识条目/关键词不等于AI判断准确率提升 | [D12](../ai/intent-knowledge-selection-and-reasoning.md) |
| [Solana RPC JSON结构](https://solana.com/docs/rpc/json-structures) / [交易指令解析](https://solana.com/docs/core/transactions/transaction-introspection) | `jsonParsed`/raw、CPI、Owner、v0 ALT，2026官方文档亦描述 **v1 transactionConfig 且v1不支持ALT** | 当前源码仅能解析特定交易和已解析指令子集，不能宣布所有交易版本已支持 | [D01基础](../foundations/solana-chain-and-market.md) |
| [Solana Token-2022费用](https://solana.com/docs/tokens/extensions/transfer-fees) / [Transfer Hook](https://solana.com/docs/tokens/extensions/transfer-hook) | 目标账户可能扣留费，Hook会触发附加CPI；原指令数额不必等于当前可动用Token | 错把 `amountRaw` 当接收者净可卖库存、重复把Hook指令当独立用户交易 | [D01/D06](../foundations/solana-chain-and-market.md) |
| [getSignaturesForAddress](https://solana.com/docs/rpc/http/getsignaturesforaddress) | 倒序签名与 `before`/`until` 游标 | 有限查询中最早可见签名≠钱包创建日；本地未见签名≠全链无交易 | [D10来源](../../docs/project/wallet-signature-discovery-v0.1.md) |

**状态声明**：上述是本轮代表性原文件及已有留存材料的源码级查阅，不是已读完所有参考仓库；未审查来源仍保持原有 `NOT_REVIEWED` / `UNVERIFIED`。商业宣传功能未获取生产源码的，不提升为已验证实现。

## 二、按旧 D01–D12 原地归位：从专业问题到当前代码证据

| 域 | 对此刻最有用的专业问题 | 代码/测试已做到 | 暂不能宣称 |
|---|---|---|---|
| **D01 协议** | Token Account vs Owner，Signature+outer/inner CPI、v0/v1、Token-2022手续费/Hook、SOL/WSOL | `server/economic-events.mjs` 原样保存RPC + 支持子集解析，`test/economic-events.test.mjs` | 全协议完整解析、复杂Swap经济归因 |
| **D02 生命周期** | 发币、建池、毕业、迁移、LP权利在不同阶段的区别 | 原Blix Coin/Discover及已迁入知识 | 当前离线图谱自动识别Creator或全生命周期 |
| **D03 微观结构** | 价格、报价、池储备、不同投资者库存/做市收益 | 原Blix行情路径与价格机制知识 | K线代理是真实滑点、价差可套利 |
| **D04 钱包角色** | 一个地址的发/收/持/卖/托管/池作用各不相同 | `server/intelligence/economic-network.mjs` 仅输出OBSERVED sender/receiver及局部卖出摘要 | 自动判私人控制者、KOL、刷量 |
| **D05 资金/关系** | 不同边类型与共享服务过滤；对同一Token多跳记录 | `facts.network.events/edges/walletFlows` 是**Token Transfer图** | 完整SOL funding graph、共同控制或真实同群体 |
| **D06 库存/成本** | Token转移总量/净变化≠当前余额/成本/可卖库存 | BigInt原始数量、签名与事件位置、未知成本标记 | 真实库存来源、成本和钱包PnL |
| **D07 群体/时序** | 新发生与本地新补查、同地址跨币重复与真正资金循环分开 | `economic-snapshot-review.mjs` 本地归档版本对比和地址重叠 | 实时监控、全部历史覆盖或同控演化 |
| **D08 跟单价值** | 原钱包盈利是否在外部可见、可报价、可成交？ | `followability-replay.mjs` 只接受明示纸面成交/信号时间 | 已验证策略超额收益或真实成交 |
| **D09 执行经济** | 费用/滑点/报价有效期/延迟/部分退出是否完整？ | 前瞻/过期quote/部分退出/费用反例测试 | 真实网络抢单/池深/手续费完整动态 |
| **D10 数据可靠性** | 供应商/本地留存覆盖、获取时点、分页与错误、同签名重数 | PR #23 SQLite原始归档、只读报告和回归测试 | 任意Mint全部历史无遗漏 |
| **D11 反证** | Dust、共享服务、空数据、重复卖出、回填、选择偏差 | 网络/快照/知识/纸面可行性的合成fixture与CI | 市场真实误报/漏报率 |
| **D12 AI使用知识** | 模型有没有选对知识、工具，并正确保留冲突？ | `local-knowledge-loader.mjs` 白名单词面选择、来源hash、撤回说明；有限AI补查 | 全152单元自动选择、真实模型独立A/B提升 |

**证据等级不得互相替换**：`SOURCE_READ`=原文已读，`AUTHOR_REPORT`=作者陈述，`CODE_INSPECTED`=代码存在，`OFFLINE_TEST`=固定反例已通过，`REAL_ARCHIVE_REVIEW`=已复核指定真实留存数据，`LIVE_READ_ONLY`=有授权环境真实联网验收，`HYPOTHESIS`=待区分解释，`UNKNOWN`=尚不可识别。当前 PR #23 的新 P1/P2 是离线候选，**没有**实盘数据正确率证明。

## 三、跨项目冲突：旧结论应怎样修正

1. **同源钱包不自动等于同一个人**：Hermes 的共同 funder 只能先作为候选，必须区分直接SOL、公共交易所/路由/程序、Dust与可实际支付下一次买入的金额。不能复制项目固定阈值。
2. **Fee Payer 不自动等于 Funder**：交易费承担方与直接转账证据分离；Blix `bubble-funding-evidence.mjs` 的现有回归优先。
3. **同Slot/同时间买入不等于 Jito Bundle 或共同控制**：拥挤的热门发行可能产生同样现象；供方标签、真实Bundle、共同事件是三种不同对象。
4. **Token Transfer 不等于 Swap卖出或投资者退出**：接收者晚些出现卖出摘要，不证明出售的就是刚转入的Token；旧 qb- 的 `full_exit` 也要防转仓。
5. **Top10集中度先给分母**：qb- 51.019219%是被跟踪钱包的余额占比，不是总供应量占比；池与Token Account/Owner必须剔分。
6. **本地有交易记录不等于该地址为真人钱包**：Mint-first 优先级只是候选排序，池/公共基础设施也可能有交易摘要。
7. **多跳 gross 不等于独立资金流入**：同一Token可经A→B→C被重复转出；需要逐笔、净变化、余额与实际对价分别报告。
8. **净额图不是交易历史**：sig+outer_i+inner_i、账户角色、raw Token数量必须留存；BigInt数额不能用浮点粗算。
9. **Token-2022 transfer raw != 实际可卖入账数量**：withheld fee与Hook可改变可用余额与CPI，必须独立审查。
10. **同钱包出现在两个Mint ≠ 卖掉A得到的钱买了B**：跨Mint地址重叠不证明资金溯源、经济控制或盈利。
11. **历史归档“新增可见”不是新链上活动**：来源回补/抓取窗口/样本排名差异可能改变本地输出，同一事件字段更正另列。
12. **最早可见签名≠钱包年龄**：分页上限、历史空缺与RPC索引能力可造成看似“新钱包”。
13. **卖出收入≠已实现收益**：未知的转入Token成本不允许人为摊入已知成本；同源更不是共用利润账户。
14. **领先钱包盈利≠后来者可复制**：链上事件时、信号最初可见时、用户能拿到有效报价时、真实成交时独立；离线回放只在合格纸面收据下产生情景算术。
15. **回测正收益≠样本外Alpha**：必须纳入未选中的币、失败/归零币、不可成交与滑点，冻结事前筛选和观察范围，不能事后追认。
16. **知识库包含某结论≠模型应用正确**：词面检索源可能漏掉反例或重复；需按真实任务测“应该调用/不应调用/误调用”，不靠文本长度。
17. **RED-COHORT历史定量结论不得引用作证据**：本仓原始文献审查记录 v4 撤回早期买家/群体研究的数值结果，旧数值不用于群体获利归因。
18. **生产源码/README≠完整市场验证**：外部真实代码只提供可借鉴实现，阈值、统计和其作者市场结论均须独立对照。
19. **GitHub CI全绿≠已完成主网资金图**：当前仅证明特定离线回归及构建通过，受限真实模型、Coin页面直接调用、真实全历史、动态监控仍未验。

## 四、四条完整业务问题怎样调用这些知识

### A. Mint → 钱包 → 库存/出货候选
先读取 [D01链上](../foundations/solana-chain-and-market.md)、[D04钱包](../mechanisms/wallet-roles-and-inventory.md) 及实际原始签名；`npm run inspect:network-offline -- --db EXISTING.sqlite --mint MINT` 输出已经捕获的转入转出、地址角色和未知。补查同钱包相关的真实 Swap/LP/池费才可能解释真实卖出与库存；当前不知道的成本、私人控制、完整历史保留 UNKNOWN。

### B. 多跳资金 → 跨 Mint 群体
先区分 Token 转移图、直接SOL资金边、shared funder假说、同槽普通共因。用两份Mint的本地归档只能报告重合地址和有限关系；不能据此推断共同操作者/跨币资金继承。下一条应核资金来源可行性、公共基础设施、真实账户类型与时间覆盖。

### C. 6/12小时转账异动 → 前兆研究
从旧知识提出库存准备/做市/派发/市场普通活跃度/回补四种竞争解释；`economic-snapshot-review.mjs` 只输出本地“新可见、样本消失、旧数据更正”。要验证市场前兆，必须包括未上涨Mint、当时能看到的原始事件、价格/LP变化与可执行成本。

### D. 关键钱包 → 可跟单性
参考 [D08/D09](../mechanisms/strategy-and-execution-economics.md) 和旧meme-观察者门槛；`npm run audit:followability-offline -- --input PAPER_RECEIPTS.json` 只评估用户已提供的纸面收据是否有前瞻、过期报价、不完整退出、缺费用等问题。可计算也只是 `PAPER_SCENARIO_CALCULATED_NOT_LIVE`；未在独立样本验证收益。

## 五、哪些知识已经真正变成程序，哪些没有

| 认识 | 当前现有可检验实现 | 仍不完成 |
|---|---|---|
| Token指令与同笔CPI去重 | `economic-events.mjs`、`economic-network.mjs`、网络专项测试 | 不支持所有程序/Token-2022语义 |
| 原始 Token 总流、净转移与零成本假象 | `facts.network`，金额用BigInt、未知库存/PnL | 未计算实际可卖库存/已实现收益 |
| 接收钱包卖出摘要去重 | 相同卖出签名/跨币线索在显示计数中去重 | 无法把具体卖出与接收库存严格配对 |
| 历史回补vs真实事件 | `economic-snapshot-review.mjs` 分类新可见/丢出样本/修订 | 未上线自动监控或告警 |
| 相同钱包跨 Mint | 仅 bounded 地址重合候选 | 不是SOL路径或群体控制权 |
| 知识按需选择 | `local-knowledge-loader.mjs` 选本地研究片段、留来源与撤回警示 | 目前仅部分专题、词面启发式，无真实模型A/B |
| 跟单前瞻/报价/成本 | `followability-replay.mjs` 离线纸面执行核查 | 未接真实报价/持仓重构/样本外策略 |
| 产品可运行入口 | `scripts/inspect-economic-network.mjs` 与 `audit-followability-offline.mjs` 本地离线只读 | 尚未在Coin页实时执行、授权模型或持续在线运行 |

## 六、下一轮证据与停止条件

- **优先核实真实Mint**：原始 v1/v0/CPI、Token-2022、Owner/ATA、SOL/WSOL与Swap/LP是否完整；失败先纠交易解析，不以AI文本覆盖。
- **同输入比较钱包图**：Blix旧 BubbleMap 与新 Token Transfer投影在池/路由/公共设施上的误联和漏联，确认每条关系所用证据、覆盖与排除条件。
- **历史库存/PnL**：先取得可核对的Token转入来源、实际卖出、成本基础覆盖，才能计算经济主体与跟随者的差别。
- **知识选择真实 A/B**：固定相同自然语言问题、Mint归档、模型和预算，对比无知识/当前词面路由/更优路由；测证据正确、误引旧研究、补查效率、费用和停止条件。没有收益不能用“知识更多”硬说提升。
- **继续覆盖未核项目**：65参考资产、152单元中未逐一核查的仍保留未审；只有新资料改变事实、判断、实现或失败测试时再升级，而不是为了覆盖率无限加文件。

**总裁决**：Blix只有一个产品主体、一个现有SQLite经济证据归档和现有专业知识树。来源目录继续保留历史，代码与测试决定已经落地的范围；AI检索不能把旧理论变成已证事实，也不能因为尚缺主网条件就否认当前可检验的离线建设。
