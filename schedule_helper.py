#!/usr/bin/env python3
"""
Helper script to switch between testing and production schedules.
"""

import os
import sys

def read_workflow_file():
    """Read the current workflow file."""
    workflow_path = '.github/workflows/data_pipeline.yml'
    try:
        with open(workflow_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Workflow file not found: {workflow_path}")
        sys.exit(1)

def write_workflow_file(content):
    """Write the workflow file."""
    workflow_path = '.github/workflows/data_pipeline.yml'
    with open(workflow_path, 'w') as f:
        f.write(content)

def set_testing_schedule():
    """Set schedule to run every 10 minutes for testing."""
    content = read_workflow_file()

    # Replace daily schedule with 10-minute schedule
    if "'35 0 * * *'" in content:
        content = content.replace(
            "- cron: '35 0 * * *'",
            "- cron: '*/10 * * * *'"
        )
        content = content.replace(
            "# Schedule to run daily at 12:35 AM UTC (7:35 AM Toronto time)",
            "# TESTING: Run every 10 minutes (more reliable than 5 minutes)\n  # For daily: '35 0 * * *' (12:35 AM UTC / 7:35 AM Toronto time)"
        )
    elif "'*/10 * * * *'" in content:
        print("⚠️ Already set to testing schedule (every 10 minutes)")
        return False
    else:
        print("❌ Could not find schedule pattern to replace")
        return False

    write_workflow_file(content)
    print("✅ Schedule set to TESTING mode: every 10 minutes")
    print("⚠️ Remember to change back to daily schedule after testing!")
    return True

def set_daily_schedule():
    """Set schedule to run daily (production)."""
    content = read_workflow_file()

    # Replace 10-minute schedule with daily schedule
    if "'*/10 * * * *'" in content:
        content = content.replace(
            "- cron: '*/10 * * * *'",
            "- cron: '35 0 * * *'"
        )
        content = content.replace(
            "# TESTING: Run every 10 minutes (more reliable than 5 minutes)\n  # For daily: '35 0 * * *' (12:35 AM UTC / 7:35 AM Toronto time)",
            "# Schedule to run daily at 12:35 AM UTC (7:35 AM Toronto time)"
        )
    elif "'35 0 * * *'" in content:
        print("⚠️ Already set to daily schedule")
        return False
    else:
        print("❌ Could not find schedule pattern to replace")
        return False

    write_workflow_file(content)
    print("✅ Schedule set to PRODUCTION mode: daily at 7:35 AM Toronto time")
    return True

def show_current_schedule():
    """Show the current schedule setting."""
    content = read_workflow_file()

    if "'*/10 * * * *'" in content:
        print("📅 Current schedule: TESTING (every 10 minutes)")
        print("⚠️ This will use GitHub Actions minutes quickly!")
    elif "'35 0 * * *'" in content:
        print("📅 Current schedule: PRODUCTION (daily at 7:35 AM Toronto time)")
    else:
        print("❓ Unknown schedule pattern")

def main():
    """Main function."""
    if len(sys.argv) != 2:
        print("🌤️ Weather Pipeline Schedule Helper")
        print("=" * 40)
        print("Usage:")
        print("  python schedule_helper.py status    # Show current schedule")
        print("  python schedule_helper.py testing   # Set to 5-minute testing")
        print("  python schedule_helper.py daily     # Set to daily production")
        print()
        show_current_schedule()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'status':
        show_current_schedule()
    elif command == 'testing':
        if set_testing_schedule():
            print()
            print("🧪 TESTING MODE ENABLED")
            print("Next steps:")
            print("1. git add .github/workflows/data_pipeline.yml")
            print("2. git commit -m 'Set testing schedule: every 5 minutes'")
            print("3. git push")
            print("4. Watch Actions tab - pipeline will run every 5 minutes")
            print("5. Run 'python schedule_helper.py daily' when done testing")
    elif command == 'daily':
        if set_daily_schedule():
            print()
            print("🏭 PRODUCTION MODE ENABLED")
            print("Next steps:")
            print("1. git add .github/workflows/data_pipeline.yml")
            print("2. git commit -m 'Set production schedule: daily'")
            print("3. git push")
            print("4. Pipeline will now run once daily at 7:35 AM Toronto time")
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: status, testing, or daily")
        sys.exit(1)

if __name__ == "__main__":
    main()
