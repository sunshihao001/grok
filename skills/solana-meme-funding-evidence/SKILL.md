---
name: solana-meme-funding-evidence
description: Examine a time-bounded, source-linked direct funding graph as a hypothesis with infrastructure, dust, missingness and future-data checks; fixture-only KB-002.
---

# KB-002 Funding Evidence — Grok development Bot skill

This is a **research-only** skill. Read `docs/knowledge-intake.md` and `knowledge/packs/KB-002-wallet-funding-evidence.md`, then retrieve only the exact pinned sources required for the question. Do not copy the third-party source work into the Bot memory. Existing `knowledge/catalog.v1.json` and `knowledge.py` stay authoritative for current runtime routing; this is an incremental research lens.

1. Ask what relationship is being claimed. Require a falsifiable question: shared direct inbound, shared terminal, transit relay, observed co-timing, or attributed ownership. These must not be interchanged.
2. For raw native transfers require signature + instruction_index, from/to, lamports, source ref, block_time, *available_at*, decision cutoff, coverage and source-address hub classification provenance.
3. Test locally only with `PYTHONPATH=src python -m solana_meme_os.funding_evidence --input fixtures/kb002-funding.json --allow-fixture`. The file contains synthetic addresses and simulated signatures. Do not call RPC, fetch secrets or label it live.
4. Distinguish material inbound from tiny unsolicited transfers; no Solana universal funding floor is asserted.
5. Record direct transfer edges, hub-excluded edges and unknown classifications separately. Missingness and future-unavailable evidence are explicit; absence does not prove independence.
6. Name at least two alternatives and a negative control, then propose raw-chain and time-safe replication. **No automatic entry signal, personal identity attribution or trade.**

KB-002 remains `reference_only` even if tests pass. No Grok Bot/Routine is provisioned by this file.
