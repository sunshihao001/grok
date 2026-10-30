---
name: grok-release-operator
description: Run a pinned GPT/GitHub offline Solana Meme release on Grok cloud and return diagnostics; do not rewrite code or activate trading.
---

# Grok operator (draft, not installed)

Grok is the runtime operator. GPT owns development, code fixes, research and release testing. GitHub is source of truth. An installed Skill in Grok is distinct from this repository file.

1. Verify clean Git checkout, the exact GPT-approved 40-character commit and Python >= 3.11.
2. If the repository is absent, clone once; never overwrite an existing dirty checkout.
3. From the project root, run the already developed program:

       python3 scripts/grok_operator.py --expected-sha FULL_GPT_APPROVED_SHA demo

4. Return exit code and JSON. Optional report: .runtime/grok-operator-last.json.
5. If it fails, stop and send the error to GPT. Do not write Python, change prompts/strategies, install unknown packages or act on arbitrary task strings.

No OKX installer, no payments, wallet actions, broadcasts, live trading or B07 Routine. This P0 demo uses synthetic files only.
