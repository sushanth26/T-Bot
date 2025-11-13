#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  🤖 GROK AI SETUP                                                          ║"
echo "╠════════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                            ║"
echo "║  Grok by xAI provides AI-powered news analysis:                            ║"
echo "║  • Sentiment analysis (bullish/bearish/neutral)                            ║"
echo "║  • News summarization                                                      ║"
echo "║  • Key insights extraction                                                 ║"
echo "║  • Trading signals                                                         ║"
echo "║                                                                            ║"
echo "╠════════════════════════════════════════════════════════════════════════════╣"
echo "║  STEPS TO GET YOUR GROK API KEY:                                           ║"
echo "║                                                                            ║"
echo "║  1. Visit: https://console.x.ai/                                           ║"
echo "║  2. Sign up or log in with your account                                    ║"
echo "║  3. Go to API Keys section                                                 ║"
echo "║  4. Create a new API key                                                   ║"
echo "║  5. Copy your API key                                                      ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Enter your Grok API key (or press Enter to skip):"
read -r GROK_KEY

if [ -z "$GROK_KEY" ]; then
    echo ""
    echo "⚠️  No API key entered. Grok analysis will not work."
    echo "   You can add it later to backend/.env:"
    echo "   GROK_API_KEY=your_key_here"
    exit 0
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Please run this script from the backend directory"
    exit 1
fi

# Check if GROK_API_KEY already exists
if grep -q "GROK_API_KEY=" .env; then
    # Update existing key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/GROK_API_KEY=.*/GROK_API_KEY=$GROK_KEY/" .env
    else
        # Linux
        sed -i "s/GROK_API_KEY=.*/GROK_API_KEY=$GROK_KEY/" .env
    fi
    echo "✅ Updated GROK_API_KEY in .env"
else
    # Add new key
    echo "" >> .env
    echo "# Grok AI (xAI) API" >> .env
    echo "GROK_API_KEY=$GROK_KEY" >> .env
    echo "✅ Added GROK_API_KEY to .env"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║  ✅ SETUP COMPLETE!                                                        ║"
echo "╠════════════════════════════════════════════════════════════════════════════╣"
echo "║                                                                            ║"
echo "║  Your Grok API key has been added to .env                                  ║"
echo "║                                                                            ║"
echo "║  Next steps:                                                               ║"
echo "║  1. Restart your backend server                                            ║"
echo "║  2. Grok will analyze news automatically                                   ║"
echo "║  3. See AI insights in the UI                                              ║"
echo "║                                                                            ║"
echo "║  To restart server:                                                        ║"
echo "║  cd backend && source venv/bin/activate && python server.py                ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"

