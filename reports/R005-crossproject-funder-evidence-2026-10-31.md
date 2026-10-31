# R005 交付与事实核查｜异常钱包跨项目源码研究（2026-10-31）

## 本轮真正的新证据
- **solana-holder-clusters**：`src/funders.ts` 中历史页满、首次交易没有识别到注资或 RPC 失败等情况返回 `null`；`src/clusters.ts` 中 `f === null` 进入 `independent.push(addr)`。该输出因此不应被统计/钱包专家解释成真正经济独立。这是可核对的**跨模块语义流失**，不是已计算过的真实误报率。
- 该项目还在第一笔交易中使用**其他账户最大的 SOL 净余额下降**作为候选 funder；当多指令、手续费、租金与多向转账同时存在时，不能将此启发式等同于直接解析的 System Transfer。
- **CyberLeek** `scripts/verify.py` 展示从原始交易提取 System Program outer/inner Transfer，按 source/destination/lamports/签名复算，从而提供更强的事实核查路径。
- **Degen-Scanner** `dev_tracer.py` 在次级样本发现中保留一部分已确认持币但 `sig_count=0`（可能由限流错误造成）的待查钱包；后续模型必须保留“数据未取到”的原因，不能用零当真实无历史。

具体锁定的 GitHub 代码及官方 RPC 说明见 [R005](../knowledge/research/R005-crossproject-funder-semantics-v1.md)。

## 本轮实际改动
1. 新增 `src/solana_meme_os/funder_evidence.py`：只读源状态分层，保留未知/未查/启发式/公共/高连接/疑似共享/唯一来源的区别，**不**推断独立经济受益人；
2. 新增 `tests/test_funder_evidence.py`：11 项合成测试，保护缺失状态不被跨层强行填充；
3. 新增 `knowledge/research/R005-crossproject-funder-semantics-v1.md`，将多仓库源码精读、竞争解释与可区分实验证据写成专题知识；
4. 在 `knowledge/expert-interaction-graph.v1.json` 中新增 **L37（数据历史覆盖→钱包角色）和 L38（钱包角色未知→统计基准）**，当前共 38 条交接；
5. 更新测试图合同、顶层专家 Skill、知识 README 与来源发现总论。

## 当前能够严谨宣称的验证等级
- 源码级：已重新取得并对比指定三个上游项目的源码；官方 Solana RPC 资料核对了余额数组与内指令、历史签名分页的语义。
- 项目级：相关 GitHub 文件写入草案分支；已使用 GitHub 接口检查内容、结构和引用（检验记录见本轮操作）。
- 静态：新增程序区分 9 种资金源证据状态，12 个旧参考研究领域之外没有宣称出现新的经济身份类。
- **未运行：** 11 项 Python 单测尚无真实运行记录；源码静态审查不能当代码通过测试，也不能说 M3 资金溯源已接入真实 Solana RPC。
- **未验证：** 真实钱包中的源地址错误比例、正常发行对照、群体同控概率、市场收益及 Grok 云端运行。

## 下一次判别性研究
取得一段带完整 signature 的真实发行 cohort 后，先对同一组钱包分别使用**最大净余额下降付款人近似**与**System Transfer 指令 sender 事实**，测量两者不一致的样本比例；同时记录历史分页/限流/取数失败和公共 hub 比例。随后检查这类源错误将改变多少个钱包群体、多少正常分母及哪些风险结论。

结果不是“更多钱包标签”，而是能知道**什么事实可用，什么解释尚待证实，某条原始证据出错时具体撤回哪些市场判断**。
