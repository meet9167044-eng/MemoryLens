from collections import Counter
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.memory import Memory
from app.models.entity import Entity

router = APIRouter()

@router.get(
    "/insights",
    summary="Aggregate stats for the Insights dashboard",
    description="Returns memory counts, entity counts, top tags, and top entities.",
)
def get_insights(db: Session = Depends(get_db)) -> Dict[str, Any]:
    memories = db.query(Memory).all()
    total_memories = len(memories)

    total_entities = db.query(Entity).count()

    cutoff = datetime.utcnow() - timedelta(days=7)
    recent_activity_count = sum(
        1 for m in memories
        if m.created_at and m.created_at.replace(tzinfo=None) >= cutoff
    )

    all_tags: List[str] = []
    for m in memories:
        if m.tags and isinstance(m.tags, list):
            all_tags.extend(m.tags)
    tag_counts = Counter(all_tags).most_common(10)
    top_tags = [{"name": name, "count": count} for name, count in tag_counts]

    all_entities = db.query(Entity).all()
    entity_name_counts = Counter(e.name for e in all_entities).most_common(10)
    top_entities = [{"name": name, "count": count} for name, count in entity_name_counts]

    return {
        "total_memories": total_memories,
        "total_entities": total_entities,
        "recent_activity_count": recent_activity_count,
        "top_tags": top_tags,
        "top_entities": top_entities,
    }
