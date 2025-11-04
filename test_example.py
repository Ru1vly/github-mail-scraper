#!/usr/bin/env python3
"""Test the parser with the example .patch file"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from scraper.parser import parse_patch, is_noreply_email

# Read the example file
example_file = Path(__file__).parent / "Example-.patch-content"
with open(example_file, 'r') as f:
    content = f.read()

print("📄 Testing parser with Example-.patch-content")
print()

try:
    result = parse_patch(content)
    print("✓ Parsed successfully!")
    print()
    print(f"  Email:    {result['email']}")
    print(f"  Username: {result['username']}")
    print()
    
    # Test noreply check
    if is_noreply_email(result['email']):
        print("⊘ This is a noreply email (would be skipped)")
    else:
        print("✓ Not a noreply email (would be saved)")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
