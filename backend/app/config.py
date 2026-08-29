from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URL: str
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 20
    ALLOWED_MIME_TYPES: list = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
