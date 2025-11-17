import os
import json
from typing import Optional, cast, List, Dict, Any

import pandas as pd
import numpy as np
import tushare as ts
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load Tushare token: prefer env var, fallback to .env
token = os.getenv("TUSHARE_TOKEN")
if not token:
    load_dotenv()
    token = os.getenv("TUSHARE_TOKEN")
if not token:
    raise RuntimeError("Missing TUSHARE_TOKEN. Set env or .env before running.")

ts.set_token(token)
pro = ts.pro_api()

# 使用相同的 MCP 实例或者创建新的实例
# 如果要使用相同的实例，需要在 server.py 中导入这些工具
mcp = FastMCP("Tushare Tech Extension")


@mcp.tool()
def get_trend_signals(
    ts_code: str,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取股票趋势信号综合分析。
    
    基于 stk_factor_pro 数据，提供多维度的趋势信号分析：
    - 价格与均线关系 (price_vs_ma5)
    - 均线排列状态 (ma5_vs_ma20) 
    - MACD信号 (macd_status)
    - 综合趋势方向 (trend_direction)
    - 趋势强度 (trend_strength)
    - 动量变化 (momentum_change)
    
    参数说明：
    - ts_code: 股票代码（必需），如 000001.SZ
    - trade_date: 交易日期，格式 YYYYMMDD
    - start_date/end_date: 开始/结束日期，格式 YYYYMMDD
    
    返回格式：
    - 单日查询（使用trade_date）：返回单个JSON对象
    - 多日查询（使用start_date/end_date）：返回JSON对象数组
    
    返回示例：
    {
      "ts_code": "000001.SZ",
      "trade_date": "20240115",
      "price_vs_ma5": "above",
      "ma5_vs_ma20": "bullish_alignment",
      "macd_status": "positive_momentum",
      "trend_direction": "up",
      "trend_strength": "strong",
      "momentum_change": "accelerating"
    }
    """
    try:
        # 获取股票因子数据
        df = pro.stk_factor_pro(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        
        if df.empty:
            return json.dumps({"error": "未获取到数据"})
        
        # 按日期排序，确保时间序列正确
        df = df.sort_values('trade_date').reset_index(drop=True)
        
        results = []
        
        for i in range(len(df)):
            current_data = df.iloc[i]
            result = {
                "ts_code": current_data['ts_code'],
                "trade_date": current_data['trade_date']
            }
            
            # 字段1: price_vs_ma5 - 价格与5日均线关系
            if pd.notna(current_data.get('close_qfq')) and pd.notna(current_data.get('ma_qfq_5')):
                close = current_data['close_qfq']
                ma5 = current_data['ma_qfq_5']
                
                # 检查是否有前一日数据进行穿越判断
                if i > 0:
                    prev_close = df.iloc[i-1]['close_qfq']
                    prev_ma5 = df.iloc[i-1]['ma_qfq_5']
                    
                    # 向上穿越：前一日close ≤ ma5，当日close > ma5
                    if prev_close <= prev_ma5 and close > ma5:
                        result["price_vs_ma5"] = "crossing_up"
                    # 向下穿越：前一日close ≥ ma5，当日close < ma5  
                    elif prev_close >= prev_ma5 and close < ma5:
                        result["price_vs_ma5"] = "crossing_down"
                    else:
                        # 静态位置
                        result["price_vs_ma5"] = "above" if close > ma5 else "below"
                else:
                    # 第一天数据，只能判断静态位置
                    result["price_vs_ma5"] = "above" if close > ma5 else "below"
            else:
                result["price_vs_ma5"] = None
            
            # 字段2: ma5_vs_ma20 - 均线排列状态
            if pd.notna(current_data.get('ma_qfq_5')) and pd.notna(current_data.get('ma_qfq_20')):
                ma5 = current_data['ma_qfq_5']
                ma20 = current_data['ma_qfq_20']
                result["ma5_vs_ma20"] = "bullish_alignment" if ma5 > ma20 else "bearish_alignment"
            else:
                result["ma5_vs_ma20"] = None
            
            # 字段3: macd_status - MACD信号
            if (pd.notna(current_data.get('macd_dif_qfq')) and 
                pd.notna(current_data.get('macd_dea_qfq'))):
                
                dif = current_data['macd_dif_qfq']
                dea = current_data['macd_dea_qfq']
                
                # 检查是否有前一日数据进行交叉判断
                if i > 0:
                    prev_dif = df.iloc[i-1]['macd_dif_qfq']
                    prev_dea = df.iloc[i-1]['macd_dea_qfq']
                    
                    # 金叉：前一日dif ≤ dea，当日dif > dea
                    if prev_dif <= prev_dea and dif > dea:
                        result["macd_status"] = "golden_cross"
                    # 死叉：前一日dif ≥ dea，当日dif < dea
                    elif prev_dif >= prev_dea and dif < dea:
                        result["macd_status"] = "death_cross"
                    else:
                        # 非交叉日
                        if dif > dea and dif > 0:
                            result["macd_status"] = "positive_momentum"
                        elif dif < dea and dif < 0:
                            result["macd_status"] = "negative_momentum"
                        else:
                            result["macd_status"] = "recovering"
                else:
                    # 第一天数据，只能判断静态状态
                    if dif > dea and dif > 0:
                        result["macd_status"] = "positive_momentum"
                    elif dif < dea and dif < 0:
                        result["macd_status"] = "negative_momentum"
                    else:
                        result["macd_status"] = "recovering"
            else:
                result["macd_status"] = None
            
            # 字段4: trend_direction - 综合趋势方向
            # 重新获取原始值（避免依赖 result 字段）
            close = current_data.get('close_qfq')
            ma5 = current_data.get('ma_qfq_5')
            ma20 = current_data.get('ma_qfq_20')
            dif = current_data.get('macd_dif_qfq')
            dea = current_data.get('macd_dea_qfq')
            
            valid_for_trend = all(pd.notna(x) for x in [close, ma5, ma20, dif, dea])
            
            if valid_for_trend:
                # 上涨：ma5 > ma20, price > ma5, 且 dif >= dea（允许金叉或正动量）
                if ma5 > ma20 and close > ma5 and dif >= dea:
                    result["trend_direction"] = "up"
                # 下跌：ma5 < ma20, price < ma5, 且 dif <= dea
                elif ma5 < ma20 and close < ma5 and dif <= dea:
                    result["trend_direction"] = "down"
                else:
                    result["trend_direction"] = "sideways"
            else:
                result["trend_direction"] = None
            
            # 字段5: trend_strength - 趋势强度
            # 使用相对MACD值（MACD/收盘价）避免股价绝对值影响
            if (pd.notna(current_data.get('macd_qfq')) and 
                pd.notna(current_data.get('close_qfq')) and 
                current_data.get('close_qfq', 0) != 0):
                
                macd_hist = current_data['macd_qfq']
                close = current_data['close_qfq']
                relative_macd = abs(macd_hist) / close  # 相对强度
                
                # 计算20日窗口内的强度（如果数据足够）
                start_idx = max(0, i-19)
                window_data = df.iloc[start_idx:i+1]
                
                if len(window_data) >= 10:  # 至少需要10天数据
                    # 计算相对MACD的历史分位数
                    valid_window = window_data[
                        (window_data['macd_qfq'].notna()) & 
                        (window_data['close_qfq'].notna()) & 
                        (window_data['close_qfq'] != 0)
                    ]
                    
                    if len(valid_window) > 0:
                        window_relative_macd = (valid_window['macd_qfq'].abs() / 
                                              valid_window['close_qfq'])
                        current_relative = relative_macd
                        
                        if len(window_relative_macd) > 0:
                            percentile = (window_relative_macd < current_relative).mean() * 100
                            
                            if percentile >= 75:
                                result["trend_strength"] = "strong"
                            elif percentile <= 25:
                                result["trend_strength"] = "weak"
                            else:
                                result["trend_strength"] = "moderate"
                        else:
                            result["trend_strength"] = "moderate"
                    else:
                        result["trend_strength"] = "moderate"
                else:
                    # 数据不足，使用相对阈值判断
                    # 基于经验：相对MACD > 1% 视为强趋势，< 0.1% 视为弱趋势
                    if relative_macd > 0.01:  # 1%
                        result["trend_strength"] = "strong"
                    elif relative_macd < 0.001:  # 0.1%
                        result["trend_strength"] = "weak"
                    else:
                        result["trend_strength"] = "moderate"
            else:
                result["trend_strength"] = None
            
            # 字段6: momentum_change - 动量变化
            if pd.notna(current_data.get('mtm_qfq')):
                current_mtm = current_data['mtm_qfq']
                
                if i > 0:
                    prev_mtm = df.iloc[i-1]['mtm_qfq']
                    
                    # 先判断动量方向是否反转（优先级最高）
                    if (prev_mtm <= 0 and current_mtm > 0) or (prev_mtm >= 0 and current_mtm < 0):
                        result["momentum_change"] = "reversing"
                    elif current_mtm > 0:  # 上涨动量
                        result["momentum_change"] = "accelerating" if current_mtm > prev_mtm else "decelerating"
                    else:  # 下跌动量
                        result["momentum_change"] = "accelerating_down" if current_mtm < prev_mtm else "decelerating_down"
                else:
                    # 第一天数据，只能判断当前状态
                    result["momentum_change"] = "accelerating" if current_mtm > 0 else "accelerating_down"
            else:
                result["momentum_change"] = None
            
            results.append(result)
        
        # 根据输入参数决定返回格式：单日查询返回单个对象，多日查询返回列表
        is_single_day = (trade_date is not None) and (start_date is None) and (end_date is None)
        
        if is_single_day and len(results) == 1:
            return json.dumps(results[0], ensure_ascii=False, indent=2)
        else:
            return json.dumps(results, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_sentiment_volume(
    ts_code: str,
    trade_date: str,
) -> str:
    """获取股票市场情绪与量能综合分析。
    
    基于 stk_factor_pro 数据，评估股票当前的市场参与度、资金流向与情绪倾向：
    - 换手率状态 (turnover_status)：反映股票流动性和市场关注度
    - 量比状态 (volume_status)：衡量当前成交量相对于近期均量的放大程度
    - OBV趋势 (obv_trend)：通过累积成交量判断资金流向
    - BRAR情绪 (brar_sentiment)：反映多空双方力量对比
    - VR容量比率 (vr_status)：通过涨跌日成交量对比衡量买卖力量
    - MFI和PSY状态 (mfi_psy_status)：综合资金流量指标和心理线指标
    - 综合市场情绪 (market_sentiment)：融合多个指标给出总体情绪倾向
    
    参数说明：
    - ts_code: 股票代码（必需），如 000001.SZ
    - trade_date: 交易日期（必需），格式 YYYYMMDD
    
    返回示例：
    {
      "ts_code": "000001.SZ",
      "trade_date": "20240115",
      "turnover_status": "high_turnover",
      "volume_status": "volume_surge",
      "obv_trend": "rising",
      "brar_sentiment": "bullish_sentiment",
      "vr_status": "bullish_volume",
      "mfi_psy_status": "mfi_neutral_psy_neutral",
      "market_sentiment": "strongly_bullish"
    }
    """
    try:
        # 获取包含当前日及历史数据（用于OBV趋势判断）
        df_hist = pro.stk_factor_pro(
            ts_code=ts_code,
            start_date=str(int(trade_date) - 10000),  # 往前推100天
            end_date=trade_date,
        )
        
        if df_hist.empty:
            return json.dumps({"error": f"未获取到 {trade_date} 附近的数据"})
        
        # 按日期排序并重置索引
        df_hist = df_hist.sort_values('trade_date').reset_index(drop=True)
        
        # 找到当前交易日的位置
        current_idx = df_hist[df_hist['trade_date'] == trade_date].index
        if len(current_idx) == 0:
            return json.dumps({"error": f"未获取到 {trade_date} 的数据"})
        
        current_idx = current_idx[0]
        current_row = df_hist.iloc[current_idx]
        
        result = {
            "ts_code": current_row['ts_code'],
            "trade_date": current_row['trade_date']
        }
        
        # ==================== 字段1: 换手率状态分析 ====================
        turnover_rate_f = current_row.get('turnover_rate_f')  # 自由流通换手率
        turnover_rate = current_row.get('turnover_rate')      # 总换手率
        
        # 优先使用自由流通换手率，更真实反映可交易股份的活跃度
        if pd.notna(turnover_rate_f):
            if turnover_rate_f >= 5.0:
                result["turnover_status"] = "high_turnover"
            elif turnover_rate_f >= 1.0:
                result["turnover_status"] = "normal_turnover"
            else:
                result["turnover_status"] = "low_turnover"
        elif pd.notna(turnover_rate):
            # 自由流通换手率缺失，回退到总换手率
            if turnover_rate >= 5.0:
                result["turnover_status"] = "high_turnover"
            elif turnover_rate >= 1.0:
                result["turnover_status"] = "normal_turnover"
            else:
                result["turnover_status"] = "low_turnover"
        else:
            result["turnover_status"] = None
        
        # ==================== 字段2: 量比状态分析 ====================
        volume_ratio = current_row.get('volume_ratio')
        
        if pd.notna(volume_ratio):
            if volume_ratio >= 2.0:
                result["volume_status"] = "volume_surge"
            elif volume_ratio >= 0.8:
                result["volume_status"] = "normal_volume"
            else:
                # volume_ratio < 0.8 统一视为量能不足
                result["volume_status"] = "volume_dry_up"
        else:
            result["volume_status"] = None
        
        # ==================== 字段3: OBV趋势分析 ====================
        obv_current = current_row.get('obv_qfq')
        
        if pd.notna(obv_current):
            if current_idx > 0:
                prev_row = df_hist.iloc[current_idx - 1]
                obv_previous = prev_row.get('obv_qfq')
                
                if pd.notna(obv_previous):
                    if obv_current > obv_previous:
                        result["obv_trend"] = "rising"
                    elif obv_current < obv_previous:
                        result["obv_trend"] = "falling"
                    else:
                        result["obv_trend"] = "flat"
                else:
                    result["obv_trend"] = "data_unavailable"
            else:
                result["obv_trend"] = "data_unavailable"
        else:
            result["obv_trend"] = "data_unavailable"
        
        # ==================== 字段4: BRAR情绪分析 ====================
        ar_value = current_row.get('brar_ar_qfq')
        br_value = current_row.get('brar_br_qfq')
        
        if pd.notna(ar_value) and pd.notna(br_value):
            # 极端情绪判断
            if ar_value > 150 and br_value < 100:
                result["brar_sentiment"] = "overly_bullish"
            elif br_value > 150 and ar_value < 100:
                result["brar_sentiment"] = "overly_bearish"
            else:
                # 常规情绪判断
                if abs(ar_value - br_value) < 5:
                    result["brar_sentiment"] = "neutral_sentiment"
                elif ar_value > br_value:
                    result["brar_sentiment"] = "bullish_sentiment"
                else:
                    result["brar_sentiment"] = "bearish_sentiment"
        else:
            result["brar_sentiment"] = None
        
        # ==================== 字段5: VR容量比率分析 ====================
        vr_value = current_row.get('vr_qfq')
        
        if pd.notna(vr_value):
            if vr_value > 150:
                result["vr_status"] = "bullish_volume"
            elif vr_value < 70:
                result["vr_status"] = "bearish_volume"
            else:
                result["vr_status"] = "neutral_volume"
        else:
            result["vr_status"] = None
        
        # ==================== 字段6: MFI和PSY状态分析 ====================
        mfi_value = current_row.get('mfi_qfq')
        psy_value = current_row.get('psy_qfq')
        
        mfi_status = ""
        psy_status = ""
        
        # MFI状态判断
        if pd.notna(mfi_value):
            if mfi_value >= 80:
                mfi_status = "mfi_overbought"
            elif mfi_value <= 20:
                mfi_status = "mfi_oversold"
            else:
                mfi_status = "mfi_neutral"
        else:
            mfi_status = "mfi_na"
        
        # PSY状态判断
        if pd.notna(psy_value):
            if psy_value >= 75:
                psy_status = "psy_overbullish"
            elif psy_value <= 25:
                psy_status = "psy_oversold"
            else:
                psy_status = "psy_neutral"
        else:
            psy_status = "psy_na"
        
        # 处理缺失数据的情况，使输出更清晰
        if mfi_status == "mfi_na" and psy_status == "psy_na":
            result["mfi_psy_status"] = "mfi_psy_unavailable"
        elif mfi_status == "mfi_na":
            result["mfi_psy_status"] = f"mfi_na_{psy_status}"
        elif psy_status == "psy_na":
            result["mfi_psy_status"] = f"{mfi_status}_psy_na"
        else:
            result["mfi_psy_status"] = f"{mfi_status}_{psy_status}"
        
        # ==================== 字段7: 综合市场情绪判断 ====================
        # 获取各字段状态
        turnover_status = result.get("turnover_status")
        volume_status = result.get("volume_status")
        obv_trend = result.get("obv_trend")
        brar_sentiment = result.get("brar_sentiment")
        vr_status = result.get("vr_status")
        
        # 强烈看涨情绪判断
        is_strongly_bullish = (
            (turnover_status == "high_turnover" or volume_status == "volume_surge") and
            obv_trend == "rising" and
            brar_sentiment in ["bullish_sentiment", "overly_bullish"] and
            vr_status == "bullish_volume"
        )
        
        # 强烈看跌情绪判断
        is_strongly_bearish = (
            (turnover_status == "high_turnover" or volume_status == "volume_surge") and
            obv_trend == "falling" and
            brar_sentiment in ["bearish_sentiment", "overly_bearish"] and
            vr_status == "bearish_volume"
        )
        
        # 冷漠情绪判断（交投清淡）
        is_apathetic = (
            turnover_status == "low_turnover" and
            volume_status == "volume_dry_up" and
            (obv_trend == "flat" or obv_trend == "data_unavailable")
        )
        
        # 综合情绪判断
        if is_strongly_bullish:
            result["market_sentiment"] = "strongly_bullish"
        elif is_strongly_bearish:
            result["market_sentiment"] = "strongly_bearish"
        elif is_apathetic:
            result["market_sentiment"] = "apathetic"
        else:
            result["market_sentiment"] = "neutral"
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})





@mcp.tool()
def get_valuation_metrics(
    ts_code: str,
    trade_date: str,
) -> str:
    """获取股票估值指标综合分析。
    
    基于 stk_factor_pro 数据，评估股票当前的估值水平与投资性价比：
    - PE状态 (pe_status)：基于历史分位数判断市盈率高低
    - PB状态 (pb_status)：基于历史分位数判断市净率水平
    - 股息吸引力 (dividend_attractiveness)：股息率绝对水平评估
    - PS状态 (ps_status)：基于历史分位数判断市销率水平
    - 市值分类 (market_cap_category)：按总市值规模分类
    - 综合估值结论 (valuation_summary)：融合多个指标给出投资建议
    
    参数说明：
    - ts_code: 股票代码（必需），如 000001.SZ
    - trade_date: 交易日期（必需），格式 YYYYMMDD
    
    返回示例：
    {
      "ts_code": "000001.SZ",
      "trade_date": "20240115",
      "pe_status": "cheap",
      "pb_status": "reasonable",
      "dividend_attractiveness": "attractive",
      "ps_status": "fair_revenue",
      "market_cap_category": "large_cap",
      "valuation_summary": "undervalued"
    }
    """
    try:
        # 获取近5年历史数据用于分位数计算（约1250个交易日）
        df_hist = pro.stk_factor_pro(
            ts_code=ts_code,
            start_date=str(int(trade_date) - 50000),  # 往前推约5年
            end_date=trade_date,
        )
        
        if df_hist.empty:
            return json.dumps({"error": f"未获取到 {trade_date} 附近的数据"})
        
        # 按日期排序并重置索引
        df_hist = df_hist.sort_values('trade_date').reset_index(drop=True)
        
        # 找到当前交易日的位置
        current_idx = df_hist[df_hist['trade_date'] == trade_date].index
        if len(current_idx) == 0:
            return json.dumps({"error": f"未获取到 {trade_date} 的数据"})
        
        current_idx = current_idx[0]
        current_row = df_hist.iloc[current_idx]
        
        result = {
            "ts_code": current_row['ts_code'],
            "trade_date": current_row['trade_date']
        }
        
        # ==================== 字段1: PE状态分析 ====================
        pe_ttm_current = current_row.get('pe_ttm')
        pe_current = current_row.get('pe')
        
        # 优先使用pe_ttm，缺失时回退到pe
        pe_to_use = pe_ttm_current if pd.notna(pe_ttm_current) else pe_current
        
        if pd.notna(pe_to_use):
            # 检查是否为亏损股
            if pe_to_use <= 0:
                result["pe_status"] = "unprofitable"
            else:
                # 获取历史PE序列（排除当前日，只使用前一日及之前的数据）
                if current_idx > 0:
                    hist_data = df_hist.iloc[:current_idx]  # 0 到 current_idx-1
                    hist_pe = hist_data[
                        (hist_data['pe_ttm'].notna()) & (hist_data['pe_ttm'] > 0)
                    ]['pe_ttm']
                    
                    # 如果pe_ttm历史数据不足，尝试使用pe
                    if len(hist_pe) < 100:
                        hist_pe = hist_data[
                            (hist_data['pe'].notna()) & (hist_data['pe'] > 0)
                        ]['pe']
                else:
                    hist_pe = pd.Series([], dtype=float)  # 当前日为第一天，无历史数据
                
                if len(hist_pe) >= 100:  # 有足够历史数据
                    # 计算历史分位数
                    percentile_30 = np.percentile(hist_pe, 30)
                    percentile_70 = np.percentile(hist_pe, 70)
                    
                    if pe_to_use > percentile_70:
                        result["pe_status"] = "expensive"
                    elif pe_to_use < percentile_30:
                        result["pe_status"] = "cheap"
                    else:
                        result["pe_status"] = "fair"
                else:
                    # 历史数据不足，使用绝对阈值
                    if pe_to_use > 50:
                        result["pe_status"] = "expensive"
                    elif pe_to_use < 15:
                        result["pe_status"] = "cheap"
                    else:
                        result["pe_status"] = "fair"
        else:
            result["pe_status"] = None  # 数据缺失，不判断
        
        # ==================== 字段2: PB状态分析 ====================
        pb_current = current_row.get('pb')
        
        if pd.notna(pb_current):
            # 获取历史PB序列（排除当前日，只使用前一日及之前的数据，并过滤负值）
            if current_idx > 0:
                hist_data = df_hist.iloc[:current_idx]  # 0 到 current_idx-1
                hist_pb = hist_data[
                    (hist_data['pb'].notna()) & (hist_data['pb'] >= 0)
                ]['pb']
            else:
                hist_pb = pd.Series([], dtype=float)  # 当前日为第一天，无历史数据
            
            if len(hist_pb) >= 100:  # 有足够历史数据
                # 计算历史分位数
                percentile_30 = np.percentile(hist_pb, 30)
                percentile_70 = np.percentile(hist_pb, 70)
                
                # 极端值处理
                if pb_current < 0.5:
                    result["pb_status"] = "deep_discount"
                elif pb_current > 10:
                    result["pb_status"] = "extreme_premium"
                elif pb_current > percentile_70:
                    result["pb_status"] = "high_premium"
                elif pb_current < percentile_30:
                    result["pb_status"] = "discount"
                else:
                    result["pb_status"] = "reasonable"
            else:
                # 历史数据不足，使用绝对阈值
                if pb_current < 0.5:
                    result["pb_status"] = "deep_discount"
                elif pb_current > 5:
                    result["pb_status"] = "high_premium"
                elif pb_current < 1:
                    result["pb_status"] = "discount"
                else:
                    result["pb_status"] = "reasonable"
        else:
            result["pb_status"] = None
        
        # ==================== 字段3: 股息吸引力分析 ====================
        dv_ttm_current = current_row.get('dv_ttm')
        dv_ratio_current = current_row.get('dv_ratio')
        
        # 优先使用dv_ttm，缺失时回退到dv_ratio
        dividend_to_use = dv_ttm_current if pd.notna(dv_ttm_current) else dv_ratio_current
        
        if pd.notna(dividend_to_use):
            if dividend_to_use >= 5.0:
                result["dividend_attractiveness"] = "very_attractive"
            elif dividend_to_use >= 3.0:
                result["dividend_attractiveness"] = "attractive"
            elif dividend_to_use >= 1.0:
                result["dividend_attractiveness"] = "moderate"
            else:
                result["dividend_attractiveness"] = "low_yield"
        else:
            result["dividend_attractiveness"] = "no_dividend"
        
        # ==================== 字段4: PS状态分析 ====================
        ps_ttm_current = current_row.get('ps_ttm')
        ps_current = current_row.get('ps')
        
        # 优先使用ps_ttm，缺失时回退到ps
        ps_to_use = ps_ttm_current if pd.notna(ps_ttm_current) else ps_current
        
        if pd.notna(ps_to_use):
            # 获取历史PS序列（排除当前日，只使用前一日及之前的数据，并过滤负值）
            if current_idx > 0:
                hist_data = df_hist.iloc[:current_idx]  # 0 到 current_idx-1
                hist_ps = hist_data[
                    (hist_data['ps_ttm'].notna()) & (hist_data['ps_ttm'] >= 0)
                ]['ps_ttm']
                
                # 如果ps_ttm历史数据不足，尝试使用ps
                if len(hist_ps) < 100:
                    hist_ps = hist_data[
                        (hist_data['ps'].notna()) & (hist_data['ps'] >= 0)
                    ]['ps']
            else:
                hist_ps = pd.Series([], dtype=float)  # 当前日为第一天，无历史数据
            
            if len(hist_ps) >= 100:  # 有足够历史数据
                # 计算历史分位数
                percentile_30 = np.percentile(hist_ps, 30)
                percentile_70 = np.percentile(hist_ps, 70)
                
                if ps_to_use > percentile_70:
                    result["ps_status"] = "overvalued_revenue"
                elif ps_to_use < percentile_30:
                    result["ps_status"] = "undervalued_revenue"
                else:
                    result["ps_status"] = "fair_revenue"
            else:
                # 历史数据不足，使用绝对阈值
                if ps_to_use > 20:
                    result["ps_status"] = "extremely_high"
                elif ps_to_use < 2:
                    result["ps_status"] = "reasonable_revenue"
                else:
                    result["ps_status"] = "fair_revenue"
        else:
            result["ps_status"] = None
        
        # ==================== 字段5: 市值分类 ====================
        total_mv_current = current_row.get('total_mv')  # 单位：万元
        
        if pd.notna(total_mv_current):
            if total_mv_current >= 10000000:  # 1000亿
                result["market_cap_category"] = "large_cap"
            elif total_mv_current >= 2000000:  # 200亿
                result["market_cap_category"] = "mid_cap"
            else:
                result["market_cap_category"] = "small_cap"
        else:
            result["market_cap_category"] = "unknown"
        
        # ==================== 字段6: 综合估值结论 ====================
        pe_status = result.get("pe_status")
        pb_status = result.get("pb_status")
        ps_status = result.get("ps_status")
        dividend_status = result.get("dividend_attractiveness")
        market_cap = result.get("market_cap_category")
        
        # 低估条件：PE/PB/PS任一低估 + 股息有吸引力（放宽要求） + 非小盘股
        has_dividend = dividend_status in ["attractive", "very_attractive", "moderate"]
        
        is_undervalued = (
            (pe_status == "cheap" or pb_status in ["discount", "deep_discount"] or 
             ps_status == "undervalued_revenue") and
            has_dividend and
            market_cap != "small_cap"
        )
        
        # 高估条件：PE和PB同时高估，或PS高估且为小盘股
        is_overvalued = (
            (pe_status == "expensive" and pb_status in ["high_premium", "extreme_premium"]) or
            (ps_status == "overvalued_revenue" and market_cap == "small_cap")
        )
        
        # 成长溢价：PE高但PS合理且为大中盘股
        is_growth_priced = (
            pe_status == "expensive" and
            ps_status in ["fair_revenue", "reasonable_revenue"] and
            market_cap in ["large_cap", "mid_cap"]
        )
        
        # 投机性：小盘股 + PE高 + 股息低
        is_speculative = (
            market_cap == "small_cap" and
            pe_status == "expensive" and
            dividend_status in ["low_yield", "no_dividend"]
        )
        
        # 亏损股特殊处理
        is_unprofitable = pe_status == "unprofitable"
        
        # 估值结论优先级：亏损股 > 低估 > 高估 > 成长溢价 > 投机性 > 中性
        if is_unprofitable:
            result["valuation_summary"] = "unprofitable"
        elif is_undervalued:
            result["valuation_summary"] = "undervalued"
        elif is_overvalued:
            result["valuation_summary"] = "overvalued"
        elif is_growth_priced:
            result["valuation_summary"] = "growth_priced"
        elif is_speculative:
            result["valuation_summary"] = "speculative"
        else:
            result["valuation_summary"] = "neutral"
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_oscillator_signals(
    ts_code: str,
    trade_date: str,
) -> str:
    """获取股票震荡指标信号分析。
    
    基于 Tushare 专业版提供的全量技术因子，对股票当前的超买、超卖状态及潜在反转信号进行结构化、语义化的判断：
    - RSI超买超卖状态 (rsi_status)
    - KDJ综合信号分析 (kdj_status)  
    - 威廉指标状态 (williams_r_status)
    - 乖离率偏离程度 (bias_status)
    - CCI异常波动预警 (cci_status)
    - 综合反转信号评估 (reversal_signal)
    
    参数说明：
    - ts_code: 股票代码（必需），如 000001.SZ
    - trade_date: 交易日期（必需），格式 YYYYMMDD
    
    返回示例：
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
    """
    try:
        # 获取包含当前日及历史数据（用于交叉信号判断）
        # 使用历史窗口而非简单的日历日计算，避免月末/月初日期错误
        df_hist = pro.stk_factor_pro(
            ts_code=ts_code,
            start_date=str(int(trade_date) - 10000),  # 往前推100天（足够获取多个交易日）
            end_date=trade_date,
        )
        
        if df_hist.empty:
            return json.dumps({"error": f"未获取到 {trade_date} 附近的数据"})
        
        # 按日期排序并重置索引
        df_hist = df_hist.sort_values('trade_date').reset_index(drop=True)
        
        # 找到当前交易日的位置
        current_idx = df_hist[df_hist['trade_date'] == trade_date].index
        if len(current_idx) == 0:
            return json.dumps({"error": f"未获取到 {trade_date} 的数据"})
        
        current_idx = current_idx[0]
        current_row = df_hist.iloc[current_idx]
        
        result = {
            "ts_code": current_row['ts_code'],
            "trade_date": current_row['trade_date']
        }
        
        # ==================== 字段1: RSI状态分析 ====================
        rsi_6 = current_row.get('rsi_qfq_6')
        rsi_12 = current_row.get('rsi_qfq_12')
        
        if pd.notna(rsi_6):
            if rsi_6 >= 70:
                result["rsi_status"] = "overbought"
            elif rsi_6 <= 30:
                result["rsi_status"] = "oversold"
            else:
                result["rsi_status"] = "neutral"
        elif pd.notna(rsi_12):
            # 回退到RSI12，阈值放宽
            if rsi_12 >= 75:
                result["rsi_status"] = "overbought"
            elif rsi_12 <= 25:
                result["rsi_status"] = "oversold"
            else:
                result["rsi_status"] = "neutral"
        else:
            result["rsi_status"] = None
        
        # ==================== 字段2: KDJ综合信号分析 ====================
        k_val = current_row.get('kdj_k_qfq')
        d_val = current_row.get('kdj_d_qfq')
        
        # 数据有效性检查：如果KDJ数据缺失，返回None而非"neutral"
        if not (pd.notna(k_val) and pd.notna(d_val)):
            result["kdj_status"] = None
        else:
            kdj_status = "neutral"  # 默认状态
            
            # 尝试获取前一日数据进行交叉判断
            try:
                # 使用历史数据中前一个交易日
                if current_idx > 0:
                    prev_row = df_hist.iloc[current_idx - 1]
                    prev_k = prev_row.get('kdj_k_qfq')
                    prev_d = prev_row.get('kdj_d_qfq')
                    
                    if pd.notna(prev_k) and pd.notna(prev_d):
                        # 金叉：前一日 K ≤ D，当日 K > D
                        if prev_k <= prev_d and k_val > d_val:
                            if k_val < 50:
                                kdj_status = "bullish_crossover_in_oversold"
                            else:
                                kdj_status = "bullish_crossover"
                        # 死叉：前一日 K ≥ D，当日 K < D
                        elif prev_k >= prev_d and k_val < d_val:
                            if k_val > 50:
                                kdj_status = "bearish_crossover_in_overbought"
                            else:
                                kdj_status = "bearish_crossover"
                        else:
                            # 非交叉日，判断超买超卖风险
                            if k_val > 80:
                                kdj_status = "overbought_risk"
                            elif k_val < 20:
                                kdj_status = "oversold_opportunity"
                            else:
                                kdj_status = "neutral"
                    else:
                        # 前一日数据缺失，仅判断当前状态
                        if k_val > 80:
                            kdj_status = "overbought_risk"
                        elif k_val < 20:
                            kdj_status = "oversold_opportunity"
                else:
                    # 当前日为序列第一个，仅判断当前状态
                    if k_val > 80:
                        kdj_status = "overbought_risk"
                    elif k_val < 20:
                        kdj_status = "oversold_opportunity"
            except Exception:
                # 异常情况下，仅判断当前状态
                if k_val > 80:
                    kdj_status = "overbought_risk"
                elif k_val < 20:
                    kdj_status = "oversold_opportunity"
            
            result["kdj_status"] = kdj_status
        
        # ==================== 字段3: 威廉指标状态 ====================
        wr1 = current_row.get('wr1_qfq')  # N=6，更敏感
        wr = current_row.get('wr_qfq')    # N=10
        
        if pd.notna(wr1):
            if wr1 >= -20:
                result["williams_r_status"] = "overbought"
            elif wr1 <= -80:
                result["williams_r_status"] = "oversold"
            else:
                result["williams_r_status"] = "neutral"
        elif pd.notna(wr):
            if wr >= -20:
                result["williams_r_status"] = "overbought"
            elif wr <= -80:
                result["williams_r_status"] = "oversold"
            else:
                result["williams_r_status"] = "neutral"
        else:
            result["williams_r_status"] = None
        
        # ==================== 字段4: BIAS乖离率状态 ====================
        bias1 = current_row.get('bias1_qfq')  # 6日乖离率
        bias2 = current_row.get('bias2_qfq')  # 12日乖离率
        bias3 = current_row.get('bias3_qfq')  # 24日乖离率
        
        bias_status = "normal_deviation"
        
        if pd.notna(bias1):
            if bias1 > 5.0:
                bias_status = "high_positive_deviation"
            elif bias1 < -5.0:
                bias_status = "high_negative_deviation"
        elif pd.notna(bias2):
            if bias2 > 6.0:
                bias_status = "high_positive_deviation"
            elif bias2 < -6.0:
                bias_status = "high_negative_deviation"
        elif pd.notna(bias3):
            if bias3 > 7.0:
                bias_status = "high_positive_deviation"
            elif bias3 < -7.0:
                bias_status = "high_negative_deviation"
        
        result["bias_status"] = bias_status
        
        # ==================== 字段5: CCI状态分析 ====================
        cci = current_row.get('cci_qfq')
        
        if pd.notna(cci):
            if cci > 100:
                result["cci_status"] = "overbought_or_breakout"
            elif cci < -100:
                result["cci_status"] = "oversold_or_breakdown"
            else:
                result["cci_status"] = "normal_range"
        else:
            result["cci_status"] = None
        
        # ==================== 字段6: 综合反转信号判断 ====================
        # 统计极端指标数量（超买或超卖）
        extreme_indicators = 0
        bullish_signals = 0
        bearish_signals = 0
        
        # 获取当前指标状态
        rsi_status = result.get("rsi_status")
        williams_r_status = result.get("williams_r_status")
        cci_status = result.get("cci_status")
        
        # 重新定义KDJ状态（从 result 字典获取）
        kdj_status = result.get("kdj_status")
        
        if rsi_status in ['oversold']:
            extreme_indicators += 1
            bullish_signals += 1
        elif rsi_status in ['overbought']:
            extreme_indicators += 1
            bearish_signals += 1
            
        if kdj_status in ['oversold_opportunity', 'bullish_crossover_in_oversold', 'bullish_crossover']:
            extreme_indicators += 1
            bullish_signals += 1
        elif kdj_status in ['overbought_risk', 'bearish_crossover_in_overbought', 'bearish_crossover']:
            extreme_indicators += 1
            bearish_signals += 1
            
        if williams_r_status in ['oversold']:
            extreme_indicators += 1
            bullish_signals += 1
        elif williams_r_status in ['overbought']:
            extreme_indicators += 1
            bearish_signals += 1
            
        if bias_status in ['high_negative_deviation']:
            extreme_indicators += 1
            bullish_signals += 1
        elif bias_status in ['high_positive_deviation']:
            extreme_indicators += 1
            bearish_signals += 1
            
        if cci_status in ['oversold_or_breakdown']:
            extreme_indicators += 1
            bullish_signals += 1
        elif cci_status in ['overbought_or_breakout']:
            extreme_indicators += 1
            bearish_signals += 1
        
        # 获取BIAS当前值用于强信号判断
        bias_current = None
        if bias1 is not None:
            bias_current = bias1
        elif bias2 is not None:
            bias_current = bias2
        elif bias3 is not None:
            bias_current = bias3
        
        # 综合判断逻辑：强化条件避免过度敏感
        if extreme_indicators >= 2:
            # 检查是否有金叉信号（看涨）
            has_bullish_crossover = any([
                kdj_status in ['bullish_crossover', 'bullish_crossover_in_oversold']
            ])
            
            # 检查乖离率极端条件（价格已回调）
            is_bias_extreme = (bias_current is not None) and (bias_current <= -4.0)
            
            # 强烈看涨反转需要：至少2个极端指标 + 金叉/连续上升 + 乖离率支持
            if has_bullish_crossover and is_bias_extreme:
                reversal_signal = "strong_bullish_reversal"
            elif bullish_signals >= 2 and is_bias_extreme:
                reversal_signal = "moderate_reversal_risk"  # 避免过度强烈判断
            elif bearish_signals >= 2:
                # 强烈看跌信号
                has_bearish_crossover = any([
                    kdj_status in ['bearish_crossover', 'bearish_crossover_in_overbought']
                ])
                
                if has_bearish_crossover:
                    reversal_signal = "strong_bearish_reversal"
                else:
                    reversal_signal = "moderate_reversal_risk"
            else:
                reversal_signal = "moderate_reversal_risk"
        else:
            reversal_signal = "no_significant_signal"
        
        result["reversal_signal"] = reversal_signal
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_volatility_profile(
    ts_code: str,
    date: str,
) -> str:
    """获取股票波动性分析。
    
    基于 Tushare 专业版技术因子数据，评估股票当前的波动水平、风险状态及潜在变盘信号。
    专门设计用于回答"这只股票最近波动大吗？"、"当前是高风险还是低风险状态？"等问题。
    
    核心分析维度：
    - ATR波动率状态 (atr_status)
    - 布林带位置与带宽分析 (bollinger_status)  
    - MASS梅斯指标波动压缩状态 (mass_status)
    - 肯特纳通道趋势位置 (keltner_status)
    - 价格极值新鲜度 (extreme_price_status)
    - 综合波动状态评估 (volatility_regime)
    - 风险预警信号 (risk_warning)
    
    参数说明：
    - ts_code: 股票代码（必需），如 000001.SZ
    - date: 分析日期（必需），格式 YYYYMMDD
    
    返回示例：
    {
      "ts_code": "000001.SZ",
      "date": "20240115",
      "atr_status": "normal_volatility",
      "bollinger_status": "upper_half",
      "mass_status": "normal_range", 
      "keltner_status": "within_keltner_channel",
      "extreme_price_status": "no_extreme_price",
      "volatility_regime": "normal_volatility",
      "risk_warning": "none"
    }
    """
    try:
        # 获取包含当前日及历史数据（用于历史窗口计算）
        df_hist = pro.stk_factor_pro(
            ts_code=ts_code,
            start_date=str(int(date) - 10000),  # 往前推100天（足够获取历史窗口）
            end_date=date,
        )
        
        if df_hist.empty:
            return json.dumps({"error": f"未获取到 {date} 附近的数据"})
        
        # 按日期排序并重置索引
        df_hist = df_hist.sort_values('trade_date').reset_index(drop=True)
        
        # 找到当前交易日的位置
        current_idx = df_hist[df_hist['trade_date'] == date].index
        if len(current_idx) == 0:
            return json.dumps({"error": f"未获取到 {date} 的数据"})
        
        current_idx = current_idx[0]
        current_row = df_hist.iloc[current_idx]
        
        result = {
            "ts_code": current_row['ts_code'],
            "date": current_row['trade_date']
        }
        
        # ==================== 字段1: ATR状态分析 ====================
        atr_val = current_row.get('atr_qfq')
        
        if pd.notna(atr_val):
            # 计算近20日ATR均值（如果数据足够）
            if current_idx >= 19:  # 有足够的20天历史数据
                hist_data = df_hist.iloc[current_idx-19:current_idx+1]
                valid_atr = hist_data['atr_qfq'].dropna()
                
                if len(valid_atr) >= 15:  # 至少需要15个有效数据点
                    avg_atr_20 = valid_atr.mean()
                    
                    if atr_val > 1.5 * avg_atr_20:
                        result["atr_status"] = "high_volatility"
                    elif atr_val < 0.7 * avg_atr_20:
                        result["atr_status"] = "low_volatility"
                    else:
                        result["atr_status"] = "normal_volatility"
                else:
                    # 数据不足，使用绝对阈值
                    if atr_val > 2.0:
                        result["atr_status"] = "high_volatility"
                    elif atr_val < 0.5:
                        result["atr_status"] = "low_volatility"
                    else:
                        result["atr_status"] = "normal_volatility"
            else:
                # 历史数据不足20天，使用绝对阈值
                if atr_val > 2.0:
                    result["atr_status"] = "high_volatility"
                elif atr_val < 0.5:
                    result["atr_status"] = "low_volatility"
                else:
                    result["atr_status"] = "normal_volatility"
        else:
            result["atr_status"] = None
        
        # ==================== 字段2: 布林带状态分析 ====================
        close = current_row.get('close_qfq')
        boll_upper = current_row.get('boll_upper_qfq')
        boll_lower = current_row.get('boll_lower_qfq')
        boll_mid = current_row.get('boll_mid_qfq')
        
        if all(pd.notna(val) for val in [close, boll_upper, boll_lower, boll_mid]):
            bollinger_status_parts = []
            
            # 价格位置判断
            if close >= boll_upper:
                bollinger_status_parts.append("above_upper_band")
            elif close <= boll_lower:
                bollinger_status_parts.append("below_lower_band")
            elif close > boll_mid:
                bollinger_status_parts.append("upper_half")
            else:
                bollinger_status_parts.append("lower_half")
            
            # 带宽状态判断（波动压缩/扩张）
            band_width = (boll_upper - boll_lower) / boll_mid
            
            if band_width > 0.15:
                bollinger_status_parts.append("wide_band")
            elif band_width < 0.08:
                bollinger_status_parts.append("narrow_band")
            # 移除normal_band状态，只有宽和窄两种状态有分析价值
            
            # 合并状态（主要位置状态 + 带宽状态）
            if "above_upper_band" in bollinger_status_parts:
                if "wide_band" in bollinger_status_parts:
                    result["bollinger_status"] = "above_upper_with_wide_band"
                elif "narrow_band" in bollinger_status_parts:
                    result["bollinger_status"] = "above_upper_with_narrow_band"
                else:
                    result["bollinger_status"] = "above_upper_band"
            elif "below_lower_band" in bollinger_status_parts:
                if "wide_band" in bollinger_status_parts:
                    result["bollinger_status"] = "below_lower_with_wide_band"
                elif "narrow_band" in bollinger_status_parts:
                    result["bollinger_status"] = "below_lower_with_narrow_band"
                else:
                    result["bollinger_status"] = "below_lower_band"
            elif "upper_half" in bollinger_status_parts:
                if "narrow_band" in bollinger_status_parts:
                    result["bollinger_status"] = "upper_half_narrow_band"
                else:
                    result["bollinger_status"] = "upper_half"
            else:  # lower_half
                if "narrow_band" in bollinger_status_parts:
                    result["bollinger_status"] = "lower_half_narrow_band"
                else:
                    result["bollinger_status"] = "lower_half"
        else:
            result["bollinger_status"] = None
        
        # ==================== 字段3: MASS梅斯指标状态分析 ====================
        mass_val = current_row.get('mass_qfq')
        
        if pd.notna(mass_val):
            # 检查前一日数据用于反转信号判断
            if current_idx > 0:
                prev_mass = df_hist.iloc[current_idx - 1]['mass_qfq']
                
                if pd.notna(prev_mass):
                    # 梅斯反转信号：今日 < 27 且 前日 >= 27
                    if mass_val < 27 and prev_mass >= 27:
                        result["mass_status"] = "mass_reversal_signal"
                    else:
                        # 经典阈值判断
                        if mass_val > 27:
                            result["mass_status"] = "high_mass"
                        elif mass_val < 26.5:
                            result["mass_status"] = "low_mass"
                        else:
                            result["mass_status"] = "reversal_zone"
                else:
                    # 前一日数据缺失，仅进行阈值判断
                    if mass_val > 27:
                        result["mass_status"] = "high_mass"
                    elif mass_val < 26.5:
                        result["mass_status"] = "low_mass"
                    else:
                        result["mass_status"] = "reversal_zone"
            else:
                # 当前日为序列第一个，仅进行阈值判断
                if mass_val > 27:
                    result["mass_status"] = "high_mass"
                elif mass_val < 26.5:
                    result["mass_status"] = "low_mass"
                else:
                    result["mass_status"] = "reversal_zone"
        else:
            result["mass_status"] = None
        
        # ==================== 字段4: 肯特纳通道状态分析 ====================
        ktn_upper = current_row.get('ktn_upper_qfq')
        ktn_down = current_row.get('ktn_down_qfq')
        
        if pd.notna(close) and pd.notna(ktn_upper) and pd.notna(ktn_down):
            if close >= ktn_upper:
                result["keltner_status"] = "above_keltner_upper"
            elif close <= ktn_down:
                result["keltner_status"] = "below_keltner_lower"
            else:
                result["keltner_status"] = "within_keltner_channel"
        else:
            result["keltner_status"] = None
        
        # ==================== 字段5: 价格极值状态分析 ====================
        topdays = current_row.get('topdays')
        lowdays = current_row.get('lowdays')
        
        # 重新获取价格用于综合判断
        current_high = current_row.get('high_qfq')
        current_low = current_row.get('low_qfq')
        
        # 首先检查是否有极值数据
        if pd.notna(topdays) or pd.notna(lowdays):
            if topdays is not None and topdays >= 20:
                extreme_status = "recent_new_high"
            elif lowdays is not None and lowdays >= 20:
                extreme_status = "recent_new_low"
            else:
                extreme_status = "no_extreme_price"
        else:
            # 如果没有极值数据，使用价格位置替代判断
            if current_idx >= 20:  # 有足够历史数据（排除当前日）
                # 前20天（不含当前日）
                hist_data = df_hist.iloc[current_idx-20:current_idx]
                hist_high = hist_data['high_qfq'].max()
                hist_low = hist_data['low_qfq'].min()
                
                if pd.notna(current_high) and pd.notna(hist_high) and current_high > hist_high:
                    extreme_status = "recent_new_high"
                elif pd.notna(current_low) and pd.notna(hist_low) and current_low < hist_low:
                    extreme_status = "recent_new_low"
                elif pd.notna(current_high) and pd.notna(hist_high) and current_high >= hist_high * 0.98:  # 接近新高
                    extreme_status = "near_new_high"
                else:
                    extreme_status = "no_extreme_price"
            else:
                extreme_status = "no_extreme_price"
        
        result["extreme_price_status"] = extreme_status
        
        # ==================== 字段6: 综合波动状态评估 ====================
        atr_status = result.get("atr_status")
        bollinger_status = result.get("bollinger_status")
        mass_status = result.get("mass_status")
        
        # 高波动风险：ATR高 + 布林带宽 + 价格极端
        is_high_vol = atr_status == "high_volatility"
        is_wide_band = "wide_band" in bollinger_status if bollinger_status else False
        is_extreme_price = extreme_status in ["recent_new_high", "recent_new_low"]
        
        if is_high_vol and is_wide_band and is_extreme_price:
            volatility_regime = "elevated_volatility"
        
        # 变盘预警：布林带窄或MASS低位且ATR低
        elif (("narrow_band" in bollinger_status) or 
              (mass_status == "low_mass")) and atr_status == "low_volatility":
            volatility_regime = "compression_before_breakout"
        
        else:
            volatility_regime = "normal_volatility"
        
        result["volatility_regime"] = volatility_regime
        
        # ==================== 字段7: 风险预警信号 ====================
        # 高位高波动风险：价格在上轨外 + 新高 + 高ATR
        if (bollinger_status and "above_upper" in bollinger_status and 
            extreme_status == "recent_new_high" and atr_status == "high_volatility"):
            risk_warning = "high_short_term_risk"
        
        # 低位高波动机会：价格在下轨外 + 新低 + 高ATR
        elif (bollinger_status and "below_lower" in bollinger_status and 
              extreme_status == "recent_new_low" and atr_status == "high_volatility"):
            risk_warning = "high_short_term_opportunity"
        
        # 低风险盘整：布林带窄 + 低ATR
        elif (bollinger_status and "narrow_band" in bollinger_status and 
              atr_status == "low_volatility"):
            risk_warning = "low_risk_consolidation"
        
        else:
            risk_warning = "none"
        
        result["risk_warning"] = risk_warning
        
        return json.dumps(result, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    mcp.run(transport="stdio")