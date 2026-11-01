# AI 项目知识导航与调用说明 V0.1

> **这是一张检索与调用地图，不是新知识本体或研究迁移。** 机器索引：[knowledge-navigation.v1.json](../knowledge/system/knowledge-navigation.v1.json)；用户体验：[UI/产品信息架构](../design/product-experience-architecture.v1.md)。所有已有机制、关联和证据正文留在原文件，继续可研究和修订。

## 1. 原有资产重新归位：分清权威、用途和运行边界

| 资产类型 | 权威位置 | 数量/范围 | AI应怎样使用 | 不可混淆 |
|---|---|---|---|---|
| 分类本体 | `knowledge/system/ontology.v1.json` | L0–L7 / D01–D12 | 从问题找到领域、必要依赖及关联；不是顺序研究任务 | 分类不等于实证结论 |
| 研究问题目录 | `knowledge/system/whole-domain-atlas.v1.json` | 152条问题 | 检查问题覆盖、机制缺口；按需钻研 | 没有152条已证知识的意思 |
| 领域知识正文 | `knowledge/domain/`、`gpt-meme-project-core.v1.md` | 多个专题与跨领域知识 | 解释市场机制、连接旧观点与新证据 | 不能被本导航摘要替代 |
| 专家认知视角 | `knowledge/experts/registry.v1.json` | 22个 | 选择能产生不同解释的专业视角 | 不等于22个已部署Bot |
| Bot职责与交接 | `design/bot-roster.v1.json`、`knowledge/bot-knowledge-profiles.v1.json` | B01–B07 | 仅在多Bot协作/移交任务时使用 | 不是专家数量，也不是运行成功 |
| 可复用项目资产 | `gpt-meme-project-index.v1.json:reference_assets.items` | 65项 | 按当前业务查候选、审查等级、出处 | 仅登记≠已安装 |
| 功能复用台账 | `reference-capability-reuse-ledger.v1.md` | 多项目/能力详审 | 查源码、依赖、风险、许可、失败与复访条件 | 审计不等于调用成功 |
| K1可选来源索引 | `knowledge/source_index.v1.json` | 21项 | `research.py`检索与研究资料候选 | 与65项参考资产定义不同 |
| 根来源登记 | `source-registry.v1.json` | 4项 | 固定根仓库/版本和引用边界 | 不是所有的资料总数 |
| 旧知识卡 | `knowledge/catalog.v1.json` | 15项 | `knowledge.py`提供历史机制/限制候选 | 命中不代表适用或真值 |
| 已编纂研究条目 | `research-units.v1.json` | 3项 | 检查具体研究记录及证据等级 | 不同于152条问题 |
| 工程与真实运行 | **工程PR #16** 的 `src/`、`tests/`、`docs/evidence/` | 现有Mint报告与离线监控原型 | 只有这里的具体分支/证据能说明代码/实测功能 | 不可与PR #14知识分支自动合并 |
| 工作方式与状态 | `current-operating-guidance.md`、`gpt-meme-progress-current.md` | 原准则与完整研究历史 | AI自主研究、产品整合、信息可靠性 | 阶段计划不是知识证据 |

**重要架构决定**：不把全部研究迁进一个新文件夹，不重编号、不抽走原文、不删除过时观点；通过稳定路径、关系和证据等级实现“单一权威源，多入口使用”。

## 2. AI 实际操作路线（自适应，不是每轮固定流程）

```text
自然语言请求
  ├── 问专业机制/新知识 → 研究问题目录 + 相关Dxx正文 + 相关专家 + 原始来源
  ├── 问Mint/钱包/资金 → 对应Dxx正文 + 工程现有能力 + 供应商/链上证据
  ├── 想增加功能/UI → 产品体验规格 + 工程计划 + 现有可复用程序 + E-L7-03
  ├── 报错/失败 → 源码/测试/日志 + D10供应商/时序 + 失败样本
  ├── 研究外部成品 → 65项资产 + 复用台账 + 实际源码与许可
  └── Grok/Bot集成 → Bot职责/交接 + 实际运行手册 + 固定提交和验收证据
                 ↓
       仅加载必要文件 → 推理/开发/验证 → 如有新证据才改原知识
```

**调用原则**：机器路由给出短名单；AI依据语境与证据选择或否定它。不要因“钱包”“资金”两个词同时出现就认定两套专家都必须工作。没有匹配或关键证据缺失时，继续从本体、其他研究、真实来源扩展，不要捏造检索命中。

## 3. 三个典型例子

**例A：**“这个币是不是有庄家控制？”→ `MINT_OVERVIEW` / `SUPPLY_CONTROL` / `FUNDING_ENTITY`候选 → D06筹码、D05资金、D01实际Token/Owner语义 → 查看工程分支供应商Holder候选与真实关系缺口 → 给出证据与公共池/Hub反例，而不是判定庄家。

**例B：**“为什么一批钱包十分钟内都往外转币？”→ `ANOMALY_TIME` / `FUNDING_ENTITY` → 现有`meme-anomaly-discovery-state.v1.md`与资金网络专题 → 工程`wallet_batch_monitor.py`目前只能证明离线窗口算法，不能把它说成实时告警 → 可继续做纯机制研究，或在有授权数据时做产品验收。

**例C：**“把Million接上，并给我容易看的界面。”→ `SOURCE_REUSE` / `PRODUCT_UI` / `GROK_OPERATION` → 功能复用台账 + UI设计 + 工程PR #16 → 审查Million是否能安全只读启动、是否会触发模拟交易、丢同签名多钱包事件 → 优先复用合法可靠的整套业务功能；不因为设计稿就部署网页。

## 4. 如何检查路由能否真正工作

项目已存在不同级别的检索函数：

- `src/solana_meme_os/knowledge.py`：15张历史卡的文字命中。功能有限，不是专家推理。
- `src/solana_meme_os/knowledge_system.py`：字面领域匹配与知识本体静态审计。
- `src/solana_meme_os/expert_brief.py`：专家简报选择；不会真的调用Grok Bot。
- `src/solana_meme_os/research.py`：选21项K1来源与研究反证要求；不是实时交易采集。
- **新增 `src/solana_meme_os/project_navigator.py`**：返回“当前任务可能需要哪些旧知识/源码/视图”的**只读导航短名单**，并可使用`--open-path`按白名单读取**原有知识文件的有界片段、原路径和SHA256**；可对路径和ID做静态检查。它不调用第三方网络、不部署Grok Bot、不生成市场结论。

在 **知识 PR #14 的检出目录**中：

```bash
PYTHONPATH=src python -m solana_meme_os.project_navigator --audit
PYTHONPATH=src python -m solana_meme_os.project_navigator --question "批量转账的钱包是不是同源"
PYTHONPATH=src python -m solana_meme_os.project_navigator --intent MINT_OVERVIEW
PYTHONPATH=src python -m solana_meme_os.project_navigator --open-path knowledge/domain/L3-wallet-actors.md
PYTHONPATH=src python -m unittest tests.test_project_navigator -v
```

`--question`只做**线索匹配**，最终由AI依据真实目标综合判断；`--intent`允许明确选择，无关键词碰撞。当文件涉及PR #16时，命令只报告工程分支位置和状态，**绝不假装该代码已在当前PR #14本地或已能调用**。

## 5. 防止再次乱套的维护方式

- **一个知识结论，一个权威正文**：导航文件只放引用与检索条件；变更现有观点应到原专题，保留反证和来源。
- **一个工程能力，一个真实验收**：需求/设计状态不自动升级到源码实现；代码存在、fixture通过、真实供应商取数、Grok部署分别记录。
- **跨分支交叉引用必须标来源分支**：PR #14知识和PR #16工程可能拥有同名旧文件，不能把错误分支内容覆盖回来。
- **从用户任务驱动导航**：任务可以是专业研究、机制发现、产品UI、工程实现、测试或评估，不强制所有任务都落到V0.2。
- **新资料只增量登记**：先检查已有65项与现有专题是否包含、是否过时、适用范围是什么，再补充或修正；不因为喜欢新名字就造平行分类。
- **可追溯而非无限上下文**：每次读必要路径/相关原文段落，避免每次塞进152条问题、22专家全文与60KB复用台账。
- **知识检索的质量验证**：应检查任务是否路由到相关原文、是否遗漏跨领域关键因素、是否误把旧完成状态当真；仅通过静态索引测试并不证明AI推理质量提高。后续可以使用固定真实问题集做有/无导航的对照评估。

## 6. 当前尚未解决的实际问题

- PR #14 的新导航与 PR #16 工程代码**仍分离**；尚未完成双分支合并及Grok部署。
- 机器路由是字面短名单，遇到隐喻、不成熟表达或新的专业机制仍需要AI主动探索。
- 资金网络与持续监控的真实数据链仍缺；UI只能清楚表达缺失，不能美化为已具备。
- 来源新鲜度、参考资产变化与自动失效检测暂未接入运行任务；新增导航不会自动让外部API可用或产生经济优势。

**结论**：让AI“知道从哪里找、何时该用、哪些不能冒充真实能力”，同时不牺牲原有专业研究的深度。
