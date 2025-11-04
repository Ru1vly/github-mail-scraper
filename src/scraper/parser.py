"""Parse email and username from .patch content (line 2)"""
import re
from typing import Dict, Optional


def parse_patch(patch_text: str) -> Dict[str, Optional[str]]:
    """Parse line 2 of a .patch file to extract email and username.
    
    Expected format on line 2:
        From: username <email@domain.com>
    
    Args:
        patch_text: Raw .patch content
    
    Returns:
        Dictionary with:
        {
            "email": str or None,
            "username": str or None,
        }
    
    Raises:
        ValueError if line 2 doesn't match expected format
    """
    lines = patch_text.split('\n')
    
    if len(lines) < 2:
        raise ValueError("Patch has less than 2 lines")
    
    line2 = lines[1].strip()
    
    # Match pattern: From: username <email@domain.com>
    # or: From: username name <email@domain.com>
    pattern = r'^From:\s+(.+?)\s+<(.+?)>$'
    match = re.match(pattern, line2)
    
    if not match:
        raise ValueError(f"Line 2 doesn't match expected format: {line2}")
    
    username = match.group(1).strip()
    email = match.group(2).strip()
    
    return {
        "email": email,
        "username": username,
    }


def is_noreply_email(email: str) -> bool:
    """Check if an email is a noreply email.
    
    Args:
        email: Email address to check
    
    Returns:
        True if email contains 'noreply', False otherwise
    """
    return 'noreply' in email.lower()
