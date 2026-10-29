# Project Agent / Bot Rules — Solana Meme Workflow OS (Grok Edition)

## Safety Boundary (Hard)

Phase 1 is read-only research / paper-only gating.

**Forbidden for all Bots**:
- real orders
- private key access
- wallet signing
- transaction broadcast
- gmgn-cli swap / multi-swap / cooking create
- auto deploy
- claims like “确定庄家”, “确定内幕”, “一定会涨”

## Roles

See `BOTS.md` for the multi-Bot development + single Monitor design.

## Required Reading Before Work

- `CONTEXT.md`
- `BOTS.md`
- Relevant design docs (link back to original Hermes repo for full history)

## Completion

Every significant rule or skill change should produce a short result note under `reports/`.

## Knowledge-preserving migration (mandatory)

- **Do not import Hermes startup, CLI, control hooks, absolute paths, memory store or runtime behavior.** Prior Hermes and qb- repositories are evidence/source archives, not Grok OS dependencies.
- Start with `knowledge/README.md` and `knowledge/catalog.v1.json`. Use `PYTHONPATH=src python -m solana_meme_os.knowledge --question "普通语言问题"` as a retrieval triage tool; this is not a substitute for reasoning or research.
- For each claim, select knowledge **by relevance and mechanism**, then test whether required inputs exist. Never copy the rule's conclusion just because keywords match.
- Label historical claims as documented_legacy_method / unverified_hypothesis / source_contract. Historical provenance does NOT validate financial effectiveness.
- A rule release requires actual market/source data, counterexamples, error attribution and independent review. Revisions go to a reviewed PR, not automatic self-upgrade.
- When retrieval has no match, explicitly expand research, add sources and a candidate card; never hallucinate missing knowledge.

## Knowledge Intake Gate

- 在解释任何 Solana 监控事件前先读 `docs/knowledge-intake.md` 和 `knowledge/registry.v0.json`；遇到匹配问题再读相应 `knowledge/packs/*.md`，必要时核对锁定 source commit。
- 不要把源库文档整库拷进 prompt 或规则文件。尊重 source-of-truth；所有概念需保留反证、缺失、替代解释。
- 仅 `reference_only` 的知识不得生成/提升冻结规则、声称正净期望或设置新自动交易门控。
- 开发 Bot 可提案新包/版本/测试；最终 Monitor 只读经接受的包，不擅自写长期知识或覆写源规则。
