# Skill Draft — M01 wallet-batch research (offline-only)

Use when asked to compare wallet batch membership and quote trade activity across 1/5/15 minute windows in a specified Solana Mint using **already normalized** economic-action records. This is a research prototype, not the live monitor.

1. Read [`p24-m01-crossmint-research.md`](p24-m01-crossmint-research.md) for the exact `m01.v1` contract and limits.
2. Confirm the input mode is `fixture`; never claim the example came from mainnet.
3. Run `PYTHONPATH=src python -m solana_meme_os.wallet_batch_monitor --input fixtures/wallet-batches-demo.json --output /tmp/m01-report.json`.
4. Check `timeframes`, `comparisons`, `candidates`, `source_refs`, `data_status` and `ignored_duplicate_events`. Incomplete windows are unknown; never compute deltas across them.
5. Describe each candidate as **observation only**. Do not attribute actors, manipulate wallets, place trades, sign, broadcast or automatically edit the approved Monitor.
6. Before any further extension, run `PYTHONPATH=src python -m unittest discover -s tests -v`. Tests on fixtures do not prove real RPC readiness.

Next research step: candidate cross-Mint patterns C01/C02/C05 and a real Solana transaction normalizer with independently verified Token Account owner and CPI economic action semantics, kept separate from this offline prototype.