import pytest
import os
import sys

# Ensure backend/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Must set TESTING=1 before any app import so Memory uses JSON not JSONB
os.environ.setdefault("TESTING", "1")

from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.db.session import get_db
from app.models.memory import Memory
from app.models.screenshot import Screenshot, ScreenshotStatus
from app.models.entity import Entity, EntityType
from app.models.relationship import Relationship, RelationshipType
from app.models.processing_job import ProcessingJob

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.base import Base

client = TestClient(app)

@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        "sqlite://", # default in memory
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture(autouse=True)
def override_dependency(db):
    app.dependency_overrides[get_db] = lambda: db
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def test_data(db):
    # Setup screenshot
    scr = Screenshot(
        id=uuid4(),
        file_path="/tmp/test.png",
        original_filename="test.png",
        status=ScreenshotStatus.COMPLETED
    )
    db.add(scr)
    
    # Setup memory
    mem1 = Memory(
        id=uuid4(),
        screenshot_id=scr.id,
        title="Test Memory 1",
        summary="A summary",
        raw_ocr_text="ocr text",
        content_type="screenshot",
        tags=["test", "tag"]
    )
    db.add(mem1)
    
    mem2 = Memory(
        id=uuid4(),
        screenshot_id=scr.id,
        title="Test Memory 2"
    )
    db.add(mem2)
    
    # Setup entity
    ent = Entity(
        memory_id=mem1.id,
        name="Python",
        entity_type=EntityType.TECHNOLOGY
    )
    db.add(ent)
    
    # Setup relationship
    rel = Relationship(
        source_id=mem1.id,
        target_id=mem2.id,
        rel_type=RelationshipType.SHARED_TAG,
        score=0.8
    )
    db.add(rel)
    db.commit()
    
    return mem1, mem2, scr

def test_get_memories_contract(test_data):
    response = client.get("/api/v1/memories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    
    # Check structure
    mem = data[0]
    assert "id" in mem
    assert "timestamp" in mem
    
    assert "source" in mem
    assert "app" in mem["source"]
    assert "type" in mem["source"]
    
    assert "screenshot" in mem
    assert "id" in mem["screenshot"]
    assert "imageUrl" in mem["screenshot"]
    
    assert "content" in mem
    assert "ocrText" in mem["content"]
    assert "title" in mem["content"]
    assert "summary" in mem["content"]
    
    assert "entities" in mem
    assert isinstance(mem["entities"], list)
    
    assert "tags" in mem
    assert isinstance(mem["tags"], list)
    
    assert "relatedMemories" in mem
    assert isinstance(mem["relatedMemories"], list)
    
    assert "metadata" in mem
    assert "language" in mem["metadata"]
    assert "contentType" in mem["metadata"]
    assert "confidence" in mem["metadata"]

def test_get_memory_by_id_contract(test_data):
    mem1, _, _ = test_data
    response = client.get(f"/api/v1/memories/{mem1.id}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == str(mem1.id)
    assert data["content"]["title"] == "Test Memory 1"
    assert len(data["entities"]) == 1
    assert data["entities"][0]["name"] == "Python"
    assert len(data["relatedMemories"]) == 1

def test_get_timeline_contract(test_data):
    response = client.get("/api/v1/timeline")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    
    # Check that they are ordered by timestamp descending
    if len(data) >= 2:
        t1 = data[0]["timestamp"]
        t2 = data[1]["timestamp"]
        assert t1 >= t2
