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