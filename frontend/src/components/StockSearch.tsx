import { useState, useEffect, useRef } from 'react'
import './StockSearch.css'

interface StockSearchProps {
  onSymbolChange: (symbol: string) => void
  currentSymbol: string
}

interface SearchResult {
  symbol: string
  name: string
  exchange: string
}

const POPULAR_STOCKS = ['TSLA', 'AAPL', 'GOOGL', 'MSFT', 'AMZN', 'NVDA', 'META', 'NFLX', 'AMD', 'COIN']

const StockSearch = ({ onSymbolChange, currentSymbol }: StockSearchProps) => {
  const [inputValue, setInputValue] = useState(currentSymbol)
  const [suggestions, setSuggestions] = useState<SearchResult[]>([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const searchRef = useRef<HTMLDivElement>(null)

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setShowSuggestions(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Fetch suggestions as user types
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (inputValue.trim().length < 1) {
        setSuggestions([])
        return
      }

      try {
        const response = await fetch(`http://localhost:8000/api/search/${inputValue}`)
        const data = await response.json()
        setSuggestions(data.results || [])
      } catch (error) {
        console.error('Search error:', error)
        setSuggestions([])
      }
    }

    const debounceTimer = setTimeout(fetchSuggestions, 300)
    return () => clearTimeout(debounceTimer)
  }, [inputValue])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    const symbol = inputValue.trim().toUpperCase()
    if (symbol) {
      onSymbolChange(symbol)
      setShowSuggestions(false)
    }
  }

  const handleQuickSelect = (symbol: string) => {
    setInputValue(symbol)
    onSymbolChange(symbol)
    setShowSuggestions(false)
  }

  const handleSuggestionClick = (result: SearchResult) => {
    setInputValue(result.symbol)
    onSymbolChange(result.symbol)
    setShowSuggestions(false)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value)
    if (e.target.value.trim().length > 0) {
      setShowSuggestions(true)
    }
  }

  return (
    <div className="stock-search" ref={searchRef}>
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          onFocus={() => inputValue.trim().length > 0 && setShowSuggestions(true)}
          placeholder="Search stocks (e.g., AAPL, Tesla)"
          className="search-input"
          autoComplete="off"
        />
        <button type="submit" className="search-button">
          🔍
        </button>
      </form>

      {showSuggestions && suggestions.length > 0 && (
        <div className="suggestions-dropdown">
          {suggestions.map((result, index) => (
            <div
              key={index}
              className="suggestion-item"
              onClick={() => handleSuggestionClick(result)}
            >
              <div className="suggestion-content">
                <div className="suggestion-symbol">{result.symbol}</div>
                <div className="suggestion-name">{result.name}</div>
              </div>
              <div className="suggestion-exchange">{result.exchange}</div>
            </div>
          ))}
        </div>
      )}

      <div className="quick-select">
        <div className="quick-label">Popular Stocks</div>
        <div className="quick-buttons">
          {POPULAR_STOCKS.map((symbol) => (
            <button
              key={symbol}
              className={`quick-btn ${currentSymbol === symbol ? 'active' : ''}`}
              onClick={() => handleQuickSelect(symbol)}
            >
              {symbol}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

export default StockSearch
