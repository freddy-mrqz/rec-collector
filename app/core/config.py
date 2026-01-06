from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App settings
    app_name: str = "Records Collector API"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./records.db"

    # JWT Settings
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Discogs OAuth
    discogs_consumer_key: str = ""
    discogs_consumer_secret: str = ""
    discogs_callback_url: str = "http://localhost:8000/api/v1/discogs/callback"

    # Encryption key for storing OAuth tokens
    token_encryption_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
