# R002｜公开交易事件的经济仓位复原：87QChghg... 案例 V0.1

> 日期：2026-10-31；研究状态：公开仓库多数据表交叉核对，未执行独立 RPC 复算。  
> 研究技能：`skills/solana-meme-expert-writing/SKILL.md`。  
> 来源版本：`sunshihao001/Why-Solana-Memecoins-Are-Over@9a7ad51d56328e91e67e3f531d6744307d0ee68b`。  
> 研究范围：案例涉及早期创建时段；绝不从单一事件推广到所有 Solana Meme。  
> 安全边界：只读研究；不含买卖指令、自动交易、签名或资产操作。

## 0｜研究问题

对一个在新币创建 Slot 早期取得大量代币的地址，复制它的交易是否能够得到同样的经济收益？

这个问题首先需要回答三个更基础的事实：  
**地址买入了多少？代币转去了哪里？记录里的“卖出”是否能与库存变化、真实对价及成交时点完全核对？**

研究该事件的重点不在于寻找“庄家”，而在于展示一个可复核的仓位分析单位如何从地址交易、交易顺序、资产流动、经济归属假设和可复制性中逐层形成。

## 1｜案例来源及原始可复核标识

- Mint：`87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump`
- 创建 Slot：`429307208`
- 创建时间（来源 `created=1782591657`）：`2026-06-27T20:20:57Z`
- 创建签名：`4ziGdYrysFAXNkxgsjwPh9nhevDgoNZKm3T2q9j7D14YWZ1mbb7zCYGyBTkthrmKtLshxFgQ63MqpBxJ7Ecbj48x`
- 第一笔记录的外部买入签名：`6FGfTfSf9oYJ9CyWmVwCMNgqEentJUQjvuuzGmu4jsxLwWv1dHonGtXD2DUUyYd7ojcEvVdZjCJE2iXyYrZeYoQ`

交叉读取三个原项目的提交数据：
- [`data/v03_onchain.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v03_onchain.json)：创建签名、四笔买入地址及金额/代币数量；
- [`data/v04_slot_order.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v04_slot_order.json)：创建 Slot 内交易索引及首位记录的外部买家；
- [`data/v05_creation_block.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v05_creation_block.json)：同期群体汇总与均价；
- [`data/v07_exit.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v07_exit.json)：Token 转移、接收者和汇总卖出；
- [`code/v07_exit.py`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/code/v07_exit.py)：如何定义 SELL、TRANSFER、累计转出和转出比例。

以上资料均为研究作者当时处理的**链上数据派生记录**。本轮检查了数据文件互相是否一致，但没有从公链 RPC 再次获取每个签名的原始交易，不得将它写作“本轮独立验证了链上事实”。

## 2｜价格形成：同一 Slot 内，也不是同一个价格

原资料记录创建交易位于该 Slot 的 index 312，随后四笔买入位于 313、314、315、316；原资料未记录在这四笔完成前的外部买家。

| Slot 内顺序 | 钱包（前缀） | 投入 SOL | 收到代币（百万枚） | 买入平均价，SOL/Token |
| --- | --- | ---: | ---: | ---: |
| 313 | `2AqFJz...` | 21.827137 | 441.614 | 0.0000000494258 |
| 314 | `9yxmCN...` | 21.150792 | 178.247 | 0.0000001186602 |
| 315 | `2wHHnA...` | 21.150190 | 98.716 | 0.0000002142523 |
| 316 | `22vL22...` | 20.813336 | 61.887 | 0.0000003363110 |

四个地址合计投入约 **84.9415 SOL**，获得 **780,464,208.09 枚代币**，在来源定义下约占总供应量 **78.046%**。最早与最晚一笔的买入均价相差约 **6.804 倍**：即使同 Slot 且相邻索引，也不能把四个地址的成交价格视为相同。

被记录的首位外部买入位于 index 601，交易签名在上文。其交易价格约 `4.14063e-7 SOL/token`；对应四个早期地址合并 VWAP 的比值 **3.805**，相对该组最早一笔地址的买入均价约 **8.38 倍**。

这两个比值仅为来源中**不同实际交易成本之间的价格对比**，不是一个策略的可实现收益倍数。外部首次买单量、其后池子价格冲击和可售数量均与这一比较不同。

**认知转化 1：** “首批买入钱包盈利”可能含有不可复制的价格形成位置优势。任何钱包监控研究都要保存 Slot 内顺序、买入成本和我们首次能够读取该交易的时点，而不是按 Slot 时间戳认为所有买家同时且同价。

## 3｜仓位流向：转账发生了，但不能直接等同于最终卖出

`v07_exit.json` 为本事件的四个早期地址分别记录一次“首次 Token 转移”，距买入的时间为 19、19、28、35 秒，接收者有三个不同地址。

| 原买入地址（前缀） | 首次转移延迟 | 转往地址（前缀） | 汇总转移量（百万 Token） | 派生数据标记的直接卖出（百万 Token） |
| --- | ---: | --- | ---: | ---: |
| `2AqFJz...` | 19 秒 | `8uSfX74...` | 441.614 | 3.406 |
| `9yxmCN...` | 19 秒 | `eUrS4Fa...` | 178.247 | 6.792 |
| `2wHHnA...` | 28 秒 | `5Xbhac...` | 98.716 | 3.028 |
| `22vL22...` | 35 秒 | `eUrS4Fa...` | 61.887 | 4.893 |

样本也保留了四条 Token 转移签名，其第一条为：

`6rByjVMZH8Ggy4Deh86cvDKtzHGqVayHKkFWrPcxZtHmp7S42vixbz1hWr9b13TrooURBu9sCnbf8C4u3rucyry`

原资料报告四个地址另有累计约 **18,119,267.30 Token** 的“直接卖出”，其记录的 SOL 增量合计 **2.46 SOL**。这个数字**不是完整实现利润，也不能从中得出本组亏损**：大部分初始 Token 已被转移，接收地址之后的卖出与资金回流不包含在这张表的经济核算边界里。

**认知转化 2：** 同一笔经济风险可能跨地址延续。钱包原地址的 Token 减少，不等于相关资本敞口退出市场；地址余额变化和完整仓位利润需要两套不同的计算边界。

