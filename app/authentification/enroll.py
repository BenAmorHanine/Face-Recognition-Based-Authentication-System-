import os
import shutil
import time
import numpy as np
from datetime import datetime
from typing import Optional
from app.face_detection.detector_factory import DetectorFactory
from app.feature_extraction.embeddings import EmbeddingGenerator
from app.database.db_handler import FaceDatabase
from app.config import ENROLLMENT_DETECTOR

class Enrollment:
    """Handles user enrollment with face detection, embedding generation, and database storage.
    
    Features:
    - Configurable face detector (MTCNN/Haar)
    - Automatic raw image archiving
    - Cropped face storage for debugging
    - Atomic database operations
    """

    def __init__(self):
        """Initialize enrollment components with dependency injection."""
        self.detector = DetectorFactory.create_detector(ENROLLMENT_DETECTOR)
        self.embedder = EmbeddingGenerator()
        self.db = FaceDatabase()

    def enroll_user(self, username: str, image_path: str) -> bool:
        """Complete enrollment workflow with error handling.
        
        Args:
            username: Unique user identifier
            image_path: Path to the enrollment image
            
        Returns:
            bool: True if enrollment succeeded, False otherwise
        """
        try:
            # 1. Archive raw image with timestamp
            raw_user_dir = f"dataset/raw/users/{username}"
            os.makedirs(raw_user_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_save_path = f"{raw_user_dir}/{timestamp}.jpg"
            shutil.copy(image_path, raw_save_path)

            # 2. Detect and crop face
            processed_path = f"dataset/processed/users/{username}.jpg"
            if not self.detector.crop_face(image_path, output_path=processed_path):
                raise ValueError("Face detection failed")

            # 3. Generate embedding
            embedding = self.embedder.generate_embedding(processed_path)
            print(f"New embedding shape: {len(embedding)}")  # should be 128
            if embedding is None:
                raise ValueError("Embedding generation failed")

            # 4. Store in database

            if not self.db.save_user(username, embedding):
                raise ValueError(f"Username {username} already exists")

            print(f"Enrollment successful for {username}")
            print(f"Raw image saved at: {raw_save_path}")
            print(f"Processed image saved at: {processed_path}")
            print(f"saved in db: {len(embedding)}")  # should be 128
            print(f"Embedding saved in database for {username}")

            return True

        except Exception as e:
            print(f"Enrollment Error: {str(e)}")
            # Cleanup failed enrollment artifacts
            if 'raw_save_path' in locals() and os.path.exists(raw_save_path):
                os.remove(raw_save_path)
            if 'processed_path' in locals() and os.path.exists(processed_path):
                os.remove(processed_path)
            return False

    def batch_enroll(self, user_data: dict) -> dict:
            """Enroll multiple users with progress tracking.
            
            Args:
                user_data: {username: image_path} dictionary
                
            Returns:
                dict: {"success": [usernames], "failed": {username: error}}
            """
            results = {"success": [], "failed": {}}
            for username, image_path in user_data.items():
                if self.enroll_user(username, image_path):
                    results["success"].append(username)
                else:
                    results["failed"][username] = "Enrollment failed"
            return results