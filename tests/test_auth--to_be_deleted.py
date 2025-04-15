"""Tests critical components using pytest.
Uses an in-memory database to avoid polluting the real database."""
import pytest
from app.authentification.enroll import Enrollment
from app.authentification.verify import Verifier
from app.database.db_handler import FaceDatabase

@pytest.fixture
def test_db():
    return FaceDatabase(":memory:")

def test_enrollment(test_db):
    enroller = Enrollment()
    assert enroller.enroll_user("test_user", "test_image.jpg") is True

def test_verification(test_db):
    verifier = Verifier()
    test_embedding = [0.1] * 128  # Mock embedding
    test_db.save_user("test_user", test_embedding)
    assert verifier.verify_user(test_embedding) == "test_user"