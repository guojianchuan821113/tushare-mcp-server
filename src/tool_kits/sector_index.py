#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
申万一级行业指数估值评估工具

该脚本基于PE_TTM和PB的历史分位数，评估当前所有申万一级行业指数的估值状态（高估/低估/中性）。
"""

import pandas as pd
import numpy as np
import tushare as ts
from datetime import datetime, timedelta
import time
import os

# 从环境变量获取Tushare token
token = os.environ.get('TUSHARE_TOKEN')
if not token:
    raise ValueError("请设置环境变量 TUSHARE_TOKEN")
pro = ts.pro_api(token)

# 行业主估值指标映射
# 基于行业特性选择估值指标：
# - PB适用于：重资产、周期性、金融行业（银行、非银、房地产、公用事业、交通运输、钢铁、有色、化工、建材、建筑、机械、石油、煤炭）
# - PE适用于：消费、科技、成长类行业
primary_metric_map = {
    '801010.SI': 'PE',  # 农林牧渔
    '801030.SI': 'PB',  # 基础化工
    '801040.SI': 'PB',  # 钢铁
    '801050.SI': 'PB',  # 有色金属
    '801080.SI': 'PE',  # 电子
    '801110.SI': 'PE',  # 家用电器
    '801120.SI': 'PE',  # 食品饮料
    '801130.SI': 'PE',  # 纺织服饰
    '801140.SI': 'PE',  # 轻工制造
    '801150.SI': 'PE',  # 医药生物
    '801160.SI': 'PB',  # 公用事业
    '801170.SI': 'PB',  # 交通运输
    '801180.SI': 'PB',  # 房地产
    '801200.SI': 'PE',  # 商贸零售
    '801210.SI': 'PE',  # 社会服务
    '801230.SI': 'PE',  # 综合
    '801710.SI': 'PB',  # 建筑材料 - 重资产行业，应使用PB
    '801720.SI': 'PB',  # 建筑装饰 - 重资产行业，应使用PB
    '801730.SI': 'PE',  # 电力设备
    '801740.SI': 'PE',  # 国防军工
    '801750.SI': 'PE',  # 计算机
    '801760.SI': 'PE',  # 传媒
    '801770.SI': 'PE',  # 通信 - 成长性行业，应使用PE
    '801780.SI': 'PB',  # 银行 - 金融行业，应使用PB
    '801790.SI': 'PB',  # 非银金融 - 金融行业，应使用PB
    '801880.SI': 'PE',  # 汽车
    '801890.SI': 'PB',  # 机械设备 - 重资产行业，应使用PB
    '801950.SI': 'PB',  # 煤炭 - 周期性行业，应使用PB
    '801960.SI': 'PB',  # 石油石化 - 周期性行业，应使用PB
    '801970.SI': 'PE',  # 环保
    '801980.SI': 'PE'   # 美容护理 - 消费行业，应使用PE
}

def get_sw_level1_indices():
    """获取所有申万一级行业指数代码"""
    try:
        df = pro.index_classify(level='L1', src='SW2021')
        return df
    except Exception as e:
        print(f"获取申万一级行业指数失败: {e}")
        return pd.DataFrame()

def get_index_daily_data(ts_code, start_date='20201110', end_date='20251110'):
    """获取单个指数的日线数据，处理Tushare API限制"""
    all_data = []
    
    # 将日期范围分成多个小段，避免超过API限制
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')
    
    # 每次获取约1年的数据，避免超过4000行限制
    delta = timedelta(days=365)
    
    current_start = start
    while current_start < end:
        current_end = min(current_start + delta, end)
        
        start_str = current_start.strftime('%Y%m%d')
        end_str = current_end.strftime('%Y%m%d')
        
        try:
            # 调用API获取数据
            df = pro.sw_daily(ts_code=ts_code, start_date=start_str, end_date=end_str, 
                            fields='ts_code,trade_date,pe,pb')
            
            if not df.empty:
                all_data.append(df)
            
            # 添加延迟，避免API调用频率限制
            time.sleep(0.2)
            
        except Exception as e:
            print(f"获取指数 {ts_code} 在 {start_str} 到 {end_str} 的数据失败: {e}")
        
        current_start = current_end + timedelta(days=1)
    
    if all_data:
        result = pd.concat(all_data, ignore_index=True)
        # 去重并按日期排序
        result = result.drop_duplicates(subset=['trade_date']).sort_values('trade_date')
        return result
    else:
        return pd.DataFrame()

def calculate_percentile(series, current_value):
    """计算当前值在历史序列中的百分位数"""
    if series.empty or pd.isna(current_value):
        return np.nan
    
    # 计算小于等于当前值的数据点数量
    count_le = sum(1 for x in series if x <= current_value and not pd.isna(x))
    total_count = sum(1 for x in series if not pd.isna(x))
    
    if total_count == 0:
        return np.nan
    
    # 计算百分位数并四舍五入为整数
    percentile = round(count_le / total_count * 100)
    return percentile

def evaluate_sector_valuation():
    """评估所有申万一级行业指数的估值状态"""
    # 获取所有申万一级行业指数
    indices_df = get_sw_level1_indices()
    
    if indices_df.empty:
        print("未能获取申万一级行业指数列表")
        return pd.DataFrame()
    
    results = []
    
    for index, row in indices_df.iterrows():
        ts_code = row['index_code']
        index_name = row['industry_name']  # 修改字段名
        
        print(f"正在处理: {ts_code} - {index_name}")
        
        # 获取指数历史数据
        daily_data = get_index_daily_data(ts_code)
        
        if daily_data.empty:
            print(f"未能获取 {ts_code} 的历史数据")
            continue
        
        # 剔除pe或pb为空的行
        clean_data = daily_data.dropna(subset=['pe', 'pb'])
        
        if clean_data.empty:
            print(f"{ts_code} 的数据为空或全部为NaN")
            continue
        
        # 获取最新交易日的数据
        latest_data = clean_data.iloc[-1]
        latest_pe = latest_data['pe']
        latest_pb = latest_data['pb']
        
        # 计算PE和PB的历史百分位数
        pe_percentile = calculate_percentile(clean_data['pe'], latest_pe)
        pb_percentile = calculate_percentile(clean_data['pb'], latest_pb)
        
        # 确定主估值指标
        primary_metric = primary_metric_map.get(ts_code, 'PE')
        
        # 判断估值状态
        if primary_metric == 'PE':
            main_percentile = pe_percentile
        else:
            main_percentile = pb_percentile
        
        if pd.isna(main_percentile):
            valuation_status = '未知'
        elif main_percentile >= 80:
            valuation_status = '高估'
        elif main_percentile <= 20:
            valuation_status = '低估'
        else:
            valuation_status = '中性'
        
        # 添加到结果列表
        results.append({
            'ts_code': ts_code,
            'name': index_name,
            'pe_latest': round(latest_pe, 2) if not pd.isna(latest_pe) else np.nan,
            'pe_percentile': int(pe_percentile) if not pd.isna(pe_percentile) else np.nan,
            'pb_latest': round(latest_pb, 2) if not pd.isna(latest_pb) else np.nan,
            'pb_percentile': int(pb_percentile) if not pd.isna(pb_percentile) else np.nan,
            'primary_metric': primary_metric,
            'valuation_status': valuation_status
        })
    
    # 创建结果DataFrame
    result_df = pd.DataFrame(results)
    
    # 按估值状态排序：高估在前，中性其次，低估在后
    status_order = {'高估': 0, '中性': 1, '低估': 2, '未知': 3}
    result_df['status_order'] = result_df['valuation_status'].map(status_order)
    result_df = result_df.sort_values('status_order').drop('status_order', axis=1)
    
    return result_df

if __name__ == "__main__":
    print("开始评估申万一级行业指数估值状态...")
    result_df = evaluate_sector_valuation()
    
    if not result_df.empty:
        print("\n申万一级行业指数估值评估结果:")
        print(result_df.to_string(index=False))
        
        # 保存结果到CSV文件
        result_df.to_csv('申万一级行业指数估值评估.csv', index=False, encoding='utf-8-sig')
        print("\n结果已保存到 '申万一级行业指数估值评估.csv'")
    else:
        print("未能获取到有效的估值评估结果")