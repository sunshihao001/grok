---
name: solana-meme-monitor
description: Read-only, source-linked Solana Meme snapshot monitoring, with freshness checks and evidence-based uncertainty reporting.
---

# Skill — observe, compare, report

**When:** one-time real observation with a verified source, or a human-approved Grok Routine. **Inputs:** token mint, reviewed repo/rules, normalized JSON source with schema_version, chain, token_address, observed_at, mode, source, metrics, optional events; Python 3.11+.

1. Verify source, clock, schema and field units. If invoking GMGN, run only the read-only collector: PYTHONPATH=src python -m solana_meme_os.gmgn_collect --address MINT. It currently leaves metrics empty until validated mappings exist.
2. Run PYTHONPATH=src python -m solana_meme_os.monitor --input OBSERVATION_PATH --state-dir .runtime. The --allow-fixture option is only for explicit demonstrations.
3. Explain change relative to prior observation, rule version, underlying source link, raw value, missing fields, contradictory evidence and limitations. Preserve state and JSONL run evidence.
4. On invalid, stale or missing inputs or unavailable login, stop and report error. Never fabricate numbers or classify hypotheses as confirmed identities.

**Validation:** PYTHONPATH=src python -m unittest discover -s tests -v. All code here is read-only; the actual Grok Routine and any production deployment require separate human review and live-source testing. No trade or transaction actions.

## Expert knowledge is required, not optional

After Step 2, read `knowledge.interpretation_candidates` from the monitor JSON. These are **candidate conceptual lenses**, not conclusions. For each alert, explain the actual measured change, what the proposed mechanism would imply, what other mechanisms could also produce it, and which missing source datum would best distinguish them. If an alert is unsupported by required evidence, say UNKNOWN and avoid upgrading risk status. See `skills/solana-meme-knowledge/SKILL.md`.
