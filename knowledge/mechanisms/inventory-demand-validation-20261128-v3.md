# MEME 经济主体、真实库存迁移与市场需求机制深度实证 V3.0
日期 2026-11-28。基线 01e7725d8337ade7ffce997d08459de1f4b63152。状态 PUBLISHED_EVENT_RECALC / SOURCE_AUDIT / PARTIAL_FLOW_RECONSTRUCTION；非独立节点核链、主网回放、完整经济主体归因、盈利实证。只读研究，无运行代码变更。
## 1. 同一批发行的买入—退出连接审计
来源原作者 https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over ，不是旧fork。实际读取 data/v06_curve_ladder.json (blob bf01bdfecbf97365d56b5e45572e94869683bf39)、data/v07_exit.json (bcb6cf9d25d1ead4f07478a8cdd924d8b2ea363d)、code/v07_exit.py (04cf1732829589cd057af53c623819223c0ea698)。
对42个Mint的177个独立Mint×wallet事件（24独立wallet）重算：162有TRANSFER、46有SELL、31两者、131仅TRANSFER、15仅SELL；32/42的观测转出量中转仓占比>=99%；34/42所有被调查执行钱包都有转仓；首次转仓延迟中位17.5s。不是177个独立经济主体，不是随机市场样本；SELL/TRANSFER是作者解析启发式，不是本项目核链真值。
进一步按Mint连接两份文件，按wallet匹配ladder signer：42/42各发行匹配钱包数一致，首轮买入量求和与tokens_bloc差<=0.1枚。以首轮买入为B、累计观测转仓T、累计观测出售S，14/42的T+S-B>1枚，6/42的(T+S)/B>1.01，最大1.0556945659421244。
案例 Mint 87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump：B=780464208.09，T=780464208.09，S=18119267.30，T+S-B=18119267.30；若误用B-T-S作为剩余库存会得到负数。最大差异 Mint HvM3WrbuWuEJTrxDMAPiPwR8oSjHUcbcTDuati9vpump：B=789579628.93，T=830670918.23，S=2884005.41，超出43975294.71。
源码解释：v07读取选定ATA全生命周期签名（至多6页），累计所有负delta交易且未按首轮买入后窗口截断，没有输出所有BUY/转入、起止余额、其他ATA、burn、完整签名列表；最大正delta owner作为转仓候选接收者；SELL基于ATA减少与owner原生SOL增加>0.0005，未充分识别WSOL、路由、混合交易、费用、账户租金。原作者输出是累计流量，不是封闭库存账本，超额可能来自再买入、转回、重复移动或分类误差，未定位具体原因，不能指控数据造假。不得将part_transferee当作供应量比例或最终控制权。正确核算须起始+所有流入-所有流出=结束，并消除同一主体内部转移，保留无法归因的库存区间。以上为V3新发现，不重复V2的概念。
## 2. 逐笔公开记录重算（不同历史样本，不能与上述42币合并）
读取 data/trace_cohorte/e1_buyers_{label}.json 共11文件1204个解析事件。源代码 data/trace_cohorte/t1_premiers_acheteurs.py blob e988ea8edd0fec24176fae54be6c6b23d099ae92：从曲线账户签名头部至多260笔读取，跳过缺失/失败，只导出events[:120]。achat=签名者token净增且原生SOL净减；vente=token净减，不保证SOL收入。原生SOL余额变化包含费用/租金等，不是严格池成交金额；同秒内顺序未独立核验。
固定窗口[首曲线时间, +60s)，要求genesis=true、事件时间非降序、最后公开记录>=60s，8/11通过时间覆盖代理；CHOCO最后40s、MIKU36s、QAMI37s，排除，不填0；即使通过也不能证明全部交易完整。全部文件内部signature无重复。保留严格符号一致的买卖（achat token>0 SOL<0；vente token<0 SOL>0），其他保留未分类。
|label|e1 blob|窗内记录/买/卖/未分类|买方SOL净减|卖方SOL净增|两者差|
|---|---|---|---:|---:|---:|
|ACID|f8806a9a42b103ebd8d8f26bfc82b5088cbcd7be|6/5/1/0|2.839072144|0.901420146|1.937651998|
|BLT|782a8e9b8867dedfdd70463b278f18987348bc3e|3/3/0/0|3.573361632|0|3.573361632|
|LEXICON|70b137263529f64e5c23ed414af0d26c3424da2b|11/6/4/1|3.702747068|0.448708649|3.254038419|
|RAO|8af95e2b9209a2392a288490c130078d3519d5d2|11/8/2/1|3.234048947|0.090008856|3.144040091|
|SAFFRON|cb9024fd093aa79c13d9cfd0f1a62f47a9039214|13/9/0/4|4.692071771|0|4.692071771|
|VISUALIZE|032c115ecb775d464643470eaf228f3238907480|44/30/12/2|18.940339028|6.239020340|12.701318688|
|sumiko|6f99c817e1d224f58a88f61e50b5d603816cd121|45/34/10/1|14.793693817|7.405653937|7.388039880|
|symx|0a3e0f3b5d6764ef535cb1b46e369f895052d9ef|8/5/3/0|4.765207310|0.611447996|4.153759314|
合计141个事件，100买、32卖、9未分类；99个Mint×买方地址。正差不等于独立需求，不是净池流量。
## 3. 加入发行前资金证据：实际小样本分组
同目录e2_funding_{label}.json，要求买方prebuy_window_reached=true；仅取ts<首曲线时间、nature=financement、amount_sol>=0.1、tx_type=TRANSFER、tx_source=SYSTEM_PROGRAM、source非空且source_known为空的记录；在同一Mint窗内两个及以上覆盖买方有共同来源，标为共享来源候选。不把source_known为空当非公共设施证明；资金门槛0.1为本轮探索性选择，非优化或已校准阈值；共同来源根据窗口结束后的买方名单归组，所以仅用于回顾性机制分解，不能用于t=0或窗内实时交易。资金记录虽发生在发行前，历史采集和标签可能后补。没有链接不等于独立；已知标签被排除亦不等于确认交易所。
|label|e2 blob|买方/有窗口覆盖/不足|共同源数/候选地址数|候选买方SOL净减|
|---|---|---|---|---:|
|ACID|81cefa5d4d5d4f4d612a5d07502b8c59eed9fe9b|5/4/1|0/0|0|
|BLT|67aed362a379a886aefae4c6e231631a3da3faf7|3/2/1|0/0|0|
|LEXICON|8f0c41fb0e3880081ea9b1d9eeff803406ac82db|6/6/0|0/0|0|
|RAO|ad50a988e1305e0fab8cc690b00c0d35d1f547ea|8/6/2|0/0|0|
|SAFFRON|d689e5bb01a7fc8296183a2900209ad6971db6b1|9/9/0|0/0|0|
|VISUALIZE|9493e90fb7fd6de98cde352c5e28317fbd243a93|29/29/0|1/4|4.583280838|
|sumiko|fad193ac18ae5f583ebe607edc354d30a9e1a57c|34/29/5|1/2|0.326180469|
|symx|42fd83bace8f2a13a7c400904a196e48e739e823|5/4/1|0/0|0|
89/99买方有源方声称的前置窗口覆盖，10/99不足；6/99共享来源候选（非独立控制真值）。
VISUALIZE 0–60s：共享源候选买4卖1，SOL净减4.583280838、净增2.135216449、差2.448064389；其余覆盖组买26卖11，SOL净减14.357058190、净增4.103803891、差10.253254299。30–60s其余组差1.748851102，token净增29886159.350887，共享组无观察买卖；不能称已确认独立承接或大户退出。
sumiko 0–60s：共享候选差0.326180469；其余有覆盖差5.155717429；未覆盖差1.906141982。30–60s 同一签名者 BjnY2Lc6CjFGWaHGi7aPXUADWC1Z8QQWStxTaJaJjhnV 在+30s净增11609478.962087 token、SOL净减0.518539280（签名22K8Ryq36Z4xUnv7iDS7yXQrDz2niQpkoUf1Foxrku3C1BbRy7ymxB2cHX5px5nFTiJ2k3wjew6L7S9yR3pxjiBY）；+39s净减同数量、SOL净增0.479488132（39MrMERXZfTnFQmoNg2emuJWh7wjosxnsyu6vW552yZ6ZVVWHEop5XFXcNwfNzTEocPMf3KWmoxUeFtSYNVsVfNn）。净token变化0，双边原生SOL变化绝对量0.998027412、差0.039051148。不是完整账户P&L，也不证明刷量；正常短线交易是竞争解释。证明观察到正现金差与交易量并不足以证明持久新增库存。
复算方法（本轮JS已执行）：对e1按上述窗口筛选，按signer累加token_delta和sol_delta；对e2过滤前置资金，Map<source, Set<wallet>>求共享候选；三组分别汇总。对v06/v07按mint与wallet连接，sum(T)+sum(S)-tokens_bloc。上述数值及源blob可重算；未运行原作者RPC脚本。
## 4. 后续数据候选与本轮边界
外部数据目录核查： https://huggingface.co/datasets/DataStore/pumpswap-amm-historical-data-sample （6000行解码样本，含slot/tx_index/ix_path/sig、用户、池、两侧储备、费用）；https://huggingface.co/datasets/pumpdatafun/pump-fun-trades-sample （含不同市场阶段reserve口径）；https://bitquery.io/datastore/datasets/pumpswap （历史交易与储备变化产品描述）；https://launchtape.io/ （事件与接收时间）；仅登记字段与候选用途，未取得完整文件或付费。外部来源的储备时点、真实/虚拟、原生SOL/WSOL、所有权及快照一致性须核查。既有V2的真实池储备案例可用于退出风险，但与本轮样本不同，不能假拼接。
下一最小实证：找同一Mint、同一池、连续事件窗口、可见时间、交易与转账完整性，先核验库存守恒和储备变化，再以固定时点的共享来源候选/无已知关系/未知分组，对照基础净流；后续窗口用净token库存持续、实际池净流和同规模双向报价衡量，避免以成交量或单一钱包余额做代理。B1/B2/B3同母体、退出收益与独立主体真值仍UNKNOWN。本轮不是新增策略/架构；现有执行集群和FCZ研究作为候选知识不删除。保存本文件与现有知识入口，未改交易程序、未签名、未付款、未运行主网或合并主干。
