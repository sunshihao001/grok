# Grok 分批知识迁移规范｜KNOW-001

**决策**：不是「全文复制」或「启动时塞进长 prompt」，而是 **原仓保真 → 知识索引 → 小型可审查的知识包 → 数据验证 → 分级发布 → 监控读入**。使用源知识系统的真源地图、分线、文档结构与反证纪律；不照搬 MQL5 单策略、Hermes 调度器或其角色设定。

## 0. 已检查的仓库与角色

- `sunshihao001/-`：旧业务流程契约、证据输出与缺失处理（有历史实现，不意味着新环境等价）。
- `sunshihao001/meme-`：第一控盘区/POC/AVWAP/风险语义及知识管理方法（研究假说、方法学；不是已验证 Solana alpha）。
- `sunshihao001/qb-`：GMGN 工具原型、钱包数据护照（经验性候选实现，原始字段语义待核实；Hermes Harness 不迁移）。
- `sunshihao001/grok`：最终 Grok 版的业务实现与监控运行真源。

四层分离：**原始事实 Raw** / **语义知识 Knowledge** / **可检验规则 Rules** / **持续运行 Runtime**。不允许 Knowledge 自动写 Rules；不允许历史文本声称是实时数据。

## 1. 启动时怎样读取，不压爆上下文

1. 始终阅读 `AGENTS.md`、`BOTS.md`、本说明和 `knowledge/registry.v0.json`（短索引）。
2. 先使用既有 `knowledge/catalog.v1.json` 的 15 张知识卡按需路由；涉及证据边界时，再查新的 KB-001，而不是一次加载全部理论库。
3. 仅按触发问题打开 `knowledge/packs/KB-*.md`；需要复核再从 registry 的 **commit + path + blob SHA** 定位原文。原有 21 份快照仍可查阅，但未自动验证为事实。
4. 工作过程中逐条形成「证据卡」；超出受审包的内容标记 `UNREVIEWED`，先读源文，不凭记忆扩写。
5. 每次迭代更新索引、变更记录、反例和测试。过时版本保留，不删除历史；任何「冻结」都需要独立 QA 与人工审查。

## 2. 分批准入与退出

| 级别 | 内容 | 允许用途 | 晋级条件 |
|---|---|---|---|
| S0 inventory | 只知道源位置、版本、职责 | 主题路由 | 文件可定位、源可校验 |
| S1 reference_only | 审查后的概念、边界与反证 | 给 Bot 的解释、补采建议 | 文本不冲突、来源和 QA 可追踪 |
| S2 verified_observation | 经过字段单位与原始交易交叉验证 | 可复算观察/变更报警 | 样本、单位、时戳、反例、来源覆盖率审计 |
| S3 candidate_rule | 固定样本/参数的候选规则 | 纸面回放、盲测 | 无未来函数、比较简单 baseline、净执行成本、漏误报统计 |
| S4 frozen_paper | 人类接受的只读纸面监控规则 | 单一最终 Monitor | 回滚、监控漂移、定期复核，**仍不可交易** |

跨级跳跃禁止；S1 文本不能被当作 S3 测试通过。源概念可作为竞争假设保留，并非全都要晋级。维护版本由 Git / registry 负责，**Bot 自己不把新搜索结果写成冻结规则**。

## 3. 第一批明确交付

- `KB-001`：证据契约、源区分、缺失降级、第一控盘区误判和反证原则，来源锁在 registry。状态 **S1 / reference_only**。
- `src/solana_meme_os/knowledge_intake.py`：独立验证本批知识索引与证据边界，保留既有 `knowledge.py` 和 15 张知识卡的运行时行为。
- 原监控继续输出 `knowledge.interpretation_candidates`；本批知识由开发 Bot 按需读取，不自动晋级为规则。现有阈值仍属**未经校准的示例**。
- `tests/test_knowledge_intake.py`：新增索引完整性、篡改拒绝、触发指导及与现有监控共存测试；原 `tests/test_knowledge.py` 保留。

## 4. 后续的最优顺序（而非照目录逐个搬）

1. **先补证据地基**：真实只读 GMGN 返回值、field/unit/slot/来源到 normalized 的确定映射，且明确 fixture 不算真实证据。
2. **KB-002 钱包资金图**：owner/token account/LP/PDA/同源资助、实体去重、地址生命周期与行为持续性；先拿可标注的反例，再做分类。
3. **KB-003 市场机制**：筹码/庄家周期、深洗、死亡盘、回收、跨池迁移。分别估计解释力，不追求概念数量。
4. **KB-004 净收益可捕获性**：钱包先验选择偏差、信号延迟、排队与复制拥挤、买卖滑点、费用、失败成交及 max adverse excursion；与简单跟单基准比较。
5. **KB-005 外部知识/工具**：对链上追踪频道、开发者语义、GMGN/其他工具进行来源等级标注；搜索关键词只提供发现路线，不能自动形成结论。

此顺序的核心理由：先判断 **事实是否可信、策略能否因果复现、净收益能否真正被跟到**，而非优先扩大抽象术语覆盖率。

## 5. 每一批必须带的验收包

`id/version`、任务负责人、问题、源仓 commit 与 blob SHA、原文定位、吸收/不吸收边界、已知反证、独立复核人、至少一条成功/失败/缺失/冲突 fixture、回归命令及结果、未解决项、降级路径、人工接受状态。发生来源冲突先记录，不擅自默默覆盖。

**当前未完成**：未验证 live GMGN 字段；未做多源链上实测；未统计误报/跟单净收益；未创建实际 Grok Bot/Routine；未取得人工冻结审批。

## 6. 与已有知识库共存

在本批启动时，主分支已经拥有 `knowledge/catalog.v1.json` 15 张卡片、`knowledge/legacy-snapshots/` 21 份历史文本快照、`knowledge.py` 的关键词及监控路由。不能覆盖这些既有成果；KB-001 是增量审查的单独参考包。快照保留不等于全部内容已被深度吸收或独立验证。

## 7. KB-002：小范围、可复算的钱包资金证据（2026-10-29）

- 研究主体：**直接入金关系是否存在**，不是把每个 `wallet` 归到一个所谓庄家，也不是重写 15 张既有卡片。
- 层级：`reference_only`。索引新增 8 份源文件，其中第三方参考只存 GitHub commit+路径+SHA 与独立方法说明；不复制其文章、图表、资金数据。
- 学习入口：`knowledge/packs/KB-002-wallet-funding-evidence.md`；开发 Bot skill：`skills/solana-meme-funding-evidence/SKILL.md`。
- 离线可复算：`PYTHONPATH=src python -m solana_meme_os.funding_evidence --input fixtures/kb002-funding.json --allow-fixture`。
- 测试包含 known-hub 排除、dust、可见时间晚于 cutoff、缺页、重复事件、未知来源、同 signature 不同指令、标签未来泄漏与非真实运行模式。
- **在真实 GMGN/RPC 原始字段、token-account owner、网络基础设施与对照分布核实前，不自动接入 Monitor。** 原先 KB-001 的源、文档与运行接口继续保留。后续研究首先决定何种非 hub 分类有可审计证据，而非先决定给谁加高风险标签。
