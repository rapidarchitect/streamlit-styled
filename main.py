
import streamlit as st
import httpx
import pandas as pd
from lightweight_charts.widgets import StreamlitChart

# ============================================================================
# Crypto Dashboard Application
#
# A professional cryptocurrency dashboard built with Streamlit featuring:
# - Real-time price data for 5 major cryptocurrencies (BTC, ETH, XMR, SOL, XRP)
# - Interactive candlestick charts with lightweight-charts
# - Historical OHLCV data from Yahoo Finance
# - Custom CSS styling with dark theme
# - Responsive layout with price cards and chart parameters
#
# The application fetches real-time prices from the DIA API and historical data
# from yfinance, displaying them in a professional trading dashboard interface.
# ============================================================================

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
# These session state variables persist across Streamlit reruns, preventing
# unnecessary API calls and improving user experience

if "symbols_list" not in st.session_state:
    # Caches the list of available cryptocurrency symbols
    st.session_state.symbols_list = None

if "chart_loaded" not in st.session_state:
    # Tracks whether the initial BTC-USD chart has been loaded to avoid
    # redundant API calls on every page reload
    st.session_state.chart_loaded = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
# Configure Streamlit page layout and visual settings
st.set_page_config(
    layout='wide',  # Use wide layout for better use of horizontal space
    page_title='Crypto Dashboard'
)

# Hide Streamlit's default footer and header to create a cleaner, custom interface
st.markdown(
    """
    <style>
        footer {display: none}
        [data-testid="stHeader"] {display: none}
    </style>
    """, unsafe_allow_html=True
)

# ============================================================================
# CSS STYLING
# ============================================================================
# Load custom CSS from style.css file to apply professional dark theme,
# custom fonts (Space Grotesk), and component-specific styling
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ============================================================================
# DASHBOARD HEADER
# ============================================================================
# Display the main dashboard title using custom CSS class for styling
st.markdown('<p class="dashboard_title">Crypto Dashboard</p>', unsafe_allow_html=True)

# ============================================================================
# PRICE CARDS SECTION
# ============================================================================
# Create 5 equal-width columns for displaying real-time cryptocurrency prices
# Column widths are set to [1, 1, 1, 1, 1] for equal distribution
btc_col, eth_col, xmr_col, sol_col, xrp_col = st.columns([1, 1, 1, 1, 1])

# ============================================================================
# PRICE FETCHING FUNCTION
# ============================================================================
def fetch_price(symbol):
    """
    Fetch real-time cryptocurrency price from DIA API.

    The DIA (Decentralized Information Asset) API provides real-time,
    decentralized price feeds for various cryptocurrencies.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTC/USDT', 'ETH/USDT')

    Returns:
        tuple: (price_string, change_percent)
            - price_string (str): Formatted price as "$X,XXX.XX" or error message
            - change_percent (float): 24-hour change percentage (unused in current UI)

    Raises:
        Returns error messages as strings instead of raising exceptions for
        graceful degradation - cards show "API Error" instead of crashing.
    """
    try:
        # ====================================================================
        # DIA API SYMBOL MAPPING
        # ====================================================================
        # Maps trading symbols to DIA API parameters (blockchain, address)
        # Format: symbol -> (DIA_name, blockchain_address, optional_blockchain)
        # Note: XRP uses XRPL blockchain instead of its name
        dia_symbols = {
            'BTC': ('Bitcoin', '0x0000000000000000000000000000000000000000'),
            'ETH': ('Ethereum', '0x0000000000000000000000000000000000000000'),
            'XMR': ('Monero', '0x0000000000000000000000000000000000000000'),
            'SOL': ('Solana', '0x0000000000000000000000000000000000000000'),
            'XRP': ('XRP', '0x0000000000000000000000000000000000000000', 'XRPL'),
        }

        # Extract base cryptocurrency symbol (BTC from BTC/USDT)
        crypto = symbol.split('/')[0]

        # Validate that the symbol is supported
        if crypto not in dia_symbols:
            return ("Symbol not supported", 0)

        # Extract DIA API parameters
        dia_info = dia_symbols[crypto]
        dia_name = dia_info[0]
        address = dia_info[1]
        blockchain = dia_info[2] if len(dia_info) > 2 else dia_name

        # ====================================================================
        # API REQUEST
        # ====================================================================
        # Query DIA API endpoint for current price data
        # Endpoint format: /v1/assetQuotation/{blockchain}/{address}
        url = f'https://api.diadata.org/v1/assetQuotation/{blockchain}/{address}'
        response = httpx.get(url, timeout=10)

        # Handle HTTP errors
        if response.status_code != 200:
            return ("API Error", 0)

        # Parse JSON response
        data = response.json()

        # ====================================================================
        # PRICE EXTRACTION
        # ====================================================================
        # Extract current price from API response
        price = data.get('Price')
        if price is None:
            return ("Price not available", 0)

        # Extract 24-hour change percentage (for future use in trend indicators)
        change_percent = data.get('Change24h', 0)
        if change_percent is None:
            change_percent = 0

        # Return formatted price string with thousands separator and currency sign
        return (f"${price:,.2f}", change_percent)

    except httpx.TimeoutException:
        # Handle network timeout (10-second limit)
        return ("Request timeout", 0)
    except Exception as e:
        # Catch-all for unexpected errors
        return (f"Error", 0)

# ============================================================================
# BTC PRICE CARD
# ============================================================================
with btc_col:
    # Fetch current BTC price from DIA API
    btc_price, btc_change = fetch_price('BTC/USDT')
    # Determine arrow color based on price change (green for up, red for down)
    arrow = '<span style="color: #00ff00;">▲</span>' if btc_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    # Render price card with custom CSS styling
    st.markdown(f'<div class="price_card"><p class="btc_text">BTC / USDT<br></p><p class="price_details">{btc_price} {arrow}</p></div>', unsafe_allow_html=True)

# ============================================================================
# ETH PRICE CARD
# ============================================================================
with eth_col:
    eth_price, eth_change = fetch_price('ETH/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if eth_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="eth_text">ETH / USDT<br></p><p class="price_details">{eth_price} {arrow}</p></div>', unsafe_allow_html=True)

# ============================================================================
# XMR PRICE CARD
# ============================================================================
with xmr_col:
    xmr_price, xmr_change = fetch_price('XMR/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if xmr_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="xmr_text">XMR / USDT<br></p><p class="price_details">{xmr_price} {arrow}</p></div>', unsafe_allow_html=True)

# ============================================================================
# SOL PRICE CARD
# ============================================================================
with sol_col:
    sol_price, sol_change = fetch_price('SOL/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if sol_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="sol_text">SOL / USDT<br></p><p class="price_details">{sol_price} {arrow}</p></div>', unsafe_allow_html=True)

# ============================================================================
# XRP PRICE CARD
# ============================================================================
with xrp_col:
    xrp_price, xrp_change = fetch_price('XRP/USDT')
    arrow = '<span style="color: #00ff00;">▲</span>' if xrp_change >= 0 else '<span style="color: #ff0000;">▼</span>'
    st.markdown(f'<div class="price_card"><p class="xrp_text">XRP / USDT<br></p><p class="price_details">{xrp_price} {arrow}</p></div>', unsafe_allow_html=True)

# ============================================================================
# SPACING
# ============================================================================
# Add vertical spacing between price cards section and chart section
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# ============================================================================
# CHART SECTION LAYOUT
# ============================================================================
# Create two columns: parameters panel (45%) and chart (155%)
# This creates a 0.45:1.55 ratio for optimal layout
params_col, chart_col = st.columns([0.45, 1.55])

# Initialize dataframe variable (will hold OHLCV data if fetched successfully)
hist_df = None

# ============================================================================
# PARAMETERS PANEL (Left Column)
# ============================================================================
with params_col:
    # Create a form to capture user input for chart parameters
    # Forms prevent rerunning the entire script on each input change
    with st.form(key='params_form'):
        # Panel header
        st.markdown('<p class="params_text">CHART DATA PARAMETERS', unsafe_allow_html=True)
        st.divider()

        # ====================================================================
        # SYMBOL SELECTION
        # ====================================================================
        # List of supported cryptocurrency trading pairs for yfinance
        # Note: These use Yahoo Finance ticker symbols (e.g., BTC-USD not BTC/USD)
        symbols = [
            'BTC-USD', 'ETH-USD', 'XMR-USD', 'SOL-USD', 'XRP-USD',
            'ADA-USD', 'DOGE-USD', 'LTC-USD', 'AVAX-USD', 'MATIC-USD'
        ]
        symbol = st.selectbox('Symbol', symbols, key='symbol_selectbox')

        # ====================================================================
        # INTERVAL AND PERIOD SELECTION
        # ====================================================================
        # Create two columns for compact layout of interval and period inputs
        interval_col, period_col = st.columns(2)

        with interval_col:
            # Time interval between candlesticks (1 minute to 1 day)
            interval = st.selectbox(
                'Interval',
                ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '12h', '1d'],
                key='interval_selectbox'
            )

        with period_col:
            # Number of candlesticks to display (10-500)
            # Default of 365 shows approximately 1 year of daily data
            period = st.number_input(
                'Period',
                min_value=10,
                max_value=500,
                value=365,
                step=1,
                key='period_no_input'
            )

        # Spacing
        st.markdown('')

        # Submit button - only triggers form submission when clicked
        update_chart = st.form_submit_button('Update chart')

        st.markdown('')

        # ====================================================================
        # CHART UPDATE LOGIC
        # ====================================================================
        if update_chart:
            try:
                # Symbol is already in correct Yahoo Finance format from selectbox
                symbol_yf = symbol

                # Fetch historical OHLCV data from yfinance
                # DIA API only provides current prices, not historical data
                import yfinance as yf
                ticker = yf.Ticker(symbol_yf)
                hist = ticker.history(period='1y')

                # Validate that data was returned
                if hist.empty:
                    st.error(f"No data found for {symbol}")
                    hist_df = None
                else:
                    # Transform dataframe to match lightweight-charts requirements
                    hist_df = hist.reset_index()
                    # Keep only OHLCV columns
                    hist_df = hist_df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
                    # Rename to lowercase column names expected by chart library
                    hist_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
                    # Ensure time column is datetime format
                    hist_df['time'] = pd.to_datetime(hist_df['time'])
            except Exception as e:
                # Display error message to user
                st.error(f"Error fetching data: {str(e)}")
                hist_df = None

# ============================================================================
# AUTO-LOAD DEFAULT CHART
# ============================================================================
# Load BTC-USD chart on first page load to provide immediate data to user
# Uses session state to prevent reloading on every Streamlit rerun
if not st.session_state.chart_loaded:
    try:
        import yfinance as yf
        ticker = yf.Ticker('BTC-USD')
        hist = ticker.history(period='1y')

        # Validate that data was fetched successfully
        if not hist.empty:
            # Transform dataframe to match chart requirements
            hist_df = hist.reset_index()
            hist_df = hist_df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            hist_df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
            hist_df['time'] = pd.to_datetime(hist_df['time'])

            # Mark that initial chart has been loaded to prevent redundant API calls
            st.session_state.chart_loaded = True
    except Exception as e:
        # Silently fail - chart will show message when data is available
        hist_df = None

# ============================================================================
# CHART DISPLAY (Right Column)
# ============================================================================
with chart_col:
    # Only render chart if historical data is available
    if hist_df is not None:
        with st.container():
            # ================================================================
            # CHART INITIALIZATION
            # ================================================================
            # Create lightweight-charts candlestick chart widget
            chart = StreamlitChart(height=450, width=1600)

            # ================================================================
            # GRID CONFIGURATION
            # ================================================================
            # Enable both vertical and horizontal gridlines for easier reading
            chart.grid(vert_enabled=True, horz_enabled=True)

            # ================================================================
            # LAYOUT CONFIGURATION
            # ================================================================
            # Set dark theme background color and typography
            # Dark background (#131722) matches professional trading interfaces
            chart.layout(
                background_color='#131722',
                font_family='Trebuchet MS',
                font_size=16
            )

            # ================================================================
            # CANDLESTICK STYLING
            # ================================================================
            # Configure colors for up/down candlesticks and wicks
            # Up color: Blue (#2962ff) | Down color: Pink/Red (#e91e63)
            chart.candle_style(
                up_color='#2962ff',
                down_color='#e91e63',
                border_up_color='#2962ffcb',
                border_down_color='#e91e63cb',
                wick_up_color='#2962ffcb',
                wick_down_color='#e91e63cb'
            )

            # ================================================================
            # VOLUME CONFIGURATION
            # ================================================================
            # Color volume bars to match candlestick colors
            chart.volume_config(
                up_color='#2962ffcb',
                down_color='#e91e63cb'
            )

            # ================================================================
            # LEGEND CONFIGURATION
            # ================================================================
            # Display legend with OHLC prices and percentage change
            chart.legend(
                visible=True,
                font_family='Trebuchet MS',
                ohlc=True,  # Show Open, High, Low, Close values
                percent=True  # Show percentage change
            )

            # ================================================================
            # DATA BINDING AND RENDERING
            # ================================================================
            # Set the dataframe and render the chart
            chart.set(hist_df)
            chart.load()

# ============================================================================
# DATA GRID DISPLAY
# ============================================================================
# Display OHLCV data in table format below the chart (full width, outside columns)
if hist_df is not None:
    # Create a copy for display to avoid modifying original data
    display_df = hist_df.copy()

    # ====================================================================
    # FORMAT TIME COLUMN
    # ====================================================================
    # Convert datetime to user-friendly YYYY-MM-DD format
    display_df['time'] = pd.to_datetime(display_df['time']).dt.strftime('%Y-%m-%d')

    # ====================================================================
    # FORMAT PRICE COLUMNS
    # ====================================================================
    # Format prices with dollar sign and thousands separator
    # Example: 43250.5 becomes "$43,250.50"
    for col in ['open', 'high', 'low', 'close']:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}")

    # ====================================================================
    # FORMAT VOLUME COLUMN
    # ====================================================================
    # Format volume with thousands separator for readability
    # Example: 1234567 becomes "1,234,567"
    display_df['volume'] = display_df['volume'].apply(lambda x: f"{x:,.0f}")

    # ====================================================================
    # RENDER DATA TABLE
    # ====================================================================
    # Display formatted dataframe as interactive table
    # use_container_width=True makes table span full page width
    st.dataframe(display_df, use_container_width=True)