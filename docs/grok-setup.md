> **2026-11-05 当前工作入口调整**：旧六Bot部署步骤仅是可选历史参考，不得作为当前部署前置条件。请优先遵循 [现行准则](../knowledge/system/current-operating-guidance.md)。下面早期的固定Bot/GMGN/阶段/专家/下一轮提示词等内容**只保留为历史研究和方法记录，不再作为默认操作命令**；原研究事实、源码与证据不因本次修正而无效。

# Grok Bot setup — implementation handoff

The existing **BOTS.md** is authoritative for the six roles: Rule Architect, GMGN Data, Wallet Structure, Evidence & Gate, QA / Fixture, and final Meme Monitor. The new bots/04-monitor.md adds the runtime owner's operating instructions; it is not an extra sixth development Bot. These roles are Grok app objects to create later, not processes initialized by this repository.

1. Connect GitHub with least privilege. Development Bots may propose scoped PRs. Only human-approved versions are available to the final Monitor.
2. Create the six Bots described in BOTS.md in the Grok Bot app; assign one owner per handoff. They share one cloud computer, so isolate work by branches and local directories.
3. Clone the repo in the shared cloud computer, install Python 3.11+, and run the offline unit tests from README.
4. Optional GMGN integration: install legitimate read-only gmgn-cli access, capture raw source samples and validate exact units/field mappings. Do not commit secrets or assume this is already working.
5. First test one real-data observation and a second changed observation while verifying the source timestamp, token address, source links, missing fields and duplicate suppression.
6. After a successful one-time test, save skills/solana-meme-monitor/SKILL.md as a Grok private Skill available to final Monitor.
7. Ask Monitor to create a **paused** Routine using routines/monitor.md; verify schedule, time zone, input, output and approval controls in the Grok app, then use its Test feature before enabling.

Never assume a GitHub commit provisions Grok Bots, credentials, Skills or a Routine.
Official: https://docs.x.ai/grok-bot/get-started and https://docs.x.ai/grok-bot/skills-routines-and-automations.
