#!/bin/bash
set -e

echo "Starting Think Tank development servers..."
echo "Frontend: http://localhost:5173"
echo "Django:   http://localhost:8000"
echo "Press Ctrl+C to stop both servers"
echo ""

# Install dependencies if needed
cd frontend
npm install > /dev/null 2>&1
cd ..

# Start both servers
(cd frontend && npm run dev) &
FRONTEND_PID=$!

python manage.py runserver &
DJANGO_PID=$!

# Cleanup on exit
trap "kill $FRONTEND_PID $DJANGO_PID 2>/dev/null; echo 'Servers stopped'" EXIT

wait
