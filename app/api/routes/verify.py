from urllib.error import HTTPError
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
import tempfile
import os

import numpy as np
from app.authentification.auth_system import AuthSystem

router = APIRouter()
auth = AuthSystem()

@router.post("/verify")
async def verify_face(image: UploadFile = File(...)):
    """Direct implementation of your verify methods"""
    try:
        # Convert upload to numpy array
        img_array = np.frombuffer(await image.read(), np.uint8)
        
        # Use your existing verify_from_memory if available
        if hasattr(auth, 'verify_from_memory'):
            result = auth.verify_from_memory(img_array)
        else:
            # Fallback to file-based verification
            with tempfile.NamedTemporaryFile(suffix='.jpg') as tmp:
                tmp.write(await image.read())
                result = auth.verify(tmp.name)
        
        # Format response according to your existing return types
        if result is None:
            return {"user": None, "confidence": 0.0}
        elif isinstance(result, str):  # "SPOOF_ATTEMPT" case
            return {"user": None, "status": result.lower()}
        else:  # Tuple (username, confidence) case
            username, confidence = result
            return {
                "user": username,
                "confidence": float(confidence),
                "remaining_attempts": auth.get_remaining_attempts()
            }
            
    except HTTPError as e:
        raise HTTPException(429, detail="Too many attempts")
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