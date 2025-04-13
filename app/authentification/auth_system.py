#enroll and verify logic
#after separating
from datetime import datetime
from typing import Dict, Optional, Tuple, List
import numpy as np
from requests.exceptions import HTTPError
from .enroll import Enrollment
from .verify import Verifier
from app.config import MAX_ATTEMPTS

class AuthSystem:
    """Unified interface for enrollment and verification workflows."""
    
    def __init__(self):
        self.enroller = Enrollment()  # Uses MTCNN by config
        self.verifier = Verifier()    # Uses Haar by config
        self.attempts = 0
        self.session_start= datetime.now()

    def enroll(self, name: str, image_path: str) -> bool:
        return self.enroller.enroll_user(name, image_path)

    def verify(self, image_path: str) -> str:
        if self.attempts > MAX_ATTEMPTS:
            raise  HTTPError("429 Too Many Requests")
        self.attempts += 1
        return self.verifier.verify_user(image_path)

    def deactivate_user(self, username: str) -> bool:
        return self.verifier.db.deactivate_user(username)  

    def batch_enroll(self, user_data: Dict[str, str]) -> Dict[str, str]:
        """Expose batch enrollment through auth system"""
        return self.enroller.batch_enroll(user_data)
    
    def verify_from_memory(self, image_array: np.ndarray) -> Optional[Tuple[str, float]]:
        """Memory-based verification endpoint"""
        if self.attempts >= self.MAX_ATTEMPTS:
            raise HTTPError("429 Too Many Requests")
        self.attempts += 1
        return self.verifier.verify_from_memory(image_array)
    
    def reset_attempts(self):
        """Reset rate limiting counter"""
        self.attempts = 0

    def get_remaining_attempts(self) -> int:
        """Show user their remaining attempts"""
        return max(0, self.MAX_ATTEMPTS - self.attempts)
    
    def get_session_info(self) -> Dict[str, str]:
        return {
            "session_start": str(self.session_start),
            "session_duration": str(datetime.now() - self.session_start)
        }
    
    def list_users(self) -> List[str]:
        """Return list of all enrolled users."""
        return self.verifier.db.list_users()

    def get_user_status(self, username: str) -> Dict[str, bool]:
        """Return whether a user exists and is active."""
        user = self.verifier.db.get_user(username)
        if user:
            return {"username": username, "active": user.active}
        return {"username": username, "exists": False}

    def reactivate_user(self, username: str) -> bool:
        """Reactivate a previously deactivated user."""
        return self.verifier.db.reactivate_user(username)

    

    
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