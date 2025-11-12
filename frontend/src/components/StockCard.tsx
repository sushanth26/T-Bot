import { useState, useEffect } from 'react'
import { StockData } from '../types'
import './StockCard.css'

interface StockCardProps {
  symbol: string
  data?: StockData
  showOnlyInfo?: boolean
  showOnlyEmas?: boolean
}

interface ManualLevel {
  value: number
  label: string
}

const StockCard = ({ symbol, data, showOnlyInfo = false, showOnlyEmas = false }: StockCardProps) => {
  const [priceChange, setPriceChange] = useState<'up' | 'down' | 'neutral'>('neutral')
  const [prevPrice, setPrevPrice] = useState<number | undefined>()
  const [manualLevels, setManualLevels] = useState<ManualLevel[]>([])
  const [manualPrice, setManualPrice] = useState('')
  const [manualLabel, setManualLabel] = useState('Support')
  const [logoError, setLogoError] = useState(false)

  const addManualLevel = () => {
    const price = parseFloat(manualPrice)
    if (!isNaN(price) && manualLabel) {
      setManualLevels([...manualLevels, { value: price, label: manualLabel }])
      setManualPrice('')
      setManualLabel('Support')  // Reset to default
    }
  }

  const removeManualLevel = (index: number) => {
    setManualLevels(manualLevels.filter((_, i) => i !== index))
  }

  const currentPrice = data?.price || (data?.type === 'trade' ? data.price : data?.ask || data?.bid)
  const dayHigh = data?.dayHigh || 0
  const dayLow = data?.dayLow || 0
  const week52High = data?.week52High || 0
  const week52Low = data?.week52Low || 0

  useEffect(() => {
    if (currentPrice !== undefined && prevPrice !== undefined) {
      if (currentPrice > prevPrice) {
        setPriceChange('up')
      } else if (currentPrice < prevPrice) {
        setPriceChange('down')
      } else {
        setPriceChange('neutral')
      }
      
      // Reset animation after a short delay
      const timeout = setTimeout(() => {
        setPriceChange('neutral')
      }, 1000)
      
      return () => clearTimeout(timeout)
    }
  }, [currentPrice, prevPrice])

  useEffect(() => {
    if (currentPrice !== undefined) {
      setPrevPrice(currentPrice)
    }
  }, [currentPrice])

  const formatPrice = (price?: number) => {
    if (price === undefined || price === 0) return '--'
    return `$${price.toFixed(2)}`
  }

  const formatTimestamp = (timestamp?: string) => {
    if (!timestamp) return '--'
    try {
      const date = new Date(timestamp)
      return date.toLocaleString('en-US', { 
        month: 'short', 
        day: 'numeric', 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false
      })
    } catch {
      return '--'
    }
  }

  const getDayPosition = () => {
    if (!currentPrice || !dayHigh || !dayLow) return 50
    const range = dayHigh - dayLow
    if (range === 0) return 50
    return Math.max(0, Math.min(100, ((currentPrice - dayLow) / range) * 100))
  }

  const get52WeekPosition = () => {
    if (!currentPrice || !week52High || !week52Low) return 50
    const range = week52High - week52Low
    if (range === 0) return 50
    return Math.max(0, Math.min(100, ((currentPrice - week52Low) / range) * 100))
  }

  const getPriceChange = () => {
    if (!currentPrice || !prevPrice) return { absolute: 0, percent: 0 }
    const absolute = currentPrice - prevPrice
    const percent = (absolute / prevPrice) * 100
    return { absolute, percent }
  }

  const change = getPriceChange()

  // If showing only EMAs, render just that section
  if (showOnlyEmas) {
    return (
      <div className="ema-only-card">
        {data?.emas && Object.keys(data.emas).length > 0 && (() => {
          const allLevels = [
            ...(currentPrice ? [{ value: currentPrice, label: 'CURRENT', timeframe: 'Price', color: 'current', isPrice: true }] : []),
            ...manualLevels.map(ml => ({ value: ml.value, label: ml.label, timeframe: 'Manual', color: 'manual', isPrice: false })),
            ...(data.premarketLevels?.PMH ? [{ value: data.premarketLevels.PMH, label: 'PMH', timeframe: 'Premarket', color: 'premarket', isPrice: false }] : []),
            ...(data.premarketLevels?.PML ? [{ value: data.premarketLevels.PML, label: 'PML', timeframe: 'Premarket', color: 'premarket', isPrice: false }] : []),
            ...(data.emas['1h_ema_50'] ? [{ value: data.emas['1h_ema_50'], label: '50 EMA', timeframe: '1hr', color: 'hour', isPrice: false }] : []),
            ...(data.emas['1h_ema_34'] ? [{ value: data.emas['1h_ema_34'], label: '34 EMA', timeframe: '1hr', color: 'hour', isPrice: false }] : []),
            ...(data.emas['10m_ema_50'] ? [{ value: data.emas['10m_ema_50'], label: '50 EMA', timeframe: '10min', color: 'tenmin', isPrice: false }] : []),
            ...(data.emas['10m_ema_34'] ? [{ value: data.emas['10m_ema_34'], label: '34 EMA', timeframe: '10min', color: 'tenmin', isPrice: false }] : []),
            ...(data.emas['10m_ema_9'] ? [{ value: data.emas['10m_ema_9'], label: '9 EMA', timeframe: '10min', color: 'tenmin', isPrice: false }] : []),
            ...(data.emas['daily_ema_50'] ? [{ value: data.emas['daily_ema_50'], label: '50 EMA', timeframe: 'Daily', color: 'daily50', isPrice: false }] : []),
            ...(data.emas['daily_ema_20'] ? [{ value: data.emas['daily_ema_20'], label: '20 EMA', timeframe: 'Daily', color: 'daily20', isPrice: false }] : []),
          ]
          
          allLevels.sort((a, b) => b.value - a.value)
          
          return (
            <div className="ema-section">
              <div className="ema-header">
                <span>📊 All Levels (High → Low)</span>
                {/* Crossover Status Indicator */}
                <div className="crossover-status">
                  {data.crossovers && data.crossovers.length > 0 ? (
                    <span className="status-indicator active" title={`${data.crossovers.length} crossover(s) detected`}>
                      🚨 {data.crossovers.length} Alert{data.crossovers.length > 1 ? 's' : ''}
                    </span>
                  ) : (
                    <span className="status-indicator inactive" title="No crossovers detected">
                      ✅ No Alerts
                    </span>
                  )}
                </div>
              </div>
              
              {/* Premarket Crossover Alerts */}
              {data.crossovers && data.crossovers.length > 0 && (
                <div className="crossover-alerts">
                  <div className="crossover-header">🚨 Premarket EMA Crossovers</div>
                  {data.crossovers.map((cross, idx) => (
                    <div key={idx} className={`crossover-alert ${cross.type}`}>
                      <span className="crossover-direction">{cross.direction}</span>
                      <span className="crossover-message">{cross.message}</span>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="manual-entry">
                <div className="manual-entry-inputs">
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Price"
                    value={manualPrice}
                    onChange={(e) => setManualPrice(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addManualLevel()}
                    className="manual-price-input"
                  />
                  <select
                    value={manualLabel}
                    onChange={(e) => setManualLabel(e.target.value)}
                    className="manual-label-select"
                  >
                    <option value="Support">Support</option>
                    <option value="Resistance">Resistance</option>
                  </select>
                  <button onClick={addManualLevel} className="manual-add-btn">
                    ➕ Add
                  </button>
                </div>
                {manualLevels.length > 0 && (
                  <div className="manual-levels-list">
                    {manualLevels.map((ml, idx) => (
                      <div key={idx} className="manual-level-chip">
                        <span>${ml.value} - {ml.label}</span>
                        <button onClick={() => removeManualLevel(idx)} className="manual-remove-btn">
                          ✕
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
              
              <div className="ema-legend">
                <span className="legend-item">
                  <span className="legend-dot current"></span> Price
                </span>
                <span className="legend-item">
                  <span className="legend-dot premarket"></span> PM
                </span>
                <span className="legend-item">
                  <span className="legend-dot daily20"></span> D20
                </span>
                <span className="legend-item">
                  <span className="legend-dot daily50"></span> D50
                </span>
                <span className="legend-item">
                  <span className="legend-dot hour"></span> 1hr
                </span>
                <span className="legend-item">
                  <span className="legend-dot tenmin"></span> 10min
                </span>
                <span className="legend-item">
                  <span className="legend-dot manual"></span> Manual
                </span>
              </div>
              
              {/* Simple List View */}
              <div className="ema-list">
                {allLevels.map((level) => (
                  <div key={`${level.timeframe}-${level.label}`} className={`ema-list-item ${level.color} ${level.isPrice ? 'is-current-price' : ''}`}>
                    <span className="ema-list-label">
                      <span className="timeframe-badge">{level.timeframe}</span>
                      {level.label}
                    </span>
                    <span className="ema-list-value">${level.value.toFixed(2)}</span>
                  </div>
                ))}
              </div>
            </div>
          )
        })()}
      </div>
    )
  }

  // Reset logo error when symbol changes
  useEffect(() => {
    setLogoError(false)
  }, [symbol, data?.logoUrl])  // Also reset when logo URL changes

  // If showing only info, render compact view
  if (showOnlyInfo) {
    if (!data) return <div className="loading">Loading...</div>
    
    return (
      <div className="stock-info-compact">
        <div className="modern-header">
          <div className="symbol-section">
            {data?.logoUrl && !logoError ? (
              <img 
                src={data.logoUrl} 
                alt={symbol} 
                className="symbol-logo-img"
                onError={() => setLogoError(true)}
              />
            ) : (
              <div className="symbol-logo">⚡</div>
            )}
            <div className="symbol-info">
              <h1 className="symbol-ticker">{symbol}</h1>
              <div className="company-details">
                <span className="company-name">{data?.companyName || 'Loading...'}</span>
                <span className="separator">•</span>
                <span className="exchange">{data?.exchange || '--'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="price-section">
          {currentPrice !== undefined ? (
            <>
              <div className="current-price">
                <span className="price-large">{currentPrice.toFixed(2)}</span>
                <span className="currency">USD</span>
              </div>
              {prevPrice && (
                <div className={`price-change ${change.absolute >= 0 ? 'positive' : 'negative'}`}>
                  {change.absolute >= 0 ? '+' : ''}{change.absolute.toFixed(2)}
                  <span className="percent">({change.percent >= 0 ? '+' : ''}{change.percent.toFixed(2)}%)</span>
                </div>
              )}
            </>
          ) : (
            <div className="price-loading">Loading...</div>
          )}
          <div className="market-status">Market closed</div>
        </div>

        {data?.bid && data?.ask && (
          <div className="quote-details">
            <div className="quote-item">
              <span className="label">Bid</span>
              <span className="value">{formatPrice(data.bid)}</span>
            </div>
            <div className="quote-item">
              <span className="label">Ask</span>
              <span className="value">{formatPrice(data.ask)}</span>
            </div>
          </div>
        )}

        <div className="range-info">
          <div className="range-row">
            <span className="range-label">Day</span>
            <div className="range-bar-mini">
              <div className="range-fill" style={{ width: `${getDayPosition()}%` }}></div>
            </div>
            <span className="range-values">{formatPrice(dayLow)} - {formatPrice(dayHigh)}</span>
          </div>
          <div className="range-row">
            <span className="range-label">52W</span>
            <div className="range-bar-mini">
              <div className="range-fill" style={{ width: `${get52WeekPosition()}%` }}></div>
            </div>
            <span className="range-values">{formatPrice(week52Low)} - {formatPrice(week52High)}</span>
          </div>
        </div>
      </div>
    )
  }

  // Full card view
  return (
    <div className={`stock-card-modern ${priceChange}`}>
      {/* Header with Symbol and Company Info */}
      <div className="modern-header">
        <div className="symbol-section">
          <div className="symbol-logo">⚡</div>
          <div className="symbol-info">
            <h1 className="symbol-ticker">{symbol}</h1>
            <div className="company-details">
              <span className="company-name">{data?.companyName || 'Loading...'}</span>
              <span className="separator">•</span>
              <span className="exchange">{data?.exchange || '--'}</span>
            </div>
            <div className="industry-tags">
              <span>{data?.sector || '--'}</span>
              <span className="separator">•</span>
              <span>{data?.industry || '--'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Price Display */}
      <div className="price-section">
        {currentPrice !== undefined ? (
          <>
            <div className="current-price">
              <span className="price-large">{currentPrice.toFixed(2)}</span>
              <span className="currency">USD</span>
            </div>
            {prevPrice && (
              <div className={`price-change ${change.absolute >= 0 ? 'positive' : 'negative'}`}>
                {change.absolute >= 0 ? '+' : ''}{change.absolute.toFixed(2)}
                <span className="percent">({change.percent >= 0 ? '+' : ''}{change.percent.toFixed(2)}%)</span>
              </div>
            )}
          </>
        ) : (
          <div className="price-loading">Loading...</div>
        )}
        
        <div className="market-status">
          <span className="status-indicator">Market closed</span>
          <span className="separator">—</span>
          <span className="last-update">Last update at {formatTimestamp(data?.timestamp)}</span>
        </div>
      </div>

      {/* Bid/Ask Pills */}
      <div className="bid-ask-section">
        <div className="bid-pill">
          <span className="pill-label">BID</span>
          <span className="pill-value">{data?.bid?.toFixed(2) || '--'} × {data?.bidSize || 0}</span>
        </div>
        <div className="ask-pill">
          <span className="pill-label">ASK</span>
          <span className="pill-value">{data?.ask?.toFixed(2) || '--'} × {data?.askSize || 0}</span>
        </div>
      </div>

      {/* Day's Range - From API */}
      {dayHigh > 0 && dayLow > 0 && (
        <div className="range-section">
          <div className="range-header">
            <span className="range-low">{dayLow.toFixed(2)}</span>
            <span className="range-label">DAY'S RANGE</span>
            <span className="range-high">{dayHigh.toFixed(2)}</span>
          </div>
          <div className="range-bar-container">
            <div className="range-bar">
              <div 
                className="range-fill" 
                style={{ width: `${getDayPosition()}%` }}
              />
              <div 
                className="range-marker" 
                style={{ left: `${getDayPosition()}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {/* 52-Week Range - From API */}
      {week52High > 0 && week52Low > 0 && (
        <div className="range-section">
          <div className="range-header">
            <span className="range-low">{week52Low.toFixed(2)}</span>
            <span className="range-label">52WK RANGE</span>
            <span className="range-high">{week52High.toFixed(2)}</span>
          </div>
          <div className="range-bar-container">
            <div className="range-bar">
              <div 
                className="range-fill" 
                style={{ width: `${get52WeekPosition()}%` }}
              />
              <div 
                className="range-marker" 
                style={{ left: `${get52WeekPosition()}%` }}
              />
            </div>
          </div>
        </div>
      )}

      {data?.emas && Object.keys(data.emas).length > 0 && (() => {
        // Combine all EMAs + current price + manual levels into one sorted list
        const allLevels = [
          // Current Price
          ...(currentPrice ? [{ value: currentPrice, label: 'CURRENT', timeframe: 'Price', color: 'current', isPrice: true }] : []),
          
          // Manual Levels
          ...manualLevels.map(ml => ({ value: ml.value, label: ml.label, timeframe: 'Manual', color: 'manual', isPrice: false })),
          
          // PIVOT POINTS COMMENTED OUT
          // ...(data.pivots?.r3 ? [{ value: data.pivots.r3, label: 'R3', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          // ...(data.pivots?.r2 ? [{ value: data.pivots.r2, label: 'R2', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          // ...(data.pivots?.r1 ? [{ value: data.pivots.r1, label: 'R1', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          // ...(data.pivots?.pivot ? [{ value: data.pivots.pivot, label: 'PP', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          // ...(data.pivots?.s1 ? [{ value: data.pivots.s1, label: 'S1', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          // ...(data.pivots?.s2 ? [{ value: data.pivots.s2, label: 'S2', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          // ...(data.pivots?.s3 ? [{ value: data.pivots.s3, label: 'S3', timeframe: 'Pivot', color: 'pivot', isPrice: false }] : []),
          
          // 1 Hour EMAs
          ...(data.emas['1h_ema_50'] ? [{ value: data.emas['1h_ema_50'], label: '50 EMA', timeframe: '1hr', color: 'hour', isPrice: false }] : []),
          ...(data.emas['1h_ema_34'] ? [{ value: data.emas['1h_ema_34'], label: '34 EMA', timeframe: '1hr', color: 'hour', isPrice: false }] : []),
          
          // 10 Minute EMAs
          ...(data.emas['10m_ema_50'] ? [{ value: data.emas['10m_ema_50'], label: '50 EMA', timeframe: '10min', color: 'tenmin', isPrice: false }] : []),
          ...(data.emas['10m_ema_34'] ? [{ value: data.emas['10m_ema_34'], label: '34 EMA', timeframe: '10min', color: 'tenmin', isPrice: false }] : []),
          ...(data.emas['10m_ema_9'] ? [{ value: data.emas['10m_ema_9'], label: '9 EMA', timeframe: '10min', color: 'tenmin', isPrice: false }] : []),
          
          // Daily EMAs
          ...(data.emas['daily_ema_50'] ? [{ value: data.emas['daily_ema_50'], label: '50 EMA', timeframe: 'Daily', color: 'daily', isPrice: false }] : []),
          ...(data.emas['daily_ema_20'] ? [{ value: data.emas['daily_ema_20'], label: '20 EMA', timeframe: 'Daily', color: 'daily', isPrice: false }] : []),
        ]

        // Sort all items by value (high to low)
        allLevels.sort((a, b) => b.value - a.value)

        return (
          <div className="ema-section">
            <div className="ema-header">📊 All Levels (High → Low)</div>
            
            {/* Manual Entry UI */}
            <div className="manual-entry">
              <div className="manual-entry-inputs">
                <input
                  type="number"
                  step="0.01"
                  placeholder="Price"
                  value={manualPrice}
                  onChange={(e) => setManualPrice(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && addManualLevel()}
                  className="manual-price-input"
                />
                <select
                  value={manualLabel}
                  onChange={(e) => setManualLabel(e.target.value)}
                  className="manual-label-select"
                >
                  <option value="Support">Support</option>
                  <option value="Resistance">Resistance</option>
                </select>
                <button onClick={addManualLevel} className="manual-add-btn">
                  ➕ Add
                </button>
              </div>
              {manualLevels.length > 0 && (
                <div className="manual-levels-list">
                  {manualLevels.map((ml, idx) => (
                    <div key={idx} className="manual-level-chip">
                      <span>${ml.value} - {ml.label}</span>
                      <button onClick={() => removeManualLevel(idx)} className="manual-remove-btn">
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            <div className="ema-legend">
              <span className="legend-item">
                <span className="legend-dot current"></span> Price
              </span>
              {/* PIVOT LEGEND COMMENTED OUT */}
              {/* <span className="legend-item">
                <span className="legend-dot pivot"></span> Pivot
              </span> */}
              <span className="legend-item">
                <span className="legend-dot manual"></span> Manual
              </span>
              <span className="legend-item">
                <span className="legend-dot daily"></span> Daily
              </span>
              <span className="legend-item">
                <span className="legend-dot hour"></span> 1hr
              </span>
              <span className="legend-item">
                <span className="legend-dot tenmin"></span> 10min
              </span>
            </div>
            
            <div className="ema-list">
              {allLevels.map((level) => (
                <div key={`${level.timeframe}-${level.label}`} className={`ema-list-item ${level.color} ${level.isPrice ? 'is-current-price' : ''}`}>
                  <span className="ema-list-label">
                    <span className="timeframe-badge">{level.timeframe}</span>
                    {level.label}
                  </span>
                  <span className="ema-list-value">{formatPrice(level.value)}</span>
                </div>
              ))}
            </div>
          </div>
        )
      })()}

      {data?.error && (
        <div className="stock-error">
          <span>⚠️ {data.error}</span>
        </div>
      )}
    </div>
  )
}

export default StockCard

