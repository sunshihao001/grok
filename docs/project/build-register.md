## 2026-11-24｜R-55：真实 Token-2022 fee 主网证据已定位，但 Blix 尚未完成归档回放

**本轮最高价值缺口**：继续追 R-54 后没有再增加 Token-2022 规则，而是寻找真实主网 `transferCheckedWithFee` 交易来跨过 `OFFLINE_TESTED → ARCHIVED_REAL_REPLAY` 的证据门槛。

**实际外部证据**：
- 当前公开 Solscan 账户索引页面已经显示真实主网账户存在 `transferCheckedWithFee` 活动，并给出具体 transaction signature；例如 KuCoin Cold Wallet 页面列出 `2dRcDZxEtwYtrSumZB1dF7M5RyF2EnhdGCz2Fc53oRFXZvFjR2YLKHCLET287NsRT3NJAVFxczV8BShanMZin` 的 `transferCheckedWithFee` 活动。[Solscan account](https://solscan.io/account/6BhBoBB47wSGjK5uzcGWNcTf2oNRPQNuv6GVdkNyj9PB)
- Solana 官方 Token-2022 文档确认 `TransferCheckedWithFee` 携带 transfer amount 与 fee；fee 在目的 Token Account withheld，而不是简单等同于完整交易成本。[官方 Transfer Fees](https://solana.com/docs/tokens/extensions/transfer-fees)
- Envio 的实证索引文章进一步指出 `transferCheckedWithFee` 既可作为 top-level instruction，也大量出现在 inner instructions；这支持继续把 outer/inner 两层都作为 Blix 的证据入口，而不是只看顶层。[Envio Solana transfer indexing](https://docs.envio.dev/blog/index-solana-stablecoin-transfers)

**当前 Blix 源码状态**：
- `server/economic-events.mjs` 已存在 `transferCheckedWithFee` 的识别、`transferFeeRaw` / `transferNetAmountRaw` 派生和 `TOKEN_2022_TRANSFER_FEE_PRESENT_PROVENANCE_UNPROVEN` 降级。
- `test/wallet-evidence-chain.test.mjs` 已存在 gross=400M、fee=5M、net=395M 的离线反例。
- 这部分源码已经存在于当前开发分支，但 **build-register 在 R-53 后没有单独登记 R-54**；本轮补齐台账，避免代码与项目状态再次脱节。

**本轮没有声称的部分**：
- Solscan 页面只证明真实主网存在该 instruction/signature，当前工具没有取得该 signature 的完整 raw/jsonParsed RPC response，因此**尚不能称 `ARCHIVED_REAL_REPLAY`**。
- 尚未验证该真实交易的 Token Account/Owner、withheld amount、pre/postTokenBalances 与 Blix decoder 一致。
- 尚未验证 Token-2022 + CPI + ALT + DEX/multi-pool 联合样本。
- GitHub CI 对当前最新代码 HEAD 尚未取得新的运行结果；历史绿色 CI 不覆盖未验证的新 HEAD。

**下一阻断/可证伪条件**：用许可的只读 RPC/归档来源取得上述真实 signature 的完整 `jsonParsed` transaction；对照 instruction `amount`、`feeAmount`、source/destination Token Account、owner、pre/postTokenBalances 与 withheld 字段。如果现有 decoder 能完整重建，则 R-54 可以升级为 `ARCHIVED_REAL_REPLAY`；如果缺字段或语义无法重建，直接标 `UNKNOWN / insufficient RPC representation`，不继续用金额差值推断。
## 2026-11-22｜R-53：同一卖出交易的同Mint净余额变化不能直接作为库存来源证据

**本轮最高价值缺口**：继续追 R-52 的底层解析后，发现当前 `recipientOutcomes()` 在判断“接收钱包后续卖出是否与这次 Transfer 数量相容”时，使用 `ownerTokenBalanceDeltaRaw()` 的**净** Token balance delta。这个值在简单卖出中有用，但在一笔复杂交易同时发生同 Mint 入账与出账时会被抵消，从而产生一个危险的假阳性：例如钱包在同一交易中先收到 100M、又转出 500M，Owner 的净变化是 -400M；如果前一笔外部 Transfer 也是 400M，旧逻辑会把它标成 `AMOUNT_COMPATIBLE_BUT_PROVENANCE_UNPROVEN`，但真实 gross outbound 是 500M，净值不能代表出售数量或库存来源。

**原始协议/成品反证**：
- Solana 官方 transaction introspection 明确把一笔交易的 outer/inner instruction 顺序作为独立结构，并说明 versioned transaction/CPI 需要从 instruction tree 与 balance metadata 一起解析；不能把一个 owner/mint 的最终净余额变化当作完整执行语义。[官方 Transaction Introspection](https://solana.com/docs/core/transactions/transaction-introspection)
- Solana 官方交易历史验证示例使用 token account 的 pre/post balance 判断方向/金额，但这只能在该账户变化足以代表单一支付事件时成立；复杂交易仍需结合交易结构。[官方 Verification Tools](https://solana.com/docs/payments/accept-payments/verification-tools)
- GitHub 的实际 DEX parser 已把“同时 buy/sell”的复杂交易视为解析边界；其 issue #28 记录了同一 transaction 同时买卖时，简单 unique-token 假设会失败。[solana-dex-parser issue #28](https://github.com/cxcx-ai/solana-dex-parser/issues/28)
- 当前 Blix 的经济证据表已经保存同一 transaction 的 outer/inner Token Transfer instruction，因此不需要建立新采集器；可以在现有证据上识别“同Mint同一交易同时 inbound/outbound”的歧义。

**原位修正**：
1. `recipientOutcomes()` 在计算 sell 的 `inventoryLink` 前，检查该 sell transaction 中同 Mint、同 Owner 的 TOKEN_TRANSFER 是否同时存在 inbound 与 outbound。
2. 若同时存在，则不再使用净 balance delta 给出“数量相容”结论，改为 `INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS`。
3. 原有“卖出数量超过单次 Transfer”反例、same-slot UNKNOWN、observedSellsTruncated 等继续保留。
4. 没有新表、新采集器、新状态机、新 Agent；只是在现有 `econ_instructions` 事实之上降低错误的库存来源解释。

**可复现反例**：
- 外部：A → B = 400M M。
- 后续复杂交易：B 同一 transaction 收到 100M M，同时从自己的 Token Account 转出 500M M。
- Owner 净变化 = -400M。
- 旧逻辑：可能误标 `AMOUNT_COMPATIBLE_BUT_PROVENANCE_UNPROVEN`。
- 新逻辑：`INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS`。
- 这只否定错误的“净变化=卖出数量/库存来源”解释，不声称已经解析出真实 swap/gross sale amount。

**证据等级**：
- `CODE_OBSERVED`: 新歧义检测已提交。
- `OFFLINE_TESTED`: 现有 wallet-evidence-chain 测试加入 mixed same-Mint inbound/outbound counterexample；当前新HEAD GitHub CI 尚未取得。
- `ARCHIVED_REAL_REPLAY`: 未取得。
- `CONNECTED_READONLY_RUNTIME`: 未取得。
- `SECURE_OPERATIONAL`: 未取得。
- `MODEL_INTERPRETATION`: 不适用。
- `UNKNOWN`: 真实主网复杂 swap/transfer 同交易样本、Token-2022 fee、WSOL wrapping、multi-pool 路径仍未验证。

**错误/反例边界**：
- “净余额下降 400M”不等于“gross sell 400M”。
- “同交易存在 outbound Token Transfer”也不等于“这就是 DEX sell”；当前代码只把证据降级为 ambiguous，不重新发明 swap parser。
- 只有明确的 protocol-level swap/transfer 解析，才可能继续讨论 gross executed amount；当前 Blix 不应从净 balance delta 推断。

**下一阻断/可证伪条件**：取得一个许可的真实复杂 versioned Mint transaction，至少包含同 Mint inbound + outbound 或 swap + transfer，比较 `pre/postTokenBalances`、outer/inner Token instructions、实际 DEX event；如果真实样本证明当前歧义检测仍会漏掉 gross-flow masking，再决定是否需要在现有 decoder 中增加更细的 transaction-level flow summary，否则保持 UNKNOWN。 

## 2026-11-21｜R-52：否证并修正 R-51 的 Versioned/ALT jsonParsed 假设

**本轮最高价值缺口**：不是继续扩展 ALT 规则，而是主动否证上一轮 R-51。对照 Solana 官方 RPC JSON 结构后发现：R-51 的离线 fixture 把 `meta.loadedAddresses` 与 `message.accountKeys` 同时作为 `jsonParsed` 输入，但官方定义中 **jsonParsed 的 `message.accountKeys[]` 已包含 lookup-table accounts，并以 `source:"lookupTable"` 标记；`meta.loadedAddresses` 在 jsonParsed 模式被省略**。因此上一轮“static keys + loadedAddresses”的 fixture 不是实际 jsonParsed 形态，不能继续作为真实 RPC 形态依据。这是本轮必须修正的错误，不保留错误知识。

**原始协议依据**：
- Solana 官方 RPC JSON Structures：parsed transaction 的 `message.accountKeys[]` 包含 static 与 lookup-table accounts；lookup-table account 的 `source` 为 `lookupTable`。同一文档明确 `meta.loadedAddresses` 在 `json/full` 中存在，而在 `jsonParsed` 中 omitted。[官方 JSON Structures](https://solana.com/docs/rpc/json-structures)
- 当前 `server/solana.js` 的真实请求仍使用 `getTransaction(..., { maxSupportedTransactionVersion: 1, encoding: "jsonParsed", commitment: "confirmed" })`，所以 R-51 的 ALT fixture 必须首先符合 jsonParsed 形态，而不是把 raw/full 形态混入其中。[当前代码](https://github.com/sunshihao001/grok/blob/integration/blix-evidence-readonly-20261108/server/solana.js)

**原位修正**：
1. `server/economic-events.mjs` 的 `fullAccountKeys(tx)` 现在先判断 `message.accountKeys` 是否包含 `source:"lookupTable"` 的 parsed account；若存在，直接使用该完整 accountKeys，不再追加 `meta.loadedAddresses`，避免 accountIndex 被重复/错位。
2. 若输入是 raw/full JSON 形态（static `accountKeys` + `meta.loadedAddresses.writable/readonly`），仍支持按 static → loaded writable → loaded readonly 组合；但这种路径不冒充 jsonParsed。
3. 现有 `test/wallet-evidence-chain.test.mjs` 的 ALT fixture 已改成真实 jsonParsed 形态：lookup-table Token Account 位于 `message.accountKeys`，`source:"lookupTable"`，`pre/postTokenBalances.accountIndex` 直接解析到 B/POOL Owner。没有新表、新采集器或新状态机。

**关键错误/反例**：
- 错误：把 `jsonParsed` 理解为“static accountKeys + meta.loadedAddresses”。官方文档否证。
- 错误：如果继续追加两份地址，`accountIndex` 会发生位移，可能把 Token Account/Owner 解析到错误地址。
- 边界：parsed accountKeys 的存在只解决地址索引；仍不能证明 Owner 是实际控制人、Transfer 是 Sale、或 Sell 使用的是刚接收库存。
- raw/full JSON 与 jsonParsed 是不同 response representation；以后真实归档必须先记录 encoding/mode，再选择解析路径。

**证据等级**：
- `CODE_OBSERVED`: 修正后的 resolver 已提交。
- `OFFLINE_TESTED`: 现有 ALT regression fixture 已修正为官方 jsonParsed 形态；新HEAD CI需要单独核查。
- `ARCHIVED_REAL_REPLAY`: 未取得。
- `CONNECTED_READONLY_RUNTIME`: 未取得。
- `SECURE_OPERATIONAL`: 未取得。
- `MODEL_INTERPRETATION`: 不适用。
- `UNKNOWN`: 尚未取得一个真实主网 versioned transaction 的完整归档来验证当前 resolver 对复杂 CPI/Token-2022/ALT 联合样本的覆盖。

**下一阻断/可证伪条件**：取得许可的真实 versioned Mint transaction，确认实际 `encoding=jsonParsed` 返回的 `message.accountKeys`、`source:lookupTable`、Token Account/Owner、CPI 与 pre/post balance 是否能被现有 resolver 一致重建；若真实样本需要 raw/full 才能补足字段，则把两种 representation 的证据等级分开，不让 AI 混用。

# Blix 滚动建设台账｜继承、修复、研究与验收

> 2026-11-08 初版。**这不是新的产品架构或专家体系**，仅作为当前 `blix` 主体的一个持续更新的工程事实清单；以后说“按照建设来”时，先更新状态和证据，再按信息价值/业务价值选下一项工作。旧知识和历史参考原位保留，不机械挪入本表。
>
> 主体：`sunshihao001/grok` 的完整原版 `blix` 产品。**2026-11-09 当前唯一集成候选为 [Draft PR #23](https://github.com/sunshihao001/grok/pull/23)，现已直接以 `blix` 为base，包含历史PR #18/#22能力而非待合并的平行产品；仍未合并/部署**。本表下方旧日期的PR #18状态为历史记录，必须以最新状态节和GitHub CI为准。


## 2026-11-20｜R-51：经济证据表自初始化契约与 Versioned/ALT 地址索引反例

**本轮最高价值缺口**：复核 R-50 后没有继续扩展 block-order。直接重新检查 `server/economic-events.mjs` 的“新库可从零工作”与 Solana versioned transaction 解码，发现两个会让 O3/O4 证据出现**静默错误或直接不可写**的基础问题：

1. `persistEvidence()` 已经写入 `econ_transactions.status`，但该表的首次 `CREATE TABLE` 定义没有 `status`，且原 migration 列表也没有补这个列。对真正从空 SQLite 开始的 evidence journal，这是 schema/写入契约不一致；不能用历史绿色CI替代当前HEAD的 fresh-DB 证明。
2. `decodeEvidence()` 和 `ownerTokenBalanceDeltaRaw()` 原先只用 `message.accountKeys` 解析 `accountIndex`。Solana versioned transaction 的 lookup-table 地址需要与静态 key 合并；否则 Token Account 的 `preTokenBalances/postTokenBalances.accountIndex` 可能无法映射到 Token Account，进而把 Owner/库存变化降级为缺失或错误。

**原始协议依据与成品反证**：
- Solana 官方 RPC JSON 结构说明：parsed transaction 的 `message.accountKeys`包含账户元数据；versioned transaction 可以使用 address table lookups；`meta.loadedAddresses` 是另一组加载地址，且不同响应模式对该字段有差异，因此实际归档必须保留可用于账户解析的完整结构/适当响应模式。[Solana RPC JSON Structures](https://solana.com/docs/rpc/json-structures)。
- 官方结构同时说明 `accountIndex` / `programIdIndex` 依赖交易账户索引，因此不能只看静态 `message.accountKeys`。
- GitHub 成品实现中可看到同样的组合规则：`solana-defi` 在解析 ALT 时显式维护 `loadedAddresses` 并把账户索引映射到完整账户列表；`Solana Explorer` 也保留 `meta.loadedAddresses`；`BEpusdt` 与 `solana-dex-cli` 均将 loaded writable/readonly 地址追加到账户列表。[solana-defi](https://github.com/Shyft-to/solana-defi/blob/c1bef8ac15075ca3a2909c48c841d44a5adc0684/Bots/Typescript/grpc-copytrade/utils/transaction-formatter.ts)、[BEpusdt](https://github.com/v03413/BEpusdt/blob/8a91be6a155c28cc07db18aa0ed0ecd06aae71582/app/task/solana.go)、[Solana Explorer](https://github.com/solana-foundation/explorer/blob/b1231e17daaeaa011a520360944c4c469a1533f9/app/entities/transaction-data/lib/adapt-parsed-transaction.ts)。

**原位修正**：
1. `econ_transactions`首次建表加入 `status TEXT NOT NULL DEFAULT 'RPC_OBSERVED'`，并增加兼容旧库的 `ALTER TABLE` migration；这与现有 `persistEvidence()` / `recipientCandidates()` / `recipientOutcomes()` 的事实状态字段一致。
2. 新增 `fullAccountKeys(tx)`，按 **static transaction keys → loaded writable → loaded readonly** 组合；`decodeEvidence()` 与 `ownerTokenBalanceDeltaRaw()`统一使用它。没有新表、新采集器、新权限。
3. 现有 `test/wallet-evidence-chain.test.mjs`增加 fresh-schema 断言和一个 versioned/ALT fixture：Token Account 只出现在 loaded writable 中，`pre/postTokenBalances.accountIndex`必须仍能解析出 B/POOL Owner；若以后移除组合逻辑，该测试会直接失败。

**关键错误/反例**：
- “历史CI曾绿”不能证明当前分支新建空DB时schema一定一致；这轮将其变成可复现 schema assertion。
- `message.accountKeys` 只有静态 key 时，ALT Token Account 的 balance index可能没有对应地址；不能把 `owner=null` 当成“没有Owner”。
- ALT address resolution 成功也只证明账户索引映射正确；仍不能证明 Token Account Owner=控制人、Transfer=Sale、或库存来源。
- 不同 RPC encoding/mode 对 versioned transaction 的 loaded-address字段存在差异；真实归档必须确认当前请求模式是否保留足够字段，否则应标 `UNKNOWN`，不能靠AI补齐。

**证据等级**：
- `CODE_OBSERVED`: schema migration 与 full-account-key resolver 已提交。
- `OFFLINE_TESTED`: fresh schema + ALT fixture 已提交到现有经济证据测试；当前HEAD的GitHub CI需要重新检查。
- `ARCHIVED_REAL_REPLAY`: 未取得。
- `CONNECTED_READONLY_RUNTIME`: 未取得。
- `SECURE_OPERATIONAL`: 未取得。
- `MODEL_INTERPRETATION`: 不适用。
- `UNKNOWN`: 真实主网 versioned transaction 的归档覆盖、RPC encoding/mode组合、复杂 CPI/Token-2022 与 ALT 的联合样本仍未验证。

**下一阻断/可证伪条件**：取得一个许可的真实 versioned Mint transaction（最好包含 ALT + Token transfer/CPI），用现有原始归档完整重放；对照 `message.accountKeys`、loaded addresses、Token Account/Owner、instruction index 与实际 balance delta。若当前RPC/归档模式不能同时提供足够字段，就明确把该交易降为 `UNKNOWN`，而不是继续扩展推断层。

## 2026-11-19｜R-50：同slot交易只有在已有 getBlock 顺序证据存在时才升级为后续事件

**本轮最高价值缺口**：R-48 将同slot transfer→sell 保持 UNKNOWN 是正确的，但 Solana 官方 getBlock(slot) 返回该 slot 的完整 transaction 数组；如果当前已有 econ_transactions 中的两笔交易都能在同一个完整 block 归档里定位，就不必永久丢弃同slot顺序证据。问题应解决为“可选补证”，而不是新建第二采集状态机。

**协议与成品反证**：
- Solana 官方 getTransaction 只返回单笔交易的 slot、blockTime、transaction/meta；没有同slot block transaction index。getBlock 返回指定 slot 的 transactions[]，因此只有 block-level archive 才能提供同slot位置证据。[getTransaction](https://solana.com/docs/rpc/http/gettransaction)、[getBlock](https://solana.com/docs/rpc/http/getblock)、[RPC JSON Structures](https://solana.com/docs/rpc/json-structures)。
- Solana 官方代码文档的 transaction introspection 继续把交易内部 instruction order 与 block/transaction context 区分，不能用处理到达顺序替代账本事实。[transaction introspection](https://github.com/solana-foundation/solana-com/blob/main/apps/docs/content/docs/en/core/transactions/transaction-introspection.mdx)。
- GitHub 成品/索引项目也把 slot、transaction、instruction 分开保存，而不是从单笔交易的时间戳推断全局顺序；例如 Indexer_TX 明确保存 transaction slot/blockTime 并在链上数据上做分类，完整历史索引项目则以 block/transaction/instruction 为不同层级数据。[Indexer_TX](https://github.com/kotarowatanabe107/Indexer_TX)、[GetBlock indexed archive](https://github.com/GetBlock-io/getblock-docs/blob/main/solana-advanced-data-tools/solana-indexed-archive.md)。

**原位代码改进**：
1. server/economic-events.mjs 给现有 econ_transactions 增加可空 block_tx_index，不新增采集器/状态机。
2. 新增 recordBlockTransactionOrder(db, block, slot)：只接受已有 block 归档对象，按 transactions[] 中签名位置写入对应已捕获 transaction；重复 signature、缺 slot 等输入拒绝；如果重新捕获同 signature 发现 slot 变化，会清空旧 block index，避免错误复用。
3. recipientOutcomes() 继续以 sell.slot > transfer.slot 为默认规则；只有 transfer/sell 同slot且两边都有 block_tx_index、且 sell index 更大时，才把 sell 纳入 follow-up。没有 block index 仍是 UNKNOWN。
4. test/wallet-evidence-chain.test.mjs 新增离线反例：同slot sell 初始不进入；注入一个 getBlock 形状的 block fixture，transfer index=0、sell index=1 后，该 sell 才进入。已有“数量超过5条”“数量大于单次transfer”等反例继续保留。

**证据等级**：
- CODE_OBSERVED: block_tx_index 与 recordBlockTransactionOrder() 已提交。
- OFFLINE_TESTED: block-order fixture 已加入现有经济证据测试；GitHub CI需按最新HEAD单独确认。
- ARCHIVED_REAL_REPLAY: 未取得。
- CONNECTED_READONLY_RUNTIME: 未取得。
- SECURE_OPERATIONAL: 未取得。
- MODEL_INTERPRETATION: 不适用。
- UNKNOWN: 真实主网 block archive 的可获得性、RPC ledger retention、同slot复杂 CPI/多池交易的完整覆盖仍未知。

**错误/反例边界**：
- getBlock 返回 block transactions ≠ 自动证明交易是“经济上的先后因果”；它只解决 ledger transaction order。
- block index ≠ inventory provenance；接收前已有库存、同Mint多次转入、部分卖出仍需库存账本证据。
- 同slot没有完整 block 归档 → 继续 UNKNOWN。
- 只拿 signature list 而没有 block-level order → 不能升级同slot顺序。

**下一阻断/可证伪条件**：取得一个许可的真实 Mint 归档，至少包含一个同slot transfer/sell 对及对应完整 block transactions[]，验证该补证是否与现有 econ_transactions 一致；若真实样本发现 block archive 常缺失或交易详情被裁剪，则保持 UNKNOWN，并评估是否只对已有完整归档开放该证据等级。

## 2026-11-17｜R-48：经济证据后续事件不能用 blockTime 排序（同slot反例修正）

**本轮最高价值缺口**：R-47已经把“接收后卖出数量相容≠该批库存来源”做成反例，但继续审查 `server/economic-events.mjs` 发现另一个会直接污染 O3/O4 的时序问题：`wallet_trades.t`来自 `blockTime * 1000`，而 Solana 的 blockTime 只有秒级；仅按时间窗口会把**同一秒甚至同一slot内、实际顺序未知的卖出**误当成 transfer 之后的卖出。对 Meme 快速交易尤其危险。

**原始源码依据与跨项目反证**：
- 当前 `server/economic-events.mjs` 的旧 `recipientOutcomes()` 以 `t>=transferAt` 查询后续 sell；旧 `crossMintCandidates()` 也以 `a.t<=funding_time<=b.t` 建立跨Mint时序候选。
- Solana RPC 的交易响应以 `slot` 标识所在区块；`blockTime` 是区块时间戳，并不是同slot内交易顺序。Solana 官方交易结构/JSON-RPC文档确认 transaction 由 slot/transaction message/指令构成，versioned transaction 还存在 lookup-table accounts；因此不能把秒级 `blockTime` 当作严格事件顺序。[官方 getTransaction](https://solana.com/docs/rpc/http/gettransaction)、[RPC JSON Structures](https://solana.com/docs/rpc/json-structures)。
- 独立成品 `anchoys1337/solana-wallet-behavior-analysis`明确把 ledger ordering 作为归因基础，并使用 **slot → block time** 的顺序而不是处理到达顺序；同时把 transfer-out 与 sell 分开，避免把库存移动当价值实现。[GitHub](https://github.com/anchoys1337/solana-wallet-behavior-analysis)。

**实际代码修正**：
1. `recipientOutcomes()`现在只把已捕获、已验证的 sell transaction 纳入后续集合，并要求 `sell.slot > transfer.slot`；同slot卖出保持 UNKNOWN，不因为相同 `blockTime` 被升级为“后续卖出”。同一 signature 也排除。
2. `crossMintCandidates()`现在要求 `sell.slot < funding.slot < buy.slot`，只有三段均有已捕获经济交易记录时才形成时间顺序候选；同slot路径不再被解释成资金先后。
3. 没有新增采集器、数据库状态机或权限；只是收紧已有只读证据查询。原始 RPC仍完整保留。

**可复现反例**：
- 在现有 `test/wallet-evidence-chain.test.mjs` 新增：transfer 与 B sell 使用相同 `slot/blockTime`；旧实现会进入 follow-up sell，新实现必须排除。
- 原有数量反例仍保留：400M transfer 后800M sell → `CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER`。
- 该测试仍是 synthetic/offline，不代表真实主网验收。

**证据等级**：
- `CODE_OBSERVED`: 新查询已提交。
- `OFFLINE_TESTED`: 同slot反例已进入现有经济证据测试，但本轮尚未得到对应新HEAD的GitHub CI运行结果。
- `ARCHIVED_REAL_REPLAY`: 未取得。
- `CONNECTED_READONLY_RUNTIME`: 未取得。
- `SECURE_OPERATIONAL`: 未取得。
- `MODEL_INTERPRETATION`: 不适用于此修正。
- `UNKNOWN`: 同slot交易的真实全链归档覆盖、block内精确交易索引是否需要更高层 `getBlock`/ledger replay，当前仍未知；本修正选择“不确定就不升级”。

**下一阻断/可证伪条件**：下一步不是继续扩大知识图，而是取得一个许可的真实Mint归档，验证同slot/跨slot的 transfer→sell 与 sell→fund→buy 顺序；若发现当前 `wallet_trades` 缺少足以严格排序的交易索引，则继续保持 UNKNOWN，并考虑只在已有 `getBlock` transaction index 或可证明顺序数据下提升证据等级。

## 2026-11-14｜R-47：将现有知识按O1–O6转成真实可见的证据缺口与AI取证问题（不新建目标层）

**起点与纠偏**：用户要求“以积累知识进行真实转换，按子部锚点推进整体及别的锚点”。R-46已在原`DOMAIN-MODEL.v1.json`明确G0–G4目标层、O1–O6业务成果、四入口/条件交接与S1–S7方法。**本轮不是再画一次图**：直接审查`investigation-continuation.mjs`发现报告六阶段虽有状态，但不能具体说明哪条专业知识对应缺失哪种事实；更严重的是任意Coin指定Mint/`/inspect`也返回“用户提交或选择Pulse观察”，混淆本地档案与市场事实。初稿尝试使用G1–G5名称，核对现有原图后立即统一改为原业务O1–O6，避免重复目标体系。

**实际代码交付**：

1. `server/intelligence/investigation-continuation.mjs`在已有`stages`/钱包/跨Mint/纸面证据之外新增`anchors`。其中`researchPriority`与`tradeReadiness`严格分开；前者只说明是否有可供审阅的**局部证据**而不对Token打研究价值分数；后者在缺信号首可得/进出场报价时必为不可评价。保留`evidenceLineage`的本地历史范围和Pulse浏览器来源差别、`knowledgeContext`的“已提供≠实际使用/增益”及六项`nextEvidence`：O1时间与覆盖；O2钱包Owner和公共设施；O3签名/指令/库存；O4真实SOL/WSOL资金路径；O5交易可参与性与退出报价；O6新事件/迟到回补及知识对照。它们是**只读建议**，没有新增RPC、市场数据源、交易权限或强制流程。
2. `server/intelligence/research-http.mjs`仅为`/discover`传入由原`validatePulseDiscoveryInput`校验的`marketObservation`。手动`/research`和`/inspect`保持`NO_PULSE_MARKET_OBSERVATION_IN_THIS_RECEIPT`，即使本地有转账，也不假装具备行情/实时来源/可复制利润。
3. `server/intelligence/pulse-discovery.mjs`把被选中Mint的**有限来源证明**传给后续AI任务；`ai-workflow.mjs`根据已经执行的局部只读工具事实算出六项证据缺口后交给模型`interpret`；`chat-completion-model.mjs`只传短`{anchor,status,missing}`，遵守24KB模型上下文预算、工具/成本/权限与事实界限。模型可综合推理，不新增固定Agent或篡改原Blix来源。
4. `web/src/pages/Intelligence.tsx`在现有调查收据展示研究值/交易准备度的独立状态、Pulse来源是否存在、六个可展开子目标和知识实际提供记录。修改测试`test/investigation-continuation.test.mjs`、`test/pulse-ai-discovery.test.mjs`、`test/intelligence-workbench-http.test.mjs`及原UI契约，涵盖正确/错误Mint、归档签名、空档案、跨Mint候选、伪来源、模型收到了缺口提示以及不会升级为真实交易信号。D08/D09、D12原领域正文和产品说明已原位增加与运行代码的连接。

**独立验收与已知失败**：`8f85212cd`旧一轮锚点UI/HTTP代码的[Node24完整测试43592248525](https://github.com/sunshihao001/grok/actions/runs/43592248525)通过；模型适用补充过程曾在`a61e00ed`触发一条测试代码错误：解析模型上下文时把真实换行误写为字面`\\n`，当时602项通过、1项失败；已在`9470fc39`修复，该提交[完整测试43592623759](https://github.com/sunshihao001/grok/actions/runs/43592623759)成功。承接Pulse来源后的`449a5289`已有[完整测试43592650490](https://github.com/sunshihao001/grok/actions/runs/43592650490)、[前端构建43592650437](https://github.com/sunshihao001/grok/actions/runs/43592650437)、[审计43592650492](https://github.com/sunshihao001/grok/actions/runs/43592650492)成功；**此后其他文档提交产生的新HEAD也需按SHA单独核查**。独立Uptime仍失败，不能写“全部工作流绿色”。这证明**实际代码+伪模型/合成SQLite+CI**，不是已在真实Meme市场上找到可赚钱币，也不是用户原机完整UI与授权主网数据源实跑。

**整体锚点影响**：本轮减少“图上O1–O6闭合”与“运行时实际不知道下一步查什么”的断层，但尚未把任何真实Mint引入当前会话的可授权本地SQLite。下一轮最值得做**冻结同一真实Mint及其source timestamp/原始签名/Owner、一次新证据反证造成O2→O3→O5判断实际修订**；若合法档案不足，保持UNKNOWN和原版源责任，不在AI层重造数据来源。G0经济价值的成功仍取决于同批机会候选、真实可参与报价与样本外对照，不因O子目标/知识被显示就宣布达成。

## 2026-11-14｜R-46：Meme多路线知识图谱和三重闭环（ai-d方法→Blix原位映射）

**需求**：R-42/R-45已完成知识归位与业务主线纠偏，本轮要解决“知识与业务都在，但如何按语义连接多入口、不同领域、数据/代码/测试、失败反馈并闭合”的跨层缺口。首先回读独立[ai-d K1–K9](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/knowledge-lifecycle-nine-stages.md)、[ai-d S1–S7/五视图/双向追溯](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md)，以及本仓既有10轴11关系、D01–D12、O1–O6与PR#23代码。没有新建平行知识系统、数据源、Bot或交易层。

**具体改变（PR#23现有集成分支）**：

1. 原位更新`knowledge/DOMAIN-MODEL.v1.json`的现有`cross_axis_alignment`：追加`businessRouteGraph`，其中**14个已有认知概念的承接说明（映射到原S类/轴/归属）、6个既有业务结果O1–O6、4个自然入口（MARKET_FIRST/MINT_FIRST/WALLET_FIRST/CROSS_MINT_FIRST）、16条**条件性业务交接边（含O2→O5机会评价接力）、**5个反馈回路**、K1–K9与原维护位置的对应，以及清晰的UNKNOWN/授权/同控/实测边界。既有10轴11关系、12领域和历史152单位未改；此图不是实际链上关联图。
2. `scripts/audit-knowledge-trace.mjs`在旧`--axes/--unit/--target/--all`不变的前提下新增**`--routes`**：检查O1–O6唯一性、领域和现有源码引用存在、S类/十轴引用、四入口路径及可选支路、所有条件交接、反馈回路首尾闭合、K1–K9与文件引用、未验和权限边界。校验失败时退出2；不会联网、运行AI或交易。已给`test/knowledge-lineage-trace.test.mjs`追加两条静态回归。
3. 原位扩写`docs/project/cross-layer-anchor-map-20261113.md`的**V0.5多路线与知识闭环**说明：14类概念分工，业务关系Mermaid图，四入口具体职责，知识/业务/工程三重闭环，失败逆向追责、一份Mint的概念越级反例与实际验收门槛；`knowledge/INTEGRATION-CROSSWALK.md`和`knowledge/README.md`补导航。原业务、来源、领域主述未被复制。

**真实检查的分级状态**：初次新增测试时，在先于V0.5文档的提交`14e5291`上，CI `43591010132`发生一项**测试文字与尚未写入的文档顺序不一致**（找不到「多路线」），其他测试通过；随后实际补上V0.5关系文档的提交`de896ae58`，其[Node24完整回归`43591180982`](https://github.com/sunshihao001/grok/actions/runs/43591180982)已显示SUCCESS（涵盖`--routes`路径检查），同一SHA的[前端构建`43591184448`](https://github.com/sunshihao001/grok/actions/runs/43591184448)及[audit`43591184451`](https://github.com/sunshihao001/grok/actions/runs/43591184451)SUCCESS。**后续两次知识导航提交的最终HEAD完整CI应重新复核**；本轮全部成果是静态图关系/文件与CI，未经真实Mint、实跑模型、真实交易机会、长期Case监控或部署。独立Uptime失败依然存在，不与代码测试合并为成功信号。

**风险锚点与下一次行动**：目前闭环只证明原位结构可自洽，不证明事实/AI/交易业务已经闭合。应停止增加更多概念图：先取得许可合法、原始签名/CPI/Owner/可见时点完整的真实Mint归档，沿任一入口跑`Coin→Intelligence→/inspect`并真实触发跨O2/O3/O5的反馈，记录哪个事实改变了哪个判断；无合法源则明确UNAVAILABLE，接着按源责任修复而不在AI侧补采。若后续实测发现多路图对业务帮助不大，应删减其静态负担而非扩成自动Agent。

## 2026-11-14｜R-45：工作重心转换为 Meme 机会发现与按需专业调查

**用户纠偏**：先前围绕知识生命周期、概念、层级、证据关系研究过多，容易将“建知识体系”误当 Blix AI扩展的主要交付目标。现确定**完整Blix市场终端+机会优先筛选+AI按需专业调查**为工作重心；异常Mint研究继续保留，但其价值和可参与交易机会价值分别评估。D01–D12/L0–L7/K1–K9属于知识/方法支援，**不是每个Mint必经筛选层或必须开发的模块数**。

**本轮真实核对的代码证据**（SOURCE_READ，不等于已在真实市场验证）：`server/engine.js` 原市场Discover/Safety/Signal流程；`triage.js`早期规则及可选快速模型分类；`early.js`早期样本、30/60/120/300秒观察；`research.js`原AI研究/钱包买入指标；`brain.js`历史结果与成本代理；`wallets.js` 的 `walletSignals`已支持钱包买入→adopt Mint→vet→raise，不能说“钱包→Mint”尚不存在；`paper.js`具有纸面报价机制。`server/intelligence/pulse-discovery.mjs` 仅能从用户浏览器提交的最多12个候选中选择**调查对象**，未独立证明实时全市场覆盖和可交易优势；`ai-workflow.mjs`仅有当前已批准的 Mint facts 和经济证据工具；`opportunity-read-comparison.mjs`是同来源/同时间候选对照，不是盈利评测。`research-http.mjs`的`/inspect`可不使用模型读取已授权本地经济证据，不能凭没有归档自动补采真实交易。

**本轮交付**：原位更新 [goal-map](goal-map.md#2026-11-14工作重心纠偏知识是支援meme市场机会是业务主线)、[现有总蓝图](blix-ai-workbench-master-plan-v1-20261113.md#2026-11-14工作重心纠偏从通用知识系统转为-meme-机会发现与专业调查) 的业务分工、钱包/市场双入口、两个独立价值判断、D01–D12→Meme实际问题与程序现状对照；[专业知识入口](../../knowledge/README.md)及[知识实际用法](knowledge-use.md)仅更正主从关系，不删除原研究、无新知识层、无新数据源/API/市场评分器、无交易与付款操作。新认知的结构内容属于**项目目标/源码对应检查**，尚未改变实时市场机会发现能力。

**下一项真正验收**：一段时间冻结的同批原Blix市场候选与Wallet→Mint候选（含被排除者）→统一来源/首次可见/成本/池报价→原版筛选与AI按需专业调查对照→只读可跟随性与失败样本复盘。没有源级首可得、钱包历史/原始RPC或有效报价时应明确UNKNOWN；优先补真实许可的证据和连接，而非再扩D/L/K概念、关键词、知识目录。当前PR#23是Draft，合并/CI状态以GitHub最新HEAD单独核查。

## 2026-11-14｜R-44：不用付费模型也能从Coin进入真实SQLite只读经济证据检查

**本轮切入点**：用户要求继续把已整理的专业知识发展成可运行的Blix AI扩展。检查最新PR#23后发现R-43已独立完成“指定Coin Mint不回退Pulse、缺Mint索引在模型调用前拒绝”等P0-B工作，因此本轮**不重复R-43**，改为解决**当前有真实本地归档但没配置收费模型就完全无法使用经济调查页面**的成品障碍。完成一个真正允许用户先读事实、再按需启动AI的增量功能，而非另一套采集/推理引擎。

### 已交付的运行能力

1. **`server/intelligence/research-http.mjs`**：新增`POST /inspect`，JSON仅允许`{mint}`；同原研究服务的loopback、Host、Origin、body长度、Mint合法性、单任务互斥与SQLite来源/指定Mint预检。无索引返回HTTP422`MINT_LOCAL_EVIDENCE_UNAVAILABLE`、无现成Schema返回503；明确“本地无记录不等于链上无交易”。新接口**无需`model`/API key/AI费开关**，只调用现有白名单`runCapability('mint-economic-evidence')`，读取原`makeOfflineEconomicReader`（现有`inspect-economic-mint.mjs`只读CLI），用现有`summarizeInvestigationContinuation`给六业务环节/UNKNOWN状态；不请求外部行情、RPC、不启动原版服务器、不签名交易。返回`modelMode:'NOT_USED'`、`verifiedMarketOpportunity:false`、`liveExecutionValidated:false`。
2. **`/health`将两个能力就绪分开**：原`ready`仍要求显式配置模型+现有归档；新增`inspectionReady`只要求现有已授权归档可读，`remainingInspections`默认24次/进程，**不消耗原`maxTasks`模型任务配额**。不因零费用就允许无限查询；保留原HTTP安全规则和收费模型严格opt-in。
3. **`web/src/pages/Intelligence.tsx`**：在原Blix AI工作台加入**“免费查看指定 Mint 的本地经济证据（不使用AI）”**按钮；始终绑定R-43的`researchMint`而非“当前列表其他币”；显示本地交易与地址、局部卖出摘要、六环状态及未知；无模型时仍能使用；真实模型调用保留原独立按钮与显式费用前提。无证据的Mint不能临时创造市场价格或补采交易。
4. **真实HTTP/SQLite进程验收**：`test/intelligence-workbench-http.test.mjs`加入无模型的Origin拒绝、额外字段拒绝、错Mint预检、独立配额、免费检查不消耗模型额度；新`test/intelligence-inspect-sqlite-http.test.mjs`两项测试，一是实文件`persistEvidence`→只读经济CLI→HTTP `/inspect`检查签名/地址/卖出摘要，二是**实际启动生产用`scripts/start-intelligence-workbench.mjs`进程**且仅设本地SQLite、不设模型，验证`/inspect`返回、`/research`为503、无交易/模型请求、SQLite SHA前后一致。另在`intelligence-ui-candidates.test.mjs`加免费路径页面回归，并将新SQLite验收列入`npm test`、`test:evidence`、`test:intelligence`。
5. **文档原位维护**：用户操作前提/权限/真实资料局限见`ai-readonly-local-workbench.md`；产品路线见`intelligence-layer.md`。没有新增专业知识领域/数据源/真实交易模块。

### 可复查验收与准确证据边界

- 包含真实进程启动和临时SQLite链路的 [综合Node24测试 #43570966620](https://github.com/sunshihao001/grok/actions/runs/43570966620) **SUCCESS**，对应 [前端构建 #43570966614](https://github.com/sunshihao001/grok/actions/runs/43570966614) **SUCCESS**、[audit #43570966671](https://github.com/sunshihao001/grok/actions/runs/43570966671) **SUCCESS**（这些指向当时经过验证的提交；最新HEAD应另行复查）。
- 测试环境**是真实本地HTTP+真实Node子进程+真实SQLite文件**，里面的交易数据是**SYNTHETIC**且在测试文件中明确标记；不是用户浏览器真正交互、真实Solana历史RPC、真实成功/失败成交或AI模型效果实证。此前封网Docker原版Blix启动验收与这个sidecar独立运行验收不能合并成已接入主网整套产品。
- `/inspect`不需要收费模型，而不是宣称所有市场数据都“免费”：用户仍需**已经存在、许可可用**且满足Schema的SQLite归档。没有归档就只能报告不可用；没有当时可用报价与首次可见时间，不能评级为可交易盈利机会。公网/远程认证仍未完成、PR#23仍Draft未部署、原版`npm start`安全门禁继续存在，外部Uptime独立失败。

### 下一项最有价值的工程缺口

**P0-C / P1-A 真实资料贯通**：查找已授权且带原始Solana `getTransaction` 签名/CPI的实际Mint归档，不把仅DEX Screener/RugCheck供应商市场快照说成链上经济交易；用已有`audit-intelligence-source-readiness.mjs`按`mint/source/first_seen/observed_at/slot`比较原Blix与经济存档的语义/覆盖，再走一次真浏览器`Coin→Intelligence→4547→报告`。只有在有真实原文和可核验时点后，才能检验接收卖出、钱包群体和交易价值。**不要再做第三次同类合成测试替代真实市场进度**。如需要联网供应商、收费模型或目标云电脑，必须核实许可、配额和运行隔离；禁止未经授权交易/签名。

## 2026-11-14｜R-43：Coin指定Mint不串币、AI入口可用与未归档收费前阻断

**承接 R-42 的P0-B**：原版Coin → Intelligence导航虽已可传Mint及问题，但原 `Intelligence.tsx` 逻辑在指定Mint不在Pulse可见候选时 `selected=candidates.find(...)??candidates[0]`，导致目标消失甚至回退到另一枚币；`SIDECAR_URL`对`127.0.0.1`使用了错误转义的RegExp；本机sidecar实际启动配置`BLIX_AI_ALLOWED_ORIGINS`默认未包含原版4421（此前仅修了HTTP模块默认值）。另外，旧sidecar只做SQLite结构预检，无法在调用可能收费的模型之前辨识当前Mint没有归档记录。

**本轮实改并且保留原版Blix所有业务代码**：

1. 原位扩充`web/src/pages/intelligence/candidates.ts`的`resolveResearchTarget`：**用户明确指定Mint的优先级高于Pulse候选**；同一Mint若在Pulse列表有原观察则显示观察来源，无则`USER_MINT_LOCAL_ARCHIVE_ONLY`，不虚构代币行情、不回退成另外的币。未指定Mint时保持原Pulse选择逻辑，不改变其榜单顺序。
2. `Intelligence.tsx`通过hash/路由和明确任务状态分别管理选中Mint、已知市场数据和已有AI回执；`runLocalResearch`与`copyTask`绑定实际`researchMint`，市场未观察时仍能对指定Mint发起**用户手动**的已授权只读调查请求、展示无行情状态。用户切换市场过滤/列表时清理显式指定状态及旧回执；`127.0.0.1`浏览器hostname正则由错误双反斜线修为正确单反斜线，避免无故禁用本机4547。
3. `scripts/start-intelligence-workbench.mjs`也将`http://127.0.0.1:4421`和`http://localhost:4421`补进**实际启动脚本的默认Origin**，保留`research-http.mjs`的loopback、Host、Origin和额度门禁。不是允许远程公网、签名、交易或模型自动启动。
4. `offline-economic-reader.mjs`新增`probeExistingEconomicMint`，在**指定的现有**SQLite只读打开、`query_only`、索引查`econ_instructions`/`wallet_trades`目标Mint是否留存；`research-http.mjs`在`/research`模型/任务额度前调用（仅实际服务被显式配置时）。未索引返回HTTP 422 `MINT_LOCAL_EVIDENCE_UNAVAILABLE`及受限状态字符串，前端显示本地未收录，不谎称全链无交易；数据库缺失、结构错、非法Mint仍拒绝，不创建数据库。该门禁只适用于**已有本地证据**，不是全链完备判定。
5. 回归：`test/intelligence-ui-candidates.test.mjs`真实调用`resolveResearchTarget`确保不串币，检查手动按钮与localhost正则；`test/intelligence-source-readiness.test.mjs`临时真实SQLite以文件哈希确认Mint级预检无写入；`test/intelligence-workbench-http.test.mjs`真实HTTP+注入伪模型确认缺Mint返回422，模型调用0、任务额度不减；存在Mint才在正确地址执行授权的模型模拟和SQLite报告。**没有用真钱、网络供应商、真实收费模型、交易或签名**。

**验收级别**：现有Node回归、HTTP注入伪模型及前端构建是**CODE/OFFLINE_MOCK_HTTP**证据；原版Blix独立封网冷启动是此前R-41证明。二者均不等于用户当前浏览器真实交互、已授权市场联网、生产云电脑或完整链上资金/库存实测。本轮没有触发既有`npm start`安全门禁覆盖，也未将整个Blix宣称为只读模式。PR#23继续Draft未合并；按每次最新HEAD检查GitHub Actions并保留独立Uptime失败。

**下一项工程入口**：P0-C/P1-A：确认一份已获授权、含同一Mint实际`econ_transactions`和`econ_instructions`/钱包历史的现有SQLite快照，与原Blix源消息的时间/池/Token账户对齐。再走一次`Coin→Intelligence→本地4547→只读归档→报告`真实浏览器E2E；无真实归档时，正确的成果是精确报不可用，不是模拟链上业务成功。真实供应商/模型费用及目标运行机器仍需明确授权与条件。


## 2026-11-14｜R-43：AI研究结果Mint身份校验与候选防替换

**执行起点已变化**：重新核查PR#23最新源码时，上一轮R-42记录的Coin指定Mint未在Pulse短名单时错误回退问题，已由并行进展修复：`web/src/pages/intelligence/candidates.ts`的`resolveResearchTarget`优先保留显式Mint，`Intelligence.tsx`已有手动`/inspect`、`/research`和“未归档不调用模型”的只读路径，服务端`mintReadiness`在模型费用/预算前拒绝缺失Mint。因此本轮**没有重复开发该功能**，转向检查下一处真实证据链漏洞。

**新发现**：`Intelligence.tsx`的模型`/research`结果原本只检查`evidence/knowledgeUse/calls`是数组，随后`setResearchResult({...data,mint})`把请求Mint直接写入结果。若服务端返回或未来适配器错误地携带其它Mint的工具输入/事实，页面会把不相干证据展示在当前Mint下；`/discover`也未在前端复核返回选择属于**实际提交的12币短名单**。服务端有自身的Mint校验，但界面是独立边界，不应以信任假设代替验收。

**本轮实际代码**：

1. `web/src/pages/intelligence/candidates.ts`新增`validateMintResearchReceipt`：检查模型研究的Mint（若声明）、所有工具调用输入、每条证据输入和实际返回结果都属于**用户指定Mint**；不允许把`verifiedMarketOpportunity:true`或`liveExecutionValidated:true`显示成已验结果；无证据的研究计划仍可作为无验证草稿。
2. 同文件新增`validatePulseSelectionReceipt`：候选数量必须匹配浏览器提交数量，模型选出的Mint必须属于**这次实际提交的短名单**，无选中时不得附带其它Mint调查；如有调查结果，复用逐笔Mint校验。
3. `web/src/pages/Intelligence.tsx`将两个校验放在`setResearchResult`、`setDiscoveryResult`前；拒绝跨Mint错误归属，不增加外部API、付费模型、交易或后台采集。
4. `test/intelligence-ui-candidates.test.mjs`新增伪造另一Mint工具输入/返回、错选非短名单Mint、错误候选数量、错误收益标志、合法无证据/拒绝候选等回归；在最终HEAD上的CI状态必须独立核实。

**验收性质**：本轮只加固前端**结果归属一致性**，不能证明本地经济档案完整、真实机会或主网数据来源正确。下一项最有价值的真实进展仍是选择一个可核验的真实SQLite Mint，完成Coin→/inspect→/research→本地经济签名→模型知识使用的同Mint回放和负例，而不是再扩知识索引。PR仍Draft，原Blix启动安全门禁继续有效。

## 2026-11-14｜R-42：十二领域专业知识原位归拢 + 扩展成品合同 + 本机AI来源修复

**本轮用户目标**：把分散在L0–L7/D01–D12、旧Grok/Hermes/qb-/meme-、65参考、GMGN/OKX/Synapse/ai-d中的专业知识整理清楚并归回正确位置，然后判断完整原版Blix上的AI扩展怎样走到可运行成品。**不是**新建概念层级、专家制度、第二套数据源或以整理文件数判定业务完成。

### 1. 已进行的实际知识修订（直接修改原文件，而不只是新增目录）

- [knowledge/README.md](../../knowledge/README.md)现在列出**12/12现有专业领域的唯一主述责任**：专业问题、知识深度、目标/业务、完整来源、当前代码/证据等级。G0–G4、L0–L7、D01–D12、K1–K9、O1–O6与D0–D9按不同用途保持独立，没有增加第13领域或额外运行Agent。
- 八份既有**主述正文**都补入“2026-11-14｜全域归位”：`foundations/solana-chain-and-market.md`（D01/D02/D10）；`mechanisms/market-price-mechanism-research.md`（D03）；`mechanisms/wallet-roles-and-inventory.md`（D04/D06）；`mechanisms/capital-organization-and-incentives.md`（D05）；`methods/anomaly-and-cohort-discovery.md`（D07）；`mechanisms/strategy-and-execution-economics.md`（D08/D09）；`cases/independent-validation-and-failure-cases.md`（D11）；`ai/intent-knowledge-selection-and-reasoning.md`（D12）。每份不是只登记名称，而是阐述需要区分的经济对象/错误推断、市场行为与反证、源级责任、原版模块、已测试边界与待验缺口。
- [外部参考入口](../../knowledge/references/README.md)、[跨知识结构表](../../knowledge/INTEGRATION-CROSSWALK.md)、[实际任务调用](knowledge-use.md)、[能力地图](capability-map.md)、[交付判断](delivery.md)及[项目入口](README.md)指向现有主述，不另建平行“知识真源”。**原始来源与独有反例保留**：Synapse笔记14/14信号、3+3 DEX、4+5 HL、5原则/4噪音及跨市场研究仍以`USER_PARAPHRASE`标记；GMGN Wallet Radar/First70/PnL/Copyability/参数在原项目对照完整保留；152旧知识ID/65历史参考/未读仓树继续跟踪`NOT_REVIEWED`和`mapped_unverified`。
- 新增的`test/p1-p2-knowledge-integrity.test.mjs`静态回归核对12个领域都指向现存的八份专业正文、历史原始资料未丢失、完整来源与成品验收引用仍在；**静态完整引用不等于逐条专业命题的独立实证**。

### 2. 扩展成品发展（不重复原版Blix）

[单一扩展层](intelligence-layer.md)现已加入明确的**三条真实用户路径**（Pulse发现/交易价值、Coin单Mint、Wallet跨币监控）、`research_priority`与`trade_readiness`两个不同结果，以及P0-A/P0-B/P0-C、P1-A/P1-B/P1-C、P2-A/P2-B的**输入依赖、组件责任、最低验收、失败/停止条件**。明确三种交付层次：可演示本地V0.1、真实只读Mint V0.2、前瞻机会评价/Case持续监控V1候选。原版采集/报价/钱包/交易代码保留，AI仅用按需只读工具解释已有事实。

**检查源码时发现具体P0-B阻断**：`webapp.js`的原版React端口4421，而`research-http.mjs`默认允许来源仅4420和5173；本机4421用户运行AI研究会被Origin拒绝。已在`research-http.mjs`默认allowlist**最小增加 `http://127.0.0.1:4421`与`http://localhost:4421`**，保持loopback/Host/Origin严格门禁、无交易或费用变更；`test/intelligence-workbench-http.test.mjs`新增真实HTTP+伪模型验证两种4421来源允许、外部网站403、返回只读标志，不调用收费模型。变更提交`1946a6e7` / `a5d4bdab`。**尚需按最终HEAD复核GitHub CI，不把源码修改当验收。**

**另一个已确认但未解决的P0-B断点**：Coin深链接能够传Mint/goal，但`Intelligence.tsx`的`selected=candidates.find(...)??candidates[0]`意味着指定Mint**不在Pulse当前观察名单**时可能回退到另一枚币。下一轮应把“用户显式指定Mint只查已授权本地归档”与“Pulse观察候选”分开建页面状态/合同，绝不合成一个伪造的市场币；测试必须确保指定Mint不被替换、无归档直报`UNAVAILABLE`、研究不会凭GET触发原版未知副作用。

### 3. 交付状态与最短后续任务

- **已核实过**：原版Blix封网容器冷启动/再次启动/HTTP/SQLite完整性；知识与部分经济/模型工具离线CI；现有PR#23草稿分支可逆更新。上述运行成果与真实联网市场完全不同。
- **本轮尚未做**：逐条全文深读65个参考及全部152历史映射；Synapse官网阈值实证；GMGN付费API；Coin任意Mint的完整交互修复；真实提供方first-available/完整RPC资金链；真实模型费用调用；云电脑部署；自动交易/盈利实证。
- **下一项高价值建设**：P0-B Coin显式Mint不依赖Pulse候选的只读UI/HTTP/SQLite接通→P0-C 使用有授权、现成真实归档校对Blix原源覆盖与首可得时间→P1-A 单Mint实际买→转→接收卖出/资金跨Mint可复查报告。若现有数据库缺真实经济表，先找原版采集/授权数据源负责的位置，不能让AI另建一个“补采事实层”。

**风险锚点**：如新的知识文档无法改变知识选取/专业判读/实际源码验收，则停止增加分类；如新的代码只让界面看起来可以研究而Mint身份或来源不一致，必须拒绝报告，而不是假装成品。当前`npm start`仍默认fail-close，隔离容器成功不准用作生产解锁凭据。

## 2026-11-14｜R-41：原版Blix真正隔离冷启动、重启与首个数据库初始化缺陷修复

**业务起点**：上一轮已经完成Coin→Intelligence导航，但不是原版Blix可运行验收。本轮从既有PR#23的实际 `npm start` 和 `server/server.js` 出发，**先测试安全门禁，再在外网彻底隔离的容器中运行原版完整服务**。不改变原版交易/账户功能语义，不运行真实钱包、RPC、收费AI或生产部署。

**首先修正上一轮引入的测试错误**：`test/intelligence-ui-candidates.test.mjs` 中深链接回归测试错误转义正则使完整Node测试在`52f270a`失败（前端构建和独立审计当时成功，不能冒充全CI成功）；`110b0469`改为直接验证实际文字及手动触发按钮，恢复绿灯。

**启动安全与实际验收路径**：
1. `test/read-only-audit.test.mjs` 现在在独立临时`RADAR_DATA`下真实执行`npm run --silent start`，清除原版危险运行确认环境变量，并断言在任何原版`server.js`模块导入/SQLite创建前以退出码2被拦截。`package.json`已将此测试加进默认完整`npm test`。这证明**缺授权时默认启动失败关闭**，不是服务安全认证。
2. 新增`scripts/verify-blix-airgap-boot.sh`及`.github/workflows/blix-airgap-boot.yml`。GitHub Actions先构建原Blix React，随后在`node:24-bookworm-slim`临时容器内运行**原版`server/server.js`**；参数 `--network none`、`--read-only`、`--cap-drop ALL`、`no-new-privileges`、资源上限、无Secrets、只读源码挂载和唯一临时`/data`数据库目录。容器只向内部loopback开放4420/4421，不映射公网端口。**这是离线诊断，不是允许用户关闭生产门禁**。
3. 首次真正冷启动暴露原版缺陷：`server/people.js`在Fomo模块完成建表前 eager `db.prepare('SELECT ... FROM fomo_traders')`，全新SQLite产生`ERR_SQLITE_ERROR: no such table: fomo_traders`，服务器立即退出。修复提交`0982817db62a63d4ca945800b7e2baff1d3d2c43`：保留各Fomo模块表的既有所有权，将次级头像来源SQL改为**首次查询时才编译**，某个可选表仍未初始化时独立跳过该来源、继续读取其它来源；不在AI层造库。新`test/people-cold-start.test.mjs`在真实独立Node子进程、全新SQLite中验证缺表不崩溃、其它来源随后建表后可读取，纳入完整测试。
4. 进一步将离线启动测试升级为**在同一个临时SQLite上冷启动→停止→第二次启动**，两次均真实HTTP检查`/api/health`、`/api/pulse`、React`/ `（4421）；关闭后执行SQLite`PRAGMA integrity_check`。 [双轮复启GitHub Actions #43550153919](https://github.com/sunshihao001/grok/actions/runs/43550153919) **SUCCESS**，原始日志包含 `BLIX_AIRGAP_BOOT_CYCLE_OK cycle=1`、`cycle=2`和`BLIX_AIRGAP_RESTART_SQLITE_INTEGRITY_OK`；此前首次成功在线CI [#43549973968](https://github.com/sunshihao001/grok/actions/runs/43549973968)。这不是实时行情源联网验证。

**证据边界与下一阻塞**：原版服务现已在完全封网容器里真实启动、可HTTP访问并重启，**不是**经过授权的联网只读运行模式；网络关闭也意味着无法检验PumpPortal/DEX/Helius/GMGN真实性、模型API、资产交易或实际机会收益。独立只读AI sidecar依旧需有真实`econ_transactions`归档与受许可模型配置；测试通过不代表Coin页面已经把AI结果直接嵌入原版面板。PR#23仍Draft/open、未部署，外部Uptime的失败与隔离启动不同。

**下一个真实任务**：先在用户确定的机器上核实Grok云电脑的Node24、磁盘持久化、端口/网络出口和只读权限边界；让原版市场数据源以可核费用/额度运行并保留首次观察时点与断流证据，随后用相同Mint联调原Blix→SQLite经济归档→本地AI服务→结果。禁止把沙箱运行直接当生产联网安全批准，也不另造第二套数据采集器。

## 2026-11-14｜R-40：PR23与blix无损研究合并 + 本地AI服务数据就绪门禁

**任务与交付目标**：承接R39“距离实际运行差什么”的P0阻塞，先消除累计 PR#23 与最新 `blix` 的 Git 合并冲突；然后修复现有**独立只读AI服务**把“已构造SQLite读取函数”误报为“已有可用本地SQLite”的真实启动就绪缺陷。保留原版Blix市场、账户、真实交易与Paper全部源码和本地风险拦截，不默默解锁原版完整运行或开启付费模型。

**已经实做的集成冲突修复**：
- 核对 GitHub `blix`、PR#23 与共同祖先 `3bc1f7d4` 的三方差异：当前 `blix` 相比PR#23主要多20个项目/知识文档改动，无原版运行核心差异。不能把其中8份双方新写的材料直接一边覆盖另一边。
- 使用三方逐行合并保留双方新增标题/段落，另以**按键、按来源项联合**的JSON合并 `knowledge/references/source-coverage-v0.1.json`，保留blix原11个外部参考、8轮旧研究、PR23新P1/P2调查记录以及来源覆盖字段；新增Synapse全分类及GMGN总览保留，未重写业务源码。
- 由现有PR#23提交 `9305637c` 与最新`blix` `1560528a` 创建双亲 `70932df9d5f11bb46731c9e00efcf7704bf7f547` 作为**同一PR23集成分支的普通快进更新**，没有合并草稿PR到正式`blix`。经GitHub最新核实：PR#23 `mergeable:true`、base SHA `1560528a`、Draft、open、未合并，比较 `behind:0`。该SHA [完整CI](https://github.com/sunshihao001/grok/actions/runs/43547571970)、[前端构建](https://github.com/sunshihao001/grok/actions/runs/43547572029)、[独立审计](https://github.com/sunshihao001/grok/actions/runs/43547571984) 均已PASS；外部Uptime仍失败，未混入成功项目。

**本地AI服务的真实运行阻塞与代码修复**：
- **错误入口**：`research-http.mjs` 旧 `ready()=typeof model==='function'&&typeof readEconomic==='function'`，即使 `BLIX_AI_DB_PATH` 指向不存在的文件或缺表的SQLite，仍可能显示健康就绪；点击研究后才在工具处失败，可能产生之前可避免的收费模型调用与任务预算消耗。
- **修正确切责任层**：`offline-economic-reader.mjs::probeExistingEconomicArchive` 在Node内建SQLite中以 `readOnly:true`、`PRAGMA query_only=ON` 核对**已有**文件与 `econ_transactions`/`econ_instructions`/`wallet_trades` 必要字段。永不创建数据库/启动原Blix/RPC。生产启动脚本 `scripts/start-intelligence-workbench.mjs` 将其接到 `createResearchHttpServer` 的可选 `sourceReadiness`。真实本机 `/health` 在无文件/缺schema时返回 `ready:false` 与不含机密路径的状态；`/research`和`/discover`在模型与任务预算之前拒绝，保持原有非预检调用方的兼容返回契约。
- **严格能力边界**：`ready:true` 只能证明模型函数已配置且**经济归档Schema可读**，不证明该Mint有数据、历史完整、模型API可达或交易盈利；任何缺源依然要保留UNKNOWN。原版 `npm start` 带真实交易/钱包与自动AI副作用，由 `scripts/read-only-audit.mjs --gate` 禁止不经风险认可启动；本轮**没有**改变原版运行安全策略、没有启动原版服务、没有授权支付，也不宣称已取得原版“全功能只读安全模式”。

**验收**：
- `test/ai-economic-workflow.test.mjs` 新增SQLite不存在/表缺失/已有归档三组实际文件/表结构检查，并比对前后SHA，严格无文件创建或修改。
- `test/intelligence-workbench-http.test.mjs` 新增受控伪模型测试：缺归档预检→HTTP503/健康非就绪、模型零调用、预算不消耗，模拟归档恢复后状态变就绪；另以子进程真启 `scripts/start-intelligence-workbench.mjs`，确认默认不开模型/交易原版HTTP路由，健康非就绪、研究拒绝。
- 中间提交 `fea1a174` / `85906615` 的CI出现旧测试中 `RESEARCH_NOT_CONFIGURED` 响应结构变化，**已通过** `648cba584b8ad0425948a22177aea61878bec1cf` 保留原调用方错误响应合同，同时在正式预检调用时返回具体`archiveStatus`；不掩盖中间回归。
- **本登记提交后最新 CI必须重新查最终 HEAD**，不能把已通过合并CI或代码修改的旧SHA当作真实运行验收。现有所有研究HTTP测试、GitHub CI均属**隔离本机模拟/文件测试**，仍未部署、联网调用真实AI、启动原版市场服务器或完成用户环境端到端。

**剩余阻塞与下一轮最短动作**：R0 当前P0“原版Blix安全市场服务启动”尚未完成，需要明确目标机器/真实配置、在无签名/无收费行为的隔离环境对源码与自动后台路由实测；Coin→真正Agent调用仍只在Intelligence页面接通，Coin Copilot仍为复制任务；若没有真实RPC事件归档，预检即使通过也不能算真实Mint调查。下一轮先用受控启动/健康/原版UI全流程实测与一份真实已授权SQLite，而不是再扩GMGN知识分类。

## 2026-11-14｜R-39：到期前取回真实DEX/RugCheck原档，发现第二枚同批Mint并校验机会假象

**为什么从R-38调整研究入口**：R-38已有对同一浏览器Pulse候选的合成AI A/B和严密的时点/Hash检查，再重复合成“B选中好币”只会空转。此前文档认为真实样本只有一个BNB，不足构成双币比较；**2026-11-14实际取回GitHub Actions原始ZIP后发现第一批同时包含第二枚SIS真实Mint**。这恢复了一个此前未利用的实证市场对照，但**并没有恢复原版Blix的真正两币候选队列、模型回执或市场优势**。

**数据恢复**：
- 从PR#16历史Actions [run 41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009)取回artifact `13067198705`，ZIP SHA256 `afeb32206d063a2f1e2ab68dbc35f736a1caa3fe093f8ecb13691171ced05053`（GitHub报2026-12-01到期），含BNB、SIS的DEX原始JSON；复核原始JSON SHA分别 `240dca2d3df8cfbf9e0f09d806d61b2ae6040abc07bcebc4b9dd3e07f3d09897`、`5cdeb33076e1df0a2efc24c1c3daf6b4cce4c3832ac131ddaf4f5ab105dbf7b4`。
- 从[run 41268982018](https://github.com/sunshihao001/grok/actions/runs/41268982018)和[run 41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)取回artifact `13068437092`、`13068576712`，含BNB两次DEX和RugCheck原始JSON；GitHub报2026-11-15 03:23:32和03:26:31 UTC到期；全部源JSON SHA与旧归档报告相符。
- 本次会话已生成**完整17个原归档成员、三个原始ZIP、manifest SHA与双Mint有界Case**的下载包 `blix-20261101-original-market-snapshots-preserved-20261114.zip`（复合SHA256 `b8ade9d33bfc16cbbb43c78fa49415490f1860e08548bae06d4853ce2325bcf8`）。**该文件是ChatGPT本轮下载产物，尚未作为二进制文件永久提交GitHub**；在GitHub档案到期前下载到安全长期位置很重要。完整哈希表与原始业务区别见[单Mint审查新增真实双Mint来源段](single-mint-audit.md)。

**真正多币同次供应商观察的事实**（首次获取时间分别为2026-11-01 02:44:23.396和02:44:23.526 UTC）：
- BNB `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`：5个配对，主PumpSwap池报价`0.0008148` USD、流动性`$91,059.46`；Orca池`$47.83`、报价`0.0008145`。三次快照延续原研究，对Pool/Holder身份校核有用，非主网Swap验收。
- SIS `FdKdpz11GsTofLaNiddrhxrsE4APZYSSfLFqQ9YKpump`：7个配对，主PumpSwap池`0.0005512` USD、流动性`$64,871.47`；Orca池`0.0004137` USD、`$52.31`。Orca报价较主池约低24.9456%，而流动性约小`1240×`，不能称实际套利；另有四池无可用报价/流动性。
- 同源两币能说明**“池数多”与“流动性好”、不同池展示价差与“可执行收益”均不是同一判断**；但没有原Blix的完整发现/拒绝名单、源最早可见、实时双边路由报价/延迟、GMGN Radar真实历史导出，也没有真钱收益。

**离线程序交付（仅增加源数据fixture和检验，不造新市场引擎）**：
- `test/fixtures/public-provider-two-mints-20261101.json`：原ZIP+原始JSON哈希、两个Mint首次来源时间、主池/旁池原始数值、覆盖边界与UNKNOWN，全部为原档复算，不标伪“Blix Pulse已发现”。
- `test/public-provider-two-mint-history.test.mjs`：确认同批双Mint与来源而非原Blix Pulse名单；重算池深比及SIS近25%**展示**价差不构成可执行套利；通过既有 `followability-replay` 验证无首次可见时间/报价的真实样本为`UNKNOWN_SIGNAL_AVAILABILITY` / `MISSING_ENTRY_EXECUTION`。
- 两项测试已加入现有`package.json`的综合与`test:intelligence`脚本；未更改原版发现、Research、真实下单、API源或自动筛币。
- [包含新测试的提交c5e7778](https://github.com/sunshihao001/grok/actions/runs/43545133023)已有Node24综合CI PASS，独立[audit](https://github.com/sunshihao001/grok/actions/runs/43545133009) PASS；**后续证据文档/台账更新至最新HEAD时需按对应SHA重新查**，不能以旧绿灯证明未来提交。

**下一项真正能回答“专业增强发现优势了吗”的数据要求**：至少一次真实 Blix Pulse/Wallet 信号窗口中的**候选全集与拒绝理由、原始来源事件/捕获/浏览器首次可见时点、两版本同预算模型回执及延迟后真实可得报价**。没有这些条件时，R-38 A/B只证明合成输入条件下两种研究方案可以改变选择；R-39仅证明实际供应商两币市场结构存在分歧并能避免错误套利推断。**真实市场优势与净可跟随性仍未建立。**

**风险锚点**：这轮真实数据对过去“只有一个Mint”的认识做了修正，但没有推翻“真实A/B不可验”的结论。**若下一轮没有获取带真实首次可见时间和候选基线的源记录，不再无限增加类似合成A/B和模型分数**，优先保存源证据并寻找真正基线。

## 2026-11-14｜R-38：GMGN/Million/Synapse机会研究进入同候选离线A/B验收

**用户目标**：不再只做成熟项目名称/标签的抽象结合，而是让GMGN Wallet Radar、Million双向发现、Synapse分发/资金行为等与原Blix发现和Paper在**同一个真实业务目标**下产生可比较、可验收的差异。优先确认是否比原版早发现值得研究或可参与的Mint，而不是增加评分。前轮[原Blix参考产品再整合](https://github.com/sunshihao001/grok/blob/blix/docs/project/reference-driven-goal-model-v0.1.md#13-2026-11-14gmgn--既有成熟产品--blix机会优先全局再整合v04)仍是知识主真源；本轮新增**实际离线验收程序**，不另做交易终端/扫描器。

**真实历史样本**：[2026-11-01三次供应商归档复查](single-mint-audit.md)的`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`。主要PumpSwap池三次报价分别`0.0008148/0.0007653/0.0007819`美元，流动性约`$91,059/$88,619/$89,628`，Orca旁池仅约48美元，头部Token Account的Owner与主要AMM池地址精确匹配。**专业分析可提出库存方向、LP与公共设施假设，但既有档案没有逐笔真实Swap/LP、候选全集和当时可执行报价，因此无法评价真实A/B挑币率或收益。** 不把合成第二Mint混进这份真实归档。

**代码成果（现有PR#23集成分支）**：
1. 在 `server/intelligence/pulse-discovery.mjs` 的旧输入校验和发现回执加入 `candidateDigestSha256`，涵盖标准化Pulse候选数组及顺序、目标、browser时点、boardStatus；**仅证明两回执采用完全相同的浏览器输入，不证明提供方数据首次可见/完整性**。
2. 新纯函数 `server/intelligence/opportunity-read-comparison.mjs::compareObservedInvestigations` 只接受已有 `snapshot/baseline/enhanced` 调查回执，可选固定时点带源线索/纸面收据；验证A/B候选哈希和时点一致、不得选未经原始候选授权的Mint；有`firstAvailableAtMs`且晚于冻结浏览器时点的增量证据被拒；时间未知保持UNKNOWN。复用原 `followability-replay`，即便收据算正收益也不变成实盘Alpha。报告原样输出 `modelBenefitEstablished:false`、`NOT_REAL_MARKET_ADVANTAGE`，不可凭模型选中不同Mint称提高质量。
3. `test/opportunity-read-comparison.test.mjs` 使用**两种脚本mock模型**比较完全相同的两Mint合成Pulse输入：A只看市场资料，B收到标记为`SYNTHETIC_TEST_ONLY`的GMGN/Million式研究线索，允许Mint选择发生变化，但不得生成已确认市场优势。负例包含更改内容同数量哈希、增量晚到、未知首可见时点、外部Mint注入、坏缓存板、纸面假阳性。
4. 额外独立CLI `scripts/audit-opportunity-comparison-offline.mjs --input EXISTING_FROZEN_A_B.json` 只读有界本地JSON并输出详细对照报告；`test/offline-opportunity-comparison-cli.test.mjs` 确保输入SHA不变、缺文件不创建、非法输入拒绝。npm脚本`audit:opportunity-a-b:offline`可用于将来Grok云电脑真实离线历史的安全对照，但目前不会自己生成真实A/B回执或从外部抓全市场。
5. 以上测试已加入`package.json`原有`test`、`test:intelligence`，未改原版`research.js`、`brain.js`、`wtrack.js`、交易/钱包/签名代码，也未使用收费接口。

**已验收**：在增加第一个对照测试后的代码提交`3aac4ff5b688ca783ef6c8c1b89047fcffd92494`，[GitHub Node24 CI #43542355930](https://github.com/sunshihao001/grok/actions/runs/43542355930) **571/571综合、20/20安全、91/91经济证据、前端构建PASS**；[独立审计 #43542355842](https://github.com/sunshihao001/grok/actions/runs/43542355842) PASS。**后加CLI与本记录的最终SHA必须分别回看最新CI，不能沿用较早的绿灯**。Uptime原外部远程健康流程出现失败，不能把它混为对照测试用例失败或忽略为上线验收成功。

**仍未实现/未验的工作**：①Blix原版完整候选Universe的历史留存与遗漏；②从钱包而非Pulse新增的Mint必须另作来源覆盖/时点对照；③全市场实时数据、GMGN/OKX真实接口和模型A/B；④真实交易信号首次对人可见时间；⑤真实双边可成交报价/失败/退出；⑥样本外收益与真正的回访学习；⑦PR#23与blix基线仍有合并冲突、未合并。下一次要**先获取同一真实观察窗口的候选和来源时间档案**并验证历史覆盖，而不是继续堆合成正收益测试。

[同Mint真实证据及离线对照详细报告](blix-ai-investigation-product-comparison-20261113.md#10-2026-11-14gmgnmillionsynapse-与原-blix-同批候选的首次离线-ab-验收)。

## 2026-11-14｜R-37：GMGN与历史成熟项目重新梳理的知识承接（不重造代码）

**本轮依据用户提出的“GMGN这些有用的项目与之前看过的项目结合重新梳理”进行源级复核。** 原位成果位于**另一个分支**（本PR的base `blix`）：[参考成品逆向目标体系新增第13节](https://github.com/sunshihao001/grok/blob/blix/docs/project/reference-driven-goal-model-v0.1.md#13-2026-11-14gmgn--既有成熟产品--blix机会优先全局再整合v04)。2026-11-14 已再次检查当前PR #23仍Draft/open/未合并/mergeable=false；**本PR工作树没有因链接自动包含那份blix知识修订，不应声称已合并**。

**新增研究结论与工程连接**：
- GMGN官方 [Wallet Radar](https://docs.gmgn.ai/index/wallet-radar.md)可从多个Mint查重复交易、较早买入、共同持有与历史利润，最贴近现有 [Million](https://github.com/Kelows/million) Token↔Wallet 双向发现与本项目跨币群体入口；但重叠地址/共Slot/同源付款均不代表同控。
- GMGN [wallet-score](https://github.com/GMGNAI/gmgn-skills/blob/main/skills/gmgn-wallet-score/SKILL.md)区分钱包历史Track Record与跟单者可获得的Copyability，涉及跟随延迟、滑点、费用、持仓节奏；对应原Blix Paper/Track Record、PR23 followability-replay及Million的copyability，不将供应商评分当实盘Alpha。
- GMGN [First70/Insider](https://docs.gmgn.ai/index/insider-traders-snipers-first-70-buyers.md)明确存在部分持仓/卖出与转仓状态难辨的限制。R35/R36已在现有PR23经济档案层做了可复核的Swap+Transfer说明，避免在AI层重新计算源交易。
- [OKX OnchainOS](https://github.com/okx/onchainos-skills)、[PumpTrace](https://github.com/AntC215/Pumptrace)、[Pulse](https://github.com/nirholas/pulse)、[HoldTech](https://github.com/co-numina/holdtech)以及Synapse用户原笔记、Nansen/Cielo/Arkham/Bubblemaps/pumpwatch/PumpGrok、旧Hermes/qb-/meme-均已按“业务结果→不同专业机制→现有Blix承接→证据/成本/授权差距”在blix文档中重新对照。**历史65项候选目录仍是全量来源索引，不表示本次65项都再次独立核验**。

**不会因此改造的部分**：原Blix已存在的市场发现/Wallet/BubbleMap/Risk/Paper与PR23只读经济采集、原版受保护Research；不拉GMGN付费源/交易钱包、不复制第二套筛币或UI、不把供应商标签堆成“庄家分数”。

**下一次真实增量验收入口**：以同一批有完整发现时点与拒绝理由的Mint，对照原版Blix，观察“多Mint→钱包候选→Mint反查”的新发现和真/伪独立群体，对已到手行情做只读费用/时效/退出判定；计入失败样本/旧盲点，只有超越原版基线时才建议接入独立自动化能力。原来的“研究优先级 vs 交易机会”保留可并存输出，**尚无真实市场优势验证**。

**状态**：SOURCE_REVIEW + DOC_COMMITTED(blix) + PR_REGISTER_POINTER；本项没有新增生产代码、API实跑、付费或真实订单，**不能引用此前CI证明本轮研究改善交易收益**。

## 2026-11-14｜R-36：原版 Research 钱包数语义与同签名交易证据进入 AI 工作台

**起点与责任边界**：承接 R-35 的两个已验证边界：原版 `research.js::gather` 统计 `COUNT(DISTINCT wt.wallet)`（当前 watching=1、side=buy、同 Mint、无历史时窗），不是独立经济主体；`wtrack.parseTransfer` 对「同笔买入+独立 Token 转移」无法提供完整单动作摘要，但 PR #23 的 `economic-events.mjs` 已归档指令级转移。**本轮不解除受保护的 `server/research.js` 文件校验，不改原交易/签名/付款代码，不新建 RPC 采集器或数据库。**

**实际增量（已提交到 PR #23 现有集成分支）**：

1. `scripts/inspect-economic-mint.mjs` 使用已有 SQLite 只读文件和现存 `wallet_trades`、`wallets` 表，在表结构可用时执行与原版 Research 相同条件的**不同跟踪买入地址计数**，并记录时间口径 `ALL_LOCALLY_STORED_WALLET_TRADE_ROWS_NO_TIME_CUTOFF`；表缺失返回 null / UNKNOWN，启发式关系组与独立经济主体都保持 null / UNKNOWN。这个报告不进入原版 Research 的评级逻辑，也不是改写用户跟踪名单。
2. 通过同一份已保存的 `econ_transactions/econ_instructions` RPC 指令与 `wallet_trades` 摘要，逐条给已核转移事件新增 `sameSignatureSenderBuySummaryObserved`。它的含义是「发出方同笔签名有本地买入摘要，且另有 Token 转移指令」，**不**代表这两个动作可以相加、不代表转仓=卖出、更不证明后续卖出的就是这批库存。RPC 完整性、Owner 和指令位置仍由原经济证据链负责。
3. 现有 `server/intelligence/mint-economic-evidence.mjs` 向模型/调用方传递源标记的 `facts.trackedWalletActivity` 与每条 `facts.recipients` 的同签名标记，同时增加不确定性说明。没有新增 Agent 工具或授权。
4. 现有 `web/src/pages/Intelligence.tsx` AI 研究收据界面（**非原 WTrack 页**）展示原始地址数、关系组及真实控制者未知，以及同笔买入摘要与 Token 转移候选，清楚提醒旧 WTrack 简化列表可能不显示混合交易。原版 Pulse、Research、WTrack 和交易入口保留。
5. `test/offline-mint-report.test.mjs` 使用 3 个地址、2 个 watched、重复买入、合成「Pool→A 买入并 A→B 转移」fixture 验证：原始跟踪地址数为 2，组数 UNKNOWN；归档指令 A→B 400 单位仍可发现，同笔买入标记为真；同一 Pool 转移不被标为 A 买入；AI 证据适配透传且 SQLite 前后 SHA256 不变。此前缺表时的 UNKNOWN 与只读测试继续保持。
6. `test/intelligence-ui-candidates.test.mjs` 增加静态 UI 审查，保障新语义文字及同签名混合事件提示不丢失。前端应再由独立 Node24 CI 的 TypeScript/Vite 编译验收；静态匹配并非界面实操测试。

**已验证层级（在本段写入前）**：包含离线 Mint 新增测试的代码提交 `b8900820c29d233d2ebfea6362adb829e98e02de` 已通过 [Node24 综合 CI](https://github.com/sunshihao001/grok/actions/runs/43536813708) 和 [审计](https://github.com/sunshihao001/grok/actions/runs/43536813668)。**后续 UI/静态测试头提交 `c8596e8064f25752c1468cf9c349b4a049cc5739` 的 CI 在本段落写入时还没有可核验结果，不能沿用旧绿灯冒充最终 HEAD 通过。** Uptime 外部服务检查失败属于既有独立事项。

**尚未完成与下一步验收**：真正原版 `research.js` 的深读提示词仍只接收 legacy raw count，AI 研究工作台通过独立能力追加语义，不等于原版已经换算关系组。WTrack 原有普通交易列表尚未接入已捕获混合交易的只读注释，且本轮**没有开放其原过滤条件**以防将池/路由交换腿误写成普通转仓。下一项应在不破坏原版保留基线下核对 UI 数据契约，选择受控 Mint 的**同一触发时刻**，对照原版候选与现有专业解释的误报/漏报以及可执行成本；主网历史、实盘盈利仍 UNKNOWN。

## 2026-11-14｜R-35：钱包群组归因与同笔转仓的跨模块契约实测

**本轮根据用户确认的工作起点**：对照 Synapse 全分类研究，针对 Blix walletSignals、Research、WTrack 与 PR #23 经济证据的两处实际语义问题，在已有责任层进行有限修改/离线验收，**没有新增市场扫描器、RPC 数据源、AI Bot、交易入口**。经济归因以真实事件和当前覆盖为限。

**C1｜钱包数量与群组归因已做源码级纠正 + 回归测试**：
- 原 `server/wallets.js::walletSignals` 对 `independent()` 启发式关系分组使用“独立钱包”口径，且将 90 秒内同步买入说成“通常意味着同一操作者或复制机器人”。两个判断均超过证据：clusters() 的同币同期交易、共同手续费付款人不能直接确定经济主体。
- 在**现有 walletSignals** 原位改为：记录原始地址数与启发式关系组数；真实独立经济主体为 `UNKNOWN`；同期买入仅为时间事实，既不能证明同控，也不能证明相互独立需求。现有安全门禁和不安全代币提示保留，原本监控事件触发逻辑不变；保留代币符号的 `$` 显示。
- 新增 `test/wallet-signal-interpretation.test.mjs`，三合成钱包 A/B/C 中 A、B 共享第三方手续费付款人，C 单独买入；相同 Mint 上 `COUNT(DISTINCT wallet)=3`，现有 `independent()` 启发式组数为 2，测试要求告警不声称共同控制、不夸大独立需求，并维持不安全资产警示。此**不是**确认 A/B 由同一个人控制。

**C2｜同笔 Swap+Token Transfer：源侧证据存在，旧 WTrack 摘要有视图边界**：
- 直接沿用现有 `test/wallet-evidence-chain.test.mjs` 的合成“Pool→A 1000、A→B 400、A 净增 600”交易，确认 `wtrack.parseTransfer(tx,A)` 对该混合动作返回 `null`，而 `wallets.readTx` 通过现有 `economic-events.mjs` 原始 RPC 存档仍可将 A→B 的 400 单位指令作为 `recipientCandidates` 追踪。**旧 WTrack 当前视图不显示不能当作链上没有转仓**。
- 原本 `wtrack.js::fromTx` 检测 Swap 就直接返回，确有“混合交易不进入普通转账馈送”的源码条件；本轮未莽撞放开这道保护（可能把 DEX 资金池腿误标普通钱包转账），**没有宣称已经修复其 UI/馈送覆盖**。应在原 WTrack 责任层先设计与历史结构兼容且可区分交易池的安全增量，或通过已有 PR #23 经济调查面板提供指令级事实，不另建源采集器。
- `server/research.js` 仍统计原始钱包地址数，尚未使用上述关系组口径；现已用独立测试量化两者不同，但**未修改原 Research 受保护逻辑**。下次应明确 API 字段语义或经原版保留回归后做针对性衔接，不假装全产品统计一致性已完成。

**CI 实际核验（代码 HEAD `97068d589658e9610361bd2a1c44289fa47f7650`）**：
- [Node24 测试流水线 #43532644105](https://github.com/sunshihao001/grok/actions/runs/43532644105)：**564/564 全部通过、20/20 安全通过、90/90 经济证据专项通过**，同时跑过静态前端构建。
- [独立审计 #43532644125](https://github.com/sunshihao001/grok/actions/runs/43532644125)：**PASS**。此前两个 CI 失败来自本轮测试标题 `$` 字符的替换错误，已修正并经仓库回读、最终 CI 重新确认。不能把中途失败隐去，亦不能把外部网站 uptime 测试失败混作本代码回归。
- **未实施**：原版 Blix 全服务启动、真实 RPC/钱包历史回放、云环境部署、模型费用、交易、签名、付款、独立利润证明；PR #23 仍 Draft 且未合并。

**下一项高价值验收**：冻结同一 Mint 的观察时点与钱包名单，比较原版 Early/Triage/Research/Wallet 信号与证据增强版本的发现结果；先确定 source/consumer 字段语义、混合动作在 WTrack UI 的安全显示契约，保持原有数据源唯一。若增强只增加标签与文件而无纠错或机会发现增量，停止扩建。

## 2026-11-14｜R-34：RPC实时流中断状态在原源层暴露，防止重连被误读为补回

**发现与边界**：server/rpc-stream.js的重新订阅从tip继续，单靠连接状态`connected:true`不能证明中断期间消息已重放；这与原版engine.js有界发行补查、wallets.js签名轮询并不冲突。此项是**源连接状态语义**修正，不是已证实链上漏包或缺少补查。

**已实施**：在现有server/rpc-stream.js的onStatus中为失败/重连增加`coverageGap`（since、reason、until、recovered:false），保留原connected/error；该字段表示此RPC流本身**尚未提供重放收据**，不是断言其他原版补查失效。test/intelligence-source-readiness.test.mjs加入FakeSocket重连正反测试。无平行数据采集器、无新AI历史补齐、无真实RPC、无交易/签名。

**当前效果与待验证**：这只是已有上游回调的可观测状态，消费者尚未验证是否读取coverageGap，不能声称下游报告已正确降级或源端恢复完整。需按最新HEAD核查CI，真实供应商回放与跨模块受益UNKNOWN。下一步应先查看既有status消费者，避免为了传播一个字段新增并行状态系统。


## 2026-11-14｜R-33：纠偏实际工程试点——无旧锚点的钱包签名扫描错误判定“已覆盖”

**目标与授权**：接续R-31/32“主动发现→定位负责层→修复→验证”，并继承R-30“数据源问题优先改善原采集层，不在AI报告私补数据”。本轮找到可由源码逻辑复现、可隔离修复的真正判断错误，而不是再扩纠偏术语。

**被证实的代码逻辑缺陷**：原server/wallets.js::pageSignatures在first=false且lastSig=null时把reached初始化为true。若扫描RPC签名每页均满50条，因pages预算耗尽、没有观察到旧锚点或短页时，函数仍返回reached=true；下游checkpointWalletPage可能记录INCREMENTAL_ANCHOR_REACHED，误导“当前窗口已追溯到边界”，虽walletSignatureCoverage.historyComplete仍保持false。复现条件并不证明真实RPC历史曾发生特定漏包，只证明逻辑存在过度确认。

**修复在正确责任层**：wallets.js::pageSignatures改为首次采样以外默认reached=false，直到实际遇到短页或显式旧锚点；已存在wallet-signature-coverage.mjs继续承担窗口、缺口/风险与游标的唯一记录。原miss日志从“the oldest were skipped”的确定陈述改为“older events may be missing”的正确不确定性，避免纠偏误报。未更改外部供应商、AI sidecar、新建游标、交易/签名入口或数据库结构。

**离线验收**：test/wallet-evidence-chain.test.mjs新增正反测试：无锚点增量扫描连续两满页（page budget）必须reached=false；短页自然结束和旧锚点场景仍true。既有test/wallet-signature-coverage.test.mjs已有reached=false持久化与historical risk测试。GitHub Actions测试/审计状态需核最后分支HEAD；本登记不预判真实主网覆盖。

**跨层影响**：O2关键钱包、O3资金Token经济链、O4跨Mint、S4血缘/来源、S5覆盖契约、S6测试、S7纠偏与防复发。通过源层共同函数影响所有钱包用户；下游报告不再直接复写RPC采集逻辑。

**仍未知**：无真实RPC/网络重放，本轮不能证明供应商实际遗漏率或补查完整性，也没有增加签名源头本身提供的事件数量。纠正的是**检测到不足时不错误报“已完整”**，属于更可靠的源数据覆盖评价，而非承诺填补历史数据。


## 2026-11-13｜R-32：纠偏机制第一次纠正自身错误诊断（已执行的跨模块复核）

**原诊断的问题**：前面的数据源责任台账只看到了server/sources.js::pumpStream里有重连、无独立历史补查，于是容易把该文件缺口扩大成“原Blix发行补查能力缺失”，进而推动新建采集逻辑。**这是证据覆盖范围错误，属于知识/源码审查失效，而不是已证明的运行BUG。**

**这轮新增的原仓源码事实**：
- server/engine.js::fillLaunchGaps()由server/livetrades.js::onLiveCreate供给链上发行事件，和PumpPortal共同发现；engine.js::backfillLaunches()从pump.fun近期列表按最多8页启动、最多4页周期补查（45秒），429停止；server/engine.js::scanRecent()另查其他发行平台近期代币。**Blix已具备有界发行回补和多来源交叉发现**。
- server/livetrades.js::loadState有2分钟内的状态恢复；这是恢复快照，不等于实时流断线期间所有交易补齐。
- server/wallets.js::pollOne/pageSignatures已提供钱包交易签名轮询补查，并经wallet-signature-coverage.mjs记录原子游标、窗口与gap。不能提议AI再建一套钱包签名源。
- server/rpc-stream.js对过期流从tip重连的行为仍成立，但“哪个具体钱包/市场事件因此漏掉、已有哪个补查组件能否弥补”需限定流种类和时间窗口，不能将不同发行、市场交易、钱包处理流混为一个事故。

**已经修复的是项目错误判断**：在[多层锚点第11–12节](cross-layer-anchor-map-20261113.md)明确撤回“缺少发行补查本身”的宽泛假设；保留真正待验问题：**已有补查对源时点、原始交易、特定断流的历史完整性与可观测coverage能否提供独立收据**。此修订为DOCUMENT_DIAGNOSIS_CORRECTED / SOURCE_CODE_REVIEWED，不能谎称发现或修复了实际漏包问题。

**新的可检验工作起点**：在R0权限范围和实际可取得的原版源证据内，选一个断流或历史不足场景，先对比engine现有补查、钱包轮询与不同RPC源的实际覆盖，再确认是否仍缺独立gap记录、重放或质量验收；必要修复只落在各自**既有**来源所有者。不在AI sidecar另造源。若现有机制已经足够，则保留观察而不增加代码。

**纠偏是否有效的证据**：这轮已从狭窄文件观察纠正为跨模块实际代码事实并避免错误开发方向；真实漏包恢复效果仍UNKNOWN，尚无新增主网/模型/付费执行。今后每条源端缺陷候选在提修复前至少查完同责任链的现有补偿机制；不要求所有小bug执行复杂RCA。


## 2026-11-13｜R-31：纠偏概念全层扩写——定位源头，修责任层，防止过度纠偏

**用户明确提出**：多个项目部位存在纠错需求，需要把“纠偏”作为完整能力打磨；它不限于改错文案或代码缺陷，涵盖目标、知识、来源、语义、采样、设计、程序、验收和AI任务选择。**总目标O1–O6不变，仍保留完整原Blix和只读扩展，不额外建设纠偏Agent。**

**本轮承接的两个权威位置**：
- [ai-d第13节：偏差/修正/根因/CAPA/单环双环学习](https://github.com/sunshihao001/ai-d/blob/main/knowledge/foundations/cross-layer-project-anchors.md#13-2026-11-13纠偏能力的深层扩写纠错校准根因修复与学习v03)，作为跨项目方法来源。
- [Blix多层锚点第12节：纠偏对象、归属、样例与验证](cross-layer-anchor-map-20261113.md#12-2026-11-13纠偏的专业扩写从修一处错到首个失效环节职责与全链结果-v03)，只在现有O1–O6/源/代码/测试中追查，不创建新的全仓映射引擎。

**源码核对与风险优先级**：原版rpc-stream.js重连有从链头接续且跳过消息的明确实现取舍；sources.js PumpPortal WS已有重连，**但不能只看此文件就推断Blix没有发行补查**：engine.js::backfillLaunches已有启动和周期有界近期列表回填，fillLaunchGaps通过livetrades.js交叉发现；钱包端wallets.js已有轮询补查，wallet-signature-coverage.mjs仍清楚记录初次采样不足/历史不完整，economic-claim-trace.mjs明确sell摘要不能证明同批转入库存；pulse-discovery.mjs只处理有限浏览器候选；followability-replay.mjs可计算有严格来源的纸面收据但不证明真实盈利。**这些只是源可见事实与潜在错误传播路径，不证明供应商/真实市场实际漏包或已验证的具体资金错误**。见原映射中带证据等级的优先对象表。


## 2026-11-25｜R-56：弱历史 inbound 不得覆盖当前交易的强歧义证据

**本轮高价值缺口**：复核 R-54 Token-2022 fee 与 R-53 mixed-flow 判断在同一 `recipientOutcomes()` 路径中的优先级。源码显示，`priorInbound` 只证明“该接收钱包在更早时间有过同 Mint inbound activity”，证据强度明显低于当前交易的 mixed same-Mint flow 或 Token-2022 transfer-fee 事实。

**发现**：原逻辑会在当前交易已经得到 `INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS` 或 `TOKEN_2022_TRANSFER_FEE_PRESENT_PROVENANCE_UNPROVEN` 后，再用任意更早 inbound 覆盖为 `PRIOR_CAPTURED_INBOUND_ACTIVITY_EXISTS`。这会丢失更强、与当前交易直接相关的证据。

**修正**：仅当当前 `inventoryLink` 为 `PROVENANCE_UNKNOWN` 或 `AMOUNT_COMPATIBLE_BUT_PROVENANCE_UNPROVEN` 时，弱 prior-inbound context 才能覆盖；不得覆盖 `INTRA_TRANSACTION_NET_DELTA_AMBIGUOUS`、`CANNOT_BE_FULLY_SOURCED_FROM_THIS_SINGLE_TRANSFER` 或 `TOKEN_2022_TRANSFER_FEE_PRESENT_PROVENANCE_UNPROVEN`。

**证据等级**：源码修正 = `CODE_OBSERVED`；现有 R-53/R-54 fixtures 可作为离线回归入口，但本次新 HEAD 的 CI = `UNKNOWN/NOT VERIFIED`，真实主网库存归因 = `UNKNOWN`。本修正不证明 provenance、common control、PnL 或交易机会。

**外部反证**：Solana 官方 `getTransaction` 将 innerInstructions、pre/post token balances、fee 分开定义；token balance 是 account-level state，而 instruction amount/fee 是 execution-level facts，因此不同证据强度不应在后处理阶段互相覆盖。citeturn149341search1turn149341search12 GitHub 的 solana-explain 也将 token balance fixtures、WSOL wrap/unwrap、Jupiter swap 与 Token-2022 fee 作为不同 transaction cases，而不是用单一 net delta 解释全部行为。citeturn149341search17

**下一阻断**：继续 R-56/R-57 的最高价值验证应是把一个真实 archived transaction 同时跑过 mixed-flow、Token-2022 fee、WSOL/SOL balance 与 block order，确认当前证据优先级在真实样本上不会产生错误升级。