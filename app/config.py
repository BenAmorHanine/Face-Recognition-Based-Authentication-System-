# Central configuration for the system
#DETECTOR_TYPE = "mtcnn"  # Options: "mtcnn" | "haar"
ENROLLMENT_DETECTOR = "mtcnn"  # High accuracy for registration
VERIFICATION_DETECTOR = "haar"  # Fast for login

EMBEDDING_MODEL = "Facenet"  # Options: "Facenet", "ArcFace", etc.
SIMILARITY_THRESHOLD = 0.7  # Adjust based on model/security needs
DATABASE_PATH = "face_auth.db"