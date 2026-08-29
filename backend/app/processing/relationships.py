"""
Phase 9 - Relationship Engine
------------------------------
Compares a Memory to all existing Memories and generates
Relationship records based on:
  1. Shared entities  (same entity name, case-insensitive)
  2. Shared tags      (overlap in memory.tags JSON array)
  3. Semantic similarity (placeholder – real cosine similarity once
     pgvector embeddings land from Phase 7)

Design rules (from spec):
  - source_id is always the lexicographically SMALLER UUID so the
    (source_id, target_id, rel_type) unique constraint prevents
    duplicate undirected rows.
  - Score is a float 0.0–1.0.
"""

from __future__ import annotations

import logging
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.memory import Memory
from app.models.entity import Entity
from app.models.relationship import Relationship, RelationshipType

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _ordered_ids(a: UUID, b: UUID) -> tuple[UUID, UUID]:
    """Return (smaller_uuid, larger_uuid) so pairs are always canonical."""
    return (a, b) if str(a) < str(b) else (b, a)


def _upsert_relationship(
    db: Session,
    source_id: UUID,
    target_id: UUID,
    rel_type: RelationshipType,
    score: float,
    explanation: str,
) -> Relationship:
    """
    Insert or update a Relationship row.
    Returns the Relationship object (not yet committed – caller commits).
    """
    src, tgt = _ordered_ids(source_id, target_id)

    existing = (
        db.query(Relationship)
        .filter_by(source_id=src, target_id=tgt, rel_type=rel_type)
        .first()
    )
    if existing:
        # Update if the new score is higher
        if score > existing.score:
            existing.score = score
            existing.explanation = explanation
        return existing

    rel = Relationship(
        source_id=src,
        target_id=tgt,
        rel_type=rel_type,
        score=score,
        explanation=explanation,
    )
    db.add(rel)
    return rel


# ─────────────────────────────────────────────
# Scoring functions
# ─────────────────────────────────────────────

def _score_shared_entities(
    memory_a: Memory,
    memory_b: Memory,
    entities_a: list[Entity],
    entities_b: list[Entity],
) -> tuple[float, str]:
    """
    Score based on number of shared entity names (case-insensitive).
    Score = shared / max(total_unique_a, total_unique_b), capped at 1.0
    """
    names_a = {e.name.lower() for e in entities_a}
    names_b = {e.name.lower() for e in entities_b}
    shared  = names_a & names_b

    if not shared:
        return 0.0, ""

    denom = max(len(names_a), len(names_b), 1)
    score = min(len(shared) / denom, 1.0)
    explanation = f"Shared entities: {', '.join(sorted(shared)[:5])}"
    return round(score, 4), explanation


def _score_shared_tags(
    memory_a: Memory,
    memory_b: Memory,
) -> tuple[float, str]:
    """
    Jaccard similarity over the tags arrays stored in memory.tags (JSONB list).
    """
    tags_a = set(memory_a.tags or [])
    tags_b = set(memory_b.tags or [])
    union  = tags_a | tags_b

    if not union:
        return 0.0, ""

    shared  = tags_a & tags_b
    if not shared:
        return 0.0, ""

    score = round(len(shared) / len(union), 4)
    explanation = f"Shared tags: {', '.join(sorted(shared)[:5])}"
    return score, explanation


# ─────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────

def compute_relationships_for_memory(
    db: Session,
    memory_id: UUID,
    min_score: float = 0.1,
) -> list[Relationship]:
    """
    Compare *memory_id* against every other Memory in the DB and persist
    any Relationship that scores above *min_score*.

    Returns the list of Relationship objects (committed to the session).
    """
    target_memory: Optional[Memory] = db.get(Memory, memory_id)
    if not target_memory:
        raise ValueError(f"Memory {memory_id} not found")

    target_entities: list[Entity] = (
        db.query(Entity).filter(Entity.memory_id == memory_id).all()
    )

    # Load all OTHER memories
    other_memories: list[Memory] = (
        db.query(Memory).filter(Memory.id != memory_id).all()
    )

    created: list[Relationship] = []

    for other in other_memories:
        other_entities = (
            db.query(Entity).filter(Entity.memory_id == other.id).all()
        )

        # 1. Shared entities
        ent_score, ent_expl = _score_shared_entities(
            target_memory, other, target_entities, other_entities
        )
        if ent_score >= min_score:
            rel = _upsert_relationship(
                db,
                source_id=memory_id,
                target_id=other.id,
                rel_type=RelationshipType.SHARED_ENTITY,
                score=ent_score,
                explanation=ent_expl,
            )
            created.append(rel)

        # 2. Shared tags
        tag_score, tag_expl = _score_shared_tags(target_memory, other)
        if tag_score >= min_score:
            rel = _upsert_relationship(
                db,
                source_id=memory_id,
                target_id=other.id,
                rel_type=RelationshipType.SHARED_TAG,
                score=tag_score,
                explanation=tag_expl,
            )
            created.append(rel)

    db.commit()
    logger.info(
        "compute_relationships_for_memory: memory=%s → %d relationships",
        memory_id, len(created),
    )
    return created


def get_related_memories(
    db: Session,
    memory_id: UUID,
    limit: int = 10,
) -> list[dict]:
    """
    Return the top *limit* related memories for *memory_id*,
    ordered by descending score.

    Returns a list of dicts:
        {memory_id, title, score, rel_type, explanation}
    """
    uid = str(memory_id)

    rows = (
        db.query(Relationship)
        .filter(
            (Relationship.source_id == memory_id) |
            (Relationship.target_id == memory_id)
        )
        .order_by(Relationship.score.desc())
        .limit(limit)
        .all()
    )

    results = []
    for row in rows:
        other_id = row.target_id if str(row.source_id) == uid else row.source_id
        other_memory: Optional[Memory] = db.get(Memory, other_id)
        results.append({
            "memory_id":   str(other_id),
            "title":       other_memory.title if other_memory else None,
            "score":       row.score,
            "rel_type":    row.rel_type,
            "explanation": row.explanation,
        })

    return results
