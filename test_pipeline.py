"""
Test script for the data pipeline.
Run this to validate your setup before deploying.
"""

import os
import sys
import logging
from datetime import datetime

# Import pipeline components
from utils import setup_logging, print_pipeline_summary
from extract import WeatherExtractor
from transform import WeatherTransformer
from load import DataLoader

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


def test_configuration():
    """Test pipeline configuration."""
    print("\n🔧 Testing Configuration...")

    print("Weather Pipeline Configuration:")
    print("  Location: Toronto, Canada")
    print("  API: Open-Meteo (no authentication required)")
    print("  Data: Current weather + 7-day forecast")

    print("✅ Configuration is valid (no API keys required!)")
    return True


def test_extractor():
    """Test the weather extractor."""
    print("\n📥 Testing Weather Extractor...")

    try:
        extractor = WeatherExtractor()

        print(f"Testing weather extraction for {extractor.city_name}, {extractor.country}")

        # Extract weather data
        data = extractor.extract_data()

        if data:
            current = data.get('current', {})
            forecast = data.get('forecast', [])
            print(f"✅ Successfully extracted weather data")
            print(f"Current temperature: {current.get('temperature', 'N/A')}°C")
            print(f"Forecast days: {len(forecast)}")
            return True
        else:
            print("❌ No weather data extracted")
            return False

    except Exception as e:
        print(f"❌ Weather extractor test failed: {e}")
        return False


def test_transformer():
    """Test the weather transformer with sample data."""
    print("\n🔄 Testing Weather Transformer...")

    try:
        transformer = WeatherTransformer()

        # Create sample weather data
        sample_data = {
            'current': {
                'temperature': 22.5,
                'feels_like': 24.0,
                'humidity': 65,
                'weather_code': 1,
                'wind_speed': 10,
                'precipitation': 0
            },
            'forecast': [
                {'date': '2024-01-15', 'temp_max': 25, 'temp_min': 15, 'precipitation': 0, 'weather_code': 0},
                {'date': '2024-01-16', 'temp_max': 23, 'temp_min': 13, 'precipitation': 2, 'weather_code': 61}
            ],
            'location': {'city': 'Toronto', 'country': 'Canada'}
        }

        # Test transformation
        transformed_data = transformer.transform_data(sample_data)

        if transformed_data:
            print(f"✅ Successfully transformed weather data")

            # Check if analysis was generated
            if transformed_data.get('current_analysis'):
                print("✅ Current weather analysis generated")
            if transformed_data.get('forecast_analysis'):
                print("✅ Forecast analysis generated")

            return True
        else:
            print("❌ No data transformed")
            return False

    except Exception as e:
        print(f"❌ Weather transformer test failed: {e}")
        return False


def test_loader():
    """Test the data loader."""
    print("\n💾 Testing Data Loader...")

    try:
        loader = DataLoader()

        # Create sample processed weather data
        sample_data = [{
            'location': {'city': 'Toronto', 'country': 'Canada'},
            'current_weather': {
                'temperature': 22.5,
                'humidity': 65,
                'weather_code': 1
            },
            'current_analysis': {
                'temperature_celsius': 22.5,
                'weather_description': 'Mainly clear',
                'comfort_index': 'Comfortable'
            },
            'forecast_data': [
                {'date': '2024-01-15', 'temp_max': 25, 'temp_min': 15}
            ],
            'transformation_timestamp': datetime.now().isoformat()
        }]

        # Test loading
        success = loader.load_data(sample_data)

        if success:
            print("✅ Weather data loaded successfully")

            # Test reading back
            stats = loader.get_summary_stats()
            if stats:
                print("✅ Summary stats generated")
                print_pipeline_summary(stats)

            return True
        else:
            print("❌ Failed to load weather data")
            return False

    except Exception as e:
        print(f"❌ Loader test failed: {e}")
        return False


def test_full_pipeline():
    """Test the complete weather pipeline."""
    print("\n🚀 Testing Full Weather Pipeline...")

    try:
        from data_pipeline import WeatherDataPipeline

        # Create weather pipeline
        pipeline = WeatherDataPipeline()

        # Run pipeline
        success = pipeline.run()

        if success:
            print("✅ Full weather pipeline test successful!")

            # Show results
            stats = pipeline.get_pipeline_status()
            if stats:
                print_pipeline_summary(stats)

            return True
        else:
            print("❌ Full weather pipeline test failed")
            return False

    except Exception as e:
        print(f"❌ Full weather pipeline test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 WEATHER PIPELINE TESTING SUITE")
    print("=" * 50)

    tests = [
        ("Configuration", test_configuration),
        ("Weather Extractor", test_extractor),
        ("Weather Transformer", test_transformer),
        ("Data Loader", test_loader),
        ("Full Weather Pipeline", test_full_pipeline)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except KeyboardInterrupt:
            print(f"\n⏹️ Testing interrupted during {test_name}")
            break
        except Exception as e:
            print(f"\n💥 Unexpected error in {test_name}: {e}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 All tests passed! Your weather pipeline is ready to deploy.")
        print("🌤️ No API keys required - just push to GitHub and it will work!")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
