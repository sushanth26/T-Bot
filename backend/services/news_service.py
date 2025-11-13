"""News fetching service"""
import requests
from datetime import datetime, timedelta
from config.settings import POLYGON_API_KEY, NEWS_CACHE, NEWS_CACHE_DURATION


def is_top_news(title: str, description: str) -> bool:
    """Determine if news is 'top news' (upgrades, downgrades, earnings, major events)"""
    text = (title + ' ' + description).lower()
    
    # Keywords for top news
    top_keywords = [
        'upgrade', 'upgrades', 'upgraded',
        'downgrade', 'downgrades', 'downgraded',
        'rating', 'ratings', 'price target',
        'earnings', 'earnings beat', 'earnings miss',
        'analyst', 'analysts',
        'buy rating', 'sell rating', 'hold rating',
        'outperform', 'underperform',
        'bullish', 'bearish',
        'initiate coverage', 'initiated coverage',
        'raises price target', 'lowers price target',
        'overweight', 'underweight',
        'strong buy', 'strong sell'
    ]
    
    return any(keyword in text for keyword in top_keywords)


def fetch_news_for_symbol(symbol: str) -> dict:
    """Fetch news for a symbol from Polygon.io API and categorize into top news and regular news"""
    top_news = []
    regular_news = []
    
    # NEWS API ENABLED FOR GROK INTEGRATION
    
    if not POLYGON_API_KEY:
        print(f"   ⚠️  Polygon API key not configured")
        return {'top_news': top_news, 'regular_news': regular_news}
    
    try:
        # Calculate date for last 7 days
        seven_days_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Polygon.io ticker news endpoint with date filter
        # Free tier: 5 requests/minute, 100 results max
        news_url = f"https://api.polygon.io/v2/reference/news?ticker={symbol}&published_utc.gte={seven_days_ago}&limit=50&order=desc&apiKey={POLYGON_API_KEY}"
        news_response = requests.get(news_url, timeout=10)
        
        if news_response.status_code == 200:
            news_data = news_response.json()
            
            # Polygon response format: {"status": "OK", "results": [...]}
            if news_data.get('status') == 'OK' and 'results' in news_data:
                articles = news_data['results']
                
                for article in articles:
                    news_item = {
                        'title': article.get('title', ''),
                        'description': article.get('description', '')[:150] if article.get('description') else '',
                        'url': article.get('article_url', ''),
                        'published_at': article.get('published_utc', ''),
                        'source': article.get('publisher', {}).get('name', 'Unknown'),
                    }
                    
                    # Categorize as top news or regular news
                    if is_top_news(news_item['title'], news_item['description']):
                        top_news.append(news_item)
                    else:
                        regular_news.append(news_item)
                
                print(f"   📰 Fetched {len(articles)} articles (last 7 days): {len(top_news)} top news, {len(regular_news)} regular")
            elif news_data.get('status') == 'ERROR':
                error_msg = news_data.get('error', 'Unknown error')
                print(f"   ⚠️  Polygon API error: {error_msg}")
            else:
                print(f"   ℹ️  No news articles available")
        elif news_response.status_code == 403:
            print(f"   ⚠️  Polygon API: Invalid or missing API key")
        elif news_response.status_code == 429:
            print(f"   ⚠️  Polygon API: Rate limit exceeded (5 req/min free tier)")
        else:
            print(f"   ⚠️  Polygon API HTTP {news_response.status_code}")
    except Exception as e:
        print(f"   ⚠️  News fetch error: {e}")
    
    return {'top_news': top_news, 'regular_news': regular_news}


def get_cached_news(symbol: str) -> dict:
    """Get news from cache or fetch if needed (only refresh every 10 minutes)"""
    news_data = {'top_news': [], 'regular_news': []}
    current_time = datetime.now()
    
    # Check if we have cached news that's still fresh
    if symbol in NEWS_CACHE:
        cache_entry = NEWS_CACHE[symbol]
        cache_age = (current_time - cache_entry['timestamp']).total_seconds()
        
        if cache_age < NEWS_CACHE_DURATION:
            # Use cached news
            news_data = cache_entry['news']
            print(f"   News: Using cache ({int(NEWS_CACHE_DURATION - cache_age)}s remaining)")
        else:
            # Cache expired, fetch new news
            news_data = fetch_news_for_symbol(symbol)
            NEWS_CACHE[symbol] = {
                'news': news_data,
                'timestamp': current_time
            }
    else:
        # No cache, fetch news
        news_data = fetch_news_for_symbol(symbol)
        NEWS_CACHE[symbol] = {
            'news': news_data,
            'timestamp': current_time
        }
    
    return news_data

