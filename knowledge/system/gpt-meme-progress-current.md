# GPT「跟单」｜唯一活跃研究恢复点（2026-10-31，P3-M01）

**当前权威**：GitHub `sunshihao001/grok`，知识分支 `knowledge/whole-spectrum-20261030-v1`（Draft PR #14）中的本文件；工程分支 `research/p24-cross-mint-m01-batch-monitor-20261031`（Draft PR #16）。PR 均未合并，主分支没有这些草案增量。

**持续研究与写作方式**：继续使用 [《持续研究与知识同步 V2》](gpt-meme-continuity-v2.md) 与 [《专业研究写作 Skill V2》](gpt-meme-research-writing-skill.v2.md)，新结果先对照已有 [唯一监控方法专题](../domain/meme-anomaly-discovery-state.v1.md)，用 `AMEND` 修订，不把每个回答复制为新专题。

## 本轮新增：按需外部专业知识补全（V2 原位置修订）

已把此前有用的“AI先理解、行业真实语言/黑话恢复、跨学科知识发现、外部证据主动反证”融合到 [持续研究V2](gpt-meme-continuity-v2.md) 和 [研究写作Skill](gpt-meme-research-writing-skill.v2.md)。当当前知识不能解释现实事件、技术字段歧义或新反例可能改变设计时，主动选择官方文档、源码、论文、GitHub 实现、实际操作者反馈等来源，而不是强制搜索固定数量平台。所得术语须转为可观测数据和反例才入库。已将 Jito Bundle 与同 slot“bundled buyers”的区别修订进 [现有监控方法专题](../domain/meme-anomaly-discovery-state.v1.md)。此补充不改变既有 P3-M01 代码已完成的范围，也不提前宣布 P4。


## 本轮 V2 机制修订：检索与参考项目长期复用（2026-10-31）

**修订范畴：研究方法增强，不是 P3-M01 工程/真实链上能力升级。** V2 现加入：跨官方协议、开源源码/tests/issues、供应商字段、X/Reddit/Telegram实践与失败、必要论文/跨学科的递进检索；对每个重要研究方向比较项目适配、替代实现、数据可得性、正常解释与成本，输出 CONTINUE/PIVOT/PAUSE/REJECT；常驻参考池按实际业务问题反复重访 Hermes/qb-/meme-/Why-Solana/OKX 与外部新候选，记录继承/更正/不可采用与再次触发条件。**所有持续研究的最终输出必须落到下一步最有价值的执行任务，且最后一项是可复制提示词。**

新增可复用竞争实现入口：Solana 官方 transaction-introspection + transaction-v1-examples、0xfnzero/sol-parser-sdk、Raydium CP-Swap、Yellowstone、Helius/Bitquery能力文档、实际开发者索引断流讨论。它们是本轮检索/阅读的源候选，不等于这些库已在当前 Python 适配器安装运行或其市场效果已实测。P3-M01 继续维持 fixture-only、legacy/v0部分转账、v1 fail-closed 和未知事件不当作零交易的真实边界。

**主研究方向依然是**：对少量真实公开签名核验当前解码语义 → 比较官方/成熟解析器与自制适配器的可靠性/成本 → 选择一个协议的经济 BUY/SELL 解码；知识主线同时继续 qb/Hermes 关键钱包和库存/时点机制，不让通用协议课程挤占 Meme 业务目标。Grok S1 云电脑仍独立待验收。


## 当前研究/工程状态

- **P2.1—P2.5**：概念探索、跨钱包/跨Mint方法比较和优先级筛选已经完成一轮；C02（同群体执行方式变化）和 C05（机会校正的沉默/迁移）获准进入局部 P3；C01（跨币资金再部署）保留候选，暂不做完整图。
- **P3-M01**：原有 `wallet_batch_monitor.py` 已有 1/5/15 分钟窗口分析与14项离线测试。
- **本轮真实新增**：在 Draft [PR #16](https://github.com/sunshihao001/grok/pull/16) 增加 `src/solana_meme_os/raw_tx_adapter.py`、24项离线对抗性测试、合成 `getTransaction` 形状 fixture、[原始解析与 C02/C05 合同](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)、11个合成合同场景。**此前38项本地离线测试通过；此后新增v1失败封闭及7项官方示例回归，六个测试文件当前共71项测试方法，GitHub monitor-tests CI对最新工程提交成功**。适配器→M01 模拟数据串联运行成功。
- **现有能力边界**：原始交易适配器只接受 `mode=fixture`；支持顶层 System Program SOL Transfer，以及顶层 SPL Token/Token-2022 的 Transfer/TransferChecked；`jsonParsed` 与部分已核对格式的 `json`/v0 loadedAddresses；区分 Token Account owner/authority/fee payer；保留 signature、slot、`available_at`、指令路径。单笔 CPI Token/SOL 转移不被猜作 Swap/用户充值。未实现 Pump.fun/Raydium/Meteora/Jupiter 的 BUY/SELL 协议级解析。
- **未知状态**：错误/缺少 TokenAccount owner、Meta/CPI/lookup、Token-2022 扩展或晚到证据均 reject/mark unknown；当前未知使整个 fixture 的 `coverage.complete=false`，是保守粗粒度设计，不是已经完成按 Slot 的采集水位。Fixture 的 `complete=true` 也不是对真实链上全部交易的独立证明。
- **C02/C05**：已有最小字段合同、11个模拟对抗场景，但**未实现两套运行监控器**。M01 聚合 JSON 只有人数统计，C02 必须另外持有 `frozen_group_members` 及原始标准化经济事件流；C05 必须另外有独立合格机会索引和可验证的窗口覆盖。

### 官方资料发现的版本边界（2026-10-31）

新外部核查确认 [Solana Versioned Transactions](https://solana.com/docs/core/transactions/versioned-transactions) 官方文档称 v1 已激活，v1 不使用 ALT，而是以内联账户和 transactionConfig 表示新的交易配置。现有 PR #16 原始适配器仍仅支持 legacy/v0；**version=1 应输出 UNSUPPORTED_TX_VERSION 且使窗口覆盖不完整，不得误记为没有交易**。工程 PR #16 已加入针对 v1 的明确 fail-closed 合成测试，等待/核查 GitHub CI；未实现 v1 解码或真实交易验证。后续官方 introspection 已有支持v1的实现参考：https://solana.com/docs/core/transactions/transaction-introspection 。此修订不更改 P3 当前阶段判断。

### 本轮公开文档样本核查与两项重要修正（2026-10-31）

**已落地、可回读**：PR #16 的 `fixtures/official-solana-gettransaction-samples.json` 固定保存Solana官方 getTransaction 文档提供的**2笔Devnet签名、3份响应编码**，以及 `tests/test_official_gettransaction_examples.py` 的7项回归。Legacy原生SOL transfer（签名 `4ReKprwf…`）正确计为1 SOL独立资金事件、不产生买入；v0 ATA Create（`56rgv1Fq…`）的 json/jsonParsed 均无假BUY，但因尚未完整支持账户创建/CPI经济语义而报告未知。**没有独立 RPC 再抓取**；官方样本未提供历史可得时间，测试注入的 `available_at` 仅是fixture时点，不适合证明前兆实时性。来源固定到 [官方文档commit 4cb392f](https://github.com/solana-foundation/solana-com/blob/4cb392f61c2ab0f8953cc314378aaf8256b7699a/apps/docs/content/docs/en/rpc/http/gettransaction.mdx)。

**修正两个真实代码错误**：
1. `meta.err` 缺字段过去被当作 `err:null`（成功）；现改为 `TRANSACTION_STATUS_UNKNOWN` 并阻止事件输出。
2. `available_at>as_of` 过去仅降级覆盖，但资金事件可能已经输出；现调整为先阻断，禁止未来证据渗入 `funding_events/events`，并标记未知。

**新外部技术约束**：v1配置错误可导致 `getBlock` 整块失败；Token-2022 TransferFee、TransferHook和ConfidentialBalance对净到账、CPI与可见金额有直接影响。参见 [现有监控方法专题 §9.1](../domain/meme-anomaly-discovery-state.v1.md) 与 [P3-M01工程契约](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)。**代码没有因此自动支持v1/Swap/特殊Token-2022**。最新工程提交 `d79eafe647542b29745b2a814850be4000d9ccd8` 的 [GitHub CI](https://github.com/sunshihao001/grok/actions/runs/41216119575) 已成功；PR#14/#16仍未合并。

**阶段**：P3 源语义验证继续；已有**官方文档响应格式**核查，未完成**独立RPC重取＋同一签名跨提供者对账**；不进入 P4 大规模实证。下一步优先独立只读重取这两笔签名（`maxSupportedTransactionVersion:1`、固定commitment、记录真实 fetched_at），再选一个协议和一类Swap做可核验解码与不支持样本测试。

## 下一步优先顺序

1. **独立只读 RPC 对账**：对官方文档两笔已公布Devnet签名，由经授权的可用节点使用 `getTransaction`、`maxSupportedTransactionVersion:1` 与固定 `commitment` 读取真实响应，记录采集时间、请求参数、可用性和差异。当前环境对 RPC POST/完整私有历史不可直接取回，因此不得称本轮已完成独立节点核查；无需接私钥。
2. **一个 Meme 协议、一个 Swap 类型**：先固定官方 program ID 与 IDL/源码、指令 discriminator 和CPI/余额校验，在明确正反例下才添加 BUY/SELL 解析。优先已有开放实现；未找到原始交易、转账和资产语义时宁可 `UNRESOLVED`。
3. **C02/C05 依赖**：冻结群体成员、维护资金/动作 as-of 记录；独立定义发行机会和覆盖水位，避免因 v1 整块失败或未知CPI产生虚假群体沉默。

## 阶段晋级判断

**P3 局部实现成立；允许启动小规模只读真实交易语义核查，但不标为 P4 已完成。** 正式进 P4 的前提：可信真实签名和标准答案可复核、支持/拒绝覆盖率已报告、真实缺失区间不会产生假零、正常对照及未触发样本可定义。模型目前不能声明生产实时监控、同控推断或交易盈利。

## 下一轮可直接复制输入

```text
继续 Solana Meme 项目 P3-M01，按照 V2 知识闭环执行。读取唯一进度、现有知识专题第9.1节和 Draft PR #16 的 raw_tx_adapter.py、official-solana-gettransaction-samples.json、测试与工程契约，勿重建系统。

优先取得官方文档中两笔Devnet签名的独立只读RPC回包（使用 maxSupportedTransactionVersion:1、固定 commitment），保留真实 fetched_at、数据来源、返回状态并与仓库保存的官方样本逐字段对账。若环境不能GET/POST该数据，明确报告阻碍；不要将合成 available_at 当成真实取得时间或把缺失meta/未知版本当0事件。

接着选择一个具体 Meme 协议、一种 BUY 或 SELL 类型，研究固定 program ID/IDL/源码与可公开核验签名，以最小独立协议适配器正确区别顶层、CPI、Token账户owner/delegate、费用、WSOL/Token2022特殊金额；给对抗性正负例，只允许可解释的成功动作进入 M01，未知保留 UNRESOLVED。C02/C05 只在可信 as-of 事件与独立完整性可得时继续。

只把新证据和修正写回已有工程合同及M01知识专题；提交GitHub PR#16/#14、回读复核、同步个人 Library 同名镜像并更新本唯一恢复点。不得签名、下单、部署正式监控；最后报告已实际完成的代码/来源/CI、未支持范围、是否进入P4和下一轮输入。
```

## 同步状态声明

GitHub 知识源在 PR #14；实现和测试在 PR #16；GPT Library 的当前便携版和原型目录已生成镜像，**Library 不等于 ChatGPT Project 文件/Instructions 已修改**。此处记录状态以经实际核查的提交、工作流和文档为准；当前没有链上实际测试、Grok Bot 正式部署或自动交易。