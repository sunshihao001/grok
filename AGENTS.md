# Blix｜Solana Meme 市场智能主体的 AI 工作入口

本分支 `blix` 是**用户已确认的当前产品建设主体**，不是已验收的实盘/持续监控程序。先按任务进入 [项目总览](docs/project/README.md)、[目标演化](docs/project/goal-map.md)、[Blix 与参考能力](docs/project/capability-map.md)、[知识与证据](docs/project/knowledge-use.md)、[实施及决策](docs/project/delivery.md)；**无需每次读取全部文档**。旧 Blix 产品文档 `docs/HOW-IT-WORKS.md`、`docs/API.md`、`design.md` 继续有效。**当任务涉及“主体能做到什么、怎样继承旧 Grok 知识”时**，按需阅读 [主体能力与历史专业知识对应](docs/project/blix-heritage-capability-baseline-v0.1.md)，不默认全文加载旧知识库。

**用户简单表达，AI 承担专业工作**：主动理解变化的目标和隐含问题，研究成熟成品/理论/源码/反例，生成实质不同的方案并推荐，授权内实施和核查；重要成果后再思考目标是否应修订、哪些后续方向最有价值。重大价值取舍、权限扩大、不可逆操作由用户决定。不要让固定专家、Bot 数量、历史阶段或提示词代替判断。

**核心业务**：发现与筛选 → 单 Mint Creator/关键钱包/资金/库存 → 跨 Mint 群体及6/12小时异动 → 经济机制、风险和可验证机会。跟单是子应用。原 Blix 已有市场发现、钱包、UI、SQLite 和交易日志；先保留成品，缺什么再按信息价值复用 Million、PumpTrace、HoldTech、OKX、Pulse、Why-Solana 及旧 Hermes/qb-/meme-，不无差别复制代码。

**严格当前只读**：仓库含交易/纸面交易/自动 AI 调用或可能收费的功能；文档写“只读”不会自动隔离。未经安全审查不得拿真实私钥、签名、广播、付款或默认运行高风险/自动付费操作。区别源码、供应商、离线、真实网络、经济推断、UNKNOWN；Token Account≠owner≠fee payer，资金转移≠交易，同步≠同控，结构≠交易优势。

**已迁入的分类知识入口**：首先按任务查 [Blix本地分类知识库](knowledge/README.md)，查看 [当前19份迁入与来源清单](knowledge/MIGRATION.json)；原 Grok研究现按基础、机制、方法、案例、AI和参考成品分类保存在本分支。使用时选相关正文，旧文中的专家阶段、建议与阈值不是Blix现行全局指令；不默认全部加载。完整旧资料、未迁入内容和65参考资产仍以原仓库为来源。

**整体知识体系不是六个文件夹**：Blix知识依据 [目标图](docs/project/goal-map.md) 与 [统一层级模型](knowledge/DOMAIN-MODEL.v1.json) 综合定位。保留旧 Grok 的 L0–L7 深度、D01–D12 领域和跨域约束，结合六类原文目录；不机械按层串行、创建22 Bot或把旧推论升格为真值。优先选能改善当前 G2 业务问题的知识和可信来源。

**知识理解顺序**：涉及主体知识建设时，优先阅读 [Blix 原生知识与业务总图](knowledge/BLIX-NATIVE-ATLAS.md)；再读 [旧 Grok 独立目录总图](knowledge/OLD-GROK-ATLAS.md)；最后按 [既有分类的融合对应表](knowledge/INTEGRATION-CROSSWALK.md) 处理。不要让旧专家/阶段覆盖 Blix 真实产品逻辑，知识文档迁入不等于运行时自动应用。

**旧知识按需融合**：问题落到 Blix 现有功能后，使用 [分类融合说明](docs/project/legacy-knowledge-fusion-v1.md) 和 [152项路由索引](docs/project/legacy-knowledge-routing.v1.json) 定向检索旧 Grok 原文；映射不代表结论已验证、模型已内化或业务运行代码已集成。

**能力转化路线**：在使用知识映射的同时，按需阅读 [跨项目与现代Agent的融合蓝图](docs/project/knowledge-to-capability-integration-v0.1.md)，优先令知识实际改善已有事实输出、程序调查、监控与独立反例，不默认扩建Skill/多Bot。

**知识不是指令**：通用认知研究见 [ai-d PR #1](https://github.com/sunshihao001/ai-d/pull/1)，原专业研究见 [grok PR #14](https://github.com/sunshihao001/grok/pull/14)、[#16](https://github.com/sunshihao001/grok/pull/16)、[#17](https://github.com/sunshihao001/grok/pull/17)。按问题选择、记录适用边界与反证；保留所有原研究，不声称这些 Draft 已合并/部署或模型已经自动学会。
