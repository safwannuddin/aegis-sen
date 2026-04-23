import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Stats from './components/Stats';
import ThreatFeed from './components/ThreatFeed';
import ThreatModal from './components/ThreatModal';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [stats, setStats] = useState({
    tokens_scanned: 0,
    anomalies_detected: 0,
    high_threats: 0,
    last_scan: null
  });
  const [threats, setThreats] = useState([]);
  const [selectedThreat, setSelectedThreat] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [healthRes, radarRes, threatsRes] = await Promise.all([
        fetch(`${API_URL}/health`),
        fetch(`${API_URL}/radar`),
        fetch(`${API_URL}/threats`)
      ]);
      
      const healthData = await healthRes.json();
      const radarData = await radarRes.json();
      const threatsData = await threatsRes.json();
      
      setStats(healthData.stats || {});
      
      // Combine radar and threats:
      // - Radar is everything being scanned
      // - Threats are analyzed anomalies with AI reports
      const combined = (radarData.radar || []).map(r => {
        const threatMatch = (threatsData.threats || []).find(t => t.analysis?.address === r.address);
        return threatMatch ? threatMatch : r;
      });

      setThreats(combined.reverse());
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-dark flex flex-col font-mono text-sm">
      {/* Header / Top Bar */}
      <header className="border-b border-border-dim p-4 flex justify-between items-center bg-terminal-bg relative">
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-primary rounded-full shadow-[0_0_8px_#00ff41]" />
            <span className="font-black tracking-[0.2em] text-white">AEGIS SENTINEL v1.0.4</span>
          </div>
          <div className="h-4 w-[1px] bg-white/10" />
          <Stats stats={stats} loading={loading} />
        </div>
        
        <div className="flex items-center gap-4 text-[10px] font-bold text-white/40">
          <span>NETWORK: SOLANA MAINNET</span>
          <span className="text-primary animate-pulse">● LIVE_POLLING</span>
        </div>

        {/* Global Scan Line */}
        <div className="scan-progress absolute bottom-0 left-0" />
      </header>

      <main className="flex-1 p-6 overflow-y-auto">
        <div className="max-w-[1400px] mx-auto">
          <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/5">
            <div>
              <h1 className="text-xl font-black text-white tracking-widest uppercase mb-1">Live Intelligence Radar</h1>
              <p className="text-white/30 text-[10px]">Real-time detection of predatory behavior on the Solana blockchain.</p>
            </div>
            <div className="text-right">
              <div className="text-[10px] text-white/20 uppercase font-black tracking-widest">Last Update</div>
              <div className="text-xs text-white/60">{stats.last_scan ? new Date(stats.last_scan).toLocaleTimeString() : 'AWAITING_SYNC'}</div>
            </div>
          </div>

          <ThreatFeed 
            threats={threats} 
            loading={loading}
            onThreatClick={setSelectedThreat}
          />
        </div>
      </main>

      <AnimatePresence>
        {selectedThreat && (
          <ThreatModal 
            threat={selectedThreat}
            onClose={() => setSelectedThreat(null)}
          />
        )}
      </AnimatePresence>

      <footer className="border-t border-border-dim p-3 bg-terminal-bg text-[9px] text-white/20 flex justify-between uppercase font-black tracking-[0.3em]">
        <div>AUTHENTICATED VIA BIRDEYE_API_v2</div>
        <div>CONSENSUS ENGINE: GEMINI_FLASH_1.5</div>
        <div>(C) 2026 AEGIS PROJECT</div>
      </footer>
    </div>
  );
}

export default App;
