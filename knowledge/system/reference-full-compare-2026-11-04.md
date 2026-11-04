# Solana Meme｜65 项原参考资产全量恢复 + 17 项增补 + 同题主体工程比较（2026-11-04）

> **定位**：当前项目原知识PR #14 的附属审查成果。历史 L0–L7 / D01–D12 / 152 研究单元 / 22 专业视角保持不变，不新建平行本体。本报告是参考项目的导航、同题比较与选型反证，不是任何程序的部署证明，也不是金融收益验证。原 65 条 **完全保留**，REF-035 是历史缺号。原项目 grok PR #14/#16/#17 于本轮检查时均 open draft。

## 0. 主体选择原则（已修订）

用户需要的是**可持续扩建的完整软件主体**：好的代码结构、真实可运行业务、可靠数据模型、持久性、用户体验、清楚的扩展边界、安全和许可证。功能缺口可以通过其他已登记成品、SDK或供应商补齐；但不能先选一个 UI 漂亮或功能多、底层却难以维护的程序。**不预设 Grok 或 BLIX 必为底座，也不把暂时缺少业务功能直接当淘汰理由。**

## 1. 来源范围与调查覆盖

- **原始来源**：`knowledge/system/gpt-meme-project-index.v1.json` 65 条；`knowledge/system/reference-assets-reading-coverage-2026-11-02.md` 逐项覆盖账；`knowledge/system/whole-domain-atlas.v1.json` 原152问题本体。
- **后续新增**：13 条上轮产品候选原样沿用（NEW-01～NEW-13），本次增补4条小型取证/开发者监控候选（NEW-14～NEW-17），共17条增补候选。**这些数量不等于已独立深审82份软件源码。**
- **已检查内容**：历史原件、GitHub仓库元数据、核心成品README、架构与文件树、部分主要源文件/数据 schema/安全约束、官方API资料、此前离线反例。对未查到源码、仓库LICENSE或授权API标记 UNKNOWN。
- **身份与别名**：原列表中的 Axiom 的 “Pulse” UI 页面 ≠ `nirholas/pulse` 开源程序。BLIX hosted 与开源 `blixvip/blixtrade` 同产品系，不算两个独立代码主体。Bubblemaps `bubblemaps.io` 与可能名称近似的第三方 `bubblemaps.dev` **不得混同**。

### 1.1 原65条分类覆盖统计

| 原登记类型 | 数量 | 是否全部实时验收 |
|---|---:|---|
| 自有工程/专业历史 | 5 | 否，仅按具体来源标记检查范围 |
| 学术/方法反证 | 6 | 否，仅按具体来源标记检查范围 |
| 开源成品/业务工作流 | 6 | 否，仅按具体来源标记检查范围 |
| SDK/解析/索引 | 8 | 否，仅按具体来源标记检查范围 |
| 链上协议/原理 | 12 | 否，仅按具体来源标记检查范围 |
| Agent/Grok 工作流 | 1 | 否，仅按具体来源标记检查范围 |
| 数据供应商/商业服务 | 11 | 否，仅按具体来源标记检查范围 |
| 交易终端/社区经验 | 16 | 否，仅按具体来源标记检查范围 |
| **总计** | **65** | **不作全部审毕声明** |

## 2. /COMPARE：统一的五个业务试题

| 同题场景 | 相同输入/操作 | 有效结果的定义 | 一票否决式反例 |
|---|---|---|---|
| S1 市场发现 | 新币/迁移/大额活动 → 点击Mint → 保存、重启、复查 | UI/API/库同时有可追溯记录，起止时间明确 | 公共WebSocket断流无缺口；多池当一池；新发行事后回填当实时 |
| S2 单Mint调查 | `EYqygbhZjP7EbM4fSn8devctnksAvPAD1Bt57XBFpump` → Creator/Pool/Holder/Wallet | 区分 Token Account、owner、pool vault、权限、真实可卖库存及来源时间 | 用池持仓当私人鲸鱼；未读Dev历史却推定“无发币史” |
| S3 跨Mint群体 | 两钱包、两个Mint、相同签名/多操作、公共 Fee Payer | 交易数、经济动作数、钱包参与数分别正确；关系不等于同受益人 | 一签名唯一导致漏钱包；简单同源或同步→庄家 |
| S4 长期监控 | 重复事件、乱序、RPC限流、WebSocket断线、历史回填、重启 | 数据可重放、可恢复，覆盖/事件/可得时间清楚 | 漏事件装成“停止”、重复记账、回填导致前瞻偏差 |
| S5 主体可扩展 | 在原产品新增**只读资金关系调查垂直切片** | 修改范围可控，API/UI可连贯呈现，既有测试不回归；无签名/交易 | 每改一处需重写大量模块；无法隔离交易或无法溯源 |

## 3. 同题矩阵（18 条完整产品/专项方案/底层工程）

> S1/S2/S3 各项为**源码/官方说明可发现的能力或不足**，并不是18套程序均已真实跑通。成本一律区分代码许可证、运行基础设施及外部API。最后一列全部为本轮实际未完成的整套验收。

| 路线 | S1发现 | S2单Mint | S3群体 | 历史与数据 | 工程与安全初审 | 运行与成本边界 |
|---|---|---|---|---|---|---|
| BLIX | 强/源头/价格/池 | 中/Holder/Dev，TokenAccount经济归因未闭环 | 中/钱包和群体候选，资金共控须反证 | 中上/SQLite/恢复/备份；事件历史选择性 | 源码细节可审、模块多、CI测试和健康/备份；集中入口可能增加扩展回归风险；MIT,Node≥24.16,可选远程与托管/交易路径需要严格隔离 | 无依赖可启动; RPC/Helius/Jup/模型服务可能产生成本；未核月费；NO_FULL_RUNTIME_ACCEPTANCE |
| Pulse | 强/发行/观察/市场生命周期 | 中/市场Mint;关键资金关系不完整 | 弱/没有原生深度群体资金网络 | 强于短期窗口/PG+PGlite+Git档案；精选交易不是全量 | 分层清楚/采集源、索引、智能、档案；多池PK、乱序窗口、衍生重复计数待实跑；MIT,Node≥24,WebSocket/可选Git Token外传需隔离 | 可用PGlite, RPC限速/归档Git仓/AI可增成本;价格未核；NO_FULL_RUNTIME_ACCEPTANCE |
| Million | 中/钱包反向发现token | 中/钱包数据较强，Mint重心有限 | 强候选/Funding、owner、wallet flows，身份不能证 | 低于Pulse/实时LiveEvent 15分钟窗口、也有历史分析缓存 | 模块化清楚；LiveEvent.signature UNIQUE导致多钱包漏记;缺常规自动测试/CI；MIT/Node24/Helius/默认纸面交易但具实盘路径/写MCP需隔离 | Helius额度/模型或服务可变；非零自动费用需确认；NO_FULL_RUNTIME_ACCEPTANCE |
| PumpTrace | 弱/非全市场 | 强/Creator+insider+可卖库存候选 | 中/偏单Mint与Dev钱包 | 中/JSON+NDJSON或Postgres；可恢复 backfill | 业务职责清晰；缺测试/CI/根LICENSE文件；内置源码读数依赖Helius；许可证可再授权未证，Node>=20、Helius key，默认worker停用 | Helius查询额度未知；付费档位未知；NO_FULL_RUNTIME_ACCEPTANCE |
| dexterm | 强/终端市场筛选 | 中/Token screen | 弱/多数功能为终端研究 | 中/SQLite/record/replay | packages模块化、测试覆盖广；单个主入口近300KB且有实盘信号能力；AGPL-3.0-only，默认终端，实验性真实信号路径禁止启动 | Node≥22.18，RPC/Helius/模型成本视配置；NO_FULL_RUNTIME_ACCEPTANCE |
| Solbeam | 中/承诺新币发现 | 中/Token risk | 中低/钱包Webhook | 中/依赖Supabase | 部分测试，真正全面落地与后端外部依赖待验；LICENSE root absent；Helius/Supabase/告警/交易模拟权需审 | Helius/Supabase/邮件服务额度；未知；NO_FULL_RUNTIME_ACCEPTANCE |
| HoldTech | 中/热门观察 | 强/持仓质量/聚簇 | 中/重叠/同源推断 | 弱/无完备持续录制 | 以数据型判定为主；scan-core内见默认公开静态API凭据，不能复制；LICENSE根文件未核；凭据风险；Token_ACCOUNT/owner要复核 | Helius费用可能且默认凭据不可复用；NO_FULL_RUNTIME_ACCEPTANCE |
| PumpGrok | 规划中/SCOUT未实现 | 工具查询 | 技能级候选 | 本地票据/重放非行情全历史 | AI工作规范/权限与工序设计明确；非市场数据主体；AGPL-3.0；Grok宿主能力未知；不签名 | Python3.12/uv；公开RPC限流，Grok运行成本未知；NO_FULL_RUNTIME_ACCEPTANCE |
| Solana Microscope | 非全市场/单程序监视 | 取决IDL与选定程序 | 不内置钱包/跨Mint经济关联 | Prometheus/Loki/检查点/回填（默认30天本地） | Carbon流与IDL解码、检查点、故障/解码指标专业；一个部署一Program；MIT；Rust/Node/Docker/Yellowstone或RPC;监控/告警可能外发 | 容器+存储+RPC/gRPC费用；需要自行估算；NO_FULL_RUNTIME_ACCEPTANCE |
| pumpwatch | 强/只限Pump | Creator行为研究 | 弱/不做综合资金网络 | 可记录发行历史/研究数据 | 面向可复现实证项目/数据快照，不能代替统一终端；MIT只读，RPC服务额度 | RPC/存储人工运营；具体费用未知；NO_FULL_RUNTIME_ACCEPTANCE |
| Kol Quest | 中/数据榜单 | 中/钱包画像 | 中/持续交易跟踪不等于资金关系 | Postgres/JSON混合 | 多源抓取依赖、数据共享与权限合规复杂；LICENSE需复核、GMGN来源使用条款 | 源接入/数据库/部署/抓取的费用不明；NO_FULL_RUNTIME_ACCEPTANCE |
| OKX OnchainOS | 强/市场服务 | 强/服务能力 | 中/标签与feed，不证明最终控制 | 外部服务由供应商管理 | 直接使用成熟服务的潜力大，但不可掌控底层索引逻辑；read-only DEX market skill 与 Wallet/Payments/Trade 必须隔离 | 账号授权、交易费用和API限制需具体核；NO_AUTHENTICATED_END_TO_END |
| GMGN | 强/商业UI | 强/标签和token详情 | 中/平台钱包指标需验证 | 提供方内部 | 可直接使用替代自建，但API与审计边界有限；潜在交易Skill/权限分隔；成本历史口述不等于现价 | 当前充值/API额度需用户授权后核；NO_AUTHENTICATED_END_TO_END |
| Bubblemaps | 弱/非发现中心 | 强/图谱 | 候选/资金/Holder关系 | 供应商掌控 | 适合替代自研图谱；无法用图直接证明最终收益权；合约/数据授权许可不同于开源代码许可 | API额度和套餐未实证；NO_AUTHENTICATED_END_TO_END |
| Cielo | 中 | 钱包/Token feed | 强/追踪钱包列表，不是主体控制 | 供应商掌控 | 现成监控可替代自建通知功能；写Tracked Wallet endpoint不得当成只读；未授权不操作 | 官方开发者文档5 credits/add request；credit价格未知；NO_AUTHENTICATED_END_TO_END |
| Nansen | 市场研究/Smart Money | 强/Token God Mode/钱包画像 | 候选/标签 | 供应商掌控 | Solana分析可直接用来减少自建，但算法黑盒；需要账户；交易功能与数据访问分隔 | 官方帮助显示Solana部分免费但API Pro，具体额度需核；NO_AUTHENTICATED_END_TO_END |
| FnZero + Carbon | 不内置发现UI | 提供原始交易解析 | 需下游主体研究 | 输出结构待持久化 | 适合作为交易语义与流处理底层，不是单独主体；版本/DEX覆盖/许可与性能要匹配 | 索引服务、RPC流成本需估算；NO_RUNTIME |
| Why-Solana | 非实时发现产品 | 资金路径与样本研究 | 强科研假说对照，不提供实时提醒 | 可复现实验缓存 | 适合判断五跳路径归因/多重检验/预注册，不做主体；代码/数据许可证各自核 | Helius历史提取成本高；NO_CURRENT_FULL_REPLICATION |

## 4. 工程主体候选：不能按功能数量排序

| 主体/架构路线 | 证实的基础优势 | 关键不足或隐含债务 | 适合作为哪一类基石 | 暂不判定 |
|---|---|---|---|---|
| [BLIX](https://github.com/blixvip/blixtrade) | 本地完整Web终端/SQLite/WAL/备份/健康/CI测试/MCP；MIT | 入口 `server/server.js` 约174KB、`public/app.js` 约270KB，功能集中；需要实证评估功能新增的修改波及面；本地/托管真实交易功能不得混同 | 产品UI与运维成熟度基石候选 | 是否比其他产品更易增加深度资金调查 |
| [Pulse](https://github.com/nirholas/pulse) | 来源适配/采集/市场智能/数据库/归档/API/Web/MCP分层；PGlite/Postgres；MIT | 多池归档唯一键、乱序窗口、精选交易样本等语义边界；钱包资金图需补 | 市场数据、历史库和可扩展采集基石候选 | 完整钱包经济事实的重建成本 |
| [Million](https://github.com/Kelows/million) | NestJS领域模块+React+Prisma+共享模型；Token↔Wallet闭环；资金/群体/钱包流；MIT | `LiveEvent.signature` UNIQUE 对同签名多钱包不够；交易与研究混合；现仓未见常规测试/CI | 钱包业务的领域模型和闭环候选 | 隔离交易后保留完整业务是否低成本 |
| [dexterm](https://github.com/dexterm-xyz/dexterm) | 清晰Packages: data/agents/mcp/packs/recorder 等，测试与权限约束广 | 以 TUI 为主、项目范围很大，包含实验性真实执行信号；AGPL | 模块化/AI权限/可审计研究工程候选 | 改为统一Web用户产品是否值得 |
| [PumpTrace](https://github.com/AntC215/Pumptrace) | Creator→钱包→关联供应→证据解释→观察列表；回填与JSON/NDJSON/Pg | LICENSE文件和CI/test目录未见；Helius依赖；全市场发现弱 | 单Mint链上取证垂直产品候选 | 许可证与运行安全、测试成熟度 |
| [Solana Microscope](https://github.com/solana-foundation/solana-microscope) REF-012 | Carbon/IDL解析→Prometheus/Loki/Grafana、告警、恢复/回填，MIT；监控工程较成熟 | **一部署监控一个程序**；无跨Mint市场产品业务/UI，基础设施运维较重 | 数据摄取、程序监控和可靠性设计基石候选 | 是否适合作为整套Meme工作台底座 |

### 4.1 跨成品已查明的具体源码/数据语义冲突

1. **BLIX vs Million**：BLIX钱包交易以 `(sig,wallet,mint)` 记录参与，Million `LiveEvent.signature` 唯一且Webhook首个订阅钱包匹配就 `break`。BLIX表达多钱包参与更自然，但仍未证明能表达一笔签名中的所有多池/多动作。必须对同一多钱包签名做离线+原版验收。
2. **Pulse**：`launch_events` 的主键 `(chain,kind,token)` 不能保存同一Mint同类多个池事件；`Rolling.hit` 对乱序事件归入最新bucket；`trades` 选择性保留标签钱包、大额单和事后入选的早期买家。它可做市场档案，但不能按全量钱包成交表解释资本网络。
3. **HoldTech**：`app/lib/scan-core.ts` 存在公开默认API键字符串，安全复用前必须去除/换成自己授权的设置；不复制凭据，且同源/同步仍需公共服务共因反证。
4. **Why-Solana / Hermes / qb- / meme-**：保留资金图、多跳、筹码控制和策略研究，但研究的「经济主体」不等于Token Account、最终受益人无法被链上唯一证明。把旧研究保留作反例/解读器，不预设旧阈值等于真实控制概率。
5. **PumpGrok vs Grok**：PumpGrok提供Agent会话职责、权限与票据经验，但其当前Scout常驻数据流水线尚未实现；不能充当独立持续采集数据库。

## 5. 数据、方法、费用、可靠性与安全：在同一事实合同下评价

| 评估面 | 每套系统必须交出的内容 | 已核查的典型问题 |
|---|---|---|
| 经济数据语义 | 签名、inner CPI、账户与Owner、原始/净变化、SOL/WSOL、多池、Token-2022、缺口、可得时间 | Million 同签名多钱包事件粒度不足；Pulse 未存全量经济事件；Grok M01 仅离线标准化fixture |
| 方法与反证 | 同步≠同控、同源≠同经济受益、Fee Payer≠Principal、销售额≠PnL | BLIX / HoldTech / Million 聚类标签须独立挑战，Why-Solana供对照 |
| 可靠性 | 断线/重试/落盘/幂等/备份/校验/恢复/覆盖证明 | Microscope 有检查点和回填；Pulse有Git快照归档；BLIX有备份和健康；但**这些不是本轮实跑结果** |
| 扩展成本 | 新增一个资金调查模块所需修改文件、接口、DB迁移、回归测试、部署变更 | 尚未作同题扩展实验，不可按文件数、测试数直接判定好坏 |
| API与基础设施费用 | Node/DB主机、RPC索引调用/限流、Helius、AI、通知、备份、授权额度 | 代码MIT不等于服务0成本；大多数供应商没有本轮端到端计费证据；保持UNKNOWN |
| 安全/许可证 | 不允许私钥/交易/签名/付费或未授权通知；审查外部写接口和静态凭据 | Million/dexterm/OKX/GMGN/BLIX含交易面；PumpGrok/dexterm AGPL；PumpTrace授权证据不完整 |
| 实际效果 | 同输入的原版运行日志、快照哈希、用户UI截图、数据复算、重启恢复 | **本轮未安装/运行任何第三方成品**，不报告吞吐量、成功率或延迟优劣 |

### 5.1 真实成本的新信息（不能夸大）

- **Cielo** 当前官方开发者文档称“添加跟踪钱包”请求消耗5 credits；这**不是**5美元，未核 credits 价格。它属于直接使用外部服务路线，不可作为可修改的本地代码主体。
- **Nansen** 官方帮助文档说明 Solana 链上分析部分已开放免费使用，但 API 仍需要 Pro 资格；不能把免费Web分析等同免费编程接口。
- **PGlite/SQLite** 允许免费本地启动，但公网RPC、WebSocket限流、Helius历史查询、云主机和模型API仍可能有显著持续支出。费用预算须以真实目标交易/钱包规模测量。
- **GMGN** 之前用户曾遇到较高API接入门槛，但不能把旧门槛当现在的最新价格。

## 6. 65项原参考资产逐项导航——编号、来源、角色与真实证据边界

> 下表 **historical_verification** 是原索引的历史登记状态；本轮个别核对只在下面“本轮特别核查”栏明确标出。所谓 SOURCE_AUDITED 并不代表全代码行审、原版可运行或主网实时数据验收。

| ID | 名称 | 类型 | 原有来源/链接 | 历史证据等级 | 本轮特别核查 |
|---|---|---|---|---|---|
| REF-001 | grok (当前正式项目) | 自有工程/专业历史 | [原来源](https://github.com/sunshihao001/grok) | SOURCE_AUDITED | GitHub PR14/16/17状态检查; 原有本体/PR工程 |
| REF-002 | 原 Solana Meme / GMGN 交易研究与 Hermes Workflow OS（跨域历史知识源） | 自有工程/专业历史 | [原来源](https://github.com/sunshihao001/-) | SOURCE_AUDITED | 历史覆盖账复用; README/learning非本轮逐行深读 |
| REF-003 | qb- GMGN单Mint程序 | 自有工程/专业历史 | [原来源](https://github.com/sunshihao001/qb-) | SOURCE_AUDITED | 历史覆盖账复用; 不是本轮新运行 |
| REF-004 | meme- 理论研究库 | 自有工程/专业历史 | [原来源](https://github.com/sunshihao001/meme-) | SOURCE_AUDITED | 历史覆盖账复用; 不是本轮新运行 |
| REF-005 | Why-Solana-Memecoins-Are-Over (个人fork) | 自有工程/专业历史 | [原来源](https://github.com/sunshihao001/Why-Solana-Memecoins-Are-Over) | SOURCE_AUDITED | 五跳历史源码/协议与既有研究继承 |
| REF-006 | Why-Solana-Memecoins-Are-Over (上游) | 学术/方法反证 | [原来源](https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over) | REPO_VERIFIED | GitHub仓库元数据核对 |
| REF-007 | Kelows/million | 开源成品/业务工作流 | [原来源](https://github.com/Kelows/million) | SOURCE_AUDITED | README, owners.service, live-feed, schema；多钱包同签名风险 |
| REF-008 | co-numina/holdtech | 开源成品/业务工作流 | [原来源](https://github.com/co-numina/holdtech) | SOURCE_AUDITED | README, app/lib/scan-core.ts；默认静态API键风险 |
| REF-009 | cinder-security/pumpwatch | 开源成品/业务工作流 | [原来源](https://github.com/cinder-security/pumpwatch) | SOURCE_AUDITED | README；只读发行/创作者研究流水线 |
| REF-010 | OKX OnchainOS Skills+CLI | 开源成品/业务工作流 | [原来源](https://github.com/okx/onchainos-skills) | SOURCE_AUDITED | README；市场只读 skill 与 wallet/支付工具同时存在 |
| REF-011 | GMGNAI/gmgn-skills | 开源成品/业务工作流 | [原来源](https://github.com/GMGNAI/gmgn-skills) | SOURCE_AUDITED | 仅继承原索引，未重新深入审 |
| REF-012 | Solana Microscope | 开源成品/业务工作流 | [原来源](https://github.com/solana-foundation/solana-microscope) | SOURCE_AUDITED | README；1-program scope, Carbon+Grafana/Loki, recovery/backfill |
| REF-013 | FnZero Solana Parser SDK Python | SDK/解析/索引 | [原来源](https://github.com/0xfnzero/sol-parser-sdk-python) | SOURCE_AUDITED | GitHub仓库元数据 |
| REF-014 | FnZero Solana Parser SDK Rust | SDK/解析/索引 | [原来源](https://github.com/0xfnzero/sol-parser-sdk) | SOURCE_AUDITED | GitHub仓库元数据 |
| REF-015 | Carbon Indexing Framework | SDK/解析/索引 | [原来源](https://github.com/sevenlabs-hq/carbon) | SOURCE_AUDITED | GitHub仓库元数据/README |
| REF-016 | solana-dex-parser-go | SDK/解析/索引 | [原来源](https://github.com/DefaultPerson/solana-dex-parser-go) | SOURCE_AUDITED | GitHub仓库元数据 |
| REF-017 | solana-dex-parser TypeScript | SDK/解析/索引 | [原来源](https://github.com/cxcx-ai/solana-dex-parser) | SOURCE_AUDITED | GitHub仓库元数据 |
| REF-018 | MadeOnSol SDK | SDK/解析/索引 | [原来源](https://github.com/MadeOnSol/madeonsol-sdk) | SOURCE_AUDITED | GitHub仓库元数据 |
| REF-019 | Helius core-ai | SDK/解析/索引 | [原来源](https://github.com/helius-labs/core-ai) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-020 | Yellowstone gRPC | SDK/解析/索引 | [原来源](https://github.com/rpcpool/yellowstone-grpc) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-021 | Raydium CP Swap | 链上协议/原理 | [原来源](https://github.com/raydium-io/raydium-cp-swap) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-022 | Pump public docs | 链上协议/原理 | [原来源](https://github.com/pump-fun/pump-public-docs) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-023 | Jito Solana Client | 链上协议/原理 | [原来源](https://github.com/Jito-Foundation/jito-solana) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-024 | Metaplex Token Metadata | 链上协议/原理 | [原来源](https://github.com/metaplex-foundation/mpl-token-metadata) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-025 | Solana Sniper Reverse Engineering | 学术/方法反证 | [原来源](https://github.com/Sorghobrayan-dotcom/solana-sniper-reverse-engineering) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-026 | MELT Dataset / Code | 学术/方法反证 | [原来源](https://github.com/git-disl/MELT) | REPO_VERIFIED | GitHub仓库元数据 |
| REF-027 | Grokbot Playbooks | Agent/Grok 工作流 | [原来源](https://github.com/sit-in/awesome-grokbot-playbooks) | REPO_VERIFIED | GitHub仓库元数据及README |
| REF-028 | Helius Enhanced/DAS/Parsed Events | 数据供应商/商业服务 | [原来源](https://www.helius.dev/solana-token-apis) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-029 | QuantBloc methodology / Base / MCP | 数据供应商/商业服务 | [原来源](https://quantbloc.com/methodology) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-030 | Triton / Fumarole / Old Faithful | 数据供应商/商业服务 | [原来源](https://triton.one/open-source) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-031 | Bitquery Solana API/Token Holder | 数据供应商/商业服务 | [原来源](https://docs.bitquery.io/docs/blockchain/Solana/solana-token-holders/) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-032 | DEX Screener | 数据供应商/商业服务 | [原来源](https://dexscreener.com/) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-033 | Solana Official Docs | 链上协议/原理 | [原来源](https://solana.com/docs/core/transactions/transaction-introspection) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-034 | Jito Docs | 链上协议/原理 | [原来源](https://docs.jito.wtf/lowlatencytxnsend/) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-036 | Meme Coin Factories (ACM CCS 2026) | 学术/方法反证 | [原来源](https://www.sigsac.org/ccs/CCS2026/program/accepted-papers.html) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-037 | A Midsummer Meme's Dream (USENIX 2026) | 学术/方法反证 | [原来源](https://www.usenix.org/conference/usenixsecurity26/presentation/mongardini) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-038 | RED-COHORT 2026 dataset | 学术/方法反证 | [原来源](https://zenodo.org/records/21765387) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-039 | Froggy V2 Scanner | 交易终端/社区经验 | [原来源](https://froggy-v2-0-by-shit101.gitbook.io/frogy-v2-0-by-shit101) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |
| REF-040 | Sputnik Parser / @sputniksol | 交易终端/社区经验 | [原来源](https://t.me/sputniksol) | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-041 | GMGN Terminal / CLI | 数据供应商/商业服务 | [原来源](https://gmgn.ai/) | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-042 | OnchainRadar | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-043 | Genesis Arbitrage | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-044 | ArbitrageScanner | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-045 | Synapse | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-046 | Axiom | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-047 | Photon | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-048 | TradeWiz | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-049 | Ray Bot | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-050 | Stratos | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-051 | Crypto GYM | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-052 | Eclipse Trencher | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-053 | taxiflip Axiom Dev Tracking教程 | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-054 | Arkham | 数据供应商/商业服务 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-055 | Nansen | 数据供应商/商业服务 | [原来源](https://www.nansen.ai/) | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-056 | Ethtective | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-057 | Resonance | 交易终端/社区经验 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-058 | BlockSec Phalcon | 数据供应商/商业服务 | [原来源](https://phalcon.blocksec.com/) | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-059 | CoinGlass | 数据供应商/商业服务 | [原来源](https://www.coinglass.com/) | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-060 | solana-foundation/transaction-v1-examples | 链上协议/原理 | [原来源](https://github.com/solana-foundation/transaction-v1-examples) | LINK_UNRESOLVED | 仅继承原索引，未重新深入审 |
| REF-061 | Meteora AMM | 链上协议/原理 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-062 | PumpSwap | 链上协议/原理 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-063 | Jupiter Aggregator | 链上协议/原理 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-064 | Clanker | 链上协议/原理 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-065 | Zora | 链上协议/原理 | 历史线索待核 | HISTORICAL_NAMED_ONLY | 仅继承原索引，未重新深入审 |
| REF-066 | RugCheck | 数据供应商/商业服务 | [原来源](https://api.rugcheck.xyz/swagger/index.html) | PAGE_VERIFIED | 仅继承原索引，未重新深入审 |

## 7. 新增17项逐项保留（不挤占旧编号）

| 新编号 | 名称 | 业务位置 | 来源 | 证据与约束 |
|---|---|---|---|---|
| NEW-01 | Pulse | market | [来源](https://github.com/nirholas/pulse) | 源代码/测试/数据模型局部核查；未部署；许可：MIT |
| NEW-02 | PumpTrace | investigation | [来源](https://github.com/AntC215/Pumptrace) | README/ARCHITECTURE/API源码核；缺LICENSE/测试/CI；许可：LICENSE_UNRESOLVED |
| NEW-03 | BLIX Trade | unified_market | [来源](https://github.com/blixvip/blixtrade) | 源码/CI/安全文档核；未实跑；大文件耦合待测；许可：MIT |
| NEW-04 | Bubblemaps | investigation | [来源](https://bubblemaps.io/) | 以前历史研究；本轮未拿到独立授权输出；许可：COMMERCIAL_UNCHECKED |
| NEW-05 | Cielo | monitor | [来源](https://cielo.finance/) | 本轮查官方开发者文档5 credits/跟踪钱包请求，费用价目未核；许可：COMMERCIAL |
| NEW-06 | PumpGrok | agent | [来源](https://github.com/swcstudiospace/PumpGrok) | README源码定位；scout pipeline未实现；不是常驻市场服务；许可：AGPL-3.0 |
| NEW-07 | dexterm | terminal | [来源](https://github.com/dexterm-xyz/dexterm) | 目录/README/docs核；实验真实信号需隔离；许可：AGPL-3.0-only |
| NEW-08 | Kol Quest | wallet | [来源](https://github.com/nirholas/kol-quest) | README/docs/源码目录核；供应商抓取合规待核；许可：LICENSE_TEXT_CHECK_NEEDED |
| NEW-09 | Solbeam | dashboard | [来源](https://github.com/CodeMuscle/solbeam) | README/目录/测试目录核，运营成熟度待验；许可：LICENSE_FILE_NOT_FOUND |
| NEW-10 | MemeTrace | screen | [来源](https://github.com/dilpreetsengh/MemeTrace) | README/目录核；非成熟基础底座；许可：UNKNOWN |
| NEW-11 | Meme Intelligence | research | [来源](https://github.com/arbincept/meme-intelligence-onchain) | README承认前瞻/因果限制；未做实时运行；许可：MIT |
| NEW-12 | ALTA | unknown | 身份未核，不编造 | 不能核实唯一仓库或成熟度；许可：UNKNOWN |
| NEW-13 | HyperGrok | unknown | 身份未核，不编造 | 不能核实唯一仓库或成熟度；许可：UNKNOWN |
| NEW-14 | find-the-insiders | investigation | [来源](https://github.com/karidasd/find-the-insiders) | 2026-11-04 仓库元数据核查；尚未源码审计；许可：UNKNOWN |
| NEW-15 | forensic-analysis-tool | investigation | [来源](https://github.com/Assylum-Labs/forensic-analysis-tool) | 仓库元数据核查；需与同组服务端一起验；许可：UNKNOWN |
| NEW-16 | forensic-tooling-server | investigation | [来源](https://github.com/Assylum-Labs/forensic-tooling-server) | 仓库元数据核查；不能假设生产完整；许可：UNKNOWN |
| NEW-17 | devtrack | creator | [来源](https://github.com/Archaneweb3/devtrack) | 仓库元数据核查；未执行，许可证待核；许可：UNKNOWN |

## 8. 全资产到原D01–D12的复用路线（不是增加本体）

| 既有研究/业务问题 | 原专业知识和协议真源 | 成熟产品/SDK复用选择 | 关键反证 |
|---|---|---|---|
| D01/D10 原始经济事件 | Solana/Pump/Jito文档、FnZero、Carbon、Microscope | 沿用成熟解析器/索引器，避免自写全量解码 | v0/ALT、inner CPI、Token-2022、WSOL、重复记账 |
| D02/D03 发行/池/微观结构 | PumpSwap/Raydium/Meteora/Jupiter, pumpwatch | Pulse/BLIX/OKX/GMGN市场业务与RugCheck服务 | 跨池/迁移/费用权利/价格与流量口径 |
| D04/D05 钱包/资金组织 | Hermes/qb-/Why-Solana, Million Funding | Million/BLIX/PumpTrace/Arkham/Nansen/Cielo/Bubblemaps | 共享Fee Payer/托管Hub/多跳不可识别/共同原因 |
| D06/D07 库存/群体演化 | 旧筹码状态/Why-Solana跨币关系 | HoldTech/PumpTrace/Million监控/Pulse时序档案 | 池Vault混入TopHolder/快照偏差/断流假停止 |
| D08/D09 策略与执行可达性 | meme-/MEV/Jito、历史Alpha研究 | dexterm/BLIX/Million 的paper/报价模块仅作研究参考 | 前瞻、样本选择、滑点、可卖深度和可复制性 |
| D11/D12 统计/AI知识进化 | Why-Solana/MELT/RED-COHORT/PumpGrok/Grokbot Playbooks | 只读MCP、证据研究、预注册基准、离线反馈 | 禁止让AI用描述性相关冒充经济控制/预测优势 |

## 9. 选型结论及下一步实际验收

**不能今天宣布唯一主程序**，但可以明确主体质量的技术评估顺序：先并行看 **Pulse（清晰数据分层）和 BLIX（完整产品/运维）**；以 **Million（钱包领域模型）和 dexterm（模块权限工程）** 做对照；将 Solana Microscope 作为基础设施可靠性强参照；PumpTrace作为取证垂直对照。其他项目按原65分类保持可查可用。

**最低验证闭环**：固定同一Mint+两钱包跨两Mint场景，先分别启动完全隔离的原版产品（无私钥/签名/外发通知/付费API自动请求），记录过程/失败/真实权限，然后做一个外部只读“钱包资金关系”扩展切片。衡量：修改扩散、数据正确性、UI连贯性、重启恢复、监控漏报和成本。只有验收过后才最终确定主体，并从其他产品按缺口补充。

**权限状态**：此报告只读第三方资料；GitHub的记录位于原知识PR#14派生的新草案分支，不修改main、PR#16工程或PR#17集成。未运行第三方程序、未调用付费API、未交易、未签名。

## 10. 可核对来源

- 原65索引：[grok 原知识索引](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/gpt-meme-project-index.v1.json)；原阅读覆盖：[2026-11-02 审读账](https://github.com/sunshihao001/grok/blob/knowledge/whole-spectrum-20261030-v1/knowledge/system/reference-assets-reading-coverage-2026-11-02.md)。
- 源码证据：[BLIX wallets.js](https://github.com/blixvip/blixtrade/blob/main/server/wallets.js) / [DB](https://github.com/blixvip/blixtrade/blob/main/server/db.js) / [test CI](https://github.com/blixvip/blixtrade/blob/main/.github/workflows/test.yml)；[Pulse stream](https://github.com/nirholas/pulse/blob/main/src/collector/solana-stream.ts) / [schema](https://github.com/nirholas/pulse/blob/main/src/db/migrations/001_init.sql)；[Million live-feed](https://github.com/Kelows/million/blob/main/apps/api/src/live/live-feed.service.ts) / [schema](https://github.com/Kelows/million/blob/main/apps/api/prisma/schema.prisma)；[PumpTrace architecture](https://github.com/AntC215/Pumptrace/blob/main/docs/ARCHITECTURE.md)；[HoldTech scan](https://github.com/co-numina/holdtech/blob/main/app/lib/scan-core.ts)；[Microscope](https://github.com/solana-foundation/solana-microscope/blob/main/README.md)；[PumpGrok](https://github.com/swcstudiospace/PumpGrok/blob/main/README.md)。
- 商业服务：[Cielo API](https://developer.cielo.finance/reference/addtrackedwallet)、[Nansen Solana Help](https://academy.nansen.ai/en/help/articles/9214978-solana-on-nansen)、[Meteora official](https://github.com/MeteoraAg)、[PumpSwap Docs](https://github.com/pump-fun/pump-public-docs/blob/main/docs/PUMP_SWAP_README.md)。

## 11. 本轮新增的跨协议范围与API成本纠偏

1. **REF-064 Clanker / REF-065 Zora**：官方[Clanker](https://github.com/clanker-devco/DOCS)主要面向 Base、Arbitrum 等 EVM 链；[Zora Coins](https://docs.zora.co/coins)采用 Uniswap v4 相关机制。可借鉴创作者费用、注意力发行、奖励权利设计，**不可直接把它们的账户/事件/DEX解析代码视为 Solana 业务功能**。Clanker是否存在扩展部署应按具体合约/链版本另核。
2. **REF-063 Jupiter 的版本及额度**：官方[Swap V2概览](https://github.com/jup-ag/docs/blob/main/swap/index.mdx)描述API Key要求，而[官方机器可读文档](https://github.com/jup-ag/docs/blob/main/llms.txt)给出匿名低速调用说明；两种表述的端点/额度条件应按实际请求和当前开发者门户核实，不能直接许诺“Jupiter永久零成本/无需授权”。研究阶段只允许获取报价，不执行下单路径。
3. **REF-061 Meteora**：现有产品不只一种池；[官方组织仓库](https://github.com/MeteoraAg/)提供 DLMM、DAMM v1/v2、动态Bonding Curve和Fee Sharing相关SDK/协议资料。市场发现与库存成本核算必须知道所选池的协议版本，不能以一套CPMM模型代替全部池。
4. **REF-054 Arkham / REF-055 Nansen**：商业链上标签与关系图可以帮助调查，但其“同经济主体/高胜率”等标签属于供应商方法，必须与原始链上证据和竞争解释区分。当前[Nansen帮助文档](https://academy.nansen.ai/en/help/articles/9214978-solana-on-nansen)表示Solana分析部分免费而API仍需要Pro资格：Web功能可用不代表可免费嵌入本地产品。
