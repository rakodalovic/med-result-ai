"""Application configuration loaded from environment variables."""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    postgres_user: str = "admin"
    postgres_password: str = "admin"
    postgres_db: str = "medbot"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

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

    model_config = {"env_file": ".env"}


settings = Settings()
