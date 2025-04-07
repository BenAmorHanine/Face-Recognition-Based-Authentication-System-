# Import required modules from project components
from app.face_detection.detector_factory import DetectorFactory
from app.feature_extraction.embeddings import EmbeddingGenerator
from app.database.db_handler import FaceDatabase
from sklearn.metrics.pairwise import cosine_similarity  # For similarity calculation
from app.config import VERIFICATION_DETECTOR, SIMILARITY_THRESHOLD  # Config settings
from app.liveness_detection.liveness import LivenessDetector


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

    def verify_user(self, image_path: str) -> str:
        """Verify a user by comparing their face embedding to stored data.
        
        Args:
            image_path: Path to the image containing the face to verify
            
        Returns:
            str: Name of the matched user, or `None` if no match found.
        """
        try:
            # Step 1: Check liveness
            if not self.liveness_checker.is_real(image_path):
                return "SPOOF_ATTEMPT"
            try:
                # Step 1: Detect and crop the face from the input image
                cropped_path = self.detector.crop_face(image_path)
                
                # Step 2: Generate embedding from the cropped face
                embedding = self.embedder.generate_embedding(cropped_path)
                
                # If no face detected in the image
                if embedding is None:
                    return None
                
                # Step 3: Compare against all stored embeddings
                for name, stored_embedding in self.db.get_all_users():
                    # Calculate similarity score (0-1 range)
                    similarity = cosine_similarity([embedding], [stored_embedding])[0][0]
                    
                    # If similarity exceeds threshold, return the matched user
                    if similarity > SIMILARITY_THRESHOLD:
                        return name
                        
                # No matches found
                return None
                
            except Exception as e:
                # Handle errors (e.g., file I/O, detector failures)
                print(f"Verification failed: {e}")
                return None
        
        except Exception as e: #EXCEPTION OF LIVENESS 
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