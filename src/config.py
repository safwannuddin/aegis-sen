"""
AEGIS Configuration - Heuristic Thresholds & API Settings
All hardcoded values for threat detection scoring.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
BIRDEYE_API_KEY = os.getenv('BIRDEYE_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Birdeye API Configuration
BIRDEYE_BASE_URL = "https://public-api.birdeye.so"
BIRDEYE_CHAIN = "solana"
POLL_INTERVAL_SECONDS = 30  # 30 seconds for live radar

# API Rate Limiting
MAX_TOKENS_PER_POLL = 10  # Only analyze top 10 trending tokens
REQUEST_TIMEOUT = 10  # seconds
RETRY_DELAY = 60  # Wait 60s on rate limit

# Heuristic Thresholds (Risk Scoring)
LIQUIDITY_DROP_THRESHOLD = 0.40  # 40% drop triggers alert
HOLDER_CONCENTRATION_THRESHOLD = 0.70  # Top 3 holders > 70% = centralized
TRADE_VELOCITY_MULTIPLIER = 10.0  # 10x spike above rolling avg
DEV_WALLET_DUMP_THRESHOLD = 0.20  # Dev dumps > 20% holdings
PRICE_DROP_THRESHOLD = 0.30  # 30% price drop in 5 min

# Risk Score Weights (Total = 100)
WEIGHT_LIQUIDITY = 30
WEIGHT_HOLDER_CONCENTRATION = 25
WEIGHT_TRADE_VELOCITY = 20
WEIGHT_DEV_ACTIVITY = 15
WEIGHT_PRICE_VOLATILITY = 10

# AI Consensus Thresholds
RISK_SCORE_AI_THRESHOLD = 70  # Pass to Gemini if Risk > 70
PREDATOR_SCORE_ALERT_THRESHOLD = 90  # Send alert if Predator > 90

# Data Persistence
CACHE_FILE = "data/token_cache.json"
CACHE_RETENTION_HOURS = 24  # Keep 24h of historical data
