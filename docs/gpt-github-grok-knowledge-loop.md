# GPT → GitHub → Grok：渐进式知识发布与吸收（V0.1）

## 目的

不再靠长篇 GPT/Grok 聊天记录反复复制知识。GPT 研究所得先写为**最小独立知识单元**，提交到既有 GitHub 仓库，经审阅后才作为 Grok 的分级学习材料；Grok 的案例执行和理解反馈回流到 GitHub，再由 GPT/人工继续研究。

```text
GPT 查证/推演 ─→ 分级知识单元（草稿）
                     │
                  GitHub PR 审阅
                     │
               approved_for_study
                     │
       Grok 按角色/层级选择、读取固定 SHA
                     │
          理解测试/真实案例（分开记录）
                     │
            反馈 → 审查 → 下一知识单元
                     │
            成熟方法才候选 Skill
                     │
             独立 F0–F6 和人工发布
```

**本方案不训练底层模型权重。** Grok 的“学习”意味着按固定来源检索和应用知识、通过专业测试，并通过反馈与 PR 更新工作材料；不是模型自动微调或账户记忆自动变得正确。

## 与旧系统分工，不建第二套真源

- `knowledge/system/ontology.v1.json`：领域 D01–D12 和 L0–L7 知识架构。
- `knowledge/source_index.v1.json`：K1 原始资料检索，固定到外部 Git commit。
- `knowledge/catalog.v1.json`：已有 15 张知识卡，不复制到每个 Bot。
- `knowledge/system/research-units.v1.json`：研究主张及其证据状态。
- **新增** `knowledge/transfer/curriculum.v1.json`：课程调度层，仅记录**学习顺序、适用 Bot、知识单元路径、验收要求和审批状态**。
- **新增** `knowledge/transfer/modules/`：GPT 查证后编制的简短教学单元，引用已有权威文献；不改写市场事实。
- `skills/`：只有实践过且可稳定复现的流程才候选独立 Skill。一个概念或一篇外部文献通常不是 Skill。
- K2 真实原始观测、结果样本、负例仍需由 B02/B03/B04/B05/B06 按原始签名和时间独立验证，不能通过学习课程或 Bot 的自述生成。

## C0–C4 的学习深度（不同于 L0–L7、K0/K1/K2、F0–F6）

| 课程级别 | 理解任务 | 可以拿来当什么 | 不能当什么 |
|---|---|---|---|
| C0 项目认知 | 职责、来源、状态、安全 | 角色初始化 | 市场事实 |
| C1 基础原理 | Solana/GMGN 数据、时间与证据门槛 | 方法基础 | 机制证据 |
| C2 专业机制 | 钱包网络、资金图、市场结构 | 提出可证伪研究假设 | 控制人或因果定论 |
| C3 研究方法 | 预测增量、OOS、净经济性 | 独立设计与评价实验 | 已验证的盈利规则 |
| C4 Skill 应用 | 可重放真实任务、失败处理与工具集成 | 可评估的工程工作流 | 自动交易授权 |

不能靠考试通过提升市场证据状态；也不能让未经审核的课程向 B07 的 Routine 注入新市场规则。

## 从 GPT 研究到 GitHub 的最小单元

1. **研究素材**：原始来源、版本、适用总体、尚未知的内容。
2. **知识陈述**：说清机制，以及不允许推断什么。
3. **归属**：一个主 D 领域、一个课程深度、适用角色，链接既有 K0/K1。
4. **反例**：至少一个竞争解释或失败模式。
5. **验证问题**：能够分辨真理解与机械复述的问答/实操。
6. **状态**：初始 `draft`，通过真正的人类审核（PR/审阅记录）才能改为 `approved_for_study`，后续可 `retired`。课程审批不等于研究结论验证。
7. **版本**：反馈必须带完整 Git SHA；移动分支上发生变化时重新确认源版本。

**课程状态不表示 Grok 已通过考核。** 考核结果仅记录在反馈包，需独立审阅。更不能从此自动发布 B07 监控规则。

## 当前第一批：仅 C1-001

`modules/C1-001-evidence-gates.md` 是已经对照现有政策编写的 F0–F6 基础课程，仍标记 `draft`。它附有「同源钱包」的反例、时间数据可用性、解释与经济目标分歧、理解检查。

没有批量导入 C1–C4 的完整内容，也没有把旧钱包经验阈值包装成已证实的交易优势。

## Grok 如何取课（需在已确认的 Git 仓库检出中运行）

```bash
PYTHONPATH=src python3 -m solana_meme_os.knowledge_delivery --audit

# 只返回获准学习的课程；当前示例为 draft，因此正常返回空列表
PYTHONPATH=src python3 -m solana_meme_os.knowledge_delivery --bot B01 --through C1

# 人工要求预览尚待审核的 GPT 课程时使用，不代表批准
PYTHONPATH=src python3 -m solana_meme_os.knowledge_delivery --bot B01 --through C1 --preview-drafts

PYTHONPATH=src python3 -m unittest discover -s tests -v
```

B01 的学习 Skill 模板：`skills/github-knowledge-intake/SKILL.md`。必须在实际 Grok 应用中启用并完成安全的单次试验，仓库创建文件并不自动安装。

## Grok → GPT 的反馈

按 `knowledge/transfer/feedback-template.json` 回传：课程 ID、完整来源 commit、实际读过的路径、使用过的工具与原始日志、关键问题答案、反例、理解缺口和建议下一项。

反馈的 `learner_self_assessment` 只能代表 Bot 自述；`reviewer_decision` 必须由 GPT/人工根据日志和测试依据作出，且只对课程理解负责。不要用一次通过就认为 Bot 已完成市场研究能力验证。

## 最简启动方式

先保留人工转发的 Grok 反馈；**不需要把整份 GPT 对话发过去**。本阶段 Grok 可以直接检出受审阅的 Git commit 并按课程清单执行。待这个链路通过多次真实任务后，再考虑利用官方 GitHub 事件触发的 Grok Routine，自动检查新审批课程（初期只生成阅读建议和反馈，绝不修改监控规则）。Webhook/事件由 Grok 账户自行连接并审批；GitHub 文件不意味着任务已安装或启用。

Grok 官方说明：私有 Skill 库在各 Bot 间共享，但需检查其启用与访问；共享云电脑的文件、浏览器会话和命令行凭据也对同一账户其他 Bot 可见。因此角色和目录不是安全隔离，敏感信息与私钥不应放入共享环境。
