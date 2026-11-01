# V0.1 真实公开Mint数据验收记录｜2026-11-01

**真实执行，不是Fixture。** 源：[GitHub Actions run 41266389009](https://github.com/sunshihao001/grok/actions/runs/41266389009)（本分支临时安全只读smoke任务）。原始JSON与报告由Action Artifact `v01-public-mint-snapshots-20261101` 保存30天；已下载ZIP进行本地只读解包、核对每份`provider-raw.json`的SHA256与`report.json`相同、每个返回池的`baseToken.address`或`quoteToken.address`确实包含目标Mint。临时的在线smoke已从标准CI撤回，后续仅保留纯离线稳定回归。

| Mint | 公开数据商 | 返回池数 | 抓取时间(UTC) | 原始JSON SHA256 |
|---|---|---:|---|---|
| `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` | DEX Screener | 5 | 2026-11-01T02:44:23.396196+00:00 | `240dca2d3df8cfbf9e0f09d806d61b2ae6040abc07bcebc4b9dd3e07f3d09897` |
| `FdKdpz11GsTofLaNiddrhxrsE4APZYSSfLFqQ9YKpump` | DEX Screener | 7 | 2026-11-01T02:44:23.526475+00:00 | `5cdeb33076e1df0a2efc24c1c3daf6b4cce4c3832ac131ddaf4f5ab105dbf7b4` |

**可复核的实际快照细节**：第一Mint的PumpSwap池`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`流动性约`$91,059.46`、供应商24h池成交量约`$5,326,458.55`；第二Mint的PumpSwap池`Ht4GxW1pL2SfamcfC3qcZEcjDHpE55TtjUjnKVs2nhxr`流动性约`$64,871.47`，供应商24h池成交量约`$2,521,823.88`。**这些是2026-11-01特定查询时刻的供应商数据，不是推荐交易，也不是SOL RPC independently verified。** 由于报告显示多个DEX/池和把目标Mint作为base/quote的不同方向，程序仅在目标作为base时引用供应商`priceUsd`；不能简单汇总池买卖次数为钱包数量。

**反例与限制**：先使用`DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263`（BONK）试验，GitHub Actions得到HTTP成功但`[]`，状态明确`NO_PAIRS_RETURNED_COVERAGE_UNKNOWN`，**不能证明BONK缺少交易池**。本地执行机DNS不可用；GitHub Action拥有网络，不等于本地/Grok云电脑已经可正常请求。现有真实验证只涵盖公开DEX池交易活跃度、流动性数据与来源保全；**没有任何Holder、Owner、Dev历史、资金图、成交细节、库存核对或异常群体的真实验证**。

**安全审查（E-L7-03 + E-L0-02 + E-L1-01 + E-L3-02 + E-L6-01）**：
- `public_pair_report.py`使用硬编码的公开HTTPS域名、固定GET、禁止转跳、响应大小限制、12秒超时、链与Mint一一匹配、空结果降级UNKNOWN，不调用钱包或交易代码。
- OKX仍是完整单Mint业务首选。其CLI`cli/src/client.rs`确有自动x402配置/支付签名流程，未经验证付款隔离前不从我们的`mint_v01`自动启动。已有`--okx-json`入口仅消费合法保存结果。
- 非OKX的公开池来源是**最低成本可运行基线**，并不能替代资金与Dev成品。不要拿本轮真实“交易池已运行”作为V0.1“完整关键钱包/Dev报告已交付”的验收通过。
- 离线控制回归应持续在`.github/workflows/ci.yml`运行；实际在线数据应按需、带记录单独验收，不让公开API波动影响CI通过。

**结论**：`REAL_PUBLIC_POOL_SNAPSHOT_VERIFIED`已证实；`REAL_FULL_MINT_INTELLIGENCE`仍待OKX安全授权或另一条确有Holder/Dev来源的成熟工作流。下一项是取得一次已授权完整`token-research` JSON，复用已验证的`mint_report.py`，补齐关键钱包/来源/Dev字段；而不是再开发第三个DEX池适配器。
