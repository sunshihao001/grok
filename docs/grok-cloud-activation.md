# Grok Bot 云电脑落地验收手册

状态：GitHub 交接材料已准备；**尚未在用户 Grok Bot 账号的云电脑上执行**。GitHub 文件本身不会创建 Bot、Skill、Routine 或外部凭据。

## 设计决定

1. **Grok 云电脑是执行场所，不是真相数据库。** 代码、规则和知识的权威版本在审核过的 GitHub commit；观察事实来自带时间和交易/来源引用的原始记录。Bot 记忆不是证据。
2. **先验收离线工作流，再接真实数据。** 当前 GMGN 收集器的标准化 metrics 是空的；离线 fixture 正常不代表实时监控或经济优势成立。
3. **一个账号下的多个 Bot 共享同一云电脑和登录。** 开发 Bot 在独立 Git 分支/目录工作，最终 Monitor 只能读取审核冻结的规则；不要把 Bot 隔离当作安全边界。
4. **Grok Routine 不等于低延迟交易服务。** 默认 30 分钟示例只适合低频研究。Meme 的秒级交易机会需要独立验证的事件采集、延迟、滑点及交易费用测量，当前项目不执行真实交易。

## 首次接入：让一个 Bot 验收，而不是立即创建六个 Bot

先在 Grok Bot App 里使用现有主 Bot，或创建一个研究部署角色。完成以下一条任务后，再按 BOTS.md 分批启用 Rule Architect、GMGN Data、Wallet Structure、Evidence & Gate、QA 和最终 Monitor。不要让多个 Bot 同时修改共享状态。

### 可直接发给 Grok Bot 的第一条消息

> 你是 Solana Meme Workflow OS 的部署核验员。你要把现有项目接入你自带的云电脑并客观验收，而不是重新写空壳。
>
> 唯一目标仓库：https://github.com/sunshihao001/grok 。阅读 AGENTS.md、BOTS.md、CONTEXT.md、knowledge/README.md、docs/on-demand-research-design.md 和 docs/grok-cloud-activation.md。原来的 Hermes、meme-、qb- 和 Why-Solana 项目是按需研究来源，不要全量导入或安装 Hermes 运行时。
>
> 在云电脑上使用可信的 GitHub 连接或只读克隆，单独建立工作目录，记录完整的 commit SHA。运行 python3 scripts/grok_cloud_doctor.py。把原始 JSON 结果、命令、当前 commit、失败项带回对话。仅当全部离线检查通过时才称为 OFFLINE_READY。
>
> 额外做一次专家知识检验：对“同源资金意味着同一控制主体吗？”使用知识目录和来源索引寻找两个相关原始来源，展示来源链接和固定 commit、机制、适用条件、反例，以及下一项可以证伪的实际链上数据。不能仅凭关键词匹配给出主体身份结论。
>
> 没有权限、没有网络或缺少源码时报告 BLOCKED。不得伪造执行结果。不得创建 Routine、提交新规则、使用私钥、签名、交易或向第三方发消息。

### 云电脑终端的最低命令

~~~bash
git clone https://github.com/sunshihao001/grok.git
cd grok
git rev-parse HEAD
python3 --version
python3 scripts/grok_cloud_doctor.py
~~~

如果克隆或访问 GitHub 需要登录，仅使用 Grok 的连接应用/安全授权流程；不要把凭据粘贴到聊天或公开仓库。命令由实际 Grok 云电脑执行，本仓库仅提供操作说明。

## 通过标准与失败含义

| 检查 | 通过意味着 | 不意味着 |
| --- | --- | --- |
| required_files + python_3_11_plus | 所需文件与 Python 环境存在 | Bot 已经掌握知识 |
| offline_unit_tests | 代码离线测试通过 | 真实数据字段正确 |
| knowledge_lookup | 15 张卡片能被定向召回 | 已证明因果关系 |
| on_demand_research | 来源索引能给出可复核研究入口 | 已获取最新链上数据 |
| fixture_baseline + fixture_deltas | 两帧模拟观察可产生变化、知识候选与无交易输出 | 已进行实时监控 |

doctor 的 OFFLINE_READY 只代表以上离线检查全部通过；输出中的 gmgn_live_mapping_verified、grok_skill_published_verified 和 grok_routine_running_verified 在此阶段固定为 false，不能据此声称已上线。

## 专家理解验收：不能靠背诵知识库

至少做三组带原始出处与反例的对照问题：

- 同源资金与交易所/桥/公共基础设施是否会混淆？能否提出区分证据？
- 钱包协调或结构异常是否意味着可实现的跟单利润？能否考虑延迟、滑点、手续费、卖出流动性与选择偏差？
- 当时不可能看到的数据或事后标签能否被识别为未来信息，并从预测输入中排除？

每次交接至少包含：question、decision_at、knowledge_ids、source_url/commit、observed_facts、alternative_explanations、missing_evidence、rejected_hypotheses、next_check。拿不到真实事实时明确 UNVERIFIED。用无知识检索的基线与知识增强 Bot 做盲测比较，再判断 AI 是否摆脱空洞输出。

## 真实监控上线的前置门槛

第一阶段仅允许 BLOCK / WATCH / PAPER_ONLY / NEED_MORE_DATA。

1. GMGN Data Bot：人工核对原始回包的时间戳、币种、字段语义和单位，输出真实映射后的标准化观察。当前 metrics 空对象，因此此项未通过。
2. Wallet Structure 与 Evidence & Gate：验证竞争解释、缺失字段及来源链，不能凭持仓集中度单独认定同一主体。
3. QA：回放正例与负例，测误报、漏报、陈旧数据、重复事件及未来信息泄漏。
4. 工程：在定时运行前处理共享状态的单写者锁、异常恢复和备份。被 gitignore 排除的 .runtime 不会因 push 自动备份；云电脑恢复后软件包可能需要重装。
5. 人审：冻结规则版本。最后才在实际 Grok App 中把技能保存，按 routines/monitor.md 创建**暂停** Routine，使用安全数据 Test，通过后由人决定是否启用。

**未做过的事不得写为已完成**：本次只提供可执行的离线交接包，没有实际接管用户 Grok 云电脑，没有验证任何真实 GMGN 数据，没有创建 Bot Skill 或 Routine。

官方资料：
- https://docs.x.ai/grok-bot/overview
- https://docs.x.ai/grok-bot/get-started
- https://docs.x.ai/grok-bot/skills-routines-and-automations
- https://docs.x.ai/grok-bot/computer-and-apps
- https://docs.x.ai/grok-bot/troubleshooting
