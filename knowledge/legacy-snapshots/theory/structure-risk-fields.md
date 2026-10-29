# 结构风险评分字段表 v0.1

> 分线：D风险管理 / H指标规则 / G样本标注  
> 版本：v0.1  
> 状态：初版字段表  
> 目的：为后续样本标注、观察指标、多机器人审查提供统一字段。  

---

## 1. 字段分组

```text
A. 基础结构字段
B. 风险评分字段
C. 确认评分字段
D. 输出分类字段
E. 解释字段
```

---

## 2. 基础结构字段

| 字段 | 类型 | 含义 |
|---|---|---|
| symbol | string | 标的 |
| timeframe | string | 周期 |
| sample_time | datetime | 样本时间 |
| first_control_zone_detected | bool | 是否识别第一控盘区 |
| poc_level | number | POC价格 |
| vah_level | number | 价值区上沿 |
| val_level | number | 价值区下沿 |
| avwap_zonestart | number | 第一控盘区起点AVWAP |
| avwap_impulsestart | number | 第一波启动AVWAP |
| current_stage | string | 当前阶段 |

---

## 3. 风险评分字段

评分建议暂用：

```text
0 = 无明显风险
1 = 轻微风险
2 = 中等风险
3 = 高风险
```

| 字段 | 含义 |
|---|---|
| death_market_score | 死亡盘风险 |
| bull_trap_score | 诱多反抽风险 |
| failed_reclaim_score | 成本锚回收失败风险 |
| distribution_score | 派发/尾仓派发风险 |
| liquidity_trap_score | 流动性陷阱风险 |
| narrative_decay_score | meme叙事/热度衰减风险 |

---

## 4. 确认评分字段

评分建议暂用：

```text
0 = 无确认
1 = 弱确认
2 = 中等确认
3 = 强确认
```

| 字段 | 含义 |
|---|---|
| first_control_zone_score | 第一控盘区质量 |
| deep_washout_reclaim_score | 深洗后回收质量 |
| cost_anchor_acceptance_score | POC/AVWAP重新接受质量 |
| second_start_score | 二次启动确认质量 |
| structure_confirmation_score | 综合结构确认质量 |

---

## 5. 关键布尔字段

| 字段 | 含义 |
|---|---|
| value_area_reentered | 是否重新进入价值区域 |
| poc_reclaimed | 是否站回POC |
| avwap_reclaimed | 是否站回AVWAP |
| pullback_holds_anchor | 回撤是否守住成本锚 |
| second_push_confirmed | 是否二次拉升确认 |
| higher_low_after_reclaim | 回收后是否形成higher low |
| bos_after_reclaim | 回收后是否BOS |
| poc_rejected | POC是否拒绝 |
| avwap_rejected | AVWAP是否拒绝 |
| first_bounce_failed | 第一次拉起是否失败 |

---

## 6. 输出分类字段

| 字段 | 类型 | 可选值 |
|---|---|---|
| final_classification | string | no_trade / observe_only / candidate_for_deeper_review / second_start_candidate |
| allowed_mode | string | no_trade / observe / research_only / candidate |
| confidence_level | string | low / medium / high |
| primary_risk | string | death_market / bull_trap / failed_reclaim / distribution / liquidity_trap / none |
| primary_confirmation | string | first_control_zone / cost_anchor_acceptance / second_start / none |

---

## 7. 解释字段

| 字段 | 类型 | 含义 |
|---|---|---|
| positive_evidence | list[string] | 正向证据 |
| negative_evidence | list[string] | 风险证据 |
| missing_evidence | list[string] | 缺失证据 |
| invalidate_reason | string/null | 否决原因 |
| next_observation | string | 下一步观察重点 |

---

## 8. JSON 输出草案

```json
{
  "symbol": "MEME/USDT",
  "timeframe": "15m",
  "current_stage": "reclaim_pullback_test",
  "risk_scores": {
    "death_market_score": 1,
    "bull_trap_score": 1,
    "failed_reclaim_score": 0,
    "distribution_score": 1,
    "liquidity_trap_score": 1,
    "narrative_decay_score": 2
  },
  "confirmation_scores": {
    "first_control_zone_score": 3,
    "deep_washout_reclaim_score": 2,
    "cost_anchor_acceptance_score": 2,
    "second_start_score": 1,
    "structure_confirmation_score": 2
  },
  "signals": {
    "value_area_reentered": true,
    "poc_reclaimed": true,
    "avwap_reclaimed": true,
    "pullback_holds_anchor": true,
    "second_push_confirmed": false,
    "higher_low_after_reclaim": true,
    "bos_after_reclaim": false,
    "poc_rejected": false,
    "avwap_rejected": false,
    "first_bounce_failed": false
  },
  "final_classification": "candidate_for_deeper_review",
  "allowed_mode": "research_only",
  "confidence_level": "medium",
  "primary_risk": "narrative_decay",
  "primary_confirmation": "cost_anchor_acceptance",
  "positive_evidence": [
    "第一控盘区明确",
    "POC与AVWAP已站回",
    "回撤暂未跌破成本锚"
  ],
  "negative_evidence": [
    "尚未二次拉升确认",
    "meme热度恢复不足"
  ],
  "missing_evidence": [
    "BOS after reclaim",
    "second push confirmation"
  ],
  "invalidate_reason": null,
  "next_observation": "等待二次拉升是否突破第一次拉起高点"
}
```
