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

## 2026-11-08｜B02钱包读取恢复的实际增量（PR #18附加修复）

- 读取签名 `readSigs` 只在钱包级转账钩子与交易摘要成功完成后标记；已有实时 `wallet_trades` 不代表原始处理完成。
- 新表 `econ_wallet_processing` 区分 `CAPTURED` / `RETRY_REQUIRED` / `COMPLETE`，并登记尝试次数和最近错误。下游失败的原始RPC已经持久保存，之后优先本地重放而非再请求网络。
- 钱包轮询增加受监控钱包内、最多10条/轮、最多5次尝试、约1分钟冷却后的本地RPC重试候选补队列。原有暂时性缺口之外，不声称覆盖从未发现过的交易。
- 新增 `test/wallet-evidence-retry.test.mjs` 4项故障注入/多钱包真实模块集成测试与 `test/economic-events.test.mjs` 2项限次/受监控重试筛选测试。共**19项新增CI测试通过**，最新全部CI **426项418通过8失败**；8项为先前已存在的WTrack/项目状态断言冲突，不能称整库绿灯。
- **边界**：转账钩子失败会使钱包读取标为需要重试，且最终持久化失败可被查看；但未验证完整服务重启、数据库锁、上游429或外部通知的一次性，`COMPLETE` 仅表示当前Wallet Reader挂载钩子与摘要已成功执行，不表示所有跨模块索引或经济语义完整。

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
