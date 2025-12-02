"""Unit tests for Mock Interview Evaluator services"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.evaluation_service import EvaluationService
from services.interview_service import InterviewService
from utils.helpers import (
    calculate_weighted_score,
    validate_score,
    truncate_text,
    format_duration
)


class TestEvaluationService(unittest.TestCase):
    """Test cases for EvaluationService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_groq_service = Mock()
        self.evaluation_service = EvaluationService(self.mock_groq_service)
    
    def test_calculate_overall_score(self):
        """Test overall score calculation"""
        score = self.evaluation_service.calculate_overall_score(
            content_score=80,
            communication_score=70,
            body_language_score=75,
            vocal_score=85
        )
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    def test_fallback_evaluation(self):
        """Test fallback evaluation structure"""
        fallback = self.evaluation_service._get_fallback_evaluation()
        
        self.assertIn('scores', fallback)
        self.assertIn('feedback', fallback)
        self.assertIn('overall_score', fallback)
        self.assertIn('strengths', fallback)
        self.assertIn('improvements', fallback)
        self.assertIn('actionable_tip', fallback)


class TestInterviewService(unittest.TestCase):
    """Test cases for InterviewService"""
    
    @patch('services.interview_service.GroqService')
    @patch('services.interview_service.EvaluationService')
    @patch('services.interview_service.MediaProcessor')
    def test_initialization(self, mock_media, mock_eval, mock_groq):
        """Test service initialization"""
        service = InterviewService()
        self.assertIsNotNone(service.groq_service)
        self.assertIsNotNone(service.evaluation_service)
        self.assertIsNotNone(service.media_processor)
    
    def test_fallback_questions(self):
        """Test fallback questions generation"""
        with patch('services.interview_service.GroqService'):
            service = InterviewService()
            questions = service._get_fallback_questions("Behavioral", 3)
            
            self.assertEqual(len(questions), 3)
            self.assertTrue(all(isinstance(q, str) for q in questions))
            self.assertTrue(all(len(q) > 0 for q in questions))


class TestHelperFunctions(unittest.TestCase):
    """Test cases for utility helper functions"""
    
    def test_calculate_weighted_score(self):
        """Test weighted score calculation"""
        scores = {'content': 80, 'communication': 70}
        weights = {'content': 0.6, 'communication': 0.4}
        
        result = calculate_weighted_score(scores, weights)
        expected = (80 * 0.6 + 70 * 0.4)
        
        self.assertEqual(result, expected)
    
    def test_validate_score(self):
        """Test score validation"""
        self.assertEqual(validate_score(50), 50.0)
        self.assertEqual(validate_score(150), 100.0)
        self.assertEqual(validate_score(-10), 0.0)
        self.assertEqual(validate_score("invalid"), 0.0)
    
    def test_truncate_text(self):
        """Test text truncation"""
        long_text = "This is a very long text that needs to be truncated"
        result = truncate_text(long_text, 20)
        
        self.assertLessEqual(len(result), 20)
        self.assertTrue(result.endswith("..."))
    
    def test_format_duration(self):
        """Test duration formatting"""
        self.assertEqual(format_duration(30), "30s")
        self.assertEqual(format_duration(90), "1.5m")
        self.assertEqual(format_duration(3600), "1.0h")


class TestScoreValidation(unittest.TestCase):
    """Test cases for score validation logic"""
    
    def test_score_range(self):
        """Test score is within valid range"""
        test_scores = [0, 25, 50, 75, 100, -10, 150]
        
        for score in test_scores:
            validated = validate_score(score)
            self.assertGreaterEqual(validated, 0)
            self.assertLessEqual(validated, 100)
    
    def test_score_types(self):
        """Test different score input types"""
        self.assertEqual(validate_score(75), 75.0)
        self.assertEqual(validate_score(75.5), 75.5)
        self.assertEqual(validate_score("75"), 75.0)
        self.assertEqual(validate_score(None), 0.0)


if __name__ == '__main__':
    unittest.main()