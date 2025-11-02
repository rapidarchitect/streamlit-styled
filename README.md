# Crypto Dashboard with Custom CSS in Streamlit

A Streamlit-based cryptocurrency dashboard featuring real-time crypto price data with custom CSS styling. This project demonstrates how to create a professional-looking dashboard using Streamlit with custom fonts, colors, and layouts.

## Features

- **Real-time Crypto Prices**: Display live prices for BTC, ETH, XMR, SOL, and XRP
- **Custom Styling**: Professional design using Space Grotesk font and custom CSS
- **Responsive Layout**: Wide layout with multiple columns for price cards
- **Error Handling**: Graceful error handling for API calls
- **TAAPI.IO Integration**: Uses TAAPI.IO API for real-time cryptocurrency pricing

## Technology Stack

- **Frontend Framework**: Streamlit
- **HTTP Client**: httpx (async-capable HTTP client)
- **Styling**: Custom CSS with Space Grotesk font
- **API**: TAAPI.IO Cryptocurrency Pricing API

## Installation

### Prerequisites
- Python 3.11+
- An API key from [TAAPI.IO](https://taapi.io)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd streamlit_css
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

Or using uv:
```bash
uv sync
```

## Configuration

### API Key Setup

1. Sign up for a free account at [TAAPI.IO](https://taapi.io)
2. Get your API key from the dashboard
3. Update `main.py` line 23:
```python
api_key = 'YOUR_ACTUAL_TAAPI_IO_API_KEY'
```

Alternatively, use environment variables for security:
```python
import os
api_key = os.getenv('TAAPI_API_KEY', 'YOUR TAAPI.IO API KEY')
```

## Running the Application

Start the Streamlit development server:
```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
.
├── main.py                    # Main dashboard application
├── style.css                  # Custom CSS styling
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Project configuration
├── README.md                 # This file
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── .gitignore               # Git ignore rules
```

## Dashboard Components

### Header
- **Dashboard Title**: Large, bold title with custom font styling
- **Empty Column**: Spacing between title and price cards

### Price Cards
Five cryptocurrency price cards displaying:
- **BTC (Bitcoin)**: Orange color (#f7931a)
- **ETH (Ethereum)**: Gray color (#a1a1a1)
- **XMR (Monero)**: Orange color (#ff6b08)
- **SOL (Solana)**: Purple color (#807af4)
- **XRP (Ripple)**: Blue color (#01acf1)

Each card shows:
- Cryptocurrency symbol and trading pair
- Current price in USDT
- Custom styling with borders, shadows, and rounded corners

## Styling Details

### Colors
- **Background**: Dark theme (#0c0e15)
- **Primary Text**: Light gray (#f6f6f6)
- **Accent Colors**: Individual colors per cryptocurrency
- **Border Color**: Dark gray (#52546a)

### Typography
- **Font Family**: Space Grotesk (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Dashboard Title**: 35px, weight 700
- **Price Details**: 30px, weight 900
- **Crypto Labels**: 14px, weight bold

### Layout
- **Columns**: 7 columns (1 title, 0.2 spacer, 5 crypto cards)
- **Width**: Full container width with custom padding
- **Padding**: 5rem left/right, 15px top, 40px bottom
- **Container Styling**: Border groove, border-radius 10px, box-shadow

## API Reference

### TAAPI.IO Endpoint
```
GET https://api.taapi.io/price
Parameters:
  - secret: Your API key
  - exchange: Exchange name (e.g., binance)
  - symbol: Trading pair (e.g., BTC/USDT)
  - interval: Time interval (1m for 1 minute)
```

### Example Response
```json
{
  "value": "43250.50"
}
```

## Error Handling

The application includes try-except blocks for each price card to handle:
- API connection failures
- Invalid API keys
- Rate limiting
- Network timeouts

When an error occurs, the card displays "API Error" instead of crashing.

## Customization

### Adding More Cryptocurrencies
1. Add a new column in the columns definition
2. Create a new `with <crypto>_col:` block
3. Update the API call with the new symbol
4. Add corresponding CSS styling

### Changing Colors
Edit the color hex values in `style.css`:
- `.btc_text`, `.eth_text`, `.xmr_text`, `.sol_text`, `.xrp_text`

### Modifying Layout
Edit `st.columns()` parameters in `main.py` to adjust column widths.

## Performance Notes

- **Caching**: Consider adding `@st.cache_data` decorator to cache API responses
- **Refresh Rate**: Streamlit reruns the entire script on interaction. To limit API calls, use caching.
- **API Rate Limits**: Check TAAPI.IO documentation for rate limiting details

## Future Enhancements

- Add price charts using lightweight-charts
- Include historical price data and trends
- Implement price change indicators (up/down arrows)
- Add more cryptocurrencies
- Create alerts for price thresholds
- Add portfolio tracking functionality
- Export price data to CSV
- Dark/light theme toggle

## Security

- Never commit your API key to version control
- Use environment variables for sensitive data
- Store API keys in `.env` file (add to `.gitignore`)

## Troubleshooting

### "API Error" displayed for all cryptocurrencies
- Check your API key is correct
- Verify TAAPI.IO account is active
- Check your internet connection
- Review TAAPI.IO dashboard for any service issues

### Custom CSS not loading
- Ensure `style.css` is in the same directory as `main.py`
- Check file name matches exactly
- Clear browser cache and reload

### Streamlit not starting
- Verify all dependencies are installed: `pip list`
- Check Python version: `python --version` (requires 3.11+)
- Try: `streamlit cache clear && streamlit run main.py`

## License

© 2024 Crypto Dashboard Project. Based on the InsightBig tutorial.

## References

- [Streamlit Documentation](https://docs.streamlit.io)
- [TAAPI.IO API Docs](https://taapi.io/documentation)
- [Space Grotesk Font](https://fonts.google.com/specimen/Space+Grotesk)
- [InsightBig Tutorial](https://www.insightbig.com/post/creating-a-crypto-dashboard-with-custom-css-in-streamlit)

## Support

For issues or questions, refer to the [Streamlit community forum](https://discuss.streamlit.io) or check the TAAPI.IO documentation.
