import React from 'react';

export default function Stats({ stats, loading }) {
  const items = [
    { label: 'Scanned', value: stats.tokens_scanned || 0, color: 'text-white' },
    { label: 'Anomalies', value: stats.anomalies_detected || 0, color: 'text-warning' },
    { label: 'High_Threats', value: stats.high_threats || 0, color: 'text-danger' },
  ];

  return (
    <div className="flex gap-8">
      {items.map((item, i) => (
        <div key={i} className="flex flex-col">
          <span className="text-[8px] font-black uppercase text-white/20 tracking-widest leading-none mb-1">{item.label}</span>
          <div className={`text-sm font-black tracking-tighter ${item.color}`}>
            {loading ? '---' : item.value}
          </div>
        </div>
      ))}
    </div>
  );
}
