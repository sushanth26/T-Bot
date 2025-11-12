"""API route handlers"""
import asyncio
from fastapi import APIRouter
from config.settings import CACHE, POPULAR_STOCKS
from services.alpaca_service import fetch_stock_data, search_stocks

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Stock Data API - Search any symbol"}


@router.get("/api/search/{query}")
async def search_stocks_endpoint(query: str):
    """Search for stocks by symbol or company name with smart ranking"""
    results = await asyncio.to_thread(search_stocks, query)
    return {"results": results}


@router.get("/api/quotes/{symbol}")
async def get_quote(symbol: str):
    """Get quote for any stock symbol with EMAs (cached for speed)"""
    symbol = symbol.upper()
    
    # Return cached data immediately if available (even if slightly stale)
    if symbol in CACHE:
        # For popular stocks, always return cache instantly
        return CACHE[symbol]
    
    # For new symbols, fetch in background but return quickly
    # Trigger background fetch
    asyncio.create_task(asyncio.to_thread(fetch_stock_data, symbol))
    
    # Return placeholder immediately
    return {
        "symbol": symbol,
        "companyName": f"{symbol} Inc.",
        "exchange": "Loading...",
        "sector": "...",
        "industry": "...",
        "price": 0,
        "bid": 0,
        "ask": 0,
        "bidSize": 0,
        "askSize": 0,
        "timestamp": "",
        "dayHigh": 0,
        "dayLow": 0,
        "week52High": 0,
        "week52Low": 0,
        "emas": {},
        "loading": True
    }


async def prefetch_popular_stocks():
    """Pre-fetch popular stocks on startup for instant switching"""
    print("🔄 Pre-fetching popular stocks...")
    
    for symbol in POPULAR_STOCKS:
        try:
            await asyncio.to_thread(fetch_stock_data, symbol)
            print(f"   ✅ {symbol} cached")
        except Exception as e:
            print(f"   ❌ {symbol} failed: {e}")
    
    print("✅ All popular stocks pre-cached!")


async def background_refresh_popular():
    """Refresh popular stocks every 5 seconds"""
    popular = ["TSLA", "AAPL", "GOOGL", "MSFT", "AMZN", "NVDA"]
    while True:
        await asyncio.sleep(5)
        for symbol in popular:
            try:
                await asyncio.to_thread(fetch_stock_data, symbol)
            except Exception as e:
                print(f"Refresh error {symbol}: {e}")

