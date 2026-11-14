# Blix 单一专业能力扩展层（渐进式整合）

**决定：Blix 始终是当前产品主体，不新建第二套市场终端。** 只明确一个扩展层：server/intelligence/。逐项整用成熟业务、有限适配或按需调用外部服务；不是把全部参考仓库源码搬到一个目录，也不是重建一套专家体系。

## 2026-11-14｜成品化实施主线：知识已经归位之后

**这一节是当前可执行交付判断；下方2026-11-06的`mint-facts`单一能力和“尚未接入UI”属于历史起点，不能覆盖已完成的PR23多能力与Coin导航。** Blix完整原版继续承担市场与用户终端；新增`server/intelligence/`是按需只读专业研究扩展，不是第二个行情采集器、钱包服务或交易引擎。专业知识主述已按[12领域](../../knowledge/README.md#2026-11-14全域专业归位总入口十二领域主述参考来源知识身份与产品验收)原位整理，不能把整理完成冒充模型已学会。

### 1. 产品要交付的三个可互相进入的实际使用场景

| 场景 | 用户看到的成品行为 | AI需要判断而原版不需要重做的工作 | 验收标准 |
|---|---|---|---|
| **市场→调查/机会（优先）** | 打开原Blix Pulse/Discover，候选说明为何出现、数据何时可得、为什么值得调查或暂不可交易 | 从原版筛选结果、钱包先行线索中选择调查深度；`research_priority`与`trade_readiness`分开；竞争假说及待查数据 | 有界市场候选/被排除对象、同源首次可见、拒绝理由和后续表现；可执行条件缺失时只输出UNKNOWN |
| **Coin→单Mint穿透** | 用户在原版Coin页点击AI扩展，Mint、问题与已观察市场上下文衔接；可打开交易签名/收转/接收后卖出和未知；结果保存 | 按问题选D01–D12的少量相关知识、只读证据工具、反例；不凭标签猜经济控制或同批售出 | 任意**用户指定**有效Mint（即使不在当前Pulse12候选中）可完成只读调查或准确报未归档；UI/HTTP/SQLite来源一致 |
| **Wallet→跨Mint/监控** | 从已跟踪钱包或图谱回查多币、地址角色/群体成员变化，保存观察案件并在新事实到来后更新 | 区分真实跨币资金对价、同地址、共享服务、动态仓位与滞后回补；更新受影响判断 | 有界真实签名与覆盖水位、持久Case重开、重复事件不重做与费用限额；不是从地址重合推同控 |

**双输出不能合并为信号**：研究优先级（异常是否值得弄清）与交易就绪（特定时间、池、金额、费用、可卖性是否具备评估依据）分别列出。AI结果只读/纸面模拟，不直接执行原版交易。知识的功能是改变调查问题与解释质量，不是替代源头事实或强迫所有币经过12领域。

### 2. 现有实现的真实状态（本轮核对源码/CI）

| 位置 | 已有可用的具体实现 | 限制和成品缺口 |
|---|---|---|
| 原版`server/` + `web/` | 原Pulse/Feed/市场与钱包触发、质量/Research/AI/Chart/交易/账户；SQLite；全新SQLite在**完全封网**Docker内可冷启、复启、HTTP health/pulse/UI通过，原代码保留 | 默认`npm start`因钱包/费用风险安全门禁仍会fail-close；真实市场源/网络/云端部署未验收 |
| `CoinAiCopilot` → `#/intelligence/:mint?goal=...` | 已有明确的Mint+问题深链接，不自动跑模型、无签名/支付 | 当前Intelligence `selected=candidates.find(...)`仍需Pulse已观察候选；不是任意Mint真正打开分析的闭环 |
| `Intelligence.tsx` + `pulse-discovery.mjs` | 用户触发从当前Pulse最多12观察候选中选一个Mint或拒绝，服务端校验候选；知识先于选择读取 | 浏览器提交时间不等于provider first-available；无完整源市场总体、同源未入选分母与实时机会率 |
| `start-intelligence-workbench.mjs` + `research-http.mjs` | 独立loopback 4547 HTTP，显式模型/SQLite配置和预检、任务/工具预算、Origin/Host校验；不导入原服务器 | 原版React常用端口4421未列入现有`DEFAULT_ORIGINS`（仅4420/5173），需在安全回归内补足；远程浏览器不能直接访问loopback，尚无安全HTTPS认证代理 |
| `local-knowledge-loader.mjs` + `ai-workflow.mjs` | 11个来源候选、默认3份知识片段、来源hash、至多2个单Mint只读能力；模型计划不能授权新工具 | 没有真实模型任务A/B证明选得对/用得对；模型API费必须独立授权与控制 |
| `offline-economic-reader.mjs` + `economic-claim-trace.mjs` | 读取**已有**SQLite经济表，局部转账/指令来源/接收者/卖出摘要与历史覆盖，不新建源 | 仅对归档证据成立；完整SOL资金路径、Swap+LP净对价、同批库存/成本和跨Mint资金闭环未真验 |
| `followability-replay.mjs` + `investigation-continuation.mjs` | 拒绝过期/不合格纸面报价及不完整退出；局部钱包状态与下一步关注建议 | 真实可交易报价/退出、可复制净收益和长期Case Watcher未运行，`NOT_RUNNING_NO_AUTONOMOUS_WATCHER`必须保留 |

### 3. 从现状到成品：按实际依赖交付，而不是再造系统

| 交付包 | 要完成的具体用户路径 | 依赖/负责组件（不复制已有能力） | 通过标准与止损条件 | 状态 |
|---|---|---|---|---|
| **P0-A 基座安全启动** | 全新Blix可以在隔离条件下真正启动/重启并提供网页/API | 原版`server/db/people`、原始web构建、测试与安全门禁 | 封网容器首次/重启成功，SQLite完整，`npm start`无授权fail-close；不等于联网安全 | **AIRGAP_RUNTIME_VERIFIED** |
| **P0-B 本地Coin→AI入口可用** | 任何合法Mint从Coin跳入AI页，不强制属于当前Pulse短名单；对“无本地归档”给明确状态，不错选另一枚币 | Coin路由、Intelligence、Research HTTP Origins、SQLite reader | 用本机4421与4547做不收费HTTP集成；目标Mint必须始终一致；伪模型+已保存测试样本；恶意Origin/越权拒绝 | **PARTIAL / 已找到两个具体入口缺口** |
| **P0-C 数据语义联通** | 从原Blix现有来源观察Mint→按时点归档→AI使用相同Mint与来源 | `sources/engine/coverage/db`为源职责；`intelligence`只读解释 | 先锁定用户授权的市场/SQLite；记录源时间、覆盖和缺失；模型不替数据源补采 | **UNVERIFIED_CONNECTED_RUNTIME** |
| **P1-A 一枚真实Mint完整经济纵切** | 买入→Token转仓→接收地址实际卖出摘要→潜在跨Mint资金事件 | 既有`economic-events`、`wallet-signature-coverage`、`economic-network`、局部历史补查 | 每个能确认的动作能回查签名/指令/净额；同批库存/资金不能确认就UNKNOWN；与原版行为/历史差异明确 | **OFFLINE_PARTIAL_ONLY** |
| **P1-B 两种优先级与机会评价** | 原Pulse/Wallet候选能分开解释研究价值和可参与性；信号可得后做只读成交模拟 | 原`triage/quality/research/quote/Paper`和`followability-replay` | 真实观察时点+指定金额下入/出报价+费用/滑点/不可成交样本，缺则阻止“盈利已验证” | **KNOWLEDGE_AND_PAPER_ONLY** |
| **P1-C AI适用性评估** | 一个问题自动选相关知识/工具，反例能改变或撤回解释 | D01–D12主述、11源只读加载器、`ai-workflow`，不添固定专家链 | 无知识/正确知识/错误知识同样数据、预算、模型设置，逐项比较事实错误/工具选择/成本 | **OFFLINE_MOCK_ONLY** |
| **P2-A 有界持续监控** | 用户保存Case并重开，真实新事件/迟到回补可准确更新结论 | 原Tracker/Journal/补查；新增必要的Case持久化/增量链接，不复写市场采集 | 至少一次重启+两次有区别的观察，新事件/补查分离，开关/预算/失败恢复可控 | **NOT_RUNNING** |
| **P2-B 实际发布/公平对照** | 同一市场时间与数据权限下原版A、确定性增强B、AI知识C的真实效果比较 | 授权运行机器、源/模型许可、认证HTTPS/限额/监控、可回滚版本 | 延迟、漏报、误报、净可参与条件、成本和故障恢复均有收据；无优势时缩减复杂度；生产与交易另授权 | **NOT_DEPLOYED** |

**最短成品路径**（不同于完整O1–O6全部达成）：

- **本地可演示V0.1**：完成P0-B，使用**已有合法SQLite**和伪模型/不收费离线适配实现原Coin→Intelligence→只读报告，证明UI、服务、数据和Mint身份不丢失；本地没有真实归档时只能演示`UNAVAILABLE`，不得伪称完成链上调查。
- **真实只读V0.2**：完成P0-C+P1-A，用一枚实际归档Mint和既有可授权源，把Blix观察→签名事实→钱包/库存候选→AI报告真正贯通，记录coverage/UNKNOWN；再检验与原版的实质增量。
- **业务验证V1候选**：完成P1-B/P1-C和有界P2-A，证明候选发现/过滤与实际调查增益，才讨论远端授权部署和长期可运行；“能发现可盈利机会”需要前瞻样本外验证，不能在这些工程阶段提前宣称。

### 4. 必须在工程责任原位置修复的缺口

1. **原数据源缺/错/断流**：`sources/engine/livetrades/coverage`等已负责采集恢复；先验证原代码已有能力与费用/许可，再在其位置修复，AI只接有来源+覆盖的只读结果，不维护第二套市场源。
2. **Solana原交易解析不完整**：交给原始交易与`economic-events`源级责任，保留全raw/CPI/ALT/Owner；AI不通过Prompt“补出”未捕获Transfer。
3. **AI选错知识/推断越级**：`local-knowledge-loader/ai-workflow`和证据校验承担责任；先用可复算反例测，避免加常驻Expert Agent。
4. **成品UI入口不通**：前端route、Origin、Mint选择、服务健康和错误提示都应在本来现有模块修；不得仅凭导航链接就称已端到端。
5. **安全与成本**：旧Blix完整交易源码必须保留，但其默认入口不得被“只读扩展”随意解锁；研究模型费用、用户权限、远程HTTPS认证和资源预算各自明确，不因容器内封网启动成功便上线公网。

### 5. 本轮建设裁决与下一次执行起点

**先处理P0-B的两个有代码指向的具体问题**：原版Blix网页`4421`与sidecar允许的Origin不一致；Coin手动指定的Mint不在当前Pulse观察列表时，研究按钮无法按指定Mint工作。可先通过不收费/离线回归校验最小修复，同时保留“浏览器市场未观察到该币”的事实，不能虚构候选行情。之后使用一个可证明存在经济原文的真实Mint SQLite进行P0-C/P1-A，才值得启用真实模型API并核预算。

**禁止的假成品路线**：全量注入152单元/安装全部GMGN Skills/造第二个扫描引擎/绕过原版安全门禁/自动签名交易/在无可得报价时生成收益结果。真实发布和外部模型供应商的任何费用仍需明确权限。工程每轮最新状态只更新[建设台账](build-register.md)，本节保持相对稳定的产品验收合同。

## 产品边界
- **Blix 本体**：原有市场发现、UI、SQLite、钱包观察和事件历史；不复制其已经成熟的同类实现。
- **专业能力扩展层**：每个能力有唯一 ID、输入、来源、缺失状态、经济语义限制和可执行测试；通过入口按需加载。
- **专业知识和 AI**：按实际调查问题调用 Hermes/qb-/meme-、D01–D12、ai-d 和外部专业证据，负责解释、反证与建议；不要求把原研究全部灌入一个模型上下文。
- **使用界面**：后续在 Blix 现有 Coin Sheet、Wallet Tracker、Research 中呈现事实与推断，避免增加重复主页。

## 第一个可执行能力：mint-facts

\`server/intelligence/index.mjs\` 是唯一加载入口，采用明确的 allowlist；只有调用 \`runCapability('mint-facts', …)\` 才加载模块。

\`mint-facts.mjs\` 利用已有本地 Blix API：
- \`GET /api/token/:mint\`
- \`GET /api/holders/:mint?top=25\`

返回统一的 \`sources\`、\`facts\`、\`unknowns\`、\`status\`。保留 Blix Holder 部分覆盖以及原始 dev/sniper/bundle 标签，但**不升级为同一经济主体、已证实内幕关系或交易优势**。源端 API 响应未独立链上核实，不能写成 \`CHAIN_VERIFIED\`。

\`server/intelligence/local-reader.mjs\` 只允许连接127.0.0.1的这两个 GET 路由，不接受任意 URL，不导入 Blix 的主服务器、账户或交易模块。CLI \`npm run inspect:mint -- <Mint>\` 只会显式请求已经启动的本地服务；不会启动 Blix，也不会调用外部研究模型。

## 隔离条件与局限
- 现有 \`npm start\` 默认阻断继续有效，**新扩展层不意味着原 Blix 已经可以安全启动**。
- \`import()\` 是按需加载，不是安全沙箱；后续引入新的程序前必须审查依赖、网络、收费、签名和副作用，必要时做进程隔离。
- 本层只有一个确定的业务能力，尚未接入原 HTTP 路由或 UI，更没有真实 Mint 主网验收。
- **单层只是统一接入点**，将来若存在多个数据模块，优先通过能力契约接入，不再扩建重复底座。

## 逐步扩展原则
按信息价值和成熟度依次考虑：
1. **现成 Mint/Creator 调查**：优先尝试 PumpTrace 完整接口与历史回填。
2. **双向 Wallet/Mint 与资金关系**：对照 Million 的成品工作流与历史覆盖。
3. **跨 Mint 时序群体**：仅在有真实事件历史、成员演化证据时加载，不能把市场成交日志当成全部转账。
4. **经济机制研究**：独立给出竞争解释、UNKNOWN、反证、数据遗漏及可推翻条件。

每加入一项，只需证明：它解决真实业务缺口、与现有接口和数据语义兼容、不产生未经授权的交易或费用、单项测试通过，并最终完成完整产品 UI 与实跑验收。
