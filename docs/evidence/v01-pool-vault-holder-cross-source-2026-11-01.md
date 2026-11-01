# V0.1 真实Mint的交易池—持有人地址交叉核对｜2026-11-01

**结论**：本轮不是又造一种钱包聚类策略，而是在现有DEX Screener和RugCheck完整现成只读API结果之间执行**地址精确相等检查**，识别“Holder排名含流动性池相关账户”这一真实产品误归因风险。相关代码直接复用现有`src/solana_meme_os/mint_v01.py`（新增`pool_related_holder_observations`，没有替换既有API和Grok架构）。

## 事实链（来源可核对）

- 查询Mint：`EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump`。
- [GitHub Actions实际在线成功运行](https://github.com/sunshihao001/grok/actions/runs/41268982018)；该次交易池+RugCheck缓存报告的压缩证据包为Run的`v01-rugcheck-public-mint-one-time`，Artifact ID **13068437092**，14天保留。它不是静态合成fixture。
- RugCheck原始JSON SHA256 **`9671b8edf008772892035b22eb952b205409bc2125cb0f8fa16db5dd1178de0c`**，DEX Screener原始JSON SHA256 **`a7f941d5f2caca8c9ebff9b908b4a58dfa1009150ed55e986cb222fcd81e4de9`**。已在独立下载的原始文件中重新计算并与报告的`input_sha256`和`raw_input_sha256`比对。
- RugCheck的`topHolders[0].address` = `BYonfuCMtQL9rLeYLhLar7Jon87Nwj7PyurLFj6sNx3i`；其`owner` = **`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`**；供应商`pct` = **`5.877731005322626`**（单位按供应商百分数）。
- DEX Screener某条`pairAddress`同为 **`81jgrpTMsQWc1rGWXutyYWW27ruiAtehUZwLydcHHWDB`**，该池`dexId=pumpswap`且包含输入Mint作为base。**这是两个原始供应商字段的确切字符串一致**，不是同控经济主体的链上证明。
- RugCheck此Mint返回20条`topHolders`、Creator地址候选`9QTjLWyhfpJ8Hm1ZALMNv9L4K6w13BSuUxMWu976Pg1Y`，`creatorTokens=null`，所以**不能声称Dev没有历史项目**。供应商归一化风险分`29`，其`risks[0]`另有`Copycat token`警告，风险分与风险规则积分不是同一个概率或同一量纲。
- RugCheck`detectedAt`为`2026-10-30T20:50:12.005503318Z`，实际响应取回时间`2026-11-01T03:23:31.969326+00:00`；缓存报告和DEX池快照**不是同slot原子状态**。不能把detectedAt当Mint创建链上时间。
- 另一次[GitHub Actions RPC验证](https://github.com/sunshihao001/grok/actions/runs/41268871079)尝试`getTokenLargestAccounts`，实际返回**HTTP 429**；因此本案例尚**没有**Solana官方RPC对该Token Account/Vault/TokenOwner的独立链上核实。源错误必须保留UNKNOWN而不是填0。

## 为什么会改变真实产品判断（原D01/D03/D04/D05/D06/D07）

1. **D01/D03账户事实与资产权利**：`Token Account`、其Token Owner、DEX池地址、池Vault、LP经济权利和最终受益人至少是不同待判定的实体层。两个供应商的池地址和Token Owner候选相等，只能高亮“池相关候选”；不能把5.88%自动算到单一私人鲸鱼或控制集团。
2. **D04/D05经济关系**：旧Hermes `learning/10–12.md`已明确行为才能形成角色、同源也只是假设；`design/phase1-skill-04-wallet-structure.md`把“5分钟内≥3钱包”和“同Funder≥2”作为协同候选规则。它们是待反证的**筛选启发式**，不能在缺真实Swap签名、公共资金Hub排除、钱包观察时间的报告上直接评出高风险庄家。
3. **D06库存**：这份供应商持仓排名的至少一项涉及疑似池地址，必须从“个人自由持仓集中度”候选统计中**独立标识**；但不应直接从总供应量扣除或自动算出可卖量。需先查实际Vault Token程序Owner、池LP份额与具体经济权限。旧`qb-/sikk_gmgn_token_report.py`的`04_key_address_matrix.csv`、`05_infrastructure_registry.csv`原本就把地址矩阵与基础设施分开，本轮用真实跨源数据证明了这个栏目分离的必要性。
4. **D07观察时钟**：RugCheck缓存创建/发现时点、公开DEX取回时点、Solana RPC Slot/检索时点不能重命名为“钱包同一秒动向”；没有交易级观察时钟，就不生成协同买卖信号。
5. **D11反证**：若只有单一RugCheck Holder名单，用户可能认为“Top1占5.88%说明有一个鲸鱼”；当与DEX池地址对照，得出竞争解释“该Top1可能是池库存”。此情形是**值得编码成负例的跨源反证**，不是新庄家模式。

## 已在工程中实现和测试的最小规则

`mint_v01.pool_related_holder_observations(pool, rug)`只有两个供应商实际返回时，才对`pool.pairs[].pool`与`rug.top_holders[].owner_candidate`或`token_account_candidate`做**严格地址全等**匹配；输出源路径、供应商百分比和`CROSS_VENDOR_POOL_ADDRESS_MATCH_NOT_CHAIN_VERIFIED`，不产生新“控盘率”、买卖信号或投资建议。对应`tests/test_mint_v01.py`增加真实形状正例、不同地址负例、缺来源负例及组合报告输出测试；GitHub [CI run 41269135139](https://github.com/sunshihao001/grok/actions/runs/41269135139)执行**120项离线单测成功**。新方法本身在CI使用合成单元输入；原始在线数据地址交叉核对另由独立脚本核实，不能混称已在Grok云电脑实盘运行。

**当前可运行级别**：真实DEX池数据、真实RugCheck缓存持有人/Creator线索、跨源地址相等反证逻辑可运行；OKX完整`token-research`仍未拿到授权真实结果；公共RPC被429限流；没有Dev完整历史、资金图、真实协议Swap、主网库存对账或Grok云电脑部署。只读，未交易未签名未付款。
