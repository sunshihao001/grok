# Vendor evidence → Grok review handoff (read-only)

This module is an executable, tested adapter for the existing Mint V0.1 report, **not** a live on-chain-event detector or a connected Grok Bot.

## Run with existing public report

1. Run the already implemented read-only Mint report:
   PYTHONPATH=src python -m solana_meme_os.mint_v01 <MINT> --rugcheck --out-dir .runtime/mint
2. Produce evidence-backed review tasks from the **same acquisition's raw bytes**:
   PYTHONPATH=src python -m solana_meme_os.vendor_event_handoff --report .runtime/mint/report.json --rugcheck-raw .runtime/mint/rugcheck-provider-raw.json --dex-raw .runtime/mint/dex-provider-raw.json --out-dir .runtime/grok-outbox/<unique-run-id>
3. Inspect evidence.json, provisional_monitor_opinion.md, and grok_task_*.md.

Create a **new out-dir per acquisition**; do not reuse an old outbox containing previous tasks.

The tool validates source hashes, Mint/chain and provider snapshot status. It generates:
- one pending **review task** per flagged RugCheck vendor risk label (not a verified on-chain incident);
- suppressed or unresolved top-holder candidates where pool infrastructure or missing ownership evidence makes a whale accusation unsafe;
- unobserved wallet/funding/RPC coverage and a "Grok NOT_EXECUTED" status.

There are **zero LLM calls** in this module. Nothing contacts OKX, Grok, a webhook, a wallet or any payment system. Claims of automatic live wallet monitoring, shared-funder control or Bot-to-Bot expert completion require distinct runtime evidence.

Check offline tests: PYTHONPATH=src python -m unittest discover -s tests -v

## Next product acceptance

Connect one independently verified Solana transaction signature with *all* wallet observations to the existing fixture-only wallet_batch_monitor. Verify replay, missingness, and provider cost. Only after this succeeds should a configured Grok Bot consume an evidence package and return an independently logged specialist response.

Source: engineering PR #16; evidence from GitHub Actions #41269179918; related domain knowledge PR #14 remains a separate, unmerged branch.
