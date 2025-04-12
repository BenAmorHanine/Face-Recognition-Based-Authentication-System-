# Embedding comparison, threshold
#not used for now, you better use it :
#if you want to use this class, you can, , and then update the verify.py to use it .
#its better to use it , bc its good factorisation and if we later wanted to add multiple matching strategies (e.g., L2 distance).
#by chat ( o for chat, el embeddings/facenet will be loaded a pretrained model)
"""from scipy.spatial.distance import cosine

class FaceRecognizer:
    def __init__(self, threshold=0.6):
        self.threshold = threshold

    def compare_embeddings(self, embedding1, embedding2):
        similarity = 1 - cosine(embedding1, embedding2)
        return similarity > self.threshold
"""

#by deepseek:
#the face_recognition could be put in the verifypy file 

from sklearn.metrics.pairwise import cosine_similarity

class FaceRecognizer:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def is_match(self, embedding1, embedding2):
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        return similarity > self.threshold


#Recommendation: Stick to sklearn for consistency with ML workflows.
