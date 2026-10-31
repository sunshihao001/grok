# P3-M01｜离线 Solana getTransaction → 事件适配器、C02/C05 数据交接（2026-10-31）

**状态：fixture-only 实验代码；无 RPC 采集、钱包/交易、协议完整解码或真实市场验证。** 本文是现有 `docs/p24-m01-crossmint-research.md` 的局部工程补充，不是新知识本体。

## 1. 精确实现范围（支持 ≠ 协议交易识别完成）

`src/solana_meme_os/raw_tx_adapter.py` 直接接收本地 `m01.raw.v1` JSON 文件，其中 `transactions[].rpc` 是 `getTransaction` 风格响应。仅允许 `chain=sol`、`mode=fixture`。输出符合现有下游 `m01.v1`，并另外返回 `adapter_audit`。

- 可解析（前提：账户和证据完备）：**顶层** System Program `transfer` → 单独的 `funding_events`；**顶层** SPL Token / Token-2022 `transfer` 和 `transferChecked` → M01 目标 Mint 的 `TRANSFER`，保留 source TokenAccount 的 owner、authority、fee payer、destination owner（若可确认）、交易签名和指令路径。支持 `jsonParsed` 形式及部分 `json` 已编译指令，后者按 **静态账户＋`meta.loadedAddresses.writable/readonly`** 顺序恢复 v0 地址查找表，且只解析已核实的 System Transfer (tag 2) 和 Token Transfer (tag 3)/TransferChecked (tag 12) 的固定格式。
- CPI Token 转账**不会**推断为一个独立 Swap，也不自动计入 M01 Token Transfer；CPI System 转账**不会**计为用户充值；未知 Token-2022 扩展和无法识别的 DEX/路由经济动作保持 `UNRESOLVED`。普通 `syncNative`、账户初始化等不是成交；本实现没有可靠的 WSOL wrap/unwrap、池子结算与 Token-2022 fee/hook 经济解析能力。
- 交易失败只记录在审计 `unsupported`，不生成成功交易事件。没有区块时间、缺少账户/owner/CPI、签名不匹配、交易格式超出能力、证据在 `as_of` 之后才取得，均采取拒绝或未知状态；未知解析降低当前合成观察范围的完整性。
- 一个已确定的来源 Token Account owner **不是** Fee payer/Delegate/实际人类主体；当前不进行 PDA/多签控制人识别。M01 `active_wallet_count` 是事件中记录的 owner 地址数，不是独立人类人数。
- `available_at` 必须由**实际采集系统**记录；Fixture 中的该字段为模拟输入，不能等同真实系统已验证的时点。相同 Slot/秒不推断内部先后因果；用指令路径记录可核对位置。

### 不支持和明确不能声称的能力

- 未实现 Pump.fun/Raydium/Meteora/Jupiter 的真实 Swap 解码；**不会输出 BUY/SELL**。M01 的买卖窗口在只含本适配器数据时为 0，这只代表**已解码范围中没有买卖事件**，不代表真实市场无交易。
- 当前 `coverage.complete=true` 仅代表**提供 Fixture 的数据集声明已完整**，不是全链索引保证。即便解析记录无误，也不得把零交易窗口直接作为 C05 沉默证据。
- 未处理完全通用的 v1+ 交易、所有 Token-2022 扩展、不同 Router 的多指令/多Swap净额归因、跨币换手归集以及完整手续费结算。
- 因当前适配器用 `coverage.complete=false` 统一拒绝未知范围，遇到一笔未知交易会使该 15 分钟 fixture 的所有子窗口标为不完整；**这是保守但粗粒度的限制**，未来需要独立全量索引和按 Slot 精确标记缺失区间。

## 2. 最小输入与命令

```bash
PYTHONPATH=src python -m solana_meme_os.raw_tx_adapter \
  --input fixtures/raw-solana-transfers-demo.json \
  --output /tmp/m01-normalized.json
PYTHONPATH=src python -m solana_meme_os.wallet_batch_monitor \
  --input /tmp/m01-normalized.json \
  --output /tmp/m01-report.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

输入必须包含 `schema_version=m01.raw.v1`、`chain=sol`、`mode=fixture`、`mint`、`quote_mint`、`quote_decimals`、`coverage`、`as_of`、`source` 与 `transactions[]`。每个交易封套包括 `signature`、`source_ref`、`available_at` 和完整保存的 `rpc`。`rpc.transaction.signatures[0]` 要与封套签名匹配。

生成的 `m01.v1` 保留独立的 `adapter_audit.funding_events[]`、`adapter_audit.unresolved[]`、`adapter_audit.unsupported[]`。这些审计字段**不是**已核验的经济主体标签，也**不能**直接替代缺失的 DEX Swap 解码。

## 3. C02：同群体跨币执行切换，最小数据契约

C02 不应仅用 M01 聚合 JSON。M01 的公开输出只含窗口成员**计数**，不包含冻结的具体成员名单，无法据此计算同一组地址在两个 Mint 的表现。**必须引用预先冻结的群体定义，并读取标准化事件流。**

输入对象最少有：

| 对象 | 不可缺字段 | 关键断言 |
|---|---|---|
| `group_snapshot` | `group_id`, `frozen_at`, `members`, `source_refs`, `selection_method` | 冻结时间早于被比较的未来机会；地址不是同控证明 |
| `mint_opportunity` | `mint`, `eligible_at`, `stage`, `venue`, `liquidity_bucket`, `source_ref` | 比较相似发行阶段/流动性，不得事后选赢家 |
| `funding` | `recipient`, `asset`, `amount_raw`, `event_time`, `available_at`, `signature` | SOL 到账本身不包含将买哪个 Mint 的信息 |
| `economic_actions` | `owner`, `mint`, `kind=BUY/SELL`, `quote_mint`, `quote_amount_raw`, `event_time`, `available_at`, `source_ref` | 必须来自经独立核验的协议级解析器；本适配器暂未实现 |
| `observation` | `as_of`, `deadline`, `coverage_status`, `source_refs` | 截止时尚未执行记为 `RIGHT_CENSORED`，不能填0或无限 |

建议的输出：每 Mint 实际参与钱包/预冻结人数、融资后首买延迟（已执行者的观察样本）、未执行/右删失人数、单笔报价资产规模分布、阶段/流动性匹配结果、不可比较原因。不输出“庄家同控概率”或净收益。

**对抗性测试设计**：同组在不同 Mint 速度变化；同组不同发行阶段导致不可比较；一半群体截至观察时仍未交易；群体定义晚于对照机会；报价资产不同；部分交易证据晚于 `as_of`。见 `fixtures/c02-c05-contract-scenarios.json`。

## 4. C05：机会校正的沉默与迁移，最小数据契约

C05 的分母必须来自独立的**合格机会索引**，不能由“钱包曾经交易过哪些 Mint”事后构造，否则未参与机会会被系统性漏掉。

| 字段 | 含义 |
|---|---|
| `eligibility_spec` | 在观察前冻结的协议、币龄、流动性、发行阶段等条件 |
| `opportunities[]` | 所有匹配条件的 Mint/venue 机会，包括未参与者 |
| `group_snapshot` | 同 C02，冻结的历史钱包集合 |
| `coverage_status` | `COMPLETE` / `UNKNOWN`，由索引覆盖证明提供，不能取自单个交易回包 |
| `participated[]` | 在已到达并可观察的机会中，该群体有无经核验的合格交易 |
| `alternative_activity[]` | 同期其他 Mint/venue 的确证活动；只是并列证据，不等于迁移因果 |

严格判定：

1. `coverage_status=UNKNOWN` → `COVERAGE_UNKNOWN`（即使当前零交易）。
2. 覆盖完整、符合条件机会为零 → `NO_OPPORTUNITY`（不是沉默）。
3. 完整、存在机会、无合格参与 → `ELIGIBLE_BUT_INACTIVE`（仅是描述性候选）。
4. 同时观察到另一 venue 活动 → 追加 `ALTERNATIVE_ACTIVITY_OBSERVED`，不自动得出地址/资金迁移。
5. 任何机会在 `as_of` 时尚不可得，不能计入当前分母。

建议负例：整个市场无符合条件的发行；RPC/索引断流；群体仍在其他Mint正常交易；机会列表按未来结果过滤；地址变更导致历史群体不再具有覆盖力。

**实现顺序**：先实现 M01 原始事件适配器的正确性和可审计性，再实现协议级单笔 Swap 解码，再逐步建立机会索引；不同时开发三个完整监控程序。

## 5. 来源和下一轮验收

- Solana 官方 [RPC JSON Structures](https://solana.com/docs/rpc/json-structures) 和 [getTransaction](https://solana.com/docs/rpc/http/gettransaction)（`json`/`jsonParsed`、`loadedAddresses`、余额 owner、meta 和 CPI）。
- Solana 官方 [Transaction Introspection](https://solana.com/docs/core/transactions/transaction-introspection)；成熟 JS 解析器优先用于后续复杂协议，不建议扩展本 Python 玩具解码器至所有 DEX。
- Solana 官方 [Tokens](https://solana.com/docs/tokens) 和 [Transfer Tokens](https://solana.com/docs/tokens/basics/transfer-tokens)；Token-2022 地址核查参考 [官方 Payments](https://solana.com/docs/payments/how-payments-work)。
- SPL Token 指令字段及编号以 [官方 `solana-program/token` 源码](https://github.com/solana-program/token/blob/main/interface/src/instruction.rs) 为依据。

**阶段结论**：本适配器在合成事务中可证明**部分转账级语义**，但没有完成任何 DEX BUY/SELL 语义验证；下一阶段适合选少量公开交易签名进行逐条人工对账，仍只读。进入正式 P4 的条件不是原型测试数量，而是已对账的真实原始交易和可审计数据覆盖。