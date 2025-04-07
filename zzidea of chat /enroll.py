import json
import os

from app.face_detection.mtcnn_detector import FaceDetector
from app.feature_extraction.facenet import EmbeddingGenerator

# Initialize
face_detector = FaceDetector()
embedder = EmbeddingGenerator(model_name="Facenet")

# Parameters
IMAGE_PATH = "path/to/input/image.jpg"
USERNAME = "john_doe"
DB_PATH = "app/database/embeddings.json"

# Step 1: Detect and crop face
cropped_face_path = face_detector.crop_face(IMAGE_PATH, output_path="cropped_face.jpg")

# Step 2: Generate embedding
embedding = embedder.generate_embedding(cropped_face_path)

if embedding is None:
    print("⚠️ No face detected in the image.")
else:
    # Step 3: Load or create embedding DB
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            db = json.load(f)
    else:
        db = {}

    # Step 4: Save new user embedding
    db[USERNAME] = embedding

    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

    print(f"✅ User '{USERNAME}' enrolled successfully.")
