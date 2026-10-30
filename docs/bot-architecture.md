> **历史架构参考**：本文件对“由 Grok 开发 Bot 实际写代码”的设想已被 [当前项目基线](project-baseline-2026-10-30.md) 更新。现阶段由 GPT 完成代码与测试，Grok 只执行固定版本；B01–B07 仍可用作专业职责划分。

# Bot Architecture Details

## Shared Computer

All Grok Bots share the user's cloud computer. Files in this repo are the source of truth for rules and skills.

## Iteration Loop

1. Dev Bot proposes change (new rule, schema tweak, fixture).
2. Another Dev Bot or human reviews.
3. Merge to main or tag as frozen.
4. Monitor Bot reloads frozen rules on next run.

## State & Artifacts

- Per-run state: `state/runs/<token>/phase_state.json`
- Reports: `reports/<date-or-task>/`
- Frozen rules: `rules/frozen/` (created on freeze)

## Monitoring Bot Interface

Expected entry points (to be implemented):
- `/sol <CA>` style command
- Scheduled scan of GMGN trending / trenches
- Output: structured JSON + human summary

Implementation of the actual monitoring logic is the job of the Dev Bots + final Monitor Bot.

## Seven-role update (V1.1)

The authoritative Bot split is [BOTS.md](../BOTS.md): B01–B06 on-demand development, B07 one read-only Monitor. The D01–D12 ontology and F0–F6 validation gates are not twelve or seven Bot instances. Parallel Bot tasks require isolated branches/directories and shared state locking; all Bot screens still share a cloud computer and credentials. Bot roles do not provide security isolation.
