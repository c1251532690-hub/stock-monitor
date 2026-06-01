import re
import time
from datetime import datetime

import streamlit as st
import yfinance as yf


def parse_symbols(text: str):
    if not text:
        return []
    return [s.strip() for s in re.split(r'[\s,;]+', text) if s.strip()]


def get_price_change(symbol: str):
    symbol = symbol.strip()
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='2d')
    if hist.empty:
        raise ValueError(f'无法获取 {symbol} 的历史数据')

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
    results = []
    for symbol in symbols:
        try:
            price, change, pct = get_price_change(symbol)
            results.append(
                {
                    '代码': symbol,
                    '最新价格': f'{price:.4f}',
                    '涨跌': f'{change:+.4f}',
                    '涨跌幅': f'{pct:+.2f}%',
                    '状态': '成功',
                }
            )
        except Exception as exc:
            results.append(
                {
                    '代码': symbol,
                    '最新价格': '-',
                    '涨跌': '-',
                    '涨跌幅': '-',
                    '状态': f'错误：{exc}',
                }
            )
    return results


def main():
    st.set_page_config(page_title='股票价格监控', layout='wide')
    st.title('股票价格监控 Web App')
    st.write('输入股票代码，支持批量查询，显示最新价格和涨跌幅，并可启用自动刷新。')

    st.sidebar.header('查询配置')
    symbols_text = st.sidebar.text_area(
        '股票代码（支持空格、逗号或分号分隔）',
        value='AAPL MSFT',
        height=120,
        help='示例：AAPL 000001.SZ 或 AAPL,MSFT,000001.SZ',
    )
    auto_refresh = st.sidebar.checkbox('启用自动刷新', value=False)
    interval = st.sidebar.number_input(
        '刷新间隔（秒）', min_value=5, max_value=3600, value=10, step=1
    )
    submit = st.sidebar.button('查询')

    symbols = parse_symbols(symbols_text)
    if not symbols:
        st.warning('请在侧边栏输入至少一个股票代码，然后点击“查询”。')
        return

    if auto_refresh:
        st.sidebar.success(f'自动刷新已开启，每 {interval} 秒刷新一次。')

    if submit or auto_refresh:
        with st.spinner('正在查询股票数据，请稍候...'):
            results = fetch_batch(symbols)

        st.subheader('查询结果')
        st.write(f'最后刷新时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        st.table(results)

        success_count = sum(1 for row in results if row['状态'] == '成功')
        error_count = len(results) - success_count
        st.info(f'查询完成：{len(results)} 支股票，成功 {success_count} 支，失败 {error_count} 支。')

        if error_count > 0:
            st.warning('部分股票获取失败，请检查代码格式或后缀是否正确，例如 000001.SZ / 600000.SS。')
        if auto_refresh:
            time.sleep(interval)
            st.rerun()
    else:
        st.info('请点击侧边栏的“查询”按钮以获取价格信息。')


if __name__ == '__main__':
    main()
