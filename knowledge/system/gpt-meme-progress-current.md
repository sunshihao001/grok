# GPT「跟单」｜唯一活跃进度与下一轮恢复点

**更新日期**：2026-10-31；**知识版本**：研究闭环 V2.0；**研究状态**：P2.5 方法筛选完成，局部 P3 开始设计，P4 尚未开始真实链上实证。

## 必须读取的已有资产

- [研究推进与知识同步 V2](gpt-meme-continuity-v2.md)；[研究写作 Skill V2](gpt-meme-research-writing-skill.v2.md)；[V1阶段坐标](gpt-meme-continuous-progression.v1.md)。
- [**唯一监控方法专题**（P2.1–P2.5）](../domain/meme-anomaly-discovery-state.v1.md)：旧的 M01–M05 / P23 / C01–C05 仍在同一专题，新判断见第7节，**不要再生成同义概念**。
- [P3-M01 离线原型 Draft PR #16](https://github.com/sunshihao001/grok/pull/16)：`src/solana_meme_os/wallet_batch_monitor.py`、`tests/test_wallet_batch_monitor.py`、`docs/p24-m01-crossmint-research.md`。研究主册位于 [Draft PR #14](https://github.com/sunshihao001/grok/pull/14)。两个 PR 尚未合并。

## 本轮 P2.5 完成什么（概念/方法，不是实证）

三项比较已完成**具体字段、误报和工程成本层面的筛选**：

- **C02 进入局部 P3**：固定历史可知的钱包群体，按发行阶段/流动性等匹配条件比较不同 Mint 的收款到首Swap延迟、参与率、下单分布、退出角色变化。需要保留没有执行的人群，防止事后筛选。
- **C05 进入局部 P3**：不能以无交易时间推定沉默；先定义**符合条件的机会分母**、数据覆盖状态、历史活跃基准，区分 NO_OPPORTUNITY / COVERAGE_UNKNOWN / ELIGIBLE_BUT_INACTIVE，再调查其他币/venue行为。机会必须在目标交易前定义。
- **C01 保留研究候选**：核查 Mint A 卖出收益经时间有向资产路径可能支持 Mint B 的交易；需同资产、余额可行性、Hub及混资区分。当前完整多跳资金图成本高且容易误判，暂不优先实现。

**本轮实质修订**：跨Mint重复钱包≠异常；跨币资本路径≠资本归属；“没交易”若无机会分母/完整覆盖≠行为停止。各项状态见唯一专题第7节。

## 工程并行线：P3-M01

**已有**：fixture-only `m01.v1` 输入、1/5/15分钟成员演化与三个描述性候选；14项新增离线测试已重新运行通过，GitHub CI 对此前 PR #16 HEAD 通过。**不是原始交易解码器、链上实时监控器或盈利策略**。

**最重要接口缺口**：真实 `getTransaction` 返回的账户与inner CPI必须被协议解码，识别 Token Account owner/delegate/PDA/fee payer，按经济Swap去重、处理 WSOL/Token-2022/手续费与真实 source、`available_at`，以及能证明窗口覆盖完整。现有代码不接受 live，下一步不要未经审核解除隔离。详见 PR #16 中 `docs/p24-m01-crossmint-research.md` 的 P2.5 适配器审计。

## 下一阶段选择

**P2.5 建议结束。** 研究下一步不继续增加候选名称；优先进行 **P3-C02 + P3-C05 最小数据契约与对抗性 fixture 设计**，工程基础先实施 **P3-M01 raw transaction → normalized economic action 的独立只读适配器**。三者可并行设计，但不要同时开发三套生产程序。

**P3阶段升级到 P4 的最低条件**：独立适配器能用已核实的原始交易覆盖关键事件类型，数据缺失/错误不会输出假事实；C02/C05 的最小对照能用相同时点数据正确构造，能产生真实正例与负例；之后才做样本覆盖/误报与前兆是否有预测价值的 P4 评价。局部 P3 设计完成不等于 P4 实证完成。

## 下一轮直接恢复研究输入

```text
继续 Solana Meme 项目，按《持续研究与知识同步 V2》执行。读取最新唯一进度与P2.1–P2.5监控专题，并检查M01 Draft PR #16，勿重设架构。

现在开展局部 P3：优先设计 C02 同群体跨Mint执行方式切换和 C05 机会校正的沉默/迁移观察。先明确 as-of 时点冻结的群体成员、可比较的发行/流动性阶段、收款到首次Swap的分布及未执行钱包、合格机会清单和 COMPLETE/UNKNOWN 的采集状态。用少量真实研究场景与可复核的对抗性合成数据，提出最小事件契约、正常对照、实现与停止条件；不要将相同钱包/公共Hub直接认作同控，也不推断盈利。

工程并行优先审查并分步构建一个与现有 M01 隔离的只读 Solana 交易适配器：交易版本和LUT、outer/inner CPI、Token/Token-2022、Token Account owner/authority、实际Swap与Transfer去重、SOL/WSOL、quote计价、真实 available_at 及覆盖审计。必须使用明确的Fixture与链上来源，运行测试并报告失败用例，未完成解析不可进入生产监控。

完成后按V2只提取新的知识差异修订现有专题与工程文档，提交GitHub草案、回读核查、同步GPT Library对应旧文件并更新唯一恢复点；Project附件/指令如不能自动更改要明确报告。给出能否进入P4的理由与下一轮可复制输入。
```

## 真实同步状态

知识 V2/P2.1–P2.5 的当前真源在 `knowledge/whole-spectrum-20261030-v1`（Draft PR #14），M01 原型/适配器审计在 `research/p24-cross-mint-m01-batch-monitor-20261031`（Draft PR #16）。两条线未合并主分支。GPT个人Library镜像与ChatGPT Project Files/Instructions是不同对象，后者仍不能由当前可用文件工具直接修改。没有真实K2市场回放或实盘收益验证。