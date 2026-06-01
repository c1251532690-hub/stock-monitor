import re
import time
from datetime import datetime

import plotly.graph_objects as go
import streamlit as st
import yfinance as yf


def parse_symbols(text: str):
    if not text:
        return []
    symbols = []
    for s in re.split(r'[\s,;]+', text):
        s = s.strip()
        if s:
            # 美股代码（不含"."）转为大写，中国股票代码保持原样
            if '.' not in s:
                s = s.upper()
            symbols.append(s)
    return symbols


def get_price_change(symbol: str):
    symbol = symbol.strip()
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period='2d')
        if hist.empty:
            # 检查是否是有效的股票代码
            if '.' in symbol:
                raise ValueError(f'股票代码 {symbol} 不存在或无法获取数据，请检查中国股票代码格式（如 000001.SZ）')
            else:
                raise ValueError(f'股票代码 {symbol} 不存在或无法获取数据，请检查代码是否正确')

        last_close = float(hist['Close'].iloc[-1])
        if len(hist) >= 2:
            prev_close = float(hist['Close'].iloc[-2])
            change = last_close - prev_close
            pct = (change / prev_close) * 100 if prev_close != 0 else 0.0
        else:
            change = 0.0
            pct = 0.0

        return last_close, change, pct
    except Exception as e:
        # 捕获网络或其他错误
        raise Exception(f'{symbol}: {str(e)}')


def get_price_history(symbol: str, period: str = 'max'):
    """获取股票的历史价格数据
    
    Args:
        symbol: 股票代码
        period: 时间范围 ('1m', '30m', '1d', '5d', '1wk', '1y', '5y', 'max')
    """
    symbol = symbol.strip()
    try:
        ticker = yf.Ticker(symbol)
        # 根据 period 选择合适的 interval
        if period in ['1m', '5m', '15m', '30m', '60m']:
            # 盘中数据，通常只能获取最近几天
            hist = ticker.history(period='7d', interval=period)
        else:
            # 日线或更长时间范围
            hist = ticker.history(period=period)
        
        if hist.empty:
            raise ValueError(f'无法获取 {symbol} 的{period}时间范围数据')
        return hist
    except Exception as e:
        raise Exception(f'{symbol}: {str(e)}')


def plot_price_chart(symbol: str, hist, period_label: str = '全部') -> go.Figure:
    """使用 plotly 绘制交互式价格走势图"""
    fig = go.Figure()

    # 添加收盘价线
    fig.add_trace(
        go.Scatter(
            x=hist.index,
            y=hist['Close'],
            mode='lines',
            name='收盘价',
            line=dict(color='#1f77b4', width=2),
            hovertemplate='<b>%{x|%Y-%m-%d %H:%M}</b><br>收盘价: ¥%{y:.2f}<extra></extra>',
        )
    )

    # 添加成交量柱状图（作为二级 y 轴）
    fig.add_trace(
        go.Bar(
            x=hist.index,
            y=hist['Volume'],
            name='成交量',
            yaxis='y2',
            marker=dict(color='rgba(158, 154, 200, 0.5)'),
            hovertemplate='<b>%{x|%Y-%m-%d}</b><br>成交量: %{y:,.0f}<extra></extra>',
        )
    )

    # 更新布局
    fig.update_layout(
        title=f'{symbol} 历史价格走势 - {period_label}',
        xaxis_title='日期',
        yaxis_title='价格（¥）',
        yaxis2=dict(title='成交量', overlaying='y', side='right'),
        hovermode='x unified',
        template='plotly_white',
        height=500,
        xaxis_rangeslider_visible=False,
        margin=dict(l=50, r=100, t=80, b=50),
    )

    return fig


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

        # 获取成功的股票代码
        successful_symbols = [row['代码'] for row in results if row['状态'] == '成功']

        # 如果有成功的股票，显示走势图
        if successful_symbols:
            st.subheader('价格走势图')
            st.write('选择时间范围查看各股票的历史价格走势（支持缩放、悬停查看价格）')

            # 时间范围映射
            period_map = {
                '1分钟': ('1m', '1分钟'),
                '30分钟': ('30m', '30分钟'),
                '日线': ('1d', '日线'),
                '周线': ('1wk', '周线'),
                '1年': ('1y', '1年'),
                '5年': ('5y', '5年'),
                '全部': ('max', '全部历史'),
            }

            # 创建选项卡来分别显示每支股票的走势图
            tabs = st.tabs(successful_symbols)

            for tab, symbol in zip(tabs, successful_symbols):
                with tab:
                    # 添加时间范围选择器
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        selected_period_label = st.selectbox(
                            '选择时间范围',
                            list(period_map.keys()),
                            index=5,  # 默认选择 '5年'
                            key=f'{symbol}_period'
                        )
                    
                    selected_period, period_label = period_map[selected_period_label]
                    
                    try:
                        with st.spinner(f'正在加载 {symbol} 的{period_label}数据...'):
                            hist = get_price_history(symbol, period=selected_period)
                        fig = plot_price_chart(symbol, hist, period_label)
                        st.plotly_chart(fig, use_container_width=True)

                        # 显示数据统计
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric('最高价', f"¥{hist['High'].max():.2f}")
                        with col2:
                            st.metric('最低价', f"¥{hist['Low'].min():.2f}")
                        with col3:
                            st.metric('平均价', f"¥{hist['Close'].mean():.2f}")
                        with col4:
                            st.metric('数据点数', len(hist))
                    except Exception as e:
                        st.error(f'无法加载 {symbol} 的走势图：{str(e)}')

        if auto_refresh:
            time.sleep(interval)
            st.rerun()
    else:
        st.info('请点击侧边栏的“查询”按钮以获取价格信息。')


if __name__ == '__main__':
    main()
