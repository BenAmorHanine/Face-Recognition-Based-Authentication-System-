#enroll and verify logic
#after separating
from .face_detection import MTCNNDetector, HaarDetector
from .feature_extraction.embeddings import EmbeddingGenerator
from .database.db_handler import FaceDatabase
from .config import DETECTOR_TYPE, SIMILARITY_THRESHOLD

class AuthSystem:
    """Orchestrates enrollment and verification workflows."""
    
    def __init__(self):
        # Initialize detector based on config
        if DETECTOR_TYPE == "mtcnn":
            self.detector = MTCNNDetector()
        else:
            self.detector = HaarDetector()
        
        self.embedder = EmbeddingGenerator()
        self.db = FaceDatabase()

    def enroll_user(self, name: str, image_path: str) -> bool:
        """Enroll a new user with face detection and embedding storage."""
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

    def verify_user(self, image_path: str) -> str:
        """Verify a user against stored embeddings."""
        cropped_path = self.detector.crop_face(image_path)
        embedding = self.embedder.generate_embedding(cropped_path)
        if embedding is None:
            return None
        
        # Compare with all stored embeddings
        for name, stored_embedding in self.db.get_all_users():
            similarity = cosine_similarity([embedding], [stored_embedding])[0][0]
            if similarity > SIMILARITY_THRESHOLD:
                return name
        return None
    

    """
from .enroll import Enrollment
from .verify import Verifier
from ..face_detection.base_detector import FaceDetector
from ..feature_extraction.embeddings import EmbeddingGenerator

class AuthSystem:
    def __init__(self):
        self.enroller = Enrollment()
        self.verifier = Verifier()
        self.detector = FaceDetector()
        self.embedder = EmbeddingGenerator()

    def enroll_user(self, name, image_path):
        return self.enroller.enroll_user(name, image_path)

    def verify_user(self, image_path):
        # Detect face and generate embedding
        cropped_path = self.detector.crop_face(image_path)
        embedding = self.embedder.generate_embedding(cropped_path)
        if embedding is None:
            return None
        return self.verifier.verify_user(embedding)
        """