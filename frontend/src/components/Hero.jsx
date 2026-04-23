import React from 'react';
import { motion } from 'framer-motion';

export default function Hero() {
  return (
    <section className="relative mb-24">
      <div className="flex flex-col items-center text-center">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-bold tracking-widest uppercase mb-8"
        >
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
          </span>
          System Status: Operational
        </motion.div>

        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-6xl md:text-8xl font-black tracking-tighter mb-8 leading-[0.9]"
        >
          AEGIS <span className="gradient-text">SENTINEL</span>
        </motion.h1>

        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="max-w-2xl text-lg md:text-xl text-white/50 leading-relaxed mb-12"
        >
          Autonomous multi-agent AI sentinel for detecting Solana rug pulls. 
          Real-time heuristic analysis powered by Gemini AI.
        </motion.p>

        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex flex-wrap justify-center gap-4"
        >
          <button className="px-8 py-4 bg-white text-black font-bold rounded-2xl hover:bg-white/90 transition-all active:scale-95 glow-primary">
            Initialize Scan
          </button>
          <button className="px-8 py-4 glass text-white font-bold rounded-2xl hover:bg-white/10 transition-all active:scale-95 border-white/5">
            View Analytics
          </button>
        </motion.div>
      </div>

      {/* Decorative Scanning Box */}
      <div className="absolute -z-10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[150%] opacity-20 pointer-events-none">
        <div className="absolute inset-0 border border-primary/10 rounded-[100px]" />
        <div className="scan-line" />
      </div>
    </section>
  );
}
