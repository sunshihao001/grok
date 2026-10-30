# OKX OnchainOS 本地运行框架审查｜Solana Meme 只读能力与真实执行边界

**版本/来源**：2026-10-30 核查 okx/onchainos-skills commit 73904b636a0f022dcc13b6d7a0dd2ed3b3195f25。重点阅读该提交中的 README、package.json、skills/okx-dex-market/SKILL.md、各 CLI reference 和 _shared/payment-notifications.md。

**当前实际状态**：检查了外部源码与 CLI 规范；本项目**没有安装、认证、调用或付费使用 OKX CLI**。所做离线程序只读入已保存的 JSON 文件。

## 1. 为什么要单独研究这套框架，而不是复制 Skill

当前项目原 GMGN 读取端依赖尚未具备可用的付费/实盘数据，且原 Python 采集器的 normalized metrics 仍为空。OKX 的 read-only DEX market 能够提供多种项目需要的市场、钱包和 Meme 特征；但它的完整 OnchainOS 生态包含钱包、交易、支付和广播功能。因此不能把“只读 DEX Skill”误当“安装整个工具栈即安全”。

当前 OKX package.json 声明 Node.js >=22.14.0。新增 grok_cloud_doctor 会检查本地 Node 版本是否达到这一先决条件，仍不进行安装。

## 2. 核查过的 CLI 命令（仅说明，不自动执行）

| 研究用途 | 官方文档中确认的 CLI 形式 | 安全与数据语义注意 |
|---|---|---|
| Solana 代币身份/decimals | onchainos token info --address ADDR --chain solana | 不能按名称/代码识别资产 |
| 市场价格/流动性 | onchainos token price-info --address ADDR --chain solana | 金额为字符串，requestTime 为上游快照时间 |
| 链上钱包持仓聚类 | onchainos token cluster-overview --address ADDR --chain solana | 是平台聚类指标，不是实际控制人证明 |
| Meme 发币详情 | onchainos memepump token-details --address ADDR --chain solana | 字段可能为空，不等于零；创建时间/迁移时间要按 Unix ms 解析 |
| Meme 开发者关联 | onchainos memepump token-dev-info --address ADDR --chain solana | 平台风险标签是待核实信息 |
| Bundle/狙击资金 | onchainos memepump token-bundle-info --address ADDR --chain solana | 不能从 bundle 标签推导正净期望 |
| 新发项目目录 | onchainos memepump tokens --chain solana --stage NEW | 检测覆盖有限，NEW 和 MIGRATING 只覆盖最近时间窗 |
| 地址买卖信号 | onchainos tracker activities --tracker-type smart_money --chain solana --trade-type 1 | 观察/数据刷新时点不一定早于交易决策 |
| 相关 WS 订阅 | onchainos ws start --channel dex-market-memepump-new-token-openapi --chain-index 501 | 需要显式启动与增量 poll、恢复，不能等同完整实时历史 |

这些命令在本阶段没有被程序直接执行。下一阶段若允许联网，只能通过代码级子命令白名单、输入参数验证与报价/收费审计，不允许运行任意字符串或按外部文本调用 shell。

## 3. 关键发现：只读并不等于不发生付款

OKX 官方私有技能文档 _shared/payment-notifications.md 记录了 x402 市场 API 超免费配额后的支付机制，并指出用户在某个付费层级确认后，CLI 后续调用可能**自动签署匹配支付请求**。这意味着即使 CLI 端点是“只读市场数据”，仍可能存在**支付副作用**。

因此当前决策：

1. 不自动运行 npx 的多 Skill 安装器；其 preflight 自带安装命令，必须获得用户明确授权。
2. 不从 Python 适配器里调用 onchainos，也不运行钱包、payment、execute、swap 或 broadcast。
3. 在实际调用之前，先由用户确认收费机制、配额状态和关闭/限制自动支付的方法。
4. 当前仅对保存下来的只读 JSON 快照做离线解析。如果包含 notifications 或 confirming，则阻断字段提升并要求人工查看。**这无法阻止外部手工 CLI 在执行前已经收费**；它只是保护本项目解析和后续流程。
5. 绝不把任何钱包私钥、API 凭据、支付默认账户或订单参数写入公共 GitHub。

## 4. 已实现的本地解析程序：okx_snapshot.py

主要输出：

- provider / 固定来源 / 操作类型 / token mint；
- 原始响应 SHA-256 和字节数；
- 用户提供的当时接收时间（可空）；
- 本地导入时间与提供者 requestTime（Unix ms，可空）；
- 经过严格 Decimal 校验的**候选数值字段**和显式缺失字段；
- address_confirmed（仅表示响应里声称的地址匹配）；
- source_authenticated=false、eligible_as_decision_feature=false、eligible_as_live_monitor_input=false。

这种保守输出设计可以在不知道真实 OKX 响应是否可被精确映射之前，为后续 B02 编写真实适配器准备字段与失败样例。

离线样例（fixture 合成，不代表任何真实价格）：

    PYTHONPATH=src python3 -m solana_meme_os.okx_snapshot \
      --input fixtures/okx-price.synthetic.json \
      --operation token_price_info \
      --address EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

预期：返回 UNVERIFIED_PROVIDER_CAPTURE，候选字段仍不自动写入 monitor.py 的 metrics。通知或支付确认、错误字段、代币不匹配、浮点/负数、top10 百分比超界等会触发阻断或错误。

## 5. 正式可用的数据适配链（未完成）

    approved OKX account / read-only source
       → operator reviews billing/CLI version
       → read-only command allowlist, timeout and output cap
       → raw response + observed-at and provider received-at capture
       → independent address+slot/decimals/units/coverage verification
       → normalized observation candidate
       → B05 challenge / K2 provenance
       → paper-only rule or research
       → B07 only after human-approved frozen release

不要把收到的 Unix 毫秒 requestTime 当成程序当时确实获取数据的证明。它可能只表示供应商快照时间。必须保存当时的本地接收日志，无法重建时保持 historical_import，不能使用回补数据做事前跟单预测。

### 接下来必须实测，而不是继续写设计

- 在 Grok 云电脑中运行 doctor，确认实际 Node/Python/CLI 是否安装；报告且不擅自安装。
- 由用户单独决定是否允许安装 OKX read-only 模块，并确认其付款/自动签名边界。
- 用经过脱敏的真实只读响应验证操作/数据结构、单位、空值、延迟、限流与计费状态。
- 再开发网络端 provider adapter，而不是直接把一整个交易/钱包 Skill 装入 B07。

固定源码参考：
- https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/skills/okx-dex-market/SKILL.md
- https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/skills/okx-dex-market/_shared/payment-notifications.md
- https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/skills/okx-dex-market/references/token-cli-reference.md
- https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/skills/okx-dex-market/references/trenches-cli-reference.md
- https://github.com/okx/onchainos-skills/blob/73904b636a0f022dcc13b6d7a0dd2ed3b3195f25/skills/okx-dex-market/references/ws.md
