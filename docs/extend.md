# Tushare MCP Server 扩展接口文档

本文档描述了 Tushare MCP Server 的扩展接口，这些接口基于基础 Tushare 数据提供了更高层次的分析功能。

## get_trend_signals - 股票趋势信号综合分析

### 接口概述

`get_trend_signals` 是一个基于 `stk_factor_pro` 数据的高级分析接口，提供多维度的股票趋势信号分析。该接口融合了价格、均线、MACD、动量等多个技术指标，为量化交易和投资决策提供综合的趋势判断。

### 功能特点

- **多维度分析**: 同时分析价格位置、均线排列、MACD信号、趋势强度和动量变化
- **穿越检测**: 智能识别价格穿越均线、MACD金叉死叉等关键信号
- **趋势综合**: 基于多重条件判断整体趋势方向，避免单一指标的假信号
- **强度评估**: 基于历史数据评估当前趋势的相对强度
- **动量监控**: 跟踪趋势动量的加速、减速和反转状态

### 参数说明

| 参数名 | 类型 | 必需 | 说明 |
|--------|------|------|------|
| ts_code | str | 是 | 股票代码，如 "000001.SZ" |
| trade_date | str | 否 | 交易日期，格式 YYYYMMDD |
| start_date | str | 否 | 开始日期，格式 YYYYMMDD |
| end_date | str | 否 | 结束日期，格式 YYYYMMDD |

> **注意**: 必须提供 `trade_date` 或 `start_date/end_date` 组合之一

### 返回字段说明

接口返回包含以下6个核心趋势信号的JSON数组：

#### 1. price_vs_ma5 - 价格与5日均线关系

判断价格相对于短期趋势的位置和穿越状态：

- `"crossing_up"`: 向上穿越 - 前一日收盘价 ≤ MA5，当日收盘价 > MA5
- `"crossing_down"`: 向下穿越 - 前一日收盘价 ≥ MA5，当日收盘价 < MA5  
- `"above"`: 价格在均线上方 - 当日收盘价 > MA5
- `"below"`: 价格在均线下方 - 当日收盘价 < MA5

#### 2. ma5_vs_ma20 - 均线排列状态

判断短期趋势与中期趋势的对齐关系：

- `"bullish_alignment"`: 多头排列 - MA5 > MA20，短期趋势向上
- `"bearish_alignment"`: 空头排列 - MA5 < MA20，短期趋势向下

#### 3. macd_status - MACD信号

基于MACD指标的趋势和动量信号：

- `"golden_cross"`: 金叉信号 - DIF线向上突破DEA线
- `"death_cross"`: 死叉信号 - DIF线向下跌破DEA线
- `"positive_momentum"`: 正向动量 - DIF > DEA 且 DIF > 0
- `"negative_momentum"`: 负向动量 - DIF < DEA 且 DIF < 0
- `"recovering"`: 恢复期 - 其他状态，如零轴附近的纠缠

#### 4. trend_direction - 综合趋势方向

基于多重条件的整体趋势判断：

- `"up"`: 上涨趋势 - 满足 MA5 > MA20、收盘价 > MA5、MACD非死叉状态
- `"down"`: 下跌趋势 - 满足 MA5 < MA20、收盘价 < MA5、MACD非金叉状态  
- `"sideways"`: 横盘震荡 - 不满足上述明确趋势条件

#### 5. trend_strength - 趋势强度

基于MACD柱状图历史分位数的相对强度评估：

- `"strong"`: 强势 - 当前MACD绝对值处于20日数据的75%分位以上
- `"weak"`: 弱势 - 当前MACD绝对值处于20日数据的25%分位以下
- `"moderate"`: 中等 - 介于强势和弱势之间

#### 6. momentum_change - 动量变化

基于动量指标的变化趋势：

- `"accelerating"`: 上涨加速 - 动量正值且数值增大
- `"decelerating"`: 上涨减速 - 动量正值但数值减小
- `"accelerating_down"`: 下跌加速 - 动量负值且数值减小（负得更多）
- `"decelerating_down"`: 下跌减速 - 动量负值但数值增大（负得减少）
- `"reversing"`: 动量反转 - 动量符号发生改变（正转负或负转正）

### 返回格式

接口根据查询参数智能返回不同格式：

- **单日查询**（使用 `trade_date`）：返回单个JSON对象
- **多日查询**（使用 `start_date`/`end_date`）：返回JSON对象数组

#### 返回示例

**单日查询返回示例：**
```json
{
  "ts_code": "000001.SZ",
  "trade_date": "20240115", 
  "price_vs_ma5": "above",
  "ma5_vs_ma20": "bullish_alignment",
  "macd_status": "positive_momentum",
  "trend_direction": "up",
  "trend_strength": "strong",
  "momentum_change": "accelerating"
}
```

**多日查询返回示例：**
```json
[
  {
    "ts_code": "000001.SZ",
    "trade_date": "20240115", 
    "price_vs_ma5": "above",
    "ma5_vs_ma20": "bullish_alignment",
    "macd_status": "positive_momentum",
    "trend_direction": "up",
    "trend_strength": "strong",
    "momentum_change": "accelerating"
  },
  {
    "ts_code": "000001.SZ",
    "trade_date": "20240116", 
    "price_vs_ma5": "crossing_up",
    "ma5_vs_ma20": "bullish_alignment",
    "macd_status": "golden_cross",
    "trend_direction": "up",
    "trend_strength": "strong",
    "momentum_change": "accelerating"
  }
]
```

### 使用示例

#### 示例1：获取单只股票特定日期的趋势信号

```python
# 获取000001.SZ在20240115的趋势信号
get_trend_signals(ts_code="000001.SZ", trade_date="20240115")
```

返回单个JSON对象（适合单日分析）：
```json
{
  "ts_code": "000001.SZ",
  "trade_date": "20240115", 
  "price_vs_ma5": "above",
  "ma5_vs_ma20": "bullish_alignment",
  "macd_status": "positive_momentum",
  "trend_direction": "up",
  "trend_strength": "strong",
  "momentum_change": "accelerating"
}
```

#### 示例2：获取股票一段时间内的趋势变化

```python
# 获取000001.SZ在2024年1月的趋势信号序列
get_trend_signals(
    ts_code="000001.SZ", 
    start_date="20240101", 
    end_date="20240131"
)
```

返回JSON数组（适合趋势跟踪）：
```json
[
  {
    "ts_code": "000001.SZ",
    "trade_date": "20240101",
    "price_vs_ma5": "below",
    "ma5_vs_ma20": "bearish_alignment",
    "macd_status": "negative_momentum",
    "trend_direction": "down",
    "trend_strength": "weak",
    "momentum_change": "decelerating_down"
  },
  {
    "ts_code": "000001.SZ",
    "trade_date": "20240115", 
    "price_vs_ma5": "crossing_up",
    "ma5_vs_ma20": "bullish_alignment",
    "macd_status": "golden_cross",
    "trend_direction": "up",
    "trend_strength": "strong",
    "momentum_change": "reversing"
  }
]
```

### 应用场景

1. **趋势跟踪策略**: 使用 `trend_direction` 和 `ma5_vs_ma20` 识别和跟随主要趋势
2. **买卖时机选择**: 结合 `price_vs_ma5` 的穿越信号和 `macd_status` 的金叉死叉
3. **风险管理**: 通过 `trend_strength` 评估持仓风险，强趋势时适当增加仓位
4. **动量策略**: 利用 `momentum_change` 识别趋势加速和减速阶段
5. **多因子选股**: 综合多个信号筛选处于强势上涨趋势的股票

### 注意事项

1. **数据依赖性**: 该接口依赖于 `stk_factor_pro` 提供的技术指标数据，确保相关字段存在且数据质量良好
2. **历史数据要求**: 部分信号（如穿越检测、强度评估）需要一定量的历史数据，新上市股票可能无法生成完整信号
3. **参数调优**: `trend_strength` 的阈值（如0.5、0.1）可根据具体股票的价格水平进行调整
4. **市场环境**: 不同市场环境下信号的有效性可能不同，建议结合其他分析工具使用
5. **滞后性**: 基于历史数据的趋势信号存在一定滞后性，不适合高频交易场景

### 技术实现

该接口内部实现逻辑严格按照设计文档执行，并针对生产环境进行了优化：

1. **数据获取**：通过 `pro.stk_factor_pro()` 获取基础技术指标数据
2. **时间序列处理**：按交易日期排序确保时间序列正确性
3. **信号计算**：逐日计算六个维度的趋势信号
4. **相对强度评估**：使用相对MACD（MACD/收盘价）避免股价绝对值影响
5. **智能返回格式**：根据查询参数自动返回单对象或列表
6. **健壮性保障**：完善的空值检查和异常处理

#### 核心改进点

- **`trend_direction`**：直接使用原始数值判断，避免对字符串状态的依赖
- **`trend_strength`**：采用相对MACD值，解决不同股价水平的比较问题
- **`momentum_change`**：优化判断顺序，先检测反转再判断加速/减速
- **返回格式**：单日查询返回对象，多日查询返回数组，提升大模型使用体验

接口源码位于 `/Users/jason/Downloads/tushare-mcp-server/src/tushare_mcp_server/server.py`，可查看具体实现细节。