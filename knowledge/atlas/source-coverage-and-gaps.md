# 全域知识来源及覆盖审计｜什么已经存在，什么还没有吃透

> **审计范围**：当前 `grok`、历史 `sunshihao001/-`（Hermes）、`sunshihao001/meme-`、`sunshihao001/qb-`、`sunshihao001/Why-Solana-Memecoins-Are-Over`、`okx/onchainos-skills`。依据各仓库目录、既有知识与部分关键源码及文档；**不是对数千文件逐行独立审计**。版本真源为 `knowledge/system/source-registry.v1.json`、`knowledge/source-admission.v1.json` 和 `docs/okx-onchainos-runtime-review.md`。当前 96 个单元仅完成了第一轮机制撰写，不得宣传全域知识已经完全吸收。

## 六组知识源的分工

| 来源 | 真实知识优势 | 现在必须如何吸收 | 禁止冒充的内容 |
|---|---|---|---|
| Solana 官方协议与 RPC | Token Program、账户、PDA/CPI、交易时钟与权限 | 优先用于 D01/D02/D10 的技术定义；再结合具体发行程序、池合约核对版本 | 不可用一条通用解释代替所有程序 |
| 原 Hermes `sunshihao001/-` | 钱包/资金/Token Panel/证据链/门控，以及 GMGN 字段→专业问题→特征/结构的思考方法 | 迁移可复用的**专业判断问题**，尤其 `learning/05–14`、`design/phase1-research/00b–00e` 和 Skill 设计；不用 Hermes CLI/hook | 旧字段阈值、0.8 置信度、2 秒同步不是事实概率 |
| `sunshihao001/meme-` | FCZ、价值区、POC、AVWAP、Sweep、Wyckoff、SMC、诱多反弹、反证实验与策略可更换性 | 作为 D03/D08/D11 的结构理论；解释为什么 FCZ 只是众多视角之一、每种锚点如何失效 | MQL5/模拟样本不自动等于 Solana 实盘 Alpha |
| `sunshihao001/qb-` | GMGN 真实响应、历史采集/钱包行为流程、脚本/纸面交易与状态事件，大量数据文件 | D10 字段字节语义、D01 解码程序候选、D04/D05/D06 构造方法、D09 执行模型、D12 程序运行与可靠性方法；**本轮主要盘点并保留引用，不优先用旧单币交易测试代替知识研究** | `data/` 存在不代表信号已验证，paper PASS 不代表盈利 |
| `Why-Solana-Memecoins-Are-Over` | 反事实基准、信息时间、检测总体、是否可交易、反选择、收益分母和失败模式的研究问题 | 作为 D08/D09/D11 的**对抗方法素材**，单独审查历史统计口径；保持 `review_only` 状态 | 不得把作者报告的数字当项目独立复现或确认的真实 Alpha |
| `okx/onchainos-skills` | 代币/钱包/市场/新币/tracker 命令规范、行情/链上查询与 CLI 代码 | 用于 D10 的只读供应商能力表，字段逐一核对单位/时间；真实命令和计费需事前审批并实际部署验证 | 源代码文档存在不等于已安装、已认证、免费或运行成功 |

官方技术来源补充：[Solana docs](https://solana.com/docs)、[Jito low-latency](https://docs.jito.wtf/lowlatencytxnsend/)、[Raydium CPMM Math](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/math.mdx)、[CPMM Fees](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/cpmm/fees.mdx)、[LaunchLab bonding curve](https://github.com/raydium-io/raydium-docs-v1/blob/main/products/launchlab/bonding-curve.mdx)。这些是技术机制参考；具体程序配置和版本另核。

## D01–D12 全领域审计清单

| D | 已有可承接的核心知识 | 第一轮本轮已建设 | 仍不足的真正深度 |
|---|---|---|---|
| **D01** | Hermes 链上基础片段、Solana 官方账户/交易文档、grok L1-L2 | 账户/授权、CPI、时间、单位、事件账本 8 单元 | 按实际 ProgramID/版本逐指令校核解析语义、跨程序复杂 swap、边界失败 |
| **D02** | Hermes lifecycle、meme 结构理论、Raydium LaunchLab 文档 | 创建→曲线→毕业→池→多池→权限/角色 8 单元 | 各 launchpad 版本的具体迁移状态、代币扩展、池费配置和异常阶段 |
| **D03** | Hermes LP、meme 成本锚理论、Raydium CPMM/LaunchLab | 池模型/储备/费收/冲击/MEV/深度 8 单元 | CLMM、不同曲线、复杂路由、跨池套利与动态 LP 的版本化数学 |
| **D04** | Hermes 钱包角色/GMGN 字段、qb- 钱包脚本、现有 L3 专家台 | 角色动态、PnL、优势来源、策略状态 8 单元 | 多地址完整头寸、成本归属、跨 Token 经济受益与退出技巧的理论深入 |
| **D05** | Hermes 同源/资金图、qb- 资金分析、现有 E-L3-02 纵深 | 本金/执行费/托管/LP/收费权、同控竞争世界 8 单元 | 可识别性理论、图中服务商角色、因果混淆和多主体利益分配 |
| **D06** | Hermes 控盘/Top10、meme 风险、grok 筹码专家 | 供应分母、权限、可卖库存、独立承接 8 单元 | 控制权动态、可交易浮筹的经济定义、库存/池深度在危机中的相互反馈 |
| **D07** | Hermes 多维时序、meme 动态策略方向、grok L3 | 事件/角色/注意力/轮动/反身性 8 单元 | 社交传播时钟与链上信息传播、跨币资金流 vs beta 的专业推理 |
| **D08** | meme FCZ/POC/AVWAP、Hermes 组合推理、grok Alpha 专家 | 六策略家族、信息窗口、竞争基准、异常与拥挤 8 单元 | 候选机制的发现理论、为何不同策略适用不同 market regime、策略切换经济学 |
| **D09** | Hermes 风险门控、qb- paper 原型、grok cost 文档 | 两侧报价/规模/费/tip/尾部/机会成本 8 单元 | 路由失败/部分退出/延迟敏感性、钱包容量竞争的真实机制模型 |
| **D10** | GMGN 12 子类字段、OKX Skill CLI、grok 源准入及快照解析 | 单位/时钟/覆盖/异常/版本/计费 8 单元 | 已验证的 provider→chain 字段对照表、live 覆盖、费用/计费与故障 |
| **D11** | meme 反证方法、Why-Solana (review_only)、grok F0–F6 | 总体/时间泄漏/负对照/消融/OOS/失败留存 8 单元 | 针对每种策略的具体 null model、完整真实研究分母与独立经济验证 |
| **D12** | 52 项 Bot 既有能力、21 位专家、Grok Python/SQLite、本体及 transfer | 知识抽取/专家协作/固定提交/运行安全/版本循环 8 单元 | 真正 Grok 云电脑实测、可靠联网采集、知识检索检验、B07 冻结发布 |

**准确的完成口径**：L0 的八个治理单元 + D01–D12 的 96 个内容单元 + 12 条跨领域链已建立“可研究的完整覆盖网格”；但细化专题与协议/数据实证仍有大量工作，不能写“96 项已经全部专业精通”或“Grok 已自动掌握”。

## 对 21 位专家和 52 项能力的覆盖

本轮采用 **`knowledge/atlas/registry.v1.json`** 连接：
- 12 个既有 D 领域，每个 8 个最小知识单元；
- 21 位已有专家的 ID/对应领域/原有专业责任；
- B01–B07 所持有的 52 项原知识能力 ID，且**52 项都可通过原 domain_id 归入 12 个领域，不丢失 ID**；
- 15 张历史主归属知识卡在原本体中全部能对应 D 领域。

但这些链接证明的是**导航与结构覆盖**，不是逐个旧能力已经达到实操熟练程度，更不是已运行的 Grok 智能体。

## 研究优先级：由知识断层决定，而不是平均排队

**第一批基础缺口**：D01 原始事件语义、D02 曲线/毕业具体协议、D03 价格/深度真实数学、D10 字段可见性。四者是所有后续钱包机制和跟单经济学的物理基础。

**第二批专业机制**：D04–D07 的经济组织、交易策略身份、筹码供应、时序与注意力，重视不同专家解释之间的真实冲突。

**第三批机会研究**：D08/D09 研究可观察、可预测、可交易三个断层；D11 独立研究方法确保不把理论解释当盈利。

**贯穿全部**：L0 来源治理、D12 知识编译/运行和 B07 发布边界。GPT 研究可以先于 K2 市场实验，但真实交易能力、净收益及 Grok 实际部署只由对应验证完成后升级。

## 与旧仓库大规模数据的关系

本轮对仓库目录和关键已读文档进行了覆盖归档，没有宣称对 `qb-` 数千原始数据文件或 `meme-` 数百资料逐行读完。后续从原资料读取时，应以**当前要解决的专家机制**定向抽取，保存 commit/path/具体知识与矛盾；不做一键整库知识迁移，不把旧框架搬进 Grok 假装专家水平提升。

[返回总览](README.md) | [Atlas 机器目录](registry.v1.json) | [跨域研究链](cross-domain-chains.md)
