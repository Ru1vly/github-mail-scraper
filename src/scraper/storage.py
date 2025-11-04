"""Simple SQLite storage for email and username from patches"""
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone


class PatchStorage:
    """Store email and username extracted from patches."""
    
    def __init__(self, db_path: str = "data/patches.db"):
        """Initialize storage, create tables if needed."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Create patches table with just email and username."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    username TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_email ON patches(email)
            """)
            conn.commit()
    
    def email_exists(self, email: str) -> bool:
        """Check if an email already exists in the database.
        
        Args:
            email: Email address to check
        
        Returns:
            True if email exists, False otherwise
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT 1 FROM patches WHERE email = ? LIMIT 1", (email,)
            )
            return cursor.fetchone() is not None
    
    def save_patch(self, email: str, username: str) -> int:
        """Save email and username to database.
        
        Args:
            email: Email address
            username: Username
        
        Returns:
            The row id
        
        Raises:
            sqlite3.IntegrityError if email already exists
        """
        now = datetime.now(timezone.utc).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO patches (email, username, created_at)
                VALUES (?, ?, ?)
                """,
                (email, username, now),
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_patch_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve a record by email."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM patches WHERE email = ?", (email,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def list_patches(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List recent patches."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT id, email, username, created_at FROM patches ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def count_patches(self) -> int:
        """Get total count of patches in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM patches")
            return cursor.fetchone()[0]
