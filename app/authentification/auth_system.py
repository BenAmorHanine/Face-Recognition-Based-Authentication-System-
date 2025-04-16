#enroll and verify logic
#after separating
from datetime import datetime
import tempfile
from typing import Dict, Optional, Tuple, List
import cv2
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
        self.MAX_ATTEMPTS = 40

    def enroll(self, name: str, image_path: str) -> bool:
        return self.enroller.enroll_user(name, image_path)

    def verify(self, image_path: str) -> str:
        if self.attempts > self.MAX_ATTEMPTS:
            raise  HTTPError("429 Too Many Requests")
        self.attempts += 1
        return self.verifier.verify_user(image_path)

    def deactivate_user(self, username: str) -> bool:
        return self.verifier.db.deactivate_user(username)  

    def batch_enroll(self, user_data: Dict[str, str]) -> Dict[str, str]:
        """Expose batch enrollment through auth system"""
        return self.enroller.batch_enroll(user_data)
    
    def verify_from_memory(self, image_array: np.ndarray) -> Optional[Tuple[str, float]]:
        """Verify a user's identity from an image array (in-memory)"""
        try:
            # Enforce attempt limits
            if self.attempts >= self.MAX_ATTEMPTS:
                raise HTTPError("429 Too Many Requests")
            self.attempts += 1

            # Save image array to a temp file
            with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
                # Convert RGB array to BGR and write to file
                if image_array.shape[-1] == 3:
                    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
                else:
                    image_bgr = image_array  # If already BGR or grayscale

                cv2.imwrite(tmp.name, image_bgr)

                # Use existing verify_user(file_path) logic
                return self.verifier.verify_user(tmp.name)

        except HTTPError:
            raise  # Re-raise to be handled by calling route
        except Exception as e:
            print(f"[ERROR] Memory verification failed: {e}")
            return None


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

    