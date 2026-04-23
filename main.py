"""
AEGIS Sentinel - Main FastAPI Server
Autonomous threat detection engine with background polling.
"""
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
from dotenv import load_dotenv

from src.birdeye_engine import BirdeyeEngine
from src.ai_consensus import AIConsensus
from src.telegram_notifier import TelegramNotifier
from src.config import POLL_INTERVAL_SECONDS, RISK_SCORE_AI_THRESHOLD

load_dotenv()

app = FastAPI(title="AEGIS Sentinel", version="1.0.0")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
radar_log = []
threat_log = []
stats = {
    'tokens_scanned': 0,
    'anomalies_detected': 0,
    'high_threats': 0,
    'last_scan': None
}

# Initialize components
birdeye = BirdeyeEngine()
ai_consensus = AIConsensus()

# Telegram (optional - only if configured)
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
telegram = None
if telegram_bot_token and telegram_chat_id:
    telegram = TelegramNotifier(telegram_bot_token, telegram_chat_id)
    telegram.test_connection()


def scan_and_analyze():
    """Background task: scan tokens, analyze threats, send alerts."""
    global threat_log, stats
    
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] === AEGIS SCAN CYCLE ===")
    
    # Step 1: Scan tokens with heuristics
    tokens = birdeye.scan_tokens()
    stats['tokens_scanned'] += len(tokens)
    
    # Update radar log (keep last 100)
    for token in tokens:
        radar_log.append({
            'timestamp': datetime.now().isoformat(),
            'token': token['symbol'],
            'address': token['address'],
            'risk_score': token['risk_score'],
            'metrics': token['metrics'],
            'flags': token['flags']
        })
    
    if len(radar_log) > 100:
        radar_log = radar_log[-100:]
        
    high_risk_tokens = [t for t in tokens if t['risk_score'] > 0]
    stats['anomalies_detected'] += len(high_risk_tokens)
    stats['last_scan'] = datetime.now().isoformat()
    
    if not high_risk_tokens:
        print("[INFO] No threats detected in this cycle.")
        return
    
    # Step 2: AI analysis on high-risk tokens
    for token in high_risk_tokens:
        if token['risk_score'] >= RISK_SCORE_AI_THRESHOLD:
            try:
                analysis = ai_consensus.analyze_token(token)
                
                # Log threat
                threat_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'token': analysis['token'],
                    'predator_score': analysis['predator_score'],
                    'analysis': analysis
                })
                
                # Keep only last 50 threats
                if len(threat_log) > 50:
                    threat_log.pop(0)
                
                # Update stats
                if analysis['predator_score'] >= 90:
                    stats['high_threats'] += 1
                
                # Send Telegram alert
                if telegram:
                    telegram.send_alert(analysis)
                
            except Exception as e:
                print(f"[ERROR] Analysis failed for {token['symbol']}: {e}")


# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scan_and_analyze, 'interval', seconds=POLL_INTERVAL_SECONDS)
scheduler.start()


@app.on_event("startup")
async def startup_event():
    """Run initial scan on startup."""
    print("[STARTUP] AEGIS Sentinel initializing...")
    scan_and_analyze()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    scheduler.shutdown()


@app.get("/")
async def root():
    """API root endpoint."""
    return {
        "service": "AEGIS Sentinel",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "last_scan": stats['last_scan'],
        "stats": stats
    }


@app.get("/threats")
async def get_threats():
    """Get recent threat detections."""
    return {
        "total": len(threat_log),
        "threats": threat_log[-20:]  # Last 20 threats
    }


@app.get("/radar")
async def get_radar():
    """Get full radar stream of scanned tokens."""
    return {
        "total": len(radar_log),
        "radar": radar_log[-20:]  # Last 20 tokens for the dashboard
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Advanced HTML dashboard with Chart.js and Cyberpunk styling."""
    
    # Extract data for graphs
    labels = [threat['token'] for threat in threat_log[-5:]]
    scores = [threat['predator_score'] for threat in threat_log[-5:]]
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AEGIS Central Command</title>
        <meta http-equiv="refresh" content="30">
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
            
            body {{
                font-family: 'Share Tech Mono', monospace;
                background-color: #050510;
                color: #00ffcc;
                margin: 0;
                padding: 20px;
                background-image: linear-gradient(rgba(0, 255, 204, 0.05) 1px, transparent 1px),
                                  linear-gradient(90deg, rgba(0, 255, 204, 0.05) 1px, transparent 1px);
                background-size: 20px 20px;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #ff0055;
                padding-bottom: 10px;
                margin-bottom: 30px;
                text-shadow: 0 0 10px #ff0055;
            }}
            h1 {{ color: #ff0055; letter-spacing: 5px; font-size: 2.5rem; }}
            
            .dashboard-grid {{
                display: grid;
                grid-template-columns: 1fr 2fr;
                gap: 20px;
            }}
            
            .panel {{
                background: rgba(10, 15, 30, 0.8);
                border: 1px solid #00ffcc;
                box-shadow: 0 0 15px rgba(0, 255, 204, 0.2);
                border-radius: 8px;
                padding: 20px;
            }}
            
            .stats-container {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }}
            
            .stat-box {{
                text-align: center;
                border-right: 1px solid rgba(0, 255, 204, 0.3);
                flex: 1;
            }}
            .stat-box:last-child {{ border: none; }}
            .stat-value {{ font-size: 2.5rem; color: #ff0055; text-shadow: 0 0 5px #ff0055; }}
            .stat-label {{ font-size: 0.9rem; letter-spacing: 1px; opacity: 0.8; }}
            
            .threat-feed {{
                max-height: 600px;
                overflow-y: auto;
            }}
            
            .threat-card {{
                border-left: 4px solid #ff0055;
                background: rgba(255, 0, 85, 0.05);
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 0 5px 5px 0;
            }}
            
            .threat-header {{
                display: flex;
                justify-content: space-between;
                font-weight: bold;
                font-size: 1.2rem;
                color: #ff0055;
                margin-bottom: 10px;
            }}
            
            .forensics {{
                color: #ddd;
                font-size: 0.9rem;
                line-height: 1.4;
                white-space: pre-wrap;
            }}
            
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🛡️ AEGIS SENTINEL 🛡️</h1>
            <p>AUTONOMOUS EXPLOIT & RUG INTELLIGENCE TERMINAL</p>
        </div>
        
        <div class="stats-container panel">
            <div class="stat-box">
                <div class="stat-value">{stats['tokens_scanned']}</div>
                <div class="stat-label">TOKENS SCANNED</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{stats['anomalies_detected']}</div>
                <div class="stat-label">ANOMALIES CAUGHT</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" style="color:#ffcc00; text-shadow: 0 0 5px #ffcc00;">{stats['high_threats']}</div>
                <div class="stat-label">CRITICAL THREATS</div>
            </div>
        </div>

        <div class="dashboard-grid">
            <div class="panel">
                <h3 style="color:#00ffcc; text-align:center; border-bottom:1px solid #00ffcc; padding-bottom:10px;">THREAT VELOCITY</h3>
                <canvas id="threatChart"></canvas>
            </div>
            
            <div class="panel threat-feed">
                <h3 style="color:#ff0055; border-bottom:1px solid #ff0055; padding-bottom:10px;">🚨 LIVE INTELLIGENCE FEED</h3>
"""
    
    # Add recent threats with actual forensics output
    for threat in reversed(threat_log[-10:]):
        # Extract the forensics text from the AI analysis object
        forensics_text = threat['analysis'].get('forensics_report', 'No detailed report generated.')
        
        html += f"""
                <div class="threat-card">
                    <div class="threat-header">
                        <span>TARGET: {threat['token']}</span>
                        <span>SCORE: {threat['predator_score']}/100</span>
                    </div>
                    <div style="font-size: 0.8rem; color:#888; margin-bottom: 10px;">DETECTED: {threat['timestamp']}</div>
                    <div class="forensics">{forensics_text}</div>
                </div>
"""
    
    if not threat_log:
        html += "<p style='text-align: center; color: #00ffcc; opacity: 0.6;'>Awaiting anomalous activity. Network secure.</p>"
    
    html += f"""
            </div>
        </div>

        <p style="text-align: center; margin-top: 30px; font-size: 0.8rem; opacity: 0.5;">
            Auto-refreshes every 30s | Last Poll: {stats['last_scan'] or 'Booting...'}
        </p>

        <script>
            const ctx = document.getElementById('threatChart').getContext('2d');
            new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: {labels},
                    datasets: [{{
                        label: 'Predator Score',
                        data: {scores},
                        backgroundColor: 'rgba(255, 0, 85, 0.7)',
                        borderColor: 'rgba(255, 0, 85, 1)',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    scales: {{
                        y: {{ beginAtZero: true, max: 100, grid: {{ color: 'rgba(0, 255, 204, 0.1)' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }},
                    plugins: {{ legend: {{ display: false }} }}
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
