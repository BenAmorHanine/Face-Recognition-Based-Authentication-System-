#after separation
import sqlite3
import numpy as np

class FaceDatabase:
    """Handles SQLite database operations for user embeddings."""
    
    def __init__(self, db_path: str = "face_auth.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create users table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                embedding BLOB
            )
        """)
        self.conn.commit()

    def save_user(self, name: str, embedding: list) -> None:
        """Save a user's face embedding to the database."""
        self.cursor.execute(
            "INSERT INTO users (name, embedding) VALUES (?, ?)",
            (name, np.array(embedding).tobytes())
        self.conn.commit()

    def get_all_users(self) -> list:
        """Retrieve all users and their embeddings."""
        return self.cursor.execute("SELECT name, embedding FROM users").fetchall()


"""
import sqlite3
import numpy as np

class FaceDatabase:
    def __init__(self, db_path="face_auth.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                embedding BLOB
            )
        """)
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