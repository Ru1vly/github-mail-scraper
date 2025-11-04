#!/usr/bin/env python3
"""
Example: Fetch and analyze a GitHub .patch URL
Run: python3 examples/fetch_example.py
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scraper.fetcher import fetch_patch
from scraper.parser import parse_patch, is_noreply_email
from scraper.storage import PatchStorage


async def main():
    # Example: Fetch a real GitHub PR patch
    # This is a small, public PR from the requests library
    url = "https://github.com/psf/requests/pull/6000.patch"
    
    print(f"🔍 Fetching: {url}")
    print()
    
    try:
        # Fetch the patch
        raw_patch = await fetch_patch(url)
        print(f"✓ Fetched {len(raw_patch)} bytes")
        
        # Parse line 2 for email and username
        parsed = parse_patch(raw_patch)
        email = parsed["email"]
        username = parsed["username"]
        print(f"✓ Parsed successfully")
        print()
        
        # Display extracted information
        print("📊 Extracted Information:")
        print(f"  Email:    {email}")
        print(f"  Username: {username}")
        print()
        
        # Check filtering rules
        storage = PatchStorage("data/patches.db")
        
        if is_noreply_email(email):
            print("⊘ Skipped: noreply email")
            return
        
        if storage.email_exists(email):
            print("⊘ Skipped: email already in database")
            return
        
        # Save to database
        row_id = storage.save_patch(email, username)
        print(f"💾 Saved to database (id={row_id})")
        print()
        
        # Show total count
        total = storage.count_patches()
        print(f"� Total emails in database: {total}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
