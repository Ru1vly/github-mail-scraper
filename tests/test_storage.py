"""Tests for the storage module"""
import tempfile
import pytest
from pathlib import Path
from scraper.storage import PatchStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        storage = PatchStorage(str(db_path))
        yield storage


def test_save_and_retrieve_patch(temp_storage):
    """Test saving and retrieving a patch."""
    email = "user@example.com"
    username = "testuser"
    
    # Save
    row_id = temp_storage.save_patch(email, username)
    assert row_id > 0
    
    # Retrieve
    retrieved = temp_storage.get_patch_by_email(email)
    assert retrieved is not None
    assert retrieved["email"] == email
    assert retrieved["username"] == username


def test_email_exists(temp_storage):
    """Test checking if email exists."""
    email = "user@example.com"
    username = "testuser"
    
    # Should not exist initially
    assert temp_storage.email_exists(email) is False
    
    # Save
    temp_storage.save_patch(email, username)
    
    # Should exist now
    assert temp_storage.email_exists(email) is True


def test_duplicate_email_raises_error(temp_storage):
    """Test that saving duplicate email raises error."""
    email = "duplicate@example.com"
    
    # First save
    temp_storage.save_patch(email, "user1")
    
    # Second save with same email should raise error
    with pytest.raises(Exception):  # sqlite3.IntegrityError
        temp_storage.save_patch(email, "user2")


def test_list_patches(temp_storage):
    """Test listing patches."""
    # Save multiple patches
    for i in range(5):
        temp_storage.save_patch(f"user{i}@example.com", f"user{i}")
    
    patches = temp_storage.list_patches(limit=10)
    assert len(patches) == 5
    
    # Should be ordered by created_at DESC
    patches = temp_storage.list_patches(limit=2)
    assert len(patches) == 2


def test_count_patches(temp_storage):
    """Test counting patches."""
    assert temp_storage.count_patches() == 0
    
    # Add some patches
    for i in range(3):
        temp_storage.save_patch(f"user{i}@example.com", f"user{i}")
    
    assert temp_storage.count_patches() == 3
