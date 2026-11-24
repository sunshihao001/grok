# Blix｜2026-11-15 最新 Agent 主体与运行时认知

> 历史平台比较研究。平台能力、成本和边界依然可供验证选型；本版对主运行主体的推荐已由[11月16日候选分工](meme-autonomous-trading-intelligence-v0.1.md)更新。两版均需实际任务验收。

## 1. 先纠正一个最重要的概念

**Blix 仍然是当前建设仓库和成熟产品基础，但不再被理解成整个系统唯一的“AI主体”。**

更准确的分层是：

```
用户目标 / 价值选择
        ↓
AI Agent：理解、研究、选择、调用工具、反证、复盘
        ↓
Agent Runtime（候选：Hermes / Muse / Grok Bot 等）
        ↓
MCP / API / Browser / Terminal / Skills
        ↓
Blix + Solana / OKX / Helius / 其他数据源
        ↓
事实与经济证据
        ↓
Case / Hypothesis / Opportunity
        ↓
AI 再判断、复核、发现缺口
```

因此：

- **Blix**：当前成熟业务、数据、UI、API、MCP、市场终端和历史运行经验的实现基础。
- **AI Agent**：真正负责“这件事下一步应该怎么做”的推理/协调主体。
- **Agent Runtime**：承载这个 Agent 长期运行、记忆、Skill、工具、浏览器、终端、定时任务和多代理协作的执行环境。
- **数据/证据层**：负责可追溯事实，不把 AI 推断直接变成真值。
- **Case/Opportunity 层**：把一次调查变成可复核的业务对象，而不是一段聊天。
- **UI**：Blix 当前 UI 是重要实现资产，但未来可以替换或增加新的入口。

这不是要立即重构 Blix。**先保持 Blix 可运行、可回归、可复用，再验证哪个 Agent Runtime 最适合承载长期工作。**

---

## 2. 2026-11-15 对三个候选运行时的最新判断

### Hermes Agent（NousResearch）

官方资料：
- https://github.com/NousResearch/hermes-agent
- https://hermes-agent.nousresearch.com/docs
- Solana Skill：https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/optional/blockchain/blockchain-solana.md

目前确认的能力包括：

- 开源、可自行部署，可运行在 VPS、GPU 集群或其他后端。
- Agent loop、工具注册、Provider routing、持久会话。
- Persistent memory，且 Memory 与 Skill 有明确分工。
- Context files（如 `HERMES.md`、`AGENTS.md`、`CLAUDE.md` 等）支持项目级上下文。
- Skills 可由 Agent 创建、更新、删除；适合把成功/失败/修正后的工作流程沉淀成程序性能力。
- MCP、Browser、Terminal、Files。
- Subagents / delegation。
- Cron / scheduled work。
- Bot Mode / 多角色长期会话。
- 多模型/Provider 路由。
- 有官方可选 Solana Skill，可查询钱包、Token、交易、活动、NFT、鲸鱼、网络状态和价格。
- 有较完整的安全隔离、危险命令审批、MCP 凭据过滤、Prompt Injection 防护等机制。

**对本项目的意义：**

Hermes 是目前最值得作为“长期自有 Meme Agent Runtime”验证的候选，因为它与本项目想形成的闭环高度匹配：

```
用户问题
→ Agent 判断
→ 调工具/查资料/查 Blix
→ 形成证据
→ 生成 Hypothesis / Case
→ 反证
→ 得出当前判断
→ 记录经验/Skill
→ 下次继续
```

但**“Hermes 最适合”目前仍是待验证假设，不是已验收结论**。

---

### Meta Muse

官方资料：
- https://muse.ai/
- https://chromewebstore.google.com/detail/muse-from-meta/jnakhhjmpmoohbjgfccbccfoifnmbdjd

目前确认：

- 每个用户有持久、隔离的 Linux Secure VM。
- 有浏览器、存储、CPU、内存。
- 支持 Skills、Connectors、Subagents、Cron。
- 可创建自定义 Connector，对接 API / CLI。
- 有持久 Memory，并允许用户查看、编辑、删除。
- 浏览器采用真实 Chromium 与安全代理机制。
- 对权限、凭据、Prompt Injection 和敏感操作有较强的产品化安全设计。
- VM 是 Muse 内部长期工作的系统记录中心。

**对本项目的意义：**

Muse 是一个非常成熟的“个人 AI + 云电脑”产品形态。它特别适合验证：

- AI 是否能长期替用户做事情；
- 浏览器、工具、文件、Connector 是否足够支撑真实工作；
- Skill + Subagent + Cron 能否形成长期工作流；
- 一个产品化 Agent 在安全边界下能做到什么。

但 Muse 是 Meta 管理的产品化运行环境。与 Hermes 相比，**用户对底层 Runtime、Provider、Agent 内部结构和长期知识组织的控制程度不同**。

因此目前不把 Muse 定义为“上层大脑”或“必须保留的一层”。它首先是**候选 Agent Runtime / 对照实验对象**。

---

### xAI Grok Bot

官方资料：
- https://docs.x.ai/grok-bot/overview
- https://docs.x.ai/grok-bot/how-grok-bot-works
- https://docs.x.ai/grok-bot/skills-routines-and-automations
- https://x.ai/news/designing-grok-bot

目前确认：

- 每个 Bot 有持久 Cloud Computer。
- 有 Browser、Filesystem、Terminal、Apps / Logins。
- Bot 是持久工作单位，Chat 可以只是一次交互入口。
- 支持 Skills / Prompts / Routines / Tools / Artifacts。
- 支持 MCP / Plugins。
- 多 Bot 可以并行和协作。
- Routines 可以按时间、事件、Webhook 等触发。
- 可以通过示范录制浏览器工作流并形成 Skill 草稿。
- Bot 有 Memory。
- 多 Bot 共享账户中的云电脑，因此 Bot 之间不是严格的安全边界。

**对本项目的意义：**

Grok Bot 已经非常接近“把任务交给一个长期 AI 同事”的产品体验。

它对 Blix 的历史意义尤其重要：

1. 第一代 Grok Bot / 旧项目已经提供了真实的 Meme AI 工作经验。
2. 其 Bot + Skill + Routine + Cloud Computer 思路可以继续作为产品设计参考。
3. Grok 不必与 Hermes 二选一；未来可以作为某种模型、Coding Worker 或外部 Agent 能力被调用。
4. 目前不能因为过去使用过 Grok Bot，就把整个未来系统继续锁死在 Grok Bot 上。

---

## 3. 三者现在应该怎么理解

| 对象 | 最准确定位 | 当前价值 |
|---|---|---|
| **Hermes Agent** | 开放、可自托管、可组合的 Agent Runtime 候选 | **最高优先验证** |
| **Muse** | 高产品化、安全型个人 AI / Cloud Computer 候选 | 对照实验 + 产品交互参考 |
| **Grok Bot** | 成熟的 AI coworker / Cloud Computer 产品 + 历史运行经验 | 历史基础 + 产品参考 + 可作为外部能力 |
| **Blix** | 当前成熟业务/数据/UI/API/MCP 实现基础 | **继续建设，不推倒重来** |
| **ai-d** | 通用认知、目标演化、研究与协同方法来源 | 上游方法，不等于运行时 |
| **旧 Hermes/qb-/meme-** | 专业研究与失败经验资产 | 按需取用，不等于当前 Hermes Agent |

### 特别注意：两个“Hermes”不能混淆

- **旧 Hermes**：本项目过去研究过的专业 Solana/Meme 调查项目/知识资产。
- **NousResearch Hermes Agent**：现在研究的通用 Agent Runtime 产品。

二者可以互相借鉴，但**不是同一个项目**。

---

## 4. 对 Blix 原有架构的实际修正

以前容易出现这样的理解：

```
Blix = 整个系统
  ├─ AI
  ├─ 知识
  ├─ 数据
  ├─ UI
  └─ 监控
```

现在应改成：

```
                    ┌──────────────────────┐
                    │       User           │
                    │  目标 / 价值 / 授权   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    AI Agent Layer    │
                    │ 理解·研究·判断·反证·复盘 │
                    └──────────┬───────────┘
                               ↓
              ┌────────────────────────────────┐
              │       Agent Runtime             │
              │ Hermes / Muse / Grok Bot / ... │
              └──────────┬─────────────────────┘
                         ↓
       ┌────────────────────────────────────────────┐
       │ Tools / MCP / API / Browser / Terminal    │
       └──────────────────┬─────────────────────────┘
                          ↓
       ┌────────────────────────────────────────────┐
       │             Blix Business Layer            │
       │ Market / Token / Wallet / UI / API / MCP  │
       └──────────────────┬─────────────────────────┘
                          ↓
       ┌────────────────────────────────────────────┐
       │        Evidence / Economic Data Core      │
       │ Tx / Instruction / Event / Wallet / Fund  │
       │ Flow / Token Account / Cross-Mint / ...   │
       └──────────────────┬─────────────────────────┘
                          ↓
       ┌────────────────────────────────────────────┐
       │       Case / Hypothesis / Opportunity     │
       └──────────────────┬─────────────────────────┘
                          ↓
                     AI 再判断 / 复核
```

这意味着以后 AI 看到 Blix 项目时，**不要因为 README 里写着“Blix 产品主体”就理解成“Blix 必须负责所有智能”。**

---

## 5. Meme 业务本身也要保持当前正确理解

系统真正要解决的不是：

- 做一个 K 线终端；
- 做一个钱包标签器；
- 做一个简单跟单 Bot；
- 做一个 AI 摘要器；
- 做一个知识库。

而是：

> **从 Solana Meme 市场中发现值得调查、尤其是具有实际参与价值的机会，并通过链上资金、钱包行为、Token、跨 Mint 关系和经济机制逐步解释“发生了什么、为什么发生、是否具有持续性、哪里可能判断错了”。**

核心调查链继续是：

```
Mint Discovery
→ Market Screening
→ Buy / Funding
→ Token Transfer
→ Receiving Wallet
→ Sell / Inventory
→ Onward Fund Flow
→ Another Mint
→ Cross-Mint Relationship
→ Economic Mechanism
→ Opportunity Judgment
→ Case
→ Recheck
```

结果至少区分：

1. **Worth Investigating**
2. **Actual Opportunity** ← 更重要

所有重要结论继续区分：

- FACT
- PLATFORM LABEL
- INFERENCE
- UNKNOWN

并保留：

- 原始证据；
- 竞争解释；
- 反证；
- 数据缺口；
- 时间；
- 来源；
- 当前判断；
- 后续复核。

---

## 6. “知识 → Agent”现在不应再做成知识库堆积

当前更准确的转换关系是：

```
旧知识 / 新研究
       ↓
专业判断依据
       ↓
Agent 能理解的 Context
       ↓
可调用的 Skill / Tool / MCP
       ↓
真实调查
       ↓
Evidence
       ↓
Case
       ↓
验证成功 / 失败
       ↓
修正 Context / Skill / 数据逻辑
```

因此：

**知识文件存在 ≠ Agent 已经掌握。**

**Skill 存在 ≠ Skill 正确。**

**AI 给出结论 ≠ 事实成立。**

只有经过真实任务和复核，才可以提升可信度。

---

## 7. 未来 Skill 应该如何形成

不要预先建立一大堆固定专家 Bot。

更好的方向是：

### 长期稳定知识

放在：

- Context / 项目说明；
- 小而稳定的 Memory；
- 专业知识文件；
- 数据模型和证据规范。

### 可重复操作

放在：

- Skill；
- MCP Tool；
- API；
- 程序。

### 临时判断

由 Agent 当前推理完成。

### 成功/失败后的新能力

只有当一个工作过程被实际验证具有重复价值时，才考虑沉淀为 Skill。

这与 Hermes 的 Memory / Skill 分工非常吻合，但**不能因为 Hermes 的设计如此，就机械复制它的所有机制**。

---

## 8. 当前不要做的事情

1. **不要马上把 Blix 重构成 Hermes。**
2. **不要马上把 Muse 删除。**
3. **不要因为 Hermes 看起来更强，就跳过真实任务验证。**
4. **不要重新建立一套庞大的“AI知识系统”取代现有 Blix。**
5. **不要把旧 Hermes 的推论直接变成事实。**
6. **不要把 GMGN / RugCheck / AI 标签直接当链上事实。**
7. **不要为了 Agent 架构先造大量 Bot、Skill、MCP。**
8. **不要把研究文件数量当作系统能力。**
9. **不要让当前只读/研究环境限制反过来删除 Blix 原版交易产品资产。**
10. **不要未经授权启用私钥、签名、广播、付款、真实交易或自动付费。**

---

## 9. 下一步真正应该验证什么

不是继续讨论“哪个产品理论上最好”。

而是做**同一任务、同一数据、同一标准**的 Hermes / Muse / Grok Bot 对照。

统一任务：

```
给定一个真实 Solana Meme 候选：

1. 发现问题
2. 获取市场数据
3. 获取 Token / Transaction
4. 识别关键钱包
5. 追踪 Buy / Sell / Transfer
6. 重建 Funding
7. 找 Receiving Wallet
8. 追踪下一跳资金
9. 查 Cross-Mint
10. 提出竞争解释
11. 找反证
12. 区分 FACT / LABEL / INFERENCE / UNKNOWN
13. 判断 Worth Investigating
14. 判断 Actual Opportunity
15. 生成 Case
16. 指出缺失数据
17. 给出下一步最高价值行动
18. 任务结束后判断哪些过程值得沉淀成 Skill
```

统一评价：

| 维度 | 检查 |
|---|---|
| 目标理解 | 是否理解完整业务，而不是只执行字面任务 |
| 自主性 | 是否自己决定下一步 |
| 工具选择 | 是否主动找到合适数据 |
| 调查深度 | 是否真正追到经济关系 |
| 反证 | 是否主动寻找自己判断的错误 |
| 证据纪律 | 是否区分事实/标签/推断/未知 |
| 记忆 | 能否延续上次工作 |
| Skill | 是否能把验证后的重复过程沉淀 |
| 长任务 | 能否持续推进而不丢目标 |
| Case | 能否形成可复核业务对象 |
| 缺口发现 | 是否知道自己不知道什么 |
| 可控性 | 用户能否控制模型、工具、权限和数据 |
| 成本 | VPS/API/模型/运行成本 |
| 安全 | 权限隔离、凭据、危险操作 |
| 可维护性 | 后续是否容易替换 Runtime |

**只有这个实验完成后，才决定 Hermes 是否正式成为主 Runtime。**

---

## 10. 当前架构结论

截至 2026-11-15：

> **Blix 继续作为当前建设基础；Agent Runtime 从“默认等同 Blix”中独立出来。Hermes Agent 是目前最值得验证的长期自有 Runtime 候选，Muse 和 Grok Bot 作为真实产品级对照与能力参考。**

如果 Hermes 在真实 Meme 调查任务中证明：

- 能持续理解目标；
- 能正确调用 Blix；
- 能使用 Solana 数据；
- 能进行深层调查；
- 能反证；
- 能形成 Case；
- 能沉淀有效 Skill；
- 能长期运行；
- 成本和安全可接受；

那么未来可以逐步形成：

```
Hermes Agent
    ↓
MCP / Tools
    ↓
Blix + Solana Data
    ↓
Evidence / Case
    ↓
Opportunity Intelligence
```

**这才是“把 Hermes 交给它”的正确含义，而不是把整个 Blix 项目搬进 Hermes。**

---

## 11. 权威性与更新规则

当未来 AI 进入本项目：

1. 先读取本文件，恢复 2026-11-15 的最新架构认知。
2. 再按任务读取 `docs/project/README.md`、`AGENTS.md` 和具体业务文档。
3. 不因为旧文件日期较早就删除旧知识；先判断它是历史事实、当前事实还是已被否证。
4. 不因为本文件较新就把其中的“候选/假设”当成已验证事实。
5. 如果真实测试否定本文件，应更新本文件并记录**为什么改、什么证据导致改、哪些旧结论失效**。
6. 新的产品研究应优先查看官方资料；产品能力与本项目适配度必须分开判断。
7. 本文件只负责恢复**当前架构认知**，不替代具体代码、数据模型、API 和测试文档。

最后更新：2026-11-15
