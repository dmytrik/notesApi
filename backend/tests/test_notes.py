import asyncio

import pytest
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.notes import routes
from src.auth.models import UserModel, NoteModel
from unittest.mock import AsyncMock
from core.dependencies import get_jwt_auth_manager


jwt_auth_manager = get_jwt_auth_manager()


@pytest.mark.asyncio
async def test_get_notes_success(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test successful retrieval of all notes.

    Verifies that an authenticated user can retrieve their notes from the database.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user = UserModel(email="notes@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    note = NoteModel(text="Test note", user_id=user.id, summary="Summary")
    db_session.add(note)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/notes/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["text"] == "Test note"


@pytest.mark.asyncio
async def test_create_note_success(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test successful creation of a note.

    Verifies that an authenticated user can create a note with a generated summary.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user = UserModel(email="create@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    mocker.patch.object(
        routes,
        "summarize_note",
        new_callable=AsyncMock,
        return_value="Summary",
    )

    payload = {"text": "New note"}
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/notes/", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["text"] == "New note"
    assert response.json()["summary"] == "Summary"


@pytest.mark.asyncio
async def test_create_note_timeout(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test note creation with a summarization timeout.

    Verifies that a timeout during summarization returns a gateway timeout error.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user = UserModel(email="timeout@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    mocker.patch.object(
        routes,
        "summarize_note",
        new_callable=AsyncMock,
        side_effect=asyncio.TimeoutError,
    )

    payload = {"text": "New note"}
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.post("/notes/", json=payload, headers=headers)

    assert response.status_code == status.HTTP_504_GATEWAY_TIMEOUT
    assert response.json()["detail"] == "Summarization took too long"


@pytest.mark.asyncio
async def test_get_note_success(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test successful retrieval of a specific note.

    Verifies that an authenticated user can retrieve a note by its ID.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user = UserModel(email="getnote@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    note = NoteModel(text="Test note", user_id=user.id, summary="Summary")
    db_session.add(note)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get(f"/notes/{note.id}/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "Test note"
    assert response.json()["summary"] == "Summary"


@pytest.mark.asyncio
async def test_get_note_not_found(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test retrieval of a non-existent note.

    Verifies that requesting a note with an invalid ID returns a not found error.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user = UserModel(email="notfound@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/notes/999/", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Note not found"


@pytest.mark.asyncio
async def test_update_note_success(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test successful update of a note.

    Verifies that an authenticated user can update a note with new text and summary.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user = UserModel(email="update@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()

    note = NoteModel(text="Old note", user_id=user.id, summary="Old summary")
    db_session.add(note)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    mocker.patch.object(
        routes,
        "summarize_note",
        new_callable=AsyncMock,
        return_value="New summary",
    )

    payload = {"text": "Updated note"}
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.patch(
        f"/notes/{note.id}/", json=payload, headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["text"] == "Updated note"
    assert response.json()["summary"] == "New summary"


@pytest.mark.asyncio
async def test_delete_note_success(
    client: AsyncClient, db_session: AsyncSession, mocker
):
    """
    Test successful deletion of a note.

    Verifies that an authenticated user can delete their own note
    and it is removed from the database.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
    """
    user = UserModel(email="delete@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    token = jwt_auth_manager.create_access_token({"user_id": user.id})

    note = NoteModel(text="Test note", user_id=user.id, summary="Summary")
    db_session.add(note)
    await db_session.commit()
    await db_session.refresh(note)

    mocker.patch("core.dependencies.get_current_user", return_value=user)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete(f"/notes/{note.id}/", headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    deleted_note = await db_session.get(NoteModel, note.id)
    assert deleted_note is None


@pytest.mark.asyncio
async def test_delete_note_not_owner(
    client: AsyncClient, db_session: AsyncSession, mocker, token
):
    """
    Test deletion of a note by a non-owner.

    Verifies that a user cannot delete a note they do not own,
    resulting in a not found error.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
        token: The JWT token fixture for authentication.
    """
    user1 = UserModel(email="user1@example.com", password="StrongPass123!")
    user2 = UserModel(email="user2@example.com", password="StrongPass123!")
    db_session.add_all([user1, user2])
    await db_session.commit()

    note = NoteModel(text="Test note", user_id=user1.id, summary="Summary")
    db_session.add(note)
    await db_session.commit()

    mocker.patch("core.dependencies.get_current_user", return_value=user2)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete(f"/notes/{note.id}/", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert (
        response.json()["detail"]
        == "Note not found or you don't have permission"
    )


@pytest.mark.asyncio
async def test_get_notes_analytics_success(
    client: AsyncClient, db_session: AsyncSession, mocker
):
    """
    Test successful retrieval of note analytics.

    Verifies that an authenticated user can retrieve analytics for their notes.

    Args:
        client: The asynchronous HTTP client for making requests.
        db_session: The asynchronous database session for database operations.
        mocker: The pytest-mock fixture for mocking dependencies.
    """
    user = UserModel(email="analytics@example.com", password="StrongPass123!")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    notes = [
        NoteModel(
            text="This is a test note", user_id=user.id, summary="Summary1"
        ),
        NoteModel(text="Short note", user_id=user.id, summary="Summary2"),
    ]
    db_session.add_all(notes)
    await db_session.commit()
    token = jwt_auth_manager.create_access_token({"user_id": user.id})
    mocker.patch("core.dependencies.get_current_user", return_value=user)
    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/notes/analytics/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total_word_count"] == 7
