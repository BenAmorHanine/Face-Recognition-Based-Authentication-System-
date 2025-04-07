# App/face_detection/detector.py

from mtcnn.mtcnn import MTCNN
import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()

    def detect_faces(self, image_path):
        # Read image
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect faces
        results = self.detector.detect_faces(image_rgb)

        faces = []
        for result in results:
            x, y, width, height = result['box']
            x, y = abs(x), abs(y)  # avoid negatives
            face = image[y:y+height, x:x+width]
            faces.append(face)

            # Draw bounding box for visualization (optional)
            cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)

        return faces, image

    def detect_and_save_faces(self, image_path, save_dir='dataset/processed'):
        faces, annotated_image = self.detect_faces(image_path)

        for i, face in enumerate(faces):
            save_path = f"{save_dir}/face_{i}.jpg"
            cv2.imwrite(save_path, face)

        return faces

# Example usage
if __name__ == "__main__":
    detector = FaceDetector()
    faces = detector.detect_and_save_faces("dataset/raw/sample.jpg")
    print(f"{len(faces)} face(s) detected and saved.")
