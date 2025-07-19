# Data Storage Options for Weather Pipeline

## Current Setup: GitHub Repository Storage

The pipeline currently stores data directly in your GitHub repository in the `data/` folder. This works great for:
- Learning and development
- Small datasets (weather data is tiny)
- Simple deployment
- Version control of data

## Alternative Storage Options

### 1. Database Storage (Recommended for Production)

#### PostgreSQL (Free Options)
```python
# Example modification to load.py
import psycopg2
import os

class DatabaseLoader:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
    
    def save_weather_data(self, weather_data):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO weather_data (date, temperature, humidity, forecast)
            VALUES (%s, %s, %s, %s)
        """, (
            weather_data['timestamp'],
            weather_data['temperature'],
            weather_data['humidity'],
            json.dumps(weather_data['forecast'])
        ))
        self.conn.commit()
```

**Free PostgreSQL Providers:**
- **Supabase** (2 free projects, 500MB each)
- **Railway** (Free tier with limits)
- **Neon** (Free tier, 3GB storage)

#### SQLite (Simplest)
```python
import sqlite3

class SQLiteLoader:
    def __init__(self, db_path='weather.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                temperature REAL,
                humidity INTEGER,
                weather_code INTEGER,
                forecast_json TEXT
            )
        """)
```

### 2. Cloud Storage

#### AWS S3 (with GitHub Actions)
```yaml
# Add to .github/workflows/data_pipeline.yml
- name: Upload to S3
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: |
    aws s3 cp data/video_data.json s3://your-bucket/weather-data/$(date +%Y%m%d).json
```

#### Google Cloud Storage
```python
from google.cloud import storage

class GCSLoader:
    def __init__(self, bucket_name):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_weather_data(self, data, filename):
        blob = self.bucket.blob(f"weather-data/{filename}")
        blob.upload_from_string(json.dumps(data))
```

### 3. Simple APIs/Services

#### Airtable (Spreadsheet-like)
```python
import requests

class AirtableLoader:
    def __init__(self, api_key, base_id, table_name):
        self.api_key = api_key
        self.base_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    
    def save_weather_record(self, weather_data):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        record = {
            "fields": {
                "Date": weather_data['timestamp'],
                "Temperature": weather_data['temperature'],
                "Humidity": weather_data['humidity'],
                "Weather": weather_data['weather_description']
            }
        }
        
        response = requests.post(
            self.base_url,
            headers=headers,
            json={"records": [record]}
        )
```

#### Google Sheets
```python
import gspread

class GoogleSheetsLoader:
    def __init__(self, credentials_file, sheet_name):
        self.gc = gspread.service_account(filename=credentials_file)
        self.sheet = self.gc.open(sheet_name).sheet1
    
    def append_weather_data(self, weather_data):
        row = [
            weather_data['timestamp'],
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['weather_description']
        ]
        self.sheet.append_row(row)
```

## Recommendation for Your Use Case

### For Learning/Demo: Keep Repository Storage ✅
- **Pros**: Simple, works immediately, no setup
- **Cons**: Limited to small datasets
- **Perfect for**: Weather data (tiny files), learning GitHub Actions

### For Production: Use Database
- **Supabase PostgreSQL** (recommended)
  - Free tier: 500MB, 2 projects
  - Built-in API and dashboard
  - Easy to set up

### Migration Path

1. **Start**: Repository storage (current setup)
2. **Scale**: Add database storage alongside repository
3. **Production**: Move to database-only storage

## Implementation Example

To add database storage while keeping repository storage:

```python
# In load.py
class HybridLoader:
    def __init__(self):
        self.file_loader = DataLoader()  # Current file-based loader
        self.db_loader = DatabaseLoader()  # New database loader
    
    def load_data(self, processed_data):
        # Save to files (for GitHub)
        file_success = self.file_loader.load_data(processed_data)
        
        # Also save to database (for querying)
        try:
            db_success = self.db_loader.save_weather_data(processed_data[0])
        except Exception as e:
            logger.warning(f"Database save failed: {e}")
            db_success = False
        
        return file_success  # GitHub Actions still needs file changes
```

## Cost Comparison

| Storage Type | Free Tier | Cost After Free |
|--------------|-----------|-----------------|
| GitHub Repo | 1GB soft limit | Free (public repos) |
| Supabase | 500MB, 2 projects | $25/month |
| AWS S3 | 5GB, 12 months | ~$0.023/GB/month |
| Google Sheets | 15GB Google Drive | $6/month (100GB) |
| SQLite File | Unlimited | Free |

## Conclusion

**For your weather pipeline**: Repository storage is perfect! Weather data is tiny (few KB per day), and you get:
- ✅ Immediate deployment
- ✅ Data versioning
- ✅ Easy access and analysis
- ✅ No additional setup or costs

You can always migrate to a database later if needed.
