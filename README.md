# Solana Meme Market Intelligence OS — Grok Bot Edition

**项目定位**：以全市场 Solana Meme 链上事件为入口，持续研究多钱包集中转账、协同买卖候选、资金与代币流向、钱包角色、市场结构、开发者活动和潜在交易风险。**跟单只是下游应用之一**，不再作为全系统唯一主线。

**本阶段状态：开发草案 / 只读与纸面研究。** GitHub 文件存在不代表 Grok 云端 Bot 已部署。没有经过验证的实际交易信号、正常/异常校准概率或真实盈亏结论。

## 首先阅读

- **[总整合蓝图](docs/knowledge-system-integration-v1.md)**：六个参考仓库如何形成统一市场事件、资金网络、行为机制及研究能力。
- **[全市场监控范围与模块](docs/solana-meme-marketwide-monitoring-scope-v1.md)**：M0–M7 能力、真实代码差距、交付边界。
- **[领域研究 Skill](skills/solana-meme-system-intelligence/SKILL.md)**：多钱包批量异动、资金路径、协调候选、正常对照、风险与纸面机会。
- **[知识与写作 Skill 入口](skills/README.md)**、[角色分工](BOTS.md) 和 [发展路线](docs/next-steps.md)。
- **[来源审计](docs/sources.md)**：原 Hermes 知识、`meme-`、`qb-`、外部实证与 OKX 候选工具。保留旧知识，但不运行 Hermes runtime。

## 当前已有代码：三个用途，不是一个“大监控系统”

| 程序 | 当前实际完成的能力 | 尚不代表 |
|---|---|---|
| `solana_meme_os.monitor` | 单 Mint 归一化快照、流动性/前十持仓变化、来源事件去重、JSONL 状态 | 市场级钱包扫描或异常机制验证 |
| `solana_meme_os.market_observatory` | **输入已有的**归一化 SOL/SPL/Swap 事件，按 5/30/300 秒等窗口聚合，输出同 Slot 买入、批量注资、Token 汇集候选 | 实时 RPC 接入、已证明 Jito Bundle、同一受益人或真实异常性 |
| `solana_meme_os.position_audit` | 交叉核验历史表中初始买入与后续累计流出的口径差额 | 资产已闭环、真实 Swap 或利润/交易优势 |

知识入口另有 `solana_meme_os.knowledge`、`solana_meme_os.research`（来源检索，不是智能判断模型）。`gmgn_collect` 仅是旧工具的只读采样原型，源字段映射尚待验证。

## 本地只读检查（Python 3.11+）

```bash
PYTHONPATH=src python -m unittest discover -s tests -v

# 仅运行明确标明的合成示例；不是实时行情
PYTHONPATH=src python -m solana_meme_os.market_observatory \
  --input fixtures/market-observatory-synthetic.json --allow-fixture

# 旧单 Mint fixture 快照测试
PYTHONPATH=src python -m solana_meme_os.monitor \
  --input fixtures/observation-1.json --allow-fixture --state-dir .runtime/demo
PYTHONPATH=src python -m solana_meme_os.monitor \
  --input fixtures/observation-2.json --allow-fixture --state-dir .runtime/demo

# 仅问题/知识路由
PYTHONPATH=src python -m solana_meme_os.research --question "同 Slot 批量资金流能证明庄家同控吗？"
```

上述命令的成功只能说明输入契约、基础代码与离线测试工作，不等于任一真实市场结论成立。

## 参考项目定位

- [旧 Hermes 专业业务知识](https://github.com/sunshihao001/-)：钱包、资金、Sybil、结构、Gate 与旧 Skill 理论（不继承运行时）。
- [meme-](https://github.com/sunshihao001/meme-)：市场阶段、成本区、策略与样本反证。
- [qb-](https://github.com/sunshihao001/qb-)：GMGN 工具/字段原型与错误经验。
- [Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over)：协调检测、资金取证、分母/时间/交易成本审计（不将局部样本外推全市场）。
- [OKX OnchainOS](https://github.com/okx/onchainos-skills)：当前优先审查的只读市场/钱包工具，尚未在本仓库完成真实接口适配。
- 本 `grok` 仓库：知识、研究和运行时集成目标。

## 禁止越界

仅只读/纸面：不读取私钥、不签名、不广播、不下单，不自动部署 Bot/Routine。异常关联 ≠ 已证明庄家身份；同 Slot ≠ Jito Bundle；钱包盈利 ≠ 可复制净收益。所有规则阈值及研究假设必须单独验证，修改只经审查合并。更详细的约束见 [AGENTS.md](AGENTS.md)。
