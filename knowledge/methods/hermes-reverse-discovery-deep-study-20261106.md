# Hermes逆向发现 × qb事实证据 × meme反证：跨学科认知深化（V0.3）

> 2026-11-06；Blix源码基准 63a3df55e38ff27b16723f994e298de3b30885b7。这是**原始研究阅读、跨项目推理、业务推演**，不是市场实证、Blix代码变更、Grok Bot已经学会或实际交易验证。继续沿用[全域参考研究](../references/source-knowledge-deep-study-v0.1.md)和[来源覆盖账本](../references/source-coverage-v0.1.json)，不重建专家体系或复制旧仓全部知识。

## 1. 范围：完整保留原始目录，但不伪称已全部读透

- [Hermes固定全目录](https://github.com/sunshihao001/-/tree/2bf694b37cce25b4a3c9364298b784039f3ecc84)，264个文件；已深入 00c/00d/00e、钱包结构/角色、证据链与缺失政策；其 learning/skills/tasks/reports/tests 尚未逐条追设计与失败链。
- [qb-固定全目录](https://github.com/sunshihao001/qb-/tree/8377ad5611255df5cd4562666a826708575334f0)，4236个文件，包含大量快照、备份和真实任务式资料。已读单Mint脚本、Wallet-Intel分层/护照/兼容读取/部分验证报告；source_wallet_bot的完整源码-样本-历史结果、其余4千余文件尚未全部审查。
- [meme-固定全目录](https://github.com/sunshihao001/meme-/tree/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a)，474个文件。已读真源、成熟度、深洗/死亡盘、诱多反抽、反证实验；原MQL5指标源码、样本标注、specs和历史修订未全量核验。

原始完整目录在上面不可变提交保留；Blix仅记录来源路径、独特认知和待审范围，不把每一旧文件复制成新卡。既有[00d全文](hermes-multidimensional-reasoning-original.md)、[00e全文](hermes-reverse-discovery-original.md)、[00c方法](hermes-feature-to-market-structure.md)继续有效。旧 PR #14、#16、#17仍属历史Draft来源，不是Blix已经合并的实跑能力。

## 2. Hermes：从“套框架”到“让异常反推框架”

[00c：五问题推理](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00c-GMGN-思维模型提炼.txt)真正的顺序是：想知道什么市场事实→链上有哪些可观察痕迹→哪些原始字段实际观察到了→如何交叉排除替代解释→结论何时、对哪些对象才成立。它不是GMGN术语速记，而是针对经济问题构建观测方式。

[00d：多维推理](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00d-GMGN-多维度推理扩展.txt)在相同字段上变换问题：从钱包角色到角色随时间转变；从量价到池/冲击；从结构到生命周期与策略适用性。这提示同一Mint不是一个静止的标签集合，而是钱包、库存、资金、池和外部注意力持续相互作用的过程。

[00e：逆向发现](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00e-字节反推框架-突破认知局限.txt)提出：变量组合、异常对照、无监督聚类、生成对立框架、时间序列挖掘、跨链比较。关键价值是**允许数据产生尚未命名的问题，而不是只给现有“吸筹/出货/庄家”找例子**。

但其科学前提必须纠正：80数值字段能组合3160对，不意味着3160条有效新规律；比例除零、变量同源性、多重比较、热门胜利样本挑选、事后观察未来、钱包标签本身的选择偏差，都可能产生假发现。00d中“同源+成本相近+同时买=极高概率同控”等属未经校准的旧假说；不应进入Blix的概率输出。更好的方式是让残差/异常生出多个竞争解释，事前列出每一种解释被什么新证据推翻。

## 3. qb-：真正独特的是调查对象选择和事实可用性约束

[原sikk单币脚本](https://github.com/sunshihao001/qb-/blob/8377ad5611255df5cd4562666a826708575334f0/sikk_gmgn_token_report.py)不是单纯汇总Top Holder；它同时寻找获利者、早期/sniper/bundler、LP基础设施、Token转入接收者、转入后卖出者。其问题意识是：**调查名单应该由经济作用决定，而不是按账户余额排序**。但是原classify()把供应商transfer_in和卖出比例≥0.6推成“分发派发钱包”，可做补查候选，不能直接确认为幕后派发者。

更值得沿用的是[Wallet-Intel四层规则](https://github.com/sunshihao001/qb-/blob/8377ad5611255df5cd4562666a826708575334f0/hermes_harness/01_control_plane/wallet_intel_data_layering_rule_v2.md)：可回溯钱包事实、关系/结构证据、带不确定性的行为解释、下游观察/研究交接。每层有不同证明责任；下游不得把上游推断写成原始事实。

[数据护照](https://github.com/sunshihao001/qb-/blob/8377ad5611255df5cd4562666a826708575334f0/hermes_harness/01_control_plane/wallet_intel_data_passport_rule_v2.md)必须记录旧/新来源、已知和缺失、事实与推断界限、是否足以继续分析。这与Blix混用Holder的current snapshot、历史账本、Jupiter/RugCheck和Bubble Map图有直接关系：**报告要先知道此时有哪些事实可用，再决定能否研究控制/库存/历史。**

[阶段6验证](https://github.com/sunshihao001/qb-/blob/8377ad5611255df5cd4562666a826708575334f0/hermes_harness/06_verification/project_governance/wallet_intel_stage6_data_passport_verification.md)的PASS只证明护照规则/模板锚点存在，明言未真实导入Token数据。不能因此说旧qb曾完成产品业务端到端验证。

## 4. meme-：最重要的知识不是价格标签，而是一个解释如何真正失败

[成熟度审计](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/第一控盘区成本中枢回收模型_成熟度审计.md)将FCZ/POC/AVWAP“二次接受”定位为结构化观察模型，并未证明自动识别、回测或盈利。其深洗、死亡盘、诱多、二次启动是一组互相竞争的市场解释，不能由单个反弹或回撤幅度倒推出操作者意图。

[反证实验](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/09_规则与回测/反证实验设计_v0.1.md)明确事前冻结定义、记录成功及失败、不能事后换成本锚排除失败样本、复合规则要与简单基准比较。此方法在Blix中可用于**链上行为假设**：当观察到拉升前12h转账激增，必须同样调查转账激增却没拉升、拉升却没有激增、公共服务批处理、RPC断流/补回导致假峰值等情况。

其策略语言仍可保留为条件假说；不能把POC当作真实控制者成本，更不能用图形形状直接生成庄家身份或交易信号。Solana市场的多池、迁移、库存转手和流动性冲击可以解释同一价格形态。

## 5. 跨行业视角如何真正帮助认知，而不是扩建“专家制度”

这些是本轮从公开学科原始材料借用的**动态问题视角**，不是声称有真人专家参与。

| 视角与来源 | 对当前Blix提出的新问题 | 何时真正有用 |
|---|---|---|
| [过程挖掘与OCEL 2.0](https://www.ocel-standard.org/) | 单个Swap同时关联签名、若干Wallet/Token Account、两个Mint、池和Fee Payer；按每个钱包/Mint单独当作唯一流程是否会割裂或重复经济事件？ | 跨Mint资本循环、多腿CPI、群体角色演化 |
| [W3C PROV-O证据溯源](https://www.w3.org/TR/prov-o/) | “资金来源”到底由哪个原始交易、哪个供应商、哪次解析/规则产生？事实和推断是否可逐级回溯？ | 多源Holder冲突、图谱来源、AI解释可重算 |
| [数字取证/事件响应NIST SP800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | 一条异常是否有原始事件链、观察时间、处理过程、缺口和失败恢复？ | 追踪历史回补、判断异常或仅缓存刷新 |
| [Pearl因果推断](https://proceedings.mlr.press/v6/pearl10a) | 同Slot、同手续费代付或资金共同来源能否识别共同控制？存在什么观测等价的其它机制？ | 钱包同控/内幕/预测优势的竞争解释 |
| [NASA系统工程验证与确认](https://www.nasa.gov/reference/2-0-fundamentals-of-systems-engineering/) | 有源码和测试不等于用户想解决的问题真正解决；能不能在真实条件下完成一项调查？ | Blix产品路线与AI外挂大脑验收 |

按当下问题择取一两个视角就够：因果+取证适合资金归因，过程挖掘+会计守恒适合跨币资产循环，可靠性+用户验证适合监控和Agent。**学科观点不是新的强制人格/22席Bot。**

## 6. 新的专业认识：以“多对象经济过程”替代单一钱包标签作为研究对象

这不是要求立刻实施OCEL数据库，而是研究事件怎样保持同一性。

Blix已读源码反映不同语义：
- [wallets.js](https://github.com/sunshihao001/grok/blob/blix/server/wallets.js) 的wallet_trades键为(sig,wallet,mint)，还存在按(sig,wallet)判断已读的路径。
- [wtrack.js](https://github.com/sunshihao001/grok/blob/blix/server/wtrack.js) 的wt_feed及wt_transfers以(wallet,sig,mint)去重，其中Token转账对手方可取“最大相反余额变化”候选。
- [solana.js](https://github.com/sunshihao001/grok/blob/blix/server/solana.js) 的parseSwaps在多个非quote Mint变动时返回空结果。
- [journal.js](https://github.com/sunshihao001/grok/blob/blix/server/journal.js) 已有tradeKey(sig,mint,n)的更细发生序号，说明原产品也认识到同一签名有多动作。

**源码支持的风险推论**：上述模块不能自动组成覆盖所有经济动作的统一历史。若一笔交易包含多条Token转移、Swap、SOL/WSOL包裹和多个Token Account，部分动作可能在按wallet/mint入库时消失；后来的AI无法从丢失信息中可靠恢复资本路径。尚未用真实交易复现。

由此形成可推翻的研究假设：**跨Mint群体研究最重要的未满足条件也许不是关联图深度，而是交易、资金、库存、时间和关系角色的多对象事件恒等。** 如果原Blix能经实测准确重建，则不需要新存储；若不能，允许考虑成熟只读事件服务、有限补记或改造，而不是永久要求外部项目服从现在的数据表。

## 7. 一次实际问题的知识融合推演（示意，不是真实Mint）

用户只问：“W1/W2一起买Mint A、Token转给W3卖，随后另一Mint B也出现同类操作，是同一伙人循环出货吗？”

**Hermes先问隐藏的市场问题**：我们看到的是同一资产的连续处置、同一资本预算的循环，还是多个独立对象共同使用基础设施？如果先贴“庄家接力”，会错过未知的角色替换和服务商执行模式。

**qb把现有信息拆开**：观察到签名中的Token转账、真实Swap、最终SOL净变化是事实；“共同资金来源”要回原始转账和历史覆盖；“同一伙控制”只能是解释候选。暂时没数据就输出不可确认而非“没有关系”。

**meme提出对立世界和失败样本**：H1共同控制分仓出货；H2共同机器人/代付费/做市服务导致同步；H3热门事件引起独立人交易与转仓；H4部分记录被缓存或漏解导致的假群体。要问各解释需哪些额外观察才会失败，不能用后来的价格走势回填当时的内幕事实。

**Blix现有能力的准确边界**：Coin/Holder提供部分当前账户视图，Bubble Map产生关系候选，Wallet/WTrack观察部分交易、转账和历史；关键缺口可能是多动作、净资产和时点一致性。正确的工作输出是“当前证据支持若干地址存在相连行为；是否共同资本控制UNKNOWN；最值得补查W3卖出净SOL→W4在B的实际出资路径、共享服务背景率及时间/数据覆盖”，而不是直接宣称“庄家概率90%”。

## 8. 进入Blix的方式与允许推翻产品路线的条件

1. **原文原位保留**：旧研究全文已有00c/d/e等入口，三仓完整目录有冻结commit，覆盖账本区分仅盘点、实读和深入研究。未审范围不靠“钱包/市场/策略”这些标签提前排除。
2. **按任务选知识**：现有[知识调用说明](../../docs/project/knowledge-use.md)及[ai-d认知Skill](../../.grok/skills/ai-d-cognitive-core/SKILL.md)在用户问题含有“同控/跨币资金/库存/异常”时检索相关原始推理、反证和竞争解释；禁止把全部文章常驻到Prompt。此处只是正确调用路径建议，**Grok Bot自动使用未验证**。
3. **事实输出限制**：未来调查应披露数据源、交易位置、Mint、Token Account、Owner、Fee Payer、Slot、观察/采集时间、未观察区间以及每条关系的证据类型；现阶段是待验证的产品要求，不是已实现改动。
4. **适合哪种产品改动由证据决定**：若只是错误标签/来源，可改现有报告和Bubble Map注释；若多腿动作无法还原，优先比较成熟来源、现有Wallet账本修复与轻量事件存储；若Blix整个运行环境安全/成本不可承载，可重新评估主体方案。**Blix作为当前基石，不是不可推翻的信条。**

必须区分“原始资料已保存”“AI能检索”“AI改变了正确判断”“运行程序通过独立验收”四件事。当前完成的是前两者的研究入口和人工专业示范，不是第三、第四项实证。

## 9. 下一轮研究，不再重复给项目打标签

主线是**跨钱包、跨Mint经济过程的可识别性**，并继续独立研究原项目全部知识范围：

- Hermes：深读00b字段数据合同、00c/00d/00e对应的grill sessions、筹码控制状态设计及learning/skills/tests/reports中的失败历史，复原“为何提出这个维度→何处适用→何处失败”。
- qb-：沿source_wallet_bot及Wallet-Intel的真实源码和保留样本，核对事实/证据/推断在运行中是否真分开；验证护照PASS到底证明什么、哪些实际未完成。
- meme-：研究原样本/指标代码/specs的事前可观测性、跨池可比性和失败样本；探讨FCZ/深洗叙事是否有独立资金/库存解释价值。
- Blix：按签名层事件对照Coin/Wallet/WTrack/Journal/Bubble Map的完整动作保留与角色归属；形成能鉴别H1/H2/H3/H4的离线反例要求。
- 成熟成品：带着具体“历史回补/资金边/多对象事件/持续档案”的新问题比较Million、PumpTrace、Pulse；继续各自整体产品研究，不因目前只检查几个模块就宣称读透。

下一轮应交付**一条完整设计—数据—推理—反例—修订链，以及它如何改变Blix产品判断**，而不是又一批没有实际判断增量的知识文件。

> 证据等级：原仓/Blix源码观察SOURCE_READ；跨行业对应和新机制问题INFERENCE/HYPOTHESIS；真实Mint、自动知识调用、离线测试、云电脑部署与连续监控均NOT_RUN。


---

## 10. 2026-11-07 原始推理链纵深补审：00c–00e、两部大稿与 Grill 原始记录

> **本节覆盖了上一轮尚未深入审阅的两部大稿及相关历史问诊，并用固定旧 fixture 做字段契约静态检查**。固定源版本：Hermes \`2bf694b37cce25b4a3c9364298b784039f3ecc84\`。本节判断为源代码/文档审阅与静态复算，非 GMGN 当前接口实测、实时 Mint 取证、完整同类项目验收或真实独立 AI A/B。前述1–9节原研究结论保留，本节补充或修正其限制。

### 10.1 来源全文结构核查、与既有 Blix 原文的关系

| 原始研究 | 固定 blob SHA | 本次实际核查范围 |
|---|---|---|
| [00b canonical字段目录](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00b-GMGN-Canonical-Bytes.md) | \`7e0141456911f6180f0c8f35f51ea7c16cc982e8\` | 12组供应商字段及其数据来源；不是Solana原始字节 |
| [00c思维模型](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00c-GMGN-%E6%80%9D%E7%BB%B4%E6%A8%A1%E5%9E%8B%E6%8F%90%E7%82%BC.txt) | \`123c087cba7af99f94565cabf6c31d0e84d98ff3\` | 8项核心模型、5种推理操作、5项GMGN语义限制、7项可跨源迁移方法 |
| [00d多维推理](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00d-GMGN-%E5%A4%9A%E7%BB%B4%E5%BA%A6%E6%8E%A8%E7%90%86%E6%89%A9%E5%B1%95.txt) | \`262866de3c4d00bcbd2c17b2c71398e6bc158465\` | 同数据按钱包角色、市场微结构、参与者生命周期、策略适用性改变问题框架 |
| [00e逆向发现](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/00e-%E5%AD%97%E8%8A%82%E5%8F%8D%E6%8E%A8%E6%A1%86%E6%9E%B6-%E7%AA%81%E7%A0%B4%E8%AE%A4%E7%9F%A5%E5%B1%80%E9%99%90.txt) | \`6c008fa4a016099cbd5a71f3ff880afada225aea\` | 六种发现路径：组合、异常对照、无标签聚类、对立生成、时间序列、跨链 |
| [gmgn-byte-combination-reasoning-v0.1.md](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/gmgn-byte-combination-reasoning-v0.1.md) | \`4f7f70dcf8bb6d77373fec859cc0ef8ab5c0b994\` | 全文结构1811行；以标题逐项核对**37条独特L1定义**，对关键SM、资金同源和时间变量细读输入、推论与阈值；还记载部分L2的应用解释及Part7方法 |
| [gmgn-byte-decomposition-v0.1.md](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/gmgn-byte-decomposition-v0.1.md) | \`c787b9c8abafae11a9f73315acfeb2603ceec414\` | 全文结构1445行；逐标题确认**16个L2候选**、七种VWAP角色映射、质量门禁、Allowed/Forbidden解释、七项显式数据/能力缺口；重点细读A1、C1/C2/C3与反证边界 |
| [2026-05-26 Grill Session](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/design/phase1-research/grill-sessions/2026-05-26-grill-bytes-to-framework.md) | \`605c2a73e641204d18f15fe6ff27be5a03036f02\` | 重读原始意图—术语澄清—资料边界—研究终点；当时明确READY_FOR_REVIEW、非已运行 |
| [canonical_bytes_intake](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/canonical_bytes_intake_20260526.md) / [updated_project_cognition_v2](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/updated_project_cognition_v2_20260526.md) | \`fa7a2a25def8daea809c7f1bdea575a212a6f5e6\` / \`c802016b2a1c276dd0aa2d2637bf44df27aee021\` | 核查原字段接入责任、阶段认知改变、数据与结构/策略分权 |
| [旧批次NEED_MORE_DATA分析](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/batch_20260526T123011Z_need_more_data_analysis.md) | \`88f96a719a1b83dbe1e9ad2459e4cfc272adabc9\` | 作者报告4个token因缺SM等正向证据未达后续Gate；**报告不是本轮原始数据重放** |

实际查看了两部全文目录和关键方法/输入/结构主张，但**未将37条和16条逐一与当前 GMGN API、链上原始交易及历史样本执行验证**。“已完整读懂53条真实市场规律”仍不成立。Blix已保存[00c原文](hermes-feature-to-market-structure.md)、[00d原文](hermes-multidimensional-reasoning-original.md)、[00e原文](hermes-reverse-discovery-original.md)；本次不再复制同样原文，保留前述大稿原路径和SHA。

### 10.2 重新恢复从“用户想法”到“发现未知”的完整原始因果链

Grill中用户的原始意图并非“做37个指标”，而是用原先的字段组合反推以前不知道的市场策略/结构。记录中的术语澄清为：GMGN所谓230+字段 → **0层供应商已处理字段**（00b列出约120个可直接用的候选字段）→ **1层37个派生变量** → **2层16个结构候选**。对照两部大稿按标题确有：

- **L1-A** 买卖压力6：buy_dominance/count_ratio/net_flow_intensity/SM/KOL方向/仓位加权SM；
- **L1-B** 动量和交易活跃5：volume_intensity/momentum/swap_per_holder/volume_per_swap/decay；
- **L1-C** 深度与质量5：市值与流动性比、距ATH、头部地址变化、流动性变化、价差代理；
- **L1-D** 钱包智能7：SM渗透/退出/盈利、KOL、fresh钱包、资金来源收敛、sniper库存；
- **L1-E** Creator/风险6：Dev、发币历史、营销、所谓insider活动、费用负担、CTO；
- **L1-F** 时间生命周期5：token年龄、curve进度速度、开盘后时间、池龄、持有人增长；
- **L1-G** 社交/注意力3：完整度、粉丝/市值、描述启发式。
- **L2十六项**：A1–A3积累、B1–B3退出、C1–C3操纵/流动性、D1–D3生命周期、E1–E3事件、F1结构健康。

**同一个字段集合在不同专业问题下可构成不同的候选机制**，这是00d的核心。00c进一步提供8类认知工作：五问题、原始/派生/解释分层、负向质疑、分母即语境、必要/增强/否定条件、方向×身份×背景、token年龄修正、Allowed/Forbidden语义边界。其5种运算模式是比例、方向×规模、方向×身份、静态×动态、缺必要条件；并且指出没有订单簿、成交≠挂单、极早期样本不足、Token级SM不等于钱包历史、Meme不能沿用CEX阈值。

**要传给Blix的是这些“如何生成问题、选择可观察对象和解释边界”的能力**，而不是强制运行37+16条旧阈值、固定阶段或一张“庄家标签表”。由00e反过来再打开搜索空间：枚举组合、寻找异常分布、发现未命名群体、生成当前假说的对立面、比较时间演化与跨市场差异。两方向相互制约：先验理论可以引导有效观测，无监督探索可挑战先验，但二者都不能直接认证共同控制或盈利优势。

### 10.3 六项由原文件细读发现的实质修正

**发现A：所谓L0原始数据已经有上游解释。** Grill本身承认Canonical是GMGN加工后的“准raw”，而非Solana的指令/CPI/资产净变动。SM/KOL、insider、wash、fresh、CTO是带供应商策略或标签的输入，即使在L1/L2多次组合也不会自动升级成独立原始证据。当前对“230+原始字段完全真实存在且一致可用”仅有旧研究宣称，**未当次对GMGN实际响应重新核契约**。

**发现B：同一来源派生的多指标可能伪装成多份支持。** 例如L2-A1依靠SM标签 cohort 的净方向、持仓、退出与市场量；L1-A4读取per-SM \`netflow_usd\`，L1-D2又看\`sell_amount_percentage\`，不同时段、不同统计分母可能混在一起。没有记录每个字段的观察窗口、样本重叠和所缺地址，不能把四条件说成“四项相互独立证明”。作者明示\`smart_degen_count >= 3\`仅为质量门，不能产生概率保证。

**发现C：资金同源特征既没有完整数据合同，也没有身份真值。** L1-D6 \`wallet_source_convergence\`写了Shannon多样性与0.7/0.3阈值，但本次读到的定义未给出可重复的Shannon归一化公式、缺失处理/选择Top20的分母，亦没有证明\`native_transfer.address\`就是Solana原始交易中某资金的真实最早来源。原文先将共享出资的地址说为同一实体，后又提醒CEX热钱包可造成伪集中。该认识应修为：**可见资金来源的集中度仅是一种图形/调查候选，服务设施、资金再分发和截断历史是竞争解释**。

**发现D：旧“反证法”本身要专业修订。** 00c、组合文档7.6将“假设没有积累时可能看到方向分歧/清仓/缺量”等反例列出，再取否定作为积累的成立条件。这有助设计筛查条件，但逻辑上“无积累”不必然等于这些条件同时出现，“四条件都满足”也不足以证实市场存在同一意图的信念积累。应区分**操作性判别定义**与**机制因果解释**；meme-要求预先冻结定义、保留模型符合但失败样本、比较更简单基线才属于可严格反证的验证路线。

**发现E：静态快照和趋势特征常跨越不同可得时间。** F2 Curve进度速率至少需两次采样，F5 Holder增长率需独立时点；Token年龄、池龄、\`netflow_usd\`历史聚合和最近1小时量可能不同。定义L2时应对齐业务时点、采集完成时点、是否已回补、数据缺失/源更新延迟；否则并非真正的先兆证据。

**发现F：旧文部分表述把启发式当事实。** C1“内幕主导”、C2“刷量”、A1“聪明钱有信念”、D6“极高概率同一实体”、所谓3分钟/2小时成熟度、\`spreading/SM=因果\`、P0/P1风险加权均缺当前校准。无K线逐笔成交时的spread/VWAP代理、固定滑点示例亦不能代替AMM真实Quote和多池路由。**保留原研究对象、候选解释和算法思路，但明确这些具体标签/阈值不是Blix运行规则**。

### 10.4 qb-原始单Mint程序的可复核“字段契约断层”

代码：[qb- \`sikk_gmgn_token_report.py\`](https://github.com/sunshihao001/qb-/blob/8377ad5611255df5cd4562666a826708575334f0/sikk_gmgn_token_report.py)，blob \`f610343bf7a2d3309e23c783556e1e59ddd1c24f\`。该源码确实将info/security/pool和holder、trader多列表合入**8个CSV视图**，其中关键钱包矩阵、基础设施清单、低权重调查范围和T+复查时间最值得保留。这比新建一张“聪明钱标签表”强得多。

但把Hermes推理直接套到此旧程序会出现明确静态不兼容：

| 来源或程序 | 实际使用的字段 | 含义与问题 |
|---|---|---|
| Hermes L1-D6推理 | \`native_transfer.address\` | 旧设计假设的资金来源候选 |
| qb单Mint \`nf\`读取 | \`(w.get("native_transfer") or {}).get("from_address")\`（仅嵌套dict） | 无该对象则返回空值，不自动读平铺别名 |
| Hermes已冻结fixture | \`native_transfer_from\` | 顶层字符串，与上述两种嵌套形式均不兼容 |

**实做静态字段对照**：固定 [场景05-信号冲突](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/fixtures/%E5%9C%BA%E6%99%AF05-%E4%BF%A1%E5%8F%B7%E5%86%B2%E7%AA%81.json)，20条Holder各有非空\`native_transfer_from\`，且20值各异；按qb源码所用**精确嵌套字段取值逻辑**检查，20条均为空；按00c/D6嵌套\`native_transfer.address\`也全部读不到。该对照**只是重现字段取值逻辑，不是运行qb依赖GMGN的完整脚本**。固定 [场景04-数据缺失](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/fixtures/%E5%9C%BA%E6%99%AF04-%E6%95%B0%E6%8D%AE%E7%BC%BA%E5%A4%B1.json) 20条本来就为空；这两个case表明**“来源读取失败”与“证据本来缺失”要区分**。

额外源码限制：
- qb对不同列表按钱包地址合并标签，但保留首次出现记录的其余非标签字段；来自不同快照/入口的金额与时间可能未同步，无法无条件当统一钱包事实。
- \`classify()\`把\`transfer_in\`且\`sell_amount_percentage>=0.6\`变成“分发派发钱包”与E4等历史等级，这是调查候选不是实证的共同控制或合谋。
- 一些\`fl(...,0) or 0\`和\`or\`别名逻辑将缺失转为0；且输出若无\`transfer_in\`便标\`主动买入\`，不能从数据缺失否定链上收款/转仓。CEX/Router候选常需保留而非误归为操盘地址。
- 选取前25个关键地址时有历史优先级，可能漏掉**非Top但跨多个Mint反复接收/卖出的关键地址**。保留低权重观察对象和复查路线，不应当作永久不重要。

**产品意义**：Blix应在研究报告里把SOURCE_FIELD_UNAVAILABLE / SCHEMA_ALIAS_MISMATCH / TRUNCATED_HISTORY / TRUE_ZERO独立表达；若不解决字段适配与资金因果语义，再强的Hermes解释也可能建立在被静默置0的数据上。这里仍是待验证的产品建议，不是已改代码。

### 10.5 meme-并非K线补充包：它对“机制被证明”的标准有更强约束

直接对照 [meme-反证实验设计](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/09_%E8%A7%84%E5%88%99%E4%B8%8E%E5%9B%9E%E6%B5%8B/%E5%8F%8D%E8%AF%81%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1_v0.1.md)、[简单基准对照](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/09_%E8%A7%84%E5%88%99%E4%B8%8E%E5%9B%9E%E6%B5%8B/%E5%9F%BA%E5%87%86%E7%AD%96%E7%95%A5%E5%AF%B9%E6%AF%94%E5%AE%9E%E9%AA%8C%E8%AE%BE%E8%AE%A1_v0.1.md)、[策略反证样本库](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/09_%E8%A7%84%E5%88%99%E4%B8%8E%E5%9B%9E%E6%B5%8B/%E7%AD%96%E7%95%A5%E5%8F%8D%E8%AF%81%E6%A0%B7%E6%9C%AC%E5%BA%93%E8%AE%BE%E8%AE%A1_v0.1.md)、[深洗/死亡盘](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/02_%E5%BA%84%E5%AE%B6%E5%91%A8%E6%9C%9F/%E6%B7%B1%E6%B4%97%E4%B8%8E%E6%AD%BB%E4%BA%A1%E7%9B%98%E8%AF%AD%E4%B9%89%E6%B7%B1%E5%8C%96_v0.1.md)以及[成熟度质疑审计](https://github.com/sunshihao001/meme-/blob/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a/09_%E8%A7%84%E5%88%99%E4%B8%8E%E5%9B%9E%E6%B5%8B/%E7%AD%96%E7%95%A5%E6%88%90%E7%86%9F%E5%BA%A6%E8%B4%A8%E7%96%91%E5%AE%A1%E8%AE%A1%E4%B8%8E%E5%95%86%E4%B8%9A%E8%AF%8A%E6%96%AD_v0.1.md)。

- **预先冻结失败定义**：触发时符合条件、后来失败，仍属于失败；不能事后说“这个不是真积累/真洗盘”。这一点直接纠正旧Hermes“异常命名后看结果再改标签”的循环风险。
- **研究误报也研究漏报**：A成功、B符合失败、C不符合却上涨、D像洗盘却死亡、E定义争议、F无法执行/成本偏差；不能只挑得出的成功图形。
- **简单策略/简单解释基线**：复杂模型必须和只看资金净流、普通活跃、单一时间窗口、随机/空模型比较；新增字段/动态专家视角只有显著改变可靠判断才有价值。
- **POC/AVWAP不是控制人真实成本**：能提供参与者竞争解释和结构失败观察，但不能直接反推匿名庄家身份或相同经济仓位；用户当下聚焦链上行为，可以只提取其“接受/拒绝/失败后续”的可证伪精神，不必强制把K线策略当主线。
- 上述仍为旧meme-的实验设计与作者自评，**不是本轮执行过的真实大样本效果**。

### 10.6 ai-d共同输入的静态诊断：有新问题，但未证明模型提升

使用相同的两个**公开合成fixture**进行内容检查。它们是旧Hermes的测试输入与历史期望输出，不属于真实Mint；本轮没有两个独立、隔离的模型上下文，也没有启动Blix运行时。因此下面是**可复核的并排分析诊断，不是严格A/B实验**，不能以“新增问题数”自评分证明AI更聪明。

| 相同固定输入 | 旧fixture约定结果/容易停下的位置 | 加入Hermes原问题 + qb字段契约 + meme反证 + ai-d知识适用检查后，明确增加的可核查问题 | 本轮判定 |
|---|---|---|---|
| **场景05：SM方向正面与结构critical冲突** | 旧期望\`wallet_roles.PASS\`、\`smart_money_count=3\`、\`sm_net_direction=accumulating\`；\`wallet_structure.WARN/critical\`、\`evidence_chain.WARN\`、终点\`WATCH\` | 20地址的资金字段是否能被Blix/qb正确读取？不同\`F0..F19\`地址能否说明真正独立？期望“SM accumulating”是否有真实净成交/窗口证据，还是来自标签及模拟预设？“critical”具体由哪些可回放异常支持？看不到可靠资金/库存、不能自动解释为吸筹或合谋 | **保留WATCH/UNKNOWN，不新增确定性机制标签**；需要签名级资金和风险触发证据；本次脚本字段静态对照发现20/20别名不兼容 |
| **场景04：资金来源缺失** | 旧期望\`wallet_structure.WARN\`、\`evidence_chain.NEED_MORE_DATA\`、\`trade_gate.NEED_MORE_DATA\`；20地址的来源字段确实为空 | 缺失是该供应商从未提供、响应字段格式变化、未采集足够历史、公共服务无可解释初始出资，还是只是测试mock？\`dominant_behavior=ACCUMULATION\`是否仅靠标签模拟而没有交易输入？应不能把0个可见资助来源解释成0条真实资金转账 | **同样保留NEED_MORE_DATA**，但细化\`MISSING_SOURCE\`/契约不符/历史不足的分支调查，不给出“资金来源分散或健康”判断 |

按 [ai-d评测规范](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md)，下一次真正比较应使用A0无额外知识、A1按需深研、A2全文过量注入负对照、A1b同源加动态学科质疑；固定同一模型版本/同样任务/工具权限，隔离上下文并匿名复核“真正新增且有依据的问题、错误断言、反证、成本和完成度”。本轮只验证了**研究方法能提出具体的额外审查点**，未验证任何模型在独立任务上性能提升。

### 10.7 跨学科合成：形成四个尚未被证明的新机制研究问题

它们是待调查的市场机制**问题而非预设的四种庄家类型**：

1. **已知标签外的结构创新**：某Token虽缺SM样本或不满足现行交易Gate，却出现有序的Token转手、库存角色替换或跨Mint资金活动。能否在不依赖SM标签时，观察到稳定可复核的经济模式？需要反例：公共服务、活跃度基线、样本选择和完整钱包历史。旧Hermes[批次报告](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/reports/batch_20260526T123011Z_need_more_data_analysis.md)记录4个token因缺SM等正向证据停在\`NEED_MORE_DATA\`，**这只说明旧门禁缺可证明的正向证据，不说明这些Token真的含未知机制**。
2. **字段契约造成的伪缺失/伪健康**：源字段别名、窗口或供应商缓存改变时，数据从“实际有但读取不到”变为0/unknown，AI随后解释成无同源或无资金转移。可用源原始JSON、固定Schema适配及再查链上事件反证。
3. **相似行为下的不同资本组织**：同源、同成本、同步买入可由一人多钱包、共同服务、独立跟随、回补批处理产生；只有库存净变化、实际对价、交易签名/多跳、费用代付与完整观察窗口可区分。图可达≠共同控制≠经济受益人。
4. **不完备历史塑造的“异常前兆”**：一段时间事件突然增多可能是新资金活动，也可能是RPC恢复/索引回填；另一些“突然沉默”可由数据缺口引起。新假说必须用事件时间、首次可用时间、观察水位和对照组区分。

**共同原则**（科学哲学×信息统计×数字取证×会计/微观结构×分布式系统×产品质量工程）：发现未知需要自由生成假说，但要对数据完整性、观察时点、样本选择、竞争解释、可重复机制与可执行净收益分别承担证明责任。学科视角按问题动态取用，不建立固定专家席位，也不把学科理论直接当Solana的链上发现。

### 10.8 已识别的Blix真实源代码落点与知识转化

本轮对照了当前[Blix\`server/triage.js\`](../../server/triage.js)、[\`server/research.js\`](../../server/research.js)、[\`server/coverage.js\`](../../server/coverage.js)、[\`server/quality.js\`](../../server/quality.js)，结合此前已读[\`bubblemap.js\`](../../server/bubblemap.js)、[\`wallets.js\`](../../server/wallets.js)、[\`wtrack.js\`](../../server/wtrack.js)：

- Blix Triage通过初始规则与LLM“slop/meh/maybe/promising”等标签选择较少Token升级研究；**但已有live trading活动的币也可进入研究**，不是绝对被视觉标签封锁。Coverage的5分钟\`runners\`处理“没出现在固定栏目却重新活跃”的已知覆盖缺口。不能声称Blix完全没有异常发现能力。
- 现有\`research.js\`同时有叙事、实时市场traction、研究输出和交易选择的prompt语义；\`brain.js\`含paper/entry逻辑。用户现在要求的是**只读专业调查**，不要将Hermes结构候选直接接到可行动的\`buy\`、\`trade.pWin\`和entry路径。
- **最有价值的知识补强**是让“研究是否值得继续”和“交易是否安全/满足已验证策略”成为不同问题：一个未知结构可能交易风险极高，但仍是解释/监控的研究候选；安全硬边界继续不降级。
- Blix\`bubblemap.js\`最早资金来源的Fee Payer回退、最多3页签名和负缓存应保留为**数据可观察性缺口**，不能用Hermes同源规则加强标签的确定性；新知识先指导报告和测试用例，之后才有代码修复资格。

**交付状态**：本轮将原始Hermes大稿、历史、qb契约、meme反证、ai-d共同输入诊断及Blix代码适用性写回原有研究正文，完善了GitHub可查询的研究成果；**没有接入实时模型检索、部署产品、修改Blix业务代码，未实际发出交易**。新报告和知识调用说明为研究可执行的候选，不代表已具备市场盈利预测。

### 10.9 下一项真正值得执行的核查

按“哪条证据能改变Blix行动/解释”排序，而非按固定小阶段：

1. **最短可证伪合同**：在只读/离线隔离下，用固定Schema样本检验\`native_transfer_from\`、\`native_transfer.from_address\`、\`native_transfer.address\`、真正原始SOL Transfer、Fee Payer、缺失与截断各输出什么；核实当前Blix如何实际传递、显示这些区别。**预计最先改变一个实际的错误归因风险判断**。
2. **Hermes原37+16深审继续**：补原始GMGN真实接口契约、标准化公式和时间窗口；对SM积累/同源/异常流动性至少建立可计算的非空/零/缺失/冲突样本。专门检查原研究中未证实阈值和同一证据多次使用问题；不机械把53条全变成标签。
3. **qb-与meme-事实基线**：沿qb的关键钱包矩阵、基础设施排除、复查计划提取独有受观察对象；用meme的B/C/D/E/F失败样本框架固定旧假说的失败条件。比较一条“资金/库存接力”候选与共享服务/热点/历史回补等反例。
4. **ai-d独立实测**：同一份去敏真实或明确合成的Mint调查，A0/A1/A2/A1b在独立上下文运行并盲审；当前本轮只完成静态诊断，不能提供伪造的改进百分比。模型调用和数据访问权限满足之后再进行。
5. **直接应用到Blix业务结果**：优先生成一份可被其现有Coin/Wallet/Research页面表达的只读报告用例，含来源、观察窗口、资金/库存变化、多个待证机制、UNKNOWN、下一次观察；如现有模块无法表达，再提出最小可测修正，而不是先新建架构。

> **验收边界**：仅原始文件复查、指标/契约逻辑静态复算、源路径核对与GitHub写回。没有任何真实行情或钱包实际回放、当前GMGN许可/API契约测试、对Blix生产分支的功能修改，也没有Grok Bot真实调用。


## 11. 2026-11-07：旧推理公式的反例复算与知识进入Blix的检验

> **本节不是再做一轮知识分类。** 已基于Hermes `00b–00e`、1811行L1/L2推理稿、1445行L2/Quality Gate规格、Grill与固定测试输入，将旧研究提出的“未知机制发现”方法推进到**可证明在哪些前提下失效**。同时核查qb原脚本、meme历史样本与Blix现有读数逻辑。以下数值是**确定性离线反例**，不是真实行情、真实账户或经校准的概率。旧原文完整保留，不直接改其结论。

### 11.1 旧研究真正的三个不同环节，不应再合并为“一个识别模型”

- **问题生成**：Hermes 00c先问经济事实→可观测痕迹→数据合同→运算/归一化→解释；00d同一批字段转化为钱包、市场微结构、生命周期及策略问题；00e在无预定结论时以字段异常、无标签聚类、对立解释、时间序列与跨链对照提出新假说。
- **观察测量**：GMGN的所谓L0不是Solana协议底层原始字节。很多字段已经来自供应商的筛选/标签/估算。37个L1依赖七大输入家族（成交、量、池、钱包、Dev、生命周期、社交），对null/零、观察时间、是否包含同一事件、币龄、池与Holder覆盖有不同合同。
- **机制证明**：16个L2是候选性解释，不是16个真实市场规律；只有具有相互区分的后续预测/反事实、独立原始事实、完整观测窗口、普通市场对照和失败样本时，才可能升级。Hermes 00c的“如果非A则有B，取非B即A”并不是一般有效的因果反证；meme的预先固定失败条件、简单基准、消融和样本外约束纠正了这一点。

**源文件存在一处重要完整性差异**：完整规格 `gmgn-byte-decomposition-v0.1.md` 的Part2定义16个L2，包括 `F1 HEALTHY_ORGANIC_MARKET`；而详解 `gmgn-byte-combination-reasoning-v0.1.md` 单独展开的L2标题只有15项，未为F1形成同样的详细五问题推理链，虽然文件末尾称“16 L2完成”。所以**有16项清单≠16项已经拥有同等论证深度**；也不是16项已对GMGN或Solana实盘核验。

### 11.2 算术与经济语义反例：三项旧L1的直接失效条件

#### 反例A：L1-B2 `volume_momentum`把“时间窗口未满”错当“放量爆发”

原文采用 `volume_1h / (volume_24h/24)` 并把高倍数解读为异常放量。如果新币只有30分钟历史，且近1小时、近24小时都包含同一笔总成交 `$1000`，则结果 **1000/(1000/24)=24**。这个值对全部交易是匀速发生还是瞬时发生没有辨识能力；只要两窗口均覆盖全部存续历史便机械成立。同样每小时1000美元、连续24小时的老币结果则为1。

- **跨学科纠错（时间序列/生存数据）**：分母不是“24小时平均正常速度”，而是**被不足24小时的存续时间稀释**；两窗口还存在样本包含和高度依赖。先对齐Token可观察年龄、完整小时覆盖与归一化基准，或设为 `NOT_COMPARABLE_YET`，不能给出生后30分钟的币自动贴“24倍爆发”。
- **对Blix价值**：`server/coverage.js`已有5分钟真实活动窗口，属于另一类“当下有活动”定义。不能将Hermes的这一原值直接融合为Blix异常发现权重，避免大量早期Mint机械触发。

#### 反例B：L1-E4 `insider_activity_composite`把可能重叠的百分比相加

原文把 `rat_trader_amount_rate + bundler_trader_amount_rate + entrapment_ratio` 直接解释成“内部人/操纵交易**总占比**”，并以 `>0.5` 断言可能由内部人主导。若三项分别是0.60、0.60、0.40，公式得 **1.60（160%）**；不同供应商标签可能作用于同一笔交易，亦可能使用不同分母与时窗。即使所有分母相同，真实并集比例只受 **max(0.60,0.60,0.40)≤并集≤min(1,1.60)** 约束，不能从三项边际比例得出并集。

- **跨学科纠错（集合论/测量理论）**：需要事件级交集/并集、定义与分母、采样时段、标签生成机制。若缺少原始交易对应关系，只能展示`vendor_rat`、`vendor_bundler`、`vendor_entrapment`三条**可能相关的观察指标**，不能相加成真实独立操纵份额。
- **对Blix价值**：高风险和可研究的异常可以并存；不要将这个不可解释的合计数字用作确定性筛选/主体归因。规则性质为 `PROXY_UNCALIBRATED`。

#### 反例C：L1-C5 `spread_quality_proxy`把储备价值比例误当交易价差

原文声称“AMM池中quote/base储备越均衡，spread越低”，建议用 `pool.quote_reserve_value` 与 `pool.base_reserve_value` 的比例代理价差。这在常见**恒定乘积池**的定义下**不能成立**：设基础币数量x、报价币数量y，现货中间价p=y/x，若两边均按同一现货价计美元值，则基础资产美元价值`x*p=y`，报价资产美元价值`y`，比例都约为1，**与池深度无关**。

离线演示（无手续费、假定恒定乘积`xy=k`）：在报价储备 $100 的小池与报价储备 $1000 的大池，各输入 $10；两池基础/报价按现价计的储备价值比都为1，但订单相对于报价储备的规模分别为10%与1%，对这个购买方向的**成交均价相对交易前现价溢价**分别为10%与1%。**相同价值比不能识别交易价格冲击。** 现货边际价格变化又是另一种口径；不要把溢价、价差、滑点、报价变化互称。

- **跨学科纠错（AMM微结构）**：考虑具体池型（CPMM/CLMM/曲线）、费率、储备、路径、流动性tick与真实`amountOut`或真实Quote；不能将C5按原公式作为“spread”，也不能将USD估值变化直接当LP撤池。CPMM和集中流动性曲线差异明确，必须按协议适配。参考[Uniswap官方常数乘积与价冲击](https://developers.uniswap.org/docs/get-started/concepts/how-uniswap-works)、[Uniswap v2定价](https://developers.uniswap.org/docs/protocols/v2/concepts/pricing)、[Raydium官方AMM/CLMM/LaunchLab差异](https://github.com/raydium-io/raydium-docs-v1/blob/main/algorithms/slippage-and-price-impact.mdx)。
- **对Blix价值**：Blix `server/quality.js`已经区分Curve与非Curve池读数、退出条件；应保留其实际读数体系，不引入Hermes错误spread代理，直到Quote/原始池型数据证明有新增信息。

### 11.3 另外四项来源可核查的系统性失效风险

1. **L1-D2 SM退出比率的分母选择**：`sm_exit_ratio = count(SM卖出占比>0.8)/smart_degen_count`；但分子来自带tag的Holder列表，分母可来自Token层总SM数。如果请求只返回前10个或无法查询全部SM，未出现者绝不是“还在持有”。先以同一`as_of`的**实际查询到的样本数、总应观测数、缺失比例**分开输出；无法对齐则`UNKNOWN`。同理L1-C3 `last_active_timestamp`可能代表任何活动，不能直接推出Token库存被操作。
2. **L1-C4流动性保留率与LP动作不是同义**：`liquidity_usd/initial_liquidity_usd`受币价与池资产价值变化影响，单凭美元数减少不能确认LP撤出；需要LP份额增减/池状态、虚拟储备、兑换记录和池型证据。
3. **qb-的关键钱包选择与它自己的“基础设施不评分”存在业务张力**：旧 `sikk_gmgn_token_report.py` 的`priority(w)`给`addr_type==2`加100分再只选前25个，尽管输出文本声称LP/Pool不进入普通钱包评分。它确实在`classify()`把`addr_type==2`单列为LP；但**分析名额仍可被基础设施优先占用**，在多来源及多池时可能挤掉非Top的资金接收/转出钱包。不能只看“有基础设施排除”就断言关键钱包覆盖完整；需对`selected[:25]`前后与筛选遗漏对象比较。
4. **meme-历史失败样本不能按`is_real_sample`直接认作实证**：读取固定 `07_样本标注/反证样本库_v0.1.csv`，20条数据行的`sample_source`均为`real_pending`，但同时`is_real_sample`均为`true`；部分有待查token名称和来源备注，仍不能推翻`real_pending`明示的待采集状态。这是**样本元数据与实证资格冲突**，不能拿20条作为确认的历史胜负或计算准确率。应依赖可核对Mint、原始快照、固定规则版本、观察起点和实际结果，未核验前一律标为`PENDING_OR_CONFLICTED`。

### 11.4 来源合同离线复算：固定mock相同，结论为何因字段路径不同而变化

固定[Hermes场景04-数据缺失](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/fixtures/%E5%9C%BA%E6%99%AF04-%E6%95%B0%E6%8D%AE%E7%BC%BA%E5%A4%B1.json)，[场景05-信号冲突](https://github.com/sunshihao001/-/blob/2bf694b37cce25b4a3c9364298b784039f3ecc84/fixtures/%E5%9C%BA%E6%99%AF05-%E4%BF%A1%E5%8F%B7%E5%86%B2%E7%AA%81.json)。只重放三个旧字段**精确属性访问方式**：平铺`native_transfer_from`，Hermes假设`native_transfer.address`，qb使用`native_transfer.from_address`。统计具有非空地址的Holder数量：

| 同一份明确mock输入 | Holder | 平铺字段 | Hermes嵌套 | qb嵌套 | 原测试期望 |
|---|---:|---:|---:|---:|---|
| 场景04：来源原本缺失 | 20 | 0 | 0 | 0 | `NEED_MORE_DATA` |
| 场景05：来源确有平铺值，20个值各异 | 20 | 20 | 0 | 0 | `WATCH`，含积累正面与风险critical冲突 |

这验证的只是**历史程序与固定样本的字段不匹配**；不能推论当前GMGN API必然返回平铺字段，也不能推断20个地址代表独立经济主体。旧qb把缺失解析为默认0时，会把`PATH_MISMATCH`误当`NO_SOURCE`；Hermes `wallet_source_convergence`本身仍要处理top20筛选、样本覆盖、公共服务和历史时间。

**检查结果**：本次静态方法用同一组原始mock数据对两条字段路径访问重复读取，得到上述0/20，未启动qb完整CLI、Blix服务、GMGN供应商或Solana RPC；与上一节10.4相互印证，新增的是其**与3项算术反例、样本元数据和产品研究筛选的统一失效链**。

### 11.5 ai-d同输入诊断：分离“新增有效问题”与“模型能力已提升”

本次不能独立启动四个隔离上下文的同型号模型，故按[ai-d既有A0/A1/A2/A1b实验规范](https://github.com/sunshihao001/ai-d/blob/main/evaluation/first-cross-domain-tests.md)执行的是**研究者静态诊断，不是AI A/B实测**。

- **固定输入**：场景05的`mock_inputs`、原`expected_outputs`、Hermes L1定义、qb精确字段路径；任何组都不允许添加虚构的交易签名、结果或钱包身份。
- **无额外解释的既有结果**：mock期望保留`SM accumulating`、风险`critical`、`WATCH`；这是**Hermes历史fixture的期望值，不是Blix当前模型实际输出**。Blix `triage.js`在真实业务中另有`slop/meh/maybe/promising`与活跃时研究升级规则，这也不是此fixture的实验结果。
- **加入知识后的具体新增审查点**：①20个平铺来源值为何在qb变成0？②同源指标的来源是供应商标签还是签名级SOL资金路径？③SM积累与critical风险的证据来自同一批钱包/同一时间窗吗？④观察到Token净库存变化还是只有GMGN历史持仓比？⑤若数据只在结果出现后补齐，这段异常是否真是先兆？
- **实际证据增量**：①字段路径不匹配可静态复算；②`volume_momentum`早期偏差、三标签叠加、AMM spread代理失效有确定性反例；③meme样本“real_pending/true”标记冲突可直接复查。其余机制解释仍是问题，不是经证实的真值。
- **未完成指标**：没有真实独立Blix模型输出与同源/不同源盲审、人工标注的经济控制真值、真实API时间覆盖、误报/漏报统计、推理成本和模型消融，因此**不能宣称AI模型因加载旧知识更准确或发现新Alpha**。

**跨行业专家方法的净贡献**（不是角色投票）：时间序列揭示24倍早期假动量；集合论揭示可疑行为占比非互斥；AMM微结构否定储备价值比价差代理；数据工程识别字段别名和隐式零；样本研究识别`real_pending`与`true`冲突；科学方法要求机制生成后保留竞争解释；产品工程审查Blix旧有发现与研究目标的不同。

### 11.6 对Blix当前产品路线的可检查结论

**不是新增37+16个信号，也不是重写钱包图算法。**

1. **知识上直接阻止三种错误转化**：Hermes旧`volume_momentum`、`insider_activity_composite`、`spread_quality_proxy`不得原样接入Blix的告警、风险或研究优先级；其原问题仍有价值，但需重构测量/计算条件。
2. **同一条异常允许多种研究价值**：`server/triage.js`根据叙事和实时活动升级研究，`server/coverage.js`有5分钟活跃补偿；这是当前已有价值。未来若出现低社交、低成交但复杂的资金/库存接力，研究价值不能被交易候选规则完全替代；应**区分“需要深入研究的异常”与“满足交易条件的候选”**，不意味着绕开安全或额度约束。
3. **旧知识吸收顺序必须改变**：先保留源文件→理解完整模型与条件→复算边界/反例→对照Blix已有模块与数据可得性→记录真正新增、纠正或拒绝的认识→仅在数据与离线验收成立后考虑最小功能变更。"按D01–D12归档"是最后一步，而不是限制探索的前提。
4. **保留UNKNOWN，不强行命名异常**：对于同源、SM、洗盘、内部人、刷量、死亡盘等旧结论，保存“已观察事实/机制候选/竞争解释/可推翻条件/未读字段”，允许将原有标签降级为未知经济现象。
5. **下一轮研究以有价值的未知为中心**：第一优先核Hermes字段的**可复算语义**（时窗、同分母、样本重叠、账户角色和池型）；其次结合qb实际关键地址矩阵查哪些匿名经济活动被前25名筛掉，再用meme真实可核验反证样本检查哪些机制假说站不住。A0/A1/A2/A1b的真正独立模型测评保持`NOT_RUN`。

本节成果：**发现并离线复算三项非平凡旧公式反例、核对两组固定mock别名、发现qb优先级名额冲突、确认meme历史20个反证样本元数据冲突，以及指出两部大稿16项与15项的论证深度差异**。它们改变Blix今后**能不能相信哪一种旧知识**的判定，而不是增加知识卡数量。
