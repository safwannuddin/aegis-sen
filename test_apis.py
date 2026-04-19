import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import discord
import asyncio

load_dotenv()

birdeye_key = os.getenv('BIRDEYE_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')
discord_token = os.getenv('DISCORD_BOT_TOKEN')

print("--- API KEY TESTING START ---")

# 1. Test Birdeye
print("\n1. Testing Birdeye API...")
if not birdeye_key:
    print("❌ BIRDEYE_API_KEY is missing from .env")
else:
    url = "https://public-api.birdeye.so/defi/tokenlist?sort_by=v24hUSD&sort_type=desc&offset=0&limit=1"
    headers = {"X-API-KEY": birdeye_key, "x-chain": "solana"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("[OK] Birdeye API is working!")
    elif response.status_code == 401:
        print("[FAIL] Birdeye API Failed: 401 Unauthorized (Invalid API Key)")
    else:
        print(f"[FAIL] Birdeye API Failed: {response.status_code} - {response.text}")

# 2. Test Gemini
print("\n2. Testing Gemini API...")
if not gemini_key:
    print("[FAIL] GEMINI_API_KEY is missing from .env")
else:
    try:
        # Override OS environment variables directly to fix the SDK bug
        os.environ['GOOGLE_API_KEY'] = gemini_key
        genai.configure(api_key=gemini_key)
        # Using the exact verified model name for their specific API key permissions
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content("Say the exact word 'Success'")
        if "Success" in response.text:
            print("[OK] Gemini API is working!")
        else:
            print("[WARN] Gemini API responded, but not as expected.")
    except Exception as e:
        print(f"[FAIL] Gemini API Failed: {e}")


print("\n--- API KEY TESTING END ---")
