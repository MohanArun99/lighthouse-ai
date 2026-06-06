#!/bin/bash

# Lighthouse AI - Quick Start Script

echo "🌐 Lighthouse AI - Starting Services..."
echo "==========================================\n"

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Error: backend directory not found"
    echo "Please run this script from the lighthouse-ai root directory"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

echo "✅ Node found: $(node --version)"

# Install backend dependencies
echo "\n📦 Installing backend dependencies..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi
pip install -q -r requirements.txt
echo "✅ Backend dependencies installed"

# Install frontend dependencies
echo "\n📦 Installing frontend dependencies..."
cd ../frontend
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found"
    exit 1
fi

if command -v pnpm &> /dev/null; then
    pnpm install
else
    npm install
fi
echo "✅ Frontend dependencies installed"

# Create .env if it doesn't exist
cd ../backend
if [ ! -f ".env" ]; then
    echo "\n📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ .env created (using DEMO_MODE=true)"
fi

echo "\n==========================================\n"
echo "🚀 Ready to launch!"
echo "\nOpen TWO terminal windows:"
echo "\nTerminal 1 (Backend):"
echo "  cd backend && python main.py"
echo "\nTerminal 2 (Frontend):"
echo "  cd frontend && npm run dev"
echo "\nThen open http://localhost:3000 in your browser"
echo "\n==========================================\n"