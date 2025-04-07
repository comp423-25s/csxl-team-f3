"""
Configuration settings for the CSXL application.
"""
import os
from typing import Optional

class Config:
    """Application configuration settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Study Buddy Configuration
    STUDY_BUDDY_MODEL: str = "gpt-4"  # Default to GPT-4, can be overridden
    STUDY_BUDDY_TEMPERATURE: float = 0.7  # Controls randomness in responses
    STUDY_BUDDY_MAX_TOKENS: int = 1000  # Maximum tokens in response
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate that required configuration is present."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set") 