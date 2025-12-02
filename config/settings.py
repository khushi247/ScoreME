import os
from typing import Dict, Any

# API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Latest stable model from Groq
GROQ_API_BASE = "https://api.groq.com/openai/v1"

# Interview Configuration
INTERVIEW_TYPES = [
    "Technical - Software Engineering",
    "Technical - Data Science",
    "Behavioral",
    "Leadership",
    "Product Management",
    "Sales",
    "Customer Service"
]

DIFFICULTY_LEVELS = ["Entry Level", "Mid Level", "Senior Level", "Executive"]

DEFAULT_NUM_QUESTIONS = 5

# Evaluation Criteria
EVALUATION_CRITERIA = {
    "content_quality": {
        "weight": 0.35,
        "description": "Accuracy, relevance, and depth of answer"
    },
    "communication": {
        "weight": 0.25,
        "description": "Clarity, structure, and articulation"
    },
    "body_language": {
        "weight": 0.20,
        "description": "Posture, eye contact, and gestures"
    },
    "confidence": {
        "weight": 0.20,
        "description": "Voice tone, pace, and assertiveness"
    }
}

# Audio/Video Settings
MAX_VIDEO_SIZE_MB = 100
MAX_AUDIO_SIZE_MB = 25
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".webm"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".ogg"]

# UI Configuration
PAGE_CONFIG: Dict[str, Any] = {
    "page_title": "Mock Interview Evaluator",
    "page_icon": "🎯",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Prompt Templates
QUESTION_GENERATION_PROMPT = """You are an expert interviewer. Generate {num_questions} realistic interview questions for a {interview_type} position at {difficulty_level}.

Requirements:
- Questions should be realistic and commonly asked in actual interviews
- Vary difficulty appropriately for the level
- Include a mix of question types (technical, behavioral, situational as appropriate)
- Format as a numbered list

Generate the questions now:"""

ANSWER_EVALUATION_PROMPT = """You are an expert interview evaluator. Evaluate the following interview response:

Question: {question}
Candidate's Answer: {answer}
Interview Type: {interview_type}
Level: {difficulty_level}

Evaluate on these criteria:
1. Content Quality (35%): Accuracy, relevance, depth
2. Communication (25%): Clarity, structure, articulation
3. Confidence (20%): Assertiveness and conviction in delivery
4. Overall Impression (20%): Professional demeanor

Provide:
1. Individual scores (0-100) for each criterion
2. Brief feedback for each criterion
3. Overall score (weighted average)
4. Key strengths (2-3 points)
5. Areas for improvement (2-3 points)
6. One specific actionable tip

Format your response as JSON:
{{
    "scores": {{
        "content_quality": <score>,
        "communication": <score>,
        "confidence": <score>,
        "overall_impression": <score>
    }},
    "feedback": {{
        "content_quality": "<feedback>",
        "communication": "<feedback>",
        "confidence": "<feedback>",
        "overall_impression": "<feedback>"
    }},
    "overall_score": <weighted_score>,
    "strengths": ["<strength1>", "<strength2>", "<strength3>"],
    "improvements": ["<improvement1>", "<improvement2>", "<improvement3>"],
    "actionable_tip": "<specific tip>"
}}"""

VIDEO_ANALYSIS_PROMPT = """You are analyzing a candidate's body language and non-verbal communication during an interview response.

Based on the video analysis data provided:
{video_analysis_data}

Evaluate the candidate's:
1. Posture and body positioning
2. Facial expressions and eye contact
3. Hand gestures and body movements
4. Overall professional presence

Provide a body language score (0-100) and specific feedback on what was observed (both positive and negative).

Format as JSON:
{{
    "body_language_score": <score>,
    "posture_feedback": "<feedback>",
    "facial_expression_feedback": "<feedback>",
    "gesture_feedback": "<feedback>",
    "overall_presence": "<feedback>"
}}"""

AUDIO_ANALYSIS_PROMPT = """Analyze the audio characteristics of this interview response:

Transcript: {transcript}
Interview Type: {interview_type}

Evaluate:
1. Speaking pace and rhythm
2. Voice clarity and articulation
3. Filler words usage (um, uh, like, etc.)
4. Tone and energy level
5. Professional communication style

Provide detailed feedback on vocal delivery and communication effectiveness.

Format as JSON:
{{
    "vocal_score": <score>,
    "pace_feedback": "<feedback>",
    "clarity_feedback": "<feedback>",
    "filler_words": {{
        "count": <number>,
        "feedback": "<feedback>"
    }},
    "tone_feedback": "<feedback>",
    "professional_delivery": "<feedback>"
}}"""
