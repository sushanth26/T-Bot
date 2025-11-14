"""Service for sector analysis and weightage calculation"""
from config.settings import rest_api


def get_sector_info(symbol: str) -> dict:
    """Get sector and estimated weightage for a stock dynamically from Alpaca API"""
    
    try:
        # Get asset info from Alpaca
        asset = rest_api.get_asset(symbol)
        
        # Extract sector from asset attributes
        sector = None
        industry = None
        
        # Debug: print all asset attributes to see what's available
        print(f"   📊 Asset attributes for {symbol}: {dir(asset)}")
        
        # Try multiple attribute names that Alpaca might use
        for attr in ['sector', 'Sector', 'classification', 'industry_group']:
            if hasattr(asset, attr):
                val = getattr(asset, attr)
                if val:
                    sector = val
                    print(f"   ✓ Found sector from {attr}: {sector}")
                    break
        
        # Try to get industry
        for attr in ['industry', 'Industry', 'sub_industry', 'industry_classification']:
            if hasattr(asset, attr):
                val = getattr(asset, attr)
                if val:
                    industry = val
                    print(f"   ✓ Found industry from {attr}: {industry}")
                    break
        
        # Fallback: Use exchange-based category if nothing else available
        if not sector:
            exchange = getattr(asset, 'exchange', 'UNKNOWN')
            if exchange != 'UNKNOWN':
                sector = f"{exchange} Listed"
                print(f"   ⚠️  Using exchange-based fallback: {sector}")
            else:
                sector = "General"
                print(f"   ⚠️  No sector data available, using: {sector}")
        
        # Get market cap estimate from latest quote
        market_cap_estimate = None
        try:
            quote = rest_api.get_latest_quote(symbol)
            if quote and hasattr(quote, 'ask_price') and quote.ask_price:
                # Use price as a proxy for relative size (not actual market cap)
                market_cap_estimate = float(quote.ask_price)
        except Exception:
            pass
        
        # Calculate relative weightage based on market cap comparison
        # Compare with other major stocks to estimate relative importance
        weightage = estimate_relative_weightage(symbol, market_cap_estimate)
        
        return {
            "sector": sector or "General",
            "industry": industry or "Not specified",
            "weightage": weightage
        }
    
    except Exception as e:
        print(f"   ⚠️  Error getting sector info for {symbol}: {e}")
        return {
            "sector": "Unknown",
            "industry": "Not specified",
            "weightage": 0.0
        }


def estimate_relative_weightage(symbol: str, price_estimate: float = None) -> float:
    """
    Estimate a stock's relative market importance based on available data
    Returns a rough percentage indicating relative size/importance
    """
    
    if not price_estimate:
        # If no data, assume moderate importance
        return 5.0
    
    try:
        # Get a few reference stocks for comparison
        # Use well-known large-cap stocks as benchmarks
        reference_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
        reference_prices = []
        
        for ref_symbol in reference_symbols:
            if ref_symbol == symbol:
                continue
            
            try:
                ref_quote = rest_api.get_latest_quote(ref_symbol)
                if ref_quote and hasattr(ref_quote, 'ask_price') and ref_quote.ask_price:
                    reference_prices.append(float(ref_quote.ask_price))
            except Exception:
                continue
        
        if not reference_prices:
            # If we can't get reference data, estimate based on price
            # Higher priced stocks tend to be larger companies (rough heuristic)
            if price_estimate > 500:
                return 15.0  # Very large company
            elif price_estimate > 200:
                return 10.0  # Large company
            elif price_estimate > 50:
                return 5.0   # Medium company
            else:
                return 2.0   # Smaller company
        
        # Compare with reference stocks
        avg_reference = sum(reference_prices) / len(reference_prices)
        
        # Calculate relative weightage
        relative_ratio = price_estimate / avg_reference
        
        # Scale to a reasonable percentage (0-25% range)
        if relative_ratio > 2.0:
            return 20.0  # Much larger than average
        elif relative_ratio > 1.0:
            return 15.0  # Larger than average
        elif relative_ratio > 0.5:
            return 10.0  # Around average
        elif relative_ratio > 0.2:
            return 5.0   # Smaller than average
        else:
            return 2.0   # Much smaller
    
    except Exception as e:
        print(f"   ⚠️  Error estimating weightage: {e}")
        return 5.0  # Default to moderate importance

