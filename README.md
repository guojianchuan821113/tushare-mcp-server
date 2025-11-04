# Tushare MCP Server

将 Tushare Pro 的多个接口封装为 MCP 工具，通过 `stdio` 供 AI 客户端（如 Claude Desktop）调用。所有工具返回 Pandas DataFrame 的 `orient="records"` JSON 字符串。

## 前置条件
- Python 3.10+
- 已安装 [uv](https://github.com/astral-sh/uv)
- 有效的 Tushare Pro Token

## 安装依赖
```bash
uv sync
```

## 配置 Token
在项目根目录创建/编辑 `.env`（已提供示例）：
```env
TUSHARE_TOKEN=your_tushare_token_here
```
代码将优先从环境变量 `TUSHARE_TOKEN` 读取，若无则再从 `.env` 加载。

## 运行服务器
```bash
uv run src/tushare_mcp_server/server.py
```
服务器使用 `stdio` 作为 MCP 传输层。

## 已封装的工具
1. `stk_factor_pro` — 股票技术面因子（专业版技术指标）
2. `moneyflow` — 个股资金流向
3. `moneyflow_cnt_ths` — 同花顺概念板块资金流向
4. `moneyflow_ind_ths` — 同花顺行业板块资金流向
5. `cyq_perf` — 股票筹码分布
6. `stock_basic` — 股票基本信息
7. `index_classify` — 行业分类信息
8. `fina_indicator` — 财务指标
9. `stk_holdernumber` — 股东人数
10. `ths_daily` — 同花顺指数日线
11. `index_weekly` — 指数周线
12. `trade_cal` — 交易日历
13. `stk_auction_o` — 集合竞价

所有工具均返回 JSON 字符串；若发生错误（参数/网络等），返回形如：
```json
{"error": "<错误信息>"}
```

## 集成到 Claude Desktop（示例）
在 `claude_desktop_config.json` 中添加：
```json
{
  "mcpServers": {
    "tushare-mcp-server": {
      "command": "uv",
      "args": ["run", "/Users/guojianchuan/Downloads/github_workspace/tushare-mcp-server/src/tushare_mcp_server/server.py"]
    }
  }
}
```

## 许可证
本项目用于演示 MCP 服务器的基本封装方式。