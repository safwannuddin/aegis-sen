import React from 'react';
import { motion } from 'framer-motion';

export default function ThreatCard({ threat, index, onClick }) {
  const analysis = threat.analysis || {};
  const score = analysis.predator_score || threat.predator_score || 0;
  
  const getSeverity = (score) => {
    if (score >= 90) return { color: 'text-danger', label: 'CRITICAL' };
    if (score >= 70) return { color: 'text-warning', label: 'HIGH' };
    if (score > 0) return { color: 'text-yellow-500', label: 'SUSP' };
    return { color: 'text-primary', label: 'SAFE' };
  };

  const severity = getSeverity(score);
  const metrics = analysis.metrics || {};
  const forensics = analysis.forensics_report || [];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: index * 0.05 }}
      onClick={onClick}
      className="grid grid-cols-12 gap-4 p-3 intel-row items-center text-[11px]"
    >
      <div className="col-span-2 flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: severity.color.includes('danger') ? '#ff0040' : severity.color.includes('warning') ? '#ffa500' : '#fbbf24' }} />
        <span className="font-black text-white">{threat.token || analysis.symbol}</span>
        <span className="text-[9px] opacity-20 truncate">{analysis.address}</span>
      </div>

      <div className={`col-span-1 text-center font-black ${severity.color}`}>
        {score}
      </div>

      <div className="col-span-2 text-right font-mono text-white/60">
        ${formatNumber(metrics.liquidity)}
      </div>

      <div className="col-span-2 text-right font-mono text-white/60">
        ${formatNumber(metrics.volume_24h)}
      </div>

      <div className="col-span-4 truncate text-white/40 italic">
        {forensics[0] || 'Analyzing on-chain behavior...'}
      </div>

      <div className="col-span-1 text-right">
        <span className={`status-pill ${severity.color} border-current opacity-70`}>
          {severity.label}
        </span>
      </div>
    </motion.div>
  );
}

function formatNumber(num) {
  if (!num) return '0';
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return Math.floor(num).toLocaleString();
}
