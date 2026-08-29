from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import List


class Settings(BaseSettings):
    # Phase 2: Database
    DATABASE_URL: str
    # Phase 3: Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_MIME_TYPES: list = ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp"]

    # Phase A: Dataset Storage
    DATASET_STORAGE_PATH: str = "./data/dataset"

    # Phase B: LLM / AI Configuration
    LLM_PROVIDER: str = "gemini"           # "gemini" | "openai" | "stub"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # Phase C: Embeddings
    EMBEDDING_PROVIDER: str = "gemini"     # "gemini" | "openai" | "local"
    EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_DIMENSIONS: int = 768

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
# Ensure dataset directories exist
os.makedirs(f"{settings.DATASET_STORAGE_PATH}/raw", exist_ok=True)
os.makedirs(f"{settings.DATASET_STORAGE_PATH}/thumbnails", exist_ok=True)
os.makedirs(f"{settings.DATASET_STORAGE_PATH}/metadata_cache", exist_ok=True)
