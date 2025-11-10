#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
申万一级行业综合分析示例

结合估值分析和盈利增长分析，筛选投资机会
"""

import os
import sys
sys.path.append('/Users/jason/Downloads/tushare-mcp-server/src/tool_kits')

from sector_index import evaluate_sector_valuation, evaluate_all_industries_profit_growth
import pandas as pd
import numpy as np

def comprehensive_analysis():
    """执行综合分析：估值 + 盈利增长"""
    
    print("=== 申万一级行业综合分析 ===")
    print("正在获取估值数据...")
    
    # 1. 获取估值数据
    valuation_df = evaluate_sector_valuation()
    if valuation_df.empty:
        print("错误：未能获取估值数据")
        return
    
    print("正在获取盈利增长数据...")
    
    # 2. 获取盈利增长数据
    growth_df = evaluate_all_industries_profit_growth()
    if growth_df.empty:
        print("错误：未能获取盈利增长数据")
        return
    
    # 3. 合并数据
    combined_df = valuation_df.merge(
        growth_df[['industry_code', 'profit_yoy_weighted', 'valid_stock_count', 'data_quality_flag']], 
        left_on='ts_code', 
        right_on='industry_code', 
        how='left'
    )
    
    # 4. 筛选和分析
    print("\n=== 综合分析结果 ===")
    
    # 筛选高景气度行业（盈利增速 > 10%）
    high_growth = combined_df[combined_df['profit_yoy_weighted'] > 10].copy()
    high_growth = high_growth.sort_values('profit_yoy_weighted', ascending=False)
    
    print(f"\n高景气度行业（盈利增速 > 10%）：{len(high_growth)} 个")
    if not high_growth.empty:
        print(high_growth[['name', 'profit_yoy_weighted', 'valuation_status', 'pe_latest', 'pb_latest']].to_string(index=False))
    
    # 筛选低估值 + 正增长行业
    value_growth = combined_df[
        (combined_df['valuation_status'] == '低估') & 
        (combined_df['profit_yoy_weighted'] > 0)
    ].copy()
    value_growth = value_growth.sort_values('profit_yoy_weighted', ascending=False)
    
    print(f"\n低估值 + 正增长行业：{len(value_growth)} 个")
    if not value_growth.empty:
        print(value_growth[['name', 'profit_yoy_weighted', 'pe_latest', 'pb_latest']].to_string(index=False))
    
    # 筛选高估 + 负增长行业（风险警示）
    risk_industries = combined_df[
        (combined_df['valuation_status'] == '高估') & 
        (combined_df['profit_yoy_weighted'] < 0)
    ].copy()
    
    print(f"\n高估 + 负增长行业（风险提示）：{len(risk_industries)} 个")
    if not risk_industries.empty:
        print(risk_industries[['name', 'profit_yoy_weighted', 'pe_latest', 'pb_latest']].to_string(index=False))
    
    # 5. 保存完整结果
    combined_df.to_csv('申万一级行业综合分析.csv', index=False, encoding='utf-8-sig')
    print(f"\n完整分析结果已保存到 '申万一级行业综合分析.csv'")
    
    # 6. 统计信息
    print(f"\n=== 统计信息 ===")
    print(f"总行业数量: {len(combined_df)}")
    print(f"有效盈利增长数据: {combined_df['profit_yoy_weighted'].notna().sum()}")
    print(f"平均盈利增速: {combined_df['profit_yoy_weighted'].mean():.2f}%")
    print(f"中位数盈利增速: {combined_df['profit_yoy_weighted'].median():.2f}%")
    
    # 估值状态分布
    valuation_counts = combined_df['valuation_status'].value_counts()
    print(f"\n估值状态分布:")
    for status, count in valuation_counts.items():
        print(f"  {status}: {count} 个")

def quick_screen():
    """快速筛选功能"""
    
    print("\n=== 快速筛选 ===")
    
    # 获取数据
    valuation_df = evaluate_sector_valuation()
    growth_df = evaluate_all_industries_profit_growth()
    
    if valuation_df.empty or growth_df.empty:
        print("错误：未能获取必要数据")
        return
    
    # 合并数据
    combined_df = valuation_df.merge(
        growth_df[['industry_code', 'profit_yoy_weighted']], 
        left_on='ts_code', 
        right_on='industry_code', 
        how='left'
    )
    
    # 定义筛选条件
    screens = {
        "高景气低估值": {
            "condition": (combined_df['profit_yoy_weighted'] > 15) & 
                         (combined_df['valuation_status'].isin(['低估', '中性'])),
            "description": "盈利增速 > 15% 且估值合理"
        },
        "稳定增长": {
            "condition": (combined_df['profit_yoy_weighted'] > 5) & 
                         (combined_df['profit_yoy_weighted'] < 30) &
                         (combined_df['valuation_status'] == '中性'),
            "description": "盈利增速 5%-30% 且估值中性"
        },
        "反转机会": {
            "condition": (combined_df['profit_yoy_weighted'] > 0) & 
                         (combined_df['valuation_status'] == '低估'),
            "description": "盈利转正且估值偏低"
        }
    }
    
    for screen_name, screen_info in screens.items():
        results = combined_df[screen_info["condition"]].copy()
        results = results.sort_values('profit_yoy_weighted', ascending=False)
        
        print(f"\n{screen_name} ({screen_info['description']}): {len(results)} 个")
        if not results.empty:
            print(results[['name', 'profit_yoy_weighted', 'valuation_status']].head(10).to_string(index=False))
        else:
            print("  无符合条件的行业")

if __name__ == "__main__":
    # 检查环境变量
    token = os.environ.get('TUSHARE_TOKEN')
    if not token:
        print("错误：请设置环境变量 TUSHARE_TOKEN")
        sys.exit(1)
    
    # 运行综合分析
    comprehensive_analysis()
    
    # 运行快速筛选
    quick_screen()
    
    print("\n=== 分析完成 ===")