from fastapi import APIRouter, HTTPException
from app.authentification.auth_system import AuthSystem

router = APIRouter()
auth = AuthSystem()

@router.post("/users/{username}/deactivate")
async def deactivate_user(username: str):
    """Direct implementation of deactivate_user()"""
    try:
        success = auth.deactivate_user(username)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        else:
            return {"status": "success"}, 200
        
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@router.post("/users/{username}/reactivate")
async def reactivate_user(username: str):
    try:
        success = auth.reactivate_user(username)
        return {"status": "success" if success else "user_not_found"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/users")
async def list_users():
    try:
        return {"users": auth.list_users()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{username}/status")
async def user_status(username: str):
    try:
        return auth.get_user_status(username)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rate-limit")
async def get_rate_limit_status():
    """Exposes get_remaining_attempts()"""
    return {
        "remaining_attempts": auth.get_remaining_attempts(),
        "max_attempts": auth.MAX_ATTEMPTS
    }

@router.post("/rate-limit/reset")
async def reset_rate_limit() -> dict:
    """Exposes reset_attempts()"""
    auth.reset_attempts()
    return {"status": "success"}, 200