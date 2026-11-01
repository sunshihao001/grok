# Release backlog

> **现行唯一产品实施次序**：[《四阶段成品交付计划 V0.1》](product-delivery-plan-v01.md)。优先按 V0.1 Mint报告 → V0.2钱包/资金 → V0.3持续异常 → V1.0 Grok入口逐项真实验收；各旧节的历史研究待办只作参考，不再启动平行规划。当前公开池真实可读，钱包/Dev完整报告未验收。

## 最新实际运行恢复（2026-11-01）

V0.1真实免费多来源Mint预览已通过：[DEX Screener + RugCheck 5池/20条Holder候选/Creator](evidence/v01-real-rugcheck-holder-2026-11-01.md)。最新已完成一条跨源反例：某Holder候选Owner恰为已知PumpSwap池，不能列为独立聪明钱。**现阶段下一产品主任务转向V0.2真实钱包/资金关系的成熟成品能力验收**，优先RugCheck insider graph、Million funding/owners，按来源/许可/只读安全/实际行为审查。未授权OKX真实完整报告、独立链上钱包归因与Grok云电脑仍未通过；旧下文“OKX唯一剩余硬阻断”的描述仅指完整增强版，不再阻断已可用的免费V0.1基本报告。

## 第一优先：先让成品跑起来，再增强业务能力（2026-11-01）

- [x] **首个薄报告入口已写入工程Draft PR #16**：`src/solana_meme_os/mint_report.py`直接消费现成OKX`token-research`标准JSON`{ok:true,data:{workflow,address,chain,core,structure,launchpad}}`；本地使用`fixtures/okx-token-research-demo.json`运行成功，生成`report.md`和`report.json`，新增6/6单测通过，**仅synthetic fixture**。
- [ ] **最小真实成品验收**：在授权且无自动交易/签名/x402自动支付的联网环境中，运行OKX的单Mint现成workflow，保存准确原始JSON，核查输入Mint、null、字段意义、链上/收到/处理时点和每次Premium消耗；用本脚本输出实际可读报告。只有此步骤验收通过才称`V0.1 REAL-MINT REPORT RUNNING`。
- [ ] **第二个真实结果**：同Mint相隔一段时间再次运行，用当前`monitor.py`仅比较经过字段定义确认的公开指标；缺失不得填0，基金/交易事件不可由余额差猜测，时间不能事后回填为实时可见。
- [ ] **第三个业务能力**：需要长期钱包监控时，再评估Million可否以**独立只读子系统**提供发现/funding/live/flows，先确保不会执行交易、不会丢同签名多钱包观察且可恢复断线；没有通过不依赖它发布群体异常。对协议Swap缺口再择FnZero或其他成熟SDK。
- [ ] **运行交付**：独立验收Node/Rust/Python实际依赖、API密钥隔离、保存目录/重启、故障日志/调用成本、Grok云电脑环境、单命令部署；所有步骤由AI负责专业实施和回读检查，用户只负责必要授权与是否接受结果。

**重要区别**：本轮已交付**离线可运行的最薄产品拼装件**，还没有真实Mint数据自动采集或长期运行；不再把无休止研究、21专家文档或71项工程单测等同于用户已能使用的成品。

## Initialization (completed locally)
- [x] Source pins, agent roles, migration map and Grok Bot setup instructions.
- [x] Read-only source validation, per-mint state, observed deltas, event de-dup and JSONL log.
- [x] Explicit fixture/live separation and rejection of stale live input.
- [x] GMGN CLI raw-only read collector with no guessing of metric values.
- [x] Six offline tests; CI workflow authored.
- [ ] GitHub-hosted CI job result observed after push.

## Real monitoring prerequisites
- [ ] Capture real GMGN CLI JSON, field descriptions, timestamp semantics and units without committing secrets.
- [ ] Test mappings for liquidity and holder share, add authoritative chain references for events, measure drift and missingness.
- [ ] Add single-writer locking/recovery or SQLite before Grok scheduling/multiwriter workflows.
- [ ] Port wallet and deployer intelligence one tested observation at a time.
- [ ] Reproduce actual historical cases; measure false alerts, coverage, abstentions, and detect data leakage.
- [ ] Human-review rule thresholds and release notes; current numbers are **unvalidated examples**.
- [ ] Actually create Grok Bots, the shared Skill and a tested Routine within Grok app.

## Rule promotion packet
Problem, version, owner, raw sources/commits/times, units, proposed mechanism, competitive explanation, tested baseline, counterexamples, false alerts, regression commands/results, rollback and explicit human approval.

Rule Engineer passing local tests **does not** imply an economically valid or production-ready monitoring rule.

## Knowledge migration (preserved, with explicit uncertainty)
- [x] Import 15 source-pinned knowledge units covering Solana lifecycle, GMGN fields, wallet roles/funding, structure, risk, evidence and tool failure modes.
- [x] Connect a deterministic knowledge selection function to monitor observations and plain-language research question routing.
- [x] Add regression tests for relevant concept retrieval, source integrity, negative cases and missing-data behavior.
- [ ] Verify original external theoretical references, look for corrected recent primary sources, and distinguish stale assumptions from currently valid mechanisms.
- [ ] Import concrete real on-chain cases and source-linked failures, not only conceptual documents.
- [ ] Test whether Grok Bot with knowledge improves judgment vs a no-knowledge baseline using blinded examples; measure false alerts and missed events.
- [ ] Improve semantic applicability and source reading in an actual Grok Bot instead of claiming literal keyword routing is full expert reasoning.

## On-demand research architecture
- [x] Read the pinned Why-Solana-Memecoins-Are-Over research methods, error audits, structural-mechanism tests, economic edge failures and source licenses.
- [x] Add a small source index of 17 pinned documents instead of copying another entire research repository.
- [x] Implement bounded optional source preview and structured research intake with a decision-time availability check.
- [x] Add offline tests for source selection, authenticity/allowlist, time-of-knowledge rejection and no-edge claims.
- [ ] Run genuine source retrieval in a configured Grok Bot and inspect live handoffs; not the same as unit tests.
- [ ] Add real transaction datasets and delayed-outcome evaluation, including null baselines, execution costs and alerts not selected on winners.
- [ ] Compare Grok with/without the on-demand source workflow under blinded case review to test reduction in unsupported assertions.

## 2026-11-01｜完整Mint只读能力联合验收（跨PR引用，不升级运行状态）

**工程立场**：现有P3-M01是fixture-only原型，GitHub测试通过不代表真实RPC/外部SDK/Grok云电脑可用。知识Draft PR #14在`knowledge/whole-spectrum-20261030-v1`，它的base与本工程Draft PR #16（`main`）不同，不能认为本工程自动继承了21专家审查和外部能力台账。

本阶段**先不新开发通用DEX解码器，也不迁移大框架**。按同一个Mint业务任务验收：
- [ ] **现成按需Mint报告**：在明确授权、禁止x402自动支付/无私钥的隔离环境，运行OKX `onchainos workflow token-research --address <mint> --chain solana`，保存源码SHA、每条子请求/失败/null/请求费用及可得时间。将输出与旧`qb-/sikk_gmgn_token_report.py`关键地址矩阵的业务需求逐项比较，不复制GMGN旧执行依赖或标签阈值。
- [ ] **现成持续钱包监控安全验收**：先评估Million只读完整成品；屏蔽交易执行及公网操作接口，验证同一签名两个订阅钱包均能被记录，且不会错误加倍计算一笔链上Swap；如源程序依赖`LiveEvent.signature @unique`和首个命中钱包`break`，**不得通过**真实群体完整性验收。
- [ ] **两时点持仓与发行历史对账**：当前TokenAccount快照与观察窗事件净变独立核对；数量保留原子金额/decimals，Token移转不自动称BUY/SELL；pumpwatch`seen_at`是本地入库时点，不将历史回补Mint计为当前Dev发行频率。
- [ ] **观察覆盖与成本**：记录源、slot/checkpoint、`observed_at`、超时/429/断流/回补、标签来源及未知状态。OKX Free套餐无WS，Million所需Helius额度/成本和服务安全需按实测核对；不因为安装一个SDK就标记运行完成。
- [ ] **Grok与跨PR工程集成**：在形成真实只读样例和负例后，再讨论如何将既有专家知识/旧qb报告输出/成熟成品服务通过最薄接口调用交到Grok云电脑。S1仍需实际创建/运行/失败复测；若知识PR和工程PR需合并，应独立检查共同基线/冲突后再申请审阅，不在这里自动合并。

**本轮新增竞品参考**：Solana Foundation MIT `solana-microscope`是单Program可恢复监控成品，重在D10可靠性，不替代任意Mint业务分析；Helius DAS/Parsed Events可做余额和事件独立对照，需授权和费用核实；详情和21专家冲突在[知识PR#14复用台账](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/reference-capability-reuse-ledger.v1.md)。**此处只是实际工程待办，不表示已经执行任何在线成品或主网监控。**

## 2026-11-01｜V0.1报告升级：从原样打印到业务候选摘要

- [x] 把已有OKX`token-research`官方输出封装成业务候选摘要：Holder地址/holdAmount/holdPercent、`fundingSource`提示、Cluster统计、Dev/Bundle存在状态、供应商时间字段与JSON来源路径。对错误/缺失/新接口形状fail-closed，不把未知当0，也不把供应商统计当已证实异常。
- [x] `fixtures/okx-documented-field-shapes-synthetic.json`合成数据演示与新模块12/12单测通过；加入旧Library快照P3-M01代码离线联合50/50通过。本轮本地未检出任何真实主网数据或已安装OKX CLI，GitHub CI独立查看。
- [ ] **阻断真实V0.1**：当前执行机没有`onchainos`CLI/已授权会话，容器外网DNS无法解析；官方OKX调用需要可用授权，SDK可能遇到x402自动支付流程，**绝不可在无控制环境或加载钱包凭据的条件下试运行**。须在可联网、明确只读范围、没有付款和交易凭据的隔离环境先验单一Mint原始输出，保留失败/限速和真实费用记录，再测试本薄适配。
- [ ] 对首份真实源报告检查`holderWalletAddress`/LP/vault、资金来源、供应商`requestTime`与观察时间；按需查询不等于连续订阅/全市场覆盖。
- [ ] 持续监控仍在下阶段：同Mint两时点 → 钱包事件订阅/增量 → 独立余额核对 → 批量异动归因。若此流程不需要Million整库，不要为Web UI提前装交易模块。

## 2026-11-01｜工程恢复前先恢复完整参考池与22位专家

当前所有曾引用的成熟成品/SDK/数据源/研究/从业者资料，已在知识Draft PR #14的[`knowledge/system/gpt-meme-project-index.v1.json`](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json)登记为`reference_assets.items`共**65项**，核实程度各不相同；原5项`source_repos`是历史固定源，不应被误以为全部。原21专家经真实产品职责缺口审查新增`E-L7-03`（开源成品集成/交付，合计22位知识视角，**不是第8个Bot**）。工程启动V0.1时先由该视角对比`OKX token-research`与备选项目的安装、接口、支付/签名风险和最小修改成本；无需安装65项。

**仍保持当前交付顺序**：V0.1运行真实Mint→现有报告；之后两时点观察→持续钱包监控；具体缺口才回访Million/pumpwatch/FnZero。工程PR #16不自动拥有知识PR #14内容，它们base不同；实际部署前需在同一可审阅候选分支做代码与知识版本对照。参考登记不会让fixture测试变成真实数据，也不等于Grok Bot已配置。

## 2026-11-01｜V0.1确实取得真实Mint公开池数据，但完整钱包/Dev报告未交付

**已交付**：工程新增`src/solana_meme_os/public_pair_report.py`、`mint_v01.py`（统一入口）、对应13项独立单测，加上原`mint_report.py`已可“直接输入Mint→免费公开池快照”，或“输入Mint+已获授权的OKX结果→有关键钱包/资金线索的报告”；没有自动签名/支付/交易/执行OKX客户端。现有OKX整套业务仍保留为优先完整来源。

**真实在线验收**：[GitHub Actions 41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009) 在公共DEX Screener API对两枚真实Mint取到5池和7池数据，含源响应SHA、获取时点与原始JSON；[证据记录](evidence/v01-real-public-pair-readonly-2026-11-01.md)附实值、哈希和GitHub Artifact，另有一次BONK返回`[]`并标`COVERAGE_UNKNOWN`，不认定“无池”。本地容器DNS失败，但已通过GitHub runner真实取数且实际下载回本地验证SHA与Mint池配对。**这仅通过`REAL_PUBLIC_POOL_SNAPSHOT`，未通过`FULL_REAL_MINT_WALLET_DEV_REPORT`**。

**当前最短剩余任务**：只有一件必须补齐：在有明确授权且没有x402自动付款能力的隔离环境安全获取真实OKX `token-research` 结果；使用现有`mint_report.py`报告与这次真实池数据同Mint核对日期、池/账户/owner/资金来源/Dev覆盖。不再新增交易执行、全市场订阅或Dex专用适配器。若OKX权限无法取得，再从65项已登记源中比较实际能提供Holder、Dev历史的其他成熟成品/公开只读数据服务，而不是把DEX Screener不足当成一套完整情报产品。

**专业观察**：同Mint可能同时作为base/quote出现在PumpSwap/Orca/Pump.fun多个池；价格字段仅可归属目标作为base时的quote，池买卖次数是池级统计而非钱包交易事件；聚合前要去重/明确分母。E-L7-03只负责交付、E-L1-01交易事实、E-L3-02资金关系、E-L0-02供应商语义、E-L6-01反证按现有知识参与，不新增专家/Bot。

