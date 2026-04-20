# AEGIS Sentinel

**Autonomous Exploit & Rug Intelligence Sentinel**

A proactive, autonomous threat detection engine for Solana tokens. AEGIS uses rule-based heuristics combined with multi-agent AI consensus to detect rug pulls, wash trading, and bot manipulation in real-time.

## Architecture

- **Birdeye Polling Engine**: Scans trending tokens every 5 minutes using Birdeye Data API
- **Heuristic Risk Scoring**: Detects anomalies (liquidity drops, wash trading, velocity spikes)
- **Multi-Agent AI Consensus**: Gemini-powered fraud analysis with dual-agent validation
- **Real-Time Alerts**: Telegram notifications for high-threat tokens (Predator Score > 90)
- **Live Dashboard**: Web interface showing threat feed and statistics

## Features

- ✅ Real-time Solana token monitoring
- ✅ 4 heuristic detection rules (liquidity, volume, velocity, wash trading)
- ✅ AI-powered threat analysis with confidence scoring
- ✅ Predator Score (0-100) threat rating system
- ✅ Forensics reports with plain-English explanations
- ✅ FastAPI REST endpoints
- ✅ Live HTML dashboard with auto-refresh
- ✅ Optional Telegram bot integration

## Prerequisites

- Python 3.8+
- Birdeye API Key ([Get one here](https://birdeye.so))
- Gemini API Key ([Get one here](https://aistudio.google.com/))
- (Optional) Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd aegis-sentinel
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file:
```env
BIRDEYE_API_KEY="your_birdeye_key_here"
GEMINI_API_KEY="your_gemini_key_here"
TELEGRAM_BOT_TOKEN=""  # Optional
TELEGRAM_CHAT_ID=""    # Optional
```

## Usage

### Run the Server

```bash
python run_server.py
```

Access:
- Dashboard: http://localhost:8000/dashboard
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Test Individual Components

Test Birdeye engine:
```bash
python tests/test_birdeye_engine.py
```

Test AI consensus:
```bash
python tests/test_ai_consensus.py
```

Test full pipeline:
```bash
python tests/test_full_pipeline.py
```

## API Endpoints

- `GET /` - Service info
- `GET /health` - Health check with stats
- `GET /threats` - Recent threat detections (JSON)
- `GET /dashboard` - Live HTML dashboard

## How It Works

1. **Polling**: Every 5 minutes, fetch top 10 trending tokens from Birdeye
2. **Heuristic Scoring**: Apply 4 detection rules to compute Risk Score (0-100)
3. **AI Analysis**: Tokens with Risk > 70 are analyzed by dual-agent Gemini pipeline
4. **Predator Score**: Final threat rating (0-100) based on AI consensus
5. **Alerting**: Scores > 90 trigger Telegram alerts (if configured)

## Detection Rules

1. **Liquidity Drop**: > 40% drop in 5 minutes
2. **Low Liquidity**: < $10k for trending tokens
3. **Trade Velocity Spike**: > 10x volume increase
4. **Wash Trading**: Volume/Liquidity ratio > 50x

## Tech Stack

- FastAPI - Web framework
- Birdeye API - Solana token data
- Google Gemini - AI analysis
- APScheduler - Background polling
- Requests - HTTP client

## Project Structure

```
aegis-sentinel/
├── src/
│   ├── birdeye_engine.py    # Polling & heuristic scoring
│   ├── ai_consensus.py       # Multi-agent AI analysis
│   ├── telegram_notifier.py  # Alert system
│   └── config.py             # Configuration & thresholds
├── tests/
│   ├── test_birdeye_engine.py
│   ├── test_ai_consensus.py
│   └── test_full_pipeline.py
├── data/
│   └── token_cache.json      # Historical data cache
├── main.py                   # FastAPI server
├── run_server.py             # Server launcher
└── requirements.txt
```

## License

MIT