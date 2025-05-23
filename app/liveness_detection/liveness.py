import cv2
from mtcnn import MTCNN

class LivenessDetector:
    """Detects spoofing attempts using eye-blink analysis."""
    
    def __init__(self):
        self.detector = MTCNN()  # For facial landmarks
    
    def is_real(self, frame_path: str) -> bool:
        """Check if the face is live using eye-blink detection."""
        frame = cv2.cvtColor(cv2.imread(frame_path), cv2.COLOR_BGR2RGB)
        faces = self.detector.detect_faces(frame)
        if not faces:
            return False
        
        # Simple eye-blink heuristic (example)
        landmarks = faces[0]['keypoints']
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']
        
        # Calculate eye aspect ratio (EAR)
        ear = (abs(left_eye[1] - right_eye[1]) / 
               abs(left_eye[0] - right_eye[0]))
        
        return ear < 0.4  # Threshold for "blinking"
    
    
    def is_real_video(self, video_path: str) -> bool:
        """Requires a short video (2-3 seconds)"""
        cap = cv2.VideoCapture(video_path)
        eye_states = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Detect eye state per frame (open/closed)
            eyes_closed = self._check_eyes_closed(frame)
            eye_states.append(eyes_closed)
        
        # Check for at least one open→closed→open transition
        return self._detect_blink_pattern(eye_states)


    """"
#THIS VERSION IS BETTTER FOR REALTIME-> live webcam
# the frame is given as fram(image array), consider that.
import cv2
from mtcnn import MTCNN

class LivenessDetector:
    def __init__(self):
        # Initialize MTCNN for facial landmark detection
        self.detector = MTCNN()

    def check_blink(self, frame):
        # Detect faces and landmarks
        faces = self.detector.detect_faces(frame)
        if not faces:
            return False  # No face detected
        
        # Extract eye coordinates
        landmarks = faces[0]['keypoints']
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']
        
        # Simple blink detection using eye aspect ratio (EAR)
        eye_aspect_ratio = (abs(left_eye[1] - right_eye[1]) / 
                           abs(left_eye[0] - right_eye[0]))
        return eye_aspect_ratio < 0.2  # Threshold for detecting a blink"""