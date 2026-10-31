# V4 运行模式选型与纵切片验收报告｜2026-10-31

## 决议与执行范围

从六种候选运行方式中，选择**事件驱动、快慢双循环、单一研究主管、按证据需要召集专家、独立反证回流**作为 Solana Meme 全市场工作流的首选架构。完整论证：[docs/dual-loop-research-runtime-architecture-v4.md](../docs/dual-loop-research-runtime-architecture-v4.md)。

**不采用**常态 17 个 Agent 全并行、将旧 Hermes 八层固定串行套入所有钱包事件、或直接将语言模型输出映射到真实交易动作。研发可有六种专业 Bot 职责，但初期正式运行计划是**一个只读 Monitor 入口、一个按需 Research Manager 入口**，专家能力通过既有知识与工具按需使用。

## 实际已经完成的执行

1. **新增 `src/solana_meme_os/research_dispatch.py`**：消费现存 M2 的 JSON 输出，在固定 `max_cases / max_source_checks / max_per_case` 下产生带资金源/钱包/Mint 时间窗作用域的静态专家研究计划。
2. **固定观察范围与时间**：`SAME_SLOT_MULTIWALLET_BUY` 用 Mint+Slot；`TOKEN_CONSOLIDATION` 用 Mint+接收者+窗口；`FUNDING_FANOUT` 用资金源+窗口；尚无独立时间窗的 `FUNDING_TO_BUY_CANDIDATE` 和跨 Mint 复用只报告 cohort aggregate，绝不自动与同时间别的 Mint 合并。
3. **重复证据预算复用**：多个不同 Case 都依赖同一 signature 时，只建议一次源交易核查，后续引用已提议的核查。
4. **稳态案例与版本**：`case_id` 与固定事件作用域绑定；晚到相同事件的签名只更新 `evidence_version`，不创造虚假的新事件身份。
5. **专家覆盖纠正**：原 `expert_router.py` 修复多场景只保留首个主责专家的错误；`knowledge/expert-capability-map.v1.json` 对两类之前未覆盖的 M2 候选建立资金到账→买入和 Token 归集专家组。六类已知 M2 候选现在可按 7 种场景配置路由。未知新协议仍走 `OPEN_DISCOVERY_REQUIRED`。
6. **知识检索纠错**：`research.py` 不再把“未知”这种过宽的单一关键词误当成某个外部源码与新问题具有专业相关性。
7. **新集成测试**：16 个调度单元测试、2 个从既有 M2 synthetic fixture 到调度计划的集成测试，并继承全部旧测试。

## 真实 CI 验收

GitHub Actions [`monitor-tests` run 41186104343](https://github.com/sunshihao001/grok/actions/runs/41186104343) 读取上述草案分支文件并执行：
- Python 3.12 / `unittest discover`：**108 tests in 0.115s，OK**；
- 原有 M2、仓位审计、知识、专家图、Funder/Cashflow、事件调度与端到端纵切片共同纳入；
- 该流水线为**离线回归环境**，不是远程 Grok Bot 云电脑、实际 Solana RPC 或实时市场性能验收。

本轮期间确实发现失败并修复：测试源文件转义换行语法错误、事件路由丢失另一场景 lead、知识检索误匹配新协议、测试默认预算未包含低优先级无签名任务；所有对应的用例均经过后续 CI 成功运行。

## 当前明确不能声称的能力

- M1 Solana 多协议原始交易/内层指令解析、WSOL CloseAccount、LP、桥、Block/Slot 真实覆盖；仍需落地。
- 云端持续任务调度、持久化队列、检查点恢复、RPC 重试/速率限制、Token 权限及签名无权限配置；还未在 Grok 云环境验收。
- 实际专家 LLM 多 Agent 执行、证据 claim 数据库存储和真实自动级联回滚；现只有静态图与待执行计划。
- 真实全市场基准、误报/漏报率、跨 Mint 经济网络、实际净收益；离线代码通过测试不是它们已成立的证据。
- 交易签名、广播、下单与主分支发布均未授权、未执行。

## 决策性下一步

不是优先增加 Bot，而是优先把一段**真实 Solana 指令与余额事实（含 WSOL/Token/Swap/LP、缺失/迟到来源）**导入现存 M2 规范格式，并留存原始签名、观察覆盖与首次可用时间。然后用真实发行总体对这套“快循环候选→慢循环核查计划→独立反证回流”进行同预算 A/B 验收，只有当效率与认知质量真实改善时再进一步部署云端研究调度。

**完成定义**：本轮已完成可运行的离线纵切片与 CI 回归；没有声称整套实时监控 OS 上线。主分支维持不变。
