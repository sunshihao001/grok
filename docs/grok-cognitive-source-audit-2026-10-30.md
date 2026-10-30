# Grok 专家认知资产复盘与来源准入审计｜2026-10-30

> **唯一执行对象**：`sunshihao001/grok`。本审计基于未合并的 Draft PR #5 的固定提交 `481e70bea2b470a3cf50011d365a8e9fc4917184`，而非 `main` 的 62 文件旧基线。审计补丁位于独立分支，不修改主分支、既有 15 卡、21 快照、原始来源或实盘交易行为。
>
> **审计深度**：对 15 张旧卡、21 份快照与 21 个 K1 来源完成逐条结构/来源清单和准入处理；并对研究代码及相关测试做针对性审查。未逐行复核 21 份原文的所有结论，也未独立复算 K2 链上数据。标记 `pinned_snapshot_unverified` 不等于发现污染或证伪。
>
> **关键纠偏**：早期优先是来源调查顺序，不是自动真值；后期参考项目的观察、方法和统计结论必须分开审核。时间维度与证据层级是两条独立轴。

## 1. 上一轮答案复盘

1. **保留**：GPT 开发 / GitHub 固定版本 / Grok 只运行，原始事实与机制/盈利证据隔离，K0/K1/K2，F0–F6 与只读边界。
2. **撤回**：“项目仅有 62 文件监控原型”的总体概括——那只描述 `main`，未包括 PR #5 的 P0 草稿。117 项测试属于 PR #5 文档记录的离线验收，不是本审计新增测试已通过。
3. **纠正**：“11 个后期文档一律污染”——PR #5 实际有 13 个 pinned 2026-10-09 外部来源；本补丁仅赋予临时 `review_only` 的**使用权限状态**，不判定文件真假、不删索引。
4. **不重复开发**：PR #5 已定义 L0–L7、D01–D12、F0–F6、B01–B07、K0/K1/K2、Grok P0 运行入口与 OKX 保存 JSON 解析。优先补跨入口统一准入，不另造相似本体或 Bot。
5. **需补证明**：实际 Grok 云端固定 SHA 运行、真实只读 K2 数据、完整负对照、可实现的 F4/F5 和人工 F6 发布仍未验证。

## 2. 认知资产分类

| 资产 | 当前数量 | 当下权威 | 实际作用 / 禁止推论 |
|---|---:|---|---|
| 旧知识卡 | 15 | `knowledge/catalog.v1.json` | 原始观察的问法、机制假设、反例需求；不证明行情或 Alpha |
| 历史原文快照 | 21 | `knowledge/legacy-snapshots/manifest.json` | 文字溯源与历史假设；非独立 K2 |
| K1 按需来源 | 21 | `knowledge/source_index.v1.json` | 按问题指向固定文档，不能代替证据 |
| K1 准入状态 | 21 | `knowledge/source-admission.v1.json` | 8 context_candidate / 13 review_only |
| 外部研究摘要 | 3 | `knowledge/system/research-units.v1.json` | `external_reported`，不自动进入默认研究包，不是本项目复算 |
| 证据门槛 | 7 (F0–F6) | `knowledge/system/filter-policy.v1.json` | 研究准入和证据条件，不表示已经 PASS |
| 数据适配与运行 | 各组件 | `src/solana_meme_os/`、`scripts/` | P0 合成测试；实盘行情、交易签名与 Grok 云部署待验 |

## 3. 15 张旧知识卡逐项保留表（结构核查）

状态分布：`{"source_contract":3,"documented_legacy_method":11,"unverified_hypothesis":1}`。这些卡的来源主要来自 Hermes / meme- / qb-，没有直接把 Why-Solana 2026-10 研究写入这 15 张卡。每卡仍须按具体原始事件核查应用条件；本次不逐句认证结论。

| ID | 候选认知对象 | 原状态 | 原始仓库 | 当前决定 |
|---|---|---|---|---|
| `candidate-entry` | 市场候选的来源 ≠ 质量结论 | `source_contract` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `market-lifecycle` | 发行、迁移、建池、流动性阶段必须分别建模 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `token-security` | 权限和卖出限制风险是不同机制 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `liquidity-depth` | 流动性变化不等于一定撤池 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `wallet-roles` | 钱包角色由行为形成候选，不是实名身份 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `funding-graph` | 资金同源是关联线索，不等于同一个人 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `sybil-wash` | 热闹可能被制造：Sybil/Wash/协调行为的区分 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `concentration` | Top10集中度变化需要区分地址与经济控制 | `documented_legacy_method` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `deployer-history` | 部署者历史和系列发行行为 | `documented_legacy_method` | -, qb- | 保留为问题/机制候选；不继承实际市场验证 |
| `gmgn-field-combinations` | GMGN组合指标只是形成问题的工具 | `documented_legacy_method` | -, qb- | 保留为问题/机制候选；不继承实际市场验证 |
| `evidence-synthesis` | 证据链、反证与缺失证据独立呈现 | `source_contract` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `research-states` | Gate本质是研究状态而非交易指令 | `source_contract` | - | 保留为问题/机制候选；不继承实际市场验证 |
| `reclaim-theory` | 第一控盘区、POC/AVWAP回收属于待验证的策略理论 | `unverified_hypothesis` | meme- | 保留为问题/机制候选；不继承实际市场验证 |
| `gmgn-raw-prototype` | 旧工具原型中的分类是启发式而非真相 | `documented_legacy_method` | qb-, - | 保留为问题/机制候选；不继承实际市场验证 |
| `anti-false-completion` | 计划、模拟测试、已部署、有效判断必须分别核验 | `documented_legacy_method` | qb- | 保留为问题/机制候选；不继承实际市场验证 |

**高风险已知项**：早期关于“几秒内买入≈内部人”“共享 CEX 出金≈同一控制者”“同步卖出≈同控”“价格相关性≈相同操作者”“默认 0.8 置信度”等说法不能凭原文继续推断；只可作为反例/待证伪问题。详见 `knowledge/legacy-audit.md`。

## 4. 21 份历史快照逐项清单（只核对来源元数据）

快照的 Git blob 完整性已有历史单元测试；**字节相同仅证明材料没被改写，不证明原文判断正确**。其中 Hermes 领域文档不作为 Grok 命令/运行时依赖；meme 理论不自动成为 Solana 策略；qb 的 Hermes Harness 只作治理方法参考。

| 已保存路径 | 来源仓库（以 manifest 为准） | 当前审核状态 |
|---|---|---|
| `knowledge/legacy-snapshots/solana-learning/L05.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L06.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L07.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L08.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L09.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L10.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L11.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L12.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L13.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L14.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/L15-GMGN.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/solana-learning/field-forensics-toolbox.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/domain-contracts/wallet-roles.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/domain-contracts/wallet-structure.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/domain-contracts/evidence-chain.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/domain-contracts/handoff-schema.md` | `sunshihao001/-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/theory/first-control-zone.md` | `sunshihao001/meme-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/theory/structure-risk-fields.md` | `sunshihao001/meme-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/theory/knowledge-source-map.md` | `sunshihao001/meme-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/method/anti-fake-completion.md` | `sunshihao001/qb-` | `pinned_snapshot_unverified` |
| `knowledge/legacy-snapshots/method/calibration.md` | `sunshihao001/qb-` | `pinned_snapshot_unverified` |

## 5. K1 21 个来源的逐条准入清单

约束：固定到提交的链接证明引用位置，不代表数据、数字和主张正确。以下 `review_only` 是**默认路由隔离，不是永久封禁**。专项审查可明确 `--include-review-only` 取回候选，但仍不得把它标为 `locally_reproduced` 或用其自动通过 F2–F6。

| 来源 ID | 仓库 | 提交前缀 | 准入状态 | 原文路径 |
|---|---|---|---|---|
| `research-methodology` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `docs/METHODOLOGY.md` |
| `failure-modes` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `docs/PITFALLS.md` |
| `time-safe-features` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `post_detection_forensics/feature_dictionary.md` |
| `temporal-leakage-audit` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `post_detection_forensics/temporal_leakage_audit.md` |
| `coordination-null-model` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `coordination_detection/results.md` |
| `economic-cycle` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `economic_mechanics/results.md` |
| `funding-graph-control` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `funder_network/results.md` |
| `tradability-vs-structure` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `post_detection_edge/README.md` |
| `pre-registered-failure` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `alpha_patterns/README.md` |
| `reproducible-pipeline` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `code/README.md` |
| `historical-mechanism-vs-profit` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `docs/ACT_IV.md` |
| `hermes-wallet-method` | `-` | `2bf694b37c` | `context_candidate` | `learning/10.md` |
| `hermes-source-relations` | `-` | `2bf694b37c` | `context_candidate` | `learning/11.md` |
| `hermes-gmgn-dimensions` | `-` | `2bf694b37c` | `context_candidate` | `learning/15-GMGN字段组合地基.md` |
| `meme-first-control-zone` | `meme-` | `5ab2b01f08` | `context_candidate` | `03_语义概念/第一控盘区定义_v0.1.md` |
| `meme-sources` | `meme-` | `5ab2b01f08` | `context_candidate` | `SOURCE_OF_TRUTH.md` |
| `gmgn-collector-example` | `qb-` | `8377ad5611` | `context_candidate` | `sikk_gmgn_token_report.py` |
| `meme-falsification-experiment` | `meme-` | `5ab2b01f08` | `context_candidate` | `09_规则与回测/反证实验设计_v0.1.md` |
| `meme-multistrategy-direction` | `meme-` | `5ab2b01f08` | `context_candidate` | `docs/project_ai_context/12_DIRECTION_SHIFT_MULTI_AGENT.md` |
| `external-post-detection-results` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `post_detection_edge/results.md` |
| `external-reentry-negative` | `Why-Solana-Memecoins-Are-Over` | `9a7ad51d56` | `review_only` | `known_group_reentry/results.md` |

### 关于 Why-Solana 的早期版本

可供审查的**初始 GitHub 提交**：`5709d49bc06597670f04ee50135227c7a3818933`（2026-07-30），含 `docs/METHODOLOGY.md`、`docs/PITFALLS.md`、`docs/SPLIT_PHASE1.md` 等。该提交自身也是对部分 2024–2025 事件的**事后重建**，不是当年实时采集日志，不可单凭“早”获得可信身份。

本阶段不把初始版本静默替换进现有 K1 索引，因为 PR #5 的 `knowledge/system/source-registry.v1.json` 当前对每个仓库固定唯一提交，并校验与 K1 索引一致。若未来需要同仓库多版本并存，先定义`source_id + revision + path`的多版本契约及许可证审计，再经独立测试引入。

## 6. 三条实际路由与本补丁的处理

- `research.py.select_sources`：默认只输出 `context_candidate`；专项查阅必须显式 `--include-review-only`，返回的条目仍携带 `admission_state`。
- `research.py.build_packet`：外部 `research_unit_candidates` 的原文也受同一个准入状态限制，不再从另一路绕过隔离。
- `bot_knowledge.py.build_role_brief`：B01–B06 默认不收到 `review_only` 文档候选；B07 冻结监控不允许显式启用这些来源。
- `knowledge/source-admission.v1.json`：覆盖 K1 **每一个现存 ID + commit + path**；缺项或被悄然替换时 fail closed。
- `validate_handoff`：保留现有“文献 ≠ 原始链上事实”的验收原则，不删除历史引用；只有经过独立审查的 K2 才能提升事实主张。

**边界**：`context_candidate` 不是 `trusted`、`approved` 或 `independently_validated`；它只表示可以默认读取作问题与方法背景。

## 7. 当前执行顺序——不偏离 PR #5 已冻结的研究方向

1. **S0 本次**：来源准入覆盖率、三条检索旁路阻断、文档反思、离线回归。与 PR #5 的 L/D/F 本体兼容。
2. **S1**：PR #5 经人工审核、固定 SHA，在真实 Grok 云电脑进行只读合成程序验收。没有云端真实日志不能叫已部署。
3. **S2**：在明确权限/价格/无自动付费边界后，测试一个 OKX 或 Solana RPC 的只读数据来源；采集日志保存真实接收时间、单位和错误。
4. **S3**：用 K2 链上材料复算钱包/资金案例，并建立未命中与失败样本。外部报告仅为假设，不能替代本项目盈利验证。
5. **S4**：独立审核通过的冻结纸面监控规则、单写入者、恢复与暂停；不自动交易、不签名、不广播。

## 8. 已识别的 PR 冲突与交付纪律

当前仍有 #3（KNOW-001）、#7（KNOW-002，叠在 #3）和 #8（KNOW-003，叠在 #7）草稿，和 #5 开发线可能有重叠；不能把这些 PR 的测试数和功能简单累加，也不能直接合并到 `main`。

本审计分支基于 PR #5 固定 SHA 构建，目的仅是给当前知识体系补来源准入和审计证据。不得借此改写交易规则、移植 Hermes、启动 Grok Bot、安装 OKX 交易/支付工具或发起真实订单。

## 9. 验收与剩余不确定性

- JSON 21/21 来源匹配，任一 ID 缺失或 pin 改动均应拒绝。
- 默认问答和专业 Bot 查询不得选中 `review_only` 来源；显式人工检视可以恢复候选，但不生成可信市场结论。
- 三个 `external_reported` 研究摘要默认不作为推荐研究结论；专项检视时仍能引用原始 pin。
- 15 张旧卡与 21 快照原样保留，旧知识测试及全部其他离线测试继续通过（实际 CI 状态须单独核查）。
- 尚无足够证据确定用户所说的“污染物”具体涉及哪些后期字段、标注或计算链路；目前的分类是**保守、可逆、待核查**的使用权限控制，不是污染调查最终裁定。
