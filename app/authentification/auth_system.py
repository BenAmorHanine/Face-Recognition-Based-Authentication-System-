#enroll and verify logic
from .enroll import Enrollment
from .verify import Verifier
from ..face_detection.detector import FaceDetector
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