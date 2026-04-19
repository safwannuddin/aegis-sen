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
    
    def fetch_trending_tokens(self) -> Optional[List[Dict]]:
        """Fetch top trending tokens from Birdeye."""
        url = f"{BIRDEYE_BASE_URL}/defi/token_trending"
        params = {
            "sort_by": "volume24hUSD",
            "sort_type": "desc",
            "offset": 0,
            "limit": MAX_TOKENS_PER_POLL
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('tokens', [])
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Birdeye API fetch failed: {e}")
            return None
    
    def calculate_risk_score(self, token: Dict) -> Dict:
        """Apply heuristic rules and compute Risk Score (0-100)."""
        address = token.get('address')
        risk_score = 0
        flags = []
        
        # Extract metrics from trending endpoint
        liquidity = token.get('liquidity', 0)
        volume_24h = token.get('volume24hUSD', 0)
        
        # Check cache for historical comparison
        cached = self.cache.get(address, {})
        prev_liquidity = cached.get('liquidity', liquidity)
        prev_volume = cached.get('volume_24h', volume_24h)
        
        # Rule 1: Liquidity Drop
        if prev_liquidity > 0 and liquidity > 0:
            liquidity_drop = (prev_liquidity - liquidity) / prev_liquidity
            if liquidity_drop > LIQUIDITY_DROP_THRESHOLD:
                risk_score += WEIGHT_LIQUIDITY
                flags.append(f"Liquidity dropped {liquidity_drop*100:.1f}%")
        
        # Rule 2: Low Liquidity (< $10k is suspicious for trending tokens)
        if liquidity < 10000:
            risk_score += WEIGHT_PRICE_VOLATILITY
            flags.append(f"Low liquidity: ${liquidity:,.0f}")
        
        # Rule 3: Trade Velocity Spike
        if prev_volume > 0 and volume_24h > 0:
            velocity_ratio = volume_24h / prev_volume
            if velocity_ratio > TRADE_VELOCITY_MULTIPLIER:
                risk_score += WEIGHT_TRADE_VELOCITY
                flags.append(f"Trade velocity spike: {velocity_ratio:.1f}x")
        
        # Rule 4: Suspicious Volume/Liquidity Ratio (> 50x suggests wash trading)
        if liquidity > 0:
            vol_liq_ratio = volume_24h / liquidity
            if vol_liq_ratio > 50:
                risk_score += WEIGHT_HOLDER_CONCENTRATION
                flags.append(f"Suspicious vol/liq ratio: {vol_liq_ratio:.1f}x")
        
        # Update cache
        self.cache[address] = {
            'liquidity': liquidity,
            'volume_24h': volume_24h,
            'last_updated': datetime.now().timestamp(),
            'symbol': token.get('symbol', 'UNKNOWN')
        }
        
        return {
            'address': address,
            'symbol': token.get('symbol'),
            'name': token.get('name'),
            'risk_score': min(risk_score, 100),
            'flags': flags,
            'metrics': {
                'liquidity': liquidity,
                'volume_24h': volume_24h,
                'vol_liq_ratio': volume_24h / liquidity if liquidity > 0 else 0
            }
        }
    
    def scan_tokens(self) -> List[Dict]:
        """Main polling loop: fetch tokens, score them, return high-risk ones."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting token scan...")
        
        # Fetch trending tokens
        tokens = self.fetch_trending_tokens()
        if not tokens:
            print("[WARN] No tokens fetched. Skipping scan.")
            return []
        
        print(f"[INFO] Fetched {len(tokens)} trending tokens")
        
        # Score each token
        results = []
        for token in tokens:
            risk_result = self.calculate_risk_score(token)
            results.append(risk_result)
            
            if risk_result['risk_score'] > 0:
                print(f"[ALERT] {risk_result['symbol']} | Risk: {risk_result['risk_score']} | {risk_result['flags']}")
        
        # Clean old cache and save
        self._clean_old_cache()
        self._save_cache()
        
        return [r for r in results if r['risk_score'] > 0]


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
