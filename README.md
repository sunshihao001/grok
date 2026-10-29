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
