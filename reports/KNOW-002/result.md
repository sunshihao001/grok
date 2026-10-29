# KNOW-002｜直接入金证据知识包

日期：2026-10-29  
状态：开发分支候选；参考级；离线测试已在 GitHub Actions 通过；**NOT HUMAN ACCEPTED**。

## 来源审查

- Hermes 旧结构设计的共同资金源/5分钟/类似卖出规则具有发现价值，但未验证同一人/同组织/收益。
- qb Wallet-Intel 合同要求 raw / normalized / evidence / inference 分层，有利于数据护照。
- 参考项目 [Why-Solana-Memecoins-Are-Over](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) 的方法强调基础设施、粉尘、null、采集完整度、截止时点，原作者文档不被复制；它的历史样本结论不外推为自动规则。
- 8 个原始文件准确版本在 `knowledge/registry.v0.json`，与 KB-001 的 7 个原始来源共存。

## 工程边界

- 新增独立 `funding_evidence.py` 及 fixture 和测试，不改现有 monitor/GMGN collector 阈值。
- 输入必须明示 `mode=fixture`、`policy.status=illustrative`、时间、证据 ref 和 coverage。
- 校验 transfer 的可见时间，区分 hub/未验证 hub/被审查非 hub 三类，按配置示例材料性阈值保留证据；不做 owner 识别。
- 预期可测试风险：重复交易、缺页、dust、hub 膨胀、未来泄漏、RPC 失败、错误标签。

## 发布前仍需做的工作

真实数据独立回查及覆盖率、source->owner 与 LP 排除、基础设施清单验证、跨币/跨周 holdout、null 测试、误报及可复制净收益均**未完成**。

## CI

命令：`PYTHONPATH=src python -m unittest discover -s tests -v`。2026-10-29 GitHub Actions run 40845060238，`PYTHONPATH=src python -m unittest discover -s tests -v`：**Ran 31 tests / OK**（commit `25da6a3e119084c37e3e19ba3d664b63b2401ce9`）。仅验证离线代码契约，**非真实钱包图准确率与净收益的验收**。


## 审计结果

- CI：https://github.com/sunshihao001/grok/actions/runs/40845060238
- 结论：`OFFLINE_TESTS_PASS / SOURCE-PINNED_REFERENCE_ONLY / HUMAN_ACCEPTANCE_PENDING`。
- 依赖：stacked PR #7 的 base 是 `feat/staged-knowledge-intake-001` (PR #3)，合并前需重新比对主分支。
