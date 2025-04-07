from abc import ABC, abstractmethod

class BaseFaceDetector(ABC):
    """Abstract base class for face detectors."""
    
    @abstractmethod
    def detect_faces(self, image_path: str) -> list:
        """Detect faces in an image.
        
        Args:
            image_path: Path to the input image.
        
        Returns:
            List of detected faces (format varies by detector).
        """
        pass

    @abstractmethod
    def crop_face(self, image_path: str, output_path: str) -> str:
        """Crop and save the first detected face.
        
        Args:
            image_path: Path to the input image.
            output_path: Path to save the cropped face.
        
        Returns:
            Path to the cropped face image.
        """
        pass
    
    
"""from mtcnn import MTCNN
import cv2 #<=> the Haar det

class FaceDetector:
    def __init__(self):
        # Initialize MTCNN detector for high-accuracy face detection
        self.detector = MTCNN()

    def detect_faces(self, image_path):
        # Read and convert image to RGB (MTCNN expects RGB format)
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        # Detect faces and facial landmarks (eyes, nose, mouth)
        faces = self.detector.detect_faces(image)
        return faces  # Returns bounding boxes and landmarks

    def crop_face(self, image_path, output_path="face.jpg"):
        # Detect faces in the input image
        faces = self.detect_faces(image_path)
        if not faces:
            raise ValueError("No faces detected!")
        
        # Extract coordinates of the first detected face
        x, y, w, h = faces[0]['box']
        # Crop and save the face region
        image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        cropped_face = image[y:y+h, x:x+w]
        cv2.imwrite(output_path, cv2.cvtColor(cropped_face, cv2.COLOR_RGB2BGR))
        return output_path  # Path to the saved cropped face
"""