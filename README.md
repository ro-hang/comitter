# Comitter

Automated commit system for maintaining GitHub contribution activity.

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Configure GitHub authentication:
   - Copy `.env.example` to `.env`
   - Add your GitHub credentials (either PAT or use SSH)

3. Create a private GitHub repository named `comitter`

4. Add remote origin:
```bash
git remote add origin git@github.com:YOUR_USERNAME/comitter.git
# or for HTTPS:
git remote add origin https://github.com/YOUR_USERNAME/comitter.git
```

5. Push initial commit:
```bash
git add .
git commit -m "Initial commit"
git push -u origin main
```

6. Set up cron jobs (see below)

## Cron Setup

Add these lines to your crontab (`crontab -e`):

```bash
0 10 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
0 12 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
0 16 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
0 17 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
0 18 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
0 20 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
0 22 * * * cd /Users/rohanghiya/comitter && /opt/homebrew/bin/poetry run python src/committer.py
```

## Manual Testing

Run manually to test:
```bash
poetry run python src/committer.py
```

## How It Works

- Runs at 7 scheduled times daily (10am, 12pm, 4pm, 5pm, 6pm, 8pm, 10pm)
- Makes exactly 1 commit per execution
- Updates counter and activity tracking files
- Natural randomness from laptop sleep patterns
- Logs all activity to `logs/committer.log`