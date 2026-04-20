"""
Test AI Consensus Engine
"""
import sys
sys.path.insert(0, '.')

from src.ai_consensus import AIConsensus

def test_with_real_data():
    """Test AI consensus with real Birdeye data."""
    from src.birdeye_engine import BirdeyeEngine
    
    print("=== FULL PIPELINE TEST ===\n")
    
    # Step 1: Scan tokens
    engine = BirdeyeEngine()
    high_risk = engine.scan_tokens()
    
    if not high_risk:
        print("No high-risk tokens detected. Exiting.")
        return
    
    # Step 2: AI analysis on top threat
    print(f"\n=== AI CONSENSUS ANALYSIS ===")
    ai = AIConsensus()
    
    # Analyze top 3 threats
    for token in high_risk[:3]:
        result = ai.analyze_token(token)
        
        print(f"\n{'='*60}")
        print(f"TOKEN: {result['token']}")
        print(f"PREDATOR SCORE: {result['predator_score']}/100")
        print(f"\nFORENSICS REPORT:")
        for i, finding in enumerate(result['forensics_report'], 1):
            print(f"  {i}. {finding}")
        print('='*60)

if __name__ == "__main__":
    test_with_real_data()
