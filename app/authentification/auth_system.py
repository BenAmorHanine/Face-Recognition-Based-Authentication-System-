#enroll and verify logic
#after separating
from .enroll import Enrollment
from .verify import Verifier

class AuthSystem:
    """Unified interface for enrollment and verification workflows."""
    
    def __init__(self):
        self.enroller = Enrollment()  # Uses MTCNN by config
        self.verifier = Verifier()    # Uses Haar by config

    def enroll(self, name: str, image_path: str) -> bool:
        return self.enroller.enroll_user(name, image_path)

    def verify(self, image_path: str) -> str:
        return self.verifier.verify_user(image_path)
    

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