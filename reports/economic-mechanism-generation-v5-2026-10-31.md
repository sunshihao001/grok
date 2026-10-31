# V5 正式研究主线与 R007 首轮实证交付｜2026-10-31

## 战略决策
确定 **“经济机制生成、跨领域认知合成与主动反证研究”** 为覆盖 Solana Meme 全市场的长期研究主线。其对象不是固定“庄家钱包”标签，而是资产、经济角色、执行时序、群体行为、正常市场对照与市场后果之间的**可推翻机制关系**。详细操作宪章：[docs/economic-mechanism-discovery-charter-v5.md](../docs/economic-mechanism-discovery-charter-v5.md)。V4 事件快慢双循环仍是工程运行方式；V5 负责生成未知机制/竞争解释，避免静态知识库只会匹配旧经验。

## 实际新增研究成果

**R007 一手派生事实的二次统计**：[知识案例](../knowledge/research/R007-capital-flow-composition-inversion-v1.md)使用固定版本 `sunshihao001/Why-Solana-Memecoins-Are-Over@9a7ad51d56328e91e67e3f531d6744307d0ee68b` 内 `data/trace_h2w6/e2_funding_h2w6gm6jz.json`：
- `financement` 标记 61 条、来源正向 SOL 变化合计 858.582182029；
- 53 条源 `SYSTEM_PROGRAM|TRANSFER` 合计 98.670927181 SOL；
- 其余 8 条源自非 System 业务标签合计 759.911254848 SOL，88.5076% 的金额；
- 其中 4 条 Meteora `REMOVE_LIQUIDITY_BY_RANGE` 合计 739.476844669 SOL，占 86.1276%；
- 21 个 `genesis_reached=true` 钱包全部至少有一次该资金标签；19 个 `genesis_reached=false` 中只有 4 个有，15 个没有。6 个 `prebuy_window_reached=false` 的钱包均没有该标签。

**明确被排除的推断**：“该来源表内的融资标签总额就是新资本直接注入”；“0 条资金标签记录证明某钱包无历史注资/经济独立”。这些推断在来源语义上不成立。

**竞争机制继续保留**：LP 既有仓位释放/资本再部署、跨市场业务收入/钱包净余额变化、供应商的复合交易主类型标记；历史缺口的 RPC 分页/钱包年龄/角色/抽样差异。它们有不同反证路径，当前均没有被这份派生表独立证明。

## 实际代码与专家连接

- `src/solana_meme_os/mechanism_discovery.py`：调用已有 `cashflow_semantics.audit_funding_table`，使用 Decimal 分解交易次数和金额来源，发现 `COUNT_VALUE_ECONOMIC_TYPE_INVERSION`；将历史覆盖与有无标签单独列联，发现 `HISTORY_COVERAGE_RECEIPT_SILENCE_TENSION`，不使用钱包身份/同控/操盘预测标签，不访问 RPC，不开仓。
- `tests/test_mechanism_discovery.py`：11 项合成测试。
- `tests/test_mechanism_discovery_routing.py`：2 项发现结果→动态专家的集成测试；价值反转优先资金/链上/流动性，历史缺口优先数据法证/钱包/统计，QA 各有独立挑战权。
- `knowledge/mechanism-synthesis-hypotheses.v1.json`：新增 HX07/HX08，累计 8 项合成候选；包括源事实、竞争假说、时点与反证。
- `knowledge/expert-capability-map.v1.json`：增加两个由源分类矛盾触发的专家研究场景，累计 9 个研究场景；仍为 17 类知识能力，不是 17 个云端 Bot。
- `CONTEXT.md`、`BOTS.md`、`skills/solana-meme-system-intelligence/SKILL.md`、`knowledge/README.md` 已将 V5 纳入正确入口。

## CI 与事实等级

GitHub Actions [`monitor-tests` run #41186971334](https://github.com/sunshihao001/grok/actions/runs/41186971334) 已实际完成：**123 项离线 Python 单元/集成测试，全通过（OK）**。本轮所有核心 GitHub 路径通过 Connector 重新读取，8 个机制候选引用的来源和专家 ID 全部有效。主分支没有写入或合并。

**尚未完成**：原 R007 JSON 通过新增 Python CLI 在 GitHub Actions 全量处理（目前从 GitHub Connector 以独立 JS 整表复算）；对真实三条大额 Meteora 交易进行独立 Solana RPC 回放；补齐 15 个未达到 genesis 的钱包的真实早期历史；研究结果自动持续触发 Grok 多专家与实时知识撤回；真实风险或交易收益样本外检验。

**下一条真正能否定或支持 HX07 的核查**：沿实际签名检查 LP Position 所属、原始存入与流动性撤出后的 Token/SOL 变化和资金去向，确认是释放旧经济仓位、已兑现的收入，还是同笔存在其他真实直接注资；同时对正常 LP 撤池钱包做匹配对照。  
**下一条能区分 HX08 的核查**：补齐原先无 genesis 的钱包的最早资金历史，以真实分页/age/活跃度/来源可得时间审计虚假 0 与钱包归因漂移；不能靠旧数据表假设缺失原因。

## 结论

本轮第一次把“由真实资料的跨专业矛盾→发现未被旧标签表达的经济问题→生成竞争机制→按机制分配专家及差异性原始证据”做成可执行、经过 CI 回归的**离线研究纵切片**。这不是完整自主发现型 AI 或市场运行时的证明；下一阶段价值来自独立 Solana 真实数据复核及普通机制负对照，而非无限叠加文档或角色数量。
