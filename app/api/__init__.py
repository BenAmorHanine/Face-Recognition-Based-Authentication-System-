# app/api/__init__.py
from fastapi import APIRouter, Depends
from app.api.routes.enroll_routes import router as enroll_router
from routes.verify import router as verify_router
from app.api.routes.admin_routes import router as admin_router
from app.authentification.auth_system import AuthSystem
# Main API router
api_router = APIRouter()

# Include all route files with proper prefixes and tags
api_router.include_router(
    enroll_router,
    prefix="/enroll",
    tags=["Enrollment"]
)

api_router.include_router(
    verify_router,
    prefix="/verify",
    tags=["Verification"]
)

api_router.include_router(
    admin_router,
    prefix="/admin",
    tags=["Administration"]
)

# Health check endpoint (optional)
# This endpoint is used to verify that the API is running and healthy.
# It is excluded from the OpenAPI schema documentation.
@api_router.get("/deep-health")
async def deep_health(auth: AuthSystem = Depends()):
    return {
        "api_online": True,
        "database_connected": auth.verifier.db is not None,
        "models_loaded": hasattr(auth.enroller, 'model')
    } 

# For backwards compatibility
__all__ = ["api_router"]