# KNOW-001｜分批知识接入执行记录

- 日期：2026-10-29
- 范围：Grok 源码分支 `feat/staged-knowledge-intake-001`；源仓只读。
- 状态：首次 CI 因覆盖已有 knowledge API 失败；修复提交已恢复原接口并新增独立 intake 模块，等待复验；**非人工最终接受**。
- 目标：原文不丢失、首包可读取、Bot 产物可见、解释不冒充交易信号。

## 已审查

- Grok 当前监控：离线演示版仅做 `liquidity_usd` / `top10_holder_pct` 差异、事件去重、输入时间校验。
- Hermes 业务工作流：phase0 handoff、缺失数据策略。运行时与本仓不兼容。
- meme 理论库：真源地图、第一控盘区、POC/AVWAP 和反证设计。它们**不能直接作为实时 Solana 策略结论**。
- qb 数据护照：事实/推断/缺失分离；`hermes_harness` 控制平面不迁移。
- 七份精确源引用（main commit + blob sha）均记录于 `knowledge/registry.v0.json`。

## 新增/修改

- 新增：`docs/knowledge-intake.md`、`knowledge/registry.v0.json`、`knowledge/packs/KB-001-evidence-bounds.md`
- 保留原有 `src/solana_meme_os/knowledge.py`、`tests/test_knowledge.py`；新增 `src/solana_meme_os/knowledge_intake.py`、`tests/test_knowledge_intake.py`。
- 原有 `src/solana_meme_os/monitor.py` 的知识卡上下文保持不变；`README.md`、`AGENTS.md`、`skills/solana-meme-monitor/SKILL.md` 补阅读契约。
- **未修改**：任何 GMGN CLI 交易操作、`rules/monitor.v0.json` 的阈值、私钥、线上 Bot/Routine。
- 测试命令：`PYTHONPATH=src python -m unittest discover -s tests -v`。
- 验证结果：以合并请求 CI 为准；不把未观测 CI 写成 PASS。

## 待处理

真实 GMGN 字段单位、Solana 钱包结构历史、跟单延迟与净成本、反例样本、跨 Bot 审查和人工冻结均未完成。先完成本次知识索引质量门控，再进入 KB-002。

## 并行基线冲突处理

PR 首次 CI 暴露 `ImportError: for_observation`：新知识读取逻辑误替换了主分支已有的 15 卡引擎。纠正方式是完全恢复 `knowledge.py`、`monitor.py`、`tests/test_knowledge.py`，独立添加 `knowledge_intake.py` 与测试。禁止将首次 CI 失败标为通过。
