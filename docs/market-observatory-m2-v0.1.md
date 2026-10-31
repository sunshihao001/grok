# M2｜Wallet Burst Observatory：多钱包群体异动离线监控原型 V0.1

**定位**：Solana Meme 全局监控 OS 的 **M2（窗口与群体事件聚合）研究原型**。不是交易 Bot、交易执行器、实时链上监听程序，也不声称已识别庄家或统计异常。

## 已实现的能力

- 接收由上游采集/解析器提供的跨 Mint 规范化事件账；
- 严格区分 SOL 转账、SPL Token 转账、已由输入来源**声称已解析为** SWAP_BUY 与 SWAP_SELL 的事件；本程序本身不验证 Swap 指令；
- 同一 `signature + instruction_index + inner_instruction_index` 的重复来源记录去重，保留原始来源引用；同 ID 内容冲突直接失败；
- 默认按 5/30/300 秒**固定时间桶**计算输入集合及各 Mint 的事件数、交易数、不同交易钱包、不同资金发送/接收 owner、SOL 转账总额、买入耗费 SOL、卖出获得 SOL、Token 转移数量。SOL 转账与 Swap 的 SOL 不相加成伪“总资金”；
- 在 60 秒**滚动窗口**中提供群体活动候选：`FUNDING_FANOUT`（一对多 SOL 注资）、`SAME_SLOT_MULTIWALLET_BUY`（同 Slot 不同地址买入）、`TOKEN_CONSOLIDATION`（多地址 Token 转向同一 owner）；
- 在 300 秒资金回看窗口内提供 `FUNDING_TO_BUY_CANDIDATE`，在跨 Mint 维度报告 `CROSS_MINT_FUNDING_REUSE`、`CROSS_MINT_WALLET_ACTIVITY`；
- `decision_at` 存在时，只有 `available_at`、`received_at`、`block_time` 都不晚于决策时点的事件才进入研究；来源未知或迟到直接剔除并计数；
- 全程保留原始 `signature`、Slot、source_ref 与时间戳，不做同控实体合并、Jito bundle 确认、收益预测或交易动作。

**特意没有完成**：Solana RPC/OKX 的真实采集、内外指令的独立解码、完整覆盖率与掉线重试、持久化流式状态、条件正常/异常基准、公共 hub 识别、市场行情合并、样本外预测和真实交易收益评估。

## 命令（从 Grok 仓库根目录）

```bash
PYTHONPATH=src python -m solana_meme_os.market_observatory \
  --input fixtures/market-observatory-synthetic.json \
  --allow-fixture \
  --windows 5 30 300 \
  --output .runtime/market-observatory-example.json

PYTHONPATH=src python -m unittest discover -s tests -v
```

⚠️ 输出目录 `.runtime/` 必须事先存在，可先 `mkdir -p .runtime`。只有在指定 `--allow-fixture` 时才允许显式合成数据输入。测试数据中的地址、Token 和交易签名均为**虚构**，绝不代表链上事实。

如有已归一化的来源数据，可将 `mode` 设为 `source_derived` 或 `rpc_supplied` 并省略 `--allow-fixture`；两种模式仍不意味着模块独立核验过上游来源。没有真实原始事件时不可用它宣称实时监控已完成。

示例：在 `2026-10-29T07:00:19Z` 决策时切断未来信息：

```bash
PYTHONPATH=src python -m solana_meme_os.market_observatory \
  --input fixtures/market-observatory-synthetic.json \
  --allow-fixture --decision-at 2026-10-29T07:00:19Z
```

## 输入契约：Canonical Event Ledger 0.1

```json
{
  "schema_version": "0.1",
  "chain": "sol",
  "mode": "fixture",
  "events": [
    {
      "signature": "synthetic-event-1",
      "slot": 100,
      "instruction_index": 0,
      "block_time": "2026-10-29T07:00:00Z",
      "available_at": "2026-10-29T07:00:00Z",
      "received_at": "2026-10-29T07:00:01Z",
      "source_ref": "synthetic-fixture",
      "event_kind": "SOL_TRANSFER",
      "from_owner": "Wallet-A",
      "to_owner": "Wallet-B",
      "amount_raw": "2000000000"
    }
  ]
}
```

`TOKEN_TRANSFER` 增加 `mint` 和 `decimals`，`amount_raw` 是 Token 原始最小单位整数字符串；`SWAP_BUY/SWAP_SELL` 使用 `wallet`、`mint`、`decimals`、`sol_amount_lamports`、`token_amount_raw`，并非 SOL_TRANSER 的字段转换。`instruction_index` 用于区分同一交易下的多条事件；同 Slot 的先后关联必须有独立 `transaction_index`，否则不能自动把同 Slot 注资认定为买入之前的资金路径。

`source_ref` 用于溯源，`available_at` 表示该来源实际已可用时间，`received_at` 表示系统实际接收时间。事后读取历史交易时不能倒填两个时点，缺失应保留为空、在 `--decision-at` 模式被剔除。

## 输出与误用边界

`scope: INPUT_COHORT_ALL_MINTS` 的意思是**这批输入事件覆盖的所有 Mint**，不表示真正采集到了全 Solana 市场所有交易。各 Mint 的指标只来自该 Mint 的 Token/SWAP 事件，不能自动把所有相关 SOL_TRANSFER 归到某个代币。相关资金关系只能作为独立的时间限制假设。

`unique_actor_addresses` 统计参与事件的地址/owner，不保证都是自然人或普通钱包；`unique_trade_wallets` 统计输入的 SWAP 交易主体地址，仍不是独立经济实体数。原始计数和正常/异常判断永远分开。

所有 `group_candidates[]` 都返回 `anomaly_status: UNASSESSED_NO_BASELINE`，任何标签不应当被解释为“异常已经证明”。

| 候选类型 | 直接证据 | 未证实的解释 |
|---|---|---|
| `SAME_SLOT_MULTIWALLET_BUY` | 多个不同地址的已归一化买入事件拥有相同 Slot | Jito Bundle、同控主体 |
| `FUNDING_FANOUT` | 相近时间内同一地址向不同接收者转账 | 这些接收者的密钥或受益人相同 |
| `FUNDING_TO_BUY_CANDIDATE` | 地址在买入前的时间窗存在 SOL 资金流入 | 该笔资金就是买单的唯一来源 |
| `TOKEN_CONSOLIDATION` | 不同发送 owner 将 Token 汇向同一接收 owner | 接收者已市场卖出、由谁受益 |
| `CROSS_MINT_FUNDING_REUSE` | 同一候选注资方在多 Mint 买入前出现 | 跨币种操盘或统一控制 |
| `CROSS_MINT_WALLET_ACTIVITY` | 同一交易地址在多个 Mint 有活动 | 非正常钱包或被证实的机器人 |

## 开发验收和限制

`tests/test_market_observatory.py` 覆盖输入范围、精确金额、去重、签名冲突、同一交易多指令、同 Slot 缺顺序、跨窗口聚合、跨 Mint 描述、决策时间及禁止伪盈利结论。测试文件写入仓库并检查，但**当前执行环境无法获取 GitHub 文件到 Python 运行容器，因此尚未完成该模块在完整仓库中的 Python unittest 执行**。已对 fixture 做独立数值核对：前 30 秒 8 条事件，3 笔 SOL 转账合计 10 SOL，3 笔买入合计 7.8 SOL，两条 Token 转账共 42 Token（2 位 decimals），6 个参与地址 / 3 个买入地址。这个数值核对不替代 Python 单元测试。

下步工程顺序应为：**M1 真正的数据/解析适配器 → M2 有状态增量事件存储 → M3 钱包和资金图 → M4 条件基准**。在有足够真实数据之前不要建立“疑似庄家确定率”或固定盈利阈值。

**认知指令：** 先记录事件，再发现群体；先描述可重复的时序关系，再比较正常基准；先排除公共结构，再推测经济关联；最后研究是否对未来市场有真正增量。
