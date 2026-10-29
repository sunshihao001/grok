# Grok Routine setup draft — NOT RUNNING

In the Grok app, after source and Skill verification, message the **Monitor Bot**:

> Create a **paused** draft Routine for Solana Meme observation; do not enable until I approve. Suggested starting cadence is every 30 minutes, subject to source limits and my local time zone. Monitor Bot is the sole owner. Use the solana-meme-monitor Skill and reviewed code in sunshihao001/grok. Only scan approved token mints with verified read-only data. Check field units, freshness and source authenticity. On each run report observed differences, counterevidence, missing fields and a source-linked audit trail to this Bot conversation. If GMGN mappings, login or fresh data are missing, report UNAVAILABLE and stop. Avoid duplicate notifications. Never place orders, swap, sign, broadcast, access secrets, alter active rules or contact third parties. Test once with safe data and report the result before I activate this Routine.

This Markdown is only an operator instruction. GitHub commits do not create a Grok Routine. See https://docs.x.ai/grok-bot/skills-routines-and-automations.

## Required knowledge handoff

Monitor must consult `knowledge/catalog.v1.json` and use `knowledge.interpretation_candidates` returned by the monitor to guide **source verification and competing explanations**. This knowledge is not proof that an event indicates rug/control/insider activity. On an unknown question, flag a research gap for a development Bot; do not automatically change active rules.
