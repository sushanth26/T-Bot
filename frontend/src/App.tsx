import { useState, useEffect } from 'react'
import './App.css'
import StockCard from './components/StockCard'
import StockSearch from './components/StockSearch'
import GrokInsights from './components/GrokInsights'
import SectorInfo from './components/SectorInfo'
import { StockData } from './types'
import { StockInfoSkeleton, EMAListSkeleton } from './components/Skeleton'
import { useGrokStream } from './hooks/useGrokStream'

function App() {
  const [currentSymbol, setCurrentSymbol] = useState('TSLA')
  const [stockData, setStockData] = useState<Record<string, StockData>>({})
  
  // Use streaming hook for Grok analysis
  const { analysis: grokAnalysis, streamingText, isStreaming } = useGrokStream(currentSymbol)

  // Fetch data for current symbol every 2 seconds
  useEffect(() => {
    const fetchQuotes = () => {
      fetch(`http://localhost:8000/api/quotes/${currentSymbol}`)
        .then((res) => {
          if (!res.ok) throw new Error('Failed to fetch')
          return res.json()
        })
        .then((quote) => {
          setStockData({
            [currentSymbol]: {
              ...quote,
              lastUpdate: Date.now(),
            }
          })
        })
        .catch((err) => {
          console.error('Failed to fetch quotes:', err)
        })
    }
    
    // Fetch immediately when symbol changes
    fetchQuotes()
    
    // Then fetch every 2 seconds
    const interval = setInterval(fetchQuotes, 2000)
    
    return () => clearInterval(interval)
  }, [currentSymbol])

  const handleSymbolChange = (newSymbol: string) => {
    setCurrentSymbol(newSymbol)
    setStockData({}) // Clear old data
  }

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1 className="title">
            <span className="title-icon">📈</span>
            Stock Monitor
          </h1>
        </div>
      </header>

      <main className="main">
        <div className="search-sidebar">
          <StockSearch 
            onSymbolChange={handleSymbolChange}
            currentSymbol={currentSymbol}
          />
          
          {/* Stock Info Section */}
          {stockData[currentSymbol] && stockData[currentSymbol].price > 0 ? (
            <>
              <div className="stock-info-sidebar">
                <StockCard
                  key={`info-${currentSymbol}`}
                  symbol={currentSymbol}
                  data={stockData[currentSymbol]}
                  showOnlyInfo={true}
                />
              </div>
              
              {/* Sector Analysis Section */}
              {stockData[currentSymbol].sectorAnalysis && 
               (stockData[currentSymbol].sectorAnalysis?.pe_ratio || 
                stockData[currentSymbol].sectorAnalysis?.lowest_pe_peers?.length) && (
                <div className="sector-info-sidebar">
                  <SectorInfo
                    analysis={stockData[currentSymbol].sectorAnalysis}
                    sector={stockData[currentSymbol].sector}
                    industry={stockData[currentSymbol].industry}
                  />
                </div>
              )}
            </>
          ) : (
            <div className="stock-info-sidebar">
              <StockInfoSkeleton />
            </div>
          )}
        </div>
        
        <div className="ema-grid">
          {stockData[currentSymbol] && stockData[currentSymbol].price > 0 ? (
            <>
              <StockCard
                key={`emas-${currentSymbol}`}
                symbol={currentSymbol}
                data={stockData[currentSymbol]}
                showOnlyEmas={true}
              />
              
              {/* News hidden - Grok analyzes it behind the scenes */}
            </>
          ) : (
            <EMAListSkeleton />
          )}
        </div>

        <div className="grok-sidebar">
          {/* Grok AI Insights - use cached first, then streaming */}
          {isStreaming ? (
            <div className="grok-loading-container">
              <div className="grok-loading">
                <div className="grok-logo-large">🤖</div>
                <div>Analyzing news with Grok AI...</div>
                {streamingText && (
                  <div className="streaming-text">{streamingText}</div>
                )}
              </div>
            </div>
          ) : (grokAnalysis || stockData[currentSymbol]?.grokAnalysis) ? (
            <GrokInsights analysis={grokAnalysis || stockData[currentSymbol]?.grokAnalysis!} />
          ) : (
            <div className="grok-loading-container">
              <div className="grok-loading">
                <div className="grok-logo-large">🤖</div>
                <div>Loading Grok analysis...</div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">
        <p>Powered by Alpaca Markets • Real-time data & EMAs</p>
      </footer>
    </div>
  )
}

export default App

