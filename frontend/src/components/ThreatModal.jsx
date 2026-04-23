import { motion } from 'framer-motion';
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

  const severityColor = score >= 90 ? '#ff0040' : score >= 70 ? '#ffa500' : '#fbbf24';

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/95 z-[100] flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.98, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.98, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="terminal-border bg-black max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-[0_0_50px_rgba(0,0,0,1)]"
      >
        {/* Terminal Header */}
        <div className="bg-[#111] p-3 border-b border-white/5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full bg-[#ff5f56]" />
              <div className="w-2.5 h-2.5 rounded-full bg-[#ffbd2e]" />
              <div className="w-2.5 h-2.5 rounded-full bg-[#27c93f]" />
            </div>
            <div className="h-4 w-[1px] bg-white/10 mx-2" />
            <span className="text-[10px] font-black text-white/40 tracking-[0.3em]">INTELLIGENCE_DOSSIER::{threat.token || analysis.symbol}</span>
          </div>
          <button onClick={onClose} className="text-white/20 hover:text-white text-xs">CLOSE [ESC]</button>
        </div>

        <div className="flex-1 overflow-y-auto p-8 font-mono">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="md:col-span-2">
              <div className="text-[10px] text-primary/60 mb-2 tracking-widest uppercase font-black">{'>'} TARGET_METADATA</div>
              <h2 className="text-5xl font-black text-white tracking-tighter mb-4 uppercase">{threat.token || analysis.symbol}</h2>
              <div className="p-3 bg-white/[0.02] border border-white/5 text-[10px] text-white/40 break-all mb-6">
                ADDR: {analysis.address}
              </div>
              
              <div className="grid grid-cols-3 gap-4">
                <MetricItem label="LIQUIDITY" value={`$${formatNumber(metrics.liquidity)}`} />
                <MetricItem label="24H_VOLUME" value={`$${formatNumber(metrics.volume_24h)}`} />
                <MetricItem label="VOL_LIQ_RATIO" value={`${metrics.vol_liq_ratio?.toFixed(1)}x`} />
              </div>
            </div>

            <div className="flex flex-col items-center justify-center p-6 border border-white/5 bg-white/[0.01] rounded-lg">
              <div className="text-[10px] text-white/20 mb-4 tracking-widest font-black uppercase">PREDATOR_SCORE</div>
              <div className="text-7xl font-black mb-2 tracking-tighter" style={{ color: severityColor }}>{score}</div>
              <div className="text-[10px] font-black uppercase tracking-widest py-1 px-3 border" style={{ borderColor: severityColor, color: severityColor }}>
                {score >= 90 ? 'CRITICAL' : score >= 70 ? 'HIGH_RISK' : 'SUSPICIOUS'}
              </div>
            </div>
          </div>

          <div className="space-y-8">
            <section>
              <div className="text-[10px] text-primary/60 mb-4 tracking-widest uppercase font-black">{'>'} ON_CHAIN_FORENSICS</div>
              <div className="space-y-1">
                {forensics.map((finding, i) => (
                  <div key={i} className="p-3 border-l-2 border-primary/20 bg-white/[0.01] text-xs text-white/60 leading-relaxed">
                    <span className="text-primary/40 mr-3">[{i.toString().padStart(2, '0')}]</span>
                    {finding}
                  </div>
                ))}
              </div>
            </section>

            {analysis.fraud_analysis && (
              <section>
                <div className="text-[10px] text-primary/60 mb-4 tracking-widest uppercase font-black">{'>'} MULTI_AGENT_CONSENSUS</div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <AgentBox name="FRAUD_ANALYST" status={analysis.fraud_analysis.threat_level} conf={analysis.fraud_analysis.confidence} />
                  <AgentBox name="BEHAVIORAL_PSYCH" status={analysis.behavior_analysis?.threat_level} conf={analysis.behavior_analysis?.confidence} />
                </div>
              </section>
            )}
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

function MetricItem({ label, value }) {
  return (
    <div>
      <div className="text-[8px] text-white/20 mb-1 font-black tracking-widest uppercase">{label}</div>
      <div className="text-sm font-black text-white">{value}</div>
    </div>
  );
}

function AgentBox({ name, status, conf }) {
  return (
    <div className="p-4 border border-white/5 bg-white/[0.01]">
      <div className="text-[8px] text-white/20 mb-2 font-black tracking-widest uppercase">{name}</div>
      <div className="text-sm font-black text-white mb-2 uppercase tracking-tighter">{status}</div>
      <div className="w-full h-0.5 bg-white/5 overflow-hidden">
        <div className="h-full bg-primary" style={{ width: `${conf}%` }} />
      </div>
      <div className="mt-1 text-[8px] text-primary/40 font-black text-right">{conf}%_CONFIDENCE</div>
    </div>
  );
}

function formatNumber(num) {
  if (!num) return '0';
  if (num >= 1000000) return (num / 1000000).toFixed(2) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(2) + 'K';
  return num.toLocaleString();
}
