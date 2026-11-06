# 按实际问题使用专业知识、AI研究与可证伪证据

## 知识来源与正确定位
| 入口 | 贡献 | 限制 |
|---|---|---|
| [ai-d PR #1](https://github.com/sunshihao001/ai-d/pull/1) | 多层目标/七并行能力、目标纠偏、知识选择、专家认知提取、研究后再思考 | Draft；未证明自动 Agent、跨模型提升或专家技能已经迁移 |
| [grok PR #14](https://github.com/sunshihao001/grok/pull/14) | D01–D12、旧专家视角、152问题与65资产的历史入口 | 登记不等于全部已验 |
| [grok PR #16](https://github.com/sunshihao001/grok/pull/16) | 原始交易解析、单 Mint 真实供应商预览与离线监控研究 | **不是 Blix 已集成的真实持续监控** |
| [grok PR #17](https://github.com/sunshihao001/grok/pull/17) | 目标演变、UI信息设计、知识导航、业务集成研究 | Draft，非 Blix 当前代码 |
| [Hermes](https://github.com/sunshihao001/-)、[qb-](https://github.com/sunshihao001/qb-)、[meme-](https://github.com/sunshihao001/meme-) | 钱包角色、资金循环、单 Mint 报告、经济机制与旧失败经验 | 不自动视作安全可运行成品 |
| [Why-Solana](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | 同源/多跳/群体协同、公共设施排除、选择偏差与反证 | 结构关系不等于真实经济主体或收益优势 |

旧知识保留原位，禁止为“让 AI 理解”将所有 Markdown 全量注入上下文或从头复建专家制度。

## 专家认知怎么进入实际产品
ai-d 最新研究区分 **知识摘要 → 问题表征/判断方法 → 经外部任务检验的实际能力迁移**。当分析一个 Mint，AI 应先明确当前用户问题和经济机制；仅提取相关研究里的必要线索、决策依据、适用/失败条件，并用交易事实及对照反证验证，不能假装理解专家不可观察的内心过程。

## 常见问题与正确知识调用
- “12小时钱包转账突然增多” → 先查可得历史、钱包名单变化、签名/资产净变化；再比较资金准备、做市、出货、Dust、公共Hub、数据回补等机制。
- “捆绑钱包占多少” → 分同Slot、真实可确认Bundle、初期买入供应占比、当前持仓；分母/窗口/Pool/Owner必须明确。
- “A买入、B接收、C卖出” → 交易签名、指令位置、Swap/Transfer和接收路径；不能直接把三地址确认为同控。
- “要新增一个专业模块” → 先研究原 Blix 是否已有；外部成熟整用/薄接口/有限适配/内置四种路线按成本与证据选择。

## 输出与数据证据的最低语义
区分 `USER_CONFIRMED`、`SOURCE_READ`、`AUTHOR_REPORT`、`SUPPLIER_RETURN`、`OFFLINE_TEST`、`LIVE_READ_ONLY`、`PRODUCTION_VERIFIED`、`INFERENCE`、`HYPOTHESIS`、`UNKNOWN`。保留来源、签名及事件位置、Slot、事件和采集时间、资产单位、覆盖/缺口、正常竞争解释、可推翻条件；无数据不能当0活动。

**每项重要成果后再想一次**：有没有比原方案更成熟的产品/算法/机制解释？新认识改变哪个上层目标或执行选择？比较少量实质方向并推荐首选；若没有增量，就继续当前路线，不为凑选项创造伪问题。
