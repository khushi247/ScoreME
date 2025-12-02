# 📁 Mock Interview Evaluator - Project Structure

## Complete File Organization

```
mock-interview-evaluator/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup configuration
├── Dockerfile                      # Docker container configuration
├── docker-compose.yml              # Docker Compose orchestration
├── Makefile                        # Build and run commands
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
├── PROJECT_STRUCTURE.md            # This file
│
├── run.sh                          # Unix/Linux/Mac run script
├── run.bat                         # Windows run script
│
├── config/                         # Configuration package
│   ├── __init__.py                 # Package initialization
│   └── settings.py                 # Application settings and constants
│       ├── API configuration (Groq)
│       ├── Interview types and levels
│       ├── Evaluation criteria
│       ├── Prompt templates
│       └── UI configuration
│
├── services/                       # Business logic services
│   ├── __init__.py                 # Package initialization
│   ├── groq_service.py             # Groq API client wrapper
│   │   ├── generate_completion()
│   │   ├── generate_json_completion()
│   │   └── generate_questions()
│   ├── evaluation_service.py       # Answer evaluation logic
│   │   ├── evaluate_answer()
│   │   ├── evaluate_video()
│   │   ├── evaluate_audio()
│   │   └── calculate_overall_score()
│   ├── interview_service.py        # Main interview orchestration
│   │   ├── generate_interview_questions()
│   │   ├── evaluate_text_response()
│   │   ├── evaluate_audio_response()
│   │   └── evaluate_video_response()
│   └── media_processor.py          # Audio/video processing
│       ├── transcribe_audio()
│       ├── analyze_video()
│       ├── validate_file_size()
│       └── validate_file_format()
│
├── ui/                             # User interface components
│   ├── __init__.py                 # Package initialization
│   ├── state.py                    # Session state management
│   │   ├── initialize_session_state()
│   │   ├── reset_interview()
│   │   ├── start_interview()
│   │   ├── next_question()
│   │   ├── previous_question()
│   │   └── add_evaluation()
│   └── components.py               # UI rendering components
│       ├── render_sidebar()
│       ├── render_interview_section()
│       ├── render_start_screen()
│       ├── render_question_screen()
│       ├── render_text_input()
│       ├── render_audio_input()
│       ├── render_video_input()
│       ├── render_evaluation_result()
│       └── render_results_screen()
│
├── utils/                          # Utility functions
│   ├── __init__.py                 # Package initialization
│   └── helpers.py                  # Helper functions
│       ├── setup_logging()
│       ├── calculate_weighted_score()
│       ├── validate_score()
│       ├── format_timestamp()
│       ├── truncate_text()
│       └── get_score_color()
│
└── tests/                          # Unit tests
    ├── __init__.py                 # Package initialization
    └── test_services.py            # Service layer tests
        ├── TestEvaluationService
        ├── TestInterviewService
        ├── TestHelperFunctions
        └── TestScoreValidation
```

## File Descriptions

### Root Level Files

| File | Purpose |
|------|---------|
| `app.py` | Main application entry point, initializes Streamlit and routes to UI |
| `requirements.txt` | Lists all Python package dependencies |
| `setup.py` | Python package installation configuration |
| `Dockerfile` | Defines Docker container image |
| `docker-compose.yml` | Multi-container Docker applications |
| `Makefile` | Build automation commands |
| `.env.example` | Template for environment variables |
| `.gitignore` | Files/folders to exclude from Git |
| `README.md` | Complete project documentation |
| `run.sh` / `run.bat` | Platform-specific run scripts |

### config/ Package

**settings.py** - Central configuration file containing:
- Groq API configuration (model, endpoints)
- Interview types and difficulty levels
- Evaluation criteria and weights
- File size and format constraints
- All AI prompt templates
- UI configuration constants

### services/ Package

**groq_service.py** - Groq API Integration
- Manages API client initialization
- Handles text and JSON completions
- Generates interview questions
- Error handling and retry logic

**evaluation_service.py** - Core Evaluation Logic
- Evaluates text answers for content quality
- Analyzes video for body language
- Assesses audio for vocal delivery
- Calculates weighted scores
- Provides fallback evaluations

**interview_service.py** - Interview Orchestration
- Coordinates all interview operations
- Generates questions for selected type/level
- Routes responses to appropriate evaluators
- Combines multi-modal evaluations
- Manages fallback scenarios

**media_processor.py** - Media File Processing
- Transcribes audio using speech recognition
- Extracts frames from video
- Analyzes body language (basic)
- Validates file sizes and formats
- Temporary file management

### ui/ Package

**state.py** - Session State Management
- Initializes all Streamlit session variables
- Manages interview progress and state
- Handles question navigation
- Stores responses and evaluations
- Provides state helper functions

**components.py** - UI Rendering
- Renders sidebar with configuration
- Displays interview start screen
- Shows questions and input interfaces
- Renders evaluation results
- Displays final results summary
- Handles all user interactions

### utils/ Package

**helpers.py** - Utility Functions
- Logging setup
- Score calculations and validations
- Text formatting and truncation
- File operations
- Time and date formatting
- Common helper functions

### tests/ Package

**test_services.py** - Unit Tests
- Tests for evaluation logic
- Tests for interview service
- Tests for utility functions
- Mock object testing
- Score validation tests

## Data Flow

```
User Input → UI Components → Interview Service → Groq/Media Services → Evaluation Service → Results Display
     ↓              ↓                ↓                    ↓                     ↓              ↓
State Manager   Session State   API Calls          Processing           Scoring        UI Update
```

## Key Design Patterns

1. **Separation of Concerns**: Each package handles specific responsibility
2. **Service Layer Pattern**: Business logic isolated in services
3. **Dependency Injection**: Services injected into dependent classes
4. **State Management**: Centralized session state handling
5. **Error Handling**: Try-catch blocks with fallback mechanisms
6. **Configuration Management**: All settings in one place

## Environment Variables

Required in `.env` file:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

## Running the Application

### Development
```bash
# Unix/Linux/Mac
./run.sh

# Windows
run.bat

# Direct
streamlit run app.py
```

### Production (Docker)
```bash
make docker-build
make docker-run
```

### Testing
```bash
make test
# or
python -m pytest tests/ -v
```

## Installation Order

1. Clone/download project
2. Create virtual environment
3. Install dependencies from `requirements.txt`
4. Copy `.env.example` to `.env`
5. Add GROQ_API_KEY to `.env`
6. Run application

## Adding New Features

### To add a new interview type:
1. Update `INTERVIEW_TYPES` in `config/settings.py`
2. Add fallback questions in `interview_service.py`

### To add new evaluation criteria:
1. Update `EVALUATION_CRITERIA` in `config/settings.py`
2. Modify prompts in `config/settings.py`
3. Update evaluation display in `ui/components.py`

### To add new media format:
1. Add format to `SUPPORTED_*_FORMATS` in `config/settings.py`
2. Update validation in `media_processor.py`

## Production Considerations

- Set appropriate file size limits
- Configure proper logging levels
- Use environment-specific `.env` files
- Implement rate limiting for API calls
- Add caching for repeated queries
- Monitor API usage and costs
- Implement user authentication if needed
- Add database for storing results
- Set up CI/CD pipeline

## License & Credits

See README.md for full details.