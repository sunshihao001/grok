# GPT 开发、GitHub 交付、Grok 云电脑运行

## 责任分工

GPT 负责研究、架构、编程、测试、知识维护、版本更新、故障修复。
GitHub 是权威源码、知识、测试、Skill 和发布版本的持久存储。
Grok 是云端运行操作员：拉取固定 Git 提交，运行 GPT 完成的程序，保留非秘密运行状态，回传错误。
用户负责第三方应用授权、安装、账户计费和监控规则发布审批。

C0–C4 是可按需调用的知识素材，不是 Grok 运行已完成程序的前置考试。Grok 不应该在云电脑临时设计 Agent 框架、重写代码、发明规则或擅自修复程序。

## 当前发布级别

这是 P0 纯离线、只读部署前验收。不是 B07 正式监控版本，也未接入真实链上/OKX 数据。PR 当前为 draft。

Grok 初次获得 GitHub 与云电脑授权后，只需进行一次克隆并固定提交：

    git clone https://github.com/sunshihao001/grok.git /workspace/grok
    cd /workspace/grok
    git fetch origin design/knowledge-system-v1
    git checkout --detach FULL_GPT_APPROVED_SHA

随后实际运行只需一个命令：

    python3 scripts/grok_operator.py --expected-sha FULL_GPT_APPROVED_SHA demo

将 FULL_GPT_APPROVED_SHA 替换为 GPT 交付的完整 40 位 SHA。不要把移动分支名当成已冻结发布版本；发布候选仍需人工批准。若工作目录已存在，先检查 git status 和有无运行中监控，不要强制覆盖/重置。

## 一键 demo 实际做什么？

1. 检查 Git 工作树和指定提交 SHA。
2. 运行知识审计和本地 unittest。
3. 用临时 SQLite 文件进行 B01 合成任务提交，以及 B02/B05 分别领取；检查重复领取。
4. 读取合成 OKX JSON，确认仅能作为未经验证的外部字段候选，不能升级为真实行情。
5. 用合成的两条 observation 运行 Monitor 变化检测，验证输出包含变化和不交易标记。
6. 输出 JSON，保存无秘密概要到 .runtime/grok-operator-last.json。

所有模块已经由 GPT 在 GitHub 中组合好；Grok 不需要手动运行五套 CLI 命令，也不用重新学习这些模块的实现原理。

**限制**：P0 demo 不访问 API、不安装 OKX、不付款、不读取私钥、不签名、不广播交易、不启用 Routine。运行通过仅代表具体云电脑的本地代码验证，不代表 Grok 已经创建七个 Bot 或有实时数据。

## 之后如何升级？

- GPT 在 GitHub 开发并通过 CI，再由人工审阅固定新 SHA。
- Grok 在确认无本地未提交变更、无运行中监控后切换到新 SHA，运行统一入口。
- 成功则记录新版本；失败时停止、回传 JSON，GPT 负责修复再发布。
- P1 再由 GPT 开发真正只读 RPC/OKX 接口及安全收费限制。
- P2 由 GPT 开发资金图、原始证据和样本外研究程序。
- P3 由 GPT 开发 B07 独立状态库、冻结规则载入、恢复和长期 Routine 所需检测。

对于真实数据、外部安装、带资费 CLI 和 Grok 私有 Skill 激活，仍需独立授权和实际环境验证。任何 Bot 不能把 fixture、文献报告或候选字段直接提升为监控发布依据。
