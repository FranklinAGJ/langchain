"""Configuration management for the Bible Motivator project."""
import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

class Config:
    """Application configuration with environment variable support."""
    
    def __init__(self):
        load_dotenv()
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables with defaults."""
        return {
            # OpenAI Configuration
            'openai_api_key': os.getenv('OPENAI_API_KEY'),
            'openai_model': os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            'openai_temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.6')),
            'openai_max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '300')),
            
            # Application Settings
            'verses_file': os.getenv('VERSES_FILE', 'bible_verses.json'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'response_max_words': int(os.getenv('RESPONSE_MAX_WORDS', '200')),
            
            # UI Settings
            'use_rich_ui': os.getenv('USE_RICH_UI', 'true').lower() == 'true',
            'show_verse_tags': os.getenv('SHOW_VERSE_TAGS', 'false').lower() == 'true',
            
            # Paths
            'project_root': Path(__file__).parent,
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self._config.get(key, default)
    
    def validate(self) -> bool:
        """Validate required configuration values."""
        required_keys = ['openai_api_key']
        
        for key in required_keys:
            if not self.get(key):
                return False
        
        return True
    
    def get_missing_config(self) -> list:
        """Get list of missing required configuration values."""
        required_keys = ['openai_api_key']
        missing = []
        
        for key in required_keys:
            if not self.get(key):
                missing.append(key)
        
        return missing

# Global config instance
config = Config()