# Setup Guide for Simple Weather Data Pipeline

This guide will walk you through setting up the automated weather data pipeline based on the Full Stack Data Science video series concepts, but simplified with no API keys required!

## Prerequisites

- Python 3.9 or higher
- Git
- GitHub account
- ✅ **No API keys needed!**
- ✅ **No external accounts required!**

## Step 1: No API Setup Required! 🎉

**This is the best part - there's literally nothing to set up!**

The pipeline uses the **Open-Meteo API** which:
- ✅ Requires no registration
- ✅ Requires no API key
- ✅ Has no rate limits for basic usage
- ✅ Provides high-quality weather data
- ✅ Works immediately out of the box

**You can skip directly to Step 2!**

## Step 2: GitHub Repository Setup

### 2.1 Create Repository
1. Create a new GitHub repository
2. Clone this code to your repository
3. Push the initial code

### 2.2 Set Up Repository Secrets
1. Go to your GitHub repository
2. Click "Settings" > "Secrets and variables" > "Actions"
3. Add the following repository secrets:

#### Required Secrets:
- `YOUTUBE_API_KEY`: Your YouTube Data API key from Step 1.3
- `GITHUB_TOKEN`: Personal access token (see Step 2.3)

#### Optional Secrets:
- `YOUTUBE_CHANNEL_ID`: Specific channel ID to process (if not set, uses default)
- `MAX_VIDEOS`: Maximum number of videos to process (default: 25)

### 2.3 Create GitHub Personal Access Token
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Data Pipeline Bot"
4. Set expiration (30 days minimum)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
6. Generate token and copy it
7. Add as `GITHUB_TOKEN` secret in your repository

## Step 3: Local Development Setup

### 3.1 Clone Repository
```bash
git clone https://github.com/yourusername/simple_pipeline.git
cd simple_pipeline
```

### 3.2 Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.4 Set Environment Variables
Create a `.env` file in the project root:
```bash
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_CHANNEL_ID=your_channel_id_here
MAX_VIDEOS=25
```

**Note**: Never commit the `.env` file to Git!

## Step 4: Testing the Pipeline

### 4.1 Run Test Suite
```bash
python test_pipeline.py
```

This will test all components and validate your setup.

### 4.2 Run Pipeline Locally
```bash
python data_pipeline.py
```

Check the `data/` folder for output files.

## Step 5: Deploy to GitHub Actions

### 5.1 Push to GitHub
```bash
git add .
git commit -m "Initial pipeline setup"
git push origin main
```

### 5.2 Verify GitHub Actions
1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see the workflow running

### 5.3 Manual Trigger
1. In the Actions tab, click "Data Pipeline Workflow"
2. Click "Run workflow" to trigger manually

## Step 6: Monitor and Maintain

### 6.1 Check Workflow Runs
- Monitor the Actions tab for successful/failed runs
- Check logs for any errors

### 6.2 Review Output Data
- Check the `data/` folder in your repository
- Review `summary_stats.json` for pipeline metrics
- Monitor `pipeline_log.json` for execution history

### 6.3 Scheduled Execution
The pipeline runs automatically daily at 12:35 AM UTC. You can modify the schedule in `.github/workflows/data_pipeline.yml`.

## Troubleshooting

### Common Issues

#### 1. "YouTube API key is required" Error
- Ensure `YOUTUBE_API_KEY` is set in repository secrets
- Verify the API key is valid and has YouTube Data API v3 enabled

#### 2. "Permission denied" Git Errors
- Check that `GITHUB_TOKEN` secret is set correctly
- Ensure the token has `repo` scope permissions

#### 3. "No data extracted" Warning
- Verify the channel ID is correct
- Check if the channel has public videos
- Ensure API quotas aren't exceeded

#### 4. Transcript Errors
- Many videos don't have transcripts available
- This is normal and won't break the pipeline
- Videos without transcripts will still have title embeddings

#### 5. Memory/Timeout Issues
- Reduce `MAX_VIDEOS` if processing too many videos
- Consider upgrading to paid GitHub Actions for longer run times

### Getting Help

1. Check the logs in GitHub Actions for detailed error messages
2. Run `python test_pipeline.py` locally to debug issues
3. Review the video tutorial for additional context
4. Check GitHub Issues for common problems

## Next Steps

Once your pipeline is running successfully:

1. **Customize the data processing** for your specific use case
2. **Add data validation** and quality checks
3. **Connect to a database** instead of file storage for larger datasets
4. **Build a search interface** using the generated embeddings
5. **Add monitoring and alerting** for production use

## Security Notes

- Never commit API keys or secrets to Git
- Use repository secrets for sensitive data
- Regularly rotate API keys and tokens
- Monitor API usage to avoid unexpected charges

## Cost Considerations

- YouTube Data API has free quotas with limits
- GitHub Actions has free minutes with limits
- Monitor usage to avoid unexpected charges
- Consider upgrading plans for heavy usage

---

**Congratulations!** 🎉 You now have a fully automated data pipeline that processes YouTube videos, extracts transcripts, generates embeddings, and runs on a schedule!
