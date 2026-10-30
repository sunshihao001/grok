# Solana Meme Workflow OS — Grok Bot Edition

GMGN 入口 + 钱包情报 + 证据链 + 门控判断的 Solana Meme 研究工作流，适配 Grok Bots 多代理迭代。

原 Hermes 版：https://github.com/sunshihao001/-
理论库：https://github.com/sunshihao001/meme-
GMGN 工具原型：https://github.com/sunshihao001/qb-

## 目标

用多个开发 Bot 迭代规则与技能，最终留一个成品监控 Bot。

Phase 1：只读研究 / 纸面门控，禁止真实交易、私钥、签名、广播。

## 快速开始

见 `docs/bot-architecture.md` 与 `BOTS.md`。

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

## 知识体系架构 V1.0

完整结构：**8 层 / 12 专业领域 / 统一溯源和反证 / 分批迁移**。这里的完整指分类、依赖和验证机制完整，不表示已迁移全部材料或证明交易策略有效。请先读 [知识系统总纲](knowledge/system/README.md)、[研究契约](knowledge/system/RESEARCH.md) 和 [分批迁移](knowledge/system/MIGRATION.md)。监控器仍是 Paper-Only，不会消费未验证的外部研究作为交易规则。

## Bot 架构 V1.1：6 个按需研发 + 1 个只读监控

[Bot 分工](BOTS.md) 与 [机器可读名单](design/bot-roster.v1.json)：B01 知识主控、B02 链上数据、B03 钱包资金、B04 Alpha/交易经济学、B05 证据反证、B06 独立 QA、B07 最终只读监控。12 个知识领域不是 12 个 Bot，七级过滤也不是七个独立 Bot。应用内 Bot 尚未创建。

## 各 Bot 的专业知识初始化包（初步研究）

[七个可复制的角色说明](bots/profiles/B01-chief-knowledge-architect.md)（同目录 B01–B07）、[知识储备清单](knowledge/bot-knowledge-profiles.v1.json)、[Bot 交接契约](docs/bot-knowledge-integration.md) 和 [Grok 云电脑激活步骤](docs/grok-knowledge-installation.md)。按需来源从 17 个增加至 21 个固定提交的入口；不批量复制理论库，也不意味着 Bot 已安装或具备实盘数据。

    PYTHONPATH=src python -m solana_meme_os.bot_knowledge --audit
    PYTHONPATH=src python -m solana_meme_os.bot_knowledge --bot B03 --question "同源资金可能是交易所服务吗"
    PYTHONPATH=src python -m solana_meme_os.bot_knowledge --validate-handoff fixtures/bot-handoff-brief.fixture.json

## GPT → GitHub → Grok：分级知识发布，不靠长对话复制

[知识发布与反馈闭环](docs/gpt-github-grok-knowledge-loop.md) · [课程目录](knowledge/transfer/curriculum.v1.json) · [Grok 取课 Skill 模板](skills/github-knowledge-intake/SKILL.md)。首个 C1-001 证据课程为 **draft**，未获人工审阅发布，不能成为监控规则。

    PYTHONPATH=src python -m solana_meme_os.knowledge_delivery --audit
    PYTHONPATH=src python -m solana_meme_os.knowledge_delivery --bot B01 --through C1 --preview-drafts

## Expert research track: executable wallet alpha (proposed, not reproduced)

[Original expert research memo](research/2026-10-30-executable-copytrade-edge.md) and [preregisterable protocol](knowledge/experiments/executable-edge-protocol.v1.json): distinguish observable actor coordination, time-eligible information, out-of-sample incremental prediction and net-executable outcomes. Four hypotheses H-A/H-B/H-C/H-D are **unproven**. As-of metadata offline checker:

    PYTHONPATH=src python -m solana_meme_os.asof_audit --input fixtures/asof-audit.synthetic.json

New [C2-001 and C3-001 knowledge units](knowledge/transfer/curriculum.v1.json) remain **draft**, build on C1-001 and must not be automatically loaded into B07.

## Local/Grok-cloud executable framework (P0, offline-only)

[Framework deepening](docs/local-runtime-framework.md) · [SQLite task inbox](src/solana_meme_os/runtime_store.py) · [Local/cloud doctor](scripts/grok_cloud_doctor.py) · [Provider capability declaration](design/local-provider-capabilities.v1.json) · [Grok handoff Skill template](skills/local-research-handoff/SKILL.md).

    python3 scripts/grok_cloud_doctor.py --repo . --audits --self-test
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store init
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store submit --input fixtures/bot-handoff-brief.fixture.json
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store claim --bot B02
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store status

The research SQLite queue does not execute its payload, authenticate Grok Bot identity, validate live market evidence or authorize B07 rules.
