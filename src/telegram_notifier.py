"""
AEGIS Telegram Notifier
Sends threat alerts to Telegram channel.
"""
import requests
from typing import Dict
from src.config import PREDATOR_SCORE_ALERT_THRESHOLD


class TelegramNotifier:
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_alert(self, analysis: Dict) -> bool:
        """Send threat alert to Telegram channel."""
        if analysis['predator_score'] < PREDATOR_SCORE_ALERT_THRESHOLD:
            return False
        
        # Format alert message
        message = self._format_alert(analysis)
        
        # Send to Telegram
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            print(f"[TELEGRAM] Alert sent for {analysis['token']}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Telegram send failed: {e}")
            return False
    
    def _format_alert(self, analysis: Dict) -> str:
        """Format analysis into Telegram message."""
        message = f"""🚨 *AEGIS THREAT ALERT* 🚨

*Token:* {analysis['token']}
*Predator Score:* {analysis['predator_score']}/100

*Forensics Report:*
"""
        for i, finding in enumerate(analysis['forensics_report'], 1):
            message += f"{i}. {finding}\n\n"
        
        message += f"*Metrics:*\n"
        message += f"• Liquidity: ${analysis['metrics']['liquidity']:,.0f}\n"
        message += f"• 24h Volume: ${analysis['metrics']['volume_24h']:,.0f}\n"
        message += f"• Vol/Liq Ratio: {analysis['metrics']['vol_liq_ratio']:.1f}x\n"
        
        message += f"\n⚠️ *PROCEED WITH EXTREME CAUTION* ⚠️"
        
        return message
    
    def test_connection(self) -> bool:
        """Test Telegram bot connection."""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get('ok'):
                print(f"[OK] Telegram bot connected: @{data['result']['username']}")
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Telegram connection failed: {e}")
            return False
