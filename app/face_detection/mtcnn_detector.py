from mtcnn import MTCNN
import cv2
from .base_detector import BaseFaceDetector

class MTCNNDetector(BaseFaceDetector):
    """High-accuracy face detector using MTCNN (with facial landmarks)."""
    
    def __init__(self):
        self.detector = MTCNN()

    def detect_faces(self, image_path: str) -> list:
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        return self.detector.detect_faces(image)  # Returns face boxes + landmarks

    def crop_face(self, image_path: str, output_path: str = "cropped_face.jpg") -> str:
        faces = self.detect_faces(image_path)
        if not faces:
            raise ValueError("No faces detected!")
        
        x, y, w, h = faces[0]['box']
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        cropped_face = image[y:y+h, x:x+w]
        cv2.imwrite(output_path, cv2.cvtColor(cropped_face, cv2.COLOR_RGB2BGR))
        return output_path