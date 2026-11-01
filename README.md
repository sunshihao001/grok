# Solana Meme Workflow OS — Grok Bot Edition

GMGN 入口 + 钱包情报 + 证据链 + 门控判断的 Solana Meme 研究工作流，适配 Grok Bots 多代理迭代。

原 Hermes 版：https://github.com/sunshihao001/-
理论库：https://github.com/sunshihao001/meme-
GMGN 工具原型：https://github.com/sunshihao001/qb-

## 目标

用多个开发 Bot 迭代规则与技能，最终留一个成品监控 Bot。

Phase 1：只读研究 / 纸面门控，禁止真实交易、私钥、签名、广播。

## 当前产品执行路线（不再扩建架构）

[《四阶段成品交付计划》](docs/product-delivery-plan-v01.md) 为唯一用户功能推进清单：**V0.1真实Mint报告 → V0.2钱包与资金 → V0.3异常监控 → V1.0 Grok自然语言入口**。优先复用OKX/Million等成熟业务程序，只补实际上缺失的接口；当前已真实验证两个Mint的公开池快照，但尚未验证完整Holder/Dev资金报告、持续监控或Grok云端运行。



见 `docs/bot-architecture.md` 与 `BOTS.md`。

## 2026-11-01｜真实V0.1免费多来源Mint报告（已联网验收）

当前首选的**无需Key的只读成品模式**：复用成熟RugCheck的免费缓存Holder/Creator/风险报告，与现有DEX Screener池信息汇总。无钱包签名、交易或自动付款，无须先获得OKX授权。

```bash
PYTHONPATH=src python -m solana_meme_os.mint_v01 EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump --rugcheck
```

2026-11-01在GitHub Actions [真实运行 #41269179918](https://github.com/sunshihao001/grok/actions/runs/41269179918)：返回**5个池、20条RugCheck Top Holder候选、1个Creator候选**，并识别其中**1个Owner与PumpSwap池地址重合**（供应商亦将其标为AMM），不将其当独立聪明钱；19个其他账户仍未独立归类。保存源JSON/SHA/时间与`report.md`/`report.json`；详见[真实验收证据](docs/evidence/v01-real-rugcheck-holder-2026-11-01.md)。此为**公开供应商可能缓存的数据和交叉地址匹配**，不等于已验证完整钱包资金/Dev历史、主网持续监控或Alpha。`--rpc-holders`可单独实验官方公共RPC，但实测遇429，不应作为常态来源。此前`--okx-json`消费已授权数据的功能保持不变，`--rugcheck --okx-json`可将来源隔离并列显示。

## V0.1 单命令读取Mint：优先使用已有OKX结果，免密时可取得公开交易池快照

本次没有重新开发OKX Holder/Dev/Cluster工作流；原`src/solana_meme_os/mint_report.py`继续消费已保存的OKX `token-research` JSON。为解决“只有离线fixture才能运行”的硬缺口，新增**严格独立**的`public_pair_report.py`，只访问DEX Screener官方公开GET`/token-pairs/v1/solana/{mint}`；并新增一条统一命令`mint_v01.py`：

```bash
# 没有OKX已授权结果时：只获取公开、可核查的交易池数据（不提供钱包/Dev结论）
PYTHONPATH=src python -m solana_meme_os.mint_v01 EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump

# 已有授权取得的OKX token-research完整JSON时：优先使用更丰富的原工作流报告
PYTHONPATH=src python -m solana_meme_os.mint_v01 <Mint> --okx-json /path/to/saved_okx_token_research.json

# 合成演示必须显式标记，不能冒充真实市场事实
PYTHONPATH=src python -m solana_meme_os.mint_v01 87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump \
  --okx-json fixtures/okx-documented-field-shapes-synthetic.json --fixture
```

输出默认在`.runtime/mint-v0.1/<Mint>/`下。公开路径保存`provider-raw.json`、`report.md`、`report.json`，保留原始响应SHA256与本地查询时点。只使用固定HTTPS公开GET、无JWT/钱包/私钥/交易/签名/自动付款能力、拒绝HTTP重定向与错误链/地址、请求限时/体积上限。**不调用OKX CLI**，因为其`client.rs`可根据x402支付配置在HTTP 402后生成付款签名；必须单独确认只读授权和支付隔离后才由操作者执行OKX原工具。

### 真实验证与现阶段范围

GitHub CI[公开单Mint对照记录](https://github.com/sunshihao001/grok/actions/runs/41266278500)在2026-11-01于托管运行器真正查询DEX Screener：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`成功返回5个池，`FdKdpz11GsTofLaNiddrhxrsE4APZYSSfLFqQ9YKpump`成功返回7个池；更早对`DezXAZ8z7PnrnRJjz3wXBoRgixCaZhdJ5Bv6PpPB263`返回空列表，程序明确`NO_PAIRS_RETURNED_COVERAGE_UNKNOWN`，**不宣称没有流动性或该Mint不存在**。这些都是**供应商当前数据**，不是Solana RPC独立核验，不能用返回池的`pairCreatedAt`替代Mint创建时点，也不能把报价资产的`priceUsd`当目标Mint价格。

[DEX Screener官方API](https://docs.dexscreener.com/api/reference)声明交易对/Token类接口300请求/分钟；这个额度不是保障持续可用的生产SLA。**公开数据入口只能完成“真实Mint→实际池流动性/成交量/交易次数→带来源的有限报告”**，不能提供Holder/Owner、资金来源、Dev历史、Bundler、已证实Swap/Token库存或盈利信号；这些字段保持`UNKNOWN_NOT_PROVIDED`。**V0.1完整经济分析报告仍未验收**；不能因为增加公开数据接口就将系统升级为持续监控。

## 第一个可运行成品的最短路线｜Mint研究报告（2026-11-01）

**先跑一个Mint，之后才做钱包持续订阅/全市场扫描。** 优先复用OKX OnchainOS现成`token-research`结果，而不是重写它的Token/Holder/Cluster/TopTrader/Dev接口。新增`mint_report.py`是本仓库**无网络、无私钥的最薄JSON报告适配层**，输出Markdown和带原始供应商字段的JSON；源码不调用OKX或支付接口，未知字段保持UNKNOWN、不擅自算控盘/盈利。

先运行可复现**合成演示**（不是链上实测）：

```bash
PYTHONPATH=src python -m solana_meme_os.mint_report \
  --mint 87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump \
  --okx-json fixtures/okx-token-research-demo.json \
  --out-dir .runtime/mint-first-product \
  --fixture
```

查看 `.runtime/mint-first-product/report.md` 和 `report.json`。离线6项单测在当前研究环境通过；GitHub CI运行状态需独立查看。

**真实Mint所需的下一项条件**：在自己授权、禁用自动支付/钱包交易的环境中安装并单独运行官方`onchainos workflow token-research --address <Mint> --chain solana`，将其`{ok:true,data:{workflow:'token-research',...}}`输出保存成JSON，再让上面的脚本改用真实文件并去掉`--fixture`。需记录真实数据获取时点、权限、API扣费和失败；脚本`processed_at`只是文件处理时点，不能当链上或供应商观测时点。**此步骤尚未实测，不能把本地合成演示称为真实成品上线。**

正式目标仍是逐步让这个报告复用现有`monitor.py`与M01获取增量事件；在真实接口字段语义核验前，不将OKX业务字段硬映射进钱包交易/库存计算。Million整套有交易模块耦合及同签名多钱包视角问题，暂不作为第一版运行依赖。

## 安全边界

- 仅 BLOCK / WATCH / PAPER_ONLY / NEED_MORE_DATA
- 禁止真实下单、gmgn-cli swap、私钥访问


## Runnable read-only monitor bootstrap (development PR)

Offline monitor implementation and tests are being added via feature branch. This component accepts **normalized observation JSON**, tracks per-mint state, labels fixtures, detects observed changes and records source-linked history; it is not the original 7-Skill Hermes pipeline. GMGN collector supports token info/security/pool read commands only; raw field/unit mappings are **not yet validated**.

    PYTHONPATH=src python -m unittest discover -s tests -v
    PYTHONPATH=src python -m solana_meme_os.monitor --input fixtures/observation-1.json --allow-fixture --state-dir .runtime/demo
    PYTHONPATH=src python -m solana_meme_os.monitor --input fixtures/observation-2.json --allow-fixture --state-dir .runtime/demo

See docs/sources.md, docs/migration.md, docs/next-steps.md, skills/solana-meme-monitor/SKILL.md and routines/monitor.md. The 0.1.0 rule thresholds are **illustrative**. No scheduled Grok Routine has been created and no live GMGN data has been verified.

## Knowledge layer: preserve expertise without inheriting Hermes runtime

Knowledge is now a first-class, **actively consulted** input: `knowledge/catalog.v1.json` contains 15 source-pinned, status-labelled concepts and methods derived from Hermes business research, meme- theory and qb- field work. Each concept has an applicable context, the evidence needed, counter-explanations and an inference boundary.

Monitor results now include `knowledge.interpretation_candidates` with sources and follow-up checks. This is **question/evidence generation, not an automatic classification of wallet identity or a trading signal**.

Plain-language knowledge routing example:

    PYTHONPATH=src python -m solana_meme_os.knowledge --question "前十持仓突然上升，是不是同源庄家？"

Read `knowledge/README.md`, `knowledge/legacy-audit.md` and `skills/solana-meme-knowledge/SKILL.md`. The engine is a deterministic starter; true Grok language understanding and source discovery still require configuring and testing the actual Grok Bots.

The first preservation wave also includes [21 original Markdown knowledge snapshots](knowledge/legacy-snapshots/README.md) with pinned source commit paths and SHA entries, so the Grok OS can read those sources locally without requiring Hermes or the original repositories to be live.

## On-demand research engine (new)

A 17-source registry now indexes the specialist external study [Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) plus the three legacy repositories **without bulk copying their content**. A runnable question-to-evidence packet helps development Bots choose what to read and highlights missing observational evidence and decision-time leakage.

    PYTHONPATH=src python -m solana_meme_os.research --question "同源钱包可能是交易所公共基础设施吗？"

See [on-demand design](docs/on-demand-research-design.md), [source registry](knowledge/source_index.v1.json), and [usage](knowledge/source-index-README.md). Source previews are opt-in and ephemeral; research packets **are not automated conclusions or validated strategies**. Offline tests do not prove actual Grok Bot expertise.


## P2.4 × P3-M01：跨币行为研究与离线钱包批次原型（实验分支）

[研究、数据契约与误判边界](docs/p24-m01-crossmint-research.md)；
[只读原型使用说明](docs/m01-wallet-batches-skill.md)。

```bash
PYTHONPATH=src python -m solana_meme_os.wallet_batch_monitor --input fixtures/wallet-batches-demo.json --output /tmp/m01-report.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

M01 只接受已经归一化的 `mode=fixture` 事件；不连接RPC、不签名、不广播、不下单。
输出 1/5/15 分钟钱包成员变化、买卖报价资产总量及带来源的描述性候选。
Token Account 与 wallet owner 不可混计，缺失区间记 `INCOMPLETE` 而非零。
这些测试仅覆盖合成事件，不代表真实链上解析或策略验证通过。

## P3-M01 离线原始交易适配器

**2026-10-31**：新增 [raw transaction adapter](src/solana_meme_os/raw_tx_adapter.py)、[对抗性测试](tests/test_raw_tx_adapter.py)、[执行与数据契约](docs/p3-m01-raw-adapter-contract.md)。只读/fixture-only；支持原始 `getTransaction` 形状的 System SOL 顶层转账和 SPL Token/Token-2022 顶层直接转账（含经元数据核对的 v0 已加载地址），**不支持 Pump.fun/Raydium/Jupiter 等 DEX Swap BUY/SELL 解析**。C02/C05 只有数据契约与模拟测试场景，尚未有监控器。

```bash
PYTHONPATH=src python -m solana_meme_os.raw_tx_adapter --input fixtures/raw-solana-transfers-demo.json --output /tmp/m01-normalized.json
PYTHONPATH=src python -m solana_meme_os.wallet_batch_monitor --input /tmp/m01-normalized.json --output /tmp/m01-observed.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

Adapter 对未知或缺少证据的操作采取 fail-closed，Fixture 的完整性声明不等于已证实链上全量覆盖；禁止将合成输出误报为链上事实、真实交易信号或生产完成。

### 2026-11-01｜Mint报告的可读钱包与资金摘要（源码演示已验）

当前`mint_report.py`不再仅按原始JSON逐节打印；`business_summary`从OKX CLI输出中在**有明确字段时**提取`key_wallet_candidates`（钱包地址、供应商持仓量/占比及源JSON路径）、`funding_source_hints`（仅供应商资金来源提示）、`vendor_cluster_statistics`（仅作为异常研究候选）、Dev/Bundle可用性、TopTrader返回样本数量、各字段的`requestTime/time`原始证据及未知项。Markdown先展示可读摘要，完整供应商JSON仍保留于JSON结果的`sections`内。

**必须注意的商业数据契约**：[OKX holder官方文档](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-holder)最多返回100个地址及可选`cursor`，不是完整全链地址历史，默认顺序不保证按余额排名；`fundingSource`无法单独证明同控。独立[Cluster overview接口](https://web3.okx.com/zh-hans/onchainos/dev-docs/market/market-token-cluster-overview)的`holderSameFundSourcePercent`等字段是供应商定义的统计指标，**不能推断几笔真实交易或真实经济控制者**。`requestTime`与`time`只列为原始字段证据，不臆造统一的实时观测时点。

额外**字段契约合成演示**：

```bash
PYTHONPATH=src python -m solana_meme_os.mint_report \
  --mint 87QChghgFr2XBNumi2Tg1MJCWHLqoTTT5KThtnDspump \
  --okx-json fixtures/okx-documented-field-shapes-synthetic.json \
  --out-dir .runtime/mint-evidence-example --fixture
PYTHONPATH=src python -m unittest discover -s tests -v
```

**本轮新增模块12项单测、本地与旧Library版M01联合50项均通过**；不是最新工程PR的完整本地回放，也不是一次真实OKX API调用。合成钱包、资金边、Dev等均只为验证数据管道，任何人都不能把`SYNTHETIC`示例作为实际Mint的链上事件。未在本项目启用API Key、自动支付、钱包、交易或Grok定时运行。
