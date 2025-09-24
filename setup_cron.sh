#!/bin/bash

# Cron job setup script for comitter

echo "Setting up cron jobs for comitter..."

# Create a temporary file with the new cron jobs
TEMP_CRON=$(mktemp)

# Get existing crontab (if any)
crontab -l 2>/dev/null > "$TEMP_CRON" || true

# Check if comitter jobs already exist
if grep -q "comitter" "$TEMP_CRON"; then
    echo "Comitter cron jobs already exist. Remove them first if you want to update."
    rm "$TEMP_CRON"
    exit 1
fi

# Add new cron jobs
cat >> "$TEMP_CRON" << 'EOF'

# Comitter - GitHub contribution automation
0 10 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
0 12 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
0 16 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
0 17 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
0 18 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
0 20 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
0 22 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py >> /Users/rohanghiya/comitter/logs/cron.log 2>&1
EOF

# Install the new crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "Cron jobs installed successfully!"
echo ""
echo "Jobs will run at: 10:00, 12:00, 16:00, 17:00, 18:00, 20:00, 22:00"
echo ""
echo "To verify, run: crontab -l"
echo "To remove, run: crontab -l | grep -v comitter | crontab -"