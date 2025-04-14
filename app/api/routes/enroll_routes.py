from urllib.error import HTTPError
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from typing import Dict, Tuple, List
import tempfile
import os
from app.authentification.auth_system import AuthSystem

router = APIRouter()
auth = AuthSystem()

@router.post("/")
@router.post("/enroll")
async def enroll_user(username: str, image: UploadFile = File(...)): # <=>File(required=True)
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



@router.post("/enroll/batch")
async def batch_enroll_users(user_data: Dict[str, UploadFile] = File(...)):
    """Implementation of batch_enroll() with file handling"""
    try:
        # Prepare {username: temp_path} dictionary
        temp_files = {}
        results = {}
        
        for username, file in user_data.items():
            # Save each file to temp location
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp.write(await file.read())
                temp_files[username] = tmp.name
        
        # Process batch enrollment
        batch_result = auth.batch_enroll(temp_files)
        
        # Cleanup temp files
        for path in temp_files.values():
            os.unlink(path)
            
        return batch_result
        
    except Exception as e:
        # Cleanup any remaining files on error
        for path in temp_files.values():
            if os.path.exists(path):
                os.unlink(path)
        raise HTTPException(400, detail=str(e))


@router.get("/session")
async def get_session_status():
    """Exposes session information"""
    return auth.get_session_info()

