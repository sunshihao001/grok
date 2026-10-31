# On-demand Source Registry｜固定版本文件指针，不是数据湖

当前 registry：knowledge/source_index.v1.json，**30个固定版本文件指针，来自8个仓库**。它服务按问题选择原始文件，不代表实时数据源已接通、接口权限已获得或源内容已独立复现。

## 来源覆盖

- sunshihao001/-：Hermes 钱包、来源关系、Sybil/协调和GMGN字段知识。
- sunshihao001/meme-：FCZ与策略语义（明确标记为未验证理论）。
- sunshihao001/qb-：GMGN只读原型和历史字段经验。
- sunshihao001/Why-Solana-Memecoins-Are-Over：协调null、资金/库存/退出路径、时间安全和失败案例。
- okx/onchainos-skills：候选只读市场/钱包接口文档；不是已接入数据源。
- xorextrace/cyberleek-onchain：原始交易资金复算方法。
- dnafund/Degen-Scanner：开发者/资金/买家路径源码。
- jayrabol/solana-holder-clusters：first-funder、owner映射、覆盖和聚类边界源码。

另有 knowledge/reference-project-discovery.v1.json 的**14个项目/论文发现记录**，其中部分只读了 README/元数据或官方文档，尚无精确文件级来源指针，不会伪装成可直接检索的30项内容。

## 路由命令

```bash
PYTHONPATH=src python -m solana_meme_os.research --question "同Slot多钱包买入是否为Jito Bundle？"
PYTHONPATH=src python -m solana_meme_os.research --question "历史分页不足时如何解释first funder未知？"
PYTHONPATH=src python -m solana_meme_os.research --question "SOL流入是否可能来自CloseAccount或LP释放？"
PYTHONPATH=src python -m solana_meme_os.research --question "如何用正常机器人生态建立协同检测null？"
```

检索结果是研究起点。必须打开具体原始文件/源码，核对commit、定义、样本范围、许可、作者主张和独立反例。多个专家引用同一来源不构成独立证据。

## Registry字段

每项记录必须固定 repository、commit、path、topics、why、kind、availability。当前统一标记 remote_on_demand；工具不会因此自动获取外部API或真实链上数据。
