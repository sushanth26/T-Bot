import React from 'react';
import { SectorAnalysis } from '../types';
import './SectorInfo.css';

interface SectorInfoProps {
  analysis: SectorAnalysis;
  sector?: string;
  industry?: string;
}

const SectorInfo: React.FC<SectorInfoProps> = ({ analysis, sector, industry }) => {
  const formatNumber = (num: number | undefined) => {
    if (!num) return 'N/A';
    if (num >= 1000000000) return `$${(num / 1000000000).toFixed(2)}B`;
    if (num >= 1000000) return `$${(num / 1000000).toFixed(2)}M`;
    return `$${num.toFixed(2)}`;
  };

  const formatRatio = (num: number | undefined) => {
    if (!num) return 'N/A';
    return num.toFixed(2);
  };

  // Use sector from props or from analysis
  const displaySector = sector || analysis.sector;
  const displayIndustry = industry || analysis.industry;

  return (
    <div className="sector-info-card">
      <div className="sector-info-header">
        <h3>📊 Sector & Valuation</h3>
      </div>

      <div className="sector-info-content">
        {/* Sector Name - Prominently displayed */}
        {displaySector && (
          <div className="info-section sector-name-section">
            <div className="info-label">Sector</div>
            <div className="info-value sector-name">{displaySector}</div>
          </div>
        )}

        {/* Industry */}
        {displayIndustry && (
          <div className="info-section">
            <div className="info-label">Industry</div>
            <div className="info-value">{displayIndustry}</div>
          </div>
        )}

        {/* P/E Ratio */}
        {analysis.pe_ratio && (
          <div className="info-section highlight">
            <div className="info-label">P/E Ratio</div>
            <div className="info-value pe-value">{formatRatio(analysis.pe_ratio)}</div>
          </div>
        )}

        {/* Market Cap */}
        {analysis.market_cap && (
          <div className="info-section">
            <div className="info-label">Market Cap</div>
            <div className="info-value">{formatNumber(analysis.market_cap)}</div>
          </div>
        )}

        {/* Other Ratios */}
        <div className="ratios-grid">
          {analysis.peg_ratio && (
            <div className="ratio-item">
              <div className="ratio-label">PEG</div>
              <div className="ratio-value">{formatRatio(analysis.peg_ratio)}</div>
            </div>
          )}
          {analysis.pb_ratio && (
            <div className="ratio-item">
              <div className="ratio-label">P/B</div>
              <div className="ratio-value">{formatRatio(analysis.pb_ratio)}</div>
            </div>
          )}
        </div>

        {/* Lowest P/E Peers */}
        {analysis.lowest_pe_peers && analysis.lowest_pe_peers.length > 0 && (
          <div className="peers-section">
            <div className="peers-header">🏆 Lowest P/E in Sector</div>
            <div className="peers-list">
              {analysis.lowest_pe_peers.map((peer, index) => (
                <div key={peer.symbol} className="peer-item">
                  <span className="peer-rank">{index + 1}</span>
                  <span className="peer-symbol">{peer.symbol}</span>
                  <span className="peer-pe">{formatRatio(peer.pe_ratio)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SectorInfo;

