# 2026-11-02｜自主研究制度收束与实际任务回归验收

> **范围**：只读知识分支PR #14；修订专家调用的现行解释、旧阶段文件在知识入口的优先关系和机器导航关键词。保留全部22个专家知识、L0–L7/D01–D12、152个研究问题、65个原参考资产与历史论证，不合并/删库/改交易；工程PR #16未改动。**通过自动化的是静态检索、制度契约和既有离线测试；真实交易、经济主体识别、Grok运行及模型长链推理质量均不在此测试之内。**

## 真实用户任务：旧/新导航输入不变，输出候选排序对照

以更新前 `knowledge-navigation.v1.json` 的真实13条路线、`project_navigator.shortlist()`字面计分公式（每命中cue加 `min(3,0.7+len(cue)/4)`）为基线。只改原导航索引的明确业务提示词、知识源路径及权威说明；`project_navigator.py`算法未改，无额外安装/供应商调用。以下是逐条实际解析原索引后得到的结果，而不是想象的LLM对话分数。

| 原始任务 | 修订前首条路由 / 主要问题 | 修订后首条路由 / 差异 | 能证明什么 |
|---|---|---|---|
| “一批多跳资金钱包到底同控，还是共用交易服务？” | `ANOMALY_TIME` 首位1.20，仅因命中“一批”；`FUNDING_ENTITY`同为1.20 | `FUNDING_ENTITY`首位6.30，匹配“多跳资金/多跳/共用交易服务”；新增原多跳审读文件 | 不再因低信息泛词把经济主体调查排在异常监控之后 |
| “OKX GMGN Bubblemaps如何复用到V0.2钱包资金报告” | `FUNDING_ENTITY`与`SOURCE_REUSE`均1.20，按ID排序导致前者先出现 | `SOURCE_REUSE`首位9.05，进入现有复用能力台账与实际API/许可证/成本审查 | 成品接入问题优先检查真实接口/费用/实现，不先发散经济理论 |
| “继续 Solana Meme 项目，原位优化现有专家、知识调用与持续推进制度，清除重复和冲突约束，保留专业知识与可靠证据，并通过实际任务检验改进效果” | `KNOWLEDGE_MANAGEMENT`首位2.40，但只指向知识主册/旧审计，没有当前活跃工作准则或真实注册表 | 首位6.30，附 `current-operating-guidance.md`、`gpt-meme-progress-current.md`、`registry.v1.json` | 制度维护能首先读取权威现行规则和正在变化的事实，而非依赖旧总结 |

这三项在 [`tests/test_project_navigator.py`](../tests/test_project_navigator.py) 已做自动回归断言：断言首要意图、原位专业知识路径/复用台账、专家是候选视角而非已调用Bot、工程分支资产的`invoked=false`及制度实际文件路径。更新只检验路由准确性，**并不声称自动执行了一位专家或真实数据调查**。

## 在同一问题上检验知识真正怎样使用（人工证据核查，非自动化LLM比较）

**问题：**“为什么多跳钱包共同出资、共签并跨群体回流，还不能证明同一控制者；下一步该查什么？”

- **直接历史来源**：Why-Solana `funder_network/code/fn_trace.py`只追最多五跳、对Hub停止并只扩展主要分支；`FN_posthoc.json`在408条有效下游首跳中记高活跃Hub收款方签名153条（含fee payer23）、其他收款方签名255条（含fee payer17）。`fn_30_analysis.py`对409原始下游路径去掉1条重复分支。它们证明作者冻结的样本存在交易授权与时间路径关系，不能证明受益所有权。
- **现有专业知识**：[L3经济主体研究§18–23](../knowledge/domain/L3-actor-economic-mechanisms-deepstudy.md)已解释Solana可分别部分签名、同质化SOL混合、公共Hub与Union-Find传递误合并、时间机会与批次重复；[Million owners源码](https://github.com/Kelows/million/blob/main/apps/api/src/analysis/owners.service.ts)有将同入场当Owner连通导致182-wallet事故的作者注释。
- **三种竞争解释**：一份资本多地址承担统一库存风险；不同客户共用托管或交易执行服务；历史上先后使用同一公共路由但并无当时联动。它们可解释部分共同地址/签名图，因此“共同签名/同源”不能被单方面升级为同控。
- **最有信息价值的下一项证据**：对事先选定的高活跃共同签名节点，观察其是否在其他Mint/不同时间段给大量与本组无关的地址提供**真实signer参与**（不仅是资金交易对手）；用GMGN历史Trader/OKX Wallet History/Bubblemaps Magic Nodes发现候选，再以少量原始Solana交易签名核对。若发现广泛外部客户，更支持公共执行服务；即使未发现，也只能提升专用资本组织候选，不能证明最终受益人。
- **当前停止边界**：没有本次授权API或RPC重放，没有真实外部客户覆盖分母、没有签名抽样、没有单一控制者真值标签，所以本例只验收“调用现有专业知识和选择下一项可区分证据”的分析质量；不宣称识别准确率改善。

## 修改、冲突裁决和实际测试结果

- **现行研究规则**：`knowledge/system/current-operating-guidance.md`和短Project指令优先。22位专家是按知识价值可选视角，允许0位；完整业务审计按重要失败机制覆盖，不强制22人会诊。旧V1 P1–P6、V2八步落库、每轮七项进度/长提示词仍作为可复用的历史方法，不能在普通任务中触发。保留原研究/来源和审核权限；只要用户目标或证据不同，可以动态重选下一步。旧方法正文保留、适用状态已在 `knowledge/system/README.md` 和 `expert-mechanism-research-method.md`原位明确。
- **已保留的安全硬约束**：真实性/时点/来源/标签与链上证据分离、只读不交易、不签名、不自动付费、不将GitHub文档/CI说成市场验证。没有修改 `filter-policy` 的发布准入标准、专家详情、研究事实或现有Bot数量。
- **自动回归**：[GitHub Actions知识分支在提交3b2996f28的运行](https://github.com/sunshihao001/grok/actions/runs/41443745112)（完整仓库`unittest discover -s tests -v`）状态`success`。该CI包括原既有测试及本轮三条新回归，用于检测将来知识索引出现类似路由回退。后续文字类制度改动的最新提交CI状态应另按提交查看，不能以旧CI代替更新后的最终验收。
- **评价限制**：这是静态导航A/B和一次真人证据链核查，没有使用旧/新两组模型的盲评或真实任务多轮可重复性检验。可以宣称“检索入口与规则冲突明显改善”，不能宣称“通用AI认知质量已量化提高”。下轮若有真实研究任务反馈，依据真实错误对比继续原位修订，无实质增量时NO_CHANGE。


## 扩展实测（2026-11-02）：12道固定任务、9道保留改写与原始证据核查

### 1. 实验规则和真实结果

- 使用同一份**固定12个复杂Meme问题**，首选领域预期在查看结果之前根据任务的中心问题定义。旧版导航索引取提交 `2e33863adf4e0687a18deae58f03240bf90df5b6`；上轮初步优化索引取原有提交 `3b2996f28f16b4d803323febdb462c4a21236ada`，本轮对照取最新知识分支。
- 精确复用当前 `project_navigator.py` 的`cue.lower() in query.lower()`、每匹配`min(3, 0.7 + cue.length/4)`及按总分下降/ID排序的逻辑；固定12题**首选意图**从最旧4/12，到上轮6/12，再到本轮12/12。本轮另有4个非该主题的负对照全部保持正确，包括产品UI、Top10池地址、原始交易解码、开发者历史。结果是**字面检索路由对固定问题的正确入口率**，不是经济事实准确率。
- 为检验是否仅对题面过拟合，另外使用**9道没有参与新增cue设计的改写题**；只2/9正确。典型失败：`"同slot五笔机器人买入是否一定属于Jito打包？"`排到`GROK_OPERATION`；`"一种代币从A的ATA移动到B的ATA，DEX并没有成交，算抛售吗？"`排到`MINT_OVERVIEW`；`"OKX统计前一千名持币者彼此转主流币的比例，是同一资金来源吗？"`排到`SOURCE_REUSE`；`"对照代码...路径条数不同如何排查重复计数？"`无匹配。
- 这批保留题没有再次靠增加同义关键词强行修成9/9。改为在**现有** `project_navigator.shortlist`输出增加`weak_literal_match`和`weak_literal_match_note`：没有词面命中、首选词面分值<3或前两候选分差<0.6时提示低辨别力，要求AI**自行**理解真实问题并审阅专业原文。该标记是信息提示、不是门禁、拒答条件、第二套Agent、模拟专家调用或语义理解能力。
- `tests/test_project_navigator.py`实际保存了10条新增主题回归＋4条负对照，以及9道保留改写题应标弱的回归。对应最新版已通过GitHub Actions `unittest discover -s tests -v`（参见本报告下方验收，提交SHA须重新核实）。**并未在旧/新两种Project指令下运行两组独立LLM**，因此没有因果证明模型认知质量提高。

### 2. 在五项高风险研究任务中实际回到专业原文，而非只看路由结果

| 固定问题 | 原来源中的可核对证据 | 专业解释/不能越级声称 | 对应专业知识 |
|---|---|---|---|
| Token移动到新钱包、没有Swap是否“已出货” | [Solana Transfer Tokens](https://solana.com/docs/tokens/basics/transfer-tokens)明确是同Mint的两个Token Account之间余额转移，不改变Mint总供应 | 转仓/托管/派发/场外结算均可能；不能将Token Transfer自身计为DEX成交，也不能因无Swap就断言不存在链下对价 | D01账户状态、D06库存及D07时序 |
| OKX `holderSameFundSourcePercent`是否等于已证明相同最终出资人 | [OKX官方Cluster Overview](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-cluster-overview)定义为Top1000持有人之间互有主流币往来的地址占比，示例还显示百分比字段的数值尺度有待实测 | 是平台行为聚合口径，不是逐级追查共同资金源，更不是共同实际受益人概率；需要源地址交易/客户背景及时间对照 | D05经济主体、D10供应商字段 |
| GMGN Bundler是不是Jito Bundle | [Jito官方](https://docs.jito.wtf/lowlatencytxnsend/)定义最多5笔交易、同slot顺序原子提交；旧[原知识专题](../knowledge/domain/meme-anomaly-discovery-state.v1.md)明确历史供应商“捆绑钱包”是标签与协议机制不同的口径 | 同slot、批量交易、GMGN标签均不能单独证明提交了某个真实Jito bundle，也不能据此确认同控 | D01交易语义、D07协调、D10字段 |
| Why-Solana 409 vs 408是否未处理重复 | [原源码`fn_30_analysis.py`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/code/fn_30_analysis.py)明示按首跳签名/primary/destination去重；`FN_INTEGRITY`仍保留4处重复读取签名 | 409→408是分析层显式减1，不能称未知统计错误；其他重复读对其他指标的影响仍需单独核查，不能说数据自检零异常 | D10完整性、D11复核 |
| 旧群体再现是否证明能跟单获利 | [原作者研究报告](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/known_group_reentry/results.md)：匹配发行规模等后无可靠新增预测改善；作者96个验证配置成本后都未产生正回报 | 群体重现是可研究结构，不等于新增可交易Alpha；且这些是原作者特定样本和成本模型，不是本项目已独立复制结果 | D08–D09收益、D11基线/OOS |

**本轮真实研究质量检查的增量**：过去导航的错误不仅是“首选标题不准”，它可能让AI把“Token转仓≈卖出”“同源比例≈同控”“供应商Bundler≈协议Bundle”“历史结构≈盈利”等误设作为起点。已通过官方协议/原来源把这四种关键**结论跃级**拆开；这证明本轮**能够给出有证据约束的正确调查问题与竞争解释**，但不是旧版/新版模型回答的随机盲评，仍不能给出“模型提升X个百分点”的结论。

### 3. 已明确保留的难题与下一次改进条件

- 固定题面12/12与独立改写2/9的落差说明纯字符串包含路由存在明显泛化弱点；不要用更多关键词为提高固定集分数无止境扩表。正确用法始终是由AI**先理解目标**，把字面路由当候选入口，必要时越过它直接审阅领域原文/源码/测试和更大范围专业来源。
- `weak_literal_match`只能提醒不应相信词面排名，**不能自动完成正确领域选择**。只有进一步在跨任务、跨表达、跨来源的受控旧/新独立模型回答中验证引用正确性、遗漏率、反证与实际执行，才可推断“模型认知质量获得普遍提升”。
- 用户希望“旧参考每个知识点理解透”，本轮没有扩大历史资产的实际已读比例；原65项覆盖状态继续以 `knowledge/system/reference-assets-reading-coverage-2026-11-02.md`为准。当前研究优先恢复相关经济机制，而非反复全量目录扫描。
- 任何有效新增认识仍按已有Dxx原位置更新；生产发布/交易/自动付款及私钥签名权限并未改变。工程PR #16、Grok运行仍独立验收。


