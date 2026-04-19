"""
Test script for Birdeye Engine
Run this to verify the polling and scoring logic works.
"""
import sys
sys.path.insert(0, '.')

from src.birdeye_engine import BirdeyeEngine

def test_single_scan():
    """Test a single scan cycle."""
    print("=== TESTING BIRDEYE ENGINE ===\n")
    
    engine = BirdeyeEngine()
    high_risk = engine.scan_tokens()
    
    print(f"\n=== RESULTS ===")
    print(f"Tokens flagged: {len(high_risk)}")
    
    if high_risk:
        print("\nDetailed Results:")
        for token in high_risk:
            print(f"\nToken: {token['symbol']} ({token['address'][:8]}...)")
            print(f"Risk Score: {token['risk_score']}/100")
            print(f"Flags: {', '.join(token['flags']) if token['flags'] else 'None'}")
            print(f"Metrics: {token['metrics']}")
    else:
        print("No high-risk tokens detected in this scan.")
    
    return high_risk

if __name__ == "__main__":
    test_single_scan()
