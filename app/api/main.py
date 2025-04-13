from fastapi import FastAPI
from api.routes import admin_routes, enroll_routes, verify_routes  # adjust import paths as needed

app = FastAPI()

app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(enroll_routes.router, prefix="/enroll", tags=["Enrollment"])
app.include_router(verify_routes.router, prefix="/verify", tags=["Verification"])
