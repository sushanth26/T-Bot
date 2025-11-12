# Stock Data Streaming App 📈

A real-time stock market data streaming application built with **Alpaca Trade API**, **FastAPI**, **React**, and **TypeScript**. This application provides live stock quotes and trades with a beautiful, modern UI.

## Features

✨ **Real-time Data Streaming** - Live stock quotes and trades via WebSocket
📊 **Multiple Stocks** - Track AAPL, GOOGL, MSFT, TSLA, and AMZN simultaneously
💹 **Visual Feedback** - Price changes highlighted with animations
🎨 **Modern UI** - Beautiful dark theme with smooth transitions
🔄 **Auto-Reconnect** - Automatic reconnection with exponential backoff
📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Alpaca Trade API** - Real-time market data provider
- **WebSockets** - Real-time bidirectional communication
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **CSS3** - Modern styling with animations

## Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn
- Alpaca API account (free paper trading account)

## Getting Started

### 1. Get Alpaca API Keys

1. Sign up for a free account at [Alpaca](https://alpaca.markets/)
2. Navigate to your [Paper Trading Dashboard](https://app.alpaca.markets/paper/dashboard/overview)
3. Generate API keys (View API Keys → Generate New Keys)
4. Copy your API Key and Secret Key

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env

# Edit .env file and add your Alpaca API credentials
# nano .env  # or use your preferred editor
```

Edit the `.env` file:
```env
ALPACA_API_KEY=your_actual_api_key_here
ALPACA_SECRET_KEY=your_actual_secret_key_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# or with yarn
# yarn install
```

### 4. Running the Application

You'll need two terminal windows:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Activate venv if not already active
python server.py
```

The backend server will start at `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will automatically open at `http://localhost:3000`

## Project Structure

```
TBot/
├── backend/
│   ├── server.py           # FastAPI server with Alpaca integration
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variables template
│
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── StockCard.tsx
│   │   │   ├── StockCard.css
│   │   │   ├── ConnectionStatus.tsx
│   │   │   └── ConnectionStatus.css
│   │   ├── hooks/          # Custom React hooks
│   │   │   └── useWebSocket.ts
│   │   ├── types/          # TypeScript type definitions
│   │   │   └── index.ts
│   │   ├── App.tsx         # Main App component
│   │   ├── App.css
│   │   ├── main.tsx        # Entry point
│   │   └── index.css       # Global styles
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
│
└── README.md
```

## API Endpoints

### REST Endpoints

- `GET /` - API health check
- `GET /api/quotes` - Get latest quotes for all tracked symbols
- `GET /api/bars/{symbol}?timeframe=1Day&limit=100` - Get historical bars

### WebSocket Endpoint

- `WS /ws` - Real-time stock data streaming

**WebSocket Message Types:**

Client → Server:
```json
{
  "type": "ping"
}
```

```json
{
  "type": "subscribe",
  "symbols": ["AAPL", "GOOGL"]
}
```

Server → Client:
```json
{
  "type": "quote",
  "symbol": "AAPL",
  "bid": 178.50,
  "ask": 178.52,
  "bidSize": 100,
  "askSize": 200,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

```json
{
  "type": "trade",
  "symbol": "AAPL",
  "price": 178.51,
  "size": 100,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Customization

### Adding More Symbols

Edit the `SYMBOLS` array in both files:

**Backend (`backend/server.py`):**
```python
SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META"]
```

**Frontend (`frontend/src/App.tsx`):**
```typescript
const SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META']
```

### Changing Colors

Edit CSS variables in `frontend/src/index.css`:
```css
:root {
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --accent-green: #10b981;
  --accent-red: #ef4444;
  --accent-blue: #3b82f6;
}
```

## Troubleshooting

### Backend Issues

**Error: "Alpaca API credentials not configured"**
- Make sure you've created a `.env` file in the `backend` directory
- Verify your API keys are correct
- Ensure the `.env` file is in the same directory as `server.py`

**Error: Module not found**
- Activate your virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**Error: Connection refused**
- Check if port 8000 is already in use
- Try running on a different port: `uvicorn server:app --port 8001`

### Frontend Issues

**Error: Cannot connect to WebSocket**
- Ensure the backend server is running on `http://localhost:8000`
- Check your browser console for error messages
- Verify CORS settings in `backend/server.py`

**Error: Module not found**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

### Market Data Issues

**No data showing**
- Market hours: Data is most active during US market hours (9:30 AM - 4:00 PM ET)
- After hours: Limited data availability outside market hours
- Paper trading: Uses IEX data feed which may have delays
- Check Alpaca [status page](https://status.alpaca.markets/) for service issues

## Development

### Backend Development

```bash
# Run with auto-reload
cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
# Run development server
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Production Deployment

### Backend

1. Set environment variables on your hosting platform
2. Use a production ASGI server (Uvicorn with Gunicorn)
3. Enable HTTPS
4. Update CORS origins to match your frontend domain

### Frontend

1. Build the production bundle: `npm run build`
2. Deploy the `dist` folder to your hosting service (Vercel, Netlify, etc.)
3. Update WebSocket URL to point to your production backend

## License

MIT License - feel free to use this project for learning and development!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Resources

- [Alpaca API Documentation](https://alpaca.markets/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Built with ❤️ using Alpaca Trade API

