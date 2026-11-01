# Release backlog

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
