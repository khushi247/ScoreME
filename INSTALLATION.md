# 📦 Installation Guide - Mock Interview Evaluator

Comprehensive installation instructions for all platforms and scenarios.

## Table of Contents
- [System Requirements](#system-requirements)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [Docker Installation](#docker-installation)
- [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Internet**: Required for API calls

### Required Software
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- pip (comes with Python)
- Git (optional, for cloning) ([Download](https://git-scm.com/downloads))

### API Requirements
- Groq API Key (free tier available)
- Sign up at: https://console.groq.com/keys

---

## Windows Installation

### Option 1: Automated Installation (Recommended)

1. **Download the project files**
   - Extract to a folder (e.g., `C:\mock-interview-evaluator`)

2. **Run the installation script**
   ```cmd
   # Double-click run.bat or run in Command Prompt:
   run.bat
   ```
   - Script will create virtual environment
   - Install all dependencies
   - Prompt for API key setup

### Option 2: Manual Installation

1. **Open Command Prompt or PowerShell**
   ```cmd
   # Navigate to project directory
   cd C:\path\to\mock-interview-evaluator
   ```

2. **Create Virtual Environment**
   ```cmd
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```cmd
   # Command Prompt:
   venv\Scripts\activate

   # PowerShell:
   venv\Scripts\Activate.ps1
   ```
   
   **Note**: If PowerShell gives execution policy error:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Upgrade pip**
   ```cmd
   python -m pip install --upgrade pip
   ```

5. **Install Dependencies**
   ```cmd
   pip install -r requirements.txt
   ```

6. **Configure Environment Variables**
   ```cmd
   # Copy template
   copy .env.example .env
   
   # Edit .env file with notepad
   notepad .env
   # Add: GROQ_API_KEY=your_key_here
   ```

7. **Run Application**
   ```cmd
   streamlit run app.py
   ```

### Windows-Specific Issues

**PyAudio Installation Error:**

If `pip install -r requirements.txt` fails on PyAudio:

```cmd
# Option 1: Download precompiled wheel
# Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Download appropriate version (e.g., PyAudio‑0.2.14‑cp39‑cp39‑win_amd64.whl)
# Install:
pip install path\to\PyAudio‑0.2.14‑cp39‑cp39‑win_amd64.whl

# Option 2: Skip PyAudio (audio features won't work)
pip install -r requirements.txt --no-deps
pip install streamlit groq opencv-python numpy Pillow python-dotenv
```

**Microsoft Visual C++ Error:**

Install Microsoft C++ Build Tools:
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Select "Desktop development with C++"

---

## macOS Installation

### Option 1: Automated Installation (Recommended)

1. **Open Terminal**

2. **Navigate to project directory**
   ```bash
   cd /path/to/mock-interview-evaluator
   ```

3. **Make script executable and run**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```

### Option 2: Manual Installation

1. **Install Homebrew** (if not installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python 3.8+** (if not installed)
   ```bash
   brew install python@3.9
   ```

3. **Install PortAudio** (required for PyAudio)
   ```bash
   brew install portaudio
   ```

4. **Navigate to project directory**
   ```bash
   cd /path/to/mock-interview-evaluator
   ```

5. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

6. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

7. **Upgrade pip**
   ```bash
   pip install --upgrade pip
   ```

8. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

9. **Configure Environment**
   ```bash
   # Copy template
   cp .env.example .env
   
   # Edit with nano or vim
   nano .env
   # Add: GROQ_API_KEY=your_key_here
   # Save: Ctrl+O, Enter, Ctrl+X
   ```

10. **Run Application**
    ```bash
    streamlit run app.py
    ```

### macOS-Specific Issues

**Command not found: python**
```bash
# Use python3 instead
python3 -m venv venv
```

**SSL Certificate Error:**
```bash
# Install certificates
/Applications/Python\ 3.9/Install\ Certificates.command
```

**Permission Denied:**
```bash
# Make script executable
chmod +x run.sh
```

---

## Linux Installation

### Ubuntu/Debian

1. **Update Package Manager**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```

2. **Install Python and Dependencies**
   ```bash
   sudo apt install python3 python3-pip python3-venv
   sudo apt install portaudio19-dev python3-pyaudio
   sudo apt install ffmpeg libsm6 libxext6  # For video processing
   ```

3. **Navigate to Project Directory**
   ```bash
   cd /path/to/mock-interview-evaluator
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

5. **Activate Virtual Environment**
   ```bash
   source venv/bin/activate
   ```

6. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env
   # Add GROQ_API_KEY=your_key_here
   ```

8. **Run Application**
   ```bash
   streamlit run app.py
   ```

### Fedora/RHEL/CentOS

```bash
# Install dependencies
sudo dnf install python3 python3-pip python3-virtualenv
sudo dnf install portaudio-devel
sudo dnf install ffmpeg

# Follow steps 3-8 from Ubuntu section
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip python-virtualenv
sudo pacman -S portaudio
sudo pacman -S ffmpeg

# Follow steps 3-8 from Ubuntu section
```

---

## Docker Installation

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually included)

### Method 1: Docker Compose (Recommended)

1. **Navigate to project directory**
   ```bash
   cd /path/to/mock-interview-evaluator
   ```

2. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env and add GROQ_API_KEY
   ```

3. **Build and Run**
   ```bash
   docker-compose up -d
   ```

4. **Access Application**
   - Open browser: http://localhost:8501

5. **Stop Application**
   ```bash
   docker-compose down
   ```

### Method 2: Docker Build

1. **Build Image**
   ```bash
   docker build -t mock-interview-app .
   ```

2. **Run Container**
   ```bash
   docker run -d \
     -p 8501:8501 \
     -e GROQ_API_KEY=your_key_here \
     --name mock-interview \
     mock-interview-app
   ```

3. **View Logs**
   ```bash
   docker logs mock-interview
   ```

4. **Stop Container**
   ```bash
   docker stop mock-interview
   docker rm mock-interview
   ```

### Docker on Windows

Use Docker Desktop:
1. Install Docker Desktop for Windows
2. Enable WSL 2 backend
3. Follow Docker Compose method above

---

## Troubleshooting

### Common Issues

#### 1. Python Version Issues

**Problem**: `python: command not found`

**Solution**:
```bash
# Try python3
python3 --version

# Or install Python
# Windows: Download from python.org
# Mac: brew install python@3.9
# Linux: sudo apt install python3
```

#### 2. pip Issues

**Problem**: `pip: command not found`

**Solution**:
```bash
# Try pip3
pip3 --version

# Or reinstall pip
python -m ensurepip --upgrade
```

#### 3. Virtual Environment Issues

**Problem**: Cannot activate virtual environment

**Solution**:
```bash
# Recreate virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

python -m venv venv
```

#### 4. Dependency Installation Fails

**Problem**: Error installing packages

**Solution**:
```bash
# Update pip first
pip install --upgrade pip setuptools wheel

# Install with verbose output
pip install -r requirements.txt -v

# Install packages individually to identify issue
pip install streamlit
pip install groq
# ... etc
```

#### 5. PyAudio Installation Fails

**Solution by Platform**:

**Windows**:
```bash
# Download precompiled wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
pip install PyAudio-0.2.14-cpXX-cpXX-win_amd64.whl
```

**Mac**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux**:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

#### 6. OpenCV Issues

**Problem**: ImportError: libGL.so.1

**Solution** (Linux):
```bash
sudo apt-get install libgl1-mesa-glx
sudo apt-get install libglib2.0-0
```

#### 7. Streamlit Port Already in Use

**Problem**: Port 8501 already in use

**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill process using port 8501
# Linux/Mac:
lsof -ti:8501 | xargs kill -9
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

#### 8. API Key Not Recognized

**Problem**: "GROQ_API_KEY not set" error

**Solution**:
```bash
# Verify .env file exists
ls -la .env  # Linux/Mac
dir .env     # Windows

# Check .env content
cat .env     # Linux/Mac
type .env    # Windows

# Ensure format is correct (no spaces):
# GROQ_API_KEY=your_key_here

# Try setting environment variable directly
export GROQ_API_KEY=your_key  # Linux/Mac
set GROQ_API_KEY=your_key     # Windows CMD
$env:GROQ_API_KEY="your_key"  # Windows PowerShell
```

### Getting More Help

1. **Check logs**: Terminal output shows detailed errors
2. **Run tests**: `python -m pytest tests/ -v`
3. **Verify Python version**: `python --version` (must be 3.8+)
4. **Check dependencies**: `pip list`
5. **Review README.md** for additional documentation

---

## Post-Installation

### Verify Installation

```bash
# Check all dependencies installed
pip list

# Run tests
python -m pytest tests/

# Start application
streamlit run app.py
```

### Optional: Development Tools

```bash
# Install development dependencies
pip install pytest black flake8 mypy

# Run linting
flake8 .

# Format code
black .

# Type checking
mypy .
```

### Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update Streamlit
pip install --upgrade streamlit

# Update Groq
pip install --upgrade groq
```

---

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Remove project directory if desired
```

---

**Installation complete! Ready to start interviewing! 🎯**