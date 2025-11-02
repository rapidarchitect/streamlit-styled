import streamlit as st
import httpx
import pandas as pd
from lightweight_charts.widgets import StreamlitChart

if "symbols_list" not in st.session_state:
    st.session_state.symbols_list = None

if "chart_loaded" not in st.session_state:
    st.session_state.chart_loaded = False

st.set_page_config(
    layout = 'wide',
    page_title = 'Crypto Dashboard'
)

st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """, unsafe_allow_html = True
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

# Add dashboard title - smaller size matching price boxes
st.markdown('<p class="dashboard_title">Crypto Dashboard</p>', unsafe_allow_html=True)

btc_col, eth_col, xmr_col, sol_col, xrp_col = st.columns([1,1,1,1,1])

def fetch_price(symbol):
    """Fetch crypto price from DIA API with error handling, returns (price, change_percent)"""
    try:
        # DIA API mapping for common cryptocurrencies
        # Format: symbol -> (DIA_name, blockchain_address)
        dia_symbols = {
            'BTC': ('Bitcoin', '0x0000000000000000000000000000000000000000'),
            'ETH': ('Ethereum', '0x0000000000000000000000000000000000000000'),
            'XMR': ('Monero', '0x0000000000000000000000000000000000000000'),
            'SOL': ('Solana', '0x0000000000000000000000000000000000000000'),
            'XRP': ('XRP', '0x0000000000000000000000000000000000000000', 'XRPL'),  # XRP uses XRPL blockchain
        }

        crypto = symbol.split('/')[0]  # Get the cryptocurrency part (BTC, ETH, etc.)

        if crypto not in dia_symbols:
            return ("Symbol not supported", 0)

        dia_info = dia_symbols[crypto]
        dia_name = dia_info[0]
        address = dia_info[1]
        blockchain = dia_info[2] if len(dia_info) > 2 else dia_name

        # Call DIA API
        url = f'https://api.diadata.org/v1/assetQuotation/{blockchain}/{address}'
        response = httpx.get(url, timeout=10)

        if response.status_code != 200:
            return ("API Error", 0)

        data = response.json()

        # Extract price and change from response
        price = data.get('Price')
        if price is None:
            return ("Price not available", 0)

        # Get 24h change percentage if available
        change_percent = data.get('Change24h', 0)
        if change_percent is None:
            change_percent = 0

        return (f"${price:,.2f}", change_percent)
    except httpx.TimeoutException:
        return ("Request timeout", 0)
    except Exception as e:
        return (f"Error", 0)

with btc_col:
    btc_price, btc_change = fetch_price('BTC/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if btc_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="btc_text">BTC / USDT<br></p><p class="price_details">{btc_price} {arrow}</p></div>', unsafe_allow_html = True)

with eth_col:
    eth_price, eth_change = fetch_price('ETH/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if eth_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="eth_text">ETH / USDT<br></p><p class="price_details">{eth_price} {arrow}</p></div>', unsafe_allow_html = True)

with xmr_col:
    xmr_price, xmr_change = fetch_price('XMR/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if xmr_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="xmr_text">XMR / USDT<br></p><p class="price_details">{xmr_price} {arrow}</p></div>', unsafe_allow_html = True)

with sol_col:
    sol_price, sol_change = fetch_price('SOL/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if sol_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="sol_text">SOL / USDT<br></p><p class="price_details">{sol_price} {arrow}</p></div>', unsafe_allow_html = True)

with xrp_col:
    xrp_price, xrp_change = fetch_price('XRP/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if xrp_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="xrp_text">XRP / USDT<br></p><p class="price_details">{xrp_price} {arrow}</p></div>', unsafe_allow_html = True)

# Add spacing between price cards and chart section
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

params_col, chart_col = st.columns([0.45, 1.55])

hist_df = None  # Initialize variable

with params_col:

    with st.form(key = 'params_form'):

        st.markdown(f'<p class="params_text">CHART DATA PARAMETERS', unsafe_allow_html = True)

        st.divider()

        # Common crypto trading pairs
        symbols = ['BTC-USD', 'ETH-USD', 'XMR-USD', 'SOL-USD', 'XRP-USD', 'ADA-USD', 'DOGE-USD', 'LTC-USD', 'AVAX-USD', 'MATIC-USD']
        symbol = st.selectbox('Symbol', symbols, key = 'symbol_selectbox')

        interval_col, period_col = st.columns(2)
        with interval_col:
            interval = st.selectbox('Interval', ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '12h', '1d'], key = 'interval_selectbox')
        with period_col:
            period = st.number_input('Period', min_value = 10, max_value = 500, value = 365, step = 1, key = 'period_no_input')

        st.markdown('')
        update_chart = st.form_submit_button('Update chart')
        st.markdown('')

        if update_chart:
            try:
                # Extract symbol for yfinance (convert BTC-USD to BTC-USD format)
                symbol_yf = symbol  # Already in correct format from selectbox
                
                # Fetch historical data from yfinance (DIA doesn't provide historical data)
                import yfinance as yf
                ticker = yf.Ticker(symbol_yf)
                hist = ticker.history(period='1y')
                
                if hist.empty:
                    st.error(f"No data found for {symbol}")
                    hist_df = None
                else:
                    # Rename columns to match chart expectations
                    hist_df = hist.reset_index()
                    hist_df = hist_df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
                    hist_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
                    hist_df['time'] = pd.to_datetime(hist_df['time'])
            except Exception as e:
                st.error(f"Error fetching data: {str(e)}")
                hist_df = None

# Auto-load BTC-USD chart on first page load
if not st.session_state.chart_loaded:
    try:
        import yfinance as yf
        ticker = yf.Ticker('BTC-USD')
        hist = ticker.history(period='1y')

        if not hist.empty:
            hist_df = hist.reset_index()
            hist_df = hist_df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            hist_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
            hist_df['time'] = pd.to_datetime(hist_df['time'])
            st.session_state.chart_loaded = True
    except Exception as e:
        hist_df = None

with chart_col:
    if hist_df is not None:
        with st.container():
            chart = StreamlitChart(height = 450, width = 1600)
            chart.grid(vert_enabled = True, horz_enabled = True)

            chart.layout(background_color='#131722', font_family='Trebuchet MS', font_size = 16)

            chart.candle_style(up_color='#2962ff', down_color='#e91e63',
                               border_up_color='#2962ffcb', border_down_color='#e91e63cb',
                               wick_up_color='#2962ffcb', wick_down_color='#e91e63cb')

            chart.volume_config(up_color='#2962ffcb', down_color='#e91e63cb')
            chart.legend(visible = True, font_family = 'Trebuchet MS', ohlc = True, percent = True)

            chart.set(hist_df)
            chart.load()

# Display data grid below chart (outside columns, full width)
if hist_df is not None:
    # Format the dataframe for display
    display_df = hist_df.copy()

    # Format time column to YYYY-MM-DD
    display_df['time'] = pd.to_datetime(display_df['time']).dt.strftime('%Y-%m-%d')

    # Format price columns with $ and thousand commas
    for col in ['open', 'high', 'low', 'close']:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")

    # Format volume column with commas
    display_df['volume'] = display_df['volume'].apply(lambda x: f"{x:,.0f}")

    st.dataframe(display_df, use_container_width=True)