# Import necessary modules from project components
from app.face_detection.detector_factory import DetectorFactory
from app.feature_extraction.embeddings import EmbeddingGenerator
from app.database.db_handler import FaceDatabase
from app.config import ENROLLMENT_DETECTOR

class Enrollment:
    """Handles the user enrollment process for facial recognition authentication.
    
    Uses a configurable face detector (default: MTCNN) for high-accuracy enrollment,
    generates facial embeddings using a deep learning model, and stores them in a database.
    """
    
    def __init__(self):
        """Initialize enrollment components.
        
        - Detector: Chosen via factory based on ENROLLMENT_DETECTOR config
        - Embedder: Converts face images to numerical vectors
        - Database: Stores user embeddings for later verification
        """
        # Initialize face detector based on configuration (MTCNN/haar)
        self.detector = DetectorFactory.create_detector(ENROLLMENT_DETECTOR)
        
        # Initialize embedding generator (uses FaceNet/ArcFace under the hood)
        self.embedder = EmbeddingGenerator()
        
        # Initialize database connection for storing embeddings
        self.db = FaceDatabase()

    def enroll_user(self, name: str, image_path: str) -> bool:
        """Main enrollment workflow. Returns True if enrollment succeeds.
        
        Process Flow:
        1. Detect and crop face from input image
        2. Generate facial embedding from cropped face
        3. Store embedding in database with username
        4. Handle errors gracefully with status returns
        
        Args:
            name: Unique identifier for the user
            image_path: File path to the enrollment image
            
        Returns:
            bool: Success status of enrollment operation
        """
        try:
            # Step 1: Detect and crop face using configured detector
            # Outputs path to temporary cropped face image
            cropped_path = self.detector.crop_face(image_path)
            
            # Step 2: Generate 128/512-dimensional embedding from face
            # Returns None if no face detected
            embedding = self.embedder.generate_embedding(cropped_path)
            
            if embedding is not None:
                # Step 3: Store in database as BLOB with username
                self.db.save_user(name, embedding)
                return True
                
            # No face detected case
            return False
            
        except Exception as e:
            # Handle file I/O, detector, or database errors
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