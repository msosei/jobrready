#!/bin/bash

# MyBrand Job Application Platform - Development Setup Script
set -e

echo "🚀 Setting up MyBrand Job Application Platform..."

# Check if required tools are installed
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Aborting." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }

# Copy environment files
echo "📝 Setting up environment files..."
cp config/example.env config/.env
echo "✅ Environment files created. Please update config/.env with your values."

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Install backend dependencies
echo "🐍 Setting up Python backend..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cd ..

# Install worker dependencies
echo "⚙️ Installing worker dependencies..."
cd backend/workers
npm install
cd ../..

# Start Redis with Docker
echo "🔴 Starting Redis..."
docker compose up -d redis

# Wait for Redis to be ready
echo "⏳ Waiting for Redis to be ready..."
sleep 5

echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Update config/.env with your Supabase, Stripe, and OpenAI credentials"
echo "2. Run the database setup: psql -f scripts/setup-db.sql"
echo "3. Start the services:"
echo "   - Frontend: cd frontend && npm run dev"
echo "   - Backend: cd backend && source .venv/bin/activate && uvicorn app.main:app --reload"
echo "   - Workers: cd backend/workers && npm run start:dev"
echo "   - Microservices: uvicorn main:app --port 8101 (in each microservice directory)"
echo ""
echo "🎉 Happy coding!"
