import { motion } from 'framer-motion';

export default function ThreatCard({ threat, index, onClick }) {
  const analysis = threat.analysis || {};
  const score = analysis.predator_score || threat.predator_score || 0;
  
  const getSeverity = (score) => {
    if (score >= 90) return { color: 'danger', label: 'CRITICAL', bg: 'bg-danger/10', border: 'border-danger' };
    if (score >= 70) return { color: 'warning', label: 'HIGH', bg: 'bg-warning/10', border: 'border-warning' };
    return { color: 'yellow-500', label: 'MEDIUM', bg: 'bg-yellow-500/10', border: 'border-yellow-500' };
  };

  const severity = getSeverity(score);
  const metrics = analysis.metrics || {};
  const timeAgo = threat.timestamp ? getTimeAgo(new Date(threat.timestamp)) : 'Just now';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      onClick={onClick}
      className={`glass-card p-6 cursor-pointer hover:scale-[1.02] transition-all duration-300 border-l-4 ${severity.border}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${severity.bg} border border-${severity.color}/20 mb-2`}>
            <span className="text-xs font-bold" style={{ color: `var(--${severity.color})` }}>
              {severity.label} THREAT
            </span>
          </div>
          <h3 className="text-2xl font-bold">{threat.token || analysis.symbol}</h3>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold" style={{ color: score >= 90 ? '#ff0040' : score >= 70 ? '#ffa500' : '#fbbf24' }}>
            {score}
          </div>
          <div className="text-xs text-gray-400">/ 100</div>
        </div>
      </div>

      {/* Metrics */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Liquidity</span>
          <span className="font-mono">${formatNumber(metrics.liquidity)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">24h Volume</span>
          <span className="font-mono">${formatNumber(metrics.volume_24h)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Vol/Liq Ratio</span>
          <span className="font-mono text-danger">{metrics.vol_liq_ratio?.toFixed(1)}x ⚠️</span>
        </div>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-4 border-t border-white/10">
        <span className="text-xs text-gray-400">{timeAgo}</span>
        <button className="text-sm text-primary hover:text-primary/80 font-medium">
          View Details →
        </button>
      </div>
    </motion.div>
  );
}

function formatNumber(num) {
  if (!num) return '0';
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return num.toFixed(0);
}

function getTimeAgo(date) {
  const seconds = Math.floor((new Date() - date) / 1000);
  if (seconds < 60) return 'Just now';
  if (seconds < 3600) return Math.floor(seconds / 60) + ' mins ago';
  if (seconds < 86400) return Math.floor(seconds / 3600) + ' hours ago';
  return Math.floor(seconds / 86400) + ' days ago';
}
