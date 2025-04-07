from app.face_detection import HaarDetector  # Use Haar for real-time
from app.feature_extraction.embeddings import EmbeddingGenerator
from app.database.db_handler import FaceDatabase
from sklearn.metrics.pairwise import cosine_similarity

class Verifier:
    """Handles user verification with fast Haar detection."""
    
    def __init__(self, threshold=0.7):
        self.detector = HaarDetector()  # Fixed to Haar
        self.embedder = EmbeddingGenerator()
        self.db = FaceDatabase()
        self.threshold = threshold

    def verify_user(self, image_path: str) -> str:
        """Verify a user by comparing embeddings."""
        try:
            cropped_path = self.detector.crop_face(image_path)
            embedding = self.embedder.generate_embedding(cropped_path)
            if embedding is None:
                return None
            
            for name, stored_embedding in self.db.get_all_users():
                similarity = cosine_similarity([embedding], [stored_embedding])[0][0]
                if similarity > self.threshold:
                    return name
            return None
        except Exception as e:
            print(f"Verification failed: {e}")
            return None

"""from ..recognition.face_recognizer import FaceRecognizer

class Verifier:
    def __init__(self, threshold=0.7):
        self.db = FaceDatabase()
        self.recognizer = FaceRecognizer(threshold)

    def verify_user(self, embedding):
        all_users = self.db.get_all_users()
        for name, stored_embedding in all_users:
            if self.recognizer.is_match(embedding, stored_embedding):
                return name
        return None"""