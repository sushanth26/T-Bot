#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  📰 POLYGON.IO NEWS API SETUP                                             ║"
echo "╠════════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                            ║"
echo "║  Polygon.io provides stock news with a free tier:                          ║"
echo "║  • FREE: 5 API calls per minute                                            ║"
echo "║  • Unlimited news articles per call                                        ║"
echo "║  • Real-time market data                                                   ║"
echo "║                                                                            ║"
echo "╠════════════════════════════════════════════════════════════════════════════╣"
echo "║  STEPS TO GET YOUR API KEY:                                                ║"
echo "║                                                                            ║"
echo "║  1. Visit: https://polygon.io/                                             ║"
echo "║  2. Click 'Get Your Free API Key' or 'Sign Up'                             ║"
echo "║  3. Create a free account                                                  ║"
echo "║  4. Go to Dashboard → API Keys                                             ║"
echo "║  5. Copy your API key                                                      ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Enter your Polygon API key (or press Enter to skip):"
read -r POLYGON_KEY

if [ -z "$POLYGON_KEY" ]; then
    echo ""
    echo "⚠️  No API key entered. News feature will not work."
    echo "   You can add it later to backend/.env:"
    echo "   POLYGON_API_KEY=your_key_here"
    exit 0
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Please run this script from the backend directory"
    exit 1
fi

# Check if POLYGON_API_KEY already exists
if grep -q "POLYGON_API_KEY=" .env; then
    # Update existing key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/POLYGON_API_KEY=.*/POLYGON_API_KEY=$POLYGON_KEY/" .env
    else
        # Linux
        sed -i "s/POLYGON_API_KEY=.*/POLYGON_API_KEY=$POLYGON_KEY/" .env
    fi
    echo "✅ Updated POLYGON_API_KEY in .env"
else
    # Add new key
    echo "" >> .env
    echo "# Polygon.io News API" >> .env
    echo "POLYGON_API_KEY=$POLYGON_KEY" >> .env
    echo "✅ Added POLYGON_API_KEY to .env"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE!                                                        ║"
echo "╠════════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                            ║"
echo "║  Your Polygon API key has been added to .env                               ║"
echo "║                                                                            ║"
echo "║  Next steps:                                                               ║"
echo "║  1. Restart your backend server                                            ║"
echo "║  2. News will now load from Polygon.io                                     ║"
echo "║  3. Free tier: 5 requests/minute                                           ║"
echo "║                                                                            ║"
echo "║  To restart server:                                                        ║"
echo "║  cd backend && source venv/bin/activate && python server.py                ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

