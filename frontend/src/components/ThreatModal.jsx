import { motion, AnimatePresence } from 'framer-motion';
import { useEffect } from 'react';

export default function ThreatModal({ threat, onClose }) {
  const analysis = threat.analysis || {};
  const score = analysis.predator_score || threat.predator_score || 0;
  const metrics = analysis.metrics || {};
  const forensics = analysis.forensics_report || [];

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onClose]);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
          className="glass-card max-w-4xl w-full max-h-[90vh] overflow-y-auto p-8"
        >
          {/* Header */}
          <div className="flex items-start justify-between mb-6">
            <div>
              <div className="text-sm text-gray-400 mb-2">THREAT ANALYSIS</div>
              <h2 className="text-4xl font-bold mb-2">{threat.token || analysis.symbol}</h2>
              <p className="text-sm text-gray-400 font-mono">{analysis.address}</p>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white text-2xl"
            >
              ×
            </button>
          </div>

          {/* Predator Score */}
          <div className="mb-8 p-6 rounded-xl bg-gradient-to-r from-danger/20 to-warning/20 border border-danger/30">
            <div className="text-sm text-gray-300 mb-2">PREDATOR SCORE</div>
            <div className="text-6xl font-bold" style={{ color: score >= 90 ? '#ff0040' : '#ffa500' }}>
              {score}<span className="text-2xl text-gray-400">/100</span>
            </div>
          </div>

          {/* Metrics */}
          <div className="mb-8">
            <h3 className="text-xl font-bold mb-4">📊 Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="glass-card p-4">
                <div className="text-sm text-gray-400 mb-1">Liquidity</div>
                <div className="text-2xl font-bold">${formatNumber(metrics.liquidity)}</div>
              </div>
              <div className="glass-card p-4">
                <div className="text-sm text-gray-400 mb-1">24h Volume</div>
                <div className="text-2xl font-bold">${formatNumber(metrics.volume_24h)}</div>
              </div>
              <div className="glass-card p-4">
                <div className="text-sm text-gray-400 mb-1">Vol/Liq Ratio</div>
                <div className="text-2xl font-bold text-danger">{metrics.vol_liq_ratio?.toFixed(1)}x</div>
              </div>
            </div>
          </div>

          {/* Forensics Report */}
          <div className="mb-8">
            <h3 className="text-xl font-bold mb-4">🔍 Forensics Report</h3>
            <div className="space-y-4">
              {forensics.map((finding, index) => (
                <div key={index} className="glass-card p-4">
                  <div className="flex items-start gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                      {index + 1}
                    </div>
                    <p className="text-gray-300 leading-relaxed">{finding}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Analysis */}
          {analysis.fraud_analysis && (
            <div className="mb-8">
              <h3 className="text-xl font-bold mb-4">🤖 AI Consensus</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="glass-card p-4">
                  <div className="text-sm text-gray-400 mb-2">Fraud Analyst</div>
                  <div className="text-lg font-bold mb-1">{analysis.fraud_analysis.threat_level}</div>
                  <div className="text-sm text-primary">Confidence: {analysis.fraud_analysis.confidence}%</div>
                </div>
                <div className="glass-card p-4">
                  <div className="text-sm text-gray-400 mb-2">Behavioral Psychologist</div>
                  <div className="text-lg font-bold mb-1">{analysis.behavior_analysis?.threat_level}</div>
                  <div className="text-sm text-primary">Confidence: {analysis.behavior_analysis?.confidence}%</div>
                </div>
              </div>
            </div>
          )}

          {/* Warning */}
          <div className="p-4 rounded-xl bg-danger/10 border border-danger/30 text-center">
            <div className="text-2xl mb-2">⚠️</div>
            <div className="font-bold text-danger">PROCEED WITH EXTREME CAUTION</div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}

function formatNumber(num) {
  if (!num) return '0';
  if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(2) + 'K';
  return num.toFixed(2);
}
