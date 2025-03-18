import asyncio

from google import generativeai as genai
from passlib.context import CryptContext

from core.settings import settings


genai.configure(api_key=settings.gemini_api_key)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=14,
    deprecated="auto"
)


async def summarize_note(text: str) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Write short description for {text}"
    task = asyncio.create_task(
        asyncio.to_thread(model.generate_content, prompt)
    )
    response = await task
    return response.text

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
