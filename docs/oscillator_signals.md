# get_oscillator_signals 技术文档

## 接口概述

`get_oscillator_signals` 是一个专门用于分析股票震荡指标的函数，基于 Tushare 的 `stk_factor_pro` 数据，提供单日技术分析快照。

## 功能特性

### 核心分析维度

1. **RSI 相对强弱指数**: 判断超买超卖状态
2. **KDJ 随机指标**: 交叉信号和趋势强度
3. **Williams %R**: 动量震荡指标
4. **BIAS 乖离率**: 价格偏离均线程度
5. **CCI 商品通道指数**: 极端价格通道突破
6. **综合反转信号**: 多指标融合判断

### 分析逻辑

- **单日聚焦**: 专门分析指定交易日的震荡指标状态
- **多层次回退**: 每个指标都有备用数据源和放宽阈值
- **交叉信号检测**: 特别关注 KDJ 金叉/死叉信号
- **综合判断**: 通过多指标一致性来确定反转概率

## 最新优化 (v2.0)

### 🔧 修复的关键问题

1. **前一日日期计算错误**
   - **问题**: 之前使用简单的日历日计算 `int(trade_date) - 1`，导致月末/月初日期错误
   - **解决**: 改为获取历史窗口数据（最近100天），从实际交易日中找到前一交易日
   - **影响**: 修复了 KDJ 交叉信号在多数情况下的失效问题

2. **反转信号逻辑强化**
   - **问题**: 之前的 `reversal_signal` 判断过于简化，未充分结合乖离率
   - **解决**: 强化 strong 信号条件：必须同时满足金叉 + 乖离率 ≤ -4%
   - **影响**: 避免过度敏感的反转信号，提高准确性

3. **KDJ 状态处理优化**
   - **问题**: 当 KDJ 数据缺失时返回 `"neutral"` 而非 `None`
   - **解决**: 明确检查数据有效性，缺失时返回 `None`
   - **影响**: 提供更准确的数据状态指示

4. **异常处理精细化**
   - **问题**: 使用宽泛的 `except:` 捕获所有异常
   - **解决**: 改为 `except Exception:` 并保持降级处理逻辑
   - **影响**: 更好的调试支持和错误追踪

### 📊 技术实现改进

#### 修复前 vs 修复后对比

| 方面 | 修复前 | 修复后 |
|------|--------|--------|
| 前一日获取 | `int(date) - 1` | 历史窗口 + 实际交易日前一交易日 |
| KDJ缺失处理 | 返回 `"neutral"` | 返回 `None` |
| 反转信号逻辑 | 简单计数 | 金叉 + 乖离率条件强化 |
| 异常处理 | `except:` | `except Exception:` |

#### 核心代码改进

```python
# 修复前：简单的日期计算
df_prev = pro.stk_factor_pro(
    start_date=str(int(current_date) - 2),
    end_date=str(int(current_date) - 1),
)

# 修复后：历史窗口方法
df_hist = pro.stk_factor_pro(
    start_date=str(int(trade_date) - 10000),
    end_date=trade_date,
)
df_hist = df_hist.sort_values('trade_date').reset_index(drop=True)
current_idx = df_hist[df_hist['trade_date'] == trade_date].index[0]
if current_idx > 0:
    prev_row = df_hist.iloc[current_idx - 1]
```

## 功能特性

### 🎯 核心功能
- **超买超卖状态判断**: 识别股票当前是否处于技术性超买或超卖状态
- **反转信号分析**: 检测可能出现的技术指标反转信号
- **综合风险评估**: 提供短期反转概率的综合评估

### 📊 分析维度

#### 1. RSI 相对强弱指标 (`rsi_status`)
- **优先级**: 优先使用 RSI(6)，回退 RSI(12)
- **超买阈值**: RSI ≥ 70 (RSI12 为 ≥ 75)
- **超卖阈值**: RSI ≤ 30 (RSI12 为 ≤ 25)
- **输出**: `"overbought"` / `"oversold"` / `"neutral"`

#### 2. KDJ 随机指标 (`kdj_status`)
- **交叉信号**: 检测金叉和死叉
- **位置判断**: 结合 K 值位置判断信号强度
- **输出选项**:
  - `"bullish_crossover_in_oversold"` - 超卖区金叉（强烈看涨）
  - `"bearish_crossover_in_overbought"` - 超买区死叉（强烈看跌）
  - `"bullish_crossover"` / `"bearish_crossover"` - 普通交叉
  - `"overbought_risk"` / `"oversold_opportunity"` - 风险/机会
  - `"neutral"` - 中性

#### 3. 威廉指标 (`williams_r_status`)
- **使用字段**: 优先 `wr1_qfq` (N=6)，回退 `wr_qfq` (N=10)
- **超买**: ≥ -20
- **超卖**: ≤ -80
- **输出**: `"overbought"` / `"oversold"` / `"neutral"`

#### 4. BIAS 乖离率 (`bias_status`)
- **多周期分析**: 6日 → 12日 → 24日 逐级回退
- **偏离阈值**: ±5% → ±6% → ±7%
- **输出**: 
  - `"high_positive_deviation"` - 高正偏离（可能回调）
  - `"high_negative_deviation"` - 高负偏离（可能反弹）
  - `"normal_deviation"` - 正常偏离

#### 5. CCI 顺势指标 (`cci_status`)
- **异常区间**: > 100 或 < -100
- **输出**: 
  - `"overbought_or_breakout"` - 超买或突破
  - `"oversold_or_breakdown"` - 超卖或破位
  - `"normal_range"` - 正常区间

#### 6. 综合反转信号 (`reversal_signal`)
- **信号强度**: 强烈反转 → 中等风险 → 无信号
- **判断逻辑**: 至少2个指标处于极端区域才触发强烈信号
- **输出选项**:
  - `"strong_bullish_reversal"` - 强烈看涨反转
  - `"strong_bearish_reversal"` - 强烈看跌反转
  - `"moderate_reversal_risk"` - 中等反转风险
  - `"none"` - 无明显反转信号

## 使用方法

### 函数签名
```python
get_oscillator_signals(ts_code: str, trade_date: str) -> str
```

### 参数说明
- **ts_code**: 股票代码，如 "000001.SZ"
- **trade_date**: 交易日期，格式 YYYYMMDD

### 调用示例
```python
# 获取平安银行的震荡信号分析
result = get_oscillator_signals("000001.SZ", "20240115")
```

### 返回格式
```json
{
  "ts_code": "000001.SZ",
  "trade_date": "20240115",
  "rsi_status": "oversold",
  "kdj_status": "bullish_crossover_in_oversold",
  "williams_r_status": "oversold",
  "bias_status": "high_negative_deviation", 
  "cci_status": "oversold_or_breakdown",
  "reversal_signal": "strong_bullish_reversal"
}
```

## 技术实现特点

### 🔧 健壮性设计
- **数据容错**: 单个指标缺失不影响其他指标分析
- **回退机制**: 主要指标缺失时自动使用备用指标
- **异常处理**: 网络异常或数据异常时的优雅降级

### 📈 算法逻辑
- **多指标确认**: 反转信号需要多个指标确认，提高准确性
- **交叉检测**: 结合历史数据进行交叉信号判断
- **语义化输出**: 直接输出可行动的信号，而非原始数值

### ⚡ 性能优化
- **最小化API调用**: 只在需要交叉信号时才调用历史数据
- **缓存友好**: 单日查询避免重复数据获取
- **快速失败**: 数据缺失时立即返回，避免无效计算

## 应用场景

### 1. 短期交易决策
- 识别超买超卖区域，辅助买卖点选择
- 检测反转信号，提高入场时机准确性

### 2. 风险控制
- 监控持仓股票的技术风险
- 及时发现潜在的反转预警

### 3. 量化策略
- 作为因子输入机器学习模型
- 构建基于震荡指标的交易信号

### 4. 投资组合管理
- 评估组合中各股票的技术状态
- 优化资产配置时机

## 注意事项

### ⚠️ 使用限制
- **趋势市失效**: 强趋势行情中震荡指标容易失效
- **数据依赖**: 需要 Tushare 专业版数据支持
- **单一日期**: 当前仅支持单日查询

### 🎯 最佳实践
- **结合趋势分析**: 与趋势信号接口配合使用效果更佳
- **多周期验证**: 建议在不同时间周期验证信号一致性
- **风险管理**: 将信号作为决策参考，而非唯一依据

## 相关接口

- `get_trend_signals`: 趋势信号分析，提供趋势方向和强度判断
- `get_oscillator_signals`: 震荡信号分析，提供超买超卖和反转判断

两者结合使用可以获得更全面的技术分析视角。