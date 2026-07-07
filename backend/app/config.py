"""Application configuration, loaded from environment / .env."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # SQLite by default so the slice runs with zero setup.
    # Swap to Postgres/Supabase by setting DATABASE_URL, e.g.
    #   postgresql+psycopg2://user:pass@host:5432/dbname
    database_url: str = "sqlite:///./study_platform.db"

    # Auth
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 days

    # Code execution sandbox
    code_timeout_seconds: int = 5
    max_code_length: int = 20_000

    # CORS — the Next.js dev server
    frontend_origin: str = "http://localhost:3000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
