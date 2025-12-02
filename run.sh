#!/bin/bash

# Mock Interview Evaluator - Run Script

echo "🎯 Starting Mock Interview Evaluator..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "❗ Please edit .env file and add your GROQ_API_KEY"
    exit 1
fi

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo "🚀 Launching application..."
streamlit run app.py

# Deactivate virtual environment on exit
deactivate