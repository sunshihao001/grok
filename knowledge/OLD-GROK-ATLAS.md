# 旧 Grok 自身目录与知识资产总图 V0.1

> 2026-11-06 | **先理解旧 Grok 自己是什么**，再讨论怎样进入 Blix。检查了 `sunshihao001/grok@main` 与 PR #14/#16/#17 的 GitHub 目录、核心程序、知识 README 和 PR 状态。全文目录扫描不等于所有文件逐行审阅；**知识主张、离线测试、历史供应商实跑、Grok Bot 云端真实运行属于不同证据级别**。

## 1. 必须首先区分四份不同的“旧 Grok”

| 版本/出处 | 核心身份 | 能确定什么 | 不能直接声称 |
|---|---|---|---|
| [旧 `main`](https://github.com/sunshihao001/grok/tree/main) | 早期 Solana Meme Workflow OS：多 Bot 构想、知识选择/只读监控的 Python 最小原型 | 代码、15张本地知识卡、历史快照、Skill说明、Fixture 与离线测试存在 | 已安装真实 Grok Bot、可24小时运行、专业因果判断已实测 |
| [PR #14 知识分支](https://github.com/sunshihao001/grok/pull/14) | 专业研究扩展：8层/12域/152知识单元/22专家视角/65参考资产 | 领域目录、专业机制研究、来源登记、导航与复用台账 | 152条是已实证命题；22个是云端Bot；65项都逐项跑过 |
| [PR #16 工程分支](https://github.com/sunshihao001/grok/pull/16) | Solana原始交易适配、单Mint免费多源调查、钱包批次与跨Mint工程研究 | 原始解析器/试运行证据/Fixture及测试；2026-11-01一次真实公开供应商查询 | 链上完整复算、实时多跳/Owner归因已验、云电脑上线 |
| [PR #17 集成分支](https://github.com/sunshihao001/grok/pull/17) | 旧知识与工程分支合用的导航/来源/集成试验 | 额外知识安装、目标/程序整合文档、离线集成工作 | 已并入 `blix`，或能够安全启动含全部权限的成品 |

2026-11-06核查时，#14/#16/#17均为 **open draft、未合并**。即使内容后来变化，也要重新核对其head SHA与目标分支，不把旧分支名字当最终稳定版本。

## 2. 旧 `main` 的目录大纲：早期“知识是核心，Grok 是承载”

```text
grok@main/
├── README.md / AGENTS.md / CONTEXT.md / BOTS.md
├── knowledge/
│   ├── README.md / catalog.v1.json          # 15个来源固定的概念/方法候选卡
│   ├── source_index.v1.json                  # 按需检索外部专业来源
│   ├── method.md / source-index-README.md / legacy-audit.md
│   └── legacy-snapshots/                    # 21个历史研究快照与manifest
├── src/solana_meme_os/
│   ├── knowledge.py                         # 本地卡的条件/词面预选
│   ├── research.py                          # 外部来源候选与时间证据请求
│   ├── monitor.py                           # 只读观测/状态 + 知识解释候选
│   └── gmgn_collect.py                      # 旧GMGN采集接口，非Blix依赖
├── skills/solana-meme-knowledge/SKILL.md
├── skills/solana-meme-monitor/SKILL.md
├── bots/04-monitor.md / routines/monitor.md / rules/monitor.v0.json
├── tests/test_knowledge.py, test_monitor.py, test_research.py
├── fixtures/observation-1.json, observation-2.json
└── docs/on-demand-research-design.md 等
```

**关键认识**：这个版本已经研究过一种简单而有价值的方法：
- **K0 常驻的少量知识**：目标/来源纪律与15张候选卡；
- **K1 按需找原文**：`knowledge.py` 与 `research.py` 基于目录/关键词生成候选和所需证据，并不是大型模型的完整推理；
- **K2 独立原始证据**：真实签名、时点、池/Wallet数据、负样本与实际结果。旧 `main` 自述当时没有已核验的完整市场 K2 运行数据。

这个思路应继承为“知识定位、适用性和证据”方法，而不复制旧 Python 运行时作为 Blix 第二套服务。

## 3. PR #14 的知识结构：是目录、专业正文和参考资产，不是Bot工程

```text
knowledge/ [PR14]
├── domain/                   # 专业研究正文：链上、市场、资金、钱包、策略、反证等
│   ├── L1-L2-chain-market.md
│   ├── L3-wallet-actors.md
│   ├── L3-E-L3-02-capital-organization-incentives.md
│   ├── L3-actor-economic-mechanisms-deepstudy.md
│   ├── L4-L5-copytrade-edge.md
│   ├── L6-L7-investigation-cases.md
│   └── ...价格、关键钱包、异常孵化等研究专题
├── system/                   # 本体、152索引、65项目台账、方法、进度与知识治理
│   ├── ontology.v1.json
│   ├── whole-domain-atlas.v1.json
│   ├── gpt-meme-project-index.v1.json
│   ├── gpt-meme-project-core.v1.md
│   ├── reference-capability-reuse-ledger.v1.md
│   ├── whole-project-convergence-audit-2026-11-01.md
│   └── 其他约25份相关体系与研究文档
├── experts/registry.v1.json  # 22个知识专家视角，非22个Bot
├── transfer/                 # C0–C4等培训/任务交接及反馈草稿
├── experiments/              # 候选实验规范
├── legacy-snapshots/         # 历史来源快照
├── catalog.v1.json, source_index.v1.json
└── README.md                 # 源版本约束、研究状态与进度
```

**旧知识层级**：L0来源与证据治理；L1协议事实；L2市场机制；L3钱包/资金主体；L4策略机制；L5执行与风险；L6实证反证；L7 Agent/运行演化。

**12个业务研究领域**（每域12项，共144项；加L0八项总152）：

| 领域 | 原研究主题 | 在旧 Grok 中属于哪类知识 |
|---|---|---|
| D01 | Solana账户、交易、CPI、余额、时间 | 协议/事实基础 |
| D02 | 发币生命周期、曲线、迁移与多池 | 发行与市场机制 |
| D03 | 流动性、定价、报价、MEV、交易质量 | 市场微结构 |
| D04 | 钱包角色、PnL、持仓策略与限制 | 行为调查 |
| D05 | 资金网络、权利、资本角色及经济主体 | 资本机制与反证 |
| D06 | 供应量、库存、池/托管、Sybil、刷量 | 持仓/库存调查 |
| D07 | 同步行为、跨Mint、异动时序与演化 | 市场事件与监控 |
| D08 | 策略/Alpha假说、跟随及探索 | 待验证策略知识 |
| D09 | 滑点、手续费、可交易性与尾部风险 | 执行经济/风险约束 |
| D10 | 数据源、覆盖、去重、时间与成本 | 数据/工程可靠性 |
| D11 | 因果解释、反证、样本外、泄漏与复算 | 实证研究方法 |
| D12 | AI任务路由、来源准入、Bot边界与知识进化 | AI协作/知识工程 |

**可靠性边界**：上述152项主要是 `mapped_unverified` 专业研究地图，不能直接作为152条已验证事实。参考资产登记65项不表示这些项目全部有同级别源码/实跑证据；22视角不表示需装22Bot。PR #14 的全文迁入应保留来源和原状态。

## 4. PR #16：与知识不同的原始交易工程资产

`src/solana_meme_os/` 在该分支含 `raw_tx_adapter.py`、`mint_v01.py`、`public_pair_report.py`、`public_rugcheck_report.py`、`public_token_accounts.py`、`wallet_batch_monitor.py`、`vendor_event_handoff.py` 等；`docs/` 含 `p3-m01-raw-adapter-contract.md`、`p24-m01-crossmint-research.md`、`product-delivery-plan-v01.md`、`evidence/`。

实际证据（[PR16](https://github.com/sunshihao001/grok/pull/16)）：2026-11-01曾通过GitHub Actions对真实Mint进行公开供应商查询，DEX Screener有5池，RugCheck缓存20条Holder Token Account候选，其中一个Owner候选与AMM池地址匹配；公共RPC遇429、未完成独立链上Owner复算，不能说20条属于20个独立钱包。**这一轮不将Python工程直接并入Blix**；先作为事实协议、反例、测试和成熟替代路径的来源。

## 5. PR #17：原有集成尝试值得继承什么？

除PR16基础代码外，有 `docs/ai-knowledge-navigation-guide.v1.md`、`docs/grok-knowledge-installation.md`、`docs/bot-knowledge-integration.md`、`docs/gpt-github-grok-knowledge-loop.md`、`docs/goal-evolution-current.json`、`docs/okx-onchainos-runtime-review.md` 等。

它属于“历史知识能否被工程端消费、是否有路径冲突、怎样控制不同来源”的对照，不是Blix的第二个知识目录真源。可用其失败/重复建设记录来审查新的Blix融合，不复制旧开发架构。

## 6. 最值得保留的内容，与需要抵抗的历史惯性

| 应当保留 | 不应直接继承 |
|---|---|
| 领域知识、原始专业问答、经济机制与竞争解释 | “同源资金=庄家”、未经校准的固定同控概率 |
| 来源固定、缺失字段、证据/反证/状态分离 | 旧GMGN收费依赖、旧绝对路径、Hermes hooks |
| 15个候选概念卡、21个旧快照和来源索引 | 把旧代码和旧多Bot/Skill数量当新产品要求 |
| PR14 152项问题体系和22种专家视角 | 为保持旧编号再造152个Blix文件或22个运行Bot |
| PR16原始交易/历史覆盖的约束及实测失败 | 把Fixture和公共供应商预览说成完整业务验收 |
| PR17合并冲突/知识安装的历史经验 | 认为未合并Draft已部署到Blix |
| 参考资产的完整来源、功能和许可边界 | 所有参考仓库都值得复制、安装或自动支付 |

## 7. 旧 Grok 与外部历史项目的关系

`sunshihao001/grok` 的历史知识来自更早的 [Hermes](https://github.com/sunshihao001/-)、[qb-](https://github.com/sunshihao001/qb-) 和 [meme-](https://github.com/sunshihao001/meme-)；PR14还登记了外部成熟产品如Million、Pulse、PumpTrace、OKX、HoldTech等。**它们不是GroK main的子目录**。旧Grok的“已登记、已摘要、已在原仓库研究、已代码复用、已联网实跑”必须逐个分开。

本轮**先把旧 Grok 仓库内部梳理完**；Hermes/qb-/meme-更深的细分目录、参考成品的原始知识应在同一套Blix分类之下继续追加，不允许反过来要求Blix按原项目重建多个知识体系。

## 8. 对接位置

- Blix原生事实与产品能力：[BLIX-NATIVE-ATLAS.md](BLIX-NATIVE-ATLAS.md)。
- Blix已经迁入多少旧知识：[MIGRATION.json](MIGRATION.json)（需按当前分支核实）。
- 旧PR14 152项到Blix模块的已有定位：[业务路由索引](../docs/project/legacy-knowledge-routing.v1.json)。
- 两套结构的去重、遗漏与接收裁决：[INTEGRATION-CROSSWALK.md](INTEGRATION-CROSSWALK.md)。
