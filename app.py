from dotenv import load_dotenv
import os

load_dotenv()  # <-- this loads variables from .env into os.environ

# Optional: confirm your key is loaded
print("GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from ui.components import render_sidebar, render_interview_section
from ui.state import initialize_session_state
from services.interview_service import InterviewService
from config.settings import PAGE_CONFIG

# Page configuration
st.set_page_config(**PAGE_CONFIG)

def main():
    """Main application entry point"""
    # Initialize session state
    initialize_session_state()
    
    # Initialize service
    interview_service = InterviewService()
    
    # Render UI
    st.title("ScoreMe — Practice. Perform. Get hired.")
    st.markdown("Practice your interview skills with AI-powered feedback on answers, body language, and communication.")
    
    # Sidebar
    render_sidebar()
    
    # Main interview section
    render_interview_section(interview_service)

if __name__ == "__main__":
    main()
