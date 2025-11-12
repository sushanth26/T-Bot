#!/bin/bash

echo "=========================================="
echo "📊 TESLA (TSLA) EMA Data Test"
echo "=========================================="
echo ""

echo "1️⃣  Multi-Timeframe EMA for TSLA:"
echo "   (1hr: 34,50 EMA | 10min: 9,34,50 EMA)"
echo ""
curl -s http://localhost:8000/api/multi-timeframe-ema/TSLA | python3 -m json.tool
echo ""
echo "=========================================="
echo ""

echo "2️⃣  TSLA Options Data:"
echo ""
curl -s http://localhost:8000/api/options/TSLA | python3 -m json.tool
echo ""
echo "=========================================="
echo ""

echo "3️⃣  1-Hour 34,50 EMA for TSLA:"
echo ""
curl -s 'http://localhost:8000/api/ema/TSLA?timeframe=1Hour&periods=34,50' | python3 -m json.tool
echo ""
echo "=========================================="
echo ""

echo "4️⃣  10-Min 9,34,50 EMA for TSLA:"
echo ""
curl -s 'http://localhost:8000/api/ema/TSLA?timeframe=10Min&periods=9,34,50' | python3 -m json.tool
echo ""
echo "=========================================="
echo ""

echo "5️⃣  All Stocks with Daily EMAs:"
echo ""
curl -s http://localhost:8000/api/quotes-with-ema | python3 -m json.tool | head -50
echo ""
echo "=========================================="
echo ""

echo "✅ Test Complete!"
echo ""
echo "📝 Note: Intraday EMAs (1hr, 10min) require:"
echo "   - Market hours (9:30 AM - 4:00 PM ET)"
echo "   - Recent trading activity"
echo "   - Alpaca data subscription"
echo ""
echo "💡 During market hours, these EMAs update in real-time!"

