# Blix 独立 AI 工作台｜本机只读研究服务（2026-11-13）

> **当前实现形态：独立的 opt-in 本机服务 + 已有 Blix React Intelligence UI + 已有 PR#23 单Mint离线经济证据工具。**
> 模型 API 已有真实 HTTP 适配代码，但仓库、CI 和此次建设**没有运行任何收费模型**，也没有绑定用户密钥/数据。实际云端模型与真实市场端到端效果 **NOT VERIFIED**。这是受控研究入口，不是机器人交易、全市场自主扫描或已经证明盈利的策略。

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

查看 `http://127.0.0.1:4547/health` 返回 `ready:false`：这代表没有同时完成只读归档和人工许可的模型配置，**不是故障**。

**只有部署者已明确同意支付模型API费用并准备好了密钥与已有数据库，才自行配置环境变量**（以下是示意，密钥不应写在仓库、网页或命令历史中）：

```sh
export BLIX_AI_DB_PATH='/absolute/path/to/already-existing-blix.sqlite'
export BLIX_AI_MODEL='your-supported-chat-completions-model'
# BLIX_AI_API_KEY: 由本机安全的环境/机密管理设施注入
export BLIX_AI_ENABLE_PAID_MODELS='I_ACCEPT_MODEL_API_CHARGES'
npm run start:intelligence:readonly
```

`BLIX_AI_CHAT_URL` 可选：默认为 `https://api.openai.com/v1/chat/completions`。仅接受 HTTPS 的`/chat/completions`端点，或本机 `http://127.0.0.1[:port]/.../chat/completions`；**URL来自服务启动环境，不接受模型/网页请求传入任意地址**。兼容性只针对 Chat Completions 的 `response_format:json_object`、`max_completion_tokens` 约定，不保证每个厂商、每一代模型都兼容；其他模型协议需独立适配。调用时仅把用户的研究目标、允许工具名称、有限的知识段落和简化的经济证据发送给已配置模型服务商；因此**研究内容可能离开本机**，部署者需先认可数据发送及该供应商条款。

`BLIX_AI_PORT` 默认 4547，`BLIX_AI_MAX_TASKS` 默认每进程8个**用户手动发起**的研究任务；每项研究至多2次工具读取、最多3次模型请求（计划/补查/解释），且不自动重试，服务一次仅处理一个任务，模型响应输出有上限。进程重启会重置预算计数，**不是跨进程严格计费控制**；实际提供商账单、配额和密钥管理仍须在服务商端设置。默认CORS仅允许原版本机 `http://localhost:4420`/`http://127.0.0.1:4420` 和本地 Vite 5173。 `BLIX_AI_ALLOWED_ORIGINS` 仅用于由部署者配置明确的 Origin 白名单，不能写`*`。只监听 `127.0.0.1`。

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
