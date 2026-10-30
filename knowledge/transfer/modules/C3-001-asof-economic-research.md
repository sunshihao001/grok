# C3-001｜预注册：AS-OF 时间、F4 增量、F5 交易经济性

**状态：draft，只能预览；先完成 C1-001 和 C2-001。**  
**面向 B01/B02/B04/B05/B06。**

## 深度目标

在一个冻结的投资决策时点，严格区分“数据何时发生、何时被观测、何时可用、何时形成交易计划、何时有可用双侧报价”。

**首要概念**：`blockTime` 并非 `feature_available_at`。历史数据回补的链上事实在真实决策时不必然可获得。实际 receipt/parse/feature availability 都需要有当时的不可变采集记录。

## 四个可证伪研究分支

- H-A：事件与到账信号间的价格吸收（P0）。
- H-B：操作者退出后**独立新资本**承接的二次结构（P1）。
- H-C：资金再部署对下一目标币实际可交易性的限制（P1）。
- H-D：风险过滤是否在等覆盖率/风险预算下改善尾部结果（P1）。

具体总体、对照、反证、研究阶段、停止规则见 `research/2026-10-30-executable-copytrade-edge.md` 和 `knowledge/experiments/executable-edge-protocol.v1.json`。

## 执行一个不含市场数据的离线时间检验

```bash
PYTHONPATH=src python3 -m solana_meme_os.asof_audit --input fixtures/asof-audit.synthetic.json
```

预期包括：一个**仅时间语义合法、尚未验证来源**的记录；一个观测晚于决策时点的拒绝；一个历史回补且无同时期可见性证明的拒绝。Fixture 绝不代表真实市场研究通过。

## 应答考题

1. 在 10:00:00 发生的交易，10:00:10 才由 RPC 被取得，10:00:05 的决策是否可引用？为什么？
2. `getTransaction` 的 `blockTime=null` 怎样处理？为何不能填 0？
3. 同源钱包结构提升涨幅命中率，但控制 market cap/liquidity 后差异不稳健，应如何报告 F4？
4. 一种实际可见但无法获取退出报价的策略，F5 应如何判定？
5. 两组信号由相同 operator 重复产生，随机切分导致的 OOS 泄露如何检查？

## 通过条件

能写出 `event <= provider_received <= parsed <= available <= decision` 的审计含义，并承认这只是必要条件，不是原始时间真实性证明；能给出完整分母、负例、group/time OOS、费用与可卖性约束，不虚构交易或盈利结果。

**注意**：`asof_audit` 的“时间一致”不等于“可作为实盘决策特征”。离线程序因为不能独立认证采集日志，`eligible_as_decision_feature` 保守保持 false。真实数据的来源真实性必须在 B02/B05 的独立审查中证明。
