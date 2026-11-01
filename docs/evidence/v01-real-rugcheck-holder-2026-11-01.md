# V0.1 真实Mint多来源只读报告｜2026-11-01

**验收性质**：GitHub Actions真实联网执行、离线代码CI另行验证；不是fixture，也**不是原始Solana RPC独立复核、完整Dev历史/钱包资金闭环、Grok云端部署或盈利实证**。

- **代码分支**：`research/p24-cross-mint-m01-batch-monitor-20261031`，工程Draft [PR #16](https://github.com/sunshihao001/grok/pull/16)；运行：[GitHub Actions #41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)。
- **完整原始证据**：[运行Artifact](https://github.com/sunshihao001/grok/actions/runs/41269179918/artifacts/13068576712) `one-shot-mint-rugcheck-readonly-20261101`，14天保留。已另行下载ZIP到本次执行容器，读取`mint/report.json`、`mint/report.md`和两份供应商原始JSON；校验供应商原始JSON SHA256与报告记录完全一致。
- **Mint**：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`
- **实际采集时间**：`2026-11-01T03:26:30.595842+00:00`（处理/采集时间，**不是链上各事件的真实发生时点**）。
- **DEX Screener**：一次公开HTTPS GET返回**5个交易池**，数据等级`PUBLIC_PROVIDER_PAIR_SNAPSHOT_UNVERIFIED_ONCHAIN`，raw SHA256见下。
- **RugCheck**：一次公开HTTPS GET `/v1/tokens/{mint}/report`（**无需Key，免费结果可能缓存**），返回 **20条Top Holder Token Account候选**、Creator候选`9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y`、供应商风险和池线索；未返回可用Creator完整历史。`topHolders`来自供应商缓存，**不是同一slot的原子链上状态**。
- **经济语义关键反例**：RugCheck的`root.topHolders[0].owner`为`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`；与DEX Screener`root[0].pairAddress`完全匹配，RugCheck`knownAccounts`又标它为`AMM / Pump Fun AMM`。因此程序**保留该记录但标为基础设施候选**，不能将它当成独立聪明钱/巨鲸。20条中**1条供应商已标AMM/Locker基础设施候选、19条未分类账户候选**；19不等于19个已确认独立人类钱包。
- **跨源匹配**：新版`mint_v01.py`新增`cross_source_pool_owner_matches` 1条，具有两个原始JSON路径和`NOT_HUMAN_WALLET_OR_COMMON_CONTROLLER_PROOF`边界。不能由地址匹配证明所有相关账户实际经济控制权。
- **运行命令**：
  ```bash
  PYTHONPATH=src python -m solana_meme_os.mint_v01 EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump --rugcheck --out-dir .runtime/mint-proof
  ```
  输出包括`report.md`、`report.json`、`dex-provider-raw.json`、`rugcheck-provider-raw.json`。本次`program_exit_code=0`、`source_errors={}`；没有启动OKX CLI、签名、交易或自动付款。

## 数据完整性校验
- `rugcheck-provider-raw.json`：SHA256 `d6baa59b89cbbfc8f4489253e35457415a2e53e8e2076da40179733ba6137054`。
- `dex-provider-raw.json`：SHA256 `a7f941d5f2caca8c9ebff9b908b4a58dfa1009150ed55e986cb222fcd81e4de9`。
- `source_status`：`okx_saved_json=NOT_SUPPLIED`、`solana_public_rpc_token_accounts=NOT_REQUESTED`、`dex_public_pairs=PUBLIC_PROVIDER_PAIR_SNAPSHOT_UNVERIFIED_ONCHAIN`、`rugcheck_public_report=RUGCHECK_CACHED_VENDOR_REPORT_NOT_INDEPENDENTLY_VERIFIED`。

## 尝试失败的第一来源与路线调整

之前同一GitHub Actions运行 [#41268726726](https://github.com/sunshihao001/grok/actions/runs/41268726726) 尝试Solana官方限流公共RPC `getTokenLargestAccounts` 返回`HTTP 429 Too Many Requests`，未获得真实Token Account列表。没有将`429`转换成无Holder、尝试交易或绕过限制；之后转用**已有成熟免费RugCheck缓存报告**。现有`--rpc-holders`保持为按需、公开RPC的研究备选（不应依赖它进行连续运行），正常成品演示推荐`--rugcheck`。

## V0.1 验收与剩余功能

- **真实Mint基础研究报告已可运行**：一次自然Mint输入 → 公开多池和供应商Top Holder/Creator/风险候选 → 交叉匹配基础设施 → 一份可读报告＋真实原始响应。
- **不得升格**：不是独立链上Holder/owner验证；RugCheck free API可能返回旧缓存；不是融资图/Dev系列历史；没有已确认单笔SWAP、连续异常或可跟单Alpha；Grok云电脑S1仍未验收。
- **后续最值任务**：V0.2直接选本次Mint的有来源钱包候选，**先用成熟RugCheck Insider Graph/Million funding/owners能力**获取一条真实资金或群体关系，再以源码/原始引用核查公共服务节点与误归因；仅补最薄的只读对接。OKX `token-research`可在安全授权、无x402自动付款后作为增强来源，不应阻塞现有免费基本成品的继续交付。

**证据等级提醒**：真正可核验的是GitHub runner请求供应商、原始JSON、两源地址相等、程序输出以及相关代码测试；RugCheck标签和风险分不是我们独立复算的链上市场结论。
