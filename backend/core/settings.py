from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration settings for the application."""

    environment: str

    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def db_host(self) -> str:
        """Return the database host based on the environment."""
        if self.environment == "local":
            return "localhost"
        return "db"

    @property
    def database_url(self) -> str:
        """Generate the database URL based on the environment."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.postgres_port}/{self.postgres_db}"
        )

settings = Settings()