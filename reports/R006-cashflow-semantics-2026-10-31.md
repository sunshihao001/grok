# R006｜现金流业务语义与专家知识反证的交付记录（2026-10-31）

## 1. 本轮为什么改写 R005

Cross-project 比较发现：CyberLeek 所取的外/内层 System Transfer 能证明**直接转账**，但不能独自覆盖 SPL Token `CloseAccount` 及 Wrapped SOL 解包、LP 撤出等所有 SOL 收款来源。Solana 官方说明 Token CloseAccount 把其 Token Account 的 lamports 送至指定 destination。不能仅凭余额最大净减认定 sender；也不能只因找不到 System Transfer 就认定没有收到 SOL。

已在 [R005](../knowledge/research/R005-crossproject-funder-semantics-v1.md) 加反证修正，并形成 [R006 专题](../knowledge/research/R006-sol-receipt-economic-semantics-v1.md)。

## 2. 对固定版本历史真实**派生表**的独立统计复算

锁定来源 `sunshihao001/Why-Solana-Memecoins-Are-Over@9a7ad51d56328e91e67e3f531d6744307d0ee68b/data/trace_h2w6/e2_funding_h2w6gm6jz.json`。通过 GitHub Connector 读取完整 JSON，并对 `wallets[].inflows[]` 按 source/type/nature 汇总，而不是直接复制 README：

- 共 **40 个钱包**；**21 个**追到 genesis、**19 个**未追到；**34 个**覆盖 prebuy window、**6 个**未覆盖。
- **905 条**派生正向 SOL 变化记录：`financement` **61 条**，`produit_de_vente` **844 条**。
- `financement` 中 **53** 条 `SYSTEM_PROGRAM|TRANSFER`，另 **8** 条为 4 Meteora `REMOVE_LIQUIDITY_BY_RANGE`、3 Magic Eden `NFT_GLOBAL_BID_CANCELLED/WITHDRAW`、1 Mayan Swift Bridge `SET_AUCTION_WINNER`。
- `produit_de_vente` 中 **839** 条的源 `tx_type=SWAP`、**5** 条不是（3 `CLOSE_ACCOUNT`、1 `INITIALIZE_ACCOUNT`、1 `TRANSFER`）。
- `n_debited_accounts=1` **904** 条，`=2` **1** 条。一个负余额候选仍不能自动确认经济付款者。
- 对全部原表记录以钱包/签名/时间阶段/分类/来源/金额组成可观察键检查，未见完全重复键；源不含完整 instruction path，未来不能据此默认有确定交易内去重能力。

生成脚本 `etape2_financement.py` 若钱包同笔交易存在 Token 负向变化便给 `produit_de_vente` 标签，否则根据 `type` 与负余额候选给 `financement`。这是公开研究的**业务启发式标签**，并不是本轮新获取的 Solana RPC 事实；“非 SWAP 主类型”同样不自动说明分类错误，可能是复合交易。

## 3. 真实运行与提交验证

- 只读模块 `src/solana_meme_os/cashflow_semantics.py` 在离线、合成输入中实际运行。
- **6 项 Python unittest 全部通过**；在隔离本地 `src/solana_meme_os` 包布局下使用 `PYTHONPATH=src` 再次执行成功。
- GitHub 上传后复读文件，模块 Git Blob SHA `bcc5ab43c3dfc16099d8d0e9762492e28c339e3a`、测试 Git Blob SHA `c66202040b9e2b82f8a785603c8ef9a1debded8f` 与本地**实际执行**的源码完全一致。
- 新增专家连接 L39 `chain→graph`、L40 `data→statistics`，当前 **40 条专家交接、17 类专业能力**均有关联；按需原始来源现 **30 条**，外部原始方法索引 **13 条**。
- 全部源 ID/专家 ID/交接 ID 重新检查：**零悬空引用**。主分支 GitHub SHA 维持 `fa10e491c0692eaa9f9b1538b1fab0d9e9fc170a`。

## 4. 未完成与下一条可证伪动作

- **没做** 40 钱包逐签名原始 RPC 重放、`CloseAccount` 的具体 lamport 去向验证或原始支付者确认；不能以 905 条派生表证明真实收入、同一操盘主体或市场净收益。
- R006 Python CLI 没有直接跑完整 535K 的源 JSON（当前本地执行容器无 GitHub DNS），但基于 GitHub Connector 读取源表的实际 JS 统计已运行。
- 之前 M2、expert_router 等模块的全部 Python 测试**并未因此自动通过**；仅 R006 这 6 项是本轮实测。
- 下一项独立验证应选择原记录中 `n_debited_accounts=2`、`financement` 非 System 的几笔以及 `CLOSE_ACCOUNT` 三笔，按签名取得 `getTransaction(jsonParsed)`，对外/内指令、WSOL 账户和 lamport 前后状态做守恒/归因核查，再评估是否改变跨钱包资金图和正常基准。

**认知成果**：在“链上事件→钱包群体→经济网络→正常基准”的交接中，事件的事实、执行程序的对价、业务标签和经济身份须四层分离，并允许新的链上证据推翻旧有专家解释。
