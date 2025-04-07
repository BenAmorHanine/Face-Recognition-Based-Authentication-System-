#Converts faces to embeddings (numerical fingerprints) using pre-trained models.
# from deepface import DeepFace

class EmbeddingGenerator:
    def __init__(self, model_name="Facenet"):
        # Initialize with a pre-trained model (e.g., FaceNet, ArcFace)
        self.model_name = model_name

    def generate_embedding(self, image_path):
        try:
            # Generate a 128/512-dimensional embedding for the face
            embedding = DeepFace.represent(
                img_path=image_path,
                model_name=self.model_name,
                enforce_detection=False  # Skip if no face is detected
            )
            return embedding[0]["embedding"]  # Return the numerical vector
        except ValueError:
            return None  # Handle cases where no face is found