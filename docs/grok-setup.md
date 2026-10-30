> **路线修订**：以下“先创建 B01/B02/B05 再扩展所有 Bot”属于较早的多 Bot 部署设想，不是当前最低部署前置。现行路线为 [GPT 开发、Grok 一 Bot 运行](project-baseline-2026-10-30.md)，仅在后续独立 AI 判断产生真实需求时再增加专业 Bot。

# Grok Bot deployment V1.1 — roles not yet created

Follow [BOTS.md](../BOTS.md) and [design/bot-roster.v1.json](../design/bot-roster.v1.json): six development Bots invoked on demand, one final read-only Monitor. A repository commit cannot create Grok Bot objects, cloud skills, credentials or Routines.

1. Create B01 (main coordinator), B02 (chain data) and B05 (independent evidence) in the Grok Bot app. Give them distinct scope, not credentials that are assumed to be isolated.
2. Connect read-only sources, clone the project on the shared cloud computer, run `PYTHONPATH=src python -m unittest discover -s tests -v` and `python -m solana_meme_os.knowledge_system --audit`.
3. Verify real GMGN/raw Solana transaction JSON, time-of-availability, units, missingness and source error reporting. Fixtures never count as real proof.
4. Create B03 (wallet), B04 (Alpha/execution economics), B06 (independent OOS QA). Use separate branches/task dirs. B04 cannot approve its own Alpha.
5. Human-review the versioned evidence/QA release packet before freezing any Monitor rule. Development Bots do not auto-promote rules.
6. Create B07 (final read-only Monitor). Configure its shared Skill and a **paused** Routine, then verify timestamps, alert de-dup, source links and single-writer state before enabling a schedule.

All Bots share a single cloud computer with shared files, sessions and credentials: **Bot separation is not security isolation**. Never store wallet keys on it. No swaps, signing, broadcast or real trades in Phase 1.

Official: https://docs.x.ai/grok-bot/bots ; https://docs.x.ai/grok-bot/computer-and-apps ; https://docs.x.ai/grok-bot/skills-routines-and-automations .
