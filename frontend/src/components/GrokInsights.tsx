import { GrokAnalysis } from '../types'
import './GrokInsights.css'

interface GrokInsightsProps {
  analysis?: GrokAnalysis
}

const GrokInsights = ({ analysis }: GrokInsightsProps) => {
  if (!analysis || !analysis.summary) {
    return null
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish': return 'bullish'
      case 'bearish': return 'bearish'
      default: return 'neutral'
    }
  }

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'bullish': return '📈'
      case 'bearish': return '📉'
      default: return '➡️'
    }
  }

  const getConfidenceBadge = (confidence: string) => {
    switch (confidence) {
      case 'high': return '🟢 High'
      case 'medium': return '🟡 Medium'
      case 'low': return '🔴 Low'
      default: return '⚪ Unknown'
    }
  }

  return (
    <div className="grok-insights">
      <div className="grok-header">
        <span className="grok-logo">🤖 Grok AI Insights</span>
        <span className="grok-confidence">{getConfidenceBadge(analysis.confidence)}</span>
      </div>

      <div className={`grok-sentiment ${getSentimentColor(analysis.sentiment)}`}>
        <span className="sentiment-icon">{getSentimentIcon(analysis.sentiment)}</span>
        <span className="sentiment-text">{analysis.sentiment.toUpperCase()}</span>
      </div>

      <div className="grok-summary">
        <div className="grok-section-title">Summary</div>
        <p>{analysis.summary}</p>
      </div>

      {analysis.key_points && analysis.key_points.length > 0 && (
        <div className="grok-key-points">
          <div className="grok-section-title">Key Points</div>
          <ul>
            {analysis.key_points.map((point, idx) => (
              <li key={idx}>{point}</li>
            ))}
          </ul>
        </div>
      )}

      {analysis.trading_signals && analysis.trading_signals.length > 0 && (
        <div className="grok-trading-signals">
          <div className="grok-section-title">Trading Signals</div>
          <ul>
            {analysis.trading_signals.map((signal, idx) => (
              <li key={idx}>{signal}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="grok-footer">
        <span className="grok-powered">Powered by Grok (xAI)</span>
        <span className="grok-disclaimer">Not financial advice</span>
      </div>
    </div>
  )
}

export default GrokInsights

