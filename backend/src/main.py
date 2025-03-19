from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.routes import router as auth_router
from src.notes.routes import router as notes_router


app = FastAPI(
    title="Notes Management API",
)

origins = [
    "http://localhost:8080",
    "http://localhost:80",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"status": "ok"}

api_version_prefix = "/api/v1"
app.include_router(
    auth_router, prefix=f"{api_version_prefix}/auth", tags=["auth"]
)
app.include_router(
    notes_router, prefix=f"{api_version_prefix}/notes", tags=["notes"]
)
