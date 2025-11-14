export interface EMAs {
  // Legacy format
  ema_9?: number
  ema_20?: number
  ema_34?: number
  ema_50?: number
  ema_200?: number
  
  // Timeframe-specific format
  "1h_ema_34"?: number
  "1h_ema_50"?: number
  "10m_ema_9"?: number
  "10m_ema_34"?: number
  "10m_ema_50"?: number
  "daily_ema_20"?: number
  "daily_ema_50"?: number
}

export interface PivotPoints {
  pivot?: number
  r1?: number
  r2?: number
  r3?: number
  s1?: number
  s2?: number
  s3?: number
}


export interface Crossover {
  type: 'cross_above' | 'cross_below'
  ema: string
  ema_value: number
  direction: string
  message: string
}

export interface PremarketLevels {
  PMH?: number  // Premarket High
  PML?: number  // Premarket Low
}

export interface GrokAnalysis {
  sentiment: 'bullish' | 'bearish' | 'neutral'
  summary: string
  key_points: string[]
  trading_signals: string[]
  confidence: 'high' | 'medium' | 'low'
}

export interface SectorAnalysis {
  sector?: string
  industry?: string
  etf_symbol?: string
  weight_percentage?: number
  pe_ratio?: number
  peg_ratio?: number
  pb_ratio?: number
  market_cap?: number
  lowest_pe_peers?: Array<{
    symbol: string
    pe_ratio: number
  }>
}

export interface StockData {
  symbol: string
  companyName?: string
  exchange?: string
  sector?: string
  industry?: string
  logoUrl?: string
  type?: 'quote' | 'trade'
  price?: number
  bid?: number
  ask?: number
  bidSize?: number
  askSize?: number
  size?: number
  timestamp?: string
  dayHigh?: number
  dayLow?: number
  week52High?: number
  week52Low?: number
  lastUpdate: number
  error?: string
  emas?: EMAs
  premarketLevels?: PremarketLevels
  pivots?: PivotPoints
  grokAnalysis?: GrokAnalysis
  sectorAnalysis?: SectorAnalysis
  crossovers?: Crossover[]
}
