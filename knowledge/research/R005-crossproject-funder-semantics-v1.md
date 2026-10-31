# R005｜跨项目原始源码交叉法证：钱包资金来源的“未知”如何变成误判 V1.0

**研究目标**：把“以跨项目证据扩展知识”落实为**对同一类链上事实的独立算法比较、错误机制归因与可测试的系统修正**。  
**日期**：2026-10-31；**状态**：已核对指定原始代码及官方 RPC 定义；未进行原项目全量运行、真实钱包归因或正常/异常准确率测评。  
**适用范围**：全市场 Solana Meme 钱包监控的 **M1 原始链上证据 → M2 事件时序 → M3 钱包/资金网络 → M4 正常/异常基准**；跟单不是主问题。

> **R006 重要反证更新（2026-10-31）**：本文件强调“用 System Transfer 指令校准直接 SOL 来源”是必要的，但**仅它不足以涵盖全部 SOL 流入**。官方 SPL Token `CloseAccount`（包括 Wrapped SOL 解包）可直接把 Token Account 的 lamports 给接收者；此外 LP 退出、桥和复合程序交易也可能产生正向余额变化。正确方法是**外/内指令 + Token/WSOL 账户状态 + SOL 前后余额/费用/租金的联合分解**，不是用 System Transfer 单一来源替换另一个余额差启发式。见 [R006 实例与 905 条派生流入审计](R006-sol-receipt-economic-semantics-v1.md) 和 [Solana 官方账户关闭说明](https://solana.com/docs/tokens/basics/close-account)。R005 中所有“System Transfer 确认”仅指该**直接转账子类型**。

## 1｜研究对象和来源固定

一手来源（全部使用固定提交版本）：

1. **solana-holder-clusters** — [`src/funders.ts`](https://github.com/jayrabol/solana-holder-clusters/blob/a75a72965479a7b715b041148803d8004fe25079/src/funders.ts) 与 [`src/clusters.ts`](https://github.com/jayrabol/solana-holder-clusters/blob/a75a72965479a7b715b041148803d8004fe25079/src/clusters.ts)；用于分析首次资金来源、缺失状态和下游 wallet grouping。
2. **Degen-Scanner** — [`dev_tracer.py`](https://github.com/dnafund/Degen-Scanner/blob/69a08d5589c47bdc33e9c6c2793cc0a69acdd85d/dev_tracer.py)；用于多跳资金/Token 路由、候选钱包选择与共享资金收敛。
3. **CyberLeek** — [`scripts/verify.py`](https://github.com/xorextrace/cyberleek-onchain/blob/283bec233a6c24849799da6e051e91689a0f187a/scripts/verify.py)；用于从原始已解析交易的外/内指令重算 System Program 转账。
4. 官方语义：[Solana getSignaturesForAddress](https://solana.com/docs/rpc/http/getsignaturesforaddress)（最新至最旧，可分页）及 [Solana RPC JSON Structures](https://solana.com/docs/rpc/json-structures)（交易 meta、账户余额和 innerInstructions）。**余额净减少不自动唯一指定转账发送方**。

本研究没有在当前环境重新向 Solana RPC 发送上述案例的真实交易查询；确认的是**源代码实际如何处理数据**及由这些选择导致的潜在误差链，而非已证明某钱包被误判。

## 2｜跨项目发现 A：首次资金来源“不知道”被聚类接口变为“独立”

`solana-holder-clusters/src/funders.ts` 有两个相关判断：
- `getSignaturesForAddress` 只取配置的有限历史，若返回页已满，说明不能确信碰到真正的第一笔历史；返回 `null`；
- 如果交易或 meta 无法获取，或首条交易中没有识别到正向 SOL 净变化，也返回 `null`。

源码里的谨慎做法是正确方向：拿不到就不猜。

**但下游 `src/clusters.ts` 对 `f === null` 执行 `independent.push(addr)`。** `independent` 因而混合了至少三种不同语义：
1. 真正有一个已看到的、在这批地址中独一的私人来源；
2. 首次来源根本查不出（历史不足/RPC 不可用/余额未识别等）；
3. 同一高度连接 funder 因“公共设施候选”阈值被排除，或资金金额低于 dust 门槛。

**推演**：如果统计专家将 `independent[]` 当作“普通独立交易者”，缺失数据/高连接 funder 会机械增加正常群体分母，使真实协调偏离被低估或误作正常。反过来把 `not in independent` 等同“庄家”也会误报。

这个结论的证据等级是**代码路径可证**，不是该项目在真实市场的误报率已测。

## 3｜跨项目发现 B：“净流出最大的人”不必然是转账发起者

同一 `funders.ts` 对钱包首条交易执行：
```text
received := target.postBalance - target.preBalance
funder   := argmin_i (other_account.postBalance - other_account.preBalance)
```
且筛选最低的负向变化。

这是一种可运行的**第一来源近似**。若一笔交易的某个账户同时支付多项费用/租金/其他资金，最大余额下降账户**不一定是**实际向目标钱包发送 SOL 的地址。对于有多个 System Transfer 的复合交易，正确发送者应由转账 instruction 的 `from`、`to`、原始 lamports 与执行上下文证实。

**CyberLeek 的不同做法**：`scripts/verify.py` 遍历外部与 inner instructions，只提取 `program=system`、`parsed.type=transfer` 的指令，以 `source/destination/lamports` 精确搜索，最后保留交易签名与 Slot。它也有观察范围与解析器限制，但其“谁向谁转了多少”作为事实，比“最大负余额账户就是付款方”更可验证。

**知识融合结果**：先用余额变化发现待查账户，再用 System Program 指令构造确认的 SOL 转账边。无法取得完整指令时只能写 `FUNDER_HEURISTIC_UNCONFIRMED`；不能进入“同源实证”或“同控”判断。

## 4｜跨项目发现 C：查询失败的零值不能推导真实行为

`Degen-Scanner/dev_tracer.py` 将候选买家分为前列优先与次级候选；对于次级候选，`0 < sig_count < 200` 视作值得加入的低活动钱包；对某些已经被其他途径确认持币的候选，即便 `sig_count == 0`（注释说明可由 rate limit 错误造成），也允许作为 `GPA recovered` 进入下一轮追踪。

**正确理解**：它将这些钱包作为**尚需进一步分析的持币候选**，并没有仅凭 0 确认它们没有历史。但这个语义必须穿透到后续专家；若后续误把 `sig_count==0` 当成“刚创建/几乎无历史”，会高估“新钱包群”。

知识融合应该引入 `history_query_status`：
- `COMPLETE_ENOUGH_FOR_QUESTION`：覆盖该研究问题需要的历史；
- `TRUNCATED_HISTORY`：分页/早期记录尚未取到；
- `RPC_ERROR_OR_RATE_LIMIT`：请求失败；
- `NO_RECORDED_ACTIVITY`：在明确查询条件下确实没有记录；
- `NOT_SCANNED`：根本未检查。

只有数据专家确认历史覆盖范围，钱包角色专家才能判断“新生、老钱包、低活跃”等时变角色。零交易数不应与失败的查询映射为一个值。

## 5｜正常机制反证：同一资金 Hub 如何有三种不同经济含义

比较三个仓库可以形成最小假说组：

- **H1 专属运营资金源**：某非公共资金钱包向多个新地址注资，随后这些钱包在一个或多个 Mint 中重复配合行动，并有可追溯 Token 库存和实际 SOL 回流；
- **H2 公共服务商/交易所**：该 Hub 向大量无关客户分发资产，接收者的后续行为独立；使用全市场/其他 Mint 的客户广度可反驳同控；
- **H3 混合基础设施**：运营网络与独立客户同时使用同一服务商；即使在 Hub 之下真实存在局部协同，不能把整个 Hub 的连通分量都归为同一主体。

**最低判别实验**：
1. 取得签名与 instruction-level 真实转账，区分 `confirmed` 和 `balance-delta-heuristic`；
2. 量化窗口内共同 funder、买家数量/金额，以及钱包年龄的真正历史覆盖率；
3. 把已知 CEX/公共服务商及高度连接未知源单列，**不要改记为独立钱包**；
4. 查跨 Mint 重复同组行为、共享库存接收和资金回流是否超出同活跃度正常基准；
5. 只有在上述证据基础上才推断运营组织候选；没有可验证 downstream，保留未知，不贴“庄家”确定标签。

该过程也不应直接给出买卖方向建议。共同运营网络与流动性后果是两种不同命题。

## 6｜具体落地：把专家间的未知保持为显式状态

新增只读 [`funder_evidence.py`](../../src/solana_meme_os/funder_evidence.py)，其**输入是上游已经归一化的“首次资金来源候选”**，不是原始 RPC 解码器。它给出：
- `FIRST_FUNDER_UNKNOWN`：已查但没有充分证据；
- `NOT_YET_SCANNED`：尚未查询；
- `FUNDER_HEURISTIC_UNCONFIRMED`：只有余额差启发式；
- `KNOWN_PUBLIC_INFRASTRUCTURE`：来源标签指向 CEX/桥/公共路由，标签仍需来源管理；
- `SOURCE_INFRASTRUCTURE_UNKNOWN`：虽有资金边，但不知道来源属于哪类服务；
- `HIGH_DEGREE_SOURCE_AMBIGUOUS`：高连接来源不能自动视作公共服务，更不能直接归为独立钱包；
- `DUST_EDGE_NOT_DISCRIMINATING`：很小资金边不足以单独形成聚类；
- `SHARED_PRIVATE_FUNDER_CANDIDATE`：通过上游声明的 System Transfer 指令确认来源且源标签为私人候选，多个地址共享相同来源；
- `UNIQUE_OBSERVED_FUNDER_NOT_OWNER_INDEPENDENCE`：在本观察集只有一个来源关系，仍不能证明经济主体独立。

每条 `RESOLVED` 输入必须有 `signature / source_ref / amount_lamports / trace_method / source_type`。输出不生成“真实独立钱包总数”、不校准异常概率，也不交易。历史数据/公共 Hub 的不确定性不会在跨层变成独立或操盘证据。

[11 项合成单元测试](../../tests/test_funder_evidence.py) 覆盖缺历史、分页状态、启发式来源、CEX、金额不足、高连接源、共享来源、唯一来源、非法数额、无签名和无交易授权。**测试文件已写入，但尚未在完整 Grok 仓库的 Python 容器内执行；不得宣称 11 项通过。**

## 7｜这个案例如何使知识框架真正增长

过去的知识模型只需要 `wallet → funder → cluster`；真实跨仓库阅读表明它缺少三种“不是资产但决定推断有效性”的关系：
- **可观测性与历史范围**：能否查到真实第一笔、哪一种查询失败了；
- **来源解析方法**：准确指令转账与启发式余额推断不是一个证据等级；
- **未知状态保持**：一个上游未知值即使经过多个模块和专家，也不能变成独立主体、异常分数或经济盈利。

这意味着专家图中不仅要有“数据专家向钱包专家传什么”，还要有**谁可以拒绝不合格证据、谁能撤回下游统计、什么反例真正改变经济解释**。

真正能用于市场的监控能力，是“知道哪些关系已经证实、哪些只是可检验的候选”，而不是把所有地址都强行分成正常、异常或庄家。

## 8｜证据等级与下一次验证

**已核对**：三个参考项目的固定提交源码、跨文件 null 传播、最大余额下降推断、Degen 次级候选逻辑，以及 Solana 官方的 RPC 余额、历史分页和内指令结构。

**未核对**：目标链上具体真实钱包的首次 funding 全历史、这三项算法真实误报率、官方服务商标签的准确性、市场正常样本与任何可交易收益；没有将这份代码接入 M1 RPC 实时监听。

**下次最有信息增量的真实实验**：选一批明确观察窗口内的钱包，对其首次 funds 同时跑“最大净亏账户推断”和“解码实际 System Transfer”，用真实签名计数**两者的源地址不一致率**；分开统计历史被截断、RPC rate limit 和已知公共 Hub 的比例。随后追踪这项差异是否会改变群体数量、正常分母和误报。数据未取得前不猜数字。

**方法收束**：跨项目的高级学习，不是选择哪个开源项目说得更专业，而是让不同项目的源码暴露彼此遗漏的机制，把错误传递变成可测试、可撤回的研究对象。
