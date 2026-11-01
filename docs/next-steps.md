# 当前唯一工程恢复点｜Solana Meme 只读成品（2026-11-01）

> 当前工程状态以本文件、[产品交付计划](product-delivery-plan-v01.md)、[真实供应商证据](evidence/v01-real-rugcheck-holder-2026-11-01.md)和工程 [Draft PR #16](https://github.com/sunshihao001/grok/pull/16)为准。此文件替换过时的阶段追踪/多版“下一步”堆叠。旧内容可由Git提交历史追溯，**不得从旧段落恢复强制阶段、OKX硬前置或未验收能力**。

## 实际目标
只读：Mint/市场事件→关键钱包→可核查的资金与Token活动/群体关系→持续观察异常→Grok按需专家解释及历史报告。AI负责设计、复用、集成和验收；用户只作需求判断与必要授权。

## 已实测
- `mint_v01.py --rugcheck`：GitHub Actions [#41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)对一个真实Mint取得DEX Screener 5池、RugCheck缓存20条Holder Token Account候选及Creator候选，保存JSON、时间和SHA。
- 程序交叉识别一条Holder owner与AMM池地址重合；其余19条未分类。公开供应商报告可能缓存；不等于独立链上Owner确认、资金群归因或盈利信号。
- 官方公共RPC尝试HTTP 429未完成独立核查；OKX完整token-research真实JSON未验，且存在授权/潜在支付风险。它是增强选项而非V0.2门槛。
- `wallet_batch_monitor.py`和`raw_tx_adapter.py`含离线测试，**尚未接入可持续的真实事件采集**。Grok云电脑S1未验收。PR #16尚未合并main。

## 当前应交付的下一项
**V0.2 一条真实、可追溯的钱包/资金关系**。沿用上述Mint的候选地址，检查可安全使用的RugCheck insider graph、Million funding/owners/flows等完整业务能力：核实源码、API/原始响应、许可、费用、签名及付款风险、数据新鲜度、Token account与owner语义。优先调用原有成熟服务而非开发重复功能。

可验收结果：同一Mint得到一条有来源、时点和方向的钱包资金或Token活动关系（可以是非同控的证据关系）；至少一个公共基础设施/未知/反归因案例；报告未覆盖字段，显示失败和限制；无私钥、签名、自动费用或交易。

如果现有来源无法产生真实关系，保留失败记录并比较更合适的只读现成方案。**不能用合成fixture、README或供应商无出处标签冒充验收。**

## 之后（不是当前强制阶段）
仅当真实事件源可靠时才复用现有1/5/15分钟聚合做连续观察、告警和恢复；之后在Grok真实运行环境验收自然语言命令→取数→专家按需解释→再次查询。需要时按实际证据改变顺序，不因路线图要求而扩建专家体系。

## 有效参考与版本边界
现有Hermes、qb-、meme-、Million、pumpwatch、OKX、Why-Solana（review_only）和知识PR #14保存业务机制与可查来源，按具体缺口调用，不整库迁移。GitHub工程草案、知识草案、ChatGPT Project/Library/账户记忆不是自动同步的相同存储位置。