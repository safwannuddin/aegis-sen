import { motion } from 'framer-motion';

export default function Stats({ stats, loading }) {
  const statCards = [
    {
      label: 'Tokens Scanned',
      value: stats.tokens_scanned || 0,
      icon: '🔍',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      label: 'Anomalies Detected',
      value: stats.anomalies_detected || 0,
      icon: '⚠️',
      color: 'from-yellow-500 to-orange-500'
    },
    {
      label: 'High Threats',
      value: stats.high_threats || 0,
      icon: '🚨',
      color: 'from-red-500 to-pink-500'
    },
    {
      label: 'Last Scan',
      value: stats.last_scan ? new Date(stats.last_scan).toLocaleTimeString() : 'Never',
      icon: '⏱️',
      color: 'from-green-500 to-emerald-500'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="glass-card p-6 hover:scale-105 transition-transform duration-300"
          >
            <div className="flex items-center justify-between mb-4">
              <span className="text-4xl">{stat.icon}</span>
              <div className={`w-12 h-12 rounded-full bg-gradient-to-br ${stat.color} opacity-20`} />
            </div>
            <div className="text-3xl font-bold mb-2">
              {loading ? (
                <div className="h-8 w-20 bg-gray-700 animate-pulse rounded" />
              ) : (
                stat.value
              )}
            </div>
            <div className="text-sm text-gray-400">{stat.label}</div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
