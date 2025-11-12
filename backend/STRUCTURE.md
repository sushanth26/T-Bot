# Backend Code Structure

## Overview
The backend has been refactored from a single monolithic `server.py` file into a modular, organized structure following best practices.

## Directory Structure

```
backend/
├── server.py              # Main FastAPI application (entry point)
├── config/
│   ├── __init__.py
│   └── settings.py        # Configuration, API keys, constants
├── services/
│   ├── __init__.py
│   ├── alpaca_service.py  # Main stock data fetching
│   ├── ema_service.py     # EMA calculations
│   ├── crossover_service.py  # Premarket crossover detection
│   └── news_service.py    # News fetching from Marketaux
├── api/
│   ├── __init__.py
│   └── routes.py          # API endpoint definitions
└── utils/
    └── __init__.py
```

## File Descriptions

### `server.py` (Entry Point)
- Initializes FastAPI application
- Sets up CORS middleware
- Registers API routes
- Handles startup events (pre-fetching popular stocks)
- **Lines of code:** ~40 (reduced from 667!)

### `config/settings.py`
Contains all configuration and shared resources:
- API keys (Alpaca, Marketaux)
- Alpaca REST API clients (`rest_api`, `data_api`)
- Cache dictionaries (`CACHE`, `NEWS_CACHE`)
- Constants (popular stocks list, cache durations)

### `services/alpaca_service.py`
Main service for interacting with Alpaca API:
- `get_company_info()` - Fetch company details and logo
- `get_current_price()` - Get latest price and quote data
- `get_day_range()` - Fetch today's high/low
- `get_52week_range()` - Fetch 52-week high/low
- `fetch_stock_data()` - Main function orchestrating all data fetching
- `search_stocks()` - Stock symbol/name search with smart ranking

### `services/ema_service.py`
EMA (Exponential Moving Average) calculations:
- `calculate_real_ema()` - Core EMA calculation from pandas Series
- `get_daily_emas()` - Fetch and calculate daily 20 & 50 EMAs
- `get_hourly_emas()` - Fetch and calculate hourly 34 & 50 EMAs
- `get_10min_emas()` - Fetch and calculate 10-minute 9, 34 & 50 EMAs
- `get_all_emas()` - Orchestrates fetching all EMAs

### `services/crossover_service.py`
Premarket EMA crossover detection:
- `detect_premarket_crossovers()` - Detects when price crosses above/below Daily & Hourly EMAs during premarket hours (4:00-9:30 AM ET)
- Uses Friday's data for testing when markets are closed
- Only alerts on actual touches/crosses (not just position)

### `services/news_service.py`
News fetching with caching:
- `fetch_news_for_symbol()` - Fetches news from Marketaux API (last 7 days)
- `get_cached_news()` - Returns cached news or fetches new if cache expired (10-minute cache)

### `api/routes.py`
API endpoint definitions:
- `GET /` - Root endpoint
- `GET /api/search/{query}` - Search stocks by symbol/name
- `GET /api/quotes/{symbol}` - Get stock quote with EMAs, news, crossovers
- `prefetch_popular_stocks()` - Pre-cache popular stocks on startup
- `background_refresh_popular()` - Continuously refresh popular stocks every 5 seconds

## Benefits of This Structure

1. **Separation of Concerns**: Each service has a single, well-defined responsibility
2. **Maintainability**: Easy to find and modify specific functionality
3. **Testability**: Individual services can be tested independently
4. **Scalability**: Easy to add new services or extend existing ones
5. **Readability**: Much easier to understand than a 667-line monolithic file
6. **Reusability**: Services can be imported and used in other parts of the application

## How to Run

```bash
cd backend
source venv/bin/activate
python server.py
```

## Migration Notes

- Old server preserved as `server_old.py` (can be deleted once confirmed working)
- All functionality remains identical
- API endpoints unchanged
- Cache behavior unchanged

## Future Enhancements

Potential additions to `utils/`:
- `utils/cache.py` - Cache management utilities
- `utils/validators.py` - Input validation functions
- `utils/formatters.py` - Data formatting utilities

