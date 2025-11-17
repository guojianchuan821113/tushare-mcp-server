#!/usr/bin/env python3
"""
Demo script for get_sentiment_volume function
展示如何使用量能情绪分析函数
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def color_text(text, color):
    """简单的颜色输出函数"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'end': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['end']}"

def get_sentiment_emoji(sentiment):
    """根据情绪返回对应的emoji"""
    emoji_map = {
        'strongly_bullish': '🐂💹',
        'strongly_bearish': '🐻📉',
        'apathetic': '😴💤',
        'neutral': '⚖️📊'
    }
    return emoji_map.get(sentiment, '❓')

def analyze_sentiment_volume(ts_code, trade_date):
    """分析股票情绪并可视化输出"""
    
    try:
        from tushare_mcp_server.server import get_sentiment_volume
        
        print(f"\n{color_text('🔍 正在分析', 'cyan')} {color_text(ts_code, 'yellow')} 在 {color_text(trade_date, 'yellow')} 的量能情绪...")
        print("=" * 70)
        
        # 调用函数
        result = get_sentiment_volume(ts_code, trade_date)
        data = json.loads(result)
        
        if 'error' in data:
            print(f"{color_text('❌ 错误:', 'red')} {data['error']}")
            return False
        
        # 输出结果
        print(f"\n{color_text('📊 基础量能指标', 'blue')}")
        print("-" * 40)
        
        # 换手率状态
        turnover = data['turnover_status']
        turnover_color = 'green' if turnover == 'high_turnover' else 'red' if turnover == 'low_turnover' else 'white'
        print(f"换手率状态: {color_text(turnover, turnover_color)}")
        
        # 量比状态
        volume = data['volume_status']
        volume_color = 'green' if volume == 'volume_surge' else 'red' if volume == 'volume_dry_up' else 'white'
        print(f"量比状态: {color_text(volume, volume_color)}")
        
        # OBV趋势
        obv = data['obv_trend']
        obv_color = 'green' if obv == 'rising' else 'red' if obv == 'falling' else 'yellow'
        print(f"OBV趋势: {color_text(obv, obv_color)}")
        
        print(f"\n{color_text('😊 情绪指标', 'blue')}")
        print("-" * 40)
        
        # BRAR情绪
        brar = data['brar_sentiment']
        brar_color = 'green' if 'bullish' in brar else 'red' if 'bearish' in brar else 'yellow'
        print(f"BRAR情绪: {color_text(brar, brar_color)}")
        
        # VR状态
        vr = data['vr_status']
        vr_color = 'green' if 'bullish' in vr else 'red' if 'bearish' in vr else 'yellow'
        print(f"VR状态: {color_text(vr, vr_color)}")
        
        # MFI_PSY状态
        mfi_psy = data['mfi_psy_status']
        print(f"MFI_PSY: {color_text(mfi_psy, 'cyan')}")
        
        print(f"\n{color_text('🎯 综合判断', 'blue')}")
        print("-" * 40)
        
        # 综合情绪
        market_sentiment = data['market_sentiment']
        emoji = get_sentiment_emoji(market_sentiment)
        
        sentiment_color = 'green' if 'bullish' in market_sentiment else 'red' if 'bearish' in market_sentiment else 'yellow'
        print(f"市场情绪: {color_text(market_sentiment, sentiment_color)} {emoji}")
        
        # 投资建议
        print(f"\n{color_text('💡 投资建议', 'purple')}")
        print("-" * 40)
        
        if market_sentiment == 'strongly_bullish':
            print(f"{color_text('🟢 积极关注', 'green')} - 多重指标显示乐观情绪")
            print("建议: 可以考虑逢低布局，但需注意风险控制")
        elif market_sentiment == 'strongly_bearish':
            print(f"{color_text('🔴 谨慎观望', 'red')} - 多重指标显示悲观情绪")
            print("建议: 暂时观望，等待情绪好转信号")
        elif market_sentiment == 'apathetic':
            print(f"{color_text('⚪ 暂时回避', 'yellow')} - 市场冷漠，交投清淡")
            print("建议: 等待市场关注度提升后再考虑参与")
        else:
            print(f"{color_text('⚪ 等待信号', 'yellow')} - 指标平衡，方向不明")
            print("建议: 保持观望，等待更明确的信号")
        
        print(f"\n{color_text('✅ 分析完成!', 'green')}")
        return True
        
    except ImportError:
        print(f"{color_text('❌ 错误:', 'red')} 无法导入 get_sentiment_volume 函数")
        print("请确保 MCP 服务器正确安装")
        return False
    except Exception as e:
        print(f"{color_text('❌ 错误:', 'red')} {str(e)}")
        return False

def main():
    """主函数"""
    print(f"{color_text('🚀 Tushare 量能情绪分析演示', 'cyan')}")
    print("=" * 70)
    
    # 检查环境
    token = os.getenv('TUSHARE_TOKEN')
    if not token:
        print(f"{color_text('❌ 错误:', 'red')} 未找到 TUSHARE_TOKEN")
        print(f"请先设置环境变量: {color_text('export TUSHARE_TOKEN=your_token', 'yellow')}")
        return
    
    # 示例分析
    stocks = [
        ("000001.SZ", "20240115"),  # 平安银行
        ("000002.SZ", "20240115"),  # 万科A
    ]
    
    for ts_code, trade_date in stocks:
        success = analyze_sentiment_volume(ts_code, trade_date)
        if not success:
            break
        print("\n" + "=" * 70)
    
    print(f"\n{color_text('📚 使用说明:', 'blue')}")
    print("- 本工具基于 Tushare Pro 的 stk_factor_pro 数据")
    print("- 综合多个技术指标判断市场情绪")
    print("- 适合日线级别的情绪分析")
    print("- 不预测价格方向，只分析情绪强度")
    
    print(f"\n{color_text('🔧 自定义分析:', 'blue')}")
    print("可以修改代码中的 stocks 列表来分析其他股票")
    print("格式: (股票代码, 交易日期)")
    print("例如: ('600000.SH', '20240115')")

if __name__ == "__main__":
    main()