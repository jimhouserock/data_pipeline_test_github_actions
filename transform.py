"""
Transform module for weather data pipeline.
Handles weather data analysis and trend calculation.
"""

import json
import logging
from datetime import datetime, timedelta
import statistics

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherTransformer:
    """Transforms raw weather data by adding analysis and trends."""

    def __init__(self):
        """Initialize weather transformer."""
        pass

    def get_weather_code_description(self, code):
        """Convert weather code to human readable description."""
        weather_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, f"Unknown weather code: {code}")

    def analyze_current_weather(self, current_data):
        """Analyze current weather conditions."""
        if not current_data:
            return None

        try:
            analysis = {
                'temperature_celsius': current_data.get('temperature'),
                'temperature_fahrenheit': round((current_data.get('temperature', 0) * 9/5) + 32, 1),
                'feels_like_celsius': current_data.get('feels_like'),
                'feels_like_fahrenheit': round((current_data.get('feels_like', 0) * 9/5) + 32, 1),
                'humidity_level': self._categorize_humidity(current_data.get('humidity')),
                'weather_description': self.get_weather_code_description(current_data.get('weather_code')),
                'wind_description': self._describe_wind(current_data.get('wind_speed')),
                'comfort_index': self._calculate_comfort_index(
                    current_data.get('temperature'),
                    current_data.get('humidity')
                ),
                'precipitation_status': 'Yes' if current_data.get('precipitation', 0) > 0 else 'No'
            }

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing current weather: {e}")
            return None

    def analyze_forecast_trends(self, forecast_data):
        """Analyze trends in the forecast data."""
        if not forecast_data or len(forecast_data) < 2:
            return None

        try:
            # Extract temperature data
            max_temps = [day.get('temp_max') for day in forecast_data if day.get('temp_max') is not None]
            min_temps = [day.get('temp_min') for day in forecast_data if day.get('temp_min') is not None]
            precipitation = [day.get('precipitation', 0) for day in forecast_data]

            if not max_temps or not min_temps:
                return None

            trends = {
                'temperature_trend': self._calculate_temperature_trend(max_temps),
                'temperature_range': {
                    'highest': max(max_temps),
                    'lowest': min(min_temps),
                    'average_high': round(statistics.mean(max_temps), 1),
                    'average_low': round(statistics.mean(min_temps), 1)
                },
                'precipitation_forecast': {
                    'total_expected': round(sum(precipitation), 1),
                    'rainy_days': sum(1 for p in precipitation if p > 0),
                    'heaviest_day': max(precipitation) if precipitation else 0
                },
                'weather_summary': self._generate_week_summary(forecast_data),
                'alerts': self._generate_weather_alerts(forecast_data)
            }

            return trends

        except Exception as e:
            logger.error(f"Error analyzing forecast trends: {e}")
            return None

    def _categorize_humidity(self, humidity):
        """Categorize humidity level."""
        if humidity is None:
            return "Unknown"
        elif humidity < 30:
            return "Low (Dry)"
        elif humidity < 60:
            return "Comfortable"
        elif humidity < 80:
            return "High"
        else:
            return "Very High (Humid)"

    def _describe_wind(self, wind_speed):
        """Describe wind conditions."""
        if wind_speed is None:
            return "Unknown"
        elif wind_speed < 5:
            return "Calm"
        elif wind_speed < 15:
            return "Light breeze"
        elif wind_speed < 25:
            return "Moderate wind"
        elif wind_speed < 35:
            return "Strong wind"
        else:
            return "Very strong wind"

    def _calculate_comfort_index(self, temp, humidity):
        """Calculate a simple comfort index."""
        if temp is None or humidity is None:
            return "Unknown"

        # Simple comfort calculation
        if 18 <= temp <= 24 and 40 <= humidity <= 60:
            return "Very Comfortable"
        elif 15 <= temp <= 27 and 30 <= humidity <= 70:
            return "Comfortable"
        elif 10 <= temp <= 30:
            return "Acceptable"
        else:
            return "Uncomfortable"

    def _calculate_temperature_trend(self, temperatures):
        """Calculate if temperatures are trending up, down, or stable."""
        if len(temperatures) < 3:
            return "Insufficient data"

        # Simple trend calculation
        first_half = temperatures[:len(temperatures)//2]
        second_half = temperatures[len(temperatures)//2:]

        avg_first = statistics.mean(first_half)
        avg_second = statistics.mean(second_half)

        diff = avg_second - avg_first

        if diff > 2:
            return "Warming trend"
        elif diff < -2:
            return "Cooling trend"
        else:
            return "Stable"

    def _generate_week_summary(self, forecast_data):
        """Generate a summary of the week's weather."""
        if not forecast_data:
            return "No forecast data available"

        weather_codes = [day.get('weather_code') for day in forecast_data if day.get('weather_code') is not None]

        # Count weather types
        clear_days = sum(1 for code in weather_codes if code in [0, 1])
        cloudy_days = sum(1 for code in weather_codes if code in [2, 3])
        rainy_days = sum(1 for code in weather_codes if code in range(51, 82))
        snowy_days = sum(1 for code in weather_codes if code in range(71, 87))

        summary_parts = []
        if clear_days > 0:
            summary_parts.append(f"{clear_days} clear day{'s' if clear_days > 1 else ''}")
        if cloudy_days > 0:
            summary_parts.append(f"{cloudy_days} cloudy day{'s' if cloudy_days > 1 else ''}")
        if rainy_days > 0:
            summary_parts.append(f"{rainy_days} rainy day{'s' if rainy_days > 1 else ''}")
        if snowy_days > 0:
            summary_parts.append(f"{snowy_days} snowy day{'s' if snowy_days > 1 else ''}")

        return ", ".join(summary_parts) if summary_parts else "Mixed conditions"

    def _generate_weather_alerts(self, forecast_data):
        """Generate weather alerts based on forecast."""
        alerts = []

        for day in forecast_data:
            temp_max = day.get('temp_max')
            temp_min = day.get('temp_min')
            precipitation = day.get('precipitation', 0)
            weather_code = day.get('weather_code')

            # Temperature alerts
            if temp_max and temp_max > 30:
                alerts.append(f"Hot weather expected on {day.get('date')}: {temp_max}°C")
            if temp_min and temp_min < -10:
                alerts.append(f"Very cold weather expected on {day.get('date')}: {temp_min}°C")

            # Precipitation alerts
            if precipitation > 10:
                alerts.append(f"Heavy precipitation expected on {day.get('date')}: {precipitation}mm")

            # Severe weather alerts
            if weather_code and weather_code >= 95:
                alerts.append(f"Thunderstorm possible on {day.get('date')}")

        return alerts if alerts else ["No weather alerts"]

    def transform_data(self, weather_data):
        """Main transformation method for weather data."""
        try:
            logger.info("Starting weather data transformation")

            if not weather_data:
                logger.warning("No weather data to transform")
                return None

            # Analyze current weather
            current_analysis = None
            if weather_data.get('current'):
                current_analysis = self.analyze_current_weather(weather_data['current'])

            # Analyze forecast trends
            forecast_analysis = None
            if weather_data.get('forecast'):
                forecast_analysis = self.analyze_forecast_trends(weather_data['forecast'])

            # Create transformed data structure
            transformed_data = {
                'location': weather_data.get('location'),
                'extraction_info': weather_data.get('extraction_summary'),
                'current_weather': weather_data.get('current'),
                'current_analysis': current_analysis,
                'forecast_data': weather_data.get('forecast'),
                'forecast_analysis': forecast_analysis,
                'transformation_timestamp': datetime.now().isoformat(),
                'data_quality': {
                    'current_available': current_analysis is not None,
                    'forecast_available': forecast_analysis is not None,
                    'forecast_days': len(weather_data.get('forecast', [])),
                    'completeness': 'Good' if current_analysis and forecast_analysis else 'Partial'
                }
            }

            logger.info("Weather data transformation completed successfully")
            return transformed_data

        except Exception as e:
            logger.error(f"Error in weather data transformation: {e}")
            return None


def main():
    """Example usage of the weather transformer."""
    # Example weather data (would come from extract.py)
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

    try:
        transformer = WeatherTransformer()
        transformed_data = transformer.transform_data(sample_data)

        if transformed_data:
            print("✅ Weather data transformed successfully")
            print(f"Current analysis available: {transformed_data['current_analysis'] is not None}")
            print(f"Forecast analysis available: {transformed_data['forecast_analysis'] is not None}")
        else:
            print("❌ No data transformed")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
