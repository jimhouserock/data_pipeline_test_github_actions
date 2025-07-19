"""
Extract module for weather data pipeline.
Handles fetching weather data from Open-Meteo API for Toronto, Canada.
"""

import requests
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherExtractor:
    """Extracts weather data from Open-Meteo API."""

    def __init__(self):
        """Initialize weather extractor for Toronto, Canada."""
        # Toronto coordinates
        self.latitude = 43.6532
        self.longitude = -79.3832
        self.city_name = "Toronto"
        self.country = "Canada"

        # Open-Meteo API base URL (no API key required!)
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(self):
        """Get current weather data for Toronto."""
        try:
            logger.info(f"Fetching current weather for {self.city_name}, {self.country}")

            # Parameters for current weather
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'current': [
                    'temperature_2m',
                    'relative_humidity_2m',
                    'apparent_temperature',
                    'precipitation',
                    'weather_code',
                    'wind_speed_10m',
                    'wind_direction_10m'
                ],
                'timezone': 'America/Toronto'
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            current = data.get('current', {})

            # Format current weather data
            weather_data = {
                'timestamp': current.get('time'),
                'city': self.city_name,
                'country': self.country,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'temperature': current.get('temperature_2m'),
                'feels_like': current.get('apparent_temperature'),
                'humidity': current.get('relative_humidity_2m'),
                'precipitation': current.get('precipitation'),
                'weather_code': current.get('weather_code'),
                'wind_speed': current.get('wind_speed_10m'),
                'wind_direction': current.get('wind_direction_10m'),
                'extracted_at': datetime.now().isoformat()
            }

            logger.info(f"Successfully fetched current weather: {weather_data['temperature']}°C")
            return weather_data

        except Exception as e:
            logger.error(f"Error fetching current weather: {e}")
            return None

    def get_forecast_data(self, days=7):
        """Get forecast data for the next few days."""
        try:
            logger.info(f"Fetching {days}-day forecast for {self.city_name}")

            # Parameters for daily forecast
            params = {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'daily': [
                    'temperature_2m_max',
                    'temperature_2m_min',
                    'precipitation_sum',
                    'weather_code',
                    'wind_speed_10m_max',
                    'wind_direction_10m_dominant'
                ],
                'timezone': 'America/Toronto',
                'forecast_days': days
            }

            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            daily = data.get('daily', {})

            # Format forecast data
            forecast_data = []
            dates = daily.get('time', [])

            for i, date in enumerate(dates):
                day_data = {
                    'date': date,
                    'city': self.city_name,
                    'country': self.country,
                    'temp_max': daily.get('temperature_2m_max', [])[i] if i < len(daily.get('temperature_2m_max', [])) else None,
                    'temp_min': daily.get('temperature_2m_min', [])[i] if i < len(daily.get('temperature_2m_min', [])) else None,
                    'precipitation': daily.get('precipitation_sum', [])[i] if i < len(daily.get('precipitation_sum', [])) else None,
                    'weather_code': daily.get('weather_code', [])[i] if i < len(daily.get('weather_code', [])) else None,
                    'wind_speed_max': daily.get('wind_speed_10m_max', [])[i] if i < len(daily.get('wind_speed_10m_max', [])) else None,
                    'wind_direction': daily.get('wind_direction_10m_dominant', [])[i] if i < len(daily.get('wind_direction_10m_dominant', [])) else None,
                    'extracted_at': datetime.now().isoformat()
                }
                forecast_data.append(day_data)

            logger.info(f"Successfully fetched {len(forecast_data)} days of forecast")
            return forecast_data

        except Exception as e:
            logger.error(f"Error fetching forecast data: {e}")
            return []

    def extract_data(self):
        """Main extraction method - gets current weather and forecast."""
        try:
            logger.info("Starting weather data extraction for Toronto")

            # Get current weather
            current_weather = self.get_current_weather()

            # Get forecast data
            forecast_data = self.get_forecast_data(days=7)

            # Combine all data
            weather_data = {
                'current': current_weather,
                'forecast': forecast_data,
                'location': {
                    'city': self.city_name,
                    'country': self.country,
                    'latitude': self.latitude,
                    'longitude': self.longitude
                },
                'extraction_summary': {
                    'timestamp': datetime.now().isoformat(),
                    'current_available': current_weather is not None,
                    'forecast_days': len(forecast_data),
                    'source': 'Open-Meteo API'
                }
            }

            logger.info(f"Successfully extracted weather data: current + {len(forecast_data)} forecast days")
            return weather_data

        except Exception as e:
            logger.error(f"Error in weather data extraction: {e}")
            return None


def get_weather_code_description(code):
    """Convert weather code to human readable description."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
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


def main():
    """Example usage of the weather extractor."""
    try:
        extractor = WeatherExtractor()
        data = extractor.extract_data()

        if data:
            print(f"✅ Weather data extracted for {data['location']['city']}")

            # Show current weather
            current = data.get('current')
            if current:
                print(f"Current: {current['temperature']}°C, {get_weather_code_description(current['weather_code'])}")

            # Show forecast summary
            forecast = data.get('forecast', [])
            print(f"Forecast: {len(forecast)} days available")

        else:
            print("❌ No weather data extracted")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
