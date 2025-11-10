# 申万一级行业指数盈利增长分析模块

## 功能概述

新增模块用于计算申万一级行业指数的**最新季度加权净利润同比增速**，作为行业景气度核心指标。

## 核心功能

### 1. 单个行业盈利增长计算

```python
from sector_index import get_industry_profit_growth

# 计算传媒行业盈利增长
result = get_industry_profit_growth('801760.SI', '20251110')
print(result)
```

返回结果格式：
```python
{
    'industry_code': '801760.SI',
    'industry_name': '传媒',
    'profit_yoy_weighted': 15.67,  # 加权扣非净利润同比增速 (%)
    'valid_stock_count': 45,       # 有效参与计算的成分股数量
    'total_stock_count': 50,       # 该行业当月总成分股数量
    'data_quality_flag': 'clean'   # 数据质量标记
}
```

### 2. 批量分析所有行业

```python
from sector_index import evaluate_all_industries_profit_growth

# 分析所有申万一级行业
result_df = evaluate_all_industries_profit_growth()
```

### 3. 命令行使用

```bash
# 运行估值分析（默认）
python sector_index.py

# 运行盈利增长分析
python sector_index.py profit_growth
```

## 数据处理规则

### 数据来源

1. **行业成分股权重**：调用 `index_weight()` 接口
   - 使用最近一个完整月份的数据
   - 权重字段：`weight`（单位：百分比）

2. **个股扣非净利润增速**：调用 `fina_indicator()` 接口
   - 优先使用 `dt_netprofit_yoy`（扣除非经常性损益后的净利润同比增长率）
   - 若缺失，则使用 `netprofit_yoy` 作为替代，并记录警告

### 数据质量控制

- **权重有效性**：剔除 `weight <= 0` 或 `NaN` 的成分股
- **财务数据有效性**：剔除 `dt_netprofit_yoy` 和 `netprofit_yoy` 均缺失的股票
- **极端值过滤**：剔除 `|growth_rate| > 1000%` 的异常值
- **无穷值处理**：剔除 `inf` 或 `-inf` 的记录

### 加权计算公式

```
weighted_growth = Σ (growth_rate_i × weight_i) / Σ weight_i
```

其中：
- `growth_rate_i`：第i只成分股的扣非净利润同比增速
- `weight_i`：第i只成分股的权重（来自指数公司官方数据）

## 数据质量标记

| 标记值 | 含义 |
|--------|------|
| `clean` | 所有股票均使用 `dt_netprofit_yoy` |
| `used_non_dt_fallback` | 部分股票使用 `netprofit_yoy` 替代 |
| `no_weight_data` | 未获取到权重数据 |
| `no_valid_data` | 无有效数据参与计算 |
| `weight_api_error` | 权重数据API调用失败 |
| `processing_error` | 处理过程中发生错误 |

## 输出文件

分析结果保存为CSV文件：`申万一级行业指数盈利增长评估.csv`

包含字段：
- `industry_code`: 行业指数代码
- `industry_name`: 行业名称
- `profit_yoy_weighted`: 加权扣非净利润同比增速 (%)
- `valid_stock_count`: 有效参与计算的成分股数量
- `total_stock_count`: 该行业当月总成分股数量
- `data_quality_flag`: 数据质量标记

## 使用示例

### 基本使用

```python
# 测试单个行业
result = get_industry_profit_growth('801760.SI', '20251110')
print(f"传媒行业加权盈利增速: {result['profit_yoy_weighted']}%")

# 批量分析
results = evaluate_all_industries_profit_growth()
print(results.head())
```

### 集成到现有分析流程

```python
# 结合估值分析
valuation_df = evaluate_sector_valuation()
growth_df = evaluate_all_industries_profit_growth()

# 合并分析结果
combined_df = valuation_df.merge(growth_df, on='industry_code', how='left')
combined_df = combined_df[['industry_code', 'name', 'valuation_status', 'profit_yoy_weighted']]

# 筛选高景气度+低估值的行业
opportunities = combined_df[
    (combined_df['profit_yoy_weighted'] > 10) & 
    (combined_df['valuation_status'] == '低估')
]
```

## 注意事项

1. **API调用限制**：批量分析会消耗较多API调用，建议控制频率
2. **数据时效性**：权重数据使用最近一个完整月份，财务数据使用最新季度报告
3. **数据质量**：关注 `data_quality_flag` 和有效股票数量，评估结果可靠性
4. **极端值处理**：自动过滤超过 ±1000% 的异常增速数据

## 依赖要求

- Python 3.6+
- pandas
- numpy
- tushare
- 有效的 Tushare API Token（需要至少2000积分）