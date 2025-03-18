import asyncio

from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException
)
from google.api_core import exceptions
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user
from core.utils import summarize_note
from src.auth.models import UserModel
from src.notes.models import NoteModel
from src.notes.schemas import (
    NoteCreateResponseSchema,
    NoteCreateRequestSchema,
    NoteBaseSchema, NoteUpdateRequestSchema
)


router = APIRouter()


@router.get(
    "/",
    response_model=list[NoteBaseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get All Notes",
    description="Retrieve a list of all notes from the database. Accessible to authenticated users.",
    responses={
        500: {
            "description": "Internal Server Error - Database error occurred.",
            "content": {
                "application/json": {
                    "example": {"detail": "Database connection failed"}
                }
            }
        }
    }
)
async def get_notes(
        db: AsyncSession = Depends(get_db),
        current_user: UserModel = Depends(get_current_user) # noqa F401
):
    try:
        stmt = select(NoteModel)
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post(
    "/",
    response_model=NoteCreateResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Note",
    description="Create a new note with text and automatically generated summary using Gemini API. Requires authentication.",
    responses={
        504: {
            "description": "Gateway Timeout - Summarization took too long.",
            "content": {
                "application/json": {
                    "example": {"detail": "Summarization took too long"}
                }
            }
        },
        503: {
            "description": "Service Unavailable - Gemini API error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Gemini API error: Failed to connect"}
                }
            }
        },
        500: {
            "description": "Internal Server Error - Database or unexpected error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to create note"}
                }
            }
        }
    }
)
async def create_note(
        note_data: NoteCreateRequestSchema,
        db: AsyncSession = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):

    try:
        note_summary = await asyncio.wait_for(summarize_note(note_data.text), timeout=10)
        note = NoteModel(
            text=note_data.text,
            summary=note_summary,
            user_id=user.id,
        )
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Summarization took too long")
    except exceptions.GoogleAPIError as api_err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Gemini API error: {str(api_err)}")
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note"
        )


@router.get(
    "/{note_id}/",
    response_model=NoteBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a Specific Note",
    description="Retrieve a single note by its ID. Accessible to authenticated users.",
    responses={
        404: {
            "description": "Not Found - Note with the specified ID does not exist.",
            "content": {
                "application/json": {
                    "example": {"detail": "Note not found"}
                }
            }
        },
        500: {
            "description": "Internal Server Error - Database error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to create note"}
                }
            }
        }
    }
)
async def get_note(
        note_id: int,
        db: AsyncSession = Depends(get_db),
        user: UserModel = Depends(get_current_user) # noqa F401
):
    try:
        stmt = select(NoteModel).where(NoteModel.id == note_id)
        result = await db.execute(stmt)
        note = result.scalars().first()

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return note
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create note"
        )


@router.patch(
    "/{note_id}/",
    response_model=NoteBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Update a Note",
    description="Update an existing note by creating a new version with the provided text and summary. Requires authentication.",
    responses={
        404: {
            "description": "Not Found - Note with the specified ID does not exist.",
            "content": {
                "application/json": {
                    "example": {"detail": "Note not found"}
                }
            }
        },
        504: {
            "description": "Gateway Timeout - Summarization took too long.",
            "content": {
                "application/json": {
                    "example": {"detail": "Summarization took too long"}
                }
            }
        },
        503: {
            "description": "Service Unavailable - Gemini API error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Gemini API error: Failed to connect"}
                }
            }
        },
        500: {
            "description": "Internal Server Error - Database or unexpected error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to update note"}
                }
            }
        }
    }
)
async def update_note(
        note_id: int,
        note_data: NoteUpdateRequestSchema,
        db: AsyncSession = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        stmt = select(NoteModel).where(NoteModel.id == note_id)
        result = await db.execute(stmt)
        note = result.scalars().first()

        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        note_summary = await asyncio.wait_for(summarize_note(note_data.text), timeout=10)
        note = NoteModel(
            text=note_data.text,
            previous_version_id=note_id,
            summary=note_summary,
            user_id=user.id,
        )
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note
    except asyncio.TimeoutError:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Summarization took too long")
    except exceptions.GoogleAPIError as api_err:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Gemini API error: {str(api_err)}")
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update note"
        )


@router.delete(
    "/{note_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a Note",
    description="Delete a note by its ID, updating version history if necessary. Requires authentication and ownership.",
    responses={
        404: {
            "description": "Not Found - Note not found or user lacks permission.",
            "content": {
                "application/json": {
                    "example": {"detail": "Note not found or you don't have permission"}
                }
            }
        },
        500: {
            "description": "Internal Server Error - Database error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Failed to delete note"}
                }
            }
        }
    }
)
async def delete_note(
        note_id: int,
        db: AsyncSession = Depends(get_db),
        user: UserModel = Depends(get_current_user)
):
    try:
        stmt = select(NoteModel).where(
            NoteModel.id == note_id,
            NoteModel.user_id == user.id
        )
        result = await db.execute(stmt)
        note = result.scalars().first()
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found or you don't have permission"
            )
        parent_stmt = select(NoteModel).where(NoteModel.previous_version_id == note_id)
        parent_result = await db.execute(parent_stmt)
        parent_note = parent_result.scalars().first()

        if parent_note:
            if not note.previous_version_id:
                parent_note.previous_version_id = None
            else:
                child_stmt = select(NoteModel).where(NoteModel.id == note.previous_version_id)
                child_result = await db.execute(child_stmt)
                child_note = child_result.scalars().first()
                if child_note:
                    parent_note.previous_version_id = child_note.id
                else:
                    parent_note.previous_version_id = None

        await db.delete(note)
        await db.commit()
        return None
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete note"
        )
