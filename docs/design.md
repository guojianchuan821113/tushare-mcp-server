# 角色与目标
你是一名专精于 Python 和 Model Context Protocol (MCP) 的专家级软件开发人员。你的任务是根据以下详细规范，创建一个完整、可运行且结构良好的 Python MCP 服务器。该服务器的目标是将 Tushare Pro 的多个数据接口封装为标准的 MCP 工具，以便 AI 客户端（如 Claude Desktop）能够调用。
# 项目概述
- **项目名称**: `tushare-mcp-server`
- **核心功能**: 将指定的 Tushare Pro API 接口转换为 MCP 工具。
- **通信方式**: 使用 `stdio` (标准输入输出) 作为 MCP 传输层。
- **数据格式**: 所有工具的返回值必须是 JSON 字符串格式，具体为 Pandas DataFrame 的 `orient="records"` 格式。
# 技术栈与依赖
- **项目管理器**: `uv`
- **Python 版本**: 3.10+
- **核心库**:
    - `mcp[cli]`: 用于实现 MCP 服务器，请使用 `FastMCP` 高级封装。
    - `tushare`: 用于调用 Tushare Pro API。
    - `python-dotenv`: 用于从 `.env` 文件加载 Tushare Token。
    - `pandas`: Tushare 依赖，用于数据处理。
# 项目结构
请按照以下标准 Python 项目结构创建文件和目录：
tushare-mcp-server/
├── .env
├── .gitignore
├── pyproject.toml
├── README.md
└── src/
└── tushare_mcp_server/
├── init.py
└── server.py
# 核心任务：实现 MCP 服务器
## 1. 初始化与配置 (`server.py`)
-   在 `src/tushare_mcp_server/server.py` 文件中开始编码。
-   导入所有必要的库。
-   使用 `python-dotenv` 加载项目根目录下的 `.env` 文件中的 `TUSHARE_TOKEN`。
-   使用 `ts.set_token()` 设置 Token，并初始化 `pro = ts.pro_api()`。
-   实例化 `FastMCP`，例如 `mcp = FastMCP("Tushare MCP Server")`。
## 2. 工具封装逻辑
对于下面列出的每一个 Tushare 接口，你必须遵循以下模式将其封装为一个独立的 MCP 工具：
-   **装饰器**: 使用 `@mcp.tool()` 装饰器。
-   **函数命名**: 将 `pro.` 后面的函数名转换为 `snake_case` 作为工具函数名（例如, `pro.stk_factor_pro()` -> `def stk_factor_pro(...)`）。
-   **参数映射**:
    -   函数参数应直接映射到 Tushare 接口的参数。
    -   为所有参数提供类型提示（`str`, `int` 等）。
    -   为常用且必要的参数（如 `ts_code`, `start_date`, `end_date`）设置默认值 `None`，并在函数内部处理，以便在客户端未提供时也能灵活调用。
-   **文档字符串**: 为每个工具函数编写清晰的 docstring，说明其功能。MCP 客户端会使用这些信息来理解工具。
-   **API 调用**: 在函数内部调用对应的 `pro.<interface_name>(...)` 方法。
-   **返回值处理**:
    -   Tushare 返回的是 Pandas DataFrame。
    -   将 DataFrame 转换为 JSON 字符串：`df.to_json(orient="records", ensure_ascii=False)`。
    -   函数必须返回这个 JSON 字符串。
-   **错误处理**: 用 `try...except` 块包装 API 调用，捕获潜在错误（如网络问题、无效参数），并返回一个包含错误信息的 JSON 字符串，例如：`json.dumps({"error": str(e)})`。
## 3. 需要封装的 Tushare 接口清单（考虑到任务规模偏大，第一步只需要实现接口1和接口2，其他接口后续扩展补充）
请严格按照以下清单，为每个接口创建一个对应的 MCP 工具：
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
## 4. 服务器启动
在 `server.py` 文件末尾，添加标准的服务器启动代码：
```python
if __name__ == "__main__":
    mcp.run(transport='stdio')
配置与部署文件
1. pyproject.toml
使用 uv 初始化项目并生成 pyproject.toml。
在 [project] 部分填入项目名称、版本等基本信息。
在 [project.dependencies] 部分列出所有依赖：mcp, tushare, python-dotenv, pandas。
2. .env 文件
创建一个名为 .env 的文件，内容如下：# 将 your_tushare_token_here 替换为你的真实 Tushare Pro Token
TUSHARE_TOKEN=your_tushare_token_here
代码中首先从环境变量TUSHARE_TOKEN中去获取，获取不到再从.env文件中去加载。
3. .gitignore
创建一个标准的 Python .gitignore 文件，确保 .env、__pycache__、.venv 等不被提交到版本库。
4. README.md
创建一个 README.md 文件，简要说明项目功能、如何安装依赖 (uv sync)、如何配置 Token (.env 文件) 以及如何运行服务器 (uv run src/tushare_mcp_server/server.py)。
同时，提供一个 claude_desktop_config.json 的配置示例，展示如何将此 MCP 服务器集成到 Claude Desktop 中。
最终交付物
请生成以下所有内容的完整代码：
完整的项目文件结构。
pyproject.toml 的内容。
src/tushare_mcp_server/server.py 的完整源代码，包含所有 13 个工具的实现。
.env 文件的示例内容。
.gitignore 文件的内容。
README.md 文件的内容。
请确保代码是生产就绪的，遵循最佳实践，并且可以直接运行。
