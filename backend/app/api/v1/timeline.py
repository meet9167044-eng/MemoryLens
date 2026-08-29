from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.memory import Memory
from app.schemas.memories import MemoryResponse
from app.api.v1.memories import map_memory_to_response

router = APIRouter(prefix="/timeline", tags=["timeline"])

@router.get("", response_model=list[MemoryResponse])
def get_timeline(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    Get all memories ordered by created_at descending.
    This exactly mimics the frontend's Timeline behavior.
    """
    memories = db.query(Memory).order_by(Memory.created_at.desc()).offset(skip).limit(limit).all()
    return [map_memory_to_response(db, m) for m in memories]
