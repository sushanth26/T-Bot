"""Alpaca API service for fetching stock data"""
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from config.settings import rest_api, data_api, CACHE
from services.ema_service import get_all_emas
from services.news_service import get_cached_news
from services.crossover_service import detect_premarket_crossovers
from services.premarket_service import get_premarket_levels
from services.grok_service import get_cached_grok_analysis


def get_company_info(symbol: str) -> dict:
    """Fetch company information from Alpaca Assets API"""
    company_data = {
        'companyName': None,
        'exchange': None,
        'sector': None,
        'industry': None,
        'logoUrl': None
    }
    
    try:
        asset = rest_api.get_asset(symbol)
        
        company_data['companyName'] = asset.name if hasattr(asset, 'name') else None
        company_data['exchange'] = asset.exchange if hasattr(asset, 'exchange') else None
        
        # Asset class can give us some industry info
        if hasattr(asset, 'asset_class'):
            company_data['industry'] = asset.asset_class.replace('_', ' ').title() if asset.asset_class else None
        
        # Try to get logo from Alpaca Logo API (paid feature)
        if hasattr(asset, 'logo_url') and asset.logo_url:
            company_data['logoUrl'] = asset.logo_url
        elif company_data['companyName']:
            # Fallback: Auto-generate Clearbit logo URL from company name
            first_word = company_data['companyName'].replace(',', '').replace('.', '').split()[0].lower()
            
            if first_word and len(first_word) > 2:
                company_data['logoUrl'] = f"https://logo.clearbit.com/{first_word}.com"
                print(f"   Logo generated: {first_word}.com")
        
        print(f"   Company: {company_data['companyName']} | {company_data['exchange']}")
                
    except Exception as e:
        print(f"   ⚠️  Asset info fetch error: {e}")
    
    return company_data


def get_current_price(symbol: str) -> dict:
    """Get current price and quote data"""
    try:
        trade = rest_api.get_latest_trade(symbol)
        quote = rest_api.get_latest_quote(symbol)
        
        return {
            'price': float(trade.price) if trade and trade.price else 0,
            'bid': float(quote.bid_price) if quote.bid_price else 0,
            'ask': float(quote.ask_price) if quote.ask_price else 0,
            'bidSize': int(quote.bid_size) if quote.bid_size else 0,
            'askSize': int(quote.ask_size) if quote.ask_size else 0,
            'timestamp': str(trade.timestamp) if trade and trade.timestamp else ""
        }
    except Exception as e:
        print(f"⚠️  Price fetch error: {e}")
        return {'price': 0, 'bid': 0, 'ask': 0, 'bidSize': 0, 'askSize': 0, 'timestamp': ''}


def get_day_range(symbol: str, current_price: float) -> dict:
    """Get today's high and low"""
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        today_bars = data_api.get_bars(
            symbol,
            TimeFrame.Minute,
            start=today,
            end=today,
            feed='iex'
        ).df
        
        if not today_bars.empty:
            return {
                'dayHigh': float(today_bars['high'].max()),
                'dayLow': float(today_bars['low'].min())
            }
        else:
            print(f"⚠️  No intraday data available for day range")
            return {'dayHigh': current_price, 'dayLow': current_price}
    except Exception as e:
        print(f"⚠️  Day range error: {e}")
        return {'dayHigh': current_price, 'dayLow': current_price}


def get_52week_range(symbol: str, current_price: float) -> dict:
    """Get 52-week high and low"""
    try:
        end_52w = datetime.now()
        start_52w = end_52w - timedelta(days=365)
        
        bars_52w = data_api.get_bars(
            symbol,
            TimeFrame.Day,
            start=start_52w.strftime("%Y-%m-%d"),
            end=end_52w.strftime("%Y-%m-%d"),
            feed='iex'
        ).df
        
        if not bars_52w.empty:
            return {
                'week52High': float(bars_52w['high'].max()),
                'week52Low': float(bars_52w['low'].min())
            }
        else:
            print(f"⚠️  No 52-week data available")
            return {'week52High': current_price, 'week52Low': current_price}
    except Exception as e:
        print(f"⚠️  52wk range error: {e}")
        return {'week52High': current_price, 'week52Low': current_price}


def fetch_stock_data(symbol: str):
    """Main function to fetch all stock data from Alpaca API"""
    try:
        # Get company info
        company_info = get_company_info(symbol)
        
        # Get current price
        price_data = get_current_price(symbol)
        price = price_data['price']
        
        # Get day range
        day_range = get_day_range(symbol, price)
        
        # Get 52-week range
        week_range = get_52week_range(symbol, price)
        
        # Get all EMAs
        emas = get_all_emas(symbol)
        
        # Get premarket high/low
        premarket_levels = get_premarket_levels(symbol)
        
        # Build result
        result = {
            "symbol": symbol,
            "companyName": company_info['companyName'],
            "exchange": company_info['exchange'],
            "sector": company_info['sector'],
            "industry": company_info['industry'],
            "price": price,
            "bid": price_data['bid'],
            "ask": price_data['ask'],
            "bidSize": price_data['bidSize'],
            "askSize": price_data['askSize'],
            "timestamp": price_data['timestamp'],
            "dayHigh": round(day_range['dayHigh'], 2),
            "dayLow": round(day_range['dayLow'], 2),
            "week52High": round(week_range['week52High'], 2),
            "week52Low": round(week_range['week52Low'], 2),
            "emas": emas,
            "premarketLevels": premarket_levels,  # PMH and PML
            "pivots": {},  # Pivots commented out for now
            "logoUrl": company_info['logoUrl']
        }
        
        # Get news (cached) - returns dict with top_news and regular_news
        news_data = get_cached_news(symbol)
        result["topNews"] = news_data.get('top_news', [])
        result["news"] = news_data.get('regular_news', [])
        
        # Get Grok AI analysis of news (if news available)
        grok_analysis = {}
        if news_data.get('top_news') or news_data.get('regular_news'):
            grok_analysis = get_cached_grok_analysis(symbol, news_data)
        result["grokAnalysis"] = grok_analysis
        
        # Detect premarket EMA crossovers
        crossovers = detect_premarket_crossovers(symbol, price, emas)
        result["crossovers"] = crossovers
        
        # Cache the result
        CACHE[symbol] = result
        
        # Log summary
        logo_status = "🖼️" if company_info['logoUrl'] else "⚡"
        crossover_status = f" | 🚨{len(crossovers)} alerts" if crossovers else ""
        top_news_count = len(news_data.get('top_news', []))
        regular_news_count = len(news_data.get('regular_news', []))
        pm_status = f" | PMH/PML: {len(premarket_levels)}" if premarket_levels else ""
        grok_status = f" | 🤖 Grok: {grok_analysis.get('sentiment', 'N/A')}" if grok_analysis else ""
        print(f"✅ {symbol} ${price} {logo_status} | Range: {day_range['dayLow']:.2f}-{day_range['dayHigh']:.2f} | EMAs: {len(emas)}{pm_status} | News: {top_news_count}/{regular_news_count}{grok_status}{crossover_status}")
        
        return result
    except Exception as e:
        print(f"❌ {symbol} Error: {e}")
        return {"symbol": symbol, "error": str(e)}


def search_stocks(query: str) -> list:
    """Search for stocks by symbol or company name"""
    try:
        assets = rest_api.list_assets(status='active', asset_class='us_equity')
        
        query_upper = query.upper()
        query_lower = query.lower()
        
        exact_matches = []
        starts_with = []
        contains = []
        
        for asset in assets:
            symbol_upper = asset.symbol.upper()
            name_lower = asset.name.lower()
            
            # Priority 1: Exact symbol match
            if symbol_upper == query_upper:
                exact_matches.append({
                    'symbol': asset.symbol,
                    'name': asset.name,
                    'exchange': asset.exchange,
                })
            # Priority 2: Symbol starts with query
            elif symbol_upper.startswith(query_upper):
                starts_with.append({
                    'symbol': asset.symbol,
                    'name': asset.name,
                    'exchange': asset.exchange,
                })
            # Priority 3: Company name starts with query or contains it
            elif name_lower.startswith(query_lower) or query_lower in name_lower:
                contains.append({
                    'symbol': asset.symbol,
                    'name': asset.name,
                    'exchange': asset.exchange,
                })
        
        # Combine results with priority order
        matches = exact_matches + starts_with[:5] + contains[:5]
        return matches[:10]  # Limit to 10 total suggestions
    except Exception as e:
        print(f"Search error: {e}")
        return []

