# 股票价格小工具（批量 + 监控）

用途：输入一个或多只股票代码，获取当前价格与涨跌幅；可启用监控模式持续刷新。

依赖安装：

```bash
pip install -r requirements.txt
```

使用示例：

```bash
# 单只查询
python stock_price.py --symbol AAPL

# 批量查询（空格分隔）
python stock_price.py --symbols AAPL 000001.SZ

# 监控模式，每 5 秒刷新一次（无限次）
python stock_price.py --symbols AAPL 000001.SZ --watch --interval 5

# 监控 10 次后停止
python stock_price.py --symbols AAPL 000001.SZ --watch --interval 5 --iterations 10

# 交互式输入（回车后输入空格分隔的代码）
python stock_price.py

``` 

说明：脚本使用 `yfinance` 从 Yahoo Finance 获取最近两日的收盘价并计算涨跌幅。某些国内代码需要带上交易所后缀，例如 `000001.SZ` 或 `600000.SS`。
