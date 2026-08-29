import uuid, enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class EntityType(str, enum.Enum):
    PERSON = "person"
    ORGANIZATION = "organization"
    TECHNOLOGY = "technology"
    FILE_PATH = "file_path"
    URL = "url"
    DATE = "date"
    LOCATION = "location"
    CODE_SYMBOL = "code_symbol"
    OTHER = "other"


class Entity(Base):
    __tablename__ = "entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    memory_id = Column(UUID(as_uuid=True), ForeignKey("memories.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(512), nullable=False)
    entity_type = Column(Enum(EntityType, name="entity_type"), nullable=False, default=EntityType.OTHER, index=True)
    value = Column(String(1024), nullable=True)
    confidence = Column(String(16), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    memory = relationship("Memory", back_populates="entities")

    def __repr__(self):
        return f"<Entity type={self.entity_type} name={self.name!r}>"
