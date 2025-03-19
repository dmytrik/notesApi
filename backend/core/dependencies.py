from fastapi import Depends, HTTPException, status, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from security.exceptions import BaseSecurityError
from security.interfaces import JWTAuthManagerInterface
from security.jwt_manager import JWTAuthManager
from core.settings import settings
from src.auth.models import UserModel


def get_jwt_auth_manager() -> JWTAuthManagerInterface:
    """
    Create an instance of JWTAuthManager for token management.

    Returns:
        An instance of JWTAuthManager implementing JWTAuthManagerInterface.

    Example:
        jwt_manager = get_jwt_auth_manager()
        token = jwt_manager.create_access_token({"user_id": 1})
    """
    return JWTAuthManager(
        secret_key_access=settings.secret_key_access,
        secret_key_refresh=settings.secret_key_refresh,
        algorithm=settings.jwt_signing_algorithm,
    )


def get_token(request: Request) -> str:
    """
    Extract the Bearer token from the Authorization header.

    Args:
        request: The incoming HTTP request containing headers.

    Returns:
        The extracted Bearer token as a string.

    Raises:
        HTTPException:
            - 401 if the Authorization header is missing.
            - 401 if the Authorization header format is invalid (not 'Bearer <token>').
    """
    authorization: str = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format. Expected 'Bearer <token>'",
        )

    return token


async def get_current_user(
    token: str = Depends(get_token),
    jwt_manager: JWTAuthManagerInterface = Depends(get_jwt_auth_manager),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """
    Retrieve the current authenticated user based on the provided access token.

    Args:
        token: The Bearer token extracted from the Authorization header.
        jwt_manager: The JWT manager for decoding the token.
        db: The asynchronous database session for querying the user.

    Returns:
        The authenticated UserModel instance.

    Raises:
        HTTPException:
            - 401 if the token is invalid, expired, or the user is not found.
    """
    try:
        payload = jwt_manager.decode_access_token(token)
        user_id = payload.get("user_id")
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return user
    except BaseSecurityError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )
