# V0.1｜Token Account 在供应商缓存与官方RPC之间的精确账户核对（2026-11-02）

**适用**：工程草案 [PR #16](https://github.com/sunshihao001/grok/pull/16)，只读单 Mint 业务报告，**非生产监控、非实盘交易、非独立RPC线上成功验收**。与已有 [真实RugCheck+DEX案例](v01-pool-vault-holder-cross-source-2026-11-01.md) 互补，不建立新钱包身份体系。

## 原问题与最小修订

此前 `mint_v01.combined()` 已将 RugCheck 缓存 `root.topHolders[]` 的 `address`、`owner` 和官方RPC `getTokenLargestAccounts`／`getMultipleAccounts` 的 Token Account、Owner 分开呈现，也能够将供应商的 Owner 与DEX池地址做交叉核对，但**没有在同一Token Account上直接比较独立来源的Owner**。两个来源出现相同Owner、不同Owner或前20名账户不重合时，业务报告没有给出有来源的解释。

本轮在既有 [`src/solana_meme_os/mint_v01.py`](../../src/solana_meme_os/mint_v01.py) 添加 `reconcile_vendor_holders_with_rpc(vendor, rpc)`，并将 `holder_rpc_reconciliation` 作为**新增可选报告字段**写入组合JSON和Markdown。完全沿用原有 `public_rugcheck_report.compile_report()` 和 `public_token_accounts.collect()` 的输入，**不新增RPC请求、SDK、授权、钱包连接、签名或收费流程**。旧的仅DEX与仅RugCheck模式仍可运行，无对照源时该字段是 `null`。

核对键是**严格相同的 Token Account 地址**，不是相同Owner或相同DEX路由；同时检查两个输入为相同有效Mint。记录供应商和RPC字段来源路径、供应商发现/采集时间、RPC两次读取的 finalized slot、原始金额及不同时间的标记。RPC Owner 只有在上游报告状态为 `RPC_PARSED_TOKEN_OWNER_NOT_BENEFICIAL_OWNER` 才参与比较。

| 两源状态 | 输出 | 可以和不可以推断 |
|---|---|---|
| 同一Token Account，两源Owner候选地址相同 | `TOKEN_ACCOUNT_OWNER_ADDRESS_AGREES_NOT_BENEFICIAL_OWNER_PROOF` | 相同**地址字段**，不证明共同资金/最终受益人；RugCheck缓存与RPC slot不同 |
| 同一Token Account，但Owner候选地址不同 | `TOKEN_ACCOUNT_OWNER_ADDRESS_CONFLICT_SNAPSHOTS_NOT_ATOMIC` | 保留冲突，可能是缓存过期、账户权利变化或数据语义错误，不静默挑一个 |
| 同一Token Account，RPC已返回账户但Owner无法解析 | `TOKEN_ACCOUNT_MATCH_OWNER_UNRESOLVED` | 账户地址重合，Owner仍未知；不是Owner不相同 |
| RugCheck账户未出现在RPC前20 | `NO_TOKEN_ACCOUNT_OVERLAP_COVERAGE_UNKNOWN`（全零重合情形）及 `vendor_accounts_not_in_rpc_top20` | 仅代表此次RPC **Top20列表** 没有它，不证明该账户不存在、供应商造假或Mint无持有人 |
| RPC或RugCheck来源失败或未请求 | `holder_rpc_reconciliation=null` | 不虚构独立核验 |

官方协议来源：[Solana `getTokenLargestAccounts`](https://solana.com/docs/rpc/http/gettokenlargestaccounts) 的返回对象是余额最大的**20个Token Account**；[Solana `getMultipleAccounts`](https://solana.com/docs/rpc/http/getmultipleaccounts) 返回按输入地址排序的账户资料，可有 `null`，`minContextSlot` 只保证第二次读数不早于指定slot，**不是两次请求的同slot原子快照**。两源金额可能因采集/slot/缓存差异而变化，因此本轮仅保留原值，不计算“持仓发生变化”或持仓集中度。

## 执行与失败反馈

**新增回归6条**：[测试源码](../../tests/test_mint_v01.py)。

1. 同一Token Account/Owner一致时只给地址一致事实，同时保留源路径和两次RPC slot。
2. 同一Token Account/Owner不一致时报告冲突，而非自动选用官方RPC或供应商一个“真值”。
3. **Owner相同但Token Account不同不匹配**，避免把两份账户直接合并。
4. RPC没有可解析Owner时标记未知；缺少来源不生成对照；Mint不一致拒绝比较。
5. RPC Top20不包括供应商缓存账户时，报告覆盖不足，不当作无Holder。
6. 运行组合报告的端到端测试：模拟一次原已有RPC读取及RugCheck读取，核验组合JSON/Markdown出现该字段及原始供应商JSON保存，断言两个来源读取调用次数仍各为1。

**首次真实CI失败**：[GitHub Actions #41448858447](https://github.com/sunshihao001/grok/actions/runs/41448858447)，134项执行时有1项测试报错：端到端测试构造的**RPC模拟报告遗漏 `retrieved_at` 字段**，在既有 `public_token_accounts.markdown()` 中出现 `KeyError`。不是主网RPC返回错误，也不是此新功能经济语义验证失败。已修正测试输入，补齐原报告要求的时间、owner_lookup_error、金额字段。

**修复后通过**：[GitHub Actions #41448982507](https://github.com/sunshihao001/grok/actions/runs/41448982507)，提交 `6ce78f69c6387fc80ade38dc44fbc58aa3c36eda`，job `unit` 状态success，**全部134项离线测试成功**，无网络访问或模拟签名。原有接口保持向后兼容。后续新提交须以其自己的CI状态为准，不用本次旧commit的成功冒充未来任何新commit的验收。

## 真实来源边界与下一步

此前真实联网证据：[一币五池与RugCheck缓存的实际报告](v01-real-rugcheck-holder-2026-11-01.md)，包括20条Top Holder候选、已报告的AMM/Pool地址重合、Creator候选；原公共RPC尝试为 **HTTP 429**，没有成功取得同币官方RPC Token Account与Owner。所以：

- **本轮已完成**：可运行逻辑、保守的跨源经济解释、负例与成功CI。
- **本轮没有完成**：任何一笔**真实**RugCheck Token Account ↔ RPC Owner的在线交叉核对；对持仓当前性、池Vault链上身份、真实关联群体的独立事实验证；OKX真实授权JSON、Dev完整历史、连续资金监控及Grok Bot上线。
- **最有价值的后续动作**：在真正可用、合法且无需密钥/付款的RPC或预先保存的已授权RPC响应出现时，先重放这项精确账户对照（固定双方响应SHA/slot和缓存时点），再判断独立核查是否改变“池相关Holder候选”的解释。不要为了这个小型对照重新造Token Program解码器或全链索引系统。

**验收标准**：成功CI仅证明代码处理已列场景；跨源一致并非真人、KOL、捆绑或操盘控制；任何经济角色必须另有独立证据。