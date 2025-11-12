"""Premarket crossover detection service"""
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from config.settings import data_api


def detect_premarket_crossovers(symbol: str, current_price: float, emas: dict) -> list:
    """Detect if price crossed above/below EMAs during premarket (4am-9:30am ET)"""
    crossovers = []
    
    try:
        # Use today's date for live premarket detection
        today = datetime.now()
        
        print(f"   🔍 Checking premarket crossovers for: {today.strftime('%Y-%m-%d %A')}")
        
        # Get today's premarket bars (extended hours)
        premarket_bars = data_api.get_bars(
            symbol,
            TimeFrame.Minute,
            start=today.strftime("%Y-%m-%d"),
            end=today.strftime("%Y-%m-%d"),
            feed='iex'
        ).df
        
        if premarket_bars.empty:
            print(f"   ❌ No bars available for {today.strftime('%Y-%m-%d')}")
            print(f"   ℹ️  Free tier limitation: Extended hours data not available")
            return crossovers
        
        print(f"   ✅ Got {len(premarket_bars)} minute bars for {today.strftime('%Y-%m-%d')}")
        
        # Get premarket data (before 9:30 AM ET)
        # Filter for premarket hours (4:00 - 9:30 ET)
        try:
            premarket_data = premarket_bars.between_time('04:00', '09:29')
        except:
            # If between_time doesn't work, try filtering by hour
            premarket_data = premarket_bars[premarket_bars.index.hour < 10]
        
        if premarket_data.empty:
            print(f"   ℹ️  No premarket hours (4:00-9:30 AM) in the {len(premarket_bars)} bars")
            print(f"   ℹ️  Free tier only provides regular hours (9:30-16:00)")
            return crossovers
        
        print(f"   ✅ Found {len(premarket_data)} premarket bars (4:00-9:30 AM)")
        
        # Only check Daily and Hourly EMAs (no 10-minute)
        ema_checks = {
            'daily_ema_20': 'Daily 20 EMA',
            'daily_ema_50': 'Daily 50 EMA',
            '1h_ema_34': '1hr 34 EMA',
            '1h_ema_50': '1hr 50 EMA',
        }
        
        # Only detect ACTUAL premarket crossovers (price touched/crossed the EMA)
        if not premarket_data.empty:
            try:
                premarket_open = float(premarket_data['open'].iloc[0])
                premarket_close = float(premarket_data['close'].iloc[-1])
                premarket_high = float(premarket_data['high'].max())
                premarket_low = float(premarket_data['low'].min())
                
                print(f"   📊 Premarket: Open=${premarket_open:.2f}, High=${premarket_high:.2f}, Low=${premarket_low:.2f}, Close=${premarket_close:.2f}")
                print(f"   🔍 Checking {len(ema_checks)} EMAs for crossovers...")
                
                for ema_key, ema_label in ema_checks.items():
                    if ema_key in emas:
                        ema_value = emas[ema_key]
                        
                        # Check if price actually TOUCHED the EMA and crossed above
                        # Open was below, price touched/crossed EMA, closed above
                        if premarket_open < ema_value and premarket_close > ema_value:
                            # Verify price actually touched the EMA level
                            if premarket_low <= ema_value <= premarket_high:
                                crossovers.append({
                                    'type': 'cross_above',
                                    'ema': ema_label,
                                    'ema_value': ema_value,
                                    'direction': '⬆️',
                                    'message': f'Crossed ABOVE {ema_label} (${ema_value:.2f}) in premarket'
                                })
                                print(f"   🚨 ALERT: Crossed ABOVE {ema_label} @ ${ema_value:.2f}")
                            else:
                                print(f"   ➖ {ema_label} @ ${ema_value:.2f}: Open below, Close above, but didn't touch")
                        
                        # Check if price actually TOUCHED the EMA and crossed below
                        # Open was above, price touched/crossed EMA, closed below
                        elif premarket_open > ema_value and premarket_close < ema_value:
                            # Verify price actually touched the EMA level
                            if premarket_low <= ema_value <= premarket_high:
                                crossovers.append({
                                    'type': 'cross_below',
                                    'ema': ema_label,
                                    'ema_value': ema_value,
                                    'direction': '⬇️',
                                    'message': f'Crossed BELOW {ema_label} (${ema_value:.2f}) in premarket'
                                })
                                print(f"   🚨 ALERT: Crossed BELOW {ema_label} @ ${ema_value:.2f}")
                            else:
                                print(f"   ➖ {ema_label} @ ${ema_value:.2f}: Open above, Close below, but didn't touch")
                        else:
                            # No crossover
                            if premarket_open < ema_value and premarket_close < ema_value:
                                print(f"   ✓ {ema_label} @ ${ema_value:.2f}: Stayed below")
                            elif premarket_open > ema_value and premarket_close > ema_value:
                                print(f"   ✓ {ema_label} @ ${ema_value:.2f}: Stayed above")
                
                if crossovers:
                    print(f"   ✅ {len(crossovers)} premarket EMA crossover(s) detected")
                else:
                    print(f"   ℹ️  No EMA crossovers during premarket")
                    
            except Exception as pm_error:
                print(f"   ⚠️  Premarket analysis error: {pm_error}")
        else:
            print(f"   ℹ️  No premarket data available (extended hours data required)")
        
    except Exception as e:
        print(f"   ⚠️  Crossover detection error: {e}")
    
    return crossovers

