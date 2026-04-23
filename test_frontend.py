"""
Quick test to verify frontend can connect to backend
"""
import requests
import json

print("Testing AEGIS Backend API...")
print("="*50)

try:
    # Test health endpoint
    response = requests.get("http://localhost:8000/health")
    print(f"\n✓ Health Check: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    # Test threats endpoint
    response = requests.get("http://localhost:8000/threats")
    print(f"\n✓ Threats Endpoint: {response.status_code}")
    data = response.json()
    print(f"Total threats: {data['total']}")
    
    print("\n" + "="*50)
    print("✓ Backend is ready for frontend!")
    print("\nTo start frontend:")
    print("  cd frontend")
    print("  npm run dev")
    print("\nThen open: http://localhost:5173")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nMake sure backend is running:")
    print("  python main.py")
