# 项目定位纠正记录｜全市场监控为主，跟单为分支

日期：2026-10-31  
草案分支：`docs/cognition-knowledge-conversion-v1`  
状态：专业认知和架构文档更新完成；**并非实际上线**。

## 用户纠正的核心要求

原研究连续 R001/R002/R003 过度聚焦“盈利钱包是否可跟单”，造成目标被缩小。用户实际希望整个 Solana Meme 市场的 **群体异动、同步/捆绑候选、多少地址在何时发生何种规模的 SOL/Token 交易、正常与异常的区分、疑似关联操盘网络、资金循环、市场结构及可交易条件** 的持续监控系统。

“跟单”定位调整为下游使用场景，不再主导系统知识目录和后续开发次序。

## 本轮已变更文件

- 新增 `skills/solana-meme-system-intelligence/SKILL.md`（新顶层领域专家技能，含事件账、窗口、钱包图、条件基准、市场研判、纸面机会分层）；
- 新增 `skills/solana-meme-system-intelligence/references/wallet-cluster-monitoring-example.md`（真实来源案例与竞争性解释）；
- 新增 `docs/solana-meme-marketwide-monitoring-scope-v1.md`（现有代码能力差距、八模块划分及第一个可验收的群体异动观察方向）；
- 更新 `skills/README.md`，将全市场系统作为首选 Skill，深度研究写作为辅助；
- 更新 `skills/solana-meme-expert-writing/SKILL.md`，明确该技能服务整个市场监控系统，而非默认跟单。

## 不变与尚未完成

- 原 Grok `src/solana_meme_os/monitor.py` 仍为单 Mint 快照监控：两个主要指标及简单事件去重；
- 尚未开发真实的市场级扫描、资金图、跨 Mint 群体监测、统计异常性判断、云端 Bot 自动运行；
- 历史 R001/R002/R003 以及本轮先前创建的离线 `src/solana_meme_os/position_audit.py` 和 `tests/test_position_audit.py` 仅作为**经济仓位核对辅助模块**，不应被描述为主监控引擎。离线测试代码已提交，但本轮没有在真实运行环境中执行新测试，不应称已测试通过。
- 不碰 `main`、`rules/`、Bot/Routine 运行配置，未做交易操作；论文级机制和样例不代表已验证盈利模式。

## 下一项开发的评估标准

优先建一个只读跨事件的 `WALLET_BURST_OBSERVATORY` 试验单元，能够在一组明示的真实数据上：
- 正确计数涉及的**独立钱包、交易、转账、SOL/Token 总额、Slot/时间窗**；
- 分辨同 Slot 多钱包、同一交易多指令与确有提交证据的 Jito Bundle；
- 按时点建立 SOL 资金源及 Token 接收图，不把共享基础设施推为同控；
- 输出条件基准下的偏离、反例和实际来源；
- 将风险/机会研究与“行为异常”分开，任何交易动作保持 paper-only。

**验收暂不以“是否成功预测涨跌”为第一指标**：先证明事实账、事件聚类和反证机制可靠，避免在错误群体分类上训练策略。

**认知引导：** 以全市场事件为起点，识别群体协作、资金网络和行为差异；将它们与流动性、筹码和市场阶段连接，最后研究哪些结构在何种条件下具有真实预测与交易价值。
