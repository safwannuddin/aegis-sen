"""
Full Pipeline Test - Birdeye → AI → Output
"""
import sys
sys.path.insert(0, '.')

from src.birdeye_engine import BirdeyeEngine
from src.ai_consensus import AIConsensus

def test_full_pipeline():
    """Test complete threat detection pipeline."""
    print("="*70)
    print("AEGIS SENTINEL - FULL PIPELINE TEST")
    print("="*70)
    
    # Step 1: Birdeye Scan
    print("\n[STEP 1] Scanning Birdeye for trending tokens...")
    engine = BirdeyeEngine()
    high_risk = engine.scan_tokens()
    
    print(f"\n[RESULT] Found {len(high_risk)} high-risk tokens")
    
    if not high_risk:
        print("\n[INFO] No threats detected. Pipeline test complete.")
        return
    
    # Step 2: AI Consensus
    print("\n[STEP 2] Running AI consensus analysis...")
    ai = AIConsensus()
    
    critical_threats = []
    
    for token in high_risk[:3]:  # Analyze top 3
        analysis = ai.analyze_token(token)
        
        if analysis['predator_score'] >= 70:
            critical_threats.append(analysis)
    
    # Step 3: Report
    print("\n" + "="*70)
    print("FINAL THREAT REPORT")
    print("="*70)
    
    if critical_threats:
        for threat in critical_threats:
            print(f"\n🚨 CRITICAL THREAT DETECTED")
            print(f"Token: {threat['token']}")
            print(f"Predator Score: {threat['predator_score']}/100")
            print(f"\nForensics:")
            for i, finding in enumerate(threat['forensics_report'], 1):
                print(f"  {i}. {finding[:100]}...")
            print("-"*70)
    else:
        print("\nNo critical threats (Predator Score >= 70) detected.")
    
    print(f"\n[COMPLETE] Pipeline test finished. Analyzed {len(high_risk)} tokens.")
    print("="*70)

if __name__ == "__main__":
    test_full_pipeline()
