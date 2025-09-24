#!/usr/bin/env python3

import os
import json
import random
import logging
from datetime import datetime
from pathlib import Path
from git import Repo
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "committer.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
COUNTER_FILE = DATA_DIR / "counter.txt"
ACTIVITY_FILE = DATA_DIR / "activity.json"

# Commit messages pool
COMMIT_MESSAGES = [
    "Update activity tracking",
    "Sync project data",
    "Update counter",
    "Daily commit",
    "Increment tracking data",
    "Update activity log",
    "Sync changes",
    "Update project state",
    "Automated update",
    "Update tracking information",
    "Sync activity data",
    "Update metrics",
    "Daily synchronization",
    "Update project files",
    "Automated commit",
]

def read_counter():
    """Read the current counter value."""
    if COUNTER_FILE.exists():
        with open(COUNTER_FILE, 'r') as f:
            return int(f.read().strip())
    return 0

def write_counter(value):
    """Write the counter value."""
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(value))

def read_activity():
    """Read the activity log."""
    if ACTIVITY_FILE.exists():
        with open(ACTIVITY_FILE, 'r') as f:
            return json.load(f)
    return {"commits": []}

def write_activity(data):
    """Write the activity log."""
    with open(ACTIVITY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def make_commit():
    """Make a single commit to the repository."""
    try:
        # Initialize repo
        repo = Repo(PROJECT_ROOT)

        # Check if we have a remote configured
        if not repo.remotes:
            logger.warning("No remote repository configured. Commit will be local only.")

        # Update counter
        counter = read_counter()
        counter += 1
        write_counter(counter)
        logger.info(f"Counter updated to {counter}")

        # Update activity log
        activity = read_activity()
        commit_entry = {
            "timestamp": datetime.now().isoformat(),
            "counter": counter,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S")
        }
        activity["commits"].append(commit_entry)

        # Keep only last 1000 entries to prevent file from growing too large
        if len(activity["commits"]) > 1000:
            activity["commits"] = activity["commits"][-1000:]

        write_activity(activity)
        logger.info("Activity log updated")

        # Select a random commit message
        commit_message = random.choice(COMMIT_MESSAGES)

        # Stage changes
        repo.index.add([str(COUNTER_FILE.relative_to(PROJECT_ROOT)),
                       str(ACTIVITY_FILE.relative_to(PROJECT_ROOT))])

        # Commit
        repo.index.commit(f"{commit_message} #{counter}")
        logger.info(f"Created commit: {commit_message} #{counter}")

        # Push if remote exists
        if repo.remotes:
            try:
                origin = repo.remote('origin')
                origin.push()
                logger.info("Pushed to remote repository")
            except Exception as e:
                logger.error(f"Failed to push to remote: {e}")
                logger.info("Commit was created locally")
        else:
            logger.info("No remote configured - commit saved locally")

        return True

    except Exception as e:
        logger.error(f"Error making commit: {e}")
        return False

def main():
    """Main function."""
    logger.info("=" * 50)
    logger.info("Starting committer script")

    # Check if git repo exists
    if not (PROJECT_ROOT / ".git").exists():
        logger.error("Git repository not found. Please run 'git init' first.")
        return 1

    # Make the commit
    if make_commit():
        logger.info("Successfully completed commit")
        return 0
    else:
        logger.error("Failed to complete commit")
        return 1

if __name__ == "__main__":
    exit(main())