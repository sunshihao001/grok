# Blix 独立 AI 工作台｜本机只读研究服务（2026-11-13）

> **当前实现形态：独立的 opt-in 本机服务 + 已有 Blix React Intelligence UI + 已有 PR#23 单Mint离线经济证据工具。**
> 模型 API 已有真实 HTTP 适配代码，但仓库、CI 和此次建设**没有运行任何收费模型**，也没有绑定用户密钥/数据。实际云端模型与真实市场端到端效果 **NOT VERIFIED**。这是受控研究入口，不是机器人交易、全市场自主扫描或已经证明盈利的策略。

## 2026-11-14｜Coin指定任意Mint的本地只读路径（PR#23当前实施）

- 原版Coin助手通过\`#/intelligence/:mint?goal=...\`传入**用户明确选择的Mint**。即使此Mint没有出现在当前Pulse列表，也不会回退到其它代币；前端只显示其原始地址和**Pulse行情UNKNOWN**，不能编造市值、Holder或数据源。
- 仅当用户主动点“调查指定 Mint 的本地经济归档”、本机4547的\`/health\`已配置、且显式模型费用开关已开启时才准备请求；网页本机地址\`localhost\`与\`127.0.0.1\`均可使用，服务默认允许原版本地4421 React来源和已登记的开发来源，仍禁止陌生Origin/Host、公网访问或交易功能。
- **付费模型之前第二次独立预检**：\`probeExistingEconomicMint\`在指定的**现有SQLite**文件以\`readOnly:true\`和\`PRAGMA query_only=ON\`检查\`econ_instructions\`或\`wallet_trades\`中此Mint有无索引行；如果没有则HTTP返回\`422 MINT_LOCAL_EVIDENCE_UNAVAILABLE\`及\`MINT_NOT_INDEXED_IN_EXISTING_ARCHIVE\`，**不调用模型、不消耗任务额度、不创建或修改数据库**。没有本地行只代表当前归档未见，不代表链上无活动或完整覆盖。
- 上述功能由真实HTTP+伪模型、临时SQLite不可变哈希、Mint不串币单元测试和React build验证。**仍未独立完成真实浏览器操作+真实主网归档+真实收费模型的完整E2E**；后续应优先使用经许可现成归档，不能靠AI补造数据或擅自开启真钱/收费服务。

## 一、什么已经接通

```
Blix React /#/intelligence （已有Pulse观察候选）
  [用户点击“运行本地 AI 证据研究”]
    → http://127.0.0.1:4547/research（独立服务，默认不自动启动）
      → ai-workflow.mjs：同一Mint、最多2次工具调用
        → local-knowledge-loader.mjs：11个固定已有专业来源
        → chat-completion-model.mjs：通过显式配置的服务端 Chat Completions API
        → mint-economic-evidence.mjs：仅通过现有SQLite只读CLI
    ← 模型草稿、已读取的工具事实、来源/签名/钱包关系、知识阶段轨迹、UNKNOWN
  [界面显示真实收据和局部钱包流，不声称经济控制/完整历史/Alpha]
```

原版 Blix 的 Coin K线、Bubble Map、Wallet、Paper、交易和部署入口不被替换或导入。新服务不会启动原版`server/server.js`，不会执行签名、下单、钱包监控、Token自动收录或广播。

**重要设计取舍**：`/api/token/:mint` 虽是 GET，在原版Blix内可能触发Mint查询、收录与安全检查。首版模型服务因此**只允许已有的`mint-economic-evidence`本地只读能力**，不授权`mint-facts`的潜在副作用HTTP GET；以后需有可证明只读、来源有时点/覆盖标识的快照接口，才可开放扩展。

## 二、部署者在本人受控环境中显式启用

前提：Node 24.16+；有现成、得到授权的 Blix SQLite 归档，且它已包含 `econ_transactions`、`econ_instructions`、`wallet_trades` 等表。若没有这些表，研究只会报告`UNAVAILABLE`，不会自动创建数据库或向 RPC 抓数据。

**只启动健康检查服务，不会联网调用模型（默认配置）**：

```sh
npm run start:intelligence:readonly
```

查看 `http://127.0.0.1:4547/health` 返回 `ready:false`：这代表没有同时完成只读归档和人工许可的模型配置，**不是故障**。服务端目前还有一个**不涉及网络或模型付费的启动前置检查**：部署者配置 `BLIX_AI_DB_PATH` 后，使用 Node SQLite `readOnly:true`、`PRAGMA query_only=ON` 检查文件确实存在，并核对 `econ_transactions`、`econ_instructions`、`wallet_trades` 的必要字段。若文件不存在、不是 SQLite 或表结构不满足，`/health` 返回 `ready:false` 和不包含本地路径的 `archiveStatus`；`/research`/`/discover` 在调用任何收费模型或消耗任务配额之前直接返回 503。

即使 `ready:true` 也**只表示该模型调用已配置且现有归档结构可读**，不保证某个 Mint 有交易、钱包历史完整、外部模型 API 真实可达或利润可验证。未配置模型时启动本机服务仍为安全健康检查，不会请求模型。此修复是**独立 AI 服务**的保障，**没有**将原版 `npm start` 变成只读或安全隔离运行；原版完整服务中的交易、钱包与自动模型费用风险继续由 `read-only-audit.mjs --gate` 拦截，不能以设置确认环境变量冒充安全认证。

**只有部署者已明确同意支付模型API费用并准备好了密钥与已有数据库，才自行配置环境变量**（以下是示意，密钥不应写在仓库、网页或命令历史中）：

```sh
export BLIX_AI_DB_PATH='/absolute/path/to/already-existing-blix.sqlite'
export BLIX_AI_MODEL='your-supported-chat-completions-model'
# BLIX_AI_API_KEY: 由本机安全的环境/机密管理设施注入
export BLIX_AI_ENABLE_PAID_MODELS='I_ACCEPT_MODEL_API_CHARGES'
npm run start:intelligence:readonly
```

`BLIX_AI_CHAT_URL` 可选：默认为 `https://api.openai.com/v1/chat/completions`。仅接受 HTTPS 的`/chat/completions`端点，或本机 `http://127.0.0.1[:port]/.../chat/completions`；**URL来自服务启动环境，不接受模型/网页请求传入任意地址**。兼容性只针对 Chat Completions 的 `response_format:json_object`、`max_completion_tokens` 约定，不保证每个厂商、每一代模型都兼容；其他模型协议需独立适配。调用时仅把用户的研究目标、允许工具名称、有限的知识段落和简化的经济证据发送给已配置模型服务商；因此**研究内容可能离开本机**，部署者需先认可数据发送及该供应商条款。

`BLIX_AI_PORT` 默认 4547，`BLIX_AI_MAX_TASKS` 默认每进程8个**用户手动发起**的研究任务；每项研究至多2次工具读取、手动单Mint任务最多3次模型请求（计划/补查/解释）；自主选取市场候选的任务额外最多1次模型请求，且不自动重试，服务一次仅处理一个任务，模型响应输出有上限。进程重启会重置预算计数，**不是跨进程严格计费控制**；实际提供商账单、配额和密钥管理仍须在服务商端设置。默认CORS仅允许原版本机 `http://localhost:4420`/`http://127.0.0.1:4420` 和本地 Vite 5173。 `BLIX_AI_ALLOWED_ORIGINS` 仅用于由部署者配置明确的 Origin 白名单，不能写`*`。只监听 `127.0.0.1`。

## 二点五、AI 自主选择市场调查对象（新接入）

**用户主动触发，不是后台不间断扫描。** 工作台复用**原Blix浏览器内当前Pulse已加载的观察候选**，从完整的市场看板阶段顺序取至多12个Mint（不是12个最有机会的Mint），按用户问题通过 `POST /discover`提交到独立本机研究服务。

- 仅当Pulse实时流或轮询在工作、当前页面已接收市场数据时开放；绝不以浏览器恢复的过期缓存自称实时。
- 服务端严格校验Mint/阶段/字段/去重/候选数量/网页提交时间；网页记录的时间**不是**提供方实际观察到价格、成交和流动性的时间，报价仍可能较旧。市场范围仅为本次提交的候选集合，**不是全Solana市场覆盖**。
- 模型 `stage:'discover'` 在这12个候选中选择**一个值得进一步调查的对象，或者返回null**。选择前会复用 `local-knowledge-loader.mjs`，按当前目标取少量Hermes/meme-/ai-d等已有专业知识，记录`knowledgeUse`；文档只影响调查问题而非真实市场事实。
- 模型选出的Mint必须属于提交候选，否则拒绝且**不会调用经济证据工具**。通过白名单后才进入原有单Mint `runAiResearchTask`；该流程仍只调用现有本地SQLite离线读取工具。
- 模型可选择`null`；此时显示调查拒绝原因，不造出一个收益机会。因多一个模型选择阶段，每个自主发现请求可能最多触发 **4次** API调用（发现+规划+补查+解释），但是仍受同一8任务每进程预算约束；费用需在模型供应商侧设置更强限额。
- 返回`continuation`是**对已有归档证据的确定性整理**：关键Owner候选、可能的跨Mint时序边、后续卖出摘要、无法定价的跟单价值与可能的观察钱包，不会自行创建监控任务。六阶段中的“未知/尚未运行”不能误读为“没有发生”。
- 发现阶段AI所见的行情快照来自用户浏览器，属于**不可信数据输入**；服务端不能仅凭这些字段证明可成交、完整交易历史、钱包同控或盈利机会。没有可靠信号可得时间/进出报价和完整退出，本版所有候选的`verifiedMarketOpportunity`均为`false`。

## 三、网页的真实限制

- 打开**本机HTTP** Blix工作台 `#/intelligence`，左侧选一个来自原Pulse的Mint，右侧输入自然语言目标。
- 研究按钮仅在本地服务健康检查显示 `ready:true` 时启用；点击后以JSON提交`mint`和`goal`。不会自行提交交易或付费网络调用。
- 中间研究结果区显示真实`result.evidence`、`result.knowledgeUse`、本地钱包转移边、未知项及模型解释。知识来源“已提供给模型”**不等于正确使用或证据支持**。
- 目前没有跨Mint实时自主搜索、持久案例库、真实行情入出报价、模型策略收益证明；仅显示当前本地经济归档可读的记录。没有相关归档时不得声称查无关联。
- **公开 HTTPS Blix / 手机远程浏览器不会自动连接本机4547服务。** 不要为了方便把4547端口监听到公网。要让远程用户真正使用，必须先做带认证、授权、限流、独立只读能力门禁的 HTTPS 后端/反代，并经过隔离与威胁测试。
- 本地研究HTTP显式验证 Origin + Host + Loopback；只是本地使用的防护，不是适用于多人公网或跨用户隔离的完整认证。

## 四、测试和证据边界

```sh
npm run test:intelligence
npm test
npm run test:security
npm run test:evidence
npm --prefix web run build
```

`test/intelligence-workbench-http.test.mjs` 使用伪提供商`fetch`和合成的本地证据归档，在真正不调用付费模型的条件下验证：模型API请求/JSON契约、API密钥仅在服务端、非法Endpoint拒绝、非法Origin拒绝、未配置模型不可运行、任务次数限制、恶意知识尝试请求交易工具被拒绝、查询返回实际知识阶段日志与局部钱包关系。以上都是**OFFLINE_MOCK_HTTP**验收；不能声称真实API供应商或真实Solana主网验证通过。

后续优先事项：将原版Blix市场时点、历史经济证据、无副作用只读行情视图及研究案例关联起来；先在一枚有真实原始交易签名的Mint上验证请求→RPC原文→钱包关系→模型解释→可视化，而不是先扩大Agent权限或增加知识专题数量。
