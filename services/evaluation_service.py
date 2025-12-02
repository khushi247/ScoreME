from typing import Dict, Any, Optional
from services.groq_service import GroqService
from config.settings import (
    ANSWER_EVALUATION_PROMPT,
    VIDEO_ANALYSIS_PROMPT,
    AUDIO_ANALYSIS_PROMPT
)
import logging

logger = logging.getLogger(__name__)


class EvaluationService:
    """Service for evaluating interview responses"""
    
    def __init__(self, groq_service: GroqService):
        self.groq_service = groq_service
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        interview_type: str,
        difficulty_level: str
    ) -> Dict[str, Any]:
        """Evaluate a text answer"""
        try:
            prompt = ANSWER_EVALUATION_PROMPT.format(
                question=question,
                answer=answer,
                interview_type=interview_type,
                difficulty_level=difficulty_level
            )
            
            system_message = "You are an expert interview evaluator. Provide honest, constructive feedback."
            
            evaluation = self.groq_service.generate_json_completion(
                prompt=prompt,
                temperature=0.6,
                system_message=system_message
            )
            
            return evaluation
        
        except Exception as e:
            logger.error(f"Error evaluating answer: {str(e)}")
            return self._get_fallback_evaluation()
    
    def evaluate_video(
        self,
        video_analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Evaluate body language from video analysis"""
        try:
            # Extract MediaPipe scores if available
            body_language_score = video_analysis_data.get('body_language_score', 75)
            posture_score = video_analysis_data.get('posture_score', 75)
            eye_contact_score = video_analysis_data.get('eye_contact_score', 75)
            gesture_score = video_analysis_data.get('gesture_score', 75)
            
            return {
                "body_language_score": body_language_score,
                "posture_score": posture_score,
                "posture_feedback": video_analysis_data.get('posture', 'Unable to analyze'),
                "eye_contact_score": eye_contact_score,
                "facial_expression_feedback": video_analysis_data.get('facial_expressions', 'Unable to analyze'),
                "gesture_score": gesture_score,
                "gesture_feedback": video_analysis_data.get('gestures', 'Unable to analyze'),
                "overall_presence": video_analysis_data.get('overall_presence', 'Unable to analyze')
            }
        
        except Exception as e:
            logger.error(f"Error evaluating video: {str(e)}")
            return {
                "body_language_score": 75,
                "posture_feedback": "Unable to analyze body language from video.",
                "facial_expression_feedback": "Video analysis unavailable.",
                "gesture_feedback": "Video analysis unavailable.",
                "overall_presence": "Please ensure good lighting and camera positioning."
            }
    
    def evaluate_audio(
        self,
        transcript: str,
        interview_type: str
    ) -> Dict[str, Any]:
        """Evaluate vocal delivery from audio"""
        try:
            prompt = AUDIO_ANALYSIS_PROMPT.format(
                transcript=transcript,
                interview_type=interview_type
            )
            
            system_message = "You are a speech and communication expert."
            
            audio_eval = self.groq_service.generate_json_completion(
                prompt=prompt,
                temperature=0.5,
                system_message=system_message
            )
            
            return audio_eval
        
        except Exception as e:
            logger.error(f"Error evaluating audio: {str(e)}")
            return {
                "vocal_score": 75,
                "pace_feedback": "Unable to analyze audio quality.",
                "clarity_feedback": "Audio analysis unavailable.",
                "filler_words": {"count": 0, "feedback": "N/A"},
                "tone_feedback": "Audio analysis unavailable.",
                "professional_delivery": "Please ensure clear audio recording."
            }
    
    def calculate_overall_score(
        self,
        content_score: float,
        communication_score: float,
        body_language_score: float,
        vocal_score: float
    ) -> float:
        """Calculate weighted overall score"""
        weights = {
            "content": 0.35,
            "communication": 0.25,
            "body_language": 0.20,
            "vocal": 0.20
        }
        
        overall = (
            content_score * weights["content"] +
            communication_score * weights["communication"] +
            body_language_score * weights["body_language"] +
            vocal_score * weights["vocal"]
        )
        
        return round(overall, 1)
    
    def _get_fallback_evaluation(self) -> Dict[str, Any]:
        """Return fallback evaluation if API fails"""
        return {
            "scores": {
                "content_quality": 70,
                "communication": 70,
                "confidence": 70,
                "overall_impression": 70
            },
            "feedback": {
                "content_quality": "Unable to evaluate due to technical error.",
                "communication": "Unable to evaluate due to technical error.",
                "confidence": "Unable to evaluate due to technical error.",
                "overall_impression": "Please try again."
            },
            "overall_score": 70,
            "strengths": ["Response recorded successfully"],
            "improvements": ["Please try submitting again for detailed feedback"],
            "actionable_tip": "Ensure your response is clear and detailed."
        }