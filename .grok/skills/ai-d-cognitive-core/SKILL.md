---
name: ai-d-cognitive-core
description: "Blix 的跨项目通用认知能力入口：按需访问 sunshihao001/ai-d 全部长期能力，包括目标理解、专业知识、未知发现、方案判断、实施验收、反证纠错和知识继承；必须保留 Blix 原生 Meme 业务目标和只读安全边界。"
---

# Blix 接入 ai-d｜全体系入口（候选 V0.1）

**唯一通用知识源**：[ai-d 跨项目认知核心 Skill](https://github.com/sunshihao001/ai-d/blob/proposal/goal-planning-knowledge-delivery-20261106/.agents/skills/ai-d-cognitive-core/SKILL.md)；首次接入所据来源版本 `a32d6a3076240110cb341b41b112578cb781208f`。上游仍为 Draft，暂不视作 `main` 已发布。

当问题涉及 AI 怎样理解普通表达、专业机制研究、发现未知、方案比较、知识适用、授权内执行、反证和长期继承时，**先检查当前 Blix 业务目标及原有能力**，再按任务访问上述 ai-d 统一入口并选择需要的原始内容；不得假装凭一个 URL 就已加载整套知识。

## 完整能力覆盖（并行能力，非七阶段程序）

| ai-d 通用能力 | Blix 中可能发挥作用的具体问题 | Blix 本地领域依据 |
|---|---|---|
| 1. 简单表达→专业问题表征与目标演化 | “这批地址是不是自己人？”先分清观察、同控猜测与用户实际研究目标 | `docs/project/goal-map.md`、`knowledge/ai/intent-knowledge-selection-and-reasoning.md` |
| 2. 跨领域专家理论与知识组织 | 从地址/Token Account/Owner 进入链上专业语义、库存与经济机制 | `knowledge/DOMAIN-MODEL.v1.json`、`knowledge/README.md` |
| 3. 主动探索、类比、未知机制和竞争解释 | 同步交易/多跳资金为何出现，哪些是公共设施、做市或数据回补？ | `knowledge/mechanisms/`、`knowledge/methods/` |
| 4. 成熟方案比较和独立判断 | 直接用 Blix、复用 OKX/Pulse/Million、有限修改还是新建程序 | `docs/project/capability-map.md`、`docs/project/delivery.md` |
| 5. 授权范围内实施、可核查交付 | 真实 Mint 调查、监控报告、源码验证和故障恢复 | `docs/project/knowledge-to-capability-integration-v0.1.md` |
| 6. 来源/证据/反证/纠错 | Token Account 不等于 Owner，资金路径不等于共同控制，离线不等于实跑 | `docs/project/knowledge-use.md`、`docs/project/read-only-safety.md` |
| 7. 长期知识继承、反馈和方法更新 | 保留旧 Grok/Hermes/qb-/meme- 的机制与失败经验，不复活旧固定流程 | `knowledge/INTEGRATION-CROSSWALK.md`、`knowledge/MIGRATION.json` |

Blix 的**Solana Meme 专业知识和产品本身仍是业务主体**。ai-d 负责跨专业、跨模型可复用的认知方法与专业研究来源；绝不把 ai-d 的案例当成链上事实，也不替换 Blix 的采集、UI、解析、业务指标或安全权限。通用部分可按需深入到上游 `knowledge/INDEX.md`（P1–P8）、`knowledge/COGNITIVE-MAP.md`、`planning/goal-navigation-v0.1.md`、`research/`、`evaluation/`，不只访问 Skill 摘要，也不一次性全文注入。

## 如何判断不是空的链接

一个具体 Meme 请求至少应能说清：本次用户目标；实际读取的 ai-d 具体原始文件/提交；与 Blix 哪项领域知识和真实源码事实相连；由此增加了什么有效竞争解释、反证或方案决策；实际产物/验收与 UNKNOWN。未读取则报告“未继承/未加载”，不要虚构。没有新增作用时可不引用 ai-d；全体系**可被调用**，不代表每次必须跑全套步骤。

## 运行环境边界

Grok CLI 官方会扫描仓库 `.grok/skills/` 下的 `SKILL.md`；本文件被存入该位置，只代表 **Grok CLI 兼容的发现候选**，尚未在云端实际运行和验证自动发现。Grok Bot 的私人共享 Skill 属于单独的 Bot 技能库，需要在该产品启用并测试；**此处的文件不会自动安装到 Grok Bot 云电脑原生 Bot**。其他使用 Blix 的 ChatGPT/Codex 应根据其各自的项目资料与 Skill 机制接入，而不是假定所有客户端都会读取该文件。

**严格只读**：本 Skill 不执行链上交易、不调用签名/广播/付费流程，不读取或泄漏私钥；项目现有交易代码的权限风险不会因写了 Skill 就消失。用户价值与重大方向由用户决定，模型推断和外部来源不能授权不可逆行为。
