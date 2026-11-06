# Hermes逆向发现 × qb事实证据 × meme反证：跨学科认知深化（V0.2）

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
