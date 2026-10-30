# 研究导航与多 Bot 交接契约

## 一、每次提问先拆三种不同命题

1. **结构命题**：某几个地址/资金路径是否出现统计异常？如何排除服务商、CEX/HUB、共同市场事件？
2. **预测命题**：在决策时刻已知的信息，能否对未来市场结果提供可复验的增量？
3. **经济命题**：在特定延迟、仓位规模、路由与退出约束下，是否有正净期望？不能用 ATH、MFE 或预测命中率替代成交收益。

某个领域只证实第一种命题时，不能跃迁至第三种。对观察到的模式也必须报告「不知道」。

## 二、Bot 职责与知识接口

- **Rule Architect**：领域路径、知识 ID、可证伪假设、适用总体、停止条件、规则版本，禁止先调阈值再写实验问题。
- **GMGN Data**：raw/provider schema、UTC/Slot、单位、字段含义、缺失/失败、与链上双源比对；不提供「庄家实名」标签。
- **Wallet Structure**：D04/D05/D06/D07 的图结构、负对照、公共 HUB、资金重用、出口钱包；分离行为与身份。
- **Evidence & Gate**：区分事实/报告/推断，比较反证，明确结构信号/预测信号/经济性与禁用未来信息。
- **QA / Fixture**：怀疑数据泄露、选择偏差、批处理读错、RPC 403 变空集、时间聚类、多次搜索带来的偶然高胜率；运行不含结论的盲测。
- **Monitor**：只消费经批准冻结的只读观察规则；遇到知识不足触发 Research Gap，不生成交易动作；引用 `knowledge_ids`、规则版本和来源。

任何 Bot 交接需包含：`question`、`domain_ids`、`knowledge_ids`、`source_refs`、`decision_cutoff_utc`、`population`、`observations`、`alternatives`、`counterevidence`、`missing`、`economic_assumptions`、`falsification`、`next_action`。

## 三、第一组外部反证实例的真正启发

`research-units.v1.json` 记录 3 条 **外部报告**（SRC-WHY）：协同资金结构可识别、统计命中率与净收益可能分离、特定负结果有样本/功效边界。这些记录帮助我们**改变提问和实验设计**，不能自动变成买卖规则，也不能外推为「所有 Solana Meme 无利可图」。

下一批可优先提出（均属开放假说）：资金再分配是否在目标代币可确定之前提供信息；协同退出后是否出现独立资金承接/二级阶段变化；高风险过滤器能否在维持机会覆盖率的情况下改善跟单者净收益。每一项先设计零假设和反例，数据覆盖不足就保持 UNKNOWN。

## 四、发布制度

开发 Bot 只能写候选与实验；独立审阅者检查时点、总体、选择偏差、经济成本与原始交易；Owner 冻结规则；Monitor 读取冻结版本。错误回滚优先于修改历史叙事。Phase 1 始终 read-only / paper-only。

## 七道证据过滤（V1.1）

参考 `knowledge/system/filter-policy.v1.json`；结构解释到 F3、预测到 F4、经济验证到 F5、Monitor 规则发布到 F6。D10 数据可见性和 D11 反证贯穿每阶段；无证据为 `INSUFFICIENT`，不是假或真。固定 `depends_on` 仅用于必需的学科原语，`related_domains` 不应无条件导入。默认研究包只返回 `NOT_EVALUATED` 的研究计划，不能据此声称过滤结果已经通过。
