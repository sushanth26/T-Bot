"""Premarket high/low service"""
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from config.settings import data_api


def get_premarket_levels(symbol: str) -> dict:
    """Get premarket high and low for current day"""
    premarket_levels = {}
    
    try:
        today = datetime.now()
        
        print(f"   🔍 Fetching premarket levels for: {today.strftime('%Y-%m-%d')}")
        
        # Get today's minute bars
        bars = data_api.get_bars(
            symbol,
            TimeFrame.Minute,
            start=today.strftime("%Y-%m-%d"),
            end=today.strftime("%Y-%m-%d"),
            feed='iex'
        ).df
        
        if bars.empty:
            print(f"   ℹ️  No bars available for today")
            return premarket_levels
        
        # Try to filter for premarket hours (4:00 AM - 9:29 AM ET)
        try:
            premarket_bars = bars.between_time('04:00', '09:29')
        except:
            # Fallback: filter by hour
            premarket_bars = bars[bars.index.hour < 10]
        
        if not premarket_bars.empty:
            pmh = float(premarket_bars['high'].max())
            pml = float(premarket_bars['low'].min())
            
            premarket_levels['PMH'] = round(pmh, 2)
            premarket_levels['PML'] = round(pml, 2)
            
            print(f"   ✅ Premarket levels: PMH=${pmh:.2f}, PML=${pml:.2f} ({len(premarket_bars)} bars)")
        else:
            # No premarket data - try using today's regular hours as fallback
            print(f"   ℹ️  No premarket bars (free tier limitation)")
            
            # Use today's regular hours high/low as PMH/PML
            if not bars.empty:
                regular_bars = bars.between_time('09:30', '16:00')
                if not regular_bars.empty:
                    # Use first 30 minutes of regular trading as "premarket proxy"
                    early_bars = regular_bars.head(30)
                    pmh = float(early_bars['high'].max())
                    pml = float(early_bars['low'].min())
                    
                    premarket_levels['PMH'] = round(pmh, 2)
                    premarket_levels['PML'] = round(pml, 2)
                    
                    print(f"   ℹ️  Using early trading hours: PMH=${pmh:.2f}, PML=${pml:.2f}")
    
    except Exception as e:
        print(f"   ⚠️  Premarket levels error: {e}")
    
    return premarket_levels

