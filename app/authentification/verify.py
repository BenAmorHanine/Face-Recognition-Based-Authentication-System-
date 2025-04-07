from ..recognition.face_recognizer import FaceRecognizer

class Verifier:
    def __init__(self, threshold=0.7):
        self.db = FaceDatabase()
        self.recognizer = FaceRecognizer(threshold)

    def verify_user(self, embedding):
        all_users = self.db.get_all_users()
        for name, stored_embedding in all_users:
            if self.recognizer.is_match(embedding, stored_embedding):
                return name
        return None