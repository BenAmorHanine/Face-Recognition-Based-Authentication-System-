# Embedding comparison, threshold
#by chat ( o for chat, el embeddings/facenet will be loaded a pretrained model)
from scipy.spatial.distance import cosine

class FaceRecognizer:
    def __init__(self, threshold=0.6):
        self.threshold = threshold

    def compare_embeddings(self, embedding1, embedding2):
        similarity = 1 - cosine(embedding1, embedding2)
        return similarity > self.threshold


#by deepseek:
#the face_recognition could be put in the verifypy file 
"""
from sklearn.metrics.pairwise import cosine_similarity

class FaceRecognizer:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def is_match(self, embedding1, embedding2):
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        return similarity > self.threshold
"""