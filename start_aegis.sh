#!/bin/bash

echo "🛡️  Starting AEGIS Sentinel..."
echo "================================"

# Start backend
echo "Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✓ AEGIS Sentinel is running!"
echo "================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Dashboard: http://localhost:8000/dashboard"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
