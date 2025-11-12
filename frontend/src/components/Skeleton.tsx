import './Skeleton.css'

export const StockInfoSkeleton = () => {
  return (
    <div className="skeleton-card">
      <div className="skeleton-header">
        <div className="skeleton-logo"></div>
        <div className="skeleton-text skeleton-title"></div>
      </div>
      <div className="skeleton-price"></div>
      <div className="skeleton-text skeleton-small"></div>
      <div className="skeleton-text skeleton-small"></div>
      <div className="skeleton-divider"></div>
      <div className="skeleton-text skeleton-medium"></div>
      <div className="skeleton-text skeleton-medium"></div>
      <div className="skeleton-text skeleton-medium"></div>
    </div>
  )
}

export const EMAListSkeleton = () => {
  return (
    <div className="skeleton-card">
      <div className="skeleton-text skeleton-title"></div>
      <div className="skeleton-divider"></div>
      {[1, 2, 3, 4, 5, 6, 7].map((i) => (
        <div key={i} className="skeleton-ema-item">
          <div className="skeleton-dot"></div>
          <div className="skeleton-text skeleton-medium"></div>
        </div>
      ))}
    </div>
  )
}

export const NewsSkeleton = ({ count = 3 }: { count?: number }) => {
  return (
    <div className="skeleton-news-list">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="skeleton-news-item">
          <div className="skeleton-text skeleton-title"></div>
          <div className="skeleton-text skeleton-small"></div>
          <div className="skeleton-text skeleton-small"></div>
          <div className="skeleton-footer">
            <div className="skeleton-text skeleton-tiny"></div>
            <div className="skeleton-text skeleton-tiny"></div>
          </div>
        </div>
      ))}
    </div>
  )
}

export const TopNewsSkeleton = () => {
  return (
    <div className="skeleton-news-list">
      {[1, 2, 3].map((i) => (
        <div key={i} className="skeleton-news-item skeleton-top-news-item">
          <div className="skeleton-star">⭐</div>
          <div className="skeleton-text skeleton-title"></div>
          <div className="skeleton-text skeleton-small"></div>
          <div className="skeleton-text skeleton-small"></div>
          <div className="skeleton-footer">
            <div className="skeleton-text skeleton-tiny"></div>
            <div className="skeleton-text skeleton-tiny"></div>
          </div>
        </div>
      ))}
    </div>
  )
}

