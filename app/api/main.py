from fastapi import FastAPI
from api.routes.enroll_routes import router as enroll_router
from api.routes.verify_routes import router as verify_router 
from api.routes.admin_routes import router as admin_router
app = FastAPI()

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(enroll_router, prefix="/enroll", tags=["Enrollment"])
app.include_router(verify_router, prefix="/verify", tags=["Verification"])
