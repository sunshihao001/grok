# 外部成熟项目对标研究｜专家写作 Skill V1.0（四轮搜索）

**应用范围补充**：该对标最初以跟单专家写作为示例，如今可用于全市场事件、异常协同、资金网络和市场结构研究的 Skill 评测。现行总入口是 [Solana Meme System Intelligence](../skills/solana-meme-system-intelligence/SKILL.md)，旧单钱包评测 E1–E5 只是一组专题，不代表完整系统能力。



- 时间：2026-10-30
- 范围：现有 `skills/solana-meme-expert-writing` 的方法与工程对标，不涉及真实交易或云端部署
- 方式：多轮外部搜索 → 原始 GitHub 仓库/规范/源码读取 → 与现有 Skill 交叉比较 → 复用决策
- 结论状态：**设计对标完成；未执行有/无 Skill 的对照评测；未安装外部工具；未验证 Grok 云端兼容性**
- 本研究不直接改写已存在的 SKILL.md。若要改，应先建立可复用的测试用例和基准，以观测到的失败驱动最小改动。

## 1. 主要结论：先复用成熟组合，而不是发明另一套元框架

我们的问题有两个部分，必须区分：

1. **怎样提高知识研究和专业写作的真正深度**：来源检索、多个角度提问、结构化证据、知识冲突、机制创新、文稿合成。
2. **怎样证明 Skill 真正在改变 Agent 行为**：触发准确、上下文加载、无 Skill 对照、独立判分、输出可复用、适配目标运行时。

当前仓库的 Expert Writing Skill V1.0 已有研究思路、源头角色、逻辑断层、错误示范和一份完整样稿，具备专业领域知识；但没有设计或运行正式的 with-skill vs without-skill 对照评测，也没有确认 Grok 云环境是否发现或加载该 Skill。现有主要任务不是大幅增加文本，而是选择性借鉴成熟工具把这些缺口补齐。

## 2. 参考项目清单与精确复用建议

| 外部成品与入口 | 复用成熟的部分 | 本项目的直接行动 | 不应照搬 |
|---|---|---|---|
| [Agent Skills 官方规范](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx) | `SKILL.md` 元数据、按需加载、`references/`、`scripts/` 和验证器 | 保留当前 `skills/solana-meme-expert-writing/` 结构，按规范做静态验证及相对路径检查 | 以文件存在推断 Grok 已支持该规范；实际加载须另测 |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | realistic eval prompts、with/without 对照、定性与定量评审、失败后迭代 | 用其测试流程设计三类 Solana Meme 研究任务和盲评协议；必要时复用其评测脚本并遵守许可 | 整套 Claude 专用工具和 subagent 调度条件；这些并非 Grok 的现成能力 |
| [OpenAI Codex skill-creator](https://github.com/openai/codex/blob/main/codex-rs/skills/src/assets/samples/skill-creator/SKILL.md) | 只写能改变 Agent 决策的指令、渐进式披露、优先保留开放判断、精简修复 | 对当前长文本去重，区分必守证据约束与灵活研究建议；保留单个强示范 | 把一般最佳实践变成每次都必须运行的重流程 |
| [Superpowers: writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) | 将 Skill 看作可验证的流程知识；RED→GREEN→REFACTOR；先看无技能失败 | 在重要改版前做三个压力/失败用例，针对真实错误最小增补；记录不会使用技能时的行为 | 机械地把软件工程 TDD 每条规则套到主观写作质量上 |
| [Stanford STORM / Co-STORM](https://github.com/stanford-oval/storm/blob/main/README.md) | perspective-guided question asking、来源支持的模拟专家访谈、预写作收集再形成结构；Co-STORM 人机协同讨论与动态心智图 | 借其提问机制：对某具体 Meme 交易问题，从钱包行为、资金/库存、微观结构、反证/执行经济角度生成竞争问题，按检索证据更新问题树 | 直接复制自动百科文章的固定大纲或认为 STORM 产物无需人工编辑；原项目也承认不是出版就绪 |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | planner/execution 分工、指定来源与扩展来源、逐条追溯来源、过滤无关材料、写报告 | 沿用其“研究问题→定向来源→互补外部搜寻→证据选择→报告综合”思路；与 Grok 的 source_index 连接 | 无必要地引入全套 Python 搜索代理、独立模型和外部 API 成本 |
| [Microsoft GraphRAG](https://github.com/microsoft/graphrag/blob/main/docs/query/overview.md) | Local/Global/DRIFT/Basic 查询分工，图结构与原文同用，问题延伸生成 | 先制定关系语义和来源图，不立即重建索引：具体钱包用局部检索，全知识盲点用全局聚合，连接问题用探索式扩展 | 当前资料有限时直接安装整个 GraphRAG 并索引所有仓库；可能引入图抽取偏差和运行成本 |
| [LangChain Open Deep Research](https://github.com/langchain-ai/open_deep_research/blob/main/src/open_deep_research/deep_researcher.py) | 研究 brief、supervisor 组织子研究、分工收集后综合 | 仅为未来 Grok 多研究 Bot 设计保留可选参考 | 此仓库当前已归档，不作为新运行依赖的优先首选 |
| [Karpathy autoresearch](https://github.com/karpathy/autoresearch) | 冻结评测规则、只改变一个受控部分、反复记录实验结果 | Skill 比较时固定输入材料、模型、评审协议，迭代修改 Skill 后保留结果记录 | 其 GPU 训练脚本和具体 val_bpb 指标与写作任务无关 |

上述并非对“交易盈利效果”的外部背书：这些是研究和 Agent 工程方法，需在我们的 Meme 场景中验证。GitHub 元数据核实（查询日）：obra/superpowers=MIT、GPT Researcher=Apache-2.0、STORM=MIT、Agent Skills=Apache-2.0、Microsoft GraphRAG=MIT、OpenAI Codex=Apache-2.0；anthropics/skills 仓库含不同授权类型的素材，复用特定文件前必须逐项核对其适用许可。LangChain Open Deep Research 已归档。

## 3. 与我们已有 Skill 的逐项对比

对草案分支 `skills/solana-meme-expert-writing/SKILL.md` 的直接检查：
- 185 行，约 6,346 字符；具有 YAML `name` 与 `description`，主文档链向两份 `references/`，大体符合 Agent Skills 的目录思路。
- 已有知识本体、竞争机制、因果反证、时间可得性和净收益边界；这些属于本项目必要的专业资产，不应被通用框架冲淡。
- 当前主 Skill 内没有 `evals/evals.json` 规范、固定基准样例或 with/without 比较记录。之前的单篇示范可证明“有一篇示范文”，不能证明“Skill 导致任何模型在陌生问题上变好”。
- Skill 文件通过 GitHub 保存 ≠ Grok 的云端 Bot 可直接加载；跨平台行为、工具权限、目录扫描、Token 限制需要运行环境核验。
- 虽然已按需引用两份参考文本，但主文依然承载不少具体领域示例；后续可参考 Codex Creator 的渐进式加载原则进行精简，前提是基准测试显示精简确有帮助。

### 当前应优先保留

1. 交易场景的问题意识：真实钱包的可跟随性，而不是“聪明钱名单”。
2. 必须区分地址、经济主体、钱包角色、交易意图、市场价格和可执行净收益。
3. 证据来源、样本选择、时间可用性、竞争性解释与反证。
4. 允许原创假说，但不将尚未验证的机制升级为交易规则。

### 优先补的四块，而不是另外发明五十项规范

1. **多视角提问技术**：参照 STORM，在初次研究中识别未被覆盖的重要问题，不再先写完整目录。
2. **研究材料路由技术**：参照 GPT Researcher，区分源代码、概念文章、平台快照、真实交易、外部实证；按问题相关度载入。
3. **检索范围策略**：参照 GraphRAG 的思路，分“个案具体深挖”“跨库全貌梳理”“从局部扩展新关系”三类；暂不部署 GraphRAG。
4. **Skill 行为验收**：参照 Anthropic/Superpowers/Codex，用同一问题和材料比较旧版与候选改版的实际输出，关注专业认知增量而非文字长度。

## 4. 建议建立的首批基准题（准备测试，不宣称已经执行）

**E1｜跨源机制深挖：**
“结合原 Hermes 中同源资金/角色分类、meme- 的第一控盘区和 Why 项目的协调性研究，深入解释同源买入何时不能证明控制权。保留互相竞争的解释，说明原文和新推论边界。不要只给条目总览。”

**E2｜历史盈利不等于可跟：**
“给定真实链上钱包交易和供应商信号时序，判断历史盈利钱包是否具有外部可复制的信息优势。必须明确数据源时间、观察延迟、可成交成本和反例。没有执行价格就不能虚构收益。”

**E3｜矛盾/未知的数据来源：**
“meme- 的 WORLDCUP 候选样本存在不同池/时间的流动性值，同时 FCZ 标注为 unknown。不要认定发生 Rug，先核对口径，写出下一步具体证据需求，并说明哪些只能留作假设。”

**E4｜自由探索能力：**
“在不按预设分类强行归纳的条件下，推演盈利钱包之外可能具有市场信息价值的失败钱包或反向行为机制，提出其独特可观测预测和可能推翻该解释的证据。”

**E5｜无关任务不误触发：**
“解释一个已经可直接确认的单个 token decimals 字段定义。” 此题应直接回答，不应触发整套长文深研 Skill。

建议评审维度：事实来源正确、研究对象清楚、竞争解释有区分力、是否产生非显然的可证伪新推断、时间/净收益边界、可转换成 Grok 下次研究行动、篇幅/重复与虚假断言。针对主观写作优先人工盲评；对于路径、数值、时间、样本分母和来源引用可做确定性核验。

**避免评测泄漏**：同一道示范题不等于独立测试；至少保留部分材料和问题做未参与改稿的测试集。

## 5. 建议实施顺序：最小改造，证据驱动

**第一段（已完成）**：四轮外部搜索、成熟项目原文与源码核对、当前 Skill 静态检查和复用优先级。

**第二段（待实施）**：固定基准输入材料、冻结 E1-E5 问题，收集无 Skill、当前 Skill 的独立输出；没有可调用的 Grok 评测运行环境就明确保留“待测”，不能编造结果。

**第三段（有失败证据后）**：只针对观测到的问题最小修改 Skill：可能是加入 STORM 风格的竞争问题生成入口，或把详细案例移到 reference，或调整前置触发文案。不要一次引入整套多 Agent 框架、GraphRAG 和全文向量索引。

**第四段（复核）**：在未参与改稿的真实材料上验证，比较有/无 Skill、旧/新 Skill 的实际研究质量；通过后再按 Grok 实际云端能力安装适配。

## 6. 结论与禁用捷径

真正值得借鉴的不是“多角色 + 更多 Prompt + 更多文件”，而是：**STORM 的问题发现、GPT Researcher 的来源研究、Agent Skills 的渐进式加载、Superpowers/Anthropic 的行为评测，以及 Codex 的最小化指令原则**。

不应因为某成熟项目有自己的 planner、subagents、RAG 数据库或 PDF 发布器，就在我们项目里复制这些运行时。先以一个真实 Solana Meme 跟单研究问题证明写作 Skill 的实际增量，再决定是否需要更重的系统工程。

**认知引导词：从成熟项目继承方法，用真实问题发现缺口；以开放推演产生新认知，以独立评测决定哪些方法值得留下。**
