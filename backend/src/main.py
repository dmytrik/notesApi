import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import nltk

from src.auth.routes import router as auth_router
from src.notes.routes import router as notes_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    try:
        nltk.download("punkt_tab", quiet=True)
        logger.info("NLTK punkt_tab downloaded successfully")
    except Exception as e:
        logger.error(f"Failed to download NLTK punkt_tab: {str(e)}")
    logger.info("Application started")

    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="Notes Management API",
    lifespan=lifespan
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
