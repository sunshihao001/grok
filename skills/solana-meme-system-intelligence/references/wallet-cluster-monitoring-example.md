# 全局钱包异动监控：真实来源示范与可检验解释 V1.0

关联主技能：[Solana Meme System Intelligence](../SKILL.md)  
类型：基于公开研究派生数据的示范，**不代表 Grok 实时监控已经运行**。  
时间：2026-10-31。  
来源冻结：`sunshihao001/Why-Solana-Memecoins-Are-Over@9a7ad51d56328e91e67e3f531d6744307d0ee68b`。

## 示例 1｜“4 个钱包同 Slot 买入”如何转换为真正的监控事件？

### 从资料中真实能看到什么

Mint：`87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump`。  
创建 Slot：`429307208`。创建时间：`2026-06-27T20:20:57Z`。

读取研究源文件：
- `data/v03_onchain.json`：四笔买入的地址/签名/Token/SOL；
- `data/v04_slot_order.json`：创建交易 index 312，早期买入 index 313、314、315、316；没有按该研究 BUY 判别规则识别的更早外部买家；
- `data/v07_exit.json`：四个地址首次代币转移距买入 19、19、28、35 秒，归入三个接收 owner。

四个钱包合计 **84.9415 SOL** 买入 **780,464,208.09 Token**，对应研究定义下约 **78.05% 供应量**。首个记录的外部买入价相对四地址总 VWAP 约 **3.805 倍**。

这应该先产生两个不同监控候选，而不是“庄家买入”一个标签：

```text
事件 1：
  SAME_SLOT_MULTIWALLET_BUY
  mint: 87QChghg...
  slot: 429307208
  window: creation_slot
  unique_wallets: 4
  distinct_buy_transactions: 4
  combined_buy_SOL: 84.9415
  bought_token_units: 780464208.09
  tx_positions: 313,314,315,316
  source_quality: SOURCE_DERIVED / not newly RPC-confirmed
  bundle_provenance: UNKNOWN
  coordination_hypothesis: OPEN

事件 2：
  POST_BUY_TOKEN_ROUTING
  origin_wallets: 4
  distinct_reported_token_receivers: 3
  first_transfer_delays_s: 19,19,28,35
  independent_swap_verification: NOT_DONE
  inventory_closed: NO
  beneficiary_identity: UNKNOWN
```

注意：这里的 `POST_BUY_TOKEN_ROUTING` 是派生文件的报告语义。源脚本是使用 Token Account 余额和 SOL 差额启发式分类的，尚需独立指令复核。

### 专家应提出三个竞争解释

**H1：共同运营的创建/执行网络。** 可能使用多地址按照预定顺序取得曲线上的早期库存。独特预测是非公共资金来源、跨 Mint 账户组合复用和库存回收路径具有持续重合。

**H2：共享执行或钱包服务商。** 多个经济主体的交易由同一服务商或公开自动化技术汇集。同样可能出现相邻交易和统一接收，但实体风险敞口不必相同。

**H3：公开发行事件吸引多个独立机器人。** 它们以相近策略在创建 Slot 竞争；同额买入和价格上升部分由绑定曲线本身解释。此时若没有非公共资金和库存路径共享，所谓“同控”的支持会减弱。

**当前判别状态：** 本案例确实具有短时间群体买入和库存路由迹象，但当前材料没有独立证明 Jito Bundle、最终受益人或收益优势。仅由“相邻的四笔”不能排除 H2/H3。

### 正常与异常相对于什么？

要报告其异常性，不能直接说“4 个钱包买入就是异常”，因为取证项目另一项研究的**告警群体本身就是按四个或更多同 Slot 大额买入筛出来的**。

对本例合理的后续比较可以是：
- 同一发行协议、相近交易时段、类似初始流动性与热度；
- 不按“4 钱包同 Slot”预选的发行全集；
- 相同钱包活动数与交易规模条件下，交易连续性、共享非 hub 资金源、跨发行重复对的 null 分布；
- 结果应报告候选数据覆盖和没有被判异常的普通发行数量。

**这里没有上述对照数据的完整运行结果，因此只能报告“群体候选事件”，不能报告独立校准的异常概率。**

## 示例 2｜资金注入 + 批量买入的另一条路径

`economic_mechanics/tables/B_roles.md` 提供一个不同的示例：launch `5AKiLB...`（原文为截断标识，2026-08-21 17:35:43），四个被研究者归为 sniper 的地址，其上游 funder 均列为 `FZNT7J...`，funding to buy 的记录均为约 **1 秒**。

原研究记录每个地址的打款 SOL 分别约 **25.352、30.402、10.202、25.352**；各自买入约 **24.69、25.25、9.88、24.69 SOL**，这是一个“先资助、紧接买入”的短窗口群体候选。

但这些地址和签名在引用表中被截断，单凭表本身无法构造供外部 RPC 查询的精确交易清单。因此：
- **作为机制启发**：一对多 SOL funding → 数个地址迅速买入同一 Mint，值得定义为 `FUNDING_FANOUT + SYNCHRONIZED_BUY` 复合候选；
- **作为完整链上事实**：仍须找到准确上游交易签名与 owner，查共同 funder 是否公共设施；
- **作为所谓操盘证据**：还缺实际受益人归属、反事实正常样本和后续市场库存证据。

这条路径说明要把“哪些钱包何时收到多少 SOL、过多久买入”纳入监控本体，而不是只看代币在什么时候上涨。

## 从两个示例提炼的可迁移能力

- **字段能力**：同一时间窗能精确解释钱包数、TX 数、资金转入金额、买入金额、独立资产数量、Token 去向。
- **时间能力**：创建 Slot 顺序、资金注资时间、各钱包买入时间及 Token 首次转移时间分开报告。
- **图谱能力**：共同资金源、库存接收者和受益实体不是同一类节点；不同假设应有不同证据边。
- **反证能力**：发现共享资金结构前，先看公共服务商、交易所/机器人、同类发行基准。
- **市场解释能力**：把观察到的买盘、库存流与价格/流动性变化联系起来，但不能凭它直接做未来收益预测。
- **审计能力**：不同观察窗口的 Token 余额不守恒时，主动标注 `UNRECONCILED`，不要编造完整卖出。
- **决策能力**：从 `OBSERVED` 到 `ANOMALOUS`、从 `ANOMALOUS` 到 `PAPER_EVALUATION_CANDIDATE` 需要分别不同的测试证据。

## 针对 Grok 的优质预警文本示范

> **钱包群体事件（历史样本）**｜Mint `87QChghg...`，Slot 429307208。四个地址在创建后的连续交易位置买入，共约 84.94 SOL、7.80 亿 Token；约 19–35 秒后，原派生资料记录四次首次转账，涉及三个接收地址。共同控制、Jito Bundle 和最终卖出均未确认。当前更值得调查的是四个地址上游资金路径及接收者实际 Swap，而不是直接认定“庄家已控盘”或输出交易建议。

这个报告的价值在于：**读者知道具体发生了什么、没有证明什么、接下来哪项取证最重要。**

## 原始来源

- [`data/v03_onchain.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v03_onchain.json)
- [`data/v04_slot_order.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v04_slot_order.json)
- [`data/v07_exit.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/v07_exit.json)
- [`economic_mechanics/tables/B_roles.md`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/economic_mechanics/tables/B_roles.md)
- [`coordination_detection/analysis_plan.md`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/coordination_detection/analysis_plan.md)

**认知引导词：** 以真实时序、金额与资金边重建群体行为，在相似背景的正常活动中寻找可反驳的偏离，再探索偏离如何传导至市场。
