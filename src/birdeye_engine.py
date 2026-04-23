"""
AEGIS Birdeye Polling Engine
Fetches trending tokens, applies rule-based heuristics, computes Risk Score.
"""
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.config import (
    BIRDEYE_API_KEY,
    BIRDEYE_BASE_URL,
    BIRDEYE_CHAIN,
    MAX_TOKENS_PER_POLL,
    REQUEST_TIMEOUT,
    LIQUIDITY_DROP_THRESHOLD,
    HOLDER_CONCENTRATION_THRESHOLD,
    TRADE_VELOCITY_MULTIPLIER,
    PRICE_DROP_THRESHOLD,
    WEIGHT_LIQUIDITY,
    WEIGHT_HOLDER_CONCENTRATION,
    WEIGHT_TRADE_VELOCITY,
    WEIGHT_PRICE_VOLATILITY,
    CACHE_FILE,
    CACHE_RETENTION_HOURS
)


class BirdeyeEngine:
    def __init__(self):
        self.headers = {
            "X-API-KEY": BIRDEYE_API_KEY,
            "x-chain": BIRDEYE_CHAIN
        }
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load historical token data from cache file."""
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_cache(self):
        """Persist cache to disk."""
        with open(CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _clean_old_cache(self):
        """Remove cache entries older than CACHE_RETENTION_HOURS."""
        cutoff = datetime.now() - timedelta(hours=CACHE_RETENTION_HOURS)
        cutoff_ts = cutoff.timestamp()
        
        for token_addr in list(self.cache.keys()):
            if self.cache[token_addr].get('last_updated', 0) < cutoff_ts:
                del self.cache[token_addr]
    
    def fetch_new_listings(self) -> Optional[List[Dict]]:
        """Fetch the most recent token listings on Solana."""
        url = f"{BIRDEYE_BASE_URL}/defi/v2/tokens/new_listing"
        params = {
            "limit": 10
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('items', [])
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Birdeye API fetch (new_listing) failed: {e}")
            return None

    def calculate_risk_score(self, token: Dict) -> Dict:
        """Apply heuristic rules to new listings and compute Risk Score (0-100)."""
        address = token.get('address')
        risk_score = 0
        flags = []
        
        liquidity = token.get('liquidity', 0)
        
        # Rule 1: Nano Liquidity (Extremely high risk for new pools)
        if liquidity < 5000:
            risk_score += 40
            flags.append(f"Nano liquidity: ${liquidity:,.0f}")
        elif liquidity < 20000:
            risk_score += 20
            flags.append(f"Low initial liquidity: ${liquidity:,.0f}")
            
        # Rule 2: Generic metadata (often used by automated rug bots)
        name = token.get('name', '').lower()
        if any(word in name for word in ['inu', 'doge', 'pepe', 'moon', 'safe']):
            risk_score += 10
            flags.append("Generic 'meme' metadata detected")

        # Rule 3: Fast listing detection
        # New listings are inherently risky until verified
        risk_score += 20
        flags.append("Unverified new listing")
        
        return {
            'address': address,
            'symbol': token.get('symbol'),
            'name': token.get('name'),
            'risk_score': min(risk_score, 100),
            'flags': flags,
            'metrics': {
                'liquidity': liquidity,
                'volume_24h': 0, # New listings won't have 24h vol yet
                'vol_liq_ratio': 0
            }
        }
    
    def scan_tokens(self) -> List[Dict]:
        """Main polling loop: focus on new listings for real-time radar."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Initializing Intelligence Radar...")
        
        # Fetch new listings
        tokens = self.fetch_new_listings()
        if not tokens:
            print("[WARN] No new listings fetched. Skipping scan.")
            return []
        
        print(f"[INFO] Scanning {len(tokens)} recent listings")
        
        # Score each token
        results = []
        for token in tokens:
            risk_result = self.calculate_risk_score(token)
            results.append(risk_result)
            
            if risk_result['risk_score'] >= 50:
                print(f"[RADAR_ALERT] {risk_result['symbol']} | Risk: {risk_result['risk_score']} | {risk_result['flags']}")
        
        return results


def test_engine():
    """Standalone test function - run this to verify engine works."""
    print("=== AEGIS BIRDEYE ENGINE TEST ===\n")
    engine = BirdeyeEngine()
    
    # Run one scan cycle
    high_risk_tokens = engine.scan_tokens()
    
    print(f"\n=== SCAN COMPLETE ===")
    print(f"High-risk tokens detected: {len(high_risk_tokens)}")
    
    if high_risk_tokens:
        print("\nTop Threats:")
        for token in sorted(high_risk_tokens, key=lambda x: x['risk_score'], reverse=True)[:5]:
            print(f"  - {token['symbol']}: Risk {token['risk_score']}")


if __name__ == "__main__":
    test_engine()
