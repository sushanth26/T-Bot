"""Grok AI service for news analysis"""
import requests
import os
from config.settings import CACHE


def analyze_news_with_grok(symbol: str, news_articles: list, top_news: list) -> dict:
    """Use Grok to analyze news and provide trading insights"""
    
    # Get Grok API key from environment
    grok_api_key = os.getenv("GROK_API_KEY", "")
    
    if not grok_api_key:
        print(f"   ⚠️  Grok API key not configured")
        return {
            'summary': 'Grok API key not configured',
            'sentiment': 'neutral',
            'key_points': [],
            'trading_signals': []
        }
    
    if not news_articles and not top_news:
        return {
            'summary': 'No news available for analysis',
            'sentiment': 'neutral',
            'key_points': [],
            'trading_signals': []
        }
    
    try:
        # Prepare news text for Grok
        news_text = ""
        
        if top_news:
            news_text += "TOP NEWS (Analyst Ratings/Upgrades):\n"
            for i, article in enumerate(top_news[:5], 1):
                news_text += f"{i}. {article.get('title', '')}\n"
                if article.get('description'):
                    news_text += f"   {article.get('description', '')[:100]}...\n"
            news_text += "\n"
        
        if news_articles:
            news_text += "RECENT NEWS:\n"
            for i, article in enumerate(news_articles[:10], 1):
                news_text += f"{i}. {article.get('title', '')}\n"
        
        # Create prompt for Grok
        prompt = f"""Analyze these news articles about {symbol} stock and provide:

1. Overall Sentiment (bullish/bearish/neutral)
2. Summary (2-3 sentences)
3. Key Points (3-5 bullet points)
4. Trading Signals (buy/sell/hold with reasoning)

News Articles:
{news_text}

Respond in JSON format:
{{
  "sentiment": "bullish/bearish/neutral",
  "summary": "brief summary",
  "key_points": ["point 1", "point 2", "point 3"],
  "trading_signals": ["signal 1", "signal 2"],
  "confidence": "high/medium/low"
}}"""

        # Call Grok API (xAI API endpoint)
        headers = {
            "Authorization": f"Bearer {grok_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "grok-beta",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a financial analyst providing concise stock trading insights based on news."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract the response
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON response
                import json
                try:
                    analysis = json.loads(content)
                    print(f"   🤖 Grok analysis: {analysis.get('sentiment', 'N/A')} sentiment, {analysis.get('confidence', 'N/A')} confidence")
                    return analysis
                except json.JSONDecodeError:
                    # Fallback if not JSON
                    return {
                        'summary': content[:200],
                        'sentiment': 'neutral',
                        'key_points': [content[:100]],
                        'trading_signals': [],
                        'confidence': 'low'
                    }
        elif response.status_code == 401:
            print(f"   ⚠️  Grok API: Invalid API key")
        elif response.status_code == 429:
            print(f"   ⚠️  Grok API: Rate limit exceeded")
        else:
            print(f"   ⚠️  Grok API HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ⚠️  Grok analysis error: {e}")
    
    return {
        'summary': 'Analysis unavailable',
        'sentiment': 'neutral',
        'key_points': [],
        'trading_signals': [],
        'confidence': 'low'
    }


def get_cached_grok_analysis(symbol: str, news_data: dict) -> dict:
    """Get Grok analysis from cache or generate new one"""
    
    # Check if we have recent Grok analysis in cache
    cache_key = f"{symbol}_grok_analysis"
    
    if cache_key in CACHE:
        cached = CACHE[cache_key]
        # Return cached analysis if less than 30 minutes old
        from datetime import datetime
        if (datetime.now() - cached.get('timestamp', datetime.min)).total_seconds() < 1800:
            print(f"   🤖 Using cached Grok analysis")
            return cached.get('analysis', {})
    
    # Generate new analysis
    top_news = news_data.get('top_news', [])
    regular_news = news_data.get('regular_news', [])
    
    analysis = analyze_news_with_grok(symbol, regular_news, top_news)
    
    # Cache the analysis
    from datetime import datetime
    CACHE[cache_key] = {
        'analysis': analysis,
        'timestamp': datetime.now()
    }
    
    return analysis

