from typing import Dict, Any, List, Optional
from services.groq_service import GroqService
from services.evaluation_service import EvaluationService
from services.media_processor import MediaProcessor
import logging

logger = logging.getLogger(__name__)


class InterviewService:
    """Main service orchestrating the interview process"""
    
    def __init__(self):
        try:
            self.groq_service = GroqService()
            self.evaluation_service = EvaluationService(self.groq_service)
            self.media_processor = MediaProcessor()
        except ValueError as e:
            logger.error(f"Failed to initialize services: {str(e)}")
            raise
    
    def generate_interview_questions(
        self,
        interview_type: str,
        difficulty_level: str,
        num_questions: int = 5
    ) -> List[str]:
        """Generate interview questions"""
        try:
            questions = self.groq_service.generate_questions(
                interview_type=interview_type,
                difficulty_level=difficulty_level,
                num_questions=num_questions
            )
            
            if not questions:
                return self._get_fallback_questions(interview_type, num_questions)
            
            return questions
        
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return self._get_fallback_questions(interview_type, num_questions)
    
    def evaluate_text_response(
        self,
        question: str,
        answer: str,
        interview_type: str,
        difficulty_level: str
    ) -> Dict[str, Any]:
        """Evaluate a text response"""
        evaluation = self.evaluation_service.evaluate_answer(
            question=question,
            answer=answer,
            interview_type=interview_type,
            difficulty_level=difficulty_level
        )
        
        return {
            "type": "text",
            "evaluation": evaluation,
            "question": question,
            "answer": answer
        }
    
    def evaluate_audio_response(
        self,
        question: str,
        audio_file,
        interview_type: str,
        difficulty_level: str
    ) -> Dict[str, Any]:
        """Evaluate an audio response"""
        # Process audio to get transcript
        transcript = self.media_processor.transcribe_audio(audio_file)
        
        # Evaluate content
        content_eval = self.evaluation_service.evaluate_answer(
            question=question,
            answer=transcript,
            interview_type=interview_type,
            difficulty_level=difficulty_level
        )
        
        # Evaluate vocal delivery
        vocal_eval = self.evaluation_service.evaluate_audio(
            transcript=transcript,
            interview_type=interview_type
        )
        
        return {
            "type": "audio",
            "transcript": transcript,
            "content_evaluation": content_eval,
            "vocal_evaluation": vocal_eval,
            "question": question
        }
    
    def evaluate_video_response(
        self,
        question: str,
        video_file,
        interview_type: str,
        difficulty_level: str
    ) -> Dict[str, Any]:
        """Evaluate a video response"""
        # Process video
        video_analysis = self.media_processor.analyze_video(video_file)
        transcript = video_analysis.get("transcript", "")
        
        # Evaluate content
        content_eval = self.evaluation_service.evaluate_answer(
            question=question,
            answer=transcript,
            interview_type=interview_type,
            difficulty_level=difficulty_level
        )
        
        # Evaluate body language
        body_language_eval = self.evaluation_service.evaluate_video(
            video_analysis_data=video_analysis.get("body_language", {})
        )
        
        # Evaluate vocal delivery
        vocal_eval = self.evaluation_service.evaluate_audio(
            transcript=transcript,
            interview_type=interview_type
        )
        
        return {
            "type": "video",
            "transcript": transcript,
            "content_evaluation": content_eval,
            "body_language_evaluation": body_language_eval,
            "vocal_evaluation": vocal_eval,
            "question": question
        }
    
    def _get_fallback_questions(self, interview_type: str, num_questions: int) -> List[str]:
        """Return fallback questions if generation fails"""
        fallback_questions = {
            "Technical - Software Engineering": [
                "Explain the difference between abstract classes and interfaces.",
                "How would you design a URL shortening service like bit.ly?",
                "What is the time complexity of common sorting algorithms?",
                "Describe your experience with version control systems.",
                "How do you approach debugging a complex issue in production?"
            ],
            "Behavioral": [
                "Tell me about a time when you faced a significant challenge at work.",
                "Describe a situation where you had to work with a difficult team member.",
                "Give an example of when you showed leadership skills.",
                "Tell me about a project you're particularly proud of.",
                "How do you handle tight deadlines and pressure?"
            ],
            "Leadership": [
                "How do you motivate a team that's falling behind on deliverables?",
                "Describe your leadership style.",
                "Tell me about a time you had to make an unpopular decision.",
                "How do you handle conflicts between team members?",
                "What's your approach to delegating tasks?"
            ]
        }
        
        questions = fallback_questions.get(
            interview_type,
            fallback_questions["Behavioral"]
        )
        
        return questions[:num_questions]