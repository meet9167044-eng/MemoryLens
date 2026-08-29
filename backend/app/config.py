from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    # Phase 2: Database
    DATABASE_URL: str
    # Phase 3: Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 20
    ALLOWED_MIME_TYPES: list = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",   # ignore Phase 1 vars (PROJECT_NAME etc.) safely
        case_sensitive=False,
    )


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
