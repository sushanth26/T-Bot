#!/bin/bash

# Setup script for Financial Modeling Prep API key
# Get your free API key at: https://financialmodelingprep.com/developer/docs/

echo "📊 Setting up Financial Modeling Prep API..."
echo ""
echo "Get your FREE API key at: https://financialmodelingprep.com/developer/docs/"
echo ""
read -p "Enter your FMP API key: " FMP_KEY

if [ -z "$FMP_KEY" ]; then
    echo "❌ No API key entered"
    exit 1
fi

# Add to .env file
if grep -q "FMP_API_KEY" .env 2>/dev/null; then
    # Update existing key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/FMP_API_KEY=.*/FMP_API_KEY=$FMP_KEY/" .env
    else
        sed -i "s/FMP_API_KEY=.*/FMP_API_KEY=$FMP_KEY/" .env
    fi
    echo "✅ FMP API key updated in .env"
else
    # Add new key
    echo "FMP_API_KEY=$FMP_KEY" >> .env
    echo "✅ FMP API key added to .env"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "You can now use:"
echo "  • ETF holdings analysis"
echo "  • P/E ratios and financial metrics"
echo "  • Sector peer comparison"
echo ""
echo "Example: analyze_sector_position('NVDA', 'SOXX')"

