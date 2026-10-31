# Solana Meme Workflow OS｜运行架构选型与实施决策 V4.0

> 日期：2026-10-31；范围：`sunshihao001/grok` 草案分支的只读全市场监控、动态专家研究、正常基准与反证回路；**并未创建 Grok Cloud Bot/接通生产流/发布告警/开仓。**  
> 这份文件是**架构决策记录 (ADR) + 可操作的实施方案**，不是新建 17 个 Bot 的承诺。  
> 机制知识基础：[`economic-mechanism-synthesis-and-judgment-v3.md`](economic-mechanism-synthesis-and-judgment-v3.md)；专家静态图：[`knowledge/expert-interaction-graph.v1.json`](../knowledge/expert-interaction-graph.v1.json)；已有 M2：[`market_observatory.py`](../src/solana_meme_os/market_observatory.py)。

## 1. 决策：分离确定性监控与开放式经济机制研究

选用 **事件驱动双循环 + 主管式研究调度 + 不变证据账与回溯**（Event-Driven Dual Loop / Evidence-First Research Manager）作为目标运行方式。

- **快循环（监控数据面）**：M1 真正 Solana/OKX 来源规范化后，M2 持续/定期执行有限时间窗的确定性事件聚合、签名去重、跨 Mint 候选发现、数据覆盖和版本监控。对外输出可复核事件和待调查名单，**不调用 17 名专家推理每笔交易**。
- **慢循环（研究控制面）**：基于用户问题、异常候选、冲突或观察缺口组成可用预算的 Case；通过 `expert_router` 查知识和专家，再由 `research_dispatch` 提出最有信息价值的**只读原始签名调查**。只在有必要时调用钱包/资金/统计/市场等专家技能。专家将事实、假说与反证附 `claim_id`、数据血缘与 `available_at`；独立 QA 不依赖主管的最终意见。
- **反向回路（反证学习面）**：下游发现原交易分类错误、历史分页不足、市场基准漂移或新程序事件后，沿 claim 依赖回溯到 M1/M2；历史版本不静默覆盖；**新规则必须在离线、盲样本、成本对照和人工审查后发布**。
- **物理运行**：初期只需要**一个最终只读监控入口 + 一个按需深研入口**，配合版本化知识 Skill/工具函数；六个开发 Bot 保持职责设计，不要求云端全部同时运行。专家是**能力/研究模块**，不是进程数。
- **AI 参与的位置**：辨别竞争机制、研究优先级、可证伪问题与多源解释；Solana 金额、签名/Slot、交易方向、真实净值、正常基准计算保持代码/数据决定，模型不能“想象”链上原始证据。

## 2. 六种可行运行方式对照与否决理由

| 方式 | 适用环节 | 对本项目的主要问题 | 决定 |
|---|---|---|---|
| 单体 Grok 提示词＋大知识包 | 小型研究示范或用户临时问题 | 内容丰富但无法持续源同步、时间状态/预算/血缘易混淆 | **保留为研究入口，不做生产架构** |
| 旧 Hermes 固定 8 层/多 Gate 流水线 | 源标准化、不可越级的基本检查 | 实体归并错误地阻断独立市场/统计；对所有事件支付同样调查成本 | **保留原始证据 Gate，否决固定解释链** |
| 17 专家全并行/多数投票 | 极少量独立审查大项目 | 大量专家引用同一供应商标签，延迟/费用上升却没有独立证据 | **否决常态全调用与投票** |
| 全自主 Agent Swarm | 研究新协议或已有成熟多工具编排 | 资源上限、解释责任、恢复/重复取数难控制，无法证实 Grok 云端支持 | **不作为初始依赖** |
| 纯确定性规则/静态阈值 | 宽泛事件扫描、单位/数据完整性 | 无法理解新机制，易被机器人/市场阶段扰动，负例检验不足 | **作为快循环基本模块** |
| **快慢双循环＋按需主管专家＋独立反证** | 大量事件、少量值得深查的行为、不断变化的市场 | 需要补 M1 真正来源、持久队列与阶段验收；目前可以先离线分步实现 | **正式推荐** |

这是基于当前系统成熟度、源事实约束与可执行性做的**工程取舍**，不是从未测过的性能分数推导。以后如果等成本实验显示单模型/纯代码已经同等有效，就应该缩减专家调度。

## 3. 数据面／控制面／审计面必须严格分开

```text
DATA PLANE (read-only)                     RESEARCH CONTROL PLANE
Solana RPC/OKX market candidate feeds       User/open discovery/market incident
      ↓ canonical instruction + time                     ↓
M1 typed ledger + source/coverage             Bounded case planner (M2 output)
      ↓                                                     ↓
M2 time-bucket / group candidates             Research manager chooses specialists
      ↓                                                     ↓
   candidate references ─────────────────→ Evidence packets & competing hypotheses
                                                  ↓
                                               Independent QA
                                                  ↓
AUDIT + KNOWLEDGE PLANE  ← claims, challenges, retractions, new motif
      ↓
Source replay / baseline recalibration / skills & code review
      ↓
Only reviewed, versioned rule promotion → Final read-only monitor
```

**研究总师的职责不是断言哪个钱包是庄家，而是保证下一个证据请求能区分竞争解释。** 固定数据质量约束与人工发布边界不交给动态语言模型推断。

### 五类触发事件

**例行扫描**：新 Mint、Swap、资金窗口、LP、Token/程序事件（目前 M2 只支持四种规范事件；LP/权限变化尚无独立解码，不能宣称已经监听）。  
**候选升级**：多个看似独立的钱包共同资金/代币归集/跨 Mint 复现；先给范围、签名、覆盖率和未验证状态，不说已证异常。  
**源错误／冲突**：账户 SOL 净变动没有找到匹配 System Transfer，但可能是 WSOL close、LP；未查到历史却被归为新钱包。此类冲突可优先于普通告警。  
**模型漂移**：机器人密度、平台路由或正常基准发生变化，旧统计阈值可能失效。  
**未知机制**：新 Program、新 Token2022 行为或预先定义不了的模式必须保存原始字段并开新研究分支，不能丢弃。

## 4. 当前最小可执行纵切片：M2 报告 → 带预算的专家调查计划

新增 [`src/solana_meme_os/research_dispatch.py`](../src/solana_meme_os/research_dispatch.py)：

1. 严格接收 M2 `schema_version=0.1`、`result_type=MULTI_WALLET_EVENT_OBSERVATORY` 和明确的非全链覆盖标记；
2. 以 **Mint、资金源、单钱包**分别组织 Case，决不在没有资产路径的情况下把同一时间的 `FUNDING_FANOUT` 与任意 Mint 的买入“叙述性合并”；
3. 将候选 Kind 路由给 `expert_router` 和源/卡片/交接规则，保留不认识的新类型给 `OPEN_DISCOVERY`，不要求预先收全所有钱包；
4. 在设置的 `max_cases/max_source_checks/max_per_case` 范围，给每个 Case 输出有限的**建议核验签名**。优先级仅是**调查工作量优先级**，不表示异常概率、市场风险或利润分数；
5. 若输入为 `fixture`，返回 `OFFLINE_SYNTHETIC_ONLY`；为 source_derived/rpc_supplied 时仍标 `SOURCE_CONFIRMATION_REQUIRED`；没有 source signature 的候选一律 `MISSING_SIGNATURES_REQUIRE_SOURCE_REPAIR`；
6. 无 M2 `decision_time_filter` 或仅仅有过滤时点均不自动确认真实预测的信息可得性；缺少基准不发布统计异常、没有报价不声称纸面收益；
7. **不自动运行专家、不执行 RPC、不更新知识规则、不推送告警、不生成交易指令**。

示例（依赖之前已存在的 `fixtures/market-observatory-synthetic.json`）：

```bash
mkdir -p .runtime
PYTHONPATH=src python -m solana_meme_os.market_observatory \
  --input fixtures/market-observatory-synthetic.json --allow-fixture \
  --output .runtime/observatory-report.json

PYTHONPATH=src python -m solana_meme_os.research_dispatch \
  --input .runtime/observatory-report.json \
  --max-cases 4 --max-source-checks 12 --max-per-case 4 \
  --output .runtime/research-plan.json
```

输出 `research-plan.json` 是计划，不是已执行结果。每个 Case 包含种类、真实签名引用、Mint 或资金源作用域、需要的专业知识、交接 ID、是否需开放发现、源确认状态、预算及调查问题。

[单元测试](../tests/test_research_dispatch.py) 针对预算/idempotence/作用域隔离/未知事件/同一个签名去重/非全链覆盖/输出不执行交易与源错误等12种情况。**现阶段测试文件已写入但不应声称在目标完整仓库跑通，须在 Grok 云环境实际执行后才能升级运行等级。**

## 5. 任务队列、调度权限与故障处理（目标设计，尚未实现）

为 Grok 云端独立运行做好接口，但不假定云环境已有 Redis、Postgres、Temporal、Celery 或持续后台进程。优先建议 **stdlib + SQLite 本地小规模持久化**；若云环境是临时/可重置文件系统，先验证磁盘持久性、退出后保存和任务触发能力，必要时改为受支持的持久工件存储，不能把不持久数据库当真。

目标 `case_task` 字段：
`case_id,event_refs,first_available_at,input_snapshot_hash,role_ids,source_checks,budget,cursor,status,attempts,created_at,updated_at,deadline,assumptions,contradictions,review_gate,algorithm_version`。

明确六个状态：`DETECTED → EVIDENCE_CHECK → HYPOTHESIS_COMPETITION → FALSIFICATION → REVIEWED → ARCHIVED`；需要资料时标 `WAITING_FOR_EVIDENCE`，源矛盾时 `SOURCE_REPAIR`，超预算则 `DEFERRED_BUDGET`。**状态是调查流程，不等于真实市场“已证实异常”状态。**

预算约束按三个维度：每日调查 Case、RPC 调用数量、LLM/专家咨询金额或 token；每个 Case 还应有最深资金跳数、期限、失败重试次数与同一来源请求去重。不能在版本没有变化时重复深查同一签名。

**状态修复与幂等**：
- 以`chain / signature / instruction-path / program / semantic event ordinal`形成原始经济事件键，避免将同交易多内指令错误合并；
- 不同供应商视为同源交易的不同陈述，做冲突审计；一旦源分类更正，沿 `depends_on_claim_ids` 提出待重算清单；
- 任何重试/中断必须保留已完成签名和 source provenance；状态不能因云电脑重启而默默重置为“没有发生事件”；
- 只读事件本身可以自动重试；钱包归属/操纵指控/纸面 alpha 的结论必须受独立反证限制；
- 手工修改规则、开放权限、主动发消息和交易均不在本阶段自动化范围内。

## 6. 不同专业任务适合不同运行组织

| 问题类型 | 正确的专家调用方式 | 可以自动做什么 | 不应自动做什么 |
|---|---|---|---|
| 普通新 Mint / 转账计数 | 单个确定性模块 | 规范化、分窗、异常候选和数据完整性 | 用模型补齐缺失交易 |
| 资金扇出 + 同 Slot 买入 | 事件→链上/资金图→统计（并行补充） | 选签名、要求源验证、匹配知识来源 | 同 Slot 直接称 bundle/同控 |
| LP/WSOL 复杂资金变动 | 链上解码与市场流动性并行，QA 驳回错误归因 | 生成归因待核清单，保留金额残差 | 净余额变化直接称外部资助/真实获利 |
| 跨 Mint 重复行为 | 资金/钱包/开发者先；统计和机制反证随后 | 在过去可见时点挖多通道 motif | 用未来再次出现的数据提前认出群 |
| 真实市场影响或收益问题 | 微观结构 + 因果 + QA；执行经济最后 | 纸面反事实与容量测试提案 | 没有报价就称正净可跟买 |
| 未知新 Program | 数据＋链上法证＋知识工程，按需引入新领域 | 保留原始事件并提出解析器升级需求 | 强迫未知事件入旧标签并用旧阈值判断 |

这样保留**专家知识的深度**，但实际运行按当前市场问题动态伸缩。

## 7. 真实执行次序（不要跳步）

**E0｜离线完成一条完整小闭环（当前）**  
在同一 M2 fixture 上得到事件窗口、候选、source-safe Case 和静态专家交接；验证预算、未知事件、跨 Mint/资金源隔离、二次执行幂等与禁止交易。当前已编写确定性计划程序与测试；生产实测仍待。

**E1｜原始来源事实补齐（首要真实工程瓶颈）**  
Solana RPC/可靠读源接入；解析 System/Token/WSOL/交易池内外指令并保存 raw meta、watermark/延迟/slot覆盖、处理时点；优先解决 R005/R006 的资金归因与 BUY/SELL 方向。M1 未完成前不声称市场全量。

**E2｜一段明确时间的可复算总体与正常基准**  
以发行年龄、交易活跃度、池深、协议、时段和观察覆盖建立正常活动对照；做公共 Hub 过滤、图 null、选样偏差和预警误报；无标注时不输出已校准异常概率。

**E3｜按需深度经济研究与独立反证**  
加入 Token 库存/收入/LP/开发者角色/跨 Mint 资金回路，建立时点冻结的 HX01–HX06 机制挑战样本。任务从有限 source checks 开始，不能无限追踪所有地址。

**E4｜云电脑持久化/调度/告警接入**  
在 Grok 云环境实测持久磁盘、可用运行时、任务触发、read-only credentials、重试和退出恢复；先挂接 Monitor 只读工作流。**不要先搭复杂 Agent 框架再找数据证明它合理。**

**E5｜纸面机会实验，独立于异常检测完成标准**  
若某机制确实在留出样本对后续行为有增量预测力，再补真实报价、交易失败/滑点/费用/退出/容量；正净值与风险范围通过后也只先 paper-only，本阶段未授权实盘。

## 8. 评价：必须让最简单的竞争方案有机会击败我们

同样数据时点、信息可得时间、RPC/LLM预算和留出发行，比较：
- `B0` 固定关键词/数量/同 Slot 规则；
- `B1` M2 仅事件和钱包关系；
- `B2` M2 + 保守源追踪/公共Hub分层；
- `B3` B2 + 正常基准/市场机制解释；
- `B4` B3 + 按需专家/主动反证/版本依赖回溯。

验收分别考核：指令分类准确率、资产守恒残差、源覆盖和误报、异常基准有效性、每种假说被证伪所需真实签名与费用、专家调度延迟、市场结果预测增量（若适用）及纸面净收益（若进入该阶段）。

**若 B4 在相同证据和预算条件下不胜 B3，专家调度器就不应为了“高认知”而保留其复杂度。**

### 外部方法（仅支撑架构取舍，不代表 Grok 已使用这些框架）

- [OpenAI Agents SDK orchestration](https://openai.github.io/openai-agents-python/multi_agent/)：代码控制与 LLM 自主调度可混合；主研究者调用专业能力和 handoff 具有不同控制权边界。
- [OpenAI Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration)：专业拆分必须提高能力隔离、工具权限或可追踪性；不应为数量而拆。
- [Apache Flink Streaming Analytics](https://nightlies.apache.org/flink/flink-docs-stable/docs/learn-flink/streaming_analytics/)：流式事件时间/晚到修订的关键条件；我们不主张初期引入完整 Flink 集群。
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)：数据血缘与专家活动的分离；可用自己的标准库/SQLite 最小实现，先验证正确性。

**决策收束：** 让实时市场扫描维持简单快速，让专家专注少数真正需要解释的未知，让证据反向修正知识与规则。不是专家越多越专业，而是每一次专家调用都能增加可核查的信息或排除一个错误机制。
