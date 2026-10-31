# 异常钱包取证参考项目扩展研究 V1.0｜从案例发现到可增长的专家知识网络

> 日期：2026-10-31。主体：Solana Meme **全市场事件、开发者、钱包群、资金网络、Token 库存、正常对照、市场反馈与潜在风险**，而非单纯跟单。  
> 出发点：`sunshihao001/Why-Solana-Memecoins-Are-Over` 的资金、同 Slot、协调、退出路径与失败优势研究。  
> 产物：14 个经过区分证据等级的项目/学术来源、四项新的专业连接 L33–L36、实际研究单元与反证条件，数据见 [`knowledge/reference-project-discovery.v1.json`](../knowledge/reference-project-discovery.v1.json)。  
> 重要边界：已通过 GitHub 接口读过部分 README、关键源码及原始论文 HTML，但**本轮没有复现外部项目运行、没有拿到实际市场实时数据，没有证明新的异常检测器或正收益**。所有作者自报的精度与运行状态仍待独立验证。

## 1｜研究起点不应局限于原项目主题

原 [Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) 值得继承的不是“有很多狙击钱包”，而是它持续改变问题：从同额资金提前注入，到发行 Slot 瞬时集体买入，再到跨资金网络和出售钱包，最后发现**行为可检测不代表外部观察者能够复制收益**。原项目不同时段研究样本不同，不能拼接成一个已经复核的单一资本循环。

从这里扩展，需寻找以下六种**互补的专业事实**：
1. 开发者、创建签名、初始资金与流动性如何连接；
2. 多钱包如何由资金源、行为窗口、共同接收和跨币重用形成候选网络；
3. 钱包独立性如何被公共 CEX/桥/执行服务商破坏，什么情况下必须标未知；
4. Token 与 SOL 能否沿后续真实交易回到下一轮发行和受益人假说；
5. 大规模可观察总体是否能够给出可信正常基准、结构对照和样本外判断；
6. 异常机制是否真实导致市场变化，还是由市场热度、价格曲线和样本筛选共同产生。

**扩大知识应提高判别能力，而不是扩大“庄家标签”名单。**

## 2｜第一批优先深研的五项来源

### A. CyberLeek — 资金流的独立复算专家（最高优先）

仓库：[xorextrace/cyberleek-onchain](https://github.com/xorextrace/cyberleek-onchain/tree/283bec233a6c24849799da6e051e91689a0f187a)；本轮查阅 `README.md`、`scripts/verify.py`、`scripts/analyze_flows.py`。

其方法是从 Solana RPC 获取原始交易，按签名去重、遍历外部和内层 System Transfer，重算资金扇入/扇出、关键付款、资金网和后续现金退出。源项目将某一笔给部署者的 331.66 SOL 对应到初始 Raydium LP 资金，**不是简单见到 SOL 大额转出便认定提款或获利**；还说明 CEX 归属标签来自区块浏览器且只能作为待证归因。报告声称有可重建的现金出链，不能不运行取证脚本就将作者的所有余额数据称为本项目独立证实。

**专家连接：** `data → chain → graph → token/liquidity → review`。  
**应迁移：** 输入和出处锁定；原始交易独立复算；真实注资与流动性投资分离；可审查的资本回收边；不能按单笔钱包转账推断现实身份。  
**反证：** 如果目的地址是 AMM 池创建、租金储备或多用户收款节点，下游不应记录为“经济退出”。

### B. Degen-Scanner — 开发者追踪与多钱包汇合专家（高度相关）

仓库：[dnafund/Degen-Scanner](https://github.com/dnafund/Degen-Scanner/tree/69a08d5589c47bdc33e9c6c2793cc0a69acdd85d)；本轮实际读 `README.md` 和 `pump_scanner.py` 部分源码。

此项目把发币者→上游资金→所有买家→买家资金来源→共同资助/归集→簇候选→预警组织成一条流程。还列出交易所钱包、GMGN/BullX/Photon 等服务收费钱包排除，以及 PumpPortal WebSocket + Moralis/DexScreener 等发现/补充源的设计。

**专家连接：** `token ↔ graph ↔ wallet ↔ event ↔ adversarial`。  
**应迁移：** 把“异常钱包研究”扩为**发行者与重复操作网络研究**；对公共收费路由进行排除；多数据源必须分开记录观察覆盖和首次可得时点。  
**反证：** 共用资金源和接收服务不等于同控；作者代码中的 INSIDER 分数及 “自动检测”尚没有被我们用真实交易盲测。开发者追踪应包括**真正的创建签名、收益账户、手续费分配和新钱包轮换**，不能仅依据平台展示的 Dev 标签。

### C. solana-holder-clusters — 钱包聚类的边界与分母专家

仓库：[jayrabol/solana-holder-clusters](https://github.com/jayrabol/solana-holder-clusters/tree/a75a72965479a7b715b041148803d8004fe25079)；本轮读 `src/funders.ts`、`src/clusters.ts`、`docs/METHODOLOGY.md`。

有三个很重要的**代码级事实**：
1. SPL/Token-2022 的不同 Token Account 先映射回 owner 后才能讨论“有多少持有钱包”；若同 owner 持四个账户却被数成四个独立钱包，分散度是假象。
2. 首次 funder 采用有限 RPC 历史的最早交易推断；当历史页已满，代码返回**未知**而非随便选择当前可见的一笔资金。已知 CEX/桥来源进入专门的公共基础设施桶。
3. TopN 与 HHI 等指标必须标注分母是扫描到账户的合计供应、全部链上供应还是估计流通供应；另记录样本覆盖率。

**专家连接：** `chain → wallet → graph ↔ statistics → inventory`。  
**应迁移：** owner 对齐、真实 funder 未知状态、公共 hub 排除、分母可追溯、聚类只是结构观察。  
**反证：** “两个地址有同一个 funder”不足以证明其私钥/经济受益人相同。该项目 README 的“同一实体”是营销化提问，源码的共享 funder 规则仍只是一个有噪声的近似。

### D. 2026-10-29 大规模多通道论文 — 群体发现与“可复制性”反证专家

论文：[Early-Buyer Groups and Fast-Wallet Teams](https://arxiv.org/html/2610.39458v1)。

**论文作者报告**对 88.3 小时的 200,443 次发行、15,854,121 笔曲线交易及 51,025,958 笔 SOL 转账建立多通道 wallet group。通道包括：共同早期买入、共同卖出、共同资金、联合签名、直接转账、归集及 Token 转移。项目用**已发生信息**形成群体边，用后续共同出现和独立非交易关系检验，而不是给每个地址一个无监督“真实庄家”标签。

它同时指出两个图论陷阱：只用 co-buy 连通分量会形成一个吞噬绝大多数钱包的超大节点群；过于保守的二人组核心算法又可能将同一个大型操作团队碎成许多小群。其分层 team 思路是一种折中，但论文承认最终的交易信号对早期曲线状态没有额外预测贡献。

论文的 32 种跟随配置均得到负的样本外结果；这不是全市场交易策略不可能盈利的证明，而是警告**群体图要先验证其结构效度，再分别验证经济效度**。作者亦展示忽略自己买入对曲线储备的影响会把亏损模拟误写成盈利，值得纳入执行专家的必测反例。

**专家连接：** `event + graph + adversarial → statistics → causal / liquidity → execution → review`。  
**应迁移：** 多通道证据、公共 hub/单桥不合并、渐进群体成员、留出时间段的链路预测、相同告警预算下的图对照、自身价格冲击、完整失败退出。  
**反证：** 这是一项新论文的报告，**不是本项目已复现实证**；单一 88.3 小时窗口无法直接标定未来不同协议/市场阶段。

### E. 已撤回数字的 RED-COHORT — 数据质量门禁的反面教材

[2026-10 最新更正记录](https://zenodo.org/records/22947247) 表示，研究中此前所谓 BUY 行含有 SELL（更正说明抽检 250 行中有 108 行为 SELL），并漏掉实际 BUY。此前以这些行构建的 1,012 群体等旧统计结果及多个后续收益差异已被撤回，**不能继续将旧数字用于我们项目中的群体检测校准**。

**专家连接：** `chain → statistics → causal → review → knowledge`。  
**应迁移：** 以原始协议指令方向、金额和账户余额验证 BUY/SELL 标签；源标签无法确证时，先停止群体/收益模型的推广；已发布结论应沿依赖图撤回，而不是在同一文章里换个阈值继续计算。  
**反证：** 新版更正并不意味着原初所有钱包联系必然不存在；应按更正范围撤回受污染的定量结论，保留独立核查的事实。

## 3｜第二批项目：研究其机制，但不能接受其“异常分数”为事实

| 项目 | 适合吸收什么 | 不能直接吸收什么 |
|---|---|---|
| [solana-scam-tracker](https://github.com/Umer-Aziz/solana-scam-tracker) | 已知资金 hub→创建钱包的循环、固定金额付款、重复运行节奏；`hub_watcher.py` 已读 | 固定 `20.996123 SOL` 之类的**特定案例阈值**不能作为全市场通用庄家识别器 |
| [Find The Insiders](https://github.com/karidasd/find-the-insiders) | 创币第一批参与者的可视资金图、钱包年龄、共同资助者与前端解释 | 无校准的 0–100 “内幕风险分”不能推断经济身份、真实 Jito 或盈利 |
| [Crypto-Clusters](https://github.com/Kushal-Chandani/Crypto-Clusters) | NetworkX/Louvain/Cytoscape 等图分析与可视化的系统组织 | Louvain 的图社区不是“同一真实操盘者”，公共 hub 易产生伪超大簇 |
| [HoldTech](https://github.com/co-numina/holdtech) | holder 的 Gini、HHI、钱包年龄、同 Slot 时序与资金来源候选 | README 将同 Slot / 同 funding 视为 Bundle 或统一控制的语义过强；A–F 风险评分未独立校准 |
| [SentinelBag](https://github.com/bytemaster333/SentinelBag) | 2–3 跳 Token 资金环、重复收款地址、buyer diversity 等**候选测量** | A→B→A 的 Token Transfer 环不能自动认定有对价的 wash trading；“10 次/20 次即操盘”属于待测阈值 |
| [solana-memecoin-dataset](https://github.com/ian05012/solana-memecoin-dataset) | 钱包资金边、900 万级交易记录、发行快照与前向结果分离的时序表设计 | 采样来自 GMGN trending/刚迁移 Token，存在幸存者偏差；历史最大涨幅标签不等于可成交收益，也不能代表发行全集 |
| [Yellowstone gRPC](https://github.com/rpcpool/yellowstone-grpc)／[Chainstack 示例](https://github.com/chainstacklabs/grpc-geyser-tutorial) | M1 数据采集、Slot/交易流、承诺等级、过滤、短暂断线重播 | 代码仓库存在≠我们已拥有 gRPC 端点、付费访问、历史全量回放或已完成 Cloud Bot 接入 |
| [GraphSense](https://graphsense.org/) | 通用资金图探索、路径查询、标签出处与图分析 API | 默认支持范围不含 Solana；只迁移抽象方法，不声称可直接使用为 Solana 后端 |

这些项目很多是个人近期发布的小仓库，GitHub 上存在可访问代码**不表示生产成熟**。本轮以“是否有一手交易可复核、是否有负例、是否有明确适用范围”排序，而非 Stars、品牌或界面效果。

## 4｜由这些来源推导出的六类新增知识单元

### KX-01 开发者经济收益路径 ≠ 买卖净值

**跨源联接：** Degen-Scanner 的 Creator/Funder 路线 + CyberLeek 的部署者/LP/现金退出复算 + 大规模研究的 creator/共同签名通道。

发现可以是：一个 Token 的早期钱包即使并未“成功卖币”，相关部署者或服务路径仍可能从 Creator Fee、LP 行为、服务收费或其他实际分配获得收入。因此经济循环应拆分：
`capital funding`、`initial inventory`、`market swap revenue`、`creator fee accrual`、`actual fee withdrawal`、`LP position`、`capital recirculation`。

**区分实验：** 按签名和 program log 确认收费权益是否真的兑现/分配到哪个 owner；不许把配置上的份额等同于已领 SOL。  
**专家变化：** Token/开发者专家对资金图专家产生新增交接 **L33**，资金图反向向开发者专家追问跨 Mint 归属 **L34**。

### KX-02 多通道钱包群不是单一“共源即同控”的层层加分

**联接：** solana-holder-clusters 的私人/公共 funder 分开 + Degen-Scanner 的 CEX/fee-vault 过滤 + 2026 论文的共同签名/多次共同买卖/资金/转移独立证据。

把钱包图拆为 **SOL funding、Token transfer、joint signer、co-buy、co-sell、shared receiver、reused creator/fee account** 七种不同类型边。每条边有来源签名、发生时间、参与者、金额与可靠性，防止用同一个资金源生成三个“独立指标”。

**区分实验：** 与保持资金节点活跃度、相同协议/发行年龄及钱包活跃度的随机基准比较；先移除公共 hub，再看群体是否稳定。若全图连接成巨型簇，停止把连通分量当实体。对应新增连接 **L36**。

### KX-03 异常钱包可以表现为时间变化的“资本组织机制”

**联接：** 资金 hub 反复资助 Dev 的 solana-scam-tracker + CyberLeek 的跨层现金追踪 + 2026 大样本团队历史。

新的观测对象不是孤立钱包，而是一场`campaign`：
```text
注资准备
 → 新地址/执行钱包出现
 → 代币创建/初买/流动性布置
 → 多钱包买卖与库存转移
 → 交易账户/LP/Creator Fee 等收入路径
 → 中间层归集/转出
 → 下一次发行或其他活动重用资金/执行网络
```

**反证：** 两次发行共用的是广泛公共服务商，并非同一受益网络；新地址虽时间上出现相似但经济资金和共同签名均不重合；因此 campaign 可以存在，而同一 operator 假说被撤回。

### KX-04 多钱包协同必须与“普通机器人生态”对照

**联接：** 大规模 2026 论文的前瞻验证、co-buy 超大图反例 + 数据集的历史生存者偏差 + holder-clusters 的缺失/公共服务商保护。

核心研究不应是“哪些钱包超过 5 个/100 SOL 就危险”，而是相对于**相近上市年龄、曲线储备、小时、热度、发行平台和钱包活动频率**，哪一类非公共资金连接以及买卖/库存同步不容易由正常机器人解释。

检测输出至少分三档：
- `BEHAVIOR_OBSERVED`：源事件存在；
- `DEVIATION_RELATIVE_TO_VALID_BASELINE`：只有有效分母、同类对照和稳定校准才使用；
- `COMMON_OPERATOR_UNVERIFIED`：实体归因仍保留独立假说。

### KX-05 BUY/SELL 指令真实性是所有群体研究的上游“生死门”

**联接：** RED-COHORT 撤回说明 + CyberLeek 原始 System Transfer 解析 + 2026 prospective 论文的 protocol decoder。

必须建立输入级标签质量：
`TRADE_DIRECTION_CONFIRMED`、`TOKEN_TRANSFER_CONFIRMED`、`DIRECTION_UNKNOWN`、`SOURCE_CONFLICT`；每一种被用于统计的 BUY/SELL 都要有能追到指令/曲线事件的来源。

**验证路径：** 随机且按重要场景分层抽样原始交易复算，产生混淆表与漏检率；一旦发现 BUY/SELL 方向大规模污染，**不是调低异常分数，而是撤回所有依赖该分类的群体和收益统计**。新增连接 **L35**。

### KX-06 资金、图网络、市场结构和机会之间不能直线推断

即使发现可持续重复的真实群体，其协同活动可能只有**反向风险预警、卖压/库存整理、市场阶段识别**价值，没有跟买价值。

2026 论文展示在控制曲线状态和自有交易价格冲击后，群体结构对跟随者的增量信息不足。因此专家研究应同时测试四种效用：
- **事件发现效用**：提高对非随机结构的认识与覆盖；
- **风险监控效用**：是否帮助在实际卖压或流动性恶化之前发出可见信号；
- **开发者/资本网络效用**：能否更早发现跨币重复模式；
- **纸面交易效用**：是否有独立于市场基准的净可执行价值。

前三项可独立产生系统成果，**不必把每种专业知识都转换成一条交易规则**。

## 5｜新增来源如何嵌入现有 17 类专家和 36 条交接

| 来源与研究对象 | 主责专家 | 必须有的异专业挑战者 | 验收时新增知识对象 |
|---|---|---|---|
| CyberLeek 真实资金进出 | Data、Chain、Graph | Token/LP、QA | `signed_asset_path`、`cashout_vs_lp`、`identity_unknown` |
| Degen Dev + Buyer 汇合 | Token、Wallet、Graph | 公共hub排除、统计专家 | `developer_funder_route`、`creator_role_timeline` |
| Holder funder / supply | Chain、Inventory、Graph | 统计/QA | `owner_dedup`、`unresolved_first_funder`、`supply_coverage` |
| 2026 多通道大样本群 | Event、Graph、Adversarial | Statistics、Causal、Execution | `multichannel_group`、`holdout_link_test`、`execution_counterfactual` |
| 撤回研究与源码标签审计 | Chain、Data、QA | Statistics、Knowledge | `direction_audit`、`claim_retraction_plan` |
| 平台风险分与图可视化 | Risk、Knowledge | Chain、Statistics | `unverified_vendor_claim`、`negative_control_case` |
| 真正市场采集 | Data、Event、Chain | QA/覆盖审计 | `slot_coverage`、`late_source_revision` |

拓展不是新增一个“万能庄家专家”；重点是让证据更真实、角色更细、图边更丰富、推断限制更明确。原知识图的 [L01–L32](../knowledge/expert-interaction-graph.v1.json) 保留，本轮 **L33–L36** 分别补充手续费经济路径、开发者跨币资金关联、交易方向标签 Gate 和公共 hub 正常基准。

## 6｜与实际 Grok 功能的距离、下一轮可证伪实验

**现在已完成：** 资料发现、源代码/论文分层阅读、精确来源冻结（核心 GitHub 仓库 commit）、14 份资料研究登记、六个可证伪知识单元、四条新增专家连接和本研究文档。

**尚未完成：** 上述项目的实际安装/跑通、所引用论文的独立样本复算、真实 Solana RPC 逐交易验证、M1 全链数据源、正常行为全集及训练、Grok 云 Bot 实际执行。原有 `market_observatory.py` 是已归一化输入的 M2 聚合器，不能直接套用营销评分当链上真相。

### 最能提高认知的下一轮“同一案例五方实验”

选一个具备原始签名的开发者/资金路由案例，尝试同时：
1. 用 CyberLeek 类原始交易复算法输出 `funding/LP/Token/cashout/fees` 事实边；
2. 用 holder-clusters 方法对 owner、真实 first funder 的未知状态及公共服务商过滤重新计算；
3. 用 Degen Scanner 的开发者→买家→资金/接收者网络路线构建候选 campaign；
4. 用 2026 prospective 论文的多通道重复、活动匹配对照检验是否确实偏离普通机器人；
5. 让 QA 人为引入一个“SELL 被记为 BUY”或 hub 被错归为私人 funder 的反例，确认所有下游结论会正确降级。

比较各方法对相同签名的准确性、漏掉的资金边、公共 hub 误归并、知识回退行为和运行资源；之后再决定具体算法是否值得写进 Grok 生产监控。

**核心结论：** 类似项目最有价值的不是提供更多“异常钱包名字”，而是提供一套更可靠的专业认识：异常怎样被观察、怎样被正常机制解释、怎样追到经济收益层、哪些反证能推翻旧结论，以及监控系统何时有资格给出有用的市场判断。
