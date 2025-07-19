"""
Load module for YouTube data pipeline.
Handles saving processed data to files and managing data persistence.
"""

import os
import json
import logging
from datetime import datetime
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Loads processed data into storage (files, databases, etc.)."""
    
    def __init__(self, data_dir='data'):
        """Initialize with data directory."""
        self.data_dir = data_dir
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_to_json(self, data, filename):
        """Save data to JSON file."""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved data to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to {filepath}: {e}")
            return False
    
    def load_from_json(self, filename):
        """Load data from JSON file."""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Loaded data from {filepath}")
                return data
            else:
                logger.warning(f"File not found: {filepath}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading from {filepath}: {e}")
            return None
    
    def save_to_csv(self, data, filename):
        """Save data to CSV file (flattened structure)."""
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Handle nested data (like embeddings) by converting to strings
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Check if column contains lists/dicts
                    sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
                    if isinstance(sample_val, (list, dict)):
                        df[col] = df[col].astype(str)
            
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Saved data to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving to {filepath}: {e}")
            return False
    
    def create_summary_stats(self, data):
        """Create summary statistics for the data."""
        try:
            stats = {
                'total_videos': len(data),
                'videos_with_transcripts': sum(1 for video in data if video.get('transcript')),
                'videos_with_embeddings': sum(1 for video in data if video.get('embeddings')),
                'total_views': sum(int(video.get('view_count', 0)) for video in data),
                'total_likes': sum(int(video.get('like_count', 0)) for video in data),
                'total_comments': sum(int(video.get('comment_count', 0)) for video in data),
                'date_range': {
                    'earliest': min(video.get('published_at', '') for video in data if video.get('published_at')),
                    'latest': max(video.get('published_at', '') for video in data if video.get('published_at'))
                },
                'generated_at': datetime.now().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error creating summary stats: {e}")
            return {}
    
    def log_pipeline_run(self, stats, success=True, error_msg=None):
        """Log pipeline execution details."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'success': success,
            'stats': stats,
            'error': error_msg
        }
        
        log_file = os.path.join(self.data_dir, 'pipeline_log.json')
        
        try:
            # Load existing logs
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
            
            # Add new log entry
            logs.append(log_entry)
            
            # Keep only last 100 entries
            logs = logs[-100:]
            
            # Save updated logs
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Logged pipeline run to {log_file}")
            
        except Exception as e:
            logger.error(f"Error logging pipeline run: {e}")
    
    def load_data(self, processed_data):
        """Main loading method - accumulates historical data."""
        try:
            logger.info(f"Loading weather data")

            # Add timestamp to new data
            from datetime import datetime
            processed_data['recorded_at'] = datetime.now().isoformat()

            # Load existing historical data
            historical_data = self.load_from_json('weather_history.json') or []

            # Append new data
            historical_data.append(processed_data)

            # Keep only last 30 days to prevent file from getting huge
            if len(historical_data) > 30:
                historical_data = historical_data[-30:]

            # Save accumulated historical data
            history_file = "weather_history.json"
            success_json = self.save_to_json(historical_data, history_file)

            # Save latest data only (for current weather)
            latest_file = "weather_latest.json"
            self.save_to_json(processed_data, latest_file)

            # Create CSV with all historical data for analysis
            csv_file = "weather_history.csv"
            success_csv = self.save_historical_csv(historical_data, csv_file)

            # Log successful run
            self.log_pipeline_run({}, success=True)

            logger.info(f"Successfully loaded weather data")
            logger.info(f"Historical records: {len(historical_data)}")
            logger.info(f"Files created: {history_file}, {latest_file}, {csv_file}")

            return True

        except Exception as e:
            error_msg = f"Error in data loading: {e}"
            logger.error(error_msg)

            # Log failed run
            self.log_pipeline_run({}, success=False, error_msg=str(e))

            return False
    
    def save_historical_csv(self, historical_data, filename):
        """Save historical data as CSV for analysis."""
        try:
            # Flatten the data for CSV
            rows = []
            for entry in historical_data:
                current = entry.get('current_weather', {})
                analysis = entry.get('current_analysis', {})

                row = {
                    'recorded_at': entry.get('recorded_at'),
                    'temperature': current.get('temperature'),
                    'feels_like': current.get('feels_like'),
                    'humidity': current.get('humidity'),
                    'weather_description': current.get('weather_description'),
                    'comfort_index': analysis.get('comfort_index'),
                    'wind_description': analysis.get('wind_description'),
                    'precipitation_status': analysis.get('precipitation_status')
                }
                rows.append(row)

            # Save as CSV
            filepath = os.path.join(self.data_dir, filename)
            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False, encoding='utf-8')
            logger.info(f"Saved historical CSV to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving historical CSV: {e}")
            return False

    def get_latest_data(self):
        """Get the most recent data."""
        return self.load_from_json('weather_latest.json')

    def get_historical_data(self):
        """Get all historical data."""
        return self.load_from_json('weather_history.json')


def main():
    """Example usage of the loader."""
    # Example processed data
    sample_data = [
        {
            'video_id': 'sample123',
            'title': 'Sample Video',
            'description': 'Sample description',
            'published_at': '2023-01-01T00:00:00Z',
            'view_count': '1000',
            'like_count': '100',
            'comment_count': '10',
            'transcript': 'This is a sample transcript...',
            'embeddings': {
                'title': [0.1, 0.2, 0.3],
                'transcript': [0.4, 0.5, 0.6],
                'combined': [0.7, 0.8, 0.9]
            },
            'transformed_at': datetime.now().isoformat()
        }
    ]
    
    try:
        loader = DataLoader()
        success = loader.load_data(sample_data)
        
        if success:
            print("Data loaded successfully")
            stats = loader.get_summary_stats()
            print("Summary stats:", stats)
        else:
            print("Failed to load data")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
