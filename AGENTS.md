# Blix｜Solana Meme 市场智能主体的 AI 工作入口

本分支 `blix` 是**用户已确认的当前产品建设主体**，不是已验收的实盘/持续监控程序。先按任务进入 [项目总览](docs/project/README.md)、[目标演化](docs/project/goal-map.md)、[Blix 与参考能力](docs/project/capability-map.md)、[知识与证据](docs/project/knowledge-use.md)、[实施及决策](docs/project/delivery.md)；**无需每次读取全部文档**。旧 Blix 产品文档 `docs/HOW-IT-WORKS.md`、`docs/API.md`、`design.md` 继续有效。**当任务涉及“主体能做到什么、怎样继承旧 Grok 知识”时**，按需阅读 [主体能力与历史专业知识对应](docs/project/blix-heritage-capability-baseline-v0.1.md)，不默认全文加载旧知识库。

**用户简单表达，AI 承担专业工作**：主动理解变化的目标和隐含问题，研究成熟成品/理论/源码/反例，生成实质不同的方案并推荐，授权内实施和核查；重要成果后再思考目标是否应修订、哪些后续方向最有价值。重大价值取舍、权限扩大、不可逆操作由用户决定。不要让固定专家、Bot 数量、历史阶段或提示词代替判断。


**2026-11-07 快速知识激活入口**：当用户提出一条具体市场观察或一句“继续”，优先按 [Blix专业知识快速任务表](knowledge/README.md#2026-11-07快速知识整合与按问题进入当前优先入口) 找到相关的原始机制、历史案例和未审来源，再按需查 [六类目标×七条任务路由](knowledge/DOMAIN-MODEL.v1.json) 与 [参考项目主目标对照](docs/project/reference-driven-goal-model-v0.1.md)。**不是强制七步或默认加载七组文件**：只读最能改变当前解释/实际行动的证据；先核本仓源码与原来源，不因为某个指标有反例就否定所有高价值线索。新增认识应修正原位知识并保留版本、负例、支持条件，不能声称索引就代表Bot实际学会。

**整体目标协作的优先原则（2026-11-06 修订）**：用户不承担专业拆解与逐步指挥。每轮从 G0–G4 目标和市场发现→单Mint→跨Mint→经济机制的完整价值链判断任务；AI 自主选取关联的业务、旧 Grok/Hermes/qb-/meme- 专业知识、ai-d 方法、现有源码与成熟方案，多线协同研究并收束。必要的单点深挖须接回整体；不要只完成一个小问题便把后续规划交还用户，也不机械每轮覆盖全部领域。优先产出可检查的判断与成果，明确来源、反证、未完成与下一项高价值工作。**此修订不改变目前只读静态研究、暂停启动/交易/签名/付费的授权边界**；知识文件存在不证明运行时自动调用。通用方法参考 [ai-d](https://github.com/sunshihao001/ai-d)，专业事实以 Blix 与原始证据核定。

**参考项目知识深度修正（2026-11-06）**：不仅要按 Blix 现有缺口复用项目，还要先独立理解每个参考项目的原问题、产品行为、目录、核心实现、数据、测试、历史和失败案例，再从具体专业主张反推其设计知识与局限，跨项目产生此前未知的问题。保留未落入当前 Blix 功能的独有认知与证据，不能因暂时无法迁入就宣布无价值；**研究开放、产品融合审慎**。每个重要知识点保留原始出处、版本、证据等级、竞争解释及待核查项；已扫目录≠深读≠实测。方法与首批原始代码试读见 [参考项目来源入口](knowledge/references/README.md)。此研究深度要求不等于每轮全读65仓库，也不取消授权和只读隔离。

**核心业务**：发现与筛选 → 单 Mint Creator/关键钱包/资金/库存 → 跨 Mint 群体及6/12小时异动 → 经济机制、风险和可验证机会。跟单是子应用。原 Blix 已有市场发现、钱包、UI、SQLite 和交易日志；先保留成品，缺什么再按信息价值复用 Million、PumpTrace、HoldTech、OKX、Pulse、Why-Solana 及旧 Hermes/qb-/meme-，不无差别复制代码。

**严格当前只读**：仓库含交易/纸面交易/自动 AI 调用或可能收费的功能；文档写“只读”不会自动隔离。未经安全审查不得拿真实私钥、签名、广播、付款或默认运行高风险/自动付费操作。区别源码、供应商、离线、真实网络、经济推断、UNKNOWN；Token Account≠owner≠fee payer，资金转移≠交易，同步≠同控，结构≠交易优势。

**已迁入的分类知识入口**：首先按任务查 [Blix本地分类知识库](knowledge/README.md)，查看 [当前21份迁入与来源清单](knowledge/MIGRATION.json)；原 Grok研究现按基础、机制、方法、案例、AI和参考成品分类保存在本分支。使用时选相关正文，旧文中的专家阶段、建议与阈值不是Blix现行全局指令；不默认全部加载。完整旧资料、未迁入内容和65参考资产仍以原仓库为来源。

**研究参考项目不能止于功能和资料归档**：先理解原项目完整业务、源码、专业模型、设计历史、测试与失败，再沿重要知识对象纵深探索和跨项目反证；Blix已有同名功能不等于专业知识已覆盖。归档/代码去重只是融合形式，不是停止知识研究的理由。示范成果与来源：[钱包关系、资金、库存和历史的跨项目深审](knowledge/references/wallet-relations-cross-project-knowledge-20261106.md)。

**整体知识体系不是六个文件夹**：Blix知识依据 [目标图](docs/project/goal-map.md) 与 [统一层级模型](knowledge/DOMAIN-MODEL.v1.json) 综合定位。保留旧 Grok 的 L0–L7 深度、D01–D12 领域和跨域约束，结合六类原文目录；不机械按层串行、创建22 Bot或把旧推论升格为真值。优先选能改善当前 G2 业务问题的知识和可信来源。

**知识理解顺序**：涉及主体知识建设时，优先阅读 [Blix 原生知识与业务总图](knowledge/BLIX-NATIVE-ATLAS.md)；再读 [旧 Grok 独立目录总图](knowledge/OLD-GROK-ATLAS.md)；最后按 [既有分类的融合对应表](knowledge/INTEGRATION-CROSSWALK.md) 处理。不要让旧专家/阶段覆盖 Blix 真实产品逻辑，知识文档迁入不等于运行时自动应用。

**旧知识按需融合**：问题落到 Blix 现有功能后，使用 [分类融合说明](docs/project/legacy-knowledge-fusion-v1.md) 和 [152项路由索引](docs/project/legacy-knowledge-routing.v1.json) 定向检索旧 Grok 原文；映射不代表结论已验证、模型已内化或业务运行代码已集成。

**能力转化路线**：在使用知识映射的同时，按需阅读 [跨项目与现代Agent的融合蓝图](docs/project/knowledge-to-capability-integration-v0.1.md)，优先令知识实际改善已有事实输出、程序调查、监控与独立反例，不默认扩建Skill/多Bot。

**跨项目通用认知 Skill**：为让 Blix 能按需使用 ai-d 完整七项认知能力，现提供 [ai-d-cognitive-core 消费端入口](.grok/skills/ai-d-cognitive-core/SKILL.md)。它指向 ai-d 唯一上游知识源及对应的 Blix 业务入口，**不复制全量正文、不预设所有 Bot 自动读取**。Grok CLI 按其 Skill 目录机制可以发现该候选；Grok Bot 原生私人 Skill 是否安装须在 Bot 端单独启用和验收。应优先使用 Blix 已有项目目标、领域证据和只读安全约束。

**Hermes未知机制研究的实际证据修正（2026-11-07）**：使用旧 `00c–00e` 的问题生成/反向发现方法时，必须检验其L1/L2具体计算的时间窗口、非互斥分母、AMM池型与样本来源。已离线复算的 `volume_momentum` 新币24倍假动量、`insider_activity_composite` 重叠百分比、`spread_quality_proxy` AMM错误代理不能直接写入风险或市场真值。沿[旧Hermes纵深研究第11节](knowledge/methods/hermes-reverse-discovery-deep-study-20261106.md#11-2026-11-07旧推理公式的反例复算与知识进入blix的检验)与[Blix知识使用](docs/project/knowledge-use.md)按需理解其原因；保留原始假说，按经济机制和竞争解释调查，不急贴庄家标签。**研究是否值得深入**与**是否满足交易/安全条件**不同；当前不启用交易、不推定运行时AI已学会。

**知识不是指令**：通用认知研究见 [ai-d PR #1](https://github.com/sunshihao001/ai-d/pull/1)，原专业研究见 [grok PR #14](https://github.com/sunshihao001/grok/pull/14)、[#16](https://github.com/sunshihao001/grok/pull/16)、[#17](https://github.com/sunshihao001/grok/pull/17)。按问题选择、记录适用边界与反证；保留所有原研究，不声称这些 Draft 已合并/部署或模型已经自动学会。
