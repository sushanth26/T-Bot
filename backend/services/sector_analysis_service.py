"""Advanced sector analysis using Yahoo Finance (yfinance)
NO API KEY NEEDED - Completely FREE!
"""
import yfinance as yf


def get_financial_ratios(symbol: str) -> dict:
    """Get financial ratios including P/E from Yahoo Finance"""
    
    print(f"   📈 Fetching financial ratios for {symbol} from Yahoo Finance...")
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'pe_ratio': info.get('trailingPE') or info.get('forwardPE'),
            'peg_ratio': info.get('pegRatio'),
            'pb_ratio': info.get('priceToBook'),
            'price_to_sales': info.get('priceToSalesTrailing12Months'),
            'market_cap': info.get('marketCap'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'beta': info.get('beta'),
            'dividend_yield': info.get('dividendYield')
        }
    
    except Exception as e:
        print(f"   ⚠️  Error fetching ratios for {symbol}: {e}")
        return {}


def find_sector_peers(symbol: str, sector: str, limit: int = 50) -> list:
    """Find peer companies in the same sector using Yahoo Finance screener"""
    
    print(f"   🔍 Finding peers in {sector} sector...")
    
    # Common stocks in major sectors (Yahoo Finance doesn't have easy screener access)
    # We'll use a curated list of major stocks by sector
    sector_stocks = {
        'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC', 'AVGO', 'QCOM', 'TXN', 
                       'AMAT', 'LRCX', 'MU', 'KLAC', 'NXPI', 'MCHP', 'ORCL', 'CRM', 'ADBE', 'CSCO'],
        'Consumer Cyclical': ['TSLA', 'AMZN', 'HD', 'MCD', 'NKE', 'SBUX', 'TGT', 'LOW', 'TJX', 'BKNG',
                              'GM', 'F', 'RIVN', 'LCID'],
        'Financial Services': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'USB', 'PNC', 'TFC', 'SCHW',
                               'V', 'MA', 'AXP', 'COF', 'BLK'],
        'Healthcare': ['UNH', 'JNJ', 'LLY', 'ABBV', 'MRK', 'TMO', 'ABT', 'PFE', 'DHR', 'BMY',
                       'AMGN', 'GILD', 'CVS', 'CI', 'HUM'],
        'Communication Services': ['GOOGL', 'META', 'DIS', 'CMCSA', 'VZ', 'T', 'NFLX', 'TMUS', 'CHTR'],
        'Consumer Defensive': ['WMT', 'PG', 'KO', 'PEP', 'COST', 'PM', 'MO', 'CL', 'MDLZ', 'KMB'],
        'Industrials': ['UPS', 'HON', 'BA', 'UNP', 'CAT', 'LMT', 'GE', 'RTX', 'DE', 'MMM'],
        'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'HAL'],
        'Basic Materials': ['LIN', 'APD', 'ECL', 'SHW', 'DD', 'NEM', 'FCX', 'NUE', 'VMC', 'MLM'],
        'Real Estate': ['PLD', 'AMT', 'CCI', 'EQIX', 'PSA', 'SPG', 'O', 'WELL', 'DLR', 'AVB'],
        'Utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'XEL', 'WEC', 'ES']
    }
    
    # Get stocks in the same sector
    peers = sector_stocks.get(sector, [])
    
    # Remove the symbol itself
    peers = [p for p in peers if p != symbol]
    
    print(f"   ✓ Found {len(peers)} potential peers in {sector}")
    
    return peers[:limit]


def get_lowest_pe_in_sector(symbol: str, sector: str, peer_count: int = 20, return_count: int = 5) -> list:
    """Get stocks with lowest P/E ratios in the same sector (only large caps > $100B)"""
    
    print(f"   📉 Finding lowest P/E large-cap stocks (>$100B) in {sector} sector...")
    
    # Find peer stocks
    peers = find_sector_peers(symbol, sector, peer_count)
    
    if not peers:
        return []
    
    # Get P/E for each peer
    peer_pe_data = []
    min_market_cap = 100_000_000_000  # $100B minimum
    
    for peer in peers:
        try:
            ticker = yf.Ticker(peer)
            info = ticker.info
            
            pe = info.get('trailingPE') or info.get('forwardPE')
            market_cap = info.get('marketCap', 0)
            
            # Only include if:
            # 1. Has valid P/E (positive)
            # 2. Market cap > $100B
            if pe and pe > 0 and market_cap >= min_market_cap:
                peer_pe_data.append({
                    'symbol': peer,
                    'pe_ratio': pe,
                    'market_cap': market_cap,
                })
                print(f"      ✓ {peer}: P/E={pe:.2f}, Cap=${market_cap/1e9:.1f}B")
        except Exception as e:
            continue
    
    # Sort by P/E (lowest first)
    peer_pe_data.sort(key=lambda x: x['pe_ratio'])
    
    lowest = peer_pe_data[:return_count]
    
    print(f"   ✓ Found {len(lowest)} large-cap stocks with lowest P/E (filtered to >$100B)")
    
    return lowest


def analyze_sector_position(symbol: str, etf_symbol: str = None) -> dict:
    """
    Comprehensive sector analysis using Yahoo Finance
    
    Returns:
    - P/E ratio and financial metrics
    - Sector & Industry
    - 5 stocks with lowest P/E in sector
    
    NO API KEY NEEDED!
    """
    
    print(f"\n   🔍 === SECTOR ANALYSIS FOR {symbol} (Yahoo Finance) ===")
    
    result = {
        'symbol': symbol,
        'financial_ratios': {},
        'lowest_pe_peers': [],
        'error': None
    }
    
    try:
        # Get financial ratios
        print(f"\n   📈 Fetching financial ratios...")
        ratios = get_financial_ratios(symbol)
        result['financial_ratios'] = ratios
        
        if ratios.get('pe_ratio'):
            print(f"   ✓ P/E Ratio: {ratios['pe_ratio']:.2f}")
        if ratios.get('market_cap'):
            market_cap_b = ratios['market_cap'] / 1e9
            print(f"   ✓ Market Cap: ${market_cap_b:.2f}B")
        
        sector = ratios.get('sector')
        if sector:
            print(f"   ✓ Sector: {sector}")
            
            # Find lowest P/E peers in sector
            print(f"\n   📉 Finding lowest P/E peers...")
            lowest_pe = get_lowest_pe_in_sector(symbol, sector, peer_count=20, return_count=5)
            result['lowest_pe_peers'] = lowest_pe
            
            if lowest_pe:
                print(f"   ✓ Lowest 5 P/E ratios in {sector}:")
                for i, peer in enumerate(lowest_pe, 1):
                    print(f"      {i}. {peer['symbol']}: P/E = {peer['pe_ratio']:.2f}")
        
        print(f"\n   ✅ Sector analysis complete for {symbol}")
        
    except Exception as e:
        print(f"   ⚠️  Error in sector analysis: {e}")
        result['error'] = str(e)
    
    return result
