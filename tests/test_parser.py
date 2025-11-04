"""Tests for the parser module"""
import pytest
from scraper.parser import parse_patch, is_noreply_email


# Sample patch content (from Example-.patch-content)
SAMPLE_PATCH = """From 3169e1e48579c78cc9b7da796f04d8027effc6bf Mon Sep 17 00:00:00 2001
From: ru1vly <ru1vly@protonmail.com>
Date: Mon, 3 Nov 2025 19:04:23 +0300
Subject: [PATCH] Workflow Orchestration Service is complete

---
 TODO.md                                       |  8 +-
"""


def test_parse_patch_basic():
    """Test parsing a simple patch for email and username."""
    result = parse_patch(SAMPLE_PATCH)
    
    assert "email" in result
    assert "username" in result
    
    assert result["email"] == "ru1vly@protonmail.com"
    assert result["username"] == "ru1vly"


def test_parse_patch_with_full_name():
    """Test parsing when username includes full name."""
    patch = """From abc123 Mon Sep 17 00:00:00 2001
From: John Doe <john.doe@example.com>
Date: Mon, 3 Nov 2025 19:04:23 +0300
"""
    result = parse_patch(patch)
    
    assert result["email"] == "john.doe@example.com"
    assert result["username"] == "John Doe"


def test_parse_patch_invalid_format():
    """Test parsing with invalid line 2 format."""
    patch = """From abc123
Invalid line format
Date: Mon, 3 Nov 2025
"""
    with pytest.raises(ValueError, match="doesn't match expected format"):
        parse_patch(patch)


def test_parse_patch_too_short():
    """Test parsing with less than 2 lines."""
    patch = "From abc123"
    
    with pytest.raises(ValueError, match="less than 2 lines"):
        parse_patch(patch)


def test_is_noreply_email():
    """Test noreply email detection."""
    assert is_noreply_email("noreply@github.com") is True
    assert is_noreply_email("NOREPLY@domain.org") is True
    assert is_noreply_email("user@example.com") is False
    assert is_noreply_email("reply@example.com") is False
