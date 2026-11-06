# Blix × AI 外挂大脑｜全局反向审查与优先决策 V0.1

> **日期：2026-11-06。审查基准：`sunshihao001/grok` 的 `blix` @ `d4be09440964bc28d171de8a6db11feb76a81026`。范围：只读 GitHub 源码、现有项目文档、`ai-d` Draft PR 与公开原始研究；未运行 Blix、未访问主网、未接入 Grok Bot、未执行测试、未更改业务代码。**
>
> 目的不是增加目标体系、专家或模块，而是回答一个实际问题：**用户只说简单目标，AI 是否已经考虑了实现目标不可缺少的业务、专业证据、可靠性、安全、成本和真实验收条件？** 结论：**尚未全部考虑到位；已存在能够改变方向的新反例，且 AI 自身效果尚未独立验证。**

## 一、判断标准：外挂大脑不是长报告，更不是自动接受 AI 的结论

将用户意图保留为三条同时成立的目标：
- 产品：以 **Blix 为当前主体**，尽量整套复用市场发现、Coin、Wallet、Bubble Map、数据服务与 Web UI；不重造第二套网站。
- 专业：从原始链上事实到经济动作，再到钱包群体、资金循环、库存、价格形成和**可推翻的多种经济机制**；跟单只是子领域。
- 合作：用户用口语说目标，AI 负责专业问题重述、发现未知、按需选知识、研究原产品和成熟替代、形成判断、在授权内行动、核查结果、发现新问题后修订；**重大目标和高风险外部操作归用户决策**。

真正的测试不是“生成了多少文档”，而是：**AI 有没有发现此前未发现且足以改变决定的风险？有没有减少用户需要自己做的专业设计？它的建议能否在明确失败条件下被核查？**

已查 `ai-d` 的 [目标导航](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/planning/goal-navigation-v0.1.md)、[跨领域实验记录](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/evaluation/first-cross-domain-tests.md)与[专家认知定位](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/research/expert-cognition-distillation-positioning-2026-11-06.md)。当前静态知识适用性测试和局部检索试验**不等于独立 A/B 模型提升证据**，已有文档明确承认这点。

新外部证据：
- Rabanser 等（ICML/PMLR 2026）[Towards a Science of AI Agent Reliability](https://proceedings.mlr.press/v306/rabanser26a.html)：单一任务成功率不能概括运行可靠性；应同时看一致性、鲁棒性、可预测性和安全；在两组基准上比较多个 Agent，发现能力提升未同步带来同等可靠性提升。**不证明本文方案已经可靠**。
- Zhao 等（ICML/PMLR 2026）[AMA-Bench](https://proceedings.mlr.press/v306/zhao26bs.html)：长程 Agent 记忆不仅是语义相似检索，因果与目标信息丢失会伤害任务表现；该研究的特定基准结果不能外推为本项目 AI 认知能力的实际增益。
- Solana [官方 getTokenLargestAccounts](https://solana.com/docs/rpc/http/gettokenlargestaccounts)、[getProgramAccounts](https://solana.com/docs/rpc/http/getprogramaccounts)、[RPC Commitment](https://solana.com/docs/rpc)：提供账户数量限制、Slot/Commitment 语义的原始边界，用来反证 Blix 的“持仓/群体”解读。

## 二、真正新增的五个跨层发现（优先于扩建功能）

### F1｜“资金来源没查到”可能被永久负缓存（SOURCE_READ，P0）

[server/bubblemap.js](../../server/bubblemap.js)：
- `PAGES=3`，`readFunder()` 最多读取约3,000条目标钱包签名；若没有到达可确认的最早历史，返回空字符串 `""`。
- `putF.run(wallet, "", t)` 持久化到 `bubble_funders`；`funderOf(wallet)` 只要不是 `undefined`，`traceNew()` 就不再追踪。
- 因此“历史超过追溯上限未找到”和“钱包确无可观察出资人”，在当前存储口径下都可能保存为同一个负结果。**源代码默认没有后续自动升级/重试这一类历史上限负结果的路径**；并不是独立运行故障复现。

**业务后果**：群体分析会缺少若干关键资金关联，但 UI 的“无边”容易被用户理解为“没有关系”。未来即使获得更好的历史供应商，旧空值仍可能阻断复查。

**更好判断**：不应立即重写 Bubble Map，而应首先把“找到”“已查但无来源”“历史截断”“供应商失败”“暂未查”作为不同证据语义，且历史截断应允许后续补查。

### F2｜跨源的当前 Holder 可能并非同一 Slot/确认状态（SOURCE_READ + RISK，P0）

[holderslive.js](../../server/holderslive.js) 的快照采用 `getProgramAccounts` 的 `commitment:"processed", withContext:true`，订阅亦是 `processed`；[bubblemap.js](../../server/bubblemap.js) 在后备的 `getTokenLargestAccounts` 与 `getMultipleAccounts` 用 `confirmed`；[coin.js](../../server/coin.js) 还可能结合 Jupiter、RugCheck 的供应商缓存。

现有 Bubble Map 输出只有某些来源摘要时间，**不是每条关系与持仓附加统一的观测 Slot/commitment/刷新时间**。这使多个看似同时存在的持仓、标签和关联，可能属于不同时间视图。并不证明每张图当前错误，但不能把组合结果解释为严格同步的链上快照。

**业务后果**：6/12小时群体“突然增持/减持”和跨来源异常可能由不同时间口径、延迟、断流恢复或重建引起。研究时要要求来源时刻、观测时刻、链上 Slot、确认状态与是否过时分别说明。

### F3｜“最大20个账户”不等于“最大20个经济 Owner”（SOURCE + OFFICIAL RPC，P0）

[Bubble Map 后备读取](../../server/bubblemap.js) 使用 `getTokenLargestAccounts` 再查询所有者合并；[Solana 官方](https://solana.com/docs/rpc/http/gettokenlargestaccounts) 明确返回的是**最多20个最大 Token Account**，不是最大20个 Owner。

单一 Owner 若有多个 Token Account，可占据多个名额；按后得到的20个账户汇总的 Owner 集合可能不同于真实前20个 Owner。更不等于经济实体排名，也不能作为全体 Holder 的代表性样本。

**业务后果**：头部 Holder 比例、群体持仓比例和未发现异常可能受到选择偏差。后备源应标明 `TOP_20_TOKEN_ACCOUNTS_THEN_GROUPED` 的覆盖口径，不与全量 `getProgramAccounts` 快照无条件混为一谈。

### F4｜`partial:false` 与供应量分母的含义不一致（SOURCE_READ，P0）

- [coin.js](../../server/coin.js) 的链上 Holder 快照有 `partial:false`、`genesis:false`、`trades:0`、`since:null`；Jupiter Holder 也有类似 `partial:false` 路径，均不能证明历史成本、交易对价或资金路径完整。
- [holders.js](../../server/holders.js) 的 Holder 份额使用 `knownSupply(mint) || 1e9`；[coin.js](../../server/coin.js) 内部交易账本 Holder `top10` 还存在固定 `SUPPLY=1e9` 的计算。对供应量非10亿的 Mint，这些百分比有分母不一致风险。
- Blix 的 ledger、chain live、Jupiter、RugCheck 的 Holder 结果各自有时间、来源、样本与 Pool 排除定义，不应直接“择优选一份”后丢掉其来源语义。

**业务后果**：AI 可能从一个看似精确的 `top10=30%` 得出“同群体控盘”的高置信结论，但这个数字可能并非全量 Owner、不同供应量分母、不同时间视图或未排除全部资金池。

### F5｜流与表有很多防错设计，但跨模块的事实一致性未受验收（SOURCE_READ + RISK，P0）

- HTTP/MCP/SSE 不等同三份独立事实：MCP 有18个读取工具但不覆盖 Coin 全部调查与钱包转账；MCP 响应截断还可能省略关键 Holder。
- [wallets.js](../../server/wallets.js) 的 `wallet_trades` 与 [wtrack.js](../../server/wtrack.js) 的 `wt_feed` / `wt_transfers` 的唯一键和动作模型不同；[journal.js](../../server/journal.js) 有独立的事件去重与24小时保留，K线是汇总数据。**没有一个现成统一、长期、可证明无损的经济事件账本**。
- 多动作交易、Swap+Transfer、Token Account/Owner、SOL/WSOL、跨 Mint 时间窗、RPC缺口仍然是关键的证据核查对象。不能只因为 Bubble Map 有四跳算法，就推出完整经济机制。

**业务后果**：每个页面单独看可能合理，合起来仍然可能出现重复记账、漏交易、错时间桶或错误同控判断。优先验证“跨模块事实是否一致”，而不是增加另一套算法。

## 三、被我们持续低估的“产品成功”问题：用户到底怎样完成一次调查？

用户不应需要说“检查 `holders.js`、`wtrack.js` 的字段”，也不应先理解数据库。

**代表性自然语言任务 A：**“今天有哪些值得深查的新币？”

成功输出应该包含：从哪些平台/时间窗发现多少候选、用了哪些过滤、为何升级调查、是否存在漏检、数据是否过时、对照对象的基线。仅输出 AI 评级和热门排行不是完整交付。

**任务 B：**“这个 Mint 是否有一伙钱包在接力出货？”

成功输出应该包含：与原始签名、动作、Token Account/Owner 对应的买入→转移→卖出顺序；每一步资金/库存如何改变、数据时间窗口、公共设施/正常交易竞争解释、缺失哪些历史。若无法排除其他解释，结论必须停在“可疑结构，控制关系未知”。

**任务 C：**“这群钱包在别的币上又出现了没有？”

成功输出应该包含：群体成员如何增删、哪些钱包跨币重复、同一组资金是否持续接力、有无历史失联和偏差、与普通活跃钱包群体相比是否异常。仅给出“共同买入3个币”不足够。

**任务 D：**“帮我持续盯住，异常时告诉我。”

成功输出应该包含：监控对象、来源、时间窗、阈值及其理由、连续记录/补数策略、通知去重和失败补发、停用条件、费用上限。**当Blix不可用时的正确答案是“未观察到完整数据”，不是“没有异常”。**

这四个任务穿过同一个 Blix 产品，涵盖用户体验、市场、事实、资金、群体、AI、监控、可靠性与云端承接；**它们是验收案例，不是要求立刻做四套产品或四个Bot。**

## 四、外挂大脑没想全的关键盲点与优先顺序

| 高价值盲点 | 不主动考虑会发生什么 | 现在应采取的判断 |
|---|---|---|
| **真实用户用法及结果质量** | 写了业务地图却不知道是否真正减少判断负担 | 把上面4个自然语言任务作为后续跨层验收的起点 |
| **反例驱动的数据质量** | “未找到关系”误报“无关系”；当前余额当历史完整 | 优先核查F1–F5，不扩建第二个钱包图 |
| **误报成本和信息价值** | 每次异常都召集昂贵大模型，造成噪声和费用 | 轻量规则先筛选，只有足以改变决策时才升级深度研究 |
| **覆盖、选择偏差与负证据** | 一组被选择的头部钱包被误称“全市场” | 增加样本口径/边界，而不是堆更多强结论 |
| **真实世界可用性** | Website开了但数据库停止、Bot休眠、通知丢失 | 区分“有UI”“可访问”“持续采集”“故障可恢复” |
| **授权和费用** | 局部MCP只读却绕过Supervisor或访问真实交易/API付费 | 禁止当前完整运行；将外部费用、密钥与交易权限独立审查 |
| **独立 AI 质量评价** | 规则越来越多，答案更长却更差 | 同任务对照普通AI、按需知识、旧过量知识，记录失败与用户实际负担 |
| **知识与路线过时** | PR、网站、插件功能更新后仍沿用旧判断 | 结论保留基准SHA、来源/时间和可推翻条件；只更新会改变产品路线的知识 |
| **停止研究与实际交付** | 永远停在“再深入一轮” | 静态研究解决可决策未知即可停止；授权后先做一个安全只读贯通任务并复核 |
| **经济机会的科学验证** | 把历史成功案例误当可复制优势 | 事件基线、失败样本、样本外、执行成本及因果竞争解释均要考虑 |

表格是**决策风险地图**，不是10项新项目治理制度，不默认每轮都扫描全部。当前最需要压住的是：数据不完整造成的自信错判；AI 自己评估自己的可靠性；研究没有明确停止条件。

## 五、下一步优先工作的实际选择

**当前研究许可下，优先顺序调整为：**

- **P0-事实契约（继续只读）**：以同一个 Mint 对比 Coin/Holder/Bubble Map 的供应量、时间/Slot、Owner、样本上限、来源、stale/partial；把 F1–F5 变成清楚的反例及未来测试输入。并联 Wallet/Transfer 路径，不让资金调查在接口拼接时丢掉经济动作。
- **P0-交付/停止判断（本报告已经建立）**：明确四个自然语言任务的合格/不合格条件，不因多看几篇文献而自动延长研究。下一轮只研究能改变“复用现有 vs 补历史 vs 修改数据模型 vs 增Bot接口”的证据。
- **P1-授权后才做**：封闭且真正隔离的只读运行环境、无真实钱包/模型费用、离线反例复现、一个 Mint 真实调查、断流/重启与报告的可复核端到端试验。用户**当前禁止启动和改业务代码**，不越权开始。
- **P2-长期目标**：具备证据合格时，再拓展跨 Mint 群体异常、可证伪机制研究、稳定推送、Grok Bot云端调用和Web看图。

### 何时可以说“AI外挂大脑初步可用”？

最低应在**独立且可复查的具体任务**中证明：
1. 用户只给普通语言，AI 自主发现问题和选择已有 Blix 功能，不再要求用户设计专业实现。
2. 结果有事实、来源、时间/覆盖与 UNKNOWN，不从“无记录”推断“无行为”，能主动排除竞争解释。
3. 有实际 UI/API/报告交付并回读；遇数据失效或网络断流能报告失败，不伪造“没发现”。
4. 与不添加知识的普通方案相比，在相同任务和预算上实际更准确、更省干预或更可靠；不得用文档数量或独立测试不充分的内部评分宣布胜利。
5. 关键权限、费用、运行风险可控；重大价值和交易授权没有被偷偷转化为默认自动操作。

**当前状态：** 已推进到“可指定的风险/反例/未来验收点”，**没有证明 AI 已经达到上述完整能力**。这比宣称“已经考虑周全”更符合外挂大脑的价值：主动发现自己还没有证据支持的部分。

## 六、基准和知识入口

- 当前 Blix：[项目目标](goal-map.md) / [完整源码](whole-product-cross-layer-audit-v0.1.md) / [HTTP MCP SSE](api-mcp-sse-contract-v0.1.md) / [官网](official-site-to-code-audit-v0.1.md)。
- 最新关键源码：`server/holderslive.js`、`server/holders.js`、`server/coin.js`、`server/bubblemap.js`、`server/wallets.js`、`server/wtrack.js`、`server/journal.js`。
- 外部来源为公开论文和 Solana RPC 官方文档；理论告诉我们**应该验证什么**，不自动证明本仓的实际结果。
- 原 Grok/Hermes/qb-/meme-/Why-Solana、65份参考资产、D01–D12继续在原来源位置按需引用，不因为此审查建立第二份重复知识总库。

**一句话的路线修订：AI 作为外挂大脑，下一步不该再增加“能够做什么”的概念列表，而应主动发现并修复“会让已有功能给出错误结论”的因果链；再用真实、独立的用户任务测试自己的判断，而不是让自己认证自己。**
