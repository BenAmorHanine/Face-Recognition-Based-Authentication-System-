#Converts faces to embeddings (numerical fingerprints) using pre-trained models.
from deepface import DeepFace
import numpy as np

class EmbeddingGenerator:
    def __init__(self, model_name="Facenet"):
        # Initialize with a pre-trained model for face embeddings
        self.model_name = model_name
        self.target_dim = 128

    def generate_embedding(self, image_path):
        try:
            # Generate a 128/512-dimensional embedding for the face
            embedding = DeepFace.represent(
                img_path=image_path,
                model_name=self.model_name,
                enforce_detection=False  # Skip if no face is detected
            )
            embedding_vector = embedding[0]["embedding"]
            if len(embedding_vector) != self.target_dim:
                raise ValueError(
                    f"Embedding must be {self.target_dim}-dim, got {len(embedding_vector)}"
                )
            
            print(f"✅ Generated embedding shape: {np.array(embedding_vector).shape}")  
            return embedding_vector
        except ValueError:
            return None  # Handle cases where no face is found
        
embedder = EmbeddingGenerator()
embedding = embedder.generate_embedding("dataset/raw/test/ahd4.jpg")