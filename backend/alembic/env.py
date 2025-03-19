import asyncio

from alembic import context

from core.database import engine, BaseModel
from core.settings import settings
from src.auth.models import UserModel  # noqa 401
from src.notes.models import NoteModel  # noqa 401


config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = BaseModel.metadata


async def run_migrations_offline():
    with engine.connect() as connection:
        context.configure(
            connection=connection.sync_connection,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )
        with context.begin_transaction():
            context.run_migrations()


async def run_migrations_online():
    async with engine.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                render_as_batch=True,
            )
        )
        async with connection.begin():
            await connection.run_sync(
                lambda sync_conn: context.run_migrations()
            )


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
