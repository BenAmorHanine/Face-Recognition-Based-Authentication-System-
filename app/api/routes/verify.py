from urllib.error import HTTPError
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
import tempfile
import os

import numpy as np
from app.authentification.auth_system import AuthSystem

router = APIRouter()
auth = AuthSystem()


"""you can use : POST /verify → defaults to memory mode.
or POST /verify?use_memory=false → forces file-based verification."""
@router.post("/")
@router.post("/verify")
async def verify_user(
    image: UploadFile = File(...), 
    use_memory: bool = True  # <- Optional flag
):
    """Direct implementation of your verify methods"""
    try:
        if use_memory:
            img_array = np.frombuffer(await image.read(), np.uint8)
            result = auth.verify_from_memory(img_array)
        else:
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                tmp.write(await image.read())
                temp_path = tmp.name
            result = auth.verify(temp_path)
            os.unlink(temp_path)

        if result is None:
            return {"user": None, "confidence": 0.0}
        elif isinstance(result, str):
            return {"user": None, "status": result.lower()}
        else:
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

