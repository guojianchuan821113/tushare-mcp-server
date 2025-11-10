#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的index_member_all+市值权重方案
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sector_index import get_industry_profit_growth

def test_single_industry():
    """测试单个行业"""
    print("=== 测试单个行业 ===")
    
    # 测试传媒行业
    result = get_industry_profit_growth('801760.SI', '20251110')
    print(f"传媒行业结果: {result}")
    
    return result

def test_multiple_industries():
    """测试多个行业"""
    print("\n=== 测试多个行业 ===")
    
    industries = ['801010.SI', '801030.SI', '801080.SI']  # 农林牧渔、基础化工、电子
    
    for industry in industries:
        result = get_industry_profit_growth(industry, '20251110')
        print(f"{industry} 结果: {result}")
        print("-" * 50)
        
        # 避免API调用过于频繁
        import time
        time.sleep(1)

if __name__ == "__main__":
    test_single_industry()
    test_multiple_industries()