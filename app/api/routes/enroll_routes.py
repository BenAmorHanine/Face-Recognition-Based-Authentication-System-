from urllib.error import HTTPError
from fastapi import APIRouter, UploadFile, File, Form , HTTPException
from datetime import datetime
from typing import Dict, Tuple, List
import tempfile
import os
from app.authentification.auth_system import AuthSystem

router = APIRouter()
auth = AuthSystem()


@router.post("/enroll")
async def enroll_user(
    username: str = Form(...),
    image: UploadFile = File(...)
):
    """Handle user enrollment with face image"""
    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            contents = await image.read()
            tmp.write(contents)
            temp_path = tmp.name
        
        # Call your business logic
        success = auth.enroll(username, temp_path)
        
        # Cleanup
        os.unlink(temp_path)
        
        if success:
            return {
                "status": "success",
                "username": username,
                "timestamp": datetime.now().isoformat()
            }
        return {
            "status": "user_exists",
            "username": username
        }

    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPError as e:
        raise HTTPException(429, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")


@router.post("/enroll/batch")
async def batch_enroll_users(
    files: List[UploadFile] = File(..., description="List of files with usernames as field names")
):
    """Batch enroll with proper Swagger documentation"""
    try:
        user_data = {}
        for file in files:
            # Extract username from the field name
            username = file.filename.split('.')[0]  # Or use the field name directly
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                contents = await file.read()
                tmp.write(contents)
                user_data[username] = tmp.name

        results = auth.batch_enroll(user_data)
        
        # Cleanup
        for path in user_data.values():
            os.unlink(path)
            
        return results
        
    except Exception as e:
        # Cleanup on error
        for path in user_data.values():
            if os.path.exists(path):
                os.unlink(path)
        raise HTTPException(400, detail=str(e))
@router.get("/session")
async def get_session_status():
    """Exposes session information"""
    return auth.get_session_info()

