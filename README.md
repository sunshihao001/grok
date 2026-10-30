# Solana Meme Workflow OS — GPT 研发 / GitHub 真源 / Grok 云端运行

**当前状态：P0 离线可运行原型；尚未验证真实 Grok 云电脑统一入口和实时链上监控。**

> [**2026-10-30 项目基线与认知统一（权威入口）**](docs/project-baseline-2026-10-30.md) · [现行执行清单](docs/next-steps.md) · [机器可读里程碑](design/delivery-roadmap.v1.json) · [GPT→Grok 交付方式](docs/gpt-build-grok-run.md)

## 目标与职责

项目目标：围绕 Solana Meme 跟单与链上结构，研究可证伪、可复算、最终有机会在真实执行成本下捕获的正净期望信号，建设**只读/Paper-Only** 研究与监控系统。

- **GPT**：主要负责研究、知识整理、程序开发、Skill、测试、修复及版本候选。
- **GitHub**：保存已审查源码/知识/实验协议及固定提交；当前主要工作在 [Draft PR #5](https://github.com/sunshihao001/grok/pull/5)。
- **Grok 云电脑**：初期一个 Operator Bot 即可；负责运行固定提交的已有程序并回传 JSON/错误，而不是重写代码。
- **用户**：批准云电脑访问、外部安装/收费和最终冻结监控规则。

B01–B07 是七个**逻辑专业职责**，不是必须先建立七个云端 Bot。C0–C4 是按需知识课程，不是运行已完成 Python 程序的前置要求。详见 [Bot 架构](BOTS.md) 和 [知识分层](knowledge/system/README.md)。

## 已经拥有的资产与实际限制

| 资产 | 当前范围 | 不能证明 |
|---|---|---|
| 专业知识 | L0–L7 / D01–D12 / F0–F6；15 历史卡、21 快照、21 来源索引 | 原始链上数据已验证，或历史经验有正净收益 |
| 工具与 Skill | 7 个 Bot 角色档案、11 个仓库 SKILL.md 模板 | Grok App 已创建并启用这些 Bot/Skill |
| Python | 知识/研究选择、结构交接、as-of 审计、SQLite 队列、OKX 离线解析、模拟监控、统一入口 | OKX/RPC 真实接入、经济实证、B07 长期运行 |
| 工程验证 | 审计基线提交 `f8cf6a376905e163ed8e51bf8f922e3127c1931f` 两项 GitHub CI success / 117 unittest 通过 | 实际 Grok 云电脑成功运行该版本 |

本文件不声称当前工作分支的每个新提交都经过上述相同测试；发布前必须以**最终具体 SHA** 核查 CI。PR 仍为 Draft，未合并 main。

## 当前唯一标准启动方式（仅在获准云电脑与固定审阅提交上）

首次在**空白、可使用的**工作目录：

~~~bash
git clone https://github.com/sunshihao001/grok.git /workspace/grok
cd /workspace/grok
git fetch origin design/knowledge-system-v1
git checkout --detach FULL_REVIEWED_SHA
python3 scripts/grok_operator.py --expected-sha FULL_REVIEWED_SHA demo
~~~

将 `FULL_REVIEWED_SHA` 替换为 GPT 提供且经过审查的完整 40 位提交。若目录已存在，先检查工作树与运行中任务，不能强制覆盖。参见 [Grok 交付手册](docs/gpt-build-grok-run.md)。

**当前 demo 只用合成/已保存数据**：知识审计、unit tests、B01/B02/B05 SQLite 合成交接、OKX 离线 JSON、Monitor fixture 回放。它不安装 OKX、不进行实时网络采集、不收费、不下单、不签名、不启动 Routine。成功输出不是市场策略验证。

## 真实数据、知识来源与安全限制

- Solana 原始 RPC 与 [OKX OnchainOS](https://github.com/okx/onchainos-skills) 是下一阶段的**待授权只读来源**，目前没有可信 K2 实时适配器。OKX Market API 可能在既有账户收费授权下产生 x402 支付副作用；请看 [OKX 源码审查](docs/okx-onchainos-runtime-review.md)。
- GMGN 因充值门槛暂停作为项目必需入口；`gmgn_collect.py` 只保留旧原型。
- 历史来源：[Hermes 研究](https://github.com/sunshihao001/-) · [meme- 理论](https://github.com/sunshihao001/meme-) · [qb- 旧工具](https://github.com/sunshihao001/qb-) · [外部反证研究](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over)。只迁移可追溯知识，**不**迁移 Hermes 运行时或未经验证的阈值。
- Phase 1 禁止真钱下单、私钥、签名、交易广播、自动付款、从研发队列自动发布规则。`rules/monitor.v0.json` 的阈值是实验样例，不是正式冻结规则。

## 文档治理

[项目基线](docs/project-baseline-2026-10-30.md) 解释所有知识轴、保留/废弃方案、真实阻塞和 S0–S5 路线；[现行执行清单](docs/next-steps.md) 只记录下一阶段需要做什么。旧 README 与历史累计待办保存在 [docs/archive/](docs/archive/README-pre-consolidation-2026-10-30.md) 和 [历史待办](docs/archive/next-steps-pre-consolidation-2026-10-30.md)，不再作为运行指令。
