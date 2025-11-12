# Quick Start Guide 🚀

Get your stock streaming app running in 5 minutes!

## Step 1: Get Alpaca API Keys (2 minutes)

1. Go to [https://alpaca.markets/](https://alpaca.markets/)
2. Click "Sign Up" and create a free account
3. Once logged in, go to [Paper Trading Dashboard](https://app.alpaca.markets/paper/dashboard/overview)
4. Click "Generate New Keys" or "View" to see your API keys
5. Copy both your **API Key** and **Secret Key**

> 💡 **Tip:** Use paper trading (free) for testing - it's perfect for this demo!

## Step 2: Backend Setup (2 minutes)

```bash
# 1. Open terminal and navigate to backend
cd backend

# 2. Create Python virtual environment
python -m venv venv

# 3. Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
echo "ALPACA_API_KEY=your_key_here
ALPACA_SECRET_KEY=your_secret_here
ALPACA_BASE_URL=https://paper-api.alpaca.markets" > .env

# 6. Edit .env with your actual keys
nano .env  # or use any text editor
```

**Your `.env` should look like:**
```env
ALPACA_API_KEY=PK1234567890ABCDEF
ALPACA_SECRET_KEY=abcdef1234567890abcdef1234567890
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

## Step 3: Frontend Setup (1 minute)

Open a **NEW terminal window** and run:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

## Step 4: Run Everything! (30 seconds)

**Keep both terminals open:**

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # if not already activated
python server.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in 300 ms

  ➜  Local:   http://localhost:3000/
```

## Step 5: Open Your Browser! 🎉

Your browser should automatically open to `http://localhost:3000`

You'll see:
- 📈 Live stock prices for AAPL, GOOGL, MSFT, TSLA, AMZN
- 🟢 Green "Connected" status indicator
- 💹 Real-time price updates with animations
- 📊 Bid/Ask prices and sizes

## Troubleshooting

### ❌ "No module named 'fastapi'"
**Solution:** Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### ❌ "WebSocket connection failed"
**Solution:** Make sure the backend is running on port 8000. Check Terminal 1.

### ❌ "Alpaca API credentials not configured"
**Solution:** Check your `.env` file exists and has the correct keys:
```bash
cat backend/.env  # Should show your API keys
```

### ❌ "No data showing"
**Possible reasons:**
1. **Market is closed** - Stock data is most active during US market hours (9:30 AM - 4:00 PM ET, Monday-Friday)
2. **Invalid API keys** - Double-check your keys in the `.env` file
3. **Wait a moment** - It may take 10-30 seconds for data to start streaming

### ❌ Port already in use
**Backend (8000):**
```bash
# Run on different port
uvicorn server:app --port 8001
# Update frontend to use ws://localhost:8001/ws
```

**Frontend (3000):**
```bash
# Vite will automatically use next available port
# Or specify: npm run dev -- --port 3001
```

## What to Expect

### During Market Hours (9:30 AM - 4:00 PM ET)
- Frequent updates every few seconds
- Price changes with green (up) or red (down) animations
- Active trading data

### After Hours
- Less frequent updates
- Limited trading activity
- May take longer to see first update

## Next Steps

Once everything is working:

1. **Add more stocks** - Edit the `SYMBOLS` array in both `backend/server.py` and `frontend/src/App.tsx`
2. **Customize colors** - Edit CSS variables in `frontend/src/index.css`
3. **Check the full README** - See `README.md` for advanced features and deployment

## Need Help?

- 📚 Check the main [README.md](README.md) for detailed documentation
- 🔗 [Alpaca API Docs](https://alpaca.markets/docs/)
- 💬 Open an issue on GitHub

---

**Enjoy your stock streaming app!** 📈✨

