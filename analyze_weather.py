#!/usr/bin/env python3
"""
Simple weather data analysis examples.
Shows what you can do with the generated weather data.
"""

import json
import pandas as pd
from datetime import datetime

def load_weather_data():
    """Load the latest weather data."""
    try:
        with open('data/weather_latest.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ No weather data found. Run the pipeline first!")
        return None

def load_historical_data():
    """Load historical weather data."""
    try:
        with open('data/weather_history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ No historical data found. Run the pipeline a few times first!")
        return None

def show_current_weather(data):
    """Display current weather conditions."""
    current = data.get('current_weather', {})
    analysis = data.get('current_analysis', {})
    
    print("🌤️ CURRENT WEATHER IN TORONTO")
    print("=" * 40)
    print(f"Temperature: {current.get('temperature', 'N/A')}°C")
    print(f"Feels like: {current.get('feels_like', 'N/A')}°C")
    print(f"Humidity: {current.get('humidity', 'N/A')}%")
    print(f"Conditions: {current.get('weather_description', 'N/A')}")
    print(f"Comfort: {analysis.get('comfort_index', 'N/A')}")
    print()

def show_forecast_summary(data):
    """Display forecast summary."""
    forecast_analysis = data.get('forecast_analysis', {})
    
    print("📅 7-DAY FORECAST SUMMARY")
    print("=" * 40)
    print(f"Trend: {forecast_analysis.get('temperature_trend', 'N/A')}")
    print(f"Summary: {forecast_analysis.get('weather_summary', 'N/A')}")
    
    alerts = forecast_analysis.get('alerts', [])
    if alerts:
        print("\n⚠️ WEATHER ALERTS:")
        for alert in alerts:
            print(f"  • {alert}")
    print()

def analyze_temperature_range(data):
    """Analyze temperature ranges."""
    forecast = data.get('forecast_data', [])
    if not forecast:
        print("No forecast data available")
        return
    
    temps = []
    for day in forecast:
        if day.get('temperature_max') and day.get('temperature_min'):
            temps.append({
                'date': day.get('date'),
                'high': day.get('temperature_max'),
                'low': day.get('temperature_min')
            })
    
    if temps:
        print("🌡️ TEMPERATURE ANALYSIS")
        print("=" * 40)
        highs = [t['high'] for t in temps]
        lows = [t['low'] for t in temps]
        
        print(f"Highest temp this week: {max(highs)}°C")
        print(f"Lowest temp this week: {min(lows)}°C")
        print(f"Average high: {sum(highs)/len(highs):.1f}°C")
        print(f"Average low: {sum(lows)/len(lows):.1f}°C")
        print()

def export_for_excel(data):
    """Create a simple CSV for Excel analysis."""
    forecast = data.get('forecast_data', [])
    if not forecast:
        print("No forecast data to export")
        return
    
    # Create simple table
    rows = []
    for day in forecast:
        rows.append({
            'Date': day.get('date'),
            'High_Temp': day.get('temperature_max'),
            'Low_Temp': day.get('temperature_min'),
            'Precipitation': day.get('precipitation_sum', 0),
            'Weather': day.get('weather_description', '')
        })
    
    df = pd.DataFrame(rows)
    df.to_csv('data/weather_analysis.csv', index=False)
    print("📊 Exported weather_analysis.csv for Excel!")
    print("   Open this file in Excel to create charts")
    print()

def main():
    """Main analysis function."""
    print("🌤️ TORONTO WEATHER DATA ANALYSIS")
    print("=" * 50)
    
    # Load data
    data = load_weather_data()
    if not data:
        return
    
    # Show current conditions
    show_current_weather(data)
    
    # Show forecast summary
    show_forecast_summary(data)
    
    # Analyze temperatures
    analyze_temperature_range(data)
    
    # Export for Excel
    export_for_excel(data)
    
    print("💡 WHAT YOU CAN DO NEXT:")
    print("=" * 50)
    print("1. Open weather_analysis.csv in Excel")
    print("2. Create temperature trend charts")
    print("3. Track weather patterns over time")
    print("4. Build a weather dashboard")
    print("5. Set up weather alerts")

if __name__ == "__main__":
    main()
