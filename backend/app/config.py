from pathlib import Path
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[1]
ENV_FILE = BACKEND_DIR / ".env"


class Settings(BaseSettings):
    # Phase 2: Database
    DATABASE_URL: str = "sqlite:///./memorylens.db"

    # Phase 3: Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 50
    ALLOWED_MIME_TYPES: list[str] = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp",
        "image/bmp",
    ]

    # Phase A: Dataset Storage
    DATASET_STORAGE_PATH: str = "./data/dataset"

    # Phase B: LLM / AI Configuration
    LLM_PROVIDER: str = "groq"  # "groq" | "gemini" | "openai" | "stub"
    GEMINI_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GROQ_CHAT_MODEL: str = "openai/gpt-oss-20b"
    GROQ_VISION_MODEL: str = "openai/gpt-oss-20b"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"

    # Phase C: Embeddings
    EMBEDDING_PROVIDER: str = "local"  # "gemini" | "openai" | "local"
    EMBEDDING_MODEL: str = "text-embedding-004"
    EMBEDDING_DIMENSIONS: int = 768

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

# Ensure upload directory exists
UPLOAD_DIR = settings.UPLOAD_DIR if os.path.isabs(settings.UPLOAD_DIR) else BACKEND_DIR / settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Ensure dataset directories exist
DATASET_DIR = settings.DATASET_STORAGE_PATH if os.path.isabs(settings.DATASET_STORAGE_PATH) else BACKEND_DIR / settings.DATASET_STORAGE_PATH
os.makedirs(DATASET_DIR / "raw", exist_ok=True)
os.makedirs(DATASET_DIR / "thumbnails", exist_ok=True)
os.makedirs(DATASET_DIR / "metadata_cache", exist_ok=True)
