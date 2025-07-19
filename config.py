"""
Configuration settings for the data pipeline.
"""

import os
from typing import Optional

class PipelineConfig:
    """Configuration class for the data pipeline."""
    
    # API Configuration
    YOUTUBE_API_KEY: Optional[str] = os.getenv('YOUTUBE_API_KEY')
    YOUTUBE_CHANNEL_ID: Optional[str] = os.getenv('YOUTUBE_CHANNEL_ID')
    
    # Pipeline Settings
    MAX_VIDEOS: int = int(os.getenv('MAX_VIDEOS', 25))
    DATA_DIR: str = os.getenv('DATA_DIR', 'data')
    
    # Model Settings
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    MAX_TRANSCRIPT_LENGTH: int = int(os.getenv('MAX_TRANSCRIPT_LENGTH', 2000))
    MAX_COMBINED_TEXT_LENGTH: int = int(os.getenv('MAX_COMBINED_TEXT_LENGTH', 5000))
    
    # Default Channel IDs for different creators (examples)
    DEFAULT_CHANNELS = {
        'data_science': 'UC_x5XG1OV2P6uZZ5FSM9Ttw',  # Example channel
        'tech_talks': 'UCBJycsmduvYEL83R_U4JriQ',    # Example channel
        'ml_tutorials': 'UCWN3xxRkmTPmbKwht9FuE5A'    # Example channel
    }
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if not cls.YOUTUBE_API_KEY:
            print("ERROR: YOUTUBE_API_KEY is required")
            return False
        
        return True
    
    @classmethod
    def get_channel_id(cls, channel_type: str = 'data_science') -> str:
        """Get channel ID with fallback to defaults."""
        return cls.YOUTUBE_CHANNEL_ID or cls.DEFAULT_CHANNELS.get(channel_type, cls.DEFAULT_CHANNELS['data_science'])
    
    @classmethod
    def print_config(cls):
        """Print current configuration (without sensitive data)."""
        print("Pipeline Configuration:")
        print(f"  Max Videos: {cls.MAX_VIDEOS}")
        print(f"  Data Directory: {cls.DATA_DIR}")
        print(f"  Embedding Model: {cls.EMBEDDING_MODEL}")
        print(f"  API Key Set: {'Yes' if cls.YOUTUBE_API_KEY else 'No'}")
        print(f"  Channel ID Set: {'Yes' if cls.YOUTUBE_CHANNEL_ID else 'No (using default)'}")
        print(f"  Log Level: {cls.LOG_LEVEL}")


# Example usage and validation
if __name__ == "__main__":
    config = PipelineConfig()
    config.print_config()
    
    if config.validate():
        print("✅ Configuration is valid")
    else:
        print("❌ Configuration is invalid")
