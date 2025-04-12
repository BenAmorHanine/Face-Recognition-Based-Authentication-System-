#after separation

import sqlite3
import numpy as np
from datetime import datetime
from typing import Optional, List, Tuple

class FaceDatabase:
    """Enhanced SQLite handler for web face recognition systems.
    Handles user embeddings with improved security and web-specific features.
    """
    
    def __init__(self, db_path: str = "face_auth.db"):
        """Initialize database with connection pooling-ready settings."""
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self._create_tables()

    def _create_tables(self) -> None:
        """Initialize database schema with web-friendly additions."""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,  # Changed from 'name' for consistency
                embedding BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE
            );
            
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY,
                username TEXT,
                attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN,
                ip_address TEXT
            );
        """)
        self.conn.commit()

    def save_user(self, username: str, embedding: list) -> bool:
            """Save user with additional checks and error handling.
            
            Args:
                username: Unique identifier
                embedding: Face embedding vector
                
            Returns:
                bool: True if successful, False if user exists
            """
            try:
                self.conn.execute(
                    "INSERT INTO users (username, embedding) VALUES (?, ?)",
                    (username, np.array(embedding).tobytes())  # Fixed: Added missing parenthesis
                )
                self.conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
    
    def get_user(self, username: str) -> Optional[dict]:
        """Get single user with secure data handling.
        
        Returns:
            dict: {'username': str, 'embedding': np.array, 'last_login': str}
            None: If user not found
        """
        row = self.conn.execute(
            "SELECT username, embedding, last_login FROM users WHERE username = ?",
            (username,)).fetchone()
        
        if row:
            return {
                'username': row['username'],
                'embedding': np.frombuffer(row['embedding'], dtype=np.float32),
                'last_login': row['last_login']
            }
        return None

    def get_all_users(self) -> List[Tuple[str, np.ndarray]]:
        """Get all active users efficiently.
        
        Returns:
            List of (username, embedding) tuples
        """
        return [
            (row['username'], np.frombuffer(row['embedding'], dtype=np.float32))
            for row in self.conn.execute(
                "SELECT username, embedding FROM users WHERE is_active = TRUE")
        ]

    def record_login_attempt(self, username: str, success: bool, ip: str) -> None:
        """Log authentication attempts for security monitoring."""
        self.conn.execute(
            "INSERT INTO login_attempts (username, success, ip_address) VALUES (?, ?, ?)",
            (username, success, ip))
        self.conn.commit()

    def deactivate_user(self, username: str) -> bool:
        """Soft-delete user instead of physical deletion."""
        self.conn.execute(
            "UPDATE users SET is_active = FALSE WHERE username = ?",
            (username,))
        self.conn.commit()
        return self.conn.total_changes > 0

    def __del__(self):
        """Ensure connections are closed properly."""
        self.conn.close()

    

"""
import sqlite3
import numpy as np

class FaceDatabase:
    #Handles SQLite database operations for user embeddings.
    
    def __init__(self, db_path: str = "face_auth.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        #Create users table if it doesn't exist.
        self.cursor.execute(
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                embedding BLOB
            )
        )
        self.conn.commit()

    def save_user(self, name: str, embedding: list) -> None:
        #Save a user's face embedding to the database.
        self.cursor.execute(
            "INSERT INTO users (name, embedding) VALUES (?, ?)",
            (name, np.array(embedding).tobytes()))
        self.conn.commit()

    def get_all_users(self) -> list:
        #Retrieve all users and their embeddings.
        return self.cursor.execute("SELECT name, embedding FROM users").fetchall()

"""

"""
import sqlite3
import numpy as np

class FaceDatabase:
    def __init__(self, db_path="face_auth.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute(
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                embedding BLOB
            )
        )
        self.conn.commit()

    def save_user(self, name, embedding):
        self.cursor.execute(
            "INSERT INTO users (name, embedding) VALUES (?, ?)",
            (name, np.array(embedding).tobytes())
        )
        self.conn.commit()

    def get_user_embedding(self, name):
        self.cursor.execute("SELECT embedding FROM users WHERE name=?", (name,))
        result = self.cursor.fetchone()
        return np.frombuffer(result[0], dtype=np.float32) if result else None
"""