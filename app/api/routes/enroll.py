from urllib.error import HTTPError
from fastapi import APIRouter, UploadFile, File, HTTPException
import numpy as np
from datetime import datetime
import cv2
import tempfile
import os
from app.authentification.auth_system import AuthSystem

router = APIRouter()
auth = AuthSystem()

@router.post("/enroll")
async def enroll_user(username: str, image: UploadFile = File(...)):
    """Direct implementation of your enroll() method"""
    try:
        # Save uploaded file to temp location (matches your file path interface)
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            contents = await image.read()
            tmp.write(contents)
            temp_path = tmp.name
        
        # Call your existing enroll method
        success = auth.enroll(username, temp_path)
        
        # Cleanup
        os.unlink(temp_path)
        
        return {
            "status": "success" if success else "user_exists",
            "username": username
        }
    except HTTPError as e:
        raise HTTPException(429, detail=str(e))
    except Exception as e:
        raise HTTPException(400, detail=str(e))
    
@router.get("/session")
async def get_session_status():
    """Exposes session information"""
    return {
        "session_start": auth.session_start,
        "session_duration": str(datetime.now() - auth.session_start)
    }

