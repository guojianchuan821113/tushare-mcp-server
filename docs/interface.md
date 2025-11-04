1.  **Tushare 接口**: `pro.stk_factor_pro()`
    -   **MCP 工具名**: `stk_factor_pro`
    -   **描述**: 获取股票技术面因子数据（专业版技术指标）。
2.  **Tushare 接口**: `pro.moneyflow()`
    -   **MCP 工具名**: `moneyflow`
    -   **描述**: 获取个股资金流向数据。
3.  **Tushare 接口**: `pro.moneyflow_cnt_ths()`
    -   **MCP 工具名**: `moneyflow_cnt_ths`
    -   **描述**: 获取同花顺概念板块资金流向数据。
4.  **Tushare 接口**: `pro.moneyflow_ind_ths()`
    -   **MCP 工具名**: `moneyflow_ind_ths`
    -   **描述**: 获取同花顺行业板块资金流向数据。
5.  **Tushare 接口**: `pro.cyq_perf()`
    -   **MCP 工具名**: `cyq_perf`
    -   **描述**: 获取股票筹码分布数据。
6.  **Tushare 接口**: `pro.stock_basic()`
    -   **MCP 工具名**: `stock_basic`
    -   **描述**: 获取股票基本信息。
7.  **Tushare 接口**: `pro.index_classify()`
    -   **MCP 工具名**: `index_classify`
    -   **描述**: 获取行业分类信息。
8.  **Tushare 接口**: `pro.fina_indicator()`
    -   **MCP 工具名**: `fina_indicator`
    -   **描述**: 获取财务指标数据。
9.  **Tushare 接口**: `pro.stk_holdernumber()`
    -   **MCP 工具名**: `stk_holdernumber`
    -   **描述**: 获取股东人数数据。
10. **Tushare 接口**: `pro.ths_daily()`
    -   **MCP 工具名**: `ths_daily`
    -   **描述**: 获取同花顺指数日线数据。
11. **Tushare 接口**: `pro.index_weekly()`
    -   **MCP 工具名**: `index_weekly`
    -   **描述**: 获取指数周线数据。
12. **Tushare 接口**: `pro.trade_cal()`
    -   **MCP 工具名**: `trade_cal`
    -   **描述**: 获取交易日历数据。
13. **Tushare 接口**: `pro.stk_auction_o()`
    -   **MCP 工具名**: `stk_auction_o`
    -   **描述**: 获取集合竞价数据。
14. **Tushare 接口**: `pro.income()`
    -   **MCP 工具名**: `income`
    -   **描述**: 获取利润表数据。
15. **Tushare 接口**: `pro.balancesheet()`
    -   **MCP 工具名**: `balancesheet`
    -   **描述**: 获取资产负债表数据。
16. **Tushare 接口**: `pro.cashflow()`
    -   **MCP 工具名**: `cashflow`
    -   **描述**: 获取现金流量表数据。
17. **Tushare 接口**: `pro.top10_floatholders()`
    -   **MCP 工具名**: `top10_floatholders`
    -   **描述**: 获取前十大流通股东数据。
18. **Tushare 接口**: `pro.index_monthly()`
    -   **MCP 工具名**: `index_monthly`
    -   **描述**: 获取指数月线行情数据。
19. **Tushare 接口**: `pro.idx_factor_pro()`
    -   **MCP 工具名**: `idx_factor_pro`
    -   **描述**: 获取指数技术因子数据（专业版）。
20. **Tushare 接口**: `pro.moneyflow_mkt_dc()`
    -   **MCP 工具名**: `moneyflow_mkt_dc`
    -   **描述**: 获取东方财富大盘资金流向数据。
21. **Tushare 接口**: `pro.moneyflow_hsgt()`
    -   **MCP 工具名**: `moneyflow_hsgt`
    -   **描述**: 获取沪深港通资金流向数据。

---

参数支持与用法简述

- `stk_factor_pro` 支持参数：`ts_code`, `trade_date`, `start_date`, `end_date`, `fields`。示例：`stk_factor_pro(ts_code="000001.SZ", start_date="20240101", end_date="20240201")`
- `moneyflow` 支持参数：`ts_code`, `trade_date`, `start_date`, `end_date`。示例：`moneyflow(ts_code="600000.SH", start_date="20240101", end_date="20240131")`
- `moneyflow_cnt_ths` 支持参数：`date`, `concept_code`, `concept_name`。示例：`moneyflow_cnt_ths(date="20240131", concept_name="算力")`
- `moneyflow_ind_ths` 支持参数：`date`, `industry_code`, `industry_name`。示例：`moneyflow_ind_ths(date="20240131", industry_name="计算机")`
- `cyq_perf` 支持参数：`ts_code`, `trade_date`, `start_date`, `end_date`。示例：`cyq_perf(ts_code="600000.SH", start_date="20240101", end_date="20240131")`
- `stock_basic` 支持参数：`ts_code`, `name`, `exchange`, `list_status`, `market`, `is_hs`, `fields`。示例：`stock_basic(list_status="L", market="主板")`
- `index_classify` 支持参数：`level`, `industry`, `src`。示例：`index_classify(level="L2", src="SW")`
- `fina_indicator` 支持参数：`ts_code`, `ann_date`, `start_date`, `end_date`, `period`, `fields`。示例：`fina_indicator(ts_code="600000.SH", period="20171231")`
- `stk_holdernumber` 支持参数：`ts_code`, `ann_date`, `start_date`, `end_date`。示例：`stk_holdernumber(ts_code="300199.SZ", start_date="20160101", end_date="20181231")`
- `ths_daily` 支持参数：`ts_code`, `trade_date`, `start_date`, `end_date`。示例：`ths_daily(ts_code="885001.TI", start_date="20240101", end_date="20240131")`
- `index_weekly` 支持参数：`ts_code`, `start_date`, `end_date`。示例：`index_weekly(ts_code="000001.SH", start_date="20240101", end_date="20240201")`
- `index_monthly` 支持参数：`ts_code`, `trade_date`, `start_date`, `end_date`, `fields`。示例：`index_monthly(ts_code="000001.SH", start_date="20240101", end_date="20241231")`
- `idx_factor_pro` 支持参数：`ts_code`, `start_date`, `end_date`, `trade_date`, `fields`。示例：`idx_factor_pro(ts_code="000001.SH", start_date="20240101", end_date="20240131")`
- `moneyflow_mkt_dc` 支持参数：`trade_date`, `start_date`, `end_date`。示例：`moneyflow_mkt_dc(start_date="20240901", end_date="20240930")`
- `moneyflow_hsgt` 支持参数：`trade_date`, `start_date`, `end_date`。示例：`moneyflow_hsgt(start_date="20240901", end_date="20240930")`
- `trade_cal` 支持参数：`exchange`, `start_date`, `end_date`, `is_open`。示例：`trade_cal(exchange="SSE", start_date="20240101", end_date="20240131", is_open=1)`
- `stk_auction_o` 支持参数：`ts_code`, `trade_date`, `start_date`, `end_date`。示例：`stk_auction_o(ts_code="600000.SH", trade_date="20240131")`
- `income` 支持参数：`ts_code`, `ann_date`, `f_ann_date`, `start_date`, `end_date`, `period`, `report_type`, `comp_type`, `fields`。示例：`income(ts_code="600000.SH", period="20171231")`
- `balancesheet` 支持参数：`ts_code`, `ann_date`, `start_date`, `end_date`, `period`, `report_type`, `comp_type`, `fields`。示例：`balancesheet(ts_code="600000.SH", period="20171231")`
- `cashflow` 支持参数：`ts_code`, `ann_date`, `f_ann_date`, `start_date`, `end_date`, `period`, `report_type`, `comp_type`, `is_calc`, `fields`。示例：`cashflow(ts_code="600000.SH", period="20171231", is_calc=1)`
- `top10_floatholders` 支持参数：`ts_code`, `period`, `ann_date`, `start_date`, `end_date`, `fields`。示例：`top10_floatholders(ts_code="600000.SH", start_date="20170101", end_date="20171231")`

说明：所有工具返回值为 JSON 字符串（records 格式）。如接口抛出异常，将返回形如 `{"error": "..."}` 的字符串。需要在环境或 `.env` 中设置 `TUSHARE_TOKEN`。