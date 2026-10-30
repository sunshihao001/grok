# Skills adapted for Grok Bots

## Planned role-specific skills — currently repository templates

The reusable templates are `solana-meme-knowledge` (existing), `solana-meme-monitor` (existing), and six newly drafted Skills: `research-intake`, `gmgn-readonly-source`, `wallet-funding-forensics`, `alpha-economic-experiment`, `evidence-falsification`, `independent-case-replay`. They are tied to B01–B07 in `knowledge/bot-knowledge-profiles.v1.json`. Do **not** confuse a checked-in SKILL.md with an enabled Grok Bot private skill: configure/enable each explicitly in the Grok UI and test. All Skills are Paper-Only and have no transaction/signing permission.

## GPT/GitHub/Grok learner (draft)

`skills/github-knowledge-intake/SKILL.md` is a proposed **read-only** per-role curriculum loader; it chooses reviewed learning units at a pinned GitHub SHA and returns a structured feedback note. It is **not automatically registered** with Grok, and it never authorizes market findings, Monitor rules or transaction execution. Test a single safe invocation before enabling it as a private Grok Skill.

## Local executable handoff (new template)

local-research-handoff/SKILL.md provides a read-only manual execution recipe for B01–B06 using runtime_store.py. It is not a registered Grok private Skill, does not authenticate the Bot, and is not for B07. Test with one safe fixture on the real cloud computer before any Routine.
