# Blix 参考项目与未整体搬迁资产入口

本目录存放的是**对成熟项目的知识研究与复用经验**，不是这些第三方项目的完整代码仓库；用户后续只运行/使用Blix。原版保留在各自仓库，是否移植业务实现需要以后单独审查许可、依赖、安全、费用和功能重叠。**不要将第三方README的功能说明当Blix已具备或独立验收。**


## 2026-11-06 研究入口纠正｜先独立理解项目，再决定如何融合 Blix

**本节修正此前“按 Blix 已知功能缺口筛选参考知识”的单向局限，而不取消成熟产品优先、事实核验和只读安全要求。** 参考仓库不是待拆的组件仓库，也不只是旧 D01–D12 分类的填空材料。它可能含有 Blix 尚未提出的问题、新的经济解释、异质的数据组织办法、工程失败经验、作者设计判断和与当前认知相矛盾的证据。

**研究与迁入分成两种不同工作**：
- **项目独立知识研究**：先恢复该项目原有的目标、用户业务、页面/API、源码流程、数据模型、依赖、时间窗口、测试/反例、设计权衡、历史演化及作者明确说明的理由；以实际模块/主张为单位渐进深读。发现原分类无法容纳的问题时，保留原名与跨域链接，不能因为目前 Blix 没对应模块就提前忽略。
- **跨项目认知合成**：对同一专业现象比较不同项目怎样定义、计算、验证和处理失败；寻找矛盾、独特假设及尚无答案的问题，结合可靠协议/理论/实例反证；区分代码可观察事实、作者主张、推定设计理由和独立验证。
- **Blix 产品吸收**：上述认识形成后，再分别决定保留为研究来源、补入原有 `foundations/mechanisms/methods/cases/ai/references`、修订旧主张、转反例测试、复用接口/程序、或提出改变产品方向的候选。**没有当前实现落点不等于没有研究价值；重复实现不等于重复知识。** 不自动引入交易/签名/支付或未经核验的第三方代码。

**覆盖要求不是“每个文件都新建一张卡”**：保留原项目完整目录清单，逐主题核查文档、实现、测试、历史与失败反馈；每条重要主张至少能回溯到代码路径/来源版本，说明它回答的问题、使用前提、竞争解释、限制、待补证据及知识关系。没有查过的标记未审阅，只有扫过目录的标记目录已发现；不把“全量扫描”说成“每个知识点已理解”。研究可循证据价值分批推进，保持业务交付并行，不要求先读完65个项目才能完善 Blix。

### 第一批跨项目源码试读：意外发现与延伸问题（仅 SOURCE_READ）

| 项目/原始代码 | 已观察到的独立知识点 | 值得继续验证的关系与未知 |
|---|---|---|
| [Million copyability.service.ts](https://github.com/Kelows/million/blob/main/apps/api/src/copyability/copyability.service.ts) | 以同池分钟K线对比鲸鱼实际进出时点及延后60秒进出，测算“可复制性”而不只计算历史钱包盈利；采样最近成交并限制成本。 | 真实净优势还受到传播延迟、滑点、容量、漏掉的样本和幸存者偏差影响；这套价格代理并非真实成交复现。对 Blix 的价值不限于钱包发现，还涉及信息时效与市场微结构。 |
| [Million decision-log.ts](https://github.com/Kelows/million/blob/main/apps/api/src/common/decision-log.ts) | 记录跳过/接受决策的阶段、代码和理由；异步写库失败被静默忽略，有保留期。 | “为什么没选中”与“是否完整记录所有判断”分开；日志缺口不能误当未发生。 |
| [Pulse merge.ts](https://github.com/nirholas/pulse/blob/main/src/collector/merge.ts)、[solana-stream.ts](https://github.com/nirholas/pulse/blob/main/src/collector/solana-stream.ts)、[restore.ts](https://github.com/nirholas/pulse/blob/main/src/archive/restore.ts) | 多源观察采用先到优先的补缺合并；部分乱序旧交易计入最新滚动桶；历史存档按可变状态upsert/事件去重恢复。 | 来源冲突如何可见、乱序时间是否产生虚假异动、快照与事件历史怎样分别保存及验收；不能只把Pulse当榜单服务。 |
| [PumpTrace backfill-manager.mjs](https://github.com/AntC215/Pumptrace/blob/main/src/modules/backfill-manager.mjs)、[interpretation-engine](https://github.com/AntC215/Pumptrace/blob/main/src/modules/interpretation-engine/analyze.mjs) | 历史回补状态、游标与恢复边界细化；直接Creator Token转移可证明一条链上关系，不等于接收方身份。 | 数据覆盖改变何种主张可以成立；如何区分具体资金关系与“控制权”标签，评分阈值如何校准。 |
| [HoldTech holder-overlap](https://github.com/co-numina/holdtech/blob/main/app/api/holder-overlap/route.ts)、[deep-scan](https://github.com/co-numina/holdtech/blob/main/app/api/deep-scan/route.ts) | 以有限Owner样本构建跨币地址重合的几何均值评分并映射“协同”等级；深查中还研究同槽、资金与集中度。 | 重合地址的抽样偏差、公共服务/独立交易者与同控的竞争解释、误报率；不能将评分名称直接当经济主体真值。 |
| [PumpGrok ARCHITECTURE](https://github.com/swcstudiospace/PumpGrok/blob/main/ARCHITECTURE.md)、[SAFETY_INVARIANTS](https://github.com/swcstudiospace/PumpGrok/blob/main/docs/SAFETY_INVARIANTS.md) | 区分Agent指令包、工具注册、Paper回放、后台服务；项目列出不变量与测试归属，但部分文档为设计且候选发现命令标为未实现。 | 将“设计上要求/源码确有/测试存在/离线通过/真实运行”分开；研究可追溯的责任、回放与失败恢复，不只看其插件目录。 |

**本表是候选知识入口，不是五个仓库已完成逐文件深审、实际测试或项目融合。** 后续原点深读必须追踪这些知识点与其它模块/设计/变更的关系；必要时新增原本没有提出的专业研究问题，而不是仅把它们映射到 Blix 的已有页面。此前65项参考资产保持来源登记，不自动宣布其余项目审查完成。

## 已保留在Blix的全文历史研究
- [旧Grok 五项目专业知识审查](legacy-reference-project-knowledge-audit.md)：旧行业产品的真实研究问题与可复用逻辑。
- [旧Grok 多跳资金与供应商证据审计](multihop-funding-evidence-audit.md)：多跳识别、公共设施和反证。
- [旧Grok 成熟参考能力复用完整台账](legacy-reference-capability-ledger.md)：较长原始审计；先按具体项目名称或业务问题定向检索，不全文注入模型。

## 外部参考项目（当前保留原文和成熟思路，不整包复制）

| 参考 | 原始项目 | 首要知识用途 |
|---|---|---|
| Million | https://github.com/Kelows/million | Mint↔钱包发现、资金/交易候选、历史窗口与排除理由 |
| PumpTrace | https://github.com/AntC215/Pumptrace | Creator归因、证据分层、历史回补、调查报告 |
| Pulse | https://github.com/nirholas/pulse | 发行生命周期、历史档案、MCP/数据来源 |
| HoldTech | https://github.com/co-numina/holdtech | Holder集中度、钱包质量、快照演化 |
| PumpGrok | https://github.com/swcstudiospace/PumpGrok | AI任务说明、Skill组织、执行收据、安全隔离 |
| OKX OnchainOS | https://github.com/okx/onchainos-skills | 已包装链上只读调查及数据工作流 |
| pumpwatch | https://github.com/cinder-security/pumpwatch | 可复现发行样本及经济行为反证 |
| Why-Solana | https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over | 多跳方法、相关主体与共享服务区分 |
| 旧 Hermes | https://github.com/sunshihao001/- | 钱包角色、资金、筹码、指标推理与历史设计 |
| 旧 qb- | https://github.com/sunshihao001/qb- | 单Mint关键地址矩阵和复查组织 |
| 旧 meme- | https://github.com/sunshihao001/meme- | 经济机制、失败市场形态、策略候选 |
| ai-d | https://github.com/sunshihao001/ai-d | AI问题表征、知识适用、认知提取、目标演变 |

**完整65项参考登记**：仍以旧Grok [gpt-meme-project-index.v1.json](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json) 为来源，而不是仅依赖本页的示例短名单。

## 尚未全文迁入但不会丢失的老资产

- 旧Grok [system目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/system)：旧执行制度、长期进度、项目收束、专家手册、来源登记、原始152单元本体；**不把过去固定执行制度复制成Blix强制指令**。主册和机制研究方法已迁入。
- 旧Grok [legacy-snapshots目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/legacy-snapshots)：更早知识文件及理论副本，适合需求出现时专项核对，不是全部现行有效。
- 旧Grok [transfer目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/transfer)：历史教学与迁移实验；当Blix需要教学/工作交接时再评估。
- 旧Grok [experiments目录](https://github.com/sunshihao001/grok/tree/knowledge/whole-spectrum-20261030-v1/knowledge/experiments)：执行边界的历史实验资产。
- 历史工程 [PR #16](https://github.com/sunshihao001/grok/pull/16) 与 [PR #17](https://github.com/sunshihao001/grok/pull/17)：代码/离线实验和迁移实践应单独审查，不当作文档迁移就已完成产品能力。

此页为来源索引，不代表每个链接已实时验证、每个参考项目知识已审查完毕或旧知识全部完成迁移。可用[迁移清单](../MIGRATION.json)判断具体状态。
