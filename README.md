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
