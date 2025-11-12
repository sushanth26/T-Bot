"""EMA calculation service"""
import pandas as pd
from datetime import datetime, timedelta
from alpaca_trade_api.rest import TimeFrame
from config.settings import data_api


def calculate_real_ema(prices: pd.Series, period: int) -> float:
    """Calculate actual EMA from price series"""
    if len(prices) < period:
        return None
    ema = prices.ewm(span=period, adjust=False).mean()
    return float(ema.iloc[-1])


def get_daily_emas(symbol: str) -> dict:
    """Fetch and calculate daily EMAs (20, 50)"""
    emas = {}
    try:
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=365)
        
        daily_bars = data_api.get_bars(
            symbol, 
            TimeFrame.Day,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_date.strftime("%Y-%m-%d"),
            feed='iex'
        ).df
        
        if not daily_bars.empty and len(daily_bars) >= 50:
            ema_20 = calculate_real_ema(daily_bars['close'], 20)
            ema_50 = calculate_real_ema(daily_bars['close'], 50)
            if ema_20: emas["daily_ema_20"] = round(ema_20, 2)
            if ema_50: emas["daily_ema_50"] = round(ema_50, 2)
            print(f"✅ Daily EMAs: 20=${ema_20:.2f}, 50=${ema_50:.2f} from {len(daily_bars)} bars")
        else:
            print(f"⚠️  Not enough daily data: {len(daily_bars) if not daily_bars.empty else 0} bars")
    except Exception as e:
        print(f"⚠️  Daily EMAs error: {e}")
    
    return emas


def get_hourly_emas(symbol: str) -> dict:
    """Fetch and calculate hourly EMAs (34, 50)"""
    emas = {}
    try:
        end_time = datetime.now() - timedelta(days=1)
        start_time = end_time - timedelta(days=60)
        
        hourly_bars = data_api.get_bars(
            symbol,
            TimeFrame.Hour,
            start=start_time.strftime("%Y-%m-%d"),
            end=end_time.strftime("%Y-%m-%d"),
            feed='iex'
        ).df
        
        if not hourly_bars.empty and len(hourly_bars) >= 50:
            ema_34 = calculate_real_ema(hourly_bars['close'], 34)
            ema_50 = calculate_real_ema(hourly_bars['close'], 50)
            if ema_34: emas["1h_ema_34"] = round(ema_34, 2)
            if ema_50: emas["1h_ema_50"] = round(ema_50, 2)
            print(f"✅ 1hr EMAs: 34=${ema_34:.2f}, 50=${ema_50:.2f} from {len(hourly_bars)} bars")
        else:
            print(f"⚠️  Not enough hourly data: {len(hourly_bars) if not hourly_bars.empty else 0} bars")
    except Exception as e:
        print(f"⚠️  1hr EMAs error: {e}")
    
    return emas


def get_10min_emas(symbol: str) -> dict:
    """Fetch and calculate 10-minute EMAs (9, 34, 50)"""
    emas = {}
    try:
        end_time = datetime.now() - timedelta(days=1)
        start_time = end_time - timedelta(days=14)
        
        minute_bars = data_api.get_bars(
            symbol,
            TimeFrame.Minute,
            start=start_time.strftime("%Y-%m-%d"),
            end=end_time.strftime("%Y-%m-%d"),
            feed='iex'
        ).df
        
        if not minute_bars.empty and len(minute_bars) >= 500:
            # Resample to 10-min bars
            bars_10m = minute_bars.resample('10min').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()
            
            if len(bars_10m) >= 50:
                ema_9 = calculate_real_ema(bars_10m['close'], 9)
                ema_34 = calculate_real_ema(bars_10m['close'], 34)
                ema_50 = calculate_real_ema(bars_10m['close'], 50)
                if ema_9: emas["10m_ema_9"] = round(ema_9, 2)
                if ema_34: emas["10m_ema_34"] = round(ema_34, 2)
                if ema_50: emas["10m_ema_50"] = round(ema_50, 2)
                print(f"✅ 10min EMAs: 9=${ema_9:.2f}, 34=${ema_34:.2f}, 50=${ema_50:.2f} from {len(bars_10m)} bars")
            else:
                print(f"⚠️  Not enough 10min bars after resample: {len(bars_10m)}")
        else:
            print(f"⚠️  Not enough minute data: {len(minute_bars) if not minute_bars.empty else 0} bars")
    except Exception as e:
        print(f"⚠️  10min EMAs error: {e}")
    
    return emas


def get_all_emas(symbol: str) -> dict:
    """Get all EMAs for a symbol"""
    all_emas = {}
    
    # Get daily EMAs
    daily_emas = get_daily_emas(symbol)
    all_emas.update(daily_emas)
    
    # Get hourly EMAs
    hourly_emas = get_hourly_emas(symbol)
    all_emas.update(hourly_emas)
    
    # Get 10-minute EMAs
    ten_min_emas = get_10min_emas(symbol)
    all_emas.update(ten_min_emas)
    
    if not all_emas:
        print("⚠️  No EMAs available - historical data not accessible")
    
    return all_emas

