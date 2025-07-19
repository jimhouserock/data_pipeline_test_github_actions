# 🌤️ Simple Weather Data Pipeline

**Test GitHub Actions with Toronto weather data - no API keys needed!**

## 🚀 Quick Start

1. **Fork this repo**
2. **Done!** GitHub Actions runs automatically

## What it does

- Gets Toronto weather data every day
- Saves to `data/` folder
- No setup required

## GitHub Actions Setup

**No credentials needed!** GitHub provides `GITHUB_TOKEN` automatically.

### Test Schedule (Currently Active)
- Runs every 5 minutes for testing
- Check "Actions" tab to see it working

### Switch to Daily Schedule
```bash
python schedule_helper.py daily
git add .
git commit -m "daily schedule"
git push
```

## Local Testing

```bash
git clone https://github.com/jimhouserock/simple_data_pipeline.git
cd simple_data_pipeline
pip install -r requirements.txt
python data_pipeline.py
```

## Files Generated

- `data/weather_data.json` - Weather data
- `data/weather_data.csv` - Same data in CSV format

That's it! Simple GitHub Actions testing with real weather data.
