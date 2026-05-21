from pathlib import Path

from pydantic_settings import BaseSettings

_backend_dir = Path(__file__).resolve().parent


class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite+aiosqlite:///{_backend_dir / 'code_quest.db'}"
    SECRET_KEY: str = "code-quest-dev-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    SANDBOX_TIMEOUT: int = 5
    SANDBOX_MAX_MEMORY_MB: int = 128

    PYTHON_PATH: str = "python"

    class Config:
        env_file = ".env"


settings = Settings()
