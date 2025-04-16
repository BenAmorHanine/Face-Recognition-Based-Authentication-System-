# Import required modules from project components
import os
from app.face_detection.detector_factory import DetectorFactory
from app.feature_extraction.embeddings import EmbeddingGenerator
from app.database.db_handler import FaceDatabase
from sklearn.metrics.pairwise import cosine_similarity  # For similarity calculation
from app.config import VERIFICATION_DETECTOR, SIMILARITY_THRESHOLD  # Config settings
from app.liveness_detection.liveness import LivenessDetector
from typing import Optional, Tuple
import tempfile
import cv2
import numpy as np


class Verifier:
    """Handles user verification by comparing facial embeddings against stored data.
    
    Uses a fast detector (e.g., Haar) for real-time verification and cosine similarity 
    to match embeddings. Configured via `VERIFICATION_DETECTOR` and `SIMILARITY_THRESHOLD`.
    """
    
    def __init__(self):
        """Initialize verification components:
        - Detector: Fast detector (Haar by default) for real-time face detection
        - Embedder: Generates facial embeddings using a pre-trained model
        - Database: Retrieves stored user embeddings for comparison
        """
        # Create detector based on config
        self.detector = DetectorFactory.create_detector(VERIFICATION_DETECTOR)
        
        # Initialize embedding generator
        self.embedder = EmbeddingGenerator()
        
        # Connect to the database of stored user embeddings
        self.db = FaceDatabase()

        self.liveness_checker = LivenessDetector()

    def verify_user(self, image_path: str) -> Optional[Tuple[str, float]]:
        """Verify a user by comparing facial embeddings."""
        try:
            """# Step 0: Validate input file
            if not os.path.exists(image_path):
                print(f"❌ File not found: {image_path}")
                return None"""

            """# Step 1: Liveness check
            if not self.liveness_checker.is_real(image_path):
                return ("SPOOF_ATTEMPT", 0.0)"""

            # Step 2: Face detection
            faces = self.detector.detect_faces(image_path)
            if not faces:
                print("❌ No faces detected")
                return None

            # Step 3: Crop face
            cropped_path = self.detector.crop_face(image_path)
            if not cropped_path or not os.path.exists(cropped_path):
                print("❌ Face cropping failed")
                return None

            # Step 4: Verify OpenCV can read the image
            img = cv2.imread(cropped_path)
            if img is None:
                print(f"❌ OpenCV read failed: {cropped_path}")
                return None

            # Step 5: Generate embedding
            embedding = self.embedder.generate_embedding(cropped_path)
            if embedding is None or len(embedding) != 128:
                print(f"❌ Invalid embedding (size: {len(embedding) if embedding else 'None'})")
                return None

            # Step 6: Compare with database
            best_match = None
            highest_score = 0.0

            for name, stored_embedding in self.db.get_all_users():
                if len(stored_embedding) != 128 or stored_embedding is None:
                    print(f"⚠️ Skipping {name}: invalid stored embedding")
                    continue

                similarity = cosine_similarity([embedding], [stored_embedding])[0][0]
                if similarity > SIMILARITY_THRESHOLD and similarity > highest_score:
                    highest_score = similarity
                    best_match = name

            return (best_match, highest_score) if best_match else None

        except Exception as e:
            print(f"Verification failed: {e}")
            return None






    def verify_from_memory(self, image_array: np.ndarray) -> Optional[Tuple[str, float]]:
        """
        Alternative method that works with in-memory image arrays
        """
        try:
            # Save array to temp file and use main verify method
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=True) as tmp:
                cv2.imwrite(tmp.name, image_array)
                return self.verify_user(tmp.name)
        except Exception as e:
            print(f"Memory verification error: {e}")
            return None
   



verifier = Verifier()
result = verifier.verify_user("dataset/raw/test/ahd1.jpg")
