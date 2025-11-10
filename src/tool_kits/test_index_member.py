#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试index_member_all接口的正确使用方法
"""

import pandas as pd
import tushare as ts
import os
import time

# 从环境变量获取Tushare token
token = os.environ.get('TUSHARE_TOKEN')
if not token:
    raise ValueError("请设置环境变量 TUSHARE_TOKEN")
pro = ts.pro_api(token)

def test_index_member_all():
    """测试index_member_all接口"""
    print("=== 测试index_member_all接口 ===")
    
    # 1. 首先获取申万一级行业分类
    print("1. 获取申万一级行业分类...")
    try:
        sw_indices = pro.index_classify(level='L1', src='SW2021')
        print(f"获取到 {len(sw_indices)} 个申万一级行业")
        print(sw_indices.head())
        
        # 2. 测试不同的参数格式
        print("\n2. 测试不同的参数格式...")
        
        # 提取第一个行业代码测试
        if not sw_indices.empty:
            first_code = sw_indices.iloc[0]['index_code']
            print(f"第一个行业代码: {first_code}")
            
            # 去掉.SI后缀
            clean_code = first_code.replace('.SI', '')
            print(f"去掉.SI后缀: {clean_code}")
            
            # 测试不同的参数组合
            test_cases = [
                {'l1_code': clean_code},
                {'l1_code': first_code},
                {'l2_code': clean_code + '01'},  # 假设二级代码
                {'l3_code': clean_code + '0101'},  # 假设三级代码
            ]
            
            for i, params in enumerate(test_cases):
                try:
                    print(f"\n测试案例 {i+1}: {params}")
                    result = pro.index_member_all(**params)
                    print(f"结果: {len(result)} 条记录")
                    if not result.empty:
                        print(result.head(3))
                    time.sleep(0.5)
                except Exception as e:
                    print(f"错误: {e}")
    
    except Exception as e:
        print(f"获取申万行业分类失败: {e}")
    
    # 3. 测试sw_daily接口
    print("\n3. 测试sw_daily接口...")
    try:
        sw_daily = pro.sw_daily(ts_code='801760.SI', start_date='20241101', end_date='20241110')
        print(f"sw_daily结果: {len(sw_daily)} 条记录")
        if not sw_daily.empty:
            print(sw_daily.head())
    except Exception as e:
        print(f"sw_daily接口错误: {e}")

if __name__ == "__main__":
    test_index_member_all()