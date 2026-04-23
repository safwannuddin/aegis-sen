import { motion } from 'framer-motion';
import ThreatCard from './ThreatCard';

export default function ThreatFeed({ threats, loading, onThreatClick }) {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold mb-2">🚨 Live Threat Feed</h2>
          <p className="text-gray-400">Real-time detection of suspicious activity</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
          <span className="w-2 h-2 bg-primary rounded-full animate-pulse" />
          <span className="text-sm text-primary">Auto-refresh</span>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="glass-card p-6 h-64 animate-pulse">
              <div className="h-6 bg-gray-700 rounded w-1/3 mb-4" />
              <div className="h-4 bg-gray-700 rounded w-2/3 mb-2" />
              <div className="h-4 bg-gray-700 rounded w-1/2" />
            </div>
          ))}
        </div>
      ) : threats.length === 0 ? (
        <div className="glass-card p-12 text-center">
          <div className="text-6xl mb-4">🛡️</div>
          <h3 className="text-xl font-semibold mb-2">No Threats Detected</h3>
          <p className="text-gray-400">System is monitoring... All clear for now.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {threats.map((threat, index) => (
            <ThreatCard
              key={`${threat.token}-${threat.timestamp}-${index}`}
              threat={threat}
              index={index}
              onClick={() => onThreatClick(threat)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
