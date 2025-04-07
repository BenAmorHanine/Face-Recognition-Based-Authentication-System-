"""
Authentication Package

Exposes key classes for face recognition-based enrollment and verification.
"""

# Import core components to simplify external access
from .auth_system import AuthSystem
from .enroll import Enrollment
from .verify import Verifier

# Define public API for "from authentication import *"
__all__ = ["AuthSystem", "Enrollment", "Verifier"]