from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from src.notes.validators import validate_note


class NoteBaseSchema(BaseModel):
    """
        Base schema for note data.

        Defines the common structure for note-related responses,
        including core fields
        and metadata, with support for ORM mapping.
    """

    id: int
    text: str
    previous_version_id: Optional[int] = None
    summary: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class NoteCreateRequestSchema(BaseModel):
    """
        Schema for creating a new note request.

        Defines the structure and validation for creating a note,
        requiring only the text field.
    """

    text: str

    @field_validator("text")
    @classmethod
    def validate_note(cls, value: str) -> str:
        """
            Validate the note text using a custom validator.

            Args:
                value: The note text to validate.

            Returns:
                 The validated note text.
        """
        return validate_note(value)


class NoteCreateResponseSchema(NoteBaseSchema):
    """
        Schema for note creation response.

        Inherits all fields from NoteBaseSchema to represent the response
        after successfully creating a note.
    """
    pass


class NoteUpdateRequestSchema(NoteCreateRequestSchema):
    """
        Schema for updating a note request.

        Inherits the text field and validation from NoteCreateRequestSchema
        for updating an existing note.
    """
    pass


class NoteAnalyticsResponseSchema(BaseModel):
    """
        Schema for note analytics response.

        Defines the structure of the response containing
        statistical data about notes,
        including word counts, averages, and rankings.
    """

    total_word_count: int
    average_note_length: float
    most_common_words: list[list]
    top_3_longest_notes: list[dict]
    top_3_shortest_notes: list[dict]
