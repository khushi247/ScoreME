import streamlit as st
from typing import List, Dict, Any


def initialize_session_state():
    """Initialize all session state variables"""
    
    # Interview configuration
    if "interview_type" not in st.session_state:
        st.session_state.interview_type = "Technical - Software Engineering"
    
    if "difficulty_level" not in st.session_state:
        st.session_state.difficulty_level = "Mid Level"
    
    if "num_questions" not in st.session_state:
        st.session_state.num_questions = 5
    
    # Interview state
    if "questions" not in st.session_state:
        st.session_state.questions = []
    
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
    
    if "interview_started" not in st.session_state:
        st.session_state.interview_started = False
    
    if "interview_completed" not in st.session_state:
        st.session_state.interview_completed = False
    
    # Responses and evaluations
    if "responses" not in st.session_state:
        st.session_state.responses = []
    
    if "evaluations" not in st.session_state:
        st.session_state.evaluations = []
    
    # UI state
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    if "response_mode" not in st.session_state:
        st.session_state.response_mode = "Text"


def reset_interview():
    """Reset interview to initial state"""
    st.session_state.questions = []
    st.session_state.current_question_index = 0
    st.session_state.interview_started = False
    st.session_state.interview_completed = False
    st.session_state.responses = []
    st.session_state.evaluations = []
    st.session_state.processing = False


def start_interview(questions: List[str]):
    """Start the interview with generated questions"""
    st.session_state.questions = questions
    st.session_state.interview_started = True
    st.session_state.current_question_index = 0
    st.session_state.responses = []
    st.session_state.evaluations = []
    st.session_state.interview_completed = False


def next_question():
    """Move to next question"""
    if st.session_state.current_question_index < len(st.session_state.questions) - 1:
        st.session_state.current_question_index += 1
    else:
        st.session_state.interview_completed = True


def previous_question():
    """Move to previous question"""
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1


def add_evaluation(evaluation: Dict[str, Any]):
    """Add evaluation to session state"""
    st.session_state.evaluations.append(evaluation)


def get_current_question() -> str:
    """Get current question"""
    if st.session_state.questions and st.session_state.current_question_index < len(st.session_state.questions):
        return st.session_state.questions[st.session_state.current_question_index]
    return ""


def get_progress() -> tuple:
    """Get interview progress (current, total)"""
    return (
        st.session_state.current_question_index + 1,
        len(st.session_state.questions)
    )