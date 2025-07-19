# Setup Guide

## Quick Start

1. Fork this repo
2. GitHub Actions runs automatically
3. Check "Actions" tab

## Credentials

**No credentials needed!** GitHub provides `GITHUB_TOKEN` automatically for public repos.

## Testing Schedule

Currently set to run every 5 minutes for testing.

Change back to daily:
```bash
python schedule_helper.py daily
```

## Local Testing

```bash
git clone https://github.com/jimhouserock/simple_data_pipeline.git
cd simple_data_pipeline
pip install -r requirements.txt
python data_pipeline.py
```

## Troubleshooting

- **Pipeline not running**: Check Actions tab for errors
- **No data**: Weather might be same as last run
- **Permission errors**: GitHub provides token automatically

That's it!
