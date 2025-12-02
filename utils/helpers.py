"""Utility helper functions for the Mock Interview Evaluator"""

import logging
from typing import Dict, Any, List
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def format_timestamp(timestamp: datetime = None) -> str:
    """Format timestamp for display"""
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def calculate_weighted_score(scores: Dict[str, float], weights: Dict[str, float]) -> float:
    """Calculate weighted average score"""
    total_score = 0.0
    total_weight = 0.0
    
    for key, score in scores.items():
        if key in weights:
            total_score += score * weights[key]
            total_weight += weights[key]
    
    return round(total_score / total_weight, 2) if total_weight > 0 else 0.0


def validate_score(score: Any) -> float:
    """Validate and normalize score to 0-100 range"""
    try:
        score = float(score)
        return max(0.0, min(100.0, score))
    except (ValueError, TypeError):
        return 0.0


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def get_score_color(score: float) -> str:
    """Get color code based on score"""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"


def extract_json_from_text(text: str) -> str:
    """Extract JSON content from text that may contain markdown code blocks"""
    # Remove markdown code blocks
    if "```json" in text:
        start = text.find("```json") + 7
        end = text.find("```", start)
        return text[start:end].strip()
    elif "```" in text:
        start = text.find("```") + 3
        end = text.find("```", start)
        return text[start:end].strip()
    return text.strip()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    import re
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename


def get_file_size_mb(file) -> float:
    """Get file size in MB"""
    file.seek(0, 2)  # Seek to end
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)  # Reset to beginning
    return round(size_mb, 2)


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split list into chunks of specified size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(*dicts: Dict) -> Dict:
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if division by zero"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format value as percentage"""
    return f"{value:.{decimals}f}%"


def is_valid_url(url: str) -> bool:
    """Check if string is a valid URL"""
    import re
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return pattern.match(url) is not None


def get_timestamp() -> int:
    """Get current timestamp in milliseconds"""
    return int(datetime.now().timestamp() * 1000)


def format_score_badge(score: float) -> str:
    """Format score as a badge emoji"""
    if score >= 90:
        return "🏆"
    elif score >= 80:
        return "🥇"
    elif score >= 70:
        return "🥈"
    elif score >= 60:
        return "🥉"
    else:
        return "📚"