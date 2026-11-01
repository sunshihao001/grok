# Grok 云电脑本地程序集成：一次性验收任务（P0）

**只读/离线任务**。在 Grok 的真实云电脑里执行，不能把 GitHub Actions 的结果当成云电脑通过。不要安装任何第三方 npm 包、连接钱包、启用 Routine 或修改主分支。

## 0. 仓库和版本

确认当前位于 /workspace/grok 或你实际检出的项目目录，运行：

    git rev-parse HEAD
    git status --short

先报告 SHA 和未提交改动。若有脏工作树，先说明并停止更新，不要覆盖。确保对应提交包含 scripts/grok_cloud_doctor.py、runtime_store.py 与 okx_snapshot.py。

## 1. 本地运行环境

    python3 scripts/grok_cloud_doctor.py --repo . --audits --self-test

回传 JSON 中的 Git SHA、Python/Node 版本、Node 是否满足 OKX >=22.14.0、缺失命令、审计和测试。不要将 Node 存在误认为 OKX 已可用。

## 2. 多 Bot 最小研究交接（使用单独 demo DB）

    PYTHONPATH=src python3 -m solana_meme_os.runtime_store --db .runtime/demo-handoff.sqlite3 init
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store --db .runtime/demo-handoff.sqlite3 submit --input fixtures/bot-handoff-brief.fixture.json
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store --db .runtime/demo-handoff.sqlite3 claim --bot B02
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store --db .runtime/demo-handoff.sqlite3 claim --bot B05
    PYTHONPATH=src python3 -m solana_meme_os.runtime_store --db .runtime/demo-handoff.sqlite3 status --packet-id FIXTURE-B01-001

若该数据库曾被运行过，不要篡改已有审计记录，应使用新的 demo 路径。报告重复提交、领取和重启后状态。注意 CLI 的 Bot ID 只是任务标签，不能核实真正哪个 Grok Bot 执行。

## 3. 已保存 OKX JSON 的离线解析（完全不会访问 OKX）

    PYTHONPATH=src python3 -m solana_meme_os.okx_snapshot \
      --input fixtures/okx-price.synthetic.json \
      --operation token_price_info \
      --address EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

请报告输出的 status、候选数值、缺失字段以及 eligible_as_live_monitor_input；必须指出它仍是 synthetic。不要尝试执行 onchainos CLI；OKX 市场查询可能附带付款机制。

## 4. Grok 必须反馈

- 仓库 SHA、实际执行目录、运行工具的版本。
- 实际发出的命令、退出状态、测试通过/失败数。
- SQLite 任务第一次领取、重复领取和 B05 独立领取的结果。
- OKX 合成样例解析的结果和为什么不能作为真实行情。
- 未解决的安装/只读数据访问/权限/账单风险。
- 只提出一项下一步工程动作，不要重复讲解市场基础知识。

本任务完成条件是**可靠的本地程序交接链路**，不是 Grok 已经掌握全部专家知识，也不是已部署实时跟单或盈利策略。
