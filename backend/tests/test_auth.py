from datetime import (
    datetime,
    timezone,
    timedelta
)

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings
from src.auth.models import UserModel, RefreshTokenModel
from core.dependencies import get_jwt_auth_manager


jwt_auth_manager = get_jwt_auth_manager()


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient, db_session: AsyncSession):
    payload = {"email": "test@example.com", "password": "StrongPass123!"}
    response = await client.post("/auth/register/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert "email" in response.json()

    user = await db_session.get(UserModel, 1)
    assert user is not None
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient, db_session: AsyncSession):
    user = UserModel(email="test2@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    payload = {"email": "test2@example.com", "password": "AnotherPass123!"}
    response = await client.post("/auth/register/", json=payload)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()["detail"] == "A user with this email test2@example.com already exists."


@pytest.mark.asyncio
async def test_login_user_success(client: AsyncClient, db_session: AsyncSession):
    user = UserModel(email="login@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    payload = {"email": "login@example.com", "password": "StrongPass123!"}
    response = await client.post("/auth/login/", json=payload)  # Зміна на json замість data

    assert response.status_code == status.HTTP_201_CREATED
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient, db_session: AsyncSession):
    user = UserModel(email="invalid@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    payload = {"email": "invalid@example.com", "password": "WrongPass12!"}
    response = await client.post("/auth/login/", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password."


@pytest.mark.asyncio
async def test_refresh_token_success(
        client: AsyncClient,
        db_session: AsyncSession,
):
    user = UserModel(email="refresh@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = jwt_auth_manager.create_refresh_token({"user_id": user.id})

    refresh_token = RefreshTokenModel(
        token=token,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.refresh_time_days)
    )
    db_session.add(refresh_token)
    await db_session.commit()

    response = await client.post(
        "/auth/refresh/",
        json={"refresh_token": token}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient, db_session: AsyncSession):
    response = await client.post(
        "/auth/refresh/",
        json={"refresh_token": "invalid_token"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()
