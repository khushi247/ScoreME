# 🎯 AI Mock Interview Evaluator

A production-ready mock interview platform powered by AI that evaluates candidates on their answers, communication skills, body language, and overall performance. Built with Streamlit and Groq's latest LLM models.

## 📋 Features

- **Multiple Interview Types**: Technical (Software Engineering, Data Science), Behavioral, Leadership, Product Management, Sales, Customer Service
- **Difficulty Levels**: Entry, Mid, Senior, and Executive level questions
- **Multi-Modal Input**: Text, Audio, and Video responses
- **Comprehensive Evaluation**:
  - Content quality and accuracy
  - Communication clarity and structure
  - Body language and posture (video)
  - Vocal delivery and confidence (audio/video)
- **Real-time AI Feedback**: Detailed scores, strengths, improvements, and actionable tips
- **Progress Tracking**: Track performance across multiple questions

## 🏗️ Project Structure

```
mock-interview-evaluator/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project documentation
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuration and constants
├── services/
│   ├── __init__.py
│   ├── groq_service.py            # Groq API integration
│   ├── evaluation_service.py      # Evaluation logic
│   ├── interview_service.py       # Main interview orchestration
│   └── media_processor.py         # Audio/video processing
└── ui/
    ├── __init__.py
    ├── state.py                   # Session state management
    └── components.py              # UI components and rendering
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key ([Get one here](https://console.groq.com/keys))

### Setup Steps

1. **Clone or download the project**

```bash
cd mock-interview-evaluator
```

2. **Create a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key
GROQ_API_KEY=your_actual_api_key_here
```

5. **Run the application**

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

### Application Settings

Edit `config/settings.py` to customize:

- Interview types and categories
- Difficulty levels
- Number of questions
- Evaluation criteria and weights
- File size limits for audio/video
- Prompt templates

## 📖 Usage Guide

### Starting an Interview

1. **Configure Settings** (in sidebar):
   - Select interview type
   - Choose difficulty level
   - Set number of questions
   - Select response mode (Text/Audio/Video)

2. **Generate Questions**: Click "Generate Questions & Start Interview"

3. **Answer Questions**:
   - **Text Mode**: Type your answer in the text area
   - **Audio Mode**: Upload an audio recording (MP3, WAV, M4A, OGG)
   - **Video Mode**: Upload a video recording (MP4, AVI, MOV, WEBM)

4. **Get Feedback**: Receive instant AI-powered evaluation with:
   - Overall score (0-100)
   - Individual scores for each criterion
   - Detailed feedback
   - Strengths and improvement areas
   - Actionable tips

5. **Review Results**: After completing all questions, view comprehensive performance summary

### Response Modes

#### Text Mode
- Best for: Quick practice, content focus
- Evaluation: Answer content, communication structure, clarity

#### Audio Mode
- Best for: Vocal delivery practice
- Evaluation: Content + vocal tone, pace, clarity, filler words
- Supported formats: MP3, WAV, M4A, OGG
- Max file size: 25MB

#### Video Mode
- Best for: Full interview simulation
- Evaluation: Content + body language + vocal delivery
- Supported formats: MP4, AVI, MOV, WEBM
- Max file size: 100MB

## 🎯 Evaluation Criteria

The AI evaluator assesses responses on:

1. **Content Quality (35%)**
   - Accuracy and relevance
   - Depth of knowledge
   - Problem-solving approach

2. **Communication (25%)**
   - Clarity and articulation
   - Logical structure
   - Professional language

3. **Body Language (20%)** _(Video only)_
   - Posture and positioning
   - Eye contact
   - Gestures and expressions

4. **Vocal Delivery (20%)** _(Audio/Video)_
   - Tone and confidence
   - Speaking pace
   - Minimal filler words

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **AI/LLM**: Groq API (llama-3.3-70b-versatile model)
- **Speech Recognition**: SpeechRecognition library
- **Video Processing**: OpenCV
- **Language**: Python 3.8+

## 📝 API Models

Currently using **Groq's llama-3.3-70b-versatile** model:
- Fast inference speed
- High-quality responses
- Cost-effective
- Not deprecated (as of latest update)

## 🔒 Security & Privacy

- API keys stored in environment variables
- No data persistence (session-based only)
- Media files processed in temporary directories
- Files automatically cleaned up after processing

## 🐛 Troubleshooting

### Common Issues

**"GROQ_API_KEY not set" error**
- Ensure `.env` file exists in project root
- Verify API key is correctly set in `.env`
- Restart the Streamlit application

**Audio transcription fails**
- Ensure clear audio quality
- Check supported formats (MP3, WAV, M4A, OGG)
- Verify file size is under 25MB

**Video analysis issues**
- Check supported formats (MP4, AVI, MOV, WEBM)
- Ensure adequate lighting in video
- Verify file size is under 100MB

**PyAudio installation issues** (Windows)
- Download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Install with: `pip install PyAudio‑0.2.14‑cp3xx‑cp3xx‑win_amd64.whl`

## 🚀 Deployment

### Streamlit Cloud

1. Push code to GitHub repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repository
4. Add `GROQ_API_KEY` in Secrets management

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t mock-interview-app .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key mock-interview-app
```

## 📈 Future Enhancements

- [ ] PDF report generation
- [ ] Interview history and analytics
- [ ] Custom question bank
- [ ] Multi-language support
- [ ] Advanced video analysis (facial recognition, emotion detection)
- [ ] Real-time recording (audio/video)
- [ ] Interview simulation with timed questions
- [ ] Peer comparison and benchmarking

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check Groq documentation: https://console.groq.com/docs
- Streamlit documentation: https://docs.streamlit.io

## 🙏 Acknowledgments

- Groq for providing fast and efficient LLM APIs
- Streamlit for the amazing web framework
- Open-source community for various libraries used

---

**Built with ❤️ for better interview preparation**