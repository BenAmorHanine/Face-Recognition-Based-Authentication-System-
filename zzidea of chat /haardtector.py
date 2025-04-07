# app/face_detection/haar_detector.py
import cv2

class HaarDetector:
    def __init__(self, cascade_path="haarcascade_frontalface_default.xml"):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)

    def detect_face(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        face_regions = []
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            face_regions.append(face)
        return face_regions
