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

export interface NewsArticle {
  title: string
  description: string
  url: string
  published_at: string
  source: string
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
  topNews?: NewsArticle[]
  news?: NewsArticle[]
  crossovers?: Crossover[]
}

export type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error'

