# Tushare Pro 接口详细使用说明

本文档详细介绍了Tushare Pro提供的22个主要接口的使用方法、参数说明和限制条件，便于大模型理解和使用这些接口。

## 接口详细说明

### 1. 股票技术面因子数据 - stk_factor_pro

**Tushare 接口**: `pro.stk_factor_pro()`
**MCP 工具名**: `stk_factor_pro`
**描述**: 获取股票每日技术面因子数据，用于跟踪股票当前走势情况，数据由Tushare社区自产，覆盖全历史；输出参数_bfq表示不复权，_qfq表示前复权 _hfq表示后复权，描述中说明了因子的默认传参，如需要特殊参数或者更多因子可以联系管理员评估。

**参数说明**:
- `ts_code` (str): 股票代码（格式：000001.SZ），非必选
- `trade_date` (str): 交易日期（格式：20240101），非必选
- `start_date` (str): 开始日期（格式：20240101），非必选
- `end_date` (str): 结束日期（格式：20240131），非必选

**使用示例**:
```python
# 获取单只股票特定时间段的技术因子
pro.stk_factor_pro(ts_code="000001.SZ", start_date="20240101", end_date="20240201")

# 获取所有股票某一天的技术因子
pro.stk_factor_pro(trade_date="20240101")
```

**返回字段**:
- `ts_code`: 股票代码
- `trade_date`: 交易日期
- `open`: 开盘价
- `open_hfq`: 开盘价（后复权）
- `open_qfq`: 开盘价（前复权）
- `high`: 最高价
- `high_hfq`: 最高价（后复权）
- `high_qfq`: 最高价（前复权）
- `low`: 最低价
- `low_hfq`: 最低价（后复权）
- `low_qfq`: 最低价（前复权）
- `close`: 收盘价
- `close_hfq`: 收盘价（后复权）
- `close_qfq`: 收盘价（前复权）
- `pre_close`: 昨收价(前复权)--为daily接口的pre_close,以当时复权因子计算值跟前一日close_qfq对不上，可不用
- `change`: 涨跌额
- `pct_chg`: 涨跌幅 （未复权，如果是复权请用 通用行情接口）
- `vol`: 成交量 （手）
- `amount`: 成交额 （千元）
- `turnover_rate`: 换手率（%）
- `turnover_rate_f`: 换手率（自由流通股）
- `volume_ratio`: 量比
- `pe`: 市盈率（总市值/净利润， 亏损的PE为空）
- `pe_ttm`: 市盈率（TTM，亏损的PE为空）
- `pb`: 市净率（总市值/净资产）
- `ps`: 市销率
- `ps_ttm`: 市销率（TTM）
- `dv_ratio`: 股息率 （%）
- `dv_ttm`: 股息率（TTM）（%）
- `total_share`: 总股本 （万股）
- `float_share`: 流通股本 （万股）
- `free_share`: 自由流通股本 （万）
- `total_mv`: 总市值 （万元）
- `circ_mv`: 流通市值（万元）
- `adj_factor`: 复权因子
- `asi_bfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `asi_hfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `asi_qfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `asit_bfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `asit_hfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `asit_qfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `atr_bfq`: 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
- `atr_hfq`: 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
- `atr_qfq`: 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
- `bbi_bfq`: BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=20
- `bbi_hfq`: BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=21
- `bbi_qfq`: BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=22
- `bias1_bfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias1_hfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias1_qfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias2_bfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias2_hfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias2_qfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias3_bfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias3_hfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias3_qfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `boll_lower_bfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_lower_hfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_lower_qfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_mid_bfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_mid_hfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_mid_qfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_upper_bfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_upper_hfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_upper_qfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `brar_ar_bfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `brar_ar_hfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `brar_ar_qfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `brar_br_bfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `brar_br_hfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `brar_br_qfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `cci_bfq`: 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
- `cci_hfq`: 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
- `cci_qfq`: 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
- `cr_bfq`: CR价格动量指标-CLOSE, HIGH, LOW, N=20
- `cr_hfq`: CR价格动量指标-CLOSE, HIGH, LOW, N=20
- `cr_qfq`: CR价格动量指标-CLOSE, HIGH, LOW, N=20
- `dma_bfq`: DMA指标-CLOSE, N1=10, N2=50, M=10
- `dma_hfq`: DMA指标-CLOSE, N1=10, N2=50, M=10
- `dma_qfq`: DMA指标-CLOSE, N1=10, N2=50, M=10
- `dmi_bfq`: DMI动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `dmi_hfq`: DMI动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `dmi_qfq`: DMI动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `ema_bfq`: EMA指数移动平均-CLOSE, N=12
- `ema_hfq`: EMA指数移动平均-CLOSE, N=12
- `ema_qfq`: EMA指数移动平均-CLOSE, N=12
- `emv_bfq`: EMV简易波动指标-CLOSE, HIGH, LOW, N=14
- `emv_hfq`: EMV简易波动指标-CLOSE, HIGH, LOW, N=14
- `emv_qfq`: EMV简易波动指标-CLOSE, HIGH, LOW, N=14
- `expma_bfq`: EXPMA指数平滑移动平均-CLOSE, N=12
- `expma_hfq`: EXPMA指数平滑移动平均-CLOSE, N=12
- `expma_qfq`: EXPMA指数平滑移动平均-CLOSE, N=12
- `kdj_j_bfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_j_hfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_j_qfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_k_bfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_k_hfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_k_qfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_d_bfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_d_hfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `kdj_d_qfq`: KDJ随机指标-CLOSE, HIGH, LOW, N1=9, N2=3, M1=3
- `macd_dea_bfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_dea_hfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_dea_qfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_diff_bfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_diff_hfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_diff_qfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_macd_bfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_macd_hfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_macd_qfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `ma_bfq`: MA移动平均线-CLOSE, N=5
- `ma_hfq`: MA移动平均线-CLOSE, N=5
- `ma_qfq`: MA移动平均线-CLOSE, N=5
- `mass_bfq`: MASS重量指标-CLOSE, HIGH, LOW, N1=9, N2=25
- `mass_hfq`: MASS重量指标-CLOSE, HIGH, LOW, N1=9, N2=25
- `mass_qfq`: MASS重量指标-CLOSE, HIGH, LOW, N1=9, N2=25
- `mtm_bfq`: MTM动量指标-CLOSE, N=12
- `mtm_hfq`: MTM动量指标-CLOSE, N=12
- `mtm_qfq`: MTM动量指标-CLOSE, N=12
- `obv_bfq`: OBV能量潮指标-CLOSE, VOL
- `obv_hfq`: OBV能量潮指标-CLOSE, VOL
- `obv_qfq`: OBV能量潮指标-CLOSE, VOL
- `psl_bfq`: PSY心理线指标-CLOSE, N=12
- `psl_hfq`: PSY心理线指标-CLOSE, N=12
- `psl_qfq`: PSY心理线指标-CLOSE, N=12
- `roc_bfq`: ROC变动率指标-CLOSE, N=12
- `roc_hfq`: ROC变动率指标-CLOSE, N=12
- `roc_qfq`: ROC变动率指标-CLOSE, N=12
- `rsi_bfq`: RSI相对强弱指标-CLOSE, N=6
- `rsi_hfq`: RSI相对强弱指标-CLOSE, N=6
- `rsi_qfq`: RSI相对强弱指标-CLOSE, N=6
- `sma_bfq`: SMA简单移动平均-CLOSE, N=12
- `sma_hfq`: SMA简单移动平均-CLOSE, N=12
- `sma_qfq`: SMA简单移动平均-CLOSE, N=12
- `slowk_bfq`: 慢速随机指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `slowk_hfq`: 慢速随机指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `slowk_qfq`: 慢速随机指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `slowd_bfq`: 慢速随机指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `slowd_hfq`: 慢速随机指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `slowd_qfq`: 慢速随机指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `srsi_bfq`: SRSI慢速相对强弱指标-CLOSE, HIGH, LOW, N1=14, N2=14, M=3
- `srsi_hfq`: SRSI慢速相对强弱指标-CLOSE, HIGH, LOW, N1=14, N2=14, M=3
- `srsi_qfq`: SRSI慢速相对强弱指标-CLOSE, HIGH, LOW, N1=14, N2=14, M=3
- `trix_bfq`: TRIX三重平滑移动平均-CLOSE, N=12
- `trix_hfq`: TRIX三重平滑移动平均-CLOSE, N=12
- `trix_qfq`: TRIX三重平滑移动平均-CLOSE, N=12
- `vr_bfq`: VR成交量变异率-CLOSE, VOL, N=24
- `vr_hfq`: VR成交量变异率-CLOSE, VOL, N=24
- `vr_qfq`: VR成交量变异率-CLOSE, VOL, N=24
- `wr10_bfq`: WR威廉指标-CLOSE, HIGH, LOW, N=10
- `wr10_hfq`: WR威廉指标-CLOSE, HIGH, LOW, N=10
- `wr10_qfq`: WR威廉指标-CLOSE, HIGH, LOW, N=10
- `wr6_bfq`: WR威廉指标-CLOSE, HIGH, LOW, N=6
- `wr6_hfq`: WR威廉指标-CLOSE, HIGH, LOW, N=6
- `wr6_qfq`: WR威廉指标-CLOSE, HIGH, LOW, N=6

**限制说明**:
- 单次调取最多返回10000条数据，可以通过日期参数循环
- 积分：5000积分每分钟可以请求30次，8000积分以上每分钟500次，具体请参阅积分获取办法

- 单次最大返回3000条数据
- 建议按股票代码和日期分段获取

---

### 2. 个股资金流向数据 - moneyflow

**Tushare 接口**: `pro.moneyflow()`
**MCP 工具名**: `moneyflow`
**描述**: 获取沪深A股票资金流向数据，分析大单小单成交情况，用于判别资金动向，数据开始于2010年。

**参数说明**:
- `ts_code` (str): 股票代码（格式：600000.SH），非必选
- `trade_date` (str): 交易日期（格式：20240101），非必选
- `start_date` (str): 开始日期（格式：20240101），非必选
- `end_date` (str): 结束日期（格式：20240131），非必选

**使用示例**:
```python
# 获取单只股票特定时间段的资金流向
pro.moneyflow(ts_code="600000.SH", start_date="20240101", end_date="20240131")

# 获取所有股票某一天的资金流向
pro.moneyflow(trade_date="20240101")
```

**返回字段**:
- `ts_code`: TS代码
- `trade_date`: 交易日期
- `buy_sm_vol`: 小单买入量（手）
- `buy_sm_amount`: 小单买入金额（万元）
- `sell_sm_vol`: 小单卖出量（手）
- `sell_sm_amount`: 小单卖出金额（万元）
- `buy_md_vol`: 中单买入量（手）
- `buy_md_amount`: 中单买入金额（万元）
- `sell_md_vol`: 中单卖出量（手）
- `sell_md_amount`: 中单卖出金额（万元）
- `buy_lg_vol`: 大单买入量（手）
- `buy_lg_amount`: 大单买入金额（万元）
- `sell_lg_vol`: 大单卖出量（手）
- `sell_lg_amount`: 大单卖出金额（万元）
- `buy_elg_vol`: 特大单买入量（手）
- `buy_elg_amount`: 特大单买入金额（万元）
- `sell_elg_vol`: 特大单卖出量（手）
- `sell_elg_amount`: 特大单卖出金额（万元）
- `net_mf_vol`: 净流入量（手）
- `net_mf_amount`: 净流入额（万元）

**各类别统计规则**:
- 小单：5万以下
- 中单：5万～20万
- 大单：20万～100万
- 特大单：成交额>=100万
- 数据基于主动买卖单统计

**限制说明**:
- 单次最大提取6000行记录，总量不限制
- 积分：用户需要至少2000积分才可以调取，基础积分有流量控制，积分越多权限越大，请自行提高积分，具体请参阅积分获取办法

- 单次最大返回3000条数据
- 建议按股票代码和日期分段获取

---

### 3. 同花顺概念板块资金流向数据 - moneyflow_cnt_ths

**Tushare 接口**: `pro.moneyflow_cnt_ths()`
**MCP 工具名**: `moneyflow_cnt_ths`
**描述**: 获取同花顺概念板块每日资金流向。

**参数说明**:
- `ts_code` (str): 代码，非必选
- `trade_date` (str): 交易日期(格式：YYYYMMDD，下同)，非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取当日同花顺板块资金流向
pro.moneyflow_cnt_ths(trade_date='20250320')

# 获取特定时间段内同花顺板块资金流向
pro.moneyflow_cnt_ths(start_date='20250301', end_date='20250320')
```

**返回字段**:
- `trade_date`: 交易日期
- `ts_code`: 板块代码
- `name`: 板块名称
- `lead_stock`: 领涨股票名称
- `close_price`: 最新价
- `pct_change`: 行业涨跌幅
- `industry_index`: 板块指数
- `company_num`: 公司数量
- `pct_change_stock`: 领涨股涨跌幅
- `net_buy_amount`: 流入资金(亿元)
- `net_sell_amount`: 流出资金(亿元)
- `net_amount`: 净额(亿元)

**限制说明**:
- 单次最大可调取5000条数据，可以根据日期和代码循环提取全部数据
- 积分：5000积分可以调取，具体请参阅积分获取办法

- 单次最大返回500条数据

---

### 4. 同花顺行业资金流向 - moneyflow_ind_ths

**Tushare 接口**: `pro.moneyflow_ind_ths()`
**MCP 工具名**: `moneyflow_ind_ths`
**描述**: 获取同花顺行业资金流向，每日盘后更新。

**参数说明**:
- `ts_code` (str): 代码，非必选
- `trade_date` (str): 交易日期(YYYYMMDD格式，下同)，非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取当日所有同花顺行业资金流向
pro.moneyflow_ind_ths(trade_date='20240927')

# 获取特定时间段的行业资金流向
pro.moneyflow_ind_ths(start_date='20240901', end_date='20240930')

# 获取特定行业的资金流向
pro.moneyflow_ind_ths(ts_code='881267.TI', trade_date='20240927')
```

**返回字段**:
- `trade_date`: 交易日期
- `ts_code`: 板块代码
- `industry`: 板块名称
- `lead_stock`: 领涨股票名称
- `close`: 收盘指数
- `pct_change`: 指数涨跌幅
- `company_num`: 公司数量
- `pct_change_stock`: 领涨股涨跌幅
- `close_price`: 领涨股最新价
- `net_buy_amount`: 流入资金(亿元)
- `net_sell_amount`: 流出资金(亿元)
- `net_amount`: 净额(亿元)

**限制说明**:
- 单次最大可调取5000条数据，可以根据日期和代码循环提取全部数据
- 需要5000积分可以调取，具体请参阅积分获取办法

---

### 5. 每日筹码及胜率 - cyq_perf

**Tushare 接口**: `pro.cyq_perf()`
**MCP 工具名**: `cyq_perf`
**描述**: 获取A股每日筹码平均成本和胜率情况，每天17~18点左右更新，数据从2018年开始来源：Tushare社区。

**参数说明**:
- `ts_code` (str): 股票代码，非必选
- `trade_date` (str): 交易日期（YYYYMMDD），非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取单只股票特定时间段的筹码及胜率
pro.cyq_perf(ts_code='600000.SH', start_date='20220101', end_date='20220429')

# 获取单只股票特定日期的筹码及胜率
pro.cyq_perf(ts_code='600000.SH', trade_date='20220429')
```

**返回字段**:
- `ts_code`: 股票代码
- `trade_date`: 交易日期
- `his_low`: 历史最低价
- `his_high`: 历史最高价
- `cost_5pct`: 5分位成本
- `cost_15pct`: 15分位成本
- `cost_50pct`: 50分位成本
- `cost_85pct`: 85分位成本
- `cost_95pct`: 95分位成本
- `weight_avg`: 加权平均成本
- `winner_rate`: 胜率

**限制说明**:
- 单次最大5000条，可以分页或者循环提取
- 120积分可以试用(查看数据)，5000积分每天20000次，10000积分每天200000次，15000积分每天不限总量

---

### 6. 股票基本信息 - stock_basic

**Tushare 接口**: `pro.stock_basic()`
**MCP 工具名**: `stock_basic`
**描述**: 获取基础信息数据，包括股票代码、名称、上市日期、退市日期等权限：2000积分起。此接口是基础信息，调取一次就可以拉取完，建议保存倒本地存储后使用。

**参数说明**:
- `ts_code` (str): TS股票代码，非必选
- `name` (str): 名称，非必选
- `market` (str): 市场类别 （主板/创业板/科创板/CDR/北交所），非必选
- `list_status` (str): 上市状态 L上市 D退市 P暂停上市，默认是L，非必选
- `exchange` (str): 交易所 SSE上交所 SZSE深交所 BSE北交所，非必选
- `is_hs` (str): 是否沪深港通标的，N否 H沪股通 S深股通，非必选

**使用示例**:
```python
# 查询当前所有正常上市交易的股票列表
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# 或者：
# 查询当前所有正常上市交易的股票列表
data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
```

**返回字段**:
- `ts_code`: TS代码
- `symbol`: 股票代码
- `name`: 股票名称
- `area`: 地域
- `industry`: 所属行业
- `fullname`: 股票全称
- `enname`: 英文全称
- `cnspell`: 拼音缩写
- `market`: 市场类型（主板/创业板/科创板/CDR）
- `exchange`: 交易所代码
- `curr_type`: 交易货币
- `list_status`: 上市状态 L上市 D退市 P暂停上市
- `list_date`: 上市日期
- `delist_date`: 退市日期
- `is_hs`: 是否沪深港通标的，N否 H沪股通 S深股通
- `act_name`: 实控人名称
- `act_ent_type`: 实控人企业性质

**限制说明**:
- 需要2000积分起
- 说明：旧版上的PE/PB/股本等字段，请在行情接口"每日指标"中获取

---

### 7. 行业分类信息 - index_classify
 

**Tushare 接口**: `pro.index_classify()`
**MCP 工具名**: `index_classify`
**描述**: 获取申万行业分类，可以获取申万2014年版本（28个一级分类，104个二级分类，227个三级分类）和2021年本版（31个一级分类，134个二级分类，346个三级分类）列表信息。

**参数说明**:
- `level` (str): 行业级别（L1/L2/L3），非必选
- `src` (str): 来源（SW申万），非必选

**使用示例**:
```python
# 获取申万一级行业分类
pro.index_classify(level="L1", src="SW")

# 获取申万二级行业分类
pro.index_classify(level="L2", src="SW")
```

**返回字段**:
- `industry_code`: 行业代码
- `index_code`: 指数代码
- `industry_name`: 一级行业
- `industry_name1`: 二级行业
- `industry_name2`: 三级行业
- `index_type`: 指数类别
- `is_pub`: 是否发布
- `reason`: 变动原因
- `stock_num`: 成分股数

**限制说明**:
- 用户需2000积分可以调取，具体请参阅积分获取办法
- 注：指数成分股小于5条该指数行情不发布

**使用注意事项**:
- 当同时指定 `level="L2"` 和 `src="SW"` 参数时，接口可能返回空数据
- 建议使用 `index_classify(level="L2")` 而不是 `index_classify(level="L2", src="SW")` 来获取申万二级行业分类信息
- 不指定 `src` 参数时，系统默认使用 `SW2014` 作为数据源

---

### 8. 申万行业成分构成 - index_member_all

**Tushare 接口**: `pro.index_member_all()`
**MCP 工具名**: `index_member_all`
**描述**: 按三级分类提取申万行业成分，可提供某个分类的所有成分，也可按股票代码提取所属分类，参数灵活限量：单次最大2000行，总量不限制权限：用户需2000积分可调取，积分获取方法请参阅积分获取办法。

**参数说明**:
- `l1_code` (str): 一级行业代码，非必选
- `l2_code` (str): 二级行业代码，非必选
- `l3_code` (str): 三级行业代码，非必选
- `ts_code` (str): 股票代码，非必选
- `is_new` (str): 是否最新（默认为"Y是"），非必选

**使用示例**:
```python
# 获取黄金分类的成份股
pro.index_member_all(l3_code='850531.SI')

# 获取000001.SZ所属行业
pro.index_member_all(ts_code='000001.SZ')
```

**返回字段**:
- `l1_code`: 一级行业代码
- `l1_name`: 一级行业名称
- `l2_code`: 二级行业代码
- `l2_name`: 二级行业名称
- `l3_code`: 三级行业代码
- `l3_name`: 三级行业名称
- `ts_code`: 成分股票代码
- `name`: 成分股票名称
- `in_date`: 纳入日期
- `out_date`: 剔除日期
- `is_new`: 是否最新Y是N否

**限制说明**:
- 单次最大2000行，总量不限制
- 用户需2000积分可调取，积分获取方法请参阅积分获取办法

---

### 9. 财务指标数据 - fina_indicator

**Tushare 接口**: `pro.fina_indicator()`
**MCP 工具名**: `fina_indicator`
**描述**: 获取上市公司财务指标数据，为避免服务器压力，现阶段每次请求最多返回100条记录，可通过设置日期多次请求获取更多数据。

**参数说明**:
- `ts_code` (str): TS股票代码,e.g. 600001.SH/000001.SZ，必选
- `ann_date` (str): 公告日期，非必选
- `start_date` (str): 报告期开始日期，非必选
- `end_date` (str): 报告期结束日期，非必选
- `period` (str): 报告期(每个季度最后一天的日期,比如20171231表示年报)，非必选

**使用示例**:
```python
# 获取单只股票特定报告期的财务指标
pro.fina_indicator(ts_code="600000.SH", period="20231231")

# 获取单只股票多个报告期的财务指标
pro.fina_indicator(ts_code="600000.SH", start_date="20230101", end_date="20231231")
```

**返回字段**:
- `ts_code`: TS代码
- `ann_date`: 公告日期
- `end_date`: 报告期
- `eps`: 基本每股收益
- `dt_eps`: 稀释每股收益
- `total_revenue_ps`: 每股营业总收入
- `revenue_ps`: 每股营业收入
- `capital_rese_ps`: 每股资本公积
- `surplus_rese_ps`: 每股盈余公积
- `undist_profit_ps`: 每股未分配利润
- `extra_item`: 非经常性损益
- `profit_dedt`: 扣除非经常性损益后的净利润（扣非净利润）
- `gross_margin`: 毛利
- `current_ratio`: 流动比率
- `quick_ratio`: 速动比率
- `cash_ratio`: 保守速动比率
- `invturn_days`: 存货周转天数
- `arturn_days`: 应收账款周转天数
- `inv_turn`: 存货周转率
- `ar_turn`: 应收账款周转率
- `ca_turn`: 流动资产周转率
- `fa_turn`: 固定资产周转率
- `assets_turn`: 总资产周转率
- `op_income`: 经营活动净收益
- `valuechange_income`: 价值变动净收益
- `interst_income`: 利息费用
- `daa`: 折旧与摊销
- `ebit`: 息税前利润
- `ebitda`: 息税折旧摊销前利润
- `fcff`: 企业自由现金流量
- `fcfe`: 股权自由现金流量
- `current_exint`: 无息流动负债
- `noncurrent_exint`: 无息非流动负债
- `interestdebt`: 带息债务
- `netdebt`: 净债务
- `tangible_asset`: 有形资产
- `working_capital`: 营运资金
- `networking_capital`: 营运流动资本
- `invest_capital`: 全部投入资本
- `retained_earnings`: 留存收益
- `diluted2_eps`: 期末摊薄每股收益
- `bps`: 每股净资产
- `ocfps`: 每股经营活动产生的现金流量净额
- `retainedps`: 每股留存收益
- `cfps`: 每股现金流量净额
- `ebit_ps`: 每股息税前利润
- `fcff_ps`: 每股企业自由现金流量
- `fcfe_ps`: 每股股东自由现金流量
- `netprofit_margin`: 销售净利率
- `grossprofit_margin`: 销售毛利率
- `cogs_of_sales`: 销售成本率
- `expense_of_sales`: 销售期间费用率
- `profit_to_gr`: 净利润/营业总收入
- `saleexp_to_gr`: 销售费用/营业总收入
- `adminexp_of_gr`: 管理费用/营业总收入
- `finaexp_of_gr`: 财务费用/营业总收入
- `impai_ttm`: 资产减值损失/营业总收入
- `gc_of_gr`: 营业总成本/营业总收入
- `op_of_gr`: 营业利润/营业总收入
- `ebit_of_gr`: 息税前利润/营业总收入
- `roe`: 净资产收益率
- `roe_waa`: 加权平均净资产收益率
- `roe_dt`: 净资产收益率(扣除非经常损益)
- `roa`: 总资产报酬率
- `npta`: 总资产净利润
- `roic`: 投入资本回报率
- `roe_yearly`: 年化净资产收益率
- `roa2_yearly`: 年化总资产报酬率
- `roe_avg`: 平均净资产收益率(增发条件)
- `opincome_of_ebt`: 经营活动净收益/利润总额
- `investincome_of_ebt`: 价值变动净收益/利润总额
- `n_op_profit_of_ebt`: 营业外收支净额/利润总额
- `tax_to_ebt`: 所得税/利润总额
- `dtprofit_to_profit`: 扣除非经常损益后的净利润/净利润
- `salescash_to_or`: 销售商品提供劳务收到的现金/营业收入
- `ocf_to_or`: 经营活动产生的现金流量净额/营业收入
- `ocf_to_opincome`: 经营活动产生的现金流量净额/经营活动净收益
- `capitalized_to_da`: 资本支出/折旧和摊销
- `debt_to_assets`: 资产负债率
- `assets_to_eqt`: 权益乘数
- `dp_assets_to_eqt`: 权益乘数(杜邦分析)
- `ca_to_assets`: 流动资产/总资产
- `nca_to_assets`: 非流动资产/总资产
- `tbassets_to_totalassets`: 有形资产/总资产
- `int_to_talcap`: 带息债务/全部投入资本
- `eqt_to_talcapital`: 归属于母公司的股东权益/全部投入资本
- `currentdebt_to_debt`: 流动负债/负债合计
- `longdeb_to_debt`: 非流动负债/负债合计
- `ocf_to_shortdebt`: 经营活动产生的现金流量净额/流动负债
- `debt_to_eqt`: 产权比率

**限制说明**:
- 用户需要至少2000积分才可以调取，具体请参阅积分获取办法
- 现阶段每次请求最多返回100条记录，可通过设置日期多次请求获取更多数据
- 提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用fina_indicator_vip接口（参数一致），需积攒5000积分

---

### 10. 股东人数数据 - stk_holdernumber

**Tushare 接口**: `pro.stk_holdernumber()`
**MCP 工具名**: `stk_holdernumber`
**描述**: 获取上市公司股东户数数据，数据不定期公布。

**参数说明**:
- `ts_code` (str): TS股票代码，非必选
- `ann_date` (str): 公告日期，非必选
- `enddate` (str): 截止日期，非必选
- `start_date` (str): 公告开始日期，非必选
- `end_date` (str): 公告结束日期，非必选

**使用示例**:
```python
# 获取单只股票特定时间段的股东人数
pro.stk_holdernumber(ts_code="300199.SZ", start_date="20160101", end_date="20181231")

# 获取所有股票某一天公布的股东人数
pro.stk_holdernumber(ann_date="20240101")
```

**返回字段**:
- `ts_code`: TS股票代码
- `ann_date`: 公告日期
- `end_date`: 截止日期
- `holder_num`: 股东户数

**限制说明**:
- 单次最大3000,总量不限制
- 600积分可调取，基础积分每分钟调取100次，5000积分以上频次相对较高

---

### 11. 同花顺板块指数行情 - ths_daily

**Tushare 接口**: `pro.ths_daily()`
**MCP 工具名**: `ths_daily`
**描述**: 获取同花顺板块指数行情。注：数据版权归属同花顺，如做商业用途，请主动联系同花顺，如需帮助请联系微信：waditu_a

**参数说明**:
- `ts_code` (str): 指数代码，非必选
- `trade_date` (str): 交易日期（YYYYMMDD格式，下同），非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取特定指数特定时间段的日线数据
pro.ths_daily(ts_code="865001.TI", start_date="20200101", end_date="20210101", fields='ts_code,trade_date,open,close,high,low,pct_change')

# 获取所有指数某一天的日线数据
pro.ths_daily(trade_date="20240101")
```

**返回字段**:
- `ts_code`: TS指数代码
- `trade_date`: 交易日
- `close`: 收盘点位
- `open`: 开盘点位
- `high`: 最高点位
- `low`: 最低点位
- `pre_close`: 昨日收盘点
- `avg_price`: 平均价
- `change`: 涨跌点位
- `pct_change`: 涨跌幅
- `vol`: 成交量
- `turnover_rate`: 换手率
- `total_mv`: 总市值
- `float_mv`: 流通市值

**限制说明**:
- 单次最大3000行数据（需6000积分），可根据指数代码、日期参数循环提取

---

### 12. 指数周线行情 - index_weekly

**Tushare 接口**: `pro.index_weekly()`
**MCP 工具名**: `index_weekly`
**描述**: 获取指数周线行情限量：单次最大1000行记录，可分批获取，总量不限制积分：用户需要至少600积分才可以调取，积分越多频次越高，具体请参阅积分获取办法

**参数说明**:
- `ts_code` (str): TS代码，非必选
- `trade_date` (str): 交易日期，非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取特定指数特定时间段的周线数据
pro.index_weekly(ts_code='000001.SH', start_date='20180101', end_date='20190329', fields='ts_code,trade_date,open,high,low,close,vol,amount')

# 获取所有指数某一周的周线数据
pro.index_weekly(trade_date='20190329', fields='ts_code,trade_date,open,high,low,close,vol,amount')
```

**返回字段**:
- `ts_code`: TS指数代码
- `trade_date`: 交易日
- `close`: 收盘点位
- `open`: 开盘点位
- `high`: 最高点位
- `low`: 最低点位
- `pre_close`: 昨日收盘点
- `change`: 涨跌点位
- `pct_chg`: 涨跌幅
- `vol`: 成交量（手）
- `amount`: 成交额（千元）

**限制说明**:
- 单次最大1000行记录，可分批获取，总量不限制
- 积分：用户需要至少600积分才可以调取，积分越多频次越高

---

### 13. 交易日历 - trade_cal

**Tushare 接口**: `pro.trade_cal()`
**MCP 工具名**: `trade_cal`
**描述**: 获取各大交易所交易日历数据,默认提取的是上交所积分：需2000积分

**参数说明**:
- `exchange` (str): 交易所 SSE上交所,SZSE深交所,CFFEX 中金所,SHFE 上期所,CZCE 郑商所,DCE 大商所,INE 上能源，非必选
- `start_date` (str): 开始日期 （格式：YYYYMMDD 下同），非必选
- `end_date` (str): 结束日期，非必选
- `is_open` (str): 是否交易 '0'休市 '1'交易，非必选

**使用示例**:
```python
# 获取特定交易所特定时间段的交易日历
pro.trade_cal(exchange='', start_date='20180101', end_date='20181231')

# 或者使用query方式获取
pro.query('trade_cal', start_date='20180101', end_date='20181231')
```

**返回字段**:
- `exchange`: 交易所 SSE上交所 SZSE深交所
- `cal_date`: 日历日期
- `is_open`: 是否交易 0休市 1交易
- `pretrade_date`: 上一个交易日

**限制说明**:
- 积分：需2000积分

---

### 14. 股票开盘集合竞价数据 - stk_auction_o

**Tushare 接口**: `pro.stk_auction_o()`
**MCP 工具名**: `stk_auction_o`
**描述**: 股票开盘9:30集合竞价数据，每天盘后更新限量：单次请求最大返回10000行数据，可根据日期循环权限：开通了股票分钟权限后可获得本接口权限，具体参考权限说明

**参数说明**:
- `ts_code` (str): 股票代码，非必选
- `trade_date` (str): 交易日期(YYYYMMDD)，非必选
- `start_date` (str): 开始日期(YYYYMMDD)，非必选
- `end_date` (str): 结束日期(YYYYMMDD)，非必选

**使用示例**:
```python
# 获取特定日期的集合竞价数据
pro.stk_auction_o(trade_date='20241122')

# 获取单只股票特定时间段的集合竞价数据
pro.stk_auction_o(ts_code="600000.SH", start_date="20240101", end_date="20240131")
```

**返回字段**:
- `ts_code`: 股票代码
- `trade_date`: 交易日期
- `close`: 开盘集合竞价收盘价
- `open`: 开盘集合竞价开盘价
- `high`: 开盘集合竞价最高价
- `low`: 开盘集合竞价最低价
- `vol`: 开盘集合竞价成交量
- `amount`: 开盘集合竞价成交额
- `vwap`: 开盘集合竞价均价

**限制说明**:
- 单次请求最大返回10000行数据，可根据日期循环
- 权限：开通了股票分钟权限后可获得本接口权限

---

### 15. 利润表 - income

**Tushare 接口**: `pro.income()`
**MCP 工具名**: `income`
**描述**: 获取上市公司财务利润表数据，单次最大3000条，建议分批取。权限：用户需有2000积分才可调取，单次积分消耗约50积分

**参数说明**:
- `ts_code` (str): TS代码，非必选
- `ann_date` (str): 公告日期，非必选
- `f_ann_date` (str): 实际公告日期，非必选
- `start_date` (str): 报告期开始日期，非必选
- `end_date` (str): 报告期结束日期，非必选
- `period` (str): 报告期，非必选
- `report_type` (str): 报告类型：1合并报表，2单季合并，3调整单季合并表，4调整合并报表，5调整前合并报表，6母公司报表，7单季母公司，8调整单季母公司，9调整母公司报表，10调整前母公司报表，非必选
- `comp_type` (str): 公司类型：1一般工商业，2银行，3保险，4证券，非必选

**使用示例**:
```python
# 获取特定股票的利润表数据
pro.income(ts_code='600519.SH', start_date='20190101', end_date='20231231')

# 获取所有股票特定报告期的利润表数据
pro.income(period='20231231', report_type=1)
```

**返回字段**:
- `ts_code`: TS代码
- `ann_date`: 公告日期
- `f_ann_date`: 实际公告日期
- `end_date`: 报告期
- `report_type`: 报告类型
- `comp_type`: 公司类型
- `basic_eps`: 基本每股收益
- `dt_eps`: 稀释每股收益
- `total_revenue`: 营业总收入
- `revenue`: 营业收入
- `int_income`: 利息收入
- `prem_earned`: 已赚保费
- `comm_income`: 手续费及佣金收入
- `n_commis_income`: 手续费及佣金净收入
- `n_oth_income`: 其他经营净收益
- `n_oth_b_income`: 加:其他业务收入
- `oth_income`: 其他业务收入
- `n_oth_r_income`: 减:其他业务成本
- `oth_r_income`: 其他业务成本
- `total_cogs`: 营业总成本
- `oper_cost`: 营业成本
- `int_exp`: 利息支出
- `comm_exp`: 手续费及佣金支出
- `biz_tax_surchg`: 营业税金及附加
- `sell_exp`: 销售费用
- `admin_exp`: 管理费用
- `fin_exp`: 财务费用
- `assets_impair_loss`: 资产减值损失
- `cred_impair_loss`: 信用减值损失
- `prem_refund`: 退保金
- `comp_payout`: 赔付支出净额
- `reser_insur_liab`: 提取保险合同准备金净额
- `div_payt`: 保单红利支出
- `reins_exp`: 分保费用
- `oper_exp`: 营业支出
- `comp_insur_payout`: 摊回保险合同准备金
- `oper_profit`: 营业利润
- `total_profit`: 利润总额
- `n_income`: 净利润
- `n_income_attr_p`: 归属于母公司所有者的净利润
- `minority_gain`: 少数股东损益
- `oth_compr_income`: 其他综合收益
- `t_compr_income`: 综合收益总额
- `compr_inc_attr_p`: 归属于母公司所有者的综合收益总额
- `compr_inc_attr_m_s`: 归属于少数股东的综合收益总额
- `ebit`: 息税前利润
- `ebitda`: 息税折旧摊销前利润
- `insurance_exp`: 保险业务支出
- `undist_profit`: 未分配利润
- `distable_profit`: 可分配利润

**限制说明**:
- 单次最大返回3000条数据，建议分批取
- 权限：用户需有2000积分才可调取，单次积分消耗约50积分

---

### 16. 资产负债表 - balancesheet

**Tushare 接口**: `pro.balancesheet()`
**MCP 工具名**: `balancesheet`
**描述**: 获取上市公司资产负债表数据积分：用户需要至少2000积分才可以调取，具体请参阅积分获取办法提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用balancesheet_vip接口（参数一致），需积攒5000积分。

**参数说明**:
- `ts_code` (str): 股票代码，必选
- `ann_date` (str): 公告日期(YYYYMMDD格式，下同)，非必选
- `start_date` (str): 公告开始日期，非必选
- `end_date` (str): 公告结束日期，非必选
- `period` (str): 报告期(每个季度最后一天的日期，比如20171231表示年报，20170630半年报，20170930三季报)，非必选
- `report_type` (str): 报告类型：见下方详细说明，非必选
- `comp_type` (str): 公司类型：1一般工商业 2银行 3保险 4证券，非必选

**使用示例**:
```python
# 获取单只股票特定报告期的资产负债表
pro.balancesheet(ts_code="600000.SH", period="20231231")

# 获取单只股票多个报告期的资产负债表
pro.balancesheet(ts_code="600000.SH", start_date="20230101", end_date="20231231")
```

**返回字段**:
- `ts_code`: TS股票代码
- `ann_date`: 公告日期
- `f_ann_date`: 实际公告日期
- `end_date`: 报告期
- `report_type`: 报表类型
- `comp_type`: 公司类型(1一般工商业2银行3保险4证券)
- `end_type`: 报告期类型
- `total_share`: 期末总股本
- `cap_rese`: 资本公积金
- `undistr_porfit`: 未分配利润
- `surplus_rese`: 盈余公积金
- `special_rese`: 专项储备
- `money_cap`: 货币资金
- `trad_asset`: 交易性金融资产
- `notes_receiv`: 应收票据
- `accounts_receiv`: 应收账款
- `oth_receiv`: 其他应收款
- `prepayment`: 预付款项
- `div_receiv`: 应收股利
- `int_receiv`: 应收利息
- `inventories`: 存货
- `amor_exp`: 待摊费用
- `nca_within_1y`: 一年内到期的非流动资产
- `sett_rsrv`: 结算备付金
- `loanto_oth_bank_fi`: 拆出资金
- `premium_receiv`: 应收保费
- `reinsur_receiv`: 应收分保账款
- `reinsur_res_receiv`: 应收分保合同准备金
- `pur_resale_fa`: 买入返售金融资产
- `oth_cur_assets`: 其他流动资产
- `total_cur_assets`: 流动资产合计
- `fa_avail_for_sale`: 可供出售金融资产
- `htm_invest`: 持有至到期投资
- `lt_eqt_invest`: 长期股权投资
- `invest_real_estate`: 投资性房地产
- `time_deposits`: 定期存款
- `oth_assets`: 其他资产
- `lt_rec`: 长期应收款
- `fix_assets`: 固定资产
- `cip`: 在建工程
- `const_materials`: 工程物资
- `fixed_assets_disp`: 固定资产清理
- `produc_bio_assets`: 生产性生物资产
- `oil_and_gas_assets`: 油气资产
- `intan_assets`: 无形资产
- `r_and_d`: 研发支出
- `goodwill`: 商誉
- `lt_amor_exp`: 长期待摊费用
- `defer_tax_assets`: 递延所得税资产
- `decr_in_disbur`: 发放贷款及垫款
- `oth_nca`: 其他非流动资产
- `total_nca`: 非流动资产合计
- `cash_reser_cb`: 现金及存放中央银行款项
- `depos_in_oth_bfi`: 存放同业和其它金融机构款项
- `prec_metals`: 贵金属
- `deriv_assets`: 衍生金融资产
- `rr_reins_une_prem`: 应收分保未到期责任准备金
- `rr_reins_outstd_cla`: 应收分保未决赔款准备金
- `rr_reins_lins_liab`: 应收分保寿险责任准备金
- `rr_reins_lthins_liab`: 应收分保长期健康险责任准备金
- `refund_depos`: 存出保证金
- `ph_pledge_loans`: 保户质押贷款
- `refund_cap_depos`: 存出资本保证金
- `indep_acct_assets`: 独立账户资产
- `client_depos`: 其中：客户资金存款
- `client_prov`: 其中：客户备付金
- `transac_seat_fee`: 其中:交易席位费
- `invest_as_receiv`: 应收款项类投资
- `total_assets`: 资产总计
- `lt_borr`: 长期借款
- `st_borr`: 短期借款
- `cb_borr`: 向中央银行借款
- `depos_ib_deposits`: 吸收存款及同业存放
- `loan_oth_bank`: 拆入资金
- `trading_fl`: 交易性金融负债
- `notes_payable`: 应付票据
- `acct_payable`: 应付账款
- `adv_receipts`: 预收款项
- `sold_for_repur_fa`: 卖出回购金融资产款
- `comm_payable`: 应付手续费及佣金
- `payroll_payable`: 应付职工薪酬
- `taxes_payable`: 应交税费
- `int_payable`: 应付利息
- `div_payable`: 应付股利
- `oth_payable`: 其他应付款
- `acc_exp`: 预提费用
- `deferred_inc`: 递延收益
- `st_bonds_payable`: 应付短期债券
- `payable_to_reinsurer`: 应付分保账款
- `rsrv_insur_cont`: 保险合同准备金
- `acting_trading_sec`: 代理买卖证券款
- `acting_uw_sec`: 代理承销证券款
- `non_cur_liab_due_1y`: 一年内到期的非流动负债
- `oth_cur_liab`: 其他流动负债
- `total_cur_liab`: 流动负债合计
- `bond_payable`: 应付债券
- `lt_payable`: 长期应付款
- `specific_payables`: 专项应付款
- `estimated_liab`: 预计

**限制说明**:
- 用户需要至少2000积分才可以调取
- 当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用balancesheet_vip接口（参数一致），需积攒5000积分

---

### 17. 现金流量表 - cashflow

**Tushare 接口**: `pro.cashflow()`
**MCP 工具名**: `cashflow`
**描述**: 获取上市公司现金流量表数据积分：用户需要至少2000积分才可以调取，具体请参阅积分获取办法提示：当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用cashflow_vip接口（参数一致），需积攒5000积分。

**参数说明**:
- `ts_code` (str): 股票代码，必选
- `ann_date` (str): 公告日期（YYYYMMDD格式，下同），非必选
- `f_ann_date` (str): 实际公告日期，非必选
- `start_date` (str): 公告开始日期，非必选
- `end_date` (str): 公告结束日期，非必选
- `period` (str): 报告期(每个季度最后一天的日期，比如20171231表示年报，20170630半年报，20170930三季报)，非必选
- `report_type` (str): 报告类型：见下方详细说明，非必选
- `comp_type` (str): 公司类型：1一般工商业 2银行 3保险 4证券，非必选
- `is_calc` (int): 是否计算报表，非必选

**使用示例**:
```python
# 获取单只股票特定报告期的现金流量表
pro.cashflow(ts_code="600000.SH", period="20231231", is_calc=1)

# 获取单只股票多个报告期的现金流量表
pro.cashflow(ts_code="600000.SH", start_date="20230101", end_date="20231231")
```

**返回字段**:
- `ts_code`: TS股票代码
- `ann_date`: 公告日期
- `f_ann_date`: 实际公告日期
- `end_date`: 报告期
- `comp_type`: 公司类型(1一般工商业2银行3保险4证券)
- `report_type`: 报表类型
- `end_type`: 报告期类型
- `net_profit`: 净利润
- `finan_exp`: 财务费用
- `c_fr_sale_sg`: 销售商品、提供劳务收到的现金
- `recp_tax_rends`: 收到的税费返还
- `n_depos_incr_fi`: 客户存款和同业存放款项净增加额
- `n_incr_loans_cb`: 向中央银行借款净增加额
- `n_inc_borr_oth_fi`: 向其他金融机构拆入资金净增加额
- `prem_fr_orig_contr`: 收到原保险合同保费取得的现金
- `n_incr_insured_dep`: 保户储金净增加额
- `n_reinsur_prem`: 收到再保业务现金净额
- `n_incr_disp_tfa`: 处置交易性金融资产净增加额
- `ifc_cash_incr`: 收取利息和手续费净增加额
- `n_incr_disp_faas`: 处置可供出售金融资产净增加额
- `n_incr_loans_oth_bank`: 拆入资金净增加额
- `n_cap_incr_repur`: 回购业务资金净增加额
- `c_fr_oth_operate_a`: 收到其他与经营活动有关的现金
- `c_inf_fr_operate_a`: 经营活动现金流入小计
- `c_paid_goods_s`: 购买商品、接受劳务支付的现金
- `c_paid_to_for_empl`: 支付给职工以及为职工支付的现金
- `c_paid_for_taxes`: 支付的各项税费
- `n_incr_clt_loan_adv`: 客户贷款及垫款净增加额
- `n_incr_dep_cbob`: 存放央行和同业款项净增加额
- `c_pay_claims_orig_inco`: 支付原保险合同赔付款项的现金
- `pay_handling_chrg`: 支付手续费的现金
- `pay_comm_insur_plcy`: 支付保单红利的现金
- `oth_cash_pay_oper_act`: 支付其他与经营活动有关的现金
- `st_cash_out_act`: 经营活动现金流出小计
- `n_cashflow_act`: 经营活动产生的现金流量净额
- `oth_recp_ral_inv_act`: 收到其他与投资活动有关的现金
- `c_disp_withdrwl_invest`: 收回投资收到的现金
- `c_recp_return_invest`: 取得投资收益收到的现金
- `n_recp_disp_fiolta`: 处置固定资产、无形资产和其他长期资产收回的现金净额
- `n_recp_disp_sobu`: 处置子公司及其他营业单位收到的现金净额
- `stot_inflows_inv_act`: 投资活动现金流入小计
- `c_pay_acq_const_fiolta`: 购建固定资产、无形资产和其他长期资产支付的现金
- `c_paid_invest`: 投资支付的现金
- `n_disp_subs_oth_biz`: 取得子公司及其他营业单位支付的现金净额
- `oth_pay_ral_inv_act`: 支付其他与投资活动有关的现金
- `n_incr_pledge_loan`: 质押贷款净增加额
- `stot_out_inv_act`: 投资活动现金流出小计
- `n_cashflow_inv_act`: 投资活动产生的现金流量净额
- `c_recp_borrow`: 取得借款收到的现金
- `proc_issue_bonds`: 发行债券收到的现金
- `oth_cash_recp_ral_fnc_act`: 收到其他与筹资活动有关的现金
- `stot_cash_in_fnc_act`: 筹资活动现金流入小计
- `free_cashflow`: 企业自由现金流量
- `c_prepay_amt_borr`: 偿还债务支付的现金
- `c_pay_dist_dpcp_int_exp`: 分配股利、利润或偿付利息支付的现金
- `incl_dvd_profit_paid_sc_ms`: 其中:子公司支付给少数股东的股利、利润
- `oth_cashpay_ral_fnc_act`: 支付其他与筹资活动有关的现金
- `stot_cashout_fnc_act`: 筹资活动现金流出小计
- `n_cash_flows_fnc_act`: 筹资活动产生的现金流量净额
- `eff_fx_flu_cash`: 汇率变动对现金的影响
- `n_incr_cash_cash_equ`: 现金及现金等价物净增加额
- `c_cash_equ_beg_period`: 期初现金及现金等价物余额
- `c_cash_equ_end_period`: 期末现金及现金等价物余额
- `c_recp_cap_contrib`: 吸收投资收到的现金
- `incl_cash_rec_saims`: 其中:子公司吸收少数股东投资收到的现金
- `uncon_invest_loss`: 未确认投资损

**限制说明**:
- 用户需要至少2000积分才可以调取
- 当前接口只能按单只股票获取其历史数据，如果需要获取某一季度全部上市公司数据，请使用cashflow_vip接口（参数一致），需积攒5000积分

---

### 17. 十大流通股东 - top10_floatholders

**Tushare 接口**: `pro.top10_floatholders()`
**MCP 工具名**: `top10_floatholders`
**描述**: 获取上市公司十大流通股东数据积分：用户需要至少2000积分才可以调取，具体请参阅积分获取办法

**参数说明**:
- `ts_code` (str): TS代码，必选
- `period` (str): 报告期(每季度最后一天，如20181231、20190331)，必选
- `ann_date` (str): 公告日期(YYYYMMDD格式)，非必选
- `start_date` (str): 公告开始日期(YYYYMMDD格式)，非必选
- `end_date` (str): 公告结束日期(YYYYMMDD格式)，非必选

**使用示例**:
```python
# 获取单只股票特定报告期的十大流通股东
pro.top10_floatholders(ts_code="600000.SH", period="20231231")

# 获取单只股票多个报告期的十大流通股东
pro.top10_floatholders(ts_code="600000.SH", start_date="20230101", end_date="20231231")
```

**返回字段**:
- `ts_code`: TS代码
- `ann_date`: 公告日期
- `end_date`: 报告期
- `name`: 股东名称
- `hold_amount`: 持有数量(股)
- `hold_ratio`: 持有比例(%)

**限制说明**:
- 用户需要至少2000积分才可以调取，具体请参阅积分获取办法

---

### 18. 指数月线行情 - index_monthly

**Tushare 接口**: `pro.index_monthly()`
**MCP 工具名**: `index_monthly`
**描述**: 获取指数月线行情数据

**参数说明**:
- `ts_code` (str): 指数代码(支持主流指数代码，如000001.SH等)，非必选
- `trade_date` (str): 交易日期(YYYYMMDD格式)，非必选
- `start_date` (str): 开始日期(YYYYMMDD格式)，非必选
- `end_date` (str): 结束日期(YYYYMMDD格式)，非必选

**使用示例**:
```python
# 获取特定指数特定时间段的月线数据
pro.index_monthly(ts_code="000001.SH", start_date="20240101", end_date="20241231")

# 获取所有指数某一个月的月线数据
pro.index_monthly(start_date="20240101", end_date="20240131")
```

**返回字段**:
- `ts_code`: TS代码
- `trade_date`: 交易日期
- `close`: 收盘点位
- `open`: 开盘点位
- `high`: 最高点位
- `low`: 最低点位
- `pre_close`: 昨收点位
- `change`: 涨跌点位
- `pct_chg`: 涨跌幅(%)
- `vol`: 成交量(手)
- `amount`: 成交额(千元)

**限制说明**:
- 单次最大返回5000条数据

---

### 20. 指数技术因子 - idx_factor_pro

**Tushare 接口**: `pro.idx_factor_pro()`
**MCP 工具名**: `idx_factor_pro`
**描述**: 获取指数每日技术面因子数据，用于跟踪指数当前走势情况，数据由Tushare社区自产，覆盖全历史；输出参数_bfq表示不复权描述中说明了因子的默认传参，如需要特殊参数或者更多因子可以联系管理员评估，指数包括大盘指数 申万行业指数 中信指数限量：单次最大8000积分：5000积分每分钟可以请求30次，8000积分以上每分钟500次

**参数说明**:
- `ts_code` (str): 指数代码(大盘指数 申万指数 中信指数)，非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选
- `trade_date` (str): 交易日期，非必选

**使用示例**:
```python
# 获取特定指数特定时间段的技术因子
pro.idx_factor_pro(ts_code="000001.SH", start_date="20240101", end_date="20240131")

# 获取所有指数某一天的技术因子
pro.idx_factor_pro(trade_date="20240101")
```

**返回字段**:
- `ts_code`: 指数代码
- `trade_date`: 交易日期
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `pre_close`: 昨收价
- `change`: 涨跌额
- `pct_change`: 涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
- `vol`: 成交量 （手）
- `amount`: 成交额 （千元）
- `asi_bfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `asit_bfq`: 振动升降指标-OPEN, CLOSE, HIGH, LOW, M1=26, M2=10
- `atr_bfq`: 真实波动N日平均值-CLOSE, HIGH, LOW, N=20
- `bbi_bfq`: BBI多空指标-CLOSE, M1=3, M2=6, M3=12, M4=20
- `bias1_bfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias2_bfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `bias3_bfq`: BIAS乖离率-CLOSE, L1=6, L2=12, L3=24
- `boll_lower_bfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_mid_bfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `boll_upper_bfq`: BOLL指标，布林带-CLOSE, N=20, P=2
- `brar_ar_bfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `brar_br_bfq`: BRAR情绪指标-OPEN, CLOSE, HIGH, LOW, M1=26
- `cci_bfq`: 顺势指标又叫CCI指标-CLOSE, HIGH, LOW, N=14
- `cr_bfq`: CR价格动量指标-CLOSE, HIGH, LOW, N=20
- `dfma_dif_bfq`: 平行线差指标-CLOSE, N1=10, N2=50, M=10
- `dfma_difma_bfq`: 平行线差指标-CLOSE, N1=10, N2=50, M=10
- `dmi_adx_bfq`: 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `dmi_adxr_bfq`: 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `dmi_mdi_bfq`: 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `dmi_pdi_bfq`: 动向指标-CLOSE, HIGH, LOW, M1=14, M2=6
- `downdays`: 连跌天数
- `updays`: 连涨天数
- `dpo_bfq`: 区间震荡线-CLOSE, M1=20, M2=10, M3=6
- `madpo_bfq`: 区间震荡线-CLOSE, M1=20, M2=10, M3=6
- `ema_bfq_10`: 指数移动平均-N=10
- `ema_bfq_20`: 指数移动平均-N=20
- `ema_bfq_250`: 指数移动平均-N=250
- `ema_bfq_30`: 指数移动平均-N=30
- `ema_bfq_5`: 指数移动平均-N=5
- `ema_bfq_60`: 指数移动平均-N=60
- `ema_bfq_90`: 指数移动平均-N=90
- `emv_bfq`: 简易波动指标-HIGH, LOW, VOL, N=14, M=9
- `maemv_bfq`: 简易波动指标-HIGH, LOW, VOL, N=14, M=9
- `expma_12_bfq`: EMA指数平均数指标-CLOSE, N1=12, N2=50
- `expma_50_bfq`: EMA指数平均数指标-CLOSE, N1=12, N2=50
- `kdj_bfq`: KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `kdj_d_bfq`: KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `kdj_k_bfq`: KDJ指标-CLOSE, HIGH, LOW, N=9, M1=3, M2=3
- `ktn_down_bfq`: 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
- `ktn_mid_bfq`: 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
- `ktn_upper_bfq`: 肯特纳交易通道, N选20日，ATR选10日-CLOSE, HIGH, LOW, N=20, M=10
- `lowdays`: LOWRANGE(LOW)表示当前最低价是近多少周期内最低价的最小值
- `topdays`: TOPRANGE(HIGH)表示当前最高价是近多少周期内最高价的最大值
- `ma_bfq_10`: 简单移动平均-N=10
- `ma_bfq_20`: 简单移动平均-N=20
- `ma_bfq_250`: 简单移动平均-N=250
- `ma_bfq_30`: 简单移动平均-N=30
- `ma_bfq_5`: 简单移动平均-N=5
- `ma_bfq_60`: 简单移动平均-N=60
- `ma_bfq_90`: 简单移动平均-N=90
- `macd_bfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_dea_bfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `macd_dif_bfq`: MACD指标-CLOSE, SHORT=12, LONG=26, M=9
- `mass_bfq`: 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
- `ma_mass_bfq`: 梅斯线-HIGH, LOW, N1=9, N2=25, M=6
- `mfi_bfq`: MFI指标是成交量的RSI指标-CLOSE, HIGH, LOW, VOL, N=14
- `mtm_bfq`: 动量指标-CLOSE, N=12, M=6
- `mtmma_bfq`: 动量指标-CLOSE, N=12, M=6
- `obv_bfq`: 能量潮指标-CLOSE, VOL
- `psy_bfq`: 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
- `psyma_bfq`: 投资者对股市涨跌产生心理波动的情绪指标-CLOSE, N=12, M=6
- `roc_bfq`: 变动率指标-CLOSE, N=12, M=6
- `maroc_bfq`: 变动率指标-CLOSE, N=12, M=6
- `rsi_bfq_12`: RSI指标-CLOSE, N=12
- `rsi_bfq_24`: RSI指标-CLOSE, N=24

**限制说明**:
- 单次最大返回8000条数据
- 需要5000积分
- 每分钟可以请求30次，8000积分以上每分钟500次

---

### 20. 大盘资金流向 - moneyflow_mkt_dc

**Tushare 接口**: `pro.moneyflow_mkt_dc()`
**MCP 工具名**: `moneyflow_mkt_dc`
**描述**: 获取东方财富大盘资金流向数据，每日盘后更新限量：单次最大3000条，可根据日期或日期区间循环获取积分：120积分可试用，5000积分可正式调取，具体请参阅积分获取办法

**参数说明**:
- `trade_date` (str): 交易日期(YYYYMMDD格式，下同），非必选
- `start_date` (str): 开始日期，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取特定时间段的资金流向
pro.moneyflow_mkt_dc(start_date="20240901", end_date="20240930")

# 获取某一天的资金流向
pro.moneyflow_mkt_dc(trade_date="20240930")
```

**返回字段**:
- `trade_date`: 交易日期
- `close_sh`: 上证收盘价（点）
- `pct_change_sh`: 上证涨跌幅(%)
- `close_sz`: 深证收盘价（点）
- `pct_change_sz`: 深证涨跌幅(%)
- `net_amount`: 今日主力净流入 净额（元）
- `net_amount_rate`: 今日主力净流入净占比%
- `buy_elg_amount`: 今日超大单净流入 净额（元）
- `buy_elg_amount_rate`: 今日超大单净流入 净占比%
- `buy_lg_amount`: 今日大单净流入 净额（元）
- `buy_lg_amount_rate`: 今日大单净流入 净占比%
- `buy_md_amount`: 今日中单净流入 净额（元）
- `buy_md_amount_rate`: 今日中单净流入 净占比%
- `buy_sm_amount`: 今日小单净流入 净额（元）
- `buy_sm_amount_rate`: 今日小单净流入 净占比%

**限制说明**:
- 单次最大返回3000条数据
- 120积分可试用，5000积分可正式调取

---

### 21. 沪深港通资金流向 - moneyflow_hsgt

**Tushare 接口**: `pro.moneyflow_hsgt()`
**MCP 工具名**: `moneyflow_hsgt`
**描述**: 获取沪股通、深股通、港股通每日资金流向数据，每次最多返回300条记录，总量不限制。每天18~20点之间完成当日更新积分要求：2000积分起，5000积分每分钟可提取500次

**参数说明**:
- `trade_date` (str): 交易日期 (二选一)，非必选
- `start_date` (str): 开始日期 (二选一)，非必选
- `end_date` (str): 结束日期，非必选

**使用示例**:
```python
# 获取特定时间段的沪深港通资金流向
pro.moneyflow_hsgt(start_date="20240901", end_date="20240930")

# 获取某一天的沪深港通资金流向
pro.moneyflow_hsgt(trade_date="20240930")
```

**返回字段**:
- `trade_date`: 交易日期
- `ggt_ss`: 港股通（上海）
- `ggt_sz`: 港股通（深圳）
- `hgt`: 沪股通（百万元）
- `sgt`: 深股通（百万元）
- `north_money`: 北向资金（百万元）
- `south_money`: 南向资金（百万元）

**限制说明**:
- 每次最多返回300条记录，总量不限制
- 2000积分起，5000积分每分钟可提取500次

---

### 23. 指数成分和权重 - index_weight

**Tushare 接口**: `pro.index_weight()`
**MCP 工具名**: `index_weight`
**描述**: 获取各类指数成分和权重，月度数据。建议按月查询时，开始日期用当月第一天、结束日期用当月最后一天。[0]

**参数说明**:
- `index_code` (str): 指数代码（必选），如 `399300.SZ`
- `trade_date` (str): 交易日期（YYYYMMDD），非必选
- `start_date` (str): 开始日期（YYYYMMDD），非必选
- `end_date` (str): 结束日期（YYYYMMDD），非必选

**使用示例**:
```python
# 提取沪深300指数2018年9月成分和权重
pro.index_weight(index_code='399300.SZ', start_date='20180901', end_date='20180930')
```

**返回字段**:
- `index_code`: 指数代码
- `con_code`: 成分代码
- `trade_date`: 交易日期
- `weight`: 权重

**限制说明**:
- 月度数据，建议按月查询 [0]
- 需要至少2000积分 [0]

---

### 23. 大盘指数每日指标 - index_dailybasic

**Tushare 接口**: `pro.index_dailybasic()`
**MCP 工具名**: `index_dailybasic`
**描述**: 获取大盘指数每日指标，目前仅提供上证综指、深证成指、上证50、中证500、中小板指、创业板指的每日指标数据。

**参数说明**:
- `trade_date` (str): 交易日期（格式：YYYYMMDD）
- `ts_code` (str): TS代码
- `start_date` (str): 开始日期（YYYYMMDD）
- `end_date` (str): 结束日期（YYYYMMDD）

说明：`trade_date`、`ts_code` 至少输入一个参数，单次限量3000条。

**使用示例**:
```python
# 获取2018-10-18某些指标
pro.index_dailybasic(trade_date='20181018', fields='ts_code,trade_date,turnover_rate,pe')
```

**返回字段**:
- `ts_code`: TS代码
- `trade_date`: 交易日期
- `total_mv`: 当日总市值（元）
- `float_mv`: 当日流通市值（元）
- `total_share`: 当日总股本（股）
- `float_share`: 当日流通股本（股）
- `free_share`: 当日自由流通股本（股）
- `turnover_rate`: 换手率
- `turnover_rate_f`: 换手率(基于自由流通股本)
- `pe`: 市盈率
- `pe_ttm`: 市盈率TTM
- `pb`: 市净率

**限制说明**:
- 用户需要至少400积分才可以调取
- 单次限量3000条



### 24. 每日指标数据 - daily_basic

**Tushare 接口**: `pro.daily_basic()`
**MCP 工具名**: `daily_basic`
**描述**: 获取全部股票每日重要的基本面指标，可用于选股分析、报表展示等。每日15点～17点更新；当财务数据缺失时，可用其中的 `pe_ttm`、`pb` 等作为替代指标。

**参数说明**:
- `ts_code` (str): 股票代码（二选一，格式如 `600000.SH`），可选
- `trade_date` (str): 交易日期（二选一，`YYYYMMDD`），可选
- `start_date` (str): 开始日期（`YYYYMMDD`），可选
- `end_date` (str): 结束日期（`YYYYMMDD`），可选
- `fields` (str): 指定返回字段，逗号分隔，可选

**使用示例**:
```python
# 获取所有股票某一天的每日指标（只取部分字段）
pro.daily_basic(trade_date='20180726', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')

# 获取单只股票一段时间的每日指标（全部字段）
pro.daily_basic(ts_code='600000.SH', start_date='20240101', end_date='20240131')
```

**返回字段（常用）**:
- `ts_code`: TS股票代码
- `trade_date`: 交易日期
- `close`: 当日收盘价
- `turnover_rate`: 换手率（%）
- `turnover_rate_f`: 换手率（自由流通股）
- `volume_ratio`: 量比
- `pe`: 市盈率（总市值/净利润，亏损时为空）
- `pe_ttm`: 市盈率（TTM，亏损时为空）
- `pb`: 市净率（总市值/净资产）
- `ps`: 市销率
- `ps_ttm`: 市销率（TTM）
- `dv_ratio`: 股息率（%）
- `dv_ttm`: 股息率（TTM）（%）
- `total_share`: 总股本（万股）
- `float_share`: 流通股本（万股）
- `free_share`: 自由流通股本（万）
- `total_mv`: 总市值（万元）
- `circ_mv`: 流通市值（万元）

**限制说明**:
- 单次最大返回6000条数据；可按日线循环提取全部历史
- 积分：至少2000积分才可以调取，5000积分无总量限制

**MCP 使用说明**:
- 工具名：`daily_basic`
- 支持参数：`ts_code`、`trade_date`、`start_date`、`end_date`、`fields`
- 至少提供 `ts_code` 或 `trade_date` 其中之一；日期格式为 `YYYYMMDD`

---

## 通用说明

1. **返回格式**：所有接口返回值为JSON字符串（records格式）。如接口抛出异常，将返回形如`{"error": "..."}`的字符串。

2. **日期格式**：所有日期参数格式为YYYYMMDD，如20240101表示2024年1月1日。

3. **股票代码格式**：
   - 沪市股票：600000.SH
   - 深市股票：000001.SZ
   - 创业板股票：300001.SZ
   - 科创板股票：688001.SH

4. **指数代码格式**：
   - 上证指数：000001.SH
   - 深证成指：399001.SZ
   - 创业板指：399006.SZ
   - 同花顺指数：885001.TI

5. **积分限制**：部分接口需要一定积分才能使用，具体限制请参考Tushare Pro官方文档。

6. **频率限制**：所有接口都有频率限制，建议合理控制调用频率，避免触发限制。

7. **数据更新**：不同接口的数据更新频率不同，大部分接口在交易日结束后更新，部分接口在盘中实时更新。

8. **Token设置**：需要在环境变量或.env文件中设置`TUSHARE_TOKEN`，否则无法调用接口。

9. **错误处理**：建议在调用接口时添加异常处理，捕获可能的错误信息。

10. **数据量限制**：大部分接口单次返回数据量有限制，如需获取大量数据，建议分批次获取。

## 最佳实践

1. **批量获取**：对于需要获取多只股票数据的情况，建议使用循环分批获取，避免一次性请求过多数据。

2. **数据缓存**：对于不经常变化的数据（如股票基本信息），建议进行本地缓存，减少接口调用次数。

3. **异常处理**：建议在调用接口时添加重试机制，处理网络波动等临时性问题。

4. **参数组合**：合理使用参数组合，如同时指定ts_code和日期范围，可以精确获取所需数据。

5. **字段筛选**：使用fields参数指定需要的字段，减少数据传输量，提高接口响应速度。

6. **数据验证**：获取数据后，建议进行必要的验证，如检查数据完整性、合理性等。

7. **日志记录**：建议记录接口调用日志，便于问题排查和统计分析。

8. **并发控制**：如需并发调用接口，建议控制并发数量，避免触发频率限制。