"""API route handlers"""
import asyncio
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from config.settings import CACHE, POPULAR_STOCKS
from services.alpaca_service import fetch_stock_data, search_stocks
from services.grok_service import stream_grok_analysis
from services.news_service import fetch_news_for_symbol
from services.sector_service import get_sector_info
from services.sector_analysis_service import analyze_sector_position

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


@router.get("/api/grok/stream/{symbol}")
async def stream_grok_endpoint(symbol: str):
    """Stream Grok AI analysis in real-time with sector context"""
    symbol = symbol.upper()
    
    try:
        # Fetch news for the symbol
        news_data = await asyncio.to_thread(fetch_news_for_symbol, symbol)
        top_news = news_data.get('top_news', [])
        regular_news = news_data.get('regular_news', [])
        
        # Get sector information and weightage
        sector_info = await asyncio.to_thread(get_sector_info, symbol)
        sector = sector_info.get('sector', 'Unknown')
        sector_weight = sector_info.get('weightage', 0.0)
        
        # Stream the Grok analysis
        return StreamingResponse(
            stream_grok_analysis(symbol, regular_news, top_news, sector, sector_weight),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no",
                "Connection": "keep-alive",
            }
        )
    
    except Exception as e:
        return {"error": str(e)}


@router.get("/api/sector/analyze/{symbol}")
async def sector_analysis_endpoint(
    symbol: str,
    etf: str = Query(None, description="ETF symbol to analyze position in (e.g., SOXX, XLK)")
):
    """
    Get comprehensive sector analysis for a stock
    
    Example: /api/sector/analyze/NVDA?etf=SOXX
    
    Returns:
    - Stock's weight in ETF (if ETF specified)
    - P/E ratio and other financial metrics
    - 5 stocks with lowest P/E in the same sector
    
    Requires: FMP_API_KEY environment variable
    """
    symbol = symbol.upper()
    
    if etf:
        etf = etf.upper()
    
    try:
        # Run sector analysis in background thread
        analysis = await asyncio.to_thread(analyze_sector_position, symbol, etf)
        return analysis
    
    except Exception as e:
        return {"error": str(e), "symbol": symbol}


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

