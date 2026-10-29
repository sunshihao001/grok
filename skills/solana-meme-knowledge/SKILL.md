---
name: solana-meme-knowledge
description: Select and apply source-pinned Solana Meme domain knowledge to plain-language problems and monitor observations, preserving alternative explanations.
---

# Portable expertise, not Hermes runtime

Inputs: user's plain-language question, new source-linked observation data, knowledge/catalog.v1.json, optional original source refs and read-only research tools.

1. Read `knowledge/README.md` and `knowledge/method.md` first. Inspect the relevant source-pinned cards and read their `snapshot_path` when available (see `knowledge/legacy-snapshots/manifest.json`); use them as hypotheses/method lenses, **not as automatic answers**.
2. Optionally preselect via `PYTHONPATH=src python -m solana_meme_os.knowledge --question "用户原话"`. It uses literal keywords only and is not the final expert selection; retrieve additional concepts if they better match the underlying mechanism.
3. Distinguish observed fact, upstream vendor inference, your hypothesis, counterevidence and unknown. For each hypothesis identify required evidence that would *disprove* it and source timeliness.
4. If a source or field is missing, decide whether additional investigation could change the conclusion; otherwise issue UNKNOWN/STOP and avoid misleading precision.
5. Return a useful conclusion with provenance, alternatives, next observation and limitations. Only a separate verified rule improvement PR can alter Monitor behavior.
6. For new insights create a proposed source-pinned card with failure cases. Do not rewrite source history or treat a bot-generated claim as validated truth.

Prohibitions: No automatic trades, private keys, swap, signing, broadcast or fake live claims. No dependencies on Hermes binaries, /HER_* commands, hooks or fixed local directories. Offline catalog checks do not prove live analytics.

## Full-system knowledge use

Consult `knowledge/system/README.md` and `ontology.v1.json` for cross-domain prerequisites and `knowledge/system/RESEARCH.md` for the structural/predictive/economic separation. New external findings in `research-units.v1.json` are claims for adversarial investigation, never auto-published trading rules. `python -m solana_meme_os.knowledge_system --question "问题"` is only literal domain navigation.
