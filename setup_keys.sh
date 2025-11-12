#!/bin/bash

echo "================================================"
echo "   Alpaca API Key Setup"
echo "================================================"
echo ""
echo "Get your FREE API keys from:"
echo "https://app.alpaca.markets/paper/dashboard/overview"
echo ""
echo "================================================"
echo ""

read -p "Enter your Alpaca API KEY: " api_key
read -p "Enter your Alpaca SECRET KEY: " secret_key

cat > /Users/sushanth/TBot/backend/.env << EOF
# Alpaca API Credentials
# Get your API keys from: https://app.alpaca.markets/paper/dashboard/overview
ALPACA_API_KEY=$api_key
ALPACA_SECRET_KEY=$secret_key

# Use paper trading URL by default
ALPACA_BASE_URL=https://paper-api.alpaca.markets
EOF

echo ""
echo "✅ API keys saved to backend/.env"
echo ""
echo "Now restart the backend server:"
echo "  1. Stop the current backend (Ctrl+C or run: pkill -f 'python server.py')"
echo "  2. cd /Users/sushanth/TBot/backend"
echo "  3. source venv/bin/activate"
echo "  4. python server.py"
echo ""

