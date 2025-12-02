@echo off
REM Mock Interview Evaluator - Run Script for Windows

echo 🎯 Starting Mock Interview Evaluator...

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo 📝 Creating .env from .env.example...
    copy .env.example .env
    echo ❗ Please edit .env file and add your GROQ_API_KEY
    pause
    exit /b 1
)

REM Install/update dependencies
echo 📚 Installing dependencies...
pip install -q -r requirements.txt

REM Run the application
echo 🚀 Launching application...
streamlit run app.py

REM Deactivate virtual environment on exit
deactivate