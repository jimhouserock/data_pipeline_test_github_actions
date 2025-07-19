"""
Utility functions for the data pipeline.
"""

import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


def setup_logging(level: str = 'INFO', format_str: Optional[str] = None):
    """Set up logging configuration."""
    if format_str is None:
        format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_str,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('data/pipeline.log', mode='a')
        ]
    )


def ensure_directory(directory: str) -> bool:
    """Ensure directory exists, create if not."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def safe_json_load(filepath: str) -> Optional[Dict]:
    """Safely load JSON file with error handling."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        logger.error(f"Error loading JSON from {filepath}: {e}")
        return None


def safe_json_save(data: Any, filepath: str) -> bool:
    """Safely save data to JSON file with error handling."""
    try:
        # Ensure directory exists
        directory = os.path.dirname(filepath)
        if directory:
            ensure_directory(directory)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Error saving JSON to {filepath}: {e}")
        return False


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Basic text cleaning
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = ' '.join(text.split())  # Remove extra whitespace
    text = text.strip()
    
    return text


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    
    # Try to truncate at word boundary
    truncated = text[:max_length]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.8:  # If we can find a space in the last 20%
        return truncated[:last_space]
    else:
        return truncated


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"


def get_file_size(filepath: str) -> str:
    """Get human readable file size."""
    try:
        size_bytes = os.path.getsize(filepath)
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    except Exception:
        return "Unknown"


def validate_video_data(video: Dict[str, Any]) -> bool:
    """Validate that video data has required fields."""
    required_fields = ['video_id', 'title']
    
    for field in required_fields:
        if not video.get(field):
            logger.warning(f"Video missing required field: {field}")
            return False
    
    return True


def create_backup(filepath: str) -> bool:
    """Create a timestamped backup of a file."""
    try:
        if not os.path.exists(filepath):
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{filepath}.backup_{timestamp}"
        
        import shutil
        shutil.copy2(filepath, backup_path)
        
        logger.info(f"Created backup: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create backup of {filepath}: {e}")
        return False


def get_latest_file(directory: str, pattern: str) -> Optional[str]:
    """Get the most recently modified file matching pattern."""
    try:
        import glob
        
        files = glob.glob(os.path.join(directory, pattern))
        if not files:
            return None
        
        # Sort by modification time, newest first
        files.sort(key=os.path.getmtime, reverse=True)
        return files[0]
        
    except Exception as e:
        logger.error(f"Error finding latest file in {directory}: {e}")
        return None


def print_pipeline_summary(stats: Dict[str, Any]):
    """Print a formatted summary of pipeline results."""
    print("\n" + "="*50)
    print("PIPELINE SUMMARY")
    print("="*50)
    
    if stats:
        print(f"Total Videos: {stats.get('total_videos', 0)}")
        print(f"Videos with Transcripts: {stats.get('videos_with_transcripts', 0)}")
        print(f"Videos with Embeddings: {stats.get('videos_with_embeddings', 0)}")
        print(f"Total Views: {stats.get('total_views', 0):,}")
        print(f"Total Likes: {stats.get('total_likes', 0):,}")
        print(f"Total Comments: {stats.get('total_comments', 0):,}")
        
        date_range = stats.get('date_range', {})
        if date_range:
            print(f"Date Range: {date_range.get('earliest', 'N/A')} to {date_range.get('latest', 'N/A')}")
        
        print(f"Generated At: {stats.get('generated_at', 'N/A')}")
    else:
        print("No statistics available")
    
    print("="*50)


# Example usage
if __name__ == "__main__":
    # Test utility functions
    setup_logging()
    
    test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
    
    # Test JSON operations
    if safe_json_save(test_data, "data/test.json"):
        loaded_data = safe_json_load("data/test.json")
        print("JSON operations successful:", loaded_data)
    
    # Test text operations
    sample_text = "This is a   sample text\nwith multiple   spaces\nand newlines."
    cleaned = clean_text(sample_text)
    print(f"Cleaned text: '{cleaned}'")
    
    truncated = truncate_text(cleaned, 20)
    print(f"Truncated text: '{truncated}'")
    
    print("Utility functions test completed!")
