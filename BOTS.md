## V5｜从被动监控到主动发现未认识的经济机制

[经济机制生成与主动反证研究 V5](docs/economic-mechanism-discovery-charter-v5.md)优先于任何固定“庄家评分”清单。专家不通过多数投票产生新的事实。新知识由**矛盾发现→提出竞争机制→选最有判别力的原始签名/对照→结果纠错与知识版本化**形成。

R007 已将此前的 `financement` 标签按交易次数与 SOL 金额分别分析，并识别历史覆盖不完整情况下的零记录语义问题。新增 [`mechanism_discovery.py`](src/solana_meme_os/mechanism_discovery.py)作为只读研究检测器，新增 [两项机制的知识登记](knowledge/mechanism-synthesis-hypotheses.v1.json)与两组专家路由（目前共9种场景）。此检测器与实际 Grok Cloud Bot/实时 Solana RPC 仍完全分开。

## 运行架构决策 V4｜事件快循环 + 受预算约束的慢研究循环

实际选型：[双循环研究运行架构 V4](docs/dual-loop-research-runtime-architecture-v4.md)。**正式拒绝**将 17 个专业能力等同 17 个持续在线的 Bot，也拒绝用固定八层解释每笔交易。当前建议只有一个只读市场监控入口和一个按需深入研究入口；17 专家是专家 Skill/方法/程序，不是同时启动的模型进程。现有 M2 六类候选已通过 7 个可组合研究场景路由，测试在 GitHub Actions 真实运行通过。

**可执行的离线纵切片**：`market_observatory.py` 输出 M2 群体候选；`research_dispatch.py` 按 Mint+Slot、资金源+时间窗、跨 Mint 总体和钱包活动分别生成 Case，且不自动把不同来源/时间的行为归并；`expert_router.py` 返回相关知识与专家，`expert_interaction.py` 给出类型化交接。研究预算限制 Case 数/拟查签名数，并复用跨 Case 同签名以避免重复查询。**尚未部署真正 RPC 调用、云端任务队列或自动 Grok 专家执行；本阶段只产生只读调查计划**。

规则：原始金额、来源归属、余额守恒、时间可得性必须由数据/指令审计确定；竞争机制由专家研究提出，独立 QA 对其提出反证；新规则必须单独审核与冻结，不因一个深研 Case 直接改变正在运行的监控。详细验收见 `tests/test_research_dispatch.py` 与 `tests/test_dual_loop_vertical_slice.py`。

# Grok Bot 分工｜市场级监控系统（研发与最终运行）

**目标**：多专业研发 Bot 负责知识与规则工程，最终只有一个获得批准的只读 Monitor Bot 使用冻结版本。文档并未在 Grok 云端创建任何 Bot。旧版六个角色保留名称以利兼容，但职责从“GMGN 单币跟单”升级为跨 Mint 群体与市场事件。

## 专家能力与研发 Bot 的区别（新增）

[专家协作架构](docs/solana-meme-expert-knowledge-orchestration-v1.md) 定义 **17 类认知能力与 12 个专业领域**，并非要求创建 17 个 Bot。下表六种 Bot 是当前研发/部署职责的**工程分组**：Data & Event 可调用 Solana 指令专家、时序/数据法证；Wallet & Network 可调用图论/钱包/对抗分析；Market Mechanism 可调用 Token 安全、微观结构、筹码、生命周期、统计和执行经济。QA 必须拥有独立反证权，研究总师在证据冲突时调整问题而非强行给定结论。

每次先由事件类型和实际缺口启动 [动态专家路由矩阵](knowledge/expert-capability-map.v1.json) 的必要组合；纯只读 `src/solana_meme_os/expert_router.py` 可先输出专家与来源的研究建议（不是已部署的多 Bot 调度）。随后按资金/市场/正常对照的发现增加专家。一个专家可以是知识 + 算法 + 参考来源，暂时由同一个研究 Bot 调用；只有当实际工具权限、延迟、资源隔离或验证需要时，才决定拆成独立 Bot。

任何专家交接都传递**事实和来源、竞争解释、反证、未知和时间边界**。不许把上一专家的推断包装为下一专家的原始观察。

## 跨专家交接与审计的新增协议（V2）

[跨层专家网络](docs/knowledge-expert-interconnection-v2.md) 使六个研发角色可共享 17 项专业能力，而不是建立 17 个重复工作的 Bot。知识交接必须指明来源/处理活动、原始事实、推断依赖、反例、首次可得时点与接收者要做的判别性检查。

[40 条已定义交接](knowledge/expert-interaction-graph.v1.json) 区分源解码、群体、资金、正常对照、市场机制、风险/交易价值和 QA 回溯；`expert_router.py` 仅建议交接，`expert_interaction.py` 仅计算影响范围。**真实 Grok Agent Handoff、长期任务队列、自动向外发告警或批准真实交易没有实施。**

## 角色和边界

| Bot（设计角色） | 新职责 | 与历史知识的连接 |
|---|---|---|
| **1 Rule & Knowledge Architect**（原 Rule Architect） | 统一研究本体、证据/异常/风险/机会的不同 Gate、可反驳机制和规则变更 | Hermes Gate 和业务 Skill；meme- 市场理论；新市场级 Skill |
| **2 Data & Event Bot**（原 GMGN Data） | 研究 Solana RPC、OKX/GMGN 候选接口、Token/SOL 单位、事件指令与数据可得时间；输出已核对归一化事件 | qb- 原型和字段法证；真实来源说明 |
| **3 Wallet & Network Bot**（原 Wallet Structure） | 钱包角色、批量资助与买入、资金/库存图、重复组合、公共 hub 排除及跨 Mint 活动 | Hermes 钱包/Sybil/资金理论；Why 项目取证 |
| **4 Market Mechanism & Evidence Bot**（原 Evidence & Gate） | 市场阶段、流动性/库存变化、正常对照与竞争解释、风险研判、纸面经济验证；保持原来的证据否决职责 | meme- 周期/成本区；Why 反证、时间安全/净经济方法 |
| **5 QA & Falsification Bot**（原 QA/Fixture） | 构造普通/异常/错源/公开服务商负例，审查钱包计数、重复事件、时间泄漏、同 Slot≠Bundle、样本分母和测试 | 历史失败/案例、反证研究 |
| **6 Final Meme Monitor Bot**（最终只读） | 按批准的数据范围运行规范事件聚合、市场快照监控与告警，保留证据与运行状态；不自行写规则 | 已冻结并通过实际运行验证的 Skill/数据/规则 |

角色重新分工不表示原来已经存在、部署或获得六个云 Bot。研发 Bot 之间只移交研究材料与版本化程序；最终 Monitor 不应该承担开发权限。

## 每个交接材料应具备的最小事实

`question, observed_event_refs, signature_and_slot, mint/pool/wallets, time_window, source/provenance, unit_and_decimals, evidence_status, candidate_mechanisms, alternative_explanations, unknowns, negative_controls, proposed_next_readonly_check, version`

如果涉及纸面交易价值，另加信息可用时点、实际可能报价、延迟、退出、手续费、样本外检验；不能因异常直接转换成买入/卖出。

## 研究工作流与发布

1. 以事件/风险/新研究问题触发研究，不要求先提供一个 Mint。
2. Data & Event 核实原始事件和观察覆盖，再交 Wallet & Network / Market Mechanism 做并行研究。
3. QA 提交能推翻主要解释的正常案例与数据质量评审。
4. Rule & Knowledge Architect 根据源证据批准将某项结论保留为知识/待测规则/已测规则；所有交易动作保持无效。
5. Final Monitor 只读已冻结版本，记录实际数据覆盖、事件、时间与异常候选；告警不声称庄家、Jito Bundle 或收益已证实。
6. 更改真实规则需要独立审查、回归、回滚说明和人工批准，不允许运行 Bot 自动自我升级。

## 当前代码与职责映射

- `src/solana_meme_os/monitor.py`：单 Mint 规范快照差分（存在）。
- `src/solana_meme_os/market_observatory.py`：对**外部提供的**事件执行窗口统计和候选关系（存在，需真实数据验证）。
- `src/solana_meme_os/position_audit.py`：历史仓位表差额审计（子课题）。
- `src/solana_meme_os/knowledge.py`、`research.py`：知识卡匹配与按需来源索引（非独立推理模型）。
- 全市场真实流式输入、正常/异常校准和 Grok Bot 自动调度：**未实现/未验证**。

完整迁移关系见 [整合蓝图](docs/knowledge-system-integration-v1.md)，运行环境说明见 [docs/grok-setup.md](docs/grok-setup.md)。

**项目安全边界**：不访问私钥、签名、广播、下单、自动部署或未经批准对外发送通知。
