# R006｜SOL 收益、外部注资与 Token 账户关闭：跨源码反证和真实派生数据审计 V1.0

- 日期：2026-10-31
- 状态：**已独立读取、按代码规则核对公开派生表与源码；未独立从 Solana RPC 逐交易重放**
- 研究目标：从“资金来源 → 钱包角色 → 经济网络 → 正常基准”中识别**事件语义被不恰当扩大**的地方，并改正上一轮 R005 以直接 System Transfer 作为唯一确认路径的过窄表述。
- 关联程序：[`src/solana_meme_os/cashflow_semantics.py`](../../src/solana_meme_os/cashflow_semantics.py)，研究性质、只读、只审计**上游派生记录标签**；不识别真实操作者或执行交易。
- 关联测试：[`tests/test_cashflow_semantics.py`](../../tests/test_cashflow_semantics.py)。本轮在隔离本地 Python 环境**实际执行 6 项合成单元测试，全通过**；之后通过 Git Blob SHA 比对确认上传的两个文件与本地运行的版本完全一致；此结果**不是**对 40 钱包数据完成 Python RPC 实盘复核。

## 1. 新的知识矛盾来自三个不同项目

**A｜CyberLeek：** [`scripts/verify.py`](https://github.com/xorextrace/cyberleek-onchain/blob/283bec233a6c24849799da6e051e91689a0f187a/scripts/verify.py) 遍历 outer/inner 指令寻找 System Program 的 `parsed.type=transfer`。这对确认特定**直接 SOL 转账**是有明确归属的事实方法，不能被误写为“识别所有 SOL 流入”。

**B｜solana-holder-clusters：** [`src/funders.ts`](https://github.com/jayrabol/solana-holder-clusters/blob/a75a72965479a7b715b041148803d8004fe25079/src/funders.ts) 选择最早可见交易的最大 SOL 净亏账户作为 first funder；但在一笔交易中，余额差无法单独确定经济支付路径。没有拿到真实早期历史时还返回 null；[下游 `clusters.ts`](https://github.com/jayrabol/solana-holder-clusters/blob/a75a72965479a7b715b041148803d8004fe25079/src/clusters.ts) 却将 null 计入 independent，进一步损害正常基准。

**C｜原 Why-Solana 研究：** [`lib_trace.py`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/trace_h2w6/lib_trace.py) 记载：经 Wrapped SOL/Token Account 关闭返回 lamports 的情形，可能无 System Transfer，但账户余额仍改变；故使用 `accountData[].nativeBalanceChange` 和明确的历史分页覆盖标志。

**官方反证：** [Solana Close Token Account](https://solana.com/docs/tokens/basics/close-account) 明确：SPL Token `CloseAccount` 会把 Token Account 持有的 lamports 转给指定 destination。Wrapped SOL 可以在有余额时关闭并释放底层 SOL，发起者或账户的 close authority 不必是该 SOL 最初的经济出资人。因此“没有 System Transfer”不能推导“没有 SOL 进入”，而“Token CloseAccount 给了地址 SOL”不能推导“close authority 就是经济出资人”。

**正确推理不应在两种算法之间二选一**：Solana 指令路径核实动作类别；资产余额变化核实账户的净变化；二者结合才能判断资金事件的经济含义，且需保留无法解释的残差和原始权益归属的未知状态。若直接把最大负余额账户当“首次 funder”，可能错配；若只统计 System Transfer，又可能漏掉 Token close、LP 退出或其他经济来源。

## 2. 对原仓库的一段实际历史资料进行独立数量核对

冻结案例：Mint `FNqJtYs7rsP1H9GXWTtc5VnDoL2GhXEUKhYN46EEpump`，代号 `h2w6gm6jz`，原研究创建日 `2024-12-13`。

**原始研究源：**
- [`data/trace_h2w6/e2_funding_h2w6gm6jz.json`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/trace_h2w6/e2_funding_h2w6gm6jz.json)
- [`data/trace_h2w6/etape2_financement.py`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/trace_h2w6/etape2_financement.py)
- [`data/trace_h2w6/lib_trace.py`](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over/blob/9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/trace_h2w6/lib_trace.py)

对该 JSON 中每个钱包的 `inflows[]` 进行分组计数，检查 `nature / tx_source / tx_type / n_debited_accounts`：

| 指标 | 实际公开派生表中的数量 | 正确理解 |
|---|---:|---|
| 分析钱包 | 40 | 已选择的研究样本，不能代表全部发币 |
| 钱包起点历史覆盖 | 21 | 21/40=52.5%；**19/40 未达到起点** |
| 买入前 21 天窗口覆盖 | 34 | 34/40=85%；**6/40 无足够覆盖，不能报告无前期资金** |
| 累计 `inflows[]` 条目 | 905 | 是来源报告的正向 SOL 变化记录，不是 905 笔独立外部资助 |
| `nature=financement` | 61 | 研究脚本认为是“非出售所得”的正向变化；不能都称直接注资 |
| `nature=produit_de_vente` | 844 | 原脚本以 Token 负向变化判定“出售所得”；不能都视为已独立解码的 Swap |
| `financement` 且 `tx_source=SYSTEM_PROGRAM` | 53 | 源**业务类型**为 System Transfer；仍非本轮独立 RPC 重放 |
| `financement` 且其他程序来源 | 8 | 4 Meteora 撤流动性、3 Magic Eden（Bid Cancel/Withdraw）、1 Mayan Bridge |
| `produit_de_vente` 且 `tx_type=SWAP` | 839 | 469 Pump Fun、367 Raydium、3 Jupiter |
| `produit_de_vente` 且其他 `tx_type` | 5 | 其中 3 Token `CLOSE_ACCOUNT`、1 `INITIALIZE_ACCOUNT`、1 System `TRANSFER` |
| 来源记录中 `n_debited_accounts=1` | 904 | 余额变动视角下仅一个来源候选，不等于确认真正经济出资方 |
| 来源记录中 `n_debited_accounts=2` | 1 | 多来源候选，尤其不能把 `srcs[0]` 当作唯一支付者 |

已抽取可追溯样本：
- Meteora 相关研究记录请以源表 `inflows[].signature` 字段为准，本轮没有从 RPC 重新核验该签名。
- `produit_de_vente|SOLANA_PROGRAM_LIBRARY|CLOSE_ACCOUNT`：原始表存在 3 条；这是需要同时查 Token 余额、Token Program 和 SOL 余额的业务混合事件，**不能直接判为错分类**。

> **严格修正：** 取证用例中的签名应从锁定 JSON 原文直接输出，不应依赖人工手录。本研究文档主要提供路径、统计和字段级重算，用户可直接运行附带的只读程序输出待复核签名。任何尚未 RPC 核验的签名只作为后续调查目标。

### 产生这些类别的实际代码

`etape2_financement.py` 的 `token_sold(tx,wallet)` 规则只要同笔交易 `tokenBalanceChanges` 存在该钱包 Token 负向变化，就返回 True；随后把钱包的正向 SOL 净变化标 `produit_de_vente`。若没有识别到 Token 减少，而交易 `type=TRANSFER` 或存在负余额候选，则标 `financement`。

这个方法的目标是避免把机器人卖 Token 得到的 SOL 误算成批量注资；**方向正确但存在语义边界**：
- Token 减少可能是转移、销毁、LP 操作或与出售并存的复杂交易，不自动证明获得 SOL 的原因是卖出；
- `tx_type` 可能仅是供应商对整笔交易的主事件标签，不等于每一条内层指令；
- `srcs[0]` 是同笔交易最大负向余额候选，不等于全部真实资金边；
- 对实际交易进行业务归因必须把 **Token 变化、SOL 变化、外/内指令和池子状态**一同解释。

**这不是发现“原研究 844 条都是错的”**。它说明真实数据分类需要比“有 Token 减少/没有 Token 减少”更精细的机制分解。

## 3. 跨专家连接新增的两项明确职责

**L39｜Solana 执行专家 → 资金图谱专家：多程序 SOL 收入来源分解**

传递带签名与指令路径的 `DIRECT_SYSTEM_TRANSFER`、`TOKEN_CLOSE_ACCOUNT_RECEIPT`、`PROGRAM_LP_WITHDRAWAL`、`BRIDGE_OR_EXTERNAL_RECEIPT`、`UNEXPLAINED_BALANCE_DELTA`。多种事件可同笔共存；记录每类的原始金额、已知接收账户、未知经济源、费用/租金/WSOL 变动。不要把全部分类塞进单一 first funder 字段。

**L40｜数据法证专家 → 统计基准专家：业务标签与历史覆盖的误差传播**

传递 `genesis_reached`、`prebuy_window_reached`、`tx_source`、`nature`、`tx_type` 的适用限制和数量/分母。正常与异常基准不能把没看到起点的 19 个钱包当成“没有出生资金”，不能把 61 条 `financement` 都默认为直接注资，也不能把 844 条 `produit_de_vente` 全部当作已核验 Swap。

这两个知识增量来自**真实跨项目方法冲突和本次源表复算**，不是抽象增加两个专家角色。

## 4. 已可用于独立复算的离线程序

在 Grok 仓库根目录，先从锁定的源路径取得 `e2_funding_h2w6gm6jz.json`：

```bash
PYTHONPATH=src python -m solana_meme_os.cashflow_semantics \
  --input data/e2_funding_h2w6gm6jz.json \
  --output .runtime/R006_cashflow_audit.json
```

这段命令只说明接口要求，`data/` 路径需由用户下载/挂载该来源文件后存在；`.runtime/` 目录也要创建。**本轮没有在完整 Grok 容器执行上述真实 JSON 命令**；源表的 40/21/34/905/61/844/53/8/839/5/904/1 是使用独立 GitHub 原文 JSON 统计复算得到。

本模块的设计保护：
- 不能把缺失 `inflows` 当零；
- 必须完整读取和校验 coverage flags；
- 同一交易/金额看似重复，在没有 instruction index 时**只标记需要原始指令复核，不删除可能真实的重复转账**；
- 任何非 System、非 Swap 的条目是**进一步审查候选**，不是已经证实的错误；
- 不输出独立经济主体、异常概率或收益结论。

## 5. 下一条真正可证伪的实证协议

选择这批样本中优先级较高的真实签名（例如 `financement` 中的 LP 撤出、`produit_de_vente` 中的 `CLOSE_ACCOUNT`，以及 `n_debited_accounts=2` 那笔），独立用 Solana `getTransaction(jsonParsed)` 取得原始/内层指令、WSOL 账户、SOL 前后余额与 Token 余额：

1. 是否有直接 System Transfer？如果没有，是否存在 CloseAccount、LP remove 或其他对价？
2. 账户总增量能分解为哪些实际资产流、费用和租金？残差能否闭合？
3. 原脚本的 `nature` 标签在多大比例上正确反映真实经济行为？
4. 样本中哪些“共同资金源”在改正后消失、分裂或出现新的下游分支？
5. 对照市场里的正常机器人/LP 活动出现同类事件的频率如何？哪些模式在事前能预测市场风险？

不能取得 RPC 时，本轮停止在“真实公开派生表有跨业务语义混合”的结论，不替其编造源链上验证或收益。

**认知升级：** 不止从钱包流向走向资本结构，还要从账户增量分解业务语义，从代码生成过程检查研究标签，从覆盖分母约束统计结论，最后在独立链上复算中让理论接受反证。
