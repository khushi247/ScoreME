import streamlit as st
from typing import Dict, Any
from ui.state import (
    reset_interview,
    start_interview,
    next_question,
    previous_question,
    get_current_question,
    get_progress,
    add_evaluation
)
from config.settings import (
    INTERVIEW_TYPES,
    DIFFICULTY_LEVELS,
    DEFAULT_NUM_QUESTIONS,
    MAX_VIDEO_SIZE_MB,
    MAX_AUDIO_SIZE_MB,
    SUPPORTED_VIDEO_FORMATS,
    SUPPORTED_AUDIO_FORMATS
)


def render_sidebar():
    """Render sidebar with configuration options"""
    with st.sidebar:
        st.header("⚙️ Interview Configuration")
        
        # Interview type selection
        st.session_state.interview_type = st.selectbox(
            "Interview Type",
            INTERVIEW_TYPES,
            index=INTERVIEW_TYPES.index(st.session_state.interview_type)
        )
        
        # Difficulty level
        st.session_state.difficulty_level = st.selectbox(
            "Difficulty Level",
            DIFFICULTY_LEVELS,
            index=DIFFICULTY_LEVELS.index(st.session_state.difficulty_level)
        )
        
        # Number of questions
        st.session_state.num_questions = st.slider(
            "Number of Questions",
            min_value=1,
            max_value=10,
            value=st.session_state.num_questions
        )
        
        # Response mode
        st.session_state.response_mode = st.radio(
            "Response Mode",
            ["Text", "Audio", "Video"],
            help="Choose how you want to respond to questions"
        )
        
        st.divider()
        
        # Instructions
        st.subheader("📋 Instructions")
        st.markdown("""
        1. Configure your interview settings
        2. Click 'Generate Questions'
        3. Answer each question
        4. Get detailed AI feedback
        5. Review your overall performance
        """)
        
        st.divider()
        
        # API Key status
        import os
        api_key = os.getenv("GROQ_API_KEY", "")
        if api_key:
            st.success("✅ API Key Configured")
        else:
            st.error("❌ GROQ_API_KEY not set")
            st.info("Set GROQ_API_KEY in environment variables")


def render_interview_section(interview_service):
    """Render main interview section"""
    
    if not st.session_state.interview_started:
        render_start_screen(interview_service)
    elif st.session_state.interview_completed:
        render_results_screen()
    else:
        render_question_screen(interview_service)


def render_start_screen(interview_service):
    """Render interview start screen"""
    st.markdown("### 🚀 Ready to Start Your Mock Interview?")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Interview Type", st.session_state.interview_type)
    with col2:
        st.metric("Difficulty", st.session_state.difficulty_level)
    with col3:
        st.metric("Questions", st.session_state.num_questions)
    
    st.markdown("---")
    
    if st.button("🎬 Generate Questions & Start Interview", type="primary", use_container_width=True):
        with st.spinner("Generating interview questions..."):
            questions = interview_service.generate_interview_questions(
                interview_type=st.session_state.interview_type,
                difficulty_level=st.session_state.difficulty_level,
                num_questions=st.session_state.num_questions
            )
            
            if questions:
                start_interview(questions)
                st.rerun()
            else:
                st.error("Failed to generate questions. Please try again.")


def render_question_screen(interview_service):
    """Render question answering screen"""
    current, total = get_progress()
    question = get_current_question()
    
    # Progress bar
    progress = current / total
    st.progress(progress, text=f"Question {current} of {total}")
    
    st.markdown("---")
    
    # Current question
    st.markdown(f"### 📝 Question {current}")
    st.info(question)
    
    # Response input based on mode
    if st.session_state.response_mode == "Text":
        render_text_input(interview_service, question)
    elif st.session_state.response_mode == "Audio":
        render_audio_input(interview_service, question)
    elif st.session_state.response_mode == "Video":
        render_video_input(interview_service, question)
    
    # Navigation buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current > 1:
            if st.button("⬅️ Previous", use_container_width=True):
                previous_question()
                st.rerun()
    
    with col3:
        if st.button("🏠 End Interview", use_container_width=True, type="secondary"):
            if st.session_state.evaluations:
                st.session_state.interview_completed = True
                st.rerun()
            else:
                st.warning("Please answer at least one question before ending.")


def render_text_input(interview_service, question):
    """Render text input for answers"""
    answer = st.text_area(
        "Your Answer",
        height=200,
        placeholder="Type your answer here...",
        key=f"answer_text_{st.session_state.current_question_index}"
    )
    
    if st.button("📤 Submit Answer", type="primary", use_container_width=True):
        if answer.strip():
            with st.spinner("Evaluating your response..."):
                evaluation = interview_service.evaluate_text_response(
                    question=question,
                    answer=answer,
                    interview_type=st.session_state.interview_type,
                    difficulty_level=st.session_state.difficulty_level
                )
                add_evaluation(evaluation)
                st.success("✅ Answer evaluated!")
                
                # Show evaluation
                render_evaluation_result(evaluation)
                
                # Move to next question or complete
                if st.button("Continue to Next Question ➡️", use_container_width=True):
                    next_question()
                    st.rerun()
        else:
            st.warning("Please enter an answer before submitting.")


def render_audio_input(interview_service, question):
    """Render audio input for answers"""
    st.markdown("🎤 **Record or upload your audio response**")
    
    audio_file = st.file_uploader(
        "Upload Audio File",
        type=["mp3", "wav", "m4a", "ogg"],
        key=f"audio_{st.session_state.current_question_index}"
    )
    
    if audio_file:
        st.audio(audio_file)
        
        if st.button("📤 Submit Audio Answer", type="primary", use_container_width=True):
            # Validate file size
            from services.media_processor import MediaProcessor
            processor = MediaProcessor()
            
            if not processor.validate_file_size(audio_file, MAX_AUDIO_SIZE_MB):
                st.error(f"File too large. Maximum size is {MAX_AUDIO_SIZE_MB}MB")
                return
            
            with st.spinner("Transcribing and evaluating your response..."):
                evaluation = interview_service.evaluate_audio_response(
                    question=question,
                    audio_file=audio_file,
                    interview_type=st.session_state.interview_type,
                    difficulty_level=st.session_state.difficulty_level
                )
                add_evaluation(evaluation)
                st.success("✅ Audio response evaluated!")
                
                # Show evaluation
                render_evaluation_result(evaluation)
                
                if st.button("Continue to Next Question ➡️", use_container_width=True):
                    next_question()
                    st.rerun()


def render_video_input(interview_service, question):
    """Render video input for answers"""
    st.markdown("🎥 **Record or upload your video response**")
    
    video_file = st.file_uploader(
        "Upload Video File",
        type=["mp4", "avi", "mov", "webm"],
        key=f"video_{st.session_state.current_question_index}"
    )
    
    if video_file:
        st.video(video_file)
        
        if st.button("📤 Submit Video Answer", type="primary", use_container_width=True):
            # Validate file size
            from services.media_processor import MediaProcessor
            processor = MediaProcessor()
            
            if not processor.validate_file_size(video_file, MAX_VIDEO_SIZE_MB):
                st.error(f"File too large. Maximum size is {MAX_VIDEO_SIZE_MB}MB")
                return
            
            with st.spinner("Analyzing video and evaluating your response..."):
                evaluation = interview_service.evaluate_video_response(
                    question=question,
                    video_file=video_file,
                    interview_type=st.session_state.interview_type,
                    difficulty_level=st.session_state.difficulty_level
                )
                add_evaluation(evaluation)
                st.success("✅ Video response evaluated!")
                
                # Show evaluation
                render_evaluation_result(evaluation)
                
                if st.button("Continue to Next Question ➡️", use_container_width=True):
                    next_question()
                    st.rerun()


def render_evaluation_result(evaluation: Dict[str, Any]):
    """Render evaluation results"""
    st.markdown("---")
    st.markdown("### 📊 Evaluation Results")
    
    if evaluation["type"] == "text":
        render_text_evaluation(evaluation["evaluation"])
    elif evaluation["type"] == "audio":
        render_audio_evaluation(evaluation)
    elif evaluation["type"] == "video":
        render_video_evaluation(evaluation)


def render_text_evaluation(evaluation: Dict[str, Any]):
    """Render text evaluation results"""
    # Overall score
    overall_score = evaluation.get("overall_score", 0)
    st.metric("Overall Score", f"{overall_score}/100", delta=get_score_delta(overall_score))
    
    # Individual scores
    col1, col2, col3, col4 = st.columns(4)
    scores = evaluation.get("scores", {})
    
    with col1:
        st.metric("Content", f"{scores.get('content_quality', 0)}/100")
    with col2:
        st.metric("Communication", f"{scores.get('communication', 0)}/100")
    with col3:
        st.metric("Confidence", f"{scores.get('confidence', 0)}/100")
    with col4:
        st.metric("Impression", f"{scores.get('overall_impression', 0)}/100")
    
    # Detailed feedback
    with st.expander("📝 Detailed Feedback", expanded=True):
        feedback = evaluation.get("feedback", {})
        for criterion, comment in feedback.items():
            st.markdown(f"**{criterion.replace('_', ' ').title()}:** {comment}")
    
    # Strengths
    with st.expander("💪 Strengths"):
        strengths = evaluation.get("strengths", [])
        for strength in strengths:
            st.markdown(f"✅ {strength}")
    
    # Improvements
    with st.expander("🎯 Areas for Improvement"):
        improvements = evaluation.get("improvements", [])
        for improvement in improvements:
            st.markdown(f"🔸 {improvement}")
    
    # Actionable tip
    st.info(f"💡 **Tip:** {evaluation.get('actionable_tip', 'Keep practicing!')}")


def render_audio_evaluation(evaluation: Dict[str, Any]):
    """Render audio evaluation results"""
    # Show transcript
    with st.expander("📝 Transcript", expanded=True):
        st.write(evaluation.get("transcript", ""))
    
    # Content evaluation
    st.markdown("#### Content Evaluation")
    render_text_evaluation(evaluation.get("content_evaluation", {}))
    
    # Vocal evaluation
    st.markdown("#### Vocal Delivery")
    vocal_eval = evaluation.get("vocal_evaluation", {})
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Vocal Score", f"{vocal_eval.get('vocal_score', 0)}/100")
    with col2:
        filler_data = vocal_eval.get("filler_words", {})
        st.metric("Filler Words", filler_data.get("count", 0))
    
    with st.expander("🎤 Vocal Feedback"):
        st.markdown(f"**Pace:** {vocal_eval.get('pace_feedback', 'N/A')}")
        st.markdown(f"**Clarity:** {vocal_eval.get('clarity_feedback', 'N/A')}")
        st.markdown(f"**Tone:** {vocal_eval.get('tone_feedback', 'N/A')}")


def render_video_evaluation(evaluation: Dict[str, Any]):
    """Render video evaluation results"""
    # Show transcript
    with st.expander("📝 Transcript"):
        st.write(evaluation.get("transcript", ""))
    
    # Content evaluation
    st.markdown("#### Content Evaluation")
    render_text_evaluation(evaluation.get("content_evaluation", {}))
    
    # Body language evaluation
    st.markdown("#### Body Language Analysis")
    body_eval = evaluation.get("body_language_evaluation", {})
    
    st.metric("Body Language Score", f"{body_eval.get('body_language_score', 0)}/100")
    
    with st.expander("👤 Body Language Feedback"):
        st.markdown(f"**Posture:** {body_eval.get('posture_feedback', 'N/A')}")
        st.markdown(f"**Facial Expressions:** {body_eval.get('facial_expression_feedback', 'N/A')}")
        st.markdown(f"**Gestures:** {body_eval.get('gesture_feedback', 'N/A')}")
        st.markdown(f"**Overall Presence:** {body_eval.get('overall_presence', 'N/A')}")
    
    # Vocal evaluation
    st.markdown("#### Vocal Delivery")
    vocal_eval = evaluation.get("vocal_evaluation", {})
    st.metric("Vocal Score", f"{vocal_eval.get('vocal_score', 0)}/100")


def render_results_screen():
    """Render final results screen"""
    st.markdown("## 🎉 Interview Completed!")
    st.balloons()
    
    if not st.session_state.evaluations:
        st.warning("No evaluations available.")
        if st.button("Start New Interview", use_container_width=True):
            reset_interview()
            st.rerun()
        return
    
    # Calculate overall statistics
    total_evaluations = len(st.session_state.evaluations)
    
    scores = []
    for eval_data in st.session_state.evaluations:
        if eval_data["type"] == "text":
            scores.append(eval_data["evaluation"].get("overall_score", 0))
        else:
            scores.append(eval_data["content_evaluation"].get("overall_score", 0))
    
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Questions Answered", total_evaluations)
    with col2:
        st.metric("Average Score", f"{avg_score:.1f}/100")
    with col3:
        performance = get_performance_level(avg_score)
        st.metric("Performance", performance)
    
    st.markdown("---")
    
    # Detailed results for each question
    st.markdown("### 📋 Detailed Results")
    
    for idx, evaluation in enumerate(st.session_state.evaluations):
        with st.expander(f"Question {idx + 1}: {evaluation.get('question', '')[:100]}..."):
            render_evaluation_result(evaluation)
    
    st.markdown("---")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start New Interview", use_container_width=True, type="primary"):
            reset_interview()
            st.rerun()
    with col2:
        if st.button("📥 Download Report", use_container_width=True):
            st.info("Report download feature coming soon!")


def get_score_delta(score: float) -> str:
    """Get score delta indicator"""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    else:
        return "Needs Work"


def get_performance_level(avg_score: float) -> str:
    """Get performance level based on average score"""
    if avg_score >= 85:
        return "🌟 Excellent"
    elif avg_score >= 70:
        return "✅ Good"
    elif avg_score >= 50:
        return "⚠️ Fair"
    else:
        return "📚 Needs Practice"