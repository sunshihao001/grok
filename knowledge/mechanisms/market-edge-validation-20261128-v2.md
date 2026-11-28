# MEME 专业优势竞争性验证与真实市场机制研究 V2.0
2026-11-28 | 承接 c96b80d48bdf1d1634b283771924b78e5582401b；证据状态 PUBLISHED_PREDICTION_RECALC + PUBLISHED_POOL_READ_RECALC + AUTHOR_REPORT + SOURCE_AUDIT；非本项目主网、模型训练、原始交易回放或盈利实证。分支沿用 V1，未改运行代码。
## 1. 实际计算：MELT 预测明细
来源 https://github.com/git-disl/MELT/tree/master/results ，论文 https://arxiv.org/html/2602.13480v2 。四个实际读取的公开CSV，全部6491条、独立Mint 6491、label=1共1575，跨文件Mint/标签不一致0，非法概率0。
|模型|源文件|blob SHA|AP|Top100/200/500/1000中非高风险数|
|---|---|---|---|---|
|LR|lr_pred_0.546495.csv|501327e871970a7558f40de251c0e398dcce9666|0.5464951215|82/147/319/575|
|RF|rf_pred_0.556894.csv|25376e18255b42d27fcd3377f6edc6003aec1426|0.5568940189|75/138/316/595|
|MLP|mlp_pred_8_0.573976.csv|f91d95076bdfdcb1a9b8d3aedc8f55e54e3a83f8|0.5739760547|85/152/346/594|
|XGB|xgb_pred_0.566936.csv|96c0dc07f56caae035a117b080b2773a4c30ba83|0.5669360497|77/147/337/600|
随机等量选取非高风险比例期望1575/6491=24.26%。MLP top100纯度85%，高风险比例15% vs 随机75.74%，下降60.74个百分点；但仅保留全部非高风险的85/1575=5.40%。Top1000 XGB纯度60%，略高于MLP59.4%，不能凭AP选唯一模型。非高风险是论文的中/低风险组合，不等于盈利或可交易。
标签语义审计：src/dataset.py blob daea3a0bdc20b86ad8133f043d59cbaaa1f122ee 将 high 编为0，其他1；src/train.py 写出 y_test 和 class1 prob，src/evaluate.py 对class1算AP。论文表7/8称 high=1，和当前公开代码相反；以代码解释本CSV而非表头。当前结果为单次发布预测，不等于论文5次平均；训练代码对每epoch测试并保存，不能证明epoch8选择独立于测试集。跨经济主体和时间切分的泄漏尚未验证。数据加载按 mint_ts 排序7:3，过滤销售持续不足60秒或持有者不足100。论文母体41470均已毕业；过滤后21635，故不能推广到全部发行。
可重现计算（本轮在JS中实际运行等价逻辑，以下Python为复现规格，未在本地重跑）：
```python
import pandas as pd
from sklearn.metrics import average_precision_score
from pathlib import Path
names = ["lr_pred_0.546495.csv","rf_pred_0.556894.csv","mlp_pred_8_0.573976.csv","xgb_pred_0.566936.csv"]
base = None
for name in names:
    d = pd.read_csv(Path("results") / name)
    assert len(d) == d.mint.nunique() == 6491
    assert d.label.isin([0,1]).all() and d.prob.between(0,1).all()
    y = d.set_index("mint").label.sort_index()
    if base is None: base = y
    else: assert y.equals(base)
    print(name, y.sum(), average_precision_score(d.label,d.prob),
          [int(d.nlargest(k,"prob").label.sum()) for k in (100,200,500,1000)])
```
## 2. 结构增量和经济损失：论文统计重算（非重新训练）
MELT表9：完整0.5729；无持仓/捆绑0.5268，差0.0461（相对8.75%）；去捆绑0.5451，差0.0278；去普通持仓0.5693，差0.0036；去市场活动0.5369，差0.0360。仅此证据支持风险分类中的结构补充价值，不是B1/B2纯市场基线严格对照；消融并非独立可加贡献。
表10作者按迁移价进入、随后一小时随机卖出时间模拟：随机top100损失60.71%，MLP损失26.64%，减少34.07百分点/相对56.12%；top200 64.84% vs31.47%，减少33.37百分点。全仍亏；未证实真实成交、退出、滑点、手续费或可复制利润。论文表7及§4报告基础筛选19835/41470=47.83%，其中约95%高风险；不能从四舍五入值推精确混淆矩阵。低复杂度基准先行。
## 3. 真实池储备序列核算
https://github.com/TrenchAutopsy/exit-liquidity-standard/blob/master/sample/flow_depth_series.csv blob 91472c1f7b44aa41eae229fa6cd645d3fcd59ca9；来源说明 SAMPLE_PROVENANCE.md blob f34df4ea772f908db9d1e72c41ba73fc99bbf3f9。公开真实链上储备导出（来源报告，未独立核链）；810行全部 ok=1、IN_BAND，各Mint一个池。按poll_ts排序，首次quote_depth_usd低于作者2500美元阈值，取紧邻前读：
|Mint前缀|行数|前深度USD|后深度USD|间隔秒|低于阈值读数|
|---|---:|---:|---:|---:|---:|
|1ptL88|374|9433.3526269|0.0008185674|36127.610|373|
|215bw6|436|9842.9150572|0.0000651584|600.412|433|
降幅99.9999913%/99.9999993%。同一池报价侧储备是单池可支出的物理上界（不等于任意仓位可成交金额）；不能从两次读数推断坍塌精确时点、资金去向或撤池/卖出原因。73h公开样本含标签72h后额外读数，勿混淆。两币按已死亡且曾有深度选出，不能估计风险率/预测效果；样本无swap，不能证实独立需求。重现：pandas读CSV，按mint_address分组，过滤ok==1、sol_band_status=='IN_BAND'，按poll_ts排序，取首次quote_depth_usd<2500和前一行，计算1-after/before与时间差；若首行已低于阈值则前状态未知。
## 4. 原参考项目的重大更新：经济循环与交易优势分离
原作者 https://github.com/searadacunha/Why-Solana-Memecoins-Are-Over （外部研究，不是本人的旧fork）。已读三个结果文件：
- economic_mechanics/results.md blob e9f6c8df1cacbc4823030794d4daa0e9a80fdbe1：协调群体的代币首次移动多数是转账而非出售；资金回流和下一发行重复支持共同经济过程，但无法判定真实身份或独立服务。
- exit_destination/results.md blob cebbf7217b71e7dcdae18103d18cbf8056913af7：148发行、1457事件、300反复出现退出钱包的定向样本；作者报告631/1280（49.30%）资金转移严格回至原出资方，607/1161（52.28%）有转账事件关联后续发行资金循环；17/24有转账的运营组闭环，其他7未知；361事件触及交易数上限。6,049次出售的观察支持转仓与卖出分离。结果是选定样本的取证，不代表全部市场或已识别真实身份。
- post_detection_edge/results.md blob 2a89e77cb3f92340275f46067b37e95b1dfaafda：1657实时报警，最终12预锁信号仅1保留预测提升（15分钟触及2倍31.0%→45.7%，n=164），作者称计成本后仍亏、盈亏平衡胜率58.5%。检测后价格不是成交价；大量断线/未观察样本。重算14.7个百分点预测提升、距离其盈亏平衡12.8个百分点。已读结果，未执行原作者脚本。与V1 Gafarov为不同采集窗口和研究设计的同方向负面证据，不是同一数据合并。
认知修正：经济行为路径存在与可交易优势分离；钱包余额下降可能仅从执行地址转向卖出地址。独立需求必须以真实净卖出、接收/关联关系不确定区间、对手买方实际支付、同一时间池状态来检验。只知道卖方网络还不能证明买方独立；价格稳定不是证明。研究新问题：在已确认实际出售而非转账后，非已关联买方的净流和可卖深度是否恢复，并且超过基础净流基准？B3仍 UNKNOWN。
## 5. 数据可达性和下一轮最小实证
GMGN数据 https://github.com/ian05012/solana-memecoin-dataset ：查目录确认tokens parquet 11015418字节，四trade分片合计约274MB；尝试本地HTTP下载，DNS不可用，连接器不支持二进制，未实际读取这些数据。README与scripts/collect.py blob 2843ec5137dbb9c0c9f4a1d0b8e3aec16e3c5ec4：公开精简采集器在请求多个接口前记captured_at，最近200交易计算时用time.time()，缺乏每字段实际可用时间，不能自动认定时间无泄漏；精简脚本不等于真实历史生成代码。trade表仅wallet/token/side/amount_usd/ts，无token数量、签名、池储备；不能单独重建库存守恒或可执行报价。MELT原始parsed traces和feature.pkl在Google Drive，未下载。下一优先从MELT标签、逐币feature（或可访问文本子集）、含swap数量和池储备的来源获得同母体B1/B2/B3；不为凑原始回放伪造数据。先核label可用时间、group划分、候选预算；模型评价不替代经济评价。
新增候选 TrenchAutopsy：公开储备样本和schema作为退出证据参考；未获得其全母体，不接入生产。优先风险基准/真实退出，同时独立需求假说保持竞争性地位。V2未形成完整B0/B1/B2/B3共同母体实验、未运行模型或交易、不改Blix、不签名、不付款。
