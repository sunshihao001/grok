# Blix AI Research Agent：保留原版产品的可选智能工作扩展（V0.1）

**定位**：Blix 仍是唯一市场产品主体。此扩展不新建行情终端、不重做钱包数据库、不替代原有的交易、UI、Research、Pulse 和服务端。复用现有 `server/intelligence/index.mjs` 与 `mint-facts` 能力，在其外增加模型驱动的任务编排入口 `server/intelligence/ai-workflow.mjs`。

## 第一条真实代码路径

`runAiResearchTask({goal, model, read, loadKnowledge?})`：

1. 普通语言任务包含**唯一** Solana Mint；没有 Mint 或有多个时返回 `NEEDS_SINGLE_MINT`，不猜测。
2. **外部显式提供**的模型适配器收到 `stage: 'plan'` 和允许使用的能力列表，生成调用计划；v0.1 只允许现有 `mint-facts`。
3. 调用前一次性验证所有工具、Mint 与调用次数。模型不能授权交易、请求未在用户目标中的新 Mint，或访问任意 URL。
4. 复用现有 Blix 的 Mint/Holder 读取能力，保留来源、缺失状态、Partial 和 UNKNOWN。
5. 可按任务调用外部专业知识检索适配器；知识片段只作为不可信资料，不作为工具授权。
6. 模型收到证据、知识和专业边界，输出摘要、竞争解释和下一项核查建议。整个模型结果永久标识 `UNVERIFIED_MODEL_INTERPRETATION`，不升级为链上事实。
7. 没有模型时返回 `MODEL_NOT_CONFIGURED`，不会偷偷调用收费 API；没有主动启动任何 Blix 服务或后台任务。

这里的模型适配器是函数 `async ({stage,...}) => object`，目前只做**注入接口**，没有接入 Grok、Claude 或其他付费 API。这样可以在具备用户授权的独立调用环境配置模型；切换模型不会让模型取得额外业务权限。

## 最小接口例子（离线测试环境）

```js
import { runAiResearchTask } from './server/intelligence/ai-workflow.mjs';
const result = await runAiResearchTask({
  goal: '调查这个 Mint 的持仓和不确定关系：<替换为真实Mint>',
  model: async ({ stage, mints }) => stage === 'plan'
    ? { calls: [{ capability: 'mint-facts', input: { mint: mints[0] } }] }
    : { summary: '待证据解释', hypotheses: [], alternativeExplanations: [], nextChecks: [] },
  read: async (path) => { /* 测试夹具；生产需要先审核安全读取服务 */ },
});
```

这段例子解释模型适配器的结构，不是已经连接模型或主网的数据实跑。

## 不扩散为重复架构

- **AI控制**：外部 Grok Bot/其他模型或将来的 Blix UI 只负责用户目标、研究规划、条件化知识和结果组织。
- **市场/证据**：Blix 原业务程序和 `server/intelligence` 统一能力入口。
- **连接**：优先复用已有 MCP/API 的获准能力；当前 MCP 不是完整的经济证据接口。
- **后续调查**：PR #23 的经济证据和独立 SQLite 报告仍是未合并候选；未来对接它时必须复用既有签名发现/重试/经济事件模型，不能另建平行采集账本。
- **原版交易保留**：扩展默认无交易权限，不删除原版交易程序。这是新扩展的权限边界，不是将原产品永久改成只读。

## 已验与未验

- 本扩展五项 **离线模拟/本地源码适配测试**：成功路径、越权工具/错误 Mint/重复调用拦截、缺 Mint/模型、模型失败和部分覆盖、与现有 `mint-facts` 的实际代码路径对接。
- 尚未做 GitHub Node 24 CI、模型真实 API、Grok Bot 安装、Blix UI、真实 RPC、单 Mint 全链验证、服务端硬只读隔离或连续运行验收。
- **特别注意**：当前原 Blix HTTP 的某些 GET 路由会触发内部数据采集/写缓存/供应商调用。此扩展的 allowlist 和 `readonly` 标签**不能**保证底层完整 Blix 服务无副作用。接入任何真实服务之前，必须先审查最小授权的只读读取通道、认证、花费限额和启动方式。

## 后续最有价值的真实交付

不是多建 Bot、插件框架或知识索引，而是在服务端权限隔离完成后：接入一个获明确授权的模型适配器，以一个真实 Mint 的自然语言任务贯通 **Blix 事实读取 → 可选专业知识 → 模型竞争解释 → 可复核报告**，记录成本、失败和来源，再考虑经济证据与跨 Mint 工作流。与 PR #23 的合流应先审查源文件和基线测试，不能直接假定 PR 已合并。

## 2026-11-10：Coin 页面上下文入口（已提交并完成前端构建）

- 原生 `CoinTabs` 新增独立的 **AI assistant** 标签，原有 `AI read`、行情、交易、持仓、Bubble Map 不变。动态导入 `AiCopilot.tsx`，避免页面初始加载所有扩展代码。
- 组件直接接收 `Coin({mint})` 传给 `CoinTabs` 的同一个 Mint，并由 `key={mint}` 重置编辑中的调查任务，避免切币串台。尊重原来的 `AiGate` 可见性/权限入口。
- 用户可选钱包关系、买入→转移→接收出售、Dev 与持仓、市场机制四类调查；可改写具体问题。
- 浏览器端**仅将当前已有页面事实整理成复制到剪贴板的研究任务**，保留源端覆盖标记、UNKNOWN 与既有 AI read 是模型观点的区分；不在页面自造可信链上历史。
- 严格标注 **Preview · agent not connected**。这不是已实现“在网页直接向 AI 提问并收到回答”，也未建立持久聊天会话或 HTTP Agent 执行入口。
- [Web CI #42815617467](https://github.com/sunshihao001/grok/actions/runs/42815617467)：Node 24 下 `npm ci --prefix web` 与 `npm run build --prefix web`（含 TypeScript type-check、Vite build、precompress）**成功**。

**下一步真实验收**：在现有能力注册/读侧硬权限隔离和模型费用授权完成后，把这个入口从“复制任务”接上受控 Agent 执行 API，实现连续工具调用、证据追溯、进度、取消以及结果回写。此前不要把入口称为可用的 AI 自动调查。
