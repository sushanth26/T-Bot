# Backend - Stock Streaming API

FastAPI server that streams real-time stock data from Alpaca Trade API.

## Features

- ✅ Real-time quote and trade streaming via WebSocket
- ✅ REST API endpoints for historical data
- ✅ Multiple stock symbol support
- ✅ Automatic reconnection handling
- ✅ CORS enabled for frontend integration

## API Endpoints

### REST Endpoints

#### GET `/`
Health check endpoint.

**Response:**
```json
{
  "message": "Alpaca Stock Data Streaming API"
}
```

#### GET `/api/quotes`
Get latest quotes for all tracked symbols.

**Response:**
```json
{
  "AAPL": {
    "symbol": "AAPL",
    "bid": 178.50,
    "ask": 178.52,
    "bidSize": 100,
    "askSize": 200,
    "timestamp": "2024-01-01T12:00:00Z"
  },
  ...
}
```

#### GET `/api/bars/{symbol}`
Get historical price bars for a symbol.

**Parameters:**
- `symbol` (path): Stock symbol (e.g., "AAPL")
- `timeframe` (query): Bar timeframe - "1Min", "5Min", "15Min", "1Hour", "1Day" (default: "1Day")
- `limit` (query): Number of bars to return (default: 100)

**Example:**
```
GET /api/bars/AAPL?timeframe=1Hour&limit=50
```

**Response:**
```json
{
  "symbol": "AAPL",
  "timeframe": "1Hour",
  "bars": [
    {
      "timestamp": "2024-01-01T09:00:00Z",
      "open": 178.00,
      "high": 179.50,
      "low": 177.80,
      "close": 179.20,
      "volume": 1234567
    },
    ...
  ]
}
```

### WebSocket Endpoint

#### WS `/ws`
Real-time stock data streaming.

**Client Messages:**

Ping (keep-alive):
```json
{
  "type": "ping"
}
```

Subscribe to symbols:
```json
{
  "type": "subscribe",
  "symbols": ["AAPL", "GOOGL"]
}
```

**Server Messages:**

Connection established:
```json
{
  "type": "connected",
  "message": "Connected to stock data stream",
  "symbols": ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
}
```

Quote update:
```json
{
  "type": "quote",
  "symbol": "AAPL",
  "bid": 178.50,
  "ask": 178.52,
  "bidSize": 100,
  "askSize": 200,
  "timestamp": "2024-01-01T12:00:00.123456Z"
}
```

Trade update:
```json
{
  "type": "trade",
  "symbol": "AAPL",
  "price": 178.51,
  "size": 100,
  "timestamp": "2024-01-01T12:00:01.234567Z"
}
```

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Required
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here

# Optional
ALPACA_BASE_URL=https://paper-api.alpaca.markets  # Paper trading (default)
# ALPACA_BASE_URL=https://api.alpaca.markets  # Live trading
```

### Tracked Symbols

Edit the `SYMBOLS` list in `server.py`:

```python
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
```

## Running the Server

### Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run with auto-reload
python server.py
```

Server will start at `http://0.0.0.0:8000`

### Production

```bash
# With Uvicorn
uvicorn server:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Dependencies

- **fastapi** - Modern web framework
- **uvicorn** - ASGI server
- **websockets** - WebSocket support
- **alpaca-trade-api** - Alpaca API client
- **python-dotenv** - Environment variable management
- **pandas** - Data manipulation
- **numpy** - Numerical operations

## Architecture

The server uses:
1. **FastAPI** for HTTP and WebSocket endpoints
2. **Alpaca Stream** for real-time market data
3. **ConnectionManager** to broadcast data to multiple WebSocket clients
4. **Asyncio** for concurrent operations

## Error Handling

- Automatic reconnection to Alpaca stream
- Graceful handling of disconnected WebSocket clients
- Error responses for invalid API requests
- Fallback behavior when API credentials are missing

## Security Notes

- ⚠️ Never commit your `.env` file
- ⚠️ Use paper trading URL for testing
- ⚠️ Keep your API keys secure
- ⚠️ Update CORS origins for production deployment

## Testing

Test the API using curl or your browser:

```bash
# Health check
curl http://localhost:8000

# Get quotes
curl http://localhost:8000/api/quotes

# Get bars
curl "http://localhost:8000/api/bars/AAPL?timeframe=1Hour&limit=10"

# WebSocket (using wscat)
wscat -c ws://localhost:8000/ws
```

## Troubleshooting

### "Alpaca API credentials not configured"
- Check your `.env` file exists
- Verify API keys are correct
- Ensure `.env` is in the same directory as `server.py`

### No data streaming
- Verify market hours (9:30 AM - 4:00 PM ET)
- Check Alpaca service status
- Ensure you're using IEX data feed (included with paper trading)

### Port already in use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill the process
kill -9 $(lsof -ti:8000)
```

## License

MIT

