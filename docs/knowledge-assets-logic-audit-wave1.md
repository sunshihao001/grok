# Solana Meme 跟单｜知识资产与机制关系审计（第一轮）

**历史审计定位**：保留原有仓位和钱包审计发现；它只覆盖初步选中的资料和部分案例，并未代表系统全领域审计完成。新系统整体以 [全市场整合蓝图](knowledge-system-integration-v1.md) 和 [钱包群体研究 Skill](../skills/solana-meme-system-intelligence/SKILL.md) 为优先入口。



- 日期：2026-10-30
- 状态：WAVE1 / SOURCE-READ AUDIT / 非完整逐文件审计、非交易效力验证
- 上位规范：[Solana Meme 跟单专业认知与知识转换规范 V1.0](solana-meme-copytrade-cognition-conversion-v1.md)
- 作用：作为后续“钱包可跟随性”首个深研单元的知识入口；不是新增交易规则
- 范围：只读核对来源目录、若干关键原文、现有 Grok 知识代码和样本记录。未改规则、Bot、Routine 和主分支。

## 1. 执行判断

当前主要短板并非“知识文档太少”，而是：**机制链的中间节点没有充分证据，部分历史规则存在归因越级，真实案例与运行工具验证不足**。应将多个项目组织成因果与反证关系，而不是把文件搬进一个更大的提示词。

建议的共同知识主线：

> 地址和交易观测 → 参与者/经济实体假设 → 资金、筹码和市场结构机制 → 决策时点可得信息 → 领先性与可跟随性 → 执行成本和退出约束 → 净收益及失效归因。

此为研究导航，不要求所有假设依次填写固定步骤；新机制可以从任何环节提出，并回头修正前面的本体、术语和数据要求。

## 2. 来源资产与审计状态

| 项目 | 已核对的实际资产 | 本轮判断 | 状态 |
|---|---|---|---|
| [原 Hermes 研究项目](https://github.com/sunshihao001/-) | `learning/10.md`、`11.md`、`16-Gate决策框架理论基石.md`、`docs/trading_system_stage_layer_design_v2.md`、`design/Skill4-筹码控制权状态层设计.md` 及目录 | 已形成地址、证据、行为、状态、决策分层，具有强业务继承价值；历史的绝对归因和具体阈值需要隔离审查 | 重点原文抽样 |
| [meme- 理论库](https://github.com/sunshihao001/meme-) | `SOURCE_OF_TRUTH.md`、`03_语义概念/第一控盘区定义_v0.1.md`、`07_样本标注/`、`09_规则与回测/` | 具备语义精化、反证类别、样本与策略验证设计；价格形态的事后定义及大量待补样本影响实时适用性 | 重点原文+三份样本记录 |
| [qb- 工具原型](https://github.com/sunshihao001/qb-) | `sikk_gmgn_token_report.py`、目录中 `hermes_harness/`、`research_loop/` 与备份工具 | 保留获取原始字段、报表与钱包启发式分类经验；脚本依赖 GMGN CLI 和特定环境，且钱包标签不是身份事实 | 工具代码抽样 |
| [Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | `docs/METHODOLOGY.md`、`docs/PITFALLS.md`、`coordination_detection/results.md`、`funder_network/results.md`、`post_detection_edge/README.md`、特征字典 | 最可借鉴的是方法：先定人群与分母，再做零假设、时间审计和净收益评估；其结论仅适用于定义的研究样本 | 方法与结果原文抽样 |
| [OKX OnchainOS](https://github.com/okx/onchainos-skills) | `skills/okx-dex-market/SKILL.md` 和技能目录 | 文档披露 Token、Market、Signal、Social、Trenches 与 WebSocket 只读查询路由；并未对当前 Grok 环境完成实测或字段校准 | 工具声明已读，实际调用未验证 |
| [Grok 目标库](https://github.com/sunshihao001/grok) | `knowledge/catalog.v1.json`、`source_index.v1.json`、`knowledge/method.md`、`knowledge/legacy-audit.md`、`src/solana_meme_os/{knowledge,research}.py`、`docs/next-steps.md` | 已有 15 张概念卡、17 个来源指针和候选研究入口；本质是检索与证据输入契约，不是完整认知引擎 | 关键代码与索引核对 |

**审计覆盖说明**：上述“已读”只针对表中材料；仓库内其余文章、历史运行数据、样本、源码和参考频道仍待深入核验，不得宣称已经完整吸收。开发者追踪、Frogy 等既往提及来源尚未纳入可复现的本轮文献清单。

## 3. 当前 15 张知识卡、17 份来源索引的实际角色

**Grok 常驻知识卡的 15 个概念标识：**

`candidate-entry`、`market-lifecycle`、`token-security`、`liquidity-depth`、`wallet-roles`、`funding-graph`、`sybil-wash`、`concentration`、`deployer-history`、`gmgn-field-combinations`、`evidence-synthesis`、`research-states`、`reclaim-theory`、`gmgn-raw-prototype`、`anti-false-completion`。

这些卡片主要保存早期问题、机制候选、适用边界和原始文件指针。它们既没有证明盈利，也未覆盖钱包的可复制收益模型。当前 `knowledge.py` 对自然语言问题的处理是字面关键词计分；`research.py` 按来源条目的 `topics` 字面匹配，生成研究入口和时间约束。名称匹配不等于真正理解问题。

17 个索引条目对 Why-Solana-Memecoins-Are-Over 方法文档的覆盖较好，但并非“17 个独立交易机制”。现有 `research.py` 的 `ALLOWED_REPOS` 仅包括上述四个历史/研究来源，不包含 `okx/onchainos-skills`。**这只是索引路由边界，并不能据此断言 OKX 数据工具本身无法连接；后续需单独设计并测试数据适配层。**

## 4. 已发现的跨项目知识冲突或跳跃

以下是重要的 **待检验问题**，不是直接宣布旧结论全部错误。

| 编号 | 历史命题或冲突 | 为什么不应直接继承 | 专业转换和所需证据 |
|---|---|---|---|
| C1 | 原 Hermes 早期理论曾将极短时差买入归为机器人或内部人 | 机器人执行与内部信息优势不是同一概念；秒级阈值未经特异性验证 | 把“首买时差分布”作为事实，再结合地址生命周期、公开事件时间和随机/同类人群对照判断机制 |
| C2 | 将交易所共同出金路径推断为同一主体 | 共享基础设施和托管钱包可能形成大量虚假的关联边 | 对资金图实施 hub 识别、角色验证、路径覆盖率和其他独立证据核验 |
| C3 | 同步卖出/买入被解释为统一控制 | 同一市场事件、机器人程序、价格触发同样能产生同步 | 比较共同信息冲击下的对照钱包，检测超出基准的剩余同步 |
| C4 | 头部持仓集中度等于实际控制权 | 地址数量与经济实体不一一对应；池子、服务商和托管实体可能扭曲 | 区分地址份额、可归因经济实体库存、可自由抛售筹码和实际流动性承接 |
| C5 | “第一控盘区”需要事后上涨才能成立 | 以未来涨幅给过去状态命名会泄漏结果，不能用于当时的信号回放 | 分离“事前候选区域”与“事后结构验证”；AVWAP 锚定规则应在信号前固定 |
| C6 | 结构观察与 Gate 决策、缺数据时全部 BLOCK | 旧 Gate 文档强调决策≠结构；所有缺失都视为 MNAR 是未经验证的强假设，且与研究输出 NEED_MORE_DATA 的语义可能冲突 | 分离“当前不授权执行”与“判定为高风险资产”；对无数据记录原因、缺失机制和风险状态，再比较不同策略的漏报/误杀 |
| C7 | 组合指标比单指标更可靠 | 多指标可能只重复测量一个共同因素，无法增加独立信息 | 特征贡献与增量预测检验；必要时做消融、共因控制与样本外比较 |
| C8 | 钱包历史利润高 → 可以跟单 | 盈利地址可能更快成交、享有更低成本或属于做市/执行网络；跟单者面临滞后和退出冲击 | 定义钱包历史可复制收益而非账面利润，复现实盘可得时间及执行条件 |
| C9 | 探测到协调/异常资金 → 存在交易机会 | Why 项目的特定样本显示可检验的统计特征仍可能没有正的可交易净收益 | 研究当时可用信息、入场报价、延迟、滑点、失败成交、退出深度及未调参测试集 |
| C10 | QB/GMGN `smart_degen`、`bundler` 等标签可直接映射角色 | 平台黑箱标签与交易主体身份、意图、长期净收益不是一个层次；源字段别名和单位需校验 | 将平台值保留为 vendor_claim，独立重算可测事实；角色仅作为候选假说 |
| C11 | 离线测试通过 → Grok 已具专业研究能力 | 现有函数主要实现来源选择、缺失与时间边界，并未在真实 Grok 云端 Bot 中进行新问题的盲测 | 新场景下比较 source correctness、反证能力、未知机制发现与过度断言率 |

**新发现的特殊冲突：研究层的 UNKNOWN/NEED_MORE_DATA 不等于风险层的“可以买”或“确定不能买”。** 现阶段统一执行边界仍是不下真实订单；研究结论要根据证据区分“不知道”和“已发现明确风险”。

## 5. 真实/模拟证据的核对

### 5.1 meme- 样本库

- `07_样本标注/模拟样本状态机演练审计报告_v0.1.md` 明确标识模拟样本，不将模拟收益和状态机演练当作交易效力验证。这部分可以继承为负例设计方法。
- `样本记录/FCZ_B_0001.md` 仍是待填模板，缺少市场标识、原始交易和具体结果。
- `样本记录/FCZ_C_0001.md` 记录 TIRED 的部分 GMGN 快照并指向 `raw_refs/tired_*.json`；但 FCZ/POC/AVWAP/实盘进出及最终收益仍为 unknown。
- `样本记录/FCZ_D_0001.md` 记录 WORLDCUP 部分 GMGN 快照并指向 `raw_refs/worldcup_*.json`；但同样没有充分的结构、执行及结果证据。
- 已核实 `raw_refs/` 的上述六份 JSON 文件存在；例如 worldcup_pool 中有极小流动性、储备量及相关字段。但单一供应商 JSON 不能自动证明完整的状态链或交易结论。
- C、D 记录同时包含 `sample_source: real_pending` 与 `is_real_sample: true`。这对自动化审计存在**状态歧义**：建议采用更清楚的证据等级，例如“实际供应商快照已保存 / 交易与价格时间序列缺失 / 结论未验证”，而不是用布尔值概括“真实样本已完成”。

因此：**不能笼统说“没有任何真实数据”；准确表述是“已有若干供应商原始快照，但缺少足以检验策略与跟单可行性的时序证据和完整结果”。**

### 5.2 Why 项目的参照警示

- `coordination_detection/results.md` 在特定 1,657 条 bundle-snipe 探测告警群体里报告了异常协调；它并未证明“所有新币的共同买入都存在相同机制”。
- `docs/PITFALLS.md` 记录分母偏差、基础设施节点、时点泄漏、测量故障及不合格控制组等导致的结论变化。
- `post_detection_edge/README.md` 在其预先定义的样本、延迟与交易策略下，发现统计预测性并未转化为正净收益。这是“先验证可交易性”的方法证据，不能套用其负收益数字来判断其他市场或策略。

第三方文本保留链接、引用与独立方法分析，不复制长篇受许可限制原文。

## 6. 首轮机制关系图（作为可拓展假设，不是已证实因果图）

```text
公开事件/市场阶段 ──► 观察到的买入同步 ──► 协调执行候选假说
         │                         ▲                 │
         │                         │                 ├── 可能反证：独立机器人对同一事件响应
         │                   共享基础设施              └── 可能反证：服务商统一执行但不同经济主体
         ▼
流动性和订单环境 ──► 钱包成交/库存变化 ──► 资金与筹码机制候选
         │                                       │
         │                                 时间窗与信息领先性
         ▼                                       ▼
报价、路由、延迟、成本 ◄────────── 决策时点可取得的跟单信号
         │
         ▼
可执行进出场与净收益评估 ──► 反证/失败归因 ──► 更新上述解释或发现新机制
```

图中线条表示**研究上的可能关联**，不是对每条边都已经完成因果识别。后续任何新机制都可以新建节点并挑战当前关系。

## 7. 优先补齐的知识缺口

| 优先度 | 缺口 | 为什么重要 | 第一个可检查成果 |
|---|---|---|---|
| P0 | “钱包 / 角色 / 经济实体 / 执行服务商 / 真实出资者”的语义区分 | 跟随的是资产风险暴露，不只是链上地址标签 | 钱包本体冲突审计 + 同一地址的竞争解释 |
| P0 | 决策时点信息与观测延迟 | 事后能看到的指标不代表实时可用 | `observed_at`、`available_at`、`decision_at` 边界案例 |
| P0 | 净收益执行机制 | 成功识别的策略可能因冲击、费率或退出失败而不可复制 | 统一成本与退出可行性测试契约 |
| P0 | 样本证据状态、来源及有效性 | 误把待填样本或供应商快照当成完整真实案例 | TIRED/WORLDCUP 样本缺口核对与原始 refs 清单 |
| P1 | 资金/筹码/市场阶段的跨域机制 | 原知识较分散，缺少可区分机制的证据链 | 同源资金与筹码状态的竞争模型 |
| P1 | 原 FCZ 模型的实时定义、锚点与前视偏差 | 价格结构理论可用，但事后定义影响预测评估 | 事前/事后双定义与失败样本 |
| P1 | Grok 知识路线与 OKX 数据适配的桥接 | 当前来源索引不是行情采集器，真实能力需验证 | 单个只读查询的字段/单位/时间/错误映射审计 |
| P1 | 真实 Grok 盲测 | “能检索”与“能研究陌生场景”有差距 | 与无知识、仅提示词基准的独立案例评分 |

## 8. 下一项纵深研究：钱包可跟随性（研究问题树 V0）

**主问题：某钱包曾经盈利，为什么可能无法被跟随；在什么额外条件下其行为才可能提供可捕获优势？**

待展开的研究分支：

1. **钱包是什么：** 独立投资者、关联地址、临时执行者、交易服务商、做市节点、开发者关联方，还是未可判定？
2. **利润来自何处：** 信息时差、资本和优先级、库存转移、交易结构、反复参与同一操作、市场 beta 或幸存者偏差？
3. **跟单者何时获知：** 第一笔上链、索引器展示、供应商信号、Bot 实际获取与预定下单时点之间的差异？
4. **跟随能否复制：** 原交易者与跟随者在成交价、深度、滑点、失败率、持仓期限与退出时点上的差距？
5. **什么反证最有力：** 无关钱包同样成功、同源群体共享平台节点、原钱包已派发、收益来自内部转账或标价、跟随成本超出毛利？
6. **哪里值得探索新机制：** 非领先钱包的反向信息、亏损钱包的避险信息、结构事件后的不对称退出机会、公开信号诱导的可测行为反转等。此处只是开放研究方向，不是交易规则。

**单元第一批应交付：** 术语/本体审计、三个竞争机制、一个可测量的数据与时间契约、至少一个真实候选样本的证据缺口，以及“何时终止/降级一个解释”的标准。不为了凑齐模板而编造数据，也不在当前阶段设置盈利阈值。

## 9. 现阶段的禁止越级与完成判据

- 不把历史文档、问答关键词、供应商标签或模拟样本当成真实交易规律。
- 不直接用旧 Hermes 的业务 Skill 或 MQL5 策略生成新的可执行买入规则。
- 不将 Grok 离线功能测试、仓库文件存在或本报告生成解释为云端 Bot 已部署或已经盈利。
- 不批量移植外部知识；先做跨源研究，再选择真正能改变判断的知识。
- 下一轮审计应以新原始证据、可区分的机制关系、可执行约束及误判修正为增量，而不是靠扩大理论词典证明进展。

**第一轮完成程度：** 主要来源入口与部分关键冲突已核对、样本状态歧义已识别、机制关系及研究优先级已写出。尚未完成仓库级逐文件知识审计、真实链上重放、OKX/Grok 运行时验证；这些均保留为后续工作。

---

### 已核对的关键原文入口

- [Grok 知识检索实现](https://github.com/sunshihao001/grok/blob/main/src/solana_meme_os/knowledge.py)
- [Grok 按需来源选择](https://github.com/sunshihao001/grok/blob/main/src/solana_meme_os/research.py)
- [Grok 原历史审计](https://github.com/sunshihao001/grok/blob/main/knowledge/legacy-audit.md)
- [原 Hermes 阶段/层级设计](https://github.com/sunshihao001/-/blob/main/docs/trading_system_stage_layer_design_v2.md)
- [原 Hermes Gate 认知](https://github.com/sunshihao001/-/blob/main/learning/16-Gate%E5%86%B3%E7%AD%96%E6%A1%86%E6%9E%B6%E7%90%86%E8%AE%BA%E5%9F%BA%E7%9F%B3.md)
- [meme- 样本采集与反证计划](https://github.com/sunshihao001/meme-/blob/main/07_%E6%A0%B7%E6%9C%AC%E6%A0%87%E6%B3%A8/GMGN%E7%9C%9F%E5%AE%9E%E6%A0%B7%E6%9C%AC%E9%87%87%E9%9B%86%E6%89%A7%E8%A1%8C%E6%B8%85%E5%8D%95_v0.1.md)
- [meme- FCZ_C_0001 候选记录](https://github.com/sunshihao001/meme-/blob/main/07_%E6%A0%B7%E6%9C%AC%E6%A0%87%E6%B3%A8/%E6%A0%B7%E6%9C%AC%E8%AE%B0%E5%BD%95/FCZ_C_0001.md)
- [meme- FCZ_D_0001 候选记录](https://github.com/sunshihao001/meme-/blob/main/07_%E6%A0%B7%E6%9C%AC%E6%A0%87%E6%B3%A8/%E6%A0%B7%E6%9C%AC%E8%AE%B0%E5%BD%95/FCZ_D_0001.md)
- [QB 旧 GMGN 单币报告原型](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)
- [Why 项目研究方法](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/METHODOLOGY.md)
- [Why 项目假设失效档案](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/docs/PITFALLS.md)
- [Why 项目可交易性研究](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/post_detection_edge/README.md)
- [OKX DEX 只读技能说明](https://github.com/okx/onchainos-skills/blob/main/skills/okx-dex-market/SKILL.md)
