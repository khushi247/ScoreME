# 🚀 Quick Start Guide - Mock Interview Evaluator

Get up and running in 5 minutes!

## ⚡ Prerequisites

- Python 3.8+ installed
- Groq API key ([Get free key here](https://console.groq.com/keys))

## 📦 Installation (3 steps)

### Step 1: Download & Setup

```bash
# Navigate to project directory
cd mock-interview-evaluator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your API key
# GROQ_API_KEY=your_actual_key_here
```

Or set environment variable directly:
```bash
# Windows (Command Prompt)
set GROQ_API_KEY=your_key_here

# Windows (PowerShell)
$env:GROQ_API_KEY="your_key_here"

# Mac/Linux
export GROQ_API_KEY=your_key_here
```

## 🎬 Run the App

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

## 🎯 Quick Usage

1. **Select Interview Type** (Sidebar)
   - Choose from Technical, Behavioral, Leadership, etc.

2. **Set Difficulty** (Sidebar)
   - Entry Level, Mid Level, Senior Level, or Executive

3. **Choose Response Mode** (Sidebar)
   - Text: Type your answers
   - Audio: Upload audio recordings
   - Video: Upload video recordings

4. **Generate Questions**
   - Click "Generate Questions & Start Interview"

5. **Answer Questions**
   - Provide your response in chosen format
   - Submit for instant AI evaluation

6. **Review Feedback**
   - Get scores for content, communication, confidence
   - Read detailed feedback and tips
   - Continue to next question

7. **Complete Interview**
   - Review overall performance
   - See average scores and insights
   - Start new interview to practice more

## 🎥 Response Modes Explained

### 📝 Text Mode
- **Best for**: Quick practice, focusing on content
- **How**: Type answer in text box → Submit
- **Evaluation**: Content quality, structure, clarity

### 🎤 Audio Mode
- **Best for**: Practicing vocal delivery
- **How**: Upload MP3/WAV file → Submit
- **Evaluation**: Content + vocal tone, pace, filler words
- **Tip**: Use phone voice recorder or any audio recording app

### 🎬 Video Mode
- **Best for**: Full interview simulation
- **How**: Upload MP4/MOV file → Submit
- **Evaluation**: Content + body language + vocal delivery
- **Tip**: Record with webcam, good lighting, plain background

## 🔧 Troubleshooting

### "GROQ_API_KEY not set"
```bash
# Make sure .env file exists and contains:
GROQ_API_KEY=your_key_here

# Or set environment variable before running
export GROQ_API_KEY=your_key_here  # Mac/Linux
set GROQ_API_KEY=your_key_here     # Windows
```

### PyAudio Installation Error (Windows)
```bash
# Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install:
pip install PyAudio‑0.2.14‑cp39‑cp39‑win_amd64.whl
```

### Import Errors
```bash
# Make sure you're in virtual environment
# Reinstall dependencies:
pip install -r requirements.txt --force-reinstall
```

### Audio/Video Processing Fails
- Check file format (MP3, WAV, M4A for audio; MP4, MOV for video)
- Ensure file size is under limit (25MB audio, 100MB video)
- Verify clear audio quality

## 🐳 Docker Quick Start

### One-Command Setup
```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

### Manual Docker
```bash
# Build image
docker build -t mock-interview-app .

# Run container
docker run -p 8501:8501 -e GROQ_API_KEY=your_key mock-interview-app
```

## 📱 Platform-Specific Run Scripts

### Windows
```bash
# Double-click or run:
run.bat
```

### Mac/Linux
```bash
# Make executable:
chmod +x run.sh

# Run:
./run.sh
```

## 💡 Pro Tips

1. **Practice Regularly**: Do 2-3 questions daily for best results
2. **Try All Modes**: Each mode focuses on different skills
3. **Read Feedback Carefully**: Actionable tips help improve faster
4. **Record in Quiet Place**: For audio/video modes
5. **Maintain Eye Contact**: Look at camera in video mode
6. **Structure Answers**: Use STAR method (Situation, Task, Action, Result)
7. **Review Previous Sessions**: Learn from past evaluations

## 🎯 Sample Workflow

**Day 1-2**: Text mode, focus on content
- Practice articulating clear, structured answers
- Build confidence with question types

**Day 3-5**: Audio mode, focus on delivery
- Work on vocal tone and pace
- Reduce filler words

**Day 6+**: Video mode, full simulation
- Combine content, delivery, body language
- Simulate real interview conditions

## 📊 Understanding Scores

| Score Range | Performance | What It Means |
|-------------|-------------|---------------|
| 85-100 | 🌟 Excellent | Interview-ready! Minor refinements only |
| 70-84 | ✅ Good | Strong performance, few improvements needed |
| 50-69 | ⚠️ Fair | Decent start, focus on key feedback areas |
| 0-49 | 📚 Needs Practice | Keep practicing, review fundamentals |

## 🆘 Getting Help

1. **Check README.md** for detailed documentation
2. **Review PROJECT_STRUCTURE.md** for technical details
3. **Run tests**: `python -m pytest tests/`
4. **Check logs** in terminal for error details
5. **Verify API Key** at https://console.groq.com/keys

## ⚙️ Configuration Tips

### Customize in `config/settings.py`:

```python
# Change number of default questions
DEFAULT_NUM_QUESTIONS = 5  # Change to 3 or 10

# Adjust file size limits
MAX_VIDEO_SIZE_MB = 100  # Change to 50 or 200
MAX_AUDIO_SIZE_MB = 25   # Change to 10 or 50

# Modify evaluation weights
EVALUATION_CRITERIA = {
    "content_quality": {"weight": 0.35},  # Adjust weights
    "communication": {"weight": 0.25},
    # ...
}
```

## 🔄 Common Commands

```bash
# Start app
streamlit run app.py

# Run tests
python -m pytest tests/

# Clean temporary files
make clean

# Check code style
make lint

# Format code
make format

# Docker build
make docker-build

# Docker run
make docker-run
```

## 📚 Next Steps

After getting comfortable:
1. ✅ Try different interview types
2. ✅ Increase difficulty levels
3. ✅ Practice with video mode
4. ✅ Review detailed feedback
5. ✅ Track improvement over time

## 🎓 Learning Resources

- **Groq Documentation**: https://console.groq.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **Interview Prep**: Practice STAR method, common questions
- **Body Language**: Research professional video presence
- **Vocal Delivery**: Learn about pace, tone, pausing

## 🚀 You're Ready!

Everything is set up. Now run:
```bash
streamlit run app.py
```

**Happy interviewing! 🎯**

---

**Having issues?** Check README.md or raise an issue on the project repository.