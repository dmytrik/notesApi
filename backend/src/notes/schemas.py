from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from src.notes.validators import validate_note


class NoteBaseSchema(BaseModel):
    id: int
    text: str
    previous_version_id: Optional[int] = None
    summary: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class NoteCreateRequestSchema(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_note(cls, value: str) -> str:
        return validate_note(value)


class NoteCreateResponseSchema(NoteBaseSchema):
    pass


class NoteUpdateRequestSchema(NoteCreateRequestSchema):
    pass
