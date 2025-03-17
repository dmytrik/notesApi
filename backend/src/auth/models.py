from datetime import datetime, timezone, timedelta

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.database import BaseModel
from src.notes.models import NoteModel
from core.utils import hash_password, verify_password
from src.auth.validators import validate_password_strength


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    _hashed_password: Mapped[str] = mapped_column(
        "hashed_password", String(255), nullable=False
    )

    notes: Mapped[list["NoteModel"]] = relationship("NoteModel", back_populates="user")
    refresh_tokens: Mapped[list["RefreshTokenModel"]] = relationship(
        "RefreshTokenModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    @property
    def password(self) -> None:
        raise AttributeError(
            "Password is write-only. Use the setter to set the password."
        )

    @password.setter
    def password(self, raw_password: str) -> None:
        validate_password_strength(raw_password)
        self._hashed_password = hash_password(raw_password)

    def verify_password(self, raw_password: str) -> bool:
        """
        Verify the provided password against the stored hashed password.
        """
        return verify_password(raw_password, self._hashed_password)

    def __repr__(self) -> str:
        return f"<User {self.email}>"


class RefreshTokenModel(BaseModel):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(
        String(512),
        unique=True,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped[UserModel] = relationship("UserModel", back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshTokenModel(id={self.id}, token={self.token}, expires_at={self.expires_at})>"
