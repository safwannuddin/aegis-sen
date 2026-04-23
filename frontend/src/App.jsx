import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Hero from './components/Hero';
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
      const [healthRes, threatsRes] = await Promise.all([
        fetch(`${API_URL}/health`),
        fetch(`${API_URL}/threats`)
      ]);
      
      const healthData = await healthRes.json();
      const threatsData = await threatsRes.json();
      
      setStats(healthData.stats || {});
      setThreats(threatsData.threats || []);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-dark">
      <Hero />
      <Stats stats={stats} loading={loading} />
      <ThreatFeed 
        threats={threats} 
        loading={loading}
        onThreatClick={setSelectedThreat}
      />
      
      {selectedThreat && (
        <ThreatModal 
          threat={selectedThreat}
          onClose={() => setSelectedThreat(null)}
        />
      )}
      
      <footer className="py-8 text-center text-gray-400 border-t border-white/10">
        <p>Powered by Birdeye Data API | Built with Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;
