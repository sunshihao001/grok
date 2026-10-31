# On-demand source registry — not a data lake

`source_index.v1.json` lists **22** curated entry points across the original Hermes domain work, the meme- theory repository, the qb- GMGN prototype, the third-party Why-Solana-Memecoins-Are-Over study, and OKX OnchainOS read-only documentation.

- Each source has a pinned Git commit, exact path, topic cues and *why to read*.
- The local `knowledge/catalog.v1.json` and its 21 historical snapshots remain a limited resident baseline. No further wholesale knowledge copy is authorized by this design.
- On an investigation, select a small set by mechanism; the existing keyword routing is only a deterministic shortlisting step. The Grok Bot must reason beyond it and search newly relevant primary sources.
- Only the operator-requested `--fetch-excerpts` option retrieves short previews of the selected pinned public text. It prints ephemeral excerpts; it never uploads them into GitHub or validates the economic claim.
- **Do not treat this index as evidence**. The actual market claim requires specific on-chain facts, observation timestamps, controls and later validation.

Third-party reference is authored by Benjamin Da Cunha. The author's CC BY-NC-ND 4.0 license covers written analysis; see upstream LICENSE-CONTENT.md. We cite links rather than copying its articles. Methods are adapted independently and are not endorsements of a trading strategy.

## Market-wide research routing

- Source lookups now cover Hermes Sybil/coordination methods, downstream receiver exits, same-Slot sequencing code and OKX interface contracts.
- Run: PYTHONPATH=src python -m solana_meme_os.research --question "同 Slot 钱包是否同控，资金从哪来？"
- Run: PYTHONPATH=src python -m solana_meme_os.research --question "OKX 行情数据字段和时间戳定义"
- These are research source pointers, not API authorization, an alert feed or proof of trader identity. See docs/knowledge-system-integration-v1.md.
