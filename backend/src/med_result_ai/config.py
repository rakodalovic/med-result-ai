"""Application configuration loaded from environment variables."""

from dotenv import find_dotenv, load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))


class Settings(BaseSettings):
    """Application settings."""

    postgres_user: str = "admin"
    postgres_password: str = "admin"  # noqa: S105
    postgres_db: str = "medbot"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    upload_dir: str = "uploads"
    openrouter_api_key: str = ""
    openrouter_model: str = "google/gemma-3-27b-it:free"

    @property
    def database_url(self) -> PostgresDsn:
        """Build the postgresql connection url."""
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )


settings = Settings()
