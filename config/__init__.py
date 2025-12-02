"""Configuration package for Mock Interview Evaluator"""

from .settings import (
    GROQ_API_KEY,
    GROQ_MODEL,
    INTERVIEW_TYPES,
    DIFFICULTY_LEVELS,
    DEFAULT_NUM_QUESTIONS,
    EVALUATION_CRITERIA,
    PAGE_CONFIG
)

__all__ = [
    'GROQ_API_KEY',
    'GROQ_MODEL',
    'INTERVIEW_TYPES',
    'DIFFICULTY_LEVELS',
    'DEFAULT_NUM_QUESTIONS',
    'EVALUATION_CRITERIA',
    'PAGE_CONFIG'
]