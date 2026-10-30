# Solana Meme knowledge is the core; Grok is the host

**Purpose:** preserve the expert learning, domain research, adversarial perspectives and practical lessons from three earlier projects while discarding Hermes-specific *runtime* assumptions. A working Bot without validated external knowledge is only orchestration.

## 专家主导的全领域知识建设（本轮 96+8 单元，未实证）

[**从小到大的 Solana Meme 全域知识总图**](atlas/README.md)是当前 D01–D12 的系统性导航：保留现有 8 层、21 位专家、7 个 Bot 角色、52 项历史能力和 15 张旧卡，向每个 D 域增加 8 个真正的专业机制问题（共 96 个）以及 L0 的 8 项治理基础。可直接阅读 [12 条跨领域推演链](atlas/cross-domain-chains.md) 与 [来源、覆盖和深度缺口审计](atlas/source-coverage-and-gaps.md)。**这是完整研究覆盖的第一轮内容，不等于 96 个市场结论均得到实证或专家已全部精通。**

本地只读知识导航：`PYTHONPATH=src python -m solana_meme_os.knowledge_atlas --audit`；也可 `--domain D03`、`--unit D05-01`、`--expert E-L3-02` 按现有本体与专家查询具体机制。程序不会联网、启动 Bot、提供交易信号或更改来源准入。

## L0–L7 专属专家视角（Draft，非已安装 Bot）

[21 位内部专业专家与完整分析程序](experts/README.md) 分布在全部八个知识层：从原始来源/交易/市场/钱包资金，到策略机会、执行、独立反证与监控治理。每位专家都有自己的知识、观察顺序、相反机制、关键查询、停止条件，并映射现有 B01–B07 工作责任；**不创建 21 个 Grok Bot**。机器注册表为 [registry.v1.json](experts/registry.v1.json)，离线专家方法查询：`PYTHONPATH=src python -m solana_meme_os.expert_brief --question "同源钱包能跟单吗？" --objective ECONOMIC`。仅提供研究材料与调查计划，不是大模型专家自动执行器或市场验证结果。

## Project-internal specialist knowledge expansion (Draft)

The existing D01–D12 ontology now has a **practical domain content entry point**: [domain/README.md](domain/README.md). Four targeted knowledge files explain actual Solana transaction/market mechanisms, wallet/funding/holder behavior, copy-trading executability, and evidence-safe cases. These are **review candidates**, not independently validated Alpha, live data integrations, or a replacement for the 15 archived source cards. Do not bulk load them into the monitor; choose only relevant domain content per question, observe the K1 source-admission restrictions, and require K2 original evidence for factual claims.

## What has been migrated

The initial catalog has 15 source-pinned cards in `knowledge/catalog.v1.json` covering:

- **Market mechanics:** pump-style token/pool lifecycle, mint/freeze/security, reserve depth, liquidity withdrawal vs repricing, GMGN discovery streams.
- **Actors and relations:** wallet role candidates, deployer history, early buyers/snipers, financing graphs, CEX infrastructure exclusions, Sybil/wash/coordination alternatives, holder concentration and entity-control differences.
- **Interpretation discipline:** multi-source evidence chain, contradictory evidence, missingness, research-only gates and source/unit verification.
- **Legacy hypotheses:** first-control-zone/POC/AVWAP reclaim. Useful for research but not validated as a Solana signal.
- **Reliability:** Hermes Harness anti-fake-completion and calibration learning, independent of Hermes command/hook machinery.

Each unit is a **portable knowledge candidate**, with a pinned original GitHub commit + path, `mechanism`, `required_evidence`, `alternative_explanations`, `inference_limit`, `next_check` and status. These are not a claim that sources are empirically validated; source traceability and truth are different things.

## How knowledge changes runtime behavior

- **Simple user request** → `python -m solana_meme_os.knowledge --question "这批钱包资金同源吗"` returns relevant knowledge and missing verification work.
- **Monitoring snapshot** → `python -m solana_meme_os.monitor ...` now appends `knowledge.interpretation_candidates` to observed changes. The cases must be evaluated against real source data.
- **Research/QA Bots** → read the same cards, scrutinize source evidence and develop independently testable alternatives.
- **Monitor Bot** → cannot promote a hypothesis to a real trade/risk conclusion; it can only report observed changes, provenance, missing inputs and plausible mechanisms.

Literal keyword routing is a reproducible **minimum interface**, not deep understanding. Grok's real language understanding needs an actual configured Bot that reads these cards and selectively retrieves primary evidence. It must be free to discover **new** mechanisms rather than being trapped by this list.

## Three status labels

- `source_contract`: known source's proposed input/output epistemic separation; not an externally certified standard.
- `documented_legacy_method`: a method or proposed workflow documented in historical source, not yet evaluated on market outcomes.
- `unverified_hypothesis`: a historical strategy or causal hypothesis requiring source data, representative positive and negative cases and independent review.

Do not confuse any label with 'empirically proven'.

## Beyond this first wave

A complete repository-wide migration has **not** happened. The first wave now includes **21 exact historical Markdown snapshots** in `knowledge/legacy-snapshots/` with a source manifest, plus 15 curated and actively routed cards. These snapshots preserve domain explanations, proposed methods and historic design contracts without any Hermes executable runtime. Most original data, notebooks, historical case evidence, tags and the full Hermes project remain in their source repos. Missing real case replay, authoritative field mappings, blind evaluation and release-calibration loops are listed in `docs/next-steps.md`.

Recommended future package structure: `knowledge/catalog.v1.json` (indexed), `knowledge/cases/` (original on-chain observations and labelled outcomes, without secrets), `knowledge/claims/` (tested and superseded claims), and `knowledge/evaluations/` (comparison against no-knowledge Bot). Do not create empty folders or call them implemented.

## Entry-point commands

    PYTHONPATH=src python -m solana_meme_os.knowledge --question "GMGN热门能证明这币安全吗？"
    PYTHONPATH=src python -m unittest discover -s tests -v

References: `docs/sources.md`, `knowledge/legacy-audit.md` and `skills/solana-meme-knowledge/SKILL.md`.

## Second wave — do not bulk migrate

New model: keep the resident 15 cards and 21 prior snapshots as a bounded historical baseline, but use `knowledge/source_index.v1.json` to consult external specialist sources **on demand**. The repo now indexes 17 documents, including methodological references from `Why-Solana-Memecoins-Are-Over`, without importing its licensed analysis into Grok. Run `python -m solana_meme_os.research --question ...` to create an evidence intake packet; see `docs/on-demand-research-design.md`. The goal is better judgment, not maximizing token count or the number of copied files.

## 完整结构与逐批填充

请优先阅读 [`system/README.md`](system/README.md) 的 8 层、12 专业领域架构，以及 [领域关系图](system/ontology.v1.json)、[来源注册](system/source-registry.v1.json)、[研究对象](system/research-units.v1.json)。现有 15 张概念卡、21 个历史快照不复制、不删除；D01/D07 的缺口保持明示。新增外部研究只是 `external_reported`，未做本地独立复算，也不改变 Monitor 规则。

```bash
PYTHONPATH=src python -m solana_meme_os.knowledge_system --audit
PYTHONPATH=src python -m solana_meme_os.knowledge_system --question "跟单资金网络滑点退出成本"
PYTHONPATH=src python -m unittest discover -s tests -v
```

领域导航为确定性关键词与依赖预选，不能替代真实 Grok Bot 的语义推理或经济性检验。
