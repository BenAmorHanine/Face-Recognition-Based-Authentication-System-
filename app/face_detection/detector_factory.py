from .mtcnn_detector import MTCNNDetector
from .haar_detector import HaarDetector

class DetectorFactory:
    """Factory to create face detectors based on config."""
    
    @staticmethod
    def create_detector(detector_type: str):
        if detector_type == "mtcnn":
            return MTCNNDetector()
        elif detector_type == "haar":
            return HaarDetector()
        else:
            raise ValueError("Invalid detector type!")