from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel


class NoteModel(BaseModel):
    """
    Database model representing a note.

    This model stores note information including text, summary, and versioning,
    with a relationship to the owning user.
    """

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    previous_version_id: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel", back_populates="notes"
    )  # noqa F821

    def __repr__(self) -> str:
        """
        Return a string representation of the NoteModel instance.

        Returns:
            A string in the format '<Note user_email text>'.
        """
        return f"<Note {self.user.email} \n {self.text}>"
