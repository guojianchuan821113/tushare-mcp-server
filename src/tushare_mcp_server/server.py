import os
import json
from typing import Optional

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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
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
        return df.to_json(orient="records", force_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run(transport="stdio")