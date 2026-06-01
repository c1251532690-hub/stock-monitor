#!/usr/bin/env python3
"""
小工具：根据股票代码获取当前价格及涨跌幅（支持批量查询与监控）

依赖：yfinance
用法示例：
  python stock_price.py --symbols AAPL 000001.SZ
  python stock_price.py --symbols AAPL 000001.SZ --watch --interval 5
  python stock_price.py # 交互式输入
"""
import argparse
import sys
import time
from datetime import datetime
import yfinance as yf


def get_price_change(symbol: str):
    symbol = symbol.strip()
    t = yf.Ticker(symbol)
    hist = t.history(period="2d")
    if hist.empty:
        raise ValueError(f"无法获取 {symbol} 的历史数据")
    last_close = float(hist['Close'].iloc[-1])
    if len(hist) >= 2:
        prev_close = float(hist['Close'].iloc[-2])
        change = last_close - prev_close
        pct = (change / prev_close) * 100 if prev_close != 0 else 0.0
    else:
        change = 0.0
        pct = 0.0
    return last_close, change, pct


def fetch_batch(symbols):
    results = {}
    for s in symbols:
        try:
            price, change, pct = get_price_change(s)
            results[s] = (price, change, pct, None)
        except Exception as e:
            results[s] = (None, None, None, str(e))
    return results


def main():
    parser = argparse.ArgumentParser(description="获取股票当前价格和涨跌幅（支持批量与监控）")
    parser.add_argument('--symbol', '-s', help='单只股票代码，例如 AAPL 或 000001.SZ')
    parser.add_argument('--symbols', '-S', nargs='+', help='批量股票代码，空格分隔，例如 AAPL 000001.SZ')
    parser.add_argument('--watch', '-w', action='store_true', help='持续刷新/监控模式')
    parser.add_argument('--interval', '-i', type=float, default=10.0, help='监控刷新间隔（秒），默认 10')
    parser.add_argument('--iterations', '-n', type=int, default=0, help='监控次数，0 表示无限（直到 Ctrl+C）')
    args = parser.parse_args()

    # 解析 symbols
    symbols = []
    if args.symbol:
        symbols.append(args.symbol)
    if args.symbols:
        symbols.extend(args.symbols)
    if not symbols:
        try:
            line = input('请输入股票代码（单个或空格分隔多个，例如 AAPL 000001.SZ）：').strip()
            if not line:
                print('\n已取消。')
                sys.exit(1)
            symbols = line.split()
        except (EOFError, KeyboardInterrupt):
            print('\n已取消。')
            sys.exit(1)

    def print_results(res):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{ts}] 查询结果：')
        for sym, vals in res.items():
            price, change, pct, err = vals
            if err:
                print(f'  {sym}: 获取失败 -> {err}')
            else:
                sign = '+' if change >= 0 else '-'
                print(f'  {sym}  当前价: {price:.4f}  变动: {sign}{abs(change):.4f}  ({sign}{abs(pct):.2f}%)')
        print('-' * 60)

    # 运行一次或进入监控循环
    if args.watch:
        iterations = args.iterations
        count = 0
        try:
            while True:
                res = fetch_batch(symbols)
                print_results(res)
                count += 1
                if iterations > 0 and count >= iterations:
                    break
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print('\n已停止监控。')
    else:
        res = fetch_batch(symbols)
        print_results(res)


if __name__ == '__main__':
    main()
