---
name: solana-meme-monitor
description: Use Grok's terminal to run the reviewed Solana Meme read-only Mint report, inspect provenance-checked evidence, and investigate candidates. Historical normalized monitoring requires independently verified data.
---

# Grok 主 Bot | 现有程序的只读调用与调查

**Current status:** This is a GitHub Skill draft, **not** evidence that a Grok Bot has run. Source repo: `sunshihao001/grok`, engineering draft PR #16, branch `research/p24-cross-mint-m01-batch-monitor-20261031`. One main Bot is sufficient for the first acceptance; historical six development Bot descriptions in BOTS.md are optional reference material, not prerequisites.

**Trigger:** User says “分析 <Solana Mint>”, “调查这个Meme”, or asks to review known Mint risks. Grok should use the terminal and existing Python CLI, **not** rebuild the Solana crawler or invent chain facts. All outputs remain read-only. Do not trade, sign, broadcast, access seed/private keys, install unknown agents, start x402 payments, or enable auto-payment.

## 1. Real Mint → reproducible source files

Use the currently checked-out **reviewed engineering PR** and confirm repository SHA and Python version (3.11+). Set `MINT` to the user's validated Solana Mint; use one fresh directory per run to prevent mixing snapshots. The following example Mint was previously tested with public vendor data; it is **not** a claim of a fresh live observation.

```bash
MINT=EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)
RUN_DIR=".runtime/grok-runs/$RUN_ID"
mkdir -p "$RUN_DIR"
git rev-parse HEAD
PYTHONPATH=src python -m solana_meme_os.mint_v01 "$MINT" --rugcheck --out-dir "$RUN_DIR/mint"
```

The command writes `report.md`, `report.json`, `dex-provider-raw.json` and, only if available, `rugcheck-provider-raw.json`. Report timestamps are **acquisition** times; RugCheck may be cached. If no report is produced, stop and report the source error.

## 2. Existing evidence handoff → Grok investigation

**Only run if the same acquisition produced all three files**: `report.json`, `rugcheck-provider-raw.json`, `dex-provider-raw.json`. If one source is unavailable, return `SOURCE_UNAVAILABLE`; do not fabricate a JSON, fill missing values with zero, or substitute an old report's raw files.

```bash
PYTHONPATH=src python -m solana_meme_os.vendor_event_handoff \
  --report "$RUN_DIR/mint/report.json" \
  --rugcheck-raw "$RUN_DIR/mint/rugcheck-provider-raw.json" \
  --dex-raw "$RUN_DIR/mint/dex-provider-raw.json" \
  --out-dir "$RUN_DIR/outbox"
```

Read `$RUN_DIR/outbox/evidence.json` and generated `grok_task_*.md`, **then** independently inspect report and source fields. The existing adapter validates raw byte SHA-256, chain/Mint, vendor data status and limited structural coherence. It emits:
- `investigations[]`: vendor **risk-label review tasks**, **not verified on-chain alerts**.
- `suppressed_candidates[]`: pool/AMM or unresolved holder identities, **not whales or insider proof**.
- `coverage.wallet_transactions=NOT_OBSERVED`, `funding_graph=NOT_OBSERVED`: do not infer live transaction activity, shared controller or copy-trading alpha.
- `model_calls=0` / `PREPARE_GROK_TASKS_ONLY_NO_BOT_INVOKED`: these describe the *program's stage*, not Grok's subsequent analysis.

The Bot's real user-facing result must distinguish **source facts**, **vendor labels**, **economic hypotheses**, **contradictory explanations**, **missing evidence**, and **best next investigation**. Reference files/field paths and the command's checked-out commit SHA. Research X discourse when it can change the current investigation; X posts are not on-chain confirmations. Any specialist knowledge perspective is optional and selected by relevance, not by mandatory role counts.

If Grok successfully performs this investigation, write the *Grok-authored* response in **a separate** `$RUN_DIR/grok_analysis.md` and retain original evidence files unchanged. This file can only prove Grok ran when it was actually created during a **real Grok session with runtime logs**; a local test or CI document must never imply that.

## 3. Separate continuous monitoring mode (not yet live)

The legacy normalized observation monitor is an **existing** module, not an authenticated RPC stream:

```bash
PYTHONPATH=src python -m solana_meme_os.monitor --input OBSERVATION_PATH --state-dir .runtime
```

Inputs must contain independently validated `schema_version`, `chain`, `token_address`, `observed_at`, `mode`, `source`, `metrics`, optionally `events`. The `--allow-fixture` flag is **demonstration-only**, never live evidence. Explain differences, contradictory evidence, source freshness and missingness; do not claim a “no activity” interval if data coverage is unknown.

**Do not enable a Routine or claim real-time monitoring until a real Grok on-cloud-computer one-shot run, an independently verified chain transaction, at least two actual observations, duplicate handling and restart recovery have separate proofs.** A future WebSocket/stream belongs in a tested persistent service (e.g., approved read-only Million functionality), not in LLM reasoning on each tx.

## Verification and boundary

- Offline CI: `PYTHONPATH=src python -m unittest discover -s tests -v`.
- Existing live public-supplier precedent: engineering evidence `docs/evidence/v01-real-rugcheck-holder-2026-11-01.md`.
- Program-to-evidence handoff: `docs/vendor-event-handoff.md`.
- Grok cloud **runtime acceptance** requires its own command transcript, source status, created files and answer. A passing GitHub CI job validates Python, **not a Grok Bot deployment**.
