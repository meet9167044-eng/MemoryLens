import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# pool_size / max_overflow are only valid for PostgreSQL (not SQLite)
_is_sqlite = settings.DATABASE_URL.startswith("sqlite")
_engine_kwargs: dict = {"pool_pre_ping": True, "echo": False}
if not _is_sqlite:
    _engine_kwargs.update({"pool_size": 10, "max_overflow": 20})

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yields a DB session; closes it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
