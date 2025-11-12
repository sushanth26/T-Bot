import { useState, useEffect } from 'react'
import './App.css'
import StockCard from './components/StockCard'
import StockSearch from './components/StockSearch'
import ConnectionStatus from './components/ConnectionStatus'
import { StockData, ConnectionStatus as ConnStatus } from './types'
import { StockInfoSkeleton, EMAListSkeleton, NewsSkeleton, TopNewsSkeleton } from './components/Skeleton'

function App() {
  const [currentSymbol, setCurrentSymbol] = useState('TSLA')
  const [stockData, setStockData] = useState<Record<string, StockData>>({})
  const [connectionStatus, setConnectionStatus] = useState<ConnStatus>('connected')

  // Fetch data for current symbol every 2 seconds
  useEffect(() => {
    const fetchQuotes = () => {
      setConnectionStatus('connecting')
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
          setConnectionStatus('connected')
        })
        .catch((err) => {
          console.error('Failed to fetch quotes:', err)
          setConnectionStatus('error')
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
          <ConnectionStatus status={connectionStatus} />
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
            <div className="stock-info-sidebar">
              <StockCard
                key={`info-${currentSymbol}`}
                symbol={currentSymbol}
                data={stockData[currentSymbol]}
                showOnlyInfo={true}
              />
            </div>
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
              
              {/* Latest News Section - Moved under All Levels */}
              <div className="regular-news-section">
                <div className="news-sidebar-header">📰 Latest News</div>
                {stockData[currentSymbol]?.news && stockData[currentSymbol].news.length > 0 ? (
                  <div className="news-sidebar-list">
                    {stockData[currentSymbol].news.map((article, index) => (
                      <a 
                        key={`news-${index}`}
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="news-sidebar-item"
                      >
                        <div className="news-sidebar-title">{article.title}</div>
                        {article.description && (
                          <div className="news-sidebar-description">{article.description}</div>
                        )}
                        <div className="news-sidebar-meta">
                          <span className="news-sidebar-source">{article.source}</span>
                          <span className="news-sidebar-date">
                            {new Date(article.published_at).toLocaleString('en-US', {
                              month: 'short',
                              day: 'numeric',
                              hour: 'numeric',
                              minute: '2-digit',
                            })}
                          </span>
                        </div>
                      </a>
                    ))}
                  </div>
                ) : (
                  <NewsSkeleton count={5} />
                )}
              </div>
            </>
          ) : (
            <>
              <EMAListSkeleton />
              <div className="regular-news-section">
                <div className="news-sidebar-header">📰 Latest News</div>
                <NewsSkeleton count={5} />
              </div>
            </>
          )}
        </div>

        <div className="news-sidebar">
          {/* Top News Section - Only in 3rd Column */}
          <div className="news-sidebar-header top-news-header">🔥 Top News (Upgrades/Analyst Ratings)</div>
          {stockData[currentSymbol]?.topNews && stockData[currentSymbol].topNews.length > 0 ? (
            <div className="news-sidebar-list">
              {stockData[currentSymbol].topNews.map((article, index) => (
                <a 
                  key={`top-${index}`}
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="news-sidebar-item top-news-item"
                >
                  <div className="news-sidebar-title">{article.title}</div>
                  {article.description && (
                    <div className="news-sidebar-description">{article.description}</div>
                  )}
                  <div className="news-sidebar-meta">
                    <span className="news-sidebar-source">{article.source}</span>
                    <span className="news-sidebar-date">
                      {new Date(article.published_at).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: 'numeric',
                        minute: '2-digit',
                      })}
                    </span>
                  </div>
                </a>
              ))}
            </div>
          ) : stockData[currentSymbol] && stockData[currentSymbol].price > 0 ? (
            <div className="news-sidebar-empty">No analyst ratings or upgrades in last 7 days</div>
          ) : (
            <TopNewsSkeleton />
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

