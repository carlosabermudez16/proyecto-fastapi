from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str
    DATABASE_URL: str
    TEST_DATABASE_URL: str
    DEBUG: bool = False
    SLACK_WEBHOOK_URL: str | None = None

    model_config = SettingsConfigDict(
        env_file=(".env", ".env_example"),
        case_sensitive=True,
        extra="ignore",  # 👈 permite variables extra
    )


settings = Settings()  # para usar en lógica de negocio y test


# para usar en endpoints
@lru_cache
def get_settings() -> Settings:
    return settings
