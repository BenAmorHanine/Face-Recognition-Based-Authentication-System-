import cv2
from mtcnn import MTCNN
from collections import deque

class RealTimeBlinkDetector:
    def __init__(self):
        self.detector = MTCNN()
        self.eye_state_history = deque(maxlen=10)  # Stores last 10 eye states
        self.blink_threshold = 0.2  # EAR threshold for closed eyes
        self.required_blinks = 2    # Minimum blinks to confirm liveness

    def _get_eye_state(self, frame):
        """Returns True if eyes open, False if closed"""
        faces = self.detector.detect_faces(frame)
        if not faces:
            return None  # No face detected
        
        landmarks = faces[0]['keypoints']
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']
        
        # Calculate Eye Aspect Ratio (EAR)
        ear = (abs(left_eye[1] - right_eye[1]) / 
               max(1, abs(left_eye[0] - right_eye[0])))  
        
        return ear > self.blink_threshold  # True=open, False=closed

    def _detect_blink_pattern(self):
        """Checks for Open→Closed→Open transitions in history"""
        blinks = 0
        for i in range(2, len(self.eye_state_history)):
            # Pattern: Open → Closed → Open
            if (self.eye_state_history[i-2] and 
                not self.eye_state_history[i-1] and 
                self.eye_state_history[i]):
                blinks += 1
        return blinks >= self.required_blinks

    def run_detection(self):
        cap = cv2.VideoCapture(0)  # Webcam
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Mirror frame for more natural UX
            frame = cv2.flip(frame, 1)
            
            # Detect eye state
            eye_state = self._get_eye_state(frame)
            if eye_state is not None:
                self.eye_state_history.append(eye_state)
                
                # Visual feedback
                color = (0, 255, 0) if eye_state else (0, 0, 255)
                cv2.putText(frame, "EYES: OPEN" if eye_state else "EYES: CLOSED",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Check for blinks
            if self._detect_blink_pattern():
                cv2.putText(frame, "LIVENESS CONFIRMED!", (10, 70),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow("Blink Detection", frame)
            
            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()


detector = RealTimeBlinkDetector()
detector.run_detection()