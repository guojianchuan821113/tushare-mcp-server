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

def get_last_month_dates(trade_date='20251110'):
    """获取最近一个完整月份的起止日期"""
    try:
        current_date = datetime.strptime(trade_date, '%Y%m%d')
        
        # 获取上个月的最后一天
        first_day_current = current_date.replace(day=1)
        last_day_last_month = first_day_current - timedelta(days=1)
        
        # 获取上个月的第一天
        first_day_last_month = last_day_last_month.replace(day=1)
        
        return first_day_last_month.strftime('%Y%m%d'), last_day_last_month.strftime('%Y%m%d')
    except Exception as e:
        print(f"日期计算失败: {e}")
        return None, None

def get_industry_profit_growth(industry_code: str, trade_date: str = '20251110') -> dict:
    """
    计算申万一级行业指数的最新季度加权净利润同比增速
    使用index_member_all获取成分股，结合市值数据计算权重
    
    Args:
        industry_code: 行业指数代码 (如 '801760.SI')
        trade_date: 交易日期 (格式: '20251110')
    
    Returns:
        dict: 包含行业盈利增长信息的字典
    """
    try:
        # 获取行业名称
        industry_name = ''
        try:
            sw_indices = get_sw_level1_indices()
            if not sw_indices.empty:
                industry_info = sw_indices[sw_indices['index_code'] == industry_code]
                if not industry_info.empty:
                    industry_name = industry_info.iloc[0]['industry_name']
        except Exception as e:
            print(f"获取行业 {industry_code} 名称失败: {e}")
        
        print(f"正在处理行业 {industry_code} - {industry_name}")
        
        # 1. 使用index_member_all获取行业成分股
        try:
            # 获取一级行业成分股（使用完整代码，包括.SI后缀）
            member_data = pro.index_member_all(l1_code=industry_code, is_new='Y')
            
            if member_data.empty:
                print(f"警告：行业 {industry_code} 未获取到成分股数据")
                return {
                    'industry_code': industry_code,
                    'industry_name': industry_name,
                    'profit_yoy_weighted': np.nan,
                    'valid_stock_count': 0,
                    'total_stock_count': 0,
                    'data_quality_flag': 'no_member_data'
                }
                
        except Exception as e:
            print(f"获取行业 {industry_code} 成分股失败: {e}")
            return {
                'industry_code': industry_code,
                'industry_name': industry_name,
                'profit_yoy_weighted': np.nan,
                'valid_stock_count': 0,
                'total_stock_count': 0,
                'data_quality_flag': 'member_api_error'
            }
        
        # 2. 获取成分股市值数据用于计算权重
        stock_codes = member_data['ts_code'].tolist()
        total_stock_count = len(stock_codes)
        
        print(f"获取到 {total_stock_count} 只成分股")
        
        # 获取最近交易日期
        recent_date = '20241108'  # 使用一个已知的最近交易日期
        
        # 获取成分股的市值数据（使用daily_basic接口）
        stock_market_caps = []
        for i, stock_code in enumerate(stock_codes):
            try:
                # 使用daily_basic接口获取市值数据
                daily_data = pro.daily_basic(ts_code=stock_code, trade_date=recent_date, 
                                           fields='ts_code,total_mv')
                
                if not daily_data.empty:
                    # 使用总市值 (total_mv) 作为权重
                    market_cap = daily_data.iloc[0]['total_mv']
                    if pd.isna(market_cap) or market_cap <= 0:
                        # 如果没有市值数据，使用等权重
                        market_cap = 1.0
                    stock_market_caps.append(market_cap)
                else:
                    # 如果获取市值数据失败，使用等权重
                    stock_market_caps.append(1.0)
                    
            except Exception as e:
                print(f"获取股票 {stock_code} 市值数据失败，使用等权重: {e}")
                stock_market_caps.append(1.0)
            
            # 避免API调用过于频繁
            if i % 10 == 0:
                time.sleep(0.1)
        
        # 3. 计算报告期
        trade_dt = datetime.strptime(trade_date, '%Y%m%d')
        if trade_dt.month <= 3:
            period = f"{trade_dt.year-1}0930"  # 上年三季度
        elif trade_dt.month <= 6:
            period = f"{trade_dt.year-1}1231"  # 上年四季度
        elif trade_dt.month <= 9:
            period = f"{trade_dt.year}0331"   # 当年一季度
        else:
            period = f"{trade_dt.year}0630"   # 当年二季度（修正：10-12月使用Q2中报，而不是Q3）
        
        print(f"使用报告期: {period}")
        
        # 4. 遍历每个成分股，获取财务数据
        valid_weights = []
        valid_growth_rates = []
        fallback_used = False
        invalid_financial_count = 0
        invalid_growth_count = 0
        
        for i, (stock_code, market_cap) in enumerate(zip(stock_codes, stock_market_caps)):
            try:
                # 获取财务数据
                fina_data = pro.fina_indicator(ts_code=stock_code, period=period)
                
                if fina_data.empty:
                    print(f"警告：成分股 {stock_code} 未获取到财务数据 (报告期: {period})")
                    invalid_financial_count += 1
                    continue
                
                latest_fina = fina_data.iloc[0]  # 取最新记录
                
                # 优先使用 dt_netprofit_yoy (扣除非经常性损益后的净利润同比增长率)
                growth_rate = None
                if 'dt_netprofit_yoy' in latest_fina and not pd.isna(latest_fina['dt_netprofit_yoy']):
                    growth_rate = latest_fina['dt_netprofit_yoy']
                elif 'netprofit_yoy' in latest_fina and not pd.isna(latest_fina['netprofit_yoy']):
                    growth_rate = latest_fina['netprofit_yoy']
                    fallback_used = True
                    print(f"警告：成分股 {stock_code} 使用 netprofit_yoy 替代 dt_netprofit_yoy")
                else:
                    print(f"警告：成分股 {stock_code} 无可用的净利润增速数据")
                    invalid_growth_count += 1
                    continue
                
                # 数据质量检查
                if pd.isna(growth_rate) or np.isinf(growth_rate) or abs(growth_rate) > 1000:
                    print(f"警告：成分股 {stock_code} 净利润增速数据异常 (growth_rate: {growth_rate})")
                    invalid_growth_count += 1
                    continue
                
                # 数据有效，加入计算列表
                valid_weights.append(market_cap)
                valid_growth_rates.append(growth_rate)
                
            except Exception as e:
                print(f"获取成分股 {stock_code} 财务数据失败: {e}")
                invalid_financial_count += 1
                continue
        
        # 5. 计算加权增长率
        if not valid_weights or not valid_growth_rates:
            print(f"行业 {industry_code} 无有效数据参与计算")
            return {
                'industry_code': industry_code,
                'industry_name': industry_name,
                'profit_yoy_weighted': np.nan,
                'valid_stock_count': 0,
                'total_stock_count': total_stock_count,
                'data_quality_flag': 'no_valid_data'
            }
        
        # 计算加权增长率
        total_weight = sum(valid_weights)
        weighted_growth = sum(g * w for g, w in zip(valid_growth_rates, valid_weights)) / total_weight
        
        # 数据质量标记
        data_quality_flag = 'used_market_cap_weight' if sum(1 for w in valid_weights if w > 1.0) > len(valid_weights) * 0.5 else 'used_equal_weight'
        if fallback_used:
            data_quality_flag += '_with_netprofit_fallback'
        
        print(f"行业 {industry_code} 处理完成：共 {total_stock_count} 只成分股，"
              f"{len(valid_weights)} 只有效，{invalid_financial_count} 只因无财务数据被跳过，"
              f"{invalid_growth_count} 只因财务数据无效被跳过")
        
        return {
            'industry_code': industry_code,
            'industry_name': industry_name,
            'profit_yoy_weighted': round(weighted_growth, 2),
            'valid_stock_count': len(valid_weights),
            'total_stock_count': total_stock_count,
            'data_quality_flag': data_quality_flag
        }
        
    except Exception as e:
        print(f"处理行业 {industry_code} 时发生错误: {e}")
        return {
            'industry_code': industry_code,
            'industry_name': '',
            'profit_yoy_weighted': np.nan,
            'valid_stock_count': 0,
            'total_stock_count': 0,
            'data_quality_flag': 'processing_error'
        }

def evaluate_all_industries_profit_growth():
    """评估所有申万一级行业的盈利增长情况"""
    # 获取所有申万一级行业指数
    indices_df = get_sw_level1_indices()
    
    if indices_df.empty:
        print("未能获取申万一级行业指数列表")
        return pd.DataFrame()
    
    results = []
    
    for index, row in indices_df.iterrows():
        ts_code = row['index_code']
        
        # 调用单个行业处理函数
        result = get_industry_profit_growth(ts_code)
        results.append(result)
        
        # 添加延迟，避免API调用频率限制
        time.sleep(0.3)
    
    # 创建结果DataFrame
    result_df = pd.DataFrame(results)
    
    # 按盈利增速排序（降序）
    result_df = result_df.sort_values('profit_yoy_weighted', ascending=False, na_position='last')
    
    return result_df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'profit_growth':
        # 运行盈利增长分析
        print("开始评估申万一级行业指数盈利增长情况...")
        profit_growth_df = evaluate_all_industries_profit_growth()
        
        if not profit_growth_df.empty:
            print("\n申万一级行业指数盈利增长评估结果:")
            print(profit_growth_df.to_string(index=False))
            
            # 保存结果到CSV文件
            profit_growth_df.to_csv('申万一级行业指数盈利增长评估.csv', index=False, encoding='utf-8-sig')
            print("\n结果已保存到 '申万一级行业指数盈利增长评估.csv'")
        else:
            print("未能获取到有效的盈利增长评估结果")
    
    else:
        # 运行估值分析（默认）
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