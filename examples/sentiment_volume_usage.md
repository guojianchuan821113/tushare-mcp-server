# get_sentiment_volume 使用指南

## 📋 功能概述

`get_sentiment_volume` 函数用于分析股票的量能情绪，帮助回答以下关键问题：

- 🎯 **市场对这只股票的关注度高吗？**
- 💰 **是资金流入还是流出？**
- 😊 **当前情绪是乐观、悲观还是冷漠？**

## 🔧 接口定义

```python
def get_sentiment_volume(ts_code: str, trade_date: str) -> str:
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 | 示例 |
|------|------|------|------|------|
| `ts_code` | str | ✅ | 股票代码 | `"000001.SZ"` |
| `trade_date` | str | ✅ | 交易日期 | `"20240115"` |

### 返回字段

| 字段名 | 类型 | 说明 | 可能值 |
|--------|------|------|--------|
| `turnover_status` | str | 换手率状态 | `"high_turnover"` / `"normal_turnover"` / `"low_turnover"` |
| `volume_status` | str | 量比状态 | `"volume_surge"` / `"normal_volume"` / `"volume_dry_up"` |
| `obv_trend` | str | OBV趋势 | `"rising"` / `"falling"` / `"flat"` / `"data_unavailable"` |
| `brar_sentiment` | str | BRAR情绪 | `"bullish_sentiment"` / `"bearish_sentiment"` / `"neutral_sentiment"` / `"overly_bullish"` / `"overly_bearish"` |
| `vr_status` | str | VR容量比率 | `"bullish_volume"` / `"bearish_volume"` / `"neutral_volume"` |
| `mfi_psy_status` | str | MFI和PSY状态组合 | `"mfi_neutral_psy_neutral"` / `"mfi_na_psy_neutral"` / `"mfi_psy_unavailable"` 等 |
| `market_sentiment` | str | 综合市场情绪 | `"strongly_bullish"` / `"strongly_bearish"` / `"apathetic"` / `"neutral"` |

## 💡 使用示例

### 基本调用

```python
from tushare_mcp_server.server import get_sentiment_volume
import json

# 分析平安银行在2024年1月15日的情绪
result = get_sentiment_volume("000001.SZ", "20240115")
data = json.loads(result)

print(f"换手率状态: {data['turnover_status']}")
print(f"市场情绪: {data['market_sentiment']}")
```

### 完整分析示例

```python
def analyze_stock_sentiment(ts_code, trade_date):
    """完整的股票情绪分析"""
    result = get_sentiment_volume(ts_code, trade_date)
    data = json.loads(result)
    
    if 'error' in data:
        print(f"❌ 错误: {data['error']}")
        return
    
    print(f"\n📊 {ts_code} 在 {trade_date} 的情绪分析")
    print("=" * 50)
    
    # 基础指标
    print(f"换手率: {data['turnover_status']}")
    print(f"量比: {data['volume_status']}")
    print(f"OBV趋势: {data['obv_trend']}")
    
    # 情绪指标
    print(f"BRAR情绪: {data['brar_sentiment']}")
    print(f"VR状态: {data['vr_status']}")
    print(f"MFI_PSY: {data['mfi_psy_status']}")
    
    # 综合判断
    sentiment = data['market_sentiment']
    print(f"\n🎯 综合情绪: {sentiment}")
    
    # 解读建议
    if sentiment == 'strongly_bullish':
        print("💹 强烈看涨: 多重指标显示乐观情绪")
    elif sentiment == 'strongly_bearish':
        print("📉 强烈看跌: 多重指标显示悲观情绪")
    elif sentiment == 'apathetic':
        print("😴 市场冷漠: 关注度低，交投清淡")
    else:
        print("⚖️ 中性情绪: 指标显示平衡状态")

# 使用示例
analyze_stock_sentiment("000001.SZ", "20240115")
```

## 📈 指标解读

### 换手率状态 (`turnover_status`)

| 状态 | 阈值 | 含义 |
|------|------|------|
| `high_turnover` | ≥5% | 高活跃度，市场关注度高 |
| `normal_turnover` | 1%-5% | 正常交易活跃度 |
| `low_turnover` | <1% | 低活跃度，流动性风险 |

### 量比状态 (`volume_status`)

| 状态 | 阈值 | 含义 |
|------|------|------|
| `volume_surge` | ≥2.0 | 成交量激增，可能有重大消息 |
| `normal_volume` | 0.8-2.0 | 正常成交量水平 |
| `volume_dry_up` | <0.8 | 成交量萎缩，市场观望 |

### OBV趋势 (`obv_trend`)

| 状态 | 含义 |
|------|------|
| `rising` | 资金流入，买盘强劲 |
| `falling` | 资金流出，卖盘主导 |
| `flat` | 资金平衡，方向不明 |
| `insufficient_data` | 数据不足，无法判断 |

### 综合情绪 (`market_sentiment`)

| 状态 | 判断条件 | 投资建议 |
|------|----------|----------|
| `strongly_bullish` | 多指标强烈看涨 | 🟢 积极关注 |
| `strongly_bearish` | 多指标强烈看跌 | 🔴 谨慎观望 |
| `apathetic` | 市场冷漠，交投清淡 | ⚪ 暂时回避 |
| `neutral` | 指标平衡，方向不明 | ⚪ 等待信号 |

## ⚠️ 注意事项

1. **数据依赖性**: 需要有效的Tushare token和相应的数据权限
2. **历史数据**: OBV趋势需要前一交易日数据
3. **实时性**: 基于盘后数据，适合日线级别分析
4. **不预测方向**: 本接口不判断价格涨跌，只分析情绪强度
5. **多指标验证**: 建议结合其他技术指标综合判断

## 🔍 错误处理

```python
result = get_sentiment_volume("000001.SZ", "20240115")
data = json.loads(result)

if 'error' in data:
    # 处理错误情况
    error_msg = data['error']
    if 'token' in error_msg:
        print("请检查Tushare token设置")
    elif '数据' in error_msg:
        print("数据获取失败，请检查日期格式和股票代码")
    else:
        print(f"未知错误: {error_msg}")
else:
    # 正常处理数据
    print("情绪分析完成")
```

## 📚 相关文档

- [Tushare Pro API文档](https://tushare.pro/document/2)
- [技术指标详解](https://tushare.pro/document/2?doc_id=159)
- [MCP服务器使用指南](./../README.md)