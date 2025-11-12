"""Configuration and constants for the application"""
import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST

load_dotenv()

# API Keys
API_KEY = os.getenv("ALPACA_API_KEY", "")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY", "")  # Free tier: 5 requests/minute

# Alpaca API Clients
rest_api = REST(
    key_id=API_KEY,
    secret_key=SECRET_KEY,
    base_url="https://paper-api.alpaca.markets",
    api_version='v2'
)

data_api = REST(
    key_id=API_KEY,
    secret_key=SECRET_KEY,
    base_url="https://data.alpaca.markets",
    api_version='v2'
)

# Cache configuration
CACHE = {}
NEWS_CACHE = {}
NEWS_CACHE_DURATION = 600  # 10 minutes in seconds

# Popular stocks for pre-fetching
POPULAR_STOCKS = ["TSLA", "AAPL", "GOOGL", "MSFT", "AMZN", "NVDA", "META", "NFLX", "AMD", "COIN"]
REFRESH_INTERVAL = 5  # seconds

