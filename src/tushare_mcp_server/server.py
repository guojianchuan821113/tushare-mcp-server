import os
import json
from typing import Optional, cast

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
    fields: Optional[str] = None,
) -> str:
    """获取股票技术面因子数据（专业版技术指标）。

    参数说明：
    - ts_code: 股票代码，如 000001.SZ
    - trade_date: 交易日期，格式 YYYYMMDD
    - start_date/end_date: 开始/结束日期，格式 YYYYMMDD
    - fields: 指定返回字段
    """
    try:
        df = pro.stk_factor_pro(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
            **({"fields": fields} if fields is not None else {})
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
    date: Optional[str] = None,
    concept_code: Optional[str] = None,
    concept_name: Optional[str] = None,
) -> str:
    """获取同花顺概念板块资金流向数据。

    - date: 日期 YYYYMMDD
    - concept_code/name: 概念代码或名称
    """
    try:
        df = pro.moneyflow_cnt_ths(
            date=date,
            concept_code=concept_code,
            concept_name=concept_name,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def moneyflow_ind_ths(
    date: Optional[str] = None,
    industry_code: Optional[str] = None,
    industry_name: Optional[str] = None,
) -> str:
    """获取同花顺行业板块资金流向数据。

    - date: 日期 YYYYMMDD
    - industry_code/name: 行业代码或名称
    """
    try:
        df = pro.moneyflow_ind_ths(
            date=date,
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
    industry: Optional[str] = None,
    src: Optional[str] = None,
) -> str:
    """获取行业分类信息。

    可选参数：level、industry、src
    """
    try:
        df = pro.index_classify(level=level, industry=industry, src=src)
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
    fields: Optional[str] = None,
) -> str:
    """获取财务指标数据。

    常用参数：ts_code、ann_date、start_date、end_date、period、fields
    """
    try:
        df = pro.fina_indicator(
            ts_code=ts_code,
            ann_date=ann_date,
            start_date=start_date,
            end_date=end_date,
            period=period,
            **({"fields": fields} if fields is not None else {})
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def stk_holdernumber(
    ts_code: Optional[str] = None,
    ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取股东人数数据。

    - ts_code: 股票代码
    - ann_date: 公告日期
    - start_date/end_date: 公告日期范围
    """
    try:
        df = pro.stk_holdernumber(
            ts_code=ts_code,
            ann_date=ann_date,
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
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """获取指数周线数据。

    - ts_code: 指数代码
    - start_date/end_date: 日期范围
    """
    try:
        df = pro.index_weekly(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def trade_cal(
    exchange: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    is_open: Optional[int] = None,
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
    fields: Optional[str] = None,
) -> str:
    """获取利润表数据。

    - ts_code: 股票代码
    - ann_date/f_ann_date: 公告日期/实际公告日期（YYYYMMDD）
    - start_date/end_date: 公告日期范围（YYYYMMDD）
    - period: 报告期（如 20171231、20170930 等）
    - report_type/comp_type: 报告类型/公司类型
    - fields: 指定返回字段
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
            **({"fields": fields} if fields is not None else {})
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def balancesheet(
    ts_code: Optional[str] = None,
    ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    report_type: Optional[str] = None,
    comp_type: Optional[str] = None,
    fields: Optional[str] = None,
) -> str:
    """获取资产负债表数据。

    - ts_code: 股票代码
    - ann_date: 公告日期（YYYYMMDD）
    - start_date/end_date: 公告日期范围（YYYYMMDD）
    - period: 报告期（如 20171231、20170930 等）
    - report_type/comp_type: 报告类型/公司类型
    - fields: 指定返回字段
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
            **({"fields": fields} if fields is not None else {})
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def cashflow(
    ts_code: Optional[str] = None,
    ann_date: Optional[str] = None,
    f_ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    period: Optional[str] = None,
    report_type: Optional[str] = None,
    comp_type: Optional[str] = None,
    is_calc: Optional[int] = None,
    fields: Optional[str] = None,
) -> str:
    """获取现金流量表数据。

    - ts_code: 股票代码
    - ann_date/f_ann_date: 公告日期/实际公告日期（YYYYMMDD）
    - start_date/end_date: 公告日期范围（YYYYMMDD）
    - period: 报告期（如 20171231、20170930 等）
    - report_type/comp_type: 报告类型/公司类型
    - is_calc: 是否计算报表
    - fields: 指定返回字段
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
            **({"fields": fields} if fields is not None else {})
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def top10_floatholders(
    ts_code: Optional[str] = None,
    period: Optional[str] = None,
    ann_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fields: Optional[str] = None,
) -> str:
    """获取前十大流通股东数据。

    - ts_code: 股票代码
    - period: 报告期（YYYYMMDD）
    - ann_date: 公告日期（YYYYMMDD）
    - start_date/end_date: 报告期范围（YYYYMMDD）
    - fields: 指定返回字段
    """
    try:
        df = pro.top10_floatholders(
            ts_code=ts_code,
            period=period,
            ann_date=ann_date,
            start_date=start_date,
            end_date=end_date,
            **({"fields": fields} if fields is not None else {})
        )
        return df.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def index_monthly(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fields: Optional[str] = None,
) -> str:
    """获取指数月线行情数据。

    参数说明：
    - ts_code: TS指数代码
    - trade_date: 交易日期，格式 YYYYMMDD
    - start_date/end_date: 开始/结束日期，格式 YYYYMMDD
    - fields: 指定返回字段
    """
    try:
        df = pro.index_monthly(
            ts_code=ts_code,
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
            **({"fields": fields} if fields is not None else {})
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
    fields: Optional[str] = None,
) -> str:
    """获取指数技术因子数据（专业版）。

    参数说明：
    - ts_code: 指数代码(大盘指数 申万指数 中信指数)
    - start_date/end_date: 开始/结束日期
    - trade_date: 交易日期
    - fields: 指定返回字段
    """
    try:
        df = pro.idx_factor_pro(
            ts_code=ts_code,
            start_date=start_date,
            end_date=end_date,
            trade_date=trade_date,
            **({"fields": fields} if fields is not None else {})
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
    - trade_date: 交易日期(YYYYMMDD格式)
    - start_date: 开始日期
    - end_date: 结束日期
    
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
    - trade_date: 交易日期(YYYYMMDD格式)
    - start_date: 开始日期
    - end_date: 结束日期
    
    数据说明：
    - 包含沪股通、深股通、港股通资金流向
    - 提供北向资金和南向资金数据
    - 每日18~20点之间完成更新
    - 每次最多返回300条记录
    """
    try:
        df = pro.moneyflow_hsgt(
            trade_date=trade_date,
            start_date=start_date,
            end_date=end_date,
        )
        return cast(str, df.to_json(orient="records", force_ascii=False))
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run(transport="stdio")
