> **Blix 历史知识全文迁入｜参考项目知识研究审计** · [原文](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/reference-projects-meme-knowledge-audit-20261030.md) · 原blob SHA `e42f319561ded6c23ba1818fb89a1f61a635accf` · 领域 D03,D04,D05,D06,D07 · **SOURCE_COPIED / UNVERIFIED**。保留原有研究、假设、争论与状态；旧Grok项目指令与阶段不再具有现行权威。

---

# 项目原点审计｜五个仓库积累了哪些 Solana Meme 交易知识、现在停在哪里

> 2026-10-30。对象：Grok Solana Meme 跟单研究，不是一般AMM教科书。逐库实读关键业务与研究文档、程序，不声称复核几千个文件或独立重新运行历史交易。来源commit固定在文末。
>
> 边界：Why-Solana 文档在本项目 source-admission.v1.json 中仍属于 review_only。本次仅为用户要求的专项知识评审，记录其研究的问题、作者自述结论与暴露的反例；不将其数字当成我们独立复验的市场事实，不修改其来源默认准入。

## 1. 当前阶段：不是缺少入门知识，而是缺少完整的跟单认知链

**实际成熟的部分**：Meme 专用字段与角色语言；候选Mint的入门/二段筛选；早期钱包、dev、sniper、smart money、bundler、转入与分发地址；同源/资金回流/Sybil/Wash的结构线索；筹码剩余、LP风险；FCZ、深洗、死亡盘、POC/AVWAP、二次启动；Evidence Chain、反证和降级。

**局部深入的部分**：原Hermes已将字段分为Raw→Feature→Structure及观察→Gate；meme-深化了FCZ真假形态和反证；qb-已有单Mint关键钱包矩阵与报告程序；当前grok的D05专家已从“同源”深入到风险资本、执行费用、服务收入和经济控制的区别。

**主要断层**：原项目会发现某个Mint里一批“值得关注”的钱包，也会生成结构候选，却没有在本项目自己的连续可见时间、真实钱包行为、剩余库存和双向成交条件下证明：其行为究竟是过去已经完成的优势，还是揭示未来可捕获的市场阶段。这不是补全一般Solana理论就能自动解决的。

**实证与运行状态**：本地已有知识、源码、草稿CI、少量机制推导；当前未验证稳定的实时OKX/RPC K2覆盖、钱包信号到真实quote的连续时钟、可执行净收益、Grok云端S1固定SHA验收。任何外部作者的统计数据都不能填补本项目自己的实证缺口。

## 2. Hermes / SIKK-GMGN：不是工具壳，是市场知识原型

来源：sunshihao001/-。

### 保留的四组专业知识

1. **GMGN字段→市场问题反推**：learning/15-GMGN字段组合地基.md 与 design/phase1-research/00b…00e，已经将市值/流动性、交易、持有人、Top10、权限、creator、发币阶段、社交与热度归类。00c总结“想知道什么事实→什么链上痕迹→哪些字段→字段组合→反例”，并分Raw/Feature/Structure。这是专家按字段提出未知市场机制的原始能力，不只是API列表。
2. **钱包经济角色初分**：learning/10.md 的 early buyer/sniper/whale/SM/KOL/exit/fresh/deployer；learning/11.md 的共同资金来源、时间/成本相似、群体行为与Top10误判；learning/12.md 的Sybil、Wash和协调买入。初版已经知道角色应是候选、事实和推断分离。
3. **籌码状态而非静态Top10**：design/Skill4-筹码控制权状态层设计.md 关注早期钱包与同源群剩余库存、全退/部分退、接收地址、资金回流、Wash风险与信号有效期；并从实体权重中排除CEX/pool/system/burn。这个问题非常贴合Meme的派发与退出，不应被宏观AMM叙述淹没。
4. **证据与决策区分**：learning/13.md Evidence Chain与反证/缺失字段；learning/14.md及16-Gate决策框架理论基石.md将结构观察、条件强弱、TTL和门控决策分开；docs/trading_system_stage_layer_design_v2.md提出结构层、筹码状态层、行为假设层和否定门禁层。

### 必须修正的旧推理

- design/phase1-research/00d 中“同源+同成本+同时间=极高概率同一实体”未经统计标定且特征可能有共同原因；不能以共同服务商/公开发币事件自动判私人同控。
- 旧Skill4的控制状态权重、概率和具体阈值是设计假设，不是已测量的经济受益或操纵概率。
- 00e中“字段穷举/从少量赢亏案例寻找异常”提供探索方法，但不能免除多重检验和样本外审查。
- GMGN字段和标签是旧数据源的语义候选；换OKX不能只改字段名称，必须重新确认单位、时间、覆盖和标签含义。

**当前认知阶段**：已有很具体的Meme钱包/筹码发现框架，经济归因与跟单时差仍未闭合。正确深化重点是这些判断在什么情况下成立、为何失效，而不是从“什么是Token Account”重新讲课。

## 3. meme-：从FCZ结构语言成长到多策略市场认知

来源：sunshihao001/meme-。

**已经研究的市场具体形态**：03_语义概念/第一控盘区定义_v0.1.md、POC与AVWAP重新接受定义_v0.1.md、02_庄家周期/深洗与死亡盘语义深化_v0.1.md，以及策略完善_v0.2/策略状态机规则_v0.2.md，已经细分早期价值区、第一波、深回撤、重新接受、失败反抽、二次推进与死亡风险。

**已经形成的自我否定**：09_规则与回测/反证实验设计_v0.1.md指出“后来没涨就说洗盘没结束”“事后移动POC/AVWAP锚点”等都会让策略不可证伪。策略成熟度质疑审计与商业诊断_v0.1.md提出样本外、复杂度增益、真实成本、失败样本库和简单基准。该仓库自评FCZ“研究中高/样本验证低、B-”属于作者阶段性描述，不能当本项目审计评级。

**重要历史转型**：docs/project_ai_context/12_DIRECTION_SHIFT_MULTI_AGENT.md（2026-06-28）已否定单一FCZ固定买卖流程，改为结构/资金/热度/风险等并行策略视角，研究根据市场状态动态选择。当前grok的多专家体系应继承的是“不将任何一条路径预设为唯一主角”，并非一定在Grok部署21个AI。

**关键未解问题**：图形POC/AVWAP不是已确认的真实同一主体成本；“深洗后回收”也可能是未区分库存与独立承接的价格形态。当前要研究的是链上哪类真实钱包和筹码变化能区分二次启动与死盘，而不是继续给FCZ增加未经验证的阈值。

## 4. qb-：曾经尝试把钱包交易知识实际编码为单币流程

来源：sunshihao001/qb-。

**已看到的实际程序与任务组织**：

- sikk_gmgn_token_report.py：单Mint读取 info/security/pool/K线及多组Top Holder、获利交易者、Smart Money、Bundler、Token转入钱包，组织“币基础→结构指标→关键地址矩阵→基础设施排除→低权重范围→复查计划→总结”，并导出CSV/Markdown。
- 该脚本有L0排除、L1快速扫描、L2早期结构全量；对于LP/pool、疑似中转、分发接收/派发、结果钱包、新钱包狙击和鲸鱼采用不同处理；标记Token/资金来源、钱包行为、持仓比例、已实现/未实现利润与追踪优先级。
- hermes_harness/01_control_plane/skill_map/sikk_skill_to_trading_structure_map_v1.md定义S1候选→S2原始→S3规范→S4污染→S5钱包事实→S6结构关系→S7行为推断→S8结构门控→S9行情→S10安全→S11策略→S12纸面→S13复盘→S14缺口发现→S15知识回流。
- docs/system_cleanup_constitution.md特意强调钱包结构、source_wallet_bot、数据与历史报告是需要保留的知识资产，不应因为旧项目庞大就全部当缓存。

**不可误报的部分**：脚本能生成某字段或文件树里存在历史数据，不能证明其当前GMGN权限可用、钱包分类准确、某次真实交易已复核或某策略有收益。qb的代码、模板与数据结构属于工程/研究原型，不是本项目当前云端稳定运行证据。

**由此识别的真正空缺**：旧程序知道该追哪几个“关键地址”，但没有解决**在具体Mint早期阶段，看到此地址时优势是否已消失、是否有后续独立承接、剩余库存是否会成为卖压**。这应是后续研究起点。

## 5. Why-Solana-Memecoins-Are-Over：外部反例知识，不是可直接继承的市场真值

来源：sunshihao001/Why-Solana-Memecoins-Are-Over；现有准入 review_only，专项阅读了README、docs/RESULTATS.md、docs/PITFALLS.md、economic_mechanics/results.md、funder_network/results.md、post_detection_edge/results.md、known_group_reentry/results.md、entry_zone/results.md、alpha_patterns/README.md。

**对当前Meme项目最有价值的几个问题**：

- **新币创建槽的经济位置**：作者在其特定pump.fun研究中重建发币创建槽内早期购买与之后的外部可进入时间，这提醒我们“最早钱包”和“后来者可见时点”可能不是同一段可复制交易。
- **重复结构不等于同一受益人**：作者研究公开工具、共同资金节点、反复出现的钱包/程序行为时，专门讨论共享基础设施和私人控制的区别。
- **信号 ≠ 正净收益**：其作者自述在特定探测警报、成本与退出模拟下，一些结构特征在测试中具有统计相关或命中率提升，却没有证明可实现正净收益。原库的1,657项报警、11/15主张审计失败等数字均属于**固定样本与研究方法的作者报告**，未被本项目独立复现，不可外推所有Meme。
- **研究能在哪些地方自我欺骗**：事后定义获利群、错误分母、坏连接/缺失值、公共HUB、用未来价格选择入场点、峰值不可成交、几十个候选中挑偶然最佳——这些都是旧Hermes/FCZ/SM评分方法应当主动防范的具体失败类型。

**合理的吸收方式**：作为“旧推理容易在哪一步跳错”的反证素材，仅在专项审计范围内讨论其外部主张；不得因为读了结果文件就解除review_only，更不得转成盈利/亏损普适定律。

## 6. grok 当前真正处于哪个阶段？

已存在：15张旧卡、21份历史固定快照、21个K1按需来源指针（13个Why-Solana review_only、8个context_candidate）、L0–L7 / D01–D12、21专家、152个原子知识目录、D05资金经济职责纵深稿、D08/D09“信号时间→预测增量→净兑现”的研究协议与离线程序/测试。

仍没有：将旧qb的单币关键地址流程和新的钱包→资金→筹码→时间→可跟随性机制贯通的**项目专属专业知识链**；稳定实时K2与完整分母；经过本地复验的价格/执行数据；Grok云电脑S1固定版本实际运行。

**能力阶段判断（非虚构分数）**：

| 专业对象 | 已有能力 | 下一层必须突破 |
|---|---|---|
| 发币候选与市场入口 | GMGN字段体系、二段筛选、单Mint原型 | 换OKX/RPC后的语义、可见时间与真实覆盖 |
| 早期钱包/SM/狙击/Dev | 角色标签丰富、状态候选和关键地址追踪 | 分清发现/速度/资本/受益/库存管理，不以标签当盈利本领 |
| 同源/资金回收 | 旧资金图+新D05经济职责深入 | 能否解释真实风险库存与时间顺序，而非认定庄家身份 |
| 筹码/分发与控制 | Skill4实体权重/剩余率/清仓/分发设计 | 把自由可卖库存、LP/托管、真实退出冲击和阶段变化接起来 |
| FCZ/深洗/二次启动 | 具体行情语言、状态机与反证意识 | 用钱包与资金行为区分真承接、短暂反抽、死盘，拒绝事后定义 |
| 跨币/群体/叙事 | 有方向与候选观察模型 | 资金重复部署与公共消息同步的差异、下一Mint何时可知 |
| 跟单剩余信息 | 已认识时间/增量/兑现三断层 | 在项目实际研究对象上解释什么时候可跟、何时只能观察 |
| 执行与验证 | 知道费用/卖出/反证重要 | 仍无完整本地实时可执行成本与K2经济验证 |

## 7. 必须把上一轮M01改成项目专属问题，而不是通用金融学题

**撤回主线表述**：“先系统研究Solana Meme所有AMM价格形成，之后才理解钱包和筹码。”它能提供基础知识，但和现有积累的业务认知差距不直接对应。

**新M01项目主问题**：

> 旧qb为何把一个新发Mint中的某些早期买家、SM、Bundler、Transfer-in、Top Holder划成“关键钱包”？这些钱包在创建slot、曲线、迁移后分别做了什么；其中多少只是GMGN标签，多少是swap/转入/费用服务/持币/退出事实；我们何时能知道其动作？这份信息对以后还有什么用？

**实际研究关系**：

新Mint的准确阶段 → 候选钱包标签与交易事实分离 → 买入/转仓/分发/历史PnL → 本金与执行服务区分 → 真实剩余Token库存 → 公开事件与服务商available_at → 当前及下一阶段的可卖/买入条件 → 决定用于研究预警、风险过滤、二阶段机会候选，还是不值得机械首买跟单。

**专家组织**：E-L4-02（跟随者剩余信息主专家），E-L3-01（钱包角色）、E-L3-02（资金经济组织）、E-L3-03（库存）、E-L1-02（时点）与E-L2-01/02（具体发行与池），按知识盲点出现时参与，不需所有专家轮流表态。

**优先研究单元**：D04-K02/K03/K04/K07，D05-K01/K02/K03/K06，D06-K05/K07/K09，D07-K01/K02/K11/K12，D08-K02/K03，D09-K01/K04。D01、D02、D03、D10按对应真实业务难点补充，而不是先上十二节AMM课程。

**后续主线建议**：M02 关键钱包的派发/剩余筹码与FCZ真假二阶段；M03 跨Mint资金复用与Dev系列/市场注意力；M04 多策略信息价值与真实跟单经济；F01 按需追溯Solana/OKX字段和具体协议。各研究仍先做理论专业推演，实证单独审查。

## 8. 项目专属性的强制检查

每次提出新的纵深研究题目，先能回答：

1. 这个题目继承哪个旧项目的**具体Meme知识或程序判断**？给出文件与原始业务角色。
2. 原方法曾回答什么？哪些证据或市场阶段决定它的含义？
3. 旧方法为什么不够：在哪个**钱包/资金/筹码/时间/跟单**连接处跳了步骤？
4. 需要哪位现有专家、哪几条Dxx-Kxx，**按需**补哪条协议/AMM/数据知识？
5. 研究完成能够对“该跟谁、为什么不能跟、什么时候改为只监控/风险排除”产生怎样的认知增量？若当前题目不能连到项目真实目标，就先降低其主线优先级。

**最终结论**：知识目录已够大；眼下的主要任务是**用旧项目已有的钱包、资金、筹码、FCZ与门控经验，把“关键钱包识别→时点→库存→后续可用信息”研究成完整机制**，而不是让通用市场原理成为主角。

## 原始引用与固定版本

- Hermes: https://github.com/sunshihao001/-/tree/2bf694b37cce25b4a3c9364298b784039f3ecc84
- meme-: https://github.com/sunshihao001/meme-/tree/5ab2b01f08e4e512fa4fcd1aed88953ff534bd0a
- qb-: https://github.com/sunshihao001/qb-/tree/8377ad5611255df5cd4562666a826708575334f0
- 外部研究（仅review_only专项）：https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/tree/9a7ad51d56328e91e67e3f531d6744307d0ee68b
- OKX接口候选: https://github.com/okx/onchainos-skills/tree/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25
- Grok原来源审计：docs/grok-cognitive-source-audit-2026-10-30.md；当前运行状态：docs/project-baseline-2026-10-30.md

## 2026-11-02 补充核查｜被历史摘要遗漏的多跳调查能力

> 本段是2026-11-02的新增源码核查，**不是改写2026-10-30原点审计的当时结论**。遵守Why-Solana `review_only`：可以读源码与方法、比较设计和反例；不能把作者数字自动当本项目真实复核、同控真值或Alpha。

1. **Hermes旧知识已有正确的研究入口**：`learning/11.md` 明说中转钱包和拆分路径可能掩盖同源；`design/phase1-research/00c` 已按“市场问题→链上痕迹→字段组合→反例”推进；`00e` 已提出无标签发现与异常驱动。但`00d`把同源、同成本、同时进场作为“极高概率同实体”，其数值和证据独立性未经校准，不能直接继承。
2. **qb-并不只做单币静态标签**：`sikk_gmgn_token_report.py` 已将“可疑中转节点”“分发接收钱包”“Token来源/去向”“资金来源类型”和LP/Pool隔离为不同业务记录，已有“追查下一个关系节点”的产品意图；程序未形成经独立验收的多跳持续调查。
3. **Why-Solana已有明确的多跳源码和实验设计**：`funder_network/code/fn_trace.py` 含 `MAX_HOPS=5`、`HOP_WINDOW=7*86400`、`HUB_N=3000`、`MIN_SOL=0.1` 与RPC缓存/分页停止；`analysis_plan.md` 规定上下游扩展、先后时间、已知角色、Hub/查询预算和`UNRESOLVED`终止类别；`fn_20_build.py` 有数据冻结、去重、时序及Hub完整性检查。它已经实现的是**受限图调查方法**，不是无限历史追溯或最终控制权确认。
4. **作者结果不是本项目的链上实证**：其`funder_network/results.md`自述以62个主要钱包为起点，报告55条上游路径、408个下游分支、13条经过8个桥接地址的有序跨群体序列；活跃地址受到抽样、有限调用和5跳边界。报告还明确说明SOL具有同质性，有序入账/出账不能证明相同lamports流转。此处只记录作者自述及可检查的研究方案，未本地重放全部RPC结果。
5. **与Million形成跨项目反例**：Million `apps/api/src/analysis/owners.service.ts`以funding/fee payer边聚合候选群组，排除高连接度Hub且不让co-entry直接合并；共享执行或服务节点足以造成错误的同控推断。图的边必须分别保留经济语义，不可把“可达关系→共同控制”当作通用规则。

**这次补充修订的原问题**：为什么既有知识中已经有“中转、同源、群体继承、多跳”，后续研究仍反复从头选择解析器或搜API？因为多数历史成果被存为“字段/项目/功能”而非“市场问题→可继续调查的证据→竞争机制→下一项值得获取的数据”。今后先恢复既有源码/实操经验，再评估OKX、GMGN、Bubblemaps、Bitquery、Nansen等成熟数据能力能否直接补齐调查边；只在额外证据可能改变解释时继续调查，并在原D04–D07/D10–D11专题原位修订。不扩建第二套专家或知识目录，不将本次补充视为V0.2多跳功能已验收。

原始研究入口：
- [Hermes 00c](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00c-GMGN-%E6%80%9D%E7%BB%B4%E6%A8%A1%E5%9E%8B%E6%8F%90%E7%82%BC.txt)、[Hermes 00e](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00e-%E5%AD%97%E8%8A%82%E5%8F%8D%E6%8E%A8%E6%A1%86%E6%9E%B6-%E7%AA%81%E7%A0%B4%E8%AE%A4%E7%9F%A5%E5%B1%80%E9%99%90.txt)
- [qb-单Mint报告](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)
- [Why-Solana研究方案](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/analysis_plan.md)、[追踪代码](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/code/fn_trace.py)、[结果（作者报告）](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/main/funder_network/results.md)
- [Million聚类源码](https://github.com/Kelows/million/blob/c89ad07caaf70773d40b45943e136eadc4f946a5/apps/api/src/analysis/owners.service.ts)


## 2026-11-02｜qb旧GMGN字段和当前官方契约的条件性不兼容（多领域高信息价值审计）

**来源实际代码**：旧 [qb- `sikk_gmgn_token_report.py`](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py) 的 `fl`对无法`float()`的值返回默认；`price=fl(info.get("price"),0) or 0`，`price*supply`生成“当前市值估算”；`info.get("持有人数量")`、`dev.get("创建者地址")`、`link.get("官网")`直接写出报告。

**独立当前契约**：[GMGN官方`skills/gmgn-token/SKILL.md`](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-token/SKILL.md) 说明 `token info` 当前为 `price`对象，USD报价字段应取`price.price`；持有人数 `holder_count`，开发者地址`dev.creator_address`，官网`link.website`。这与旧qb相应解析存在**可定位的结构/字段名差异**。

**合成独立检查（非GMGN真实授权返回，非qb原程序运行）**：给旧字段提取逻辑一个符合GMGN当前文档结构的JSON样例：`price={"price":"0.0000025"}, circulating_supply="1000000000", holder_count=1250, dev.creator_address=示例合法形状地址, link.website=https://example.org`。按旧`fl`规则，嵌套对象不能`float()`，得到`price=0`、`market_cap=0`，中文键的Holder数、Creator和官网缺失；按当前文档键则是报价0.0000025、估算市值2500（单位按假设字段）、Holder1250及非空Creator/官网。五个测试字段均有不同结果。**这个演示只验证条件性不兼容，不代表旧GMGN CLI `--raw`在当时就是今天的JSON结构**，也未检验2026当前CLI实际授权响应。

**为什么这是全局优先级而不是一个小API问题**：
- D02发行者/社交：Dev/官网字段缺失会扭曲发行者历史与社会传播研究入口。
- D03/D09市场价格与执行：可用报价变成0会连带市值/流动性比率和后续经济成本推理失真。
- D04/D06钱包与筹码：Holder统计缺失会干扰持有群体分母及结构解释。
- D10/D11供应商可靠性与验证：用`or 0`会把`字段不匹配/无数据`无声伪装成真实价格0；最终可能在新一轮报表中形成“已计算”的虚假结论。
- D12复用与产品：旧qb的“币基础→结构→关键钱包→基础设施剔除→复查计划”**整体业务调查思路值得继承**，不能在未经实际契约验收前直接复用该脚本的旧字段或未经校准的筛选阈值。

**裁决**：已有成熟GMGN Skill和OKX全景工作流优先按真实当次授权响应建合同，再用旧qb的业务矩阵组织报告；对于没有来源、响应格式不符、字段未返回，应输出`UNKNOWN / DATA_CONTRACT_MISMATCH`而非0。不要为此新造数据平台或增加一个新专家；先复用原始JSON与官方文档核对必要字段，再决定是否采用该旧程序的部分输出语义。

**研究成熟度**：两份固定来源源码/文档已核，离线条件性解析反例已核；尚无真实GMGN授权CLI返回，也没有对旧qb所有字段逐个做端到端对照，不能将本节当成已修复qb运行时。



---

## 2026-11-06｜Hermes × qb- × meme- 原始知识纵深与跨学科反证（SOURCE_READ，不等于全库验收）

**本轮问题**：此前“参考项目→功能标签→Blix模块”过早裁剪原始知识，特别是旧Hermes如何提出新框架、qb-如何组织可复查对象与证据、meme-如何证伪后验市场解释之间的联系。坚持把旧项目当独立研究对象；下面给出**已读原文的具体认识**，未读的原库文件绝不等同已覆盖。

### 1. 知识覆盖状态及此前错误简化

- **[旧Hermes](https://github.com/sunshihao001/-)**：本轮通过 Git 树确认264个文件；深读 [00c 思维模型](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00c-GMGN-思维模型提炼.txt)、[00d 多维推理](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00d-GMGN-多维度推理扩展.txt)、[00e 反向生成](https://github.com/sunshihao001/-/blob/main/design/phase1-research/00e-字节反推框架-突破认知局限.txt)、[研究拷问记录](https://github.com/sunshihao001/-/blob/main/design/phase1-research/grill-sessions/2026-05-26-grill-bytes-to-framework.md)、[钱包结构设计](https://github.com/sunshihao001/-/blob/main/design/phase1-skill-04-wallet-structure.md)、[筹码控制状态草案](https://github.com/sunshihao001/-/blob/main/design/Skill4-筹码控制权状态层设计.md)。**未完成**学习资料、源码和全部测试的逐条覆盖。
- **[qb-](https://github.com/sunshihao001/qb-)**：目录发现4236个文件，3338个落在data/、610个在hermes_harness/；这不是4236项不同专业结论，更不是4236次有效实盘。已读 [单Mint报告脚本](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py)、[4TKY摘要](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/summary_overview.md)、[同一Mint的标准化钱包交易](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/wallet_data/normalized/wallet_trade_normalized.json)、[资金边CSV](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/structure_analysis/wallet_fact/fund_flow_edges.csv)、[判断候选](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/structure_analysis/intelligence/wallet_intelligence_decision.json)，以及 [防假完成](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/22_anti_self_deception/README.md)、[真实任务回放边界](https://github.com/sunshihao001/qb-/blob/main/hermes_harness/23_real_task_regression/README.md)。大量历史原始文件和测试未逐项复核。
- **[meme-](https://github.com/sunshihao001/meme-)**：目录发现474个文件，涵盖外部资料吸收、市场定义、规则、标注、消融和工程；非单纯K线策略仓。已读 [FCZ定义](https://github.com/sunshihao001/meme-/blob/main/03_语义概念/第一控盘区定义_v0.1.md)、[深洗/死亡盘](https://github.com/sunshihao001/meme-/blob/main/02_庄家周期/深洗与死亡盘语义深化_v0.1.md)、[反证设计](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/反证实验设计_v0.1.md)、[消融模板](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/消融实验执行模板_v0.1.md)、[反证字段](https://github.com/sunshihao001/meme-/blob/main/07_样本标注/GMGN反证样本库字段表_v0.1.md)、[策略自审](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/策略成熟度质疑审计与商业诊断_v0.1.md)、[FCZ_B_0001](https://github.com/sunshihao001/meme-/blob/main/07_样本标注/样本记录/FCZ_B_0001.md)、[FCZ_D_0001](https://github.com/sunshihao001/meme-/blob/main/07_样本标注/样本记录/FCZ_D_0001.md)。没有完成逐Mint独立链上复算。

### 2. Hermes真正独特的认知链，不应降格为“钱包标签”

**第一层，问题驱动的可观察量设计**：00c 从“要理解什么市场事实→什么链上痕迹→供应商哪个字段可能观察→哪些字段联合→需要哪个分母”反推派生特征。其“选分母=选比较背景”可迁移到持仓占比、钱包活动比率、资金路径覆盖和池深度，并且与 Blix 当前不同模块分母不一致风险直接相关。旧文将 GMGN 聚合字段视为Canonical，并非Solana原始事件；需要保留中间处理层，不能改叫真正raw chain fact。

**第二层，同一证据下的多问题表征**：00d 将同一字段分别问钱包角色演化、钱包行为相似、市场微结构、资金组织生命周期、策略适用环境。研究价值是**切换要解释的对象和尺度**，而不是“维度越多标签越准”。其中“同源＋入场时间/成本相近→极高概率同一实体”没有经审定的先验、基准率、独立证据或对照，必须降级为有竞争解释的同源/同步候选。微结构部分用K线位置代理实际买压也只能作代理，不能等同主动买卖成交量；写出的“庄家阶段”尤其不能从价格形状直接确定真实主控人。

**第三层，从意外中生成未知**：00e 提出枚举字段组合、极端异常、无标签聚类、对立假设、时间序列和跨链比较。这些是**假设发现工具**而非已知市场机制。所谓“5–10%完全想不到的组合”等比例无实证依据；80个字段两两组合已有3160种，若后续还搜索多函数、时窗、阈值，会明显放大选择偏差与伪发现。正确迁移的是：先发现意外 → 生成竞争性机制 → 冻结可观测区分标准 → 用不同时间/不同Mint留出样本检验；不能“发现形状就命名为新真值”。

**第四层，库存与时序不能被资金标签吞并**：[筹码控制状态层](https://github.com/sunshihao001/-/blob/main/design/Skill4-筹码控制权状态层设计.md) 已提出实体剩余库存、流入/流出/回流、已清仓实体权重、公共设施排除、时间新鲜度、状态转移与 UNKNOWN。其真正价值是“角色/资金网络应与剩余可售库存和行为变化共同分析”，而非继承未校准的控制权概率、贝叶斯似然和设计数值。

### 3. qb-的独有价值：对象选择、证据拆分、演化记录与反证

- 原 [单Mint报告脚本](https://github.com/sunshihao001/qb-/blob/main/sikk_gmgn_token_report.py) 不仅输出角色标签，还输出分析深度、代币基础、结构指标、关键地址矩阵、**基础设施登记、低权重范围、后续复查计划**等；方法价值是成本受约束时仍保留被忽略对象与跳过理由。其分级阈值/供应商标签是旧假设，不直接复用。
- 4TKY [早期摘要](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/summary_overview.md) 报94条wallet_trade、missing_trade_records=94、交易总数0；**另一个同Mint标准化交易文件**记录record_count=95并有buy/sell记录。可能是**不同时间批次/不同数据来源/报告未同步**，本轮未证明程序统计错误；恰恰说明不能把同一Mint不同阶段的结果无版本对齐地拼成“完整结论”。
- 4TKY [资金边CSV](https://github.com/sunshihao001/qb-/blob/main/data/source_wallet_bot/live/4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump/structure_analysis/wallet_fact/fund_flow_edges.csv) 的金额、时间为unknown，relation_type是pre_buy_funding_candidate，来自GMGN native_transfer L1，却给数值confidence_score=0.6；这个0.6不是已校准的实际共控概率，且缺少原交易签名/金额/时间，因此仅可用作**补查队列与数据缺失反例**。旧决策文件E3/E2等分级也不能升级为经济实体确定性。
- [hermes_harness](https://github.com/sunshihao001/qb-/tree/main/hermes_harness) 具有防假完成、真实任务回放与上下文/权限校验研究；此部分与 ai-d 对模型是否真的完成、历史知识是否误用的研究相关，不能当作纯钱包代码遗弃。但历史测试夹具通过不能代表 Blix 本地实跑。

### 4. meme-的独有价值：从“有漂亮解释”转向“有可推翻的解释”

- FCZ定义中“成本共识”“控盘区”是经济机制**假设**，POC/AVWAP 是价格×成交分布的**统计代理**；不能从成交密集区直接反推特定控制者的真实建仓成本。
- [反证设计](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/反证实验设计_v0.1.md) 包括“规则符合但失败”“规则不符合却大涨”“死亡盘误判”等，要求冻结规则与事前信息、不事后更改边界，是独特且可迁移的**市场解释失败登记**办法。适合 Blix 异常监控的误报/漏报追踪，不要求先建立交易策略。
- [消融模板](https://github.com/sunshihao001/meme-/blob/main/09_规则与回测/消融实验执行模板_v0.1.md) 将复杂结构与POC-only、AVWAP-only、sweep-only简单基准比较；**当前仅实验模板**，不能声称策略有效。
- [FCZ_B_0001](https://github.com/sunshihao001/meme-/blob/main/07_样本标注/样本记录/FCZ_B_0001.md) 仍为空模板；[FCZ_D_0001](https://github.com/sunshihao001/meme-/blob/main/07_样本标注/样本记录/FCZ_D_0001.md) 有WORLDCUP候选快照和GMGN来源，但`sample_source=real_pending`同时`is_real_sample=true`，且候选/trending 与token快照的 holder_count 和 liquidity 显著不同，未确认同时间/同池/同语义；应视为**来源与复算待审**，不能当作成功反证完成的“实证样本”。
- 深洗/死亡盘文档的部分定义含“后续恢复才算深洗”，容易造成**事后看结果给历史时点标签**。若Blix要在t时预测，必须只用t时可获得的信息；事后定义可用于生命周期归档，不能伪装成t时可判定的预警。

### 5. 借用跨学科专业视角做竞争性重建（各为分析方法，不虚构专家参与）

| 视角与可核验经典来源 | 给旧项目的审查问题 | 对 Blix 判断的实际改变 |
|---|---|---|
| **科学哲学／溯因推理**：[Peirce研究说明](https://plato.stanford.edu/entries/peirce/) | 意外观察能否生成几个真正不同的解释？每个解释推出什么可观察、可被否定的后果？ | 00e生成的是“候选解释”，不是新增真值；把替代假设与缺证据连接回调查任务 |
| **统计学／多重比较**：[Benjamini–Hochberg 1995](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) | 3160+字段组合、不同阈值/窗口反复搜索是否产生伪发现？有没有冻结定义、留出样本、选择偏差记录？ | 先做探索、稳定性/负例与样本外确认，再考虑提升为长期知识 |
| **流程挖掘／序列行为**：[IEEE Process Mining Manifesto](https://tf-pm.org/resources/manifesto) | 原始事件是否完整？转币→换钱包→出售与普通路由/共享平台的事件序列如何区分？缺史能否导致沉默假象？ | 从静态Holder关系升级为有覆盖说明的时间事件链与机制候选；不要求复制固定序列标签 |
| **实体解析／因果推断**：[记录链接方法综述](https://academic.oup.com/ije/article/45/3/954/2572621)、[Pearl因果推断](https://proceedings.mlr.press/v6/pearl10a) | 同源/同步/共享地址是关联还是同控？是否有共同服务、热门事件、采样机制这样的替代原因？ | 分离钱包地址→行为关系→经济主体假说；不同证据层分开，不把图簇自动当“庄家” |
| **数字取证／证据工程**：[NIST SP 800-86](https://csrc.nist.gov/pubs/sp/800/86/final) | 来源是否可复核、事件/抓取时间、原始快照版本、缺失情况是否清楚？ | qb- 4TKY摘要与后续规范化数据必须区分批次；保留SOURCE/TIME/COVERAGE，修复可追溯性 |
| **机器学习／概念漂移**：[Gama等2014](https://doi.org/10.1145/2523813) | 原来有效的钱包形态、模式阈值、供应商口径在不同发行平台/时间段是否仍成立？ | 区分概念发现、时间条件下的失效与阶段转换；避免静态标签恒定化 |
| **产品与系统工程**：[视角结合的架构逆向研究](https://www.sciencedirect.com/science/article/pii/S0164121224003212) | 旧文档的专业意图和旧代码实际执行、测试覆盖、界面表现是否一致？ | 用现有 Blix 事实/API/UI 承载新的报告语义；确有缺口才选择小改、外部复用或产品方向调整 |
| **AI认知与知识调用**：[ai-d知识组织协议](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/organization-protocol.md) | 是否因为Blix当前没有模块就丢掉独有知识？是否历史全文注入导致认知退化？ | 独立研究深度与运行时按需调用分开；按实际问题检索有关原文，不创建固定“专家Bot” |

### 6. 三种互相竞争的机制解释示范

假设未来某Mint观察到：早期A/B/C收到同一来源资金，在短时间买入；随后部分Token转到D/E；D/E卖出，价格没有明显下跌。

- **H1：组织性库存转移/分发并出货**。预期：可跨时间重现有方向的资金/Token接力、原群体库存净减少、接收方后续有可归因出售；控制权身份仍UNKNOWN。
- **H2：独立买家与共享服务/路由造成的表面连接**。预期：共同入口是CEX、路由、公共资助平台，分组跨大量无关Mint出现；精确Token转移链或独立资金闭环不足。
- **H3：套利、做市或跨池再平衡**。预期：同签名/近时间存在对价腿、多池资产与库存变化，净风险敞口与简单“单向出货”不一致。

**决定性研究不是让AI三选一**，而是根据可检验的区分信息，查签名、动作位置、Token Account/Owner、SOL/WSOL与手续费、池和公共设施、时间覆盖、跨Mint复现与反面案例。某些假设无法仅链上识别，保留UNKNOWN；不得因为“价格没跌”自动改称吸筹。该场景是分析设计，不是真实Mint实跑。

### 7. 这次认识具体改变Blix什么，怎样限制融合？

1. **知识对象从“功能标签”升级为“问题—证据—机制—反证—适用条件—相邻知识”的连接**；保存旧来源全目录、变更/测试线索，未审阅保持UNKNOWN。无需每个文件新建知识卡；特别有认知增量的原理优先补到既有 `methods/mechanisms/cases`。
2. **知识可深化≠都必须写进运行时**：实际用户调查只调用相关原文和具体反例；不把Hermes 00d/00e不可靠阈值、Bayes伪精度、qb-启发式E分级与meme-事后FCZ判断升为默认真值。
3. **业务实现不只看当前Holder或价格图**：优先复原地址—转移—库存—时间—资金来源—下一Mint之间的可追溯事件关系；解决不同模块分母、Fee Payer误认funding、历史截断、数据延迟后，再做机制解释。
4. **完整产品仍是Blix**：参考成果可以改变Blix业务调查输出、未知问题空间和下一项成熟能力复用决策，不需要重做终端或照搬旧Bot/规则。继续静态只读，未修改交易业务/启动服务。

### 8. 下一轮必须回答的高信息价值问题（联合研究，不是单点修复）

**纵深**：继续核读Hermes 00b/字段契约、Skill 8 状态机及关联测试，验证“观察→角色→群体→库存→机制”在哪一步丢失身份和时序；核读qb- 4TKY数据批次、生成记录与完整链上证据，解释94 vs 95、funding边缺amount/time；核读meme-真实/待验证样本和前瞻/事后定义，找出能够独立重放的反证样本。

**横向**：以相同Mint和同一时间窗口，对照Blix现有`coin/holders/bubblemap/wtrack`与Million资金分析、Pulse历史快照、PumpTrace回补的实际代码语义，识别真实缺口、公共设施误报与来源缺口。**仅做静态原代码与现成样本核查，未授权实跑则不启动**。

**认知实验候选**：给AI同一“钱包接力+出货”问题，比较只用Blix事实、按需引入Hermes+qb-+meme-原始研究、再加入外部实例的三个条件；由独立事实和盲审检查“发现未知、假设可区分性、错误归因、缺失保真与用户介入”，不能以AI回答丰富度证明融合成功。

**验收边界**：本轮已核查以上特定文件并提交研究修订；没有复算4TKY链上交易、没有跑Blix或旧程序、没有证明概率分数、策略收益或主体能力已增强。知识回填位置仍是本审计与原Blix已有导航，不新增Bot/强制阶段。
