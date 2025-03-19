from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from core.settings import settings


class BaseModel(DeclarativeBase):
    """
        Base class for all SQLAlchemy models.

        This class serves as the declarative base for defining database models
        using SQLAlchemy's ORM. All model classes should inherit from this base.
    """
    pass


engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
    """
        Provide an asynchronous database session.

        This function creates an AsyncSession instance for database operations
        and yields it to the caller, ensuring the session is properly closed
        after use. Intended for use as a FastAPI dependency.

        Yields:
            AsyncSession: An asynchronous database session.

        Example:
            async def endpoint(db: AsyncSession = Depends(get_db)):
                # Use db here
                pass
    """
    async with async_session() as session:
        yield session
