from fastapi import FastAPI

from src.auth.routes import router as auth_router


app = FastAPI(
    title="Notes Management API",
)

api_version_prefix = "/api/v1"
app.include_router(auth_router, prefix=f"{api_version_prefix}/auth", tags=["auth"])
