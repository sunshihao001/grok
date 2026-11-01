# P2.4 跨 Mint 重复行为研究 × P3-M01 离线钱包批次监控原型（2026-10-31）

**状态**：5 种研究候选已设计；M01 为离线 fixture-only 原型。没有真实交易账户、私钥、RPC 采集器、实盘成交或自动告警部署。本文件不是盈利信号。

## 研究依据和保留边界

- Solana 官方交易与账户语义：https://solana.com/docs/rpc/json-structures 、https://solana.com/docs/tokens 、https://solana.com/docs/core/transactions/transaction-introspection 。一笔 Swap 的底层 CPI/转账不可被当作多笔独立经济交易；Token Account 不是独立钱包；owner 只表示链上授权关系，不表示真人或单一实体。
- 原始研究 [Early-Buyer Groups and Fast-Wallet Teams](https://arxiv.org/abs/2610.39458)（2026-10-29）：多渠道钱包群识别有结构描述价值，但不能直接推出跟随优势；其样本和规则不能直接当作本地 K2 证据。
- [RED-COHORT-2026](https://arxiv.org/abs/2607.02795)（2026-07-02）：重复同时买入容易由钱包活跃程度和市场本身吸引力解释，活跃匹配的负对照很重要。
- 用户参考项目 [`coordination_detection`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/tree/main/coordination_detection) 与 [`funder_network`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/tree/main/funder_network)：共享融资、时间同步、重复结伴可以描述结构；枢纽网络、抽样边界和人口选择偏差必须保留。写作内容仅为原创归纳及方法候选，不转录研究的受限分析。
- OKX [`okx-dex-market`](https://github.com/okx/onchainos-skills/tree/main/skills/okx-dex-market) 的只读候选发现不等于全链资金图自动重建。

## 五项可实际监控的跨币或跨群体候选

| ID | 观察事件与最小字段 | 不同于 P2.3 的地方 | 核心对照/可能误判 | 优先级 |
|---|---|---|---|---|
| C01 跨币资金再部署延迟 | Mint A 卖出产生 quote 资产→非共享地址资金转移→另一组钱包在 Mint B 买入；signature、asset、amount、time、transfer graph | 不仅发现单币退出，而是追踪退出至下一轮活动间隔及其变化 | 公共 HUB、交易所、混合资产；不能把资金来源推定为同一控制人 | A：研究，接 M03 |
| C02 同一地址群执行方式切换 | 固定钱包组在不同 Mint 的融资至首买延迟、单次投入、买入分批、退出方式；发行阶段与流动性 | 钱包相同不代表行为相同，寻找环境变化下的策略转换 | 币龄、池深、拥堵、公开活动及抢先交易竞争 | A：研究，接 M02/M01 |
| C03 不同群体执行模板相似 | 不同地址群重复“分发→买入→转仓→归集”的事件语法；交易顺序、CPI、工具程序 | 即使没有地址重叠也能发现重复模式，但只能作为模板匹配 | 相同机器人软件、交易服务、支付接口导致大量无关主体同模 | B：探索，不做同控分类 |
| C04 跨币钱包数—实际买入背离 | 固定 quote mint 的 buy wallet count、buy notional、单笔金额分布与群体库存；按 Mint/市场阶段分层 | 从单币变化到跨币行为尺度差异 | 价格计价不同、币龄、市值、池深不匹配；交易量≠净资金 | A：M01 可先输出基础字段 |
| C05 原有行为沉默与交易对象迁移 | 资金继续活动但原 Mint/策略阶段停止；后续另一 Mint/平台活动；funding、swap、venue、coverage | 监控原有序列的中断，而不仅是重复出现 | 数据断流、交易服务停机、市场整体冷却、时区效应 | A：P2.5 深化 |

## 发现重点：跨币比较必须保留市场背景

同一群体在新币曲线期、迁移期和已有 AMM 池时，正常的延迟/金额/路径会不同。应保留发行阶段、来源协议、池深、竞争状态和交易延迟后再比较；只比较“同样 10 个钱包”没有意义。跨币的相似时序仅表明候选模板，**不说明同一控制者或预知发行**。观察到的变化与预测后续变化属于两个研究问题。

## M01 原型目标与边界

命令（标准库，无依赖；只读模拟数据）：

```bash
PYTHONPATH=src python -m solana_meme_os.wallet_batch_monitor --input fixtures/wallet-batches-demo.json --output /tmp/m01-report.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

这份原型**不是 Solana RPC 原始交易解码器**。输入必须是上游已经核查后的经济行为事件。要接真实数据，必须另设计 raw transaction→outer/inner CPI→Swap 经济事件→Token Account owner 的解析适配器，补充原始签名、指令位置与覆盖完整性审计。任何 `mode=live` 输入在该原型中会被拒绝。

### 输入契约 m01.v1

```json
{
  "schema_version": "m01.v1", "mode": "fixture", "chain": "sol",
  "mint": "<base58 mint>", "quote_mint": "<quote asset mint>", "quote_decimals": 9,
  "source": {"tool": "synthetic_fixture", "ref": "fixture://..."},
  "coverage": {"start": "2026-10-31T00:00:00Z", "end": "2026-10-31T00:30:00Z", "complete": true, "gaps": []},
  "as_of": "2026-10-31T00:35:00Z", "events": []
}
```

每条事件：`event_id`、`signature`、`slot`、`event_time`、`available_at`、`source_ref`、`kind` (BUY/SELL/TRANSFER)、`tx_status` (SUCCESS/FAILED/UNRESOLVED)。成功的经济行为必须有经上游正确映射的 `wallet_owner`；`token_account` 可选，仅作为独立账户证据；BUY/SELL 必须有对应 `quote_mint` 与正整数 `quote_amount_raw`。`TRANSFER` 只表示**目标 Mint 的转账动作**，其 `wallet_owner` 是被上游认定的发起方，不代表所有收款者主动参与。当前不支持真实 Solana 账户所有权变更或多跳 SOL 资金图，不应把资金转账误标为 BUY。

`coverage` 的起止需为 15 分钟边界且 `as_of >= end`，在此范围内计算 1/5/15 分钟互不重叠窗口。`gaps` 指明缺失区间；`complete=false` 表示全部窗口数据不充分。未解析及晚于 `as_of` 才可得的事件使其所处窗口 `INCOMPLETE`，对应计数为 `null` 而非 0，并阻止相邻窗口差异报警。失败交易独立计数、不作为成功买入。完全相同 `event_id` 去重，冲突事件拒绝。

### 输出契约 m01.result.v1

- `timeframes.1m/5m/15m.windows`：每个窗口的独立 actor、买/卖 actor、买卖 quote raw 量、首次观测/历史重新出现、证据来源及完整性。
- `comparisons`：仅在前后两个完整相邻窗口比较 `retained_count`、`entered_count`、`inactive_count`、`entry_share`、`retention_share`、`jaccard`。`first_observed` 是**本次输入历史内首次观测**，绝非链上新建钱包；一个没有活动的窗口也不等于永久退出。
- `candidates`：`BUYERS_UP_QUOTE_VOLUME_DOWN`、`SAME_COUNT_FULL_MEMBER_REPLACEMENT`、`SUSTAINED_ACTIVITY_THEN_STOPPED`。均为**描述性研究候选**，无统计校准、不表示因果、庄家或利润。最后一类要求连续两个完整且各有至少三个活跃钱包的窗口，然后观察到完整的零活跃窗口以降低噪声；该要求不是统计显著性阈值。
- `source_refs`：只保留输入中的来源；所有地址、签名在 fixture 中都是虚构，不是链上事实。`quote_amount_raw` 必须根据 `quote_decimals` 才能显示为常规单位，不能混计不同 quote mint。

### 测试与故障说明

单元测试覆盖同一钱包多个代币账户、重复事件、事件冲突、来源和时间校验、失败交易、未知解析、迟到事件、完整零窗口、窗口缺口、身份替换、重复活跃/返回、报价资产一致、1/5/15 分钟窗口和 CLI 演示。功能测试不能证明真实 Solana 指令解析、上市阶段分类、跨币主体识别、网络覆盖或投资信号有效。

## 下一阶段与进度

- **P2.4：已形成 5 种跨币/跨群体候选**，已明确字段、实际新颖处和正常解释。推荐向 **P2.5 方法筛选与交接** 推进；无需为凑更多概念停留。
- **P3-M01：离线原型可以开发并在 fixture 上测试**。其正确性限于该输入契约；必须进行真实 raw transaction 适配器、Token Program/Token-2022/WSOL/ATA、CPI 去重以及覆盖与延迟审计，才可进一步尝试真实链上只读分析。现阶段不得部署 live monitor。
- **P4：尚未对真实历史 Mint 或真实钱包进行回放与误报验证**。下一轮先以极少量独立链上交易做 read-only 语义核验，避免急于全网覆盖。

**下一轮适合的任务**：在 P2.5 中为 C01、C02、C05 与 M01 打通能力依赖，审查哪些能在现有数据源和成本限制下获得早于目标事件的真实证据；并在 P3-M01 基础上开发一个可复核的 Solana 原始交易解析适配器及对抗性交易 fixture，仍不连接真实交易账户。

## P2.5 补充审计：M01 实际原始交易适配器缺口（2026-10-31）

**变更性质：AMEND 工程说明，未修改程序代码/生产规则。** 当前 `wallet_batch_monitor.py` 是 `fixture` 输入的下游窗口计算器，不具备“链上原始交易解码”能力。原有 `wallet_owner`、`kind` 和 `quote_amount_raw` 均由未实现的上游经济动作解析器提供；14项单测及 CI 仅证明合成契约的离线行为。

### 解析层最小输入与决策

| 原始取数对象 | M01 所需输出 | 未解决时如何处理 |
|---|---|---|
| `getTransaction(signature, encoding=json/jsonParsed, maxSupportedTransactionVersion=...)` 的 version、`meta.err`、blockTime/slot | 事件签名、时点、成功/失败状态 | `null`/缺元数据不能视为零交易；标记 UNKNOWN / 重试条件 |
| static account keys、地址查找表 loadedAddresses、outer + inner CPI、指令层级 | 唯一经济动作的 `event_id`、指令位置和证据 | 不能把一个Swap的多条CPI Token Transfer计为多个Swap；不识别程序则 `UNRESOLVED` |
| SPL Token Program / Token-2022 对应 Token Account的 mint、owner、delegate、PDA与指令时点 | 实际代币账户归属、执行授权者、fee payer分别记录 | `wallet_owner` 不能从fee payer或token account地址臆造；未定型主体不能计入独立人类钱包 |
| Pump.fun/其他曲线、Raydium/Meteora及路由的真实成交语义 | BUY/SELL经济动作，目标Mint和quote amount | 仅有转账或Token余额变化不足以宣称是买卖 |
| SOL、WSOL、SPL quote 的原始金额、decimal、费用和rent、Token-2022扩展 | 统一报价资产及单位，可靠的分窗口成交量 | 不同资产不可相加；transfer fee/hook/隐藏金额无法解释时标未知 |
| 窗口采集范围、索引页码/slot/tx完整性、source、`available_at` 和修订水位 | COMPLETE/INCOMPLETE、as-of快照与修订结果 | 一次 `getSignaturesForAddress` 或少量 `getTransaction` 的结果**不能证明某个Mint的全量零活动**；源断流时不可输出沉默告警 |

### 当前代码逐项观察和界限

1. 输入只接受 `mode=fixture`，对真实 `mode=live` 明确拒绝。**这是正确的安全隔离，不要为了接真实数据先删除此限制。** 应先在独立适配器中测试真实交易解码，并继续输出离线验证文件。
2. `wallet_owner` 是上游声称已经归一化的地址。代码按此去重，含 `TRANSFER` 的发起方参与活跃统计；不包含收款方自动主动参与。它既不是全市场持有人数，也不是实际控制者人数。
3. 当前 `source_refs` 对单窗口证据最多保留30项；这适合摘要但**不是完整审计事件索引**。真实链上研究必须可通过签名和指令索引追查未列出的全部经济事件。
4. 固定窗口为1/5/15分钟、3天输入上限与每Mint单报价资产；默认比较窗口间的BUY规模而**非外部净资本投入**。下一步不能把 C01 资金闭环或 C05 机会分母强行塞入现有指标。
5. 旧测试已涵盖重复事件、Token Account owner 冲突、缺失窗口、晚到数据、失败交易、假设成员替换。**新增适配器测试**仍需要：LUT v0/版本变动、多层CPI、多Swap同交易、fee payer≠token owner、ATA/PDA、WSOL wrap/unwrap、Token-2022 TransferFee/TransferHook、真实缺失 meta、不同资产金额、同槽事件顺序。
6. `available_at` 必须记录采集系统实际收到证据的时间，不能借用区块时间充当可得时间；同Slot内同时间事件要保留交易签名与可复核指令位置，不制造秒级因果顺序。

**优先实现次序**（仅设计交接）：先用少量已核查 Solana 原始签名和有标准答案的交易类型建设独立只读适配器及其 fixture；严格验证经济动作、归属与来源；再将已归一化事件送入 M01，随后推进 C02 和 C05。优先借鉴官方 `@solana/transaction-introspection` 解析账户索引/LUT/CPI，而非自行简化所有协议结构；其为 JS 工具包，现有 Python 原型尚未接入该包。官方说明：https://solana.com/docs/core/transactions/transaction-introspection 。
## P3-M01 真实指令语义适配器：本轮实际增量

**变更性质：AMEND 工程交接；代码位于 Draft PR #16，未改生产监控。** [独立适配器说明和 C02/C05 数据契约](p3-m01-raw-adapter-contract.md) 取代此前“适配器尚不存在”的旧工程状态。适配器已在合成 `getTransaction` 形状输入中解析直接 SPL Token/Token-2022 Token Transfer（并核对 source Token Account owner 与 fee payer/authority 不是同一概念）、System SOL 直接转账，以及 v0 编译格式的已加载地址；所有 DEX CPI Token/SOL 交易均不能直接视为独立 Swap 或用户充值。无协议级 BUY/SELL 解码、无真实 RPC 采集与覆盖核验。

**新增的结构性限制**：现有 M01 输出只提供窗口钱包数量，没有预冻结的成员地址列表，不能直接作为 C02 相同钱包群跨 Mint 的成员依据。C02 必须从历史冻结群体定义与原始经济事件流开始；C05 必须独立获取合格机会全集及采集完整性，不能用零事件推断行为沉默。

测试与模拟场景见 `tests/test_raw_tx_adapter.py`、`fixtures/raw-solana-transfers-demo.json` 和 `fixtures/c02-c05-contract-scenarios.json`。合成测试支持后续小样本**人工逐笔只读核查**，不代表链上真实例子已核验。
