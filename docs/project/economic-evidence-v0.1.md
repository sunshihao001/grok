# Blix｜经济事件证据层 V0.1：来源、验证、边界

状态：FEATURE_BRANCH_ONLY / ISOLATED_TESTED / NOT_LIVE_CHAIN_VERIFIED。
基线：blix commit 3bc1f7d4befc4e11e21d9a67fabbd5c4d259b1e7。

## 修复的原有断点
- 实时成交先进入 wallet_trades 时，旧 wallets.readTx 直接提前返回，完整 RPC 交易和 onTx 无机会处理。
- parseSwaps / parseTransfer 是余额净变化摘要，混合 Swap+Transfer 和多个接收方会漏记或误归因。
- Holder 快照不能发现所有清仓的接收钱包；跨 Mint 时间相近不证明资金真正同源。

## 已接入的实现
- server/economic-events.mjs：完整保存已取得的 getTransaction(jsonParsed) RPC 对象（包含 meta、日志、原始外层指令、innerInstructions、pre/post 账户及余额）；以签名和 SHA256 保留原文与版本。econ_instructions 按 signature/outer_i/inner_i 保存每一条原始指令，并为可识别的 SPL Token、Token-2022 和 System SOL 转移提供保守索引。
- 只根据 RPC pre/postTokenBalances 的 accountIndex 映射 Token Account 与 Owner。未知、歧义或冲突保持 null；未解码交易指令仍保留完整原文。不得把金额净变化当成逐笔完整买卖记录。
- server/wallets.js：不再因 wallet_trades 已经有成交记录而跳过完整 RPC 交易获取，先保存源证据，再走原有钩子及摘要。
- server/server.js：仅 owner 的本地证据 GET /api/evidence/tx/:signature、/api/evidence/recipients/:wallet?mint=...、/api/evidence/cross-mint/:wallet?hours=24、/api/evidence/missing/:wallet。它们只读取本地 SQLite，不执行新的 RPC、AI 付费调用、签名或交易。
- scripts/replay-economic-evidence.mjs：显式提供 --db 已存在数据库和 --input 本地归档 JSON，离线补录至 SQLite；最多每批500笔，不访问网络。切勿直接指定生产数据库进行试验。

## 离线验收
- test/economic-events.test.mjs：13项隔离 SQLite 回归测试通过，包括重复重放、混合交易 A 买入后向 B 转移、A 同签名向 B/C 各转不同数量、缺失/冲突 Owner、不成立的交易状态、历史遗漏签名和跨 Mint 时间候选。
- 离线归档导入：第一次 stored:1，第二次 duplicates:1（同内容幂等）。
- 未运行原 Blix 正式服务、真实主网钱包 RPC、完整历史索引、长期云端监控或交易。没有宣称实际生产端验证。

## AI 与市场经济解释限制
1. “无损”仅意味着已取得的完整 jsonParsed RPC 数据对象可被原样存储和重放，**不是整个 Solana 历史被完整采集**，也不是所有 CPI 自动得到正确交易或资本归因。
2. recipients 只表明被捕获交易内可以映射 Token Account Owner 的指令边；池、公共设施和协议 CPI 可能同样产生边。候选接收钱包**不会自动订阅**，没有验证后续一定卖出。
3. cross-mint 输出有明确 SOL 转出和后续不同 Mint 买入的时间候选，但 SOL 是可替代资产，即使转账成立，也不证明“售出所得的同一批 lamports 被用于后续买入”，亦不证明共同控制。
4. missing 只列已存在 wallet_trades 却缺少 RPC 原文的签名。没有列出不等于原始钱包历史完整。尚未解决旧 WTrack、PnL、BubbleMap 与行情流全量经济事件对齐。
5. 新表可能增加存储与写入负担；上线前需要验证源接口可靠性、磁盘预算、历史补查水位、重启与权限。Blix 仍有其他未隔离的交易路径，不能因本次代码只读而认为原服务可安全启动。

## 后续真实验收所需
- 在经安全隔离的环境中对真实签名重放：多 CPI、Token-2022、v1/ALT、Token Account 新建/关闭、Swap+Transfer、LP 事件。
- 检查完成持仓清仓的 B 依然能否从历史真实转账中被发现，而不是依赖当前 Holder。
- 对跨 Mint 资金与公共服务节点进行反证；有必要时复用 PumpTrace 可续传游标与 Million 的候选钱包发现，不重造 UI。

## V0.2 安全的经济证据加固（2026-11-08）
**状态：FIX_BRANCH_ONLY / TESTS_ADDED_NOT_YET_CI_VERIFIED / NOT_LIVE.**
- 使用 Solana 官方 Token-2022 Program ID，且同步修复 wtrack 的旧错误常量。
- `persistEvidence` 检查 RPC 第一笔签名与输入签名一致；冲突拒绝写入。
- 交易索引持久化 Owner 冲突字段；同一 Token Account 的前后余额中，部分缺失的 Owner 不再等同于确实冲突。明确冲突的转账不得生成接收者候选。
- 在 `econ_transactions` 中保留 `capture_source` 和请求 `commitment`；这些只是采集元数据，不能证明整段交易历史完整。写入路径支持旧表增量迁移。
- `wallets.readTx` 在完成保存与原有钱包摘要之后标记已处理，避免后续步骤错误时提前屏蔽重试。
- 新增 owner-only `GET /api/evidence/recipient-outcomes/:wallet?mint=...&hours=24`，只在已经捕获的证据和本地 Wallet Trades 中匹配接收地址后续卖出及跨 Mint 时间候选；**不会自动订阅新钱包、发起 RPC 或签名**，也不能证明卖掉的是刚转入的筹码。
- 证据表缺失时 GET 返回未初始化标记，不再触发 SQLite CREATE/MIGRATE；当前旧表结构需要写入路径迁移后才能进行新索引查询。
- 追加签名一致性、Token-2022、Owner 缺失/冲突、Mint 冲突、接收者后续行为和纯读取等离线测试。
**仍未解决：** 官方真实签名归档验收、Solana CPI 更深层语义、Token-2022 扩展净到账、真正的经济对价/库存守恒、受控的历史补档、自动新钱包监控、原主服务只读安全隔离、UI/MCP 的完整业务整合。该分支不得直接认为生产可用。
