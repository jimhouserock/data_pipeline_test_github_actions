"""
Main weather data pipeline orchestrator.
Coordinates the ETL process: Extract -> Transform -> Load
"""

import os
import sys
import logging
from datetime import datetime

# Import our ETL modules
from extract import WeatherExtractor
from transform import WeatherTransformer
from load import DataLoader

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WeatherDataPipeline:
    """Main weather pipeline orchestrator."""

    def __init__(self):
        """Initialize pipeline with configuration."""
        # Initialize ETL components
        self.extractor = WeatherExtractor()
        self.transformer = WeatherTransformer()
        self.loader = DataLoader()

        logger.info("Weather data pipeline initialized for Toronto, Canada")

    def run(self):
        """Execute the complete weather ETL pipeline."""
        try:
            logger.info("=" * 60)
            logger.info("STARTING WEATHER DATA PIPELINE FOR TORONTO")
            logger.info("=" * 60)

            start_time = datetime.now()

            # Step 1: Extract
            logger.info("Step 1: EXTRACTING weather data from Open-Meteo API")
            raw_data = self.extract_data()

            if not raw_data:
                logger.error("No weather data extracted. Pipeline stopped.")
                return False

            # Step 2: Transform
            logger.info("Step 2: TRANSFORMING weather data (analysis + trends)")
            processed_data = self.transform_data(raw_data)

            if not processed_data:
                logger.error("No data transformed. Pipeline stopped.")
                return False

            # Step 3: Load
            logger.info("Step 3: LOADING weather data to storage")
            success = self.load_data(processed_data)

            if not success:
                logger.error("Failed to load data. Pipeline failed.")
                return False

            # Pipeline completed successfully
            end_time = datetime.now()
            duration = end_time - start_time

            logger.info("=" * 60)
            logger.info("WEATHER PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"Duration: {duration}")
            logger.info(f"Location: {processed_data.get('location', {}).get('city', 'Unknown')}")
            logger.info(f"Current temp: {processed_data.get('current_weather', {}).get('temperature', 'N/A')}°C")
            logger.info(f"Forecast days: {len(processed_data.get('forecast_data', []))}")
            logger.info("=" * 60)

            return True

        except Exception as e:
            logger.error(f"Weather pipeline failed with error: {e}")
            return False

    def extract_data(self):
        """Extract weather data using the extractor."""
        try:
            data = self.extractor.extract_data()

            if data:
                current = data.get('current', {})
                forecast = data.get('forecast', [])
                logger.info(f"Extracted weather data: current + {len(forecast)} forecast days")

                # Log current conditions
                if current.get('temperature') is not None:
                    logger.info(f"Current conditions: {current['temperature']}°C")

            return data

        except Exception as e:
            logger.error(f"Error in weather data extraction: {e}")
            return None

    def transform_data(self, raw_data):
        """Transform weather data using the transformer."""
        try:
            processed_data = self.transformer.transform_data(raw_data)
            if processed_data:
                logger.info("Weather data transformed successfully")
            return processed_data

        except Exception as e:
            logger.error(f"Error in weather data transformation: {e}")
            return None

    def load_data(self, processed_data):
        """Load weather data using the loader."""
        try:
            # Pass processed data directly to loader
            success = self.loader.load_data(processed_data)
            if success:
                logger.info("Weather data loaded successfully")
            return success

        except Exception as e:
            logger.error(f"Error in loading weather data: {e}")
            return False

    def get_pipeline_status(self):
        """Get status of the last pipeline run."""
        try:
            stats = self.loader.get_summary_stats()
            return stats
        except Exception as e:
            logger.error(f"Error getting pipeline status: {e}")
            return None


def main():
    """Main entry point for the weather pipeline."""
    try:
        logger.info("Weather Data Pipeline for Toronto, Canada")
        logger.info("Using Open-Meteo API (no authentication required)")

        # Create and run pipeline
        pipeline = WeatherDataPipeline()

        success = pipeline.run()

        if success:
            logger.info("Weather pipeline completed successfully!")

            # Print summary
            stats = pipeline.get_pipeline_status()
            if stats:
                logger.info("Pipeline Summary:")
                logger.info(f"  Data entries: {stats.get('total_videos', 0)}")  # Reusing video field name
                logger.info(f"  Generated at: {stats.get('generated_at', 'N/A')}")

            sys.exit(0)
        else:
            logger.error("Weather pipeline failed!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
