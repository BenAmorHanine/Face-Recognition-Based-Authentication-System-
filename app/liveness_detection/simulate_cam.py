import cv2
import numpy as np
import os

class MockCamera:
    def __init__(self):
        self.width, self.height = 640, 480
        self.frame_count = 0
        os.makedirs("output_frames", exist_ok=True)  # Create output directory
        
    def read(self):
        """Generates frames with simple patterns for testing"""
        # Create a gradient background
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        cv2.rectangle(frame, (0, 0), (self.width, self.height), 
                    (self.frame_count % 255, 100, 200), -1)
        
        # Add a moving rectangle
        pos = self.frame_count % 100
        cv2.rectangle(frame, (pos, pos), (pos+200, pos+100), (255, 255, 255), 2)
        
        self.frame_count += 1
        return True, frame

# Usage - Headless Mode
cap = MockCamera()
max_frames = 10  # Generate 10 frames for testing

for i in range(max_frames):
    ret, frame = cap.read()
    
    # Save frames to files instead of displaying
    cv2.imwrite(f"output_frames/frame_{i:04d}.jpg", frame)
    print(f"Generated frame {i} - saved to output_frames/")

print(f"Done! Generated {max_frames} test frames in output_frames/ directory")

if "CODESPACES" not in os.environ:  # Local machine
    cv2.imshow("Output", frame)
    cv2.waitKey(1)
else:  # Codespaces
    cv2.imwrite(f"output_frames/frame_{i:04d}.jpg", frame)