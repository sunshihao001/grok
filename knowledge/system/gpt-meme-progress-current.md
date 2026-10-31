# GPT「跟单」｜唯一活跃研究恢复点（2026-10-31，P3-M01）

**当前权威**：GitHub `sunshihao001/grok`，知识分支 `knowledge/whole-spectrum-20261030-v1`（Draft PR #14）中的本文件；工程分支 `research/p24-cross-mint-m01-batch-monitor-20261031`（Draft PR #16）。PR 均未合并，主分支没有这些草案增量。

**持续研究与写作方式**：继续使用 [《持续研究与知识同步 V2》](gpt-meme-continuity-v2.md) 与 [《专业研究写作 Skill V2》](gpt-meme-research-writing-skill.v2.md)，新结果先对照已有 [唯一监控方法专题](../domain/meme-anomaly-discovery-state.v1.md)，用 `AMEND` 修订，不把每个回答复制为新专题。

## 本轮新增：按需外部专业知识补全（V2 原位置修订）

已把此前有用的“AI先理解、行业真实语言/黑话恢复、跨学科知识发现、外部证据主动反证”融合到 [持续研究V2](gpt-meme-continuity-v2.md) 和 [研究写作Skill](gpt-meme-research-writing-skill.v2.md)。当当前知识不能解释现实事件、技术字段歧义或新反例可能改变设计时，主动选择官方文档、源码、论文、GitHub 实现、实际操作者反馈等来源，而不是强制搜索固定数量平台。所得术语须转为可观测数据和反例才入库。已将 Jito Bundle 与同 slot“bundled buyers”的区别修订进 [现有监控方法专题](../domain/meme-anomaly-discovery-state.v1.md)。此补充不改变既有 P3-M01 代码已完成的范围，也不提前宣布 P4。

## 当前研究/工程状态

- **P2.1—P2.5**：概念探索、跨钱包/跨Mint方法比较和优先级筛选已经完成一轮；C02（同群体执行方式变化）和 C05（机会校正的沉默/迁移）获准进入局部 P3；C01（跨币资金再部署）保留候选，暂不做完整图。
- **P3-M01**：原有 `wallet_batch_monitor.py` 已有 1/5/15 分钟窗口分析与14项离线测试。
- **本轮真实新增**：在 Draft [PR #16](https://github.com/sunshihao001/grok/pull/16) 增加 `src/solana_meme_os/raw_tx_adapter.py`、24项离线对抗性测试、合成 `getTransaction` 形状 fixture、[原始解析与 C02/C05 合同](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/p3-m01-raw-adapter-contract.md)、11个合成合同场景。**38项本地离线测试通过，最新 GitHub monitor-tests CI 成功**。适配器→M01 模拟数据串联运行成功。
- **现有能力边界**：原始交易适配器只接受 `mode=fixture`；支持顶层 System Program SOL Transfer，以及顶层 SPL Token/Token-2022 的 Transfer/TransferChecked；`jsonParsed` 与部分已核对格式的 `json`/v0 loadedAddresses；区分 Token Account owner/authority/fee payer；保留 signature、slot、`available_at`、指令路径。单笔 CPI Token/SOL 转移不被猜作 Swap/用户充值。未实现 Pump.fun/Raydium/Meteora/Jupiter 的 BUY/SELL 协议级解析。
- **未知状态**：错误/缺少 TokenAccount owner、Meta/CPI/lookup、Token-2022 扩展或晚到证据均 reject/mark unknown；当前未知使整个 fixture 的 `coverage.complete=false`，是保守粗粒度设计，不是已经完成按 Slot 的采集水位。Fixture 的 `complete=true` 也不是对真实链上全部交易的独立证明。
- **C02/C05**：已有最小字段合同、11个模拟对抗场景，但**未实现两套运行监控器**。M01 聚合 JSON 只有人数统计，C02 必须另外持有 `frozen_group_members` 及原始标准化经济事件流；C05 必须另外有独立合格机会索引和可验证的窗口覆盖。

## 下一步优先顺序

1. **P3-M01 只读小样本核验（最高优先级）**：选择少量可公开核查的真实 Solana 交易签名和官方/协议原始文档，人工写出正确的 TokenAccount owner、Token/SOL Transfer、CPI、版本/LUT、Swap 未知结果。对照适配器，记录可支持与应拒绝的实例，尤其检验实际 RPC 原始响应格式。不要求模拟数据“长得像真实”就算完成。
2. **P3 协议适配**：基于核验结果，选择**一个**协议和**一种**明确交易类型（例如 Pump.fun 的简单 Swap），检查其官方程序 ID、IDL/源码、余额变化与 CPI 语义，再设计可信 BUY/SELL 解析。不凭余额差直接分类，不扩展至所有 DEX。
3. **C02/C05**：复用经过真实语义核验的标准化事件，先测试冻结群体、右删失和机会分母/UNKNOWN 的正确性；不用先建全网监控，也不推断庄家和盈利。

## 阶段晋级判断

**P3 局部实现成立；允许启动小规模只读真实交易语义核查，但不标为 P4 已完成。** 正式进 P4 的前提：可信真实签名和标准答案可复核、支持/拒绝覆盖率已报告、真实缺失区间不会产生假零、正常对照及未触发样本可定义。模型目前不能声明生产实时监控、同控推断或交易盈利。

## 下一轮可直接复制输入

```text
继续 Solana Meme 项目，按照 V2 知识闭环执行。先读取唯一研究恢复点、P2.1–P2.5 方法融合专题与 Draft PR #16 的 raw_tx_adapter.py、tests 和工程契约，不重设架构。

本轮聚焦 P3-M01 的**少量公开真实 Solana 原始交易语义核查**：优先官方原始示例和可独立核对的真实签名，建立逐笔标准答案（交易版本、静态/loaded账户、TokenAccount owner、授权者、fee payer、outer/inner CPI、Token vs SOL 转账、未知Swap及采集时点），将实际 RPC 保存为只读 fixture，运行适配器和对抗测试。支持不足的协议必须标 UNRESOLVED，不得凭余额变化推定 BUY/SELL，不得根据少数签名声称 Mint 的窗口采集完整。

随后从一个具体 Meme 协议中选择最简单、可公开核验的一种 Swap 类型，研究官方程序 ID、IDL 和原始源码，判断何时能增加协议级买卖解码。同步检查 C02/C05 的成员冻结、右删失和合格机会分母所需的具体事件还缺什么。

把真正新增的字段、错误反例与测试结果修订进现有工程文档和监控专题，提交当前 Draft PR、读回核查，更新 GPT Library 镜像及唯一恢复点；无法直接修改 Project 文件时如实报告。最后给出是否具备进入 P4 的具体条件和下一轮可复制输入。
```

## 同步状态声明

GitHub 知识源在 PR #14；实现和测试在 PR #16；GPT Library 的当前便携版和原型目录已生成镜像，**Library 不等于 ChatGPT Project 文件/Instructions 已修改**。此处记录状态以经实际核查的提交、工作流和文档为准；当前没有链上实际测试、Grok Bot 正式部署或自动交易。