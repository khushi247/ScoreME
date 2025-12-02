import json
from typing import Dict, Any, List, Optional
from groq import Groq
from config.settings import GROQ_API_KEY, GROQ_MODEL
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GroqService:
    """Service for interacting with Groq API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq client"""
        self.api_key = api_key or GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required. Set it in environment variables.")
        
        self.client = Groq(api_key=self.api_key)
        self.model = GROQ_MODEL
        logger.info(f"Initialized GroqService with model: {self.model}")
    
    def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        system_message: Optional[str] = None
    ) -> str:
        """Generate a completion from Groq API"""
        try:
            messages = []
            
            if system_message:
                messages.append({
                    "role": "system",
                    "content": system_message
                })
            
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            raise
    
    def generate_json_completion(
        self,
        prompt: str,
        temperature: float = 0.5,
        max_tokens: int = 2048,
        system_message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a JSON completion from Groq API"""
        try:
            response_text = self.generate_completion(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                system_message=system_message
            )
            
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            return json.loads(response_text)
        
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            return {
                "error": "Failed to parse JSON response",
                "raw_response": response_text
            }
        except Exception as e:
            logger.error(f"Error generating JSON completion: {str(e)}")
            raise
    
    def generate_questions(
        self,
        interview_type: str,
        difficulty_level: str,
        num_questions: int
    ) -> List[str]:
        """Generate interview questions"""
        from config.settings import QUESTION_GENERATION_PROMPT
        
        prompt = QUESTION_GENERATION_PROMPT.format(
            num_questions=num_questions,
            interview_type=interview_type,
            difficulty_level=difficulty_level
        )
        
        system_message = "You are an expert technical and behavioral interviewer with years of experience."
        
        response = self.generate_completion(
            prompt=prompt,
            temperature=0.8,
            system_message=system_message
        )
        
        questions = []
        for line in response.split('\n'):
            line = line.strip()
            if line and any(line.startswith(f"{i}.") or line.startswith(f"{i})") for i in range(1, 100)):
                question = line.split('.', 1)[-1].split(')', 1)[-1].strip()
                if question:
                    questions.append(question)
        
        return questions[:num_questions]