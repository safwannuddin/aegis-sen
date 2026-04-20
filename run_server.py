"""
AEGIS Sentinel - Server Launcher
Quick start script for the FastAPI server.
"""
import uvicorn

if __name__ == "__main__":
    print("="*70)
    print("🛡️  AEGIS SENTINEL - AUTONOMOUS THREAT DETECTION ENGINE")
    print("="*70)
    print("\nStarting server...")
    print("Dashboard: http://localhost:8000/dashboard")
    print("API Docs: http://localhost:8000/docs")
    print("Health: http://localhost:8000/health")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
