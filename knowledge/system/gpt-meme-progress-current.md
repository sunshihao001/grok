# Solana Meme｜当前可恢复状态（2026-11-01）

> **当前入口**：[工作准则](current-operating-guidance.md) · [工程产品计划](https://github.com/sunshihao001/grok/blob/research/p24-cross-mint-m01-batch-monitor-20261031/docs/product-delivery-plan-v01.md) · [工程PR #16](https://github.com/sunshihao001/grok/pull/16) · [知识PR #14](https://github.com/sunshihao001/grok/pull/14)。本文件取代历史P2.2/P3-M01研究阶段作为默认恢复点；以前的阶段表、复制提示词、来源审计和研究记录仍可由 Git 历史与现存专题追溯，不是当期执行指令。

## 产品目的
让程序持续观察Solana Meme的Mint、关键钱包、交易/转账、资金与Token库存关系，发现真实异常并提供按需Grok专家研判。只读、可核查；不默认交易、签名或自动付费。AI承担产品统筹、方案取舍与工程整合。

## 已有实绩（非产品全完成）
- **V0.1免费真实Mint基础预览已验收**：`PYTHONPATH=src python -m solana_meme_os.mint_v01 EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump --rugcheck`，工程Draft PR #16，真实[Actions #41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)。
- 本次取得DEX Screener 5池、RugCheck缓存20条Token Account/Holder候选、Creator候选，保存可追溯的原始JSON、时间和哈希；1条Owner与AMM池地址匹配且供应商标AMM；19条仍未分类。并非20个独立聪明钱或链上同slot独立复算。
- Solana公共RPC尝试返回HTTP 429；未拿到所需独立Holder历史。OKX真实完整token-research JSON未验，可能涉及费用/授权；不再阻塞免费V0.2推进。
- 已有`wallet_batch_monitor.py`离线窗口算法和raw adapter部分测试；**没有真实持续事件输入、资金关系验证、Grok云电脑运行或盈利证明**。两个PR仍为Draft，未合并main。

## 下一步：唯一优先产品缺口（可根据实测改变选型）
**V0.2单Mint真实钱包与资金/Token关系**。从本次Mint的有来源候选出发：
1. 检查现成RugCheck insider graph、Million funding/owners/flows或其他已审成熟服务的**实际源码/接口、许可、权限、费用、输入/输出、覆盖和失败行为**；先尝试安全只读业务能力，不能只引用README。
2. 选择一个真实候选地址集合，给出至少一条可复核的资金或Token活动/关系边（源、获取时点、经济语义、不确定性），及至少一个公共设施/未知反例。若安全数据源不可得，记录明确阻碍并比较其他现成方案，不重复实现功能。
3. 成功后将确认的实际事件流接入既有聚合算法，再按需求验连续监控和Grok按需研判；不能因文档或fixture成功跳级宣称可运行。

**既有知识**：原Hermes、qb-、meme-、K0/K1/K2、L0–L7、D01–D12、152知识单元、22专家视角、65参考资产均保留为可选择的知识与来源，不作为强制推进流程。PR #15旧104项仅为历史对照草案。

## 过时指令的处理
不再从历史阶段 P1–P6、P2.2、旧B01-B05顺序、D03-first、FnZero-only或“每轮强制编译知识/固定提示词”自动恢复。相关内容仅在解决当前具体问题或解释历史决策时读取。重大新事实才修正现有知识条目；不要因存量文件庞大而复写一份新架构。

## 存储边界
GitHub提交只更改相应分支；ChatGPT Project附件、Project Instructions、个人Library、账户Memory不会自动修改。未真正写入的位置不得报告“已更新/已记住”。