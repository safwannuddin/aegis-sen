@echo off
echo 🛡️  Starting AEGIS Sentinel...
echo ================================

echo Starting backend server...
start "AEGIS Backend" python main.py

timeout /t 3 /nobreak > nul

echo Starting frontend...
cd frontend
start "AEGIS Frontend" npm run dev

echo.
echo ✓ AEGIS Sentinel is running!
echo ================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo Dashboard: http://localhost:8000/dashboard
echo.
echo Press any key to stop...
pause > nul
