from datetime import datetime

from sqlalchemy import (
    Integer,
    DateTime,
    ForeignKey,
    Text,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel


class NoteModel(BaseModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    previous_version_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note {self.user.email} \n {self.text}>"
