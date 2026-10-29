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
