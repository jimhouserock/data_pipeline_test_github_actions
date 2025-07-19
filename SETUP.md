# 🌤️ Setup Guide for Simple Weather Data Pipeline

**Get Toronto weather data automatically - no API keys, no setup, just works!**

This guide shows you how to deploy an automated weather data pipeline that runs daily and requires zero configuration.

## 🎯 **Quick Start (30 seconds)**

1. **Fork this repository** (click Fork button above)
2. **That's it!** GitHub Actions will start running automatically
3. **Check the Actions tab** to see your pipeline working
4. **Weather data appears** in the `data/` folder daily

## 📋 **Prerequisites**

- ✅ GitHub account (free)
- ✅ **That's literally it!**

**No API keys, no external accounts, no complex setup required!**

## 🚀 **Deployment Options**

### **Option 1: Fork and Go (Recommended)**
Perfect for most users - just fork and it works!

1. Click **"Fork"** button at the top of this repository
2. GitHub Actions automatically starts running
3. Check **"Actions"** tab to see your pipeline working
4. Weather data appears in **`data/`** folder within minutes

### **Option 2: Clone for Local Development**
For developers who want to modify the code:

```bash
git clone https://github.com/jimhouserock/simple_data_pipeline.git
cd simple_data_pipeline
pip install -r requirements.txt
python data_pipeline.py
```

### **Option 3: Create Your Own Repository**
To start fresh with your own repo:

1. Create new GitHub repository
2. Clone this code to your repository
3. Push to your repo
4. GitHub Actions will start automatically

## 🔧 **No Configuration Required!**

**The pipeline uses Open-Meteo API which requires:**
- ❌ No API keys
- ❌ No registration
- ❌ No secrets or tokens
- ❌ No external accounts
- ✅ **Just works immediately!**

**GitHub provides the `GITHUB_TOKEN` automatically - no manual setup needed!**

## 🧪 **Testing Your Pipeline**

### **Test Locally (Optional)**
```bash
# Clone the repository
git clone https://github.com/jimhouserock/simple_data_pipeline.git
cd simple_data_pipeline

# Install dependencies
pip install -r requirements.txt

# Run full test suite
python test_pipeline.py

# Run pipeline once
python data_pipeline.py

# Check generated data
ls data/
```

### **Test on GitHub**
1. Go to your forked repository
2. Click **"Actions"** tab
3. Click **"Weather Data Pipeline Workflow"**
4. Click **"Run workflow"** → **"Run workflow"**
5. Watch it run in real-time!

### **Verify It's Working**
✅ Check **Actions** tab shows green checkmarks
✅ Check **`data/`** folder has new files
✅ Check **commit history** shows automatic updates
✅ Check **files** contain Toronto weather data

## ⏰ **Pipeline Schedule**

### **Default Schedule**
- **Daily**: 12:35 AM UTC (7:35 AM Toronto time)
- **Manual**: Anytime via GitHub Actions
- **On Push**: When you update code

### **Test with Frequent Runs**
To test scheduling, temporarily change the schedule to run every 5 minutes:

1. Edit `.github/workflows/data_pipeline.yml`
2. Change the cron line:
```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
```
3. Commit and push the change
4. Watch it run every 5 minutes in Actions tab
5. **Remember to change it back** to daily schedule:
```yaml
schedule:
  - cron: '35 0 * * *'  # Daily at 12:35 AM UTC
```

### **Monitor Pipeline**
- **Actions Tab**: See all runs and logs
- **Data Folder**: Check new weather files
- **Commit History**: See automatic data updates

## 📊 **Understanding the Output**

### **Generated Files**
- **`video_data.json`** - Complete weather data and analysis
- **`video_data.csv`** - Spreadsheet format for Excel
- **`summary_stats.json`** - Pipeline statistics
- **`pipeline_log.json`** - Execution history

### **Sample Weather Data**
```json
{
  "current_weather": {
    "temperature": 22.8,
    "humidity": 65,
    "weather_description": "Overcast"
  },
  "forecast_analysis": {
    "temperature_trend": "Warming trend",
    "alerts": ["Hot weather expected on 2025-07-24: 36.7°C"]
  }
}
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Pipeline Not Running**
- Check if repository is public (private repos have limited free Actions)
- Verify `.github/workflows/data_pipeline.yml` exists
- Check Actions tab for error messages

#### **2. No Data Generated**
- Pipeline might be running but not committing changes
- Check Actions logs for "No changes detected"
- Weather data might be identical to previous run

#### **3. Permission Errors**
- GitHub automatically provides `GITHUB_TOKEN`
- If issues persist, check repository settings
- Ensure Actions are enabled in repository settings

#### **4. Actions Disabled**
- Go to repository Settings → Actions → General
- Ensure "Allow all actions and reusable workflows" is selected

### **Getting Help**
1. Check **Actions** tab logs for detailed error messages
2. Run `python test_pipeline.py` locally to debug
3. Check **Issues** tab in this repository
4. Review the **README.md** for additional guidance

## 🚀 **Next Steps**

### **Extend Your Pipeline**
- **🌍 Multiple Cities**: Add Montreal, Vancouver, New York
- **📊 Visualizations**: Create weather charts and graphs
- **🗄️ Database**: Connect to PostgreSQL or MySQL
- **📧 Alerts**: Email notifications for severe weather
- **🌐 Web App**: Build a weather dashboard

### **Learn More**
- **[storage_options.md](storage_options.md)** - Database alternatives
- **[example_usage.py](example_usage.py)** - Data analysis examples
- **[Open-Meteo API](https://open-meteo.com/)** - Weather data documentation

## 💰 **Cost Information**

- **Open-Meteo API**: Completely free, no limits
- **GitHub Actions**: 2,000 free minutes/month (this uses ~1 minute/day)
- **Repository Storage**: Free for public repos
- **Total Cost**: $0 forever! 🎉

## 🎯 **Success Checklist**

✅ Repository forked or cloned
✅ Actions tab shows green checkmarks
✅ `data/` folder contains weather files
✅ Automatic commits appear in history
✅ Pipeline runs on schedule

---

**🎉 Congratulations!** You now have a fully automated weather data pipeline that collects Toronto weather data daily and requires zero maintenance!
