import os
import json
from typing import Optional, cast

import pandas as pd
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

mcp = FastMCP("Tushare MCP Server")


@mcp.tool()
def stk_factor_pro(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取股票技术面因子数据（专业版技术指标）。

    参数说明：
    - ts_code: 股票代码，如 000001.SZ
    - trade_date: 交易日期，格式 YYYYMMDD
    - start_date/end_date: 开始/结束日期，格式 YYYYMMDD
    """
    try:
        df = pro.stk_factor_pro(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def moneyflow(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取个股资金流向数据。

    - ts_code: 股票代码
    - trade_date: 交易日期
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.moneyflow(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def moneyflow_cnt_ths(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取同花顺概念板块资金流向数据。

    - ts_code: 板块代码
    - trade_date: 交易日期 YYYYMMDD
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.moneyflow_cnt_ths(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def moneyflow_ind_ths(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    industry_code: Optional[str] = None,
    industry_name: Optional[str] = None,
) -> str:
    """获取同花顺行业板块资金流向数据。

    - ts_code: 板块代码
    - trade_date: 交易日期 YYYYMMDD
    - start_date/end_date: 日期范围
    - industry_code/name: 行业代码或名称
    """
    try:
        df = pro.moneyflow_ind_ths(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
            industry_code=industry_code,
            industry_name=industry_name,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def cyq_perf(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取股票筹码分布数据。

    - ts_code: 股票代码
    - trade_date: 交易日期
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.cyq_perf(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def stock_basic(
    ts_code: Optional[str] = None,
    name: Optional[str] = None,
    exchange: Optional[str] = None,
    list_status: Optional[str] = None,
    market: Optional[str] = None,
    is_hs: Optional[str] = None,
    fields: Optional[str] = None,
) -> str:
    """获取股票基本信息。

    常用参数：ts_code、name、exchange、list_status、market、is_hs、fields
    """
    try:
        df = pro.stock_basic(
            ts_code=ts_code,
            name=name,
            exchange=exchange,
            list_status=list_status,
            market=market,
            is_hs=is_hs,
            **({"fields": fields} if fields is not None else {})
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_classify(
    level: Optional[str] = None,
    src: Optional[str] = None,
) -> str:
    """获取行业分类信息。

    可选参数：level、src
    """
    try:
        df = pro.index_classify(level=level, src=src)
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def fina_indicator(
    ts_code: Optional[str] = None,
    ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
) -> str:
    """获取财务指标数据。

    常用参数：ts_code、ann_date、start_date、end_date、period
    """
    try:
        df = pro.fina_indicator(
            ts_code=ts_code,
            ann_date=ann_date,
            start_date=start_date,
            end_date=end_date,
            period=period,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def stk_holdernumber(
    ts_code: Optional[str] = None,
    ann_date: Optional[str] = None,
    enddate: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取股东人数数据。

    - ts_code: 股票代码
    - ann_date: 公告日期
    - enddate: 截止日期
    - start_date/end_date: 公告日期范围
    """
    try:
        df = pro.stk_holdernumber(
            ts_code=ts_code,
            ann_date=ann_date,
            enddate=enddate,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def ths_daily(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取同花顺指数日线数据。

    - ts_code: 指数代码
    - trade_date: 交易日期
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.ths_daily(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_weekly(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取指数周线数据。

    - ts_code: 指数代码
    - trade_date: 交易日期
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.index_weekly(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date)
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def trade_cal(
    exchange: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    is_open: Optional[str] = None,
) -> str:
    """获取交易日历数据。

    - exchange: 交易所代码（SSE/ SZSE / …）
    - start_date/end_date: 日期范围
    - is_open: 是否交易日（1 是，0 否）
    """
    try:
        df = pro.trade_cal(
            exchange=exchange,
            start_date=start_date,
            end_date=end_date,
            is_open=is_open,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def stk_auction_o(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取集合竞价数据。

    - ts_code: 股票代码
    - trade_date: 交易日期
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.stk_auction_o(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def income(
    ts_code: Optional[str] = None,
    ann_date: Optional[str] = None,
    f_ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    report_type: Optional[str] = None,
    comp_type: Optional[str] = None,
) -> str:
    """获取利润表数据。

    - ts_code: 股票代码
    - ann_date/f_ann_date: 公告日期/实际公告日期（YYYYMMDD）
    - start_date/end_date: 公告日期范围（YYYYMMDD）
    - period: 报告期（如 20171231、20170930 等）
    - report_type/comp_type: 报告类型/公司类型
    """
    try:
        df = pro.income(
            ts_code=ts_code,
            ann_date=ann_date,
            f_ann_date=f_ann_date,
            start_date=start_date,
            end_date=end_date,
            period=period,
            report_type=report_type,
            comp_type=comp_type,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def balancesheet(
    ts_code: str,
    ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    report_type: Optional[str] = None,
    comp_type: Optional[str] = None,
) -> str:
    """获取资产负债表数据。

    - ts_code: 股票代码
    - ann_date: 公告日期（YYYYMMDD）
    - start_date/end_date: 公告日期范围（YYYYMMDD）
    - period: 报告期（如 20171231、20170930 等）
    - report_type/comp_type: 报告类型/公司类型
    """
    try:
        df = pro.balancesheet(
            ts_code=ts_code,
            ann_date=ann_date,
            start_date=start_date,
            end_date=end_date,
            period=period,
            report_type=report_type,
            comp_type=comp_type,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def cashflow(
    ts_code: str,
    ann_date: Optional[str] = None,
    f_ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    report_type: Optional[str] = None,
    comp_type: Optional[str] = None,
    is_calc: Optional[int] = None,
) -> str:
    """获取现金流量表数据。

    - ts_code: 股票代码
    - ann_date/f_ann_date: 公告日期/实际公告日期（YYYYMMDD）
    - start_date/end_date: 公告日期范围（YYYYMMDD）
    - period: 报告期（如 20171231、20170930 等）
    - report_type/comp_type: 报告类型/公司类型
    - is_calc: 是否计算报表
    """
    try:
        df = pro.cashflow(
            ts_code=ts_code,
            ann_date=ann_date,
            f_ann_date=f_ann_date,
            start_date=start_date,
            end_date=end_date,
            period=period,
            report_type=report_type,
            comp_type=comp_type,
            is_calc=is_calc,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def top10_floatholders(
    ts_code: str,
    period: str,
    ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取前十大流通股东数据。

    - ts_code: 股票代码
    - period: 报告期（YYYYMMDD）
    - ann_date: 公告日期（YYYYMMDD）
    - start_date/end_date: 报告期范围（YYYYMMDD）
    """
    try:
        df = pro.top10_floatholders(
            ts_code=ts_code,
            period=period,
            ann_date=ann_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_monthly(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取指数月线行情数据。

    参数说明：
    - ts_code: TS指数代码
    - trade_date: 交易日期，格式 YYYYMMDD
    - start_date/end_date: 开始/结束日期，格式 YYYYMMDD
    """
    try:
        df = pro.index_monthly(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def idx_factor_pro(
    ts_code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    trade_date: Optional[str] = None,
) -> str:
    """获取指数技术因子数据（专业版）。

    参数说明：
    - ts_code: 指数代码(大盘指数 申万指数 中信指数)
    - start_date/end_date: 开始/结束日期
    - trade_date: 交易日期
    """
    try:
        df = pro.idx_factor_pro(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date,
            trade_date=trade_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def moneyflow_mkt_dc(
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取东方财富大盘资金流向数据。

    参数说明：
    - trade_date: 交易日期(YYYYMMDD格式) (可选参数)
    - start_date: 开始日期(YYYYMMDD格式) (可选参数)
    - end_date: 结束日期(YYYYMMDD格式) (可选参数)
    
    注意：所有参数都是可选的，如果不提供任何参数，将返回默认数据
    日期格式必须为YYYYMMDD，例如: 20240101
    
    示例调用：
    moneyflow_mkt_dc(start_date="20240101", end_date="20240131")
    moneyflow_mkt_dc()  # 返回默认数据
    
    数据说明：
    - 每日盘后更新
    - 包含上证/深证收盘价、涨跌幅
    - 提供主力净流入、超大单、大单、中单、小单资金流向数据
    """
    try:
        df = pro.moneyflow_mkt_dc(
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def moneyflow_hsgt(
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取沪深港通资金流向数据。

    参数说明：
    - trade_date: 交易日期(YYYYMMDD格式) (必需参数之一)
    - start_date: 开始日期(YYYYMMDD格式) (必需参数之一)
    - end_date: 结束日期(YYYYMMDD格式)
    
    注意：必须提供以下参数之一: trade_date, start_date
    日期格式必须为YYYYMMDD，例如: 20240101
    
    示例调用：
    moneyflow_hsgt(start_date="20240101", end_date="20240131")
    
    数据说明：
    - 包含沪股通、深股通、港股通资金流向
    - 提供北向资金和南向资金数据
    - 每日18~20点之间完成更新
    - 每次最多返回300条记录
    """
    # 参数验证
    if trade_date is None and start_date is None:
        return json.dumps({"error": "必须提供以下参数之一: trade_date, start_date"})
    
    # 日期格式验证
    date_fields = {"trade_date": trade_date, "start_date": start_date, "end_date": end_date}
    for field_name, date_value in date_fields.items():
        if date_value is not None and not (len(date_value) == 8 and date_value.isdigit()):
            return json.dumps({"error": f"参数 {field_name} 的日期格式不正确，必须为YYYYMMDD格式，例如: 20240101"})
    
    try:
        df = pro.moneyflow_hsgt(
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_weight(
    index_code: str,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取各类指数成分和权重（月度数据）。

    - index_code: 指数代码（必选），如 399300.SZ
    - trade_date: 交易日期 YYYYMMDD（可选）
    - start_date/end_date: 日期范围 YYYYMMDD（可选）
    """
    try:
        df = pro.index_weight(
            index_code=index_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_dailybasic(
    trade_date: Optional[str] = None,
    ts_code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取大盘指数每日指标数据。

    - trade_date: 交易日期 YYYYMMDD
    - ts_code: TS指数代码
    - start_date/end_date: 日期范围 YYYYMMDD
    """
    try:
        df = pro.index_dailybasic(
            trade_date=trade_date,
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def daily_basic(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fields: Optional[str] = None,
) -> str:
    """获取全部股票每日重要的基本面指标。

    - ts_code: 股票代码（二选一）
    - trade_date: 交易日期（二选一，YYYYMMDD）
    - start_date/end_date: 日期范围（YYYYMMDD）
    - fields: 指定返回字段（可选）
    """
    try:
        df = pro.daily_basic(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
            **({"fields": fields} if fields is not None else {}),
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_member_all(
    l1_code: Optional[str] = None,
    l2_code: Optional[str] = None,
    l3_code: Optional[str] = None,
    ts_code: Optional[str] = None,
    is_new: Optional[str] = None,
) -> str:
    """获取申万行业成分构成(分级)。

    参数说明：
    - l1_code: 一级行业代码（可选）
    - l2_code: 二级行业代码（可选）
    - l3_code: 三级行业代码（可选）
    - ts_code: 股票代码（可选）
    - is_new: 是否最新（可选，默认为"Y"）
    
    使用说明：
    - 可按三级分类提取申万行业成分，可提供某个分类的所有成分
    - 也可按股票代码提取所属分类，参数灵活
    - 单次最大2000行，总量不限制
    
    示例调用：
    # 获取黄金分类的成份股
    index_member_all(l3_code='850531.SI')
    
    # 获取000001.SZ所属行业
    index_member_all(ts_code='000001.SZ')
    """
    try:
        df = pro.index_member_all(
            l1_code=l1_code,
            l2_code=l2_code,
            l3_code=l3_code,
            ts_code=ts_code,
            is_new=is_new,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


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


if __name__ == "__main__":
    mcp.run(transport="stdio")
