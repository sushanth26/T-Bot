"""Grok AI service for news analysis"""
import requests
import os
import json
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
            "model": "grok-4-fast-reasoning",
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
                    # Strip markdown code blocks if present
                    if '```json' in content:
                        content = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        content = content.split('```')[1].split('```')[0].strip()
                    
                    analysis = json.loads(content)
                    print(f"   🤖 Grok analysis: {analysis.get('sentiment', 'N/A')} sentiment, {len(analysis.get('key_points', []))} points, {analysis.get('confidence', 'N/A')} confidence")
                    return analysis
                except json.JSONDecodeError as e:
                    print(f"   ⚠️  JSON parse error: {e}")
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


def stream_grok_analysis(symbol: str, news_articles: list, top_news: list, sector: str = None, sector_weight: float = None):
    """Stream Grok analysis in real-time (generator for SSE)"""
    
    # Get Grok API key from environment
    grok_api_key = os.getenv("GROK_API_KEY", "")
    
    if not grok_api_key:
        yield f"data: {json.dumps({'error': 'Grok API key not configured'})}\n\n"
        return
    
    if not news_articles and not top_news:
        yield f"data: {json.dumps({'error': 'No news available for analysis'})}\n\n"
        return
    
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
        
        # Build sector context
        sector_context = ""
        if sector:
            sector_context = f"\n\nStock Context:\n- Sector: {sector}"
            if sector_weight:
                sector_context += f"\n- Weightage in {sector} sector: {sector_weight:.2f}%"
        
        # Create prompt for Grok
        prompt = f"""Analyze these news articles about {symbol} stock and provide:

1. Overall Sentiment (bullish/bearish/neutral)
2. Summary (2-3 sentences)
3. Key Points (3-5 bullet points)
4. Trading Signals (buy/sell/hold with reasoning)
{sector_context}

News Articles:
{news_text}

Consider the stock's sector and market position in your analysis. Respond in JSON format:
{{
  "sentiment": "bullish/bearish/neutral",
  "summary": "brief summary",
  "key_points": ["point 1", "point 2", "point 3"],
  "trading_signals": ["signal 1", "signal 2"],
  "confidence": "high/medium/low"
}}"""

        # Call Grok API with streaming enabled
        headers = {
            "Authorization": f"Bearer {grok_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "grok-4-fast-reasoning",
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
            "max_tokens": 500,
            "stream": True
        }
        
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
            stream=True
        )
        
        if response.status_code == 200:
            full_content = ""
            
            # Stream the response
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    
                    if line_text.startswith('data: '):
                        data_str = line_text[6:]  # Remove 'data: ' prefix
                        
                        if data_str == '[DONE]':
                            break
                        
                        try:
                            chunk_data = json.loads(data_str)
                            
                            if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                delta = chunk_data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                
                                if content:
                                    full_content += content
                                    # Send chunk to frontend
                                    yield f"data: {json.dumps({'chunk': content, 'type': 'content'})}\n\n"
                        
                        except json.JSONDecodeError:
                            continue
            
            # After streaming completes, parse the full JSON response
            try:
                # Strip markdown code blocks if present
                parsed_content = full_content
                if '```json' in parsed_content:
                    parsed_content = parsed_content.split('```json')[1].split('```')[0].strip()
                elif '```' in parsed_content:
                    parsed_content = parsed_content.split('```')[1].split('```')[0].strip()
                
                analysis = json.loads(parsed_content)
                
                # Send final parsed analysis
                yield f"data: {json.dumps({'type': 'complete', 'analysis': analysis})}\n\n"
                
                # Cache the analysis
                from datetime import datetime
                cache_key = f"{symbol}_grok_analysis"
                CACHE[cache_key] = {
                    'analysis': analysis,
                    'timestamp': datetime.now()
                }
                
            except json.JSONDecodeError as e:
                # If parsing fails, send the raw content
                yield f"data: {json.dumps({'type': 'complete', 'analysis': {'summary': full_content[:200], 'sentiment': 'neutral', 'key_points': [], 'trading_signals': [], 'confidence': 'low'}})}\n\n"
        
        else:
            error_msg = f"Grok API HTTP {response.status_code}"
            yield f"data: {json.dumps({'error': error_msg})}\n\n"
    
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"


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

