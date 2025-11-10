#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tushare as ts
import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import os

def get_index_valuation_analysis():
    """
    获取A股主要宽基指数的估值状态分析
    
    分析目标指数（共6个）及对应 Tushare 代码：
    - 上证综指：000001.SH
    - 深证成指：399001.SZ
    - 上证50：000016.SH
    - 中证500：000905.SH
    - 中小板指：399005.SZ
    - 创业板指：399006.SZ
    """
    
    # 从环境变量获取Tushare token
    token = os.getenv("TUSHARE_TOKEN")
    if not token:
        raise ValueError("请设置环境变量 TUSHARE_TOKEN")
    ts.set_token(token)
    pro = ts.pro_api()
    
    # 定义要分析的指数
    indices = [
        {"ts_code": "000001.SH", "name": "上证综指"},
        {"ts_code": "399001.SZ", "name": "深证成指"},
        {"ts_code": "000016.SH", "name": "上证50"},
        {"ts_code": "000905.SH", "name": "中证500"},
        {"ts_code": "399005.SZ", "name": "中小板指"},
        {"ts_code": "399006.SZ", "name": "创业板指"}
    ]
    
    # 计算日期范围（最近10年）
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=365*10)).strftime("%Y%m%d")
    
    results = []
    
    for index in indices:
        print(f"正在分析 {index['name']} ({index['ts_code']})...")
        
        try:
            # 获取指数历史数据
            all_data = []
            current_start_date = start_date
            current_end_date = end_date
            
            # 分段获取数据（处理Tushare单次请求限制）
            while current_start_date <= end_date:
                # 计算当前段的结束日期（最多一年）
                temp_end_date = min(
                    datetime.strptime(current_start_date, "%Y%m%d") + timedelta(days=365),
                    datetime.strptime(end_date, "%Y%m%d")
                ).strftime("%Y%m%d")
                
                # 调用Tushare API获取数据
                df = pro.index_dailybasic(
                    ts_code=index['ts_code'],
                    start_date=current_start_date,
                    end_date=temp_end_date,
                    fields='ts_code,trade_date,pe_ttm,pb'
                )
                
                if not df.empty:
                    all_data.append(df)
                
                # 更新下一段的开始日期
                current_start_date = (datetime.strptime(temp_end_date, "%Y%m%d") + timedelta(days=1)).strftime("%Y%m%d")
                
                # 如果已经到达结束日期，退出循环
                if current_start_date > end_date:
                    break
            
            if not all_data:
                print(f"警告: {index['name']} 没有获取到数据")
                continue
                
            # 合并所有数据
            full_data = pd.concat(all_data, ignore_index=True)
            
            # 按交易日期排序
            full_data = full_data.sort_values('trade_date')
            
            # 去除空值
            full_data = full_data.dropna(subset=['pe_ttm', 'pb'])
            
            if full_data.empty:
                print(f"警告: {index['name']} 去除空值后没有数据")
                continue
            
            # 获取最新的估值数据
            latest_data = full_data.iloc[-1]
            current_pe_ttm = latest_data['pe_ttm']
            current_pb = latest_data['pb']
            
            # 计算百分位数
            pe_ttm_percentile = np.percentile(full_data['pe_ttm'], current_pe_ttm)
            pb_percentile = np.percentile(full_data['pb'], current_pb)
            
            # 使用pandas计算百分位数（更准确的方法）
            pe_ttm_percentile = (full_data['pe_ttm'] < current_pe_ttm).mean() * 100
            pb_percentile = (full_data['pb'] < current_pb).mean() * 100
            
            # 判断估值状态
            if pe_ttm_percentile < 20 and pb_percentile < 20:
                valuation_status = "低估"
            elif pe_ttm_percentile > 80 and pb_percentile > 80:
                valuation_status = "高估"
            else:
                valuation_status = "中性"
            
            # 构建结果字典
            result = {
                "ts_code": index['ts_code'],
                "name": index['name'],
                "current_pe_ttm": round(float(current_pe_ttm), 2),
                "current_pb": round(float(current_pb), 2),
                "pe_ttm_percentile_10y": round(float(pe_ttm_percentile), 1),
                "pb_percentile_10y": round(float(pb_percentile), 1),
                "valuation_status": valuation_status
            }
            
            results.append(result)
            print(f"{index['name']} 分析完成: PE_TTM百分位={pe_ttm_percentile:.1f}%, PB百分位={pb_percentile:.1f}%, 状态={valuation_status}")
            
        except Exception as e:
            print(f"分析 {index['name']} 时出错: {str(e)}")
            continue
    
    # 将结果保存到JSON文件
    output_file = "index_valuation_summary.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("✅ 估值分析完成，结果已保存至 index_valuation_summary.json")
    return results

if __name__ == "__main__":
    get_index_valuation_analysis()