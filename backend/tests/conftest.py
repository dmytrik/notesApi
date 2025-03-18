import asyncio

import pytest
import httpx
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from jose import jwt

from core.database import BaseModel, get_db
from core.settings import settings
from src.main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

SECRET_KEY = settings.secret_key_access
ALGORITHM = settings.jwt_signing_algorithm


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(async_engine):
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db

    async with LifespanManager(app):
        async with AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test/api/v1"
        ) as ac:
            yield ac


@pytest.fixture
def token():
    payload = {"user_id": 1, "exp": 1744910000}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
