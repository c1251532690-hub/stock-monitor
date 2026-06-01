# 股票价格监控 Streamlit Web App

这是一个基于 Streamlit 的股票价格查询与监控工具，支持输入单只或多只股票代码，显示最新价格与涨跌幅，并可开启自动刷新。

## 主要功能

- 支持输入单个或多个股票代码
- 支持批量股票查询（空格、逗号或分号分隔）
- 显示最新价格、涨跌值、涨跌幅和查询状态
- **多时间范围走势图**：1分钟、30分钟、日线、周线、1年、5年、全部历史
- **交互式图表**：支持缩放、拖拽、鼠标悬停查看具体价格和时间
- **多股票对比**：使用选项卡分别查看不同股票的走势
- **数据统计**：显示最高价、最低价、平均价等关键指标
- 支持自动刷新功能

## 安装依赖

```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
```

## 运行 Web App

```bash
.\.venv\Scripts\python -m streamlit run app.py
```

## 命令行工具

如果你希望继续使用原有命令行版本，也可以运行：

```bash
.\.venv\Scripts\python stock_price.py --symbol AAPL
.\.venv\Scripts\python stock_price.py --symbols AAPL 000001.SZ
.\.venv\Scripts\python stock_price.py --symbols AAPL 000001.SZ --watch --interval 5
```

命令行版本支持单只查询、批量查询和监控刷新。

## 使用说明

1. 在侧边栏输入股票代码，支持空格、逗号或分号分隔。
   - 示例：`AAPL MSFT` 或 `AAPL,000001.SZ,600000.SS`
2. 美股代码会自动转换为大写（例如 `nvda` 会自动识别为 `NVDA`）
3. 点击"查询"按钮手动执行一次查询。
4. 查询结果将以表格形式显示每个股票的最新价格、涨跌和涨跌幅。
5. **查看走势图**：
   - 如果查询成功，在表格下方会显示"价格走势图"部分
   - 点击对应的选项卡查看该股票的历史价格走势
   - 在"选择时间范围"下拉框中选择不同的时间周期：
     - **1分钟**：盘中 1 分钟级别数据
     - **30分钟**：盘中 30 分钟级别数据
     - **日线**：每日收盘价数据
     - **周线**：每周收盘价数据
     - **1年**：过去 1 年的日线数据
     - **5年**：过去 5 年的日线数据
     - **全部**：从上市至今的完整历史数据
   - 图表支持缩放（鼠标滚轮或拖拽）、悬停查看具体价格和时间
   - 下方显示最高价、最低价、平均价等统计数据
6. 勾选"启用自动刷新"后，页面会按照设置的间隔自动更新数据和图表。

## 部署到 Streamlit Cloud

1. 将仓库推送到 GitHub：

```bash
cd C:\workspace_stock_tool
& "C:\Program Files\Git\cmd\git.exe" add .
& "C:\Program Files\Git\cmd\git.exe" commit -m "Add Streamlit deployment files"
& "C:\Program Files\Git\cmd\git.exe" push origin main
```

2. 登录 https://streamlit.io/cloud 并连接你的 GitHub 账号。
3. 在 Streamlit Cloud 中选择 `stock-monitor` 仓库，并将应用入口设置为：

```
app.py
```

4. 确保 `requirements.txt` 存在于仓库根目录，Streamlit Cloud 会自动安装依赖。

部署成功后，你会得到一个可直接访问的 Web 应用链接。

## 代码说明

- `app.py`: Streamlit Web App 主程序
  - `parse_symbols()`: 解析股票代码字符串
  - `get_price_change()`: 获取最新价格和涨跌信息
  - `get_price_history()`: 获取完整历史价格数据（从上市至今）
  - `plot_price_chart()`: 使用 plotly 绘制交互式走势图
- `stock_price.py`: 原有命令行工具，保留兼容性
- `requirements.txt`: Web App 所需依赖

## 注意

- 国内股票代码请加交易所后缀，例如 `000001.SZ` 或 `600000.SS`
- 数据来源为 Yahoo Finance，某些代码可能需要调整后缀才能获取到
