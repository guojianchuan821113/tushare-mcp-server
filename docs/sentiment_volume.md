# 市场情绪与量能分析接口文档

## 📋 接口概述

`get_sentiment_volume(ts_code, trade_date)` 是一个专门用于分析股票市场情绪与量能的综合接口。该接口通过多个技术指标评估股票当前的市场参与度、资金流向与情绪倾向。

## 🎯 分析目标

本接口帮助回答以下关键问题：
- "市场对这只股票的关注度高吗？"
- "是资金流入还是流出？"
- "当前情绪是乐观、悲观还是冷漠？"

> 💡 **核心聚焦**：量能（Volume）+ 情绪（Sentiment），不判断价格方向，只判断**强度与倾向**

## 📊 输出字段详解

### 1. 换手率状态 (`turnover_status`)

**价值**：反映股票流动性和市场关注度，高换手常伴随趋势启动或变盘。

**判断标准**：
- 优先使用 `turnover_rate_f`（自由流通换手率）
- `turnover_rate_f ≥ 5%` → `"high_turnover"`（高活跃）
- `1% ≤ turnover_rate_f < 5%` → `"normal_turnover"`
- `turnover_rate_f < 1%` → `"low_turnover"`（流动性风险）

**回退机制**：自由流通换手率缺失时使用总换手率

### 2. 量比状态 (`volume_status`)

**价值**：衡量当前成交量相对于近期均量的放大程度，是短期情绪突变的领先指标。

**判断标准**：
- `volume_ratio ≥ 2.0` → `"volume_surge"`（量能激增）
- `0.8 ≤ volume_ratio < 1.5` → `"normal_volume"`
- `volume_ratio < 0.5` → `"volume_dry_up"`（交投清淡）

### 3. OBV趋势 (`obv_trend`)

**价值**：通过累积成交量判断资金流向，OBV上升 = 资金流入。

**判断逻辑**：
- `"rising"`：当日OBV > 前日OBV（资金流入）
- `"falling"`：当日OBV < 前日OBV（资金流出）
- `"flat"`：当日OBV = 前日OBV（无变化）
- `"data_unavailable"`：数据不足或首日数据

### 4. BRAR情绪 (`brar_sentiment`)

**价值**：BRAR指标将市场情绪分为买方力量和卖方力量。

**判断逻辑**：
- **常规情绪**：
  - `AR > BR` → `"bullish_sentiment"`（买方占优）
  - `AR < BR` → `"bearish_sentiment"`（卖方占优）
  - `AR ≈ BR`（差值 < 5）→ `"neutral_sentiment"`

- **极端情绪**：
  - `AR > 150` 且 `BR < 100` → `"overly_bullish"`（过度乐观）
  - `BR > 150` 且 `AR < 100` → `"overly_bearish"`（过度悲观）

### 5. VR容量比率 (`vr_status`)

**价值**：通过上涨日与下跌日成交量对比，衡量买卖力量平衡。

**判断标准**：
- `vr > 150` → `"bullish_volume"`（买盘强劲）
- `vr < 70` → `"bearish_volume"`（卖盘主导）
- `70 ≤ vr ≤ 150` → `"neutral_volume"`

### 6. MFI和PSY状态 (`mfi_psy_status`)

**价值**：
- **MFI**：成交量加权的RSI，>80超买，<20超卖
- **PSY**：上涨天数占比，>75超买，<25超卖

**输出格式**：组合字符串，如 `"mfi_overbought_psy_neutral"`，缺失数据时使用 `"mfi_na"` 或 `"psy_na"`，两者都缺失时返回 `"mfi_psy_unavailable"`

### 7. 综合市场情绪 (`market_sentiment`)

**价值**：融合多个指标给出总体情绪倾向判断。

**判断规则**：

#### 🔥 强烈看涨 (`"strongly_bullish"`)
**需同时满足**：
- `turnover_status == "high_turnover"` **或** `volume_status == "volume_surge"`
- **且** `obv_trend == "rising"`
- **且** `brar_sentiment == "bullish_sentiment"`
- **且** `vr_status == "bullish_volume"`

#### 🔴 强烈看跌 (`"strongly_bearish"`)
**需同时满足**：
- `turnover_status == "high_turnover"` **或** `volume_status == "volume_surge"`
- **且** `obv_trend == "falling"`
- **且** `brar_sentiment == "bearish_sentiment"`
- **且** `vr_status == "bearish_volume"`

#### 😴 市场冷漠 (`"apathetic"`)
**需同时满足**：
- `turnover_status == "low_turnover"`
- **且** `volume_status == "volume_dry_up"`
- **且** `obv_trend == "flat"`（或数据不可用）

#### ⚖️ 中性 (`"neutral"`)
其他情况，指标指向不一致

## 📈 使用示例

```python
from tushare_mcp_server.tech_ext import get_sentiment_volume

# 分析某股票的市场情绪
result = get_sentiment_volume("000001.SZ", "20240115")
print(result)
```

**输出示例**：
```json
{
  "ts_code": "000001.SZ",
  "trade_date": "20240115",
  "turnover_status": "high_turnover",
  "volume_status": "volume_surge",
  "obv_trend": "rising",
  "brar_sentiment": "bullish_sentiment",
  "vr_status": "bullish_volume",
  "mfi_psy_status": "mfi_neutral_psy_neutral",
  "market_sentiment": "strongly_bullish"
}
```

## 🔍 数据解读指南

### 强烈看涨情绪解读
- ✅ 市场高度关注（高换手或量能激增）
- ✅ 资金持续流入（OBV上升）
- ✅ 买方情绪占优（BRAR看涨）
- ✅ 买盘力量强劲（VR显示买方主导）

**适用场景**：趋势启动确认、突破信号验证

### 强烈看跌情绪解读
- 🔴 市场高度关注但方向偏空
- 🔴 资金持续流出（OBV下降）
- 🔴 卖方情绪占优（BRAR看跌）
- 🔴 卖盘力量强劲（VR显示卖方主导）

**适用场景**：下跌趋势确认、风险预警

### 市场冷漠解读
- 😴 交投极度清淡（低换手+量比萎缩）
- 😴 资金流动平缓（OBV持平）
- 😴 市场观望情绪浓厚

**适用场景**：震荡整理期、变盘前夜

## ⚠️ 使用注意事项

1. **数据依赖性**：部分指标需要历史数据，首日数据可能显示为`"data_unavailable"`

2. **阈值灵活性**：所有阈值基于经验设定，可根据具体市场环境和个股特性调整

3. **避免单一指标决策**：综合情绪需要多个指标一致指向，避免单一指标误判

4. **市场环境适应性**：
   - 牛市中阈值可适当放宽
   - 熊市中阈值可适当收紧
   - 震荡市中重点关注"冷漠"信号

5. **时间窗口选择**：本接口为单日分析，如需趋势判断建议结合多日数据

## 🔧 技术实现

### 数据源
所有指标均来自 `stk_factor_pro` 接口，使用前复权数据：

| 指标类型 | 使用字段 | 说明 |
|---------|---------|------|
| 基础量能 | `turnover_rate`, `turnover_rate_f`, `volume_ratio` | 换手率、量比 |
| OBV能量潮 | `obv_qfq` | 累积成交量指标 |
| BRAR情绪 | `brar_ar_qfq`, `brar_br_qfq` | 人气意愿指标 |
| VR容量比率 | `vr_qfq` | 成交量变异率 |
| MFI资金流量 | `mfi_qfq` | 资金流量指标 |
| PSY心理线 | `psy_qfq` | 市场心理指标 |

### 历史数据处理
- 获取当前交易日及前100天历史数据
- 按日期排序确保时间序列正确
- 使用索引定位当前交易日位置

### 异常处理
- 数据缺失时对应字段返回`null`
- 综合字段基于可用数据降级判断
- 错误信息统一返回格式：`{"error": "错误描述"}`

## 📚 相关接口

- [`get_trend_signals()`](trend_signals.md)：趋势信号分析
- [`get_oscillator_signals()`](oscillator_signals.md)：震荡指标分析
- [`get_volatility_profile()`](volatility_profile.md)：波动率分析

## 🔄 更新日志

- **v1.0.0**: 初始版本，实现完整的情绪与量能分析功能