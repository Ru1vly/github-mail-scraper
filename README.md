# GitHub .patch Email Scraper

A Python tool for extracting email addresses and usernames from GitHub `.patch` URLs.

## Features

- ✅ Extracts email and username from line 2 of .patch files
- ✅ Skips noreply emails automatically
- ✅ Deduplicates by email (skips if already in database)
- ✅ Async HTTP fetching with retry logic
- ✅ SQLite storage for collected emails
- ✅ CLI interface with Typer
- ✅ Unit tests

## Quick Start

### 1. Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

Or use the quick start script:

```bash
./quickstart.sh
```

### 2. Fetch a .patch URL

```bash
./scraper.sh fetch https://github.com/owner/repo/pull/123.patch
```

Or with full python command:

```bash
PYTHONPATH=src python3 -m scraper.cli fetch https://github.com/owner/repo/pull/123.patch
```

With authentication (recommended to avoid rate limits):

```bash
./scraper.sh fetch https://github.com/owner/repo/pull/123.patch --token YOUR_GITHUB_TOKEN
```

### 3. List collected emails

```bash
./scraper.sh list-patches
```

## How It Works

The scraper extracts information from line 2 of GitHub .patch files, which has this format:

```
From: username <email@domain.com>
```

### Filtering Rules

1. **Skip if email exists**: Emails are deduplicated automatically
2. **Skip noreply emails**: Any email containing "noreply" is skipped
3. **Extract only line 2**: Only the author information from line 2 is stored

## Storage

Data is stored in `data/patches.db` (SQLite) with this simple schema:

| Column     | Type    | Description                    |
|------------|---------|--------------------------------|
| id         | INTEGER | Primary key                    |
| email      | TEXT    | Email address (unique)         |
| username   | TEXT    | Username/display name          |
| created_at | TEXT    | ISO 8601 timestamp             |

## Example Output

```bash
$ ./scraper.sh fetch https://github.com/psf/requests/pull/6000.patch

Fetching https://github.com/psf/requests/pull/6000.patch...
✓ Saved to database (id=1)
  Email: developer@example.com
  Username: John Doe
```

Skipping scenarios:

```bash
# Noreply email
⊘ Skipped: noreply email (noreply@github.com)

# Duplicate email
⊘ Skipped: email already in database (developer@example.com)
```

## Running Tests

```bash
PYTHONPATH=src pytest -v
```

Or quick run:

```bash
PYTHONPATH=src pytest -q
```

## Tech Stack

- **Python 3.9+** with async/await
- **httpx** - Async HTTP client with retry logic
- **Typer + Rich** - Modern CLI with beautiful output
- **SQLite** - Embedded database
- **pytest** - Testing framework

## Architecture

```
src/scraper/
├── fetcher.py   # Async HTTP client with retry logic
├── parser.py    # Line 2 email/username extraction
├── storage.py   # SQLite storage with deduplication
└── cli.py       # CLI interface
```

## Rate Limits

GitHub has rate limits:
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour

Use `--token` to authenticate and avoid hitting limits.

## Example Script

See `examples/fetch_example.py` for a complete working example:

```bash
python3 examples/fetch_example.py
```

## Next Steps

- Add batch processing (read URLs from a file)
- Add worker queue for large-scale scraping
- Export to CSV/JSON
- Add web UI for browsing collected emails
- Deploy as a Docker container

## License

MIT
