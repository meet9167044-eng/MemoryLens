"""
Unit Tests for Phase 9 - Relationship Engine
---------------------------------------------
All tests use in-memory SQLite via a real SQLAlchemy session.
No database server required to run these tests.
"""
import uuid
import sys
import os
import pytest

# Adjust path so tests can find backend modules when run from the backend/ dir
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.memory import Memory
from app.models.entity import Entity, EntityType
from app.models.relationship import Relationship, RelationshipType
from app.processing.relationships import (
    compute_relationships_for_memory,
    get_related_memories,
    _ordered_ids,
    _score_shared_entities,
    _score_shared_tags,
)


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture(scope="function")
def db():
    """In-memory SQLite session — fresh for every test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


from app.models.screenshot import Screenshot

def _make_memory(db, title="Test", tags=None, entities=None) -> Memory:
    """Helper: create & persist a Memory with optional tags and entities."""
    scr = Screenshot(
        id=uuid.uuid4(),
        file_path="/tmp/dummy.jpg",
        original_filename="dummy.jpg"
    )
    db.add(scr)
    db.flush()

    mem = Memory(
        id=uuid.uuid4(),
        screenshot_id=scr.id,
        title=title,
        tags=tags or [],
        raw_ocr_text="",
        content_type="screenshot",
    )
    db.add(mem)
    db.flush()

    for name, etype in (entities or []):
        ent = Entity(
            id=uuid.uuid4(),
            memory_id=mem.id,
            name=name,
            entity_type=etype,
        )
        db.add(ent)
    db.commit()
    return mem


# ─────────────────────────────────────────────
# Unit tests for scoring helpers
# ─────────────────────────────────────────────

def test_ordered_ids_always_smaller_first():
    """_ordered_ids should return (smaller, larger) regardless of argument order."""
    a = uuid.UUID("00000000-0000-0000-0000-000000000001")
    b = uuid.UUID("00000000-0000-0000-0000-000000000002")
    assert _ordered_ids(a, b) == (a, b)
    assert _ordered_ids(b, a) == (a, b)


def test_score_shared_entities_no_overlap():
    mem_a = Memory(id=uuid.uuid4(), tags=[], title="A")
    mem_b = Memory(id=uuid.uuid4(), tags=[], title="B")
    ents_a = [Entity(id=uuid.uuid4(), memory_id=mem_a.id, name="CUDA", entity_type=EntityType.TECHNOLOGY)]
    ents_b = [Entity(id=uuid.uuid4(), memory_id=mem_b.id, name="Python", entity_type=EntityType.TECHNOLOGY)]
    score, expl = _score_shared_entities(mem_a, mem_b, ents_a, ents_b)
    assert score == 0.0
    assert expl == ""


def test_score_shared_entities_full_overlap():
    mem_a = Memory(id=uuid.uuid4(), tags=[], title="A")
    mem_b = Memory(id=uuid.uuid4(), tags=[], title="B")
    ents = [
        Entity(id=uuid.uuid4(), memory_id=mem_a.id, name="CUDA", entity_type=EntityType.TECHNOLOGY),
    ]
    score, expl = _score_shared_entities(mem_a, mem_b, ents, ents)
    assert score == 1.0
    assert "CUDA" in expl.lower() or "cuda" in expl.lower()


def test_score_shared_tags_identical():
    mem_a = Memory(id=uuid.uuid4(), tags=["error", "gpu"], title="A")
    mem_b = Memory(id=uuid.uuid4(), tags=["error", "gpu"], title="B")
    score, expl = _score_shared_tags(mem_a, mem_b)
    assert score == 1.0


def test_score_shared_tags_no_overlap():
    mem_a = Memory(id=uuid.uuid4(), tags=["apple"], title="A")
    mem_b = Memory(id=uuid.uuid4(), tags=["banana"], title="B")
    score, expl = _score_shared_tags(mem_a, mem_b)
    assert score == 0.0


def test_score_shared_tags_empty():
    mem_a = Memory(id=uuid.uuid4(), tags=[], title="A")
    mem_b = Memory(id=uuid.uuid4(), tags=[], title="B")
    score, expl = _score_shared_tags(mem_a, mem_b)
    assert score == 0.0


# ─────────────────────────────────────────────
# Integration tests (SQLite in-memory)
# ─────────────────────────────────────────────

def test_shared_entity_produces_relationship(db):
    """
    Two memories sharing the 'CUDA' entity should generate a SHARED_ENTITY relationship.
    This is the acceptance criterion from the Phase 9 spec.
    """
    mem_1 = _make_memory(db, title="mem_1827", tags=[],
                         entities=[("CUDA", EntityType.TECHNOLOGY)])
    mem_2 = _make_memory(db, title="mem_1842", tags=[],
                         entities=[("CUDA", EntityType.TECHNOLOGY)])

    rels = compute_relationships_for_memory(db, memory_id=mem_1.id)

    entity_rels = [r for r in rels if r.rel_type == RelationshipType.SHARED_ENTITY]
    assert len(entity_rels) >= 1
    assert entity_rels[0].score > 0.0
    assert "CUDA" in (entity_rels[0].explanation or "").upper()


def test_identical_tags_produce_strong_relationship(db):
    """Memories with identical tags should score 1.0 on SHARED_TAG."""
    mem_a = _make_memory(db, title="A", tags=["gpu", "error"])
    mem_b = _make_memory(db, title="B", tags=["gpu", "error"])

    rels = compute_relationships_for_memory(db, memory_id=mem_a.id)
    tag_rels = [r for r in rels if r.rel_type == RelationshipType.SHARED_TAG]

    assert len(tag_rels) >= 1
    assert tag_rels[0].score == 1.0


def test_no_duplicate_undirected_rows(db):
    """
    Computing relationships twice must not create duplicate rows —
    only upsert with a higher score.
    """
    mem_a = _make_memory(db, title="A", tags=["shared"])
    mem_b = _make_memory(db, title="B", tags=["shared"])

    compute_relationships_for_memory(db, memory_id=mem_a.id)
    compute_relationships_for_memory(db, memory_id=mem_a.id)  # run again

    count = db.query(Relationship).count()
    # Should have exactly 1 row (SHARED_TAG between a and b)
    assert count == 1


def test_unrelated_memories_produce_no_relationship(db):
    """Memories with nothing in common should not create any relationship rows."""
    _make_memory(db, title="A", tags=["alpha"],
                 entities=[("foo", EntityType.OTHER)])
    mem_b = _make_memory(db, title="B", tags=["beta"],
                         entities=[("bar", EntityType.OTHER)])

    rels = compute_relationships_for_memory(db, memory_id=mem_b.id)
    assert len(rels) == 0


def test_get_related_memories_returns_sorted_by_score(db):
    """get_related_memories should return results ordered by score desc."""
    mem_main = _make_memory(db, title="Main", tags=["x", "y", "z"])
    _make_memory(db, title="HalfMatch", tags=["x"])
    _make_memory(db, title="FullMatch", tags=["x", "y", "z"])

    compute_relationships_for_memory(db, memory_id=mem_main.id)
    results = get_related_memories(db, memory_id=mem_main.id)

    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_compute_relationships_raises_for_missing_memory(db):
    """Engine must raise ValueError for an unknown memory_id."""
    with pytest.raises(ValueError, match="not found"):
        compute_relationships_for_memory(db, memory_id=uuid.uuid4())
