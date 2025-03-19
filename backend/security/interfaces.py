from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional


class JWTAuthManagerInterface(ABC):
    """
    Interface for JWT Authentication Manager.
    Defines methods for creating, decoding, and verifying JWT tokens.
    """

    @abstractmethod
    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new access token.
        """
        pass

    @abstractmethod
    def create_refresh_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a new refresh token.
        """
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> dict:
        """
        Decode and validate an access token.
        """
        pass

    @abstractmethod
    def decode_refresh_token(self, token: str) -> dict:
        """
        Decode and validate a refresh token.
        """
        pass
