import cv2
from .base_detector import BaseFaceDetector

class HaarDetector(BaseFaceDetector):
    """Fast face detector using Haar Cascades (optimized for real-time)."""
    
    def __init__(self):
        self.classifier = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect_faces(self, image_path: str) -> list:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    def crop_face(self, image_path: str, output_path: str = "cropped_face.jpg") -> str:
        faces = self.detect_faces(image_path)
        if len(faces) == 0:
            raise ValueError("No faces detected!")
        
        x, y, w, h = faces[0]
        image = cv2.imread(image_path)
        cropped_face = image[y:y+h, x:x+w]
        cv2.imwrite(output_path, cropped_face)
        return output_path