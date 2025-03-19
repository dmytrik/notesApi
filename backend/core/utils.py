import asyncio

from google import generativeai as genai
from passlib.context import CryptContext

from core.settings import settings


genai.configure(api_key=settings.gemini_api_key)

pwd_context = CryptContext(
    schemes=["bcrypt"], bcrypt__rounds=14, deprecated="auto"
)


async def summarize_note(text: str) -> str:
    """
    Generate a short summary for the given note text using Gemini API.

    This function asynchronously calls the Gemini API to create a brief description
    of the provided text by running the model in a separate thread.

    Args:
        text: The text of the note to summarize.

    Returns:
        A string containing the generated summary.

    Raises:
        asyncio.CancelledError: If the task is cancelled before completion.
        Exception: If the Gemini API call fails (e.g., network issues).
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Write short description for {text}"
    task = asyncio.create_task(
        asyncio.to_thread(model.generate_content, prompt)
    )
    response = await task
    return response.text


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: The plain text password to hash.

    Returns:
        The hashed password as a string.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
