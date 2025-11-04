# Quick Reference

## Install
```bash
python3 -m pip install -r requirements.txt
```

## Usage
```bash
# Fetch a .patch URL
./scraper.sh fetch https://github.com/owner/repo/pull/123.patch

# With token
./scraper.sh fetch URL --token YOUR_TOKEN

# List collected emails
./scraper.sh list-patches

# Show help
./scraper.sh --help
```

## Test
```bash
# Test with example file
python3 test_example.py

# Run unit tests
PYTHONPATH=src pytest -v
```

## What Gets Extracted

From line 2 of .patch files:
```
From: username <email@domain.com>
       ^^^^^^^^   ^^^^^^^^^^^^^^^^^
       stored     stored (unique key)
```

## Filtering Rules

1. ✓ Skip if email exists
2. ✓ Skip noreply emails
3. ✓ Extract only line 2

## Database Location

`data/patches.db` (SQLite)

View with:
```bash
sqlite3 data/patches.db "SELECT * FROM patches;"
```
