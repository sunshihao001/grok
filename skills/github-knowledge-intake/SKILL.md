---
name: github-knowledge-intake
description: Load a reviewed, role-scoped Solana Meme learning unit from a pinned GitHub checkout, test understanding and report evidence-backed feedback. Never change trading rules.
---

# GitHub knowledge intake — Grok Bot draft skill

**Status: repository template only, not installed in Grok. Paper-Only.**

## When to use

A user requests a new staged GPT research/knowledge lesson after a reviewed repository change. The one authoritative version is the pinned Git checkout, **not** ChatGPT dialogue, copied snippets or Bot memory.

## Required input

- Repository: `sunshihao001/grok`.
- Explicit full Git SHA (40 hexadecimal characters), not a moving `main` or PR branch name; for the first trial it may be the current reviewed draft commit *for preview only*.
- Learner Bot ID B01–B06 and learning depth C0–C4.
- Read-only access to the GitHub repository and terminal, if available.

## Process

1. Check the requested commit exists and the working directory matches it: `git rev-parse HEAD`. If not, do not claim the lesson was read.
2. Read `AGENTS.md`, `knowledge/transfer/README.md`, and `knowledge/transfer/curriculum.v1.json`. Do not import all upstream repositories into context.
3. Run `PYTHONPATH=src python3 -m solana_meme_os.knowledge_delivery --audit`.
4. Run `PYTHONPATH=src python3 -m solana_meme_os.knowledge_delivery --bot B01 --through C1` (replace values with actual Bot role/depth). The default command includes **only approved_for_study** material. If a human explicitly asks to evaluate a draft, add `--preview-drafts` and keep the result draft-only.
5. For each selected lesson, open its knowledge file and the pinned checkout's authority_paths, inspect any competing source and read the questions in `study_checks`.
6. Answer the study checks using your own reasoning. Include a negative case and a clear example of missing evidence, without fabricating chain values.
7. Return a versioned `knowledge/transfer/feedback-template.json`-shaped reply with verified repository SHA, read paths, answered questions, confusion and measured test results. You may suggest new knowledge or skill work, but must **not** mark your own learning passed or promote market rules.
8. Human/GPT reviewer evaluates the reply; only after review may a lesson or Skill change be proposed through a GitHub PR. Not a Monitor release.

## Validation and boundaries

- No source or permission: return `SOURCE_UNAVAILABLE`.
- No approved learning units: return `NO_APPROVED_LESSON`, not a market conclusion.
- An unreviewed/draft module remains preview-only even if you answer all questions correctly.
- A lesson contains *research methods*; an external paper or past observation is not locally verified market evidence.
- No private key, wallet access, swaps, signing, broadcast or rule self-promotion.
- GitHub branch changes and Grok UI private-skill creation are separate actions. Test manually once before saving the workflow as a private Skill or building a Routine.
