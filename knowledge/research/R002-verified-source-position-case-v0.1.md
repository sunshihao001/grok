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

## 4｜本轮新增的关键审计发现：派生数据暂时无法完成库存守恒

将同一 Mint 在两个 JSON 文件中的数量相互核对：

```text
v03：四钱包创建 Slot 买入           780,464,208.09 Token
v07：四钱包累计“转移”             780,464,208.09 Token
v07：四钱包累计“直接卖出”          18,119,267.30 Token
v07：“转移 + 直接卖出”            798,583,475.39 Token
超过 v03 初始买入记录              18,119,267.30 Token（约 2.32%）
```

这**不是已证实的账本违规、凭空增发或源码作假**。两个派生文件未必使用同一时间边界：`v03` 仅描述创建 Slot 买入，而 `v07` 扫描相关 Token Account 的后续活动；后续再次买入、外部转入、重复口径或事件分类问题，均可能使汇总量不符合“只看首批四笔买入”的简单守恒模型。

但只用当前汇总字段，无法判断哪一种解释成立。

尤其要核对 `code/v07_exit.py` 实际计算方式：

- `sigs_all(ata)` 按 Token Account 地址枚举多笔历史交易，而不是只取首个创建 Slot；
- `classify()` 根据关联 ATA Token 余额减少与 owner SOL 余额净增 `>0.0005` 将交易归为 SELL，或者根据其他 owner 的 Token 正增把它归为 TRANSFER。这是**派生分类器**，尚非我们已独立核实 AMM swap 指令及净成交对价的证据；
- 导出的单钱包记录仅显示第一次识别的 BUY 的时间，没有汇总此后所有额外买入/转入的 Token 数量；
- `part_transferee` 在源码中定义为 `tt/(tt+tv)`，即报告中“转移量相对转移量与卖出量之和”的份额。它不等于严格意义上的“发行总供应量被转移比例”。本事件该值是 0.9773，但 `tt` 数值恰好等于最初四钱包获得的 780,464,208.09 枚。

**专业判断：** 此时不得宣布“钱包已经全部卖掉”“资金已实现盈利”或“token 守恒失败”。正确结论是：`INVENTORY_RECONCILIATION_OPEN`。真正需要补的是同一 Token Account 的完整按序 BUY / TRANSFER / SELL / 其他变化及余额，消除重复记账后再计算现金流。

这正是知识转化需要实现的质量差别：从“引用一个转移占比”进化到“先检验该占比的分母、事件分类和余额守恒口径”。

## 5｜经济主体推断应比资产图更保守

在该事件中，四个狙击地址转向三个接收地址，其中 `9yxmCN...` 与 `22vL22...` 的首笔转移均指向 `eUrS4Fa...`。

这一条“两个地址向同一接收者转币”能够支持**共享接收通道**的观察，但不能单独证明：

- 两个原地址由同一真实人控制；
- 接收者持有者是利润的最终受益人；
- 该转移一定为了出货或操纵；
- 接收者在收到 Token 后立即卖出了全部仓位；
- 项目已经确认了资本从该接收者回到原资金源。

后续资料 `exit_destination/results.md` 在**另外的选定样本**中确实深入追查了接收钱包在 PumpSwap 上的卖出与回流，提示这种机制可以被更深地审计；但那些结果不能在缺少 Mint 对应关系的情况下直接算作本案例“已验证的下游路径”。

相关研究：  
https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/exit_destination/results.md

**专业判断：** 当前只获得了 `ASSET_PATH_PARTIALLY_TRACED`，没有获得 `ECONOMIC_BENEFICIARY_CONFIRMED` 或 `POSITION_PNL_CLOSED`。

## 6｜三项新机制：让案例提出可推翻的研究问题

### M1：创建 Slot 内的成本分层（Entry Priority Advantage）

同一 Slot 的四笔连续买入，其单位成本已差约 6.8 倍；外部记录的第一次交易成本进一步高于早期组的合并成本。由此提出：某些高盈利地址的收益可能来自其在发行交易队列中的位置，而不是未来市场需求预测能力。

**必须挑战的替代解释：** 买入代币数量与支付 SOL 的不同可能还反映具体的 bonding-curve 算法、创建者先买和费用差异，而非单纯“私有信息”。

**验证：** 重放创建指令和每笔真实 swap 的 Token/SOL 前后余额，计算池子状态连续变化，核对每笔买入是否为交易行为、报表是否剔除相关费用，并对不同发行定义一致的先后成本优势。

### M2：代币转移可能代表库存托管/执行分工，而非最终出货（Position Routing）

若早期账户将主要库存转至稳定的接收账户，而后者另行选择时机和路径出售，单地址买卖跟随会遗漏真正的价格暴露变化。

**竞争模型：** 纯粹地址整理、资产托管、交易服务商共同接口或跨方经济所有权转移也可能产生相似记录。

**验证：** 逐签名追查接收账户的 Token 入/出、对应 Swap 真实对价与可能回流路径；对每一次转移保留时间和控制归因的分离。只要原钱包—接收者控制关系仍未知，不能强行汇总为实体 PnL。

### M3：风险监控可能比复制买入更可迁移（Inventory-Risk Information）

即使原钱包的极早入场成本不可复制，原地址及接收者的库存变动可能改变后续可售供给与市场承接风险。提出“不是跟它买，而是研究这组库存变化如何影响下一段价格/池深”的反向研究假说。

**竞争模型：** 相关库存流动可能发生在价格变化之后，仅仅跟随已有市场趋势；也可能内部转账并未增加市场卖压。

**验证：** 严格使用 `available_at <= decision_at` 的 Token 转移/Swap 指标，预测尚未发生的池深变化、真实卖出强度与净收益；与只用成交/价格/流动性指标的对照模型比较，按代币/操作簇拆分样本。若增量不成立，归入描述性知识。

## 7｜面向 Grok 的可执行取证合同

要把本次案例由“公开数据交叉核对”提升为“独立真实链上复原”，下次只读研究至少完成：

| 验证节点 | 所需事实 | 完成条件 |
| --- | --- | --- |
| 原始创建及四笔买入 | 五个真实签名，Slot、顺序、pre/post Token/SOL 和费用 | 每笔实际输入输出能复算；时间及程序名称记录完整 |
| 四次首次转移 | 四条 `premier_transfert_sig`、接收地址、Token Account Owner | Token 变动能与原报表一致，分清转移与 swap |
| 18,119,267.30 Token 多出的流转口径 | 原始 ATA 整个生命周期的每笔事件 | 查明是否由额外买入、外部转入、重复事件或分类/汇总问题形成 |
| 三个接收地址的后续行为 | Token 入/出、真实卖出对价、未实现库存和手续费 | 能明确哪些资产路径已闭合、哪些未知 |
| 资金与主体归因 | SOL 回流签名、公共 hub 排除、重复网络 | 只能在有独立证据时推断同一经济主体 |
| 跟单可行性 | 数据源首次可得、接收时间、真实报价、限额、费用和退出 | 不使用过去买入价替代当时可执行成交价；正净收益需独立测试 |

**现阶段没有实际完成 RPC 验证、没有核实接收者最终现金流、也没有计算跟单净收益。** Solscan 的相应页面本轮网页访问失败，因此不能声称已借助区块浏览器复核交易。若无法取得原始链上数据，应维持这一证据状态，不借助市场叙事补齐缺口。

## 8｜本单元完成的知识转化

1. **从地址标签到经济对象：** “首批钱包”只是活动分类；仓位应该依循买入、转出、下游交易与未解归属重建。
2. **从时间戳到价格形成顺序：** 相同 Slot 也可能有很大的成本差；不保留同 Slot 索引、价格和首次对外可见时间，就无法研究复制优势。
3. **从指标读取到数据审计：** 转移份额的分母和累计数量必须过库存守恒检查；发现矛盾首先进入来源验证，而非情绪化宣布项目异常。
4. **从市场解释到交易研究：** 即使证实某种重复执行网络，也须另行检验观察后是否具有预测增量和可成交净收益。

**结论：** 本案例支持“早期进入的成本位置不同、代币存在快速跨地址流转、单地址经济结果未闭合”这三个相互分离的事实层；不能支持“已经确认真实控制者”或“已发现可跟单正期望”。

**认知引导：** 穿透地址，核对资产；穿透交易时点，复原价格形成；穿透历史利润，检验观察者真正能捕获的经济价值。

## 附录｜精确交易引用（便于下一次独立复算）

以下是来源 `v03_onchain.json` 与 `v07_exit.json` 中记录的签名，不代表本轮已经重新向 RPC 查询：

| 角色 | 钱包（前缀） | 交易签名 |
| --- | --- | --- |
| 创建 | `78wF7WAi...` | `4ziGdYrysFAXNkxgsjwPh9nhevDgoNZKm3T2q9j7D14YWZ1mbb7zCYGyBTkthrmKtLshxFgQ63MqpBxJ7Ecbj48x` |
| 首批买入 | `2AqFJzcg...` | `Zspqx61MdabA2r5g78i1c1u66ofFBoU5Tz549A2NyACinC79oJ2NxFSgiEdcZZ4731Bpykcyyt2Bi4K7FhuJySS` |
| 首批买入 | `9yxmCNwZ...` | `55ZLsiuEKNqNUqhi5mDaTkynAacPG5LwRs7YxG97SNYxSf6N3MCNW8LHm3T8CrAhjW76BUY996QdunvkuhoiP58Y` |
| 首批买入 | `2wHHnAmd...` | `5sPKJDzbhAAzhmyeC7BkWGM1eJjezyUHBDcCvEwe4t8eaWGG37ksFqzEJn1jckq15jV3cAL4cC2dCLrHZ3SCsqMZ` |
| 首批买入 | `22vL22Pc...` | `3tKPXxhiH4MDxXnQaXEsq8nJnh6R81bHPnNiQQFbndTTDgffDhkSbTMhh82ZpiQrh7LVFUNaZpV2LVqAJftC8CSk` |
| 首次转移 | `2AqFJzcg...` | `6rByjVMZH8Ggy4Deh86cvDKtzHGqVayHKkFWrPcxZtHmp7S42vixbz1hWr9b13TrooURBu9sCnbf8C4u3rucyry` |
| 首次转移 | `9yxmCNwZ...` | `51hwM1aiSkVVDisq7GYGMANjx5LyQG4zVH36j91j44t3Dqcv5HKAHMxV8DxhQt7obfnZm7vfVPmRcVc32ngKmgwm` |
| 首次转移 | `2wHHnAmd...` | `4iRbhcbjxZiTcByXgnRpwZkM8W4t1nRn6L9WQCdBiPyeSzTk8C73Pg8fUyR1Tpwb9pf37VhYJs1DTwwXhUm92qZg` |
| 首次转移 | `22vL22Pc...` | `LM6X8n4ZWaVuZk985Hr5AxrV288sUdPJHv83cXSvRkJrW4pZC1sqoB893SXmE5TWiQW4jDsSa86LNn6vATKdt1b` |
| 外部首次记录的买入 | 脱敏记录，签名可用 | `6FGfTfSf9oYJ9CyWmVwCMNgqEentJUQjvuuzGmu4jsxLwWv1dHonGtXD2DUUyYd7ojcEvVdZjCJE2iXyYrZeYoQ` |

三个 Token 接收 owner 地址：
- `8uSfX74yDSvq2L8TjM6sj86mnYziqmJCGQsLMLzk4vTH`
- `eUrS4Faom5MmRbaDK7y99yXADvUbUvxEd233T7jNMy9`
- `5Xbhacwcttq3VwwNxbvPE5DC2vAFVPuvdZnedumE9qY7`

注：以上收款 owner 与其 Token Account 的关联，仍以重新读取完整交易 `preTokenBalances`、`postTokenBalances` 及指令事实为最终验证门槛。
