# MEME 真实市场需求质量、价格形成与优势可捕获性实证 V4.0
2026-11-28 | 承接 30677ae3022b64df7c1c3b8fe683f9dd6857d3a2，沿用原研究分支。证据 PUBLISHED_EVENT_RECALC / EXPLORATORY_TEMPORAL_TEST / SOURCE_AUDIT；非独立RPC核验、生产策略或净收益实证。无运行代码改动。
## 1. 同池成交与储备核算
来源 datastore.sh (2026), Pump.fun PumpSwap AMM Historical Data Sample, https://huggingface.co/datasets/DataStore/pumpswap-amm-historical-data-sample （CC BY-SA 4.0）；说明 https://huggingface.co/datasets/DataStore/pumpswap-amm-historical-data-sample/blob/main/README.md 。通过公开预览直接读取同一pool、同slot两行，而非下载全文件。数据集服务器rows接口不可达，本地HTTPS DNS失败，GitHub样本路径404。预览中顺序并非链上顺序；按slot、tx_index、ix_path对齐。
pool=5qkKu9cjHdMnz4ZjZnT8D9terboob6ADioJaZ29e85dR，slot=425520001，2026-06-10 09:38:33 UTC，两行ix_path=[3,0]，ix_name=buy_exact_quote_in。
|tx_index|sig|base reserve raw|quote reserve raw|base out|quote_amount_in_with_lp_fee|quote_amount_in|max_quote_amount_in|user_quote_amount_in|lp_fee|protocol_fee|creator_fee|
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|1332|2zcx6f7zE2b6uQBHWU8KS8E3kiDg9fxwwtyxnMktPW1ZQ…（签名前缀，按池/区块/序号定位）|130041653963294|139355382440|454843233207|490108694|495000000|495000000|489130433|978261|244566|4646740|
|1333|2y9gF3N3GHULsUv4cmMaUzL9xmar1Xo1UxbsKRX6UoUm63NY3veWnneUwrXih4MQUjCr6QQovJU4gJX6qBGeT1yX|129586810730087|139845491134|9064346865|9802173|9900000|9900000|9782607|19566|4892|92935|
实际BigInt核算：X0-base_out1=X1、Y0+quote_amount_in_with_lp_fee1=Y1，两项残差0。支持这两行储备为成交前，而README称成交后；仅局部证据，不推广全库。价格代理 p=Y/X（raw单位，未验证mint方向、decimals，不称SOL/代币），p0=.0010716211167179936，p1=.0010791645410988665，变动+0.70392644%；第一笔入池报价资产/初始报价储备=.3516969961%；k增加.0006995355%。第二笔推算X2=X1-base_out2、Y2=Y1+quote_amount_in_with_lp_fee2，p2=.0010793156788927512，较p1+0.01400507%，累计+.71803010%；没有第三快照，不能称实测。两行 gross quote_amount_in - protocol_fee - creator_fee = quote_amount_in_with_lp_fee；但user_quote_amount_in与入池金额差分别-978261/-19566，恰为负LP fee；README明确exact-in不能直接用普通buy公式。未解清真实钱包扣款与全部费用，未使用该字段计算交易利润。
实际经济意义：前一笔资金造成的价格变化已经进入下一笔成交前状态；观察到真实买入不自动拥有买入前价格。相同资金规模在不同储备条件产生不同冲击。对本池假设恒定乘积且无卖出费，用第一笔得到的base数量，在第一笔后按Y1*b/(X1+b)估算卖出489133853.64 raw，第二笔后估算489202237.50 raw；不是历史报价/成交，忽略手续费与其他订单，不作收益结论。
## 2. 新协议语义反例（独立竞争路线：执行/流动性语义，而非钱包评分）
Pump官方 https://github.com/pump-fun/pump-public-docs/blob/main/docs/VIRTUAL_QUOTE_RESERVES_FEE_ADJUSTMENT.md ，blob 14d7c316bad91feb976d06e3f88955ae637ea609：较新v2及multi_hop场景中协议/创作者费暂存vault，不属于定价流动性；effective_quote_reserves=raw vault+signed virtual_quote_reserves；fee sweep使raw减少但virtual反向变化，定价有效储备不变；boost还可能使有效储备含额外虚拟部分。因此raw vault、定价有效储备、实际可兑现余额必须区分。历史六月样本没有该字段，不能倒用新版本或假设boost/费率。V2的原生储备案例仅物理约束，不能直接推广为全部协议定价状态。要按历史程序版本和池类型核验。
## 3. 首次探索性样本外对照：基础价格/流量 vs 增加净库存代理
复用V3的11个独立Mint事件文件，不复用V3的60秒切片。原始公开解析事件1204条，严格买卖符号一致（achat token>0 SOL<0；vente token<0 SOL>0），共1141条；每Mint按原文件顺序划分不重叠40条记录块，前20特征、后20结果；特征和结果交界同秒的块排除（9块），仅12块可用，按Mint首次曲线时间前7币训练8块、后4币测试4块（实际后4中QAMI零块，测试3币）。不保证训练窗口实际结束时间均早于测试所有时间，需查cut；切分依据发行时点，以下cut/持续时间可复查；为本轮探索性自定规格，非预注册。
price_proxy=abs(signer SOL delta/token delta)，不是池价格或成交报价，含费用/账户余额影响。mom=log(特征最后5笔单位价格代理中位数/最初5笔中位数)。flow=(买方SOL减少-卖方SOL增加)/(两者和)。retain=Σ_wallet max(0,窗口买入token-窗口卖出token)/总买入token；是交易净增加代理、不是实际持仓，未识别转账、主体和同控；同一窗口内不使用未来交易。目标 y=log(结果块末5笔代理中位数/特征末5笔代理中位数)>0。结果时长不同，不能当统一时间持仓策略。
|Mint|split|块起点(0-based)|flow|mom|retain|未来log变化|cut epoch|未来秒|
|---|---|---:|---:|---:|---:|---:|---:|---:|
|VISUALIZE|train|40|.445665|.322607|.864258|.165167|1726264876|38|
|RAO|train|0|.767551|.181022|.870880|.533223|1730203105|120|
|RAO|train|40|.675621|.456118|.777519|.327807|1730203334|76|
|SAFFRON|train|0|.962984|.276746|.983507|.372549|1731452179|18|
|BLT|train|0|.607980|.397548|.725601|.345247|1732052657|25|
|BLT|train|40|-.709384|-.611438|.682824|-.151857|1732052699|408|
|ACID|train|0|.329218|.169168|.481022|.355463|1733737909|95|
|symx|train|40|.227988|.110966|.792179|.911032|1734741044|16138|
|sumiko|test|40|-.677161|-.401285|0|.475631|1735219745|369|
|LEXICON|test|0|.452594|-.005014|.612351|1.673260|1735504113|4|
|MIKU|test|0|.982454|.165071|.994560|-.132500|1735711414|2|
|MIKU|test|80|.517049|-.003834|1|-.263647|1735711436|10|
原始e1 blob见V3；额外 CHOCO 44090fc6606ec2141124b760ac8f8cebc7f504e7、MIKU 66b7c1e07b7e26544e6960e4f9c475d47449613d、QAMI df8393203919901cd2de13b67f24b1f2b5b34120。排除块：ACID40、CHOCO0、MIKU40、QAMI0/40、SAFFRON40、VISUALIZE0、sumiko0、symx0。注意1141是符号过滤记录数而非独立样本；未考虑共同钱包跨Mint泄漏。
实际JS拟合逻辑：训练特征按训练均值及总体标准差标准化；零初始系数的logistic，1500步全批量梯度下降，lr=.05，非截距L2梯度系数=.1；阈值.5。常数基准训练正类7/8=.875；测试2正2负。
|模型|4个测试上涨概率（按表顺序）|正确数|Brier（低好）|
|---|---|---:|---:|
|常数基准|.875/.875/.875/.875|2|.390625|
|基础flow+mom|.38751963/.91823830/.97645872/.92587447|1|.5481330887|
|基础+retain|.28503508/.91171228/.97980285/.93685101|1|.5891682490|
增加retain后Brier恶化.04103516；两模型皆差于常数；训练正类7/8偏斜、测试3币仅4块、观察期限2–369秒（训练最长16138秒），不能统计证明库存代理无效，也不能用于交易。测试MIKU两块retain近1仍价格代理下跌；sumiko retain=0却上涨。是反例与弱实证，不是完整B1/B2/B3、独立需求预测或实际收益检验。
## 4. 实际裁决与下一步
保留真实需求研究为候选，不把高净库存代理当买入触发；先验证与市场基础信息相比的增量，固定实际可用时点、固定持有时间与真实双向报价，分发行者/经济主体/时间留出。不能连续获得同池完整swap+transfer+reserve，不能核算经济主体库存和需求持续性；没有新证据证明获利。
竞争研究方向：A 延续库存承接但要求主体归因与后续可执行报价；B 研究同一信号出现后可获取的剩余价格空间、费用与成交时滞，先做真实退出否证；C 研究流动性/有效储备/协议版本对风险判断的影响，不能将fee sweep错误归为需求崩塌。优先B/C作为数据可验证性更高的约束研究，不提前建系统。当前数据源获取障碍应先解决：开放完整事件/池状态、可用时间及费用版本；不能重复拿同一小样本反复调参。保留V1–V3结果、未签名、未付款、未交易、未合并主干。
