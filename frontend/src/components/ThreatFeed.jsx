import { motion } from 'framer-motion';
import ThreatCard from './ThreatCard';

export default function ThreatFeed({ threats, loading, onThreatClick }) {
  if (loading && threats.length === 0) {
    return (
      <div className="space-y-1">
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} className="h-10 w-full bg-white/[0.02] border border-white/5 animate-pulse" />
        ))}
      </div>
    );
  }

  return (
    <div className="terminal-border bg-terminal-bg/50 overflow-hidden">
      {/* Table Header */}
      <div className="grid grid-cols-12 gap-4 p-3 bg-white/[0.02] border-b border-white/5 text-[10px] font-black uppercase tracking-widest text-white/40">
        <div className="col-span-2">Token / Symbol</div>
        <div className="col-span-1 text-center">Score</div>
        <div className="col-span-2 text-right">Liquidity</div>
        <div className="col-span-2 text-right">24h Vol</div>
        <div className="col-span-4">Forensics Snippet</div>
        <div className="col-span-1 text-right">Status</div>
      </div>

      <div className="divide-y divide-white/5">
        {threats.length === 0 ? (
          <div className="p-12 text-center text-white/20 italic text-xs tracking-widest">
            AWAITING ANOMALOUS ACTIVITY... NETWORK SECURE.
          </div>
        ) : (
          threats.map((threat, index) => (
            <ThreatCard
              key={`${threat.token}-${threat.timestamp}-${index}`}
              threat={threat}
              index={index}
              onClick={() => onThreatClick(threat)}
            />
          ))
        )}
      </div>
    </div>
  );
}
