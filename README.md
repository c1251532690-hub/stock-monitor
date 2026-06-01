# 股票价格监控 Streamlit Web App

这是一个基于 Streamlit 的股票价格查询与监控工具，支持输入单只或多只股票代码，显示最新价格与涨跌幅，并可开启自动刷新。

## 主要功能

- 支持输入单个或多个股票代码
- 支持批量股票查询（空格、逗号或分号分隔）
- 显示最新价格、涨跌值、涨跌幅和查询状态
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
2. 勾选“启用自动刷新”后，页面会按照设置的间隔自动更新数据。
3. 点击“查询”按钮手动执行一次查询。
4. 查询结果将以表格形式显示每个股票的最新价格、涨跌和涨跌幅。

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
- `stock_price.py`: 原有命令行工具，保留兼容性
- `requirements.txt`: Web App 所需依赖

## 注意

- 国内股票代码请加交易所后缀，例如 `000001.SZ` 或 `600000.SS`
- 数据来源为 Yahoo Finance，某些代码可能需要调整后缀才能获取到
