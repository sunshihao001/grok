# M2 交付记录｜Wallet Burst Observatory 离线原型（2026-10-31）

**目标**：将“以全市场链上事件为起点”转换成第一项可审查的实际代码能力，不再围绕跟单钱包排序。  
**分支**：`docs/cognition-knowledge-conversion-v1`（未触及 `main`、生产规则、Bot 或 Routine）。  
**范围**：规范化事件数据输入的多钱包聚合、关系候选及证据留存。只有研究用途，不交易。

## 已写入

- `src/solana_meme_os/market_observatory.py`：只读研究实现；
- `fixtures/market-observatory-synthetic.json`：**11 条合成事件**、2 个示例 Mint、资金注入、同 Slot 买入、Token 汇总和跨 Mint 重复活动；
- `tests/test_market_observatory.py`：**18 项测试方法**，覆盖单元计数、同交易多指令、去重与冲突、时效边界、滚动跨桶、跨 Mint、同 Slot 无执行顺序时不可推断资金先行、来源缺失/字段精度及防止伪结论；
- `docs/market-observatory-m2-v0.1.md`：CLI、输入/输出 Schema、行为语义和限制；
- 已更新顶层市场监控 Skill、技能目录、市场级建设范围文档。

## 真实完成的功能与不可混淆的含义

本实现对同一**输入事件集合**做全 Mint 和按 Mint 统计，绝不假称拥有全链事件覆盖。它提供：
- 时间窗口的已归一化交易/转账数量、交易地址数量、发送/接收 owner 和精确 SOL / Token 原始整数金额；
- `FUNDING_FANOUT`、`SAME_SLOT_MULTIWALLET_BUY`、`TOKEN_CONSOLIDATION`、`FUNDING_TO_BUY_CANDIDATE`、`CROSS_MINT_FUNDING_REUSE`、`CROSS_MINT_WALLET_ACTIVITY`；
- 来源冲突失败、重复事件去重、同 Slot 缺交易顺序时不推断资金先行、决策时点信息过滤；
- 任何模型输出中 `UNASSESSED_NO_BASELINE`、`UNVERIFIED`、`no_trading=true` 等明确的非结论状态。

特别禁止：从 `same-slot` 自动推断真实 Jito Bundle；从同源自动推断同一经济受益者；从 Token 转出自动推断卖出；从候选事件自动给“异常确定率”或交易信号。

## 验收证据与限制

**已核查：** GitHub 草案分支中源文件、测试、合成数据和文档均存在；并对合成输入前 30 秒做了独立数值核算：
- 总共 11 条合成事件，其中前 30 秒 8 条；
- 前 30 秒 3 笔 SOL 转账，共 **10 SOL**；
- 前 30 秒 3 笔 SWAP_BUY 输入，共 **7.8 SOL**；
- 前 30 秒两笔示意 Token 转账，共 **42 Token**（decimals=2）；
- 前 30 秒 **6 个不同参与地址、3 个不同交易地址**；
- 同一交易签名下多条独立指令应算多事件、一交易；通过测试合同保证，不因重复供应商记录增加独立成交数。

**未核实：** 当前工具执行容器无法从 GitHub 下载该草案分支的 Python 文件，因此没有实际执行 `python -m unittest` 或完整 CLI 烟测。**不能称“18 项测试通过”**。真实 Solana RPC/OKX 采集、独立 Swap 解码和云端 Grok Bot 加载也未完成。

**下一条可验收的工程任务**：完成 M1 只读 Solana RPC/OKX 数据适配器，明确 Instruction/Token Account/SOL 余额单位，采集一段带签名的真实事件并记录首次可得时间；之后用现有 M2 原型作回放，方可继续 M3 钱包资金图和 M4 正常/异常对照基准。

**认知定位**：事实时间窗与资产数额 → 钱包群体与资金网络 → 同类市场行为对照 → 经济机制竞争 → 独立可执行性研究。跟单是最下游可能使用这些能力的一个分支。
