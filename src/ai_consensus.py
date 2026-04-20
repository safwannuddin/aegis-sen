"""
AEGIS AI Consensus Engine
Multi-agent Gemini pipeline for threat analysis and Predator Score calculation.
"""
import os
import google.generativeai as genai
from typing import Dict, List
from src.config import GEMINI_API_KEY

# Configure Gemini
os.environ['GOOGLE_API_KEY'] = GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)


class AIConsensus:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    def _fraud_analyst_prompt(self, token_data: Dict) -> str:
        """Generate prompt for Fraud Analyst agent."""
        return f"""You are a DeFi Fraud Analyst. Analyze this Solana token for rug pull indicators.

Token: {token_data['symbol']} ({token_data['name']})
Address: {token_data['address']}

Metrics:
- Liquidity: ${token_data['metrics']['liquidity']:,.2f}
- 24h Volume: ${token_data['metrics']['volume_24h']:,.2f}
- Volume/Liquidity Ratio: {token_data['metrics']['vol_liq_ratio']:.1f}x

Risk Flags: {', '.join(token_data['flags']) if token_data['flags'] else 'None'}

Analyze:
1. Is the liquidity sufficient or suspiciously low?
2. Does the volume/liquidity ratio indicate wash trading?
3. What is the likelihood of a rug pull?

Respond in this exact format:
THREAT_LEVEL: [Low/Medium/High]
CONFIDENCE: [0-100]
REASONING: [2-3 sentences]"""
    
    def _behavioral_psychologist_prompt(self, token_data: Dict) -> str:
        """Generate prompt for Behavioral Psychologist agent."""
        return f"""You are a Behavioral Psychologist analyzing trading patterns for bot activity.

Token: {token_data['symbol']}
24h Volume: ${token_data['metrics']['volume_24h']:,.2f}
Volume/Liquidity Ratio: {token_data['metrics']['vol_liq_ratio']:.1f}x

Risk Flags: {', '.join(token_data['flags']) if token_data['flags'] else 'None'}

Analyze:
1. Does the volume pattern suggest coordinated bot activity?
2. Is this organic trading or artificial manipulation?
3. What behavioral red flags exist?

Respond in this exact format:
THREAT_LEVEL: [Low/Medium/High]
CONFIDENCE: [0-100]
REASONING: [2-3 sentences]"""
    
    def _parse_agent_response(self, response_text: str) -> Dict:
        """Parse agent response into structured data."""
        lines = response_text.strip().split('\n')
        result = {
            'threat_level': 'Unknown',
            'confidence': 0,
            'reasoning': ''
        }
        
        for line in lines:
            if line.startswith('THREAT_LEVEL:'):
                result['threat_level'] = line.split(':', 1)[1].strip()
            elif line.startswith('CONFIDENCE:'):
                try:
                    result['confidence'] = int(line.split(':', 1)[1].strip())
                except ValueError:
                    result['confidence'] = 0
            elif line.startswith('REASONING:'):
                result['reasoning'] = line.split(':', 1)[1].strip()
        
        return result
    
    def analyze_token(self, token_data: Dict) -> Dict:
        """Run multi-agent analysis and compute Predator Score."""
        print(f"\n[AI] Analyzing {token_data['symbol']}...")
        
        # Agent 1: Fraud Analyst
        fraud_prompt = self._fraud_analyst_prompt(token_data)
        fraud_response = self.model.generate_content(fraud_prompt)
        fraud_analysis = self._parse_agent_response(fraud_response.text)
        print(f"[AI] Fraud Analyst: {fraud_analysis['threat_level']} (Confidence: {fraud_analysis['confidence']}%)")
        
        # Agent 2: Behavioral Psychologist
        behavior_prompt = self._behavioral_psychologist_prompt(token_data)
        behavior_response = self.model.generate_content(behavior_prompt)
        behavior_analysis = self._parse_agent_response(behavior_response.text)
        print(f"[AI] Behavioral Psychologist: {behavior_analysis['threat_level']} (Confidence: {behavior_analysis['confidence']}%)")
        
        # Compute Predator Score (0-100)
        threat_scores = {
            'Low': 20,
            'Medium': 50,
            'High': 80
        }
        
        fraud_score = threat_scores.get(fraud_analysis['threat_level'], 0)
        behavior_score = threat_scores.get(behavior_analysis['threat_level'], 0)
        
        # Weighted average with confidence
        fraud_weight = fraud_analysis['confidence'] / 100
        behavior_weight = behavior_analysis['confidence'] / 100
        total_weight = fraud_weight + behavior_weight
        
        if total_weight > 0:
            predator_score = int((fraud_score * fraud_weight + behavior_score * behavior_weight) / total_weight)
        else:
            predator_score = token_data['risk_score']  # Fallback to heuristic score
        
        # Generate forensics report
        forensics = [
            f"Fraud Analysis: {fraud_analysis['reasoning']}",
            f"Behavioral Analysis: {behavior_analysis['reasoning']}",
            f"Risk Heuristics: {', '.join(token_data['flags']) if token_data['flags'] else 'No flags'}"
        ]
        
        return {
            'token': token_data['symbol'],
            'address': token_data['address'],
            'predator_score': predator_score,
            'fraud_analysis': fraud_analysis,
            'behavior_analysis': behavior_analysis,
            'forensics_report': forensics,
            'metrics': token_data['metrics']
        }
    
    def batch_analyze(self, high_risk_tokens: List[Dict]) -> List[Dict]:
        """Analyze multiple tokens and return those above threshold."""
        results = []
        
        for token in high_risk_tokens:
            try:
                analysis = self.analyze_token(token)
                results.append(analysis)
            except Exception as e:
                print(f"[ERROR] AI analysis failed for {token['symbol']}: {e}")
        
        return results


def test_ai_consensus():
    """Standalone test for AI consensus engine."""
    print("=== TESTING AI CONSENSUS ENGINE ===\n")
    
    # Mock high-risk token data
    mock_token = {
        'symbol': 'SCAM',
        'name': 'Scam Token',
        'address': 'ABC123...',
        'risk_score': 55,
        'flags': ['Suspicious vol/liq ratio: 500.0x', 'Low liquidity: $5,000'],
        'metrics': {
            'liquidity': 5000,
            'volume_24h': 2500000,
            'vol_liq_ratio': 500.0
        }
    }
    
    ai = AIConsensus()
    result = ai.analyze_token(mock_token)
    
    print(f"\n=== ANALYSIS COMPLETE ===")
    print(f"Token: {result['token']}")
    print(f"Predator Score: {result['predator_score']}/100")
    print(f"\nForensics Report:")
    for i, finding in enumerate(result['forensics_report'], 1):
        print(f"{i}. {finding}")


if __name__ == "__main__":
    test_ai_consensus()
