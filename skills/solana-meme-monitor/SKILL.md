---
name: solana-meme-monitor
description: Read-only Solana Meme Mint investigation and source-linked observation; run existing Python commands, verify evidence, and explain uncertainty. No trading.
---

# Grok 主Bot｜按需单Mint调查与观察（调用现有程序）

**实际运行门槛：** Grok云电脑中必须有已审查的 `sunshihao001/grok` 工程PR #16工作树、Python 3.11+及可访问的只读数据源。GitHub代码/Skill文件存在不等于Grok已经安装/执行；先记录 `git rev-parse HEAD`，不得把Actions结果充当Grok运行结果。

**优先级原则（成品先于研究）**：收到普通自然语言请求时，**先理解用户实际想完成的使用场景，并尝试已有可运行成品能力**，而不是默认拓展知识库、召集专家或新建功能。自主提出用户未想到的高价值产品想法、可直接使用的成熟完整业务及替代方案；按运行证据、覆盖、成本、只读安全与可验证用户结果选择，不固定依赖Million/OKX/Pulse/某个框架。用户要求全市场发现时不得强行缩成“先输入单Mint”；单Mint命令是已存在的按需调查入口，不是唯一默认产品形态。真实监控数据不足不得伪称上线，仍可交付部分结果；只有被验证的运行能力可以作为已具备的功能。

## 模式C：用户提出“发现今天热门币、过滤批量盘、持续异常监控”——全市场产品场景

**这是正式产品目标，不应被模式A的单Mint入口取代。** 将市场发行、低质量盘识别、当天热度、代币/钱包/资金异动、事件触发的深度调查、历史反馈作为同一产品的相互连接行为；允许钱包或开发者异常反向发现代币，而非固定线性阶段。

1. 先查当前已运行能力和旧成果，按完整业务能力横向比较Pulse、OKX、Million、pumpwatch、HoldTech、Cielo等以及新发现的成品；能完整调用优先调用，其次有限组合；禁止因示例列名排除其他候选。
2. 要得到当天候选时必须有**真实且有时间戳的市场输入**，逐次记录候选Mint、来源、筛选理由、缺失信息与误杀复查入口；不能用历史fixture、单Mint快照或宣称存在的第三方接口冒充实时自动扫描。批量发行、Holder集中度和钱包同控均需区分地址/池/Token账户与经济主体。
3. 有真实事件、稳定时间语义和可核实交易信息时，才触发成熟钱包/资金调查，并复用现有只读Mint报告与证据包。当前模式B的离线窗口**不能**被声称为真实持续监控；没有全天候采集与重连补录证据时标记未验。
4. 每轮自主选择最能缩短距离用户可用产品的实施或验证动作，记录实际执行、版本、输出、可复现测试、未完成项。不要用规划文字、角色数量、知识索引或虚构榜单代替运行成果；用户无需懂产品与开发技术。

## 模式A：用户提出“分析这个 Mint”或“调查这枚 Meme”——成品入口优先

先运行**已有产品单命令**，不需要先让用户理解两条CLI的拼接，也不创建额外Bot、重写解析器或搭建MCP服务。以下在工程PR #16仓库根目录执行（Mint从用户输入取得）：

```bash
PYTHONPATH=src python -m solana_meme_os.product <REAL_SOLANA_MINT>
```

程序仅组合原有`mint_v01`与`vendor_event_handoff`，自动创建新运行目录，返回`run_status.json`路径、`mint/report.json`、`mint/report.md`及（来源校验通过时）`grok-outbox/evidence.json`。运行阶段不发起任何Grok调用、不签名、不交易、不自动付款。

**判定本次运行能否交付**：
- **exit 0 / `READY_FOR_GROK_REVIEW_NOT_EXECUTED`**：两个来源的原始文件完成身份/哈希核验。你必须实际读取`report.md`、`report.json`、`evidence.json`，结合项目现有专业知识及可用X资料独立调查，单独保存`grok_analysis.md`。只有真的在Grok云电脑执行和回读，才能把Grok执行状态记为通过。
- **exit 4 / `PARTIAL_MINT_REPORT_NO_GROK_HANDOFF`**：只取得部分来源时，基础Mint报告仍可查看；解释缺失来源，不声称已完成多源核查、钱包调查或Bot分析。
- **exit 2/3**：数据采集/验证或运行目录错误，读取`run_status.json`或失败输出并说明原因，绝不补造数据。

**本阶段能给用户什么**：真实公开池与缓存Holder/Creator候选、供应商标签及时间/来源、跨源池基础设施候选抑制、可复查的风险问题；没有真实交易签名时不得声称已经识别操盘手资金、Token出售、钱包群体异动和可交易收益。X不可用时标`X_RESEARCH_UNAVAILABLE`。正式产品功能优先于新增专家、阶段或研究制度。

**可以按需进一步使用**：旧两条独立CLI仍然保留，供指定来源/排错和复盘；未来由用户实际需要再调用经过授权的Million/OKX等完整只读业务，而不是把来源缺失自动变成自研新适配器。实际交付应包含本次程序退出状态、Git SHA、文件路径、时间、可靠事实、竞争解释和一个最有价值的后续行动。

## 模式B：用户请求“观察变化/追踪钱包”

目前仅有 `solana_meme_os.monitor`（规范化观测输入）和 `wallet_batch_monitor`（fixture-only的1/5/15分钟经济事件聚合），**尚无真实、可靠的持续链上事件流**。

1. 先确认观察来自被允许的数据来源、时间/字段单位、Mint地址和覆盖范围；仅真实归因的交易事件才可交给批次监控。不能把模式A的供应商快照变成已确认的BUY/SELL。
2. 对已有合法观测文件运行：
   `PYTHONPATH=src python -m solana_meme_os.monitor --input OBSERVATION_PATH --state-dir .runtime`
   `--allow-fixture`只能用于明确标注为演示的离线测试。
3. 依据已记录的状态变化、来源和竞争解释输出观察报告。数据缺失或断开时报告UNKNOWN，不输出“该钱包停止交易”的肯定结论；不因Grok的Routine存在就称真实监控已上线。
4. 只有经过**真实观察两时点、缺失恢复和重复事件核验**，且用户要求持续扫描，才考虑已授权的Routine；Routine创建/启用与云电脑运行仍需在Grok端逐项验收。

**专业知识选择**：按当前任务调用相关D01–D12或已有专家视角即可，**不强制22位专家会诊、六Bot启动或固定阶段流程**。专业意见必须能改变经济解释或下一步核查。相关资料保存在 `knowledge/` 和旧参考仓库。

**安全边界**：仅只读网络查询、既有审核过的CLI和本地报告。禁止私钥、交易签名/广播、购买服务、自动付款、安装未经审查代码、未经用户授权的对外发布或把X营销利润当事实。

**工程测试（不是Grok云端验收）**：`PYTHONPATH=src python -m unittest discover -s tests -v`；真实GitHub Actions双来源采集与交接证据见 `.github/workflows/one-shot-public-rpc-holder-20261101.yml`。
