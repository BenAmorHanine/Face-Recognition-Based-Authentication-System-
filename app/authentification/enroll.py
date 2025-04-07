from app.face_detection import MTCNNDetector  # Use MTCNN for enrollment
from app.feature_extraction.embeddings import EmbeddingGenerator
from app.database.db_handler import FaceDatabase

class Enrollment:
    """Handles user enrollment with high-accuracy MTCNN detection."""
    
    def __init__(self):
        self.detector = MTCNNDetector()  # Fixed to MTCNN
        self.embedder = EmbeddingGenerator()
        self.db = FaceDatabase()

    def enroll_user(self, name: str, image_path: str) -> bool:
        """Enroll a user by detecting, cropping, and storing their face."""
        try:
            cropped_path = self.detector.crop_face(image_path)
            embedding = self.embedder.generate_embedding(cropped_path)
            if embedding is not None:
                self.db.save_user(name, embedding)
                return True
            return False
        except Exception as e:
            print(f"Enrollment failed: {e}")
            return False
    
    
"""from ..face_detection.base_detector import FaceDetector
from ..feature_extraction.embeddings import EmbeddingGenerator
from ..database.db_handler import FaceDatabase

class Enrollment:
    def __init__(self):
        # Initialize dependencies
        self.detector = FaceDetector()
        self.embedder = EmbeddingGenerator()
        self.db = FaceDatabase()

    def enroll_user(self, name, image_path):
        try:
            # Step 1: Detect and crop the face
            cropped_path = self.detector.crop_face(image_path)
            # Step 2: Generate embedding from the cropped face
            embedding = self.embedder.generate_embedding(cropped_path)
            if embedding is not None:
                # Step 3: Save to database
                self.db.save_user(name, embedding)
                return True
            return False  # No face detected
        except Exception as e:
            print(f"Enrollment failed: {e}")
            return False

"""