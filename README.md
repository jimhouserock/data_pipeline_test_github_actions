# 🌤️ Simple Weather Data Pipeline

**An automated weather data pipeline that requires ZERO API keys!**

This project demonstrates building a production-ready data pipeline using GitHub Actions, inspired by Full Stack Data Science concepts but simplified for immediate deployment.

## 🚀 **Quick Start - No Setup Required!**

1. **Fork this repository**
2. **That's it!** The pipeline will automatically start running daily

## 📊 **What This Pipeline Does**

This implements a complete ETL (Extract, Transform, Load) process:

- **🔄 Extract**: Fetches current weather + 7-day forecast for Toronto from Open-Meteo API
- **⚙️ Transform**: Analyzes trends, calculates comfort indices, generates weather alerts
- **💾 Load**: Saves processed data to multiple formats (JSON, CSV, logs)
- **🤖 Automate**: Runs daily at 7:35 AM Toronto time via GitHub Actions

**Location**: Toronto, Canada 🇨🇦

## ✨ **Why This is Better Than Complex Pipelines**

| Feature | Traditional Pipelines | This Pipeline |
|---------|----------------------|---------------|
| **Setup Time** | Hours/Days | 30 seconds |
| **API Keys** | Required | None needed |
| **Cost** | Often paid | Completely free |
| **Maintenance** | High | Zero |
| **Learning Curve** | Steep | Gentle |

## Project Structure

```
simple_pipeline/
├── .github/
│   └── workflows/
│       └── data_pipeline.yml    # GitHub Actions workflow
├── data/                        # Output data directory
├── extract.py                   # Weather data extraction script
├── transform.py                 # Weather data transformation script
├── load.py                      # Data loading script
├── data_pipeline.py             # Main orchestrator script
├── config.py                    # Configuration management
├── utils.py                     # Utility functions
├── test_pipeline.py             # Testing suite
├── example_usage.py             # Usage examples
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore file
├── README.md                    # This file
└── SETUP.md                     # Setup instructions
```

## Features

- **No API Keys Required**: Uses free Open-Meteo API with no authentication
- **Automated Scheduling**: Runs daily at 12:35 AM UTC (7:35 AM Toronto time)
- **Manual Triggers**: Can be triggered manually through GitHub UI
- **Change Detection**: Only commits new data if changes are detected
- **Weather Analysis**: Temperature trends, comfort indices, weather alerts
- **Dependency Caching**: Optimizes build times

## 🎯 **How to Use This Repository**

### **Option 1: Fork and Go (Recommended)**
1. Click "Fork" button above
2. GitHub Actions will automatically start running
3. Check the "Actions" tab to see your pipeline running
4. Weather data will appear in the `data/` folder daily

### **Option 2: Clone Locally**
```bash
git clone https://github.com/jimhouserock/simple_data_pipeline.git
cd simple_data_pipeline
pip install -r requirements.txt
python data_pipeline.py
```

### **Option 3: Test Everything**
```bash
python test_pipeline.py  # Run full test suite
python example_usage.py  # See data analysis examples
```

## 🔧 **No Setup Required!**

This pipeline uses the **Open-Meteo API** which requires:
- ❌ No API key
- ❌ No registration
- ❌ No authentication
- ❌ No billing setup
- ✅ **Just works immediately!**

The `GITHUB_TOKEN` is automatically provided by GitHub Actions - no manual setup needed!

## 📅 **Pipeline Schedule**

- **Automatic**: Runs daily at 12:35 AM UTC (7:35 AM Toronto time)
- **Manual**: Trigger anytime via GitHub Actions
- **On Push**: Runs when you push code changes

### **Manual Trigger**
1. Go to "Actions" tab in your repository
2. Select "Weather Data Pipeline Workflow"
3. Click "Run workflow" → "Run workflow"
4. Watch it execute in real-time!

### **Monitor Pipeline**
- **Actions Tab**: See all pipeline runs and logs
- **Data Folder**: Check generated weather files
- **Commit History**: See automatic data commits

## Pipeline Components

- **Extract**: Fetches current weather and 7-day forecast from Open-Meteo API
- **Transform**: Analyzes trends, calculates comfort indices, generates weather alerts
- **Load**: Saves processed data to JSON/CSV files in the data directory

## Output

The pipeline generates the following files in the `data/` directory:
- `video_data.json`: Weather data and analysis (reusing existing structure)
- `video_data.csv`: Weather data in CSV format for easy analysis
- `summary_stats.json`: Pipeline statistics and summary
- `pipeline_log.json`: Execution logs and timestamps

## 📊 **Sample Output**

The pipeline generates rich weather data and analysis for Toronto:

```json
{
  "current_weather": {
    "temperature": 22.8,
    "feels_like": 23.6,
    "humidity": 65,
    "weather_description": "Overcast"
  },
  "current_analysis": {
    "comfort_index": "Comfortable",
    "wind_description": "Light breeze",
    "precipitation_status": "No"
  },
  "forecast_analysis": {
    "temperature_trend": "Warming trend",
    "weather_summary": "4 cloudy days, 3 rainy days",
    "alerts": ["Hot weather expected on 2025-07-24: 36.7°C"]
  }
}
```

### **Generated Files**
- `📄 video_data.json` - Complete weather data and analysis
- `📊 video_data.csv` - Tabular format for Excel/analysis
- `📈 summary_stats.json` - Pipeline statistics
- `📝 pipeline_log.json` - Execution history

## 🚀 **What You'll Learn**

This pipeline teaches real-world data engineering concepts:

- **ETL Patterns**: Extract, Transform, Load best practices
- **GitHub Actions**: CI/CD and automation workflows
- **Data Processing**: JSON/CSV handling, trend analysis
- **Error Handling**: Robust pipeline design
- **Scheduling**: Cron jobs and automated execution
- **Version Control**: Data versioning with Git

## 🔧 **Extend This Pipeline**

Ready to level up? Try these enhancements:

- **🌍 Multiple Cities**: Add Montreal, Vancouver, New York
- **🗄️ Database Storage**: Connect to PostgreSQL/MySQL
- **📧 Alerts**: Email notifications for severe weather
- **📊 Visualizations**: Charts and graphs with matplotlib
- **🌐 Web Dashboard**: Flask/FastAPI weather app
- **🤖 ML Models**: Weather prediction algorithms

## 🎯 **Why This Approach Works**

✅ **Immediate Success** - No frustrating API setup
✅ **Real Data** - Actual Toronto weather, not dummy data
✅ **Production Ready** - Same patterns used in industry
✅ **Cost Effective** - Completely free to run
✅ **Scalable** - Easy to extend and modify

## 📚 **Additional Resources**

- **[SETUP.md](SETUP.md)** - Detailed setup instructions
- **[storage_options.md](storage_options.md)** - Database alternatives
- **[Open-Meteo API](https://open-meteo.com/)** - Weather data source
- **[GitHub Actions Docs](https://docs.github.com/en/actions)** - Automation guide

## 📄 **License**

MIT License - feel free to fork, modify, and use for any purpose!

---

**⭐ Star this repo if it helped you learn data pipelines!**
