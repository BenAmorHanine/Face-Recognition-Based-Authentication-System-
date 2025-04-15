from fastapi import FastAPI
from app.api.routes.enroll_routes import router as enroll_router
from app.api.routes.verify_routes import router as verify_router 
from app.api.routes.admin_routes import router as admin_router
app = FastAPI()
app.include_router(enroll_router, prefix="/api/v1") 

@app.get("/")
def read_root():
    return {"message": "Welcome to the FACE BASED AUTHENTIFICATION FastApi app!"}

app.include_router(admin_router) 
app.include_router(enroll_router , prefix="/enroll")
app.include_router(verify_router)

"""app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(enroll_router, prefix="/enroll", tags=["Enrollment"])
app.include_router(verify_router, prefix="/verify", tags=["Verification"])
"""