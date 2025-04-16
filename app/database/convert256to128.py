# Add this to FaceDatabase
import numpy as np
from db_handler import FaceDatabase
def fix_embedding_sizes(self):
    """Convert all 256-dim embeddings to 128-dim (truncate)."""
    cursor = self.conn.execute("SELECT id, username, embedding FROM users")
    for row in cursor:
        old_embedding = np.frombuffer(row["embedding"], dtype=np.float32)
        if len(old_embedding) == 256:
            new_embedding = old_embedding[:128]  # Take first 128 values
            self.conn.execute(
                "UPDATE users SET embedding = ? WHERE id = ?",
                (new_embedding.tobytes(), row["id"])
            )
    self.conn.commit()

db = FaceDatabase()
fix_embedding_sizes(db)  # Truncates 256-dim → 128-dim